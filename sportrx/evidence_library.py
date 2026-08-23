"""Evidence library index for SportRx local source files."""

from __future__ import annotations

from pathlib import Path
from typing import Any


CLAIM_BOUNDARY = (
    "Evidence Library summarizes locally saved SportRx evidence notes for "
    "review. It is not a systematic review, automated citation engine, RAG "
    "system, scientific validation, or medical clearance."
)


REQUIRED_LIBRARY_FILES = [
    "evidence/library/source_index.md",
    "evidence/literature_matrix.md",
    "evidence/evidence_appraisal.md",
    "evidence/claim_policy.md",
]


def _tier_sort_key(tier: str) -> tuple[int, str]:
    order = {"A": 0, "B": 1, "B/C": 2, "C": 3, "not_appraised": 9}
    return (order.get(tier, 8), tier)


def _split_table_row(line: str) -> list[str]:
    return [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(set(cell.replace(" ", "")) <= {"-", ":"} for cell in cells)


def _parse_section_tables(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []

    rows: list[dict[str, str]] = []
    section = "Uncategorized"
    header: list[str] | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            section = line[3:].strip()
            header = None
            continue
        if not line.startswith("|"):
            header = None
            continue

        cells = _split_table_row(line)
        if _is_separator_row(cells):
            continue
        if header is None:
            header = cells
            continue
        if len(cells) != len(header):
            continue

        row = {key: value for key, value in zip(header, cells)}
        row["section"] = section
        rows.append(row)

    return rows


def build_evidence_library(root: str | Path = ".") -> dict[str, Any]:
    """Build a browsable index from the local SportRx evidence files."""

    root_path = Path(root)
    file_status = {path: (root_path / path).exists() for path in REQUIRED_LIBRARY_FILES}
    source_rows = _parse_section_tables(root_path / "evidence/library/source_index.md")
    matrix_rows = _parse_section_tables(root_path / "evidence/literature_matrix.md")

    matrix_by_id = {row.get("ID", ""): row for row in matrix_rows if row.get("ID")}
    sources: list[dict[str, Any]] = []
    for row in source_rows:
        source_id = row.get("Evidence ID", "")
        matrix = matrix_by_id.get(source_id, {})
        saved_in = row.get("Saved in", "")
        sources.append(
            {
                "id": source_id,
                "topic": row.get("section", "Uncategorized"),
                "source": row.get("Source", ""),
                "saved_in": f"evidence/library/{saved_in}" if saved_in and not saved_in.startswith("evidence/") else saved_in,
                "product_use": row.get("Product use", ""),
                "evidence_tier": matrix.get("Evidence tier", "not_appraised"),
                "limits": matrix.get("Limits", "Not yet appraised in literature_matrix.md."),
            }
        )

    topic_order: list[str] = []
    for item in sources:
        if item["topic"] not in topic_order:
            topic_order.append(item["topic"])

    topics = [
        {
            "topic": topic,
            "source_count": sum(1 for item in sources if item["topic"] == topic),
            "source_ids": [item["id"] for item in sources if item["topic"] == topic],
        }
        for topic in topic_order
    ]

    tier_counts: dict[str, int] = {}
    for item in sources:
        tier = item["evidence_tier"]
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
    tier_counts = dict(sorted(tier_counts.items(), key=lambda item: _tier_sort_key(item[0])))

    missing_appraisal_ids = [item["id"] for item in sources if item["evidence_tier"] == "not_appraised"]
    topic_cards: list[dict[str, Any]] = []
    for topic in topics:
        topic_sources = [item for item in sources if item["topic"] == topic["topic"]]
        topic_tiers: dict[str, int] = {}
        for item in topic_sources:
            tier = item["evidence_tier"]
            topic_tiers[tier] = topic_tiers.get(tier, 0) + 1
        topic_cards.append(
            {
                "topic": topic["topic"],
                "source_count": topic["source_count"],
                "source_ids": topic["source_ids"],
                "tier_counts": dict(sorted(topic_tiers.items(), key=lambda item: _tier_sort_key(item[0]))),
                "strongest_tier": min(topic_tiers, key=_tier_sort_key) if topic_tiers else "not_appraised",
                "needs_appraisal": any(item["evidence_tier"] == "not_appraised" for item in topic_sources),
                "example_limit": next((item["limits"] for item in topic_sources if item["limits"]), "No limits recorded."),
            }
        )

    quality_summary = {
        "appraised_sources": sum(1 for item in sources if item["evidence_tier"] != "not_appraised"),
        "not_appraised_sources": len(missing_appraisal_ids),
        "guideline_sources": sum(1 for item in sources if item["evidence_tier"] == "A"),
        "measurement_sources": sum(1 for item in sources if "Measurement" in item["topic"]),
        "hybrid_sources": sum(1 for item in sources if "HYROX" in item["topic"] or "Hybrid" in item["topic"]),
    }
    status = "ready_for_review" if all(file_status.values()) and sources else "needs_review"
    return {
        "schema": "sportrx.evidence_library",
        "schema_version": "0.1",
        "status": status,
        "required_files_present": sum(1 for present in file_status.values() if present),
        "required_file_count": len(file_status),
        "required_files": [{"path": path, "present": present} for path, present in file_status.items()],
        "source_count": len(sources),
        "topic_count": len(topics),
        "tier_counts": tier_counts,
        "quality_summary": quality_summary,
        "missing_appraisal_ids": missing_appraisal_ids,
        "topics": topics,
        "topic_cards": topic_cards,
        "sources": sources,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def evidence_library_markdown(library: dict[str, Any]) -> str:
    """Export the Evidence Library index as Markdown."""

    lines = [
        "# SportRx Evidence Library",
        "",
        f"- Status: {library['status']}",
        f"- Sources: {library['source_count']}",
        f"- Topics: {library['topic_count']}",
        f"- Required files: {library['required_files_present']} / {library['required_file_count']}",
        f"- Claim boundary: {library['claim_boundary']}",
        "",
        "## Topics",
    ]
    for topic in library.get("topic_cards", library["topics"]):
        tier_summary = ", ".join(f"{tier}: {count}" for tier, count in topic.get("tier_counts", {}).items())
        tier_suffix = f" ({tier_summary})" if tier_summary else ""
        lines.append(f"- {topic['topic']}: {topic['source_count']} sources{tier_suffix}")

    if library.get("quality_summary"):
        summary = library["quality_summary"]
        lines.extend(
            [
                "",
                "## Quality Summary",
                f"- Appraised sources: {summary['appraised_sources']}",
                f"- Not appraised sources: {summary['not_appraised_sources']}",
                f"- Guideline sources: {summary['guideline_sources']}",
                f"- Measurement sources: {summary['measurement_sources']}",
                f"- Hybrid/HYROX sources: {summary['hybrid_sources']}",
            ]
        )

    lines.extend(["", "## Sources"])
    for item in library["sources"]:
        lines.extend(
            [
                "",
                f"### {item['id']}",
                f"- Topic: {item['topic']}",
                f"- Source: {item['source']}",
                f"- Evidence tier: {item['evidence_tier']}",
                f"- Saved in: `{item['saved_in']}`",
                f"- Product use: {item['product_use']}",
                f"- Limits: {item['limits']}",
            ]
        )

    if library["missing_appraisal_ids"]:
        lines.extend(["", "## Missing Appraisal"])
        for source_id in library["missing_appraisal_ids"]:
            lines.append(f"- `{source_id}`")

    return "\n".join(lines) + "\n"
