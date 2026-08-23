"""Input ledger for SportRx product transparency.

The ledger explains why each input exists. It does not score a user or create
new decision rules.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Input Ledger documents current SportRx input provenance and output roles. "
    "It does not validate rules, predict outcomes, or provide medical clearance."
)


INPUT_SPECS = [
    {
        "field_id": "age",
        "label": "Age",
        "unit": "years",
        "entry_type": "direct numeric",
        "source_type": "self_reported",
        "used_by": ["Safety Gate", "Prescription intensity"],
        "output_role": "Adult-scope check and heart-rate estimate where aerobic prescription uses HR guidance.",
    },
    {
        "field_id": "training_days",
        "label": "Recent training days",
        "unit": "days/week",
        "entry_type": "direct numeric",
        "source_type": "self_reported",
        "used_by": ["Quick Match", "HYROX Check", "Training Profile"],
        "output_role": "Describes recent training consistency and rough challenge fit.",
    },
    {
        "field_id": "weekly_training_minutes",
        "label": "Recent training volume",
        "unit": "minutes/week",
        "entry_type": "direct numeric",
        "source_type": "self_reported",
        "used_by": ["Quick Match", "HYROX Check", "Training Profile"],
        "output_role": "Describes current aerobic base; not treated as a measured performance test.",
    },
    {
        "field_id": "running_minutes_per_week",
        "label": "Running or brisk-walking volume",
        "unit": "minutes/week",
        "entry_type": "direct numeric",
        "source_type": "self_reported",
        "used_by": ["Quick Match", "HYROX Check"],
        "output_role": "Describes run exposure and rough hybrid-race preparation context.",
    },
    {
        "field_id": "longest_continuous_run_minutes",
        "label": "Longest continuous run/walk",
        "unit": "minutes",
        "entry_type": "direct numeric",
        "source_type": "self_reported",
        "used_by": ["Quick Match"],
        "output_role": "Describes recent continuous locomotion exposure.",
    },
    {
        "field_id": "strength_days_per_week",
        "label": "Strength training frequency",
        "unit": "days/week",
        "entry_type": "direct numeric",
        "source_type": "self_reported",
        "used_by": ["Quick Match", "HYROX Check", "Training Profile"],
        "output_role": "Describes strength-training context; not a measured strength test.",
    },
    {
        "field_id": "high_intensity_sessions_last_4w",
        "label": "High-intensity sessions",
        "unit": "sessions/4 weeks",
        "entry_type": "direct numeric",
        "source_type": "self_reported",
        "used_by": ["Quick Match"],
        "output_role": "Describes recent high-intensity exposure for rough fit only.",
    },
    {
        "field_id": "loaded_movement_sessions_last_4w",
        "label": "Loaded movement sessions",
        "unit": "sessions/4 weeks",
        "entry_type": "direct numeric",
        "source_type": "self_reported",
        "used_by": ["Quick Match"],
        "output_role": "Describes recent loaded-movement exposure for rough fit only.",
    },
    {
        "field_id": "available_days_per_week",
        "label": "Available training days",
        "unit": "days/week",
        "entry_type": "direct numeric",
        "source_type": "self_reported",
        "used_by": ["Training Block", "Prescription"],
        "output_role": "Constrains weekly frequency in generated training blocks.",
    },
    {
        "field_id": "max_minutes_per_session",
        "label": "Maximum session length",
        "unit": "minutes",
        "entry_type": "direct numeric",
        "source_type": "self_reported",
        "used_by": ["Training Block", "Prescription"],
        "output_role": "Constrains session duration in generated training blocks.",
    },
    {
        "field_id": "primary_goal",
        "label": "Primary goal",
        "unit": "category",
        "entry_type": "selection",
        "source_type": "self_reported",
        "used_by": ["Quick Match", "Training Profile"],
        "output_role": "Changes product language and route priority; it is not a performance measure.",
    },
    {
        "field_id": "equipment_access",
        "label": "Equipment access",
        "unit": "equipment list",
        "entry_type": "multi-select",
        "source_type": "self_reported",
        "used_by": ["Benchmark Protocol", "Lab Readiness"],
        "output_role": "Selects standard or low-equipment benchmark paths.",
    },
    {
        "field_id": "one_km_run_seconds",
        "label": "1 km run",
        "unit": "seconds",
        "entry_type": "measured test",
        "source_type": "measured",
        "used_by": ["HYROX Check", "Training Profile"],
        "output_role": "Can affect Running and measured strongest-area/gap comparison when enough measured areas exist.",
    },
    {
        "field_id": "five_km_run_seconds",
        "label": "5 km run",
        "unit": "seconds",
        "entry_type": "measured test",
        "source_type": "measured",
        "used_by": ["HYROX Check", "Training Profile"],
        "output_role": "Can affect Running and measured strongest-area/gap comparison when enough measured areas exist.",
    },
    {
        "field_id": "one_km_row_seconds",
        "label": "1 km RowErg",
        "unit": "seconds",
        "entry_type": "measured test",
        "source_type": "measured",
        "used_by": ["HYROX Check", "Training Profile"],
        "output_role": "Can affect Station experience when recorded.",
    },
    {
        "field_id": "one_km_ski_seconds",
        "label": "1 km SkiErg",
        "unit": "seconds",
        "entry_type": "measured test",
        "source_type": "measured",
        "used_by": ["HYROX Check", "Training Profile"],
        "output_role": "Can affect Station experience when recorded.",
    },
    {
        "field_id": "station_test_score",
        "label": "Station circuit",
        "unit": "score",
        "entry_type": "measured test",
        "source_type": "measured",
        "used_by": ["HYROX Check", "Training Profile"],
        "output_role": "Can affect Strength endurance and Station experience when recorded.",
    },
    {
        "field_id": "station_test_protocol",
        "label": "Station circuit protocol source",
        "unit": "protocol source",
        "entry_type": "protocol provenance",
        "source_type": "protocol_provenance",
        "used_by": ["HYROX Check", "Lab Test Quality"],
        "output_role": "Documents where the Station circuit score came from; affects review readiness, not measured performance.",
    },
    {
        "field_id": "work_capacity_test_score",
        "label": "Work-capacity test",
        "unit": "score",
        "entry_type": "measured test",
        "source_type": "measured",
        "used_by": ["HYROX Check", "Training Profile"],
        "output_role": "Can affect Work capacity when recorded.",
    },
    {
        "field_id": "work_capacity_test_protocol",
        "label": "Work-capacity protocol source",
        "unit": "protocol source",
        "entry_type": "protocol provenance",
        "source_type": "protocol_provenance",
        "used_by": ["HYROX Check", "Lab Test Quality"],
        "output_role": "Documents where the Work capacity score came from; affects review readiness, not measured performance.",
    },
    {
        "field_id": "symptoms",
        "label": "Exercise-related symptoms",
        "unit": "checklist",
        "entry_type": "safety checklist",
        "source_type": "safety_screen",
        "used_by": ["Safety Gate"],
        "output_role": "Can block automated training handoff; never changes measured performance.",
    },
    {
        "field_id": "known_conditions",
        "label": "Known health conditions",
        "unit": "checklist",
        "entry_type": "safety checklist",
        "source_type": "safety_screen",
        "used_by": ["Safety Gate"],
        "output_role": "Can caution or block automated training handoff; never changes measured performance.",
    },
    {
        "field_id": "recent_major_injury",
        "label": "Recent major injury",
        "unit": "yes/no",
        "entry_type": "safety checkbox",
        "source_type": "safety_screen",
        "used_by": ["Safety Gate"],
        "output_role": "Can caution automated handoff; never changes measured performance.",
    },
    {
        "field_id": "preferred_activity",
        "label": "Preferred activity",
        "unit": "category",
        "entry_type": "selection",
        "source_type": "self_reported",
        "used_by": ["Aerobic prescription"],
        "output_role": "Selects the default aerobic activity label when generating FITT-VP plans.",
    },
]


LEGACY_COMPATIBILITY_FIELDS = {
    "exercise_days_last_4w": "Legacy alias for training_days.",
    "mvpa_minutes_per_week": "Legacy alias for weekly_training_minutes.",
    "endurance_background": "Legacy subjective rating; current rules ignore it and use behavior fields instead.",
    "resistance_background": "Legacy subjective rating; current rules ignore it and use behavior fields instead.",
    "running_comfort": "Legacy subjective rating; current rules ignore it and use run/walk minutes instead.",
    "hiit_comfort": "Legacy subjective rating; current rules ignore it and use session counts instead.",
    "loaded_movement_comfort": "Legacy subjective rating; current rules ignore it and use session counts instead.",
}


IGNORED_FIELDS = {
    "vo2max": "No documented SportRx v2.2 rule uses VO2max.",
    "hrmax": "No documented SportRx v2.2 rule uses HRmax.",
    "resting_hr": "No documented SportRx v2.2 rule uses resting heart rate.",
}


def _has_value(value: Any) -> bool:
    if value is None or value == "":
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def _format_value(value: Any, unit: str) -> str:
    if not _has_value(value):
        return "Not provided"
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "Not provided"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    return f"{value} {unit}" if unit not in {"category", "checklist", "equipment list", "yes/no"} else str(value)


def build_input_ledger(profile: dict[str, Any]) -> dict[str, Any]:
    """Build a transparent list of active, missing, legacy, and ignored inputs."""

    rows = []
    for spec in INPUT_SPECS:
        value = profile.get(spec["field_id"])
        provided = _has_value(value)
        source_type = spec["source_type"]
        if source_type == "measured" and not provided:
            status = "not_tested"
            affects_output = False
        elif provided:
            status = "active"
            affects_output = True
        else:
            status = "not_provided"
            affects_output = False
        rows.append(
            {
                **spec,
                "status": status,
                "value": _format_value(value, spec["unit"]),
                "affects_output": affects_output,
                "used_by": spec["used_by"],
            }
        )

    for field_id, detail in LEGACY_COMPATIBILITY_FIELDS.items():
        if field_id in profile:
            rows.append(
                {
                    "field_id": field_id,
                    "label": field_id,
                    "unit": "legacy",
                    "entry_type": "legacy compatibility",
                    "source_type": "derived",
                    "used_by": ["Backward compatibility"],
                    "output_role": detail,
                    "status": "legacy",
                    "value": _format_value(profile.get(field_id), "legacy"),
                    "affects_output": False,
                }
            )

    for field_id, detail in IGNORED_FIELDS.items():
        if field_id in profile:
            rows.append(
                {
                    "field_id": field_id,
                    "label": field_id,
                    "unit": "ignored",
                    "entry_type": "unsupported",
                    "source_type": "ignored",
                    "used_by": [],
                    "output_role": detail,
                    "status": "ignored",
                    "value": _format_value(profile.get(field_id), "ignored"),
                    "affects_output": False,
                }
            )

    summary = {
        "total_rows": len(rows),
        "active_inputs": sum(1 for row in rows if row["status"] == "active"),
        "measured_tests_recorded": sum(1 for row in rows if row["source_type"] == "measured" and row["status"] == "active"),
        "not_tested": sum(1 for row in rows if row["status"] == "not_tested"),
        "safety_inputs": sum(1 for row in rows if row["source_type"] == "safety_screen"),
        "legacy_or_ignored": sum(1 for row in rows if row["status"] in {"legacy", "ignored"}),
    }
    return {
        "schema": "sportrx.input_ledger",
        "schema_version": "0.1",
        "summary": summary,
        "rows": rows,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def input_ledger_markdown(ledger: dict[str, Any]) -> str:
    """Export the input ledger as Markdown."""

    summary = ledger["summary"]
    lines = [
        "# SportRx Input Ledger",
        "",
        f"- Active inputs: {summary['active_inputs']}",
        f"- Measured tests recorded: {summary['measured_tests_recorded']}",
        f"- Not tested: {summary['not_tested']}",
        f"- Legacy or ignored fields: {summary['legacy_or_ignored']}",
        f"- Claim boundary: {ledger['claim_boundary']}",
        "",
        "## Inputs",
    ]
    for row in ledger["rows"]:
        used_by = ", ".join(row["used_by"]) if row["used_by"] else "Not used"
        lines.append(
            f"- `{row['field_id']}` - {row['label']} [{row['status']}]: "
            f"{row['value']}. Used by: {used_by}. Role: {row['output_role']}"
        )
    return "\n".join(lines) + "\n"
