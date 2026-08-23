from sportrx.test_day_brief import build_test_day_brief, test_day_brief_markdown


def test_test_day_brief_builds_standard_operator_checklist():
    brief = build_test_day_brief(["row", "kettlebell", "track"])

    assert brief["schema"] == "sportrx.test_day_brief"
    assert brief["path"] == "standard"
    assert brief["pre_test_checks"]
    assert len(brief["components"]) >= 3
    assert brief["components"][0]["order"] == 1
    assert "RPE_0_10" in brief["components"][0]["record_fields"]
    assert any("Safety Gate is not RED" in item for item in brief["pre_test_checks"])


def test_test_day_brief_keeps_low_equipment_path():
    brief = build_test_day_brief([])

    component_ids = {component["component_id"] for component in brief["components"]}

    assert brief["path"] == "low_equipment"
    assert "run_1km_or_6min" in component_ids
    assert "bodyweight_circuit" in component_ids


def test_test_day_brief_claim_boundary_blocks_overclaiming():
    brief = build_test_day_brief(["ski"])
    claim = brief["claim_boundary"].lower()

    assert "does not score performance" in claim
    assert "predict race results" in claim
    assert "medical clearance" in claim


def test_test_day_brief_markdown_exports_component_order():
    brief = build_test_day_brief(["row", "kettlebell"])
    markdown = test_day_brief_markdown(brief)

    assert "# SportRx Test-Day Brief" in markdown
    assert "Component Order" in markdown
    assert "1 km run" in markdown
    assert "After Test" in markdown
