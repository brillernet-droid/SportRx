"""60-second current profile matching for SportRx Labs."""

from __future__ import annotations

from typing import Any

from .safety_gate import automated_handoff_allowed, evaluate_safety_gate


PACKS = {
    "hybrid_race": {
        "name": "Hybrid Race",
        "status": "enabled",
        "cta": "Enter Hybrid Race Performance Lab",
        "targets": {
            "training_days": 3,
            "weekly_minutes": 150,
            "running_minutes": 75,
            "longest_continuous_run_minutes": 30,
            "strength_days": 2,
            "high_intensity_sessions_last_4w": 4,
            "loaded_movement_sessions_last_4w": 4,
        },
    },
    "running_5k_10k": {
        "name": "5K/10K Running",
        "status": "registry_ready",
        "cta": "Join the 5K/10K registry waitlist",
        "targets": {
            "training_days": 2,
            "weekly_minutes": 75,
            "running_minutes": 60,
            "longest_continuous_run_minutes": 20,
            "strength_days": 0,
            "high_intensity_sessions_last_4w": 0,
            "loaded_movement_sessions_last_4w": 0,
        },
    },
}


QUICK_MATCH_INPUTS = [
    {
        "field_id": "age",
        "label": "Age",
        "unit": "years",
        "affects": "Safety Gate / adult-scope check",
        "role": "Safety and scope only; it does not raise or lower Quick Match fit.",
    },
    {
        "field_id": "training_days",
        "label": "Recent training days",
        "unit": "days/week",
        "affects": "Quick Match",
        "role": "Estimates recent training consistency from behavior, not confidence or identity.",
    },
    {
        "field_id": "weekly_training_minutes",
        "label": "Recent training volume",
        "unit": "minutes/week",
        "affects": "Quick Match / Training Profile",
        "role": "Describes recent volume; it is not a measured performance test.",
    },
    {
        "field_id": "running_minutes_per_week",
        "label": "Running or brisk-walking volume",
        "unit": "minutes/week",
        "affects": "Quick Match / HYROX Check",
        "role": "Describes run exposure for hybrid-race context.",
    },
    {
        "field_id": "longest_continuous_run_minutes",
        "label": "Longest continuous run/walk",
        "unit": "minutes",
        "affects": "Quick Match",
        "role": "Describes recent continuous locomotion exposure.",
    },
    {
        "field_id": "strength_days_per_week",
        "label": "Strength training frequency",
        "unit": "days/week",
        "affects": "Quick Match / HYROX Check",
        "role": "Describes strength-training context; not a measured strength score.",
    },
    {
        "field_id": "high_intensity_sessions_last_4w",
        "label": "High-intensity sessions",
        "unit": "sessions/4 weeks",
        "affects": "Quick Match",
        "role": "Describes recent exposure to harder efforts.",
    },
    {
        "field_id": "loaded_movement_sessions_last_4w",
        "label": "Loaded movement sessions",
        "unit": "sessions/4 weeks",
        "affects": "Quick Match",
        "role": "Describes recent exposure to loaded carries, sled-like work, or similar station demands.",
    },
    {
        "field_id": "available_days_per_week",
        "label": "Available training days",
        "unit": "days/week",
        "affects": "Training Block / Prescription",
        "role": "Constrains future frequency; not used as a performance advantage.",
    },
    {
        "field_id": "max_minutes_per_session",
        "label": "Maximum session length",
        "unit": "minutes/session",
        "affects": "Training Block / Prescription",
        "role": "Constrains session duration in rule-based starter plans.",
    },
    {
        "field_id": "primary_goal",
        "label": "Primary goal",
        "unit": "category",
        "affects": "Routing / explanation language",
        "role": "Changes how SportRx frames next steps; it is not a performance metric.",
    },
]


BEHAVIOR_FIELDS = [
    "training_days",
    "weekly_training_minutes",
    "running_minutes_per_week",
    "longest_continuous_run_minutes",
    "strength_days_per_week",
    "high_intensity_sessions_last_4w",
    "loaded_movement_sessions_last_4w",
]


CONTEXT_FIELDS = ["age", "available_days_per_week", "max_minutes_per_session", "primary_goal"]


LEGACY_SUBJECTIVE_FIELDS = [
    "endurance_background",
    "resistance_background",
    "running_comfort",
    "hiit_comfort",
    "loaded_movement_comfort",
]


EXCLUDED_MEASURED_FIELDS = [
    "one_km_run_seconds",
    "five_km_run_seconds",
    "one_km_row_seconds",
    "one_km_ski_seconds",
    "station_test_score",
    "work_capacity_test_score",
]


def build_quick_match_intake_contract(
    profile: dict[str, Any],
    input_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Explain the visible Quick Match intake contract without changing rules."""

    input_review = input_review or build_quick_match_input_review(profile)
    field_specs = {item["field_id"]: item for item in QUICK_MATCH_INPUTS}

    groups = [
        _contract_group(
            "Safety / scope",
            "Kept separate from performance matching.",
            ["age"],
            profile,
            field_specs,
            expected_output="Can block or contextualize scope; never improves fit.",
        ),
        _contract_group(
            "Recent behavior",
            "Direct numbers from the last 4 weeks.",
            BEHAVIOR_FIELDS,
            profile,
            field_specs,
            expected_output="Used only for rough challenge routing before measured tests.",
        ),
        _contract_group(
            "Future constraints",
            "Availability limits for a later training handoff.",
            ["available_days_per_week", "max_minutes_per_session", "primary_goal"],
            profile,
            field_specs,
            expected_output="Constrains or frames training; not a performance advantage.",
        ),
    ]

    legacy_present = [
        field_id for field_id in LEGACY_SUBJECTIVE_FIELDS if profile.get(field_id) is not None
    ]
    measured_present = [
        field_id for field_id in EXCLUDED_MEASURED_FIELDS if profile.get(field_id) is not None
    ]
    missing_required = [
        field_id
        for field_id in BEHAVIOR_FIELDS + ["age", "available_days_per_week", "max_minutes_per_session"]
        if profile.get(field_id) is None
    ]

    status = "contract_ready"
    next_action = "Use Quick Match as a quantified self-report screen, then move to Benchmark for measured performance."
    if missing_required:
        status = "needs_numeric_intake"
        next_action = "Fill the missing direct-number fields before interpreting Quick Match."
    elif legacy_present:
        status = "legacy_subjective_values_present"
        next_action = "Remove legacy comfort/background values; current Quick Match should rely on countable behavior."

    return {
        "schema": "sportrx.quick_match_intake_contract",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "groups": groups,
        "group_count": len(groups),
        "required_numeric_fields": len(BEHAVIOR_FIELDS) + 3,
        "missing_required_fields": missing_required,
        "legacy_subjective_fields_present": legacy_present,
        "excluded_measured_fields_present": measured_present,
        "excluded_measurement_policy": (
            "Measured tests such as 1 km run, 5 km run, RowErg, SkiErg, station "
            "circuit, and work-capacity scores belong in HYROX Check / Benchmark "
            "Log. Quick Match does not use them."
        ),
        "primary_message": (
            "Quick Match asks for countable recent behavior, not background identity, "
            "adaptability, confidence, or self-rated fitness."
        ),
        "input_review_status": input_review.get("quality_status", "unknown"),
        "claim_boundary": (
            "Quick Match Intake Contract documents why fields are collected. It "
            "does not validate SportRx, score measured performance, predict race "
            "results, or provide medical clearance."
        ),
    }


def quick_match_intake_contract_markdown(contract: dict[str, Any]) -> str:
    """Export the Quick Match intake contract as Markdown."""

    lines = [
        "# SportRx Quick Match Intake Contract",
        "",
        f"- Status: {contract['status']}",
        f"- Required numeric fields: {contract['required_numeric_fields']}",
        f"- Input review status: {contract['input_review_status']}",
        f"- Claim boundary: {contract['claim_boundary']}",
        "",
        contract["primary_message"],
        "",
        "## Field groups",
    ]
    for group in contract["groups"]:
        lines.extend(
            [
                "",
                f"### {group['label']}",
                f"- Purpose: {group['purpose']}",
                f"- Collected: {group['collected']} / {group['total']}",
                f"- Output role: {group['expected_output']}",
            ]
        )
        for field in group["fields"]:
            lines.append(
                f"- `{field['field_id']}` - {field['label']}: {field['value']} "
                f"({field['unit']}); {field['role']}"
            )
    lines.extend(
        [
            "",
            "## Excluded from Quick Match",
            f"- Measurement policy: {contract['excluded_measurement_policy']}",
        ]
    )
    if contract["legacy_subjective_fields_present"]:
        lines.append(f"- Legacy subjective fields present: {', '.join(contract['legacy_subjective_fields_present'])}")
    if contract["excluded_measured_fields_present"]:
        lines.append(f"- Measured fields present but ignored here: {', '.join(contract['excluded_measured_fields_present'])}")
    if contract["missing_required_fields"]:
        lines.append(f"- Missing required fields: {', '.join(contract['missing_required_fields'])}")
    return "\n".join(lines) + "\n"


def _contract_group(
    label: str,
    purpose: str,
    field_ids: list[str],
    profile: dict[str, Any],
    field_specs: dict[str, dict[str, Any]],
    expected_output: str,
) -> dict[str, Any]:
    fields = []
    for field_id in field_ids:
        spec = field_specs[field_id]
        provided = field_id in profile and profile.get(field_id) is not None
        fields.append(
            {
                "field_id": field_id,
                "label": spec["label"],
                "unit": spec["unit"],
                "value": profile.get(field_id, "Not collected"),
                "status": "collected" if provided else "not_collected",
                "role": spec["role"],
            }
        )
    collected = sum(1 for field in fields if field["status"] == "collected")
    return {
        "label": label,
        "purpose": purpose,
        "expected_output": expected_output,
        "collected": collected,
        "total": len(fields),
        "status": "ready" if collected == len(fields) else "waiting",
        "fields": fields,
    }


def build_quick_match_input_review(profile: dict[str, Any]) -> dict[str, Any]:
    """Explain which Quick Match inputs are used and what they can affect."""

    fields = []
    missing = []
    for spec in QUICK_MATCH_INPUTS:
        field_id = spec["field_id"]
        provided = field_id in profile and profile.get(field_id) is not None
        if not provided:
            missing.append(field_id)
        fields.append(
            {
                **spec,
                "value": profile.get(field_id, "Not collected"),
                "status": "collected" if provided else "not_collected",
            }
        )

    behavior_collected = sum(1 for field_id in BEHAVIOR_FIELDS if field_id in profile and profile.get(field_id) is not None)
    context_collected = sum(1 for field_id in CONTEXT_FIELDS if field_id in profile and profile.get(field_id) is not None)
    quality_status = "usable_behavior_snapshot" if behavior_collected == len(BEHAVIOR_FIELDS) else "needs_more_behavior_context"
    return {
        "schema": "sportrx.quick_match_input_review",
        "schema_version": "0.1",
        "quality_status": quality_status,
        "behavior_fields_collected": behavior_collected,
        "behavior_fields_total": len(BEHAVIOR_FIELDS),
        "context_fields_collected": context_collected,
        "context_fields_total": len(CONTEXT_FIELDS),
        "missing_fields": missing,
        "fields": fields,
        "claim_boundary": (
            "Quick Match uses recent self-reported behavior for rough product routing. "
            "It is not a measured performance test, readiness score, medical clearance, "
            "race prediction, or injury-risk estimate."
        ),
    }


def build_quick_match_intake_quality(
    profile: dict[str, Any],
    input_review: dict[str, Any] | None = None,
    safety_gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Summarize whether Quick Match input is usable and where to route next."""

    input_review = input_review or build_quick_match_input_review(profile)
    safety_gate = safety_gate or evaluate_safety_gate(profile)
    missing_behavior = [
        field_id
        for field_id in BEHAVIOR_FIELDS
        if field_id not in profile or profile.get(field_id) is None
    ]
    nonzero_behavior = [
        field_id
        for field_id in BEHAVIOR_FIELDS
        if field_id in profile and _numeric_value(profile.get(field_id)) > 0
    ]
    legacy_ignored = [
        field_id
        for field_id in LEGACY_SUBJECTIVE_FIELDS
        if field_id in profile and profile.get(field_id) is not None
    ]
    constraints_ready = all(
        field_id in profile and profile.get(field_id) is not None
        for field_id in ["available_days_per_week", "max_minutes_per_session"]
    )

    if not automated_handoff_allowed(safety_gate):
        status = "blocked_by_safety_gate"
        next_action = "Resolve Safety Gate before Quick Match routing or training handoff."
    elif missing_behavior:
        status = "needs_more_behavior_context"
        next_action = "Complete the missing recent-behavior fields before using Quick Match."
    elif len(nonzero_behavior) < 3:
        status = "low_behavior_signal"
        next_action = "Use Quick Match only as a sparse intake record and route to SportRx Hybrid Benchmark v1."
    else:
        status = "ready_for_quick_match_routing"
        next_action = "Use this intake for rough routing, then continue to HYROX Check or Benchmark Protocol for measured data."

    cards = [
        _intake_card(
            "Safety Gate",
            safety_gate.get("status", "not_reviewed"),
            "Safety can block routing, but never changes performance scores.",
            "blocked" if not automated_handoff_allowed(safety_gate) else "ready",
        ),
        _intake_card(
            "Behavior Snapshot",
            f"{input_review['behavior_fields_collected']} / {input_review['behavior_fields_total']}",
            "Recent days, minutes, run/walk exposure, strength, high-intensity, and loaded movement fields.",
            "ready" if not missing_behavior else "waiting",
        ),
        _intake_card(
            "Active Signals",
            f"{len(nonzero_behavior)} / {len(BEHAVIOR_FIELDS)}",
            "Zero is valid, but many zeros mean Quick Match is low-signal and should route to Benchmark first.",
            "ready" if len(nonzero_behavior) >= 3 else "waiting",
        ),
        _intake_card(
            "Time Constraints",
            "Ready" if constraints_ready else "Missing",
            "Future days and session length constrain training blocks; they are not performance advantages.",
            "ready" if constraints_ready else "waiting",
        ),
        _intake_card(
            "Legacy Ignored",
            len(legacy_ignored),
            "Subjective background / comfort fields are preserved only as ignored legacy compatibility data.",
            "ready" if not legacy_ignored else "waiting",
        ),
        _intake_card(
            "Measurement Route",
            "Benchmark required",
            "Quick Match never replaces HYROX Check or SportRx Hybrid Benchmark v1 measured results.",
            "waiting",
        ),
    ]
    return {
        "schema": "sportrx.quick_match_intake_quality",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "missing_behavior_fields": missing_behavior,
        "nonzero_behavior_fields": nonzero_behavior,
        "legacy_ignored_fields": legacy_ignored,
        "constraints_ready": constraints_ready,
        "cards": cards,
        "claim_boundary": (
            "Intake Quality checks whether the self-reported Quick Match record is usable for rough routing. "
            "It is not a measured performance profile, validation result, readiness score, or medical clearance."
        ),
    }


def build_quick_match_lab_intake_sheet(
    profile: dict[str, Any],
    intake_quality: dict[str, Any] | None = None,
    intake_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a lab-style intake sheet for direct-number Quick Match fields."""

    intake_contract = intake_contract or build_quick_match_intake_contract(profile)
    intake_quality = intake_quality or build_quick_match_intake_quality(profile)
    field_specs = {item["field_id"]: item for item in QUICK_MATCH_INPUTS}
    sections = [
        _lab_intake_section(
            "Participant scope",
            "Who is entering the prototype; not a performance score.",
            ["age", "primary_goal"],
            profile,
            field_specs,
            "Safety / routing context",
        ),
        _lab_intake_section(
            "Past 4 weeks",
            "Countable recent behavior. These numbers can be zero.",
            BEHAVIOR_FIELDS,
            profile,
            field_specs,
            "Quick Match routing only",
        ),
        _lab_intake_section(
            "Next 4 weeks",
            "Training availability constraints for later prescription handoff.",
            ["available_days_per_week", "max_minutes_per_session"],
            profile,
            field_specs,
            "Training constraint",
        ),
    ]
    collected = sum(section["collected"] for section in sections)
    total = sum(section["total"] for section in sections)
    measured_fields_present = [
        field_id for field_id in EXCLUDED_MEASURED_FIELDS if profile.get(field_id) is not None
    ]
    if intake_quality["status"] == "blocked_by_safety_gate":
        status = "safety_gate_first"
        next_action = "Resolve Safety Gate before using Quick Match or Benchmark handoff."
    elif intake_quality["status"] == "low_behavior_signal":
        status = "benchmark_first"
        next_action = "Treat this as a sparse intake sheet and route to SportRx Hybrid Benchmark v1."
    elif intake_contract["status"] == "needs_numeric_intake":
        status = "needs_direct_numbers"
        next_action = "Complete the direct-number intake fields before interpreting Quick Match."
    else:
        status = "ready_for_self_report_routing"
        next_action = "Use this self-reported intake for rough routing, then test in Benchmark."

    cards = [
        _intake_card(
            "Direct-number intake",
            f"{collected} / {total}",
            "Age, recent behavior, and time constraints are entered as numbers instead of vague background labels.",
            "ready" if collected == total else "waiting",
        ),
        _intake_card(
            "Measured performance",
            "0 used",
            "1 km, 5 km, RowErg, SkiErg, station, and work-capacity tests are excluded from Quick Match.",
            "waiting",
        ),
        _intake_card(
            "Missing-data rule",
            "No imputation",
            "Missing or untested performance data stays Not tested; SportRx does not fill midpoint or average values.",
            "ready",
        ),
        _intake_card(
            "Next step",
            zh_status(status),
            next_action,
            "ready" if status == "ready_for_self_report_routing" else "waiting",
        ),
    ]
    return {
        "schema": "sportrx.quick_match_lab_intake_sheet",
        "schema_version": "0.1",
        "status": status,
        "collected_fields": collected,
        "total_fields": total,
        "sections": sections,
        "cards": cards,
        "measured_fields_present_but_ignored": measured_fields_present,
        "not_tested_policy": "Performance tests not entered here remain Not tested and do not receive average or midpoint values.",
        "primary_message": (
            "Quick Match is a direct-number self-report intake sheet. It records "
            "what the user says they did recently; it does not measure performance."
        ),
        "next_action": next_action,
        "claim_boundary": (
            "Lab Intake Sheet improves transparency of the entry flow. It is not "
            "a validated assessment, readiness score, medical clearance, race "
            "prediction, or injury-risk estimate."
        ),
    }


def quick_match_lab_intake_sheet_markdown(sheet: dict[str, Any]) -> str:
    """Export the Quick Match lab intake sheet as Markdown."""

    lines = [
        "# SportRx Quick Match Lab Intake Sheet",
        "",
        f"- Status: {sheet['status']}",
        f"- Collected fields: {sheet['collected_fields']} / {sheet['total_fields']}",
        f"- Next action: {sheet['next_action']}",
        f"- Claim boundary: {sheet['claim_boundary']}",
        "",
        sheet["primary_message"],
        "",
        "## Not-tested policy",
        "",
        sheet["not_tested_policy"],
        "",
        "## Sections",
    ]
    for section in sheet["sections"]:
        lines.extend(
            [
                "",
                f"### {section['label']}",
                f"- Purpose: {section['purpose']}",
                f"- Output role: {section['output_role']}",
                f"- Collected: {section['collected']} / {section['total']}",
            ]
        )
        for field in section["fields"]:
            lines.append(
                f"- `{field['field_id']}`: {field['value']} {field['unit']} "
                f"({field['source_type']}; {field['status']})"
            )
    if sheet["measured_fields_present_but_ignored"]:
        lines.extend(
            [
                "",
                "## Measured fields ignored here",
                "",
                ", ".join(sheet["measured_fields_present_but_ignored"]),
            ]
        )
    return "\n".join(lines) + "\n"


def _lab_intake_section(
    label: str,
    purpose: str,
    field_ids: list[str],
    profile: dict[str, Any],
    field_specs: dict[str, dict[str, Any]],
    output_role: str,
) -> dict[str, Any]:
    fields = []
    for field_id in field_ids:
        spec = field_specs[field_id]
        provided = field_id in profile and profile.get(field_id) is not None
        fields.append(
            {
                "field_id": field_id,
                "label": spec["label"],
                "unit": spec["unit"],
                "value": profile.get(field_id, "Not collected"),
                "status": "collected" if provided else "not_collected",
                "source_type": "self_report_direct_number"
                if spec["unit"] != "category"
                else "self_report_category",
                "output_role": output_role,
                "boundary": spec["role"],
            }
        )
    collected = sum(1 for field in fields if field["status"] == "collected")
    return {
        "label": label,
        "purpose": purpose,
        "output_role": output_role,
        "collected": collected,
        "total": len(fields),
        "status": "ready" if collected == len(fields) else "waiting",
        "fields": fields,
    }


def zh_status(status: str) -> str:
    labels = {
        "ready_for_self_report_routing": "Self-report routing ready",
        "benchmark_first": "Benchmark first",
        "needs_direct_numbers": "Needs direct numbers",
        "safety_gate_first": "Safety Gate first",
    }
    return labels.get(status, status)


def _ratio(value: float, target: float) -> float:
    if target <= 0:
        return 1.0
    return max(0.0, min(value / target, 1.0))


def _numeric_value(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _intake_card(label: str, value: object, detail: str, status: str) -> dict[str, Any]:
    return {
        "label": label,
        "value": value,
        "detail": detail,
        "status": status,
    }


def _component(
    profile: dict[str, Any],
    key: str,
    target: float,
) -> float:
    if key in profile and profile.get(key) is not None:
        return _ratio(float(profile.get(key) or 0), target)
    return 0.0


def _score_pack(profile: dict[str, Any], targets: dict[str, int]) -> tuple[int, dict[str, float]]:
    weekly_minutes = float(profile.get("weekly_training_minutes", profile.get("mvpa_minutes_per_week", 0)) or 0)
    components = {
        "training_consistency": _ratio(float(profile.get("training_days", 0) or 0), targets["training_days"]),
        "training_volume": _ratio(weekly_minutes, targets["weekly_minutes"]),
        "running_volume": _component(
            profile,
            "running_minutes_per_week",
            targets["running_minutes"],
        ),
        "longest_continuous_run": _component(
            profile,
            "longest_continuous_run_minutes",
            targets["longest_continuous_run_minutes"],
        ),
        "strength_frequency": _component(
            profile,
            "strength_days_per_week",
            targets["strength_days"],
        ),
        "high_intensity_exposure": _component(
            profile,
            "high_intensity_sessions_last_4w",
            targets["high_intensity_sessions_last_4w"],
        ),
        "loaded_movement_exposure": _component(
            profile,
            "loaded_movement_sessions_last_4w",
            targets["loaded_movement_sessions_last_4w"],
        ),
    }
    score = round(
        (
            components["training_consistency"] * 0.16
            + components["training_volume"] * 0.18
            + components["running_volume"] * 0.16
            + components["longest_continuous_run"] * 0.14
            + components["strength_frequency"] * 0.16
            + components["high_intensity_exposure"] * 0.10
            + components["loaded_movement_exposure"] * 0.10
        )
        * 100
    )
    return int(score), components


def _join_labels(labels: list[str]) -> str:
    if not labels:
        return "Not enough information"
    if len(labels) == 1:
        return labels[0]
    return " and ".join(labels)


def _capability_and_limiter(components: dict[str, float]) -> tuple[str, str]:
    labels = {
        "training_consistency": "training consistency",
        "training_volume": "weekly training volume",
        "running_volume": "running volume",
        "longest_continuous_run": "longest continuous run",
        "strength_frequency": "strength frequency",
        "high_intensity_exposure": "high-intensity exposure",
        "loaded_movement_exposure": "loaded movement exposure",
    }
    if not components:
        return "Not enough information", "Not enough information"

    max_value = max(components.values())
    min_value = min(components.values())
    if max_value - min_value <= 0.03:
        return "Balanced from quick check", "No single main gap from quick check"

    strongest = [key for key, value in components.items() if abs(value - max_value) <= 0.03]
    limiter = [key for key, value in components.items() if abs(value - min_value) <= 0.03]
    return _join_labels([labels[key] for key in strongest]), _join_labels([labels[key] for key in limiter])


def _fit_category(score: int) -> str:
    if score >= 82:
        return "Strong current fit"
    if score >= 66:
        return "Good current fit"
    if score >= 48:
        return "Some preparation needed"
    return "More preparation needed"


def _evidence_for_pack(
    pack_id: str,
    components: dict[str, float],
    profile: dict[str, Any],
    targets: dict[str, int],
) -> tuple[list[str], list[str]]:
    reasons: list[str] = []
    missing: list[str] = []
    training_days = int(profile.get("training_days", 0) or 0)
    weekly_minutes = int(profile.get("weekly_training_minutes", profile.get("mvpa_minutes_per_week", 0)) or 0)
    running_minutes = int(profile.get("running_minutes_per_week", 0) or 0)
    longest_run = int(profile.get("longest_continuous_run_minutes", 0) or 0)
    strength_days = int(profile.get("strength_days_per_week", 0) or 0)
    hiit_sessions = int(profile.get("high_intensity_sessions_last_4w", 0) or 0)
    loaded_sessions = int(profile.get("loaded_movement_sessions_last_4w", 0) or 0)

    if components["training_consistency"] >= 0.8:
        reasons.append(f"{training_days} training days/week reported")
    else:
        missing.append(f"Training days below {targets['training_days']}/week")
    if components["training_volume"] >= 0.8:
        reasons.append(f"{weekly_minutes} total training min/week reported")
    else:
        missing.append(f"Weekly volume below about {targets['weekly_minutes']} min/week")
    if components["running_volume"] >= 0.7:
        reasons.append(f"{running_minutes} running/walking min/week reported")
    else:
        missing.append("More weekly running/walking volume")
    if components["longest_continuous_run"] >= 0.7:
        reasons.append(f"{longest_run} min longest continuous run/walk reported")
    else:
        missing.append("Longer continuous run/walk exposure")
    if pack_id == "hybrid_race":
        if components["strength_frequency"] >= 0.7:
            reasons.append(f"{strength_days} strength days/week reported")
        else:
            missing.append("More weekly strength training exposure")
        if components["high_intensity_exposure"] < 0.7:
            missing.append("More recent high-intensity exposure")
        if components["loaded_movement_exposure"] < 0.7:
            missing.append("More recent loaded movement exposure")
        if hiit_sessions or loaded_sessions:
            reasons.append(f"{hiit_sessions} high-intensity and {loaded_sessions} loaded sessions in last 4 weeks")
    if pack_id == "running_5k_10k":
        if components["running_volume"] >= 0.7 or components["longest_continuous_run"] >= 0.7:
            reasons.append("Recent running/walking exposure is close to this challenge")
        else:
            missing.append("More running-specific practice")
    return reasons[:4], missing[:4]


def _athlete_label(profile: dict[str, Any], strongest: str, limiter: str) -> str:
    goal = str(profile.get("primary_goal", "") or "").lower()
    if "first" in goal:
        return "first-challenge builder"
    if "performance" in goal or "improve" in goal:
        return "performance-oriented recreational athlete"
    if "strength" in strongest and "endurance" in limiter:
        return "strength-leaning hybrid starter"
    if "endurance" in strongest and "strength" in limiter:
        return "endurance-leaning hybrid starter"
    return "general hybrid starter"


def quick_match(profile: dict[str, Any]) -> dict[str, Any]:
    """Return low-friction current profile challenge matches."""

    safety_gate = evaluate_safety_gate(profile)
    matches = []
    combined_components: dict[str, float] | None = None

    for pack_id, pack in PACKS.items():
        score, components = _score_pack(profile, pack["targets"])
        if pack_id == "hybrid_race":
            combined_components = components
        strongest, limiter = _capability_and_limiter(components)
        reasons, missing = _evidence_for_pack(pack_id, components, profile, pack["targets"])
        matches.append(
            {
                "pack_id": pack_id,
                "event_profile": pack["name"],
                "pack_status": pack["status"],
                "current_profile_match": score,
                "fit_category": _fit_category(score),
                "strongest_capability": strongest,
                "obvious_limiter": limiter,
                "why_it_fits": reasons,
                "what_is_missing": missing,
                "cta": pack["cta"],
            }
        )

    combined_components = combined_components or {}
    strongest, limiter = _capability_and_limiter(combined_components)
    input_review = build_quick_match_input_review(profile)
    intake_contract = build_quick_match_intake_contract(profile, input_review)
    intake_quality = build_quick_match_intake_quality(profile, input_review, safety_gate)
    lab_intake_sheet = build_quick_match_lab_intake_sheet(profile, intake_quality, intake_contract)
    return {
        "product": "SportRx Labs",
        "mode": "quick_match",
        "safety_gate": safety_gate,
        "athlete_profile_label": _athlete_label(profile, strongest, limiter),
        "strongest_capability": strongest,
        "obvious_limiter": limiter,
        "top_matches": sorted(matches, key=lambda item: item["current_profile_match"], reverse=True),
        "input_review": input_review,
        "intake_contract": intake_contract,
        "intake_quality": intake_quality,
        "lab_intake_sheet": lab_intake_sheet,
        "next_action": "Enter Hybrid Race Performance Lab",
        "language_guardrail": "This is a current profile match, not innate ability or genetic suitability.",
    }
