from sportrx.events import match_events


def test_event_match_ranks_accessible_event_for_active_runner():
    result = match_events(
        {
            "age": 28,
            "height_cm": 170,
            "weight_kg": 64,
            "resting_hr": 60,
            "exercise_days_last_4w": 4,
            "mvpa_minutes_per_week": 180,
            "running_minutes_per_week": 120,
            "strength_days_per_week": 1,
            "available_days_per_week": 5,
            "max_minutes_per_session": 60,
            "symptoms": [],
            "known_conditions": [],
        }
    )

    assert result["matches"][0]["stars"] >= 4
    assert result["matches"][0]["status"] in {"recommended", "possible_with_preparation"}


def test_event_match_unavailable_when_safety_blocked():
    result = match_events({"age": 45, "symptoms": ["dizziness_or_syncope"]})

    assert result["matches"] == []
    assert result["readiness"]["band"] == "needs_review"
