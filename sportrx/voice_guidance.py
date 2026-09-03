"""Build bounded Chinese voice scripts from approved SportRX content."""

from __future__ import annotations

from typing import Any


def build_session_voice_script(
    session: dict[str, Any],
    *,
    activity_label: str,
    intensity_label: str,
    talk_test: str,
) -> str:
    """Turn one approved session into a short device-read training guide."""

    duration = int(session.get("duration_min", 0))
    rpe = session.get("rpe_0_10", [])
    rpe_text = f"{rpe[0]} 到 {rpe[1]}" if isinstance(rpe, (list, tuple)) and len(rpe) >= 2 else "处方所示范围"
    return "".join(
        [
            f"今天的训练是{activity_label}，总时长约{duration}分钟，目标强度是{intensity_label}，主观用力程度 R P E {rpe_text}。",
            "开始前，用轻松走或轻松骑行热身五到十分钟。",
            f"训练过程中，保持能够{talk_test.rstrip('。')}的节奏，以完成整段训练为优先。",
            "如果出现胸痛、异常气短、头晕或其他明显不适，请停止训练。",
            "结束后逐渐降低速度，并回到 SportRX 记录完成情况和本次 R P E。",
        ]
    )


def build_exercise_voice_script(exercise: dict[str, Any], *, display_name: str | None = None) -> str:
    """Read the stored Chinese movement steps without inventing new coaching."""

    instruction_steps = exercise.get("instruction_steps", {})
    steps = instruction_steps.get("zh", []) if isinstance(instruction_steps, dict) else []
    if not steps:
        instructions = exercise.get("instructions", {})
        fallback = instructions.get("zh", "") if isinstance(instructions, dict) else ""
        steps = [fallback] if fallback else []
    name = str(display_name or exercise.get("name", "这个动作"))
    spoken_steps = "".join(f"第{index}步，{str(step).strip()}" for index, step in enumerate(steps[:8], start=1))
    return f"下面是{name}的动作指导。{spoken_steps}动作说明来自本地内容库，不替代现场指导或个人安全判断。"
