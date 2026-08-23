"""Reviewer handoff guide for SportRx prototype trials."""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Reviewer Handoff explains how to inspect the local SportRx prototype. It "
    "does not validate SportRx, create athlete norms, predict outcomes, or "
    "provide medical clearance."
)


def _priority_artifacts(catalog: dict[str, Any]) -> list[dict[str, str]]:
    priority_ids = {
        "first_run_guide_markdown",
        "measurement_timeline_markdown",
        "protocol_markdown",
        "test_day_brief_markdown",
        "lab_readiness_markdown",
        "session_snapshot_json",
    }
    items = []
    for item in catalog.get("items", []):
        if item.get("id") in priority_ids or item.get("when_to_use") == "Open first":
            items.append(
                {
                    "filename": item["filename"],
                    "label": item["label"],
                    "when_to_use": item["when_to_use"],
                    "purpose": item["purpose"],
                }
            )
    return items


def build_reviewer_handoff(
    runtime: dict[str, Any],
    scenarios: list[dict[str, Any]],
    catalog: dict[str, Any],
    launch: dict[str, Any],
) -> dict[str, Any]:
    """Build a one-page guide for people reviewing a local SportRx build."""

    commands = runtime.get("commands", [])
    run_command = commands[-1] if commands else "python3 -m streamlit run app/streamlit_app.py"
    status_ready = (
        runtime.get("status") == "ready_to_run_locally"
        and len(scenarios) >= 3
        and catalog.get("artifact_count", 0) >= 18
    )

    return {
        "schema": "sportrx.reviewer_handoff",
        "schema_version": "0.1",
        "status": "ready_for_reviewer_handoff" if status_ready else "needs_review",
        "open_first": [
            {"label": "Run locally", "command": run_command},
            {"label": "Start in Workbench", "page": "Workbench"},
            {"label": "Load a demo scenario", "page": "Workbench / Demo Scenario Library"},
            {"label": "Download Review Pack", "page": "Export Center"},
        ],
        "demo_scenarios": [
            {
                "id": item["id"],
                "label": item["label"],
                "stage": item["stage"],
                "best_for": item["best_for"],
            }
            for item in scenarios
        ],
        "priority_artifacts": _priority_artifacts(catalog),
        "review_questions": [
            "Can a first-time reviewer understand where to start?",
            "Does the measurement-first boundary feel clear?",
            "Are Not tested and prerequisite gates visible?",
            "Can the reviewer export and restore a local trial?",
            "Do the outputs avoid validated-score, prediction, and medical-clearance claims?",
        ],
        "claim_guardrails": [
            "Do not describe SportRx as scientifically validated.",
            "Do not call outputs injury-risk prediction or medical clearance.",
            "Do not present synthetic scenarios as athlete norms or percentiles.",
            "Do not use Safety Gate as a performance score.",
            "Do not hide missing benchmark data; keep it as Not tested.",
        ],
        "runtime_summary": {
            "status": runtime.get("status"),
            "python_version": runtime.get("python_version"),
            "streamlit_version": runtime.get("streamlit_version"),
            "passed_checks": runtime.get("passed_checks"),
            "total_checks": runtime.get("total_checks"),
        },
        "launch_summary": {
            "status": launch.get("status"),
            "qa_status": launch.get("qa_status"),
            "package_status": launch.get("package_status"),
            "passed_checks": launch.get("passed_checks"),
            "total_checks": launch.get("total_checks"),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def reviewer_handoff_markdown(handoff: dict[str, Any]) -> str:
    """Export reviewer handoff guidance as Markdown."""

    lines = [
        "# SportRx Reviewer Handoff",
        "",
        f"- Status: {handoff['status']}",
        f"- Claim boundary: {handoff['claim_boundary']}",
        "",
        "## Open First",
    ]
    for item in handoff["open_first"]:
        if "command" in item:
            lines.append(f"- {item['label']}: `{item['command']}`")
        else:
            lines.append(f"- {item['label']}: {item['page']}")

    lines.extend(["", "## Demo Scenarios"])
    for scenario in handoff["demo_scenarios"]:
        lines.append(
            f"- `{scenario['id']}` - {scenario['label']} ({scenario['stage']}): {scenario['best_for']}"
        )

    lines.extend(["", "## Priority Artifacts"])
    for artifact in handoff["priority_artifacts"]:
        lines.append(
            f"- `{artifact['filename']}` - {artifact['label']} ({artifact['when_to_use']}): {artifact['purpose']}"
        )

    lines.extend(["", "## Review Questions"])
    for question in handoff["review_questions"]:
        lines.append(f"- {question}")

    lines.extend(["", "## Claim Guardrails"])
    for guardrail in handoff["claim_guardrails"]:
        lines.append(f"- {guardrail}")

    runtime = handoff["runtime_summary"]
    launch = handoff["launch_summary"]
    lines.extend(
        [
            "",
            "## Runtime Summary",
            f"- Runtime: {runtime.get('status')}",
            f"- Python: {runtime.get('python_version')}",
            f"- Streamlit: {runtime.get('streamlit_version') or 'not installed'}",
            f"- Checks: {runtime.get('passed_checks')} / {runtime.get('total_checks')}",
            "",
            "## Launch Summary",
            f"- Launch: {launch.get('status')}",
            f"- QA: {launch.get('qa_status')}",
            f"- Package: {launch.get('package_status')}",
            f"- Checks: {launch.get('passed_checks')} / {launch.get('total_checks')}",
        ]
    )
    return "\n".join(lines) + "\n"
