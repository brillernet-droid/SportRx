"""Lab readiness console for SportRx measurement pages.

This module summarizes whether the current local state is ready for measurement,
handoff, or retest. It is product navigation and data-quality guidance only.
"""

from __future__ import annotations

from typing import Any

from .safety_gate import automated_handoff_allowed, benchmark_allowed


CLAIM_BOUNDARY = (
    "Lab Readiness Console summarizes product state and measurement readiness "
    "only. It does not score performance, validate outcomes, predict injury, "
    "or provide medical clearance."
)


def _status_card(card_id: str, label: str, status: str, detail: str, action: str) -> dict[str, str]:
    return {
        "id": card_id,
        "label": label,
        "status": status,
        "detail": detail,
        "action": action,
    }


def build_lab_readiness_console(
    profile: dict[str, Any],
    passport: dict[str, Any],
    benchmark_summary: dict[str, Any],
) -> dict[str, Any]:
    """Build a lab-console summary from existing SportRx state."""

    safety = passport.get("safety_gate", {})
    safety_status = safety.get("status", "UNKNOWN")
    measured = passport.get("measured_performance_areas", {})
    measured_count = int(measured.get("count", 0) or 0)
    equipment = list(profile.get("equipment_access", []) or [])
    session_count = int(benchmark_summary.get("session_count", 0) or 0)
    retest_ready = bool(benchmark_summary.get("retest_ready"))
    starter_available = bool(passport.get("starter_path", {}).get("available"))

    cards = [
        _status_card(
            "safety_gate",
            "Safety Gate",
            "blocked" if not benchmark_allowed(safety) else "ready",
            f"Current gate: {safety_status}. Safety can block training handoff, but does not change measured performance.",
            "Resolve Safety Gate before Benchmark or training handoff." if not benchmark_allowed(safety) else "Continue measurement with normal stop rules.",
        ),
        _status_card(
            "equipment_path",
            "Equipment Path",
            "ready" if equipment else "needs_setup",
            "Equipment selected: " + (", ".join(equipment) if equipment else "none yet"),
            "Select available equipment before choosing the standard or low-equipment protocol.",
        ),
        _status_card(
            "measurement_depth",
            "Measurement Depth",
            "ready" if measured_count >= 2 else "needs_measurement",
            measured.get("label", f"{measured_count} measured performance areas"),
            "Complete at least two measured performance dimensions before interpreting strongest area vs main gap.",
        ),
        _status_card(
            "benchmark_log",
            "Benchmark Log",
            "ready" if session_count > 0 else "not_started",
            benchmark_summary.get("message", "No benchmark sessions recorded yet."),
            "Save raw test results with unit, RPE, equipment, substitution, and notes.",
        ),
        _status_card(
            "retest_anchor",
            "Retest Anchor",
            "ready" if retest_ready else "waiting",
            "Comparable retest available." if retest_ready else "No comparable retest yet.",
            "Repeat the same component with the same protocol when ready to compare raw change.",
        ),
    ]

    blocked = [card for card in cards if card["status"] == "blocked"]
    needs_work = [card for card in cards if card["status"] in {"needs_setup", "needs_measurement", "not_started"}]
    if blocked:
        status = "blocked_by_safety_gate"
        next_action = blocked[0]["action"]
    elif not equipment:
        status = "needs_equipment_path"
        next_action = "Select the available equipment path before logging a Benchmark session."
    elif measured_count < 2:
        status = "needs_measurement"
        next_action = "Complete at least two SportRx Hybrid Benchmark components."
    elif session_count == 0:
        status = "ready_to_log"
        next_action = "Save the first Benchmark Log session."
    elif starter_available and not retest_ready:
        status = "ready_for_training_handoff"
        next_action = "Use Training Profile / Starter Path, then retest with the same protocol later."
    elif retest_ready:
        status = "ready_for_retest_review"
        next_action = "Review raw retest change and export the local evidence bundle."
    else:
        status = "measurement_in_progress"
        next_action = needs_work[0]["action"] if needs_work else "Continue using the same protocol."

    return {
        "schema": "sportrx.lab_readiness_console",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "cards": cards,
        "summary": {
            "safety_gate": safety_status,
            "equipment_count": len(equipment),
            "measured_performance_areas": measured_count,
            "benchmark_sessions": session_count,
            "retest_ready": retest_ready,
            "starter_path_available": starter_available,
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def lab_readiness_markdown(console: dict[str, Any]) -> str:
    """Export a Lab Readiness Console summary as Markdown."""

    summary = console.get("summary", {})
    lines = [
        "# SportRx Lab Readiness Console",
        "",
        f"- Status: {console.get('status')}",
        f"- Next action: {console.get('next_action')}",
        f"- Claim boundary: {console.get('claim_boundary', CLAIM_BOUNDARY)}",
        "",
        "## Summary",
        f"- Safety Gate: {summary.get('safety_gate', 'UNKNOWN')}",
        f"- Equipment count: {summary.get('equipment_count', 0)}",
        f"- Measured performance areas: {summary.get('measured_performance_areas', 0)}",
        f"- Benchmark sessions: {summary.get('benchmark_sessions', 0)}",
        f"- Retest ready: {summary.get('retest_ready', False)}",
        f"- Starter path available: {summary.get('starter_path_available', False)}",
        "",
        "## Cards",
    ]
    for card in console.get("cards", []):
        lines.append(f"- [{card['status']}] {card['label']}: {card['detail']} Action: {card['action']}")
    return "\n".join(lines) + "\n"
