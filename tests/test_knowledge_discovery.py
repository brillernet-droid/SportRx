from sportrx.knowledge_discovery import discover_knowledge_candidates


def test_crossref_discovery_normalises_metadata_into_candidates_only():
    def fetch_json(_: str):
        return {"message": {"items": [{"DOI": "10.1000/test", "title": ["Test review"], "URL": "https://doi.org/10.1000/test", "container-title": ["Sports Medicine"], "published": {"date-parts": [[2025]]}}]}}

    result = discover_knowledge_candidates("endurance training", "endurance", fetch_json=fetch_json)

    assert result["provider"] == "crossref"
    assert result["status"] == "review_required"
    assert result["candidates"][0]["doi"] == "10.1000/test"
    assert result["candidates"][0]["review_status"] == "candidate"
