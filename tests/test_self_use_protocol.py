from sportrx.demo_seed import build_demo_state
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.self_use_protocol import build_self_use_protocol, self_use_protocol_markdown
from sportrx.validation_readiness import build_validation_readiness_matrix


def _demo_matrix():
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
    return state, matrix


def test_self_use_protocol_guides_ready_demo_without_validation_claim():
    state, matrix = _demo_matrix()

    protocol = build_self_use_protocol(matrix, state["profile"])

    assert protocol["schema"] == "sportrx.self_use_protocol"
    assert protocol["status"] == "ready_to_run_phase_0"
    assert protocol["duration_weeks"] == 4
    assert protocol["participant_scope"] == "1 builder"
    assert protocol["current_validation_claim"] == "Prototype; not validated."
    assert "finish-time prediction" in protocol["blocked_claims"]
    assert any(item["week"] == "Week 4" and "Retest" in item["label"] for item in protocol["weekly_schedule"])


def test_self_use_protocol_waits_when_capture_gates_are_missing():
    matrix = {
        "capture_ready": False,
        "current_validation_claim": "Prototype; not validated.",
        "capture_checks": [],
        "blocked_claims": ["validated readiness score"],
    }

    protocol = build_self_use_protocol(matrix, {})

    assert protocol["status"] == "needs_capture_setup"
    assert "Complete validation data-capture gates" in protocol["next_action"]
    assert protocol["equipment_path"] == "standard_or_low_equipment_path_pending"


def test_self_use_protocol_markdown_exports_schedule_fields_and_boundaries():
    state, matrix = _demo_matrix()
    protocol = build_self_use_protocol(matrix, state["profile"])

    markdown = self_use_protocol_markdown(protocol)

    assert "# SportRx Phase 0 Self-Use Protocol" in markdown
    assert "Week 4 - Retest and export" in markdown
    assert "Minimum Data Fields" in markdown
    assert "Blocked Claims" in markdown
    assert "does not validate SportRx" in markdown
