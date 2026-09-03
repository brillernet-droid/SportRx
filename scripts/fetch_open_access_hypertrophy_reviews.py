"""Download the reviewed open-access hypertrophy PDFs to ignored private storage.

Only articles verified as open access in Europe PMC are listed here. The files
and generated manifest stay under ``evidence/private/`` and are never included
in the public release package or Knowledge RAG model context.
"""

from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "evidence/private/fulltext/hypertrophy"
MANIFEST_PATH = OUTPUT_DIR / "manifest.json"

OPEN_ACCESS_ARTICLES = (
    {
        "source_id": "RT-FREE-MACHINE-SR-2023",
        "pmcid": "PMC10426227",
        "doi": "10.1186/s13102-023-00713-4",
        "filename": "PMC10426227_free_weight_vs_machine_2023.pdf",
        "download_url": "https://europepmc.org/articles/PMC10426227?pdf=render",
        "access_check": "Europe PMC isOpenAccess=Y and hasPDF=Y",
    },
    {
        "source_id": "RT-ROM-SR-2020",
        "pmcid": "PMC6977096",
        "doi": "10.1177/2050312120901559",
        "filename": "PMC6977096_range_of_motion_2020.pdf",
        "download_url": "https://europepmc.org/articles/PMC6977096?pdf=render",
        "access_check": "Europe PMC isOpenAccess=Y and hasPDF=Y",
    },
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download(article: dict[str, str], destination: Path) -> None:
    request = Request(article["download_url"], headers={"User-Agent": "SportRX-evidence-fetch/0.1"})
    with urlopen(request, timeout=120) as response:  # nosec B310: fixed reviewed HTTPS endpoints
        payload = response.read()
    if not payload.startswith(b"%PDF-"):
        raise ValueError(f"Download for {article['source_id']} is not a PDF.")
    destination.write_bytes(payload)


def fetch_open_access_reviews(*, force: bool = False) -> dict[str, object]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for article in OPEN_ACCESS_ARTICLES:
        destination = OUTPUT_DIR / article["filename"]
        if force or not destination.exists():
            _download(article, destination)
            status = "downloaded"
        else:
            status = "already_present"
        records.append(
            {
                **article,
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
    result = fetch_open_access_reviews()
    print(json.dumps(result, ensure_ascii=False, indent=2))
