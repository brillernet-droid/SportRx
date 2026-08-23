"""Feedback loop dashboard objects for SportRx.

This layer summarizes training feedback and benchmark retests. It does not
predict outcomes or validate minimal meaningful changes.
"""

from __future__ import annotations

from typing import Any

from .benchmark_log import compare_retest_sessions, summarize_benchmark_sessions
from .plan_actual import classify_plan_actual


CLAIM_BOUNDARY = (
    "Feedback loop summaries use user-entered completion, RPE, and raw retest "
    "records. They are not predictions, validated recovery scores, medical "
    "clearance, or injury-risk estimates."
)


def _decision_map(plan: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(item["after_week"]): item for item in plan.get("progression_log", [])}


def _weekly_feedback_rows(plan: dict[str, Any], feedback_by_week: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    decisions = _decision_map(plan)
    rows = []
    for week in plan.get("weeks", [])[:-1]:
        week_number = int(week["week"])
        feedback = feedback_by_week.get(week_number, {})
        planned = int(week.get("frequency_per_week", 0) or 0)
        completed = feedback.get("completed_sessions")
        completion_rate = None
        if completed is not None and planned > 0:
            completion_rate = round(int(completed) / planned, 2)
        decision = decisions.get(week_number, {}).get("decision", {})
        if decision.get("plan_actual"):
            plan_actual = decision["plan_actual"]
        else:
            plan_actual = classify_plan_actual(
                planned,
                completed,
                feedback.get("average_rpe"),
                felt_too_hard=bool(feedback.get("felt_too_hard", False)),
                adverse_event=bool(feedback.get("adverse_event", False)),
            )
        rows.append(
            {
                "week": week_number,
                "planned_sessions": planned,
                "completed_sessions": completed,
                "completion_rate": completion_rate,
                "average_rpe": feedback.get("average_rpe"),
                "felt_too_hard": bool(feedback.get("felt_too_hard", False)),
                "adverse_event": bool(feedback.get("adverse_event", False)),
                "decision_action": decision.get("action", "not_entered"),
                "decision_rationale": decision.get("rationale", "No feedback entered yet."),
                "plan_actual": plan_actual,
                "reason_codes": plan_actual["reason_codes"],
                "reason_labels": plan_actual["reason_labels"],
                "flags": plan_actual["flags"],
            }
        )
    return rows


def _adherence_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    recorded = [row for row in rows if row["completed_sessions"] is not None]
    planned_total = sum(row["planned_sessions"] for row in recorded)
    completed_total = sum(int(row["completed_sessions"]) for row in recorded)
    rpes = [float(row["average_rpe"]) for row in recorded if row["average_rpe"] is not None]
    if not recorded:
        status = "No weekly feedback recorded"
        average_completion = None
    else:
        average_completion = round(completed_total / planned_total, 2) if planned_total else None
        status = "On track" if average_completion is not None and average_completion >= 0.8 else "Needs review"
        if any(row["adverse_event"] for row in recorded):
            status = "Pause and review"
    return {
        "weeks_recorded": len(recorded),
        "planned_sessions": planned_total,
        "completed_sessions": completed_total,
        "average_completion_rate": average_completion,
        "average_rpe": round(sum(rpes) / len(rpes), 1) if rpes else None,
        "status": status,
    }


def _next_actions(adherence: dict[str, Any], retest_comparisons: list[dict[str, Any]]) -> list[str]:
    if adherence["status"] == "Pause and review":
        return [
            "Pause automated progression because an adverse event was reported.",
            "Clarify the safety issue before increasing training.",
            "Keep benchmark records raw; do not interpret performance change during a stop flag.",
        ]
    if adherence["weeks_recorded"] == 0:
        return [
            "Enter Week 1 feedback after completing the first training week.",
            "Record completed sessions and average RPE.",
            "Retest only after a repeatable training block or benchmark session.",
        ]
    if not retest_comparisons:
        return [
            "Continue weekly feedback entry.",
            "Complete a later Benchmark Log using the same protocol.",
            "Compare raw retest values before changing the next training focus.",
        ]
    return [
        "Review weekly feedback together with raw retest change.",
        "Use the same benchmark protocol for the next retest.",
        "Keep progression conservative unless completion and RPE remain stable.",
    ]


def build_feedback_dashboard(
    plan: dict[str, Any],
    feedback_by_week: dict[int, dict[str, Any]],
    benchmark_sessions: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a dashboard object for weekly feedback and benchmark retests."""

    benchmark_summary = summarize_benchmark_sessions(benchmark_sessions)
    retest_comparisons = compare_retest_sessions(benchmark_sessions)
    if not plan.get("weeks"):
        return {
            "schema": "sportrx.feedback_dashboard",
            "schema_version": "0.1",
            "available": False,
            "reason": "No active training plan is available.",
            "weekly_feedback": [],
            "plan_actual_reasons": [],
            "adherence": _adherence_summary([]),
            "latest_progression": None,
            "benchmark_summary": benchmark_summary,
            "retest_comparisons": retest_comparisons,
            "next_actions": ["Resolve the safety gate or complete required measurements before training feedback."],
            "claim_boundary": CLAIM_BOUNDARY,
        }

    weekly_rows = _weekly_feedback_rows(plan, feedback_by_week)
    adherence = _adherence_summary(weekly_rows)
    latest_progression = plan.get("progression_log", [])[-1] if plan.get("progression_log") else None
    return {
        "schema": "sportrx.feedback_dashboard",
        "schema_version": "0.1",
        "available": True,
        "weekly_feedback": weekly_rows,
        "plan_actual_reasons": [row["plan_actual"] for row in weekly_rows],
        "adherence": adherence,
        "latest_progression": latest_progression,
        "benchmark_summary": benchmark_summary,
        "retest_comparisons": retest_comparisons,
        "next_actions": _next_actions(adherence, retest_comparisons),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def feedback_dashboard_markdown(dashboard: dict[str, Any]) -> str:
    """Export the feedback dashboard as markdown."""

    lines = [
        "# SportRx Feedback Loop Dashboard",
        "",
        f"- Available: {dashboard['available']}",
        f"- Claim boundary: {dashboard['claim_boundary']}",
        "",
        "## Adherence",
    ]
    adherence = dashboard["adherence"]
    for key in ["status", "weeks_recorded", "planned_sessions", "completed_sessions", "average_completion_rate", "average_rpe"]:
        lines.append(f"- {key}: {adherence.get(key)}")

    lines.extend(["", "## Weekly Feedback"])
    for row in dashboard["weekly_feedback"] or ["No weekly feedback recorded."]:
        if isinstance(row, str):
            lines.append(f"- {row}")
        else:
            lines.append(
                f"- Week {row['week']}: {row['completed_sessions']}/{row['planned_sessions']} sessions, "
                f"RPE {row['average_rpe']}, decision {row['decision_action']}, "
                f"reasons {', '.join(row['reason_codes'])}"
            )

    lines.extend(["", "## Plan-Actual Reason Codes"])
    for item in dashboard.get("plan_actual_reasons", []):
        lines.append(
            f"- {item['action_label']}: {', '.join(item['reason_codes'])}; "
            f"flags: {', '.join(item['flags']) if item['flags'] else 'none'}"
        )

    lines.extend(["", "## Benchmark Retest"])
    if dashboard["retest_comparisons"]:
        for item in dashboard["retest_comparisons"]:
            lines.append(
                f"- {item['test']}: {item['first_value']} -> {item['latest_value']} "
                f"{item['value_unit']} ({item['direction']})"
            )
    else:
        lines.append("- No repeated benchmark components yet.")

    lines.extend(["", "## Next Actions"])
    for action in dashboard["next_actions"]:
        lines.append(f"- {action}")
    return "\n".join(lines) + "\n"
