"""Structured evidence records and local retrieval for internal SportRX review.

This module is deliberately retrieval-only. It indexes approved local evidence
records but never generates training, medical, prediction, or clearance advice.
"""

from __future__ import annotations

import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any


CLAIM_BOUNDARY = (
    "SportRX Evidence Store is an internal retrieval and audit layer. It does "
    "not provide medical clearance, diagnose conditions, predict injury or race "
    "outcomes, create athlete percentiles, validate a readiness score, or change "
    "exercise dose."
)

RECORD_FILES = {
    "sources": "evidence/records/sources.json",
    "claims": "evidence/records/claims.json",
    "rules": "evidence/records/rules.json",
    "protocols": "evidence/records/protocols.json",
}
RECORD_PACK_GLOB = "evidence/records/packs/*_{lane}.json"
LANES = tuple(RECORD_FILES)
REVIEW_STATUSES = {"reviewed", "needs_revision", "candidate"}
RULE_STATUSES = {"allowed_ui", "explain_only", "internal_only", "blocked"}
COMPONENT_PROTOCOL_STATUSES = {"supported", "partial_evidence", "experimental"}
REQUIRED_MEASUREMENT_COMPONENT_IDS = {
    "1km_run",
    "6min_run_walk",
    "erg_1km",
    "station_circuit",
    "compromised_run",
}

REQUIRED_FIELDS = {
    "sources": {
        "id",
        "citation",
        "stable_url",
        "evidence_tier",
        "population",
        "access_status",
        "content_storage",
        "limitations",
        "review_status",
        "reviewed_by",
        "reviewed_at",
    },
    "claims": {
        "id",
        "statement",
        "applies_to",
        "evidence_tier",
        "source_ids",
        "allowed_language",
        "disallowed_language",
        "limitations",
        "review_status",
        "reviewed_by",
        "reviewed_at",
    },
    "rules": {
        "id",
        "module",
        "product_status",
        "input_fields",
        "output",
        "claim_ids",
        "failure_modes",
        "review_status",
        "reviewed_by",
        "reviewed_at",
    },
    "protocols": {
        "id",
        "name",
        "scope",
        "steps",
        "equipment",
        "raw_units",
        "stop_conditions",
        "rpe_capture",
        "retest_requirements",
        "claim_ids",
        "review_status",
        "reviewed_by",
        "reviewed_at",
    },
}


def _root_path(root: str | Path) -> Path:
    return Path(root).resolve()


def _read_record_file(root: Path, lane: str) -> list[dict[str, Any]]:
    path = root / RECORD_FILES[lane]
    paths = [path] if path.exists() else []
    paths.extend(sorted(root.glob(RECORD_PACK_GLOB.format(lane=lane))))
    records: list[dict[str, Any]] = []
    for record_path in paths:
        payload = json.loads(record_path.read_text(encoding="utf-8"))
        pack_records = payload.get("records", [])
        if isinstance(pack_records, list):
            records.extend(pack_records)
    return records


def load_evidence_records(root: str | Path = ".") -> dict[str, list[dict[str, Any]]]:
    """Load structured evidence records without creating an index."""

    root_path = _root_path(root)
    return {lane: _read_record_file(root_path, lane) for lane in LANES}


def _mapped_rule_ids(root: Path) -> set[str]:
    """Read canonical rule IDs from the existing human-reviewed rule map."""

    path = root / "evidence/rule_evidence_map.md"
    if not path.exists():
        return set()
    ids: set[str] = set()
    in_rules = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "## Current Rules":
            in_rules = True
            continue
        if in_rules and line.startswith("## "):
            break
        if not in_rules or not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if cells and cells[0] not in {"Rule ID", "---"} and re.fullmatch(r"[A-Z]+-\d+", cells[0] or ""):
            ids.add(cells[0])
    return ids


def _missing_fields(record: dict[str, Any], required: set[str]) -> list[str]:
    return sorted(field for field in required if field not in record or record[field] in (None, "", []))


def _duplicate_ids(records: list[dict[str, Any]]) -> set[str]:
    counts: dict[str, int] = defaultdict(int)
    for record in records:
        counts[str(record.get("id", ""))] += 1
    return {record_id for record_id, count in counts.items() if record_id and count > 1}


def validate_evidence_records(root: str | Path = ".") -> dict[str, Any]:
    """Validate local evidence links and return a review-ready audit result."""

    root_path = _root_path(root)
    records = load_evidence_records(root_path)
    errors: list[str] = []
    warnings: list[str] = []

    for lane in LANES:
        path = root_path / RECORD_FILES[lane]
        if not path.exists():
            errors.append(f"missing record file: {RECORD_FILES[lane]}")
            continue
        for duplicate_id in sorted(_duplicate_ids(records[lane])):
            errors.append(f"duplicate {lane} id: {duplicate_id}")
        for record in records[lane]:
            record_id = record.get("id", "<missing id>")
            missing = _missing_fields(record, REQUIRED_FIELDS[lane])
            if missing:
                errors.append(f"{lane}:{record_id} missing required fields: {', '.join(missing)}")
            if record.get("review_status") not in REVIEW_STATUSES:
                errors.append(f"{lane}:{record_id} has invalid review_status")

    sources_by_id = {record.get("id"): record for record in records["sources"]}
    claims_by_id = {record.get("id"): record for record in records["claims"]}
    rules_by_id = {record.get("id"): record for record in records["rules"]}

    for source_id, source in sources_by_id.items():
        if source_id and not str(source.get("stable_url", "")).startswith("https://"):
            errors.append(f"sources:{source_id} must use an https stable_url")
        if source.get("content_storage") != "metadata_only":
            errors.append(f"sources:{source_id} must not store source full text in the public evidence store")

    identifiers: dict[tuple[str, str], str] = {}
    for source_id, source in sources_by_id.items():
        for identifier_type, value in source.get("identifiers", {}).items():
            normalized = str(value).strip().casefold()
            if not normalized:
                continue
            key = (str(identifier_type).strip().casefold(), normalized)
            if key in identifiers:
                errors.append(
                    f"sources:{source_id} duplicates {identifier_type} from {identifiers[key]}"
                )
            identifiers[key] = str(source_id)

    for claim_id, claim in claims_by_id.items():
        for source_id in claim.get("source_ids", []):
            if source_id not in sources_by_id:
                errors.append(f"claims:{claim_id} references unknown source: {source_id}")
        if not claim.get("allowed_language") or not claim.get("disallowed_language"):
            errors.append(f"claims:{claim_id} needs allowed and disallowed language")

    for rule_id, rule in rules_by_id.items():
        if rule.get("product_status") not in RULE_STATUSES:
            errors.append(f"rules:{rule_id} has invalid product_status")
        claim_ids = rule.get("claim_ids", [])
        for claim_id in claim_ids:
            if claim_id not in claims_by_id:
                errors.append(f"rules:{rule_id} references unknown claim: {claim_id}")
        if rule.get("product_status") == "allowed_ui":
            if not claim_ids:
                errors.append(f"rules:{rule_id} allowed_ui rule has no claim link")
            for claim_id in claim_ids:
                claim = claims_by_id.get(claim_id, {})
                if claim.get("review_status") != "reviewed":
                    errors.append(f"rules:{rule_id} allowed_ui rule links unreviewed claim: {claim_id}")
                if not claim.get("source_ids"):
                    errors.append(f"rules:{rule_id} allowed_ui rule has claim without sources: {claim_id}")

    for protocol in records["protocols"]:
        protocol_id = protocol.get("id", "<missing id>")
        for claim_id in protocol.get("claim_ids", []):
            if claim_id not in claims_by_id:
                errors.append(f"protocols:{protocol_id} references unknown claim: {claim_id}")
        component_id = protocol.get("measurement_component_id")
        if component_id:
            status = protocol.get("protocol_evidence_status")
            if status not in COMPONENT_PROTOCOL_STATUSES:
                errors.append(f"protocols:{protocol_id} has invalid protocol_evidence_status")
            for field in ("standardization_fields", "limitations"):
                if not protocol.get(field):
                    errors.append(f"protocols:{protocol_id} component protocol missing {field}")
            if not protocol.get("claim_ids"):
                errors.append(f"protocols:{protocol_id} component protocol has no claim link")

    component_protocols = [
        protocol for protocol in records["protocols"] if protocol.get("measurement_component_id")
    ]
    component_ids = [protocol.get("measurement_component_id") for protocol in component_protocols]
    for component_id in sorted(REQUIRED_MEASUREMENT_COMPONENT_IDS - set(component_ids)):
        errors.append(f"missing component protocol evidence record: {component_id}")
    for component_id in sorted({item for item in component_ids if component_ids.count(item) > 1}):
        errors.append(f"duplicate component protocol evidence record: {component_id}")

    mapped_rule_ids = _mapped_rule_ids(root_path)
    missing_rule_records = sorted(mapped_rule_ids - set(rules_by_id))
    if missing_rule_records:
        errors.append(f"missing structured rule records: {', '.join(missing_rule_records)}")
    extra_rule_records = sorted(set(rules_by_id) - mapped_rule_ids)
    if extra_rule_records:
        warnings.append(f"structured rules not yet listed in rule map: {', '.join(extra_rule_records)}")

    counts = {lane: len(records[lane]) for lane in LANES}
    return {
        "schema": "sportrx.evidence_validation",
        "schema_version": "0.1",
        "status": "ready_for_internal_retrieval" if not errors else "needs_evidence_review",
        "valid": not errors,
        "counts": counts,
        "errors": errors,
        "warnings": warnings,
        "mapped_rule_count": len(mapped_rule_ids),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_protocol_evidence_ledger(root: str | Path = ".") -> dict[str, Any]:
    """Return a review-ready component evidence ledger without source full text."""

    records = load_evidence_records(root)
    claims_by_id = {record["id"]: record for record in records["claims"]}
    sources_by_id = {record["id"]: record for record in records["sources"]}
    components = []
    for protocol in records["protocols"]:
        component_id = protocol.get("measurement_component_id")
        if not component_id:
            continue
        claim_ids = list(protocol.get("claim_ids", []))
        source_ids = sorted(
            {
                source_id
                for claim_id in claim_ids
                for source_id in claims_by_id.get(claim_id, {}).get("source_ids", [])
            }
        )
        components.append(
            {
                "component_id": component_id,
                "protocol_id": protocol["id"],
                "name": protocol["name"],
                "evidence_status": protocol["protocol_evidence_status"],
                "standardization_fields": protocol["standardization_fields"],
                "limitations": protocol["limitations"],
                "claim_ids": claim_ids,
                "sources": [
                    {"id": source_id, "citation": sources_by_id[source_id]["citation"], "stable_url": sources_by_id[source_id]["stable_url"]}
                    for source_id in source_ids
                    if source_id in sources_by_id
                ],
            }
        )
    return {
        "schema": "sportrx.protocol_evidence_ledger",
        "schema_version": "0.1",
        "components": sorted(components, key=lambda item: item["component_id"]),
        "claim_boundary": "The ledger documents evidence status and limits. It does not validate SportRX scores, norms, injury risk, medical clearance, or race prediction.",
    }


def _text(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {_text(item)}" for key, item in value.items())
    return str(value)


def _title(lane: str, record: dict[str, Any]) -> str:
    if lane == "sources":
        return f"{record['id']} - {record['citation']}"
    if lane == "claims":
        return f"{record['id']} - {record['statement']}"
    if lane == "rules":
        return f"{record['id']} - {record['output']}"
    return f"{record['id']} - {record['name']}"


def build_evidence_corpus(root: str | Path = ".") -> list[dict[str, Any]]:
    """Compile reviewed records into retrieval documents without raw source text."""

    records = load_evidence_records(root)
    corpus: list[dict[str, Any]] = []
    for lane in LANES:
        for record in records[lane]:
            corpus.append(
                {
                    "lane": lane,
                    "record_id": record["id"],
                    "title": _title(lane, record),
                    "content": _text(record),
                    "payload": record,
                }
            )
    return corpus


def _default_index_path(root: Path) -> Path:
    return root / ".cache" / "sportrx_evidence.sqlite"


def build_evidence_index(root: str | Path = ".", db_path: str | Path | None = None) -> dict[str, Any]:
    """Build a local SQLite FTS5 index from the approved structured records."""

    root_path = _root_path(root)
    validation = validate_evidence_records(root_path)
    if not validation["valid"]:
        raise ValueError("Cannot index invalid evidence records: " + "; ".join(validation["errors"]))

    index_path = Path(db_path) if db_path is not None else _default_index_path(root_path)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    corpus = build_evidence_corpus(root_path)
    with sqlite3.connect(index_path) as connection:
        connection.execute("DROP TABLE IF EXISTS evidence_documents")
        connection.execute("DROP TABLE IF EXISTS evidence_fts")
        connection.execute(
            "CREATE TABLE evidence_documents (record_id TEXT PRIMARY KEY, lane TEXT NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL, payload_json TEXT NOT NULL)"
        )
        connection.execute("CREATE VIRTUAL TABLE evidence_fts USING fts5(record_id UNINDEXED, lane UNINDEXED, title, content)")
        for document in corpus:
            payload_json = json.dumps(document["payload"], ensure_ascii=False, sort_keys=True)
            connection.execute(
                "INSERT INTO evidence_documents VALUES (?, ?, ?, ?, ?)",
                (document["record_id"], document["lane"], document["title"], document["content"], payload_json),
            )
            connection.execute(
                "INSERT INTO evidence_fts VALUES (?, ?, ?, ?)",
                (document["record_id"], document["lane"], document["title"], document["content"]),
            )
    return {
        "schema": "sportrx.evidence_index",
        "schema_version": "0.1",
        "status": "ready",
        "path": str(index_path),
        "document_count": len(corpus),
        "lane_counts": {lane: sum(1 for document in corpus if document["lane"] == lane) for lane in LANES},
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _query_tokens(query: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_-]+|[\u4e00-\u9fff]+", query.casefold())


def _source_ids_for_document(document: dict[str, Any], claims_by_id: dict[str, dict[str, Any]]) -> list[str]:
    payload = document["payload"]
    if document["lane"] == "sources":
        return [payload["id"]]
    if document["lane"] == "claims":
        return list(payload.get("source_ids", []))
    source_ids: list[str] = []
    for claim_id in payload.get("claim_ids", []):
        source_ids.extend(claims_by_id.get(claim_id, {}).get("source_ids", []))
    return list(dict.fromkeys(source_ids))


def _limits_for_document(document: dict[str, Any], claims_by_id: dict[str, dict[str, Any]]) -> list[str]:
    payload = document["payload"]
    limits = [payload["limitations"]] if payload.get("limitations") else []
    for claim_id in payload.get("claim_ids", []):
        limit = claims_by_id.get(claim_id, {}).get("limitations")
        if limit:
            limits.append(limit)
    return list(dict.fromkeys(limits))


def _score_document(document: dict[str, Any], query: str, tokens: list[str]) -> float:
    record_id = document["record_id"].casefold()
    title = document["title"].casefold()
    content = document["content"].casefold()
    normalized = query.casefold().strip()
    score = 0.0
    if normalized == record_id:
        score += 100.0
    elif normalized and normalized in record_id:
        score += 60.0
    if normalized and normalized in title:
        score += 30.0
    elif normalized and normalized in content:
        score += 18.0
    for token in tokens:
        if token == record_id:
            score += 50.0
        elif token in title:
            score += 8.0
        elif token in content:
            score += 3.0
    return score


def search_evidence(
    query: str,
    lane: str | None = None,
    root: str | Path = ".",
    limit: int = 8,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """Search approved evidence records by lane, ID, topic, or phrase.

    Results are records and boundaries only, never generated recommendations.
    """

    if lane is not None and lane not in LANES:
        raise ValueError(f"lane must be one of: {', '.join(LANES)}")
    if not query or not query.strip():
        raise ValueError("query must not be empty")

    root_path = _root_path(root)
    index = build_evidence_index(root_path, db_path)
    records = load_evidence_records(root_path)
    claims_by_id = {record["id"]: record for record in records["claims"]}
    documents = build_evidence_corpus(root_path)
    if lane is not None:
        documents = [document for document in documents if document["lane"] == lane]
    tokens = _query_tokens(query)
    ranked = sorted(
        ((document, _score_document(document, query, tokens)) for document in documents),
        key=lambda item: (-item[1], item[0]["record_id"]),
    )
    results = []
    for document, score in ranked:
        if score <= 0:
            continue
        results.append(
            {
                "lane": document["lane"],
                "id": document["record_id"],
                "title": document["title"],
                "score": round(score, 2),
                "source_ids": _source_ids_for_document(document, claims_by_id),
                "limitations": _limits_for_document(document, claims_by_id),
                "record": document["payload"],
            }
        )
        if len(results) >= limit:
            break
    return {
        "schema": "sportrx.evidence_search",
        "schema_version": "0.1",
        "query": query,
        "lane": lane,
        "index_path": index["path"],
        "result_count": len(results),
        "results": results,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def trace_rule(rule_id: str, root: str | Path = ".") -> dict[str, Any]:
    """Return an auditable rule-to-claim-to-source trace for internal review."""

    records = load_evidence_records(root)
    rule = next((item for item in records["rules"] if item["id"] == rule_id), None)
    if rule is None:
        return {
            "schema": "sportrx.rule_trace",
            "schema_version": "0.1",
            "status": "not_found",
            "rule_id": rule_id,
            "claims": [],
            "sources": [],
            "claim_boundary": CLAIM_BOUNDARY,
        }
    claims_by_id = {item["id"]: item for item in records["claims"]}
    sources_by_id = {item["id"]: item for item in records["sources"]}
    claims = [claims_by_id[claim_id] for claim_id in rule["claim_ids"] if claim_id in claims_by_id]
    source_ids = list(dict.fromkeys(source_id for claim in claims for source_id in claim["source_ids"]))
    sources = [sources_by_id[source_id] for source_id in source_ids if source_id in sources_by_id]
    return {
        "schema": "sportrx.rule_trace",
        "schema_version": "0.1",
        "status": "ready",
        "rule_id": rule_id,
        "rule": rule,
        "claims": claims,
        "sources": sources,
        "limitations": list(dict.fromkeys(claim["limitations"] for claim in claims)),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def evaluate_retrieval_set(
    root: str | Path = ".",
    evaluation_path: str | Path = "evidence/evaluation/retrieval_set.json",
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """Run the curated internal retrieval checks against structured records."""

    root_path = _root_path(root)
    path = Path(evaluation_path)
    path = path if path.is_absolute() else root_path / path
    records = json.loads(path.read_text(encoding="utf-8")).get("records", [])
    failures: list[dict[str, Any]] = []
    for item in records:
        result = search_evidence(
            item["query"],
            lane=item["lane"],
            root=root_path,
            limit=1,
            db_path=db_path,
        )
        actual_id = result["results"][0]["id"] if result["results"] else None
        if actual_id != item["expected_id"]:
            failures.append({"id": item["id"], "expected_id": item["expected_id"], "actual_id": actual_id})
    return {
        "schema": "sportrx.evidence_retrieval_evaluation_result",
        "schema_version": "0.1",
        "status": "passed" if not failures else "failed",
        "query_count": len(records),
        "failure_count": len(failures),
        "failures": failures,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def evaluate_unsafe_query_set(
    root: str | Path = ".",
    evaluation_path: str | Path = "evidence/evaluation/unsafe_queries.json",
) -> dict[str, Any]:
    """Check that unsafe prompts map to an explicit boundary rule and claim.

    This is not an answer generator. It verifies that a future explanation layer
    has a documented route to a bounded, non-prescriptive response.
    """

    root_path = _root_path(root)
    path = Path(evaluation_path)
    path = path if path.is_absolute() else root_path / path
    records = json.loads(path.read_text(encoding="utf-8")).get("records", [])
    failures: list[dict[str, Any]] = []
    for item in records:
        trace = trace_rule(item["expected_rule_id"], root_path)
        claim_ids = {claim["id"] for claim in trace.get("claims", [])}
        if trace["status"] != "ready" or item["expected_claim_id"] not in claim_ids:
            failures.append(
                {
                    "id": item["id"],
                    "expected_rule_id": item["expected_rule_id"],
                    "expected_claim_id": item["expected_claim_id"],
                }
            )
    return {
        "schema": "sportrx.evidence_unsafe_query_evaluation_result",
        "schema_version": "0.1",
        "status": "passed" if not failures else "failed",
        "query_count": len(records),
        "failure_count": len(failures),
        "failures": failures,
        "claim_boundary": CLAIM_BOUNDARY,
    }
