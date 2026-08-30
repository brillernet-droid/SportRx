from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_data_governance_document_limits_real_data_collection_and_claims():
    document = (ROOT / "evidence/data_governance.md").read_text(encoding="utf-8")

    assert "does not recruit participants" in document
    assert "anonymous `participant_id`" in document
    assert "deletion request" in document
    assert "Never commit real session logs" in document
    assert "medical clearance" in document
