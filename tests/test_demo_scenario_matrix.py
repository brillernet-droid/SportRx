from sportrx.demo_scenario_matrix import build_demo_scenario_matrix, demo_scenario_matrix_markdown


def test_demo_scenario_matrix_compares_all_review_states():
    matrix = build_demo_scenario_matrix()

    assert matrix["schema"] == "sportrx.demo_scenario_matrix"
    assert matrix["status"] == "ready"
    assert matrix["scenario_count"] == 3
    assert matrix["complete_loop_count"] == 1
    assert matrix["measurement_gated_count"] >= 1
    assert matrix["recommended_first_scenario"] == "complete_loop"
    assert "not validation data" in matrix["claim_boundary"]


def test_demo_scenario_matrix_rows_show_gates_and_review_pages():
    matrix = build_demo_scenario_matrix()
    rows = {row["id"]: row for row in matrix["rows"]}

    assert rows["measure_first"]["starter_path_available"] is False
    assert rows["measure_first"]["measured_area_count"] < 2
    assert "Benchmark Protocol" in rows["measure_first"]["recommended_pages"]
    assert rows["benchmark_underway"]["product_state"] == "partial_measurement"
    assert rows["complete_loop"]["starter_path_available"] is True
    assert rows["complete_loop"]["retest_ready"] is True
    assert "Release QA" in rows["complete_loop"]["recommended_pages"]


def test_demo_scenario_matrix_markdown_exports_comparison():
    matrix = build_demo_scenario_matrix()
    markdown = demo_scenario_matrix_markdown(matrix)

    assert "# SportRx Demo Scenario Matrix" in markdown
    assert "Measure First" in markdown
    assert "Benchmark Underway" in markdown
    assert "Complete Loop" in markdown
    assert "Claim boundary" in markdown
