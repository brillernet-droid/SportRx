"""First-run guidance for the SportRx demo.

The guide helps a new reviewer choose a path through the prototype without
adding prescription logic or scientific claims.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "First Run Guide is product navigation only. It does not validate SportRx, "
    "score performance, predict outcomes, or provide medical clearance."
)


def _count_measured(passport: dict[str, Any]) -> int:
    return int(passport.get("measured_performance_areas", {}).get("count", 0) or 0)


def build_first_run_guide(
    passport: dict[str, Any],
    benchmark_sessions: list[dict[str, Any]],
    feedback_by_week: dict[int | str, dict[str, Any]],
    pilot_feedback_entries: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build launch-style guidance for first-time local reviewers."""

    measured_count = _count_measured(passport)
    benchmark_count = len(benchmark_sessions)
    feedback_count = len(feedback_by_week)
    pilot_feedback_entries = pilot_feedback_entries or []
    starter_available = bool(passport.get("starter_path", {}).get("available"))

    if measured_count < 2:
        recommended_path = "measure_first"
        next_page = "Benchmark Protocol"
        next_action = "先按 SportRx Hybrid Benchmark v1 完成至少两个组件。"
    elif not starter_available:
        recommended_path = "training_profile"
        next_page = "Training Profile"
        next_action = "查看哪些输出仍被 gate 阻断。"
    elif feedback_count == 0:
        recommended_path = "starter_path"
        next_page = "训练"
        next_action = "查看 4 周 Training Block，并在完成后记录 Week 1 RPE。"
    elif benchmark_count < 2:
        recommended_path = "retest"
        next_page = "Benchmark Log"
        next_action = "用同一 protocol 再测一次可比较组件。"
    else:
        recommended_path = "review_export"
        next_page = "Export Center"
        next_action = "导出报告、benchmark logs、snapshot 和 QA 材料。"

    paths = [
        {
            "id": "complete_demo",
            "label": "直接看完整示例",
            "best_for": "第一次评审、录屏、向朋友解释产品闭环",
            "start_page": "Workbench",
            "primary_action": "点击 Workbench 首屏的“加载完整示例”",
            "button_label": "加载完整示例",
            "action_type": "load_demo",
            "expected_time_min": 3,
            "outcome": "看到测量、Training Profile、训练、复测、导出和 QA 的完整样子。",
            "success_check": "页面出现完整 demo 数据、Benchmark logs、训练反馈和复测状态。",
        },
        {
            "id": "quick_self_intake",
            "label": "先填自己的训练行为",
            "best_for": "只想先体验，不想立刻做完整 benchmark",
            "start_page": "Quick Match",
            "primary_action": "填写过去 4 周训练天数、分钟数、跑走、力量和高强度次数",
            "button_label": "进入 Quick Match",
            "action_type": "navigate",
            "expected_time_min": 5,
            "outcome": "得到一份明确标注为 self-reported intake 的粗筛结果。",
            "success_check": "Intake Precision Audit 显示 direct numeric 字段，不把它当作 measured performance。",
        },
        {
            "id": "measure_first",
            "label": "用自己的测试数据",
            "best_for": "自己试用或给 alpha 用户试用",
            "start_page": "Benchmark Protocol",
            "primary_action": "先选器械路径，再完成至少两个 Benchmark 组件",
            "button_label": "开始 Benchmark",
            "action_type": "navigate",
            "expected_time_min": 15,
            "outcome": "得到一个不靠猜测补齐的 current measured picture。",
            "success_check": "至少两个 Benchmark 组件被记录，缺失项目仍显示 Not tested。",
        },
        {
            "id": "review_export",
            "label": "发布审阅 / 交给别人看",
            "best_for": "GitHub README、外部 reviewer、教练或同伴复盘",
            "start_page": "Export Center",
            "primary_action": "下载 Export Bundle 和 Session Snapshot",
            "button_label": "打开 Export Center",
            "action_type": "navigate",
            "expected_time_min": 5,
            "outcome": "拿到可复盘、可恢复、claim boundary 清楚的本地文件。",
            "success_check": "Export Bundle、Session Snapshot、Review Pack ZIP 和 Release QA 都可下载或查看。",
        },
    ]

    return {
        "schema": "sportrx.first_run_guide",
        "schema_version": "0.1",
        "status": "ready_for_guided_trial",
        "recommended_path": recommended_path,
        "next_page": next_page,
        "next_action": next_action,
        "state_summary": {
            "measured_performance_areas": measured_count,
            "benchmark_sessions": benchmark_count,
            "feedback_weeks": feedback_count,
            "pilot_feedback_entries": len(pilot_feedback_entries),
            "starter_path_available": starter_available,
        },
        "paths": paths,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def first_run_guide_markdown(guide: dict[str, Any]) -> str:
    """Export the first-run guide as Markdown."""

    summary = guide.get("state_summary", {})
    lines = [
        "# SportRx First Run Guide",
        "",
        f"- Recommended path: {guide.get('recommended_path')}",
        f"- Next page: {guide.get('next_page')}",
        f"- Next action: {guide.get('next_action')}",
        f"- Claim boundary: {guide.get('claim_boundary', CLAIM_BOUNDARY)}",
        "",
        "## Current State",
        f"- Measured performance areas: {summary.get('measured_performance_areas', 0)}",
        f"- Benchmark sessions: {summary.get('benchmark_sessions', 0)}",
        f"- Feedback weeks: {summary.get('feedback_weeks', 0)}",
        f"- Pilot feedback entries: {summary.get('pilot_feedback_entries', 0)}",
        f"- Starter path available: {summary.get('starter_path_available', False)}",
        "",
        "## Paths",
    ]
    for path in guide.get("paths", []):
        lines.extend(
            [
                f"### {path['label']}",
                f"- Best for: {path['best_for']}",
                f"- Start page: {path['start_page']}",
                f"- Primary action: {path['primary_action']}",
                f"- Success check: {path['success_check']}",
                f"- Expected time: {path['expected_time_min']} min",
                f"- Outcome: {path['outcome']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
