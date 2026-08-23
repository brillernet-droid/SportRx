"""Whole-session quality review for SportRx local prototype use."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .benchmark_log import summarize_benchmark_sessions
from .evidence_library import build_evidence_library
from .feedback_loop import build_feedback_dashboard
from .lab_readiness import build_lab_readiness_console
from .output_prerequisites import build_output_prerequisites


CLAIM_BOUNDARY = (
    "Session Quality Review summarizes whether the current local SportRx "
    "session has enough recorded data for product interpretation. It is not a "
    "performance score, validation result, prediction, medical risk estimate, "
    "or medical clearance."
)


def _gate(gate_id: str, label: str, status: str, detail: str, action: str) -> dict[str, Any]:
    return {
        "id": gate_id,
        "label": label,
        "status": status,
        "detail": detail,
        "action": action,
    }


def _overall_status(gates: list[dict[str, Any]], passport: dict[str, Any]) -> tuple[str, str]:
    safety_status = passport.get("safety_gate", {}).get("status")
    measured_count = int(passport.get("measured_performance_areas", {}).get("count", 0) or 0)
    starter_available = bool(passport.get("starter_path", {}).get("available"))
    benchmark_ready = any(gate["id"] == "benchmark_log" and gate["status"] == "ready" for gate in gates)
    feedback_ready = any(gate["id"] == "feedback_loop" and gate["status"] == "ready" for gate in gates)
    retest_ready = any(gate["id"] == "retest_anchor" and gate["status"] == "ready" for gate in gates)
    evidence_ready = any(gate["id"] == "evidence_library" and gate["status"] == "ready" for gate in gates)

    if safety_status == "RED":
        return "blocked_by_safety_gate", "Resolve Safety Gate before automated training handoff."
    if measured_count < 2:
        return "measurement_first", "Complete at least two measured performance dimensions before tailored interpretation."
    if not benchmark_ready:
        return "ready_to_log_first_benchmark", "Save a raw Benchmark Log session with protocol, RPE, and equipment notes."
    if starter_available and not feedback_ready:
        return "training_handoff_ready", "Use the Starter Path, then record weekly completion and RPE."
    if feedback_ready and not retest_ready:
        return "feedback_record_ready", "Repeat comparable benchmark components when ready to review raw change."
    if retest_ready and evidence_ready:
        return "release_review_ready", "Review export artifacts, evidence boundaries, and release QA before sharing."
    return "needs_review", "Review the waiting gates before external handoff."


def build_session_quality_review(
    profile: dict[str, Any],
    passport: dict[str, Any],
    plan: dict[str, Any],
    benchmark_sessions: list[dict[str, Any]],
    feedback_by_week: dict[int, dict[str, Any]],
    evidence_files_present: dict[str, bool] | None = None,
    root: str | Path = ".",
) -> dict[str, Any]:
    """Build a whole-session quality review from existing SportRx gates."""

    benchmark_summary = summarize_benchmark_sessions(benchmark_sessions)
    dashboard = build_feedback_dashboard(plan, feedback_by_week, benchmark_sessions)
    lab_readiness = build_lab_readiness_console(profile, passport, benchmark_summary)
    output_gates = build_output_prerequisites(passport, benchmark_summary, dashboard)
    evidence_library = build_evidence_library(root)
    evidence_files_present = evidence_files_present or {}

    safety_status = passport.get("safety_gate", {}).get("status", "UNKNOWN")
    measured_count = int(passport.get("measured_performance_areas", {}).get("count", 0) or 0)
    benchmark_count = int(benchmark_summary.get("session_count", 0) or 0)
    feedback_weeks = int(dashboard.get("adherence", {}).get("weeks_recorded", 0) or 0)
    retest_ready = bool(benchmark_summary.get("retest_ready"))
    output_summary = output_gates.get("summary", {})
    evidence_file_count = sum(1 for present in evidence_files_present.values() if present)
    evidence_file_total = len(evidence_files_present)

    gates = [
        _gate(
            "safety_gate",
            "Safety Gate",
            "blocked" if safety_status == "RED" else "ready",
            f"Safety Gate is {safety_status}. Safety can block training but never changes measured performance.",
            "Stop automated handoff and seek appropriate professional assessment." if safety_status == "RED" else "Continue with normal stop rules.",
        ),
        _gate(
            "measurement_depth",
            "Measurement Depth",
            "ready" if measured_count >= 2 else "waiting",
            f"{measured_count} measured performance dimensions recorded.",
            "Complete at least two measured dimensions before strongest area / main gap interpretation.",
        ),
        _gate(
            "benchmark_log",
            "Benchmark Log",
            "ready" if benchmark_count > 0 else "waiting",
            benchmark_summary.get("message", "No benchmark sessions recorded yet."),
            "Record raw results, protocol version, RPE, equipment, substitutions, and notes.",
        ),
        _gate(
            "output_gates",
            "Output Gates",
            "ready" if output_summary.get("blocked_outputs", 0) == 0 else "waiting",
            (
                f"{output_summary.get('active_outputs', 0)} active, "
                f"{output_summary.get('blocked_outputs', 0)} blocked, "
                f"{output_summary.get('provisional_outputs', 0)} provisional, "
                f"{output_summary.get('waiting_outputs', 0)} waiting."
            ),
            "Review blocked or provisional outputs before external handoff.",
        ),
        _gate(
            "feedback_loop",
            "Feedback Loop",
            "ready" if feedback_weeks > 0 else "waiting",
            f"{feedback_weeks} weekly feedback records saved.",
            "Record completion and average RPE after the first training week.",
        ),
        _gate(
            "retest_anchor",
            "Retest Anchor",
            "ready" if retest_ready else "waiting",
            "Comparable retest is available." if retest_ready else "No comparable retest yet.",
            "Repeat the same benchmark component with the same protocol before comparing raw change.",
        ),
        _gate(
            "evidence_library",
            "Evidence Library",
            "ready" if evidence_library["status"] == "ready_for_review" else "waiting",
            f"{evidence_library['source_count']} sources across {evidence_library['topic_count']} topics.",
            "Add source appraisal before using evidence claims in public handoff.",
        ),
        _gate(
            "evidence_files",
            "Evidence Files",
            "ready" if evidence_file_total == 0 or evidence_file_count == evidence_file_total else "waiting",
            (
                "Evidence file context not provided."
                if evidence_file_total == 0
                else f"{evidence_file_count} / {evidence_file_total} required evidence files present."
            ),
            "Keep claim policy, rule map, validation plan, and source index available for release review.",
        ),
    ]

    status, next_action = _overall_status(gates, passport)
    status_counts: dict[str, int] = {}
    for gate in gates:
        status_counts[gate["status"]] = status_counts.get(gate["status"], 0) + 1

    return {
        "schema": "sportrx.session_quality_review",
        "schema_version": "0.1",
        "status": status,
        "next_action": next_action,
        "gates": gates,
        "status_counts": status_counts,
        "summary": {
            "safety_gate": safety_status,
            "measured_performance_areas": measured_count,
            "benchmark_sessions": benchmark_count,
            "feedback_weeks": feedback_weeks,
            "retest_ready": retest_ready,
            "starter_path_available": bool(passport.get("starter_path", {}).get("available")),
            "lab_readiness_status": lab_readiness.get("status"),
            "active_outputs": output_summary.get("active_outputs", 0),
            "blocked_outputs": output_summary.get("blocked_outputs", 0),
            "evidence_sources": evidence_library["source_count"],
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def session_quality_review_markdown(review: dict[str, Any]) -> str:
    """Export a whole-session quality review as Markdown."""

    summary = review.get("summary", {})
    lines = [
        "# SportRx Session Quality Review",
        "",
        f"- Status: {review['status']}",
        f"- Next action: {review['next_action']}",
        f"- Claim boundary: {review['claim_boundary']}",
        "",
        "## Summary",
        f"- Safety Gate: {summary.get('safety_gate')}",
        f"- Measured performance areas: {summary.get('measured_performance_areas')}",
        f"- Benchmark sessions: {summary.get('benchmark_sessions')}",
        f"- Feedback weeks: {summary.get('feedback_weeks')}",
        f"- Retest ready: {summary.get('retest_ready')}",
        f"- Starter Path available: {summary.get('starter_path_available')}",
        f"- Active outputs: {summary.get('active_outputs')}",
        f"- Blocked outputs: {summary.get('blocked_outputs')}",
        f"- Evidence sources: {summary.get('evidence_sources')}",
        "",
        "## Gates",
    ]
    for gate in review["gates"]:
        lines.append(f"- [{gate['status']}] {gate['label']}: {gate['detail']} Action: {gate['action']}")
    return "\n".join(lines) + "\n"
