"""Metadata-only discovery adapters for the SportRX Knowledge RAG queue."""

from __future__ import annotations

import json
from typing import Any, Callable
from urllib.parse import quote_plus
from urllib.request import urlopen

from .knowledge_rag import KNOWLEDGE_TOPICS, ingest_candidates


FetchJson = Callable[[str], dict[str, Any]]


def _fetch_json(url: str) -> dict[str, Any]:
    with urlopen(url, timeout=20) as response:  # nosec B310 - fixed public metadata endpoints
        return json.loads(response.read().decode("utf-8"))


def discover_knowledge_candidates(
    query: str,
    topic: str,
    provider: str = "crossref",
    rows: int = 10,
    fetch_json: FetchJson | None = None,
) -> dict[str, Any]:
    """Discover metadata candidates; review is still required before indexing."""

    if topic not in KNOWLEDGE_TOPICS:
        raise ValueError("topic must be a known SportRX knowledge topic")
    if provider not in {"crossref", "openalex", "pubmed"}:
        raise ValueError("provider must be crossref, openalex, or pubmed")
    fetch_json = fetch_json or _fetch_json
    count = max(1, min(int(rows), 20))
    encoded = quote_plus(query)
    if provider == "crossref":
        payload = fetch_json(f"https://api.crossref.org/works?query.bibliographic={encoded}&rows={count}")
        raw = [
            {
                "id": f"CROSSREF-{item.get('DOI', '') or index}",
                "title": (item.get("title") or [""])[0],
                "doi": item.get("DOI"),
                "source_url": item.get("URL"),
                "journal": (item.get("container-title") or [""])[0],
                "year": (item.get("published", {}).get("date-parts") or [[None]])[0][0],
                "topic": topic,
                "discovery_source": "crossref",
            }
            for index, item in enumerate(payload.get("message", {}).get("items", []), start=1)
        ]
    elif provider == "openalex":
        payload = fetch_json(f"https://api.openalex.org/works?search={encoded}&per-page={count}")
        raw = [
            {
                "id": f"OPENALEX-{item.get('id', '').rsplit('/', 1)[-1] or index}",
                "title": item.get("title"),
                "doi": (item.get("doi") or "").removeprefix("https://doi.org/"),
                "source_url": item.get("doi") or item.get("id"),
                "journal": (item.get("primary_location", {}).get("source") or {}).get("display_name"),
                "year": item.get("publication_year"),
                "topic": topic,
                "discovery_source": "openalex",
            }
            for index, item in enumerate(payload.get("results", []), start=1)
        ]
    else:
        search = fetch_json(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax={count}&term={encoded}")
        ids = search.get("esearchresult", {}).get("idlist", [])
        if not ids:
            raw = []
        else:
            details = fetch_json("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id=" + ",".join(ids))
            raw = [
                {
                    "id": f"PMID-{pmid}",
                    "title": details.get("result", {}).get(pmid, {}).get("title"),
                    "pmid": pmid,
                    "source_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    "journal": details.get("result", {}).get(pmid, {}).get("fulljournalname"),
                    "year": details.get("result", {}).get(pmid, {}).get("pubdate", "")[:4],
                    "topic": topic,
                    "discovery_source": "pubmed",
                }
                for pmid in ids
            ]
    result = ingest_candidates(raw)
    result.update({"provider": provider, "query": query, "topic": topic})
    return result
