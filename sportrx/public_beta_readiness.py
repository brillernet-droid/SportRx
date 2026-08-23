"""Public beta readiness checks for SportRx.

This module summarizes product-release gates only. It does not validate rules,
estimate medical risk, score athletic performance, or predict outcomes.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Public Beta Readiness is a product-release gate for the local prototype. "
    "It does not validate SportRx, create athlete norms, provide medical "
    "clearance, or prove training outcomes."
)


def build_public_beta_readiness(
    qa: dict[str, Any],
    launch: dict[str, Any],
    runtime: dict[str, Any],
    package_manifest: dict[str, Any],
    runbook: dict[str, Any],
    evidence_files_present: dict[str, bool],
    pilot_review: dict[str, Any],
) -> dict[str, Any]:
    """Build a public-beta gate from existing release and pilot-review checks."""

    evidence_ready = bool(evidence_files_present) and all(evidence_files_present.values())
    pilot_entries = int(pilot_review.get("entry_count", 0))
    pilot_flags = list(pilot_review.get("review_flags", []))

    checks = [
        _check(
            "beta_runtime",
            "Runtime is ready for local reviewers",
            runtime.get("status") == "ready_to_run_locally",
            f"Runtime status: {runtime.get('status', 'unknown')}.",
        ),
        _check(
            "beta_release_qa",
            "Release QA is complete",
            qa.get("status") == "ready_for_demo_review",
            f"{qa.get('passed_checks', 0)} / {qa.get('total_checks', 0)} Release QA checks passed.",
        ),
        _check(
            "beta_launch",
            "Launch readiness is complete",
            launch.get("status") == "ready_for_public_demo",
            f"{launch.get('passed_checks', 0)} / {launch.get('total_checks', 0)} Launch checks passed.",
        ),
        _check(
            "beta_package",
            "Public package is clean",
            package_manifest.get("status") == "ready_for_public_package",
            f"Package status: {package_manifest.get('status', 'unknown')}.",
        ),
        _check(
            "beta_runbook",
            "Demo runbook is ready",
            runbook.get("status") == "ready",
            f"Runbook status: {runbook.get('status', 'unknown')}.",
        ),
        _check(
            "beta_evidence_context",
            "Evidence context is present",
            evidence_ready,
            "All required evidence files are present."
            if evidence_ready
            else "Evidence files are incomplete in the current QA context.",
        ),
        _check(
            "beta_pilot_feedback_depth",
            "Pilot feedback has enough entries for pattern review",
            pilot_entries >= 5,
            f"{pilot_entries} local pilot feedback entries recorded.",
        ),
        _check(
            "beta_pilot_feedback_flags",
            "Pilot feedback has no low-rating flags",
            pilot_entries >= 5 and not pilot_flags,
            "No low-rating fields flagged."
            if pilot_entries >= 5 and not pilot_flags
            else _pilot_flag_detail(pilot_entries, pilot_flags),
        ),
    ]

    core_ids = {
        "beta_runtime",
        "beta_release_qa",
        "beta_launch",
        "beta_package",
        "beta_runbook",
        "beta_evidence_context",
    }
    core_ready = all(item["passed"] for item in checks if item["id"] in core_ids)
    if not core_ready:
        status = "needs_release_fix"
        next_action = "Fix release, runtime, package, runbook, or evidence gates before inviting outside reviewers."
    elif pilot_entries < 5:
        status = "limited_review_ready_collect_pilot_feedback"
        next_action = "Run limited reviewer sessions and collect at least five local pilot feedback entries before public beta messaging."
    elif pilot_flags:
        status = "pilot_feedback_needs_review"
        next_action = "Review low-scoring pilot feedback fields before calling this a public beta candidate."
    else:
        status = "public_beta_candidate"
        next_action = "Export the review pack and public package, then run the planned public beta review."

    return {
        "schema": "sportrx.public_beta_readiness",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "passed_checks": sum(1 for item in checks if item["passed"]),
        "total_checks": len(checks),
        "checks": checks,
        "cards": [
            _card("Runtime", runtime.get("status", "unknown"), checks[0]["detail"], checks[0]["status"]),
            _card("Release QA", qa.get("status", "unknown"), checks[1]["detail"], checks[1]["status"]),
            _card("Launch", launch.get("status", "unknown"), checks[2]["detail"], checks[2]["status"]),
            _card("Public Package", package_manifest.get("status", "unknown"), checks[3]["detail"], checks[3]["status"]),
            _card("Evidence", f"{sum(evidence_files_present.values())} / {len(evidence_files_present)}", checks[5]["detail"], checks[5]["status"]),
            _card("Pilot Feedback", f"{pilot_entries} entries", checks[6]["detail"], checks[6]["status"]),
            _card("Pilot Flags", len(pilot_flags), checks[7]["detail"], checks[7]["status"]),
            _card("Claim Boundary", "Product gate only", CLAIM_BOUNDARY, "pass"),
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def public_beta_readiness_markdown(readiness: dict[str, Any]) -> str:
    """Export public beta readiness as markdown."""

    lines = [
        "# SportRx Public Beta Readiness",
        "",
        f"- Status: {readiness['status']}",
        f"- Passed: {readiness['passed_checks']} / {readiness['total_checks']}",
        f"- Next action: {readiness['next_action']}",
        f"- Claim boundary: {readiness['claim_boundary']}",
        "",
        "## Checks",
    ]
    for item in readiness["checks"]:
        lines.append(f"- [{item['status']}] {item['label']}: {item['detail']}")
    return "\n".join(lines) + "\n"


def _check(check_id: str, label: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "id": check_id,
        "label": label,
        "status": "pass" if passed else "needs_review",
        "passed": bool(passed),
        "detail": detail,
    }


def _card(label: str, value: object, detail: str, status: str) -> dict[str, Any]:
    return {
        "label": label,
        "value": value,
        "detail": detail,
        "status": "ready" if status == "pass" else "waiting",
    }


def _pilot_flag_detail(pilot_entries: int, pilot_flags: list[str]) -> str:
    if pilot_entries < 5:
        return "Collect at least five local entries before reviewing pilot feedback flags."
    return f"Low-rating fields flagged: {', '.join(pilot_flags)}."
