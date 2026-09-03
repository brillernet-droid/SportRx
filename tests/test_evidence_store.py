import json
import shutil
import sqlite3
from pathlib import Path

from sportrx.evidence_store import (
    build_protocol_evidence_ledger,
    build_evidence_index,
    evaluate_retrieval_set,
    evaluate_unsafe_query_set,
    search_evidence,
    trace_rule,
    validate_evidence_records,
)


ROOT = Path(__file__).resolve().parents[1]


def test_structured_evidence_records_validate_and_cover_current_rules():
    validation = validate_evidence_records(ROOT)

    assert validation["valid"]
    assert validation["status"] == "ready_for_internal_retrieval"
    assert validation["counts"] == {"sources": 60, "claims": 51, "rules": 17, "protocols": 9}
    assert validation["mapped_rule_count"] == 17
    assert "does not provide medical clearance" in validation["claim_boundary"]


def test_validator_rejects_a_claim_without_a_required_boundary_field(tmp_path):
    shutil.copytree(ROOT / "evidence", tmp_path / "evidence")
    claims_path = tmp_path / "evidence/records/claims.json"
    payload = json.loads(claims_path.read_text(encoding="utf-8"))
    payload["records"][0].pop("applies_to")
    claims_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    validation = validate_evidence_records(tmp_path)

    assert not validation["valid"]
    assert any("claims:CLM-SAFE-001 missing required fields: applies_to" in error for error in validation["errors"])


def test_internal_index_search_and_rule_trace_return_sources_and_limits(tmp_path):
    db_path = tmp_path / "evidence.sqlite"
    index = build_evidence_index(ROOT, db_path)
    search = search_evidence("PATH-001", lane="rules", root=ROOT, db_path=db_path)
    trace = trace_rule("PATH-001", ROOT)

    assert index["document_count"] == 137
    assert db_path.exists()
    with sqlite3.connect(db_path) as connection:
        assert connection.execute("SELECT count(*) FROM evidence_fts").fetchone()[0] == 137
    assert search["results"][0]["id"] == "PATH-001"
    assert search["results"][0]["source_ids"]
    assert search["results"][0]["limitations"]
    assert trace["status"] == "ready"
    assert trace["claims"][0]["id"] == "CLM-PATH-001"
    assert trace["sources"]


def test_validator_rejects_duplicate_source_identifier_across_packs(tmp_path):
    shutil.copytree(ROOT / "evidence", tmp_path / "evidence")
    pack_path = tmp_path / "evidence/records/packs/goal_prescription_sources.json"
    payload = json.loads(pack_path.read_text(encoding="utf-8"))
    payload["records"][1]["identifiers"]["pmid"] = payload["records"][0]["identifiers"]["pmid"]
    pack_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    validation = validate_evidence_records(tmp_path)

    assert not validation["valid"]
    assert any("duplicates pmid" in error for error in validation["errors"])


def test_protocol_evidence_ledger_keeps_each_measurement_component_honest():
    ledger = build_protocol_evidence_ledger(ROOT)
    components = {item["component_id"]: item for item in ledger["components"]}

    assert set(components) == {"1km_run", "6min_run_walk", "erg_1km", "station_circuit", "compromised_run"}
    assert components["1km_run"]["evidence_status"] == "partial_evidence"
    assert components["erg_1km"]["sources"]
    assert components["station_circuit"]["evidence_status"] == "experimental"
    assert "no direct validation" in components["station_circuit"]["limitations"]
    assert "does not validate SportRX scores" in ledger["claim_boundary"]


def test_validator_rejects_missing_component_protocol_evidence(tmp_path):
    shutil.copytree(ROOT / "evidence", tmp_path / "evidence")
    protocols_path = tmp_path / "evidence/records/protocols.json"
    payload = json.loads(protocols_path.read_text(encoding="utf-8"))
    payload["records"] = [
        record for record in payload["records"] if record.get("measurement_component_id") != "erg_1km"
    ]
    protocols_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    validation = validate_evidence_records(tmp_path)

    assert not validation["valid"]
    assert "missing component protocol evidence record: erg_1km" in validation["errors"]


def test_curated_normal_and_unsafe_retrieval_sets_pass(tmp_path):
    normal = evaluate_retrieval_set(ROOT, db_path=tmp_path / "evaluation.sqlite")
    unsafe = evaluate_unsafe_query_set(ROOT)

    assert normal["status"] == "passed"
    assert normal["query_count"] >= 30
    assert unsafe["status"] == "passed"
    assert unsafe["query_count"] >= 15
