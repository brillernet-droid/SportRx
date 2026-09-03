"""Public release package helpers for SportRx.

The release package is a local convenience artifact. It is not a scientific
validation bundle and must not include internal review notes or generated cache
files.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile


PACKAGE_CLAIM_BOUNDARY = (
    "The public release package is a clean code and documentation artifact. It "
    "does not validate SportRx, create medical clearance, or prove outcomes."
)


PUBLIC_TOP_LEVEL_FILES = {
    ".dockerignore",
    ".gitignore",
    "CHANGELOG.md",
    "DEPLOY_TENCENT.md",
    "Dockerfile",
    "LICENSE",
    "README.md",
    "README.en.md",
    "ROADMAP.md",
    "pyproject.toml",
    "requirements.txt",
    "render.yaml",
}


PUBLIC_PREFIXES = (
    "app/",
    "scripts/",
    "sportrx/",
    "tests/",
    "examples/",
    "data/",
    "evidence/",
    "docs/",
)


EXCLUDED_PARTS = {
    ".DS_Store",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".cache",
    "__pycache__",
    "dist",
    "venv",
    ".venv",
}


EXCLUDED_PREFIXES = (
    "data/.local/",
    "docs/internal/",
    "evidence/private/",
)


EXCLUDED_SUFFIXES = (
    ".pyc",
    ".pyo",
    ".zip",
)


REQUIRED_PUBLIC_FILES = [
    ".gitignore",
    ".dockerignore",
    "README.md",
    "README.en.md",
    "CHANGELOG.md",
    "DEPLOY_TENCENT.md",
    "Dockerfile",
    "render.yaml",
    "ROADMAP.md",
    "LICENSE",
    "pyproject.toml",
    "requirements.txt",
    "app/streamlit_app.py",
    "scripts/run_local.sh",
    "scripts/smoke_check.py",
    "scripts/build_knowledge_seed.py",
    "scripts/build_knowledge_evaluation_seed.py",
    "scripts/sync_exercise_dataset.py",
    "data/exercises/README.md",
    "data/exercises/THIRD_PARTY_NOTICES.md",
    "data/exercises/LICENSE-upstream-MIT.md",
    "data/exercises/catalogue.json",
    "sportrx/alpha_dataset_template.py",
    "sportrx/artifact_catalog.py",
    "sportrx/automation_guard.py",
    "sportrx/benchmark_worksheet.py",
    "sportrx/demo_experience.py",
    "sportrx/demo_runbook.py",
    "sportrx/demo_scenario_matrix.py",
    "sportrx/demo_scenarios.py",
    "sportrx/evidence_coverage.py",
    "sportrx/evidence_library.py",
    "sportrx/evidence_store.py",
    "sportrx/exercise_catalogue.py",
    "sportrx/knowledge_discovery.py",
    "sportrx/knowledge_rag.py",
    "sportrx/launch_command_center.py",
    "sportrx/launch_readiness.py",
    "sportrx/local_accounts.py",
    "sportrx/measurement_timeline.py",
    "sportrx/metric_sources.py",
    "sportrx/open_source_integration.py",
    "sportrx/output_prerequisites.py",
    "sportrx/page_health.py",
    "sportrx/pilot_feedback.py",
    "sportrx/plan_actual.py",
    "sportrx/protocol_deviation.py",
    "sportrx/protocol_source.py",
    "sportrx/public_beta_readiness.py",
    "sportrx/release_candidate_summary.py",
    "sportrx/release_qa.py",
    "sportrx/reviewer_handoff.py",
    "sportrx/reviewer_session_plan.py",
    "sportrx/retest_interpretation.py",
    "sportrx/review_pack_integrity.py",
    "sportrx/export_archive.py",
    "sportrx/export_bundle.py",
    "sportrx/first_run_guide.py",
    "sportrx/guided_review.py",
    "sportrx/guided_workout.py",
    "sportrx/input_ledger.py",
    "sportrx/intake_precision.py",
    "sportrx/lab_readiness.py",
    "sportrx/runtime_doctor.py",
    "sportrx/schema_registry.py",
    "sportrx/screening_provider_registry.py",
    "sportrx/self_use_protocol.py",
    "sportrx/session_snapshot.py",
    "sportrx/session_quality_review.py",
    "sportrx/test_day_brief.py",
    "sportrx/test_session_operator.py",
    "sportrx/terminology.py",
    "sportrx/validation_readiness.py",
    "sportrx/venue_entry.py",
    "sportrx/voice_guidance.py",
    "evidence/claim_policy.md",
    "evidence/data_governance.md",
    "evidence/knowledge/README.md",
    "evidence/knowledge/cards.json",
    "evidence/knowledge/candidates.json",
    "evidence/knowledge/discovery_queries.json",
    "evidence/knowledge/safety_curation_backlog.md",
    "evidence/knowledge/evaluation/retrieval_set.json",
    "evidence/knowledge/evaluation/boundary_set.json",
    "evidence/knowledge/evaluation/answer_quality_set.json",
    "evidence/rule_evidence_map.md",
    "evidence/records/README.md",
    "evidence/records/sources.json",
    "evidence/records/claims.json",
    "evidence/records/rules.json",
    "evidence/records/protocols.json",
    "evidence/records/screening_providers.json",
    "evidence/evaluation/retrieval_set.json",
    "evidence/evaluation/unsafe_queries.json",
    "docs/zh-CN/quickstart.md",
    "docs/zh-CN/product-guide.md",
    "docs/zh-CN/claim-boundaries.md",
    "docs/zh-CN/goal-first-prescription-design.md",
    "docs/zh-CN/terminology.md",
    "docs/zh-CN/venue-entry.md",
    "docs/zh-CN/public-preview.md",
    "docs/research/open_source_landscape.md",
    "docs/research/github_comparable_products_2026.md",
    "tests/test_alpha_dataset_template.py",
    "tests/test_artifact_catalog.py",
    "tests/test_benchmark_worksheet.py",
    "tests/test_demo_experience.py",
    "tests/test_demo_runbook.py",
    "tests/test_demo_scenario_matrix.py",
    "tests/test_demo_scenarios.py",
    "tests/test_data_governance.py",
    "tests/test_evidence_coverage.py",
    "tests/test_evidence_library.py",
    "tests/test_evidence_store.py",
    "tests/test_exercise_catalogue.py",
    "tests/test_export_archive.py",
    "tests/test_first_run_guide.py",
    "tests/test_guided_review.py",
    "tests/test_guided_workout.py",
    "tests/test_input_ledger.py",
    "tests/test_intake_precision.py",
    "tests/test_knowledge_discovery.py",
    "tests/test_knowledge_rag.py",
    "tests/test_lab_readiness.py",
    "tests/test_launch_command_center.py",
    "tests/test_launch_readiness.py",
    "tests/test_local_accounts.py",
    "tests/test_measurement_timeline.py",
    "tests/test_metric_sources.py",
    "tests/test_open_source_integration.py",
    "tests/test_output_prerequisites.py",
    "tests/test_page_health.py",
    "tests/test_pilot_feedback.py",
    "tests/test_plan_actual.py",
    "tests/test_protocol_deviation.py",
    "tests/test_protocol_source.py",
    "tests/test_public_beta_readiness.py",
    "tests/test_release_candidate_summary.py",
    "tests/test_release_qa.py",
    "tests/test_reviewer_handoff.py",
    "tests/test_reviewer_session_plan.py",
    "tests/test_retest_interpretation.py",
    "tests/test_review_pack_integrity.py",
    "tests/test_runtime_doctor.py",
    "tests/test_schema_registry.py",
    "tests/test_self_use_protocol.py",
    "tests/test_session_snapshot.py",
    "tests/test_session_quality_review.py",
    "tests/test_smoke_check.py",
    "tests/test_test_day_brief.py",
    "tests/test_test_session_operator.py",
    "tests/test_terminology.py",
    "tests/test_validation_readiness.py",
    "tests/test_voice_guidance.py",
]


def _release_path(path: str | Path) -> str:
    """Normalize a filesystem-ish path into a stable POSIX release path."""

    raw = str(path).replace("\\", "/").strip()
    while raw.startswith("./"):
        raw = raw[2:]
    return PurePosixPath(raw).as_posix()


def should_include_release_path(path: str | Path) -> bool:
    """Return whether a repository-relative path belongs in the public package."""

    release_path = _release_path(path)
    if not release_path or release_path == ".":
        return False

    parts = set(PurePosixPath(release_path).parts)
    if parts & EXCLUDED_PARTS:
        return False
    if any(release_path.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    if release_path.endswith(EXCLUDED_SUFFIXES):
        return False

    if release_path in PUBLIC_TOP_LEVEL_FILES:
        return True
    return any(release_path.startswith(prefix) for prefix in PUBLIC_PREFIXES)


def _package_check(check_id: str, label: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "id": check_id,
        "label": label,
        "status": "pass" if passed else "needs_review",
        "passed": bool(passed),
        "detail": detail,
    }


def build_release_package_manifest(root: str | Path) -> dict[str, Any]:
    """Build a manifest describing the files eligible for a public release zip."""

    root_path = Path(root).resolve()
    included_files: list[str] = []
    excluded_examples: list[str] = []

    for file_path in sorted(root_path.rglob("*")):
        if not file_path.is_file():
            continue
        rel_path = file_path.relative_to(root_path).as_posix()
        if should_include_release_path(rel_path):
            included_files.append(rel_path)
        elif len(excluded_examples) < 40:
            excluded_examples.append(rel_path)

    included_set = set(included_files)
    missing_required = [path for path in REQUIRED_PUBLIC_FILES if path not in included_set]
    internal_leaks = [path for path in included_files if path.startswith("docs/internal/")]
    cache_leaks = [
        path
        for path in included_files
        if "__pycache__" in PurePosixPath(path).parts or path.endswith(EXCLUDED_SUFFIXES)
    ]
    hidden_leaks = [
        path
        for path in included_files
        if path not in {".gitignore", ".dockerignore"} and any(part.startswith(".") for part in PurePosixPath(path).parts)
    ]

    checks = [
        _package_check(
            "pkg_required_files",
            "Required public files are included",
            not missing_required,
            "All required files present." if not missing_required else f"Missing: {', '.join(missing_required)}",
        ),
        _package_check(
            "pkg_internal_docs",
            "Internal review and strategy files are excluded",
            not internal_leaks,
            "No docs/internal files included." if not internal_leaks else f"Leaked: {', '.join(internal_leaks[:5])}",
        ),
        _package_check(
            "pkg_cache_files",
            "Generated cache and archive files are excluded",
            not cache_leaks,
            "No cache, bytecode, or zip files included." if not cache_leaks else f"Leaked: {', '.join(cache_leaks[:5])}",
        ),
        _package_check(
            "pkg_hidden_files",
            "Hidden local tooling files are excluded",
            not hidden_leaks,
            "No hidden files included." if not hidden_leaks else f"Leaked: {', '.join(hidden_leaks[:5])}",
        ),
        _package_check(
            "pkg_public_research",
            "Public research notes are included",
            any(path.startswith("docs/research/") for path in included_files),
            "docs/research included for product positioning and GitHub landscape notes.",
        ),
        _package_check(
            "pkg_tests",
            "Tests are included",
            any(path.startswith("tests/") for path in included_files),
            "tests/ included for transparent local verification.",
        ),
    ]

    passed = sum(1 for item in checks if item["passed"])
    return {
        "schema": "sportrx.release_package_manifest",
        "schema_version": "0.1",
        "status": "ready_for_public_package" if passed == len(checks) else "needs_review",
        "root": str(root_path),
        "included_file_count": len(included_files),
        "included_files": included_files,
        "excluded_examples": excluded_examples,
        "passed_checks": passed,
        "total_checks": len(checks),
        "checks": checks,
        "claim_boundary": PACKAGE_CLAIM_BOUNDARY,
    }


def write_release_package(root: str | Path, output_path: str | Path) -> dict[str, Any]:
    """Write a public release zip and return its manifest."""

    root_path = Path(root).resolve()
    output = Path(output_path).resolve()
    manifest = build_release_package_manifest(root_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for rel_path in manifest["included_files"]:
            archive.write(root_path / rel_path, arcname=rel_path)

    manifest = dict(manifest)
    manifest["output_path"] = str(output)
    manifest["output_filename"] = output.name
    return manifest
