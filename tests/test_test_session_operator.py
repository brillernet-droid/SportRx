from sportrx.test_session_operator import (
    build_test_day_command_board,
    build_test_session_operator,
    test_day_command_board_markdown,
    test_session_operator_markdown,
)


def test_test_session_operator_builds_standard_sequence():
    operator = build_test_session_operator(["row", "kettlebell", "track"], safety_gate_status="GREEN")

    assert operator["schema"] == "sportrx.test_session_operator"
    assert operator["status"] == "ready_for_test_day"
    assert operator["path"] == "standard"
    assert operator["component_count"] >= 3
    assert operator["recommended_components"] >= 2
    assert operator["steps"][0]["step_id"] == "safety_gate"
    assert any(step["component_id"] == "run_1km" for step in operator["component_steps"])
    assert any("RPE_0_10" in step["required_fields"] for step in operator["component_steps"])


def test_test_session_operator_blocks_red_safety_gate_without_scoring():
    operator = build_test_session_operator(["row"], safety_gate_status="RED")

    assert operator["status"] == "blocked_by_safety_gate"
    assert operator["preflight_steps"][0]["status"] == "blocked"
    assert "does not score performance" in operator["claim_boundary"]


def test_test_session_operator_keeps_low_equipment_path():
    operator = build_test_session_operator([], safety_gate_status="GREEN")

    component_ids = {step["component_id"] for step in operator["component_steps"]}

    assert operator["path"] == "low_equipment"
    assert "run_1km_or_6min" in component_ids
    assert "bodyweight_circuit" in component_ids


def test_test_session_operator_markdown_exports_steps_and_boundaries():
    operator = build_test_session_operator(["ski"], safety_gate_status="GREEN")
    markdown = test_session_operator_markdown(operator)

    assert "# SportRx Test Session Operator" in markdown
    assert "Operator Steps" in markdown
    assert "Benchmark Log handoff" in markdown
    assert "medical clearance" in markdown


def test_test_day_command_board_summarizes_operator_without_scoring():
    operator = build_test_session_operator(["row", "track"], safety_gate_status="GREEN")
    board = build_test_day_command_board(operator)

    assert board["schema"] == "sportrx.test_day_command_board"
    assert board["status"] == "ready_for_operator"
    assert board["path"] == "standard"
    assert len(board["cards"]) == 4
    assert any(card["id"] == "record_now" and card["value"] == "7 fields" for card in board["cards"])
    assert "completion status" in board["required_fields"]
    assert "retest anchor" in board["primary_message"].lower()
    assert "does not score performance" in board["claim_boundary"]


def test_test_day_command_board_preserves_red_safety_block():
    operator = build_test_session_operator(["row"], safety_gate_status="RED")
    board = build_test_day_command_board(operator)
    cards = {card["id"]: card for card in board["cards"]}

    assert board["status"] == "blocked_by_safety_gate"
    assert cards["preflight"]["status"] == "blocked"
    assert cards["component_sequence"]["status"] == "ready"
    assert "screening follow-up" in board["next_action"]


def test_test_day_command_board_markdown_exports_phases_and_fields():
    board = build_test_day_command_board(build_test_session_operator([], safety_gate_status="GREEN"))
    markdown = test_day_command_board_markdown(board)

    assert "# SportRx Test-Day Command Board" in markdown
    assert "Command Cards" in markdown
    assert "Test-Day Phases" in markdown
    assert "Required Fields" in markdown
    assert "medical clearance" in markdown
