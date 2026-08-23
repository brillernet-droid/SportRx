"""GREEN/YELLOW/RED safety gate for SportRx 2.0.

The safety gate is independent from performance. It does not diagnose disease,
estimate medical risk percentages, or clear a user for competition.
"""

from __future__ import annotations

from typing import Any


WARNING_SYMPTOMS = {
    "chest_pain",
    "unexplained_shortness_of_breath",
    "dizziness_or_syncope",
    "palpitations",
    "ankle_swelling",
    "known_heart_murmur",
    "pain_with_walking",
}

RELEVANT_CONDITIONS = {
    "cardiovascular_disease",
    "metabolic_disease",
    "renal_disease",
    "pulmonary_disease",
}

HIGH_INTENSITY_GOALS = {
    "hybrid_race",
    "race",
    "improve_performance",
    "high_intensity",
    "hyrox",
    "crossfit",
}


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def evaluate_safety_gate(profile: dict[str, Any]) -> dict[str, Any]:
    """Return a GREEN, YELLOW, or RED safety status."""

    flags: list[str] = []
    reasons: list[str] = []
    age = int(profile.get("age", 0) or 0)
    intended_intensity = str(profile.get("intended_intensity", "") or "").lower()
    primary_goal = str(profile.get("primary_goal", profile.get("goal", "")) or "").lower()

    symptoms = sorted(set(_as_list(profile.get("symptoms"))) & WARNING_SYMPTOMS)
    if symptoms:
        flags.extend(f"SYMPTOM_{item.upper()}" for item in symptoms)
        reasons.append("Relevant signs or symptoms were reported.")

    if age and age < 18:
        flags.append("AGE_UNDER_18")
        reasons.append("SportRx 2.0 web demo is intended for adults.")

    high_intensity_intent = intended_intensity in {"vigorous", "high"} or any(
        token in primary_goal for token in HIGH_INTENSITY_GOALS
    )

    conditions = sorted(set(_as_list(profile.get("known_conditions"))) & RELEVANT_CONDITIONS)
    if conditions:
        flags.extend(f"CONDITION_{item.upper()}" for item in conditions)
        reasons.append("A relevant cardiovascular, metabolic, renal, or pulmonary condition was reported.")

    if profile.get("pregnant") is True:
        flags.append("PREGNANCY_SCOPE")
        reasons.append("Pregnancy/postpartum exercise decisions require a more specific pathway.")

    if profile.get("recent_major_injury") is True:
        flags.append("RECENT_MAJOR_INJURY")
        reasons.append("A recent major injury was reported.")

    if symptoms or age < 18:
        status = "RED"
        training_handoff = False
        recommendation = "Stop automated training handoff and seek appropriate professional assessment."
    elif conditions and high_intensity_intent:
        status = "RED"
        training_handoff = False
        recommendation = "High-intensity participation should not be handed off automatically."
    elif conditions or profile.get("pregnant") is True or profile.get("recent_major_injury") is True:
        status = "YELLOW"
        training_handoff = True
        recommendation = "Further professional assessment or clarification is recommended before high-intensity participation."
    else:
        status = "GREEN"
        training_handoff = True
        recommendation = "No major automated stop flag identified."

    return {
        "status": status,
        "flags": flags,
        "reasons": reasons,
        "training_handoff_allowed": training_handoff,
        "recommendation": recommendation,
        "disclaimer": "SportRx does not provide medical diagnosis, medical clearance, or emergency advice.",
    }
