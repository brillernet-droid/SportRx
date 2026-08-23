from sportrx.artifact_catalog import build_artifact_catalog, artifact_catalog_markdown
from sportrx.demo_seed import build_demo_state
from sportrx.export_bundle import build_export_bundle
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription


def _bundle_files():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    return build_export_bundle(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
    )["files"]


def test_artifact_catalog_groups_export_files_for_review():
    catalog = build_artifact_catalog(_bundle_files())
    categories = {group["category"] for group in catalog["categories"]}

    assert catalog["schema"] == "sportrx.artifact_catalog"
    assert "Start Here" in categories
    assert "Measurement" in categories
    assert "Raw Data" in categories
    assert "Restore" in categories
    assert any(item["filename"] == "sportrx_reviewer_handoff.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_terminology_guide.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_demo_experience_console.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_guided_review_console.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_input_ledger.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_quick_match_intake_contract.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_quick_match_lab_intake_sheet.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_measurement_schema_registry.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_evidence_library.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_evidence_coverage.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_session_quality_review.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_validation_readiness_matrix.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_phase_0_self_use_protocol.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_benchmark_worksheet.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_test_day_command_board.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_measurement_intake_matrix.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_measurement_intake_matrix.csv" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_protocol_source_guide.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_intake_precision_audit.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_release_candidate_summary.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_page_health_matrix.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_alpha_dataset_dictionary.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_alpha_participants_template.csv" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_protocol_deviation_review.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_retest_interpretation_guard.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_session_snapshot.json" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_demo_scenario_matrix.md" for item in catalog["items"])
    assert any(item["filename"] == "sportrx_reviewer_session_plan.md" for item in catalog["items"])
    assert "review handoff only" in catalog["claim_boundary"]


def test_artifact_catalog_markdown_lists_key_files():
    catalog = build_artifact_catalog(_bundle_files())
    markdown = artifact_catalog_markdown(catalog)

    assert "# SportRx Artifact Catalog" in markdown
    assert "sportrx_reviewer_handoff.md" in markdown
    assert "sportrx_terminology_guide.md" in markdown
    assert "sportrx_demo_experience_console.md" in markdown
    assert "sportrx_guided_review_console.md" in markdown
    assert "sportrx_input_ledger.md" in markdown
    assert "sportrx_quick_match_intake_contract.md" in markdown
    assert "sportrx_quick_match_lab_intake_sheet.md" in markdown
    assert "sportrx_measurement_schema_registry.md" in markdown
    assert "sportrx_evidence_library.md" in markdown
    assert "sportrx_evidence_coverage.md" in markdown
    assert "sportrx_session_quality_review.md" in markdown
    assert "sportrx_validation_readiness_matrix.md" in markdown
    assert "sportrx_phase_0_self_use_protocol.md" in markdown
    assert "sportrx_benchmark_worksheet.md" in markdown
    assert "sportrx_test_day_command_board.md" in markdown
    assert "sportrx_measurement_intake_matrix.md" in markdown
    assert "sportrx_measurement_intake_matrix.csv" in markdown
    assert "sportrx_protocol_source_guide.md" in markdown
    assert "sportrx_intake_precision_audit.md" in markdown
    assert "sportrx_release_candidate_summary.md" in markdown
    assert "sportrx_page_health_matrix.md" in markdown
    assert "sportrx_alpha_dataset_dictionary.md" in markdown
    assert "sportrx_alpha_benchmark_sessions_template.csv" in markdown
    assert "sportrx_protocol_deviation_review.md" in markdown
    assert "sportrx_retest_interpretation_guard.md" in markdown
    assert "sportrx_first_run_guide.md" in markdown
    assert "sportrx_benchmark_log.json" in markdown
    assert "sportrx_demo_scenario_matrix.md" in markdown
    assert "sportrx_reviewer_session_plan.md" in markdown
