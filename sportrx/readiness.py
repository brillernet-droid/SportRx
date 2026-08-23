"""Sport readiness scoring for SportRx.

The readiness score is a product signal, not a medical clearance score. It is
designed to summarize whether a user appears ready for gradual exercise
progression under the narrow prototype assumptions.
"""

from __future__ import annotations

from typing import Any

from .assessment import classify_fitness
from .safety_gate import evaluate_safety_gate


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))


def _bmi(profile: dict[str, Any]) -> float | None:
    height_cm = float(profile.get("height_cm", 0) or 0)
    weight_kg = float(profile.get("weight_kg", 0) or 0)
    if height_cm <= 0 or weight_kg <= 0:
        return None
    return weight_kg / ((height_cm / 100) ** 2)


def calculate_readiness(profile: dict[str, Any]) -> dict[str, Any]:
    """Calculate an explainable 0-100 sport readiness score."""

    safety = evaluate_safety_gate(profile)
    assessment = classify_fitness(profile)

    if safety["status"] == "RED":
        return {
            "score": None,
            "band": "needs_review",
            "label": "Needs further review",
            "strengths": [],
            "risks": safety["reasons"],
            "recommendations": [
                "Do not use SportRx for automatic prescription until the safety screen is resolved."
            ],
            "components": {"safety_gate": "blocked"},
            "note": "This is not medical clearance.",
        }

    mvpa = int(profile.get("mvpa_minutes_per_week", 0) or 0)
    days = int(profile.get("exercise_days_last_4w", 0) or 0)
    available_days = int(profile.get("available_days_per_week", 3) or 3)
    max_session = int(profile.get("max_minutes_per_session", 30) or 30)
    sleep_hours = profile.get("sleep_hours")
    stress_1_10 = profile.get("stress_1_10")
    resting_hr = int(profile.get("resting_hr", 0) or 0)
    recent_injury = bool(profile.get("recent_injury", False))

    activity_score = _clamp((mvpa / 150) * 28, 0, 28)
    consistency_score = _clamp((days / 4) * 16, 0, 16)
    capacity_score = _clamp(((available_days * max_session) / 150) * 18, 0, 18)

    if sleep_hours is None:
        recovery_score = 10
    else:
        recovery_score = _clamp((float(sleep_hours) - 5) / 3 * 12, 0, 12)

    if stress_1_10 is None:
        stress_score = 8
    else:
        stress_score = _clamp((10 - float(stress_1_10)) / 9 * 10, 0, 10)

    physiology_score = 16
    risks: list[str] = []
    strengths: list[str] = []
    recommendations: list[str] = []

    bmi = _bmi(profile)
    if bmi is not None:
        if bmi >= 30:
            physiology_score -= 6
            risks.append("BMI is in a range where gradual progression and joint-load management matter.")
        elif 18.5 <= bmi < 25:
            strengths.append("BMI is within a common reference range.")

    systolic_bp = profile.get("systolic_bp")
    diastolic_bp = profile.get("diastolic_bp")
    if systolic_bp is not None and diastolic_bp is not None:
        if int(systolic_bp) >= 140 or int(diastolic_bp) >= 90:
            physiology_score -= 8
            risks.append("Reported blood pressure is elevated; SportRx should stay conservative.")

    if resting_hr >= 85:
        physiology_score -= 4
        risks.append("Resting heart rate is relatively high, so intensity should be monitored carefully.")
    elif 45 <= resting_hr <= 70:
        strengths.append("Resting heart rate is compatible with ordinary aerobic progression.")

    if recent_injury:
        physiology_score -= 10
        risks.append("Recent injury history increases progression risk.")

    if safety["status"] == "YELLOW":
        physiology_score -= 6
        risks.append("Safety gate is YELLOW; high-intensity participation needs clarification.")

    physiology_score = _clamp(physiology_score, 0, 16)
    score = round(activity_score + consistency_score + capacity_score + recovery_score + stress_score + physiology_score)
    if safety["status"] == "YELLOW":
        score = min(score, 69)

    if assessment["fitness_class"] == "active":
        strengths.append("Current activity already approaches common adult aerobic targets.")
    elif assessment["fitness_class"] == "low_active":
        strengths.append("Some recent exercise history is present.")
    else:
        risks.append("Current aerobic base is low; avoid rapid jumps in weekly volume.")

    if available_days * max_session >= 120:
        strengths.append("Available weekly time is enough for a realistic progression path.")
    else:
        risks.append("Available exercise time is limited, so goals should be staged.")

    if score >= 85:
        band = "high"
        label = "High readiness"
        recommendations.append("Use gradual progression and monitor RPE, but no major prototype-level barrier is detected.")
    elif score >= 70:
        band = "moderate_high"
        label = "Ready with gradual progression"
        recommendations.append("Start with a conservative 4-week progression and reassess weekly completion and RPE.")
    elif score >= 50:
        band = "moderate"
        label = "Build base first"
        recommendations.append("Prioritize consistency and aerobic base before aggressive event-specific training.")
    else:
        band = "low"
        label = "Low readiness"
        recommendations.append("Use a low-dose starter plan and resolve risk factors before challenging events.")

    return {
        "score": int(score),
        "band": band,
        "label": label,
        "strengths": strengths[:4],
        "risks": risks[:4],
        "recommendations": recommendations,
        "components": {
            "safety_gate": safety["status"],
            "activity": round(activity_score, 1),
            "consistency": round(consistency_score, 1),
            "time_capacity": round(capacity_score, 1),
            "recovery": round(recovery_score, 1),
            "stress": round(stress_score, 1),
            "physiology": round(physiology_score, 1),
        },
        "note": "This score supports exercise decisions but is not medical clearance.",
    }
