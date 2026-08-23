from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_check_builds_pass_report():
    namespace = runpy.run_path(str(ROOT / "scripts" / "smoke_check.py"))
    report = namespace["build_smoke_report"](ROOT)

    assert report["schema"] == "sportrx.smoke_check"
    assert report["status"] == "pass"
    assert report["passed_checks"] == report["total_checks"]
    assert any(check["id"] == "smoke_review_pack_zip" for check in report["checks"])
    assert "do not validate SportRx rules" in report["claim_boundary"]
