from sportrx.benchmark_log import summarize_benchmark_sessions
from sportrx.demo_seed import build_demo_state
from sportrx.lab_readiness import build_lab_readiness_console, lab_readiness_markdown
from sportrx.passport import build_readiness_passport


def test_lab_readiness_routes_default_state_to_measurement():
    profile = {"age": 35, "training_days": 2, "weekly_training_minutes": 80, "symptoms": [], "known_conditions": []}
    passport = build_readiness_passport(profile)
    console = build_lab_readiness_console(profile, passport, summarize_benchmark_sessions([]))

    assert console["schema"] == "sportrx.lab_readiness_console"
    assert console["status"] in {"needs_equipment_path", "needs_measurement"}
    assert console["summary"]["measured_performance_areas"] < 2
    assert any(card["id"] == "measurement_depth" for card in console["cards"])
    assert "does not score performance" in console["claim_boundary"]


def test_lab_readiness_marks_demo_state_ready_for_retest_review():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    console = build_lab_readiness_console(
        state["profile"],
        passport,
        summarize_benchmark_sessions(state["benchmark_sessions"]),
    )

    assert console["status"] == "ready_for_retest_review"
    assert console["summary"]["equipment_count"] > 0
    assert console["summary"]["measured_performance_areas"] >= 2
    assert console["summary"]["benchmark_sessions"] == 2
    assert console["summary"]["retest_ready"] is True


def test_lab_readiness_keeps_safety_gate_separate_and_blocking():
    profile = {
        "age": 35,
        "training_days": 3,
        "weekly_training_minutes": 120,
        "one_km_run_seconds": 360,
        "station_test_score": 60,
        "station_test_protocol": "SportRx Hybrid Benchmark v1",
        "equipment_access": ["track", "dumbbell"],
        "symptoms": ["chest_pain"],
        "known_conditions": [],
    }
    passport = build_readiness_passport(profile)
    console = build_lab_readiness_console(profile, passport, summarize_benchmark_sessions([]))

    assert console["status"] == "blocked_by_safety_gate"
    assert console["summary"]["safety_gate"] == "RED"
    assert any(card["id"] == "safety_gate" and card["status"] == "blocked" for card in console["cards"])
    assert console["summary"]["measured_performance_areas"] >= 2


def test_lab_readiness_markdown_exports_cards():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    console = build_lab_readiness_console(
        state["profile"],
        passport,
        summarize_benchmark_sessions(state["benchmark_sessions"]),
    )

    markdown = lab_readiness_markdown(console)

    assert "# SportRx Lab Readiness Console" in markdown
    assert "Safety Gate" in markdown
    assert "Retest Anchor" in markdown
