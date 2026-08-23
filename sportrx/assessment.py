"""Simple current-activity classification for SportRx v0.1."""

from __future__ import annotations

from typing import Any


def classify_fitness(profile: dict[str, Any]) -> dict[str, Any]:
    """Classify current aerobic activity status using transparent rules."""

    days = int(profile.get("exercise_days_last_4w", 0) or 0)
    mvpa = int(profile.get("mvpa_minutes_per_week", 0) or 0)
    experience = str(profile.get("exercise_experience", "beginner") or "beginner")

    if days <= 0 or mvpa < 30:
        fitness_class = "inactive"
        summary = "Inactive: little structured moderate-to-vigorous activity in the last 4 weeks."
    elif days < 3 or mvpa < 150:
        fitness_class = "low_active"
        summary = "Low active: some recent activity, but below common adult aerobic targets."
    else:
        fitness_class = "active"
        summary = "Active: already meeting or approaching common adult aerobic targets."

    return {
        "fitness_class": fitness_class,
        "exercise_days_last_4w": days,
        "mvpa_minutes_per_week": mvpa,
        "exercise_experience": experience,
        "summary": summary,
        "rules": [
            "inactive if weekly MVPA < 30 min or 0 exercise days",
            "low_active if below 3 days/week or below 150 min/week",
            "active if >= 3 days/week and >= 150 min/week",
        ],
    }
