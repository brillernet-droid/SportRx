import pytest

from sportrx.guided_workout import build_guided_workout


def _session(duration: int = 30) -> dict:
    return {
        "activity": "brisk walking",
        "duration_min": duration,
        "intensity": "light_to_moderate",
        "rpe_0_10": [3, 5],
    }


def test_guided_workout_preserves_prescribed_duration_and_intensity():
    session = _session(30)

    workout = build_guided_workout(
        session,
        activity_label="快走",
        intensity_label="轻到中等强度",
        talk_test="可以说出完整短句",
    )

    assert workout["duration_seconds"] == 1800
    assert sum(phase["duration_seconds"] for phase in workout["phases"]) == 1800
    assert [phase["duration_seconds"] for phase in workout["phases"]] == [300, 1200, 300]
    assert workout["session_activity"] == session["activity"]
    assert "RPE 3 到 5" in workout["phases"][1]["voice_cue"]


def test_guided_workout_uses_selected_catalogue_content_without_changing_dose():
    exercise = {
        "id": "exercise:test",
        "name": "sample movement",
        "instruction_steps": {"zh": ["保持身体直立。", "采用稳定节奏。"]},
    }

    workout = build_guided_workout(
        _session(20),
        exercise=exercise,
        exercise_label="跑步机快走",
        activity_label="快走",
    )

    main_phase = workout["phases"][1]
    assert workout["exercise_id"] == "exercise:test"
    assert workout["duration_seconds"] == 1200
    assert main_phase["title"] == "跑步机快走"
    assert main_phase["content_source"] == "exercise_catalogue"
    assert main_phase["instruction"] == "保持身体直立。 采用稳定节奏。"


def test_guided_workout_keeps_short_sessions_usable_and_exact():
    workout = build_guided_workout(_session(10), activity_label="快走")

    assert [phase["duration_seconds"] for phase in workout["phases"]] == [120, 360, 120]
    assert sum(phase["duration_seconds"] for phase in workout["phases"]) == 600


def test_guided_workout_rejects_too_short_session():
    with pytest.raises(ValueError, match="at least 3 minutes"):
        build_guided_workout(_session(2))
