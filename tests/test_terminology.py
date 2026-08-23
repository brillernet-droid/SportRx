from sportrx.terminology import build_terminology_guide, terminology_markdown


def test_terminology_guide_keeps_chinese_first_terms_stable():
    guide = build_terminology_guide()
    terms = {item["term"]: item for item in guide["terms"]}

    assert guide["schema"] == "sportrx.terminology_guide"
    assert guide["status"] == "ready_for_language_edition_review"
    assert guide["language_edition_count"] == 3
    assert guide["user_facing_language_editions"] == ["zh_user", "en_user"]
    assert guide["term_count"] >= 10
    assert "HYROX" in terms
    assert "RPE" in terms
    assert "Benchmark" in terms
    assert "Not tested" in terms
    assert "Safety Gate" in terms
    assert "SportRx" in guide["allowed_shared_terms"]
    assert "current measured picture" in " ".join(guide["preferred_language_rules"])
    assert "does not validate SportRx" in guide["claim_boundary"]


def test_terminology_guide_blocks_unvalidated_product_language():
    guide = build_terminology_guide()
    blocked = {item["phrase"] for item in guide["blocked_language"]}

    assert "readiness score" in blocked
    assert "risk percentage" in blocked
    assert "medical clearance" in blocked
    assert "AI coach" in blocked
    assert "official HYROX readiness" in blocked


def test_terminology_markdown_exports_rules_terms_and_boundaries():
    guide = build_terminology_guide()
    markdown = terminology_markdown(guide)

    assert "# SportRx Terminology Guide" in markdown
    assert "HYROX" in markdown
    assert "RPE" in markdown
    assert "Not tested" in markdown
    assert "## Blocked Language" in markdown
    assert "Language editions: 3" in markdown
    assert "medical clearance" in markdown
    assert "does not validate SportRx" in markdown
