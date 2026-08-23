"""Artifact catalog for SportRx export bundles."""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Artifact Catalog explains local export files for review handoff only. It "
    "does not validate SportRx, score performance, predict outcomes, or provide "
    "medical clearance."
)


ARTIFACT_METADATA = {
    "reviewer_handoff_markdown": ("Start Here", "Open first", "One-page reviewer guide for run, demo, export, and claim boundaries."),
    "release_candidate_summary_markdown": ("Start Here", "Open first", "One-page release candidate status, run commands, open-first artifacts, and blocked claims."),
    "first_run_guide_markdown": ("Start Here", "Open first", "Reviewer onboarding and first-use path."),
    "terminology_markdown": ("Start Here", "Open first", "Chinese-first terminology contract for retained English sport-science and product terms."),
    "demo_experience_markdown": ("Start Here", "Open first", "First-screen demo experience map for guided review, trust anchors, and blocked impressions."),
    "guided_review_markdown": ("Start Here", "Open first", "Guided review checklist for scenario choice, walkthrough progress, next page, exports, and Release QA."),
    "input_ledger_markdown": ("Start Here", "Open first", "Explains every collected, missing, legacy, and ignored input."),
    "quick_match_intake_contract_markdown": ("Start Here", "Open before Quick Match", "Explains why Quick Match asks direct numeric behavior fields and excludes subjective ratings or measured tests."),
    "quick_match_lab_intake_sheet_markdown": ("Start Here", "Open before Quick Match", "Direct-number intake sheet for age, recent behavior, constraints, and Not tested boundaries."),
    "intake_precision_markdown": ("Start Here", "Open first", "Audits input measurability, collection type, output role, and user-facing boundaries."),
    "measurement_schema_registry_markdown": ("Start Here", "Open first", "Documents local data objects, required fields, export coverage, and claim boundaries."),
    "evidence_library_markdown": ("Start Here", "Open first", "Browsable local evidence source index with tiers, product use, and limits."),
    "evidence_coverage_markdown": ("Start Here", "Open first", "Summarizes rule-evidence coverage, allowed/explain-only/blocked claims, and required evidence files."),
    "session_quality_review_markdown": ("Start Here", "Open first", "Whole-session gate review for measurement depth, feedback, retest, evidence, and output readiness."),
    "validation_readiness_markdown": ("Start Here", "Open first", "Validation phase matrix showing current allowed claims and missing real-data evidence."),
    "self_use_protocol_markdown": ("Start Here", "Before self-use", "Four-week Phase 0 protocol for builder self-use, baseline, feedback, retest, and claim boundaries."),
    "measurement_timeline_markdown": ("Start Here", "Open first", "Visual status of the full measurement loop."),
    "page_health_matrix_markdown": ("Start Here", "Open first", "Page-by-page product responsibility, success signal, evidence, and blocked-claim matrix."),
    "open_source_integration_markdown": ("Start Here", "Open first", "GitHub comparable-product lessons adopted, deferred, and rejected."),
    "protocol_markdown": ("Measurement", "Before testing", "Repeatable benchmark protocol."),
    "benchmark_worksheet_markdown": ("Measurement", "Before testing", "Printable test-day data-capture worksheet."),
    "test_day_brief_markdown": ("Measurement", "Before testing", "Operator checklist for test day."),
    "test_day_command_board_markdown": ("Measurement", "During testing", "First-screen command board for preflight, component tests, raw recording, log handoff, and retest anchor."),
    "test_session_operator_markdown": ("Measurement", "During testing", "Step-by-step benchmark operator mode for local test execution."),
    "lab_readiness_markdown": ("Measurement", "Before testing", "Safety, equipment, measurement, log, and retest state."),
    "measurement_intake_matrix_markdown": ("Measurement", "After testing", "Measured versus Not tested component matrix with provenance and next measurement actions."),
    "measurement_intake_matrix_csv": ("Raw Data", "After testing", "Spreadsheet-friendly measured versus Not tested component matrix."),
    "protocol_source_guide_markdown": ("Measurement", "Before testing", "Protocol-source presets and boundaries for Station and Work capacity protocol scores."),
    "benchmark_log_entry_contract_markdown": ("Measurement", "During testing", "Component-specific Benchmark Log fields, units, import policies, and not-allowed inferences."),
    "protocol_deviation_markdown": ("Measurement", "After testing", "Review of substitutions, missing RPE/equipment context, and retest protocol consistency."),
    "benchmark_log_json": ("Raw Data", "After testing", "Structured benchmark session data."),
    "benchmark_log_csv": ("Raw Data", "After testing", "Spreadsheet-friendly benchmark session data."),
    "training_profile_markdown": ("Training", "After measurement", "Current measured picture and handoff boundaries."),
    "training_block_markdown": ("Training", "After measurement", "4-week starter training block if gates allow it."),
    "feedback_dashboard_markdown": ("Feedback", "After training", "Weekly completion, RPE, and retest dashboard."),
    "retest_interpretation_markdown": ("Feedback", "After retest", "Guardrail for whether raw retest changes have comparable protocol context."),
    "launch_readiness_markdown": ("Release", "Before sharing", "Public-demo readiness report."),
    "runtime_doctor_markdown": ("Release", "Before sharing", "Local runtime and launch readiness."),
    "demo_runbook_markdown": ("Release", "Before sharing", "Guided reviewer script."),
    "demo_scenario_matrix_markdown": ("Release", "Before sharing", "Side-by-side synthetic scenario comparison for reviewers."),
    "reviewer_session_plan_markdown": ("Release", "Before sharing", "Time-boxed 3/8/12-minute reviewer tracks with pages, artifacts, and guardrails."),
    "pilot_feedback_prompt_markdown": ("Pilot", "During review", "Questions for collecting structured reviewer feedback."),
    "alpha_dataset_dictionary_markdown": ("Pilot", "Before alpha", "Data dictionary for 5-10 participant alpha data capture."),
    "alpha_participants_template_csv": ("Pilot", "Before alpha", "Header-only participant and test-window capture template."),
    "alpha_benchmark_sessions_template_csv": ("Pilot", "Before alpha", "Header-only raw benchmark component capture template."),
    "alpha_weekly_feedback_template_csv": ("Pilot", "Before alpha", "Header-only weekly plan-actual and RPE capture template."),
    "alpha_pilot_review_template_csv": ("Pilot", "Before alpha", "Header-only alpha product-review feedback template."),
    "pilot_feedback_json": ("Pilot", "After review", "Structured local pilot feedback entries."),
    "pilot_feedback_markdown": ("Pilot", "After review", "Readable pilot feedback summary."),
    "session_snapshot_json": ("Restore", "Any time", "Restorable app state for local handoff."),
    "session_snapshot_markdown": ("Restore", "Any time", "Readable snapshot summary."),
    "manifest_json": ("Manifest", "Any time", "Machine-readable export manifest."),
}


def build_artifact_catalog(files: list[dict[str, Any]]) -> dict[str, Any]:
    """Build an audience-friendly catalog for export bundle artifacts."""

    items = []
    for index, artifact in enumerate(files, start=1):
        category, when_to_use, purpose = ARTIFACT_METADATA.get(
            artifact["id"],
            ("Other", "As needed", artifact.get("label", "Export artifact.")),
        )
        items.append(
            {
                "order": index,
                "id": artifact["id"],
                "filename": artifact["filename"],
                "label": artifact["label"],
                "mime": artifact["mime"],
                "category": category,
                "when_to_use": when_to_use,
                "purpose": purpose,
            }
        )

    categories = []
    for category in ["Start Here", "Measurement", "Raw Data", "Training", "Feedback", "Release", "Pilot", "Restore", "Manifest", "Other"]:
        grouped = [item for item in items if item["category"] == category]
        if grouped:
            categories.append({"category": category, "artifact_count": len(grouped), "items": grouped})

    return {
        "schema": "sportrx.artifact_catalog",
        "schema_version": "0.1",
        "artifact_count": len(items),
        "categories": categories,
        "items": items,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def artifact_catalog_markdown(catalog: dict[str, Any]) -> str:
    """Export the artifact catalog as Markdown."""

    lines = [
        "# SportRx Artifact Catalog",
        "",
        f"- Artifacts: {catalog['artifact_count']}",
        f"- Claim boundary: {catalog['claim_boundary']}",
        "",
        "## Catalog",
    ]
    for group in catalog["categories"]:
        lines.extend(["", f"### {group['category']}"])
        for item in group["items"]:
            lines.append(
                f"- `{item['filename']}` - {item['label']} ({item['when_to_use']}): {item['purpose']}"
            )
    return "\n".join(lines) + "\n"
