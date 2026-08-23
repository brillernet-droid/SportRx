"""Aerobic intensity calculations for SportRx v0.1."""

from __future__ import annotations

from typing import Any


INTENSITY_ZONES = {
    "light": {
        "hrmax_pct": (0.57, 0.63),
        "hrr_pct": (0.30, 0.39),
        "rpe_0_10": (3, 4),
        "talk_test": "Easy conversation should be possible.",
    },
    "light_to_moderate": {
        "hrmax_pct": (0.57, 0.70),
        "hrr_pct": (0.30, 0.50),
        "rpe_0_10": (3, 5),
        "talk_test": "Talking should be comfortable; singing becomes harder near the top of the range.",
    },
    "moderate": {
        "hrmax_pct": (0.64, 0.76),
        "hrr_pct": (0.40, 0.59),
        "rpe_0_10": (5, 6),
        "talk_test": "You can talk, but singing should be difficult.",
    },
}


def estimate_hrmax(age: int) -> int:
    """Estimate maximal heart rate with the simple 220-age equation."""

    return max(80, 220 - int(age))


def calculate_intensity(profile: dict[str, Any], level: str = "moderate") -> dict[str, Any]:
    """Return target HR and RPE ranges for a selected aerobic intensity level."""

    if level not in INTENSITY_ZONES:
        raise ValueError(f"Unknown intensity level: {level}")

    age = int(profile.get("age", 0) or 0)
    resting_hr = int(profile.get("resting_hr", 0) or 0)
    hrmax = estimate_hrmax(age)
    zone = INTENSITY_ZONES[level]
    hrmax_pct = zone["hrmax_pct"]
    hrr_pct = zone["hrr_pct"]

    target_hr_zone = (
        round(hrmax * hrmax_pct[0]),
        round(hrmax * hrmax_pct[1]),
    )

    hrr_zone = None
    if resting_hr > 0 and resting_hr < hrmax:
        reserve = hrmax - resting_hr
        hrr_zone = (
            round(resting_hr + reserve * hrr_pct[0]),
            round(resting_hr + reserve * hrr_pct[1]),
        )

    return {
        "level": level,
        "estimated_hrmax_bpm": hrmax,
        "target_hr_zone_bpm": target_hr_zone,
        "hrr_target_zone_bpm": hrr_zone,
        "rpe_0_10": zone["rpe_0_10"],
        "talk_test": zone["talk_test"],
        "method_note": "Heart-rate zones are estimates; RPE and talk test remain usable without a wearable.",
    }
