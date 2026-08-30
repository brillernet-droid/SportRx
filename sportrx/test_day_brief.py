"""Test-day brief for SportRx Hybrid Benchmark v1.

The brief turns the protocol into a concise operator checklist for a local
benchmark session. It does not score or interpret performance.
"""

from __future__ import annotations

from typing import Any

from .benchmark_protocol import get_benchmark_protocol


CLAIM_BOUNDARY = (
    "Test-Day Brief is an operational checklist for running a repeatable "
    "benchmark session. It does not score performance, validate outcomes, "
    "predict race results, estimate injury risk, or provide medical clearance."
)


def _record_fields(component: dict[str, Any]) -> list[str]:
    fields = ["completed", "raw_result", "unit", "RPE_0_10", "equipment", "substitution", "notes"]
    for field in component.get("fields", []):
        if field not in fields:
            fields.append(field)
    return fields


def build_test_day_brief(equipment_access: list[str] | None = None) -> dict[str, Any]:
    """Build a concise test-day brief from the selected benchmark protocol."""

    protocol = get_benchmark_protocol(equipment_access)
    components = []
    for order, component in enumerate(protocol["component_protocols"], start=1):
        components.append(
            {
                "order": order,
                "component_id": component["component_id"],
                "test": component["test"],
                "area": component["area"],
                "optional": component["optional"],
                "purpose": component["purpose"],
                "required_equipment": component["required_equipment"],
                "setup": component["setup"],
                "execution": component["execution"],
                "record_fields": _record_fields(component),
                "stop_if": component.get("stop_if", []),
                "retest_notes": component.get("retest_notes", []),
            }
        )

    return {
        "schema": "sportrx.test_day_brief",
        "schema_version": "0.1",
        "benchmark_name": protocol["name"],
        "protocol_version": protocol["version"],
        "path": protocol["path"],
        "equipment_access": protocol["equipment_access"],
        "pre_test_checks": [
            "Confirm Safety Gate has explicitly allowed Benchmark entry.",
            "Choose the same route, machine, load, substitutions, and component order before starting.",
            "Prepare a timer and a place to record raw values immediately.",
            "Use 8-12 minutes of warm-up before the first component.",
        ],
        "global_stop_rules": protocol["global_stop_rules"],
        "components": components,
        "recording_principles": protocol["recording_principles"],
        "after_test": [
            "Save the Benchmark Log with component values, units, RPE, equipment, substitutions, and notes.",
            "Keep missing components as Not tested.",
            "Use the same protocol for retest before comparing raw change.",
            "Export the local session snapshot if another reviewer needs to reproduce the state.",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def test_day_brief_markdown(brief: dict[str, Any]) -> str:
    """Export the test-day brief as Markdown."""

    lines = [
        "# SportRx Test-Day Brief",
        "",
        f"- Benchmark: {brief['benchmark_name']}",
        f"- Path: {brief['path']}",
        f"- Protocol: {brief['protocol_version']}",
        f"- Equipment: {', '.join(brief.get('equipment_access', [])) or 'low-equipment / not selected'}",
        f"- Claim boundary: {brief.get('claim_boundary', CLAIM_BOUNDARY)}",
        "",
        "## Pre-Test Checks",
    ]
    for item in brief["pre_test_checks"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Stop Rules"])
    for rule in brief["global_stop_rules"]:
        lines.append(f"- {rule}")

    lines.extend(["", "## Component Order"])
    for component in brief["components"]:
        optional = "optional" if component["optional"] else "required"
        lines.extend(
            [
                f"### {component['order']}. {component['test']} ({optional})",
                f"- Area: {component['area']}",
                f"- Purpose: {component['purpose']}",
                f"- Required equipment: {', '.join(component['required_equipment']) or 'none'}",
                f"- Record fields: {', '.join(component['record_fields'])}",
                "- Setup:",
            ]
        )
        for setup in component["setup"]:
            lines.append(f"  - {setup}")
        lines.append("- Execution:")
        for execution in component["execution"]:
            lines.append(f"  - {execution}")

    lines.extend(["", "## After Test"])
    for item in brief["after_test"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Recording Principles"])
    for principle in brief["recording_principles"]:
        lines.append(f"- {principle}")
    return "\n".join(lines) + "\n"


test_day_brief_markdown.__test__ = False
