from pathlib import Path

from sportrx.demo_runbook import build_demo_runbook
from sportrx.demo_seed import build_demo_state
from sportrx.launch_command_center import build_launch_command_center
from sportrx.launch_readiness import build_launch_readiness
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES


ROOT = Path(__file__).resolve().parents[1]


def _ready_launch_and_runbook():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    evidence = {path: True for path in REQUIRED_EVIDENCE_FILES}
    launch = build_launch_readiness(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        evidence,
        root=str(ROOT),
    )
    return launch, build_demo_runbook(launch)


def test_launch_command_center_summarizes_ready_demo_state():
    launch, runbook = _ready_launch_and_runbook()
    command_center = build_launch_command_center(launch, runbook)

    assert command_center["schema"] == "sportrx.launch_command_center"
    assert command_center["status"] == "ready"
    assert len(command_center["cards"]) == 4
    assert all(card["status"] == "ready" for card in command_center["cards"])
    assert "not validation" in command_center["claim_boundary"]


def test_launch_command_center_flags_incomplete_state():
    launch, runbook = _ready_launch_and_runbook()
    launch = {**launch, "status": "needs_review", "passed_checks": 3}
    command_center = build_launch_command_center(launch, runbook)

    assert command_center["status"] == "needs_review"
    assert command_center["cards"][0]["status"] == "needs_review"
