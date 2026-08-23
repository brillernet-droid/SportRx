"""Protocol-source guide for protocol-derived SportRx lab scores.

The guide documents provenance options for Station and Work capacity protocol
scores. It does not validate the protocol or score performance.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Protocol Source Guide documents allowed provenance labels for "
    "protocol-derived SportRx lab scores. It does not validate protocols, "
    "create norms, score performance, predict outcomes, or provide medical "
    "clearance."
)


PROTOCOL_SOURCE_PRESETS = [
    "SportRx Hybrid Benchmark v1 / standard",
    "SportRx Hybrid Benchmark v1 / low-equipment",
    "Benchmark Log import",
    "Other documented protocol",
]


PROTOCOL_SOURCE_OPTIONS = ["", *PROTOCOL_SOURCE_PRESETS]


PROTOCOL_SOURCE_HELP = {
    "": "Not selected",
    "SportRx Hybrid Benchmark v1 / standard": "Use when the score came from the standard SportRx Hybrid Benchmark v1 setup.",
    "SportRx Hybrid Benchmark v1 / low-equipment": "Use when the score came from the low-equipment SportRx Hybrid Benchmark v1 path.",
    "Benchmark Log import": "Use when the score was imported from a saved Benchmark Log record.",
    "Other documented protocol": "Use only when you can name the protocol, version, and setup notes.",
}


SOURCE_ROWS = [
    {
        "source": "SportRx Hybrid Benchmark v1 / standard",
        "status": "accepted_preset",
        "use_when": "The result came from the standard SportRx Hybrid Benchmark v1 setup.",
        "accepted_for": ["station_test_protocol", "work_capacity_test_protocol"],
        "requires_note": False,
        "not_allowed_for": "Official HYROX ranking, percentile, race prediction, or medical clearance.",
    },
    {
        "source": "SportRx Hybrid Benchmark v1 / low-equipment",
        "status": "accepted_preset",
        "use_when": "The result came from the low-equipment SportRx Hybrid Benchmark v1 path.",
        "accepted_for": ["station_test_protocol", "work_capacity_test_protocol"],
        "requires_note": False,
        "not_allowed_for": "Comparing directly with standard-equipment results without noting the path.",
    },
    {
        "source": "Benchmark Log import",
        "status": "accepted_preset",
        "use_when": "The value was imported from a saved Benchmark Log component with compatible units.",
        "accepted_for": ["station_test_protocol", "work_capacity_test_protocol"],
        "requires_note": False,
        "not_allowed_for": "Converting raw-only rounds, distance, or mixed work into a score.",
    },
    {
        "source": "Other documented protocol",
        "status": "accepted_with_note",
        "use_when": "A non-SportRx protocol was used and the protocol name, version, setup, and load are documented.",
        "accepted_for": ["station_test_protocol", "work_capacity_test_protocol"],
        "requires_note": True,
        "not_allowed_for": "Vague labels such as gym test, coach score, hard workout, or personal feeling.",
    },
]


def resolve_protocol_source_choice(current_value: object) -> str:
    """Map a stored protocol-source string back to a UI preset choice."""

    value = str(current_value or "").strip()
    if value in PROTOCOL_SOURCE_OPTIONS:
        return value
    if value:
        return "Other documented protocol"
    return ""


def resolve_protocol_source_value(choice: str, note: object = "") -> str:
    """Return the stored protocol source from a preset and optional note."""

    choice = str(choice or "").strip()
    note_value = str(note or "").strip()
    if choice == "Other documented protocol":
        return note_value
    return choice


def build_protocol_source_guide(profile: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a guide for protocol-source selection and current source state."""

    profile = profile or {}
    source_fields = [
        {
            "field_id": "station_test_protocol",
            "label": "Station circuit protocol source",
            "current_value": str(profile.get("station_test_protocol", "") or "").strip(),
            "score_field": "station_test_score",
            "score_entered": profile.get("station_test_score") is not None,
        },
        {
            "field_id": "work_capacity_test_protocol",
            "label": "Work capacity protocol source",
            "current_value": str(profile.get("work_capacity_test_protocol", "") or "").strip(),
            "score_field": "work_capacity_test_score",
            "score_entered": profile.get("work_capacity_test_score") is not None,
        },
    ]
    for item in source_fields:
        current = item["current_value"]
        choice = resolve_protocol_source_choice(current)
        item["selected_preset"] = choice
        item["status"] = (
            "not_required"
            if not item["score_entered"]
            else "source_recorded"
            if current
            else "source_required"
        )
        item["next_action"] = (
            "No protocol source needed until the protocol score is entered."
            if item["status"] == "not_required"
            else "Keep the same source label for retest."
            if item["status"] == "source_recorded"
            else "Select a preset source or document another protocol before using this score."
        )

    required_count = sum(1 for item in source_fields if item["score_entered"])
    recorded_count = sum(1 for item in source_fields if item["score_entered"] and item["current_value"])
    status = "protocol_sources_ready" if recorded_count == required_count else "needs_protocol_source"
    if required_count == 0:
        status = "waiting_for_protocol_scores"

    return {
        "schema": "sportrx.protocol_source_guide",
        "schema_version": "0.1",
        "status": status,
        "preset_count": len(PROTOCOL_SOURCE_PRESETS),
        "source_fields": source_fields,
        "sources": SOURCE_ROWS,
        "required_source_count": required_count,
        "recorded_source_count": recorded_count,
        "primary_message": (
            "Protocol-derived Station and Work capacity scores need a named "
            "source before they can count as measured performance."
        ),
        "next_action": (
            "Use SportRx Benchmark presets when possible; use Other documented "
            "protocol only when protocol details are known."
        ),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def protocol_source_guide_markdown(guide: dict[str, Any]) -> str:
    """Export the protocol-source guide as Markdown."""

    lines = [
        "# SportRx Protocol Source Guide",
        "",
        f"- Status: {guide['status']}",
        f"- Presets: {guide['preset_count']}",
        f"- Required sources: {guide['recorded_source_count']} / {guide['required_source_count']}",
        f"- Claim boundary: {guide['claim_boundary']}",
        "",
        guide["primary_message"],
        "",
        "## Accepted Sources",
    ]
    for item in guide["sources"]:
        lines.extend(
            [
                "",
                f"### {item['source']}",
                f"- Status: {item['status']}",
                f"- Use when: {item['use_when']}",
                f"- Accepted for: {', '.join(item['accepted_for'])}",
                f"- Requires note: {item['requires_note']}",
                f"- Not allowed for: {item['not_allowed_for']}",
            ]
        )
    lines.extend(["", "## Current Profile Fields"])
    for item in guide["source_fields"]:
        lines.append(
            f"- `{item['field_id']}` - {item['status']}: "
            f"{item['current_value'] or 'Not selected'}. {item['next_action']}"
        )
    return "\n".join(lines) + "\n"
