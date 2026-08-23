from sportrx.schema_registry import build_measurement_schema_registry, measurement_schema_registry_markdown


def test_schema_registry_documents_local_data_contracts():
    registry = build_measurement_schema_registry()

    assert registry["schema"] == "sportrx.measurement_schema_registry"
    assert registry["status"] == "complete"
    assert registry["object_count"] >= 10
    assert registry["exported_object_count"] == registry["object_count"]
    assert any(item["id"] == "benchmark_session" for item in registry["objects"])
    assert any(item["id"] == "component_result" for item in registry["objects"])
    assert "does not validate measures" in registry["claim_boundary"]


def test_schema_registry_flags_missing_export_coverage():
    registry = build_measurement_schema_registry({"benchmark_log_json", "manifest_json"})

    assert registry["status"] == "missing_export_coverage"
    assert registry["missing_export_count"] > 0
    assert any(item["export_status"] == "missing_from_current_bundle" for item in registry["objects"])


def test_schema_registry_markdown_exports_objects_and_boundaries():
    registry = build_measurement_schema_registry()
    markdown = measurement_schema_registry_markdown(registry)

    assert "# SportRx Measurement Schema Registry" in markdown
    assert "Benchmark Session" in markdown
    assert "Component Result" in markdown
    assert "Not-tested policy" in markdown
    assert "medical clearance" in markdown
