import pytest

from sportrx.session_feedback import create_session_feedback, summarize_session_feedback


def test_completed_session_requires_rpe():
    with pytest.raises(ValueError, match="RPE is required"):
        create_session_feedback(week=1, session_index=0, completed=True)


def test_session_feedback_aggregates_completion_and_rpe():
    records = [
        create_session_feedback(week=1, session_index=0, completed=True, rpe=4),
        create_session_feedback(week=1, session_index=1, completed=False),
        create_session_feedback(week=1, session_index=2, completed=True, rpe=6),
    ]

    summary = summarize_session_feedback(3, records)

    assert summary["week_complete"] is True
    assert summary["ready_for_progression"] is True
    assert summary["weekly_feedback"]["completed_sessions"] == 2
    assert summary["weekly_feedback"]["average_rpe"] == 5.0


def test_adverse_event_allows_immediate_stop_route():
    summary = summarize_session_feedback(
        3,
        [create_session_feedback(week=1, session_index=0, completed=False, adverse_event=True)],
    )

    assert summary["week_complete"] is False
    assert summary["ready_for_progression"] is True
    assert summary["weekly_feedback"]["adverse_event"] is True
