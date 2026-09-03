"""Reviewed hypertrophy movement atlas over the local exercise catalogue.

The atlas describes muscle-region coverage, movement families and practical
equipment substitutions. It is an educational content layer: it never selects
training dose, declares a best exercise, or makes a medical suitability decision.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from .evidence_store import load_evidence_records
from .exercise_catalogue import get_exercise, load_exercise_catalogue


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ATLAS_PATH = PROJECT_ROOT / "data" / "exercises" / "hypertrophy_atlas.json"

CONTENT_BOUNDARY = (
    "SportRX Hypertrophy Movement Atlas explains muscle-region coverage, movement "
    "families and equipment alternatives. It does not prescribe sets, repetitions, "
    "load, frequency or progression; diagnose pain; or identify one universally best exercise."
)

REQUIRED_REGION_FIELDS = {
    "id",
    "label_en",
    "label_zh",
    "anatomical_scope",
    "primary_joint_actions",
    "movement_pattern_ids",
    "coverage_notes_zh",
    "limitations",
    "evidence_claim_ids",
}

REQUIRED_PATTERN_FIELDS = {
    "id",
    "label_en",
    "label_zh",
    "joint_actions",
    "primary_region_ids",
    "secondary_region_ids",
    "classification",
    "representative_exercise_ids",
    "equipment_options",
    "selection_notes_zh",
    "limitations",
    "evidence_claim_ids",
}


def atlas_path(path: str | Path | None = None) -> Path:
    return Path(path) if path else DEFAULT_ATLAS_PATH


@lru_cache(maxsize=4)
def _load_atlas_cached(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    if not path.exists():
        raise FileNotFoundError(f"Hypertrophy movement atlas is not available: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_hypertrophy_atlas(payload)
    return payload


def load_hypertrophy_atlas(path: str | Path | None = None) -> dict[str, Any]:
    """Load the reviewed atlas and validate all catalogue/evidence links."""

    return _load_atlas_cached(str(atlas_path(path).resolve()))


def _missing(record: dict[str, Any], required: set[str]) -> list[str]:
    return sorted(field for field in required if record.get(field) in (None, "", []))


def _duplicates(records: list[dict[str, Any]]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for record in records:
        identifier = str(record.get("id", ""))
        if identifier in seen:
            duplicates.add(identifier)
        seen.add(identifier)
    return duplicates


def validate_hypertrophy_atlas(
    payload: dict[str, Any],
    *,
    root: str | Path = PROJECT_ROOT,
) -> dict[str, Any]:
    """Validate muscle, movement, catalogue and evidence relationships."""

    errors: list[str] = []
    if payload.get("schema") != "sportrx.hypertrophy_movement_atlas.v1":
        errors.append("unsupported hypertrophy atlas schema")

    regions = payload.get("muscle_regions", [])
    patterns = payload.get("movement_patterns", [])
    if not isinstance(regions, list) or not regions:
        errors.append("atlas requires muscle_regions")
        regions = []
    if not isinstance(patterns, list) or not patterns:
        errors.append("atlas requires movement_patterns")
        patterns = []

    for identifier in sorted(_duplicates(regions)):
        errors.append(f"duplicate muscle region id: {identifier}")
    for identifier in sorted(_duplicates(patterns)):
        errors.append(f"duplicate movement pattern id: {identifier}")

    root_path = Path(root).resolve()
    catalogue = load_exercise_catalogue(root_path / "data/exercises/catalogue.json")
    exercises = {item["id"]: item for item in catalogue["exercises"]}
    evidence = load_evidence_records(root_path)
    claim_ids = {item["id"] for item in evidence["claims"]}
    region_ids = {str(item.get("id", "")) for item in regions}
    pattern_ids = {str(item.get("id", "")) for item in patterns}

    for region in regions:
        region_id = str(region.get("id", "<missing id>"))
        missing = _missing(region, REQUIRED_REGION_FIELDS)
        if missing:
            errors.append(f"muscle region {region_id} missing: {', '.join(missing)}")
        for pattern_id in region.get("movement_pattern_ids", []):
            if pattern_id not in pattern_ids:
                errors.append(f"muscle region {region_id} references unknown pattern: {pattern_id}")
        for claim_id in region.get("evidence_claim_ids", []):
            if claim_id not in claim_ids:
                errors.append(f"muscle region {region_id} references unknown claim: {claim_id}")

    covered_regions: set[str] = set()
    for pattern in patterns:
        pattern_id = str(pattern.get("id", "<missing id>"))
        missing = _missing(pattern, REQUIRED_PATTERN_FIELDS - {"secondary_region_ids"})
        if "secondary_region_ids" not in pattern:
            missing.append("secondary_region_ids")
        if missing:
            errors.append(f"movement pattern {pattern_id} missing: {', '.join(missing)}")
        referenced_regions = pattern.get("primary_region_ids", []) + pattern.get("secondary_region_ids", [])
        for region_id in referenced_regions:
            if region_id not in region_ids:
                errors.append(f"movement pattern {pattern_id} references unknown region: {region_id}")
            covered_regions.add(region_id)
        for exercise_id in pattern.get("representative_exercise_ids", []):
            if exercise_id not in exercises:
                errors.append(f"movement pattern {pattern_id} references unknown exercise: {exercise_id}")
        representative_equipment = {
            exercises[exercise_id]["equipment"]
            for exercise_id in pattern.get("representative_exercise_ids", [])
            if exercise_id in exercises
        }
        if not representative_equipment.issubset(set(pattern.get("equipment_options", []))):
            errors.append(f"movement pattern {pattern_id} omits representative equipment")
        for claim_id in pattern.get("evidence_claim_ids", []):
            if claim_id not in claim_ids:
                errors.append(f"movement pattern {pattern_id} references unknown claim: {claim_id}")

    for region_id in sorted(region_ids - covered_regions):
        errors.append(f"muscle region has no movement coverage: {region_id}")

    if errors:
        raise ValueError("; ".join(errors))
    return {
        "schema": "sportrx.hypertrophy_atlas_validation",
        "valid": True,
        "muscle_region_count": len(regions),
        "movement_pattern_count": len(patterns),
        "representative_exercise_count": len(
            {exercise_id for item in patterns for exercise_id in item["representative_exercise_ids"]}
        ),
        "content_boundary": CONTENT_BOUNDARY,
    }


def atlas_summary(path: str | Path | None = None) -> dict[str, Any]:
    payload = load_hypertrophy_atlas(path)
    validation = validate_hypertrophy_atlas(payload)
    return {
        **validation,
        "version": payload["version"],
        "reviewed_at": payload["reviewed_at"],
        "source_catalogue": payload["source_catalogue"],
        "excluded_scope": payload["excluded_scope"],
    }


def get_muscle_region(region_id: str, path: str | Path | None = None) -> dict[str, Any] | None:
    payload = load_hypertrophy_atlas(path)
    patterns_by_id = {item["id"]: item for item in payload["movement_patterns"]}
    for region in payload["muscle_regions"]:
        if region["id"] == region_id:
            claims, sources = _evidence_trace(region["evidence_claim_ids"])
            return {
                **region,
                "movement_patterns": [patterns_by_id[item] for item in region["movement_pattern_ids"]],
                "claims": claims,
                "sources": sources,
                "content_boundary": CONTENT_BOUNDARY,
            }
    return None


@lru_cache(maxsize=1)
def _evidence_maps() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    evidence = load_evidence_records(PROJECT_ROOT)
    claims_by_id = {item["id"]: item for item in evidence["claims"]}
    sources_by_id = {item["id"]: item for item in evidence["sources"]}
    return claims_by_id, sources_by_id


def _evidence_trace(claim_ids: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    claims_by_id, sources_by_id = _evidence_maps()
    claims = [claims_by_id[item] for item in claim_ids if item in claims_by_id]
    source_ids = list(dict.fromkeys(source_id for claim in claims for source_id in claim["source_ids"]))
    return claims, [sources_by_id[item] for item in source_ids if item in sources_by_id]


def _search_text(pattern: dict[str, Any], regions: dict[str, dict[str, Any]]) -> str:
    region_text = " ".join(
        f"{regions[item]['label_en']} {regions[item]['label_zh']} {' '.join(regions[item].get('aliases_zh', []))}"
        for item in pattern["primary_region_ids"] + pattern["secondary_region_ids"]
    )
    values = [
        pattern["id"],
        pattern["label_en"],
        pattern["label_zh"],
        pattern["joint_actions"],
        pattern["equipment_options"],
        pattern["selection_notes_zh"],
        region_text,
    ]
    return " ".join(" ".join(value) if isinstance(value, list) else str(value) for value in values).casefold()


def search_hypertrophy_movements(
    query: str = "",
    *,
    muscle_region: str | None = None,
    equipment: str | None = None,
    limit: int = 12,
    path: str | Path | None = None,
) -> dict[str, Any]:
    """Search reviewed movement families without producing a workout."""

    payload = load_hypertrophy_atlas(path)
    regions = {item["id"]: item for item in payload["muscle_regions"]}
    terms = [term.casefold() for term in query.strip().split() if term]
    scored: list[tuple[int, dict[str, Any]]] = []
    for pattern in payload["movement_patterns"]:
        related_regions = pattern["primary_region_ids"] + pattern["secondary_region_ids"]
        if muscle_region and muscle_region not in related_regions:
            continue
        if equipment and equipment not in pattern["equipment_options"]:
            continue
        searchable = _search_text(pattern, regions)
        if terms and not all(term in searchable for term in terms):
            continue
        score = 0
        if muscle_region in pattern["primary_region_ids"]:
            score += 40
        if equipment in pattern["equipment_options"]:
            score += 20
        score += 10 * sum(term in f"{pattern['label_en']} {pattern['label_zh']}".casefold() for term in terms)
        scored.append((score, pattern))

    scored.sort(key=lambda item: (-item[0], item[1]["id"]))
    results: list[dict[str, Any]] = []
    for _score, pattern in scored[: max(0, limit)]:
        claims, sources = _evidence_trace(pattern["evidence_claim_ids"])
        exercises = [get_exercise(exercise_id) for exercise_id in pattern["representative_exercise_ids"]]
        if equipment:
            exercises = [exercise for exercise in exercises if exercise and exercise["equipment"] == equipment]
        results.append(
            {
                **pattern,
                "primary_regions": [regions[item] for item in pattern["primary_region_ids"]],
                "secondary_regions": [regions[item] for item in pattern["secondary_region_ids"]],
                "representative_exercises": exercises,
                "claims": claims,
                "sources": sources,
            }
        )
    return {
        "schema": "sportrx.hypertrophy_movement_search.v1",
        "status": "ready" if results else "no_reviewed_match",
        "query": query,
        "filters": {"muscle_region": muscle_region, "equipment": equipment},
        "results": results,
        "content_boundary": CONTENT_BOUNDARY,
    }
