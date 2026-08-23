from sportrx.evidence_library import build_evidence_library, evidence_library_markdown


def test_evidence_library_indexes_saved_sources():
    library = build_evidence_library(".")

    assert library["schema"] == "sportrx.evidence_library"
    assert library["status"] == "ready_for_review"
    assert library["source_count"] >= 20
    assert library["topic_count"] >= 4
    assert library["required_files_present"] == library["required_file_count"]
    assert any(item["id"] == "PA-WHO-2020" for item in library["sources"])
    assert any(item["id"] == "HYROX-PHYS-2025" for item in library["sources"])
    assert "A" in library["tier_counts"]
    assert library["quality_summary"]["appraised_sources"] == library["source_count"]
    assert library["quality_summary"]["measurement_sources"] >= 1
    assert library["topic_cards"]
    assert all("strongest_tier" in item for item in library["topic_cards"])
    assert "not a systematic review" in library["claim_boundary"]


def test_evidence_library_preserves_source_limits():
    library = build_evidence_library(".")
    hyrox = next(item for item in library["sources"] if item["id"] == "HYROX-PHYS-2025")

    assert hyrox["topic"] == "HYROX, HIFT, And Hybrid Competition"
    assert hyrox["evidence_tier"] == "C"
    assert "prediction" in hyrox["limits"].lower()
    assert hyrox["saved_in"].startswith("evidence/library/")


def test_evidence_library_markdown_exports_topics_and_sources():
    library = build_evidence_library(".")
    markdown = evidence_library_markdown(library)

    assert "# SportRx Evidence Library" in markdown
    assert "Guideline And Public-Health Foundations" in markdown
    assert "PA-WHO-2020" in markdown
    assert "HYROX-PHYS-2025" in markdown
    assert "Quality Summary" in markdown
    assert "Claim boundary" in markdown
