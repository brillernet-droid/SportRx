from pathlib import Path

from sportrx.demo_runbook import build_demo_runbook
from sportrx.demo_seed import build_demo_state
from sportrx.launch_readiness import build_launch_readiness
from sportrx.passport import build_readiness_passport
from sportrx.pilot_feedback import build_pilot_review_console, create_pilot_feedback_entry
from sportrx.prescription import generate_prescription
from sportrx.public_beta_readiness import build_public_beta_readiness, public_beta_readiness_markdown
from sportrx.release_package import build_release_package_manifest
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES, build_release_qa
from sportrx.runtime_doctor import build_runtime_doctor


ROOT = Path(__file__).resolve().parents[1]


def _release_inputs(entries=None):
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
    pilot_review = build_pilot_review_console(entries or [])
    return qa, launch, runtime, package_manifest, runbook, evidence, pilot_review


def _good_entries(count=5):
    return [
        create_pilot_feedback_entry(
            reviewer_role="coach",
            ratings={
                "setup_clarity": 5,
                "measurement_realism": 4,
                "trust": 4,
                "actionability": 5,
                "visual_polish": 4,
            },
            comments={"overall": f"review {index}"},
            consent_to_contact=True,
            contact=f"reviewer{index}@example.com",
            review_date="2026-08-22",
        )
        for index in range(count)
    ]


def test_public_beta_readiness_routes_clean_release_to_limited_review_without_pilot_depth():
    readiness = build_public_beta_readiness(*_release_inputs())

    assert readiness["schema"] == "sportrx.public_beta_readiness"
    assert readiness["status"] == "limited_review_ready_collect_pilot_feedback"
    assert any(check["id"] == "beta_pilot_feedback_depth" for check in readiness["checks"])
    assert "does not validate" in readiness["claim_boundary"]


def test_public_beta_readiness_requires_release_gates_before_external_review():
    qa, launch, runtime, package_manifest, runbook, evidence, pilot_review = _release_inputs(_good_entries())
    runtime = dict(runtime)
    runtime["status"] = "needs_runtime_review"

    readiness = build_public_beta_readiness(qa, launch, runtime, package_manifest, runbook, evidence, pilot_review)

    assert readiness["status"] == "needs_release_fix"
    assert any(check["id"] == "beta_runtime" and check["status"] == "needs_review" for check in readiness["checks"])


def test_public_beta_readiness_marks_candidate_after_clean_pilot_pattern_review():
    readiness = build_public_beta_readiness(*_release_inputs(_good_entries()))
    markdown = public_beta_readiness_markdown(readiness)

    assert readiness["status"] == "public_beta_candidate"
    assert readiness["passed_checks"] == readiness["total_checks"]
    assert "# SportRx Public Beta Readiness" in markdown
    assert "public_beta_candidate" in markdown
