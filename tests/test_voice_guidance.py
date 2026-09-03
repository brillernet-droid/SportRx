from __future__ import annotations

from sportrx.voice_guidance import build_exercise_voice_script, build_session_voice_script


def test_session_voice_script_uses_prescribed_dose_and_stop_boundary():
    script = build_session_voice_script(
        {"duration_min": 30, "rpe_0_10": [4, 5]},
        activity_label="快走",
        intensity_label="中等",
        talk_test="可以说话，但唱歌会比较困难。",
    )

    assert "快走" in script
    assert "30分钟" in script
    assert "R P E 4 到 5" in script
    assert "停止训练" in script


def test_exercise_voice_script_reads_only_stored_chinese_steps():
    exercise = {
        "name": "walking on incline treadmill",
        "instruction_steps": {"zh": ["调整坡度。", "以舒适速度开始行走。"]},
        "instructions": {"zh": "未使用的备用说明。"},
    }

    script = build_exercise_voice_script(exercise, display_name="跑步机坡度快走")

    assert "跑步机坡度快走" in script
    assert "第1步，调整坡度。" in script
    assert "第2步，以舒适速度开始行走。" in script
    assert "未使用的备用说明" not in script
    assert "不替代现场指导" in script
