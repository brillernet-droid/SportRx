"""Test-session operator for SportRx Hybrid Benchmark v1.

The operator view turns the benchmark protocol into an on-screen test-day
control surface. It does not score performance or interpret results.
"""

from __future__ import annotations

from typing import Any

from .test_day_brief import build_test_day_brief


CLAIM_BOUNDARY = (
    "Test Session Operator supports repeatable local benchmark execution only. "
    "It does not score performance, validate outcomes, predict race results, "
    "estimate injury risk, or provide medical clearance."
)


def _unit_hint(component_id: str) -> str:
    if component_id in {"run_1km", "row_or_ski_1km", "compromised_run"}:
        return "seconds"
    if component_id == "run_1km_or_6min":
        return "seconds or meters; choose one protocol and keep it for retest"
    if "circuit" in component_id or component_id == "transition_practice":
        return "rounds, time, or protocol score only when a documented rule exists"
    return "raw value with unit"


def _component_step(component: dict[str, Any]) -> dict[str, Any]:
    required_fields = [
        "completed",
        "raw_result",
        "unit",
        "RPE_0_10",
        "equipment",
        "substitution",
        "notes",
    ]
    return {
        "step_id": f"component_{component['order']}",
        "order": component["order"],
        "type": "component",
        "component_id": component["component_id"],
        "label": component["test"],
        "area": component["area"],
        "optional": component["optional"],
        "status": "optional" if component["optional"] else "recommended",
        "purpose": component["purpose"],
        "setup": component["setup"],
        "execution": component["execution"],
        "required_fields": required_fields,
        "record_now": [
            "Raw result immediately after the component",
            "Unit exactly as tested",
            "RPE 0-10 within 2 minutes",
            "Equipment, route, load, substitution, and notes",
        ],
        "unit_hint": _unit_hint(component["component_id"]),
        "stop_if": component["stop_if"],
        "retest_anchor": component["retest_notes"],
        "benchmark_log_handoff": "Save this as a Benchmark Log component. Missing values stay Not tested.",
    }


def build_test_session_operator(
    equipment_access: list[str] | None = None,
    *,
    safety_gate_status: str | None = None,
) -> dict[str, Any]:
    """Build an operator-mode checklist for a local benchmark session."""

    brief = build_test_day_brief(equipment_access)
    safety_status = (safety_gate_status or "UNKNOWN").upper()
    blocked = safety_status == "RED"
    component_steps = [_component_step(component) for component in brief["components"]]
    preflight_steps = [
        {
            "step_id": "safety_gate",
            "order": 1,
            "type": "preflight",
            "label": "Safety Gate",
            "status": "blocked" if blocked else "ready",
            "instruction": "Do not run the benchmark when Safety Gate is RED.",
            "record": "Safety Gate status before testing.",
        },
        {
            "step_id": "protocol_lock",
            "order": 2,
            "type": "preflight",
            "label": "Protocol Lock",
            "status": "ready",
            "instruction": "Choose route, machine, load, substitutions, and component order before starting.",
            "record": "Protocol version, benchmark path, equipment access, route/machine/load notes.",
        },
        {
            "step_id": "warm_up",
            "order": 3,
            "type": "preflight",
            "label": "Warm-up",
            "status": "ready",
            "instruction": "Use 8-12 minutes of easy movement plus a few short practice efforts.",
            "record": "Warm-up completed and any abnormal symptoms.",
        },
    ]
    after_steps = [
        {
            "step_id": "save_benchmark_log",
            "order": len(preflight_steps) + len(component_steps) + 1,
            "type": "handoff",
            "label": "Save Benchmark Log",
            "status": "required",
            "instruction": "Save component results with values, units, RPE, equipment, substitutions, and notes.",
            "record": "Benchmark Log session saved locally.",
        },
        {
            "step_id": "retest_anchor",
            "order": len(preflight_steps) + len(component_steps) + 2,
            "type": "handoff",
            "label": "Retest Anchor",
            "status": "required",
            "instruction": "Use the same protocol and setup when retesting before comparing raw change.",
            "record": "Retest notes captured in export or session snapshot.",
        },
    ]
    steps = preflight_steps + component_steps + after_steps

    return {
        "schema": "sportrx.test_session_operator",
        "schema_version": "0.1",
        "status": "blocked_by_safety_gate" if blocked else "ready_for_test_day",
        "benchmark_name": brief["benchmark_name"],
        "protocol_version": brief["protocol_version"],
        "path": brief["path"],
        "equipment_access": brief["equipment_access"],
        "safety_gate_status": safety_status,
        "total_steps": len(steps),
        "component_count": len(component_steps),
        "recommended_components": sum(1 for step in component_steps if not step["optional"]),
        "optional_components": sum(1 for step in component_steps if step["optional"]),
        "steps": steps,
        "component_steps": component_steps,
        "preflight_steps": preflight_steps,
        "after_steps": after_steps,
        "global_stop_rules": brief["global_stop_rules"],
        "next_action": (
            "Resolve Safety Gate before running the operator."
            if blocked
            else "Run the steps in order, then save results in Benchmark Log."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_test_day_command_board(operator: dict[str, Any]) -> dict[str, Any]:
    """Summarize an operator session into a test-day command board."""

    blocked = operator["status"] == "blocked_by_safety_gate"
    first_component = operator["component_steps"][0] if operator["component_steps"] else None
    required_fields = [
        "completion status",
        "raw result",
        "unit",
        "RPE 0-10",
        "equipment / route / load",
        "substitution",
        "notes",
    ]
    cards = [
        {
            "id": "preflight",
            "label": "Preflight",
            "value": "Blocked" if blocked else "Ready",
            "detail": "Safety Gate, protocol lock, and warm-up must be checked before component testing.",
            "status": "blocked" if blocked else "ready",
        },
        {
            "id": "component_sequence",
            "label": "Component sequence",
            "value": f"{operator['recommended_components']} recommended + {operator['optional_components']} optional",
            "detail": (
                f"Start with {first_component['label']}." if first_component else "No component steps available."
            ),
            "status": "ready" if operator["component_count"] else "waiting",
        },
        {
            "id": "record_now",
            "label": "Record now",
            "value": f"{len(required_fields)} fields",
            "detail": "Every completed component needs raw value, unit, RPE, equipment context, substitutions, and notes.",
            "status": "ready",
        },
        {
            "id": "handoff",
            "label": "Benchmark Log handoff",
            "value": "Required",
            "detail": "Save the raw session before importing compatible fields or interpreting retest change.",
            "status": "waiting",
        },
    ]
    phases = [
        {
            "phase": "1. Preflight",
            "action": "Confirm Safety Gate, lock protocol, and complete warm-up.",
            "record": "Safety Gate status, protocol version, equipment path, route/machine/load notes.",
        },
        {
            "phase": "2. Component tests",
            "action": "Run recommended components in order; optional components can remain Not tested.",
            "record": "Raw result, unit, RPE, equipment, substitutions, and notes after each component.",
        },
        {
            "phase": "3. Save log",
            "action": "Save Benchmark Log before using results elsewhere.",
            "record": "Session-level notes, protocol deviations, and component rows.",
        },
        {
            "phase": "4. Retest anchor",
            "action": "Retest with the same route, equipment, loads, and order before comparing change.",
            "record": "Retest setup notes and comparable component IDs.",
        },
    ]
    return {
        "schema": "sportrx.test_day_command_board",
        "schema_version": "0.1",
        "status": "blocked_by_safety_gate" if blocked else "ready_for_operator",
        "benchmark_name": operator["benchmark_name"],
        "path": operator["path"],
        "protocol_version": operator["protocol_version"],
        "safety_gate_status": operator["safety_gate_status"],
        "cards": cards,
        "phases": phases,
        "required_fields": required_fields,
        "primary_message": (
            "Test-Day Command Board turns the benchmark protocol into a local "
            "operator workflow: preflight, component tests, raw recording, log "
            "handoff, and retest anchor."
        ),
        "next_action": operator["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def test_day_command_board_markdown(board: dict[str, Any]) -> str:
    """Export the test-day command board as Markdown."""

    lines = [
        "# SportRx Test-Day Command Board",
        "",
        f"- Benchmark: {board['benchmark_name']}",
        f"- Path: {board['path']}",
        f"- Protocol: {board['protocol_version']}",
        f"- Safety Gate: {board['safety_gate_status']}",
        f"- Status: {board['status']}",
        f"- Claim boundary: {board['claim_boundary']}",
        "",
        board["primary_message"],
        "",
        "## Command Cards",
    ]
    for card in board["cards"]:
        lines.extend(
            [
                "",
                f"### {card['label']}",
                f"- Value: {card['value']}",
                f"- Status: {card['status']}",
                f"- Detail: {card['detail']}",
            ]
        )
    lines.extend(["", "## Test-Day Phases"])
    for phase in board["phases"]:
        lines.extend(
            [
                "",
                f"### {phase['phase']}",
                f"- Action: {phase['action']}",
                f"- Record: {phase['record']}",
            ]
        )
    lines.extend(["", "## Required Fields"])
    for field in board["required_fields"]:
        lines.append(f"- {field}")
    lines.extend(["", "## Next Action", "", board["next_action"]])
    return "\n".join(lines) + "\n"


def test_session_operator_markdown(operator: dict[str, Any]) -> str:
    """Export the test-session operator as Markdown."""

    lines = [
        "# SportRx Test Session Operator",
        "",
        f"- Benchmark: {operator['benchmark_name']}",
        f"- Path: {operator['path']}",
        f"- Protocol: {operator['protocol_version']}",
        f"- Safety Gate: {operator['safety_gate_status']}",
        f"- Status: {operator['status']}",
        f"- Steps: {operator['total_steps']}",
        f"- Claim boundary: {operator['claim_boundary']}",
        "",
        "## Operator Steps",
    ]
    for step in operator["steps"]:
        lines.extend(
            [
                "",
                f"### {step['order']}. {step['label']}",
                f"- Type: {step['type']}",
                f"- Status: {step['status']}",
            ]
        )
        if step["type"] == "component":
            lines.extend(
                [
                    f"- Area: {step['area']}",
                    f"- Unit hint: {step['unit_hint']}",
                    f"- Required fields: {', '.join(step['required_fields'])}",
                    f"- Benchmark Log handoff: {step['benchmark_log_handoff']}",
                ]
            )
            lines.append("- Record now:")
            for item in step["record_now"]:
                lines.append(f"  - {item}")
        else:
            lines.extend([f"- Instruction: {step['instruction']}", f"- Record: {step['record']}"])

    lines.extend(["", "## Global Stop Rules"])
    for rule in operator["global_stop_rules"]:
        lines.append(f"- {rule}")
    lines.extend(["", "## Next Action", "", operator["next_action"]])
    return "\n".join(lines) + "\n"


test_session_operator_markdown.__test__ = False
test_day_command_board_markdown.__test__ = False
