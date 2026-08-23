"""Experimental event-fit matching for SportRx Labs.

Event matching is a decision-support layer. It estimates preparation fit from
current activity, sport experience, and readiness. It does not certify safety or
predict race outcomes.
"""

from __future__ import annotations

from typing import Any

from .readiness import calculate_readiness


EVENTS = {
    "5k": {
        "name": "5K run",
        "pack_status": "registry_ready",
        "mvpa": 45,
        "days": 2,
        "running_minutes": 20,
        "strength_days": 0,
    },
    "10k": {
        "name": "10K run",
        "pack_status": "registry_ready",
        "mvpa": 90,
        "days": 3,
        "running_minutes": 45,
        "strength_days": 0,
    },
    "half_marathon": {
        "name": "Half marathon",
        "pack_status": "future",
        "mvpa": 150,
        "days": 3,
        "running_minutes": 90,
        "strength_days": 1,
    },
    "hyrox": {
        "name": "HYROX-style fitness race",
        "pack_status": "enabled",
        "mvpa": 120,
        "days": 3,
        "running_minutes": 45,
        "strength_days": 2,
    },
    "crossfit_intro": {
        "name": "CrossFit beginner class",
        "pack_status": "future",
        "mvpa": 90,
        "days": 2,
        "running_minutes": 0,
        "strength_days": 2,
    },
    "sprint_triathlon": {
        "name": "Sprint triathlon",
        "pack_status": "future",
        "mvpa": 180,
        "days": 4,
        "running_minutes": 45,
        "strength_days": 1,
        "requires_swim_bike": True,
    },
}


def _ratio(value: float, target: float) -> float:
    if target <= 0:
        return 1.0
    return max(0.0, min(value / target, 1.0))


def _stars(score: float) -> int:
    if score >= 0.82:
        return 5
    if score >= 0.66:
        return 4
    if score >= 0.50:
        return 3
    if score >= 0.34:
        return 2
    return 1


def match_events(profile: dict[str, Any]) -> dict[str, Any]:
    """Return ranked event matches from current readiness inputs."""

    readiness = calculate_readiness(profile)
    if readiness["score"] is None:
        return {
            "readiness": readiness,
            "matches": [],
            "note": "Event matching is unavailable until the safety screen is resolved.",
        }

    mvpa = float(profile.get("mvpa_minutes_per_week", 0) or 0)
    days = float(profile.get("exercise_days_last_4w", 0) or 0)
    running_minutes = float(profile.get("running_minutes_per_week", 0) or 0)
    strength_days = float(profile.get("strength_days_per_week", 0) or 0)
    swim_experience = bool(profile.get("swim_experience", False))
    bike_experience = bool(profile.get("bike_experience", False))
    recent_injury = bool(profile.get("recent_injury", False))
    readiness_ratio = readiness["score"] / 100

    matches = []
    for event_id, event in EVENTS.items():
        components = {
            "readiness": readiness_ratio,
            "aerobic_base": _ratio(mvpa, event["mvpa"]),
            "consistency": _ratio(days, event["days"]),
            "running_specificity": _ratio(running_minutes, event["running_minutes"]),
            "strength_specificity": _ratio(strength_days, event["strength_days"]),
        }

        if event.get("requires_swim_bike"):
            components["swim_bike_specificity"] = 1.0 if swim_experience and bike_experience else 0.25

        score = (
            components["readiness"] * 0.30
            + components["aerobic_base"] * 0.25
            + components["consistency"] * 0.15
            + components["running_specificity"] * 0.15
            + components["strength_specificity"] * 0.10
            + components.get("swim_bike_specificity", 1.0) * 0.05
        )

        if recent_injury:
            score -= 0.10

        star_rating = _stars(score)
        if star_rating >= 5:
            status = "recommended"
        elif star_rating == 4:
            status = "possible_with_preparation"
        elif star_rating == 3:
            status = "base_building_needed"
        else:
            status = "not_recommended_yet"

        gaps = []
        if components["aerobic_base"] < 0.7:
            gaps.append("increase aerobic base")
        if components["running_specificity"] < 0.7 and event["running_minutes"] > 0:
            gaps.append("add running-specific preparation")
        if components["strength_specificity"] < 0.7 and event["strength_days"] > 0:
            gaps.append("add strength preparation")
        if event.get("requires_swim_bike") and components["swim_bike_specificity"] < 0.7:
            gaps.append("build swim and bike experience")

        matches.append(
            {
                "event_id": event_id,
                "event": event["name"],
                "pack_status": event.get("pack_status", "future"),
                "stars": star_rating,
                "status": status,
                "fit_score": round(max(score, 0), 2),
                "gaps": gaps[:3],
                "rationale": f"{event['name']} fit is based on readiness, aerobic base, consistency, and sport-specific preparation.",
            }
        )

    return {
        "readiness": readiness,
        "matches": sorted(matches, key=lambda item: item["fit_score"], reverse=True),
        "note": "Event matching is experimental decision support, not medical clearance or race prediction.",
    }
