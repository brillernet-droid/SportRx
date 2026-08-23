"""Guided review console for SportRx.

This module turns existing demo, walkthrough, and launch-readiness state into a
single first-screen navigation object. It does not add sport rules.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Guided Review Console organizes existing SportRx demo navigation only. It "
    "does not validate SportRx, score performance, predict outcomes, or provide "
    "medical clearance."
)


def build_guided_review_console(
    walkthrough: dict[str, Any],
    first_run: dict[str, Any],
    launch: dict[str, Any],
    scenario_matrix: dict[str, Any],
) -> dict[str, Any]:
    """Build a guided review object from current product navigation state."""

    completion = walkthrough.get("completion", {})
    complete_steps = int(completion.get("complete_steps", 0) or 0)
    total_steps = int(completion.get("total_steps", 0) or 0)
    progress_percent = round((complete_steps / total_steps) * 100) if total_steps else 0
    next_step = walkthrough.get("next_step", {})
    export_count = len(launch.get("export_files", []))
    launch_ready = launch.get("status") == "ready_for_public_demo"
    scenario_ready = scenario_matrix.get("scenario_count", 0) >= 3
    first_run_ready = first_run.get("status") == "ready_for_guided_trial"
    walkthrough_ready = total_steps >= 9

    cards = [
        {
            "id": "recommended_scenario",
            "label": "Recommended Scenario",
            "value": scenario_matrix.get("recommended_first_scenario", "unknown"),
            "detail": f"{scenario_matrix.get('scenario_count', 0)} synthetic states available for guided review.",
            "status": "ready" if scenario_ready else "waiting",
        },
        {
            "id": "demo_progress",
            "label": "Demo Progress",
            "value": f"{complete_steps} / {total_steps}",
            "detail": f"{progress_percent}% of walkthrough steps are complete in the current state.",
            "status": "ready" if complete_steps >= 7 else "waiting",
        },
        {
            "id": "next_page",
            "label": "Next Page",
            "value": first_run.get("next_page", next_step.get("page", "Workbench")),
            "detail": first_run.get("next_action", next_step.get("why", "Review the next product step.")),
            "status": "ready" if first_run_ready else "waiting",
        },
        {
            "id": "release_gate",
            "label": "Release Gate",
            "value": launch.get("status", "unknown"),
            "detail": f"{launch.get('passed_checks', 0)} / {launch.get('total_checks', 0)} launch checks passed.",
            "status": "ready" if launch_ready else "waiting",
        },
        {
            "id": "export_pack",
            "label": "Export Pack",
            "value": f"{export_count} expected files",
            "detail": "Review artifacts, benchmark logs, QA notes, and restore snapshots stay local and downloadable.",
            "status": "ready" if export_count >= 30 else "waiting",
        },
    ]

    review_steps = [
        {
            "step": item["step"],
            "page": item["page"],
            "title": item["title"],
            "status": item["status"],
            "why": item["why"],
            "action": "Open page" if item["status"] not in {"complete"} else "Review if needed",
        }
        for item in walkthrough.get("steps", [])
    ]

    quick_actions = [
        {
            "id": "load_complete_loop",
            "label": "Load Complete Loop",
            "target": "Workbench",
            "purpose": "Show the full synthetic review loop before asking someone to judge the product.",
        },
        {
            "id": "start_benchmark",
            "label": "Start Benchmark",
            "target": "Benchmark Protocol",
            "purpose": "Move from self-report into repeatable measured data.",
        },
        {
            "id": "open_training_profile",
            "label": "Open Training Profile",
            "target": "Training Profile",
            "purpose": "Inspect current measured picture, known/unknown fields, and handoff gates.",
        },
        {
            "id": "export_review_pack",
            "label": "Export Review Pack",
            "target": "Export Center",
            "purpose": "Download local review artifacts and Session Snapshot.",
        },
        {
            "id": "check_release_qa",
            "label": "Check Release QA",
            "target": "Release QA",
            "purpose": "Confirm product-readiness and claim-boundary gates.",
        },
    ]

    ready_cards = sum(1 for item in cards if item["status"] == "ready")
    status = "ready_for_guided_review" if ready_cards == len(cards) and walkthrough_ready else "needs_guided_review"

    return {
        "schema": "sportrx.guided_review_console",
        "schema_version": "0.1",
        "status": status,
        "ready_cards": ready_cards,
        "total_cards": len(cards),
        "progress_percent": progress_percent,
        "cards": cards,
        "review_steps": review_steps,
        "quick_actions": quick_actions,
        "primary_message": "Use Guided Review to move from scenario selection to measurement, handoff, export, and Release QA without guessing the next click.",
        "next_action": first_run.get("next_action", next_step.get("why", "Continue the guided review path.")),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def guided_review_markdown(console: dict[str, Any]) -> str:
    """Export the guided review console as Markdown."""

    lines = [
        "# SportRx Guided Review Console",
        "",
        f"- Status: {console['status']}",
        f"- Progress: {console['progress_percent']}%",
        f"- Ready cards: {console['ready_cards']} / {console['total_cards']}",
        f"- Claim boundary: {console['claim_boundary']}",
        "",
        "## Review Position",
        "",
        console["primary_message"],
        "",
        "## Cards",
    ]
    for item in console["cards"]:
        lines.extend(
            [
                "",
                f"### {item['label']}",
                "",
                f"- Status: {item['status']}",
                f"- Value: {item['value']}",
                f"- Detail: {item['detail']}",
            ]
        )
    lines.extend(["", "## Review Steps"])
    for item in console["review_steps"]:
        lines.append(f"- Step {item['step']} - {item['page']}: {item['title']} ({item['status']})")
    lines.extend(["", "## Quick Actions"])
    for item in console["quick_actions"]:
        lines.append(f"- {item['label']} -> {item['target']}: {item['purpose']}")
    lines.extend(["", "## Next Action", "", console["next_action"]])
    return "\n".join(lines) + "\n"
