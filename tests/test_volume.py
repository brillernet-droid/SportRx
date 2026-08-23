from sportrx.volume import estimate_initial_volume


def test_inactive_limited_time_stays_within_capacity():
    profile = {
        "mvpa_minutes_per_week": 0,
        "available_days_per_week": 2,
        "max_minutes_per_session": 20,
    }
    assessment = {"fitness_class": "inactive"}

    result = estimate_initial_volume(profile, assessment)

    assert result["frequency_per_week"] == 2
    assert result["duration_min"] == 20
    assert result["weekly_minutes"] == 40
    assert result["weekly_minutes"] <= result["available_capacity_min"]


def test_low_active_does_not_jump_directly_to_full_guideline_when_time_limited():
    profile = {
        "mvpa_minutes_per_week": 60,
        "available_days_per_week": 3,
        "max_minutes_per_session": 30,
    }
    assessment = {"fitness_class": "low_active"}

    result = estimate_initial_volume(profile, assessment)

    assert result["weekly_minutes"] == 90
    assert result["progression_ceiling_min"] == 90
