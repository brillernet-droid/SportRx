"""Reviewer runbook for the SportRx public demo.

The runbook turns launch-readiness state into a short guided demo script. It is
product documentation, not scientific evidence.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "The demo runbook is a product-review guide. It must not be presented as "
    "scientific validation, medical clearance, race prediction, or injury-risk "
    "assessment."
)


PAGE_TALKING_POINTS = {
    "Workbench": "Start with the measurement loop, current gates, and what the demo refuses to claim.",
    "Quick Match": "Show that the first screen uses recent training behavior, not subjective adaptability labels.",
    "HYROX Check": "Show measured, self-reported, not-tested, and ignored metric sources.",
    "Benchmark Protocol": "Show standard and low-equipment testing paths plus stop rules.",
    "Benchmark Log": "Show raw results, RPE, equipment, substitutions, and retest comparability.",
    "Training Profile": "Show current measured picture, output gates, known/unknown, and handoff boundary.",
    "训练": "Show the 4-week starter block only after measurement gates are satisfied.",
    "复测": "Show weekly feedback, plan-actual reason codes, and raw retest comparison.",
    "Export Center": "Show user-owned Markdown/JSON/CSV artifacts.",
    "Release QA": "Show product QA, public package status, and launch readiness.",
}


def build_demo_runbook(launch_readiness: dict[str, Any]) -> dict[str, Any]:
    """Build a guided reviewer script from a launch-readiness report."""

    review_path = launch_readiness.get("review_path", [])
    steps = [
        {
            "step": item["step"],
            "page": item["page"],
            "task": item["task"],
            "status": item["status"],
            "talking_point": PAGE_TALKING_POINTS.get(item["page"], "Review this page in the measurement loop."),
        }
        for item in review_path
    ]

    must_show = [
        step
        for step in steps
        if step["page"] in {"Workbench", "HYROX Check", "Benchmark Log", "Training Profile", "复测", "Release QA"}
    ]
    guardrails = [
        "Do not call SportRx validated.",
        "Do not call outputs medical clearance.",
        "Do not claim injury-risk percentages.",
        "Do not present retest deltas as validated meaningful change.",
        "Do not describe demo seed data as athlete norms.",
    ]
    status = "ready" if launch_readiness.get("status") == "ready_for_public_demo" else "needs_review"
    return {
        "schema": "sportrx.demo_runbook",
        "schema_version": "0.1",
        "status": status,
        "launch_status": launch_readiness.get("status"),
        "estimated_minutes": 12 if status == "ready" else 8,
        "steps": steps,
        "must_show": must_show,
        "guardrails": guardrails,
        "opening_line": (
            "SportRx is a measurement-first sport performance lab prototype for recreational athletes."
        ),
        "closing_line": (
            "The next milestone is better measurement and real pilot data, not broader AI coaching."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def demo_runbook_markdown(runbook: dict[str, Any]) -> str:
    """Export the reviewer runbook as markdown."""

    lines = [
        "# SportRx Demo Runbook",
        "",
        f"- Status: {runbook['status']}",
        f"- Launch status: {runbook['launch_status']}",
        f"- Estimated time: {runbook['estimated_minutes']} minutes",
        f"- Claim boundary: {runbook['claim_boundary']}",
        "",
        "## Opening",
        runbook["opening_line"],
        "",
        "## Must Show",
    ]
    for item in runbook["must_show"]:
        lines.append(f"- {item['page']}: {item['talking_point']}")

    lines.extend(["", "## Full Review Path"])
    for item in runbook["steps"]:
        lines.append(f"- Step {item['step']} - {item['page']}: {item['task']} ({item['status']})")

    lines.extend(["", "## Guardrails"])
    for item in runbook["guardrails"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Closing", runbook["closing_line"]])
    return "\n".join(lines) + "\n"
