from sportrx import generate_prescription
from sportrx.performance_lab import assess_hybrid_performance


def test_old_valid_sportrx_user_data_still_loads():
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

    plan = generate_prescription(profile)
    lab = assess_hybrid_performance(profile)

    assert plan["safety"]["auto_prescription"] is True
    assert lab["assessment_completeness"] == "LOW"
