from sportrx.demo_seed import build_demo_state
from sportrx.first_run_guide import build_first_run_guide, first_run_guide_markdown
from sportrx.passport import build_readiness_passport


def test_first_run_guide_routes_incomplete_state_to_measurement():
    passport = build_readiness_passport(
        {"age": 35, "training_days": 2, "weekly_training_minutes": 80, "symptoms": [], "known_conditions": []}
    )

    guide = build_first_run_guide(passport, [], {})

    assert guide["schema"] == "sportrx.first_run_guide"
    assert guide["recommended_path"] == "measure_first"
    assert guide["next_page"] == "Benchmark Protocol"
    assert any(path["id"] == "quick_self_intake" for path in guide["paths"])
    assert all("success_check" in path for path in guide["paths"])
    assert next(path for path in guide["paths"] if path["id"] == "complete_demo")["primary_action"].startswith("点击 Workbench 首屏")
    assert guide["state_summary"]["measured_performance_areas"] < 2
    assert "product navigation only" in guide["claim_boundary"]


def test_first_run_guide_routes_complete_demo_to_export():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])

    guide = build_first_run_guide(passport, state["benchmark_sessions"], state["feedback_by_week"])

    assert guide["recommended_path"] == "review_export"
    assert guide["next_page"] == "Export Center"
    assert guide["state_summary"]["benchmark_sessions"] == 2
    assert guide["state_summary"]["feedback_weeks"] == 2


def test_first_run_guide_markdown_exports_paths():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    guide = build_first_run_guide(passport, state["benchmark_sessions"], state["feedback_by_week"])

    markdown = first_run_guide_markdown(guide)

    assert "# SportRx First Run Guide" in markdown
    assert "直接看完整示例" in markdown
    assert "先填自己的训练行为" in markdown
    assert "用自己的测试数据" in markdown
    assert "发布审阅 / 交给别人看" in markdown
    assert "Success check" in markdown
