"""Weekly aerobic volume rules for SportRx v0.1."""

from __future__ import annotations

from typing import Any


def round_to_nearest_5(minutes: float) -> int:
    return int(round(minutes / 5) * 5)


def clamp(value: int, lower: int, upper: int) -> int:
    return max(lower, min(value, upper))


def estimate_initial_volume(profile: dict[str, Any], assessment: dict[str, Any]) -> dict[str, Any]:
    """Estimate a feasible Week 1 frequency-duration plan."""

    available_days = clamp(int(profile.get("available_days_per_week", 3) or 3), 1, 7)
    max_session = clamp(int(profile.get("max_minutes_per_session", 30) or 30), 10, 120)
    capacity = available_days * max_session
    current_mvpa = int(profile.get("mvpa_minutes_per_week", 0) or 0)
    fitness_class = assessment["fitness_class"]

    if fitness_class == "inactive":
        frequency = min(available_days, 3)
        target_total = min(capacity, max(30, min(75, current_mvpa + 45)))
    elif fitness_class == "low_active":
        frequency = min(available_days, 4)
        target_total = min(capacity, max(60, min(120, current_mvpa + 30)))
    else:
        frequency = min(available_days, 5)
        target_total = min(capacity, max(90, min(150, current_mvpa)))

    duration = clamp(round_to_nearest_5(target_total / frequency), 10, max_session)
    total = duration * frequency

    return {
        "frequency_per_week": frequency,
        "duration_min": duration,
        "weekly_minutes": total,
        "available_capacity_min": capacity,
        "progression_ceiling_min": min(150, capacity),
        "rule_note": "Week 1 balances guideline direction, recent activity, and stated time capacity.",
    }


def reshape_volume(total_minutes: int, available_days: int, max_session: int, preferred_frequency: int) -> dict[str, Any]:
    """Convert a weekly total into a practical frequency x duration shape."""

    available_days = clamp(available_days, 1, 7)
    max_session = clamp(max_session, 10, 120)
    total_minutes = clamp(total_minutes, 10, available_days * max_session)

    frequency = clamp(preferred_frequency, 1, available_days)
    duration = round_to_nearest_5(total_minutes / frequency)

    if duration > max_session and frequency < available_days:
        frequency = min(available_days, frequency + 1)
        duration = round_to_nearest_5(total_minutes / frequency)

    duration = clamp(duration, 10, max_session)
    return {
        "frequency_per_week": frequency,
        "duration_min": duration,
        "weekly_minutes": frequency * duration,
    }
