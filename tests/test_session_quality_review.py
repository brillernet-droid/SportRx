from sportrx.demo_seed import build_demo_state
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES
from sportrx.session_quality_review import build_session_quality_review, session_quality_review_markdown


def _evidence():
    return {path: True for path in REQUIRED_EVIDENCE_FILES}


def test_session_quality_routes_default_state_to_measurement_first():
    profile = {"age": 35, "training_days": 2, "weekly_training_minutes": 80, "symptoms": [], "known_conditions": []}
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile)

    review = build_session_quality_review(profile, passport, plan, [], {}, _evidence(), ".")

    assert review["schema"] == "sportrx.session_quality_review"
    assert review["status"] == "measurement_first"
    assert review["summary"]["measured_performance_areas"] < 2
    assert any(gate["id"] == "measurement_depth" and gate["status"] == "waiting" for gate in review["gates"])
    assert "not a performance score" in review["claim_boundary"]


def test_session_quality_marks_complete_demo_ready_for_release_review():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])

    review = build_session_quality_review(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        _evidence(),
        ".",
    )

    assert review["status"] == "release_review_ready"
    assert review["summary"]["benchmark_sessions"] >= 2
    assert review["summary"]["feedback_weeks"] >= 1
    assert review["summary"]["retest_ready"] is True
    assert review["summary"]["evidence_sources"] >= 20
    assert all(gate["status"] == "ready" for gate in review["gates"])


def test_session_quality_keeps_red_safety_gate_blocking():
    profile = {"age": 40, "symptoms": ["chest_pain"], "known_conditions": []}
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile)

    review = build_session_quality_review(profile, passport, plan, [], {}, _evidence(), ".")

    assert review["status"] == "blocked_by_safety_gate"
    assert review["summary"]["safety_gate"] == "RED"
    assert any(gate["id"] == "safety_gate" and gate["status"] == "blocked" for gate in review["gates"])


def test_session_quality_markdown_exports_gates():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    review = build_session_quality_review(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        _evidence(),
        ".",
    )

    markdown = session_quality_review_markdown(review)

    assert "# SportRx Session Quality Review" in markdown
    assert "release_review_ready" in markdown
    assert "Evidence Library" in markdown
