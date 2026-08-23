from sportrx.benchmark_log import build_component_result, create_benchmark_session
from sportrx.demo_seed import build_demo_state
from sportrx.feedback_loop import build_feedback_dashboard
from sportrx.output_prerequisites import build_output_prerequisites
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription


def test_output_prerequisites_block_tailored_outputs_when_measurement_is_missing():
    passport = build_readiness_passport(
        {
            "age": 35,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    register = build_output_prerequisites(passport)
    outputs = {item["output_id"]: item for item in register["outputs"]}

    assert outputs["strongest_area_main_gap"]["status"] == "blocked_by_measurement"
    assert outputs["starter_path"]["status"] == "blocked"
    assert "Need at least two measured performance dimensions." in outputs["starter_path"]["missing"]
    assert register["summary"]["blocked_outputs"] >= 2
    assert "product gates" in register["claim_boundary"]


def test_output_prerequisites_mark_feedback_and_retest_active_when_demo_is_loaded():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    dashboard = build_feedback_dashboard(plan, state["feedback_by_week"], state["benchmark_sessions"])
    register = build_output_prerequisites(passport, dashboard["benchmark_summary"], dashboard)
    outputs = {item["output_id"]: item for item in register["outputs"]}

    assert outputs["strongest_area_main_gap"]["status"] == "active"
    assert outputs["starter_path"]["status"] == "active"
    assert outputs["feedback_loop"]["status"] == "active"
    assert outputs["retest_comparison"]["status"] == "active"


def test_output_prerequisites_wait_for_repeated_benchmark_components():
    passport = build_readiness_passport(
        {
            "age": 35,
            "one_km_run_seconds": 300,
            "station_test_score": 70,
            "symptoms": [],
            "known_conditions": [],
        }
    )
    session = create_benchmark_session(
        {},
        [build_component_result("run_1km", value=360, value_unit="seconds", rpe_0_10=7)],
        session_date="2026-08-01",
    )
    plan = generate_prescription({"age": 35, "symptoms": [], "known_conditions": []})
    dashboard = build_feedback_dashboard(plan, {}, [session])
    register = build_output_prerequisites(passport, dashboard["benchmark_summary"], dashboard)
    outputs = {item["output_id"]: item for item in register["outputs"]}

    assert outputs["retest_comparison"]["status"] == "waiting_for_retest"
    assert "Repeat the same benchmark component" in outputs["retest_comparison"]["missing"][0]
