from sportrx import generate_prescription


def test_prescription_generates_four_week_aerobic_plan():
    profile = {
        "age": 40,
        "resting_hr": 68,
        "exercise_days_last_4w": 0,
        "mvpa_minutes_per_week": 0,
        "available_days_per_week": 3,
        "max_minutes_per_session": 30,
        "preferred_activity": "brisk walking",
        "symptoms": [],
        "known_conditions": [],
    }

    result = generate_prescription(profile)

    assert result["safety"]["auto_prescription"] is True
    assert len(result["weeks"]) == 4
    assert result["weeks"][0]["fitt_vp"]["type"] == "brisk walking"
    assert result["weeks"][0]["weekly_minutes"] < result["weeks"][-1]["weekly_minutes"]


def test_prescription_blocks_unsafe_profile():
    result = generate_prescription({"age": 45, "symptoms": ["dizziness_or_syncope"]})

    assert result["safety"]["auto_prescription"] is False
    assert result["weeks"] == []
