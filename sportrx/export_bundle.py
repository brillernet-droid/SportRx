"""Export bundle assembly for SportRx review and pilot use."""

from __future__ import annotations

import json
from typing import Any

from .alpha_dataset_template import alpha_dataset_csv_templates, alpha_dataset_dictionary_markdown, build_alpha_dataset_template
from .artifact_catalog import artifact_catalog_markdown, build_artifact_catalog
from .benchmark_log import (
    benchmark_log_entry_contract_markdown,
    build_benchmark_log_entry_contract,
    export_sessions_csv,
    export_sessions_json,
    summarize_benchmark_sessions,
)
from .benchmark_protocol import get_benchmark_protocol, protocol_markdown
from .benchmark_worksheet import benchmark_worksheet_markdown, build_benchmark_worksheet
from .demo_runbook import build_demo_runbook, demo_runbook_markdown
from .demo_experience import build_demo_experience_console, demo_experience_markdown
from .demo_scenario_matrix import build_demo_scenario_matrix, demo_scenario_matrix_markdown
from .demo_scenarios import build_demo_scenarios
from .evidence_coverage import build_evidence_coverage, evidence_coverage_markdown
from .evidence_library import build_evidence_library, evidence_library_markdown
from .feedback_loop import build_feedback_dashboard, feedback_dashboard_markdown
from .first_run_guide import build_first_run_guide, first_run_guide_markdown
from .guided_review import build_guided_review_console, guided_review_markdown
from .input_ledger import build_input_ledger, input_ledger_markdown
from .intake_precision import build_intake_precision_audit, intake_precision_markdown
from .lab_readiness import build_lab_readiness_console, lab_readiness_markdown
from .launch_readiness import build_launch_readiness, launch_readiness_markdown
from .measurement_timeline import build_measurement_timeline, measurement_timeline_markdown
from .open_source_integration import build_open_source_integration_console, open_source_integration_markdown
from .page_health import build_page_health_matrix, page_health_matrix_markdown
from .performance_lab import assess_hybrid_performance, measurement_intake_matrix_csv, measurement_intake_matrix_markdown
from .pilot_feedback import export_pilot_feedback_json, pilot_feedback_markdown, pilot_feedback_prompt_markdown
from .pilot_feedback import build_pilot_review_console
from .protocol_deviation import build_protocol_deviation_review, protocol_deviation_markdown
from .protocol_source import build_protocol_source_guide, protocol_source_guide_markdown
from .public_beta_readiness import build_public_beta_readiness, public_beta_readiness_markdown
from .quick_match import (
    build_quick_match_intake_contract,
    build_quick_match_lab_intake_sheet,
    quick_match_intake_contract_markdown,
    quick_match_lab_intake_sheet_markdown,
)
from .release_candidate_summary import build_release_candidate_summary, release_candidate_summary_markdown
from .release_package import build_release_package_manifest
from .report import build_training_profile_report, report_markdown
from .reviewer_handoff import build_reviewer_handoff, reviewer_handoff_markdown
from .reviewer_session_plan import build_reviewer_session_plan, reviewer_session_plan_markdown
from .retest_interpretation import build_retest_interpretation_guard, retest_interpretation_markdown
from .runtime_doctor import build_runtime_doctor, runtime_doctor_markdown
from .schema_registry import build_measurement_schema_registry, measurement_schema_registry_markdown
from .self_use_protocol import build_self_use_protocol, self_use_protocol_markdown
from .session_snapshot import build_session_snapshot, session_snapshot_json, session_snapshot_markdown
from .session_quality_review import build_session_quality_review, session_quality_review_markdown
from .test_day_brief import build_test_day_brief, test_day_brief_markdown
from .test_session_operator import (
    build_test_day_command_board,
    build_test_session_operator,
    test_day_command_board_markdown,
    test_session_operator_markdown,
)
from .terminology import build_terminology_guide, terminology_markdown
from .training_block import build_training_block, training_block_markdown
from .validation_readiness import build_validation_readiness_matrix, validation_readiness_markdown
from .walkthrough import build_walkthrough


CLAIM_BOUNDARY = (
    "Export bundles package user-owned SportRx prototype outputs. They do not "
    "create validation data, athlete norms, predictions, or medical clearance."
)


def build_export_bundle(
    profile: dict[str, Any],
    passport: dict[str, Any],
    plan: dict[str, Any],
    benchmark_sessions: list[dict[str, Any]],
    feedback_by_week: dict[int, dict[str, Any]],
    evidence_files_present: dict[str, bool] | None = None,
    root: str | None = None,
    pilot_feedback_entries: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a list of exportable SportRx artifacts."""

    benchmark_summary = summarize_benchmark_sessions(benchmark_sessions)
    report = build_training_profile_report(passport, benchmark_summary)
    block = build_training_block(passport, plan, feedback_by_week)
    dashboard = build_feedback_dashboard(plan, feedback_by_week, benchmark_sessions)
    retest_guard = build_retest_interpretation_guard(benchmark_sessions)
    lab_readiness = build_lab_readiness_console(profile, passport, benchmark_summary)
    lab_result = assess_hybrid_performance(profile)
    measurement_intake_matrix = lab_result["measurement_intake_matrix"]
    protocol_source_guide = build_protocol_source_guide(profile)
    benchmark_log_entry_contract = build_benchmark_log_entry_contract(profile.get("equipment_access", []))
    protocol_deviation = build_protocol_deviation_review(benchmark_sessions)
    protocol = get_benchmark_protocol(profile.get("equipment_access", []))
    worksheet = build_benchmark_worksheet(profile.get("equipment_access", []))
    test_day_brief = build_test_day_brief(profile.get("equipment_access", []))
    test_operator = build_test_session_operator(
        profile.get("equipment_access", []),
        safety_gate_status=passport.get("safety_gate", {}).get("status"),
    )
    test_day_command_board = build_test_day_command_board(test_operator)
    launch = build_launch_readiness(
        profile,
        passport,
        plan,
        benchmark_sessions,
        feedback_by_week,
        evidence_files_present or {},
        root=root,
    )
    runbook = build_demo_runbook(launch)
    scenario_matrix = build_demo_scenario_matrix()
    walkthrough = build_walkthrough(passport, benchmark_summary, dashboard)
    timeline = build_measurement_timeline(walkthrough)
    page_health = build_page_health_matrix(walkthrough)
    open_source = build_open_source_integration_console()
    runtime = build_runtime_doctor(root or ".")
    pilot_feedback_entries = pilot_feedback_entries or []
    pilot_review = build_pilot_review_console(pilot_feedback_entries)
    package_manifest = build_release_package_manifest(root or ".")
    public_beta = build_public_beta_readiness(
        {"status": launch["qa_status"], "passed_checks": 1 if launch["qa_status"] != "needs_review" else 0, "total_checks": 1},
        launch,
        runtime,
        package_manifest,
        runbook,
        evidence_files_present or {},
        pilot_review,
    )
    snapshot = build_session_snapshot(profile, benchmark_sessions, feedback_by_week, pilot_feedback_entries)
    first_run = build_first_run_guide(passport, benchmark_sessions, feedback_by_week, pilot_feedback_entries)
    terminology = build_terminology_guide()
    input_ledger = build_input_ledger(profile)
    quick_match_contract = build_quick_match_intake_contract(profile)
    quick_match_lab_sheet = build_quick_match_lab_intake_sheet(profile)
    intake_precision = build_intake_precision_audit(profile)
    schema_registry = build_measurement_schema_registry()
    session_quality = build_session_quality_review(
        profile,
        passport,
        plan,
        benchmark_sessions,
        feedback_by_week,
        evidence_files_present or {},
        root or ".",
    )
    demo_experience = build_demo_experience_console(
        first_run,
        launch,
        session_quality,
        terminology,
        open_source,
    )
    guided_review = build_guided_review_console(walkthrough, first_run, launch, scenario_matrix)
    validation_readiness = build_validation_readiness_matrix(
        profile,
        passport,
        plan,
        benchmark_sessions,
        feedback_by_week,
        pilot_feedback_entries,
        root or ".",
    )
    self_use_protocol = build_self_use_protocol(validation_readiness, profile)
    session_plan = build_reviewer_session_plan(first_run, scenario_matrix, runbook)
    evidence_library = build_evidence_library(root or ".")
    evidence_coverage = build_evidence_coverage(root or ".", evidence_files_present or None)
    alpha_dataset = build_alpha_dataset_template()
    alpha_csv_templates = alpha_dataset_csv_templates(alpha_dataset)

    files = [
        {
            "id": "first_run_guide_markdown",
            "label": "First Run Guide",
            "filename": "sportrx_first_run_guide.md",
            "mime": "text/markdown",
            "content": first_run_guide_markdown(first_run),
        },
        {
            "id": "terminology_markdown",
            "label": "Terminology Guide",
            "filename": "sportrx_terminology_guide.md",
            "mime": "text/markdown",
            "content": terminology_markdown(terminology),
        },
        {
            "id": "demo_experience_markdown",
            "label": "Demo Experience Console",
            "filename": "sportrx_demo_experience_console.md",
            "mime": "text/markdown",
            "content": demo_experience_markdown(demo_experience),
        },
        {
            "id": "guided_review_markdown",
            "label": "Guided Review Console",
            "filename": "sportrx_guided_review_console.md",
            "mime": "text/markdown",
            "content": guided_review_markdown(guided_review),
        },
        {
            "id": "input_ledger_markdown",
            "label": "Input Ledger",
            "filename": "sportrx_input_ledger.md",
            "mime": "text/markdown",
            "content": input_ledger_markdown(input_ledger),
        },
        {
            "id": "quick_match_intake_contract_markdown",
            "label": "Quick Match Intake Contract",
            "filename": "sportrx_quick_match_intake_contract.md",
            "mime": "text/markdown",
            "content": quick_match_intake_contract_markdown(quick_match_contract),
        },
        {
            "id": "quick_match_lab_intake_sheet_markdown",
            "label": "Quick Match Lab Intake Sheet",
            "filename": "sportrx_quick_match_lab_intake_sheet.md",
            "mime": "text/markdown",
            "content": quick_match_lab_intake_sheet_markdown(quick_match_lab_sheet),
        },
        {
            "id": "intake_precision_markdown",
            "label": "Intake Precision Audit",
            "filename": "sportrx_intake_precision_audit.md",
            "mime": "text/markdown",
            "content": intake_precision_markdown(intake_precision),
        },
        {
            "id": "measurement_schema_registry_markdown",
            "label": "Measurement Schema Registry",
            "filename": "sportrx_measurement_schema_registry.md",
            "mime": "text/markdown",
            "content": measurement_schema_registry_markdown(schema_registry),
        },
        {
            "id": "evidence_library_markdown",
            "label": "Evidence Library",
            "filename": "sportrx_evidence_library.md",
            "mime": "text/markdown",
            "content": evidence_library_markdown(evidence_library),
        },
        {
            "id": "evidence_coverage_markdown",
            "label": "Evidence Coverage",
            "filename": "sportrx_evidence_coverage.md",
            "mime": "text/markdown",
            "content": evidence_coverage_markdown(evidence_coverage),
        },
        {
            "id": "session_quality_review_markdown",
            "label": "Session Quality Review",
            "filename": "sportrx_session_quality_review.md",
            "mime": "text/markdown",
            "content": session_quality_review_markdown(session_quality),
        },
        {
            "id": "validation_readiness_markdown",
            "label": "Validation Readiness Matrix",
            "filename": "sportrx_validation_readiness_matrix.md",
            "mime": "text/markdown",
            "content": validation_readiness_markdown(validation_readiness),
        },
        {
            "id": "self_use_protocol_markdown",
            "label": "Phase 0 Self-Use Protocol",
            "filename": "sportrx_phase_0_self_use_protocol.md",
            "mime": "text/markdown",
            "content": self_use_protocol_markdown(self_use_protocol),
        },
        {
            "id": "measurement_timeline_markdown",
            "label": "Measurement Loop Timeline",
            "filename": "sportrx_measurement_timeline.md",
            "mime": "text/markdown",
            "content": measurement_timeline_markdown(timeline),
        },
        {
            "id": "page_health_matrix_markdown",
            "label": "Page Health Matrix",
            "filename": "sportrx_page_health_matrix.md",
            "mime": "text/markdown",
            "content": page_health_matrix_markdown(page_health),
        },
        {
            "id": "open_source_integration_markdown",
            "label": "Open-Source Integration Notes",
            "filename": "sportrx_open_source_integration.md",
            "mime": "text/markdown",
            "content": open_source_integration_markdown(open_source),
        },
        {
            "id": "protocol_markdown",
            "label": "Benchmark Protocol",
            "filename": "sportrx_hybrid_benchmark_protocol.md",
            "mime": "text/markdown",
            "content": protocol_markdown(protocol),
        },
        {
            "id": "benchmark_worksheet_markdown",
            "label": "Benchmark Worksheet",
            "filename": "sportrx_benchmark_worksheet.md",
            "mime": "text/markdown",
            "content": benchmark_worksheet_markdown(worksheet),
        },
        {
            "id": "test_day_brief_markdown",
            "label": "Test-Day Brief",
            "filename": "sportrx_test_day_brief.md",
            "mime": "text/markdown",
            "content": test_day_brief_markdown(test_day_brief),
        },
        {
            "id": "test_day_command_board_markdown",
            "label": "Test-Day Command Board",
            "filename": "sportrx_test_day_command_board.md",
            "mime": "text/markdown",
            "content": test_day_command_board_markdown(test_day_command_board),
        },
        {
            "id": "test_session_operator_markdown",
            "label": "Test Session Operator",
            "filename": "sportrx_test_session_operator.md",
            "mime": "text/markdown",
            "content": test_session_operator_markdown(test_operator),
        },
        {
            "id": "lab_readiness_markdown",
            "label": "Lab Readiness Console",
            "filename": "sportrx_lab_readiness_console.md",
            "mime": "text/markdown",
            "content": lab_readiness_markdown(lab_readiness),
        },
        {
            "id": "measurement_intake_matrix_markdown",
            "label": "Measurement Intake Matrix",
            "filename": "sportrx_measurement_intake_matrix.md",
            "mime": "text/markdown",
            "content": measurement_intake_matrix_markdown(measurement_intake_matrix),
        },
        {
            "id": "measurement_intake_matrix_csv",
            "label": "Measurement Intake Matrix CSV",
            "filename": "sportrx_measurement_intake_matrix.csv",
            "mime": "text/csv",
            "content": measurement_intake_matrix_csv(measurement_intake_matrix),
        },
        {
            "id": "protocol_source_guide_markdown",
            "label": "Protocol Source Guide",
            "filename": "sportrx_protocol_source_guide.md",
            "mime": "text/markdown",
            "content": protocol_source_guide_markdown(protocol_source_guide),
        },
        {
            "id": "benchmark_log_entry_contract_markdown",
            "label": "Benchmark Log Entry Contract",
            "filename": "sportrx_benchmark_log_entry_contract.md",
            "mime": "text/markdown",
            "content": benchmark_log_entry_contract_markdown(benchmark_log_entry_contract),
        },
        {
            "id": "protocol_deviation_markdown",
            "label": "Protocol Deviation Review",
            "filename": "sportrx_protocol_deviation_review.md",
            "mime": "text/markdown",
            "content": protocol_deviation_markdown(protocol_deviation),
        },
        {
            "id": "benchmark_log_json",
            "label": "Benchmark Log JSON",
            "filename": "sportrx_benchmark_log.json",
            "mime": "application/json",
            "content": export_sessions_json(benchmark_sessions),
        },
        {
            "id": "benchmark_log_csv",
            "label": "Benchmark Log CSV",
            "filename": "sportrx_benchmark_log.csv",
            "mime": "text/csv",
            "content": export_sessions_csv(benchmark_sessions),
        },
        {
            "id": "training_profile_markdown",
            "label": "Training Profile Report",
            "filename": "sportrx_training_profile_report.md",
            "mime": "text/markdown",
            "content": report_markdown(report),
        },
        {
            "id": "training_block_markdown",
            "label": "4-Week Training Block",
            "filename": "sportrx_4_week_training_block.md",
            "mime": "text/markdown",
            "content": training_block_markdown(block),
        },
        {
            "id": "feedback_dashboard_markdown",
            "label": "Feedback Dashboard",
            "filename": "sportrx_feedback_dashboard.md",
            "mime": "text/markdown",
            "content": feedback_dashboard_markdown(dashboard),
        },
        {
            "id": "retest_interpretation_markdown",
            "label": "Retest Interpretation Guard",
            "filename": "sportrx_retest_interpretation_guard.md",
            "mime": "text/markdown",
            "content": retest_interpretation_markdown(retest_guard),
        },
        {
            "id": "launch_readiness_markdown",
            "label": "Launch Readiness",
            "filename": "sportrx_launch_readiness.md",
            "mime": "text/markdown",
            "content": launch_readiness_markdown(launch),
        },
        {
            "id": "public_beta_readiness_markdown",
            "label": "Public Beta Readiness",
            "filename": "sportrx_public_beta_readiness.md",
            "mime": "text/markdown",
            "content": public_beta_readiness_markdown(public_beta),
        },
        {
            "id": "runtime_doctor_markdown",
            "label": "Runtime Doctor",
            "filename": "sportrx_runtime_doctor.md",
            "mime": "text/markdown",
            "content": runtime_doctor_markdown(runtime),
        },
        {
            "id": "demo_runbook_markdown",
            "label": "Demo Runbook",
            "filename": "sportrx_demo_runbook.md",
            "mime": "text/markdown",
            "content": demo_runbook_markdown(runbook),
        },
        {
            "id": "demo_scenario_matrix_markdown",
            "label": "Demo Scenario Matrix",
            "filename": "sportrx_demo_scenario_matrix.md",
            "mime": "text/markdown",
            "content": demo_scenario_matrix_markdown(scenario_matrix),
        },
        {
            "id": "reviewer_session_plan_markdown",
            "label": "Reviewer Session Plan",
            "filename": "sportrx_reviewer_session_plan.md",
            "mime": "text/markdown",
            "content": reviewer_session_plan_markdown(session_plan),
        },
        {
            "id": "pilot_feedback_prompt_markdown",
            "label": "Pilot Feedback Prompt",
            "filename": "sportrx_pilot_feedback_prompt.md",
            "mime": "text/markdown",
            "content": pilot_feedback_prompt_markdown(),
        },
        {
            "id": "alpha_dataset_dictionary_markdown",
            "label": "Alpha Dataset Dictionary",
            "filename": "sportrx_alpha_dataset_dictionary.md",
            "mime": "text/markdown",
            "content": alpha_dataset_dictionary_markdown(alpha_dataset),
        },
        {
            "id": "alpha_participants_template_csv",
            "label": "Alpha Participants Template CSV",
            "filename": "sportrx_alpha_participants_template.csv",
            "mime": "text/csv",
            "content": alpha_csv_templates["participants"],
        },
        {
            "id": "alpha_benchmark_sessions_template_csv",
            "label": "Alpha Benchmark Sessions Template CSV",
            "filename": "sportrx_alpha_benchmark_sessions_template.csv",
            "mime": "text/csv",
            "content": alpha_csv_templates["benchmark_sessions"],
        },
        {
            "id": "alpha_weekly_feedback_template_csv",
            "label": "Alpha Weekly Feedback Template CSV",
            "filename": "sportrx_alpha_weekly_feedback_template.csv",
            "mime": "text/csv",
            "content": alpha_csv_templates["weekly_feedback"],
        },
        {
            "id": "alpha_pilot_review_template_csv",
            "label": "Alpha Pilot Review Template CSV",
            "filename": "sportrx_alpha_pilot_review_template.csv",
            "mime": "text/csv",
            "content": alpha_csv_templates["pilot_review"],
        },
        {
            "id": "pilot_feedback_json",
            "label": "Pilot Feedback JSON",
            "filename": "sportrx_pilot_feedback.json",
            "mime": "application/json",
            "content": export_pilot_feedback_json(pilot_feedback_entries),
        },
        {
            "id": "pilot_feedback_markdown",
            "label": "Pilot Feedback Markdown",
            "filename": "sportrx_pilot_feedback.md",
            "mime": "text/markdown",
            "content": pilot_feedback_markdown(pilot_feedback_entries),
        },
        {
            "id": "session_snapshot_json",
            "label": "Session Snapshot JSON",
            "filename": "sportrx_session_snapshot.json",
            "mime": "application/json",
            "content": session_snapshot_json(snapshot),
        },
        {
            "id": "session_snapshot_markdown",
            "label": "Session Snapshot Markdown",
            "filename": "sportrx_session_snapshot.md",
            "mime": "text/markdown",
            "content": session_snapshot_markdown(snapshot),
        },
    ]
    release_candidate = build_release_candidate_summary(
        qa={
            "status": launch["qa_status"],
            "passed_checks": 1 if launch["qa_status"] != "needs_review" else 0,
            "total_checks": 1,
        },
        launch=launch,
        runtime=runtime,
        package_manifest=package_manifest,
        public_beta=public_beta,
        export_file_count=len(files) + 4,
        review_pack_file_count=len(files) + 4,
    )
    files.insert(
        0,
        {
            "id": "release_candidate_summary_markdown",
            "label": "Release Candidate Summary",
            "filename": "sportrx_release_candidate_summary.md",
            "mime": "text/markdown",
            "content": release_candidate_summary_markdown(release_candidate),
        },
    )
    handoff_seed_catalog = build_artifact_catalog(files)
    handoff = build_reviewer_handoff(runtime, build_demo_scenarios(), handoff_seed_catalog, launch)
    files.insert(
        0,
        {
            "id": "reviewer_handoff_markdown",
            "label": "Reviewer Handoff",
            "filename": "sportrx_reviewer_handoff.md",
            "mime": "text/markdown",
            "content": reviewer_handoff_markdown(handoff),
        },
    )
    catalog = build_artifact_catalog(files)
    files.insert(
        0,
        {
            "id": "artifact_catalog_markdown",
            "label": "Artifact Catalog",
            "filename": "sportrx_artifact_catalog.md",
            "mime": "text/markdown",
            "content": artifact_catalog_markdown(catalog),
        },
    )
    manifest = {
        "schema": "sportrx.export_bundle",
        "schema_version": "0.1",
        "artifact_count": len(files),
        "artifacts": [
            {
                "id": item["id"],
                "label": item["label"],
                "filename": item["filename"],
                "mime": item["mime"],
            }
            for item in files
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    files.insert(
        0,
        {
            "id": "manifest_json",
            "label": "Export Manifest",
            "filename": "sportrx_export_manifest.json",
            "mime": "application/json",
            "content": json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True),
        },
    )
    return {
        "schema": "sportrx.export_bundle",
        "schema_version": "0.1",
        "files": files,
        "manifest": manifest,
        "claim_boundary": CLAIM_BOUNDARY,
    }
