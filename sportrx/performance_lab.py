"""Hybrid Race Check for SportRx 2.1.

This module keeps measured and reported information separate from unknown
information. Missing tests stay missing; no midpoint score is assigned to an
untested capacity.
"""

from __future__ import annotations

import csv
from io import StringIO
from typing import Any

from .metric_sources import build_metric_source_register
from .safety_gate import automated_handoff_allowed, benchmark_allowed, evaluate_safety_gate


PERFORMANCE_DIMENSIONS = {
    "running_capacity": "Running",
    "aerobic_base": "Aerobic fitness",
    "strength_endurance": "Strength endurance",
    "station_experience": "Station experience",
    "work_capacity": "Work capacity",
}


LAB_TEST_FIELDS = [
    {
        "field_id": "one_km_run_seconds",
        "label": "1 km run",
        "unit": "seconds",
        "dimension": "Running",
        "protocol_role": "Measured running capacity input.",
    },
    {
        "field_id": "five_km_run_seconds",
        "label": "5 km run",
        "unit": "seconds",
        "dimension": "Running",
        "protocol_role": "Measured running capacity input.",
    },
    {
        "field_id": "one_km_row_seconds",
        "label": "1 km RowErg",
        "unit": "seconds",
        "dimension": "Station experience",
        "protocol_role": "Measured station-specific erg input.",
    },
    {
        "field_id": "one_km_ski_seconds",
        "label": "1 km SkiErg",
        "unit": "seconds",
        "dimension": "Station experience",
        "protocol_role": "Measured station-specific erg input.",
    },
    {
        "field_id": "station_test_score",
        "label": "Station circuit",
        "unit": "score",
        "dimension": "Strength endurance / Station experience",
        "protocol_role": "Protocol-derived station or strength-endurance input; source must be recorded.",
        "protocol_source_field": "station_test_protocol",
    },
    {
        "field_id": "work_capacity_test_score",
        "label": "Work capacity",
        "unit": "score",
        "dimension": "Work capacity",
        "protocol_role": "Protocol-derived compromised or mixed-work capacity input; source must be recorded.",
        "protocol_source_field": "work_capacity_test_protocol",
    },
]


LAB_CONTEXT_FIELDS = [
    {
        "field_id": "training_days",
        "label": "Training days",
        "unit": "days/week",
        "role": "Training context; not used for measured strongest-area versus main-gap comparison.",
    },
    {
        "field_id": "weekly_training_minutes",
        "label": "Weekly training volume",
        "unit": "minutes/week",
        "role": "Training context and aerobic-base estimate; not treated as a performance test.",
    },
    {
        "field_id": "running_minutes_per_week",
        "label": "Running volume",
        "unit": "minutes/week",
        "role": "Training context and aerobic-base estimate; not treated as a performance test.",
    },
    {
        "field_id": "strength_days_per_week",
        "label": "Strength training frequency",
        "unit": "days/week",
        "role": "Training context; not treated as a measured strength-endurance result.",
    },
    {
        "field_id": "available_days_per_week",
        "label": "Available training days",
        "unit": "days/week",
        "role": "Prescription constraint; not a performance advantage.",
    },
    {
        "field_id": "max_minutes_per_session",
        "label": "Maximum session length",
        "unit": "minutes/session",
        "role": "Prescription constraint; not a performance advantage.",
    },
]


def _ratio(value: float, target: float) -> float:
    if target <= 0:
        return 1.0
    return max(0.0, min(value / target, 1.0))


def _pace_score(seconds: float | None, excellent: float, starter: float) -> float | None:
    if seconds is None or seconds <= 0:
        return None
    if seconds <= excellent:
        return 100.0
    if seconds >= starter:
        return 35.0
    return 35.0 + (starter - seconds) / (starter - excellent) * 65.0


def _category(score: float | None) -> str:
    if score is None:
        return "Not tested"
    if score >= 82:
        return "Strong current area"
    if score >= 66:
        return "Good base"
    if score >= 45:
        return "Developing"
    return "Needs more work"


def _exposure_label(value: Any) -> str:
    if value is None:
        return "Not reported"
    sessions = int(value or 0)
    if sessions >= 4:
        return f"{sessions} sessions in last 4 weeks"
    if sessions > 0:
        return f"{sessions} session(s) in last 4 weeks"
    return "0 sessions in last 4 weeks"


def _completion(dimensions: dict[str, dict[str, Any]]) -> dict[str, Any]:
    assessed = sum(1 for item in dimensions.values() if item["score"] is not None)
    total = len(dimensions)
    if assessed >= 5:
        level = "HIGH"
    elif assessed >= 3:
        level = "MODERATE"
    else:
        level = "LOW"
    return {
        "level": level,
        "assessed": assessed,
        "total": total,
        "label": f"{assessed} of {total} key areas assessed",
    }


def _measured_performance_areas(dimensions: dict[str, dict[str, Any]]) -> dict[str, Any]:
    measured = [
        item["label"]
        for item in dimensions.values()
        if item["score"] is not None and item["source"] == "measured"
    ]
    return {
        "count": len(measured),
        "areas": measured,
        "label": f"{len(measured)} measured performance areas",
    }


def _analyze_measured_dimensions(dimensions: dict[str, dict[str, Any]]) -> dict[str, Any]:
    measured = {key: value["score"] for key, value in dimensions.items() if value["score"] is not None}
    measured_performance = {
        key: value["score"]
        for key, value in dimensions.items()
        if value["score"] is not None and value["source"] == "measured"
    }
    if len(measured_performance) < 2:
        return {
            "strongest_area": "Not enough measured data",
            "main_gap": "Not enough measured data",
            "main_development_areas": [],
            "profile_balance": "At least two measured performance areas are needed for comparison",
        }

    max_score = max(measured_performance.values())
    min_score = min(measured_performance.values())
    strongest = [key for key, score in measured_performance.items() if abs(score - max_score) <= 3]
    weakest = [key for key, score in measured_performance.items() if abs(score - min_score) <= 3]

    if max_score - min_score <= 5:
        return {
            "strongest_area": "Balanced",
            "main_gap": "No single dominant gap identified",
            "main_development_areas": [],
            "profile_balance": "Balanced across measured areas",
        }

    strongest_label = _join_labels([PERFORMANCE_DIMENSIONS[key] for key in strongest])
    weakest_label = _join_labels([PERFORMANCE_DIMENSIONS[key] for key in weakest])
    return {
        "strongest_area": strongest_label,
        "main_gap": weakest_label,
        "main_development_areas": [PERFORMANCE_DIMENSIONS[key] for key in weakest],
        "profile_balance": "Uneven across measured areas",
    }


def _join_labels(labels: list[str]) -> str:
    if not labels:
        return "Not enough data"
    if len(labels) == 1:
        return labels[0]
    return " and ".join(labels)


def _training_profile(dimensions: dict[str, dict[str, Any]], analysis: dict[str, Any]) -> str:
    running = dimensions["running_capacity"]["score"]
    strength = dimensions["strength_endurance"]["score"]
    if analysis["profile_balance"].startswith("Balanced"):
        return "Balanced"
    if running is not None and strength is not None:
        if running - strength >= 10:
            return "Running-dominant"
        if strength - running >= 10:
            return "Strength-dominant"
    if dimensions["work_capacity"]["score"] is not None and dimensions["work_capacity"]["score"] >= 75:
        return "Work-capacity dominant"
    return "Still being mapped"


def _readiness_category(score: float | None, safety_status: str, assessed_areas: int) -> str:
    if safety_status == "RED":
        return "Training handoff blocked"
    if score is None or assessed_areas < 3:
        return "Not enough measured data"
    if score >= 82:
        return "Strong current profile"
    if score >= 66:
        return "Well prepared"
    if score >= 45:
        return "Building"
    return "Early stage"


def _dimension(
    label: str,
    score: float | None,
    evidence: list[str],
    missing: list[str],
    source: str,
) -> dict[str, Any]:
    return {
        "label": label,
        "score": None if score is None else round(score),
        "status": _category(score),
        "evidence": evidence,
        "missing": missing,
        "source": source,
    }


def _has_value(profile: dict[str, Any], key: str) -> bool:
    value = profile.get(key)
    if value is None or value == "":
        return False
    if isinstance(value, (list, tuple, set, dict)) and not value:
        return False
    return True


def _has_protocol_source(profile: dict[str, Any], source_key: str) -> bool:
    return bool(str(profile.get(source_key, "") or "").strip())


def _protocol_score_value(profile: dict[str, Any], value_key: str, source_key: str) -> float | None:
    if not _has_value(profile, value_key) or not _has_protocol_source(profile, source_key):
        return None
    return float(profile.get(value_key))


def build_lab_measurement_review(
    profile: dict[str, Any],
    dimensions: dict[str, dict[str, Any]],
    training_context: dict[str, Any],
    safety_gate: dict[str, Any],
    measured_performance: dict[str, Any],
) -> dict[str, Any]:
    """Explain measured, untested, self-reported, and safety-screened lab inputs."""

    test_fields = []
    for spec in LAB_TEST_FIELDS:
        tested = _has_value(profile, spec["field_id"])
        protocol_source_field = spec.get("protocol_source_field")
        protocol_source = (
            profile.get(protocol_source_field, "")
            if protocol_source_field and tested
            else "standard timed field"
            if tested
            else "Not tested"
        )
        source_ready = not protocol_source_field or not tested or _has_protocol_source(profile, protocol_source_field)
        if tested and source_ready:
            status = "measured"
        elif tested:
            status = "measured_needs_protocol"
        else:
            status = "not_tested"
        test_fields.append(
            {
                **spec,
                "status": status,
                "value": profile.get(spec["field_id"]) if tested else "Not tested",
                "affects_gap_comparison": status == "measured",
                "protocol_source": protocol_source,
            }
        )

    context_fields = []
    for spec in LAB_CONTEXT_FIELDS:
        provided = _has_value(profile, spec["field_id"])
        context_fields.append(
            {
                **spec,
                "status": "self_reported" if provided else "not_collected",
                "value": profile.get(spec["field_id"]) if provided else "Not collected",
            }
        )

    dimension_fields = [
        {
            "dimension_id": dimension_id,
            "label": item["label"],
            "source": item["source"],
            "status": item["status"],
            "value": "Not tested" if item["score"] is None else item["score"],
            "comparison_role": (
                "eligible_for_gap_comparison"
                if item["source"] == "measured" and item["score"] is not None
                else "context_or_not_tested"
            ),
        }
        for dimension_id, item in dimensions.items()
    ]

    measured_test_count = sum(1 for item in test_fields if item["status"] == "measured")
    needs_protocol_count = sum(1 for item in test_fields if item["status"] == "measured_needs_protocol")
    not_tested_count = sum(1 for item in test_fields if item["status"] == "not_tested")
    measured_area_count = int(measured_performance.get("count", 0) or 0)
    comparison_ready = measured_area_count >= 2
    safety_status = safety_gate.get("status", "UNKNOWN")
    if not automated_handoff_allowed(safety_gate):
        next_action = "Resolve Safety Gate before automated training handoff."
        gate_status = "blocked"
    elif not comparison_ready:
        next_action = "Complete at least two measured performance dimensions before comparing strongest area and main gap."
        gate_status = "waiting"
    else:
        next_action = "Comparison gate is open; keep protocol and units repeatable for retest."
        gate_status = "ready"

    cards = [
        {
            "id": "measured_tests",
            "label": "Measured Tests",
            "value": f"{measured_test_count} / {len(LAB_TEST_FIELDS)}",
            "detail": "Only completed tests with required protocol source are counted; blanks remain Not tested.",
            "status": "ready" if measured_test_count else "waiting",
        },
        {
            "id": "measured_areas",
            "label": "Measured Areas",
            "value": measured_performance.get("label", f"{measured_area_count} measured performance areas"),
            "detail": "At least two measured performance areas are needed for strongest/gap comparison.",
            "status": "ready" if comparison_ready else "waiting",
        },
        {
            "id": "not_tested",
            "label": "Not Tested",
            "value": str(not_tested_count),
            "detail": "Missing tests are not replaced by average, midpoint, or fake benchmark values.",
            "status": "ready" if not_tested_count == 0 else "waiting",
        },
        {
            "id": "self_reported_context",
            "label": "Self-reported Context",
            "value": f"{sum(1 for item in context_fields if item['status'] == 'self_reported')} fields",
            "detail": "Context can shape feasibility and aerobic-base context; it is not measured performance.",
            "status": "ready",
        },
        {
            "id": "safety_boundary",
            "label": "Safety Boundary",
            "value": safety_status,
            "detail": "Safety can block handoff, but never raises or lowers measured performance.",
            "status": "blocked" if not automated_handoff_allowed(safety_gate) else "ready",
        },
    ]

    return {
        "schema": "sportrx.lab_measurement_review",
        "schema_version": "0.1",
        "status": gate_status,
        "next_action": next_action,
        "measured_test_count": measured_test_count,
        "needs_protocol_test_count": needs_protocol_count,
        "not_tested_test_count": not_tested_count,
        "measured_performance_area_count": measured_area_count,
        "comparison_ready": comparison_ready,
        "test_fields": test_fields,
        "context_fields": context_fields,
        "dimension_fields": dimension_fields,
        "cards": cards,
        "claim_boundary": (
            "Lab Measurement Review documents input provenance and measurement gates only. "
            "It does not validate SportRx, predict outcomes, estimate injury risk, or provide medical clearance."
        ),
    }


def build_lab_test_quality(
    profile: dict[str, Any],
    measurement_review: dict[str, Any],
    safety_gate: dict[str, Any],
) -> dict[str, Any]:
    """Check whether measured lab inputs have enough protocol provenance."""

    measured_tests = [item for item in measurement_review["test_fields"] if item["status"] == "measured"]
    needs_protocol_tests = [
        item for item in measurement_review["test_fields"] if item["status"] == "measured_needs_protocol"
    ]
    entered_tests = measured_tests + needs_protocol_tests
    timed_tests = [
        item
        for item in measured_tests
        if item["field_id"] in {"one_km_run_seconds", "five_km_run_seconds", "one_km_row_seconds", "one_km_ski_seconds"}
    ]
    protocol_score_tests = [
        item
        for item in entered_tests
        if item["field_id"] in {"station_test_score", "work_capacity_test_score"}
    ]
    missing_protocol_sources = [
        item["field_id"]
        for item in needs_protocol_tests
        if item["field_id"] in {"station_test_score", "work_capacity_test_score"}
    ]
    comparison_ready = bool(measurement_review.get("comparison_ready"))

    if not benchmark_allowed(safety_gate):
        status = "blocked_by_safety_gate"
        next_action = "Resolve Safety Gate before interpreting lab test quality."
    elif not entered_tests:
        status = "waiting_for_measured_tests"
        next_action = "Complete at least one SportRx Hybrid Benchmark component before interpreting lab quality."
    elif missing_protocol_sources:
        status = "needs_protocol_source"
        next_action = "Add protocol source for station or work-capacity score fields before treating them as review-ready."
    elif not comparison_ready:
        status = "needs_more_measured_areas"
        next_action = "Record at least two measured performance areas before strongest-area and main-gap comparison."
    else:
        status = "review_ready_measurement_record"
        next_action = "Keep units, protocol source, and test order stable for retest comparison."

    return {
        "schema": "sportrx.lab_test_quality",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "measured_test_count": len(measured_tests),
        "needs_protocol_test_count": len(needs_protocol_tests),
        "timed_test_count": len(timed_tests),
        "protocol_score_test_count": len(protocol_score_tests),
        "missing_protocol_sources": missing_protocol_sources,
        "comparison_ready": comparison_ready,
        "cards": [
            {
                "id": "timed_tests",
                "label": "Timed Tests",
                "value": f"{len(timed_tests)} fields",
                "detail": "Run, RowErg, and SkiErg entries are raw timed fields.",
                "status": "ready" if timed_tests else "waiting",
            },
            {
                "id": "protocol_scores",
                "label": "Protocol Scores",
                "value": f"{len(protocol_score_tests)} fields",
                "detail": "Station and work-capacity scores must come from a named protocol or Benchmark Log.",
                "status": "ready" if protocol_score_tests and not missing_protocol_sources else "waiting",
            },
            {
                "id": "protocol_sources",
                "label": "Protocol Sources",
                "value": "Complete" if not missing_protocol_sources else f"{len(missing_protocol_sources)} missing",
                "detail": "Protocol provenance is required before protocol scores affect measured performance.",
                "status": "ready" if not missing_protocol_sources else "waiting",
            },
            {
                "id": "comparison_gate",
                "label": "Comparison Gate",
                "value": "Open" if comparison_ready else "Waiting",
                "detail": "At least two measured performance areas are required before comparing strongest area and main gap.",
                "status": "ready" if comparison_ready else "waiting",
            },
            {
                "id": "safety_boundary",
                "label": "Safety Boundary",
                "value": safety_gate.get("status", "UNKNOWN"),
                "detail": "Safety can block interpretation, but never raises or lowers measured performance.",
                "status": "blocked" if not benchmark_allowed(safety_gate) else "ready",
            },
        ],
        "claim_boundary": (
            "Lab Test Quality checks protocol provenance and interpretation readiness only. "
            "It does not create validation, convert raw results into scores, or provide medical clearance."
        ),
    }


def build_measurement_intake_matrix(
    measurement_review: dict[str, Any],
    lab_test_quality: dict[str, Any],
) -> dict[str, Any]:
    """Build a lab-style matrix of measured and not-tested inputs."""

    rows = []
    protocol_missing = set(lab_test_quality.get("missing_protocol_sources", []))
    for item in measurement_review["test_fields"]:
        field_id = item["field_id"]
        measured = item["status"] in {"measured", "measured_needs_protocol"}
        is_protocol_score = field_id in {"station_test_score", "work_capacity_test_score"}
        if not measured:
            intake_status = "not_tested"
            source_status = "not_applicable"
            next_step = "Run this component through SportRx Hybrid Benchmark v1 or save it in Benchmark Log."
        elif field_id in protocol_missing:
            intake_status = "measured_needs_protocol"
            source_status = "missing_protocol_source"
            next_step = "Add the protocol source before treating this record as review-ready."
        else:
            intake_status = "measured_review_ready"
            source_status = "protocol_recorded" if is_protocol_score else "raw_timed_field"
            next_step = "Keep the same unit, setup, and protocol for retest."

        rows.append(
            {
                "field_id": field_id,
                "test": item["label"],
                "dimension": item["dimension"],
                "status": intake_status,
                "value": item["value"],
                "unit": item["unit"],
                "data_kind": "protocol_score" if is_protocol_score else "raw_timed_field",
                "source_status": source_status,
                "protocol_source": item.get("protocol_source", ""),
                "counts_for_gap_comparison": bool(item["affects_gap_comparison"]),
                "next_step": next_step,
            }
        )

    measured_rows = [row for row in rows if row["status"] != "not_tested"]
    not_tested_rows = [row for row in rows if row["status"] == "not_tested"]
    review_ready_rows = [row for row in rows if row["status"] == "measured_review_ready"]
    missing_protocol_rows = [row for row in rows if row["status"] == "measured_needs_protocol"]
    comparison_ready = bool(measurement_review.get("comparison_ready"))

    if lab_test_quality.get("status") == "blocked_by_safety_gate":
        status = "blocked_by_safety_gate"
        next_action = "Resolve Safety Gate before training handoff; measured values remain unchanged."
    elif missing_protocol_rows:
        status = "needs_protocol_source"
        next_action = "Add protocol source for Station circuit or Work capacity before review handoff."
    elif not comparison_ready:
        status = "needs_more_measured_dimensions"
        next_action = "Measure at least two performance dimensions before comparing strongest area and main gap."
    else:
        status = "measurement_matrix_ready"
        next_action = "Use the matrix for Training Profile handoff and keep the same protocol for retest."

    return {
        "schema": "sportrx.measurement_intake_matrix",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "rows": rows,
        "summary": {
            "measured": len(measured_rows),
            "not_tested": len(not_tested_rows),
            "review_ready": len(review_ready_rows),
            "missing_protocol_source": len(missing_protocol_rows),
            "total": len(rows),
            "comparison_ready": comparison_ready,
        },
        "claim_boundary": (
            "Measurement Intake Matrix displays input status and provenance only. "
            "It does not create scores, validate cutoffs, predict outcomes, or provide medical clearance."
        ),
    }


def measurement_intake_matrix_markdown(matrix: dict[str, Any]) -> str:
    """Export Measurement Intake Matrix as Markdown."""

    summary = matrix["summary"]
    lines = [
        "# SportRx Measurement Intake Matrix",
        "",
        f"- Status: {matrix['status']}",
        f"- Measured: {summary['measured']} / {summary['total']}",
        f"- Not tested: {summary['not_tested']}",
        f"- Review ready: {summary['review_ready']}",
        f"- Missing protocol source: {summary['missing_protocol_source']}",
        f"- Comparison ready: {summary['comparison_ready']}",
        f"- Next action: {matrix['next_action']}",
        f"- Claim boundary: {matrix['claim_boundary']}",
        "",
        "## Components",
        "",
        "| Test | Dimension | Status | Value | Unit | Data kind | Source status | Gap comparison | Next step |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in matrix["rows"]:
        gap = "yes" if row["counts_for_gap_comparison"] else "no"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["test"]),
                    str(row["dimension"]),
                    str(row["status"]),
                    str(row["value"]),
                    str(row["unit"]),
                    str(row["data_kind"]),
                    str(row["source_status"]),
                    gap,
                    str(row["next_step"]),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def measurement_intake_matrix_csv(matrix: dict[str, Any]) -> str:
    """Export Measurement Intake Matrix rows as CSV."""

    output = StringIO()
    fieldnames = [
        "field_id",
        "test",
        "dimension",
        "status",
        "value",
        "unit",
        "data_kind",
        "source_status",
        "protocol_source",
        "counts_for_gap_comparison",
        "next_step",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in matrix["rows"]:
        writer.writerow({field: row.get(field, "") for field in fieldnames})
    return output.getvalue()


def assess_hybrid_performance(profile: dict[str, Any]) -> dict[str, Any]:
    """Assess current Hybrid Race profile without inventing missing data."""

    safety_gate = evaluate_safety_gate({**profile, "primary_goal": "hybrid_race", "intended_intensity": "high"})
    weekly_minutes = profile.get("weekly_training_minutes", profile.get("mvpa_minutes_per_week"))
    training_days = profile.get("training_days", profile.get("exercise_days_last_4w"))
    running_minutes = profile.get("running_minutes_per_week")
    strength_days = profile.get("strength_days_per_week")
    available_days = int(profile.get("available_days_per_week", 3) or 3)
    max_minutes = int(profile.get("max_minutes_per_session", 30) or 30)

    run_tests = [
        ("1 km run", _pace_score(profile.get("one_km_run_seconds"), excellent=240, starter=420)),
        ("5 km run", _pace_score(profile.get("five_km_run_seconds"), excellent=1500, starter=2400)),
    ]
    measured_run = [(name, score) for name, score in run_tests if score is not None]
    running_score = None
    if measured_run:
        running_score = sum(score for _, score in measured_run) / len(measured_run)

    aerobic_score = None
    aerobic_evidence: list[str] = []
    if weekly_minutes is not None or training_days is not None or running_minutes is not None:
        minutes = float(weekly_minutes or 0)
        days = float(training_days or 0)
        run_minutes = float(running_minutes or 0)
        aerobic_score = _ratio(minutes, 180) * 45 + _ratio(days, 4) * 25 + _ratio(run_minutes, 90) * 30
        if weekly_minutes is not None:
            aerobic_evidence.append(f"{int(minutes)} min/week reported training")
        if training_days is not None:
            aerobic_evidence.append(f"{int(days)} training days/week")
        if running_minutes is not None:
            aerobic_evidence.append(f"{int(run_minutes)} running min/week")

    strength_score = _protocol_score_value(profile, "station_test_score", "station_test_protocol")

    row_score = _pace_score(profile.get("one_km_row_seconds"), excellent=225, starter=360)
    ski_score = _pace_score(profile.get("one_km_ski_seconds"), excellent=240, starter=390)
    station_scores = [score for score in [row_score, ski_score, strength_score] if score is not None]
    station_score = sum(station_scores) / len(station_scores) if station_scores else None

    work_capacity_score = _protocol_score_value(profile, "work_capacity_test_score", "work_capacity_test_protocol")
    if work_capacity_score is None:
        work_capacity_score = profile.get("compromised_run_score")
    work_capacity_score = float(work_capacity_score) if work_capacity_score is not None else None

    dimensions = {
        "running_capacity": _dimension(
            "Running",
            running_score,
            [f"{name} completed" for name, _ in measured_run],
            [] if measured_run else ["No recent 1 km or 5 km run test"],
            "measured" if measured_run else "missing",
        ),
        "aerobic_base": _dimension(
            "Aerobic fitness",
            aerobic_score,
            aerobic_evidence,
            [] if aerobic_score is not None else ["No weekly training volume or running volume reported"],
            "reported_training" if aerobic_score is not None else "missing",
        ),
        "strength_endurance": _dimension(
            "Strength endurance",
            strength_score,
            ["Station or strength-endurance test completed"] if strength_score is not None else [],
            [] if strength_score is not None else ["No station or strength-endurance test"],
            "measured" if strength_score is not None else "missing",
        ),
        "station_experience": _dimension(
            "Station experience",
            station_score,
            _station_evidence(row_score, ski_score, strength_score),
            [] if station_score is not None else ["No RowErg, SkiErg, or station-specific test"],
            "measured" if station_score is not None else "missing",
        ),
        "work_capacity": _dimension(
            "Work capacity",
            work_capacity_score,
            ["Compromised or mixed-work test completed"] if work_capacity_score is not None else [],
            [] if work_capacity_score is not None else ["No compromised running or mixed-work test"],
            "measured" if work_capacity_score is not None else "missing",
        ),
    }

    completeness = _completion(dimensions)
    measured_performance = _measured_performance_areas(dimensions)
    analysis = _analyze_measured_dimensions(dimensions)
    measured_scores = [item["score"] for item in dimensions.values() if item["score"] is not None]
    readiness_score = round(sum(measured_scores) / len(measured_scores)) if measured_scores else None

    training_context = {
        "days_available_per_week": available_days,
        "minutes_available_per_session": max_minutes,
        "equipment_access": profile.get("equipment_access", []),
        "recent_training_consistency": None if training_days is None else f"{int(training_days)} days/week",
        "weekly_training_volume": None if weekly_minutes is None else f"{int(weekly_minutes)} min/week",
        "resistance_training_history": None if strength_days is None else f"{int(strength_days)} days/week",
        "high_intensity_exposure": _exposure_label(profile.get("high_intensity_sessions_last_4w")),
        "loaded_movement_exposure": _exposure_label(profile.get("loaded_movement_sessions_last_4w")),
    }

    what_we_know = _what_we_know(dimensions, training_context)
    what_we_do_not_know = _what_we_do_not_know(dimensions)
    what_to_measure_next = _what_to_measure_next(dimensions)
    metric_sources = build_metric_source_register(profile, dimensions, training_context, safety_gate)
    measurement_review = build_lab_measurement_review(profile, dimensions, training_context, safety_gate, measured_performance)
    lab_test_quality = build_lab_test_quality(profile, measurement_review, safety_gate)
    measurement_intake_matrix = build_measurement_intake_matrix(measurement_review, lab_test_quality)

    training_profile = _training_profile(dimensions, analysis)
    return {
        "event_pack": "hybrid_race",
        "event_profile": "Hybrid Race",
        "title": "Hybrid Race Check",
        "safety_gate": safety_gate,
        "assessment_completeness": completeness["level"],
        "areas_assessed": completeness,
        "measured_performance_areas": measured_performance,
        "readiness_score": readiness_score,
        "current_measured_picture": _readiness_category(readiness_score, safety_gate["status"], completeness["assessed"]),
        "readiness_category": _readiness_category(readiness_score, safety_gate["status"], completeness["assessed"]),
        "training_profile": training_profile,
        "athlete_type": training_profile,
        "training_profile_note": "This describes your current training profile, not your innate potential.",
        "performance_profile": dimensions,
        "dimension_scores": {key: value["score"] for key, value in dimensions.items()},
        "training_context": training_context,
        "metric_sources": metric_sources,
        "measurement_review": measurement_review,
        "lab_test_quality": lab_test_quality,
        "measurement_intake_matrix": measurement_intake_matrix,
        "strongest_area": analysis["strongest_area"],
        "main_gap": analysis["main_gap"],
        "main_development_areas": analysis["main_development_areas"],
        "profile_balance": analysis["profile_balance"],
        "strongest_capability": analysis["strongest_area"],
        "primary_limiter": analysis["main_gap"],
        "top_3_priorities": _priorities(analysis["main_development_areas"], safety_gate["status"]),
        "what_we_know": what_we_know,
        "what_we_do_not_know": what_we_do_not_know,
        "what_to_measure_next": what_to_measure_next,
        "goal": profile.get("primary_goal", "understand profile"),
        "evidence_status": {
            "safety_gate": "evidence_backed",
            "dimension_rules": "expert_informed",
            "readiness_category": "experimental",
            "benchmark_cutoffs": "not_validated",
        },
        "note": "Tests completed reflects input completeness, not predictive confidence.",
    }


def _station_evidence(row_score: float | None, ski_score: float | None, station_score: float | None) -> list[str]:
    evidence = []
    if row_score is not None:
        evidence.append("1 km row completed")
    if ski_score is not None:
        evidence.append("1 km ski completed")
    if station_score is not None:
        evidence.append("Station or strength-endurance test completed")
    return evidence


def _what_we_know(dimensions: dict[str, dict[str, Any]], training_context: dict[str, Any]) -> list[str]:
    known = []
    for item in dimensions.values():
        known.extend(item["evidence"])
    for label, value in [
        ("Training availability", f"{training_context['days_available_per_week']} days/week"),
        ("Session length", f"{training_context['minutes_available_per_session']} min/session"),
        ("Recent training", training_context["weekly_training_volume"]),
        ("Resistance training", training_context["resistance_training_history"]),
    ]:
        if value:
            known.append(f"{label}: {value}")
    return known[:8]


def _what_we_do_not_know(dimensions: dict[str, dict[str, Any]]) -> list[str]:
    unknown = []
    for item in dimensions.values():
        unknown.extend(item["missing"])
    return unknown[:8]


def _what_to_measure_next(dimensions: dict[str, dict[str, Any]]) -> list[str]:
    next_tests = []
    if dimensions["running_capacity"]["score"] is None:
        next_tests.append("1 km or 5 km run benchmark")
    if dimensions["strength_endurance"]["score"] is None:
        next_tests.append("Station strength-endurance circuit")
    if dimensions["station_experience"]["score"] is None:
        next_tests.append("Row/Ski or low-equipment station substitute")
    if dimensions["work_capacity"]["score"] is None:
        next_tests.append("Compromised running or mixed-work test")
    return next_tests[:4]


def _priorities(main_development_areas: list[str], safety_status: str) -> list[str]:
    if safety_status == "RED":
        return [
            "Resolve the safety gate before automated training.",
            "Use professional assessment for exercise participation decisions.",
            "Return to SportRx after the stop flag is clarified.",
        ]
    if not main_development_areas:
        return [
            "Complete the SportRx Hybrid Benchmark.",
            "Keep training consistent for the next 4 weeks.",
            "Retest the same benchmark before changing the focus.",
        ]

    joined = " and ".join(main_development_areas)
    if "Strength endurance" in main_development_areas or "Station experience" in main_development_areas:
        return [
            "Build station-specific strength endurance.",
            "Keep running volume steady while adding circuits.",
            "Retest a station circuit in 4 weeks.",
        ]
    if "Running" in joined or "Aerobic" in joined:
        return [
            "Build repeatable aerobic running volume.",
            "Keep most sessions easy enough to repeat.",
            "Retest 1 km or 5 km in 4 weeks.",
        ]
    if "Work capacity" in main_development_areas:
        return [
            "Add controlled mixed-work intervals.",
            "Avoid stacking hard sessions on consecutive days.",
            "Retest a compromised run or mixed circuit.",
        ]
    return [
        f"Develop {joined.lower()}.",
        "Use a small 4-week block rather than a big jump.",
        "Retest the weakest measured area.",
    ]
