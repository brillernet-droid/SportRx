from sportrx.demo_seed import build_demo_state
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.validation_readiness import build_validation_readiness_matrix, validation_readiness_markdown


def test_validation_readiness_keeps_demo_not_validated():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])

    matrix = build_validation_readiness_matrix(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        [],
        ".",
    )

    assert matrix["schema"] == "sportrx.validation_readiness_matrix"
    assert matrix["status"] == "ready_to_collect_self_use_data"
    assert matrix["current_validation_claim"] == "Prototype; not validated."
    assert matrix["capture_ready"] is True
    assert matrix["passed_checks"] == matrix["total_checks"]
    assert "validated readiness score" in matrix["blocked_claims"]
    assert "does not validate SportRx" in matrix["claim_boundary"]


def test_validation_readiness_waits_for_capture_setup_without_data():
    profile = {"age": 35, "training_days": 2, "weekly_training_minutes": 80, "symptoms": [], "known_conditions": []}
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile)

    matrix = build_validation_readiness_matrix(profile, passport, plan, [], {}, [], ".")

    assert matrix["status"] == "needs_data_capture_setup"
    assert matrix["capture_ready"] is False
    assert matrix["summary"]["benchmark_sessions"] == 0
    assert matrix["phases"][0]["status"] == "needs_local_trial"
    assert "Complete data-capture gates" in matrix["next_action"]


def test_validation_readiness_markdown_exports_phases_and_blocked_claims():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    matrix = build_validation_readiness_matrix(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        [],
        ".",
    )

    markdown = validation_readiness_markdown(matrix)

    assert "# SportRx Validation Readiness Matrix" in markdown
    assert "Prototype; not validated." in markdown
    assert "Phase 0 - Self-use" in markdown
    assert "finish-time prediction" in markdown
