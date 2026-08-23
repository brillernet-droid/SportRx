"""Quantified intake audit for SportRx user-facing inputs.

This module makes the intake contract explicit: what is numeric, what is a
measured test, what is safety-only, and what is ignored. It does not introduce
new scoring rules.
"""

from __future__ import annotations

from typing import Any

from .input_ledger import build_input_ledger


CLAIM_BOUNDARY = (
    "Intake Precision Audit explains how current inputs are collected and used. "
    "It does not validate SportRx, score performance, estimate risk, or provide "
    "medical clearance."
)


ENTRY_TYPE_LABELS = {
    "direct numeric": "direct_numeric",
    "measured test": "measured_test",
    "protocol provenance": "protocol_provenance",
    "safety checklist": "safety_only",
    "safety checkbox": "safety_only",
    "multi-select": "context_selection",
    "selection": "context_selection",
    "legacy compatibility": "legacy_ignored",
    "unsupported": "unsupported_ignored",
}


LEGACY_ALIAS_FIELDS = {"exercise_days_last_4w", "mvpa_minutes_per_week"}
LEGACY_SUBJECTIVE_FIELDS = {
    "endurance_background",
    "resistance_background",
    "running_comfort",
    "hiit_comfort",
    "loaded_movement_comfort",
}


def build_intake_precision_audit(profile: dict[str, Any]) -> dict[str, Any]:
    """Build a product-facing audit of input precision and output roles."""

    ledger = build_input_ledger(profile)
    rows = []
    for item in ledger["rows"]:
        precision_class = ENTRY_TYPE_LABELS.get(item["entry_type"], "other")
        if item["field_id"] in LEGACY_ALIAS_FIELDS:
            precision_class = "legacy_alias"
        elif item["field_id"] in LEGACY_SUBJECTIVE_FIELDS:
            precision_class = "legacy_subjective_ignored"
        rows.append(
            {
                "field_id": item["field_id"],
                "label": item["label"],
                "value": item["value"],
                "unit": item["unit"],
                "entry_type": item["entry_type"],
                "precision_class": precision_class,
                "source_type": item["source_type"],
                "status": item["status"],
                "affects_output": item["affects_output"],
                "used_by": item["used_by"],
                "output_role": item["output_role"],
                "user_boundary": _boundary_for(item, precision_class),
            }
        )

    collected_rows = [row for row in rows if row["status"] == "active"]
    direct_numeric_rows = [row for row in rows if row["precision_class"] == "direct_numeric"]
    measured_rows = [row for row in rows if row["precision_class"] == "measured_test"]
    ignored_rows = [row for row in rows if row["status"] in {"legacy", "ignored"}]
    problematic_ignored_rows = [
        row
        for row in ignored_rows
        if row["precision_class"] in {"legacy_subjective_ignored", "unsupported_ignored"}
    ]
    active_affecting_rows = [row for row in collected_rows if row["affects_output"]]

    status = "intake_contract_ready"
    next_action = (
        "Use Quick Match for quantified self-reported behavior, then use SportRx "
        "Hybrid Benchmark v1 for measured performance."
    )
    if problematic_ignored_rows:
        status = "review_ignored_fields"
        next_action = "Remove or ignore unsupported and legacy subjective values before trusting the intake."
    elif not active_affecting_rows:
        status = "needs_active_inputs"
        next_action = "Collect direct numeric behavior fields before interpreting intake."

    return {
        "schema": "sportrx.intake_precision_audit",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "summary": {
            "active_affecting_inputs": len(active_affecting_rows),
            "direct_numeric_fields": len(direct_numeric_rows),
            "direct_numeric_collected": sum(1 for row in direct_numeric_rows if row["status"] == "active"),
            "measured_test_fields": len(measured_rows),
            "measured_tests_recorded": sum(1 for row in measured_rows if row["status"] == "active"),
            "not_tested": sum(1 for row in measured_rows if row["status"] == "not_tested"),
            "safety_only_fields": sum(1 for row in rows if row["precision_class"] == "safety_only"),
            "ignored_or_legacy_fields": len(ignored_rows),
            "problematic_ignored_fields": len(problematic_ignored_rows),
        },
        "rows": rows,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _boundary_for(row: dict[str, Any], precision_class: str) -> str:
    if precision_class == "legacy_alias":
        return "Backward-compatible alias; current rules use the direct numeric field."
    if row["status"] in {"legacy", "ignored"}:
        return "Ignored by current rules; should not affect output."
    if precision_class == "measured_test":
        return "Only counts when measured; missing values remain Not tested."
    if precision_class == "safety_only":
        return "Can block or caution training handoff; never changes performance."
    if precision_class == "direct_numeric":
        return "Quantified self-report; useful for routing and constraints, not a lab test."
    if precision_class == "protocol_provenance":
        return "Documents test source; improves review quality, not measured score."
    if precision_class == "context_selection":
        return "Context or routing language; not a performance measurement."
    return "Documented input; check output role before interpretation."


def intake_precision_markdown(audit: dict[str, Any]) -> str:
    """Export the intake precision audit as Markdown."""

    summary = audit["summary"]
    lines = [
        "# SportRx Intake Precision Audit",
        "",
        f"- Status: {audit['status']}",
        f"- Active affecting inputs: {summary['active_affecting_inputs']}",
        f"- Direct numeric fields: {summary['direct_numeric_collected']} / {summary['direct_numeric_fields']}",
        f"- Measured tests recorded: {summary['measured_tests_recorded']} / {summary['measured_test_fields']}",
        f"- Not tested: {summary['not_tested']}",
        f"- Ignored or legacy fields: {summary['ignored_or_legacy_fields']}",
        f"- Claim boundary: {audit['claim_boundary']}",
        "",
        "## Inputs",
    ]
    for row in audit["rows"]:
        used_by = ", ".join(row["used_by"]) if row["used_by"] else "Not used"
        lines.append(
            f"- `{row['field_id']}` - {row['label']} [{row['precision_class']} / {row['status']}]: "
            f"{row['value']}. Used by: {used_by}. Boundary: {row['user_boundary']}"
        )
    return "\n".join(lines) + "\n"
