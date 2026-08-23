"""Alpha data-capture templates for SportRx pilot testing.

The templates define what to collect during early alpha use. They intentionally
ship with headers only: no sample athletes, no fake norms, and no derived
claims.
"""

from __future__ import annotations

import csv
from io import StringIO
from typing import Any


CLAIM_BOUNDARY = (
    "Alpha Dataset Template structures local pilot data capture only. It does "
    "not validate SportRx, create athlete norms, estimate injury risk, predict "
    "performance, or provide medical clearance."
)


MINIMUM_RULES = [
    "Use anonymous participant_id values; do not store names in the template.",
    "Leave missing tests blank and record not_tested_reason; do not impute averages.",
    "Keep Safety Gate status separate from benchmark results and training feedback.",
    "Preserve raw units exactly as measured before creating any derived fields.",
    "Do not create percentiles, norms, validation claims, or prediction labels from alpha data.",
]


TABLES = [
    {
        "id": "participants",
        "filename": "sportrx_alpha_participants_template.csv",
        "purpose": "One row per alpha participant and baseline/retest window.",
        "fields": [
            "participant_id",
            "consent_to_contact",
            "age",
            "sex",
            "safety_gate_status",
            "equipment_access",
            "baseline_date",
            "retest_date",
            "notes",
        ],
    },
    {
        "id": "benchmark_sessions",
        "filename": "sportrx_alpha_benchmark_sessions_template.csv",
        "purpose": "One row per measured or explicitly not-tested benchmark component.",
        "fields": [
            "participant_id",
            "session_id",
            "session_type",
            "test_date",
            "protocol_version",
            "component_id",
            "component_label",
            "value",
            "unit",
            "rpe",
            "equipment_used",
            "substitution",
            "protocol_deviation_notes",
            "not_tested_reason",
        ],
    },
    {
        "id": "weekly_feedback",
        "filename": "sportrx_alpha_weekly_feedback_template.csv",
        "purpose": "One row per participant training week after a Starter Path is used.",
        "fields": [
            "participant_id",
            "week",
            "planned_sessions",
            "completed_sessions",
            "completion_rate",
            "average_rpe",
            "felt_too_hard",
            "pain_or_symptom_note",
            "missed_session_reason",
            "plan_actual_action",
        ],
    },
    {
        "id": "pilot_review",
        "filename": "sportrx_alpha_pilot_review_template.csv",
        "purpose": "One row per participant or reviewer product-feedback submission.",
        "fields": [
            "participant_id",
            "review_date",
            "reviewer_role",
            "setup_clarity",
            "measurement_realism",
            "trust",
            "actionability",
            "visual_polish",
            "first_impression",
            "measurement_confusion",
            "trust_boundary",
            "next_improvement",
            "contact_consent",
        ],
    },
]


def build_alpha_dataset_template() -> dict[str, Any]:
    """Build the alpha data-capture schema package."""

    return {
        "schema": "sportrx.alpha_dataset_template",
        "schema_version": "0.1",
        "status": "ready_for_alpha_capture",
        "participant_scope": "5-10 recreational adult alpha participants",
        "tables": TABLES,
        "table_count": len(TABLES),
        "minimum_rules": MINIMUM_RULES,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def alpha_dataset_csv_templates(template: dict[str, Any] | None = None) -> dict[str, str]:
    """Return header-only CSV templates keyed by table id."""

    template = template or build_alpha_dataset_template()
    csv_templates: dict[str, str] = {}
    for table in template["tables"]:
        buffer = StringIO()
        writer = csv.DictWriter(buffer, fieldnames=table["fields"])
        writer.writeheader()
        csv_templates[table["id"]] = buffer.getvalue()
    return csv_templates


def alpha_dataset_dictionary_markdown(template: dict[str, Any] | None = None) -> str:
    """Export the alpha dataset template as a readable data dictionary."""

    template = template or build_alpha_dataset_template()
    lines = [
        "# SportRx Alpha Dataset Template",
        "",
        f"- Status: {template['status']}",
        f"- Scope: {template['participant_scope']}",
        f"- Claim boundary: {template['claim_boundary']}",
        "",
        "## Minimum Rules",
    ]
    for rule in template["minimum_rules"]:
        lines.append(f"- {rule}")

    lines.append("")
    lines.append("## Tables")
    for table in template["tables"]:
        lines.extend(
            [
                "",
                f"### {table['id']}",
                f"- Filename: `{table['filename']}`",
                f"- Purpose: {table['purpose']}",
                "",
                "| Field |",
                "| --- |",
            ]
        )
        for field in table["fields"]:
            lines.append(f"| `{field}` |")

    return "\n".join(lines) + "\n"
