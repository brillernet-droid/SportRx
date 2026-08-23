"""ZIP archive helpers for SportRx export bundles."""

from __future__ import annotations

from io import BytesIO
import json
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

from .review_pack_integrity import build_review_pack_integrity, review_pack_integrity_markdown


CLAIM_BOUNDARY = (
    "Review Pack ZIP archives local SportRx export artifacts for review and "
    "handoff. It does not create validation data, athlete norms, predictions, "
    "or medical clearance."
)


def build_review_pack_manifest(bundle: dict[str, Any]) -> dict[str, Any]:
    """Build a manifest for a ZIP archive created from an export bundle."""

    files = bundle.get("files", [])
    integrity = build_review_pack_integrity(files)
    return {
        "schema": "sportrx.review_pack_manifest",
        "schema_version": "0.1",
        "archive_filename": "sportrx_review_pack.zip",
        "payload_file_count": len(files),
        "archive_entry_count": len(files) + 2,
        "file_count": len(files),
        "integrity_status": integrity["status"],
        "integrity": integrity,
        "files": [
            {
                "filename": item["filename"],
                "label": item["label"],
                "mime": item["mime"],
                "byte_size": integrity["files"][index]["byte_size"],
                "sha256": integrity["files"][index]["sha256"],
            }
            for index, item in enumerate(files)
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_review_pack_zip(bundle: dict[str, Any]) -> bytes:
    """Return a ZIP archive containing all current export bundle files."""

    archive_manifest = build_review_pack_manifest(bundle)
    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as archive:
        for item in bundle.get("files", []):
            archive.writestr(item["filename"], item["content"])
        archive.writestr(
            "sportrx_review_pack_integrity.md",
            review_pack_integrity_markdown(archive_manifest["integrity"]),
        )
        archive.writestr(
            "sportrx_review_pack_manifest.json",
            json.dumps(archive_manifest, ensure_ascii=False, indent=2, sort_keys=True),
        )
    return buffer.getvalue()
