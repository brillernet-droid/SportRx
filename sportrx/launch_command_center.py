"""Workbench command-center view model for SportRx.

This module converts launch/readiness/runbook state into compact cards for the
first screen. It does not add product logic or scientific claims.
"""

from __future__ import annotations

from typing import Any


def build_launch_command_center(
    launch_readiness: dict[str, Any],
    runbook: dict[str, Any],
) -> dict[str, Any]:
    """Build compact launch cards for the Workbench first screen."""

    launch_ready = launch_readiness.get("status") == "ready_for_public_demo"
    runbook_ready = runbook.get("status") == "ready"
    output_summary = launch_readiness.get("output_gate_summary", {})

    cards = [
        {
            "id": "demo_loop",
            "label": "Demo Loop",
            "status": "ready" if launch_ready else "needs_review",
            "value": f"{launch_readiness.get('passed_checks', 0)} / {launch_readiness.get('total_checks', 0)} checks",
            "detail": "Launch readiness is complete." if launch_ready else "Load demo data and review blocked checks.",
            "cta_page": "Release QA",
        },
        {
            "id": "output_gates",
            "label": "Output Gates",
            "status": "ready" if output_summary.get("total_outputs", 0) else "needs_review",
            "value": f"{output_summary.get('active_outputs', 0)} active outputs",
            "detail": f"{output_summary.get('blocked_outputs', 0)} blocked, {output_summary.get('provisional_outputs', 0)} provisional.",
            "cta_page": "Training Profile",
        },
        {
            "id": "public_package",
            "label": "Public Package",
            "status": "ready" if launch_readiness.get("package_status") == "ready_for_public_package" else "needs_review",
            "value": launch_readiness.get("package_status", "unknown"),
            "detail": "Internal notes and generated files are excluded from the package.",
            "cta_page": "Release QA",
        },
        {
            "id": "reviewer_script",
            "label": "Reviewer Script",
            "status": "ready" if runbook_ready else "needs_review",
            "value": f"{len(runbook.get('must_show', []))} must-show pages",
            "detail": f"{runbook.get('estimated_minutes', 0)} min guided demo with claim guardrails.",
            "cta_page": "Workbench",
        },
    ]
    return {
        "schema": "sportrx.launch_command_center",
        "schema_version": "0.1",
        "status": "ready" if all(card["status"] == "ready" for card in cards) else "needs_review",
        "cards": cards,
        "primary_message": (
            "Public demo package is ready for review."
            if all(card["status"] == "ready" for card in cards)
            else "Review the highlighted launch cards before public demo."
        ),
        "claim_boundary": "Command Center summarizes product-readiness state only; it is not validation.",
    }
