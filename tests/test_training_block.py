from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.training_block import build_training_block, training_block_markdown


def test_training_block_stays_blocked_without_enough_measurement():
    passport = build_readiness_passport(
        {
            "age": 35,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "symptoms": [],
            "known_conditions": [],
        }
    )
    core_plan = generate_prescription(
        {
            "age": 35,
            "exercise_days_last_4w": 3,
            "mvpa_minutes_per_week": 120,
            "available_days_per_week": 3,
            "max_minutes_per_session": 45,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    block = build_training_block(passport, core_plan)

    assert block["available"] is False
    assert "Hybrid Benchmark" in block["reason"]
    assert block["weeks"] == []


def test_training_block_builds_four_week_sessions_when_path_available():
    passport = build_readiness_passport(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 180,
            "running_minutes_per_week": 90,
            "one_km_run_seconds": 300,
            "station_test_score": 70,
            "station_test_protocol": "SportRx Hybrid Benchmark v1",
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "symptoms": [],
            "known_conditions": [],
        }
    )
    core_plan = generate_prescription(
        {
            "age": 35,
            "exercise_days_last_4w": 4,
            "mvpa_minutes_per_week": 180,
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "preferred_activity": "running",
            "symptoms": [],
            "known_conditions": [],
        }
    )

    block = build_training_block(passport, core_plan)

    assert block["available"] is True
    assert len(block["weeks"]) == 4
    assert block["weeks"][0]["sessions"]
    assert block["claim_boundary"]
    assert "injury-risk" in block["claim_boundary"]


def test_training_block_markdown_exports_block_or_reason():
    blocked = build_training_block(
        {"starter_path": {"available": False, "reason": "Complete benchmark first."}, "next_action": "Benchmark"},
        {"weeks": []},
    )

    markdown = training_block_markdown(blocked)

    assert "# SportRx 4-Week Starter Path" in markdown
    assert "Complete benchmark first." in markdown


def test_training_block_hard_stops_after_an_adverse_event():
    passport = build_readiness_passport(
        {
            "age": 35,
            "training_days": 4,
            "weekly_training_minutes": 180,
            "running_minutes_per_week": 90,
            "one_km_run_seconds": 300,
            "station_test_score": 70,
            "station_test_protocol": "SportRx Hybrid Benchmark v1",
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "symptoms": [],
            "known_conditions": [],
        }
    )
    core_plan = generate_prescription(
        {
            "age": 35,
            "exercise_days_last_4w": 4,
            "mvpa_minutes_per_week": 180,
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    block = build_training_block(passport, core_plan, {1: {"adverse_event": True}})

    assert block["available"] is False
    assert block["automation_guard"]["status"] == "automation_hard_stop"
    assert block["weeks"] == []
