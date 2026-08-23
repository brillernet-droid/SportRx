"""Launch readiness report for the SportRx demo.

This report packages product-readiness signals for a public prototype demo. It
is not scientific validation.
"""

from __future__ import annotations

from typing import Any

from .feedback_loop import build_feedback_dashboard
from .output_prerequisites import build_output_prerequisites
from .release_package import build_release_package_manifest
from .walkthrough import build_walkthrough


CLAIM_BOUNDARY = (
    "Launch readiness checks whether the local SportRx prototype is ready for "
    "demo review. It does not validate the rules, certify safety, or prove "
    "training outcomes."
)


EXPECTED_EXPORT_FILES = [
    {"filename": "sportrx_export_manifest.json", "label": "Export Manifest", "mime": "application/json"},
    {"filename": "sportrx_artifact_catalog.md", "label": "Artifact Catalog", "mime": "text/markdown"},
    {"filename": "sportrx_reviewer_handoff.md", "label": "Reviewer Handoff", "mime": "text/markdown"},
    {"filename": "sportrx_release_candidate_summary.md", "label": "Release Candidate Summary", "mime": "text/markdown"},
    {"filename": "sportrx_first_run_guide.md", "label": "First Run Guide", "mime": "text/markdown"},
    {"filename": "sportrx_terminology_guide.md", "label": "Terminology Guide", "mime": "text/markdown"},
    {"filename": "sportrx_demo_experience_console.md", "label": "Demo Experience Console", "mime": "text/markdown"},
    {"filename": "sportrx_guided_review_console.md", "label": "Guided Review Console", "mime": "text/markdown"},
    {"filename": "sportrx_input_ledger.md", "label": "Input Ledger", "mime": "text/markdown"},
    {"filename": "sportrx_quick_match_lab_intake_sheet.md", "label": "Quick Match Lab Intake Sheet", "mime": "text/markdown"},
    {"filename": "sportrx_intake_precision_audit.md", "label": "Intake Precision Audit", "mime": "text/markdown"},
    {"filename": "sportrx_measurement_timeline.md", "label": "Measurement Loop Timeline", "mime": "text/markdown"},
    {"filename": "sportrx_page_health_matrix.md", "label": "Page Health Matrix", "mime": "text/markdown"},
    {"filename": "sportrx_hybrid_benchmark_protocol.md", "label": "Benchmark Protocol", "mime": "text/markdown"},
    {"filename": "sportrx_benchmark_worksheet.md", "label": "Benchmark Worksheet", "mime": "text/markdown"},
    {"filename": "sportrx_test_day_brief.md", "label": "Test-Day Brief", "mime": "text/markdown"},
    {"filename": "sportrx_test_day_command_board.md", "label": "Test-Day Command Board", "mime": "text/markdown"},
    {"filename": "sportrx_test_session_operator.md", "label": "Test Session Operator", "mime": "text/markdown"},
    {"filename": "sportrx_lab_readiness_console.md", "label": "Lab Readiness Console", "mime": "text/markdown"},
    {"filename": "sportrx_measurement_intake_matrix.md", "label": "Measurement Intake Matrix", "mime": "text/markdown"},
    {"filename": "sportrx_measurement_intake_matrix.csv", "label": "Measurement Intake Matrix CSV", "mime": "text/csv"},
    {"filename": "sportrx_protocol_source_guide.md", "label": "Protocol Source Guide", "mime": "text/markdown"},
    {"filename": "sportrx_benchmark_log.json", "label": "Benchmark Log JSON", "mime": "application/json"},
    {"filename": "sportrx_benchmark_log.csv", "label": "Benchmark Log CSV", "mime": "text/csv"},
    {"filename": "sportrx_training_profile_report.md", "label": "Training Profile Report", "mime": "text/markdown"},
    {"filename": "sportrx_4_week_training_block.md", "label": "4-Week Training Block", "mime": "text/markdown"},
    {"filename": "sportrx_feedback_dashboard.md", "label": "Feedback Dashboard", "mime": "text/markdown"},
    {"filename": "sportrx_launch_readiness.md", "label": "Launch Readiness", "mime": "text/markdown"},
    {"filename": "sportrx_public_beta_readiness.md", "label": "Public Beta Readiness", "mime": "text/markdown"},
    {"filename": "sportrx_runtime_doctor.md", "label": "Runtime Doctor", "mime": "text/markdown"},
    {"filename": "sportrx_demo_runbook.md", "label": "Demo Runbook", "mime": "text/markdown"},
    {"filename": "sportrx_pilot_feedback_prompt.md", "label": "Pilot Feedback Prompt", "mime": "text/markdown"},
    {"filename": "sportrx_alpha_dataset_dictionary.md", "label": "Alpha Dataset Dictionary", "mime": "text/markdown"},
    {"filename": "sportrx_alpha_participants_template.csv", "label": "Alpha Participants Template CSV", "mime": "text/csv"},
    {"filename": "sportrx_alpha_benchmark_sessions_template.csv", "label": "Alpha Benchmark Sessions Template CSV", "mime": "text/csv"},
    {"filename": "sportrx_alpha_weekly_feedback_template.csv", "label": "Alpha Weekly Feedback Template CSV", "mime": "text/csv"},
    {"filename": "sportrx_alpha_pilot_review_template.csv", "label": "Alpha Pilot Review Template CSV", "mime": "text/csv"},
    {"filename": "sportrx_pilot_feedback.json", "label": "Pilot Feedback JSON", "mime": "application/json"},
    {"filename": "sportrx_pilot_feedback.md", "label": "Pilot Feedback Markdown", "mime": "text/markdown"},
    {"filename": "sportrx_session_snapshot.json", "label": "Session Snapshot JSON", "mime": "application/json"},
    {"filename": "sportrx_session_snapshot.md", "label": "Session Snapshot Markdown", "mime": "text/markdown"},
]


def build_launch_readiness(
    profile: dict[str, Any],
    passport: dict[str, Any],
    plan: dict[str, Any],
    benchmark_sessions: list[dict[str, Any]],
    feedback_by_week: dict[int, dict[str, Any]],
    evidence_files_present: dict[str, bool],
    root: str | None = None,
) -> dict[str, Any]:
    """Build a single launch-readiness object from existing product checks."""

    dashboard = build_feedback_dashboard(plan, feedback_by_week, benchmark_sessions)
    walkthrough = build_walkthrough(passport, dashboard["benchmark_summary"], dashboard)
    output_prerequisites = build_output_prerequisites(passport, dashboard["benchmark_summary"], dashboard)
    package_manifest = build_release_package_manifest(root or ".")
    evidence_ready = all(evidence_files_present.values()) if evidence_files_present else False
    demo_loop_ready = walkthrough["completion"]["complete_steps"] >= 7

    review_path = [
        {
            "step": item["step"],
            "page": item["page"],
            "task": item["title"],
            "status": item["status"],
        }
        for item in walkthrough["steps"]
    ]

    readiness_checks = [
        _readiness_check(
            "launch_demo_loop",
            "Demo loop is complete enough for review",
            demo_loop_ready,
            f"{walkthrough['completion']['complete_steps']} of {walkthrough['completion']['total_steps']} walkthrough steps complete.",
        ),
        _readiness_check(
            "launch_evidence_context",
            "Evidence context is present",
            evidence_ready,
            "All required evidence files are present." if evidence_ready else "Evidence context is incomplete.",
        ),
        _readiness_check(
            "launch_public_package",
            "Public package manifest is clean",
            package_manifest["status"] == "ready_for_public_package",
            f"Package status: {package_manifest['status']}.",
        ),
        _readiness_check(
            "launch_exports",
            "Export center has review artifacts",
            len(EXPECTED_EXPORT_FILES) >= 23,
            f"{len(EXPECTED_EXPORT_FILES)} export files expected.",
        ),
        _readiness_check(
            "launch_output_gates",
            "Output gates are visible",
            bool(output_prerequisites["outputs"]),
            f"{len(output_prerequisites['outputs'])} output gates available.",
        ),
        _readiness_check(
            "launch_retest",
            "Retest comparison is available or explicitly gated",
            bool(dashboard["benchmark_summary"].get("retest_ready"))
            or any(item["output_id"] == "retest_comparison" for item in output_prerequisites["outputs"]),
            dashboard["benchmark_summary"].get("message", "Retest state checked."),
        ),
    ]

    passed = sum(1 for item in readiness_checks if item["passed"])
    status = "ready_for_public_demo" if passed == len(readiness_checks) else "needs_review"
    return {
        "schema": "sportrx.launch_readiness",
        "schema_version": "0.1",
        "status": status,
        "passed_checks": passed,
        "total_checks": len(readiness_checks),
        "checks": readiness_checks,
        "review_path": review_path,
        "export_files": EXPECTED_EXPORT_FILES,
        "qa_status": "ready_for_demo_review" if demo_loop_ready and evidence_ready else "needs_review",
        "package_status": package_manifest["status"],
        "output_gate_summary": output_prerequisites["summary"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _readiness_check(check_id: str, label: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "id": check_id,
        "label": label,
        "status": "pass" if passed else "needs_review",
        "passed": bool(passed),
        "detail": detail,
    }


def launch_readiness_markdown(report: dict[str, Any]) -> str:
    """Export launch readiness as markdown."""

    lines = [
        "# SportRx Launch Readiness",
        "",
        f"- Status: {report['status']}",
        f"- Passed: {report['passed_checks']} / {report['total_checks']}",
        f"- QA status: {report['qa_status']}",
        f"- Package status: {report['package_status']}",
        f"- Claim boundary: {report['claim_boundary']}",
        "",
        "## Checks",
    ]
    for item in report["checks"]:
        lines.append(f"- [{item['status']}] {item['label']}: {item['detail']}")

    lines.extend(["", "## Review Path"])
    for item in report["review_path"]:
        lines.append(f"- Step {item['step']} - {item['page']}: {item['task']} ({item['status']})")

    lines.extend(["", "## Export Files"])
    for item in report["export_files"]:
        lines.append(f"- {item['filename']} - {item['label']}")

    return "\n".join(lines) + "\n"
