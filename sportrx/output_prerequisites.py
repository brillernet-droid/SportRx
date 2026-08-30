"""Output prerequisite register for SportRx.

The register explains why user-facing outputs are available, blocked, or
provisional. It does not add new scoring or override existing gates.
"""

from __future__ import annotations

from typing import Any

from .safety_gate import automated_handoff_allowed


CLAIM_BOUNDARY = (
    "Output prerequisites explain product gates only. They do not validate "
    "SportRx, create medical clearance, or prove that a prescription will work."
)


def _output(
    output_id: str,
    label: str,
    status: str,
    requirements: list[str],
    met: list[str],
    missing: list[str],
    affects_user: str,
) -> dict[str, Any]:
    return {
        "output_id": output_id,
        "label": label,
        "status": status,
        "requirements": requirements,
        "met": met,
        "missing": missing,
        "affects_user": affects_user,
    }


def build_output_prerequisites(
    passport: dict[str, Any],
    benchmark_summary: dict[str, Any] | None = None,
    feedback_dashboard: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build prerequisite states for the main SportRx outputs."""

    benchmark_summary = benchmark_summary or {}
    feedback_dashboard = feedback_dashboard or {}
    safety_status = passport.get("safety_gate", {}).get("status")
    measured_count = int(passport.get("measured_performance_areas", {}).get("count", 0) or 0)
    has_two_measured = measured_count >= 2
    starter_available = bool(passport.get("starter_path", {}).get("available"))
    feedback_weeks = int(feedback_dashboard.get("adherence", {}).get("weeks_recorded", 0) or 0)
    retest_ready = bool(benchmark_summary.get("retest_ready"))
    benchmark_sessions = int(benchmark_summary.get("session_count", 0) or 0)

    outputs = [
        _output(
            "safety_gate",
            "Safety Gate",
            "active" if safety_status else "blocked",
            ["Basic safety screen fields are present or intentionally empty."],
            [f"Safety Gate status: {safety_status}"] if safety_status else [],
            [] if safety_status else ["Safety Gate has not been evaluated."],
            "Can block automated training handoff; never changes measured performance.",
        ),
        _output(
            "training_profile",
            "Training Profile",
            "active",
            ["Profile can summarize known and unknown information."],
            ["Report can show current known/unknown state."],
            [],
            "Always available as a summary; may be limited when tests are missing.",
        ),
        _output(
            "strongest_area_main_gap",
            "Strongest Area / Main Gap",
            "active" if has_two_measured else "blocked_by_measurement",
            ["At least two measured performance dimensions."],
            [f"{measured_count} measured performance dimensions"] if has_two_measured else [],
            [] if has_two_measured else [f"Need 2 measured performance dimensions; currently {measured_count}."],
            "Controls whether SportRx compares strengths and gaps.",
        ),
        _output(
            "starter_path",
            "Starter Path",
            "active" if starter_available else "blocked",
            ["Safety Gate permits automated handoff.", "At least two measured performance dimensions.", "A usable main gap exists."],
            _starter_path_met(passport, has_two_measured),
            _starter_path_missing(passport, has_two_measured),
            "Controls whether SportRx creates a tailored 4-week starter path.",
        ),
        _output(
            "training_block",
            "4-week Training Block",
            "active" if starter_available else "blocked",
            ["Starter Path is available.", "Core FITT-VP plan is available."],
            ["Starter Path is available."] if starter_available else [],
            [] if starter_available else ["Starter Path is not available."],
            "Controls whether the Training page shows executable weekly sessions.",
        ),
        _output(
            "feedback_loop",
            "Feedback Loop",
            "active" if feedback_weeks > 0 else "provisional",
            ["A training plan exists.", "At least one week of completion/RPE feedback for adaptive decisions."],
            [f"{feedback_weeks} feedback weeks recorded"] if feedback_weeks else ["Training plan exists."],
            [] if feedback_weeks else ["No completed weekly feedback yet; progression is a preview."],
            "Controls whether progression is adaptive feedback or provisional preview.",
        ),
        _output(
            "retest_comparison",
            "Benchmark Retest Comparison",
            "active" if retest_ready else "waiting_for_retest",
            ["At least two sessions include the same comparable benchmark component."],
            [f"{benchmark_sessions} benchmark sessions recorded"] if retest_ready else [],
            [] if retest_ready else ["Repeat the same benchmark component before comparing change."],
            "Controls whether SportRx shows personal pre/post benchmark comparison.",
        ),
    ]

    status_counts: dict[str, int] = {}
    for item in outputs:
        status_counts[item["status"]] = status_counts.get(item["status"], 0) + 1

    return {
        "schema": "sportrx.output_prerequisites",
        "schema_version": "0.1",
        "outputs": outputs,
        "summary": {
            "total_outputs": len(outputs),
            "active_outputs": status_counts.get("active", 0),
            "blocked_outputs": sum(count for status, count in status_counts.items() if status.startswith("blocked")),
            "provisional_outputs": status_counts.get("provisional", 0),
            "waiting_outputs": status_counts.get("waiting_for_retest", 0),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _starter_path_met(passport: dict[str, Any], has_two_measured: bool) -> list[str]:
    met = []
    if automated_handoff_allowed(passport.get("safety_gate", {})):
        met.append("Safety Gate permits automated handoff.")
    if has_two_measured:
        met.append("At least two measured performance dimensions.")
    if passport.get("main_gap") not in {"Not enough measured data", "Not enough data"}:
        met.append("Main gap is usable.")
    return met


def _starter_path_missing(passport: dict[str, Any], has_two_measured: bool) -> list[str]:
    missing = []
    if not automated_handoff_allowed(passport.get("safety_gate", {})):
        missing.append("Safety Gate routing blocks automated handoff.")
    if not has_two_measured:
        missing.append("Need at least two measured performance dimensions.")
    if passport.get("main_gap") in {"Not enough measured data", "Not enough data"}:
        missing.append("Main gap is not yet meaningful.")
    return missing
