"""Internal SportRX knowledge-corpus retrieval and constrained synthesis.

This module is intentionally separate from ``evidence_store``. Knowledge cards
teach sport-science concepts; they cannot change SportRX safety, measurement,
prescription, or progression rules.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any

from .evidence_store import load_evidence_records


CARD_PATH = "evidence/knowledge/cards.json"
CANDIDATE_PATH = "evidence/knowledge/candidates.json"
RETRIEVAL_EVALUATION_PATH = "evidence/knowledge/evaluation/retrieval_set.json"
BOUNDARY_EVALUATION_PATH = "evidence/knowledge/evaluation/boundary_set.json"
ANSWER_EVALUATION_PATH = "evidence/knowledge/evaluation/answer_quality_set.json"
INDEX_PATH = ".cache/sportrx_knowledge.sqlite"
EMBEDDING_PATH = ".cache/sportrx_knowledge_embeddings.json"
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
KNOWLEDGE_TOPICS = (
    "training_principles",
    "endurance",
    "strength_power",
    "hiit_hift_hybrid",
    "testing",
    "monitoring_recovery",
    "biomechanics_motor_control",
    "environmental_physiology",
    "nutrition_supplements",
    "sports_medicine_injury_rehab",
)
ACCESS_TIERS = {"public_metadata", "open_access_private", "licensed_private"}
REVIEW_STATUSES = {"candidate", "reviewed", "rejected", "needs_revision"}
QUESTION_POLICIES = {"education", "research_only"}
TARGET_CARD_COUNT = 300
MINIMUM_SYNTHESIS_CARD_COUNT = 60
MINIMUM_RETRIEVAL_EVALUATIONS = 150
MINIMUM_BOUNDARY_EVALUATIONS = 50
MINIMUM_ANSWER_EVALUATIONS = 60

CLAIM_BOUNDARY = (
    "SportRX Knowledge RAG is an internal research explanation layer. It does "
    "not make medical diagnoses, provide clearance, estimate injury risk, predict "
    "race outcomes, create percentiles, or change Safety Gate, measurement, "
    "training-dose, or progression rules."
)
CLINICAL_BOUNDARY = (
    "Research summary only. It is not diagnosis, rehabilitation guidance, medical "
    "clearance, or a personalised recommendation."
)

REQUIRED_CARD_FIELDS = {
    "id",
    "topic",
    "subtopic",
    "title_en",
    "title_zh",
    "keywords_en",
    "keywords_zh",
    "source_ids",
    "evidence_tier",
    "population",
    "summary_zh",
    "technical_summary_en",
    "limitations",
    "review_status",
    "reviewed_by",
    "reviewed_at",
    "access_tier",
    "question_policy",
}


def _root(root: str | Path) -> Path:
    return Path(root).resolve()


def _load_json(root: Path, relative_path: str) -> list[dict[str, Any]]:
    path = root / relative_path
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    return records if isinstance(records, list) else []


def load_knowledge_cards(root: str | Path = ".") -> list[dict[str, Any]]:
    """Load public card metadata and summaries, never private source files."""

    return _load_json(_root(root), CARD_PATH)


def load_knowledge_candidates(root: str | Path = ".") -> list[dict[str, Any]]:
    """Load discovery candidates that are deliberately excluded from retrieval."""

    return _load_json(_root(root), CANDIDATE_PATH)


def _load_evaluation(root: Path, relative_path: str) -> list[dict[str, Any]]:
    return _load_json(root, relative_path)


def _missing(record: dict[str, Any], fields: set[str]) -> list[str]:
    return sorted(field for field in fields if record.get(field) in (None, "", []))


def validate_knowledge_records(root: str | Path = ".") -> dict[str, Any]:
    """Validate the knowledge corpus without promoting candidates to reviewed."""

    root_path = _root(root)
    cards = load_knowledge_cards(root_path)
    candidates = load_knowledge_candidates(root_path)
    source_ids = {item["id"] for item in load_evidence_records(root_path)["sources"]}
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    for card in cards:
        card_id = str(card.get("id", "<missing id>"))
        if card_id in seen:
            errors.append(f"duplicate knowledge card id: {card_id}")
        seen.add(card_id)
        missing = _missing(card, REQUIRED_CARD_FIELDS)
        if missing:
            errors.append(f"knowledge card {card_id} missing: {', '.join(missing)}")
        if card.get("topic") not in KNOWLEDGE_TOPICS:
            errors.append(f"knowledge card {card_id} has invalid topic")
        if card.get("access_tier") not in ACCESS_TIERS:
            errors.append(f"knowledge card {card_id} has invalid access_tier")
        if card.get("review_status") not in REVIEW_STATUSES:
            errors.append(f"knowledge card {card_id} has invalid review_status")
        if card.get("question_policy") not in QUESTION_POLICIES:
            errors.append(f"knowledge card {card_id} has invalid question_policy")
        for source_id in card.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"knowledge card {card_id} references unknown source: {source_id}")
        if "evidence/private" in _card_text(card).lower():
            errors.append(f"knowledge card {card_id} leaks a private path")

    candidate_keys: set[tuple[str, str]] = set()
    for candidate in candidates:
        title = _normalise_title(candidate.get("title", ""))
        key = (str(candidate.get("doi", "")).lower(), title)
        if key in candidate_keys:
            errors.append("duplicate knowledge candidate by DOI/title")
        candidate_keys.add(key)
        if candidate.get("review_status") != "candidate":
            errors.append(f"knowledge candidate {candidate.get('id', '<missing id>')} is not candidate status")
        if candidate.get("topic") not in KNOWLEDGE_TOPICS:
            errors.append(f"knowledge candidate {candidate.get('id', '<missing id>')} has invalid topic")

    approved = [card for card in cards if card.get("review_status") == "reviewed"]
    covered_topics = sorted({card["topic"] for card in approved if card.get("topic") in KNOWLEDGE_TOPICS})
    if len(approved) < MINIMUM_SYNTHESIS_CARD_COUNT:
        warnings.append(f"synthesis remains disabled until {MINIMUM_SYNTHESIS_CARD_COUNT} reviewed cards are available")
    if len(approved) < TARGET_CARD_COUNT:
        warnings.append(f"v1 target is {TARGET_CARD_COUNT} reviewed cards; current reviewed count is {len(approved)}")
    return {
        "schema": "sportrx.knowledge_validation",
        "schema_version": "0.1",
        "valid": not errors,
        "status": "ready_for_internal_research" if not errors else "needs_knowledge_review",
        "card_count": len(cards),
        "reviewed_card_count": len(approved),
        "candidate_count": len(candidates),
        "covered_topics": covered_topics,
        "errors": errors,
        "warnings": warnings,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _card_text(card: dict[str, Any]) -> str:
    values = [
        card.get("id", ""), card.get("topic", ""), card.get("subtopic", ""),
        card.get("title_en", ""), card.get("title_zh", ""), card.get("keywords_en", []),
        card.get("keywords_zh", []), card.get("population", ""), card.get("summary_zh", ""),
        card.get("technical_summary_en", ""), card.get("limitations", ""), card.get("source_ids", []),
    ]
    return " ".join(" ".join(value) if isinstance(value, list) else str(value) for value in values)


def _normalise_title(value: str) -> str:
    return re.sub(r"\W+", " ", value.casefold()).strip()


def _tokenise(value: str) -> list[str]:
    english = re.findall(r"[a-z0-9][a-z0-9_-]*", value.casefold())
    chinese = re.findall(r"[\u4e00-\u9fff]{2,}", value)
    return english + chinese


def build_knowledge_index(root: str | Path = ".", db_path: str | Path | None = None) -> dict[str, Any]:
    """Build local FTS5 retrieval over approved cards only."""

    root_path = _root(root)
    output = Path(db_path) if db_path else root_path / INDEX_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    approved = [card for card in load_knowledge_cards(root_path) if card.get("review_status") == "reviewed"]
    with sqlite3.connect(output) as connection:
        connection.execute("DROP TABLE IF EXISTS knowledge_cards")
        connection.execute("DROP TABLE IF EXISTS knowledge_fts")
        connection.execute("CREATE TABLE knowledge_cards (card_id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
        connection.execute("CREATE VIRTUAL TABLE knowledge_fts USING fts5(card_id UNINDEXED, content)")
        for card in approved:
            content = _card_text(card)
            connection.execute("INSERT INTO knowledge_cards VALUES (?, ?)", (card["id"], json.dumps(card, ensure_ascii=False)))
            connection.execute("INSERT INTO knowledge_fts VALUES (?, ?)", (card["id"], content))
    return {
        "schema": "sportrx.knowledge_index",
        "schema_version": "0.1",
        "status": "ready" if approved else "no_reviewed_cards",
        "document_count": len(approved),
        "semantic_status": "optional_sentence_transformers_not_compiled",
        "db_path": str(output),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def compile_knowledge_embeddings(
    root: str | Path = ".",
    embedding_path: str | Path | None = None,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> dict[str, Any]:
    """Compile local multilingual embeddings for approved cards only.

    The model is optional and runs locally. It is never sent to DeepSeek and is
    intentionally absent from the default lightweight application install.
    """

    root_path = _root(root)
    output = Path(embedding_path) if embedding_path else root_path / EMBEDDING_PATH
    approved = [card for card in load_knowledge_cards(root_path) if card.get("review_status") == "reviewed"]
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        return {"schema": "sportrx.knowledge_embeddings", "status": "dependency_missing", "model_name": model_name, "document_count": len(approved), "claim_boundary": CLAIM_BOUNDARY}
    model = SentenceTransformer(model_name)
    vectors = model.encode([_card_text(card) for card in approved], normalize_embeddings=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"model_name": model_name, "records": [{"card_id": card["id"], "vector": vector.tolist()} for card, vector in zip(approved, vectors)]}), encoding="utf-8")
    return {"schema": "sportrx.knowledge_embeddings", "status": "ready", "model_name": model_name, "document_count": len(approved), "embedding_path": str(output), "claim_boundary": CLAIM_BOUNDARY}


def _semantic_scores(query: str, root: Path) -> dict[str, float]:
    """Return local cosine similarities when a compiled optional index exists."""

    path = root / EMBEDDING_PATH
    if not path.exists():
        return {}
    try:
        from sentence_transformers import SentenceTransformer
        payload = json.loads(path.read_text(encoding="utf-8"))
        model = SentenceTransformer(payload["model_name"])
        query_vector = model.encode([query], normalize_embeddings=True)[0].tolist()
        return {
            item["card_id"]: sum(left * right for left, right in zip(query_vector, item["vector"]))
            for item in payload.get("records", [])
        }
    except (ImportError, KeyError, OSError, ValueError, TypeError):
        return {}


def _source_metadata(
    source_ids: list[str], source_records: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Expose reviewable source metadata only, never local full-text paths."""

    return [
        {
            "id": source_id,
            "citation": source_records[source_id]["citation"],
            "stable_url": source_records[source_id]["stable_url"],
            "evidence_tier": source_records[source_id]["evidence_tier"],
            "access_status": source_records[source_id]["access_status"],
            "limitations": source_records[source_id]["limitations"],
        }
        for source_id in source_ids
        if source_id in source_records
    ]


def _result_card(
    card: dict[str, Any], score: float, source_records: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    return {
        "id": card["id"],
        "topic": card["topic"],
        "subtopic": card["subtopic"],
        "title_zh": card["title_zh"],
        "title_en": card["title_en"],
        "summary_zh": card["summary_zh"],
        "evidence_tier": card["evidence_tier"],
        "population": card["population"],
        "limitations": card["limitations"],
        "source_ids": card["source_ids"],
        "sources": _source_metadata(card["source_ids"], source_records),
        "access_tier": card["access_tier"],
        "question_policy": card["question_policy"],
        "score": round(score, 4),
    }


def search_knowledge(
    query: str,
    filters: dict[str, Any] | None = None,
    root: str | Path = ".",
    limit: int = 6,
) -> dict[str, Any]:
    """Retrieve reviewed knowledge cards with deterministic bilingual ranking."""

    root_path = _root(root)
    filters = filters or {}
    cards = [card for card in load_knowledge_cards(root_path) if card.get("review_status") == "reviewed"]
    topic = filters.get("topic")
    policy = filters.get("question_policy")
    evidence_tier = filters.get("evidence_tier")
    access_tier = filters.get("access_tier")
    if topic:
        cards = [card for card in cards if card.get("topic") == topic]
    if policy:
        cards = [card for card in cards if card.get("question_policy") == policy]
    if evidence_tier:
        cards = [card for card in cards if card.get("evidence_tier") == evidence_tier]
    if access_tier:
        cards = [card for card in cards if card.get("access_tier") == access_tier]
    query_tokens = _tokenise(query)
    semantic_scores = _semantic_scores(query, root_path)
    scored: list[tuple[float, dict[str, Any]]] = []
    for card in cards:
        text = _card_text(card).casefold()
        matches = sum(1 for token in query_tokens if token in text)
        # Preserve deterministic look-up when a reviewer adds surrounding
        # terms, for example "K-CARD-015 RPE".
        query_text = query.casefold()
        identifiers = {card["id"].casefold(), *[item.casefold() for item in card["source_ids"]]}
        exact_id = 100.0 if any(identifier in query_text for identifier in identifiers) else 0.0
        title_boost = 1.5 if any(token in f"{card['title_en']} {card['title_zh']}".casefold() for token in query_tokens) else 0.0
        semantic_score = semantic_scores.get(card["id"], 0.0)
        if matches or exact_id or semantic_score > 0.15:
            scored.append((matches + exact_id + title_boost + 0.55 * semantic_score, card))
    scored.sort(key=lambda item: (-item[0], item[1]["id"]))
    source_records = {item["id"]: item for item in load_evidence_records(root_path)["sources"]}
    return {
        "schema": "sportrx.knowledge_search",
        "schema_version": "0.1",
        "status": "ready" if scored else "no_reviewed_evidence_found",
        "query": query,
        "filters": filters,
        "retrieval_mode": "hybrid_lexical_semantic" if semantic_scores else "lexical_bilingual; semantic embeddings compile locally when the optional dependency is installed",
        "results": [_result_card(card, score, source_records) for score, card in scored[:limit]],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ingest_candidates(
    candidates: list[dict[str, Any]], root: str | Path = "."
) -> dict[str, Any]:
    """Normalise and deduplicate discovery results without writing or approving them."""

    existing = load_knowledge_candidates(root)
    cards = load_knowledge_cards(root)
    known = {
        (str(item.get("doi", "")).lower(), _normalise_title(item.get("title", item.get("title_en", ""))))
        for item in [*existing, *cards]
    }
    ready: list[dict[str, Any]] = []
    duplicates: list[str] = []
    for index, candidate in enumerate(candidates, start=1):
        title = str(candidate.get("title", "")).strip()
        doi = str(candidate.get("doi", "")).strip().lower()
        key = (doi, _normalise_title(title))
        if not title or key in known:
            duplicates.append(str(candidate.get("id", index)))
            continue
        known.add(key)
        ready.append(
            {
                "id": str(candidate.get("id") or f"K-CAND-{index:04d}"),
                "title": title,
                "doi": doi or None,
                "pmid": candidate.get("pmid") or None,
                "source_url": candidate.get("source_url") or None,
                "journal": candidate.get("journal") or None,
                "year": candidate.get("year") or None,
                "topic": candidate.get("topic", "training_principles"),
                "discovery_source": candidate.get("discovery_source", "manual_import"),
                "review_status": "candidate",
            }
        )
    return {
        "schema": "sportrx.knowledge_candidate_intake",
        "schema_version": "0.1",
        "status": "review_required",
        "candidates": ready,
        "duplicate_ids": duplicates,
        "claim_boundary": "Candidate intake never approves a source, creates a knowledge card, or changes a SportRX rule.",
    }


def review_knowledge_card(
    cards: list[dict[str, Any]], card_id: str, decision: str, reviewer: str, reviewed_at: str
) -> dict[str, Any]:
    """Return a reviewed copy of a card; persistence is an explicit curator action."""

    if decision not in {"reviewed", "needs_revision", "rejected"}:
        raise ValueError("decision must be reviewed, needs_revision, or rejected")
    updated = []
    found = False
    for card in cards:
        next_card = dict(card)
        if card.get("id") == card_id:
            found = True
            next_card.update({"review_status": decision, "reviewed_by": reviewer, "reviewed_at": reviewed_at})
        updated.append(next_card)
    return {
        "schema": "sportrx.knowledge_review",
        "schema_version": "0.1",
        "status": "review_recorded" if found else "not_found",
        "cards": updated,
        "claim_boundary": "A review decision changes knowledge-card eligibility only; it cannot change SportRX product rules.",
    }


def _policy_for_query(query: str, cards: list[dict[str, Any]]) -> dict[str, Any] | None:
    text = query.casefold()
    rule_terms = ("how many minutes", "training dose", "weekly volume", "progression", "safety gate", "medical clearance")
    if any(term in text for term in rule_terms):
        return {"status": "route_to_rule_trace", "message": "This question can affect a SportRX decision and must use the deterministic rule-evidence trace instead."}
    clinical = any(card.get("question_policy") == "research_only" for card in cards)
    if clinical:
        return {"status": "research_only", "message": CLINICAL_BOUNDARY}
    return None


def synthesize_knowledge(
    query: str,
    retrieved_card_ids: list[str],
    root: str | Path = ".",
    api_key: str | None = None,
    client: Any | None = None,
) -> dict[str, Any]:
    """Create citation-bound Chinese synthesis from explicitly retrieved cards only."""

    root_path = _root(root)
    approved = [card for card in load_knowledge_cards(root_path) if card.get("review_status") == "reviewed"]
    readiness = knowledge_evaluation_status(root_path)
    if len(approved) < MINIMUM_SYNTHESIS_CARD_COUNT or not readiness["synthesis_gate_passed"]:
        return {"schema": "sportrx.knowledge_synthesis", "status": "corpus_not_ready", "answer_zh": "当前已审核知识卡不足，暂不生成综合回答。请继续完成来源审核。", "claim_boundary": CLAIM_BOUNDARY}
    selected = [card for card in approved if card["id"] in set(retrieved_card_ids)]
    if not selected:
        return {"schema": "sportrx.knowledge_synthesis", "status": "retrieval_insufficient", "answer_zh": "没有足够的已审核证据卡可用于回答这个问题。", "claim_boundary": CLAIM_BOUNDARY}
    policy = _policy_for_query(query, selected)
    if policy and policy["status"] == "route_to_rule_trace":
        return {"schema": "sportrx.knowledge_synthesis", **policy, "claim_boundary": CLAIM_BOUNDARY}

    context = [
        {key: card[key] for key in ("id", "title_en", "title_zh", "summary_zh", "evidence_tier", "limitations", "source_ids", "question_policy")}
        for card in selected
    ]
    api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if client is None and not api_key:
        return {"schema": "sportrx.knowledge_synthesis", "status": "configuration_required", "answer_zh": "已找到审核证据，但未配置 DeepSeek API Key。", "retrieval_ids": [card["id"] for card in selected], "claim_boundary": CLAIM_BOUNDARY}
    try:
        if client is None:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash"),
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are SportRX Knowledge Lab. Answer only from supplied reviewed cards. Return JSON with answer_zh, evidence_strength, cited_card_ids, cited_source_ids, limitations, boundary. Never give diagnosis, clearance, injury probability, race prediction, percentiles, or personalised training dose."},
                {"role": "user", "content": json.dumps({"question": query, "cards": context}, ensure_ascii=False)},
            ],
            stream=False,
        )
        payload = json.loads(response.choices[0].message.content)
    except Exception as exc:  # Provider errors must not fall back to invented text.
        return {"schema": "sportrx.knowledge_synthesis", "status": "provider_unavailable", "answer_zh": "知识综合服务暂时不可用；请先查看已检索到的证据卡。", "error_type": type(exc).__name__, "retrieval_ids": [card["id"] for card in selected], "claim_boundary": CLAIM_BOUNDARY}

    allowed_cards = {card["id"] for card in selected}
    allowed_sources = {source_id for card in selected for source_id in card["source_ids"]}
    cited_cards = list(payload.get("cited_card_ids", []))
    cited_sources = list(payload.get("cited_source_ids", []))
    if not payload.get("answer_zh") or not cited_cards or not cited_sources or not set(cited_cards) <= allowed_cards or not set(cited_sources) <= allowed_sources:
        return {"schema": "sportrx.knowledge_synthesis", "status": "citation_validation_failed", "answer_zh": "模型输出未能通过引用校验；请直接查看证据卡。", "retrieval_ids": [card["id"] for card in selected], "claim_boundary": CLAIM_BOUNDARY}
    return {
        "schema": "sportrx.knowledge_synthesis",
        "schema_version": "0.1",
        "status": "research_only" if policy else "ready",
        "answer_zh": str(payload["answer_zh"]),
        "evidence_strength": payload.get("evidence_strength", "not stated"),
        "cited_card_ids": cited_cards,
        "cited_source_ids": cited_sources,
        "limitations": payload.get("limitations", [card["limitations"] for card in selected]),
        "boundary": CLINICAL_BOUNDARY if policy else CLAIM_BOUNDARY,
        "retrieval_ids": [card["id"] for card in selected],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def knowledge_corpus_summary(root: str | Path = ".") -> dict[str, Any]:
    """Return internal progress without claiming that the 300-card target is met."""

    validation = validate_knowledge_records(root)
    approved = [card for card in load_knowledge_cards(root) if card.get("review_status") == "reviewed"]
    topic_counts = Counter(card["topic"] for card in approved)
    evaluations = knowledge_evaluation_status(root)
    return {
        "schema": "sportrx.knowledge_corpus_summary",
        "schema_version": "0.1",
        "status": "v1_ready" if validation["valid"] and len(approved) >= TARGET_CARD_COUNT else "foundation_in_progress",
        "reviewed_card_count": len(approved),
        "minimum_synthesis_card_count": MINIMUM_SYNTHESIS_CARD_COUNT,
        "target_card_count": TARGET_CARD_COUNT,
        "topic_counts": {topic: topic_counts.get(topic, 0) for topic in KNOWLEDGE_TOPICS},
        "synthesis_enabled": validation["valid"] and evaluations["synthesis_gate_passed"],
        "validation": validation,
        "evaluations": evaluations,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def evaluate_knowledge_retrieval_set(root: str | Path = ".") -> dict[str, Any]:
    """Run deterministic retrieval checks against reviewed knowledge cards."""

    root_path = _root(root)
    records = _load_evaluation(root_path, RETRIEVAL_EVALUATION_PATH)
    failures = []
    for item in records:
        result = search_knowledge(item["query"], root=root_path, limit=1)
        actual = result["results"][0]["id"] if result["results"] else None
        if actual != item.get("expected_card_id"):
            failures.append({"id": item.get("id"), "expected": item.get("expected_card_id"), "actual": actual})
    return {"status": "passed" if not failures else "failed", "query_count": len(records), "failures": failures, "claim_boundary": CLAIM_BOUNDARY}


def evaluate_knowledge_boundary_set(root: str | Path = ".") -> dict[str, Any]:
    """Confirm unsafe or clinical prompts receive a documented boundary route."""

    root_path = _root(root)
    cards = [card for card in load_knowledge_cards(root_path) if card.get("review_status") == "reviewed"]
    by_id = {card["id"]: card for card in cards}
    records = _load_evaluation(root_path, BOUNDARY_EVALUATION_PATH)
    failures = []
    for item in records:
        selected = [by_id[card_id] for card_id in item.get("card_ids", []) if card_id in by_id]
        policy = _policy_for_query(item["query"], selected)
        actual = policy["status"] if policy else "education"
        if actual != item.get("expected_status"):
            failures.append({"id": item.get("id"), "expected": item.get("expected_status"), "actual": actual})
    return {"status": "passed" if not failures else "failed", "query_count": len(records), "failures": failures, "claim_boundary": CLAIM_BOUNDARY}


def knowledge_evaluation_status(root: str | Path = ".") -> dict[str, Any]:
    """Report release gates without pretending an unevaluated model is ready."""

    root_path = _root(root)
    retrieval = evaluate_knowledge_retrieval_set(root_path)
    boundary = evaluate_knowledge_boundary_set(root_path)
    answer_records = _load_evaluation(root_path, ANSWER_EVALUATION_PATH)
    answer_passed = [item for item in answer_records if item.get("review_status") == "passed"]
    gate = (
        retrieval["status"] == "passed" and retrieval["query_count"] >= MINIMUM_RETRIEVAL_EVALUATIONS
        and boundary["status"] == "passed" and boundary["query_count"] >= MINIMUM_BOUNDARY_EVALUATIONS
        and len(answer_passed) >= MINIMUM_ANSWER_EVALUATIONS
        and len([card for card in load_knowledge_cards(root_path) if card.get("review_status") == "reviewed"]) >= MINIMUM_SYNTHESIS_CARD_COUNT
    )
    return {
        "retrieval": retrieval,
        "boundary": boundary,
        "answer_quality_count": len(answer_records),
        "answer_quality_passed_count": len(answer_passed),
        "synthesis_gate_passed": gate,
        "claim_boundary": CLAIM_BOUNDARY,
    }
