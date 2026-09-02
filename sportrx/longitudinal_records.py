"""Stable local record contracts for Program Pack plans and user-owned data.

These contracts are deliberately narrow. A device, venue, or future connector
may contribute a measurement or completed-session record, but it cannot write
directly to a prescription or progression decision.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


ALLOWED_SOURCES = {"self_report", "manual", "device", "venue_equipment", "import"}
ALLOWED_QUALITY = {"reported", "recorded", "verified", "unknown"}


def create_measurement_record(
    *,
    metric: str,
    value: float | int | str | None,
    unit: str | None,
    source: str,
    quality: str = "recorded",
    observed_at: str | None = None,
    consented: bool = True,
    protocol_id: str | None = None,
    not_tested_reason: str | None = None,
) -> dict[str, Any]:
    """Create a source-labelled measurement without imputing missing values."""

    if not metric.strip():
        raise ValueError("metric is required")
    if source not in ALLOWED_SOURCES:
        raise ValueError("source must be a known structured source")
    if quality not in ALLOWED_QUALITY:
        raise ValueError("quality must be a known quality label")
    if value is None and not not_tested_reason:
        raise ValueError("missing measurements require a not_tested_reason")
    if value is not None and not unit:
        raise ValueError("measured values require a unit")
    return {
        "record_type": "measurement",
        "id": f"meas_{uuid4().hex}",
        "metric": metric.strip(),
        "value": value,
        "unit": unit.strip() if isinstance(unit, str) and unit.strip() else None,
        "status": "not_tested" if value is None else "measured",
        "not_tested_reason": not_tested_reason if value is None else None,
        "source": source,
        "quality": quality,
        "observed_at": observed_at or _now_iso(),
        "consented": bool(consented),
        "protocol_id": protocol_id,
    }


def create_completed_session_record(
    *,
    plan_id: str,
    program_pack_id: str,
    week: int,
    session_index: int,
    completed: bool,
    rpe: float | None,
    source: str = "manual",
    occurred_at: str | None = None,
    protocol_deviation: str | None = None,
) -> dict[str, Any]:
    """Create an execution record; it does not apply progression itself."""

    if not plan_id.strip() or not program_pack_id.strip():
        raise ValueError("plan_id and program_pack_id are required")
    if int(week) < 1 or int(session_index) < 0:
        raise ValueError("week and session_index are out of range")
    if source not in ALLOWED_SOURCES:
        raise ValueError("source must be a known structured source")
    if completed and rpe is None:
        raise ValueError("completed sessions require RPE")
    if rpe is not None and not 0 <= float(rpe) <= 10:
        raise ValueError("RPE must be between 0 and 10")
    return {
        "record_type": "completed_session",
        "id": f"session_{uuid4().hex}",
        "plan_id": plan_id.strip(),
        "program_pack_id": program_pack_id.strip(),
        "week": int(week),
        "session_index": int(session_index),
        "completed": bool(completed),
        "rpe": round(float(rpe), 1) if rpe is not None else None,
        "source": source,
        "occurred_at": occurred_at or _now_iso(),
        "protocol_deviation": protocol_deviation or None,
    }


def build_plan_record(prescription: dict[str, Any]) -> dict[str, Any]:
    """Extract a source-ready Plan record from a deterministic prescription."""

    pack = prescription.get("program_pack") or {}
    if not pack or not prescription.get("weeks"):
        raise ValueError("an active Program Pack prescription is required")
    return {
        "record_type": "plan",
        "id": f"plan_{uuid4().hex}",
        "program_pack_id": pack["id"],
        "program_pack_version": pack["version"],
        "rule_ids": list(prescription.get("rule_trace", [])),
        "created_at": _now_iso(),
        "commitment_boundary": prescription["commitment_boundary"],
        "weeks": prescription["weeks"],
    }


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
