"""Rule-coded plan-versus-actual feedback explanations.

This layer makes weekly progression decisions inspectable without adding new
training-load models or injury-risk predictions.
"""

from __future__ import annotations

from typing import Any


REASON_LABELS = {
    "ADVERSE_EVENT_REPORTED": "Adverse event reported",
    "HIGH_COMPLETION_LOW_RPE": "High completion with low RPE",
    "HIGH_COMPLETION_TARGET_RPE": "High completion with target RPE",
    "LOW_COMPLETION_HIGH_RPE": "Low completion with high RPE",
    "FEEDBACK_INCOMPLETE": "Feedback incomplete",
    "FELT_TOO_HARD": "Week felt too hard",
    "COMPLETION_BELOW_TARGET": "Completion below target",
    "RPE_ABOVE_TARGET": "RPE above target",
    "RPE_BELOW_TARGET": "RPE below target",
    "HOLD_FOR_STABILITY": "Hold for stability",
    "PROVISIONAL_NO_FEEDBACK": "Provisional preview without feedback",
}


ACTION_LABELS = {
    "pause": "Pause automated progression",
    "increase": "Increase dose",
    "small_increase": "Small increase",
    "decrease": "Decrease dose",
    "hold": "Hold current dose",
    "not_entered": "Not entered",
}


def classify_plan_actual(
    planned_sessions: int,
    completed_sessions: int | None,
    average_rpe: float | None,
    felt_too_hard: bool = False,
    adverse_event: bool = False,
) -> dict[str, Any]:
    """Return reason codes for a weekly plan-versus-actual comparison."""

    planned = max(1, int(planned_sessions or 1))
    completed = None if completed_sessions is None else max(0, min(int(completed_sessions), planned))
    completion_rate = None if completed is None else round(completed / planned, 2)
    flags: list[str] = []

    if adverse_event:
        reason_codes = ["ADVERSE_EVENT_REPORTED"]
        action = "pause"
    elif completed is None or average_rpe is None:
        reason_codes = ["FEEDBACK_INCOMPLETE"]
        action = "not_entered"
    elif completion_rate is not None and completion_rate >= 0.8 and average_rpe < 4 and not felt_too_hard:
        reason_codes = ["HIGH_COMPLETION_LOW_RPE", "RPE_BELOW_TARGET"]
        action = "increase"
    elif completion_rate is not None and completion_rate >= 0.8 and 4 <= average_rpe <= 6 and not felt_too_hard:
        reason_codes = ["HIGH_COMPLETION_TARGET_RPE"]
        action = "small_increase"
    elif completion_rate is not None and completion_rate < 0.6 and (felt_too_hard or average_rpe >= 7):
        reason_codes = ["LOW_COMPLETION_HIGH_RPE"]
        action = "decrease"
    else:
        reason_codes = ["HOLD_FOR_STABILITY"]
        action = "hold"

    if felt_too_hard:
        flags.append("FELT_TOO_HARD")
    if completion_rate is not None and completion_rate < 0.8:
        flags.append("COMPLETION_BELOW_TARGET")
    if average_rpe is not None and average_rpe > 6:
        flags.append("RPE_ABOVE_TARGET")
    if average_rpe is not None and average_rpe < 4:
        flags.append("RPE_BELOW_TARGET")

    return {
        "planned_sessions": planned,
        "completed_sessions": completed,
        "completion_rate": completion_rate,
        "average_rpe": average_rpe,
        "felt_too_hard": bool(felt_too_hard),
        "adverse_event": bool(adverse_event),
        "action": action,
        "action_label": ACTION_LABELS.get(action, action),
        "reason_codes": reason_codes,
        "reason_labels": [REASON_LABELS[code] for code in reason_codes],
        "flags": flags,
        "flag_labels": [REASON_LABELS[code] for code in flags],
        "claim_boundary": (
            "Plan-actual reason codes explain rule-based weekly adjustment only. "
            "They are not recovery scores, risk predictions, or medical advice."
        ),
    }


def provisional_plan_actual(planned_sessions: int) -> dict[str, Any]:
    """Return a reason object for a no-feedback provisional preview."""

    return {
        "planned_sessions": max(1, int(planned_sessions or 1)),
        "completed_sessions": None,
        "completion_rate": None,
        "average_rpe": None,
        "felt_too_hard": False,
        "adverse_event": False,
        "action": "small_increase",
        "action_label": ACTION_LABELS["small_increase"],
        "reason_codes": ["PROVISIONAL_NO_FEEDBACK"],
        "reason_labels": [REASON_LABELS["PROVISIONAL_NO_FEEDBACK"]],
        "flags": [],
        "flag_labels": [],
        "claim_boundary": (
            "This is a provisional preview. Enter weekly completion and RPE before "
            "treating it as an adaptive progression decision."
        ),
    }
