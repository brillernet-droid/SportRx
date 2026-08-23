from sportrx.protocol_source import (
    build_protocol_source_guide,
    protocol_source_guide_markdown,
    resolve_protocol_source_choice,
    resolve_protocol_source_value,
)


def test_protocol_source_guide_lists_accepted_sources_and_boundaries():
    guide = build_protocol_source_guide(
        {
            "station_test_score": 70,
            "station_test_protocol": "SportRx Hybrid Benchmark v1 / standard",
            "work_capacity_test_score": 65,
        }
    )

    assert guide["schema"] == "sportrx.protocol_source_guide"
    assert guide["status"] == "needs_protocol_source"
    assert guide["preset_count"] == 4
    assert guide["required_source_count"] == 2
    assert guide["recorded_source_count"] == 1
    assert any(item["source"] == "Benchmark Log import" for item in guide["sources"])
    assert "does not validate protocols" in guide["claim_boundary"]


def test_protocol_source_resolution_preserves_custom_documented_source():
    assert resolve_protocol_source_choice("Coach protocol v2") == "Other documented protocol"
    assert resolve_protocol_source_value("Other documented protocol", "Coach protocol v2") == "Coach protocol v2"
    assert resolve_protocol_source_value("Benchmark Log import") == "Benchmark Log import"


def test_protocol_source_guide_markdown_exports_sources_and_current_fields():
    markdown = protocol_source_guide_markdown(
        build_protocol_source_guide(
            {
                "station_test_score": 70,
                "station_test_protocol": "Benchmark Log import",
            }
        )
    )

    assert "# SportRx Protocol Source Guide" in markdown
    assert "SportRx Hybrid Benchmark v1 / standard" in markdown
    assert "Benchmark Log import" in markdown
    assert "station_test_protocol" in markdown
