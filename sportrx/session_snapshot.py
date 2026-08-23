"""Local session snapshot helpers for SportRx.

Snapshots preserve local prototype state so a reviewer can restore the same
inputs and logs later. They are not scientific validation data.
"""

from __future__ import annotations

from datetime import date
import json
from typing import Any


SCHEMA = "sportrx.session_snapshot"
SCHEMA_VERSION = "0.1"
CLAIM_BOUNDARY = (
    "Session snapshots are local product-state files. They do not validate "
    "SportRx, create athlete norms, predict outcomes, or provide medical "
    "clearance."
)


def _normalize_feedback_keys(feedback_by_week: dict[int | str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(week): feedback for week, feedback in feedback_by_week.items()}


def build_session_snapshot(
    profile: dict[str, Any],
    benchmark_sessions: list[dict[str, Any]],
    feedback_by_week: dict[int | str, dict[str, Any]],
    pilot_feedback_entries: list[dict[str, Any]] | None = None,
    *,
    snapshot_date: str | None = None,
) -> dict[str, Any]:
    """Build a portable local snapshot of current SportRx session state."""

    normalized_feedback = _normalize_feedback_keys(feedback_by_week)
    pilot_feedback_entries = pilot_feedback_entries or []
    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "snapshot_date": snapshot_date or date.today().isoformat(),
        "app_state": {
            "profile": dict(profile),
            "benchmark_sessions": list(benchmark_sessions),
            "feedback_by_week": normalized_feedback,
            "pilot_feedback_entries": list(pilot_feedback_entries),
        },
        "counts": {
            "benchmark_sessions": len(benchmark_sessions),
            "feedback_weeks": len(normalized_feedback),
            "pilot_feedback_entries": len(pilot_feedback_entries),
        },
        "restore_notes": [
            "Restoring a snapshot recalculates SportRx outputs from saved inputs.",
            "Snapshot data is local product state, not validation data.",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def session_snapshot_json(snapshot: dict[str, Any]) -> str:
    """Serialize a session snapshot to stable JSON."""

    return json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True)


def restore_session_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize a SportRx session snapshot for app restore."""

    if snapshot.get("schema") != SCHEMA:
        raise ValueError("Not a SportRx session snapshot.")
    app_state = snapshot.get("app_state")
    if not isinstance(app_state, dict):
        raise ValueError("Snapshot is missing app_state.")

    raw_feedback = app_state.get("feedback_by_week", {})
    if not isinstance(raw_feedback, dict):
        raise ValueError("Snapshot feedback_by_week must be an object.")
    feedback_by_week: dict[int, dict[str, Any]] = {}
    for week, feedback in raw_feedback.items():
        if str(week).isdigit() and isinstance(feedback, dict):
            feedback_by_week[int(week)] = feedback

    profile = app_state.get("profile", {})
    benchmark_sessions = app_state.get("benchmark_sessions", [])
    pilot_feedback_entries = app_state.get("pilot_feedback_entries", [])
    if not isinstance(profile, dict):
        raise ValueError("Snapshot profile must be an object.")
    if not isinstance(benchmark_sessions, list):
        raise ValueError("Snapshot benchmark_sessions must be a list.")
    if not isinstance(pilot_feedback_entries, list):
        raise ValueError("Snapshot pilot_feedback_entries must be a list.")

    return {
        "profile": profile,
        "benchmark_sessions": benchmark_sessions,
        "feedback_by_week": feedback_by_week,
        "pilot_feedback_entries": pilot_feedback_entries,
    }


def session_snapshot_markdown(snapshot: dict[str, Any]) -> str:
    """Export a short human-readable summary of a session snapshot."""

    counts = snapshot.get("counts", {})
    lines = [
        "# SportRx Session Snapshot",
        "",
        f"- Date: {snapshot.get('snapshot_date', 'unknown')}",
        f"- Benchmark sessions: {counts.get('benchmark_sessions', 0)}",
        f"- Feedback weeks: {counts.get('feedback_weeks', 0)}",
        f"- Pilot feedback entries: {counts.get('pilot_feedback_entries', 0)}",
        f"- Claim boundary: {snapshot.get('claim_boundary', CLAIM_BOUNDARY)}",
        "",
        "## Restore Notes",
    ]
    for note in snapshot.get("restore_notes", []):
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"
