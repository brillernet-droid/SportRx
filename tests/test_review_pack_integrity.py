from sportrx.demo_seed import build_demo_state
from sportrx.export_bundle import build_export_bundle
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.review_pack_integrity import build_review_pack_integrity, review_pack_integrity_markdown


def _demo_files():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    bundle = build_export_bundle(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
    )
    return bundle["files"]


def test_review_pack_integrity_hashes_every_payload_file():
    integrity = build_review_pack_integrity(_demo_files())

    assert integrity["schema"] == "sportrx.review_pack_integrity"
    assert integrity["status"] == "ready_for_review_handoff"
    assert integrity["payload_file_count"] >= 29
    assert integrity["passed_checks"] == integrity["total_checks"]
    assert all(len(item["sha256"]) == 64 for item in integrity["files"])
    assert not integrity["duplicate_filenames"]
    assert not integrity["internal_path_leaks"]
    assert "does not validate SportRx rules" in integrity["claim_boundary"]


def test_review_pack_integrity_flags_duplicate_and_internal_paths():
    files = [
        {"id": "a", "filename": "same.md", "label": "A", "mime": "text/markdown", "content": "alpha"},
        {"id": "b", "filename": "same.md", "label": "B", "mime": "text/markdown", "content": "beta"},
        {"id": "c", "filename": "docs/internal/secret.md", "label": "C", "mime": "text/markdown", "content": "secret"},
    ]

    integrity = build_review_pack_integrity(files)

    assert integrity["status"] == "needs_review"
    assert "same.md" in integrity["duplicate_filenames"]
    assert "docs/internal/secret.md" in integrity["internal_path_leaks"]
    assert any(check["id"] == "integrity_unique_filenames" and not check["passed"] for check in integrity["checks"])
    assert any(check["id"] == "integrity_no_internal_paths" and not check["passed"] for check in integrity["checks"])


def test_review_pack_integrity_markdown_lists_checksums():
    integrity = build_review_pack_integrity(_demo_files())
    markdown = review_pack_integrity_markdown(integrity)

    assert "# SportRx Review Pack Integrity" in markdown
    assert "File Checksums" in markdown
    assert "sportrx_export_manifest.json" in markdown
    assert integrity["files"][0]["sha256"] in markdown
