from pathlib import Path

from sportrx.runtime_doctor import build_runtime_doctor, runtime_doctor_markdown


ROOT = Path(__file__).resolve().parents[1]


def test_runtime_doctor_marks_current_repo_ready():
    report = build_runtime_doctor(ROOT, python_version=(3, 11, 0), streamlit_version="1.61.1")

    assert report["schema"] == "sportrx.runtime_doctor"
    assert report["status"] == "ready_to_run_locally"
    assert report["passed_checks"] == report["total_checks"]
    assert "bash scripts/run_local.sh" in report["commands"]
    assert "python3 scripts/smoke_check.py" in report["commands"]
    assert "local app launch readiness" in report["claim_boundary"]


def test_runtime_doctor_flags_old_python():
    report = build_runtime_doctor(ROOT, python_version=(3, 9, 9), streamlit_version="1.61.1")

    assert report["status"] == "needs_review"
    assert any(check["id"] == "runtime_python_version" and not check["passed"] for check in report["checks"])


def test_runtime_doctor_flags_missing_required_files(tmp_path):
    report = build_runtime_doctor(tmp_path, python_version=(3, 11, 0), streamlit_version="1.61.1")

    assert report["status"] == "needs_review"
    assert any(check["id"] == "runtime_required_files" and not check["passed"] for check in report["checks"])


def test_runtime_doctor_markdown_exports_commands():
    report = build_runtime_doctor(ROOT, python_version=(3, 11, 0), streamlit_version="1.61.1")

    markdown = runtime_doctor_markdown(report)

    assert "# SportRx Runtime Doctor" in markdown
    assert "bash scripts/run_local.sh" in markdown
    assert "python3 scripts/smoke_check.py" in markdown
