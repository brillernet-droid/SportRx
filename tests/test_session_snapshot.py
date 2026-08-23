import json

import pytest

from sportrx.demo_seed import build_demo_state
from sportrx.pilot_feedback import create_pilot_feedback_entry
from sportrx.session_snapshot import (
    build_session_snapshot,
    restore_session_snapshot,
    session_snapshot_json,
    session_snapshot_markdown,
)


def test_session_snapshot_packages_local_state():
    state = build_demo_state()
    entry = create_pilot_feedback_entry(
        reviewer_role="coach",
        ratings={
            "setup_clarity": 4,
            "measurement_realism": 5,
            "trust": 4,
            "actionability": 4,
            "visual_polish": 3,
        },
        comments={"first_impression": "Measurement-first."},
    )

    snapshot = build_session_snapshot(
        state["profile"],
        state["benchmark_sessions"],
        state["feedback_by_week"],
        [entry],
        snapshot_date="2026-08-22",
    )

    assert snapshot["schema"] == "sportrx.session_snapshot"
    assert snapshot["snapshot_date"] == "2026-08-22"
    assert snapshot["counts"]["benchmark_sessions"] == 2
    assert snapshot["counts"]["feedback_weeks"] == 2
    assert snapshot["counts"]["pilot_feedback_entries"] == 1
    assert set(snapshot["app_state"]["feedback_by_week"]) == {"1", "2"}
    assert "not validation data" in " ".join(snapshot["restore_notes"])


def test_session_snapshot_json_roundtrip_restores_week_keys():
    state = build_demo_state()
    snapshot = build_session_snapshot(
        state["profile"],
        state["benchmark_sessions"],
        state["feedback_by_week"],
        snapshot_date="2026-08-22",
    )

    restored = restore_session_snapshot(json.loads(session_snapshot_json(snapshot)))

    assert restored["profile"]["age"] == state["profile"]["age"]
    assert len(restored["benchmark_sessions"]) == 2
    assert set(restored["feedback_by_week"]) == {1, 2}
    assert restored["pilot_feedback_entries"] == []


def test_session_snapshot_rejects_wrong_schema():
    with pytest.raises(ValueError, match="SportRx session snapshot"):
        restore_session_snapshot({"schema": "other"})


def test_session_snapshot_markdown_summarizes_counts():
    state = build_demo_state()
    snapshot = build_session_snapshot(
        state["profile"],
        state["benchmark_sessions"],
        state["feedback_by_week"],
        snapshot_date="2026-08-22",
    )

    markdown = session_snapshot_markdown(snapshot)

    assert "# SportRx Session Snapshot" in markdown
    assert "Benchmark sessions: 2" in markdown
    assert "Feedback weeks: 2" in markdown
