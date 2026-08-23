from sportrx.open_source_integration import (
    build_open_source_integration_console,
    open_source_integration_markdown,
)


def test_open_source_integration_console_shows_adopted_and_deferred_boundaries():
    console = build_open_source_integration_console()

    assert console["schema"] == "sportrx.open_source_integration_console"
    assert console["status"] == "architecture_positioned"
    assert console["adopted_count"] >= 7
    assert console["later_count"] >= 4
    assert "AI chat coach" in console["rejected_boundaries"]
    assert "official event readiness label" in console["rejected_boundaries"]
    assert "large exercise browser" in console["rejected_boundaries"]
    assert console["rejected_boundaries"].count("race finish prediction") == 1
    assert "not validate SportRx" in console["claim_boundary"]
    assert console["verified_sources"][0]["status"] == "product_research_only"
    assert any(item["project"] == "FitOntology" and item["status"] == "adopted" for item in console["projects"])
    assert any(item["project"] == "HYROX-Pace" and item["status"] == "later" for item in console["projects"])
    assert any(item["project"] == "WODIS" and item["status"] == "adopted" for item in console["projects"])
    assert any(item["project"] == "OpenAthlete" and item["status"] == "adopted" for item in console["projects"])
    assert any(item["project"] == "Section 11" and item["status"] == "adopted" for item in console["projects"])
    assert any(item["project"] == "REGmon" and item["status"] == "adopted" for item in console["projects"])
    assert any(item["project"] == "AthleteLoadMonitor" and item["status"] == "adopted" for item in console["projects"])
    assert any(item["project"] == "Athlete Report Generator" and item["status"] == "later" for item in console["projects"])
    assert any(item["project"] == "Free Exercise DB" and item["status"] == "later" for item in console["projects"])
    assert any(item["lane"] == "FITT-VP Handoff" for item in console["integration_lanes"])
    assert any(item["lane"] == "Protocol Documents" for item in console["integration_lanes"])
    assert any(item["lane"] == "Pilot Data Capture" for item in console["integration_lanes"])


def test_open_source_integration_markdown_exports_sources_without_claiming_validation():
    console = build_open_source_integration_console()
    markdown = open_source_integration_markdown(console)

    assert "# SportRx Open-Source Integration Notes" in markdown
    assert "https://github.com/aassoiants/workout-open-data-spec" in markdown
    assert "https://github.com/Conalh/fit-ontology" in markdown
    assert "https://github.com/openathleteorg/openathlete" in markdown
    assert "https://github.com/CrankAddict/section-11" in markdown
    assert "https://github.com/REGmon-project/regmon" in markdown
    assert "https://github.com/SaxionAMI/AthleteLoadMonitor" in markdown
    assert "https://github.com/BartWil/athlete_report_generator" in markdown
    assert "## Source Boundary" in markdown
    assert "## Scan Record" in markdown
    assert "## Integration Lanes" in markdown
    assert "fake percentiles" in markdown or "fake percentile" in markdown
    assert "do not validate SportRx" in markdown
    assert "product architecture, UX, export formats, and scope boundaries" in markdown
