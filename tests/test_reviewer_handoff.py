from pathlib import Path

from sportrx.artifact_catalog import build_artifact_catalog
from sportrx.demo_scenarios import build_demo_scenarios
from sportrx.demo_seed import build_demo_state
from sportrx.export_bundle import build_export_bundle
from sportrx.launch_readiness import build_launch_readiness
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES
from sportrx.reviewer_handoff import build_reviewer_handoff, reviewer_handoff_markdown
from sportrx.runtime_doctor import build_runtime_doctor


ROOT = Path(__file__).resolve().parents[1]


def _handoff():
    state = build_demo_state()
    profile = state["profile"]
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile, feedback_by_week=state["feedback_by_week"])
    evidence = {path: True for path in REQUIRED_EVIDENCE_FILES}
    launch = build_launch_readiness(
        profile,
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        evidence,
        root=str(ROOT),
    )
    runtime = build_runtime_doctor(ROOT, python_version=(3, 11, 0), streamlit_version="1.61.1")
    bundle = build_export_bundle(profile, passport, plan, state["benchmark_sessions"], state["feedback_by_week"])
    catalog = build_artifact_catalog(bundle["files"])
    return build_reviewer_handoff(runtime, build_demo_scenarios(), catalog, launch)


def test_reviewer_handoff_summarizes_review_path_without_validation_claims():
    handoff = _handoff()

    assert handoff["schema"] == "sportrx.reviewer_handoff"
    assert handoff["status"] == "ready_for_reviewer_handoff"
    assert len(handoff["demo_scenarios"]) == 3
    assert any(item.get("page") == "Export Center" for item in handoff["open_first"])
    assert any(item["filename"] == "sportrx_first_run_guide.md" for item in handoff["priority_artifacts"])
    assert any(item["filename"] == "sportrx_session_snapshot.json" for item in handoff["priority_artifacts"])
    assert any("scientifically validated" in item for item in handoff["claim_guardrails"])
    assert "does not validate" in handoff["claim_boundary"]


def test_reviewer_handoff_markdown_lists_commands_and_guardrails():
    markdown = reviewer_handoff_markdown(_handoff())

    assert "# SportRx Reviewer Handoff" in markdown
    assert "Demo Scenarios" in markdown
    assert "bash scripts/run_local.sh" in markdown
    assert "Do not use Safety Gate as a performance score" in markdown
