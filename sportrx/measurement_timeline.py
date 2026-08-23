"""Measurement-loop timeline view model for SportRx."""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Measurement Loop Timeline visualizes product workflow state only. It does "
    "not validate SportRx, score performance, predict outcomes, or provide "
    "medical clearance."
)


STATUS_STAGE = {
    "complete": "done",
    "recommended": "current",
    "needs_measurement": "waiting",
    "no_log_yet": "waiting",
    "limited_report": "waiting",
    "blocked_by_measurement_gate": "blocked",
    "awaiting_feedback_or_retest": "waiting",
    "nothing_to_export_yet": "waiting",
    "qa_needs_demo_loop": "waiting",
}


def build_measurement_timeline(walkthrough: dict[str, Any]) -> dict[str, Any]:
    """Convert walkthrough state into a compact measurement-loop timeline."""

    items = []
    for step in walkthrough.get("steps", []):
        raw_status = step.get("status", "not_started")
        stage = STATUS_STAGE.get(raw_status, "waiting")
        items.append(
            {
                "step": step["step"],
                "page": step["page"],
                "title": step["title"],
                "status": raw_status,
                "stage": stage,
                "why": step["why"],
            }
        )

    done = sum(1 for item in items if item["stage"] == "done")
    current = next((item for item in items if item["stage"] in {"current", "waiting", "blocked"}), items[-1] if items else None)
    return {
        "schema": "sportrx.measurement_timeline",
        "schema_version": "0.1",
        "items": items,
        "current_step": current,
        "completion": {
            "done": done,
            "total": len(items),
            "percent": round(done / len(items), 2) if items else 0,
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def measurement_timeline_markdown(timeline: dict[str, Any]) -> str:
    """Export the measurement timeline as Markdown."""

    completion = timeline.get("completion", {})
    lines = [
        "# SportRx Measurement Loop Timeline",
        "",
        f"- Complete: {completion.get('done', 0)} / {completion.get('total', 0)}",
        f"- Percent: {completion.get('percent', 0)}",
        f"- Claim boundary: {timeline.get('claim_boundary', CLAIM_BOUNDARY)}",
        "",
        "## Timeline",
    ]
    for item in timeline.get("items", []):
        lines.append(
            f"- Step {item['step']} - {item['page']}: {item['title']} "
            f"[{item['stage']} / {item['status']}]. {item['why']}"
        )
    return "\n".join(lines) + "\n"
