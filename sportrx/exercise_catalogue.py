"""Local exercise-content catalogue, separate from SportRX prescription rules.

The catalogue provides movement names, equipment and upstream instructional text.
It never decides a training dose, medical route, progression or exercise safety.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOGUE_PATH = PROJECT_ROOT / "data" / "exercises" / "catalogue.json"

BODY_PART_LABELS = {
    "back": "背部",
    "cardio": "心肺训练",
    "chest": "胸部",
    "lower arms": "前臂",
    "lower legs": "小腿",
    "neck": "颈部",
    "shoulders": "肩部",
    "upper arms": "上臂",
    "upper legs": "大腿",
    "waist": "核心与腰腹",
}


def catalogue_path(path: str | Path | None = None) -> Path:
    """Return the local, reviewed catalogue path."""

    return Path(path) if path else DEFAULT_CATALOGUE_PATH


@lru_cache(maxsize=4)
def _load_catalogue_cached(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    if not path.exists():
        raise FileNotFoundError(
            "Exercise catalogue is not available. Run scripts/sync_exercise_dataset.py before using it."
        )
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    validate_exercise_catalogue(payload)
    return payload


def load_exercise_catalogue(path: str | Path | None = None) -> dict[str, Any]:
    """Load the vendored text-only movement catalogue."""

    return _load_catalogue_cached(str(catalogue_path(path).resolve()))


def validate_exercise_catalogue(payload: dict[str, Any]) -> None:
    """Validate the fields SportRX uses from a synchronised upstream snapshot."""

    if payload.get("schema") != "sportrx.exercise_catalogue.v1":
        raise ValueError("Unsupported exercise catalogue schema.")
    if not isinstance(payload.get("source"), dict) or not payload["source"].get("repository"):
        raise ValueError("Exercise catalogue requires source metadata.")
    exercises = payload.get("exercises")
    if not isinstance(exercises, list) or not exercises:
        raise ValueError("Exercise catalogue must contain exercises.")
    if int(payload.get("count", -1)) != len(exercises):
        raise ValueError("Exercise catalogue count does not match exercises.")

    identifiers: set[str] = set()
    for exercise in exercises:
        identifier = str(exercise.get("id", ""))
        if not identifier or identifier in identifiers:
            raise ValueError("Exercise catalogue identifiers must be unique.")
        identifiers.add(identifier)
        for field in ("name", "body_part", "equipment", "target", "instructions"):
            if not exercise.get(field):
                raise ValueError(f"Exercise {identifier} is missing {field}.")
        instructions = exercise["instructions"]
        if not isinstance(instructions, dict) or not instructions.get("zh") or not instructions.get("en"):
            raise ValueError(f"Exercise {identifier} requires Chinese and English instructions.")
        if "image" in exercise or "gif_url" in exercise or "media_id" in exercise:
            raise ValueError("SportRX catalogue intentionally excludes third-party media fields.")


def body_part_label(value: str) -> str:
    return BODY_PART_LABELS.get(value, value)


def catalogue_summary(path: str | Path | None = None) -> dict[str, Any]:
    payload = load_exercise_catalogue(path)
    exercises = payload["exercises"]
    return {
        "count": len(exercises),
        "body_parts": sorted({str(item["body_part"]) for item in exercises}),
        "equipment": sorted({str(item["equipment"]) for item in exercises}),
        "source": payload["source"],
        "generated_at": payload.get("generated_at"),
        "content_boundary": "动作库提供内容与操作说明；不构成自动处方、医疗建议或动作安全筛查。",
    }


def get_exercise(exercise_id: str, path: str | Path | None = None) -> dict[str, Any] | None:
    for exercise in load_exercise_catalogue(path)["exercises"]:
        if exercise["id"] == exercise_id:
            return exercise
    return None


def search_exercises(
    query: str = "",
    *,
    body_part: str | None = None,
    equipment: str | None = None,
    limit: int = 24,
    path: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Search approved local movement content without producing a prescription."""

    query_terms = [term.casefold() for term in query.strip().split() if term]
    scored_matches: list[tuple[int, dict[str, Any]]] = []
    for exercise in load_exercise_catalogue(path)["exercises"]:
        if body_part and exercise["body_part"] != body_part:
            continue
        if equipment and exercise["equipment"] != equipment:
            continue
        name = str(exercise["name"]).casefold()
        metadata = " ".join(
            [
                str(exercise["id"]),
                str(exercise["body_part"]),
                str(exercise["equipment"]),
                str(exercise["target"]),
                str(exercise["muscle_group"]),
            ]
        ).casefold()
        instructions = " ".join(
            [str(exercise["instructions"]["zh"]), str(exercise["instructions"]["en"])]
        ).casefold()
        searchable = f"{name} {metadata} {instructions}"
        if query_terms and not all(term in searchable for term in query_terms):
            continue

        score = 0
        if query_terms:
            if all(term in name for term in query_terms):
                score += 100
            if name.startswith(" ".join(query_terms)):
                score += 30
            score += 20 * sum(term in metadata for term in query_terms)
            score += 2 * sum(term in instructions for term in query_terms)
        scored_matches.append((score, exercise))

    scored_matches.sort(key=lambda item: (-item[0], item[1]["name"].casefold(), item[1]["id"]))
    return [exercise for _score, exercise in scored_matches[:limit]]
