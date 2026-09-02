import pytest

from sportrx import build_plan_record, create_completed_session_record, create_measurement_record, generate_prescription


def test_missing_measurement_stays_not_tested_with_a_reason():
    record = create_measurement_record(
        metric="six_minute_run_distance",
        value=None,
        unit=None,
        source="manual",
        not_tested_reason="no suitable route",
    )

    assert record["status"] == "not_tested"
    assert record["value"] is None
    assert record["not_tested_reason"] == "no suitable route"


def test_measurement_requires_reason_instead_of_missing_value_imputation():
    with pytest.raises(ValueError, match="not_tested_reason"):
        create_measurement_record(metric="resting_hr", value=None, unit=None, source="manual")


def test_completed_session_carries_pack_and_source_but_not_a_dose_decision():
    record = create_completed_session_record(
        plan_id="plan_123",
        program_pack_id="low_activity_aerobic_v1",
        week=1,
        session_index=0,
        completed=True,
        rpe=5,
        source="device",
    )

    assert record["program_pack_id"] == "low_activity_aerobic_v1"
    assert record["source"] == "device"
    assert "progression" not in record


def test_plan_record_traces_pack_and_rule_ids():
    prescription = generate_prescription(
        {
            "age": 36,
            "exercise_days_last_4w": 0,
            "mvpa_minutes_per_week": 0,
            "available_days_per_week": 3,
            "max_minutes_per_session": 30,
            "preferred_activity": "brisk walking",
            "symptoms": [],
            "known_conditions": [],
        }
    )
    plan = build_plan_record(prescription)

    assert plan["program_pack_id"] == "low_activity_aerobic_v1"
    assert plan["rule_ids"] == ["SAFE-001", "CORE-002", "INT-001"]
