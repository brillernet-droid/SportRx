"""Protocol deviation review for SportRx Benchmark Log sessions."""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Protocol Deviation Review summarizes benchmark-record consistency only. "
    "It does not score performance, validate the protocol, predict outcomes, "
    "estimate injury risk, or provide medical clearance."
)


def _equipment_key(result: dict[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(str(item) for item in result.get("equipment", []) or []))


def _substitution_key(result: dict[str, Any]) -> str:
    return str(result.get("substitution") or "").strip().lower()


def _protocol_context(result: dict[str, Any]) -> dict[str, Any]:
    """Return non-empty protocol context without changing legacy records."""

    return {
        str(key): value
        for key, value in dict(result.get("protocol_context", {}) or {}).items()
        if value is not None and value != ""
    }


def _completed_results(sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for session in sessions:
        for result in session.get("component_results", []):
            if result.get("completed") and result.get("value") is not None:
                rows.append(
                    {
                        **result,
                        "session_id": session.get("session_id"),
                        "session_date": session.get("date"),
                        "benchmark_path": session.get("benchmark_path"),
                        "protocol_version": session.get("protocol_version"),
                    }
                )
    return rows


def _component_record_review(result: dict[str, Any]) -> dict[str, Any]:
    flags: list[str] = []
    if not result.get("value_unit"):
        flags.append("missing_unit")
    if result.get("rpe_0_10") is None:
        flags.append("missing_rpe")
    if not result.get("equipment"):
        flags.append("missing_equipment")
    if result.get("substitution"):
        flags.append("substitution_recorded")

    if "missing_unit" in flags:
        status = "needs_review"
    elif flags:
        status = "deviation_or_context"
    else:
        status = "protocol_record_complete"

    return {
        "session_id": result.get("session_id"),
        "session_date": result.get("session_date"),
        "component_id": result.get("component_id"),
        "test": result.get("test", result.get("component_id")),
        "status": status,
        "flags": flags,
        "value_unit": result.get("value_unit"),
        "rpe_0_10": result.get("rpe_0_10"),
        "equipment": list(result.get("equipment", []) or []),
        "substitution": result.get("substitution"),
        "protocol_context": _protocol_context(result),
        "notes": result.get("notes", ""),
    }


def _retest_comparability(component_id: str, records: list[dict[str, Any]]) -> dict[str, Any]:
    sorted_records = sorted(records, key=lambda item: item.get("session_date") or "")
    baseline = sorted_records[0]
    latest = sorted_records[-1]
    changes: list[str] = []

    if baseline.get("benchmark_path") != latest.get("benchmark_path"):
        changes.append("benchmark_path_changed")
    if baseline.get("protocol_version") != latest.get("protocol_version"):
        changes.append("protocol_version_changed")
    if baseline.get("value_unit") != latest.get("value_unit"):
        changes.append("unit_changed")
    if _equipment_key(baseline) != _equipment_key(latest):
        changes.append("equipment_changed")
    if _substitution_key(baseline) != _substitution_key(latest):
        changes.append("substitution_changed")

    baseline_context = _protocol_context(baseline)
    latest_context = _protocol_context(latest)
    for field in sorted(set(baseline_context) | set(latest_context)):
        baseline_value = baseline_context.get(field)
        latest_value = latest_context.get(field)
        if baseline_value != latest_value:
            suffix = "missing" if baseline_value in {None, ""} or latest_value in {None, ""} else "changed"
            changes.append(f"protocol_context:{field}_{suffix}")

    return {
        "component_id": component_id,
        "test": latest.get("test", component_id),
        "session_count": len(sorted_records),
        "status": "comparable_retest" if not changes else "context_changed",
        "changes": changes,
        "baseline_date": baseline.get("session_date"),
        "latest_date": latest.get("session_date"),
        "baseline_protocol": f"{baseline.get('benchmark_path')} / {baseline.get('protocol_version')}",
        "latest_protocol": f"{latest.get('benchmark_path')} / {latest.get('protocol_version')}",
        "baseline_equipment": list(baseline.get("equipment", []) or []),
        "latest_equipment": list(latest.get("equipment", []) or []),
        "baseline_protocol_context": baseline_context,
        "latest_protocol_context": latest_context,
        "baseline_substitution": baseline.get("substitution"),
        "latest_substitution": latest.get("substitution"),
    }


def build_protocol_deviation_review(sessions: list[dict[str, Any]]) -> dict[str, Any]:
    """Review protocol consistency across saved Benchmark Log sessions."""

    completed = _completed_results(sessions)
    component_reviews = [_component_record_review(result) for result in completed]
    records_by_component: dict[str, list[dict[str, Any]]] = {}
    for result in completed:
        records_by_component.setdefault(result.get("component_id", "unknown"), []).append(result)

    retest_reviews = [
        _retest_comparability(component_id, records)
        for component_id, records in sorted(records_by_component.items())
        if len(records) >= 2
    ]

    flag_counts: dict[str, int] = {}
    for item in component_reviews:
        for flag in item["flags"]:
            flag_counts[flag] = flag_counts.get(flag, 0) + 1

    context_changed = [item for item in retest_reviews if item["status"] == "context_changed"]
    needs_review = [item for item in component_reviews if item["status"] == "needs_review"]
    deviation_or_context = [
        item
        for item in component_reviews
        if item["status"] == "deviation_or_context"
    ]

    if not sessions:
        status = "no_benchmark_logs"
        next_action = "Record a Benchmark Log before reviewing protocol deviations."
    elif not completed:
        status = "no_completed_measurements"
        next_action = "Save at least one completed component with a raw value."
    elif needs_review:
        status = "needs_protocol_review"
        next_action = "Fix missing units before interpreting or exporting the benchmark record."
    elif context_changed:
        status = "retest_context_changed"
        next_action = "Treat retest changes as contextual until route, equipment, unit, and substitution match again."
    elif deviation_or_context:
        status = "reviewable_with_context"
        next_action = "Keep substitutions, missing RPE, or equipment notes visible when reviewing this session."
    else:
        status = "repeatable_protocol_record"
        next_action = "Benchmark records are repeatable enough for local product review."

    return {
        "schema": "sportrx.protocol_deviation_review",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "session_count": len(sessions),
        "completed_component_count": len(completed),
        "component_reviews": component_reviews,
        "retest_reviews": retest_reviews,
        "flag_counts": flag_counts,
        "context_changed_count": len(context_changed),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def protocol_deviation_markdown(review: dict[str, Any]) -> str:
    """Export Protocol Deviation Review as Markdown."""

    lines = [
        "# SportRx Protocol Deviation Review",
        "",
        f"- Status: {review['status']}",
        f"- Next action: {review['next_action']}",
        f"- Sessions: {review['session_count']}",
        f"- Completed components: {review['completed_component_count']}",
        f"- Context-changed retests: {review['context_changed_count']}",
        f"- Claim boundary: {review['claim_boundary']}",
        "",
        "## Component Records",
    ]
    for item in review["component_reviews"]:
        flags = ", ".join(item["flags"]) if item["flags"] else "none"
        lines.append(
            f"- [{item['status']}] {item['session_date']} / {item['test']}: "
            f"unit={item['value_unit']}, RPE={item['rpe_0_10']}, flags={flags}"
        )

    lines.extend(["", "## Retest Comparability"])
    if not review["retest_reviews"]:
        lines.append("- No repeated completed components yet.")
    for item in review["retest_reviews"]:
        changes = ", ".join(item["changes"]) if item["changes"] else "none"
        lines.append(
            f"- [{item['status']}] {item['test']}: {item['baseline_date']} -> "
            f"{item['latest_date']}; changes={changes}"
        )
    return "\n".join(lines) + "\n"
