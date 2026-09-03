"""Audit the evidence chain behind each SportRX goal route."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .evidence_store import load_evidence_records
from .knowledge_rag import load_knowledge_cards


MANIFEST_PATH = "evidence/prescription/manifest.json"
REQUIRED_GOALS = {
    "build_habit",
    "improve_aerobic_fitness",
    "general_fitness",
    "muscle_gain",
    "fat_loss",
    "performance_entry",
}
PRODUCT_STATUSES = {
    "active_aerobic_foundation",
    "active_but_aerobic_only",
    "assessment_only",
    "measurement_first",
}
REQUIRED_FIELDS = {
    "goal_id",
    "label_zh",
    "product_status",
    "rule_ids",
    "claim_ids",
    "source_ids",
    "card_ids",
    "supports",
    "does_not_support",
    "next_evidence_action",
}


def load_prescription_knowledge(root: str | Path = ".") -> dict[str, Any]:
    path = Path(root).resolve() / MANIFEST_PATH
    return json.loads(path.read_text(encoding="utf-8"))


def validate_prescription_knowledge(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root).resolve()
    payload = load_prescription_knowledge(root_path)
    goals = payload.get("goals", [])
    evidence = load_evidence_records(root_path)
    known = {lane: {item["id"] for item in records} for lane, records in evidence.items()}
    known["cards"] = {item["id"] for item in load_knowledge_cards(root_path)}
    errors: list[str] = []
    seen: set[str] = set()

    for goal in goals:
        goal_id = str(goal.get("goal_id", "<missing>"))
        if goal_id in seen:
            errors.append(f"duplicate goal_id: {goal_id}")
        seen.add(goal_id)
        missing = sorted(field for field in REQUIRED_FIELDS if field not in goal or goal[field] in (None, ""))
        if missing:
            errors.append(f"goal:{goal_id} missing fields: {', '.join(missing)}")
        if goal.get("product_status") not in PRODUCT_STATUSES:
            errors.append(f"goal:{goal_id} has invalid product_status")
        for lane, field in (("rules", "rule_ids"), ("claims", "claim_ids"), ("sources", "source_ids"), ("cards", "card_ids")):
            for record_id in goal.get(field, []):
                if record_id not in known[lane]:
                    errors.append(f"goal:{goal_id} references unknown {lane[:-1]}: {record_id}")
        if goal.get("product_status", "").startswith("active") and not goal.get("rule_ids"):
            errors.append(f"goal:{goal_id} is active without a deterministic rule mapping")
        if not goal.get("claim_ids") or not goal.get("source_ids") or not goal.get("card_ids"):
            errors.append(f"goal:{goal_id} has an incomplete evidence chain")
        if not goal.get("supports") or not goal.get("does_not_support"):
            errors.append(f"goal:{goal_id} needs supported and prohibited language")

    missing_goals = sorted(REQUIRED_GOALS - seen)
    if missing_goals:
        errors.append(f"missing goal routes: {', '.join(missing_goals)}")

    return {
        "schema": "sportrx.prescription_knowledge_validation",
        "schema_version": "0.1",
        "valid": not errors,
        "status": "review_ready" if not errors else "needs_revision",
        "goal_count": len(goals),
        "mapped_goal_ids": sorted(seen),
        "errors": errors,
        "claim_boundary": (
            "This manifest documents evidence coverage and product status. It does not enable a program pack, "
            "change exercise dose, or validate individual outcomes."
        ),
    }
