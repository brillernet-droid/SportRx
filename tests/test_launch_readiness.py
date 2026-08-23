from pathlib import Path

from sportrx.demo_seed import build_demo_state
from sportrx.launch_readiness import build_launch_readiness, launch_readiness_markdown
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.release_qa import REQUIRED_EVIDENCE_FILES


ROOT = Path(__file__).resolve().parents[1]


def test_launch_readiness_marks_complete_demo_ready():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    evidence = {path: True for path in REQUIRED_EVIDENCE_FILES}

    report = build_launch_readiness(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        evidence,
        root=str(ROOT),
    )

    assert report["schema"] == "sportrx.launch_readiness"
    assert report["status"] == "ready_for_public_demo"
    assert report["passed_checks"] == report["total_checks"]
    assert report["package_status"] == "ready_for_public_package"
    assert len(report["review_path"]) >= 9
    assert any(item["filename"] == "sportrx_launch_readiness.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_public_beta_readiness.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_runtime_doctor.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_reviewer_handoff.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_release_candidate_summary.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_terminology_guide.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_demo_experience_console.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_guided_review_console.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_input_ledger.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_quick_match_lab_intake_sheet.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_demo_runbook.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_first_run_guide.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_measurement_timeline.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_benchmark_worksheet.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_lab_readiness_console.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_measurement_intake_matrix.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_measurement_intake_matrix.csv" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_protocol_source_guide.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_intake_precision_audit.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_page_health_matrix.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_alpha_dataset_dictionary.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_alpha_weekly_feedback_template.csv" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_test_day_brief.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_test_day_command_board.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_test_session_operator.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_pilot_feedback_prompt.md" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_session_snapshot.json" for item in report["export_files"])
    assert any(item["filename"] == "sportrx_session_snapshot.md" for item in report["export_files"])


def test_launch_readiness_flags_incomplete_default_state():
    profile = {
        "age": 35,
        "training_days": 3,
        "weekly_training_minutes": 120,
        "available_days_per_week": 3,
        "max_minutes_per_session": 45,
        "symptoms": [],
        "known_conditions": [],
    }
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile)

    report = build_launch_readiness(profile, passport, plan, [], {}, {}, root=str(ROOT))

    assert report["status"] == "needs_review"
    assert any(item["status"] == "needs_review" for item in report["checks"])


def test_launch_readiness_markdown_exports_review_path():
    state = build_demo_state()
    passport = build_readiness_passport(state["profile"])
    plan = generate_prescription(state["profile"], feedback_by_week=state["feedback_by_week"])
    evidence = {path: True for path in REQUIRED_EVIDENCE_FILES}
    report = build_launch_readiness(
        state["profile"],
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        evidence,
        root=str(ROOT),
    )

    markdown = launch_readiness_markdown(report)

    assert "# SportRx Launch Readiness" in markdown
    assert "Review Path" in markdown
    assert "Export Files" in markdown
