"""Guided protocol for SportRx Hybrid Benchmark v1.

The protocol layer describes how to run and repeat the benchmark. It does not
score users, create percentiles, or make medical or race predictions.
"""

from __future__ import annotations

from typing import Any

from .benchmark import get_hybrid_benchmark


CLAIM_BOUNDARY = (
    "Protocol guidance only. This is not a validated score, percentile, race "
    "prediction, injury-risk estimate, or medical clearance."
)


GLOBAL_STOP_RULES = [
    "Do not test unless Safety Gate has explicitly allowed Benchmark entry.",
    "Stop if chest pain, unexplained shortness of breath, dizziness, faintness, or unusual palpitations occur.",
    "Stop if pain changes your movement pattern or feels sharp, worsening, or unusual.",
    "Keep the first attempt controlled if you are new to HYROX or hybrid-style training.",
]


def _component_protocol(component: dict[str, Any], benchmark_path: str) -> dict[str, Any]:
    component_id = component["id"]
    common = {
        "component_id": component_id,
        "test": component["test"],
        "area": component["area"],
        "required_equipment": component.get("required_equipment", []),
        "fields": component.get("fields", []),
        "optional": bool(component.get("optional", False)),
        "protocol_evidence_id": component.get("protocol_evidence_id", "not_mapped"),
        "protocol_evidence_status": component.get("protocol_evidence_status", "experimental"),
        "record": [
            "Completion status",
            "Raw result in the listed unit",
            "RPE 0-10 within 2 minutes after finishing",
            "Equipment, substitution, load, route, and notes",
        ],
        "retest_notes": [
            "Use the same route, machine, load, substitution, and component order when possible.",
            "Compare raw results against your own previous result before using group benchmarks.",
        ],
    }

    details = {
        "run_1km": {
            "purpose": "Measure current short aerobic running output.",
            "setup": [
                "Use a measured 1 km route, track, or treadmill.",
                "Record surface, gradient, and whether the result was indoor or outdoor.",
            ],
            "execution": [
                "Warm up first, then complete 1 km at a hard but controlled effort.",
                "Do not sprint the first 200 m on a first test.",
            ],
            "stop_if": GLOBAL_STOP_RULES[1:3],
        },
        "station_circuit": {
            "purpose": "Capture repeatable strength-endurance and station tolerance.",
            "setup": [
                "Choose the same movements and loads before starting.",
                "Write down kettlebell, dumbbell, carry, lunge, or bodyweight substitutions.",
            ],
            "execution": [
                "Complete the station circuit with consistent movement standards.",
                "Record rounds, time, load, and any movement breaks.",
            ],
            "stop_if": GLOBAL_STOP_RULES[1:],
        },
        "row_or_ski_1km": {
            "purpose": "Measure station-specific machine output when RowErg or SkiErg is available.",
            "setup": [
                "Use the same RowErg or SkiErg model and damper setting for retest.",
                "Record whether the test was row or ski.",
            ],
            "execution": [
                "Complete 1 km at a hard but controlled effort.",
                "Keep technique consistent instead of chasing one-off peak output.",
            ],
            "stop_if": GLOBAL_STOP_RULES[1:3],
        },
        "compromised_run": {
            "purpose": "Observe running output after station fatigue.",
            "setup": [
                "Use the same measured 400 m route or treadmill setup each time.",
                "Run this after the station circuit if it is safe and appropriate.",
            ],
            "execution": [
                "Complete 400 m after station work without maximal sprinting.",
                "Record time and RPE separately from the fresh running test.",
            ],
            "stop_if": GLOBAL_STOP_RULES[1:],
        },
        "run_1km_or_6min": {
            "purpose": "Create a low-equipment aerobic field-test anchor.",
            "setup": [
                "Use a safe repeatable route and timer.",
                "Choose either 1 km time or 6-minute distance, then keep that choice for retest.",
            ],
            "execution": [
                "Run or run/walk at a hard but controlled effort.",
                "Record whether the result is time for 1 km or distance for 6 minutes.",
            ],
            "stop_if": GLOBAL_STOP_RULES[1:3],
        },
        "bodyweight_circuit": {
            "purpose": "Capture low-equipment strength-endurance tolerance.",
            "setup": [
                "Choose the same bodyweight circuit and movement standards before starting.",
                "Record substitutions such as step-ups, lunges, or loaded backpack carries.",
            ],
            "execution": [
                "Complete the circuit at a repeatable effort and record rounds or time.",
                "Avoid turning the first test into a maximal unsupervised challenge.",
            ],
            "stop_if": GLOBAL_STOP_RULES[1:],
        },
        "transition_practice": {
            "purpose": "Observe tolerance when switching between locomotion and station work.",
            "setup": [
                "Use the same route, transition space, and movement options each time.",
                "Keep this optional if the first two low-equipment tests are already demanding.",
            ],
            "execution": [
                "Alternate run/walk and bodyweight station blocks.",
                "Record completed rounds and RPE rather than creating a score.",
            ],
            "stop_if": GLOBAL_STOP_RULES[1:],
        },
    }

    fallback = {
        "purpose": "Collect a repeatable raw benchmark measurement.",
        "setup": ["Use the same setup when retesting."],
        "execution": ["Complete the component according to the listed test description."],
        "stop_if": GLOBAL_STOP_RULES[1:],
    }
    context_fields = {
        "run_1km": ["route_or_treadmill", "surface", "gradient_or_incline", "timing_method", "warmup_minutes", "familiarization_level", "test_order"],
        "run_1km_or_6min": ["test_variant", "route_or_treadmill", "surface", "gradient_or_incline", "timing_method", "warmup_minutes", "familiarization_level", "test_order"],
        "row_or_ski_1km": ["erg_type", "erg_model", "drag_factor", "timing_method", "warmup_minutes", "familiarization_level", "test_order"],
        "station_circuit": ["movement_standard", "loads_used", "rest_rule", "warmup_minutes", "familiarization_level", "test_order"],
        "bodyweight_circuit": ["movement_standard", "rest_rule", "warmup_minutes", "familiarization_level", "test_order"],
        "compromised_run": ["route_or_treadmill", "surface", "gradient_or_incline", "timing_method", "preceding_station_circuit", "warmup_minutes", "familiarization_level", "test_order"],
        "transition_practice": ["movement_standard", "rest_rule", "route_or_treadmill", "warmup_minutes", "familiarization_level", "test_order"],
    }
    return {
        **common,
        **details.get(component_id, fallback),
        "benchmark_path": benchmark_path,
        "standardization_fields": context_fields.get(component_id, ["warmup_minutes", "test_order"]),
    }


def get_benchmark_protocol(equipment_access: list[str] | None = None) -> dict[str, Any]:
    """Return a guided, repeatable protocol for the selected benchmark path."""

    benchmark = get_hybrid_benchmark(equipment_access)
    spec = benchmark["spec"]
    component_protocols = [_component_protocol(component, benchmark["path"]) for component in spec["components"]]
    return {
        "name": spec["name"],
        "label": spec["label"],
        "version": spec["version"],
        "path": benchmark["path"],
        "evidence_status": spec["evidence_status"],
        "claim_boundary": CLAIM_BOUNDARY,
        "equipment_access": list(equipment_access or []),
        "test_day_flow": [
            {
                "step": "1. Safety Gate",
                "instruction": "Confirm Safety Gate Benchmark eligibility and no warning symptoms before testing.",
            },
            {
                "step": "2. Same-Protocol Setup",
                "instruction": "Choose route, machine, load, substitutions, and order before starting.",
            },
            {
                "step": "3. Warm-up",
                "instruction": "Use 8-12 minutes of easy movement plus a few short practice efforts.",
            },
            {
                "step": "4. Component Tests",
                "instruction": "Complete selected components in order and record raw results immediately.",
            },
            {
                "step": "5. Notes And Retest Anchor",
                "instruction": "Save equipment, route, loads, substitutions, RPE, and notes for retest.",
            },
        ],
        "global_stop_rules": GLOBAL_STOP_RULES,
        "component_protocols": component_protocols,
        "recording_principles": [
            "Missing components stay Not tested.",
            "Do not convert rounds, distance, or mixed station work into a score without a documented rule.",
            "At least two measured dimensions are needed before SportRx compares strongest area and main gap.",
            "Safety Gate can block training handoff, but it does not raise or lower performance results.",
            "Each component states whether its protocol has partial evidence or remains experimental.",
        ],
    }


def protocol_markdown(protocol: dict[str, Any]) -> str:
    """Export the guided protocol as a readable markdown document."""

    lines = [
        f"# {protocol['name']}",
        "",
        f"- Path: {protocol['path']}",
        f"- Version: {protocol['version']}",
        f"- Evidence status: {protocol['evidence_status']}",
        f"- Claim boundary: {protocol['claim_boundary']}",
        "",
        "## Test-Day Flow",
    ]
    for item in protocol["test_day_flow"]:
        lines.append(f"- {item['step']}: {item['instruction']}")

    lines.extend(["", "## Stop Rules"])
    for rule in protocol["global_stop_rules"]:
        lines.append(f"- {rule}")

    lines.extend(["", "## Components"])
    for component in protocol["component_protocols"]:
        lines.extend(
            [
                f"### {component['test']}",
                f"- Area: {component['area']}",
                f"- Purpose: {component['purpose']}",
                f"- Protocol evidence: {component['protocol_evidence_status']} ({component['protocol_evidence_id']})",
                f"- Required equipment: {', '.join(component['required_equipment'])}",
                f"- Fields: {', '.join(component['fields'])}",
                "- Setup:",
            ]
        )
        for setup in component["setup"]:
            lines.append(f"  - {setup}")
        lines.append("- Execution:")
        for execution in component["execution"]:
            lines.append(f"  - {execution}")
        lines.append("- Record:")
        for record in component["record"]:
            lines.append(f"  - {record}")
        lines.append(f"- Standardization fields: {', '.join(component['standardization_fields'])}")

    lines.extend(["", "## Recording Principles"])
    for principle in protocol["recording_principles"]:
        lines.append(f"- {principle}")
    return "\n".join(lines) + "\n"
