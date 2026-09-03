import json
from pathlib import Path

import pytest

from scripts.fetch_open_access_hypertrophy_reviews import OPEN_ACCESS_ARTICLES
from sportrx.release_package import should_include_release_path
from sportrx.training_anatomy import (
    CONTENT_BOUNDARY,
    get_training_anatomy_record,
    load_training_anatomy,
    search_training_anatomy,
    training_anatomy_summary,
    validate_training_anatomy,
)


ROOT = Path(__file__).resolve().parents[1]


def test_training_anatomy_has_reviewed_structural_coverage():
    summary = training_anatomy_summary()

    assert summary["valid"]
    assert summary["record_count"] == 34
    assert summary["region_count"] == 16
    assert summary["action_count"] >= 40
    assert "does not diagnose" in summary["content_boundary"]


def test_chinese_search_handles_individual_muscles_actions_and_joint_crossing():
    anterior_deltoid = search_training_anatomy("三角肌前束")
    rectus_femoris = search_training_anatomy("股直肌 跨关节")
    hamstrings = search_training_anatomy("腘绳肌 髋伸 屈膝")

    assert anterior_deltoid["results"][0]["id"] == "ANAT-MUSCLE-006"
    assert rectus_femoris["results"][0]["id"] == "ANAT-MUSCLE-022"
    assert {item["id"] for item in hamstrings["results"][:3]} == {
        "ANAT-MUSCLE-026", "ANAT-MUSCLE-027", "ANAT-MUSCLE-028"
    }
    assert "双关节肌" in rectus_femoris["results"][0]["functional_tags_zh"]


def test_anatomy_detail_returns_sources_claims_and_no_activation_claim():
    record = get_training_anatomy_record("ANAT-MUSCLE-013")

    assert record is not None
    assert record["sources"]
    assert record["claims"]
    assert "肘伸" in record["primary_action_terms_zh"]
    assert "estimate muscle activation" in record["content_boundary"]
    assert CONTENT_BOUNDARY.endswith("maximizes a muscle.")


def test_validator_rejects_unknown_atlas_and_evidence_links():
    payload = json.loads(json.dumps(load_training_anatomy()))
    payload["records"][0]["movement_pattern_ids"] = ["missing_pattern"]
    payload["records"][0]["source_ids"] = ["missing_source"]

    with pytest.raises(ValueError) as error:
        validate_training_anatomy(payload, root=ROOT)

    assert "unknown pattern" in str(error.value)
    assert "unknown source" in str(error.value)


def test_fulltext_fetch_list_is_open_access_only_and_private_files_are_excluded():
    assert {item["source_id"] for item in OPEN_ACCESS_ARTICLES} == {
        "RT-FREE-MACHINE-SR-2023", "RT-ROM-SR-2020"
    }
    assert all(item["download_url"].startswith("https://europepmc.org/") for item in OPEN_ACCESS_ARTICLES)
    assert all("isOpenAccess=Y" in item["access_check"] for item in OPEN_ACCESS_ARTICLES)
    assert not should_include_release_path("evidence/private/fulltext/hypertrophy/example.pdf")
