"""Demo scenario matrix for SportRx reviewer guidance.

The matrix compares synthetic app states so reviewers can choose the right
demo path without mistaking sample data for validation evidence.
"""

from __future__ import annotations

from typing import Any

from .demo_scenarios import build_demo_scenario_state, build_demo_scenarios
from .feedback_loop import build_feedback_dashboard
from .passport import build_readiness_passport
from .prescription import generate_prescription


CLAIM_BOUNDARY = (
    "Demo Scenario Matrix compares synthetic product-review states only. It is "
    "not validation data, athlete norms, benchmark percentiles, or evidence that "
    "SportRx improves outcomes."
)


def _recommended_pages(scenario_id: str, starter_available: bool, retest_ready: bool) -> list[str]:
    if scenario_id == "measure_first":
        return ["Workbench", "Quick Match", "Benchmark Protocol", "Export Center"]
    if scenario_id == "benchmark_underway":
        return ["Workbench", "Benchmark Log", "Training Profile", "Benchmark Protocol"]
    if starter_available and retest_ready:
        return ["Workbench", "Training Profile", "训练", "复测", "Export Center", "Release QA"]
    return ["Workbench", "Training Profile", "Export Center"]


def _scenario_row(scenario: dict[str, Any]) -> dict[str, Any]:
    state = build_demo_scenario_state(scenario["id"])
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    dashboard = build_feedback_dashboard(plan, state["feedback_by_week"], state["benchmark_sessions"])
    measured_count = int(passport.get("measured_performance_areas", {}).get("count", 0))
    session_count = len(state["benchmark_sessions"])
    feedback_weeks = len(state["feedback_by_week"])
    retest_ready = bool(dashboard.get("benchmark_summary", {}).get("retest_ready", False))
    starter_available = bool(passport.get("starter_path", {}).get("available", False))

    if session_count > 0 and measured_count < 2:
        product_state = "partial_measurement"
        reviewer_focus = "Raw Benchmark Log, missing components, missing retest, and conservative Training Profile handoff."
    elif measured_count < 2:
        product_state = "measurement_gated"
        reviewer_focus = "Not tested handling, measurement gates, and Benchmark Protocol routing."
    elif not retest_ready:
        product_state = "partial_measurement"
        reviewer_focus = "Raw Benchmark Log, missing retest, and conservative Training Profile handoff."
    else:
        product_state = "complete_review_loop"
        reviewer_focus = "Full measured loop: Training Profile, Starter Path, feedback, retest, export, and QA."

    return {
        "id": scenario["id"],
        "label": scenario["label"],
        "stage": scenario["stage"],
        "best_for": scenario["best_for"],
        "expected_state": scenario["expected_state"],
        "product_state": product_state,
        "measured_area_count": measured_count,
        "benchmark_sessions": session_count,
        "feedback_weeks": feedback_weeks,
        "starter_path_available": starter_available,
        "retest_ready": retest_ready,
        "recommended_pages": _recommended_pages(scenario["id"], starter_available, retest_ready),
        "reviewer_focus": reviewer_focus,
        "claim_boundary": scenario["claim_boundary"],
    }


def build_demo_scenario_matrix() -> dict[str, Any]:
    """Build a side-by-side review matrix for all synthetic demo scenarios."""

    scenarios = build_demo_scenarios()
    rows = [_scenario_row(scenario) for scenario in scenarios]
    ready_rows = [row for row in rows if row["product_state"] == "complete_review_loop"]
    gated_rows = [row for row in rows if row["product_state"] == "measurement_gated"]
    return {
        "schema": "sportrx.demo_scenario_matrix",
        "schema_version": "0.1",
        "status": "ready",
        "scenario_count": len(rows),
        "complete_loop_count": len(ready_rows),
        "measurement_gated_count": len(gated_rows),
        "rows": rows,
        "recommended_first_scenario": "complete_loop" if ready_rows else rows[0]["id"],
        "primary_message": "Use Measure First to show honesty, Benchmark Underway to show partial data, and Complete Loop to show the full release demo.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def demo_scenario_matrix_markdown(matrix: dict[str, Any]) -> str:
    """Export the demo scenario matrix as Markdown."""

    lines = [
        "# SportRx Demo Scenario Matrix",
        "",
        f"- Status: {matrix['status']}",
        f"- Scenarios: {matrix['scenario_count']}",
        f"- Recommended first scenario: {matrix['recommended_first_scenario']}",
        f"- Claim boundary: {matrix['claim_boundary']}",
        "",
        "## Scenario Comparison",
    ]
    for row in matrix["rows"]:
        lines.extend(
            [
                "",
                f"### {row['label']}",
                "",
                f"- ID: `{row['id']}`",
                f"- Stage: {row['stage']}",
                f"- Product state: {row['product_state']}",
                f"- Measured areas: {row['measured_area_count']}",
                f"- Benchmark sessions: {row['benchmark_sessions']}",
                f"- Feedback weeks: {row['feedback_weeks']}",
                f"- Starter Path available: {row['starter_path_available']}",
                f"- Retest ready: {row['retest_ready']}",
                f"- Best for: {row['best_for']}",
                f"- Reviewer focus: {row['reviewer_focus']}",
                f"- Recommended pages: {', '.join(row['recommended_pages'])}",
            ]
        )
    return "\n".join(lines) + "\n"
