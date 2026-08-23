"""Reviewer session plan for SportRx guided prototype review.

The plan turns scenario, runbook, and export artifacts into time-boxed review
tracks. It is product guidance, not scientific evidence.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Reviewer Session Plan guides local product review only. It does not "
    "validate SportRx, create athlete norms, predict outcomes, or provide "
    "medical clearance."
)


def _scenario_lookup(matrix: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["id"]: row for row in matrix.get("rows", [])}


def build_reviewer_session_plan(
    first_run_guide: dict[str, Any],
    scenario_matrix: dict[str, Any],
    runbook: dict[str, Any],
) -> dict[str, Any]:
    """Build time-boxed reviewer tracks for the local SportRx prototype."""

    scenarios = _scenario_lookup(scenario_matrix)
    complete = scenarios.get("complete_loop", {})
    measure_first = scenarios.get("measure_first", {})
    partial = scenarios.get("benchmark_underway", {})
    guardrails = list(runbook.get("guardrails", []))
    common_artifacts = [
        "sportrx_first_run_guide.md",
        "sportrx_demo_scenario_matrix.md",
        "sportrx_reviewer_handoff.md",
    ]
    tracks = [
        {
            "id": "quick_scan",
            "label": "3-minute quick scan",
            "duration_min": 3,
            "scenario_id": "complete_loop",
            "best_for": "A first impression, screen recording, or quick stakeholder walkthrough.",
            "page_sequence": ["Workbench", "Training Profile", "Export Center"],
            "show": [
                "Launch Command Center",
                "Demo Scenario Matrix",
                "Training Profile current measured picture",
                "Review Pack download",
            ],
            "success_criteria": [
                "Reviewer understands SportRx is measurement-first.",
                "Reviewer sees that synthetic demo data are not validation data.",
                "Reviewer can find local export artifacts.",
            ],
            "artifacts": common_artifacts + ["sportrx_training_profile_report.md"],
            "scenario_state": complete.get("product_state", "complete_review_loop"),
        },
        {
            "id": "guided_measurement_review",
            "label": "8-minute guided measurement review",
            "duration_min": 8,
            "scenario_id": "benchmark_underway",
            "best_for": "Reviewing partial data handling, Not tested states, and Benchmark Log honesty.",
            "page_sequence": ["Workbench", "Benchmark Protocol", "Benchmark Log", "Training Profile", "Export Center"],
            "show": [
                "Test Session Operator",
                "Benchmark Log quality review",
                "HYROX import compatibility",
                "Training Profile known/unknown boundaries",
                "Measurement Schema Registry",
            ],
            "success_criteria": [
                "Reviewer sees partial records remain partial.",
                "Reviewer sees raw-only results are not converted into scores.",
                "Reviewer can explain why tailored Starter Path may stay gated.",
            ],
            "artifacts": common_artifacts
            + [
                "sportrx_test_session_operator.md",
                "sportrx_benchmark_log.json",
                "sportrx_measurement_schema_registry.md",
            ],
            "scenario_state": partial.get("product_state", "partial_measurement"),
        },
        {
            "id": "full_release_review",
            "label": "12-minute full release review",
            "duration_min": 12,
            "scenario_id": "complete_loop",
            "best_for": "A complete release-candidate inspection before sharing the repository.",
            "page_sequence": list(
                dict.fromkeys(
                    complete.get("recommended_pages", [])
                    + ["Benchmark Protocol", "Benchmark Log", "Pilot Feedback", "Release QA"]
                )
            ),
            "show": [
                "Full measurement loop",
                "4-week Training Block",
                "Feedback Loop and retest comparison",
                "Pilot Feedback prompt",
                "Release QA and Public Beta Readiness",
            ],
            "success_criteria": [
                "Reviewer can run the complete demo without extra setup.",
                "Reviewer can export review artifacts and public package checks.",
                "Reviewer sees claim guardrails repeated across release screens.",
            ],
            "artifacts": common_artifacts
            + [
                "sportrx_demo_runbook.md",
                "sportrx_review_pack.zip",
                "sportrx_public_beta_readiness.md",
            ],
            "scenario_state": complete.get("product_state", "complete_review_loop"),
        },
    ]

    recommended = first_run_guide.get("recommended_path", "complete_demo")
    if recommended == "measure_first":
        next_track = "guided_measurement_review"
    elif recommended == "review_export":
        next_track = "quick_scan"
    else:
        next_track = "full_release_review"

    return {
        "schema": "sportrx.reviewer_session_plan",
        "schema_version": "0.1",
        "status": "ready",
        "next_track": next_track,
        "track_count": len(tracks),
        "total_review_minutes": sum(track["duration_min"] for track in tracks),
        "tracks": tracks,
        "guardrails": guardrails,
        "primary_message": "Choose a time-boxed review track before loading demo data or judging release readiness.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def reviewer_session_plan_markdown(plan: dict[str, Any]) -> str:
    """Export the reviewer session plan as Markdown."""

    lines = [
        "# SportRx Reviewer Session Plan",
        "",
        f"- Status: {plan['status']}",
        f"- Tracks: {plan['track_count']}",
        f"- Next track: {plan['next_track']}",
        f"- Total review minutes: {plan['total_review_minutes']}",
        f"- Claim boundary: {plan['claim_boundary']}",
        "",
        "## Tracks",
    ]
    for track in plan["tracks"]:
        lines.extend(
            [
                "",
                f"### {track['label']}",
                "",
                f"- ID: `{track['id']}`",
                f"- Duration: {track['duration_min']} minutes",
                f"- Scenario: `{track['scenario_id']}` ({track['scenario_state']})",
                f"- Best for: {track['best_for']}",
                f"- Page sequence: {' -> '.join(track['page_sequence'])}",
                f"- Artifacts: {', '.join(track['artifacts'])}",
                "- Show:",
            ]
        )
        for item in track["show"]:
            lines.append(f"  - {item}")
        lines.append("- Success criteria:")
        for item in track["success_criteria"]:
            lines.append(f"  - {item}")

    lines.extend(["", "## Guardrails"])
    for item in plan["guardrails"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"
