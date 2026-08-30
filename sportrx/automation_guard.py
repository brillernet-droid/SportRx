"""Canonical hard-stop guard for post-feedback automated SportRX outputs."""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Automation Guard is a product stop rule. It does not diagnose an event, "
    "provide medical clearance, or decide when someone can resume exercise."
)


def build_automation_guard(feedback_by_week: dict[int, dict[str, Any]] | None = None) -> dict[str, Any]:
    """Block automated outputs whenever a user has reported an adverse event."""

    feedback_by_week = feedback_by_week or {}
    affected_weeks = sorted(
        int(week)
        for week, feedback in feedback_by_week.items()
        if bool(feedback.get("adverse_event"))
    )
    if affected_weeks:
        return {
            "status": "automation_hard_stop",
            "automated_outputs_allowed": False,
            "affected_weeks": affected_weeks,
            "reason": "An adverse event was reported. Automated training, progression, retest interpretation, and exports are paused.",
            "next_action": "Do not continue automated SportRX outputs until the issue has been reviewed outside this prototype.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    return {
        "status": "clear",
        "automated_outputs_allowed": True,
        "affected_weeks": [],
        "reason": None,
        "next_action": "No post-feedback hard stop is active.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
