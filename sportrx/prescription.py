"""Prescription assembly for SportRx v0.1."""

from __future__ import annotations

from typing import Any

from .assessment import classify_fitness
from .intensity import calculate_intensity
from .plan_actual import provisional_plan_actual
from .progression import apply_progression, evaluate_week
from .readiness import calculate_readiness
from .screening import screen_user
from .volume import estimate_initial_volume


DAY_PATTERNS = {
    1: ["Saturday"],
    2: ["Tuesday", "Saturday"],
    3: ["Tuesday", "Thursday", "Sunday"],
    4: ["Monday", "Wednesday", "Friday", "Sunday"],
    5: ["Monday", "Tuesday", "Thursday", "Saturday", "Sunday"],
    6: ["Monday", "Tuesday", "Wednesday", "Friday", "Saturday", "Sunday"],
    7: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
}


def _default_activity(profile: dict[str, Any]) -> str:
    preferred = str(profile.get("preferred_activity", "") or "").strip()
    if preferred:
        return preferred
    common = str(profile.get("common_activity", "") or "").strip()
    return common or "brisk walking"


def _week_sessions(week: int, volume: dict[str, Any], profile: dict[str, Any], intensity: dict[str, Any]) -> list[dict[str, Any]]:
    frequency = int(volume.get("frequency_per_week", 0))
    if frequency <= 0:
        return []

    days = DAY_PATTERNS.get(frequency, DAY_PATTERNS[3])
    activity = _default_activity(profile)
    return [
        {
            "day": day,
            "activity": activity,
            "duration_min": int(volume["duration_min"]),
            "intensity": intensity["level"],
            "target_hr_zone_bpm": intensity["target_hr_zone_bpm"],
            "hrr_target_zone_bpm": intensity["hrr_target_zone_bpm"],
            "rpe_0_10": intensity["rpe_0_10"],
            "talk_test": intensity["talk_test"],
            "status": "provisional" if week > 1 else "ready",
        }
        for day in days
    ]


def generate_prescription(
    profile: dict[str, Any],
    feedback_by_week: dict[int, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Generate a 4-week aerobic FITT-VP prescription."""

    feedback_by_week = feedback_by_week or {}
    safety = screen_user(profile)
    if not safety["auto_prescription"]:
        return {
            "product": "SportRx",
            "version": "0.1.0",
            "safety": safety,
            "readiness": calculate_readiness(profile),
            "weeks": [],
        }

    assessment = classify_fitness(profile)
    readiness = calculate_readiness(profile)
    intensity_level = "light_to_moderate" if assessment["fitness_class"] == "inactive" else "moderate"
    intensity = calculate_intensity(profile, intensity_level)
    available_days = int(profile.get("available_days_per_week", 3) or 3)
    max_session = int(profile.get("max_minutes_per_session", 30) or 30)

    current_volume = estimate_initial_volume(profile, assessment)
    weeks: list[dict[str, Any]] = []
    progression_log: list[dict[str, Any]] = []

    for week in range(1, 5):
        if week > 1:
            feedback = feedback_by_week.get(week - 1)
            if feedback:
                decision = evaluate_week(
                    planned_sessions=int(current_volume["frequency_per_week"]),
                    completed_sessions=int(feedback.get("completed_sessions", 0) or 0),
                    average_rpe=feedback.get("average_rpe"),
                    felt_too_hard=bool(feedback.get("felt_too_hard", False)),
                    adverse_event=bool(feedback.get("adverse_event", False)),
                )
            else:
                decision = {
                    "action": "small_increase",
                    "change_pct": 0.10,
                    "completion_rate": None,
                    "average_rpe": None,
                    "felt_too_hard": False,
                    "adverse_event": False,
                    "rationale": "No feedback entered; this is a provisional 10% progression preview.",
                    "plan_actual": provisional_plan_actual(int(current_volume["frequency_per_week"])),
                    "reason_codes": ["PROVISIONAL_NO_FEEDBACK"],
                    "flags": [],
                }

            next_volume = apply_progression(current_volume, decision, available_days, max_session)
            progression_log.append({"after_week": week - 1, "decision": decision, "next_volume": next_volume})
            current_volume = next_volume

        weeks.append(
            {
                "week": week,
                "frequency_per_week": int(current_volume.get("frequency_per_week", 0)),
                "duration_min": int(current_volume.get("duration_min", 0)),
                "weekly_minutes": int(current_volume.get("weekly_minutes", 0)),
                "fitt_vp": {
                    "frequency": f"{current_volume.get('frequency_per_week', 0)} days/week",
                    "intensity": intensity["level"],
                    "time": f"{current_volume.get('duration_min', 0)} min/session",
                    "type": _default_activity(profile),
                    "volume": f"{current_volume.get('weekly_minutes', 0)} min/week",
                    "progression": "Adjusted weekly from completion and RPE feedback.",
                },
                "sessions": _week_sessions(week, current_volume, profile, intensity),
            }
        )

        if current_volume.get("paused"):
            break

    return {
        "product": "SportRx",
        "version": "0.1.0",
        "goal": profile.get("goal", "Improve aerobic fitness / general health"),
        "safety": safety,
        "assessment": assessment,
        "readiness": readiness,
        "intensity": intensity,
        "initial_volume": weeks[0] if weeks else None,
        "weeks": weeks,
        "progression_log": progression_log,
        "scope": "Apparently healthy adults, aerobic exercise only.",
    }
