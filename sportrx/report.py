"""Report objects for SportRx training profile pages.

Reports organize measured information for users and coaches. They do not add
new scoring, predictions, percentiles, or medical clearance.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from .output_prerequisites import build_output_prerequisites
from .safety_gate import automated_handoff_allowed

CLAIM_BOUNDARY = (
    "SportRx reports summarize current measured and reported information only. "
    "They are not medical clearance, race prediction, injury-risk estimates, "
    "validated percentiles, or proof of future performance."
)


def _status_label(passport: dict[str, Any]) -> str:
    if not automated_handoff_allowed(passport["safety_gate"]):
        return "Training handoff blocked"
    if not passport["starter_path"]["available"]:
        return "Benchmark needed before tailored training"
    return "Starter Path available"


def _performance_rows(passport: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for key, item in passport.get("performance_profile", {}).items():
        rows.append(
            {
                "dimension_id": key,
                "label": item["label"],
                "status": item["status"],
                "score": item["score"],
                "source": item["source"],
                "evidence": item["evidence"],
                "missing": item["missing"],
            }
        )
    return rows


def build_training_profile_report(
    passport: dict[str, Any],
    benchmark_summary: dict[str, Any] | None = None,
    feedback_dashboard: dict[str, Any] | None = None,
    *,
    report_date: str | None = None,
) -> dict[str, Any]:
    """Build a user-facing report object from a passport result."""

    benchmark_summary = benchmark_summary or {
        "session_count": 0,
        "latest_date": None,
        "measured_components": [],
        "retest_ready": False,
        "message": "No benchmark sessions recorded yet.",
    }
    return {
        "schema": "sportrx.training_profile_report",
        "schema_version": "0.1",
        "report_date": report_date or date.today().isoformat(),
        "title": "SportRx Training Profile Report",
        "event_profile": passport["event_profile_match"],
        "status_label": _status_label(passport),
        "current_measured_picture": passport["current_measured_picture"],
        "training_profile": passport["training_profile"],
        "safety_gate": passport["safety_gate"],
        "measurement": {
            "areas_assessed": passport["areas_assessed"],
            "measured_performance_areas": passport["measured_performance_areas"],
            "benchmark_sessions": benchmark_summary,
            "lab_test_quality": passport.get("lab_test_quality", {}),
        },
        "performance_rows": _performance_rows(passport),
        "metric_sources": passport.get("metric_sources", {}),
        "output_prerequisites": build_output_prerequisites(passport, benchmark_summary, feedback_dashboard),
        "strongest_area": passport["strongest_area"],
        "main_gap": passport["main_gap"],
        "starter_path_status": {
            "available": passport["starter_path"]["available"],
            "reason": passport["starter_path"].get("reason"),
            "based_on_gap": passport["starter_path"].get("based_on_gap"),
        },
        "next_action": passport["next_action"],
        "priorities": passport["top_3_priorities"],
        "known": passport["what_we_know"],
        "unknown": passport["what_we_do_not_know"],
        "measure_next": passport["what_to_measure_next"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(report: dict[str, Any]) -> str:
    """Export the report object as plain markdown."""

    lines = [
        f"# {report['title']}",
        "",
        f"- Date: {report['report_date']}",
        f"- Event profile: {report['event_profile']}",
        f"- Status: {report['status_label']}",
        f"- Training profile: {report['training_profile']}",
        f"- Current measured picture: {report['current_measured_picture']}",
        f"- Safety Gate: {report['safety_gate']['status']}",
        "",
        "## Measurement",
        f"- Areas assessed: {report['measurement']['areas_assessed']['label']}",
        f"- Measured performance areas: {report['measurement']['measured_performance_areas']['label']}",
        f"- Benchmark sessions: {report['measurement']['benchmark_sessions']['session_count']}",
        f"- Lab test quality: {report['measurement'].get('lab_test_quality', {}).get('status', 'not_reviewed')}",
        "",
        "## Performance Profile",
    ]
    for row in report["performance_rows"]:
        score = "Not tested" if row["score"] is None else row["score"]
        lines.append(f"- {row['label']}: {row['status']} ({score}; source: {row['source']})")

    metric_sources = report.get("metric_sources", {})
    if metric_sources:
        lines.extend(["", "## Metric Sources"])
        for item in metric_sources.get("all_metrics", []):
            affects = "affects output" if item["affects_output"] else "does not affect output"
            lines.append(f"- {item['label']}: {item['source_label']} ({affects})")

    output_prerequisites = report.get("output_prerequisites", {})
    if output_prerequisites:
        lines.extend(["", "## Output Prerequisites"])
        for item in output_prerequisites.get("outputs", []):
            missing = "; ".join(item["missing"]) if item["missing"] else "none"
            lines.append(f"- {item['label']}: {item['status']} (missing: {missing})")

    lines.extend(
        [
            "",
            "## Interpretation Boundary",
            f"- Strongest area: {report['strongest_area']}",
            f"- Main gap: {report['main_gap']}",
            f"- Next action: {report['next_action']}",
            "",
            "## Priorities",
        ]
    )
    for item in report["priorities"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Known"])
    for item in report["known"] or ["No measured or reported information available."]:
        lines.append(f"- {item}")

    lines.extend(["", "## Unknown"])
    for item in report["unknown"] or ["No major unknown items listed."]:
        lines.append(f"- {item}")

    lines.extend(["", "## Measure Next"])
    for item in report["measure_next"] or ["Retest the same benchmark when appropriate."]:
        lines.append(f"- {item}")

    lines.extend(["", "## Claim Boundary", report["claim_boundary"]])
    return "\n".join(lines) + "\n"
