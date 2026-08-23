from pathlib import Path

from sportrx.demo_runbook import build_demo_runbook, demo_runbook_markdown
from sportrx.demo_seed import build_demo_state
from sportrx.launch_readiness import build_launch_readiness
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES


ROOT = Path(__file__).resolve().parents[1]


def _launch_report():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    evidence = {path: True for path in REQUIRED_EVIDENCE_FILES}
    return build_launch_readiness(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        evidence,
        root=str(ROOT),
    )


def test_demo_runbook_builds_reviewer_script_from_launch_readiness():
    runbook = build_demo_runbook(_launch_report())

    assert runbook["schema"] == "sportrx.demo_runbook"
    assert runbook["status"] == "ready"
    assert runbook["must_show"]
    assert any(item["page"] == "Release QA" for item in runbook["must_show"])
    assert "not be presented as scientific validation" in runbook["claim_boundary"]
    assert any("injury-risk" in item for item in runbook["guardrails"])


def test_demo_runbook_markdown_exports_guardrails_and_path():
    runbook = build_demo_runbook(_launch_report())
    markdown = demo_runbook_markdown(runbook)

    assert "# SportRx Demo Runbook" in markdown
    assert "Must Show" in markdown
    assert "Guardrails" in markdown
    assert "Full Review Path" in markdown
