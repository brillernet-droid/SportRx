from sportrx.passport import build_readiness_passport
from sportrx.report import build_training_profile_report, report_markdown


def test_training_profile_report_summarizes_passport_without_predictions():
    passport = build_readiness_passport(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 180,
            "running_minutes_per_week": 90,
            "one_km_run_seconds": 300,
            "station_test_score": 70,
            "station_test_protocol": "SportRx Hybrid Benchmark v1 0.1 / standard / Benchmark Log 2026-08-22",
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    report = build_training_profile_report(passport, report_date="2026-08-22")

    assert report["schema"] == "sportrx.training_profile_report"
    assert report["event_profile"] == "Hybrid Race"
    assert report["measurement"]["measured_performance_areas"]["count"] >= 2
    assert report["measurement"]["lab_test_quality"]["status"] == "review_ready_measurement_record"
    assert report["performance_rows"]
    assert report["metric_sources"]["schema"] == "sportrx.metric_source_register"
    assert report["output_prerequisites"]["schema"] == "sportrx.output_prerequisites"
    assert "race prediction" in report["claim_boundary"]
    assert "validated percentiles" in report["claim_boundary"]


def test_report_markdown_keeps_missing_values_explicit():
    passport = build_readiness_passport(
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
    report = build_training_profile_report(passport, report_date="2026-08-22")
    markdown = report_markdown(report)

    assert "# SportRx Training Profile Report" in markdown
    assert "Not tested" in markdown
    assert "Benchmark needed before tailored training" in markdown
    assert "Claim Boundary" in markdown
    assert "Metric Sources" in markdown
    assert "Output Prerequisites" in markdown
    assert "Lab test quality" in markdown
