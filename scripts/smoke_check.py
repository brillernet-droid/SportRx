"""Local smoke check for a SportRx release candidate."""

from __future__ import annotations

from io import BytesIO
import json
from pathlib import Path
import sys
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sportrx.demo_seed import build_demo_state
from sportrx.export_archive import build_review_pack_zip
from sportrx.export_bundle import build_export_bundle
from sportrx.passport import build_readiness_passport
from sportrx.prescription import generate_prescription
from sportrx.release_package import build_release_package_manifest
from sportrx.runtime_doctor import build_runtime_doctor


def build_smoke_report(root: Path = ROOT) -> dict[str, object]:
    """Run fast product-readiness checks without launching Streamlit."""

    state = build_demo_state()
    profile = state["profile"]
    passport = build_readiness_passport(profile)
    plan = generate_prescription(profile, feedback_by_week=state["feedback_by_week"])
    bundle = build_export_bundle(
        profile,
        passport,
        plan,
        state["benchmark_sessions"],
        state["feedback_by_week"],
        root=str(root),
    )
    zip_bytes = build_review_pack_zip(bundle)
    with ZipFile(BytesIO(zip_bytes)) as archive:
        archive_names = set(archive.namelist())
        archive_manifest = json.loads(archive.read("sportrx_review_pack_manifest.json").decode("utf-8"))
    package_manifest = build_release_package_manifest(root)
    runtime = build_runtime_doctor(root)

    checks = [
        {
            "id": "smoke_runtime",
            "passed": runtime["status"] == "ready_to_run_locally",
            "detail": f"Runtime status: {runtime['status']}.",
        },
        {
            "id": "smoke_export_bundle",
            "passed": len(bundle["files"]) >= 23,
            "detail": f"{len(bundle['files'])} export files generated.",
        },
        {
            "id": "smoke_review_pack_zip",
            "passed": "sportrx_review_pack_manifest.json" in archive_names
            and "sportrx_review_pack_integrity.md" in archive_names
            and "sportrx_reviewer_handoff.md" in archive_names
            and "sportrx_benchmark_worksheet.md" in archive_names
            and archive_manifest["integrity_status"] == "ready_for_review_handoff",
            "detail": f"{len(archive_names)} ZIP entries generated.",
        },
        {
            "id": "smoke_public_package",
            "passed": package_manifest["status"] == "ready_for_public_package",
            "detail": f"Package status: {package_manifest['status']}.",
        },
        {
            "id": "smoke_demo_loop",
            "passed": bool(passport["metric_sources"]["all_metrics"]) and passport["safety_gate"]["status"] in {"GREEN", "YELLOW", "RED"},
            "detail": f"Safety Gate: {passport['safety_gate']['status']}; metrics: {len(passport['metric_sources']['all_metrics'])}.",
        },
    ]
    passed = sum(1 for check in checks if check["passed"])
    return {
        "schema": "sportrx.smoke_check",
        "schema_version": "0.1",
        "status": "pass" if passed == len(checks) else "needs_review",
        "passed_checks": passed,
        "total_checks": len(checks),
        "checks": checks,
        "claim_boundary": "Smoke checks verify local packaging and runtime wiring only; they do not validate SportRx rules or outcomes.",
    }


def main() -> int:
    report = build_smoke_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
