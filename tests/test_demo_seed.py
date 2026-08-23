from sportrx.demo_seed import build_demo_state
from sportrx.feedback_loop import build_feedback_dashboard
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.training_block import build_training_block


def test_demo_seed_supports_full_loop():
    state = build_demo_state()
    profile = state["profile"]
    passport = build_readiness_passport(profile)
    plan = generate_prescription(
        {
            **profile,
            "exercise_days_last_4w": profile["training_days"],
            "mvpa_minutes_per_week": profile["weekly_training_minutes"],
            "common_activity": "running",
            "preferred_activity": "running",
            "intended_intensity": "moderate",
        },
        feedback_by_week=state["feedback_by_week"],
    )
    block = build_training_block(passport, plan)
    dashboard = build_feedback_dashboard(plan, state["feedback_by_week"], state["benchmark_sessions"])

    assert len(state["benchmark_sessions"]) == 2
    assert "station_test_protocol" in profile
    assert passport["starter_path"]["available"] is True
    assert passport["lab_test_quality"]["status"] == "review_ready_measurement_record"
    assert block["available"] is True
    assert dashboard["adherence"]["weeks_recorded"] == 2
    assert dashboard["benchmark_summary"]["retest_ready"] is True
    assert dashboard["retest_comparisons"]


def test_demo_seed_is_labeled_as_synthetic_sample_data():
    state = build_demo_state()

    assert "synthetic sample" in state["claim_boundary"].lower()
    assert "not validation data" in state["claim_boundary"].lower()
