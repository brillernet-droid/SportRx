"""Registry for externally operated exercise-screening pathways.

SportRX does not copy, translate, score, or store answers from an external
screening instrument. This registry only records whether a venue pathway has
been reviewed for a specific deployment context.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .evidence_store import load_evidence_records


REGISTRY_PATH = "evidence/records/screening_providers.json"
REQUIRED_FIELDS = {
    "id",
    "label",
    "deployment_status",
    "applicability",
    "permitted_use",
    "source_url",
    "language",
    "version",
    "reviewed_at",
    "limitations",
    "member_message",
    "source_ids",
}
ALLOWED_STATUSES = {"approved_for_venue", "research_required", "retired"}


def load_screening_providers(root: str | Path = ".") -> list[dict[str, Any]]:
    path = Path(root).resolve() / REGISTRY_PATH
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    return records if isinstance(records, list) else []


def get_screening_provider(
    provider_id: str | None, providers: list[dict[str, Any]] | None = None, root: str | Path = "."
) -> dict[str, Any] | None:
    candidates = providers if providers is not None else load_screening_providers(root)
    return next((item for item in candidates if item.get("id") == provider_id), None)


def validate_screening_provider_registry(root: str | Path = ".") -> dict[str, Any]:
    providers = load_screening_providers(root)
    source_ids = {record["id"] for record in load_evidence_records(root)["sources"]}
    errors: list[str] = []
    seen: set[str] = set()
    for provider in providers:
        provider_id = str(provider.get("id", "<missing id>"))
        if provider_id in seen:
            errors.append(f"duplicate screening provider id: {provider_id}")
        seen.add(provider_id)
        missing = sorted(field for field in REQUIRED_FIELDS if provider.get(field) in (None, "", []))
        if missing:
            errors.append(f"screening provider {provider_id} missing: {', '.join(missing)}")
        if provider.get("deployment_status") not in ALLOWED_STATUSES:
            errors.append(f"screening provider {provider_id} has invalid deployment_status")
        if not str(provider.get("source_url", "")).startswith("https://"):
            errors.append(f"screening provider {provider_id} must use an https source_url")
        for source_id in provider.get("source_ids", []):
            source = next((item for item in load_evidence_records(root)["sources"] if item["id"] == source_id), None)
            if source_id not in source_ids:
                errors.append(f"screening provider {provider_id} references unknown source: {source_id}")
            elif source is None or source.get("review_status") != "reviewed" or not source.get("limitations"):
                errors.append(f"screening provider {provider_id} needs a reviewed source with limitations: {source_id}")
        message = str(provider.get("member_message", "")).lower()
        if not any(token in message for token in ("medical", "医疗", "诊断")):
            errors.append(f"screening provider {provider_id} needs a non-diagnostic member message")
    approved = [item for item in providers if item.get("deployment_status") == "approved_for_venue"]
    return {
        "schema": "sportrx.screening_provider_registry",
        "schema_version": "0.1",
        "status": "venue_ready" if not errors and approved else "research_required",
        "provider_count": len(providers),
        "approved_provider_count": len(approved),
        "errors": errors,
        "claim_boundary": (
            "Registry status documents external screening-pathway review only. It does not "
            "validate SportRX, provide medical clearance, or diagnose a member."
        ),
    }
