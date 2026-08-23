"""Human-readable explanations for SportRx rule outputs."""

from __future__ import annotations

from typing import Any


def explain_prescription(output: dict[str, Any]) -> str:
    """Explain the generated plan without delegating authority to an LLM."""

    safety = output.get("safety", {})
    if not safety.get("auto_prescription", False):
        reasons = " ".join(safety.get("reasons", []))
        return f"SportRx is not generating an automatic plan because: {reasons}"

    assessment = output["assessment"]
    week1 = output["weeks"][0]
    intensity = output["intensity"]
    return (
        f"SportRx classified the current activity state as {assessment['fitness_class']}. "
        f"Week 1 starts with {week1['frequency_per_week']} sessions of about "
        f"{week1['duration_min']} minutes, totaling {week1['weekly_minutes']} minutes. "
        f"The target intensity is {intensity['level']}, using RPE {intensity['rpe_0_10'][0]}-"
        f"{intensity['rpe_0_10'][1]} on a 0-10 scale and an estimated heart-rate zone of "
        f"{intensity['target_hr_zone_bpm'][0]}-{intensity['target_hr_zone_bpm'][1]} bpm."
    )


def explain_progression(decision: dict[str, Any]) -> str:
    """Explain a progression decision in product language."""

    action = decision.get("action", "hold")
    if action == "pause":
        return "Automatic adjustment is paused because a potential safety issue was reported."
    if action == "increase":
        return "Next week can increase because completion was high and RPE was below the target range."
    if action == "small_increase":
        return "Next week can progress slightly because completion was high and RPE stayed appropriate."
    if action == "decrease":
        return "Next week should reduce load because completion was low and the week felt too hard."
    return "Next week should hold steady until the current dose feels repeatable."
