"""SportRx v0.1 rule engine.

The package intentionally keeps the exercise-prescription logic separate from
the Streamlit demo. v0.1 covers only apparently healthy adults and aerobic
exercise planning.
"""

from .alpha_dataset_template import (
    alpha_dataset_csv_templates,
    alpha_dataset_dictionary_markdown,
    build_alpha_dataset_template,
)
from .artifact_catalog import artifact_catalog_markdown, build_artifact_catalog
from .automation_guard import build_automation_guard
from .events import match_events
from .exercise_catalogue import (
    BODY_PART_LABELS,
    body_part_label,
    catalogue_summary,
    get_exercise,
    load_exercise_catalogue,
    search_exercises,
    validate_exercise_catalogue,
)
from .benchmark import empty_benchmark_result, get_hybrid_benchmark
from .benchmark_log import (
    benchmark_profile_patch,
    build_benchmark_import_compatibility,
    build_benchmark_log_entry_contract,
    benchmark_log_entry_contract_markdown,
    compare_retest_sessions,
    create_benchmark_session,
    evaluate_benchmark_session_quality,
    export_sessions_csv,
    export_sessions_json,
    summarize_benchmark_sessions,
)
from .benchmark_protocol import get_benchmark_protocol, protocol_markdown
from .benchmark_worksheet import build_benchmark_worksheet, benchmark_worksheet_markdown
from .demo_runbook import build_demo_runbook, demo_runbook_markdown
from .demo_experience import build_demo_experience_console, demo_experience_markdown
from .demo_scenario_matrix import build_demo_scenario_matrix, demo_scenario_matrix_markdown
from .demo_scenarios import build_demo_scenario_state, build_demo_scenarios
from .demo_seed import build_demo_benchmark_sessions, build_demo_feedback_by_week, build_demo_profile, build_demo_state
from .evidence_coverage import build_evidence_coverage, evidence_coverage_markdown
from .evidence_library import build_evidence_library, evidence_library_markdown
from .export_archive import build_review_pack_manifest, build_review_pack_zip
from .export_bundle import build_export_bundle
from .feedback_loop import build_feedback_dashboard, feedback_dashboard_markdown
from .first_run_guide import build_first_run_guide, first_run_guide_markdown
from .guided_review import build_guided_review_console, guided_review_markdown
from .input_ledger import build_input_ledger, input_ledger_markdown
from .intake_precision import build_intake_precision_audit, intake_precision_markdown
from .lab_readiness import build_lab_readiness_console, lab_readiness_markdown
from .knowledge_rag import (
    build_knowledge_index,
    compile_knowledge_embeddings,
    ingest_candidates,
    knowledge_corpus_summary,
    review_knowledge_card,
    search_knowledge,
    synthesize_knowledge,
    validate_knowledge_records,
)
from .knowledge_discovery import discover_knowledge_candidates
from .launch_command_center import build_launch_command_center
from .launch_readiness import build_launch_readiness, launch_readiness_markdown
from .longitudinal_records import (
    build_plan_record,
    create_completed_session_record,
    create_measurement_record,
)
from .language_editions import (
    build_language_edition_contract,
    get_language_edition,
    language_edition_label,
    language_edition_markdown,
    language_edition_options,
    page_label,
    ui_text,
)
from .measurement_timeline import build_measurement_timeline, measurement_timeline_markdown
from .metric_sources import build_metric_source_register
from .open_source_integration import build_open_source_integration_console, open_source_integration_markdown
from .output_prerequisites import build_output_prerequisites
from .page_health import build_page_health_matrix, page_health_matrix_markdown
from .passport import build_readiness_passport
from .pilot_feedback import (
    build_pilot_feedback_prompt,
    build_pilot_review_console,
    create_pilot_feedback_entry,
    export_pilot_feedback_json,
    pilot_feedback_markdown,
    pilot_feedback_prompt_markdown,
    summarize_pilot_feedback,
)
from .plan_actual import classify_plan_actual, provisional_plan_actual
from .prescription import generate_prescription
from .program_packs import get_program_pack, load_program_packs, resolve_program_pack, validate_program_packs
from .protocol_deviation import build_protocol_deviation_review, protocol_deviation_markdown
from .protocol_source import (
    PROTOCOL_SOURCE_HELP,
    PROTOCOL_SOURCE_OPTIONS,
    build_protocol_source_guide,
    protocol_source_guide_markdown,
    resolve_protocol_source_choice,
    resolve_protocol_source_value,
)
from .public_beta_readiness import build_public_beta_readiness, public_beta_readiness_markdown
from .quick_match import (
    build_quick_match_input_review,
    build_quick_match_intake_contract,
    build_quick_match_intake_quality,
    build_quick_match_lab_intake_sheet,
    quick_match,
    quick_match_intake_contract_markdown,
    quick_match_lab_intake_sheet_markdown,
)
from .readiness import calculate_readiness
from .release_candidate_summary import build_release_candidate_summary, release_candidate_summary_markdown
from .release_package import build_release_package_manifest, should_include_release_path, write_release_package
from .release_qa import build_release_qa, release_qa_markdown
from .report import build_training_profile_report, report_markdown
from .reviewer_handoff import build_reviewer_handoff, reviewer_handoff_markdown
from .reviewer_session_plan import build_reviewer_session_plan, reviewer_session_plan_markdown
from .retest_interpretation import build_retest_interpretation_guard, retest_interpretation_markdown
from .review_pack_integrity import build_review_pack_integrity, review_pack_integrity_markdown
from .runtime_doctor import build_runtime_doctor, runtime_doctor_markdown
from .schema_registry import build_measurement_schema_registry, measurement_schema_registry_markdown
from .safety_gate import evaluate_safety_gate
from .screening_provider_registry import load_screening_providers, validate_screening_provider_registry
from .venue_entry import build_venue_entry_assessment
from .self_use_protocol import build_self_use_protocol, self_use_protocol_markdown
from .session_snapshot import (
    build_session_snapshot,
    restore_session_snapshot,
    session_snapshot_json,
    session_snapshot_markdown,
)
from .session_feedback import create_session_feedback, summarize_session_feedback
from .session_quality_review import build_session_quality_review, session_quality_review_markdown
from .share_card import build_readiness_passport_card, build_sport_match_card
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

__all__ = [
    "build_readiness_passport",
    "build_readiness_passport_card",
    "build_sport_match_card",
    "build_alpha_dataset_template",
    "build_artifact_catalog",
    "build_automation_guard",
    "build_benchmark_worksheet",
    "BODY_PART_LABELS",
    "body_part_label",
    "catalogue_summary",
    "build_benchmark_import_compatibility",
    "build_benchmark_log_entry_contract",
    "build_feedback_dashboard",
    "build_review_pack_manifest",
    "build_review_pack_zip",
    "build_first_run_guide",
    "build_guided_review_console",
    "build_input_ledger",
    "build_intake_precision_audit",
    "build_lab_readiness_console",
    "build_knowledge_index",
    "compile_knowledge_embeddings",
    "ingest_candidates",
    "knowledge_corpus_summary",
    "review_knowledge_card",
    "search_knowledge",
    "synthesize_knowledge",
    "validate_knowledge_records",
    "discover_knowledge_candidates",
    "build_launch_readiness",
    "build_plan_record",
    "build_launch_command_center",
    "build_language_edition_contract",
    "build_measurement_timeline",
    "build_measurement_schema_registry",
    "build_metric_source_register",
    "build_output_prerequisites",
    "build_page_health_matrix",
    "build_open_source_integration_console",
    "build_pilot_feedback_prompt",
    "build_pilot_review_console",
    "build_public_beta_readiness",
    "build_protocol_deviation_review",
    "build_protocol_source_guide",
    "build_quick_match_input_review",
    "build_quick_match_intake_contract",
    "build_quick_match_intake_quality",
    "build_quick_match_lab_intake_sheet",
    "build_demo_runbook",
    "build_demo_experience_console",
    "build_demo_scenario_matrix",
    "build_demo_scenario_state",
    "build_demo_scenarios",
    "build_demo_benchmark_sessions",
    "build_demo_feedback_by_week",
    "build_demo_profile",
    "build_demo_state",
    "build_export_bundle",
    "build_evidence_coverage",
    "build_evidence_library",
    "build_release_qa",
    "build_release_candidate_summary",
    "build_release_package_manifest",
    "build_reviewer_handoff",
    "build_reviewer_session_plan",
    "build_retest_interpretation_guard",
    "build_review_pack_integrity",
    "build_runtime_doctor",
    "build_self_use_protocol",
    "build_session_snapshot",
    "build_session_quality_review",
    "build_test_day_brief",
    "build_test_day_command_board",
    "build_test_session_operator",
    "build_terminology_guide",
    "build_training_block",
    "build_validation_readiness_matrix",
    "build_training_profile_report",
    "build_walkthrough",
    "calculate_readiness",
    "alpha_dataset_csv_templates",
    "alpha_dataset_dictionary_markdown",
    "classify_plan_actual",
    "benchmark_profile_patch",
    "benchmark_log_entry_contract_markdown",
    "compare_retest_sessions",
    "create_benchmark_session",
    "create_completed_session_record",
    "create_measurement_record",
    "create_pilot_feedback_entry",
    "demo_runbook_markdown",
    "demo_experience_markdown",
    "demo_scenario_matrix_markdown",
    "empty_benchmark_result",
    "evaluate_safety_gate",
    "build_venue_entry_assessment",
    "load_screening_providers",
    "validate_screening_provider_registry",
    "evaluate_benchmark_session_quality",
    "artifact_catalog_markdown",
    "benchmark_worksheet_markdown",
    "feedback_dashboard_markdown",
    "first_run_guide_markdown",
    "guided_review_markdown",
    "input_ledger_markdown",
    "intake_precision_markdown",
    "lab_readiness_markdown",
    "export_sessions_csv",
    "export_sessions_json",
    "export_pilot_feedback_json",
    "evidence_coverage_markdown",
    "evidence_library_markdown",
    "generate_prescription",
    "get_program_pack",
    "load_program_packs",
    "resolve_program_pack",
    "validate_program_packs",
    "get_exercise",
    "get_benchmark_protocol",
    "get_hybrid_benchmark",
    "get_language_edition",
    "language_edition_label",
    "language_edition_markdown",
    "language_edition_options",
    "launch_readiness_markdown",
    "load_exercise_catalogue",
    "measurement_timeline_markdown",
    "measurement_schema_registry_markdown",
    "open_source_integration_markdown",
    "page_health_matrix_markdown",
    "page_label",
    "match_events",
    "pilot_feedback_markdown",
    "pilot_feedback_prompt_markdown",
    "protocol_markdown",
    "protocol_deviation_markdown",
    "protocol_source_guide_markdown",
    "public_beta_readiness_markdown",
    "provisional_plan_actual",
    "resolve_protocol_source_choice",
    "resolve_protocol_source_value",
    "quick_match",
    "quick_match_intake_contract_markdown",
    "quick_match_lab_intake_sheet_markdown",
    "report_markdown",
    "reviewer_handoff_markdown",
    "reviewer_session_plan_markdown",
    "retest_interpretation_markdown",
    "review_pack_integrity_markdown",
    "release_qa_markdown",
    "release_candidate_summary_markdown",
    "runtime_doctor_markdown",
    "restore_session_snapshot",
    "self_use_protocol_markdown",
    "search_exercises",
    "summarize_benchmark_sessions",
    "summarize_pilot_feedback",
    "session_snapshot_json",
    "session_snapshot_markdown",
    "create_session_feedback",
    "summarize_session_feedback",
    "session_quality_review_markdown",
    "should_include_release_path",
    "test_day_brief_markdown",
    "test_day_command_board_markdown",
    "test_session_operator_markdown",
    "terminology_markdown",
    "training_block_markdown",
    "ui_text",
    "validation_readiness_markdown",
    "validate_exercise_catalogue",
    "write_release_package",
    "PROTOCOL_SOURCE_HELP",
    "PROTOCOL_SOURCE_OPTIONS",
]
