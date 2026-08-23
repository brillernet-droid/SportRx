from sportrx.demo_seed import build_demo_state
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES, build_release_qa, release_qa_markdown


def _demo_inputs():
    state = build_demo_state()
    profile = state["profile"]
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile, feedback_by_week=state["feedback_by_week"])
    evidence = {path: True for path in REQUIRED_EVIDENCE_FILES}
    return state, profile, passport, plan, evidence


def test_release_qa_marks_complete_demo_ready_for_review():
    state, profile, passport, plan, evidence = _demo_inputs()

    qa = build_release_qa(profile, passport, plan, state["benchmark_sessions"], state["feedback_by_week"], evidence)

    assert qa["status"] == "ready_for_demo_review"
    assert qa["passed_checks"] == qa["total_checks"]
    assert "does not validate" in qa["claim_boundary"]
    assert any(check["id"] == "qa_review_pack_zip" for check in qa["checks"])
    assert any(check["id"] == "qa_review_pack_integrity" for check in qa["checks"])
    assert any(check["id"] == "qa_demo_scenarios" for check in qa["checks"])
    assert any(check["id"] == "qa_demo_scenario_matrix" for check in qa["checks"])
    assert any(check["id"] == "qa_reviewer_session_plan" for check in qa["checks"])
    assert any(check["id"] == "qa_runtime_doctor" for check in qa["checks"])
    assert any(check["id"] == "qa_plan_actual_reasons" for check in qa["checks"])
    assert any(check["id"] == "qa_output_prerequisites" for check in qa["checks"])
    assert any(check["id"] == "qa_session_quality_review" for check in qa["checks"])
    assert any(check["id"] == "qa_session_quality_review_export" for check in qa["checks"])
    assert any(check["id"] == "qa_validation_readiness_matrix" for check in qa["checks"])
    assert any(check["id"] == "qa_validation_readiness_export" for check in qa["checks"])
    assert any(check["id"] == "qa_self_use_protocol" for check in qa["checks"])
    assert any(check["id"] == "qa_self_use_protocol_export" for check in qa["checks"])
    assert any(check["id"] == "qa_lab_readiness_console" for check in qa["checks"])
    assert any(check["id"] == "qa_measurement_intake_matrix" for check in qa["checks"])
    assert any(check["id"] == "qa_alpha_dataset_template" for check in qa["checks"])
    assert any(check["id"] == "qa_protocol_deviation_review" for check in qa["checks"])
    assert any(check["id"] == "qa_retest_interpretation_guard" for check in qa["checks"])
    assert any(check["id"] == "qa_pilot_feedback_prompt" for check in qa["checks"])
    assert any(check["id"] == "qa_first_run_guide" for check in qa["checks"])
    assert any(check["id"] == "qa_terminology_guide" for check in qa["checks"])
    assert any(check["id"] == "qa_terminology_export" for check in qa["checks"])
    assert any(check["id"] == "qa_demo_experience_console" for check in qa["checks"])
    assert any(check["id"] == "qa_demo_experience_export" for check in qa["checks"])
    assert any(check["id"] == "qa_guided_review_console" for check in qa["checks"])
    assert any(check["id"] == "qa_guided_review_export" for check in qa["checks"])
    assert any(check["id"] == "qa_reviewer_handoff" for check in qa["checks"])
    assert any(check["id"] == "qa_release_candidate_summary_export" for check in qa["checks"])
    assert any(check["id"] == "qa_input_ledger" for check in qa["checks"])
    assert any(check["id"] == "qa_quick_match_intake_contract" for check in qa["checks"])
    assert any(check["id"] == "qa_quick_match_intake_contract_export" for check in qa["checks"])
    assert any(check["id"] == "qa_quick_match_lab_intake_sheet" for check in qa["checks"])
    assert any(check["id"] == "qa_quick_match_lab_intake_sheet_export" for check in qa["checks"])
    assert any(check["id"] == "qa_intake_precision_audit" for check in qa["checks"])
    assert any(check["id"] == "qa_intake_precision_export" for check in qa["checks"])
    assert any(check["id"] == "qa_artifact_catalog" for check in qa["checks"])
    assert any(check["id"] == "qa_schema_registry" for check in qa["checks"])
    assert any(check["id"] == "qa_evidence_library" for check in qa["checks"])
    assert any(check["id"] == "qa_evidence_library_export" for check in qa["checks"])
    assert any(check["id"] == "qa_evidence_coverage" for check in qa["checks"])
    assert any(check["id"] == "qa_evidence_coverage_export" for check in qa["checks"])
    assert any(check["id"] == "qa_measurement_timeline" for check in qa["checks"])
    assert any(check["id"] == "qa_page_health_matrix" for check in qa["checks"])
    assert any(check["id"] == "qa_page_health_matrix_export" for check in qa["checks"])
    assert any(check["id"] == "qa_runtime_doctor_export" for check in qa["checks"])
    assert any(check["id"] == "qa_public_beta_readiness_export" for check in qa["checks"])
    assert any(check["id"] == "qa_lab_readiness_export" for check in qa["checks"])
    assert any(check["id"] == "qa_measurement_intake_matrix_export" for check in qa["checks"])
    assert any(check["id"] == "qa_measurement_intake_matrix_csv_export" for check in qa["checks"])
    assert any(check["id"] == "qa_protocol_source_guide" for check in qa["checks"])
    assert any(check["id"] == "qa_protocol_source_guide_export" for check in qa["checks"])
    assert any(check["id"] == "qa_benchmark_log_entry_contract_export" for check in qa["checks"])
    assert any(check["id"] == "qa_alpha_dataset_template_exports" for check in qa["checks"])
    assert any(check["id"] == "qa_protocol_deviation_export" for check in qa["checks"])
    assert any(check["id"] == "qa_retest_interpretation_export" for check in qa["checks"])
    assert any(check["id"] == "qa_benchmark_worksheet_export" for check in qa["checks"])
    assert any(check["id"] == "qa_test_day_brief_export" for check in qa["checks"])
    assert any(check["id"] == "qa_test_day_command_board_export" for check in qa["checks"])
    assert any(check["id"] == "qa_test_session_operator_export" for check in qa["checks"])
    assert any(check["id"] == "qa_session_snapshot" for check in qa["checks"])


def test_release_qa_flags_missing_evidence_context():
    state, profile, passport, plan, _ = _demo_inputs()

    qa = build_release_qa(profile, passport, plan, state["benchmark_sessions"], state["feedback_by_week"], {})

    assert qa["status"] == "needs_review"
    assert any(check["status"] == "needs_review" for check in qa["checks"])


def test_release_qa_markdown_exports_checks():
    state, profile, passport, plan, evidence = _demo_inputs()
    qa = build_release_qa(profile, passport, plan, state["benchmark_sessions"], state["feedback_by_week"], evidence)
    markdown = release_qa_markdown(qa)

    assert "# SportRx Release QA" in markdown
    assert "ready_for_demo_review" in markdown
    assert "Checks" in markdown
