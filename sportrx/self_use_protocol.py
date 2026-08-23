"""Phase 0 self-use protocol pack for SportRx.

This module prepares an operational self-use plan. It does not turn self-use
into validation evidence by itself.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Phase 0 Self-Use Protocol guides one builder through product testing only. "
    "It does not validate SportRx, create athlete norms, predict outcomes, "
    "estimate injury risk, or provide medical clearance."
)


MINIMUM_DATA_FIELDS = [
    {
        "field": "self_use_id",
        "why": "Links baseline, weekly feedback, and retest without using a public identity.",
        "required": True,
    },
    {
        "field": "test_date",
        "why": "Separates baseline, weekly notes, and Week 4 retest chronologically.",
        "required": True,
    },
    {
        "field": "safety_gate_status",
        "why": "Confirms whether automated training should proceed; it never changes performance scoring.",
        "required": True,
    },
    {
        "field": "equipment_setup",
        "why": "Keeps baseline and retest comparable when standard and low-equipment paths differ.",
        "required": True,
    },
    {
        "field": "raw_benchmark_results",
        "why": "Preserves measured component values; missing tests must remain Not tested.",
        "required": True,
    },
    {
        "field": "session_rpe",
        "why": "Captures subjective difficulty after training or testing without replacing measured results.",
        "required": True,
    },
    {
        "field": "weekly_adherence",
        "why": "Shows whether the starter block was actually completed before interpreting retest context.",
        "required": True,
    },
    {
        "field": "protocol_deviation_notes",
        "why": "Records substitutions, skipped items, pain, equipment changes, and timing differences.",
        "required": True,
    },
]


PRE_START_CHECKS = [
    "Safety Gate result is visible before any training recommendation.",
    "Hybrid Benchmark v1 path is selected from actual equipment access.",
    "Baseline worksheet or Benchmark Log is ready before testing.",
    "Protocol, export bundle, and claim boundaries are saved before Week 1.",
    "Self-use notes template is ready for friction, confusion, and wording issues.",
]


STOP_OR_REVIEW_RULES = [
    "Safety Gate returns RED or requests professional review.",
    "Chest pain, fainting, unusual breathlessness, or other abnormal symptoms appear.",
    "Pain changes movement quality or forces test substitution.",
    "Baseline and retest setup cannot be made comparable.",
    "Week 4 retest is missing; do not interpret training response.",
]


SUCCESS_CRITERIA = [
    "The builder can complete setup without external explanation.",
    "Benchmark instructions are clear enough to run without ad hoc decisions.",
    "Missing performance data remains Not tested in every output.",
    "Weekly feedback explains progression context without pretending to validate the system.",
    "Week 4 retest can be exported with comparable raw measurements and deviation notes.",
]


def _schedule() -> list[dict[str, Any]]:
    return [
        {
            "week": "Week 0",
            "label": "Baseline setup",
            "goal": "Create the first measured picture before training starts.",
            "required_actions": [
                "Run Safety Gate.",
                "Choose standard or low-equipment Hybrid Benchmark v1 path.",
                "Record raw benchmark results and mark skipped items as Not tested.",
                "Export baseline Review Pack snapshot.",
            ],
            "outputs": ["Safety Gate status", "Baseline Benchmark Log", "Protocol Deviation Review"],
        },
        {
            "week": "Week 1",
            "label": "First training week",
            "goal": "Check whether the starter block is usable in real life.",
            "required_actions": [
                "Follow the available starter block only if measurement gates allow it.",
                "Record completed sessions, session RPE, and missed-session reason codes.",
                "Write one short product-friction note after the week.",
            ],
            "outputs": ["Weekly Feedback", "Plan-Actual reasons", "Product-friction note"],
        },
        {
            "week": "Week 2",
            "label": "Adjustment week",
            "goal": "Observe whether progression rules feel explainable and conservative.",
            "required_actions": [
                "Review previous-week completion and RPE.",
                "Apply progression only through existing rule outputs.",
                "Record any wording, intensity, or schedule confusion.",
            ],
            "outputs": ["Weekly Feedback", "Progression explanation", "Confusion note"],
        },
        {
            "week": "Week 3",
            "label": "Stability week",
            "goal": "Check whether the plan remains practical before retesting.",
            "required_actions": [
                "Continue the starter block without adding unplanned sport packs.",
                "Record adherence, RPE, pain/symptom notes, and protocol deviations.",
                "Confirm retest setup can match baseline.",
            ],
            "outputs": ["Weekly Feedback", "Retest setup check", "Deviation notes"],
        },
        {
            "week": "Week 4",
            "label": "Retest and export",
            "goal": "Retest the same measured dimensions and keep interpretation guarded.",
            "required_actions": [
                "Repeat the same Hybrid Benchmark v1 components where possible.",
                "Run Retest Interpretation Guard before describing change.",
                "Export the full Review Pack with baseline, feedback, retest, and notes.",
            ],
            "outputs": ["Retest Benchmark Log", "Retest Interpretation Guard", "Review Pack ZIP"],
        },
    ]


def build_self_use_protocol(validation_matrix: dict[str, Any], profile: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a Phase 0 self-use protocol from validation-readiness state."""

    profile = profile or {}
    capture_ready = bool(validation_matrix.get("capture_ready"))
    equipment = profile.get("equipment_access") or []
    equipment_path = "standard_or_low_equipment_path_pending"
    if equipment:
        equipment_path = "selected_from_available_equipment"

    blocked_claims = list(validation_matrix.get("blocked_claims", []))
    return {
        "schema": "sportrx.self_use_protocol",
        "schema_version": "0.1",
        "status": "ready_to_run_phase_0" if capture_ready else "needs_capture_setup",
        "duration_weeks": 4,
        "participant_scope": "1 builder",
        "current_validation_claim": validation_matrix.get("current_validation_claim", "Prototype; not validated."),
        "equipment_path": equipment_path,
        "capture_checks": validation_matrix.get("capture_checks", []),
        "pre_start_checks": PRE_START_CHECKS,
        "weekly_schedule": _schedule(),
        "minimum_data_fields": MINIMUM_DATA_FIELDS,
        "stop_or_review_rules": STOP_OR_REVIEW_RULES,
        "success_criteria": SUCCESS_CRITERIA,
        "blocked_claims": blocked_claims,
        "next_action": (
            "Run Week 0 baseline using real builder data, then export the baseline snapshot."
            if capture_ready
            else "Complete validation data-capture gates before starting Phase 0 self-use."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def self_use_protocol_markdown(protocol: dict[str, Any]) -> str:
    """Export the Phase 0 self-use protocol as Markdown."""

    lines = [
        "# SportRx Phase 0 Self-Use Protocol",
        "",
        f"- Status: {protocol['status']}",
        f"- Duration: {protocol['duration_weeks']} weeks",
        f"- Participant scope: {protocol['participant_scope']}",
        f"- Current validation claim: {protocol['current_validation_claim']}",
        f"- Next action: {protocol['next_action']}",
        f"- Claim boundary: {protocol['claim_boundary']}",
        "",
        "## Pre-Start Checks",
    ]
    for item in protocol["pre_start_checks"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Weekly Schedule"])
    for week in protocol["weekly_schedule"]:
        lines.extend(
            [
                f"### {week['week']} - {week['label']}",
                f"- Goal: {week['goal']}",
                "- Required actions:",
            ]
        )
        for action in week["required_actions"]:
            lines.append(f"  - {action}")
        lines.append(f"- Outputs: {', '.join(week['outputs'])}")

    lines.extend(["", "## Minimum Data Fields"])
    for field in protocol["minimum_data_fields"]:
        required = "required" if field["required"] else "optional"
        lines.append(f"- `{field['field']}` ({required}): {field['why']}")

    lines.extend(["", "## Stop Or Review Rules"])
    for rule in protocol["stop_or_review_rules"]:
        lines.append(f"- {rule}")

    lines.extend(["", "## Success Criteria"])
    for item in protocol["success_criteria"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Blocked Claims"])
    for claim in protocol["blocked_claims"]:
        lines.append(f"- {claim}")
    return "\n".join(lines) + "\n"
