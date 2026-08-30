"""Executable 4-week training block view for SportRx.

This module turns an available Starter Path plus the Core FITT-VP plan into a
clear training block. It does not create a new training model or override the
measurement gate.
"""

from __future__ import annotations

from typing import Any

from .automation_guard import build_automation_guard


CLAIM_BOUNDARY = (
    "Training blocks are rule-based starter prescriptions. They are not medical "
    "clearance, race prediction, injury-risk estimates, or individualized coaching."
)


def _session_purpose(focus: str, session_index: int) -> str:
    focus_lower = focus.lower()
    if "retest" in focus_lower:
        return "Retest anchor"
    if "station" in focus_lower or "strength" in focus_lower:
        return "Station practice"
    if "running" in focus_lower or "aerobic" in focus_lower:
        return "Aerobic base"
    if "mixed" in focus_lower or "transition" in focus_lower:
        return "Controlled mixed work"
    return ["Build consistency", "Practice repeatability", "Prepare for retest"][min(session_index, 2)]


def _session_from_core(session: dict[str, Any], focus: str, index: int) -> dict[str, Any]:
    return {
        "session_id": f"{session.get('day', 'session').lower()}_{index + 1}",
        "day": session.get("day"),
        "purpose": _session_purpose(focus, index),
        "activity": session.get("activity"),
        "duration_min": session.get("duration_min"),
        "intensity": session.get("intensity"),
        "rpe_0_10": session.get("rpe_0_10"),
        "talk_test": session.get("talk_test"),
        "target_hr_zone_bpm": session.get("target_hr_zone_bpm"),
        "status": session.get("status"),
        "execution_note": "Keep this repeatable; record completion and session RPE after training.",
    }


def build_training_block(
    passport: dict[str, Any],
    core_plan: dict[str, Any],
    feedback_by_week: dict[int, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a reportable 4-week starter training block."""

    automation_guard = build_automation_guard(feedback_by_week)
    if not automation_guard["automated_outputs_allowed"]:
        return {
            "schema": "sportrx.training_block",
            "schema_version": "0.1",
            "available": False,
            "reason": automation_guard["reason"],
            "next_action": automation_guard["next_action"],
            "weeks": [],
            "automation_guard": automation_guard,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    starter_path = passport.get("starter_path", {})
    if not starter_path.get("available"):
        return {
            "schema": "sportrx.training_block",
            "schema_version": "0.1",
            "available": False,
            "reason": starter_path.get("reason", "Starter Path is not available."),
            "next_action": starter_path.get("next_action", passport.get("next_action", "Complete benchmark first.")),
            "weeks": [],
            "automation_guard": automation_guard,
            "claim_boundary": CLAIM_BOUNDARY,
        }

    core_weeks = {week["week"]: week for week in core_plan.get("weeks", [])}
    week_blocks = []
    for starter_week in starter_path.get("weeks", []):
        week_number = int(starter_week["week"])
        core_week = core_weeks.get(week_number, {})
        sessions = [
            _session_from_core(session, starter_week["focus"], index)
            for index, session in enumerate(core_week.get("sessions", []))
        ]
        week_blocks.append(
            {
                "week": week_number,
                "focus": starter_week["focus"],
                "starter_instruction": starter_week["instruction"],
                "weekly_minutes": core_week.get("weekly_minutes"),
                "frequency_per_week": core_week.get("frequency_per_week"),
                "duration_min": core_week.get("duration_min"),
                "fitt_vp": core_week.get("fitt_vp", {}),
                "sessions": sessions,
                "review_prompt": "Record completed sessions, average RPE, and whether the week felt too hard.",
            }
        )

    return {
        "schema": "sportrx.training_block",
        "schema_version": "0.1",
        "available": True,
        "event_pack": starter_path.get("event_pack"),
        "based_on_gap": starter_path.get("based_on_gap"),
        "training_profile": passport.get("training_profile"),
        "safety_gate_status": passport.get("safety_gate", {}).get("status"),
        "automation_guard": automation_guard,
        "weeks": week_blocks,
        "progression_policy": [
            "Progress weekly from completion and RPE feedback.",
            "Do not increase intensity and volume at the same time.",
            "Pause automated progression if adverse symptoms are reported.",
            "Retest with the same benchmark protocol when possible.",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def training_block_markdown(block: dict[str, Any]) -> str:
    """Export a training block as plain markdown."""

    lines = [
        "# SportRx 4-Week Starter Path",
        "",
        f"- Available: {block['available']}",
        f"- Claim boundary: {block['claim_boundary']}",
    ]
    if not block["available"]:
        lines.extend(["", f"- Reason: {block['reason']}", f"- Next action: {block['next_action']}"])
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            f"- Based on gap: {block['based_on_gap']}",
            f"- Training profile: {block['training_profile']}",
            f"- Safety Gate: {block['safety_gate_status']}",
            "",
            "## Progression Policy",
        ]
    )
    for item in block["progression_policy"]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("## Weekly Block")
    for week in block["weeks"]:
        lines.extend(
            [
                "",
                f"### Week {week['week']}: {week['focus']}",
                f"- Starter instruction: {week['starter_instruction']}",
                f"- Frequency: {week['frequency_per_week']} sessions/week",
                f"- Duration: {week['duration_min']} min/session",
                f"- Weekly minutes: {week['weekly_minutes']}",
            ]
        )
        for session in week["sessions"]:
            lines.append(
                f"- {session['day']}: {session['purpose']} - {session['activity']}, "
                f"{session['duration_min']} min, RPE {session['rpe_0_10']}"
            )
    return "\n".join(lines) + "\n"
