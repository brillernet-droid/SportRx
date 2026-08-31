import json

import pytest

from sportrx.exercise_catalogue import (
    body_part_label,
    catalogue_summary,
    get_exercise,
    load_exercise_catalogue,
    search_exercises,
    validate_exercise_catalogue,
)


def test_catalogue_is_text_only_and_has_traceable_source():
    catalogue = load_exercise_catalogue()

    assert catalogue["count"] >= 1000
    assert catalogue["source"]["repository"] == "hasaneyldrm/exercises-dataset"
    assert len(catalogue["source"]["upstream_commit"]) == 40
    assert catalogue["source"]["media_included"] is False
    assert all("image" not in exercise and "gif_url" not in exercise for exercise in catalogue["exercises"])


def test_catalogue_search_and_detail_are_bilingual():
    matches = search_exercises("3/4 sit-up", limit=8)

    assert matches
    assert matches[0]["name"] == "3/4 sit-up"
    assert all(item["instructions"]["zh"] and item["instructions"]["en"] for item in matches)
    assert get_exercise(matches[0]["id"])["id"] == matches[0]["id"]


def test_catalogue_filters_and_summary():
    summary = catalogue_summary()
    cardio = search_exercises(body_part="cardio", limit=200)

    assert summary["count"] >= len(cardio) > 0
    assert all(item["body_part"] == "cardio" for item in cardio)
    assert body_part_label("waist") == "核心与腰腹"


def test_catalogue_validation_rejects_media_and_missing_chinese_instruction(tmp_path):
    catalogue = load_exercise_catalogue()
    broken = json.loads(json.dumps(catalogue))
    broken["exercises"][0]["image"] = "images/not-permitted.jpg"
    with pytest.raises(ValueError, match="media"):
        validate_exercise_catalogue(broken)

    broken = json.loads(json.dumps(catalogue))
    broken["exercises"][0]["instructions"]["zh"] = ""
    with pytest.raises(ValueError, match="Chinese"):
        validate_exercise_catalogue(broken)
