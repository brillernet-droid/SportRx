"""Review Pack integrity checks for SportRx export handoff."""

from __future__ import annotations

import hashlib
from pathlib import PurePosixPath
from typing import Any


CLAIM_BOUNDARY = (
    "Review Pack Integrity verifies local export packaging only. It does not "
    "validate SportRx rules, prove training outcomes, create athlete norms, or "
    "provide medical clearance."
)


INTERNAL_PREFIXES = ("docs/internal/",)
CACHE_PARTS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
BLOCKED_SUFFIXES = (".pyc", ".pyo")


def _content_bytes(content: Any) -> bytes:
    if isinstance(content, bytes):
        return content
    if isinstance(content, str):
        return content.encode("utf-8")
    return str(content).encode("utf-8")


def _check(check_id: str, label: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "id": check_id,
        "label": label,
        "status": "pass" if passed else "needs_review",
        "passed": bool(passed),
        "detail": detail,
    }


def build_review_pack_integrity(files: list[dict[str, Any]]) -> dict[str, Any]:
    """Build checksum, duplicate, and leak checks for Review Pack payload files."""

    entries: list[dict[str, Any]] = []
    filename_counts: dict[str, int] = {}
    internal_leaks: list[str] = []
    cache_leaks: list[str] = []
    empty_files: list[str] = []

    for order, item in enumerate(files, start=1):
        filename = str(item.get("filename", ""))
        payload = _content_bytes(item.get("content", ""))
        digest = hashlib.sha256(payload).hexdigest()
        path = PurePosixPath(filename)
        filename_counts[filename] = filename_counts.get(filename, 0) + 1

        if any(filename.startswith(prefix) for prefix in INTERNAL_PREFIXES):
            internal_leaks.append(filename)
        if set(path.parts) & CACHE_PARTS or filename.endswith(BLOCKED_SUFFIXES):
            cache_leaks.append(filename)
        if len(payload) == 0:
            empty_files.append(filename)

        entries.append(
            {
                "order": order,
                "id": item.get("id", ""),
                "filename": filename,
                "label": item.get("label", ""),
                "mime": item.get("mime", ""),
                "byte_size": len(payload),
                "sha256": digest,
            }
        )

    duplicate_filenames = sorted(name for name, count in filename_counts.items() if count > 1)
    total_bytes = sum(item["byte_size"] for item in entries)
    checks = [
        _check(
            "integrity_payload_present",
            "Review Pack payload files are present",
            bool(entries),
            f"{len(entries)} payload files available for integrity review.",
        ),
        _check(
            "integrity_sha256",
            "Every payload file has a SHA-256 checksum",
            all(len(item["sha256"]) == 64 for item in entries),
            f"{len(entries)} checksum records generated.",
        ),
        _check(
            "integrity_unique_filenames",
            "Payload filenames are unique",
            not duplicate_filenames,
            "No duplicate filenames." if not duplicate_filenames else f"Duplicates: {', '.join(duplicate_filenames)}",
        ),
        _check(
            "integrity_no_internal_paths",
            "Payload does not include internal review paths",
            not internal_leaks,
            "No docs/internal paths included." if not internal_leaks else f"Leaked: {', '.join(internal_leaks[:5])}",
        ),
        _check(
            "integrity_no_cache_paths",
            "Payload does not include generated cache or bytecode paths",
            not cache_leaks,
            "No cache or bytecode paths included." if not cache_leaks else f"Leaked: {', '.join(cache_leaks[:5])}",
        ),
        _check(
            "integrity_no_empty_files",
            "Payload files are non-empty",
            not empty_files,
            "No empty payload files." if not empty_files else f"Empty: {', '.join(empty_files[:5])}",
        ),
    ]
    passed = sum(1 for item in checks if item["passed"])
    return {
        "schema": "sportrx.review_pack_integrity",
        "schema_version": "0.1",
        "status": "ready_for_review_handoff" if passed == len(checks) else "needs_review",
        "payload_file_count": len(entries),
        "total_bytes": total_bytes,
        "checks": checks,
        "passed_checks": passed,
        "total_checks": len(checks),
        "duplicate_filenames": duplicate_filenames,
        "internal_path_leaks": internal_leaks,
        "cache_path_leaks": cache_leaks,
        "empty_files": empty_files,
        "files": entries,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def review_pack_integrity_markdown(integrity: dict[str, Any]) -> str:
    """Export Review Pack integrity data as Markdown."""

    lines = [
        "# SportRx Review Pack Integrity",
        "",
        f"- Status: {integrity['status']}",
        f"- Payload files: {integrity['payload_file_count']}",
        f"- Total bytes: {integrity['total_bytes']}",
        f"- Checks: {integrity['passed_checks']} / {integrity['total_checks']}",
        f"- Claim boundary: {integrity['claim_boundary']}",
        "",
        "## Checks",
    ]
    for item in integrity["checks"]:
        lines.append(f"- [{item['status']}] {item['label']}: {item['detail']}")

    lines.extend(["", "## File Checksums"])
    for item in integrity["files"]:
        lines.append(f"- `{item['filename']}` ({item['byte_size']} bytes): `{item['sha256']}`")

    return "\n".join(lines) + "\n"
