from sportrx.demo_experience import build_demo_experience_console, demo_experience_markdown
from sportrx.demo_runbook import build_demo_runbook
from sportrx.demo_scenario_matrix import build_demo_scenario_matrix
from sportrx.demo_seed import build_demo_state
from sportrx.first_run_guide import build_first_run_guide
from sportrx.launch_readiness import build_launch_readiness
from sportrx.open_source_integration import build_open_source_integration_console
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES
from sportrx.reviewer_session_plan import build_reviewer_session_plan
from sportrx.session_quality_review import build_session_quality_review
from sportrx.terminology import build_terminology_guide


def _console():
    state = build_demo_state()
    profile = state["profile"]
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile, feedback_by_week=state["feedback_by_week"])
    evidence = {path: True for path in REQUIRED_EVIDENCE_FILES}
    launch = build_launch_readiness(profile, passport, plan, state["benchmark_sessions"], state["feedback_by_week"], evidence)
    first_run = build_first_run_guide(passport, state["benchmark_sessions"], state["feedback_by_week"], [])
    session_quality = build_session_quality_review(profile, passport, plan, state["benchmark_sessions"], state["feedback_by_week"], evidence, ".")
    runbook = build_demo_runbook(launch)
    build_reviewer_session_plan(first_run, build_demo_scenario_matrix(), runbook)
    return build_demo_experience_console(
        first_run,
        launch,
        session_quality,
        build_terminology_guide(),
        build_open_source_integration_console(),
    )


def test_demo_experience_console_summarizes_first_screen_and_trust_anchors():
    console = _console()

    assert console["schema"] == "sportrx.demo_experience_console"
    assert console["status"] == "ready_for_guided_demo"
    assert console["ready_cards"] == console["total_cards"]
    assert any(item["id"] == "first_screen" for item in console["cards"])
    assert any(item["id"] == "language_contract" for item in console["cards"])
    assert any("Not tested" in item for item in console["trust_anchors"])
    assert any("AI coach" in item for item in console["blocked_impressions"])
    assert "does not validate SportRx" in console["claim_boundary"]


def test_demo_experience_markdown_exports_guided_review_path():
    markdown = demo_experience_markdown(_console())

    assert "# SportRx Demo Experience Console" in markdown
    assert "First Impression" in markdown
    assert "Guided Sequence" in markdown
    assert "HYROX" in markdown
    assert "medical-clearance" in markdown
    assert "does not validate SportRx" in markdown
