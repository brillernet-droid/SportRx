"""Runtime readiness checks for the local SportRx prototype."""

from __future__ import annotations

from importlib import metadata
from pathlib import Path
import sys
from typing import Any


CLAIM_BOUNDARY = (
    "Runtime Doctor checks local app launch readiness only. It does not "
    "validate SportRx rules, certify safety, prove outcomes, or provide medical "
    "clearance."
)


REQUIRED_RUNTIME_PATHS = [
    "app/streamlit_app.py",
    "README.md",
    "pyproject.toml",
    "scripts/run_local.sh",
    "scripts/smoke_check.py",
    "sportrx/__init__.py",
    "sportrx/release_qa.py",
    "evidence/claim_policy.md",
    "tests/test_streamlit_app_import.py",
]


def _check(check_id: str, label: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "id": check_id,
        "label": label,
        "status": "pass" if passed else "needs_review",
        "passed": bool(passed),
        "detail": detail,
    }


def _streamlit_version() -> str | None:
    try:
        return metadata.version("streamlit")
    except metadata.PackageNotFoundError:
        return None


def build_runtime_doctor(
    root: str | Path = ".",
    *,
    python_version: tuple[int, int, int] | None = None,
    streamlit_version: str | None = None,
) -> dict[str, Any]:
    """Build a local runtime readiness report."""

    root_path = Path(root).resolve()
    python_version = python_version or sys.version_info[:3]
    streamlit_version = streamlit_version if streamlit_version is not None else _streamlit_version()
    missing_paths = [path for path in REQUIRED_RUNTIME_PATHS if not (root_path / path).exists()]

    checks = [
        _check(
            "runtime_python_version",
            "Python version is supported",
            python_version >= (3, 10, 0),
            f"Python {'.'.join(str(part) for part in python_version)} detected; SportRx requires >= 3.10.",
        ),
        _check(
            "runtime_streamlit_available",
            "Streamlit is installed",
            bool(streamlit_version),
            f"Streamlit {streamlit_version} detected." if streamlit_version else "Streamlit is not installed.",
        ),
        _check(
            "runtime_required_files",
            "Required runtime files are present",
            not missing_paths,
            "All required runtime files present." if not missing_paths else "Missing: " + ", ".join(missing_paths),
        ),
    ]
    passed = sum(1 for item in checks if item["passed"])
    return {
        "schema": "sportrx.runtime_doctor",
        "schema_version": "0.1",
        "status": "ready_to_run_locally" if passed == len(checks) else "needs_review",
        "root": str(root_path),
        "python_version": ".".join(str(part) for part in python_version),
        "streamlit_version": streamlit_version,
        "passed_checks": passed,
        "total_checks": len(checks),
        "checks": checks,
        "commands": [
            'python3 -m pip install -e ".[dev,app]"',
            "python3 scripts/smoke_check.py",
            "PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider",
            "bash scripts/run_local.sh",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def runtime_doctor_markdown(report: dict[str, Any]) -> str:
    """Export Runtime Doctor as Markdown."""

    lines = [
        "# SportRx Runtime Doctor",
        "",
        f"- Status: {report['status']}",
        f"- Python: {report['python_version']}",
        f"- Streamlit: {report.get('streamlit_version') or 'not installed'}",
        f"- Passed: {report['passed_checks']} / {report['total_checks']}",
        f"- Claim boundary: {report['claim_boundary']}",
        "",
        "## Checks",
    ]
    for check in report["checks"]:
        lines.append(f"- [{check['status']}] {check['label']}: {check['detail']}")

    lines.extend(["", "## Commands"])
    for command in report["commands"]:
        lines.append(f"- `{command}`")
    return "\n".join(lines) + "\n"
