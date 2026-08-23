from sportrx.input_ledger import build_input_ledger, input_ledger_markdown


def test_input_ledger_marks_measured_missing_and_safety_inputs():
    ledger = build_input_ledger(
        {
            "age": 35,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "one_km_run_seconds": 310,
            "station_test_score": None,
            "symptoms": [],
            "known_conditions": ["metabolic_disease"],
        }
    )

    rows = {item["field_id"]: item for item in ledger["rows"]}

    assert ledger["schema"] == "sportrx.input_ledger"
    assert rows["one_km_run_seconds"]["status"] == "active"
    assert rows["one_km_run_seconds"]["source_type"] == "measured"
    assert rows["station_test_score"]["status"] == "not_tested"
    assert rows["station_test_score"]["affects_output"] is False
    assert rows["known_conditions"]["source_type"] == "safety_screen"
    assert "never changes measured performance" in rows["known_conditions"]["output_role"]
    assert ledger["summary"]["measured_tests_recorded"] == 1


def test_input_ledger_tracks_protocol_provenance_fields():
    ledger = build_input_ledger(
        {
            "age": 35,
            "station_test_score": 72,
            "station_test_protocol": "SportRx Hybrid Benchmark v1 0.1 / standard / Benchmark Log 2026-08-22",
            "work_capacity_test_score": 68,
        }
    )
    rows = {item["field_id"]: item for item in ledger["rows"]}

    assert rows["station_test_protocol"]["source_type"] == "protocol_provenance"
    assert rows["station_test_protocol"]["status"] == "active"
    assert rows["station_test_protocol"]["affects_output"] is True
    assert "review readiness" in rows["station_test_protocol"]["output_role"]
    assert rows["work_capacity_test_protocol"]["status"] == "not_provided"
    assert rows["work_capacity_test_protocol"]["affects_output"] is False


def test_input_ledger_exposes_legacy_and_ignored_fields_without_using_them():
    ledger = build_input_ledger(
        {
            "age": 35,
            "training_days": 3,
            "weekly_training_minutes": 120,
            "running_comfort": 4,
            "vo2max": 54,
            "hrmax": 190,
        }
    )
    rows = {item["field_id"]: item for item in ledger["rows"]}

    assert rows["running_comfort"]["status"] == "legacy"
    assert rows["running_comfort"]["affects_output"] is False
    assert rows["vo2max"]["status"] == "ignored"
    assert rows["hrmax"]["status"] == "ignored"
    assert ledger["summary"]["legacy_or_ignored"] == 3


def test_input_ledger_markdown_lists_claim_boundary_and_roles():
    markdown = input_ledger_markdown(build_input_ledger({"age": 35, "one_km_run_seconds": 300}))

    assert "# SportRx Input Ledger" in markdown
    assert "one_km_run_seconds" in markdown
    assert "does not validate rules" in markdown
