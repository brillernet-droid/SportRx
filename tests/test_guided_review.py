from sportrx.benchmark_log import summarize_benchmark_sessions
from sportrx.demo_scenario_matrix import build_demo_scenario_matrix
from sportrx.demo_seed import build_demo_state
from sportrx.feedback_loop import build_feedback_dashboard
from sportrx.first_run_guide import build_first_run_guide
from sportrx.guided_review import build_guided_review_console, guided_review_markdown
from sportrx.launch_readiness import build_launch_readiness
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES
from sportrx.walkthrough import build_walkthrough


def _complete_console():
    state = build_demo_state()
    profile = state["profile"]
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile, feedback_by_week=state["feedback_by_week"])
    dashboard = build_feedback_dashboard(plan, state["feedback_by_week"], state["benchmark_sessions"])
    summary = summarize_benchmark_sessions(state["benchmark_sessions"])
    walkthrough = build_walkthrough(passport, summary, dashboard)
    first_run = build_first_run_guide(passport, state["benchmark_sessions"], state["feedback_by_week"])
    evidence = {path: True for path in REQUIRED_EVIDENCE_FILES}
    launch = build_launch_readiness(profile, passport, plan, state["benchmark_sessions"], state["feedback_by_week"], evidence)
    return build_guided_review_console(walkthrough, first_run, launch, build_demo_scenario_matrix())


def test_guided_review_console_summarizes_complete_demo_path():
    console = _complete_console()

    assert console["schema"] == "sportrx.guided_review_console"
    assert console["status"] == "ready_for_guided_review"
    assert console["ready_cards"] == console["total_cards"]
    assert console["progress_percent"] >= 80
    assert any(item["id"] == "recommended_scenario" for item in console["cards"])
    assert any(item["target"] == "Release QA" for item in console["quick_actions"])
    assert "does not validate SportRx" in console["claim_boundary"]


def test_guided_review_console_marks_unmeasured_state_as_waiting():
    profile = {"age": 35, "training_days": 2, "weekly_training_minutes": 80, "symptoms": [], "known_conditions": []}
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile)
    dashboard = build_feedback_dashboard(plan, {}, [])
    walkthrough = build_walkthrough(passport, summarize_benchmark_sessions([]), dashboard)
    first_run = build_first_run_guide(passport, [], {})
    launch = build_launch_readiness(profile, passport, plan, [], {}, {}, root=".")
    console = build_guided_review_console(walkthrough, first_run, launch, build_demo_scenario_matrix())

    assert console["status"] == "needs_guided_review"
    assert console["progress_percent"] < 80
    assert any(item["status"] == "waiting" for item in console["cards"])


def test_guided_review_markdown_exports_cards_steps_and_actions():
    markdown = guided_review_markdown(_complete_console())

    assert "# SportRx Guided Review Console" in markdown
    assert "Review Steps" in markdown
    assert "Quick Actions" in markdown
    assert "Release QA" in markdown
    assert "does not validate SportRx" in markdown
