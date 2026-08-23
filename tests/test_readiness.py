from sportrx.readiness import calculate_readiness


def test_readiness_returns_score_for_safe_user():
    result = calculate_readiness(
        {
            "age": 32,
            "height_cm": 178,
            "weight_kg": 74,
            "resting_hr": 58,
            "exercise_days_last_4w": 4,
            "mvpa_minutes_per_week": 160,
            "available_days_per_week": 4,
            "max_minutes_per_session": 45,
            "sleep_hours": 7,
            "stress_1_10": 4,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["score"] >= 70
    assert result["band"] in {"moderate_high", "high"}
    assert result["components"]["activity"] > 0


def test_readiness_blocks_when_safety_screen_blocks():
    result = calculate_readiness({"age": 45, "symptoms": ["chest_pain"], "known_conditions": []})

    assert result["score"] is None
    assert result["band"] == "needs_review"
    assert result["risks"]
