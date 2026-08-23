"""Benchmark log records for SportRx.

The log layer stores raw benchmark measurements first. It does not create
percentiles, predictions, or validated readiness scores.
"""

from __future__ import annotations

import csv
import io
import json
from datetime import date
from typing import Any
from uuid import uuid4

from .benchmark import get_hybrid_benchmark


SCHEMA_VERSION = "0.1"


def _clean_optional_number(value: Any) -> float | None:
    if value is None or value == "":
        return None
    number = float(value)
    if number <= 0:
        return None
    return number


def _component_map(path: str, equipment_access: list[str] | None = None) -> dict[str, dict[str, Any]]:
    benchmark = get_hybrid_benchmark(equipment_access)
    spec = benchmark["spec"]
    return {component["id"]: {**component, "benchmark_path": path or benchmark["path"]} for component in spec["components"]}


def _entry_contract_for_component(component: dict[str, Any]) -> dict[str, Any]:
    component_id = component["id"]
    fields = list(component.get("fields", []))
    base = {
        "component_id": component_id,
        "test": component["test"],
        "area": component["area"],
        "required_fields": fields,
        "primary_value_field": "raw_result",
        "primary_value_label": "Raw result",
        "allowed_value_units": ["raw"],
        "companion_fields": [field for field in fields if field != "rpe_0_10"],
        "rpe_required": "rpe_0_10" in fields,
        "equipment_hint": ", ".join(component.get("required_equipment", [])),
        "import_policy": "raw_only",
        "ui_hint": "Record the raw result exactly as tested.",
        "not_allowed": [
            "Do not estimate missing performance data.",
            "Do not convert this result into percentiles or race predictions.",
        ],
    }

    if component_id == "run_1km":
        base.update(
            {
                "primary_value_field": "time_seconds",
                "primary_value_label": "1 km time",
                "allowed_value_units": ["seconds"],
                "companion_fields": [],
                "import_policy": "direct_hyrox_import",
                "ui_hint": "Enter the measured 1 km time in seconds.",
            }
        )
    elif component_id == "row_or_ski_1km":
        base.update(
            {
                "primary_value_field": "time_seconds",
                "primary_value_label": "1 km row/ski time",
                "allowed_value_units": ["seconds"],
                "companion_fields": ["modality"],
                "import_policy": "needs_row_or_ski_modality",
                "ui_hint": "Enter time in seconds and identify RowErg or SkiErg.",
            }
        )
    elif component_id == "compromised_run":
        base.update(
            {
                "primary_value_field": "time_seconds",
                "primary_value_label": "400 m compromised-run time",
                "allowed_value_units": ["seconds"],
                "companion_fields": [],
                "import_policy": "raw_only",
                "ui_hint": "Enter the post-circuit 400 m time in seconds.",
            }
        )
    elif component_id == "station_circuit":
        base.update(
            {
                "primary_value_field": "rounds_completed",
                "primary_value_label": "Rounds completed",
                "allowed_value_units": ["rounds", "score", "points"],
                "companion_fields": ["time_seconds", "loads_used"],
                "import_policy": "raw_rounds_only_unless_protocol_score",
                "ui_hint": "Use rounds for raw station-circuit completion. Use score/points only when a documented protocol score already exists.",
                "not_allowed": [
                    "Do not turn rounds, loads, or mixed station work into a 0-100 score without a documented protocol source.",
                    "Do not infer HYROX race readiness from this station record.",
                ],
            }
        )
    elif component_id == "run_1km_or_6min":
        base.update(
            {
                "primary_value_field": "distance_meters",
                "primary_value_label": "Distance or 1 km time",
                "allowed_value_units": ["meters", "seconds"],
                "companion_fields": ["time_seconds"],
                "import_policy": "raw_only",
                "ui_hint": "Use meters for a 6-minute run/walk or seconds for a measured 1 km time.",
            }
        )
    elif component_id == "bodyweight_circuit":
        base.update(
            {
                "primary_value_field": "rounds_completed",
                "primary_value_label": "Rounds completed",
                "allowed_value_units": ["rounds"],
                "companion_fields": ["time_seconds"],
                "import_policy": "raw_only",
                "ui_hint": "Enter completed bodyweight rounds and keep time context for retest comparability.",
            }
        )
    elif component_id == "transition_practice":
        base.update(
            {
                "primary_value_field": "rounds_completed",
                "primary_value_label": "Rounds completed",
                "allowed_value_units": ["rounds"],
                "companion_fields": ["notes"],
                "import_policy": "raw_only",
                "ui_hint": "Enter completed rounds and describe the transition block in notes.",
            }
        )

    base["companion_fields"] = [
        field for field in base["companion_fields"] if field != base["primary_value_field"] and field != "rpe_0_10"
    ]
    return base


def build_benchmark_log_entry_contract(equipment_access: list[str] | None = None) -> dict[str, Any]:
    """Describe exactly what each Benchmark Log component should collect."""

    benchmark = get_hybrid_benchmark(equipment_access)
    spec = benchmark["spec"]
    components = [_entry_contract_for_component(component) for component in spec["components"]]
    return {
        "schema": "sportrx.benchmark_log_entry_contract",
        "schema_version": SCHEMA_VERSION,
        "benchmark_name": spec["name"],
        "benchmark_path": benchmark["path"],
        "protocol_version": spec["version"],
        "evidence_status": spec["evidence_status"],
        "components": components,
        "primary_message": "Benchmark Log records component-specific raw results first. Missing tests stay Not tested; raw station work is not converted into synthetic scores.",
        "claim_boundary": "Entry contracts define data capture only. They do not validate SportRx, score performance, predict races, or provide medical clearance.",
    }


def benchmark_log_entry_contract_markdown(contract: dict[str, Any]) -> str:
    """Export the Benchmark Log entry contract as Markdown."""

    lines = [
        "# SportRx Benchmark Log Entry Contract",
        "",
        f"- Benchmark: {contract['benchmark_name']}",
        f"- Path: {contract['benchmark_path']}",
        f"- Protocol: {contract['protocol_version']}",
        f"- Evidence status: {contract['evidence_status']}",
        f"- Claim boundary: {contract['claim_boundary']}",
        "",
        contract["primary_message"],
        "",
        "## Component Contracts",
    ]
    for component in contract["components"]:
        lines.extend(
            [
                "",
                f"### {component['test']}",
                "",
                f"- Component ID: {component['component_id']}",
                f"- Area: {component['area']}",
                f"- Primary value: {component['primary_value_field']} ({', '.join(component['allowed_value_units'])})",
                f"- Required fields: {', '.join(component['required_fields'])}",
                f"- Companion fields: {', '.join(component['companion_fields']) or 'None'}",
                f"- Import policy: {component['import_policy']}",
                f"- UI hint: {component['ui_hint']}",
                f"- Equipment hint: {component['equipment_hint']}",
                "- Not allowed:",
            ]
        )
        for item in component["not_allowed"]:
            lines.append(f"  - {item}")
    return "\n".join(lines) + "\n"


def build_component_result(
    component_id: str,
    *,
    value: float | int | None = None,
    value_unit: str = "",
    rpe_0_10: float | int | None = None,
    equipment: list[str] | None = None,
    substitution: str | None = None,
    result_fields: dict[str, Any] | None = None,
    completed: bool = True,
    notes: str = "",
) -> dict[str, Any]:
    """Build a normalized raw component result."""

    return {
        "component_id": component_id,
        "completed": bool(completed),
        "value": _clean_optional_number(value),
        "value_unit": value_unit,
        "rpe_0_10": _clean_optional_number(rpe_0_10),
        "equipment": list(equipment or []),
        "substitution": substitution or None,
        "result_fields": dict(result_fields or {}),
        "notes": notes.strip(),
    }


def evaluate_benchmark_session_quality(
    component_results: list[dict[str, Any]],
    equipment_access: list[str] | None = None,
) -> dict[str, Any]:
    """Review a draft benchmark session before it is saved.

    This is a data-quality check, not a performance score. It helps the UI show
    what can be interpreted now and what should remain as raw/unfinished data.
    """

    completed_with_value = [
        result for result in component_results if result.get("completed") and result.get("value") is not None
    ]
    completed_without_value = [
        result for result in component_results if result.get("completed") and result.get("value") is None
    ]
    value_without_completion = [
        result for result in component_results if not result.get("completed") and result.get("value") is not None
    ]
    missing_rpe = [
        result["component_id"]
        for result in completed_with_value
        if result.get("rpe_0_10") is None
    ]
    missing_unit = [
        result["component_id"]
        for result in completed_with_value
        if not result.get("value_unit")
    ]
    contract_lookup = {
        component["component_id"]: component
        for component in build_benchmark_log_entry_contract(equipment_access)["components"]
    }
    unexpected_unit = [
        result["component_id"]
        for result in completed_with_value
        if contract_lookup.get(result["component_id"])
        and result.get("value_unit")
        and result.get("value_unit") not in contract_lookup[result["component_id"]].get("allowed_value_units", [])
    ]
    missing_required_context = []
    for result in completed_with_value:
        contract = contract_lookup.get(result["component_id"], {})
        result_fields = result.get("result_fields", {}) or {}
        for field in contract.get("companion_fields", []):
            if field in {"notes", "loads_used"}:
                continue
            if result_fields.get(field) in {None, ""}:
                missing_required_context.append(f"{result['component_id']}:{field}")
    measured_areas = sorted(
        {
            result.get("area", result.get("component_id", "unknown"))
            for result in completed_with_value
        }
    )

    issues = []
    warnings = []
    if not completed_with_value:
        issues.append("At least one completed component with a raw value is required before saving a Benchmark Log.")
    if completed_without_value:
        issues.append("Completed components need a raw result value before they can be saved as measured.")
    if missing_unit:
        issues.append("Completed components need a result unit.")
    if unexpected_unit:
        issues.append("Completed components use a unit outside the component entry contract: " + ", ".join(unexpected_unit))
    if value_without_completion:
        warnings.append("Some values were entered for components not marked complete; they will not count as measured.")
    if missing_rpe:
        warnings.append("RPE is missing for completed components: " + ", ".join(missing_rpe))
    if missing_required_context:
        warnings.append("Some completed components are missing companion context fields: " + ", ".join(missing_required_context))
    if len(measured_areas) < 2:
        warnings.append("At least two measured areas are recommended before interpreting strongest area vs main gap.")

    return {
        "status": "ready_to_save" if not issues else "needs_review",
        "save_allowed": not issues,
        "completed_components": len(completed_with_value),
        "measured_areas": measured_areas,
        "measured_area_count": len(measured_areas),
        "interpretation_ready": len(measured_areas) >= 2,
        "issues": issues,
        "warnings": warnings,
        "claim_boundary": "Session quality checks review data completeness only. They are not performance scores or validation claims.",
    }


def _completed_with_value(result: dict[str, Any]) -> bool:
    return bool(result.get("completed")) and result.get("value") is not None


def _hyrox_import_mapping(result: dict[str, Any]) -> dict[str, Any]:
    component_id = result.get("component_id", "unknown")
    unit = result.get("value_unit")
    equipment = set(result.get("equipment", []) or [])
    substitution = str(result.get("substitution") or "").lower()

    if not _completed_with_value(result):
        return {
            "component_id": component_id,
            "status": "not_measured",
            "target_fields": [],
            "reason": "Component is not completed with a raw value.",
        }

    if component_id == "run_1km" and unit == "seconds":
        return {
            "component_id": component_id,
            "status": "importable",
            "target_fields": ["one_km_run_seconds"],
            "label": "1 km run -> one_km_run_seconds",
            "reason": "Direct time-to-time mapping.",
        }

    if component_id == "row_or_ski_1km" and unit == "seconds":
        if "row" in equipment or "row" in substitution:
            return {
                "component_id": component_id,
                "status": "importable",
                "target_fields": ["one_km_row_seconds"],
                "label": "1 km row -> one_km_row_seconds",
                "reason": "Direct RowErg time-to-time mapping.",
            }
        if "ski" in equipment or "ski" in substitution:
            return {
                "component_id": component_id,
                "status": "importable",
                "target_fields": ["one_km_ski_seconds"],
                "label": "1 km ski -> one_km_ski_seconds",
                "reason": "Direct SkiErg time-to-time mapping.",
            }
        return {
            "component_id": component_id,
            "status": "needs_detail",
            "target_fields": [],
            "reason": "Row/Ski 1 km needs RowErg or SkiErg modality before HYROX Check import.",
        }

    if component_id == "station_circuit" and unit in {"score", "points"}:
        return {
            "component_id": component_id,
            "status": "importable",
            "target_fields": ["station_test_score", "station_test_protocol"],
            "label": "station circuit score -> station_test_score + station_test_protocol",
            "reason": "Protocol score can be carried with its Benchmark Log provenance.",
        }

    return {
        "component_id": component_id,
        "status": "raw_only",
        "target_fields": [],
        "reason": f"{component_id} remains raw benchmark log data.",
    }


def build_benchmark_import_compatibility(component_results: list[dict[str, Any]]) -> dict[str, Any]:
    """Review whether raw Benchmark Log results can hand off to HYROX Check.

    This is a compatibility check only. It does not score, normalize, or convert
    raw benchmark data into synthetic performance fields.
    """

    measured_mappings = [
        _hyrox_import_mapping(result)
        for result in component_results
        if _completed_with_value(result)
    ]
    importable = [item for item in measured_mappings if item["status"] == "importable"]
    needs_detail = [item for item in measured_mappings if item["status"] == "needs_detail"]
    raw_only = [item for item in measured_mappings if item["status"] == "raw_only"]

    if not measured_mappings:
        status = "no_completed_results"
        next_action = "Complete at least one Benchmark component before checking HYROX import compatibility."
    elif importable and (needs_detail or raw_only):
        status = "partial_import_ready"
        next_action = "Import the compatible fields and keep the rest as raw Benchmark Log data."
    elif importable:
        status = "ready_for_hyrox_import"
        next_action = "These measured fields can be imported into HYROX Check after saving."
    elif needs_detail:
        status = "needs_modality_detail"
        next_action = "Add RowErg/SkiErg modality or substitution detail before importing."
    else:
        status = "raw_log_only"
        next_action = "Save as raw Benchmark Log first; do not create artificial HYROX Check fields."

    return {
        "status": status,
        "hyrox_import_ready": bool(importable),
        "direct_import_count": len(importable),
        "needs_detail_count": len(needs_detail),
        "raw_only_count": len(raw_only),
        "importable_fields": sorted({field for item in importable for field in item["target_fields"]}),
        "items": measured_mappings,
        "importable": importable,
        "needs_detail": needs_detail,
        "raw_only": raw_only,
        "next_action": next_action,
        "claim_boundary": "Import compatibility is a data-handoff check only. It does not convert raw results into validated scores.",
    }


def create_benchmark_session(
    profile: dict[str, Any],
    component_results: list[dict[str, Any]],
    *,
    benchmark_path: str | None = None,
    session_date: str | None = None,
    protocol_version: str | None = None,
    global_notes: str = "",
) -> dict[str, Any]:
    """Create a user-owned benchmark session record."""

    equipment_access = list(profile.get("equipment_access", []) or [])
    benchmark = get_hybrid_benchmark(equipment_access)
    path = benchmark_path or benchmark["path"]
    spec = benchmark["spec"]
    component_lookup = _component_map(path, equipment_access)

    normalized_results = []
    for result in component_results:
        component_id = result["component_id"]
        component = component_lookup.get(component_id, {"area": "unknown", "test": component_id, "fields": []})
        normalized_results.append(
            {
                **build_component_result(
                    component_id,
                    value=result.get("value"),
                    value_unit=result.get("value_unit", ""),
                    rpe_0_10=result.get("rpe_0_10"),
                    equipment=result.get("equipment", []),
                    substitution=result.get("substitution"),
                    result_fields=result.get("result_fields", {}),
                    completed=result.get("completed", True),
                    notes=result.get("notes", ""),
                ),
                "area": component.get("area", "unknown"),
                "test": component.get("test", component_id),
            }
        )

    completed = [item for item in normalized_results if item["completed"] and item["value"] is not None]
    quality = evaluate_benchmark_session_quality(normalized_results, equipment_access)
    import_compatibility = build_benchmark_import_compatibility(normalized_results)
    return {
        "schema": "sportrx.benchmark_session",
        "schema_version": SCHEMA_VERSION,
        "session_id": f"bench_{uuid4().hex[:12]}",
        "date": session_date or date.today().isoformat(),
        "event_profile": "HYROX / Hybrid Race",
        "benchmark_name": spec["name"],
        "benchmark_path": path,
        "protocol_version": protocol_version or spec["version"],
        "evidence_status": spec["evidence_status"],
        "safety_gate_status": profile.get("safety_gate_status"),
        "profile_snapshot": {
            "age": profile.get("age"),
            "training_days": profile.get("training_days"),
            "weekly_training_minutes": profile.get("weekly_training_minutes", profile.get("mvpa_minutes_per_week")),
            "running_minutes_per_week": profile.get("running_minutes_per_week"),
            "strength_days_per_week": profile.get("strength_days_per_week"),
            "equipment_access": equipment_access,
        },
        "component_results": normalized_results,
        "completion": {
            "completed_components": len(completed),
            "total_recorded_components": len(normalized_results),
            "status": "recorded" if completed else "no_completed_measurements",
        },
        "session_quality": quality,
        "import_compatibility": import_compatibility,
        "notes": global_notes.strip(),
        "claim_boundary": "Raw benchmark log only. Not a validated score, percentile, race prediction, or medical clearance.",
    }


def summarize_benchmark_sessions(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize local benchmark logs for the current user."""

    if not sessions:
        return {
            "session_count": 0,
            "latest_date": None,
            "measured_components": [],
            "retest_ready": False,
            "message": "No benchmark sessions recorded yet.",
        }

    latest = sessions[-1]
    measured_components = sorted(
        {
            result["component_id"]
            for session in sessions
            for result in session.get("component_results", [])
            if result.get("completed") and result.get("value") is not None
        }
    )
    return {
        "session_count": len(sessions),
        "latest_date": latest.get("date"),
        "measured_components": measured_components,
        "retest_ready": len(sessions) >= 2,
        "message": "Retest comparison available." if len(sessions) >= 2 else "Record a later retest using the same protocol.",
    }


def _latest_completed_results(sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest_by_component: dict[str, dict[str, Any]] = {}
    for session in sessions:
        for result in session.get("component_results", []):
            if result.get("completed") and result.get("value") is not None:
                latest_by_component[result["component_id"]] = {
                    **result,
                    "session_date": session.get("date"),
                    "benchmark_name": session.get("benchmark_name"),
                    "benchmark_path": session.get("benchmark_path"),
                    "protocol_version": session.get("protocol_version"),
                    "session_id": session.get("session_id"),
                }
    return list(latest_by_component.values())


def benchmark_profile_patch(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    """Map compatible benchmark logs into HYROX Check profile inputs.

    Only direct, unit-compatible mappings are used. Raw benchmark values that do
    not match an existing HYROX Check field stay in the log instead of being
    converted into artificial scores.
    """

    patch: dict[str, Any] = {}
    applied: list[str] = []
    skipped: list[str] = []

    for result in _latest_completed_results(sessions):
        value = result.get("value")
        protocol_source = _profile_patch_protocol_source(result)
        mapping = _hyrox_import_mapping(result)

        if mapping["status"] != "importable":
            skipped.append(mapping["reason"])
            continue

        target_fields = mapping["target_fields"]
        if "one_km_run_seconds" in target_fields:
            patch["one_km_run_seconds"] = int(value)
            applied.append(f"1 km run -> one_km_run_seconds ({protocol_source})")
        elif "one_km_row_seconds" in target_fields:
            patch["one_km_row_seconds"] = int(value)
            applied.append(f"1 km row -> one_km_row_seconds ({protocol_source})")
        elif "one_km_ski_seconds" in target_fields:
            patch["one_km_ski_seconds"] = int(value)
            applied.append(f"1 km ski -> one_km_ski_seconds ({protocol_source})")
        elif "station_test_score" in target_fields:
            patch["station_test_score"] = int(max(0, min(float(value), 100)))
            patch["station_test_protocol"] = protocol_source
            applied.append(f"station circuit score -> station_test_score + station_test_protocol ({protocol_source})")

    return {
        "profile_patch": patch,
        "applied": applied,
        "skipped": skipped,
        "claim_boundary": "Only unit-compatible raw measurements are imported. No benchmark value is converted into a validated score.",
    }


def _profile_patch_protocol_source(result: dict[str, Any]) -> str:
    name = result.get("benchmark_name") or "SportRx Hybrid Benchmark"
    version = result.get("protocol_version") or "unknown protocol"
    path = result.get("benchmark_path") or "unknown path"
    date_label = result.get("session_date") or "unknown date"
    return f"{name} {version} / {path} / Benchmark Log {date_label}"


def compare_retest_sessions(sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Compare earliest and latest completed values for repeated components."""

    by_component: dict[str, list[dict[str, Any]]] = {}
    for session in sessions:
        for result in session.get("component_results", []):
            if result.get("completed") and result.get("value") is not None:
                by_component.setdefault(result["component_id"], []).append({**result, "date": session.get("date")})

    comparisons = []
    for component_id, results in sorted(by_component.items()):
        if len(results) < 2:
            continue
        first = results[0]
        latest = results[-1]
        delta = float(latest["value"]) - float(first["value"])
        unit = latest.get("value_unit") or first.get("value_unit") or ""
        lower_is_better = unit == "seconds"
        improved = delta < 0 if lower_is_better else delta > 0
        comparisons.append(
            {
                "component_id": component_id,
                "test": latest.get("test", component_id),
                "first_date": first.get("date"),
                "latest_date": latest.get("date"),
                "first_value": first.get("value"),
                "latest_value": latest.get("value"),
                "value_unit": unit,
                "delta": round(delta, 2),
                "direction": "improved" if improved else "not_improved_or_unclear",
                "claim_boundary": "Retest comparison only; not a prediction or validated minimal detectable change.",
            }
        )
    return comparisons


def export_sessions_json(sessions: list[dict[str, Any]]) -> str:
    """Export sessions as stable, readable JSON."""

    return json.dumps(
        {
            "schema": "sportrx.benchmark_log_export",
            "schema_version": SCHEMA_VERSION,
            "sessions": sessions,
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


def export_sessions_csv(sessions: list[dict[str, Any]]) -> str:
    """Flatten benchmark component results to CSV."""

    output = io.StringIO()
    fieldnames = [
        "session_id",
        "date",
        "benchmark_path",
        "protocol_version",
        "component_id",
        "area",
        "test",
        "completed",
        "value",
        "value_unit",
        "rpe_0_10",
        "equipment",
        "substitution",
        "notes",
        "result_fields",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for session in sessions:
        for result in session.get("component_results", []):
            writer.writerow(
                {
                    "session_id": session.get("session_id"),
                    "date": session.get("date"),
                    "benchmark_path": session.get("benchmark_path"),
                    "protocol_version": session.get("protocol_version"),
                    "component_id": result.get("component_id"),
                    "area": result.get("area"),
                    "test": result.get("test"),
                    "completed": result.get("completed"),
                    "value": result.get("value"),
                    "value_unit": result.get("value_unit"),
                    "rpe_0_10": result.get("rpe_0_10"),
                    "equipment": "|".join(result.get("equipment", [])),
                    "substitution": result.get("substitution") or "",
                    "notes": result.get("notes") or "",
                    "result_fields": json.dumps(result.get("result_fields", {}), ensure_ascii=False, sort_keys=True),
                }
            )
    return output.getvalue()
