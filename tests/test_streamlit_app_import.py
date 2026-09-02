import importlib


def test_streamlit_app_imports():
    module = importlib.import_module("app.streamlit_app")

    assert hasattr(module, "main")
    assert hasattr(module, "aerobic_v01_app")
    assert hasattr(module, "_hero_status_console")
    assert hasattr(module, "_demo_experience_console")
    assert hasattr(module, "_demo_experience_sequence_rows")
    assert hasattr(module, "_v01_developer_mode")
    assert hasattr(module, "_guided_review_console")
    assert hasattr(module, "_guided_action_rail")
    assert hasattr(module, "_guided_review_step_rows")
    assert hasattr(module, "_lab_workflow_board")
    assert hasattr(module, "_report_dashboard")
    assert hasattr(module, "_training_profile_handoff_board")
    assert hasattr(module, "_profile_dimension_cards")
    assert hasattr(module, "_profile_basis_text")
    assert hasattr(module, "_measured_profile_summary")
    assert hasattr(module, "_benchmark_log_dashboard")
    assert hasattr(module, "_benchmark_session_gallery")
    assert hasattr(module, "_benchmark_draft_session_board")
    assert hasattr(module, "_release_candidate_console")
    assert hasattr(module, "_release_reviewer_brief")
    assert hasattr(module, "_public_beta_console")
    assert hasattr(module, "_evidence_coverage_console")
    assert hasattr(module, "_evidence_library_console")
    assert hasattr(module, "_evidence_topic_cards")
    assert hasattr(module, "_evidence_source_cards")
    assert hasattr(module, "_evidence_claim_boundary_board")
    assert hasattr(module, "_evidence_library_rows")
    assert hasattr(module, "knowledge_lab_page")
    assert hasattr(module, "_page_health_rows")
    assert hasattr(module, "_validation_readiness_console")
    assert hasattr(module, "_validation_phase_rows")
    assert hasattr(module, "_validation_capture_rows")
    assert hasattr(module, "_self_use_protocol_console")
    assert hasattr(module, "_self_use_week_rows")
    assert hasattr(module, "_self_use_field_rows")
    assert hasattr(module, "_open_source_integration_console")
    assert hasattr(module, "_terminology_rows")
    assert hasattr(module, "_terminology_rule_rows")
    assert hasattr(module, "_terminology_blocked_rows")
    assert hasattr(module, "_export_center_console")
    assert hasattr(module, "_export_release_package_board")
    assert hasattr(module, "_review_pack_integrity_rows")
    assert hasattr(module, "_schema_registry_console")
    assert hasattr(module, "_demo_scenario_matrix_console")
    assert hasattr(module, "_scenario_switcher")
    assert hasattr(module, "_reviewer_session_plan_console")
    assert hasattr(module, "_workbench_launch_selector")
    assert hasattr(module, "_trial_mode_launcher")
    assert hasattr(module, "_mobile_nav")
    assert hasattr(module, "public_home_page")
    assert hasattr(module, "public_quick_match_page")
    assert hasattr(module, "public_benchmark_page")
    assert hasattr(module, "public_profile_page")
    assert hasattr(module, "_quick_match_input_console")
    assert hasattr(module, "_quick_match_contract_console")
    assert hasattr(module, "_quick_match_intake_console")
    assert hasattr(module, "_quick_match_match_cards")
    assert hasattr(module, "_quick_match_reason_label")
    assert hasattr(module, "_intake_precision_console")
    assert hasattr(module, "_intake_precision_rows")
    assert hasattr(module, "_measured_number_input")
    assert hasattr(module, "_test_status")
    assert hasattr(module, "_protocol_source_choice")
    assert hasattr(module, "_protocol_source_value")
    assert hasattr(module, "_session_quality_console")
    assert hasattr(module, "_session_quality_rows")
    assert hasattr(module, "_protocol_deviation_console")
    assert hasattr(module, "_protocol_deviation_component_rows")
    assert hasattr(module, "_protocol_deviation_retest_rows")
    assert hasattr(module, "_retest_interpretation_console")
    assert hasattr(module, "_retest_interpretation_rows")
    assert hasattr(module, "_measurement_intake_matrix_console")
    assert hasattr(module, "_lab_component_board")
    assert hasattr(module, "_lab_measured_picture_cards")
    assert hasattr(module, "_measurement_intake_rows")
    assert hasattr(module, "_lab_measurement_review")
    assert hasattr(module, "_lab_test_quality_console")
    assert hasattr(module, "_protocol_source_guide_console")
    assert hasattr(module, "_protocol_source_rows")
    assert hasattr(module, "_benchmark_protocol_console")
    assert hasattr(module, "_benchmark_protocol_components")
    assert hasattr(module, "_test_session_operator_console")
    assert hasattr(module, "_operator_flow_board")
    assert hasattr(module, "_operator_component_cards")
    assert hasattr(module, "_quality_review_panel")
    assert hasattr(module, "_training_block_console")
    assert hasattr(module, "_training_week_cards")
    assert hasattr(module, "_training_range_label")
    assert hasattr(module, "_feedback_loop_console")
    assert hasattr(module, "_feedback_loop_snapshot")
    assert hasattr(module, "_feedback_decision_panel")
    assert hasattr(module, "_weekly_feedback_cards")
    assert hasattr(module, "_retest_loop_cards")
    assert hasattr(module, "_feedback_percent_label")
    assert hasattr(module, "_pilot_review_console")
    assert hasattr(module, "_alpha_dataset_template_console")
    assert hasattr(module, "_alpha_dataset_table_rows")

    assert module._protocol_source_choice("Custom protocol v1") == "Other documented protocol"
    assert module._protocol_source_value("Other documented protocol", "Custom protocol v1") == "Custom protocol v1"
    assert module._protocol_source_value("Benchmark Log import") == "Benchmark Log import"
    assert module._training_range_label((5, 6)) == "5-6"
    assert module._feedback_percent_label(0.82) == "82%"
    assert module._feedback_percent_label(None) == "未填写"
    assert module._quick_match_reason_label("120 total training min/week reported") == "120 分钟/周训练总量（自报）"
    assert module._v01_activity("cycling") == "骑行"
    assert module._v01_exercise_label({"name": "stationary bike walk"}) == "立式单车轻松骑"
    cycling_suggestions = module._v01_discovery_exercises("cycling")
    assert len(cycling_suggestions) == 3
    assert {item["name"] for item in cycling_suggestions} == {
        "stationary bike run v. 3",
        "cycle cross trainer",
        "stationary bike walk",
    }
    assert module._v01_intensity("light_to_moderate") == "轻松到中等"
    assert module._v01_fitness_class("inactive") == "目前运动不足"


def test_developer_mode_is_explicitly_opt_in(monkeypatch):
    module = importlib.import_module("app.streamlit_app")

    monkeypatch.delenv("SPORT_RX_DEVELOPER_MODE", raising=False)
    assert module._v01_developer_mode() is False

    monkeypatch.setenv("SPORT_RX_DEVELOPER_MODE", "1")
    assert module._v01_developer_mode() is True
