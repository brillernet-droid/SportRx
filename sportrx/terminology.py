"""Terminology guide for SportRX language editions.

This module standardizes product language only. It does not create or validate
any sport-science rule.
"""

from __future__ import annotations

from typing import Any

from .language_editions import ALLOWED_SHARED_TERMS, LANGUAGE_EDITIONS


CLAIM_BOUNDARY = (
    "Terminology Guide standardizes SportRX product language only. It does not "
    "validate SportRX, score performance, create athlete norms, predict outcomes, "
    "or provide medical clearance."
)


TERMS = [
    {
        "term": "HYROX",
        "display": "HYROX",
        "zh_explanation": "保留英文。用于描述混合耐力/功能性体能赛事语境；SportRX 当前只做 HYROX-style benchmark，不声称官方认证或赛事完赛预测。",
        "use_in_ui": "Event context, benchmark naming, user-facing examples.",
        "do_not_say": "官方 HYROX readiness、完赛概率、官方赛事认证。",
    },
    {
        "term": "RPE",
        "display": "RPE",
        "zh_explanation": "保留英文。主观用力程度，SportRX 使用 0-10 记录训练或测试后的体感强度。",
        "use_in_ui": "Benchmark Log, Feedback Loop, Starter Path review.",
        "do_not_say": "把 RPE 当成客观生理负荷或医疗指标。",
    },
    {
        "term": "Benchmark",
        "display": "Benchmark",
        "zh_explanation": "保留英文。指可复测的测试记录，重点是 protocol、原始数值、单位、RPE、器械和日期。",
        "use_in_ui": "SportRX Hybrid Benchmark v1, Benchmark Log, retest review.",
        "do_not_say": "人群百分位、已验证等级、运动员标准。",
    },
    {
        "term": "Not tested",
        "display": "Not tested",
        "zh_explanation": "保留英文短语。表示该测试未完成，不用平均值、中位数或默认值填补。",
        "use_in_ui": "HYROX Check, Measurement Intake Matrix, exports.",
        "do_not_say": "用默认分、平均表现、假设值替代缺失测试。",
    },
    {
        "term": "Measured",
        "display": "Measured",
        "zh_explanation": "保留英文。表示有可追溯的原始结果、单位、日期或 protocol context。",
        "use_in_ui": "Measured picture, strongest area, main gap comparison.",
        "do_not_say": "没有原始数值时说已实测。",
    },
    {
        "term": "Safety Gate",
        "display": "Safety Gate",
        "zh_explanation": "保留英文。只负责训练交接安全边界；可以阻断建议，但不提高或降低 measured performance。",
        "use_in_ui": "Workbench, Quick Match, Training Profile, Release QA.",
        "do_not_say": "医学诊断、医疗许可、风险百分比。",
    },
    {
        "term": "Training Profile",
        "display": "Training Profile",
        "zh_explanation": "保留英文。表示当前训练画像和 measured picture，不等于运动员类型或正式能力等级。",
        "use_in_ui": "Training Profile report and handoff sections.",
        "do_not_say": "athlete type、validated level、readiness score。",
    },
    {
        "term": "Starter Path",
        "display": "Starter Path",
        "zh_explanation": "保留英文。表示在安全门和实测数据满足后生成的保守 4-week training handoff。",
        "use_in_ui": "Training page and Training Block export.",
        "do_not_say": "治疗方案、保证提升、赛事备赛完整周期。",
    },
    {
        "term": "Current measured picture",
        "display": "current measured picture",
        "zh_explanation": "优先使用。表示当前已经实测和仍未测试的组合，而不是 readiness 或综合能力评分。",
        "use_in_ui": "Workbench hero, Training Profile, report summaries.",
        "do_not_say": "validated readiness、综合运动能力分。",
    },
    {
        "term": "Release QA",
        "display": "Release QA",
        "zh_explanation": "保留英文。只检查本地产品完整性、导出物和 claim boundary，不代表科学验证。",
        "use_in_ui": "Release QA page, public package checks.",
        "do_not_say": "validation passed、科学验证完成。",
    },
]


PREFERRED_LANGUAGE_RULES = [
    "Choose one language edition for normal users: Chinese user edition or English Lab Edition.",
    "Internal Mixed Review is allowed only for development, QA, and reviewer handoff.",
    "HYROX, RPE, Benchmark, Safety Gate, Training Profile, Starter Path, and Release QA may stay stable across editions as shared product terms.",
    "Use current measured picture / training profile / strongest area / what needs work instead of readiness score until formal validation exists.",
    "Use Not tested for missing performance data; do not fill missing tests with average, midpoint, or default scores.",
    "Safety Gate can block training handoff, but it must not alter measured performance scoring or gap comparison.",
    "FITT-VP is a conservative training handoff layer, not the full product identity.",
    "Release QA and Public Beta Readiness are product-readiness checks, not scientific validation.",
]


BLOCKED_LANGUAGE = [
    {
        "phrase": "readiness score",
        "reason": "Formal validation does not exist; use current measured picture instead.",
    },
    {
        "phrase": "risk percentage",
        "reason": "SportRX does not estimate medical, injury, or event-risk percentages.",
    },
    {
        "phrase": "medical clearance",
        "reason": "Safety Gate is a product boundary, not clinical clearance.",
    },
    {
        "phrase": "validated performance",
        "reason": "SportRX is still a prototype without formal validation data.",
    },
    {
        "phrase": "athlete norm",
        "reason": "No real athlete benchmark dataset or percentile model exists yet.",
    },
    {
        "phrase": "AI coach",
        "reason": "SportRX is positioned as measurement and prescription intelligence, not a chat coach.",
    },
    {
        "phrase": "official HYROX readiness",
        "reason": "SportRX is not affiliated with or certified by HYROX.",
    },
]


def build_terminology_guide() -> dict[str, Any]:
    """Build the product-language contract used by UI and exports."""

    retained_english = [item["display"] for item in TERMS if item["display"][0].isascii()]
    return {
        "schema": "sportrx.terminology_guide",
        "schema_version": "0.1",
        "status": "ready_for_language_edition_review",
        "language_edition_count": len(LANGUAGE_EDITIONS),
        "user_facing_language_editions": [item["id"] for item in LANGUAGE_EDITIONS if item["user_facing"]],
        "internal_language_editions": [item["id"] for item in LANGUAGE_EDITIONS if not item["user_facing"]],
        "term_count": len(TERMS),
        "blocked_phrase_count": len(BLOCKED_LANGUAGE),
        "rule_count": len(PREFERRED_LANGUAGE_RULES),
        "retained_english_terms": retained_english,
        "allowed_shared_terms": ALLOWED_SHARED_TERMS,
        "terms": TERMS,
        "preferred_language_rules": PREFERRED_LANGUAGE_RULES,
        "blocked_language": BLOCKED_LANGUAGE,
        "primary_message": "SportRX separates Chinese, English, and internal mixed-language editions while keeping shared sport-science terms stable.",
        "next_action": "Use this guide when editing UI copy, README text, export labels, reviewer handoff, and public beta notes.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def terminology_markdown(guide: dict[str, Any]) -> str:
    """Export the terminology guide as Markdown."""

    lines = [
        "# SportRX Terminology Guide",
        "",
        f"- Status: {guide['status']}",
        f"- Terms: {guide['term_count']}",
        f"- Preferred language rules: {guide['rule_count']}",
        f"- Blocked phrases: {guide['blocked_phrase_count']}",
        f"- Language editions: {guide['language_edition_count']}",
        f"- Claim boundary: {guide['claim_boundary']}",
        "",
        "## Product Language Position",
        "",
        guide["primary_message"],
        "",
        "## Preferred Language Rules",
    ]
    for rule in guide["preferred_language_rules"]:
        lines.append(f"- {rule}")
    lines.extend(["", "## Terms"])
    for item in guide["terms"]:
        lines.extend(
            [
                "",
                f"### {item['display']}",
                "",
                f"- Chinese explanation: {item['zh_explanation']}",
                f"- Use in UI: {item['use_in_ui']}",
                f"- Do not say: {item['do_not_say']}",
            ]
        )
    lines.extend(["", "## Blocked Language"])
    for item in guide["blocked_language"]:
        lines.append(f"- `{item['phrase']}` - {item['reason']}")
    lines.extend(["", "## Next Action", "", guide["next_action"]])
    return "\n".join(lines) + "\n"
