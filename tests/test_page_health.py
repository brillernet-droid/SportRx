from sportrx.demo_seed import build_demo_state
from sportrx.feedback_loop import build_feedback_dashboard
from sportrx.page_health import build_page_health_matrix, page_health_matrix_markdown
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.walkthrough import build_walkthrough


def _matrix():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    dashboard = build_feedback_dashboard(plan, state["feedback_by_week"], state["benchmark_sessions"])
    walkthrough = build_walkthrough(passport, dashboard["benchmark_summary"], dashboard)
    return build_page_health_matrix(walkthrough)


def test_page_health_matrix_lists_page_roles_and_boundaries():
    matrix = _matrix()
    rows = {item["page"]: item for item in matrix["rows"]}

    assert matrix["schema"] == "sportrx.page_health_matrix"
    assert matrix["status"] == "ready_for_page_review"
    assert matrix["page_count"] >= 12
    assert rows["Quick Match"]["lane"] == "Intake"
    assert "not a measured performance test" in rows["Quick Match"]["blocked_claim"]
    assert rows["Release QA"]["lane"] == "Release"
    assert "does not validate SportRx" in matrix["claim_boundary"]


def test_page_health_matrix_markdown_exports_success_signals():
    markdown = page_health_matrix_markdown(_matrix())

    assert "# SportRx Page Health Matrix" in markdown
    assert "Primary question" in markdown
    assert "Success signal" in markdown
    assert "Blocked claim" in markdown
    assert "Trial Mode Launcher" in markdown
