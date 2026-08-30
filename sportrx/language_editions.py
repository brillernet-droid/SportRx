"""Language edition contract for SportRX.

The contract separates user-facing language versions from the internal mixed
review surface. It governs product copy only; it does not affect measurement,
scoring, safety, or prescription rules.
"""

from __future__ import annotations

from typing import Any


CLAIM_BOUNDARY = (
    "Language editions govern user-facing product copy only. They do not change "
    "Safety Gate decisions, measured performance values, training handoff rules, "
    "or validation status."
)


ALLOWED_SHARED_TERMS = [
    "SportRX",
    "HYROX",
    "RPE",
    "Benchmark",
    "Safety Gate",
    "Training Profile",
    "Starter Path",
    "Release QA",
    "RowErg",
    "SkiErg",
]


LANGUAGE_EDITIONS = [
    {
        "id": "zh_user",
        "label": "中文版",
        "short_label": "中文",
        "interface_language": "zh-CN",
        "status": "primary_user_edition",
        "user_facing": True,
        "description": "面向早期试用者的中文用户版；除专有名词外，按钮、说明和页面标题应使用中文。",
        "copy_rule": "中文句子不夹英文解释；只保留 SportRX、HYROX、RPE、Benchmark 等专有术语。",
        "review_rule": "任何新增中文界面文案都必须先判断是否可以完整中文表达。",
    },
    {
        "id": "en_user",
        "label": "English Lab Edition",
        "short_label": "English",
        "interface_language": "en-US",
        "status": "user_edition_copy_audit_required",
        "user_facing": True,
        "description": "English user-facing lab edition. Normal controls, page titles, and explanations should be written in English.",
        "copy_rule": "English screens should not contain Chinese helper text, Chinese button labels, or mixed-language sentences.",
        "review_rule": "Before public English testing, run a copy audit on every visible page and export label.",
    },
    {
        "id": "internal_mixed",
        "label": "Internal Mixed Review",
        "short_label": "Internal",
        "interface_language": "mixed",
        "status": "internal_only",
        "user_facing": False,
        "description": "内部开发和审阅用混合语言界面；不能作为正常用户体验版本。",
        "copy_rule": "允许中英文混合用于开发审阅，但必须明确标记为 internal-only。",
        "review_rule": "混合语言只能用于内部 QA、代码审阅和导出物检查。",
    },
]


PAGE_LABELS = {
    "Venue Entry": {
        "zh_user": "入会分流",
        "en_user": "Venue Entry",
        "internal_mixed": "Venue Entry",
    },
    "Workbench": {
        "zh_user": "工作台",
        "en_user": "Workbench",
        "internal_mixed": "Workbench",
    },
    "Quick Match": {
        "zh_user": "快速匹配",
        "en_user": "Quick Match",
        "internal_mixed": "Quick Match",
    },
    "HYROX Check": {
        "zh_user": "HYROX 检查",
        "en_user": "HYROX Check",
        "internal_mixed": "HYROX Check",
    },
    "Benchmark Protocol": {
        "zh_user": "Benchmark 流程",
        "en_user": "Benchmark Protocol",
        "internal_mixed": "Benchmark Protocol",
    },
    "Benchmark Log": {
        "zh_user": "Benchmark 记录",
        "en_user": "Benchmark Log",
        "internal_mixed": "Benchmark Log",
    },
    "Training Profile": {
        "zh_user": "训练画像",
        "en_user": "Training Profile",
        "internal_mixed": "Training Profile",
    },
    "训练": {
        "zh_user": "训练",
        "en_user": "Training",
        "internal_mixed": "训练",
    },
    "复测": {
        "zh_user": "复测",
        "en_user": "Retest",
        "internal_mixed": "复测",
    },
    "Pilot Feedback": {
        "zh_user": "试用反馈",
        "en_user": "Pilot Feedback",
        "internal_mixed": "Pilot Feedback",
    },
    "Evidence Library": {
        "zh_user": "循证库",
        "en_user": "Evidence Library",
        "internal_mixed": "Evidence Library",
    },
    "Knowledge Lab": {
        "zh_user": "知识实验室",
        "en_user": "Knowledge Lab",
        "internal_mixed": "Knowledge Lab",
    },
    "Export Center": {
        "zh_user": "导出中心",
        "en_user": "Export Center",
        "internal_mixed": "Export Center",
    },
    "Release QA": {
        "zh_user": "发布 QA",
        "en_user": "Release QA",
        "internal_mixed": "Release QA",
    },
}


UI_TEXT = {
    "sidebar_caption": {
        "zh_user": "中文版用户界面；保留少量专有术语。",
        "en_user": "English user interface; shared product terms stay stable.",
        "internal_mixed": "Internal mixed-language review surface.",
    },
    "language_selector": {
        "zh_user": "语言版本",
        "en_user": "Language edition",
        "internal_mixed": "Language edition",
    },
    "language_policy_title": {
        "zh_user": "语言边界",
        "en_user": "Language Boundary",
        "internal_mixed": "Language Boundary",
    },
    "language_policy_caption": {
        "zh_user": "中文版和英文版面向用户；Internal Mixed 只用于内部审阅。",
        "en_user": "Chinese and English editions are user-facing; Internal Mixed is review-only.",
        "internal_mixed": "Mixed language is allowed here only because this is an internal review edition.",
    },
    "demo_controls": {
        "zh_user": "示例控制",
        "en_user": "Demo Controls",
        "internal_mixed": "Demo controls",
    },
    "load_complete_demo": {
        "zh_user": "加载完整示例",
        "en_user": "Load Complete Demo",
        "internal_mixed": "加载完整示例",
    },
    "demo_scenario": {
        "zh_user": "示例场景",
        "en_user": "Demo Scenario",
        "internal_mixed": "Demo scenario",
    },
    "load_selected_scenario": {
        "zh_user": "加载所选场景",
        "en_user": "Load Selected Scenario",
        "internal_mixed": "加载所选场景",
    },
    "reset_prototype": {
        "zh_user": "重置原型",
        "en_user": "Reset Prototype",
        "internal_mixed": "重置原型",
    },
    "session_snapshot": {
        "zh_user": "会话快照",
        "en_user": "Session Snapshot",
        "internal_mixed": "Session snapshot",
    },
    "download_snapshot_json": {
        "zh_user": "下载会话快照",
        "en_user": "Download Session Snapshot",
        "internal_mixed": "下载 Session Snapshot",
    },
    "download_snapshot_summary": {
        "zh_user": "下载快照摘要",
        "en_user": "Download Snapshot Summary",
        "internal_mixed": "下载 Snapshot Summary",
    },
    "import_snapshot": {
        "zh_user": "导入快照 JSON",
        "en_user": "Import Snapshot JSON",
        "internal_mixed": "导入 Snapshot JSON",
    },
    "restore_snapshot": {
        "zh_user": "恢复快照",
        "en_user": "Restore Snapshot",
        "internal_mixed": "恢复 Snapshot",
    },
    "snapshot_restored": {
        "zh_user": "会话快照已恢复。",
        "en_user": "Session Snapshot restored.",
        "internal_mixed": "Session Snapshot 已恢复。",
    },
    "snapshot_import_failed": {
        "zh_user": "快照无法导入",
        "en_user": "Snapshot import failed",
        "internal_mixed": "Snapshot 无法导入",
    },
    "navigation": {
        "zh_user": "导航",
        "en_user": "Navigation",
        "internal_mixed": "导航",
    },
    "public_measurement_scope_caption": {
        "zh_user": "当前手机版展示完整测试流程；详细原始记录与导出暂不在此试用路径开放。",
        "en_user": "This mobile path shows the full test flow; detailed raw records and exports are not part of this trial path.",
        "internal_mixed": "Detailed raw records and exports are available in the internal review surface.",
    },
}


def get_language_edition(edition_id: str | None = None) -> dict[str, Any]:
    """Return a language edition by id, defaulting to Chinese user edition."""

    target = edition_id or "zh_user"
    return next((item for item in LANGUAGE_EDITIONS if item["id"] == target), LANGUAGE_EDITIONS[0])


def language_edition_options(include_internal: bool = True) -> list[str]:
    """Return selectable edition ids, excluding internal review when requested."""

    return [
        item["id"]
        for item in LANGUAGE_EDITIONS
        if include_internal or item["user_facing"]
    ]


def language_edition_label(edition_id: str | None = None) -> str:
    """Return the selector label for a language edition."""

    return str(get_language_edition(edition_id)["label"])


def page_label(page_id: str, edition_id: str | None = None) -> str:
    """Return a page label for the selected edition."""

    edition = get_language_edition(edition_id)["id"]
    return PAGE_LABELS.get(page_id, {}).get(edition, page_id)


def ui_text(key: str, edition_id: str | None = None) -> str:
    """Return a UI string for the selected edition."""

    edition = get_language_edition(edition_id)["id"]
    return UI_TEXT.get(key, {}).get(edition, key)


def build_language_edition_contract(current_edition_id: str | None = None) -> dict[str, Any]:
    """Build the language-version contract shown in the UI and exports."""

    current = get_language_edition(current_edition_id)
    user_facing = [item for item in LANGUAGE_EDITIONS if item["user_facing"]]
    internal = [item for item in LANGUAGE_EDITIONS if not item["user_facing"]]
    return {
        "schema": "sportrx.language_edition_contract",
        "schema_version": "0.1",
        "status": "active",
        "current_edition": current,
        "edition_count": len(LANGUAGE_EDITIONS),
        "user_facing_count": len(user_facing),
        "internal_count": len(internal),
        "allowed_shared_terms": ALLOWED_SHARED_TERMS,
        "page_labels": {
            page_id: {
                edition["id"]: page_label(page_id, edition["id"])
                for edition in LANGUAGE_EDITIONS
            }
            for page_id in PAGE_LABELS
        },
        "primary_message": "SportRX separates Chinese, English, and internal mixed-language editions before public testing.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def language_edition_markdown(contract: dict[str, Any]) -> str:
    """Export the language edition contract as Markdown."""

    lines = [
        "# SportRX Language Edition Contract",
        "",
        f"- Status: {contract['status']}",
        f"- Editions: {contract['edition_count']}",
        f"- User-facing editions: {contract['user_facing_count']}",
        f"- Internal editions: {contract['internal_count']}",
        f"- Claim boundary: {contract['claim_boundary']}",
        "",
        "## Current Edition",
        "",
        f"- ID: `{contract['current_edition']['id']}`",
        f"- Label: {contract['current_edition']['label']}",
        f"- Interface language: {contract['current_edition']['interface_language']}",
        f"- Status: {contract['current_edition']['status']}",
        f"- Copy rule: {contract['current_edition']['copy_rule']}",
        "",
        "## Allowed Shared Terms",
    ]
    for term in contract["allowed_shared_terms"]:
        lines.append(f"- {term}")
    lines.extend(["", "## Page Labels"])
    for page_id, labels in contract["page_labels"].items():
        lines.append(
            f"- `{page_id}`: 中文 `{labels['zh_user']}` / English `{labels['en_user']}` / Internal `{labels['internal_mixed']}`"
        )
    return "\n".join(lines) + "\n"
