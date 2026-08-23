from sportrx.benchmark_worksheet import build_benchmark_worksheet, benchmark_worksheet_markdown


def test_benchmark_worksheet_builds_standard_test_day_sheet():
    worksheet = build_benchmark_worksheet(["row", "kettlebell"])

    assert worksheet["schema"] == "sportrx.benchmark_worksheet"
    assert worksheet["benchmark_path"] == "standard"
    assert worksheet["protocol_version"] == "0.1"
    assert len(worksheet["session_setup"]) >= 4
    assert len(worksheet["safety_checklist"]) >= 3
    assert any(row["component_id"] == "run_1km" for row in worksheet["component_rows"])
    assert any(row["component_id"] == "row_or_ski_1km" for row in worksheet["component_rows"])
    assert "does not score performance" in worksheet["claim_boundary"]


def test_benchmark_worksheet_builds_low_equipment_path():
    worksheet = build_benchmark_worksheet([])

    assert worksheet["benchmark_path"] == "low_equipment"
    assert any(row["component_id"] == "run_1km_or_6min" for row in worksheet["component_rows"])
    assert any("Missing components stay Not tested" in item for item in worksheet["recording_principles"])


def test_benchmark_worksheet_markdown_is_printable():
    markdown = benchmark_worksheet_markdown(build_benchmark_worksheet(["ski"]))

    assert "# SportRx Hybrid Benchmark v1 Worksheet" in markdown
    assert "Safety Checklist" in markdown
    assert "Completed: [ ] yes / [ ] no" in markdown
    assert "Retest anchor" in markdown
