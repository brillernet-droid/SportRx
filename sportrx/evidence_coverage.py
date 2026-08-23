"""Evidence coverage registry for SportRx release review.

This module summarizes local evidence files and rule-evidence coverage. It is
not a scientific validation engine.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


CLAIM_BOUNDARY = (
    "Evidence Coverage summarizes local evidence files and rule-evidence mapping "
    "for release review only. It does not validate SportRx, prove outcomes, "
    "create athlete norms, or provide medical clearance."
)


REQUIRED_EVIDENCE_FILES = [
    "evidence/claim_policy.md",
    "evidence/rule_evidence_map.md",
    "evidence/validation_plan.md",
    "evidence/library/source_index.md",
]


def _read_text(root: str | Path, relative_path: str) -> str:
    path = Path(root) / relative_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _parse_rule_rows(markdown: str) -> list[dict[str, Any]]:
    rows = []
    in_rules = False
    for line in markdown.splitlines():
        if line.strip() == "## Current Rules":
            in_rules = True
            continue
        if in_rules and line.startswith("## "):
            break
        if not in_rules or not line.startswith("|"):
            continue
        cells = [cell.strip().replace("`", "") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 7 or cells[0] in {"Rule ID", "---"}:
            continue
        rows.append(
            {
                "rule_id": cells[0],
                "product_rule": cells[1],
                "inputs": cells[2],
                "evidence_tier": cells[3],
                "sources": [source.strip() for source in cells[4].split(",") if source.strip()],
                "status": cells[5],
                "notes": cells[6],
            }
        )
    return rows


def _count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item.get(key, "unknown")] = counts.get(item.get(key, "unknown"), 0) + 1
    return dict(sorted(counts.items()))


def build_evidence_coverage(
    root: str | Path = ".",
    evidence_files_present: dict[str, bool] | None = None,
) -> dict[str, Any]:
    """Build a release-review summary of evidence files and mapped rules."""

    evidence_files_present = evidence_files_present or {
        path: (Path(root) / path).exists() for path in REQUIRED_EVIDENCE_FILES
    }
    rule_text = _read_text(root, "evidence/rule_evidence_map.md")
    claim_text = _read_text(root, "evidence/claim_policy.md")
    validation_text = _read_text(root, "evidence/validation.md")
    source_index_text = _read_text(root, "evidence/library/source_index.md")
    rules = _parse_rule_rows(rule_text)

    status_counts = _count_by(rules, "status")
    tier_counts: dict[str, int] = {}
    for rule in rules:
        for tier in [item.strip() for item in rule["evidence_tier"].split("/") if item.strip()]:
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
    tier_counts = dict(sorted(tier_counts.items()))

    source_ids = sorted({source for rule in rules for source in rule["sources"] if source != "None"})
    forbidden_terms = [
        "Completion probability",
        "Injury-risk percentage",
        "Fake percentiles or norms",
        "Medical clearance",
    ]
    forbidden_present = [term for term in forbidden_terms if term in claim_text]
    validation_boundaries = [
        phrase
        for phrase in [
            "does not claim formal validation",
            "Not Validated",
            "Knowledge Base Status",
        ]
        if phrase in validation_text
    ]
    source_index_ready = bool(source_index_text and "Evidence ID" in source_index_text)
    required_ready = bool(evidence_files_present) and all(evidence_files_present.values())
    blocked_rules = [rule for rule in rules if rule["status"] == "blocked"]
    explain_only_rules = [rule for rule in rules if rule["status"] == "explain_only"]

    status = "ready_for_release_review"
    if not required_ready or not rules or not source_index_ready:
        status = "needs_evidence_context"

    return {
        "schema": "sportrx.evidence_coverage",
        "schema_version": "0.1",
        "status": status,
        "required_files": [
            {
                "path": path,
                "present": bool(evidence_files_present.get(path, False)),
            }
            for path in REQUIRED_EVIDENCE_FILES
        ],
        "required_files_present": sum(1 for value in evidence_files_present.values() if value),
        "required_file_count": len(REQUIRED_EVIDENCE_FILES),
        "rule_count": len(rules),
        "status_counts": status_counts,
        "tier_counts": tier_counts,
        "source_count": len(source_ids),
        "source_ids": source_ids,
        "blocked_rules": blocked_rules,
        "explain_only_rules": explain_only_rules,
        "rules": rules,
        "forbidden_claims_present": forbidden_present,
        "validation_boundaries": validation_boundaries,
        "source_index_ready": source_index_ready,
        "primary_message": "SportRx exposes rule evidence coverage before inviting external reviewers.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def evidence_coverage_markdown(coverage: dict[str, Any]) -> str:
    """Export evidence coverage as Markdown."""

    lines = [
        "# SportRx Evidence Coverage",
        "",
        f"- Status: {coverage['status']}",
        f"- Required files: {coverage['required_files_present']} / {coverage['required_file_count']}",
        f"- Rules mapped: {coverage['rule_count']}",
        f"- Sources referenced: {coverage['source_count']}",
        f"- Claim boundary: {coverage['claim_boundary']}",
        "",
        "## Rule Status Counts",
    ]
    for status, count in coverage["status_counts"].items():
        lines.append(f"- {status}: {count}")

    lines.extend(["", "## Evidence Tier Counts"])
    for tier, count in coverage["tier_counts"].items():
        lines.append(f"- {tier}: {count}")

    lines.extend(["", "## Required Evidence Files"])
    for item in coverage["required_files"]:
        mark = "present" if item["present"] else "missing"
        lines.append(f"- {item['path']}: {mark}")

    lines.extend(["", "## Explain-Only Rules"])
    for rule in coverage["explain_only_rules"]:
        lines.append(f"- `{rule['rule_id']}` - {rule['product_rule']}")

    lines.extend(["", "## Blocked Rules"])
    for rule in coverage["blocked_rules"]:
        lines.append(f"- `{rule['rule_id']}` - {rule['product_rule']}: {rule['notes']}")

    lines.extend(["", "## Forbidden Claim Policy"])
    for item in coverage["forbidden_claims_present"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"
