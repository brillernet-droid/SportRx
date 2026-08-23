from sportrx.passport import build_readiness_passport


def test_passport_contains_required_fields():
    result = build_readiness_passport(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 200,
            "running_minutes_per_week": 100,
            "longest_continuous_run_minutes": 35,
            "strength_days_per_week": 2,
            "available_days_per_week": 4,
            "max_minutes_per_session": 60,
            "high_intensity_sessions_last_4w": 4,
            "loaded_movement_sessions_last_4w": 4,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    for key in [
        "event_profile_match",
        "experimental_readiness_score",
        "current_measured_picture",
        "safety_gate",
        "athlete_type",
        "dimension_scores",
        "performance_profile",
        "training_context",
        "metric_sources",
        "lab_test_quality",
        "output_prerequisites",
        "strongest_capability",
        "primary_limiter",
        "what_we_know",
        "what_we_do_not_know",
        "what_to_measure_next",
        "top_3_priorities",
        "assessment_completeness",
        "next_action",
        "rule_evidence_explanation",
    ]:
        assert key in result


def test_passport_red_safety_blocks_starter_path():
    result = build_readiness_passport({"age": 40, "symptoms": ["chest_pain"], "known_conditions": []})

    assert result["safety_gate"]["status"] == "RED"
    assert result["starter_path"]["available"] is False


def test_passport_routes_to_benchmark_when_not_enough_measured_data():
    result = build_readiness_passport(
        {
            "age": 35,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["measured_performance_areas"]["count"] < 2
    assert result["starter_path"]["available"] is False
    assert "Hybrid Benchmark" in result["starter_path"]["reason"]


def test_passport_result_does_not_require_experimental_score():
    result = build_readiness_passport({"age": 40, "symptoms": ["chest_pain"], "known_conditions": []})

    assert result["experimental_readiness_score"] is None
    assert result["current_measured_picture"] == "Training handoff blocked"
    assert result["readiness_category"] == "Training handoff blocked"
