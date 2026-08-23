"""Product walkthrough helpers for the SportRx demo app."""

from __future__ import annotations

from typing import Any


def _status(done: bool, waiting_reason: str = "") -> str:
    return "complete" if done else waiting_reason or "not_started"


def build_walkthrough(passport: dict[str, Any], benchmark_summary: dict[str, Any], feedback_dashboard: dict[str, Any]) -> dict[str, Any]:
    """Build a guided review path for the current app state."""

    has_measurements = int(passport.get("measured_performance_areas", {}).get("count", 0)) >= 2
    has_benchmarks = int(benchmark_summary.get("session_count", 0)) > 0
    has_retest = bool(benchmark_summary.get("retest_ready"))
    has_training_block = bool(passport.get("starter_path", {}).get("available"))
    has_feedback = int(feedback_dashboard.get("adherence", {}).get("weeks_recorded", 0)) > 0
    steps = [
        {
            "step": 1,
            "page": "Quick Match",
            "title": "训练行为粗筛",
            "status": "complete",
            "why": "先用过去 4 周训练行为建立起点。",
        },
        {
            "step": 2,
            "page": "HYROX Check",
            "title": "填写或导入实测表现",
            "status": _status(has_measurements, "needs_measurement"),
            "why": "至少两个实测表现维度后，才比较 strongest area 和 main gap。",
        },
        {
            "step": 3,
            "page": "Benchmark Protocol",
            "title": "确认测试 protocol",
            "status": "complete" if has_benchmarks else "recommended",
            "why": "复测前需要固定路径、器械、顺序和记录口径。",
        },
        {
            "step": 4,
            "page": "Benchmark Log",
            "title": "保存原始 Benchmark Log",
            "status": _status(has_benchmarks, "no_log_yet"),
            "why": "记录原始结果、RPE、器械、替代动作和 notes。",
        },
        {
            "step": 5,
            "page": "Training Profile",
            "title": "查看 Training Profile Report",
            "status": _status(has_measurements, "limited_report"),
            "why": "报告总结已知、未知、下一步测试和训练交接边界。",
        },
        {
            "step": 6,
            "page": "训练",
            "title": "生成 4 周 Training Block",
            "status": _status(has_training_block, "blocked_by_measurement_gate"),
            "why": "只有测量足够时，才生成针对性起步训练。",
        },
        {
            "step": 7,
            "page": "复测",
            "title": "查看 Feedback Loop",
            "status": _status(has_feedback or has_retest, "awaiting_feedback_or_retest"),
            "why": "用完成率、RPE 和原始复测变化观察下一步调整。",
        },
        {
            "step": 8,
            "page": "Export Center",
            "title": "下载本地导出材料",
            "status": _status(has_benchmarks or has_feedback or has_training_block, "nothing_to_export_yet"),
            "why": "把 protocol、logs、report、training block 和 feedback dashboard 作为本地文件导出。",
        },
        {
            "step": 9,
            "page": "Release QA",
            "title": "查看发布前自检",
            "status": _status(has_benchmarks and has_training_block and (has_feedback or has_retest), "qa_needs_demo_loop"),
            "why": "检查 demo loop、导出物、claim boundary 和证据文件状态。",
        },
    ]
    next_step = next((step for step in steps if step["status"] not in {"complete", "recommended"}), steps[-1])
    return {
        "schema": "sportrx.walkthrough",
        "schema_version": "0.1",
        "steps": steps,
        "next_step": next_step,
        "completion": {
            "complete_steps": sum(1 for step in steps if step["status"] == "complete"),
            "total_steps": len(steps),
        },
    }
