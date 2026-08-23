from sportrx.metric_sources import build_metric_source_register
from sportrx.performance_lab import assess_hybrid_performance


def test_metric_source_register_labels_measured_reported_and_not_tested():
    profile = {
        "age": 35,
        "training_days": 3,
        "weekly_training_minutes": 120,
        "running_minutes_per_week": 60,
        "one_km_run_seconds": 300,
        "available_days_per_week": 3,
        "max_minutes_per_session": 45,
        "symptoms": [],
        "known_conditions": [],
    }
    result = assess_hybrid_performance(profile)
    register = result["metric_sources"]

    sources = {item["metric_id"]: item for item in register["performance_metrics"]}

    assert sources["running_capacity"]["source_type"] == "measured"
    assert sources["running_capacity"]["affects_output"] is True
    assert sources["aerobic_base"]["source_type"] == "self_reported"
    assert "not used to compare strongest area" in sources["aerobic_base"]["output_role"]
    assert sources["strength_endurance"]["source_type"] == "not_tested"
    assert sources["strength_endurance"]["affects_output"] is False
    assert register["summary"]["measured_performance_metrics"] == 1


def test_metric_source_register_marks_unsupported_inputs_as_ignored():
    profile = {
        "age": 35,
        "training_days": 4,
        "weekly_training_minutes": 180,
        "running_minutes_per_week": 90,
        "one_km_run_seconds": 300,
        "station_test_score": 70,
        "available_days_per_week": 4,
        "max_minutes_per_session": 45,
        "vo2max": 55,
        "hrmax": 190,
        "resting_hr": 50,
        "symptoms": [],
        "known_conditions": [],
    }
    result = assess_hybrid_performance(profile)
    unsupported = {item["metric_id"]: item for item in result["metric_sources"]["unsupported_inputs"]}

    assert set(unsupported) == {"vo2max", "hrmax", "resting_hr"}
    assert all(item["affects_output"] is False for item in unsupported.values())
    assert all(item["source_type"] == "unsupported" for item in unsupported.values())


def test_metric_source_register_tracks_protocol_provenance_separately():
    profile = {
        "age": 35,
        "training_days": 4,
        "weekly_training_minutes": 180,
        "running_minutes_per_week": 90,
        "station_test_score": 70,
        "station_test_protocol": "SportRx Hybrid Benchmark v1 0.1 / standard / Benchmark Log 2026-08-22",
        "available_days_per_week": 4,
        "max_minutes_per_session": 45,
        "symptoms": [],
        "known_conditions": [],
    }
    result = assess_hybrid_performance(profile)
    protocol = {item["metric_id"]: item for item in result["metric_sources"]["protocol_metrics"]}

    assert protocol["station_test_protocol"]["source_type"] == "protocol_provenance"
    assert protocol["station_test_protocol"]["affects_output"] is True
    assert "review readiness" in protocol["station_test_protocol"]["output_role"]
    assert protocol["work_capacity_test_protocol"]["source_type"] == "not_tested"
    assert result["metric_sources"]["summary"]["protocol_provenance_metrics"] == 1


def test_metric_source_register_can_be_built_directly():
    profile = {"symptoms": ["chest_pain"], "known_conditions": []}
    performance_profile = {
        "running_capacity": {
            "label": "Running",
            "score": None,
            "source": "missing",
            "evidence": [],
            "missing": ["No run test"],
        }
    }
    training_context = {"days_available_per_week": 3, "minutes_available_per_session": 45}
    safety_gate = {"status": "RED"}

    register = build_metric_source_register(profile, performance_profile, training_context, safety_gate)

    assert register["schema"] == "sportrx.metric_source_register"
    assert register["safety_metrics"][0]["source_type"] == "safety_screen"
    assert "never raises or lowers measured performance" in register["safety_metrics"][0]["output_role"]
