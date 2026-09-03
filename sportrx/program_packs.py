"""Versioned Program Pack registry and non-diagnostic route selection.

The core engine does not infer a training dose from a broad population label.
It first resolves a versioned Pack, then the Pack's rule IDs determine whether
the current product is allowed to generate a prescription. This first registry
keeps only the aerobic rules live; other routes deliberately remain assessment
or professional-collaboration paths.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


PACK_DIRECTORY = Path(__file__).resolve().parents[1] / "data" / "program_packs"
RULE_RECORD_PATH = Path(__file__).resolve().parents[1] / "evidence" / "records" / "rules.json"
_REQUIRED_FIELDS = {
    "id",
    "version",
    "name",
    "release_status",
    "automation_level",
    "applicability",
    "exclusions",
    "required_inputs",
    "rule_ids",
    "measurement_protocols",
    "content_mapping",
    "evidence_version",
    "limitations",
    "withdrawal_switch",
}
_GOAL_ALIASES = {
    "Improve aerobic fitness / general health": "build_activity_habit",
    "improve_aerobic_fitness": "improve_aerobic_fitness",
    "build_activity_habit": "build_activity_habit",
    "general_fitness": "general_fitness",
    "muscle_gain": "muscle_gain",
    "fat_loss": "fat_loss",
    "metabolic_health": "metabolic_health",
    "performance_entry": "performance_entry",
}


def load_program_packs() -> list[dict[str, Any]]:
    """Load the public registry in a stable order after validating it."""

    packs: list[dict[str, Any]] = []
    for path in sorted(PACK_DIRECTORY.glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            packs.append(json.load(handle))
    validate_program_packs(packs)
    return packs


def validate_program_packs(packs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Validate Pack publication fields before a Pack may be routed."""

    packs = packs if packs is not None else _load_unvalidated_packs()
    allowed_rule_ids = _allowed_rule_ids()
    ids: set[str] = set()
    errors: list[str] = []
    for pack in packs:
        pack_id = str(pack.get("id", ""))
        missing = sorted(_REQUIRED_FIELDS - set(pack))
        if missing:
            errors.append(f"{pack_id or '<missing id>'}: missing {', '.join(missing)}")
        if not pack_id:
            continue
        if pack_id in ids:
            errors.append(f"duplicate program pack id: {pack_id}")
        ids.add(pack_id)
        applicability = pack.get("applicability", {})
        if not isinstance(applicability, dict) or not applicability.get("goals"):
            errors.append(f"{pack_id}: applicability.goals is required")
        if pack.get("automation_level") not in {"self_service", "assessment_only"}:
            errors.append(f"{pack_id}: unsupported automation_level")
        if pack.get("release_status") not in {"released", "released_limited", "assessment_only"}:
            errors.append(f"{pack_id}: unsupported release_status")
        if pack.get("automation_level") == "self_service" and not pack.get("rule_ids"):
            errors.append(f"{pack_id}: self-service Pack requires rule_ids")
        unknown_rule_ids = sorted(set(pack.get("rule_ids", [])) - allowed_rule_ids)
        if unknown_rule_ids:
            errors.append(f"{pack_id}: rule_ids are missing or not allowed_ui: {', '.join(unknown_rule_ids)}")
        if not isinstance(pack.get("withdrawal_switch"), bool):
            errors.append(f"{pack_id}: withdrawal_switch must be boolean")
    if errors:
        raise ValueError("Invalid Program Pack registry: " + "; ".join(errors))
    return {"valid": True, "pack_count": len(packs), "pack_ids": sorted(ids)}


def get_program_pack(pack_id: str) -> dict[str, Any] | None:
    """Return one Pack without exposing the mutable registry object."""

    for pack in load_program_packs():
        if pack["id"] == pack_id:
            return deepcopy(pack)
    return None


def resolve_program_pack(profile: dict[str, Any]) -> dict[str, Any]:
    """Match a current scenario to a Pack or a non-automated collaboration route."""

    age = int(profile.get("age", 0) or 0)
    goal = _GOAL_ALIASES.get(str(profile.get("goal", "")), "build_activity_habit")
    safety_signals = _has_scope_or_safety_signal(profile, age)
    used_inputs = ["age", "goal", "symptoms", "known_conditions", "pregnant"]

    if safety_signals:
        return {
            "route": "professional_collaboration",
            "automation_allowed": False,
            "pack": None,
            "goal": goal,
            "used_inputs": used_inputs,
            "not_measured": ["performance tests", "device data"],
            "reason": "当前场景不进入自助自动处方；需要由外部专业流程确认下一步。",
            "limitations": ["这不是医疗诊断、医疗清除或治疗建议。"],
        }

    pack = next(
        (item for item in load_program_packs() if goal in item["applicability"]["goals"]),
        get_program_pack("low_activity_aerobic_v1"),
    )
    if pack is None:
        raise RuntimeError("The Program Pack registry has no fallback Pack.")
    automation_allowed = pack["automation_level"] == "self_service" and pack["release_status"] in {
        "released",
        "released_limited",
    }
    route = "self_service" if automation_allowed else "assessment_only"
    return {
        "route": route,
        "automation_allowed": automation_allowed,
        "pack": deepcopy(pack),
        "goal": goal,
        "used_inputs": used_inputs + list(pack["required_inputs"]),
        "not_measured": ["performance tests", "device data"],
        "reason": (
            "当前方案已发布，可在其明确边界内生成有氧起点。"
            if automation_allowed
            else "当前方案只开放评估与记录准备，尚未开放自动训练剂量。"
        ),
        "limitations": list(pack["limitations"]),
    }


def _load_unvalidated_packs() -> list[dict[str, Any]]:
    packs: list[dict[str, Any]] = []
    for path in sorted(PACK_DIRECTORY.glob("*.json")):
        with path.open(encoding="utf-8") as handle:
            packs.append(json.load(handle))
    return packs


def _allowed_rule_ids() -> set[str]:
    with RULE_RECORD_PATH.open(encoding="utf-8") as handle:
        records = json.load(handle).get("records", [])
    return {str(record["id"]) for record in records if record.get("product_status") == "allowed_ui"}


def _has_scope_or_safety_signal(profile: dict[str, Any], age: int) -> bool:
    if age < 18 or age > 64 or profile.get("pregnant") is True:
        return True
    symptoms = profile.get("symptoms") or []
    conditions = profile.get("known_conditions") or []
    return bool(symptoms or conditions)
