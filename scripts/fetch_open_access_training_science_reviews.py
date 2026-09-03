"""Download reviewed open-access training-science JATS XML to private storage.

The fixed list contains only articles with PubMed Central records. Downloads
and checksums stay under ``evidence/private/`` and never enter Git, release
packages, or Knowledge RAG model context.
"""

from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "evidence/private/fulltext/training_science"
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"

OPEN_ACCESS_ARTICLES = (
    ("TS-RT-UMBRELLA-2024", "PMC10818109", "10.1016/j.jshs.2023.06.005", "resistance_prescription_umbrella_2024"),
    ("TS-RT-REST-2024", "PMC11349676", "10.3389/fspor.2024.1429789", "inter_set_rest_2024"),
    ("TS-RT-VL-2023", "PMC9807551", "10.1007/s40279-022-01754-4", "velocity_loss_2023"),
    ("TS-RT-AUTOREG-2022", "PMC8762534", "10.1186/s40798-021-00404-9", "autoregulation_2022"),
    ("TS-END-TID-2024", "PMC11329428", "10.1007/s40279-024-02034-z", "endurance_intensity_distribution_2024"),
    ("TS-END-TAPER-2023", "PMC10171681", "10.1371/journal.pone.0282838", "endurance_taper_2023"),
    ("TS-FLEX-CHRONIC-2024", "PMC10980866", "10.1016/j.jshs.2023.06.002", "chronic_stretching_2024"),
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download(url: str, destination: Path) -> None:
    request = Request(url, headers={"User-Agent": "SportRX-evidence-fetch/0.1"})
    with urlopen(request, timeout=120) as response:  # nosec B310: fixed reviewed HTTPS endpoints
        payload = response.read()
    if b"<article" not in payload[:1000]:
        raise ValueError(f"Download from {url} is not JATS full-text XML.")
    destination.write_bytes(payload)


def fetch_open_access_reviews(*, force: bool = False) -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for source_id, pmcid, doi, stem in OPEN_ACCESS_ARTICLES:
        filename = f"{pmcid}_{stem}.xml"
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
        destination = OUTPUT_DIR / filename
        if force or not destination.exists():
            _download(url, destination)
            status = "downloaded"
        else:
            status = "already_present"
        records.append(
            {
                "source_id": source_id,
                "pmcid": pmcid,
                "doi": doi,
                "filename": filename,
                "download_url": url,
                "access_check": "PubMed Central record; JATS full text downloaded through the Europe PMC REST API",
                "status": status,
                "bytes": destination.stat().st_size,
                "sha256": _sha256(destination),
            }
        )

    manifest = {
        "schema": "sportrx.private_fulltext_manifest.v1",
        "retrieved_at": date.today().isoformat(),
        "storage_policy": "Local private storage only; excluded from Git, public release packages and model context.",
        "records": records,
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


if __name__ == "__main__":
    print(json.dumps(fetch_open_access_reviews(), ensure_ascii=False, indent=2))
