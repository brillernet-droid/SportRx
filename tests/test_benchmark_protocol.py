from sportrx.benchmark_protocol import get_benchmark_protocol, protocol_markdown


def test_standard_protocol_includes_stop_rules_and_components():
    protocol = get_benchmark_protocol(["row", "kettlebell"])

    assert protocol["path"] == "standard"
    assert protocol["global_stop_rules"]
    assert any("Safety Gate is RED" in rule for rule in protocol["global_stop_rules"])
    assert {component["component_id"] for component in protocol["component_protocols"]} >= {
        "run_1km",
        "station_circuit",
        "row_or_ski_1km",
    }


def test_low_equipment_protocol_keeps_low_equipment_path():
    protocol = get_benchmark_protocol([])

    assert protocol["path"] == "low_equipment"
    component_ids = {component["component_id"] for component in protocol["component_protocols"]}
    assert "run_1km_or_6min" in component_ids
    assert "bodyweight_circuit" in component_ids


def test_protocol_claim_boundary_blocks_overclaims():
    protocol = get_benchmark_protocol(["ski"])

    claim = protocol["claim_boundary"].lower()
    assert "not a validated score" in claim
    assert "race prediction" in claim
    assert "medical clearance" in claim


def test_protocol_markdown_exports_components_and_recording_principles():
    protocol = get_benchmark_protocol(["row", "kettlebell"])
    exported = protocol_markdown(protocol)

    assert "# SportRx Hybrid Benchmark v1" in exported
    assert "1 km run" in exported
    assert "Missing components stay Not tested" in exported
    assert "percentile" in exported
