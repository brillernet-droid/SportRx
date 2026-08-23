from sportrx.progression import apply_progression, evaluate_week


def test_high_completion_low_rpe_increases():
    decision = evaluate_week(planned_sessions=3, completed_sessions=3, average_rpe=3)

    assert decision["action"] == "increase"
    assert decision["change_pct"] == 0.15


def test_small_increase_changes_actual_session_shape_after_rounding():
    decision = evaluate_week(planned_sessions=3, completed_sessions=3, average_rpe=5)
    volume = {"frequency_per_week": 3, "duration_min": 15, "weekly_minutes": 45, "progression_ceiling_min": 90}

    result = apply_progression(volume, decision, available_days=3, max_session=30)

    assert result["weekly_minutes"] > volume["weekly_minutes"]


def test_low_completion_high_rpe_decreases():
    decision = evaluate_week(planned_sessions=3, completed_sessions=1, average_rpe=8, felt_too_hard=True)

    assert decision["action"] == "decrease"


def test_adverse_event_pauses_progression():
    decision = evaluate_week(planned_sessions=3, completed_sessions=3, average_rpe=5, adverse_event=True)
    volume = {"frequency_per_week": 3, "duration_min": 20, "weekly_minutes": 60, "progression_ceiling_min": 150}

    result = apply_progression(volume, decision, available_days=3, max_session=30)

    assert result["paused"] is True
    assert result["weekly_minutes"] == 0
