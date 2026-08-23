"""One-page release candidate summary for SportRx.

This module summarizes product-release state from existing gates. It does not
perform scientific validation or create new exercise-prescription rules.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Release Candidate Summary is a product handoff snapshot only. It does not "
    "validate SportRx, prove training outcomes, provide medical clearance, "
    "estimate injury risk, or create athlete norms."
)


BLOCKED_CLAIMS = [
    "validated sport readiness score",
    "medical clearance",
    "injury-risk percentage",
    "finish-time prediction",
    "population percentile or athlete norm",
    "guaranteed training outcome",
]


def build_release_candidate_summary(
    *,
    qa: dict[str, Any],
    launch: dict[str, Any],
    runtime: dict[str, Any],
    package_manifest: dict[str, Any],
    public_beta: dict[str, Any],
    export_file_count: int,
    review_pack_file_count: int | None = None,
) -> dict[str, Any]:
    """Build a one-page product release handoff from existing gates."""

    qa_ready = qa.get("status") == "ready_for_demo_review"
    launch_ready = launch.get("status") == "ready_for_public_demo"
    runtime_ready = runtime.get("status") == "ready_to_run_locally"
    package_ready = package_manifest.get("status") == "ready_for_public_package"
    export_ready = export_file_count >= 40
    beta_status = public_beta.get("status", "unknown")
    beta_gate_ready = beta_status in {"limited_review_ready_collect_pilot_feedback", "public_beta_candidate"}

    checks = [
        _check("candidate_runtime", "Runtime can start locally", runtime_ready, runtime.get("status", "unknown")),
        _check("candidate_release_qa", "Release QA passes", qa_ready, _gate_detail(qa)),
        _check("candidate_launch", "Launch readiness passes", launch_ready, _gate_detail(launch)),
        _check("candidate_package", "Public package is clean", package_ready, package_manifest.get("status", "unknown")),
        _check("candidate_exports", "Review exports are available", export_ready, f"{export_file_count} export files."),
        _check("candidate_beta_gate", "External-review gate is clear", beta_gate_ready, beta_status),
    ]
    passed = sum(1 for item in checks if item["passed"])

    if all(item["passed"] for item in checks) and beta_status == "public_beta_candidate":
        status = "public_beta_candidate"
        next_action = "Run the public beta review with exported artifacts and pilot-feedback monitoring."
    elif all(item["passed"] for item in checks[:5]) and beta_gate_ready:
        status = "limited_review_candidate"
        next_action = "Invite limited reviewers, collect at least five pilot-feedback entries, and keep public-beta claims blocked."
    else:
        status = "needs_release_work"
        next_action = "Resolve failing runtime, release, launch, package, or export gates before inviting outside reviewers."

    return {
        "schema": "sportrx.release_candidate_summary",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "passed_checks": passed,
        "total_checks": len(checks),
        "checks": checks,
        "cards": [
            _card("Runtime", runtime.get("status", "unknown"), "Local app launch state."),
            _card("Release QA", qa.get("status", "unknown"), _gate_detail(qa)),
            _card("Launch", launch.get("status", "unknown"), _gate_detail(launch)),
            _card("Public Package", package_manifest.get("status", "unknown"), "Internal files and caches excluded."),
            _card("Review Pack", f"{review_pack_file_count or export_file_count} files", "Local handoff artifacts available."),
            _card("External Gate", beta_status, public_beta.get("next_action", "")),
        ],
        "open_first": [
            "README.md",
            "sportrx_first_run_guide.md",
            "sportrx_page_health_matrix.md",
            "sportrx_release_qa.md",
            "sportrx_review_pack.zip",
        ],
        "run_commands": [
            'python3 -m pip install -e ".[dev,app]"',
            "python3 scripts/smoke_check.py",
            "bash scripts/run_local.sh",
        ],
        "blocked_claims": BLOCKED_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def release_candidate_summary_markdown(summary: dict[str, Any]) -> str:
    """Export the release candidate summary as Markdown."""

    lines = [
        "# SportRx Release Candidate Summary",
        "",
        f"- Status: {summary['status']}",
        f"- Passed: {summary['passed_checks']} / {summary['total_checks']}",
        f"- Next action: {summary['next_action']}",
        f"- Claim boundary: {summary['claim_boundary']}",
        "",
        "## Product Gates",
    ]
    for check in summary["checks"]:
        lines.append(f"- [{check['status']}] {check['label']}: {check['detail']}")

    lines.extend(["", "## Open First"])
    for item in summary["open_first"]:
        lines.append(f"- `{item}`")

    lines.extend(["", "## Run Commands"])
    for command in summary["run_commands"]:
        lines.append(f"- `{command}`")

    lines.extend(["", "## Blocked Claims"])
    for claim in summary["blocked_claims"]:
        lines.append(f"- {claim}")
    return "\n".join(lines) + "\n"


def _check(check_id: str, label: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "id": check_id,
        "label": label,
        "status": "pass" if passed else "needs_review",
        "passed": bool(passed),
        "detail": detail,
    }


def _card(label: str, value: object, detail: str) -> dict[str, Any]:
    return {"label": label, "value": value, "detail": detail}


def _gate_detail(gate: dict[str, Any]) -> str:
    if "passed_checks" in gate and "total_checks" in gate:
        return f"{gate.get('passed_checks', 0)} / {gate.get('total_checks', 0)} checks passed."
    return str(gate.get("status", "unknown"))
