import csv
from io import StringIO

from sportrx.alpha_dataset_template import (
    alpha_dataset_csv_templates,
    alpha_dataset_dictionary_markdown,
    build_alpha_dataset_template,
)


def test_alpha_dataset_template_declares_scope_and_boundaries():
    template = build_alpha_dataset_template()

    assert template["schema"] == "sportrx.alpha_dataset_template"
    assert template["status"] == "ready_for_alpha_capture"
    assert template["table_count"] == 4
    assert "5-10 recreational adult" in template["participant_scope"]
    assert "does not validate SportRx" in template["claim_boundary"]
    assert any("do not impute averages" in rule for rule in template["minimum_rules"])


def test_alpha_dataset_csv_templates_are_header_only():
    template = build_alpha_dataset_template()
    csv_templates = alpha_dataset_csv_templates(template)

    assert set(csv_templates) == {"participants", "benchmark_sessions", "weekly_feedback", "pilot_review"}
    for table in template["tables"]:
        content = csv_templates[table["id"]]
        rows = list(csv.reader(StringIO(content)))
        assert rows == [table["fields"]]
        assert "participant_id" in rows[0]


def test_alpha_dataset_dictionary_lists_tables_and_rules():
    markdown = alpha_dataset_dictionary_markdown(build_alpha_dataset_template())

    assert "# SportRx Alpha Dataset Template" in markdown
    assert "## Minimum Rules" in markdown
    assert "participants" in markdown
    assert "benchmark_sessions" in markdown
    assert "weekly_feedback" in markdown
    assert "pilot_review" in markdown
    assert "not_tested_reason" in markdown
