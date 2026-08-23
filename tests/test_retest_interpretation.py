from sportrx.benchmark_log import build_component_result, create_benchmark_session
from sportrx.demo_seed import build_demo_state
from sportrx.retest_interpretation import build_retest_interpretation_guard, retest_interpretation_markdown


def test_retest_interpretation_marks_demo_comparable():
    guard = build_retest_interpretation_guard(build_demo_state()["benchmark_sessions"])

    assert guard["schema"] == "sportrx.retest_interpretation_guard"
    assert guard["status"] == "comparable_raw_change"
    assert guard["comparison_count"] >= 3
    assert guard["comparable_count"] == guard["comparison_count"]
    assert guard["context_changed_count"] == 0
    assert all(item["interpretation_status"] == "comparable_raw_change" for item in guard["items"])
    assert "does not prove training effects" in guard["claim_boundary"]


def test_retest_interpretation_waits_for_repeated_component():
    session = create_benchmark_session(
        {"equipment_access": ["row"]},
        [build_component_result("run_1km", value=370, value_unit="seconds", rpe_0_10=7, equipment=["track"])],
        session_date="2026-08-01",
    )

    guard = build_retest_interpretation_guard([session])

    assert guard["status"] == "waiting_for_retest"
    assert guard["comparison_count"] == 0
    assert "Repeat at least one completed benchmark component" in guard["next_action"]


def test_retest_interpretation_flags_context_changed():
    first = create_benchmark_session(
        {"equipment_access": ["row"]},
        [build_component_result("row_or_ski_1km", value=300, value_unit="seconds", rpe_0_10=8, equipment=["row"])],
        session_date="2026-08-01",
    )
    second = create_benchmark_session(
        {"equipment_access": ["ski"]},
        [build_component_result("row_or_ski_1km", value=290, value_unit="seconds", rpe_0_10=8, equipment=["ski"])],
        session_date="2026-08-22",
    )

    guard = build_retest_interpretation_guard([first, second])

    assert guard["status"] == "context_changed"
    assert guard["context_changed_count"] == 1
    assert guard["items"][0]["interpretation_status"] == "context_changed"
    assert "equipment_changed" in guard["items"][0]["context_changes"]


def test_retest_interpretation_markdown_exports_guardrails():
    guard = build_retest_interpretation_guard(build_demo_state()["benchmark_sessions"])
    markdown = retest_interpretation_markdown(guard)

    assert "# SportRx Retest Interpretation Guard" in markdown
    assert "Comparable raw changes" in markdown
    assert "comparable_raw_change" in markdown
