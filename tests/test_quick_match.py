from sportrx.quick_match import (
    build_quick_match_input_review,
    build_quick_match_intake_contract,
    build_quick_match_intake_quality,
    build_quick_match_lab_intake_sheet,
    quick_match,
    quick_match_intake_contract_markdown,
    quick_match_lab_intake_sheet_markdown,
)


def test_quick_match_returns_current_profile_match_without_talent_language():
    result = quick_match(
        {
            "age": 30,
            "training_days": 4,
            "weekly_training_minutes": 200,
            "running_minutes_per_week": 90,
            "longest_continuous_run_minutes": 30,
            "strength_days_per_week": 2,
            "high_intensity_sessions_last_4w": 4,
            "loaded_movement_sessions_last_4w": 4,
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "primary_goal": "first finish",
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["top_matches"]
    assert result["top_matches"][0]["event_profile"] == "Hybrid Race"
    assert "talent" not in result["language_guardrail"].lower()


def test_quick_match_marks_running_pack_registry_ready():
    result = quick_match(
        {
            "age": 28,
            "training_days": 2,
            "weekly_training_minutes": 80,
            "running_minutes_per_week": 60,
            "longest_continuous_run_minutes": 25,
            "strength_days_per_week": 0,
            "high_intensity_sessions_last_4w": 0,
            "loaded_movement_sessions_last_4w": 0,
            "available_days_per_week": 2,
            "max_minutes_per_session": 30,
        }
    )

    running_pack = [item for item in result["top_matches"] if item["pack_id"] == "running_5k_10k"][0]
    assert running_pack["pack_status"] == "registry_ready"


def test_quick_match_user_facing_output_uses_categories_not_fake_100s():
    result = quick_match(
        {
            "age": 30,
            "training_days": 7,
            "weekly_training_minutes": 420,
            "running_minutes_per_week": 180,
            "longest_continuous_run_minutes": 60,
            "strength_days_per_week": 4,
            "high_intensity_sessions_last_4w": 8,
            "loaded_movement_sessions_last_4w": 8,
            "available_days_per_week": 7,
            "max_minutes_per_session": 90,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert all("fit_category" in item for item in result["top_matches"])
    assert all("/100" not in item["fit_category"] for item in result["top_matches"])
    assert result["top_matches"][0]["why_it_fits"]


def test_quick_match_tie_does_not_return_same_strongest_and_gap():
    result = quick_match(
        {
            "age": 30,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "running_minutes_per_week": 60,
            "longest_continuous_run_minutes": 20,
            "strength_days_per_week": 1,
            "high_intensity_sessions_last_4w": 2,
            "loaded_movement_sessions_last_4w": 2,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["strongest_capability"] != result["obvious_limiter"]


def test_quick_match_ignores_measured_run_tests():
    profile = {
        "age": 30,
        "training_days": 3,
        "weekly_training_minutes": 120,
        "running_minutes_per_week": 60,
        "longest_continuous_run_minutes": 20,
        "strength_days_per_week": 1,
        "high_intensity_sessions_last_4w": 2,
        "loaded_movement_sessions_last_4w": 2,
        "available_days_per_week": 3,
        "max_minutes_per_session": 45,
        "symptoms": [],
        "known_conditions": [],
    }
    with_tests = {**profile, "one_km_run_seconds": 240, "five_km_run_seconds": 1500}

    assert quick_match(profile)["top_matches"] == quick_match(with_tests)["top_matches"]


def test_quick_match_explains_input_roles_without_turning_age_into_performance():
    profile = {
        "age": 30,
        "training_days": 3,
        "weekly_training_minutes": 120,
        "running_minutes_per_week": 60,
        "longest_continuous_run_minutes": 20,
        "strength_days_per_week": 1,
        "high_intensity_sessions_last_4w": 2,
        "loaded_movement_sessions_last_4w": 2,
        "available_days_per_week": 3,
        "max_minutes_per_session": 45,
        "primary_goal": "first finish",
        "symptoms": [],
        "known_conditions": [],
    }

    review = build_quick_match_input_review(profile)
    fields = {field["field_id"]: field for field in review["fields"]}

    assert review["quality_status"] == "usable_behavior_snapshot"
    assert fields["age"]["affects"] == "Safety Gate / adult-scope check"
    assert "does not raise or lower Quick Match" in fields["age"]["role"]
    assert fields["max_minutes_per_session"]["affects"] == "Training Block / Prescription"
    assert review["missing_fields"] == []
    assert "readiness score" in review["claim_boundary"]


def test_quick_match_result_carries_input_review():
    result = quick_match(
        {
            "age": 30,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "running_minutes_per_week": 60,
            "longest_continuous_run_minutes": 20,
            "strength_days_per_week": 1,
            "high_intensity_sessions_last_4w": 2,
            "loaded_movement_sessions_last_4w": 2,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "primary_goal": "first finish",
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["input_review"]["behavior_fields_collected"] == 7
    assert result["intake_contract"]["schema"] == "sportrx.quick_match_intake_contract"
    assert result["intake_contract"]["status"] == "contract_ready"
    assert result["input_review"]["context_fields_collected"] == 4
    assert result["intake_quality"]["schema"] == "sportrx.quick_match_intake_quality"
    assert result["intake_quality"]["status"] == "ready_for_quick_match_routing"
    assert result["lab_intake_sheet"]["schema"] == "sportrx.quick_match_lab_intake_sheet"
    assert result["lab_intake_sheet"]["status"] == "ready_for_self_report_routing"


def test_quick_match_intake_contract_explains_numeric_input_boundary():
    contract = build_quick_match_intake_contract(
        {
            "age": 30,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "running_minutes_per_week": 60,
            "longest_continuous_run_minutes": 20,
            "strength_days_per_week": 1,
            "high_intensity_sessions_last_4w": 2,
            "loaded_movement_sessions_last_4w": 2,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "primary_goal": "first finish",
            "one_km_run_seconds": 300,
        }
    )

    assert contract["status"] == "contract_ready"
    assert contract["group_count"] == 3
    assert contract["required_numeric_fields"] == 10
    assert contract["excluded_measured_fields_present"] == ["one_km_run_seconds"]
    assert "background identity" in contract["primary_message"]
    assert "Quick Match does not use them" in contract["excluded_measurement_policy"]
    assert all(group["label"] != "Adaptability" for group in contract["groups"])


def test_quick_match_intake_contract_flags_legacy_subjective_values():
    contract = build_quick_match_intake_contract(
        {
            "age": 30,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "running_minutes_per_week": 60,
            "longest_continuous_run_minutes": 20,
            "strength_days_per_week": 1,
            "high_intensity_sessions_last_4w": 2,
            "loaded_movement_sessions_last_4w": 2,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "primary_goal": "first finish",
            "running_comfort": 5,
        }
    )

    assert contract["status"] == "legacy_subjective_values_present"
    assert contract["legacy_subjective_fields_present"] == ["running_comfort"]


def test_quick_match_intake_contract_markdown_exports_groups_and_exclusions():
    markdown = quick_match_intake_contract_markdown(
        build_quick_match_intake_contract(
            {
                "age": 30,
                "training_days": 3,
                "weekly_training_minutes": 120,
                "running_minutes_per_week": 60,
                "longest_continuous_run_minutes": 20,
                "strength_days_per_week": 1,
                "high_intensity_sessions_last_4w": 2,
                "loaded_movement_sessions_last_4w": 2,
                "available_days_per_week": 3,
                "max_minutes_per_session": 45,
                "primary_goal": "first finish",
            }
        )
    )

    assert "# SportRx Quick Match Intake Contract" in markdown
    assert "Recent behavior" in markdown
    assert "Excluded from Quick Match" in markdown


def test_quick_match_ignores_legacy_subjective_background_ratings():
    profile = {
        "age": 30,
        "training_days": 3,
        "weekly_training_minutes": 120,
        "running_minutes_per_week": 60,
        "longest_continuous_run_minutes": 20,
        "strength_days_per_week": 1,
        "high_intensity_sessions_last_4w": 2,
        "loaded_movement_sessions_last_4w": 2,
        "available_days_per_week": 3,
        "max_minutes_per_session": 45,
        "symptoms": [],
        "known_conditions": [],
    }
    with_legacy_ratings = {
        **profile,
        "endurance_background": 5,
        "resistance_background": 5,
        "running_comfort": 5,
        "hiit_comfort": 5,
        "loaded_movement_comfort": 5,
    }

    assert quick_match(profile)["top_matches"] == quick_match(with_legacy_ratings)["top_matches"]


def test_intake_quality_routes_sparse_behavior_to_benchmark_first():
    quality = build_quick_match_intake_quality(
        {
            "age": 30,
            "training_days": 0,
            "weekly_training_minutes": 0,
            "running_minutes_per_week": 0,
            "longest_continuous_run_minutes": 0,
            "strength_days_per_week": 0,
            "high_intensity_sessions_last_4w": 0,
            "loaded_movement_sessions_last_4w": 0,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "primary_goal": "first finish",
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert quality["status"] == "low_behavior_signal"
    assert quality["nonzero_behavior_fields"] == []
    assert "Hybrid Benchmark" in quality["next_action"]


def test_intake_quality_lists_legacy_subjective_fields_as_ignored():
    quality = build_quick_match_intake_quality(
        {
            "age": 30,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "running_minutes_per_week": 60,
            "longest_continuous_run_minutes": 20,
            "strength_days_per_week": 1,
            "high_intensity_sessions_last_4w": 2,
            "loaded_movement_sessions_last_4w": 2,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "primary_goal": "first finish",
            "running_comfort": 5,
            "hiit_comfort": 5,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert quality["status"] == "ready_for_quick_match_routing"
    assert quality["legacy_ignored_fields"] == ["running_comfort", "hiit_comfort"]
    assert any(card["label"] == "Legacy Ignored" and card["status"] == "waiting" for card in quality["cards"])


def test_intake_quality_safety_gate_blocks_routing():
    quality = build_quick_match_intake_quality(
        {
            "age": 40,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "running_minutes_per_week": 60,
            "longest_continuous_run_minutes": 20,
            "strength_days_per_week": 1,
            "high_intensity_sessions_last_4w": 2,
            "loaded_movement_sessions_last_4w": 2,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "primary_goal": "first finish",
            "symptoms": ["chest_pain"],
            "known_conditions": [],
        }
    )

    assert quality["status"] == "blocked_by_safety_gate"
    assert "Safety Gate" in quality["next_action"]


def test_lab_intake_sheet_makes_quick_match_feel_like_direct_number_record():
    sheet = build_quick_match_lab_intake_sheet(
        {
            "age": 30,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "running_minutes_per_week": 60,
            "longest_continuous_run_minutes": 20,
            "strength_days_per_week": 1,
            "high_intensity_sessions_last_4w": 2,
            "loaded_movement_sessions_last_4w": 2,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "primary_goal": "first finish",
            "one_km_run_seconds": 300,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert sheet["status"] == "ready_for_self_report_routing"
    assert sheet["collected_fields"] == sheet["total_fields"]
    assert sheet["measured_fields_present_but_ignored"] == ["one_km_run_seconds"]
    assert "does not measure performance" in sheet["primary_message"]
    assert "Not tested" in sheet["not_tested_policy"]
    assert any(section["label"] == "Past 4 weeks" for section in sheet["sections"])
    assert any(card["label"] == "Measured performance" and card["value"] == "0 used" for card in sheet["cards"])


def test_lab_intake_sheet_routes_sparse_or_blocked_records_before_matching_claims():
    sparse_sheet = build_quick_match_lab_intake_sheet(
        {
            "age": 30,
            "training_days": 0,
            "weekly_training_minutes": 0,
            "running_minutes_per_week": 0,
            "longest_continuous_run_minutes": 0,
            "strength_days_per_week": 0,
            "high_intensity_sessions_last_4w": 0,
            "loaded_movement_sessions_last_4w": 0,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "primary_goal": "first finish",
            "symptoms": [],
            "known_conditions": [],
        }
    )
    blocked_sheet = build_quick_match_lab_intake_sheet(
        {
            "age": 30,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "running_minutes_per_week": 60,
            "longest_continuous_run_minutes": 20,
            "strength_days_per_week": 1,
            "high_intensity_sessions_last_4w": 2,
            "loaded_movement_sessions_last_4w": 2,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "primary_goal": "first finish",
            "symptoms": ["chest_pain"],
            "known_conditions": [],
        }
    )

    assert sparse_sheet["status"] == "benchmark_first"
    assert "Hybrid Benchmark" in sparse_sheet["next_action"]
    assert blocked_sheet["status"] == "safety_gate_first"
    assert "Safety Gate" in blocked_sheet["next_action"]


def test_lab_intake_sheet_markdown_exports_boundary_and_sections():
    markdown = quick_match_lab_intake_sheet_markdown(
        build_quick_match_lab_intake_sheet(
            {
                "age": 30,
                "training_days": 3,
                "weekly_training_minutes": 120,
                "running_minutes_per_week": 60,
                "longest_continuous_run_minutes": 20,
                "strength_days_per_week": 1,
                "high_intensity_sessions_last_4w": 2,
                "loaded_movement_sessions_last_4w": 2,
                "available_days_per_week": 3,
                "max_minutes_per_session": 45,
                "primary_goal": "first finish",
                "symptoms": [],
                "known_conditions": [],
            }
        )
    )

    assert "# SportRx Quick Match Lab Intake Sheet" in markdown
    assert "Past 4 weeks" in markdown
    assert "does not measure performance" in markdown
    assert "validated assessment" in markdown
