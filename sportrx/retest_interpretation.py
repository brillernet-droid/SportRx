"""Retest interpretation guard for SportRx benchmark changes."""

from __future__ import annotations

from typing import Any

from .benchmark_log import compare_retest_sessions
from .protocol_deviation import build_protocol_deviation_review


CLAIM_BOUNDARY = (
    "Retest Interpretation Guard checks whether raw pre/post benchmark changes "
    "have comparable protocol context. It does not prove training effects, "
    "validate minimal detectable change, predict outcomes, or provide medical "
    "clearance."
)


def _context_by_component(deviation_review: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["component_id"]: item for item in deviation_review.get("retest_reviews", [])}


def build_retest_interpretation_guard(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    """Combine raw retest deltas with protocol-context comparability checks."""

    comparisons = compare_retest_sessions(sessions)
    deviation_review = build_protocol_deviation_review(sessions)
    context_lookup = _context_by_component(deviation_review)

    items: list[dict[str, Any]] = []
    for comparison in comparisons:
        context = context_lookup.get(comparison["component_id"], {})
        context_status = context.get("status", "not_reviewed")
        if context_status == "comparable_retest":
            interpretation_status = "comparable_raw_change"
            interpretation = "Raw change can be reviewed with matching protocol context."
        elif context_status == "context_changed":
            interpretation_status = "context_changed"
            interpretation = "Raw change is visible, but protocol context changed."
        else:
            interpretation_status = "context_not_reviewed"
            interpretation = "Raw change is visible, but protocol context is not fully reviewed."

        items.append(
            {
                **comparison,
                "context_status": context_status,
                "context_changes": context.get("changes", []),
                "interpretation_status": interpretation_status,
                "interpretation": interpretation,
                "baseline_protocol": context.get("baseline_protocol"),
                "latest_protocol": context.get("latest_protocol"),
            }
        )

    context_changed = [item for item in items if item["interpretation_status"] == "context_changed"]
    comparable = [item for item in items if item["interpretation_status"] == "comparable_raw_change"]

    if not sessions:
        status = "no_benchmark_logs"
        next_action = "Record Benchmark Log sessions before reviewing retest interpretation."
    elif not items:
        status = "waiting_for_retest"
        next_action = "Repeat at least one completed benchmark component before interpreting raw change."
    elif context_changed and comparable:
        status = "mixed_retest_context"
        next_action = "Separate comparable raw changes from context-changed retests."
    elif context_changed:
        status = "context_changed"
        next_action = "Do not interpret raw change as comparable until protocol context matches again."
    else:
        status = "comparable_raw_change"
        next_action = "Review raw change together with weekly feedback; do not treat it as validated training effect."

    return {
        "schema": "sportrx.retest_interpretation_guard",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "comparison_count": len(items),
        "comparable_count": len(comparable),
        "context_changed_count": len(context_changed),
        "items": items,
        "protocol_deviation_status": deviation_review["status"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def retest_interpretation_markdown(guard: dict[str, Any]) -> str:
    """Export Retest Interpretation Guard as Markdown."""

    lines = [
        "# SportRx Retest Interpretation Guard",
        "",
        f"- Status: {guard['status']}",
        f"- Next action: {guard['next_action']}",
        f"- Comparisons: {guard['comparison_count']}",
        f"- Comparable raw changes: {guard['comparable_count']}",
        f"- Context-changed comparisons: {guard['context_changed_count']}",
        f"- Protocol deviation status: {guard['protocol_deviation_status']}",
        f"- Claim boundary: {guard['claim_boundary']}",
        "",
        "## Retest Items",
    ]
    if not guard["items"]:
        lines.append("- No repeated benchmark components yet.")
    for item in guard["items"]:
        changes = ", ".join(item["context_changes"]) if item["context_changes"] else "none"
        lines.append(
            f"- [{item['interpretation_status']}] {item['test']}: "
            f"{item['first_value']} -> {item['latest_value']} {item['value_unit']} "
            f"({item['direction']}); context changes: {changes}"
        )
    return "\n".join(lines) + "\n"
