"""SportRx Hybrid Benchmark v1 specification.

The benchmark is a prototype testing layer. It is not validated and does not
provide percentile rankings, medical clearance, or race prediction.
"""

from __future__ import annotations

from typing import Any


STANDARD_BENCHMARK = {
    "name": "SportRx Hybrid Benchmark v1",
    "label": "Prototype benchmark",
    "version": "0.1",
    "components": [
        {
            "id": "run_1km",
            "area": "running",
            "test": "1 km run",
            "fields": ["time_seconds", "rpe_0_10"],
            "required_equipment": ["measured route or treadmill", "timer"],
            "protocol_evidence_id": "PROTO-COMPONENT-1KM-RUN-V1",
            "protocol_evidence_status": "partial_evidence",
        },
        {
            "id": "station_circuit",
            "area": "strength_endurance",
            "test": "3-round station circuit",
            "fields": ["rounds_completed", "time_seconds", "rpe_0_10", "loads_used"],
            "required_equipment": ["kettlebell or dumbbell", "space for carries or lunges"],
            "protocol_evidence_id": "PROTO-COMPONENT-STATION-CIRCUIT-V1",
            "protocol_evidence_status": "experimental",
        },
        {
            "id": "row_or_ski_1km",
            "area": "station_experience",
            "test": "1 km row or 1 km ski",
            "fields": ["modality", "time_seconds", "rpe_0_10"],
            "required_equipment": ["RowErg or SkiErg"],
            "optional": True,
            "protocol_evidence_id": "PROTO-COMPONENT-ERG-1KM-V1",
            "protocol_evidence_status": "partial_evidence",
        },
        {
            "id": "compromised_run",
            "area": "work_capacity",
            "test": "400 m run after station circuit",
            "fields": ["time_seconds", "rpe_0_10"],
            "required_equipment": ["measured route or treadmill", "timer"],
            "optional": True,
            "protocol_evidence_id": "PROTO-COMPONENT-COMPROMISED-RUN-V1",
            "protocol_evidence_status": "experimental",
        },
    ],
    "safety_notes": [
        "Do not complete benchmark testing when the safety gate is RED.",
        "Stop the test if warning symptoms occur.",
        "Keep the first attempt submaximal if you are new to hybrid training.",
    ],
    "retest_guidance": "Repeat the same version after 4 weeks using the same setup.",
    "evidence_status": "experimental",
}


LOW_EQUIPMENT_BENCHMARK = {
    "name": "SportRx Hybrid Benchmark v1",
    "label": "Prototype benchmark - low-equipment path",
    "version": "0.1-low-equipment",
    "components": [
        {
            "id": "run_1km_or_6min",
            "area": "running",
            "test": "1 km run or 6-minute run/walk",
            "fields": ["distance_meters", "time_seconds", "rpe_0_10"],
            "required_equipment": ["safe route", "timer"],
            "protocol_evidence_id": "PROTO-COMPONENT-6MIN-RUN-WALK-V1",
            "protocol_evidence_status": "partial_evidence",
        },
        {
            "id": "bodyweight_circuit",
            "area": "strength_endurance",
            "test": "Bodyweight station circuit",
            "fields": ["rounds_completed", "time_seconds", "rpe_0_10"],
            "required_equipment": ["floor space"],
            "substitutions": ["step-ups instead of sled push", "loaded backpack carry if safe"],
            "protocol_evidence_id": "PROTO-COMPONENT-STATION-CIRCUIT-V1",
            "protocol_evidence_status": "experimental",
        },
        {
            "id": "transition_practice",
            "area": "work_capacity",
            "test": "Run/walk plus bodyweight transition block",
            "fields": ["rounds_completed", "rpe_0_10", "notes"],
            "required_equipment": ["safe route", "floor space"],
            "optional": True,
            "protocol_evidence_id": "PROTO-COMPONENT-COMPROMISED-RUN-V1",
            "protocol_evidence_status": "experimental",
        },
    ],
    "safety_notes": STANDARD_BENCHMARK["safety_notes"],
    "retest_guidance": "Repeat the same low-equipment version after 4 weeks.",
    "evidence_status": "experimental",
}


def get_hybrid_benchmark(equipment_access: list[str] | None = None) -> dict[str, Any]:
    """Return standard benchmark when equipment exists, otherwise low-equipment path."""

    equipment = set(equipment_access or [])
    if {"row", "ski"} & equipment or {"kettlebell", "dumbbell"} & equipment:
        return {
            "available": True,
            "path": "standard",
            "spec": STANDARD_BENCHMARK,
            "scoring": {
                "status": "placeholder",
                "note": "Scoring cutoffs are not validated. Store raw test results first.",
            },
        }
    return {
        "available": True,
        "path": "low_equipment",
        "spec": LOW_EQUIPMENT_BENCHMARK,
        "scoring": {
            "status": "placeholder",
            "note": "Use this path to collect repeatable measurements without specialized machines.",
        },
    }


def empty_benchmark_result() -> dict[str, Any]:
    """Return an explicit unavailable result state before testing."""

    return {
        "completed": False,
        "status": "Not tested",
        "results": {},
        "missing": [
            "No running benchmark recorded",
            "No strength-endurance circuit recorded",
            "No station-specific result recorded",
            "No compromised-work result recorded",
        ],
        "next_action": "Complete the SportRx Hybrid Benchmark v1 or use the low-equipment path.",
    }
