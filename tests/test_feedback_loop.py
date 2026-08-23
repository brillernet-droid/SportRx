from sportrx.benchmark_log import build_component_result, create_benchmark_session
from sportrx.feedback_loop import build_feedback_dashboard, feedback_dashboard_markdown
from sportrx.prescription import generate_prescription


def _plan():
    return generate_prescription(
        {
            "age": 35,
            "exercise_days_last_4w": 3,
            "mvpa_minutes_per_week": 120,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "preferred_activity": "running",
            "symptoms": [],
            "known_conditions": [],
        }
    )


def test_feedback_dashboard_handles_missing_plan():
    dashboard = build_feedback_dashboard({"weeks": []}, {}, [])

    assert dashboard["available"] is False
    assert dashboard["adherence"]["status"] == "No weekly feedback recorded"
    assert "predictions" in dashboard["claim_boundary"]


def test_feedback_dashboard_summarizes_weekly_feedback():
    plan = _plan()
    dashboard = build_feedback_dashboard(
        plan,
        {1: {"completed_sessions": 3, "average_rpe": 5, "felt_too_hard": False, "adverse_event": False}},
        [],
    )

    assert dashboard["available"] is True
    assert dashboard["adherence"]["weeks_recorded"] == 1
    assert dashboard["adherence"]["completed_sessions"] == 3
    assert dashboard["adherence"]["average_completion_rate"] == 1.0
    assert dashboard["weekly_feedback"][0]["decision_action"] in {"not_entered", "small_increase"}
    assert dashboard["weekly_feedback"][0]["reason_codes"]
    assert dashboard["plan_actual_reasons"]


def test_feedback_dashboard_includes_raw_retest_comparisons():
    first = create_benchmark_session(
        {"equipment_access": ["row"]},
        [build_component_result("run_1km", value=370, value_unit="seconds", rpe_0_10=7)],
        session_date="2026-08-01",
    )
    second = create_benchmark_session(
        {"equipment_access": ["row"]},
        [build_component_result("run_1km", value=355, value_unit="seconds", rpe_0_10=7)],
        session_date="2026-08-29",
    )

    dashboard = build_feedback_dashboard(_plan(), {}, [first, second])

    assert dashboard["benchmark_summary"]["retest_ready"] is True
    assert dashboard["retest_comparisons"][0]["direction"] == "improved"
    assert "prediction" in dashboard["retest_comparisons"][0]["claim_boundary"]


def test_feedback_dashboard_markdown_exports_summary():
    dashboard = build_feedback_dashboard(_plan(), {}, [])
    markdown = feedback_dashboard_markdown(dashboard)

    assert "# SportRx Feedback Loop Dashboard" in markdown
    assert "No repeated benchmark components yet" in markdown
    assert "Claim boundary" in markdown
    assert "Plan-Actual Reason Codes" in markdown
