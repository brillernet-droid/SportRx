"""Synthetic demo scenarios for SportRx product review.

Scenarios let reviewers inspect the app at different workflow states. They are
not validation data, athlete norms, or benchmark percentiles.
"""

from __future__ import annotations

from typing import Any

from .benchmark_log import build_component_result, create_benchmark_session
from .demo_seed import build_demo_profile, build_demo_state


CLAIM_BOUNDARY = (
    "Demo scenarios are synthetic product-review states. They are not "
    "validation data, athlete norms, benchmark percentiles, or evidence that "
    "SportRx improves outcomes."
)


SCENARIO_LIBRARY = [
    {
        "id": "measure_first",
        "label": "Measure First",
        "stage": "New user / no measured tests",
        "best_for": "体验 SportRx 如何诚实地显示 Not tested 和 gate 输出。",
        "expected_state": "Starter Path blocked until measured data exists.",
    },
    {
        "id": "benchmark_underway",
        "label": "Benchmark Underway",
        "stage": "Partial benchmark log",
        "best_for": "查看只有一次 benchmark 记录时，系统如何提示复测和缺失数据。",
        "expected_state": "Training Profile partially available, retest still waiting.",
    },
    {
        "id": "complete_loop",
        "label": "Complete Loop",
        "stage": "Full synthetic review loop",
        "best_for": "演示完整闭环：测试、训练、反馈、复测、导出和 QA。",
        "expected_state": "Release demo review can be inspected end to end.",
    },
]


def build_demo_scenarios() -> list[dict[str, Any]]:
    """Return public metadata for available demo scenarios."""

    return [{**item, "claim_boundary": CLAIM_BOUNDARY} for item in SCENARIO_LIBRARY]


def _measure_first_state() -> dict[str, Any]:
    profile = {
        "age": 34,
        "sex": "female",
        "height_cm": 166,
        "weight_kg": 66,
        "training_days": 2,
        "weekly_training_minutes": 75,
        "exercise_days_last_4w": 2,
        "mvpa_minutes_per_week": 75,
        "available_days_per_week": 3,
        "max_minutes_per_session": 40,
        "running_minutes_per_week": 25,
        "longest_continuous_run_minutes": 12,
        "strength_days_per_week": 1,
        "high_intensity_sessions_last_4w": 0,
        "loaded_movement_sessions_last_4w": 1,
        "preferred_activity": "brisk walking",
        "primary_goal": "understand profile",
        "goal": "Improve aerobic fitness / general health",
        "equipment_access": [],
        "symptoms": [],
        "known_conditions": [],
    }
    return {
        "profile": profile,
        "benchmark_sessions": [],
        "feedback_by_week": {},
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _benchmark_underway_state() -> dict[str, Any]:
    profile = build_demo_profile()
    profile = {
        **profile,
        "one_km_run_seconds": None,
        "station_test_score": None,
        "one_km_row_seconds": None,
    }
    session = create_benchmark_session(
        profile,
        [
            build_component_result("run_1km", value=340, value_unit="seconds", rpe_0_10=7, equipment=["track"]),
            build_component_result(
                "station_circuit",
                completed=False,
                value=None,
                value_unit="score",
                equipment=["kettlebell", "dumbbell"],
                notes="Planned but not completed in this partial scenario.",
            ),
        ],
        session_date="2026-08-15",
        global_notes="Synthetic partial benchmark scenario. Retest and full interpretation are intentionally incomplete.",
    )
    return {
        "profile": profile,
        "benchmark_sessions": [session],
        "feedback_by_week": {},
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_demo_scenario_state(scenario_id: str) -> dict[str, Any]:
    """Return a complete app state for a named synthetic demo scenario."""

    if scenario_id == "measure_first":
        return _measure_first_state()
    if scenario_id == "benchmark_underway":
        return _benchmark_underway_state()
    if scenario_id == "complete_loop":
        state = build_demo_state()
        return {**state, "claim_boundary": CLAIM_BOUNDARY}
    raise ValueError(f"Unknown demo scenario: {scenario_id}")
