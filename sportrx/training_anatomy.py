"""Reviewed training-anatomy records for SportRX knowledge retrieval.

This module connects broad anatomy to the existing hypertrophy movement atlas.
It describes structures and actions, not exercise dose, diagnosis, activation
percentages, or individual suitability.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from .evidence_store import load_evidence_records
from .exercise_catalogue import load_exercise_catalogue
from .hypertrophy_atlas import load_hypertrophy_atlas


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ANATOMY_PATH = PROJECT_ROOT / "data" / "exercises" / "training_anatomy.json"

CONTENT_BOUNDARY = (
    "SportRX Training Anatomy is an educational structure-and-action reference. "
    "It does not diagnose weakness or pain, estimate muscle activation, prescribe "
    "training dose, or prove that an exercise isolates or maximizes a muscle."
)

ACTION_SEARCH_ZH = {
    "shoulder horizontal adduction": ["肩水平内收"],
    "shoulder horizontal abduction": ["肩水平外展"],
    "shoulder adduction": ["肩内收"],
    "shoulder abduction": ["肩外展"],
    "shoulder extension": ["肩伸", "肩伸展"],
    "shoulder flexion": ["肩屈", "肩屈曲"],
    "shoulder internal rotation": ["肩内旋"],
    "shoulder external rotation": ["肩外旋"],
    "scapular elevation": ["肩胛上提"],
    "scapular depression": ["肩胛下压"],
    "scapular retraction": ["肩胛后缩"],
    "scapular protraction": ["肩胛前伸"],
    "scapular upward rotation": ["肩胛上回旋"],
    "scapular downward rotation": ["肩胛下回旋"],
    "elbow flexion": ["肘屈"],
    "elbow extension": ["肘伸"],
    "forearm supination": ["前臂旋后"],
    "hip extension": ["髋伸"],
    "hip flexion": ["髋屈"],
    "hip abduction": ["髋外展"],
    "hip adduction": ["髋内收"],
    "hip external rotation": ["髋外旋"],
    "hip internal rotation": ["髋内旋"],
    "knee extension": ["膝伸"],
    "knee flexion": ["膝屈", "屈膝"],
    "ankle plantar flexion": ["踝跖屈", "跖屈"],
    "trunk flexion": ["躯干屈曲"],
    "trunk lateral flexion": ["躯干侧屈"],
    "trunk rotation": ["躯干旋转"],
    "trunk stabilization": ["躯干稳定"],
    "spinal extension": ["脊柱伸展"],
    "spinal lateral flexion": ["脊柱侧屈"],
    "wrist flexion": ["腕屈"],
    "wrist extension": ["腕伸"],
    "finger flexion": ["指屈"],
    "finger extension": ["指伸"],
    "grip": ["握持", "握力"],
    "pelvic stabilization": ["骨盆稳定"],
    "abdominal compression": ["腹腔压缩"],
}

REQUIRED_FIELDS = {
    "id",
    "name_en",
    "name_zh",
    "anatomical_group",
    "atlas_region_ids",
    "origin_summary",
    "insertion_summary",
    "crosses_joints",
    "primary_actions",
    "secondary_actions",
    "role_in_training",
    "movement_pattern_ids",
    "representative_exercise_ids",
    "source_ids",
    "claim_ids",
    "limitations",
}


def anatomy_path(path: str | Path | None = None) -> Path:
    return Path(path) if path else DEFAULT_ANATOMY_PATH


@lru_cache(maxsize=4)
def _load_cached(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    if not path.exists():
        raise FileNotFoundError(f"Training anatomy records are not available: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_training_anatomy(payload)
    return payload


def load_training_anatomy(path: str | Path | None = None) -> dict[str, Any]:
    return _load_cached(str(anatomy_path(path).resolve()))


def validate_training_anatomy(
    payload: dict[str, Any],
    *,
    root: str | Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Validate anatomy records against the atlas, catalogue and evidence store."""

    errors: list[str] = []
    if payload.get("schema") != "sportrx.training_anatomy.v1":
        errors.append("unsupported training anatomy schema")
    records = payload.get("records", [])
    if not isinstance(records, list) or not records:
        errors.append("training anatomy requires records")
        records = []

    root_path = Path(root).resolve()
    atlas = load_hypertrophy_atlas(root_path / "data/exercises/hypertrophy_atlas.json")
    catalogue = load_exercise_catalogue(root_path / "data/exercises/catalogue.json")
    evidence = load_evidence_records(root_path)
    region_ids = {item["id"] for item in atlas["muscle_regions"]}
    pattern_ids = {item["id"] for item in atlas["movement_patterns"]}
    exercise_ids = {item["id"] for item in catalogue["exercises"]}
    source_ids = {item["id"] for item in evidence["sources"]}
    claim_ids = {item["id"] for item in evidence["claims"]}

    seen: set[str] = set()
    for record in records:
        identifier = str(record.get("id", "<missing id>"))
        if identifier in seen:
            errors.append(f"duplicate anatomy id: {identifier}")
        seen.add(identifier)
        missing = sorted(
            field
            for field in REQUIRED_FIELDS
            if field not in record or (field not in {"secondary_actions"} and record[field] in (None, "", []))
        )
        if missing:
            errors.append(f"anatomy record {identifier} missing: {', '.join(missing)}")
        for region_id in record.get("atlas_region_ids", []):
            if region_id not in region_ids:
                errors.append(f"anatomy record {identifier} references unknown region: {region_id}")
        for pattern_id in record.get("movement_pattern_ids", []):
            if pattern_id not in pattern_ids:
                errors.append(f"anatomy record {identifier} references unknown pattern: {pattern_id}")
        for exercise_id in record.get("representative_exercise_ids", []):
            if exercise_id not in exercise_ids:
                errors.append(f"anatomy record {identifier} references unknown exercise: {exercise_id}")
        for source_id in record.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"anatomy record {identifier} references unknown source: {source_id}")
        for claim_id in record.get("claim_ids", []):
            if claim_id not in claim_ids:
                errors.append(f"anatomy record {identifier} references unknown claim: {claim_id}")

    if errors:
        raise ValueError("; ".join(errors))
    return {
        "schema": "sportrx.training_anatomy_validation",
        "valid": True,
        "record_count": len(records),
        "region_count": len({region for item in records for region in item["atlas_region_ids"]}),
        "action_count": len({action for item in records for action in item["primary_actions"]}),
        "content_boundary": CONTENT_BOUNDARY,
    }


def training_anatomy_summary(path: str | Path | None = None) -> dict[str, Any]:
    payload = load_training_anatomy(path)
    return {
        **validate_training_anatomy(payload),
        "version": payload["version"],
        "reviewed_at": payload["reviewed_at"],
        "scope": payload["scope"],
    }


@lru_cache(maxsize=1)
def _evidence_maps() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    evidence = load_evidence_records(PROJECT_ROOT)
    return (
        {item["id"]: item for item in evidence["claims"]},
        {item["id"]: item for item in evidence["sources"]},
    )


def _with_trace(record: dict[str, Any]) -> dict[str, Any]:
    claims_by_id, sources_by_id = _evidence_maps()
    claims = [claims_by_id[item] for item in record["claim_ids"]]
    source_ids = list(dict.fromkeys([*record["source_ids"], *(source for claim in claims for source in claim["source_ids"])]))
    return {
        **record,
        "primary_action_terms_zh": _action_terms_zh(record["primary_actions"]),
        "secondary_action_terms_zh": _action_terms_zh(record["secondary_actions"]),
        "functional_tags_zh": _functional_tags_zh(record),
        "claims": claims,
        "sources": [sources_by_id[item] for item in source_ids if item in sources_by_id],
        "content_boundary": CONTENT_BOUNDARY,
    }


def _action_terms_zh(actions: list[str]) -> list[str]:
    return list(
        dict.fromkeys(
            term
            for action in actions
            for key, terms in ACTION_SEARCH_ZH.items()
            if key in action.casefold()
            for term in terms
        )
    )


def _functional_tags_zh(record: dict[str, Any]) -> list[str]:
    tags = ["训练解剖", "运动解剖学"]
    if len(record["crosses_joints"]) >= 2:
        tags.extend(["跨关节", "双关节肌"])
    return tags


def get_training_anatomy_record(record_id: str, path: str | Path | None = None) -> dict[str, Any] | None:
    for record in load_training_anatomy(path)["records"]:
        if record["id"] == record_id:
            return _with_trace(record)
    return None


def search_training_anatomy(
    query: str = "",
    *,
    atlas_region: str | None = None,
    action: str | None = None,
    limit: int = 20,
    path: str | Path | None = None,
) -> dict[str, Any]:
    """Search reviewed anatomy records without making a prescription."""

    terms = [term.casefold() for term in query.strip().split() if term]
    scored: list[tuple[int, dict[str, Any]]] = []
    for record in load_training_anatomy(path)["records"]:
        if atlas_region and atlas_region not in record["atlas_region_ids"]:
            continue
        actions = record["primary_actions"] + record["secondary_actions"]
        if action and not any(action.casefold() in item.casefold() for item in actions):
            continue
        action_terms_zh = _action_terms_zh(actions)
        functional_tags_zh = _functional_tags_zh(record)
        values = [
            record["id"], record["name_en"], record["name_zh"], record.get("aliases_zh", []),
            record["anatomical_group"], record["atlas_region_ids"], actions,
            action_terms_zh, functional_tags_zh, record["role_in_training"], record["movement_pattern_ids"],
        ]
        searchable = " ".join(" ".join(value) if isinstance(value, list) else str(value) for value in values).casefold()
        if terms and not all(term in searchable for term in terms):
            continue
        name_text = f"{record['name_en']} {record['name_zh']} {' '.join(record.get('aliases_zh', []))}".casefold()
        score = 100 * sum(term in name_text for term in terms)
        score += 30 if atlas_region in record["atlas_region_ids"] else 0
        score += 20 if action and any(action.casefold() in item.casefold() for item in actions) else 0
        scored.append((score, record))

    scored.sort(key=lambda item: (-item[0], item[1]["id"]))
    results = [_with_trace(record) for _score, record in scored[: max(0, limit)]]
    return {
        "schema": "sportrx.training_anatomy_search.v1",
        "status": "ready" if results else "no_reviewed_match",
        "query": query,
        "filters": {"atlas_region": atlas_region, "action": action},
        "results": results,
        "content_boundary": CONTENT_BOUNDARY,
    }
