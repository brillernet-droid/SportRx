"""Shareable result-card data for SportRx Labs."""

from __future__ import annotations

from typing import Any


def build_sport_match_card(quick_match_result: dict[str, Any], short_url: str = "sportrx.local/labs") -> dict[str, Any]:
    """Build a QR-ready Sport Match card object."""

    top = quick_match_result["top_matches"][0]
    return {
        "brand": "SportRx Labs",
        "card_type": "sport_match",
        "event_profile": top["event_profile"],
        "training_profile": quick_match_result["athlete_profile_label"],
        "current_fit": top["fit_category"],
        "strongest_area": quick_match_result["strongest_capability"],
        "work_on_next": quick_match_result["obvious_limiter"],
        "tested": "Quick Match only",
        "short_url": short_url,
        "qr_ready": True,
        "disclaimer": "Current profile match only. Not innate ability, genetic suitability, or medical clearance.",
    }


def build_readiness_passport_card(passport: dict[str, Any], short_url: str = "sportrx.local/passport") -> dict[str, Any]:
    """Build a QR-ready race-check card object."""

    return {
        "brand": "SportRx Labs",
        "card_type": "race_check",
        "event_profile": f"{passport['event_profile_match']} Check",
        "training_profile": passport["training_profile"],
        "current_picture": passport["current_measured_picture"],
        "safety_gate": passport["safety_gate"]["status"],
        "strongest_area": passport["strongest_area"],
        "work_on_next": passport["main_gap"],
        "tested": passport["areas_assessed"]["label"],
        "short_url": short_url,
        "qr_ready": True,
        "disclaimer": "Prototype race check. Not medical clearance, race prediction, or injury prediction.",
    }
