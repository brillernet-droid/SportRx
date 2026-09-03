import json
from pathlib import Path

import pytest

from sportrx.hypertrophy_atlas import (
    CONTENT_BOUNDARY,
    atlas_summary,
    get_muscle_region,
    load_hypertrophy_atlas,
    search_hypertrophy_movements,
    validate_hypertrophy_atlas,
)


ROOT = Path(__file__).resolve().parents[1]


def test_reviewed_hypertrophy_atlas_links_muscles_patterns_exercises_and_claims():
    summary = atlas_summary()

    assert summary["valid"]
    assert summary["muscle_region_count"] == 16
    assert summary["movement_pattern_count"] == 21
    assert summary["representative_exercise_count"] == 62
    assert "does not prescribe sets" in summary["content_boundary"]
    assert summary["source_catalogue"]["upstream_repository"] == "hasaneyldrm/exercises-dataset"


def test_muscle_region_keeps_direct_and_secondary_coverage_separate():
    chest = get_muscle_region("pectorals")
    assert chest is not None

    horizontal_push = next(item for item in chest["movement_patterns"] if item["id"] == "horizontal_push")
    assert horizontal_push["primary_region_ids"] == ["pectorals"]
    assert set(horizontal_push["secondary_region_ids"]) == {"deltoid_anterior", "triceps"}
    assert "universally best exercise" in chest["content_boundary"]


def test_search_accepts_body_part_language_and_equipment_filters():
    back = search_hypertrophy_movements("背部")
    dumbbell_shoulders = search_hypertrophy_movements(muscle_region="deltoid_lateral", equipment="dumbbell")

    assert back["status"] == "ready"
    assert {item["id"] for item in back["results"]} >= {"vertical_pull", "horizontal_pull"}
    assert {item["id"] for item in dumbbell_shoulders["results"]} >= {"vertical_push", "lateral_raise"}
    assert all(
        exercise and exercise["id"].startswith("exercises-dataset:") and exercise["equipment"] == "dumbbell"
        for result in dumbbell_shoulders["results"]
        for exercise in result["representative_exercises"]
    )
    assert all(result["claims"] and result["sources"] for result in dumbbell_shoulders["results"])


def test_atlas_validator_rejects_unknown_exercise_and_claim():
    payload = json.loads(json.dumps(load_hypertrophy_atlas()))
    payload["movement_patterns"][0]["representative_exercise_ids"] = ["missing:exercise"]
    payload["muscle_regions"][0]["evidence_claim_ids"] = ["missing-claim"]

    with pytest.raises(ValueError) as error:
        validate_hypertrophy_atlas(payload, root=ROOT)

    message = str(error.value)
    assert "unknown exercise" in message
    assert "unknown claim" in message


def test_atlas_is_content_only_and_hypertrophy_pack_stays_assessment_only():
    atlas = load_hypertrophy_atlas()
    pack = json.loads((ROOT / "data/program_packs/hypertrophy_foundation_v0.json").read_text(encoding="utf-8"))

    assert atlas["content_boundary"].startswith("Educational movement coverage only")
    assert CONTENT_BOUNDARY.endswith("one universally best exercise.")
    assert pack["release_status"] == "assessment_only"
    assert pack["rule_ids"] == []
    assert pack["content_mapping"]["dose_authority"] == "none"
