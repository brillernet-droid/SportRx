from pathlib import Path
from zipfile import ZipFile

from sportrx.release_package import (
    build_release_package_manifest,
    should_include_release_path,
    write_release_package,
)


ROOT = Path(__file__).resolve().parents[1]


def test_should_include_release_path_keeps_public_files():
    assert should_include_release_path(".gitignore")
    assert should_include_release_path(".dockerignore")
    assert should_include_release_path("README.md")
    assert should_include_release_path("README.en.md")
    assert should_include_release_path("DEPLOY_TENCENT.md")
    assert should_include_release_path("Dockerfile")
    assert should_include_release_path("requirements.txt")
    assert should_include_release_path("app/streamlit_app.py")
    assert should_include_release_path("scripts/run_local.sh")
    assert should_include_release_path("sportrx/prescription.py")
    assert should_include_release_path("docs/research/open_source_landscape.md")
    assert should_include_release_path("docs/zh-CN/quickstart.md")
    assert should_include_release_path("sportrx/evidence_store.py")
    assert should_include_release_path("evidence/records/sources.json")
    assert should_include_release_path("evidence/data_governance.md")
    assert should_include_release_path("evidence/knowledge/cards.json")
    assert should_include_release_path("evidence/records/screening_providers.json")
    assert should_include_release_path("docs/zh-CN/venue-entry.md")
    assert should_include_release_path("docs/zh-CN/public-preview.md")


def test_should_include_release_path_excludes_internal_and_generated_files():
    assert not should_include_release_path("docs/internal/AI_REVIEW_BRIEF.md")
    assert not should_include_release_path("docs/internal/archive/SportRx_2.1_review_package.zip")
    assert not should_include_release_path("sportrx/__pycache__/prescription.cpython-314.pyc")
    assert not should_include_release_path(".pytest_cache/v/cache/nodeids")
    assert not should_include_release_path("dist/SportRx_public.zip")
    assert not should_include_release_path(".cache/sportrx_evidence.sqlite")
    assert not should_include_release_path("evidence/private/licensed_source.pdf")
    assert not should_include_release_path("data/.local/accounts.json")


def test_release_package_manifest_is_public_ready():
    manifest = build_release_package_manifest(ROOT)

    assert manifest["status"] == "ready_for_public_package"
    assert manifest["passed_checks"] == manifest["total_checks"]
    assert "app/streamlit_app.py" in manifest["included_files"]
    assert "scripts/run_local.sh" in manifest["included_files"]
    assert "scripts/smoke_check.py" in manifest["included_files"]
    assert "sportrx/benchmark_worksheet.py" in manifest["included_files"]
    assert "sportrx/demo_experience.py" in manifest["included_files"]
    assert "sportrx/release_qa.py" in manifest["included_files"]
    assert "sportrx/artifact_catalog.py" in manifest["included_files"]
    assert "sportrx/demo_scenarios.py" in manifest["included_files"]
    assert "sportrx/export_archive.py" in manifest["included_files"]
    assert "sportrx/first_run_guide.py" in manifest["included_files"]
    assert "sportrx/guided_review.py" in manifest["included_files"]
    assert "sportrx/input_ledger.py" in manifest["included_files"]
    assert "sportrx/lab_readiness.py" in manifest["included_files"]
    assert "sportrx/measurement_timeline.py" in manifest["included_files"]
    assert "sportrx/protocol_source.py" in manifest["included_files"]
    assert "sportrx/public_beta_readiness.py" in manifest["included_files"]
    assert "sportrx/reviewer_handoff.py" in manifest["included_files"]
    assert "sportrx/runtime_doctor.py" in manifest["included_files"]
    assert "sportrx/session_snapshot.py" in manifest["included_files"]
    assert "sportrx/test_day_brief.py" in manifest["included_files"]
    assert "sportrx/terminology.py" in manifest["included_files"]
    assert "sportrx/evidence_store.py" in manifest["included_files"]
    assert "evidence/records/sources.json" in manifest["included_files"]
    assert "evidence/evaluation/retrieval_set.json" in manifest["included_files"]
    assert "evidence/data_governance.md" in manifest["included_files"]
    assert "sportrx/knowledge_rag.py" in manifest["included_files"]
    assert "evidence/knowledge/cards.json" in manifest["included_files"]
    assert ".dockerignore" in manifest["included_files"]
    assert "render.yaml" in manifest["included_files"]
    assert "evidence/records/screening_providers.json" in manifest["included_files"]
    assert "evidence/knowledge/evaluation/retrieval_set.json" in manifest["included_files"]
    assert "evidence/knowledge/evaluation/boundary_set.json" in manifest["included_files"]
    assert "evidence/knowledge/evaluation/answer_quality_set.json" in manifest["included_files"]
    assert "README.md" in manifest["included_files"]
    assert "README.en.md" in manifest["included_files"]
    assert "DEPLOY_TENCENT.md" in manifest["included_files"]
    assert "Dockerfile" in manifest["included_files"]
    assert "requirements.txt" in manifest["included_files"]
    assert ".gitignore" in manifest["included_files"]
    assert "docs/research/github_comparable_products_2026.md" in manifest["included_files"]
    assert "docs/zh-CN/quickstart.md" in manifest["included_files"]
    assert "docs/zh-CN/product-guide.md" in manifest["included_files"]
    assert "docs/zh-CN/claim-boundaries.md" in manifest["included_files"]
    assert "docs/zh-CN/terminology.md" in manifest["included_files"]
    assert "docs/zh-CN/venue-entry.md" in manifest["included_files"]
    assert "docs/zh-CN/public-preview.md" in manifest["included_files"]
    assert all(not path.startswith("docs/internal/") for path in manifest["included_files"])
    assert all("__pycache__" not in path for path in manifest["included_files"])
    assert all(not path.endswith(".zip") for path in manifest["included_files"])


def test_write_release_package_excludes_internal_files(tmp_path):
    output_path = tmp_path / "SportRx_public.zip"
    manifest = write_release_package(ROOT, output_path)

    assert output_path.exists()
    assert manifest["output_filename"] == "SportRx_public.zip"

    with ZipFile(output_path) as archive:
        names = set(archive.namelist())

    assert "app/streamlit_app.py" in names
    assert ".gitignore" in names
    assert "README.md" in names
    assert "README.en.md" in names
    assert "DEPLOY_TENCENT.md" in names
    assert "Dockerfile" in names
    assert "requirements.txt" in names
    assert "scripts/run_local.sh" in names
    assert "scripts/smoke_check.py" in names
    assert "sportrx/benchmark_worksheet.py" in names
    assert "sportrx/demo_experience.py" in names
    assert "sportrx/artifact_catalog.py" in names
    assert "sportrx/demo_scenarios.py" in names
    assert "sportrx/export_archive.py" in names
    assert "sportrx/first_run_guide.py" in names
    assert "sportrx/guided_review.py" in names
    assert "sportrx/input_ledger.py" in names
    assert "sportrx/lab_readiness.py" in names
    assert "sportrx/measurement_timeline.py" in names
    assert "sportrx/protocol_source.py" in names
    assert "sportrx/public_beta_readiness.py" in names
    assert "sportrx/reviewer_handoff.py" in names
    assert "sportrx/runtime_doctor.py" in names
    assert "sportrx/session_snapshot.py" in names
    assert "sportrx/test_day_brief.py" in names
    assert "sportrx/terminology.py" in names
    assert "sportrx/evidence_store.py" in names
    assert "evidence/records/claims.json" in names
    assert "evidence/evaluation/unsafe_queries.json" in names
    assert "evidence/data_governance.md" in names
    assert "sportrx/knowledge_rag.py" in names
    assert "evidence/knowledge/cards.json" in names
    assert "evidence/knowledge/evaluation/retrieval_set.json" in names
    assert "evidence/knowledge/evaluation/boundary_set.json" in names
    assert "evidence/knowledge/evaluation/answer_quality_set.json" in names
    assert "docs/research/open_source_landscape.md" in names
    assert "docs/zh-CN/quickstart.md" in names
    assert "docs/zh-CN/product-guide.md" in names
    assert "docs/zh-CN/claim-boundaries.md" in names
    assert "docs/zh-CN/terminology.md" in names
    assert not any(name.startswith("docs/internal/") for name in names)
    assert not any("__pycache__" in name for name in names)
    assert not any(name.endswith(".pyc") or name.endswith(".zip") for name in names)
