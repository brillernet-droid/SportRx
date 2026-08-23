"""Adaptive weekly progression rules for SportRx v0.1."""

from __future__ import annotations

from typing import Any

from .plan_actual import classify_plan_actual
from .volume import clamp, reshape_volume


def evaluate_week(
    planned_sessions: int,
    completed_sessions: int,
    average_rpe: float | None,
    felt_too_hard: bool = False,
    adverse_event: bool = False,
) -> dict[str, Any]:
    """Classify weekly feedback into a progression decision."""

    planned_sessions = max(1, int(planned_sessions))
    completed_sessions = clamp(int(completed_sessions), 0, planned_sessions)
    completion_rate = completed_sessions / planned_sessions
    plan_actual = classify_plan_actual(
        planned_sessions,
        completed_sessions,
        average_rpe,
        felt_too_hard=felt_too_hard,
        adverse_event=adverse_event,
    )

    if plan_actual["action"] == "pause":
        action = "pause"
        change_pct = 0.0
        rationale = "An adverse symptom/event was reported, so automatic adjustment is paused."
    elif plan_actual["action"] == "increase":
        action = "increase"
        change_pct = 0.15
        rationale = "Completion was high and RPE was below the target range."
    elif plan_actual["action"] == "small_increase":
        action = "small_increase"
        change_pct = 0.10
        rationale = "Completion was high and RPE stayed in an appropriate range."
    elif plan_actual["action"] == "decrease":
        action = "decrease"
        change_pct = -0.10
        rationale = "Completion was low and perceived difficulty was high."
    else:
        action = "hold"
        change_pct = 0.0
        rationale = "Feedback suggests holding the current dose before progressing."

    return {
        "action": action,
        "change_pct": change_pct,
        "completion_rate": round(completion_rate, 2),
        "average_rpe": average_rpe,
        "felt_too_hard": felt_too_hard,
        "adverse_event": adverse_event,
        "rationale": rationale,
        "plan_actual": plan_actual,
        "reason_codes": plan_actual["reason_codes"],
        "flags": plan_actual["flags"],
    }


def apply_progression(
    current_volume: dict[str, Any],
    decision: dict[str, Any],
    available_days: int,
    max_session: int,
) -> dict[str, Any]:
    """Apply a weekly feedback decision to the next week's dose."""

    if decision["action"] == "pause":
        return {
            "frequency_per_week": 0,
            "duration_min": 0,
            "weekly_minutes": 0,
            "paused": True,
        }

    current_total = int(current_volume["weekly_minutes"])
    ceiling = int(current_volume.get("progression_ceiling_min", min(150, available_days * max_session)))
    next_total = round(current_total * (1 + float(decision["change_pct"])))

    if decision["action"] in {"increase", "small_increase"}:
        next_total = max(current_total + 5, next_total)
    elif decision["action"] == "decrease":
        next_total = min(current_total - 5, next_total)

    next_total = clamp(next_total, 10, ceiling)
    shaped = reshape_volume(
        total_minutes=next_total,
        available_days=available_days,
        max_session=max_session,
        preferred_frequency=int(current_volume["frequency_per_week"]),
    )

    if decision["action"] in {"increase", "small_increase"} and shaped["weekly_minutes"] <= current_total:
        if shaped["duration_min"] + 5 <= max_session:
            shaped["duration_min"] += 5
            shaped["weekly_minutes"] = shaped["frequency_per_week"] * shaped["duration_min"]
        elif shaped["frequency_per_week"] < available_days:
            shaped["frequency_per_week"] += 1
            shaped["weekly_minutes"] = shaped["frequency_per_week"] * shaped["duration_min"]

    if decision["action"] == "decrease" and shaped["weekly_minutes"] >= current_total:
        if shaped["duration_min"] - 5 >= 10:
            shaped["duration_min"] -= 5
            shaped["weekly_minutes"] = shaped["frequency_per_week"] * shaped["duration_min"]

    shaped["progression_ceiling_min"] = ceiling
    shaped["paused"] = False
    return shaped
