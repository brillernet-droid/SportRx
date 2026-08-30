"""Non-diagnostic safety routing for SportRX.

Venue Entry uses a configured external screening pathway and stores only its
member-reported route metadata. Legacy internal profiles retain their prior
prototype behaviour so historical local demos stay reproducible.
"""

from __future__ import annotations

from typing import Any

from .screening_provider_registry import get_screening_provider


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

ROUTE_ELIGIBLE = "eligible_for_benchmark"
ROUTE_FOLLOW_UP = "screening_follow_up_needed"
ROUTE_STOP = "stop_automation"
EXTERNAL_SCREENING_OUTCOMES = {"completed_continue", "follow_up_needed", "not_completed"}


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


def _venue_safety_gate(
    profile: dict[str, Any], providers: list[dict[str, Any]] | None, root: str
) -> dict[str, Any]:
    """Route a venue member without reading or preserving screening answers."""

    screening = profile.get("venue_screening") or {}
    age = int(profile.get("age", 0) or 0)
    provider_id = screening.get("provider_id")
    provider = get_screening_provider(provider_id, providers, root)
    consent = screening.get("consent") is True
    outcome = str(screening.get("member_reported_outcome", "not_completed"))
    changed_since_screening = screening.get("health_changed_since_screening") is True
    reasons: list[str] = []
    flags: list[str] = []

    if age < 18:
        route = ROUTE_STOP
        flags.append("ADULT_SCOPE_REQUIRED")
        reasons.append("SportRX Venue Entry is limited to adults aged 18 or older.")
    elif changed_since_screening:
        route = ROUTE_STOP
        flags.append("HEALTH_STATUS_CHANGED")
        reasons.append("A relevant change since the external screening was reported.")
    elif not consent:
        route = ROUTE_FOLLOW_UP
        flags.append("VENUE_ENTRY_CONSENT_REQUIRED")
        reasons.append("Consent is required before using the local venue-entry routing result.")
    elif not provider or provider.get("deployment_status") != "approved_for_venue":
        route = ROUTE_FOLLOW_UP
        flags.append("SCREENING_PATHWAY_NOT_APPROVED")
        reasons.append("No approved Chinese-context screening pathway is configured for this venue flow.")
    elif outcome not in EXTERNAL_SCREENING_OUTCOMES or outcome != "completed_continue":
        route = ROUTE_FOLLOW_UP
        flags.append("SCREENING_FOLLOW_UP_REQUIRED")
        reasons.append("The external screening pathway has not been completed for continued participation.")
    else:
        route = ROUTE_ELIGIBLE

    status = {ROUTE_ELIGIBLE: "GREEN", ROUTE_FOLLOW_UP: "YELLOW", ROUTE_STOP: "RED"}[route]
    benchmark_allowed = route == ROUTE_ELIGIBLE
    return {
        "status": status,
        "route": route,
        "flags": flags,
        "reasons": reasons,
        "benchmark_allowed": benchmark_allowed,
        "automated_handoff_allowed": benchmark_allowed,
        "training_handoff_allowed": benchmark_allowed,
        "deployment_status": "venue_ready" if provider and provider.get("deployment_status") == "approved_for_venue" else "demo_only",
        "screening_provider_id": provider_id,
        "screening_provider_version": screening.get("provider_version"),
        "member_reported_outcome": outcome,
        "disclaimer": "SportRX does not provide medical diagnosis, medical clearance, emergency advice, or an interpretation of an external screening instrument.",
    }


def _legacy_safety_gate(profile: dict[str, Any]) -> dict[str, Any]:
    """Preserve prior internal prototype routing for saved demos and unit fixtures."""

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
        "route": {"GREEN": ROUTE_ELIGIBLE, "YELLOW": ROUTE_FOLLOW_UP, "RED": ROUTE_STOP}[status],
        "flags": flags,
        "reasons": reasons,
        "benchmark_allowed": status == "GREEN",
        "automated_handoff_allowed": status == "GREEN",
        "training_handoff_allowed": training_handoff,
        "deployment_status": "legacy_internal_only",
        "recommendation": recommendation,
        "disclaimer": "SportRx does not provide medical diagnosis, medical clearance, or emergency advice.",
    }


def evaluate_safety_gate(
    profile: dict[str, Any], *, providers: list[dict[str, Any]] | None = None, root: str = "."
) -> dict[str, Any]:
    """Return deterministic safety routing without changing performance values.

    Profiles with ``venue_screening`` use the new external-screening handoff.
    Other inputs remain internal legacy prototype paths and are never a venue
    deployment route.
    """

    if isinstance(profile.get("venue_screening"), dict):
        return _venue_safety_gate(profile, providers, root)
    return _legacy_safety_gate(profile)


def benchmark_allowed(safety_gate: dict[str, Any]) -> bool:
    """True only for an explicit eligible-for-benchmark route."""

    return bool(safety_gate.get("benchmark_allowed"))


def automated_handoff_allowed(safety_gate: dict[str, Any]) -> bool:
    """True only when safety routing permits automated output."""

    return bool(safety_gate.get("automated_handoff_allowed"))
