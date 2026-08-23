"""Demo experience polish layer for SportRx.

The goal is to make the first product screen feel guided and review-ready
without adding new sport rules or hidden scores.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Demo Experience Console organizes the local product demo and review path "
    "only. It does not validate SportRx, score performance, predict outcomes, "
    "or provide medical clearance."
)


def build_demo_experience_console(
    first_run: dict[str, Any],
    launch: dict[str, Any],
    session_quality: dict[str, Any],
    terminology: dict[str, Any],
    open_source: dict[str, Any],
) -> dict[str, Any]:
    """Build a first-screen experience layer for guided demo review."""

    launch_ready = launch.get("status") == "ready_for_public_demo"
    language_ready = terminology.get("status") == "ready_for_language_edition_review"
    quality_ready = session_quality.get("status") in {
        "release_review_ready",
        "ready_for_release_review",
        "ready_for_training_handoff",
    }
    traceability_ready = bool(open_source.get("integration_lanes"))

    cards = [
        {
            "id": "first_screen",
            "label": "First Screen",
            "value": "Workbench",
            "detail": "Open on current measured picture, Safety Gate, Benchmark state, and next action.",
            "status": "ready",
        },
        {
            "id": "trial_paths",
            "label": "Trial Paths",
            "value": f"{len(first_run.get('paths', []))} paths",
            "detail": "Complete demo, Quick Match self-intake, Benchmark-first, and export review paths are visible.",
            "status": "ready" if len(first_run.get("paths", [])) >= 4 else "waiting",
        },
        {
            "id": "language_contract",
            "label": "Language Contract",
            "value": "Edition-separated",
            "detail": "Chinese, English, and internal mixed-language editions are separated while shared product terms remain stable.",
            "status": "ready" if language_ready else "waiting",
        },
        {
            "id": "traceable_logic",
            "label": "Traceable Logic",
            "value": f"{len(open_source.get('integration_lanes', []))} lanes",
            "detail": "Open-source lessons are translated into integration lanes, not copied features.",
            "status": "ready" if traceability_ready else "waiting",
        },
        {
            "id": "release_gate",
            "label": "Release Gate",
            "value": launch.get("status", "unknown"),
            "detail": f"{launch.get('passed_checks', 0)} / {launch.get('total_checks', 0)} launch checks passed.",
            "status": "ready" if launch_ready else "waiting",
        },
        {
            "id": "session_quality",
            "label": "Session Quality",
            "value": session_quality.get("status", "unknown"),
            "detail": "Quality gates keep missing measurement, retest, feedback, and evidence context visible.",
            "status": "ready" if quality_ready else "waiting",
        },
    ]

    guided_sequence = [
        {
            "step": 1,
            "label": "Open Workbench",
            "page": "Workbench",
            "purpose": "See measured picture, Safety Gate, Benchmark state, and next action before entering forms.",
        },
        {
            "step": 2,
            "label": "Choose Trial Mode",
            "page": "Workbench",
            "purpose": "Load a complete demo, start Quick Match, or begin Benchmark-first measurement.",
        },
        {
            "step": 3,
            "label": "Inspect Measurement",
            "page": "HYROX Check / Benchmark Protocol",
            "purpose": "Separate Measured from Not tested and keep protocol context visible.",
        },
        {
            "step": 4,
            "label": "Review Handoff",
            "page": "Training Profile / 训练",
            "purpose": "Only show Starter Path when Safety Gate and measured-data gates allow it.",
        },
        {
            "step": 5,
            "label": "Export Review Pack",
            "page": "Export Center / Release QA",
            "purpose": "Download local artifacts and confirm claim boundaries before sharing.",
        },
    ]

    trust_anchors = [
        "Safety Gate remains separate from performance scoring.",
        "Missing performance tests stay Not tested.",
        "Every export includes claim boundaries.",
        "Terminology Guide blocks readiness-score, risk-percentage, and medical-clearance language.",
        "Open-source references are product research, not scientific validation.",
    ]

    blocked_impressions = [
        "Do not present SportRx as an AI coach.",
        "Do not imply official HYROX readiness.",
        "Do not show fake percentiles, fake norms, or event finish predictions.",
        "Do not describe Release QA as scientific validation.",
    ]

    ready_cards = sum(1 for item in cards if item["status"] == "ready")
    status = "ready_for_guided_demo" if ready_cards == len(cards) else "needs_demo_polish"

    return {
        "schema": "sportrx.demo_experience_console",
        "schema_version": "0.1",
        "status": status,
        "ready_cards": ready_cards,
        "total_cards": len(cards),
        "cards": cards,
        "guided_sequence": guided_sequence,
        "trust_anchors": trust_anchors,
        "blocked_impressions": blocked_impressions,
        "primary_message": "SportRx should open like a modern sport performance lab: measured picture first, trial path second, training handoff only after gates.",
        "next_action": "Use this console to review whether the first five minutes feel guided, credible, and measurement-first.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def demo_experience_markdown(console: dict[str, Any]) -> str:
    """Export the demo experience console as Markdown."""

    lines = [
        "# SportRx Demo Experience Console",
        "",
        f"- Status: {console['status']}",
        f"- Ready cards: {console['ready_cards']} / {console['total_cards']}",
        f"- Claim boundary: {console['claim_boundary']}",
        "",
        "## First Impression",
        "",
        console["primary_message"],
        "",
        "## Experience Cards",
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
    lines.extend(["", "## Guided Sequence"])
    for item in console["guided_sequence"]:
        lines.append(f"- Step {item['step']} - {item['label']} ({item['page']}): {item['purpose']}")
    lines.extend(["", "## Trust Anchors"])
    for item in console["trust_anchors"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Blocked Impressions"])
    for item in console["blocked_impressions"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Action", "", console["next_action"]])
    return "\n".join(lines) + "\n"
