"""Safety screening rules for SportRx v0.1.

This module does not diagnose disease. It only decides whether SportRx should
continue with automated aerobic exercise prescription for the narrow v0.1
population: apparently healthy adults.
"""

from __future__ import annotations

from typing import Any

from .safety_gate import automated_handoff_allowed, evaluate_safety_gate


BLOCKING_SYMPTOMS = {
    "chest_pain",
    "unexplained_shortness_of_breath",
    "dizziness_or_syncope",
    "palpitations",
    "ankle_swelling",
    "known_heart_murmur",
    "pain_with_walking",
}

BLOCKING_CONDITIONS = {
    "cardiovascular_disease",
    "metabolic_disease",
    "renal_disease",
    "pulmonary_disease",
}


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def screen_user(profile: dict[str, Any]) -> dict[str, Any]:
    """Return whether automated prescription is allowed for this profile."""

    safety_gate = evaluate_safety_gate(profile)
    if isinstance(profile.get("venue_screening"), dict):
        allowed = automated_handoff_allowed(safety_gate)
        return {
            "auto_prescription": allowed,
            "safety_gate": safety_gate,
            "flags": list(safety_gate["flags"]),
            "reasons": list(safety_gate["reasons"]),
            "next_step": (
                "Continue to Benchmark."
                if allowed
                else "SportRX will not generate an automatic plan from Venue Entry. Follow the external screening pathway."
            ),
            "disclaimer": "SportRX is a non-diagnostic routing prototype and is not a medical diagnosis or emergency service.",
        }
    reasons: list[str] = []
    flags: list[str] = []
    age = int(profile.get("age", 0) or 0)

    if age < 18:
        reasons.append("SportRx v0.1 is limited to adults aged 18 or older.")
        flags.append("AGE_UNDER_18")
    if age > 64:
        reasons.append("SportRx v0.1 does not yet cover older-adult prescription.")
        flags.append("AGE_OVER_V01_SCOPE")

    symptoms = set(_as_list(profile.get("symptoms")))
    matched_symptoms = sorted(symptoms & BLOCKING_SYMPTOMS)
    if matched_symptoms:
        reasons.append("One or more exercise-related warning symptoms were reported.")
        flags.extend(f"SYMPTOM_{item.upper()}" for item in matched_symptoms)

    conditions = set(_as_list(profile.get("known_conditions")))
    matched_conditions = sorted(conditions & BLOCKING_CONDITIONS)
    if matched_conditions:
        reasons.append("A cardiovascular, metabolic, renal, or pulmonary condition was reported.")
        flags.extend(f"CONDITION_{item.upper()}" for item in matched_conditions)

    if profile.get("pregnant") is True:
        reasons.append("Pregnancy/postpartum exercise prescription is outside v0.1 scope.")
        flags.append("PREGNANCY_SCOPE")

    if safety_gate["status"] == "RED" and not reasons:
        reasons.extend(safety_gate["reasons"])
        flags.extend(safety_gate["flags"])

    auto_prescription = not reasons and safety_gate["automated_handoff_allowed"]
    return {
        "auto_prescription": auto_prescription,
        "safety_gate": safety_gate,
        "flags": flags,
        "reasons": reasons,
        "next_step": (
            "Continue to assessment."
            if auto_prescription
            else "SportRx will not generate an automatic plan. Consider professional evaluation before starting or changing exercise."
        ),
        "disclaimer": "SportRx is a prototype and is not a medical diagnosis or emergency service.",
    }
