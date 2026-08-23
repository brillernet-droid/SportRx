from sportrx.demo_seed import build_demo_state
from sportrx.feedback_loop import build_feedback_dashboard
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.benchmark_log import summarize_benchmark_sessions
from sportrx.walkthrough import build_walkthrough


def test_walkthrough_routes_default_user_to_measurement():
    profile = {"age": 35, "training_days": 3, "weekly_training_minutes": 120, "symptoms": [], "known_conditions": []}
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile)
    dashboard = build_feedback_dashboard(plan, {}, [])
    walkthrough = build_walkthrough(passport, summarize_benchmark_sessions([]), dashboard)

    assert walkthrough["next_step"]["page"] == "HYROX Check"
    assert walkthrough["steps"][1]["status"] == "needs_measurement"


def test_walkthrough_demo_state_reaches_feedback_loop():
    state = build_demo_state()
    profile = state["profile"]
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile, feedback_by_week=state["feedback_by_week"])
    dashboard = build_feedback_dashboard(plan, state["feedback_by_week"], state["benchmark_sessions"])
    walkthrough = build_walkthrough(passport, summarize_benchmark_sessions(state["benchmark_sessions"]), dashboard)

    assert walkthrough["completion"]["complete_steps"] >= 8
    assert walkthrough["steps"][-1]["status"] == "complete"
