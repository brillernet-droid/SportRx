from pathlib import Path

from sportrx.evidence_coverage import build_evidence_coverage, evidence_coverage_markdown


ROOT = Path(__file__).resolve().parents[1]


def test_evidence_coverage_parses_rule_map_and_claim_boundaries():
    coverage = build_evidence_coverage(ROOT)

    assert coverage["schema"] == "sportrx.evidence_coverage"
    assert coverage["status"] == "ready_for_release_review"
    assert coverage["rule_count"] >= 15
    assert coverage["status_counts"]["allowed_ui"] >= 1
    assert coverage["status_counts"]["blocked"] >= 1
    assert coverage["source_count"] >= 10
    assert any(rule["rule_id"] == "PRED-001" for rule in coverage["blocked_rules"])
    assert "Medical clearance" in coverage["forbidden_claims_present"]
    assert "does not validate SportRx" in coverage["claim_boundary"]


def test_evidence_coverage_flags_missing_required_file_context():
    coverage = build_evidence_coverage(
        ROOT,
        {
            "evidence/claim_policy.md": True,
            "evidence/rule_evidence_map.md": False,
            "evidence/validation_plan.md": True,
            "evidence/library/source_index.md": True,
        },
    )

    assert coverage["status"] == "needs_evidence_context"
    assert coverage["required_files_present"] == 3


def test_evidence_coverage_markdown_exports_status_counts():
    coverage = build_evidence_coverage(ROOT)
    markdown = evidence_coverage_markdown(coverage)

    assert "# SportRx Evidence Coverage" in markdown
    assert "Rule Status Counts" in markdown
    assert "Blocked Rules" in markdown
    assert "PRED-001" in markdown
