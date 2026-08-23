"""Demo seed data for the SportRx Streamlit prototype.

The seed creates a plausible local demo state so reviewers can experience the
full measurement loop without typing every field manually. It is sample data,
not athlete norms or validation data.
"""

from __future__ import annotations

from typing import Any

from .benchmark_log import build_component_result, create_benchmark_session


def build_demo_profile() -> dict[str, Any]:
    """Return a complete demo profile with measured HYROX Check fields."""

    return {
        "age": 32,
        "sex": "female",
        "height_cm": 168,
        "weight_kg": 64,
        "training_days": 4,
        "weekly_training_minutes": 190,
        "exercise_days_last_4w": 4,
        "mvpa_minutes_per_week": 190,
        "available_days_per_week": 4,
        "max_minutes_per_session": 55,
        "running_minutes_per_week": 95,
        "longest_continuous_run_minutes": 35,
        "strength_days_per_week": 2,
        "high_intensity_sessions_last_4w": 3,
        "loaded_movement_sessions_last_4w": 4,
        "preferred_activity": "running",
        "primary_goal": "first finish",
        "goal": "Improve aerobic fitness / general health",
        "one_km_run_seconds": 318,
        "station_test_score": 68,
        "station_test_protocol": "SportRx Hybrid Benchmark v1 0.1 / standard / Benchmark Log 2026-08-22",
        "one_km_row_seconds": 284,
        "equipment_access": ["row", "kettlebell", "dumbbell", "track"],
        "symptoms": [],
        "known_conditions": [],
    }


def build_demo_benchmark_sessions(profile: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Return two local benchmark sessions for retest comparison."""

    profile = profile or build_demo_profile()
    first = create_benchmark_session(
        profile,
        [
            build_component_result("run_1km", value=330, value_unit="seconds", rpe_0_10=7, equipment=["track"]),
            build_component_result(
                "station_circuit",
                value=62,
                value_unit="score",
                rpe_0_10=7,
                equipment=["kettlebell", "dumbbell"],
                notes="Controlled circuit score for demo import.",
            ),
            build_component_result("row_or_ski_1km", value=292, value_unit="seconds", rpe_0_10=8, equipment=["row"]),
        ],
        session_date="2026-08-01",
        global_notes="Demo baseline benchmark. Same route and station setup planned for retest.",
    )
    second = create_benchmark_session(
        profile,
        [
            build_component_result("run_1km", value=318, value_unit="seconds", rpe_0_10=7, equipment=["track"]),
            build_component_result(
                "station_circuit",
                value=68,
                value_unit="score",
                rpe_0_10=7,
                equipment=["kettlebell", "dumbbell"],
                notes="Same circuit, same loads.",
            ),
            build_component_result("row_or_ski_1km", value=284, value_unit="seconds", rpe_0_10=8, equipment=["row"]),
        ],
        session_date="2026-08-22",
        global_notes="Demo retest benchmark. Shows raw component comparison only.",
    )
    return [first, second]


def build_demo_feedback_by_week() -> dict[int, dict[str, Any]]:
    """Return a small weekly feedback record for demo progression."""

    return {
        1: {
            "completed_sessions": 4,
            "average_rpe": 5.0,
            "felt_too_hard": False,
            "adverse_event": False,
        },
        2: {
            "completed_sessions": 3,
            "average_rpe": 6.0,
            "felt_too_hard": False,
            "adverse_event": False,
        },
    }


def build_demo_state() -> dict[str, Any]:
    """Return all state pieces needed to hydrate the demo app."""

    profile = build_demo_profile()
    return {
        "profile": profile,
        "benchmark_sessions": build_demo_benchmark_sessions(profile),
        "feedback_by_week": build_demo_feedback_by_week(),
        "claim_boundary": "Demo data is synthetic sample input for product review. It is not validation data or athlete norms.",
    }
