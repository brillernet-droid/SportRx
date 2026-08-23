"""Metric source register for SportRx outputs.

This module makes input provenance explicit. It does not create new scores; it
only documents what each visible output can know from the current profile.
"""

from __future__ import annotations

from typing import Any


SOURCE_LABELS = {
    "measured": "Measured",
    "self_reported": "Self-reported",
    "estimated": "Estimated",
    "derived": "Derived from SportRx rules",
    "not_tested": "Not tested",
    "safety_screen": "Safety screen",
    "protocol_provenance": "Protocol provenance",
    "unsupported": "Not used",
}


UNSUPPORTED_INPUTS = {
    "vo2max": "No documented SportRx v2.2 rule uses VO2max.",
    "hrmax": "No documented SportRx v2.2 rule uses HRmax.",
    "resting_hr": "No documented SportRx v2.2 rule uses resting heart rate.",
}


def _has_value(profile: dict[str, Any], key: str) -> bool:
    value = profile.get(key)
    if value is None:
        return False
    if value == "":
        return False
    if isinstance(value, (list, tuple, set, dict)) and not value:
        return False
    return True


def _source_type(raw_source: str) -> str:
    if raw_source == "measured":
        return "measured"
    if raw_source == "missing":
        return "not_tested"
    if raw_source == "reported_training":
        return "self_reported"
    return raw_source or "not_tested"


def _metric(
    metric_id: str,
    label: str,
    source_type: str,
    inputs: list[str],
    affects_output: bool,
    output_role: str,
    value: Any = None,
    detail: str | None = None,
) -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "label": label,
        "source_type": source_type,
        "source_label": SOURCE_LABELS.get(source_type, source_type),
        "inputs": inputs,
        "value": value,
        "affects_output": bool(affects_output),
        "output_role": output_role,
        "detail": detail or "",
    }


def build_metric_source_register(
    profile: dict[str, Any],
    performance_profile: dict[str, dict[str, Any]],
    training_context: dict[str, Any],
    safety_gate: dict[str, Any],
) -> dict[str, Any]:
    """Build a user-facing register of metric sources and output roles."""

    performance_inputs = {
        "running_capacity": ["one_km_run_seconds", "five_km_run_seconds"],
        "aerobic_base": ["weekly_training_minutes", "training_days", "running_minutes_per_week"],
        "strength_endurance": ["station_test_score"],
        "station_experience": ["one_km_row_seconds", "one_km_ski_seconds", "station_test_score"],
        "work_capacity": ["work_capacity_test_score", "compromised_run_score"],
    }

    performance_metrics = []
    for metric_id, item in performance_profile.items():
        source_type = _source_type(str(item.get("source", "")))
        measured = source_type == "measured"
        self_reported = source_type == "self_reported"
        if measured:
            output_role = "Can affect strongest area, main gap, and Starter Path handoff when at least two measured performance areas exist."
        elif self_reported:
            output_role = "Describes training context and current measured picture; not used to compare strongest area versus main gap."
        else:
            output_role = "Does not affect scoring or gap comparison until tested."
        performance_metrics.append(
            _metric(
                metric_id,
                item["label"],
                source_type,
                performance_inputs.get(metric_id, []),
                measured or self_reported,
                output_role,
                value="Not tested" if item.get("score") is None else item.get("score"),
                detail="; ".join(item.get("evidence") or item.get("missing") or []),
            )
        )

    context_specs = [
        (
            "days_available_per_week",
            "Available training days",
            ["available_days_per_week"],
            training_context.get("days_available_per_week"),
            "Constrains frequency in generated training blocks.",
        ),
        (
            "minutes_available_per_session",
            "Available session length",
            ["max_minutes_per_session"],
            training_context.get("minutes_available_per_session"),
            "Constrains duration in generated training blocks.",
        ),
        (
            "equipment_access",
            "Equipment access",
            ["equipment_access"],
            training_context.get("equipment_access"),
            "Selects standard or low-equipment benchmark paths and exercise options.",
        ),
        (
            "recent_training_consistency",
            "Recent training consistency",
            ["training_days", "exercise_days_last_4w"],
            training_context.get("recent_training_consistency"),
            "Describes current training context.",
        ),
        (
            "weekly_training_volume",
            "Weekly training volume",
            ["weekly_training_minutes", "mvpa_minutes_per_week"],
            training_context.get("weekly_training_volume"),
            "Describes current training context and aerobic-base estimate.",
        ),
        (
            "resistance_training_history",
            "Resistance training frequency",
            ["strength_days_per_week"],
            training_context.get("resistance_training_history"),
            "Describes current training context.",
        ),
    ]
    context_metrics = [
        _metric(
            metric_id,
            label,
            "self_reported" if value not in (None, [], "") else "not_tested",
            inputs,
            value not in (None, [], ""),
            output_role if value not in (None, [], "") else "Does not affect output until provided.",
            value=value,
        )
        for metric_id, label, inputs, value, output_role in context_specs
    ]

    protocol_specs = [
        (
            "station_test_protocol",
            "Station circuit protocol source",
            ["station_test_protocol"],
            profile.get("station_test_protocol"),
            "Documents where the Station circuit score came from; affects Lab Test Quality review readiness, not measured performance.",
        ),
        (
            "work_capacity_test_protocol",
            "Work-capacity protocol source",
            ["work_capacity_test_protocol"],
            profile.get("work_capacity_test_protocol"),
            "Documents where the Work capacity score came from; affects Lab Test Quality review readiness, not measured performance.",
        ),
    ]
    protocol_metrics = [
        _metric(
            metric_id,
            label,
            "protocol_provenance" if value not in (None, [], "") else "not_tested",
            inputs,
            value not in (None, [], ""),
            output_role if value not in (None, [], "") else "Does not affect Lab Test Quality until provided.",
            value=value,
        )
        for metric_id, label, inputs, value, output_role in protocol_specs
    ]

    safety_metrics = [
        _metric(
            "symptoms",
            "Exercise-related symptoms",
            "safety_screen" if _has_value(profile, "symptoms") else "not_tested",
            ["symptoms"],
            True,
            "Can block automated training handoff; never raises or lowers measured performance.",
            value=profile.get("symptoms", []),
            detail=f"Safety Gate status: {safety_gate.get('status')}",
        ),
        _metric(
            "known_conditions",
            "Known health conditions",
            "safety_screen" if _has_value(profile, "known_conditions") else "not_tested",
            ["known_conditions"],
            True,
            "Can block or caution automated training handoff; never raises or lowers measured performance.",
            value=profile.get("known_conditions", []),
            detail=f"Safety Gate status: {safety_gate.get('status')}",
        ),
        _metric(
            "recent_major_injury",
            "Recent major injury",
            "safety_screen" if _has_value(profile, "recent_major_injury") else "not_tested",
            ["recent_major_injury"],
            True,
            "Can caution automated handoff; never changes measured performance.",
            value=profile.get("recent_major_injury"),
            detail=f"Safety Gate status: {safety_gate.get('status')}",
        ),
    ]

    unsupported_inputs = [
        _metric(
            key,
            key,
            "unsupported",
            [key],
            False,
            "Ignored because no documented SportRx rule currently uses this input.",
            value=profile.get(key),
            detail=reason,
        )
        for key, reason in UNSUPPORTED_INPUTS.items()
        if key in profile
    ]

    all_metrics = performance_metrics + context_metrics + protocol_metrics + safety_metrics + unsupported_inputs
    measured_count = sum(1 for item in performance_metrics if item["source_type"] == "measured")
    not_tested_count = sum(1 for item in all_metrics if item["source_type"] == "not_tested")
    return {
        "schema": "sportrx.metric_source_register",
        "schema_version": "0.1",
        "summary": {
            "total_metrics": len(all_metrics),
            "measured_performance_metrics": measured_count,
            "not_tested_metrics": not_tested_count,
            "unsupported_inputs": len(unsupported_inputs),
            "protocol_provenance_metrics": sum(1 for item in protocol_metrics if item["source_type"] == "protocol_provenance"),
        },
        "performance_metrics": performance_metrics,
        "context_metrics": context_metrics,
        "protocol_metrics": protocol_metrics,
        "safety_metrics": safety_metrics,
        "unsupported_inputs": unsupported_inputs,
        "all_metrics": all_metrics,
        "claim_boundary": (
            "Metric source labels document provenance only. They do not validate "
            "SportRx, estimate risk, or create athlete norms."
        ),
    }
