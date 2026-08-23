from pathlib import Path

from sportrx.demo_runbook import build_demo_runbook
from sportrx.demo_seed import build_demo_state
from sportrx.launch_readiness import build_launch_readiness
from sportrx.passport import build_readiness_passport
from sportrx.pilot_feedback import build_pilot_review_console
from sportrx.prescription import generate_prescription
from sportrx.public_beta_readiness import build_public_beta_readiness
from sportrx.release_candidate_summary import build_release_candidate_summary, release_candidate_summary_markdown
from sportrx.release_package import build_release_package_manifest
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES, build_release_qa
from sportrx.runtime_doctor import build_runtime_doctor


ROOT = Path(__file__).resolve().parents[1]


def _summary():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    evidence = {path: True for path in REQUIRED_EVIDENCE_FILES}
    qa = build_release_qa(state["profile"], passport, plan, state["benchmark_sessions"], state["feedback_by_week"], evidence)
    launch = build_launch_readiness(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        evidence,
        root=str(ROOT),
    )
    runtime = build_runtime_doctor(ROOT, python_version=(3, 11, 0), streamlit_version="1.61.1")
    package_manifest = build_release_package_manifest(ROOT)
    runbook = build_demo_runbook(launch)
    public_beta = build_public_beta_readiness(
        qa,
        launch,
        runtime,
        package_manifest,
        runbook,
        evidence,
        build_pilot_review_console([]),
    )
    return build_release_candidate_summary(
        qa=qa,
        launch=launch,
        runtime=runtime,
        package_manifest=package_manifest,
        public_beta=public_beta,
        export_file_count=46,
        review_pack_file_count=46,
    )


def test_release_candidate_summary_collects_existing_product_gates():
    summary = _summary()

    assert summary["schema"] == "sportrx.release_candidate_summary"
    assert summary["status"] == "limited_review_candidate"
    assert summary["passed_checks"] == summary["total_checks"]
    assert "sportrx_release_qa.md" in summary["open_first"]
    assert "bash scripts/run_local.sh" in summary["run_commands"]
    assert "injury-risk percentage" in summary["blocked_claims"]
    assert "does not validate SportRx" in summary["claim_boundary"]


def test_release_candidate_summary_markdown_exports_handoff_snapshot():
    markdown = release_candidate_summary_markdown(_summary())

    assert "# SportRx Release Candidate Summary" in markdown
    assert "Product Gates" in markdown
    assert "Open First" in markdown
    assert "Blocked Claims" in markdown
