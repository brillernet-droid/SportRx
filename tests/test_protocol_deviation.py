from sportrx.benchmark_log import build_component_result, create_benchmark_session
from sportrx.demo_seed import build_demo_state
from sportrx.protocol_deviation import build_protocol_deviation_review, protocol_deviation_markdown


def test_protocol_deviation_marks_demo_as_repeatable_record():
    state = build_demo_state()

    review = build_protocol_deviation_review(state["benchmark_sessions"])

    assert review["schema"] == "sportrx.protocol_deviation_review"
    assert review["status"] == "repeatable_protocol_record"
    assert review["session_count"] == 2
    assert review["completed_component_count"] >= 6
    assert review["context_changed_count"] == 0
    assert all(item["status"] == "comparable_retest" for item in review["retest_reviews"])
    assert "does not score performance" in review["claim_boundary"]


def test_protocol_deviation_flags_missing_rpe_and_substitution_context():
    session = create_benchmark_session(
        {"equipment_access": []},
        [
            build_component_result("run_1km_or_6min", value=1000, value_unit="meters"),
            build_component_result(
                "bodyweight_circuit",
                value=4,
                value_unit="rounds",
                rpe_0_10=7,
                substitution="step-ups instead of lunges",
            ),
        ],
        session_date="2026-08-22",
    )

    review = build_protocol_deviation_review([session])

    assert review["status"] == "reviewable_with_context"
    assert review["flag_counts"]["missing_rpe"] == 1
    assert review["flag_counts"]["missing_equipment"] == 2
    assert review["flag_counts"]["substitution_recorded"] == 1


def test_protocol_deviation_flags_retest_context_changes():
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

    review = build_protocol_deviation_review([first, second])

    assert review["status"] == "retest_context_changed"
    assert review["context_changed_count"] == 1
    retest = review["retest_reviews"][0]
    assert retest["status"] == "context_changed"
    assert "equipment_changed" in retest["changes"]


def test_protocol_deviation_markdown_exports_component_and_retest_context():
    review = build_protocol_deviation_review(build_demo_state()["benchmark_sessions"])
    markdown = protocol_deviation_markdown(review)

    assert "# SportRx Protocol Deviation Review" in markdown
    assert "Retest Comparability" in markdown
    assert "comparable_retest" in markdown
    assert "Protocol Deviation Review" in markdown
