import json
import shutil
from pathlib import Path

from sportrx.prescription_knowledge import validate_prescription_knowledge


ROOT = Path(__file__).resolve().parents[1]


def test_goal_prescription_manifest_has_complete_traceable_routes():
    result = validate_prescription_knowledge(ROOT)

    assert result["valid"]
    assert result["status"] == "review_ready"
    assert result["goal_count"] == 6
    assert "muscle_gain" in result["mapped_goal_ids"]
    assert "does not enable a program pack" in result["claim_boundary"]


def test_assessment_only_goal_can_have_no_rules_but_must_keep_evidence_chain(tmp_path):
    shutil.copytree(ROOT / "evidence", tmp_path / "evidence")
    manifest_path = tmp_path / "evidence/prescription/manifest.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    muscle_gain = next(item for item in payload["goals"] if item["goal_id"] == "muscle_gain")
    assert muscle_gain["product_status"] == "assessment_only"
    assert muscle_gain["rule_ids"] == []

    muscle_gain["card_ids"] = []
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    result = validate_prescription_knowledge(tmp_path)
    assert not result["valid"]
    assert any("incomplete evidence chain" in error for error in result["errors"])
