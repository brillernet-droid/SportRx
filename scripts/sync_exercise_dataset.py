"""Synchronise text-only movement content from the reviewed upstream dataset.

The upstream project includes third-party images and GIFs under separate terms.
This script deliberately strips every media field before writing SportRX data.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_COMMIT = "7455efae41b330c265e7cd4b78dfa848e7ce5ebd"
DEFAULT_SOURCE_URL = f"https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/{UPSTREAM_COMMIT}/data/exercises.json"
DEFAULT_OUTPUT = ROOT / "data" / "exercises" / "catalogue.json"


def _download_json(url: str) -> list[dict]:
    request = Request(url, headers={"User-Agent": "SportRX-catalogue-sync/0.1"})
    with urlopen(request, timeout=60) as response:  # nosec B310: reviewed HTTPS source passed by maintainer
        payload = json.load(response)
    if not isinstance(payload, list):
        raise ValueError("Expected a JSON array from the upstream exercise dataset.")
    return payload


def _normalise(source_exercises: list[dict]) -> list[dict]:
    exercises: list[dict] = []
    for source in source_exercises:
        instructions = source.get("instructions", {})
        steps = source.get("instruction_steps", {})
        if not instructions.get("zh") or not instructions.get("en"):
            continue
        exercises.append(
            {
                "id": f"exercises-dataset:{source['id']}",
                "upstream_id": str(source["id"]),
                "name": str(source["name"]),
                "category": str(source["category"]),
                "body_part": str(source["body_part"]),
                "equipment": str(source["equipment"]),
                "target": str(source["target"]),
                "muscle_group": str(source["muscle_group"]),
                "secondary_muscles": [str(item) for item in source.get("secondary_muscles", [])],
                "instructions": {"zh": str(instructions["zh"]), "en": str(instructions["en"])},
                "instruction_steps": {
                    "zh": [str(item) for item in steps.get("zh", [])],
                    "en": [str(item) for item in steps.get("en", [])],
                },
            }
        )
    return exercises


def build_catalogue(source_exercises: list[dict], source_url: str) -> dict:
    exercises = _normalise(source_exercises)
    return {
        "schema": "sportrx.exercise_catalogue.v1",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "count": len(exercises),
        "source": {
            "repository": "hasaneyldrm/exercises-dataset",
            "repository_url": "https://github.com/hasaneyldrm/exercises-dataset",
            "upstream_commit": UPSTREAM_COMMIT,
            "raw_url": source_url,
            "license": "MIT for data structure and instructional text; third-party media excluded.",
            "media_included": False,
            "notice": "Exercise media is not included. See data/exercises/THIRD_PARTY_NOTICES.md.",
        },
        "exercises": exercises,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Synchronise the SportRX text-only exercise catalogue.")
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    catalogue = build_catalogue(_download_json(args.source_url), args.source_url)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(catalogue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {catalogue['count']} text-only exercises to {args.output}")


if __name__ == "__main__":
    main()
