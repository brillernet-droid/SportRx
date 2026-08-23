import json

from sportrx.pilot_feedback import (
    build_pilot_feedback_prompt,
    build_pilot_review_console,
    create_pilot_feedback_entry,
    export_pilot_feedback_json,
    pilot_feedback_markdown,
    pilot_feedback_prompt_markdown,
    summarize_pilot_feedback,
)


def test_pilot_feedback_prompt_exports_measurement_questions():
    prompt = build_pilot_feedback_prompt()
    markdown = pilot_feedback_prompt_markdown(prompt)

    assert prompt["schema"] == "sportrx.pilot_feedback_prompt"
    assert "Measurement" in markdown
    assert "not scientific validation" in prompt["claim_boundary"]


def test_create_pilot_feedback_entry_preserves_consent_boundary():
    entry = create_pilot_feedback_entry(
        reviewer_role="coach",
        ratings={"setup_clarity": 5, "measurement_realism": 4, "trust": 4, "actionability": 5, "visual_polish": 4},
        comments={"first_impression": "Feels like a testing product."},
        consent_to_contact=False,
        contact="hidden@example.com",
        review_date="2026-08-22",
    )

    assert entry["schema"] == "sportrx.pilot_feedback_entry"
    assert entry["consent"]["contact"] == ""
    assert entry["ratings"]["setup_clarity"] == 5
    assert "testing product" in entry["comments"]["first_impression"]


def test_pilot_feedback_summary_and_exports_do_not_claim_validation():
    entry = create_pilot_feedback_entry(
        reviewer_role="athlete",
        ratings={"setup_clarity": 4, "measurement_realism": 3, "trust": 4, "actionability": 4, "visual_polish": 5},
        comments={"confusing": "Some test names need examples."},
        review_date="2026-08-22",
    )
    summary = summarize_pilot_feedback([entry])
    exported = json.loads(export_pilot_feedback_json([entry]))
    markdown = pilot_feedback_markdown([entry])

    assert summary["entry_count"] == 1
    assert summary["status"] == "needs_more_feedback"
    assert exported["schema"] == "sportrx.pilot_feedback_export"
    assert "not scientific validation" in exported["claim_boundary"]
    assert "SportRx Pilot Feedback" in markdown


def test_pilot_review_console_summarizes_local_product_feedback_only():
    entry = create_pilot_feedback_entry(
        reviewer_role="coach",
        ratings={"setup_clarity": 5, "measurement_realism": 4, "trust": 4, "actionability": 5, "visual_polish": 4},
        comments={"next_improvement": "Show examples for test setup."},
        consent_to_contact=True,
        contact="coach@example.com",
        review_date="2026-08-22",
    )

    empty = build_pilot_review_console([])
    one = build_pilot_review_console([entry])
    five = build_pilot_review_console([entry, entry, entry, entry, entry])

    assert empty["status"] == "needs_more_feedback"
    assert empty["overall_average"] is None
    assert one["entry_count"] == 1
    assert one["consent_to_contact_count"] == 1
    assert one["comment_count"] == 1
    assert five["status"] == "ready_for_pattern_review"
    assert "not scientific validation" in five["claim_boundary"]
