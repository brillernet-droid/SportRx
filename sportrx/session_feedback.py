"""Session-level feedback records for the SportRX adaptive aerobic loop.

The module only aggregates user-entered completion and RPE records. It does
not add a recovery score, diagnose an event, or alter training dose directly.
"""

from __future__ import annotations

from typing import Any


def create_session_feedback(
    *,
    week: int,
    session_index: int,
    completed: bool,
    rpe: float | None = None,
    felt_too_hard: bool = False,
    adverse_event: bool = False,
) -> dict[str, Any]:
    """Create one validated, minimal session feedback record."""

    if int(week) < 1:
        raise ValueError("week must be at least 1")
    if int(session_index) < 0:
        raise ValueError("session_index must be non-negative")
    if completed and rpe is None:
        raise ValueError("RPE is required when a session was completed")
    if rpe is not None and not 0 <= float(rpe) <= 10:
        raise ValueError("RPE must be between 0 and 10")

    return {
        "week": int(week),
        "session_index": int(session_index),
        "completed": bool(completed),
        "rpe": round(float(rpe), 1) if completed and rpe is not None else None,
        "felt_too_hard": bool(felt_too_hard),
        "adverse_event": bool(adverse_event),
    }


def summarize_session_feedback(planned_sessions: int, records: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate one week's records for the existing weekly progression rule."""

    planned_sessions = max(1, int(planned_sessions or 1))
    by_index: dict[int, dict[str, Any]] = {}
    for record in records:
        session_index = int(record.get("session_index", -1))
        if 0 <= session_index < planned_sessions:
            by_index[session_index] = record

    ordered_records = [by_index[index] for index in sorted(by_index)]
    completed_records = [record for record in ordered_records if bool(record.get("completed"))]
    rpes = [float(record["rpe"]) for record in completed_records if record.get("rpe") is not None]
    adverse_event = any(bool(record.get("adverse_event")) for record in ordered_records)
    felt_too_hard = any(bool(record.get("felt_too_hard")) for record in ordered_records)
    recorded_sessions = len(ordered_records)
    complete = recorded_sessions == planned_sessions
    ready_for_progression = complete or adverse_event

    return {
        "planned_sessions": planned_sessions,
        "recorded_sessions": recorded_sessions,
        "missing_session_indexes": [index for index in range(planned_sessions) if index not in by_index],
        "completed_sessions": len(completed_records),
        "average_rpe": round(sum(rpes) / len(rpes), 1) if rpes else None,
        "felt_too_hard": felt_too_hard,
        "adverse_event": adverse_event,
        "week_complete": complete,
        "ready_for_progression": ready_for_progression,
        "weekly_feedback": {
            "completed_sessions": len(completed_records),
            "average_rpe": round(sum(rpes) / len(rpes), 1) if rpes else None,
            "felt_too_hard": felt_too_hard,
            "adverse_event": adverse_event,
        }
        if ready_for_progression
        else None,
    }
