"""Build a guided execution timeline without changing prescription dose."""

from __future__ import annotations

from typing import Any


ACTIVITY_LABELS = {
    "brisk walking": "快走",
    "easy jogging": "轻松慢跑",
    "cycling": "骑行",
    "elliptical": "椭圆机",
}


def _phase_minutes(total_minutes: int) -> tuple[int, int, int]:
    """Split a session while preserving the prescribed total duration."""

    if total_minutes < 3:
        raise ValueError("A guided workout requires at least 3 minutes.")
    if total_minutes >= 25:
        warmup = cooldown = 5
    elif total_minutes >= 15:
        warmup = cooldown = 3
    else:
        warmup = cooldown = max(1, total_minutes // 5)
    return warmup, total_minutes - warmup - cooldown, cooldown


def _exercise_cue(exercise: dict[str, Any] | None) -> str:
    if not exercise:
        return "保持动作自然稳定，不必追求速度。"
    steps = exercise.get("instruction_steps", {})
    chinese_steps = steps.get("zh", []) if isinstance(steps, dict) else []
    if chinese_steps:
        return " ".join(str(step).strip() for step in chinese_steps[:2] if str(step).strip())
    instructions = exercise.get("instructions", {})
    return str(instructions.get("zh", "")).strip() if isinstance(instructions, dict) else ""


def build_guided_workout(
    session: dict[str, Any],
    *,
    exercise: dict[str, Any] | None = None,
    exercise_label: str | None = None,
    activity_label: str | None = None,
    intensity_label: str | None = None,
    talk_test: str | None = None,
) -> dict[str, Any]:
    """Create a three-phase runner from an already approved session.

    Exercise-catalogue content supplies movement wording only. It never changes
    the prescribed activity, duration, intensity, or progression.
    """

    total_minutes = int(session.get("duration_min", 0) or 0)
    warmup_minutes, main_minutes, cooldown_minutes = _phase_minutes(total_minutes)
    activity = str(session.get("activity", "brisk walking"))
    activity_name = activity_label or ACTIVITY_LABELS.get(activity, activity)
    main_title = exercise_label or activity_name
    intensity_name = intensity_label or str(session.get("intensity", "处方强度"))
    talk_test_text = (talk_test or "保持能够说出完整短句的节奏").rstrip("。")
    rpe = session.get("rpe_0_10", [])
    if isinstance(rpe, (list, tuple)) and len(rpe) >= 2:
        rpe_text = f"RPE {rpe[0]} 到 {rpe[1]}"
    else:
        rpe_text = "保持处方所示 RPE"

    phases = [
        {
            "id": "warmup",
            "label": "热身",
            "title": f"轻松{activity_name}",
            "duration_seconds": warmup_minutes * 60,
            "instruction": "从轻松节奏开始，让呼吸和动作逐渐进入状态。",
            "voice_cue": f"开始热身。用轻松的{activity_name}逐渐进入状态。",
            "content_source": "prescription_protocol",
        },
        {
            "id": "main",
            "label": "主训练",
            "title": main_title,
            "duration_seconds": main_minutes * 60,
            "instruction": _exercise_cue(exercise),
            "voice_cue": (
                f"进入主训练，{main_title}。目标强度是{intensity_name}，{rpe_text}，"
                f"{talk_test_text}。"
            ),
            "content_source": "exercise_catalogue" if exercise else "prescription_protocol",
        },
        {
            "id": "cooldown",
            "label": "放松",
            "title": f"放慢{activity_name}",
            "duration_seconds": cooldown_minutes * 60,
            "instruction": "逐渐降低速度，让呼吸平稳下来，不要突然停止。",
            "voice_cue": f"进入放松。逐渐放慢{activity_name}，让呼吸平稳下来。",
            "content_source": "prescription_protocol",
        },
    ]

    return {
        "schema": "sportrx.guided_workout.v1",
        "session_activity": activity,
        "duration_minutes": total_minutes,
        "duration_seconds": total_minutes * 60,
        "phase_count": len(phases),
        "phases": phases,
        "exercise_id": exercise.get("id") if exercise else None,
        "dose_boundary": "Guidance preserves the approved session duration and intensity.",
    }
