import pytest

from sportrx.demo_scenarios import build_demo_scenario_state, build_demo_scenarios
from sportrx.feedback_loop import build_feedback_dashboard
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription


def test_demo_scenarios_list_public_review_states():
    scenarios = build_demo_scenarios()
    ids = {item["id"] for item in scenarios}

    assert ids == {"measure_first", "benchmark_underway", "complete_loop"}
    assert all("not validation data" in item["claim_boundary"].lower() for item in scenarios)


def test_measure_first_scenario_blocks_training_handoff():
    state = build_demo_scenario_state("measure_first")
    passport = build_readiness_passport(state["profile"])

    assert state["benchmark_sessions"] == []
    assert passport["starter_path"]["available"] is False
    assert passport["measured_performance_areas"]["count"] < 2


def test_benchmark_underway_scenario_has_partial_log_without_retest():
    state = build_demo_scenario_state("benchmark_underway")
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"])
    dashboard = build_feedback_dashboard(plan, state["feedback_by_week"], state["benchmark_sessions"])

    assert len(state["benchmark_sessions"]) == 1
    assert dashboard["benchmark_summary"]["retest_ready"] is False
    assert passport["measured_performance_areas"]["count"] < 2


def test_complete_loop_scenario_supports_full_demo_review():
    state = build_demo_scenario_state("complete_loop")
    passport = build_readiness_passport(state["profile"])

    assert len(state["benchmark_sessions"]) == 2
    assert state["feedback_by_week"]
    assert passport["starter_path"]["available"] is True


def test_demo_scenario_rejects_unknown_id():
    with pytest.raises(ValueError, match="Unknown demo scenario"):
        build_demo_scenario_state("missing")
