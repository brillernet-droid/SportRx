"""4-week starter paths based on the main area to improve."""

from __future__ import annotations

from typing import Any


def build_starter_path(lab_result: dict[str, Any]) -> dict[str, Any]:
    """Return a conservative 4-week starter path for the lab result."""

    if lab_result["safety_gate"]["status"] == "RED":
        return {
            "available": False,
            "reason": "RED safety gate blocks automated training generation.",
            "weeks": [],
        }

    measured_count = int(lab_result.get("measured_performance_areas", {}).get("count", 0))
    if measured_count < 2 or lab_result.get("main_gap") == "Not enough measured data":
        return {
            "available": False,
            "reason": "Complete the SportRx Hybrid Benchmark before building a tailored starter path.",
            "weeks": [],
            "next_action": "Complete the SportRx Hybrid Benchmark v1.",
        }

    limiter = lab_result["main_gap"]
    templates = {
        "Running": [
            "Build repeatable aerobic volume",
            "Add one short controlled running benchmark session",
            "Extend the longest easy session",
            "Retest 1 km or 5 km at controlled effort",
        ],
        "Aerobic fitness": [
            "Build repeatable aerobic volume",
            "Protect easy intensity and weekly consistency",
            "Add 5-10 minutes to one aerobic session",
            "Retest an easy aerobic session or 1 km benchmark",
        ],
        "Strength endurance": [
            "Learn the station circuit movements",
            "Complete 3 controlled strength-endurance rounds",
            "Add one round or slightly reduce rest",
            "Retest the same station circuit",
        ],
        "Station experience": [
            "Practice low-skill station substitutes",
            "Add row, ski, carry, or low-equipment alternatives",
            "Link easy running with station practice",
            "Retest a station-specific circuit",
        ],
        "Work capacity": [
            "Use short mixed sessions without racing them",
            "Add controlled run-to-station transitions",
            "Repeat the same mixed session with steadier pacing",
            "Retest a compromised run or mixed circuit",
        ],
        "No single dominant gap identified": [
            "Keep a balanced week",
            "Add one benchmark you have not tested yet",
            "Repeat the same training rhythm",
            "Retest the weakest measured area",
        ],
    }
    focus_key = next((key for key in templates if key in limiter), "No single dominant gap identified")
    focus = templates[focus_key]
    return {
        "available": True,
        "event_pack": lab_result["event_pack"],
        "based_on_gap": limiter,
        "weeks": [
            {
                "week": index + 1,
                "focus": item,
                "instruction": _week_instruction(index, focus_key),
            }
            for index, item in enumerate(focus)
        ],
    }


def _week_instruction(index: int, focus_key: str) -> str:
    examples = {
        "Running": [
            "Tuesday: 30 min easy run, RPE 3-4.",
            "Thursday: 25 min easy run plus 4 relaxed strides.",
            "Saturday: 40 min easy run/walk.",
            "Retest 1 km or 5 km without sprinting the start.",
        ],
        "Strength endurance": [
            "Tuesday: 30 min easy aerobic work.",
            "Thursday: 3 rounds of controlled squats, carries, lunges, and push work.",
            "Saturday: easy run plus short circuit practice.",
            "Repeat the same circuit and note RPE.",
        ],
        "Station experience": [
            "Tuesday: 30 min easy run.",
            "Thursday: station practice with available equipment or bodyweight substitutes.",
            "Saturday: easy run plus 2-3 station blocks.",
            "Retest the same station setup.",
        ],
        "Work capacity": [
            "Tuesday: easy aerobic session.",
            "Thursday: short run-to-station transitions at RPE 5-6.",
            "Saturday: repeatable mixed session, not a race effort.",
            "Retest one mixed session and compare pacing.",
        ],
    }
    fallback = [
        "Keep the session repeatable.",
        "Do not add intensity and volume at the same time.",
        "Use RPE to keep the work controlled.",
        "Retest one area with the same setup.",
    ]
    return examples.get(focus_key, fallback)[index]
