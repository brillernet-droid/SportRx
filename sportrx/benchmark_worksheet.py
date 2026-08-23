"""Printable benchmark worksheet for SportRx Hybrid Benchmark sessions."""

from __future__ import annotations

from typing import Any

from .benchmark_protocol import get_benchmark_protocol


CLAIM_BOUNDARY = (
    "Benchmark Worksheet is a local data-capture aid. It does not score "
    "performance, validate SportRx, predict outcomes, or provide medical clearance."
)


def _blank_line(label: str, hint: str = "") -> dict[str, str]:
    return {"label": label, "hint": hint}


def build_benchmark_worksheet(equipment_access: list[str] | None = None) -> dict[str, Any]:
    """Build a test-day worksheet from the selected benchmark protocol."""

    protocol = get_benchmark_protocol(equipment_access)
    component_rows = []
    for order, component in enumerate(protocol["component_protocols"], start=1):
        component_rows.append(
            {
                "order": order,
                "component_id": component["component_id"],
                "test": component["test"],
                "area": component["area"],
                "optional": component["optional"],
                "required_equipment": component["required_equipment"],
                "record_fields": component["fields"],
                "result_blank": "________________",
                "unit_blank": "________________",
                "rpe_blank": "____ / 10",
                "equipment_blank": "________________",
                "substitution_blank": "________________",
                "notes_blank": "________________",
                "retest_anchor": "Use the same setup, order, route, load, and substitution when possible.",
            }
        )

    return {
        "schema": "sportrx.benchmark_worksheet",
        "schema_version": "0.1",
        "title": "SportRx Hybrid Benchmark v1 Worksheet",
        "protocol_name": protocol["name"],
        "protocol_version": protocol["version"],
        "benchmark_path": protocol["path"],
        "equipment_access": list(equipment_access or []),
        "claim_boundary": CLAIM_BOUNDARY,
        "session_setup": [
            _blank_line("Date", "YYYY-MM-DD"),
            _blank_line("Tester / reviewer", "optional"),
            _blank_line("Location / route", "track, treadmill, gym, outdoor route"),
            _blank_line("Equipment model / loads", "RowErg/SkiErg damper, dumbbell/kettlebell loads, substitutions"),
            _blank_line("Body state before test", "sleep, soreness, unusual symptoms, warm-up notes"),
        ],
        "safety_checklist": [
            {"item": rule, "checkbox": "[ ]"}
            for rule in protocol["global_stop_rules"]
        ],
        "component_rows": component_rows,
        "after_test": [
            _blank_line("Protocol deviations", "anything not done as planned"),
            _blank_line("Adverse signs or stop reasons", "if any"),
            _blank_line("Retest anchor", "what must stay the same next time"),
            _blank_line("Import notes", "which fields can be entered into Benchmark Log / HYROX Check"),
        ],
        "recording_principles": protocol["recording_principles"],
    }


def benchmark_worksheet_markdown(worksheet: dict[str, Any]) -> str:
    """Export the worksheet as Markdown for printing or handoff."""

    lines = [
        f"# {worksheet['title']}",
        "",
        f"- Protocol: {worksheet['protocol_name']} / {worksheet['protocol_version']}",
        f"- Path: {worksheet['benchmark_path']}",
        f"- Equipment access: {', '.join(worksheet['equipment_access']) if worksheet['equipment_access'] else 'low-equipment / not specified'}",
        f"- Claim boundary: {worksheet['claim_boundary']}",
        "",
        "## Session Setup",
    ]
    for item in worksheet["session_setup"]:
        lines.append(f"- {item['label']}: ____________________  _{item['hint']}_")

    lines.extend(["", "## Safety Checklist"])
    for item in worksheet["safety_checklist"]:
        lines.append(f"- {item['checkbox']} {item['item']}")

    lines.extend(["", "## Component Results"])
    for component in worksheet["component_rows"]:
        optional = "optional" if component["optional"] else "recommended"
        lines.extend(
            [
                "",
                f"### {component['order']}. {component['test']} ({optional})",
                f"- Area: {component['area']}",
                f"- Required equipment: {', '.join(component['required_equipment'])}",
                f"- Record fields: {', '.join(component['record_fields'])}",
                f"- Completed: [ ] yes / [ ] no",
                f"- Result: {component['result_blank']}",
                f"- Unit: {component['unit_blank']}",
                f"- RPE: {component['rpe_blank']}",
                f"- Equipment / load: {component['equipment_blank']}",
                f"- Substitution: {component['substitution_blank']}",
                f"- Notes: {component['notes_blank']}",
                f"- Retest anchor: {component['retest_anchor']}",
            ]
        )

    lines.extend(["", "## After Test"])
    for item in worksheet["after_test"]:
        lines.append(f"- {item['label']}: ____________________  _{item['hint']}_")

    lines.extend(["", "## Recording Principles"])
    for principle in worksheet["recording_principles"]:
        lines.append(f"- {principle}")
    return "\n".join(lines) + "\n"
