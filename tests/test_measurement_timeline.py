from sportrx.benchmark_log import summarize_benchmark_sessions
from sportrx.demo_seed import build_demo_state
from sportrx.feedback_loop import build_feedback_dashboard
from sportrx.measurement_timeline import build_measurement_timeline, measurement_timeline_markdown
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.walkthrough import build_walkthrough


def _walkthrough_for(profile, benchmark_sessions=None, feedback_by_week=None):
    benchmark_sessions = benchmark_sessions or []
    feedback_by_week = feedback_by_week or {}
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile, feedback_by_week=feedback_by_week)
    dashboard = build_feedback_dashboard(plan, feedback_by_week, benchmark_sessions)
    return build_walkthrough(passport, summarize_benchmark_sessions(benchmark_sessions), dashboard)


def test_measurement_timeline_marks_default_user_waiting_for_measurement():
    walkthrough = _walkthrough_for(
        {"age": 35, "training_days": 2, "weekly_training_minutes": 80, "symptoms": [], "known_conditions": []}
    )

    timeline = build_measurement_timeline(walkthrough)

    assert timeline["schema"] == "sportrx.measurement_timeline"
    assert timeline["completion"]["done"] == 1
    assert timeline["current_step"]["page"] == "HYROX Check"
    assert timeline["current_step"]["stage"] == "waiting"
    assert "workflow state only" in timeline["claim_boundary"]


def test_measurement_timeline_marks_demo_state_mostly_done():
    state = build_demo_state()
    walkthrough = _walkthrough_for(state["profile"], state["benchmark_sessions"], state["feedback_by_week"])

    timeline = build_measurement_timeline(walkthrough)

    assert timeline["completion"]["done"] >= 8
    assert timeline["completion"]["percent"] >= 0.8
    assert timeline["items"][-1]["stage"] == "done"


def test_measurement_timeline_markdown_exports_steps():
    state = build_demo_state()
    walkthrough = _walkthrough_for(state["profile"], state["benchmark_sessions"], state["feedback_by_week"])
    timeline = build_measurement_timeline(walkthrough)

    markdown = measurement_timeline_markdown(timeline)

    assert "# SportRx Measurement Loop Timeline" in markdown
    assert "Quick Match" in markdown
    assert "Export Center" in markdown
