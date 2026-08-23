import json
from io import BytesIO
from zipfile import ZipFile

from sportrx.demo_seed import build_demo_state
from sportrx.export_archive import build_review_pack_manifest, build_review_pack_zip
from sportrx.export_bundle import build_export_bundle
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription


def _demo_bundle():
    state = build_demo_state()
    profile = state["profile"]
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile, feedback_by_week=state["feedback_by_week"])
    return build_export_bundle(profile, passport, plan, state["benchmark_sessions"], state["feedback_by_week"])


def test_review_pack_manifest_describes_export_bundle():
    bundle = _demo_bundle()

    manifest = build_review_pack_manifest(bundle)

    assert manifest["schema"] == "sportrx.review_pack_manifest"
    assert manifest["archive_filename"] == "sportrx_review_pack.zip"
    assert manifest["file_count"] == len(bundle["files"])
    assert manifest["payload_file_count"] == len(bundle["files"])
    assert manifest["archive_entry_count"] == len(bundle["files"]) + 2
    assert manifest["integrity_status"] == "ready_for_review_handoff"
    assert any(item["filename"] == "sportrx_artifact_catalog.md" for item in manifest["files"])
    assert any(item["filename"] == "sportrx_reviewer_handoff.md" for item in manifest["files"])
    assert any(item["filename"] == "sportrx_input_ledger.md" for item in manifest["files"])
    assert any(item["filename"] == "sportrx_quick_match_lab_intake_sheet.md" for item in manifest["files"])
    assert any(item["filename"] == "sportrx_protocol_source_guide.md" for item in manifest["files"])
    assert any(item["filename"] == "sportrx_benchmark_worksheet.md" for item in manifest["files"])
    assert any(item["filename"] == "sportrx_test_day_brief.md" for item in manifest["files"])
    assert any(item["filename"] == "sportrx_test_day_command_board.md" for item in manifest["files"])
    assert all(item["byte_size"] > 0 for item in manifest["files"])
    assert all(len(item["sha256"]) == 64 for item in manifest["files"])
    assert "does not create validation data" in manifest["claim_boundary"]


def test_review_pack_zip_contains_all_bundle_files_and_manifest():
    bundle = _demo_bundle()

    payload = build_review_pack_zip(bundle)

    with ZipFile(BytesIO(payload)) as archive:
        names = set(archive.namelist())
        archive_manifest = json.loads(archive.read("sportrx_review_pack_manifest.json").decode("utf-8"))

    expected_names = {item["filename"] for item in bundle["files"]}
    assert expected_names <= names
    assert "sportrx_review_pack_manifest.json" in names
    assert "sportrx_review_pack_integrity.md" in names
    assert "sportrx_reviewer_handoff.md" in names
    assert "sportrx_input_ledger.md" in names
    assert "sportrx_quick_match_lab_intake_sheet.md" in names
    assert "sportrx_protocol_source_guide.md" in names
    assert "sportrx_benchmark_worksheet.md" in names
    assert "sportrx_test_day_command_board.md" in names
    assert archive_manifest["file_count"] == len(bundle["files"])
    assert archive_manifest["integrity_status"] == "ready_for_review_handoff"
    assert not any(name.startswith("docs/internal/") for name in names)
    assert not any("__pycache__" in name for name in names)
