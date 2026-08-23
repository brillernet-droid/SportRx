from sportrx.demo_runbook import build_demo_runbook
from sportrx.demo_scenario_matrix import build_demo_scenario_matrix
from sportrx.first_run_guide import build_first_run_guide
from sportrx.reviewer_session_plan import build_reviewer_session_plan, reviewer_session_plan_markdown


def _runbook(status="ready_for_public_demo"):
    return build_demo_runbook(
        {
            "status": status,
            "review_path": [
                {"step": 1, "page": "Workbench", "task": "Open product state", "status": "complete"},
                {"step": 2, "page": "Release QA", "task": "Check release gates", "status": "complete"},
            ],
        }
    )


def test_reviewer_session_plan_builds_time_boxed_tracks():
    first_run = build_first_run_guide(
        {"measured_performance_areas": {"count": 0}, "starter_path": {"available": False}},
        [],
        {},
    )
    plan = build_reviewer_session_plan(first_run, build_demo_scenario_matrix(), _runbook())

    assert plan["schema"] == "sportrx.reviewer_session_plan"
    assert plan["status"] == "ready"
    assert plan["track_count"] == 3
    assert plan["next_track"] == "guided_measurement_review"
    assert plan["total_review_minutes"] == 23
    assert any(track["id"] == "quick_scan" for track in plan["tracks"])
    assert any("Do not call SportRx validated" in item for item in plan["guardrails"])
    assert "does not validate SportRx" in plan["claim_boundary"]


def test_reviewer_session_plan_routes_complete_state_to_quick_scan():
    first_run = {"recommended_path": "review_export"}
    plan = build_reviewer_session_plan(first_run, build_demo_scenario_matrix(), _runbook())

    assert plan["next_track"] == "quick_scan"
    full = next(track for track in plan["tracks"] if track["id"] == "full_release_review")
    guided = next(track for track in plan["tracks"] if track["id"] == "guided_measurement_review")
    assert guided["scenario_state"] == "partial_measurement"
    assert "Release QA" in full["page_sequence"]
    assert "sportrx_review_pack.zip" in full["artifacts"]


def test_reviewer_session_plan_markdown_exports_tracks_and_guardrails():
    first_run = {"recommended_path": "review_export"}
    plan = build_reviewer_session_plan(first_run, build_demo_scenario_matrix(), _runbook())
    markdown = reviewer_session_plan_markdown(plan)

    assert "# SportRx Reviewer Session Plan" in markdown
    assert "3-minute quick scan" in markdown
    assert "8-minute guided measurement review" in markdown
    assert "12-minute full release review" in markdown
    assert "Guardrails" in markdown
