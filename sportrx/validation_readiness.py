"""Validation readiness matrix for SportRx release review."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .benchmark_log import summarize_benchmark_sessions
from .evidence_library import build_evidence_library
from .retest_interpretation import build_retest_interpretation_guard
from .session_quality_review import build_session_quality_review


CLAIM_BOUNDARY = (
    "Validation Readiness Matrix tracks whether SportRx is ready to collect "
    "validation evidence. It does not validate SportRx, create athlete norms, "
    "prove training effects, predict outcomes, or provide medical clearance."
)


PHASES = [
    {
        "id": "phase_0_self_use",
        "label": "Phase 0 - Self-use",
        "target_sample": "1 builder",
        "minimum_requirements": [
            "Baseline benchmark",
            "Weekly completion and RPE",
            "Week 4 retest using the same setup",
            "Product-friction notes",
        ],
        "allowed_claim": "Used internally for product testing.",
    },
    {
        "id": "phase_1_tiny_alpha",
        "label": "Phase 1 - Tiny Alpha",
        "target_sample": "5-10 recreational adults",
        "minimum_requirements": [
            "Onboarding completion",
            "Safety Gate result",
            "At least two measured performance dimensions",
            "Weekly adherence",
            "Retest result",
            "User confusion points",
        ],
        "allowed_claim": "Early usability-tested prototype.",
    },
    {
        "id": "phase_2_pilot_dataset",
        "label": "Phase 2 - Pilot Dataset",
        "target_sample": "30-50 users",
        "minimum_requirements": [
            "Longitudinal user ID",
            "Baseline and retest dates",
            "Safety Gate status",
            "Equipment access",
            "Raw benchmark results",
            "RPE",
            "Session adherence",
            "Protocol deviation notes",
        ],
        "allowed_claim": "Pilot-tested benchmark workflow; not population-normed.",
    },
]


BLOCKED_CLAIMS = [
    "finish-time prediction",
    "completion probability",
    "injury-risk percentage",
    "population percentile",
    "medical clearance",
    "validated readiness score",
]


def _required_file_status(root: Path) -> dict[str, bool]:
    paths = [
        "evidence/validation_plan.md",
        "evidence/validation.md",
        "evidence/evidence_appraisal.md",
        "evidence/rule_evidence_map.md",
    ]
    return {path: (root / path).exists() for path in paths}


def _phase_rows(
    benchmark_summary: dict[str, Any],
    retest_guard: dict[str, Any],
    feedback_by_week: dict[int, dict[str, Any]],
    pilot_feedback_entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    feedback_weeks = len(feedback_by_week)
    pilot_feedback_count = len(pilot_feedback_entries)
    has_baseline_and_retest = bool(retest_guard.get("comparison_count", 0))

    rows = []
    for phase in PHASES:
        if phase["id"] == "phase_0_self_use":
            ready_to_collect = benchmark_summary.get("session_count", 0) >= 1 and feedback_weeks >= 1
            evidence_gap = (
                "Needs real self-use data; synthetic demo state does not count as validation evidence."
                if not has_baseline_and_retest
                else "Needs builder-owned self-use designation and notes before claiming Phase 0 completion."
            )
            status = "collection_ready" if ready_to_collect else "needs_local_trial"
        elif phase["id"] == "phase_1_tiny_alpha":
            ready_to_collect = pilot_feedback_count >= 5
            evidence_gap = "Needs 5-10 real recreational adults under a tiny-alpha protocol."
            status = "ready_after_self_use" if ready_to_collect else "blocked_until_self_use"
        else:
            ready_to_collect = False
            evidence_gap = "Needs 30-50 users and a formal pilot dataset before any pilot-tested claim."
            status = "blocked_until_alpha"

        rows.append(
            {
                **phase,
                "status": status,
                "ready_to_collect": ready_to_collect,
                "evidence_gap": evidence_gap,
            }
        )
    return rows


def build_validation_readiness_matrix(
    profile: dict[str, Any],
    passport: dict[str, Any],
    plan: dict[str, Any],
    benchmark_sessions: list[dict[str, Any]],
    feedback_by_week: dict[int, dict[str, Any]],
    pilot_feedback_entries: list[dict[str, Any]] | None = None,
    root: str | Path = ".",
) -> dict[str, Any]:
    """Build validation-readiness state without claiming validation completion."""

    root_path = Path(root)
    pilot_feedback_entries = pilot_feedback_entries or []
    benchmark_summary = summarize_benchmark_sessions(benchmark_sessions)
    retest_guard = build_retest_interpretation_guard(benchmark_sessions)
    session_quality = build_session_quality_review(
        profile,
        passport,
        plan,
        benchmark_sessions,
        feedback_by_week,
        {},
        root_path,
    )
    evidence_library = build_evidence_library(root_path)
    required_files = _required_file_status(root_path)
    phases = _phase_rows(benchmark_summary, retest_guard, feedback_by_week, pilot_feedback_entries)

    capture_checks = [
        {
            "id": "validation_plan_present",
            "label": "Validation plan is present",
            "passed": required_files["evidence/validation_plan.md"],
            "detail": "evidence/validation_plan.md defines self-use, alpha, and pilot phases.",
        },
        {
            "id": "benchmark_capture",
            "label": "Benchmark capture exists",
            "passed": benchmark_summary.get("session_count", 0) > 0,
            "detail": f"{benchmark_summary.get('session_count', 0)} Benchmark Log sessions recorded.",
        },
        {
            "id": "feedback_capture",
            "label": "Weekly feedback capture exists",
            "passed": len(feedback_by_week) > 0,
            "detail": f"{len(feedback_by_week)} weekly feedback records saved.",
        },
        {
            "id": "retest_guard",
            "label": "Retest interpretation guard exists",
            "passed": retest_guard["status"] not in {"no_benchmark_logs", "waiting_for_retest"},
            "detail": f"Retest guard status: {retest_guard['status']}.",
        },
        {
            "id": "evidence_library",
            "label": "Evidence library exists",
            "passed": evidence_library["status"] == "ready_for_review",
            "detail": f"{evidence_library['source_count']} sources indexed.",
        },
        {
            "id": "session_quality",
            "label": "Session quality gates exist",
            "passed": bool(session_quality.get("gates")),
            "detail": f"Session quality status: {session_quality.get('status')}.",
        },
    ]
    passed_checks = sum(1 for item in capture_checks if item["passed"])
    capture_ready = passed_checks == len(capture_checks)
    status = "ready_to_collect_self_use_data" if capture_ready else "needs_data_capture_setup"

    return {
        "schema": "sportrx.validation_readiness_matrix",
        "schema_version": "0.1",
        "status": status,
        "current_validation_claim": "Prototype; not validated.",
        "next_action": (
            "Run Phase 0 self-use with real builder data and notes."
            if capture_ready
            else "Complete data-capture gates before starting self-use validation."
        ),
        "capture_ready": capture_ready,
        "passed_checks": passed_checks,
        "total_checks": len(capture_checks),
        "capture_checks": capture_checks,
        "required_files": [{"path": path, "present": present} for path, present in required_files.items()],
        "phases": phases,
        "blocked_claims": BLOCKED_CLAIMS,
        "summary": {
            "benchmark_sessions": benchmark_summary.get("session_count", 0),
            "feedback_weeks": len(feedback_by_week),
            "retest_comparisons": retest_guard.get("comparison_count", 0),
            "pilot_feedback_entries": len(pilot_feedback_entries),
            "evidence_sources": evidence_library.get("source_count", 0),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def validation_readiness_markdown(matrix: dict[str, Any]) -> str:
    """Export Validation Readiness Matrix as Markdown."""

    lines = [
        "# SportRx Validation Readiness Matrix",
        "",
        f"- Status: {matrix['status']}",
        f"- Current validation claim: {matrix['current_validation_claim']}",
        f"- Capture checks: {matrix['passed_checks']} / {matrix['total_checks']}",
        f"- Next action: {matrix['next_action']}",
        f"- Claim boundary: {matrix['claim_boundary']}",
        "",
        "## Capture Checks",
    ]
    for check in matrix["capture_checks"]:
        status = "pass" if check["passed"] else "needs_review"
        lines.append(f"- [{status}] {check['label']}: {check['detail']}")

    lines.extend(["", "## Validation Phases"])
    for phase in matrix["phases"]:
        lines.extend(
            [
                f"### {phase['label']}",
                f"- Status: {phase['status']}",
                f"- Target sample: {phase['target_sample']}",
                f"- Allowed claim after completion: {phase['allowed_claim']}",
                f"- Evidence gap: {phase['evidence_gap']}",
            ]
        )

    lines.extend(["", "## Blocked Claims"])
    for claim in matrix["blocked_claims"]:
        lines.append(f"- {claim}")
    return "\n".join(lines) + "\n"
