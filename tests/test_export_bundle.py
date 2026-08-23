import json

from sportrx.demo_seed import build_demo_state
from sportrx.export_bundle import build_export_bundle
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription


def test_export_bundle_packages_review_artifacts():
    state = build_demo_state()
    profile = state["profile"]
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile, feedback_by_week=state["feedback_by_week"])

    bundle = build_export_bundle(profile, passport, plan, state["benchmark_sessions"], state["feedback_by_week"])

    file_ids = {item["id"] for item in bundle["files"]}
    assert "manifest_json" in file_ids
    assert "artifact_catalog_markdown" in file_ids
    assert "reviewer_handoff_markdown" in file_ids
    assert "release_candidate_summary_markdown" in file_ids
    assert "first_run_guide_markdown" in file_ids
    assert "terminology_markdown" in file_ids
    assert "demo_experience_markdown" in file_ids
    assert "guided_review_markdown" in file_ids
    assert "input_ledger_markdown" in file_ids
    assert "quick_match_intake_contract_markdown" in file_ids
    assert "quick_match_lab_intake_sheet_markdown" in file_ids
    assert "intake_precision_markdown" in file_ids
    assert "measurement_schema_registry_markdown" in file_ids
    assert "evidence_library_markdown" in file_ids
    assert "evidence_coverage_markdown" in file_ids
    assert "session_quality_review_markdown" in file_ids
    assert "validation_readiness_markdown" in file_ids
    assert "self_use_protocol_markdown" in file_ids
    assert "measurement_timeline_markdown" in file_ids
    assert "page_health_matrix_markdown" in file_ids
    assert "open_source_integration_markdown" in file_ids
    assert "protocol_markdown" in file_ids
    assert "benchmark_worksheet_markdown" in file_ids
    assert "test_day_brief_markdown" in file_ids
    assert "test_day_command_board_markdown" in file_ids
    assert "test_session_operator_markdown" in file_ids
    assert "lab_readiness_markdown" in file_ids
    assert "measurement_intake_matrix_markdown" in file_ids
    assert "measurement_intake_matrix_csv" in file_ids
    assert "protocol_source_guide_markdown" in file_ids
    assert "benchmark_log_entry_contract_markdown" in file_ids
    assert "protocol_deviation_markdown" in file_ids
    assert "benchmark_log_json" in file_ids
    assert "training_profile_markdown" in file_ids
    assert "training_block_markdown" in file_ids
    assert "feedback_dashboard_markdown" in file_ids
    assert "retest_interpretation_markdown" in file_ids
    assert "launch_readiness_markdown" in file_ids
    assert "public_beta_readiness_markdown" in file_ids
    assert "runtime_doctor_markdown" in file_ids
    assert "demo_runbook_markdown" in file_ids
    assert "demo_scenario_matrix_markdown" in file_ids
    assert "reviewer_session_plan_markdown" in file_ids
    assert "pilot_feedback_prompt_markdown" in file_ids
    assert "alpha_dataset_dictionary_markdown" in file_ids
    assert "alpha_participants_template_csv" in file_ids
    assert "alpha_benchmark_sessions_template_csv" in file_ids
    assert "alpha_weekly_feedback_template_csv" in file_ids
    assert "alpha_pilot_review_template_csv" in file_ids
    assert "pilot_feedback_json" in file_ids
    assert "pilot_feedback_markdown" in file_ids
    assert "session_snapshot_json" in file_ids
    assert "session_snapshot_markdown" in file_ids
    assert "predictions" in bundle["claim_boundary"]


def test_export_manifest_is_valid_json():
    state = build_demo_state()
    profile = state["profile"]
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile)
    bundle = build_export_bundle(profile, passport, plan, state["benchmark_sessions"], state["feedback_by_week"])
    manifest = next(item for item in bundle["files"] if item["id"] == "manifest_json")

    parsed = json.loads(manifest["content"])

    assert parsed["schema"] == "sportrx.export_bundle"
    assert parsed["artifact_count"] == 53
