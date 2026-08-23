from sportrx.performance_lab import assess_hybrid_performance, measurement_intake_matrix_csv, measurement_intake_matrix_markdown


def test_hybrid_lab_works_without_equipment_tests():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 3,
            "weekly_training_minutes": 150,
            "running_minutes_per_week": 60,
            "strength_days_per_week": 1,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "high_intensity_sessions_last_4w": 3,
            "loaded_movement_sessions_last_4w": 2,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["assessment_completeness"] in {"LOW", "MODERATE"}
    assert result["readiness_score"] is not None
    assert set(result["dimension_scores"]) == {
        "running_capacity",
        "aerobic_base",
        "strength_endurance",
        "station_experience",
        "work_capacity",
    }
    assert result["dimension_scores"]["strength_endurance"] is None
    assert result["training_context"]["days_available_per_week"] == 3
    assert result["training_context"]["high_intensity_exposure"] == "3 session(s) in last 4 weeks"
    assert "time_capacity" not in result["dimension_scores"]
    assert result["metric_sources"]["schema"] == "sportrx.metric_source_register"
    assert result["measurement_review"]["schema"] == "sportrx.lab_measurement_review"
    assert result["measurement_review"]["comparison_ready"] is False
    assert result["measurement_intake_matrix"]["schema"] == "sportrx.measurement_intake_matrix"
    assert result["measurement_intake_matrix"]["summary"]["not_tested"] >= 1


def test_hybrid_lab_reports_high_completeness_with_optional_tests():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 220,
            "running_minutes_per_week": 120,
            "strength_days_per_week": 2,
            "available_days_per_week": 5,
            "max_minutes_per_session": 60,
            "one_km_run_seconds": 270,
            "five_km_run_seconds": 1650,
            "one_km_row_seconds": 260,
            "one_km_ski_seconds": 290,
            "station_test_score": 75,
            "work_capacity_test_score": 70,
            "station_test_protocol": "SportRx Hybrid Benchmark v1",
            "work_capacity_test_protocol": "SportRx Hybrid Benchmark v1",
            "resting_hr": 58,
            "vo2max": 45,
            "hrmax": 190,
            "equipment_access": ["row", "ski", "sled"],
            "high_intensity_sessions_last_4w": 4,
            "loaded_movement_sessions_last_4w": 4,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["assessment_completeness"] == "HIGH"
    assert result["measurement_review"]["comparison_ready"] is True
    assert result["measurement_review"]["measured_test_count"] == 6
    assert result["lab_test_quality"]["status"] == "review_ready_measurement_record"


def test_missing_running_data_stays_missing():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 3,
            "weekly_training_minutes": 150,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    running = result["performance_profile"]["running_capacity"]
    assert running["score"] is None
    assert running["status"] == "Not tested"
    assert "No recent 1 km or 5 km run test" in result["what_we_do_not_know"]


def test_missing_station_data_stays_missing_without_midpoint_score():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 3,
            "weekly_training_minutes": 150,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["performance_profile"]["station_experience"]["score"] is None
    assert result["performance_profile"]["station_experience"]["status"] == "Not tested"


def test_equal_dimension_scores_report_balanced_not_same_strongest_and_limiter():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 180,
            "running_minutes_per_week": 90,
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "one_km_run_seconds": 300,
            "station_test_score": 75,
            "work_capacity_test_score": 75,
            "station_test_protocol": "SportRx Hybrid Benchmark v1",
            "work_capacity_test_protocol": "SportRx Hybrid Benchmark v1",
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["strongest_area"] != result["main_gap"]
    assert result["main_gap"] != result["strongest_area"]


def test_tied_lowest_dimensions_are_reported_together():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 180,
            "running_minutes_per_week": 90,
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "one_km_run_seconds": 270,
            "station_test_score": 40,
            "work_capacity_test_score": 40,
            "station_test_protocol": "SportRx Hybrid Benchmark v1",
            "work_capacity_test_protocol": "SportRx Hybrid Benchmark v1",
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert "Strength endurance" in result["main_development_areas"]
    assert "Work capacity" in result["main_development_areas"]


def test_performance_and_training_context_are_separate():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 1,
            "weekly_training_minutes": 30,
            "available_days_per_week": 7,
            "max_minutes_per_session": 90,
            "one_km_run_seconds": 300,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert "time_capacity" not in result["dimension_scores"]
    assert result["training_context"]["days_available_per_week"] == 7
    assert result["strongest_area"] != "training time capacity"


def test_assessment_completeness_counts_assessed_areas_only():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "one_km_run_seconds": 300,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["areas_assessed"]["assessed"] == 1
    assert result["areas_assessed"]["label"] == "1 of 5 key areas assessed"
    assert result["readiness_category"] == "Not enough measured data"


def test_unused_lab_values_do_not_change_outputs():
    profile = {
        "age": 35,
        "training_days": 4,
        "weekly_training_minutes": 180,
        "running_minutes_per_week": 90,
        "available_days_per_week": 4,
        "max_minutes_per_session": 45,
        "one_km_run_seconds": 300,
        "station_test_score": 70,
        "symptoms": [],
        "known_conditions": [],
    }
    with_unused = {**profile, "vo2max": 65, "hrmax": 205, "resting_hr": 42}

    base = assess_hybrid_performance(profile)
    changed = assess_hybrid_performance(with_unused)

    assert base["performance_profile"] == changed["performance_profile"]
    assert base["training_context"] == changed["training_context"]
    assert changed["metric_sources"]["summary"]["unsupported_inputs"] == 3


def test_safety_gate_does_not_modify_measured_performance():
    profile = {
        "age": 35,
        "training_days": 4,
        "weekly_training_minutes": 180,
        "running_minutes_per_week": 90,
        "available_days_per_week": 4,
        "max_minutes_per_session": 45,
        "one_km_run_seconds": 300,
        "station_test_score": 70,
        "symptoms": [],
        "known_conditions": [],
    }
    red_profile = {**profile, "symptoms": ["chest_pain"]}

    base = assess_hybrid_performance(profile)
    red = assess_hybrid_performance(red_profile)

    assert red["safety_gate"]["status"] == "RED"
    assert base["performance_profile"] == red["performance_profile"]
    assert red["measurement_review"]["status"] == "blocked"


def test_lab_measurement_review_keeps_context_separate_from_measured_tests():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 180,
            "running_minutes_per_week": 90,
            "strength_days_per_week": 2,
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "one_km_run_seconds": 300,
            "symptoms": [],
            "known_conditions": [],
        }
    )
    review = result["measurement_review"]
    context = {item["field_id"]: item for item in review["context_fields"]}
    tests = {item["field_id"]: item for item in review["test_fields"]}

    assert tests["one_km_run_seconds"]["status"] == "measured"
    assert tests["five_km_run_seconds"]["status"] == "not_tested"
    assert context["weekly_training_minutes"]["status"] == "self_reported"
    assert "not used for measured" in context["training_days"]["role"]
    assert review["measured_performance_area_count"] == 1


def test_lab_test_quality_flags_protocol_scores_without_source():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 180,
            "running_minutes_per_week": 90,
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "one_km_run_seconds": 300,
            "station_test_score": 70,
            "work_capacity_test_score": 65,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    quality = result["lab_test_quality"]

    assert quality["schema"] == "sportrx.lab_test_quality"
    assert quality["status"] == "needs_protocol_source"
    assert quality["missing_protocol_sources"] == ["station_test_score", "work_capacity_test_score"]
    assert result["performance_profile"]["strength_endurance"]["score"] is None
    assert result["performance_profile"]["work_capacity"]["score"] is None
    assert result["measurement_review"]["needs_protocol_test_count"] == 2


def test_lab_test_quality_requires_protocol_source_before_scores_count():
    profile = {
        "age": 35,
        "training_days": 4,
        "weekly_training_minutes": 180,
        "running_minutes_per_week": 90,
        "available_days_per_week": 4,
        "max_minutes_per_session": 45,
        "one_km_run_seconds": 300,
        "station_test_score": 70,
        "work_capacity_test_score": 65,
        "symptoms": [],
        "known_conditions": [],
    }
    with_sources = {
        **profile,
        "station_test_protocol": "SportRx Hybrid Benchmark v1",
        "work_capacity_test_protocol": "SportRx Hybrid Benchmark v1",
    }

    base = assess_hybrid_performance(profile)
    sourced = assess_hybrid_performance(with_sources)

    assert base["performance_profile"]["strength_endurance"]["score"] is None
    assert base["performance_profile"]["work_capacity"]["score"] is None
    assert sourced["performance_profile"]["strength_endurance"]["score"] == 70
    assert sourced["performance_profile"]["work_capacity"]["score"] == 65
    assert sourced["lab_test_quality"]["status"] == "review_ready_measurement_record"
    assert sourced["lab_test_quality"]["missing_protocol_sources"] == []


def test_measurement_intake_matrix_flags_missing_protocol_source():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 180,
            "running_minutes_per_week": 90,
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "one_km_run_seconds": 300,
            "station_test_score": 70,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    matrix = result["measurement_intake_matrix"]
    rows = {row["field_id"]: row for row in matrix["rows"]}

    assert matrix["status"] == "needs_protocol_source"
    assert matrix["summary"]["missing_protocol_source"] == 1
    assert rows["one_km_run_seconds"]["status"] == "measured_review_ready"
    assert rows["station_test_score"]["status"] == "measured_needs_protocol"
    assert rows["five_km_run_seconds"]["status"] == "not_tested"
    assert "does not create scores" in matrix["claim_boundary"]


def test_measurement_intake_matrix_ready_when_sources_and_dimensions_exist():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 180,
            "running_minutes_per_week": 90,
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "one_km_run_seconds": 300,
            "station_test_score": 70,
            "station_test_protocol": "SportRx Hybrid Benchmark v1",
            "symptoms": [],
            "known_conditions": [],
        }
    )

    matrix = result["measurement_intake_matrix"]

    assert matrix["status"] == "measurement_matrix_ready"
    assert matrix["summary"]["comparison_ready"] is True
    assert matrix["summary"]["review_ready"] == 2


def test_measurement_intake_matrix_markdown_exports_review_table():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "one_km_run_seconds": 300,
            "station_test_score": 70,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    markdown = measurement_intake_matrix_markdown(result["measurement_intake_matrix"])

    assert "# SportRx Measurement Intake Matrix" in markdown
    assert "| Test | Dimension | Status |" in markdown
    assert "1 km run" in markdown
    assert "station_test_score" not in markdown
    assert "does not create scores" in markdown


def test_measurement_intake_matrix_csv_exports_spreadsheet_rows():
    result = assess_hybrid_performance(
        {
            "age": 35,
            "one_km_run_seconds": 300,
            "station_test_score": 70,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    exported = measurement_intake_matrix_csv(result["measurement_intake_matrix"])

    assert "field_id,test,dimension,status" in exported
    assert "one_km_run_seconds,1 km run,Running,measured_review_ready" in exported
    assert "station_test_score,Station circuit" in exported
    assert "five_km_run_seconds,5 km run,Running,not_tested" in exported
