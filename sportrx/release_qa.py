"""Release QA checks for the SportRx prototype.

These checks are product-readiness checks, not scientific validation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .alpha_dataset_template import build_alpha_dataset_template
from .demo_experience import build_demo_experience_console
from .demo_scenario_matrix import build_demo_scenario_matrix
from .demo_scenarios import build_demo_scenarios
from .evidence_coverage import build_evidence_coverage
from .evidence_library import build_evidence_library
from .export_archive import build_review_pack_manifest, build_review_pack_zip
from .export_bundle import build_export_bundle
from .feedback_loop import build_feedback_dashboard
from .first_run_guide import build_first_run_guide
from .guided_review import build_guided_review_console
from .intake_precision import build_intake_precision_audit
from .lab_readiness import build_lab_readiness_console
from .launch_readiness import build_launch_readiness
from .open_source_integration import build_open_source_integration_console
from .output_prerequisites import build_output_prerequisites
from .page_health import build_page_health_matrix
from .performance_lab import assess_hybrid_performance
from .protocol_deviation import build_protocol_deviation_review
from .protocol_source import build_protocol_source_guide
from .quick_match import build_quick_match_intake_contract, build_quick_match_lab_intake_sheet
from .retest_interpretation import build_retest_interpretation_guard
from .runtime_doctor import build_runtime_doctor
from .self_use_protocol import build_self_use_protocol
from .session_quality_review import build_session_quality_review
from .terminology import build_terminology_guide
from .validation_readiness import build_validation_readiness_matrix
from .walkthrough import build_walkthrough


CLAIM_BOUNDARY = (
    "Release QA checks product completeness and claim boundaries only. Passing "
    "QA does not validate SportRx, create medical clearance, or prove outcomes."
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


REQUIRED_EVIDENCE_FILES = [
    "evidence/claim_policy.md",
    "evidence/rule_evidence_map.md",
    "evidence/validation_plan.md",
    "evidence/library/source_index.md",
]


def _check(check_id: str, label: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "id": check_id,
        "label": label,
        "status": "pass" if passed else "needs_review",
        "passed": bool(passed),
        "detail": detail,
    }


def build_release_qa(
    profile: dict[str, Any],
    passport: dict[str, Any],
    plan: dict[str, Any],
    benchmark_sessions: list[dict[str, Any]],
    feedback_by_week: dict[int, dict[str, Any]],
    evidence_files_present: dict[str, bool] | None = None,
) -> dict[str, Any]:
    """Build release-readiness checks for the current local prototype state."""

    dashboard = build_feedback_dashboard(plan, feedback_by_week, benchmark_sessions)
    bundle = build_export_bundle(profile, passport, plan, benchmark_sessions, feedback_by_week)
    archive_manifest = build_review_pack_manifest(bundle)
    archive_bytes = build_review_pack_zip(bundle)
    demo_scenarios = build_demo_scenarios()
    runtime = build_runtime_doctor(".")
    lab_readiness = build_lab_readiness_console(profile, passport, dashboard["benchmark_summary"])
    lab_result = assess_hybrid_performance(profile)
    measurement_intake_matrix = lab_result["measurement_intake_matrix"]
    protocol_source_guide = build_protocol_source_guide(profile)
    protocol_deviation = build_protocol_deviation_review(benchmark_sessions)
    retest_guard = build_retest_interpretation_guard(benchmark_sessions)
    walkthrough = build_walkthrough(passport, dashboard["benchmark_summary"], dashboard)
    page_health = build_page_health_matrix(walkthrough)
    output_prerequisites = build_output_prerequisites(passport, dashboard["benchmark_summary"], dashboard)
    quick_match_contract = build_quick_match_intake_contract(profile)
    quick_match_lab_sheet = build_quick_match_lab_intake_sheet(profile)
    intake_precision = build_intake_precision_audit(profile)
    evidence_files_present = evidence_files_present or {}
    evidence_library = build_evidence_library(PROJECT_ROOT)
    evidence_coverage = build_evidence_coverage(PROJECT_ROOT, evidence_files_present)
    session_quality = build_session_quality_review(
        profile,
        passport,
        plan,
        benchmark_sessions,
        feedback_by_week,
        evidence_files_present,
        PROJECT_ROOT,
    )
    validation_readiness = build_validation_readiness_matrix(
        profile,
        passport,
        plan,
        benchmark_sessions,
        feedback_by_week,
        [],
        PROJECT_ROOT,
    )
    self_use_protocol = build_self_use_protocol(validation_readiness, profile)
    alpha_dataset = build_alpha_dataset_template()
    terminology = build_terminology_guide()
    first_run = build_first_run_guide(passport, benchmark_sessions, feedback_by_week, [])
    launch = build_launch_readiness(profile, passport, plan, benchmark_sessions, feedback_by_week, evidence_files_present, PROJECT_ROOT)
    demo_experience = build_demo_experience_console(
        first_run,
        launch,
        session_quality,
        terminology,
        build_open_source_integration_console(),
    )
    guided_review = build_guided_review_console(walkthrough, first_run, launch, build_demo_scenario_matrix())

    checks = [
        _check(
            "qa_demo_loop",
            "Demo loop has measurements, training, feedback, and retest data",
            walkthrough["completion"]["complete_steps"] >= 7,
            f"{walkthrough['completion']['complete_steps']} of {walkthrough['completion']['total_steps']} walkthrough steps complete.",
        ),
        _check(
            "qa_export_bundle",
            "Export bundle contains all local review artifacts",
            len(bundle["files"]) >= 23,
            f"{len(bundle['files'])} files available for local download.",
        ),
        _check(
            "qa_runtime_doctor",
            "Runtime Doctor reports local run readiness",
            runtime["status"] == "ready_to_run_locally",
            f"Runtime status: {runtime['status']}.",
        ),
        _check(
            "qa_review_pack_zip",
            "Review Pack ZIP is buildable",
            len(archive_bytes) > 0 and archive_manifest["file_count"] == len(bundle["files"]),
            f"{archive_manifest['file_count']} files archived for review handoff.",
        ),
        _check(
            "qa_review_pack_integrity",
            "Review Pack payload has integrity checksums",
            archive_manifest["integrity_status"] == "ready_for_review_handoff",
            (
                f"{archive_manifest['integrity']['payload_file_count']} payload files hashed; "
                f"{archive_manifest['integrity']['passed_checks']} / "
                f"{archive_manifest['integrity']['total_checks']} integrity checks passed."
            ),
        ),
        _check(
            "qa_demo_scenarios",
            "Demo Scenario Library is available",
            len(demo_scenarios) >= 3,
            f"{len(demo_scenarios)} synthetic product-review scenarios available.",
        ),
        _check(
            "qa_claim_boundary",
            "Export bundle preserves claim boundaries",
            "predictions" in bundle["claim_boundary"] and "medical clearance" in bundle["claim_boundary"],
            bundle["claim_boundary"],
        ),
        _check(
            "qa_safety_boundary",
            "Safety Gate remains visible in product state",
            bool(passport.get("safety_gate", {}).get("status")),
            f"Safety Gate status: {passport.get('safety_gate', {}).get('status')}",
        ),
        _check(
            "qa_measurement_gate",
            "Targeted training is gated by measurement state",
            bool(passport.get("starter_path", {}).get("available")) == (
                int(passport.get("measured_performance_areas", {}).get("count", 0)) >= 2
            ),
            f"Measured performance areas: {passport.get('measured_performance_areas', {}).get('count', 0)}.",
        ),
        _check(
            "qa_metric_sources",
            "Visible outputs include metric source labels",
            bool(passport.get("metric_sources", {}).get("all_metrics")),
            f"{len(passport.get('metric_sources', {}).get('all_metrics', []))} metric source records available.",
        ),
        _check(
            "qa_lab_readiness_console",
            "Lab readiness console is available",
            bool(lab_readiness.get("cards")),
            f"Lab readiness status: {lab_readiness.get('status')}.",
        ),
        _check(
            "qa_measurement_intake_matrix",
            "Measurement intake matrix is available",
            (
                measurement_intake_matrix["schema"] == "sportrx.measurement_intake_matrix"
                and measurement_intake_matrix["summary"]["total"] >= 6
                and "does not create scores" in measurement_intake_matrix["claim_boundary"]
            ),
            (
                f"{measurement_intake_matrix['summary']['measured']} measured; "
                f"{measurement_intake_matrix['summary']['not_tested']} not tested; "
                f"status: {measurement_intake_matrix['status']}."
            ),
        ),
        _check(
            "qa_protocol_deviation_review",
            "Protocol deviation review is available",
            protocol_deviation["status"] != "no_benchmark_logs",
            f"{protocol_deviation['completed_component_count']} completed components; status: {protocol_deviation['status']}.",
        ),
        _check(
            "qa_retest_interpretation_guard",
            "Retest interpretation guard is available",
            retest_guard["status"] not in {"no_benchmark_logs", "waiting_for_retest"},
            f"{retest_guard['comparison_count']} retest comparisons; status: {retest_guard['status']}.",
        ),
        _check(
            "qa_plan_actual_reasons",
            "Feedback Loop includes plan-actual reason codes",
            bool(dashboard.get("plan_actual_reasons")),
            f"{len(dashboard.get('plan_actual_reasons', []))} weekly reason-code records available.",
        ),
        _check(
            "qa_output_prerequisites",
            "User-facing outputs expose prerequisite gates",
            bool(output_prerequisites.get("outputs")),
            f"{len(output_prerequisites.get('outputs', []))} output prerequisite records available.",
        ),
        _check(
            "qa_session_quality_review",
            "Whole-session quality review is available",
            bool(session_quality.get("gates")) and session_quality["status"] != "needs_review",
            f"{len(session_quality.get('gates', []))} quality gates; status: {session_quality.get('status')}.",
        ),
        _check(
            "qa_validation_readiness_matrix",
            "Validation readiness matrix is available",
            validation_readiness["current_validation_claim"] == "Prototype; not validated.",
            (
                f"{validation_readiness['passed_checks']} / {validation_readiness['total_checks']} "
                f"capture checks; claim: {validation_readiness['current_validation_claim']}"
            ),
        ),
        _check(
            "qa_self_use_protocol",
            "Phase 0 self-use protocol is available",
            (
                self_use_protocol["current_validation_claim"] == "Prototype; not validated."
                and self_use_protocol["duration_weeks"] == 4
                and bool(self_use_protocol.get("minimum_data_fields"))
            ),
            (
                f"{self_use_protocol['duration_weeks']}-week protocol; "
                f"claim: {self_use_protocol['current_validation_claim']}."
            ),
        ),
        _check(
            "qa_alpha_dataset_template",
            "Alpha dataset template is available without fake norms",
            (
                alpha_dataset["schema"] == "sportrx.alpha_dataset_template"
                and alpha_dataset["table_count"] == 4
                and "does not validate SportRx" in alpha_dataset["claim_boundary"]
                and any("do not impute averages" in rule for rule in alpha_dataset["minimum_rules"])
            ),
            f"{alpha_dataset['table_count']} header-only tables; status: {alpha_dataset['status']}.",
        ),
        _check(
            "qa_demo_scenario_matrix",
            "Demo scenario matrix is exportable",
            any(item["id"] == "demo_scenario_matrix_markdown" for item in bundle["files"]),
            "Demo scenario matrix helps reviewers choose the right synthetic product-review state.",
        ),
        _check(
            "qa_reviewer_session_plan",
            "Reviewer session plan is exportable",
            any(item["id"] == "reviewer_session_plan_markdown" for item in bundle["files"]),
            "Reviewer session plan provides time-boxed review tracks for external reviewers.",
        ),
        _check(
            "qa_pilot_feedback_prompt",
            "Pilot feedback prompt is exportable",
            any(item["id"] == "pilot_feedback_prompt_markdown" for item in bundle["files"]),
            "Pilot feedback prompt is included in the export bundle.",
        ),
        _check(
            "qa_alpha_dataset_template_exports",
            "Alpha dataset templates are exportable",
            all(
                artifact_id in {item["id"] for item in bundle["files"]}
                for artifact_id in {
                    "alpha_dataset_dictionary_markdown",
                    "alpha_participants_template_csv",
                    "alpha_benchmark_sessions_template_csv",
                    "alpha_weekly_feedback_template_csv",
                    "alpha_pilot_review_template_csv",
                }
            ),
            "Alpha dictionary and four header-only CSV templates are included.",
        ),
        _check(
            "qa_first_run_guide",
            "First-run guide is exportable",
            any(item["id"] == "first_run_guide_markdown" for item in bundle["files"]),
            "First-run guide is included for reviewers opening SportRx for the first time.",
        ),
        _check(
            "qa_terminology_guide",
            "Terminology guide is available",
            (
                terminology["schema"] == "sportrx.terminology_guide"
                and {"HYROX", "RPE", "Benchmark", "Not tested"}.issubset(
                    {item["term"] for item in terminology["terms"]}
                )
                and any(item["phrase"] == "medical clearance" for item in terminology["blocked_language"])
                and "does not validate SportRx" in terminology["claim_boundary"]
            ),
            (
                f"{terminology['term_count']} terms; "
                f"{terminology['blocked_phrase_count']} blocked phrases."
            ),
        ),
        _check(
            "qa_terminology_export",
            "Terminology guide is exportable",
            any(item["id"] == "terminology_markdown" for item in bundle["files"]),
            "Terminology Guide keeps language editions, shared terms, and blocked language reviewable.",
        ),
        _check(
            "qa_demo_experience_console",
            "Demo experience console is available",
            (
                demo_experience["schema"] == "sportrx.demo_experience_console"
                and demo_experience["status"] == "ready_for_guided_demo"
                and any("Not tested" in item for item in demo_experience["trust_anchors"])
                and any("AI coach" in item for item in demo_experience["blocked_impressions"])
                and "does not validate SportRx" in demo_experience["claim_boundary"]
            ),
            (
                f"{demo_experience['ready_cards']} / {demo_experience['total_cards']} "
                "first-screen experience cards ready."
            ),
        ),
        _check(
            "qa_demo_experience_export",
            "Demo experience console is exportable",
            any(item["id"] == "demo_experience_markdown" for item in bundle["files"]),
            "Demo Experience Console documents the guided first-screen review path.",
        ),
        _check(
            "qa_guided_review_console",
            "Guided review console is available",
            (
                guided_review["schema"] == "sportrx.guided_review_console"
                and guided_review["status"] == "ready_for_guided_review"
                and guided_review["progress_percent"] >= 80
                and any(item["target"] == "Release QA" for item in guided_review["quick_actions"])
                and "does not validate SportRx" in guided_review["claim_boundary"]
            ),
            (
                f"{guided_review['ready_cards']} / {guided_review['total_cards']} "
                f"guided review cards ready; progress {guided_review['progress_percent']}%."
            ),
        ),
        _check(
            "qa_guided_review_export",
            "Guided review console is exportable",
            any(item["id"] == "guided_review_markdown" for item in bundle["files"]),
            "Guided Review Console documents scenario choice, next page, walkthrough progress, and Release QA handoff.",
        ),
        _check(
            "qa_reviewer_handoff",
            "Reviewer handoff is exportable",
            any(item["id"] == "reviewer_handoff_markdown" for item in bundle["files"]),
            "Reviewer handoff is included to explain run, demo, export, and claim boundaries.",
        ),
        _check(
            "qa_release_candidate_summary_export",
            "Release candidate summary is exportable",
            any(item["id"] == "release_candidate_summary_markdown" for item in bundle["files"]),
            "Release Candidate Summary is included as a one-page product handoff snapshot.",
        ),
        _check(
            "qa_input_ledger",
            "Input ledger is exportable",
            any(item["id"] == "input_ledger_markdown" for item in bundle["files"]),
            "Input ledger is included to explain collected, missing, legacy, and ignored inputs.",
        ),
        _check(
            "qa_quick_match_intake_contract",
            "Quick Match intake contract is available",
            (
                quick_match_contract["schema"] == "sportrx.quick_match_intake_contract"
                and quick_match_contract["status"] == "contract_ready"
                and quick_match_contract["required_numeric_fields"] >= 10
                and "background identity" in quick_match_contract["primary_message"]
                and "Quick Match does not use them" in quick_match_contract["excluded_measurement_policy"]
                and "does not validate SportRx" in quick_match_contract["claim_boundary"]
            ),
            (
                f"{quick_match_contract['group_count']} intake groups; "
                f"status: {quick_match_contract['status']}."
            ),
        ),
        _check(
            "qa_quick_match_intake_contract_export",
            "Quick Match intake contract is exportable",
            any(item["id"] == "quick_match_intake_contract_markdown" for item in bundle["files"]),
            "Quick Match Intake Contract is included to explain direct numeric intake and excluded measured tests.",
        ),
        _check(
            "qa_quick_match_lab_intake_sheet",
            "Quick Match Lab Intake Sheet is available",
            (
                quick_match_lab_sheet["schema"] == "sportrx.quick_match_lab_intake_sheet"
                and quick_match_lab_sheet["total_fields"] >= 10
                and "Not tested" in quick_match_lab_sheet["not_tested_policy"]
                and "does not measure performance" in quick_match_lab_sheet["primary_message"]
                and "not a validated assessment" in quick_match_lab_sheet["claim_boundary"]
            ),
            (
                f"{quick_match_lab_sheet['collected_fields']} / "
                f"{quick_match_lab_sheet['total_fields']} direct intake fields collected."
            ),
        ),
        _check(
            "qa_quick_match_lab_intake_sheet_export",
            "Quick Match Lab Intake Sheet is exportable",
            any(item["id"] == "quick_match_lab_intake_sheet_markdown" for item in bundle["files"]),
            "Quick Match Lab Intake Sheet is included as the direct-number self-report record.",
        ),
        _check(
            "qa_intake_precision_audit",
            "Intake precision audit is available",
            (
                intake_precision["schema"] == "sportrx.intake_precision_audit"
                and intake_precision["summary"]["direct_numeric_fields"] >= 8
                and "does not validate SportRx" in intake_precision["claim_boundary"]
            ),
            (
                f"{intake_precision['summary']['direct_numeric_collected']} / "
                f"{intake_precision['summary']['direct_numeric_fields']} direct numeric fields; "
                f"{intake_precision['summary']['measured_tests_recorded']} measured tests recorded."
            ),
        ),
        _check(
            "qa_intake_precision_export",
            "Intake precision audit is exportable",
            any(item["id"] == "intake_precision_markdown" for item in bundle["files"]),
            "Intake Precision Audit is included to separate direct numeric, measured, safety, context, and ignored inputs.",
        ),
        _check(
            "qa_artifact_catalog",
            "Artifact catalog is exportable",
            any(item["id"] == "artifact_catalog_markdown" for item in bundle["files"]),
            "Artifact catalog is included to explain review handoff files.",
        ),
        _check(
            "qa_schema_registry",
            "Measurement schema registry is exportable",
            any(item["id"] == "measurement_schema_registry_markdown" for item in bundle["files"]),
            "Measurement schema registry documents local data objects and export coverage.",
        ),
        _check(
            "qa_evidence_coverage",
            "Evidence coverage registry is available",
            evidence_coverage["status"] == "ready_for_release_review",
            f"{evidence_coverage['rule_count']} rules mapped; {evidence_coverage['required_files_present']} / {evidence_coverage['required_file_count']} required evidence files present.",
        ),
        _check(
            "qa_evidence_library",
            "Evidence library source index is available",
            evidence_library["status"] == "ready_for_review",
            f"{evidence_library['source_count']} sources across {evidence_library['topic_count']} topics.",
        ),
        _check(
            "qa_evidence_coverage_export",
            "Evidence coverage is exportable",
            any(item["id"] == "evidence_coverage_markdown" for item in bundle["files"]),
            "Evidence coverage is included to summarize rule statuses and blocked claims.",
        ),
        _check(
            "qa_evidence_library_export",
            "Evidence library is exportable",
            any(item["id"] == "evidence_library_markdown" for item in bundle["files"]),
            "Evidence library is included to summarize saved sources, tiers, product use, and limits.",
        ),
        _check(
            "qa_measurement_timeline",
            "Measurement timeline is exportable",
            any(item["id"] == "measurement_timeline_markdown" for item in bundle["files"]),
            "Measurement timeline is included in the export bundle.",
        ),
        _check(
            "qa_page_health_matrix",
            "Page health matrix is available",
            (
                page_health["schema"] == "sportrx.page_health_matrix"
                and page_health["page_count"] >= 12
                and "does not validate SportRx" in page_health["claim_boundary"]
            ),
            f"{page_health['page_count']} pages; status: {page_health['status']}.",
        ),
        _check(
            "qa_page_health_matrix_export",
            "Page health matrix is exportable",
            any(item["id"] == "page_health_matrix_markdown" for item in bundle["files"]),
            "Page Health Matrix is included to document page responsibilities and blocked claims.",
        ),
        _check(
            "qa_session_quality_review_export",
            "Session quality review is exportable",
            any(item["id"] == "session_quality_review_markdown" for item in bundle["files"]),
            "Session Quality Review summarizes data quality gates for reviewer handoff.",
        ),
        _check(
            "qa_validation_readiness_export",
            "Validation readiness matrix is exportable",
            any(item["id"] == "validation_readiness_markdown" for item in bundle["files"]),
            "Validation Readiness Matrix keeps validation claims separate from product readiness.",
        ),
        _check(
            "qa_self_use_protocol_export",
            "Phase 0 self-use protocol is exportable",
            any(item["id"] == "self_use_protocol_markdown" for item in bundle["files"]),
            "Phase 0 Self-Use Protocol turns the next validation step into a repeatable local process.",
        ),
        _check(
            "qa_open_source_integration_export",
            "Open-source integration notes are exportable",
            any(item["id"] == "open_source_integration_markdown" for item in bundle["files"]),
            "Open-source integration notes explain adopted, deferred, and rejected comparable-product patterns.",
        ),
        _check(
            "qa_runtime_doctor_export",
            "Runtime Doctor is exportable",
            any(item["id"] == "runtime_doctor_markdown" for item in bundle["files"]),
            "Runtime Doctor is included in the export bundle.",
        ),
        _check(
            "qa_public_beta_readiness_export",
            "Public Beta Readiness is exportable",
            any(item["id"] == "public_beta_readiness_markdown" for item in bundle["files"]),
            "Public Beta Readiness is included in the export bundle.",
        ),
        _check(
            "qa_lab_readiness_export",
            "Lab readiness console is exportable",
            any(item["id"] == "lab_readiness_markdown" for item in bundle["files"]),
            "Lab readiness console is included in the export bundle.",
        ),
        _check(
            "qa_measurement_intake_matrix_export",
            "Measurement intake matrix is exportable",
            any(item["id"] == "measurement_intake_matrix_markdown" for item in bundle["files"]),
            "Measurement Intake Matrix preserves measured, not-tested, and provenance status for review.",
        ),
        _check(
            "qa_measurement_intake_matrix_csv_export",
            "Measurement intake matrix CSV is exportable",
            any(item["id"] == "measurement_intake_matrix_csv" for item in bundle["files"]),
            "Measurement Intake Matrix CSV supports spreadsheet review without creating new scores.",
        ),
        _check(
            "qa_protocol_source_guide",
            "Protocol source guide is available",
            (
                protocol_source_guide["schema"] == "sportrx.protocol_source_guide"
                and protocol_source_guide["preset_count"] >= 4
                and any(item["source"] == "Benchmark Log import" for item in protocol_source_guide["sources"])
                and "does not validate protocols" in protocol_source_guide["claim_boundary"]
            ),
            (
                f"{protocol_source_guide['preset_count']} protocol-source presets; "
                f"status: {protocol_source_guide['status']}."
            ),
        ),
        _check(
            "qa_protocol_source_guide_export",
            "Protocol source guide is exportable",
            any(item["id"] == "protocol_source_guide_markdown" for item in bundle["files"]),
            "Protocol Source Guide explains protocol-score provenance before testing.",
        ),
        _check(
            "qa_benchmark_log_entry_contract_export",
            "Benchmark Log entry contract is exportable",
            any(item["id"] == "benchmark_log_entry_contract_markdown" for item in bundle["files"]),
            "Benchmark Log Entry Contract explains component-specific fields, units, and not-allowed inferences.",
        ),
        _check(
            "qa_protocol_deviation_export",
            "Protocol deviation review is exportable",
            any(item["id"] == "protocol_deviation_markdown" for item in bundle["files"]),
            "Protocol Deviation Review keeps retest context visible.",
        ),
        _check(
            "qa_retest_interpretation_export",
            "Retest interpretation guard is exportable",
            any(item["id"] == "retest_interpretation_markdown" for item in bundle["files"]),
            "Retest Interpretation Guard keeps raw change boundaries visible.",
        ),
        _check(
            "qa_benchmark_worksheet_export",
            "Benchmark worksheet is exportable",
            any(item["id"] == "benchmark_worksheet_markdown" for item in bundle["files"]),
            "Benchmark worksheet is included for test-day data capture.",
        ),
        _check(
            "qa_test_day_brief_export",
            "Test-day brief is exportable",
            any(item["id"] == "test_day_brief_markdown" for item in bundle["files"]),
            "Test-day brief is included in the export bundle.",
        ),
        _check(
            "qa_test_day_command_board_export",
            "Test-Day Command Board is exportable",
            any(item["id"] == "test_day_command_board_markdown" for item in bundle["files"]),
            "Test-Day Command Board is included for first-screen benchmark execution review.",
        ),
        _check(
            "qa_test_session_operator_export",
            "Test Session Operator is exportable",
            any(item["id"] == "test_session_operator_markdown" for item in bundle["files"]),
            "Test Session Operator is included for step-by-step benchmark execution.",
        ),
        _check(
            "qa_session_snapshot",
            "Session snapshot is exportable",
            any(item["id"] == "session_snapshot_json" for item in bundle["files"]),
            "Session snapshot is included in the export bundle for local restore.",
        ),
    ]

    for path in REQUIRED_EVIDENCE_FILES:
        checks.append(
            _check(
                f"qa_evidence_{path.replace('/', '_').replace('.', '_')}",
                f"Evidence file present: {path}",
                bool(evidence_files_present.get(path, False)),
                "Present" if evidence_files_present.get(path, False) else "Missing from current QA context.",
            )
        )

    passed = sum(1 for item in checks if item["passed"])
    return {
        "schema": "sportrx.release_qa",
        "schema_version": "0.1",
        "status": "ready_for_demo_review" if passed == len(checks) else "needs_review",
        "passed_checks": passed,
        "total_checks": len(checks),
        "checks": checks,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def release_qa_markdown(qa: dict[str, Any]) -> str:
    """Export release QA as markdown."""

    lines = [
        "# SportRx Release QA",
        "",
        f"- Status: {qa['status']}",
        f"- Passed: {qa['passed_checks']} / {qa['total_checks']}",
        f"- Claim boundary: {qa['claim_boundary']}",
        "",
        "## Checks",
    ]
    for item in qa["checks"]:
        lines.append(f"- [{item['status']}] {item['label']}: {item['detail']}")
    return "\n".join(lines) + "\n"
