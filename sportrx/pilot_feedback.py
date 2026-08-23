"""Consent-first pilot feedback capture for SportRx.

Feedback records are local review artifacts. They are not validation data until
collected under an explicit pilot protocol with consent and analysis rules.
"""

from __future__ import annotations

import json
from datetime import date
from typing import Any


CLAIM_BOUNDARY = (
    "Pilot feedback captures local product-review observations only. It is not "
    "scientific validation, athlete norms, medical evidence, or proof of "
    "training outcomes."
)


RATING_FIELDS = {
    "setup_clarity": "First setup clarity",
    "measurement_realism": "Measurement realism",
    "trust": "Trust in the explanation",
    "actionability": "Next-action clarity",
    "visual_polish": "Visual polish",
}


PROMPT_SECTIONS = [
    {
        "section": "First impression",
        "questions": [
            "What did you think SportRx was for after the first screen?",
            "Did it feel more like a testing product or a generic AI fitness tool?",
        ],
    },
    {
        "section": "Measurement",
        "questions": [
            "Which inputs felt measurable and which felt vague?",
            "Did Not tested / measured / self-reported labels make the result more trustworthy?",
        ],
    },
    {
        "section": "Training handoff",
        "questions": [
            "Did the Starter Path appear only after enough measurement?",
            "Were the plan-actual reason codes understandable?",
        ],
    },
    {
        "section": "Trust boundary",
        "questions": [
            "Did the product avoid overclaiming validation, risk, or prediction?",
            "What claim or wording made you hesitate?",
        ],
    },
]


def build_pilot_feedback_prompt() -> dict[str, Any]:
    """Return the structured feedback prompt for alpha reviewers."""

    return {
        "schema": "sportrx.pilot_feedback_prompt",
        "schema_version": "0.1",
        "title": "SportRx Pilot Feedback Prompt",
        "rating_fields": RATING_FIELDS,
        "sections": PROMPT_SECTIONS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def create_pilot_feedback_entry(
    *,
    reviewer_role: str,
    ratings: dict[str, int],
    comments: dict[str, str],
    consent_to_contact: bool = False,
    contact: str = "",
    review_date: str | None = None,
) -> dict[str, Any]:
    """Create a local pilot feedback entry."""

    normalized_ratings = {key: _rating(ratings.get(key)) for key in RATING_FIELDS}
    return {
        "schema": "sportrx.pilot_feedback_entry",
        "schema_version": "0.1",
        "review_date": review_date or date.today().isoformat(),
        "reviewer_role": reviewer_role.strip() or "unspecified",
        "ratings": normalized_ratings,
        "comments": {key: str(value).strip() for key, value in comments.items() if str(value).strip()},
        "consent": {
            "local_product_review": True,
            "consent_to_contact": bool(consent_to_contact),
            "contact": contact.strip() if consent_to_contact else "",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def summarize_pilot_feedback(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize local pilot feedback entries without making validation claims."""

    averages: dict[str, float | None] = {}
    for key in RATING_FIELDS:
        values = [int(entry.get("ratings", {}).get(key, 0)) for entry in entries if entry.get("ratings", {}).get(key)]
        averages[key] = round(sum(values) / len(values), 1) if values else None
    low_fields = [key for key, value in averages.items() if value is not None and value < 3.5]
    return {
        "schema": "sportrx.pilot_feedback_summary",
        "schema_version": "0.1",
        "entry_count": len(entries),
        "average_ratings": averages,
        "review_flags": low_fields,
        "status": "needs_more_feedback" if len(entries) < 5 else "ready_for_pattern_review",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_pilot_review_console(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a product-review console for local alpha feedback."""

    summary = summarize_pilot_feedback(entries)
    averages = summary["average_ratings"]
    scored_values = [value for value in averages.values() if value is not None]
    overall_average = round(sum(scored_values) / len(scored_values), 1) if scored_values else None
    consent_count = sum(1 for entry in entries if entry.get("consent", {}).get("consent_to_contact"))
    comment_count = sum(len(entry.get("comments", {})) for entry in entries)
    lowest_field = None
    lowest_value = None
    for key, value in averages.items():
        if value is not None and (lowest_value is None or value < lowest_value):
            lowest_field = key
            lowest_value = value

    if summary["entry_count"] == 0:
        next_action = "Collect the first local product-review entry after a guided demo."
    elif summary["entry_count"] < 5:
        next_action = "Collect at least five entries before looking for product-review patterns."
    elif summary["review_flags"]:
        next_action = "Review low-scoring fields before public beta messaging."
    else:
        next_action = "Review comments and export the local pilot feedback bundle."

    return {
        "schema": "sportrx.pilot_review_console",
        "schema_version": "0.1",
        "status": summary["status"],
        "entry_count": summary["entry_count"],
        "overall_average": overall_average,
        "lowest_field": lowest_field,
        "lowest_value": lowest_value,
        "consent_to_contact_count": consent_count,
        "comment_count": comment_count,
        "review_flags": summary["review_flags"],
        "next_action": next_action,
        "cards": [
            {
                "id": "entries",
                "label": "Entries",
                "value": summary["entry_count"],
                "detail": "Local product-review entries only.",
                "status": "ready" if summary["entry_count"] >= 5 else "waiting",
            },
            {
                "id": "overall_average",
                "label": "Average Rating",
                "value": "Not enough data" if overall_average is None else overall_average,
                "detail": "Average across current rating fields.",
                "status": "ready" if overall_average is not None and overall_average >= 3.5 else "waiting",
            },
            {
                "id": "lowest_field",
                "label": "Lowest Field",
                "value": "Not enough data" if lowest_field is None else RATING_FIELDS[lowest_field],
                "detail": "Use this to prioritize product fixes, not validation claims.",
                "status": "ready" if lowest_field is not None and lowest_field not in summary["review_flags"] else "waiting",
            },
            {
                "id": "review_flags",
                "label": "Review Flags",
                "value": len(summary["review_flags"]),
                "detail": "Fields below 3.5 should be inspected before broader sharing.",
                "status": "ready" if not summary["review_flags"] else "waiting",
            },
            {
                "id": "comments",
                "label": "Comments",
                "value": comment_count,
                "detail": "Qualitative comments explain rating patterns.",
                "status": "ready" if comment_count else "waiting",
            },
            {
                "id": "consent",
                "label": "Contact Consent",
                "value": consent_count,
                "detail": "Contact information is stored only when consent is checked.",
                "status": "ready" if consent_count else "waiting",
            },
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def pilot_feedback_prompt_markdown(prompt: dict[str, Any] | None = None) -> str:
    """Export the feedback prompt as markdown."""

    prompt = prompt or build_pilot_feedback_prompt()
    lines = [
        f"# {prompt['title']}",
        "",
        f"- Claim boundary: {prompt['claim_boundary']}",
        "",
        "## Ratings",
    ]
    for key, label in prompt["rating_fields"].items():
        lines.append(f"- {label} (`{key}`): 1-5")
    for section in prompt["sections"]:
        lines.extend(["", f"## {section['section']}"])
        for question in section["questions"]:
            lines.append(f"- {question}")
    return "\n".join(lines) + "\n"


def export_pilot_feedback_json(entries: list[dict[str, Any]]) -> str:
    """Export local feedback entries as JSON."""

    return json.dumps(
        {
            "schema": "sportrx.pilot_feedback_export",
            "schema_version": "0.1",
            "summary": summarize_pilot_feedback(entries),
            "entries": entries,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


def pilot_feedback_markdown(entries: list[dict[str, Any]]) -> str:
    """Export local feedback entries as markdown."""

    summary = summarize_pilot_feedback(entries)
    lines = [
        "# SportRx Pilot Feedback",
        "",
        f"- Entries: {summary['entry_count']}",
        f"- Status: {summary['status']}",
        f"- Claim boundary: {summary['claim_boundary']}",
        "",
        "## Average Ratings",
    ]
    for key, value in summary["average_ratings"].items():
        lines.append(f"- {RATING_FIELDS[key]}: {'not enough data' if value is None else value}")
    lines.extend(["", "## Entries"])
    for index, entry in enumerate(entries, start=1):
        lines.append(f"- Entry {index}: {entry['reviewer_role']} on {entry['review_date']}")
        for key, value in entry.get("comments", {}).items():
            lines.append(f"  - {key}: {value}")
    if not entries:
        lines.append("- No local pilot feedback entries recorded yet.")
    return "\n".join(lines) + "\n"


def _rating(value: int | None) -> int:
    if value is None:
        return 0
    return max(1, min(5, int(value)))
