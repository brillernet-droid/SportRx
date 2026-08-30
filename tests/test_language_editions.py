from sportrx.language_editions import (
    build_language_edition_contract,
    language_edition_label,
    language_edition_markdown,
    language_edition_options,
    page_label,
    ui_text,
)


def test_language_editions_define_user_and_internal_versions():
    contract = build_language_edition_contract("zh_user")

    assert contract["schema"] == "sportrx.language_edition_contract"
    assert contract["edition_count"] == 3
    assert contract["user_facing_count"] == 2
    assert contract["internal_count"] == 1
    assert contract["current_edition"]["id"] == "zh_user"
    assert "HYROX" in contract["allowed_shared_terms"]
    assert "do not change Safety Gate" in contract["claim_boundary"]


def test_language_edition_page_labels_stay_separate():
    assert page_label("Workbench", "zh_user") == "工作台"
    assert page_label("Workbench", "en_user") == "Workbench"
    assert page_label("Training Profile", "zh_user") == "训练画像"
    assert page_label("Venue Entry", "zh_user") == "测试前确认"
    assert page_label("Venue Entry", "en_user") == "Venue Entry"
    assert page_label("训练", "en_user") == "Training"
    assert page_label("复测", "en_user") == "Retest"


def test_language_edition_selector_and_ui_text_are_localized():
    options = language_edition_options()

    assert options == ["zh_user", "en_user", "internal_mixed"]
    assert language_edition_options(include_internal=False) == ["zh_user", "en_user"]
    assert language_edition_label("zh_user") == "中文版"
    assert language_edition_label("en_user") == "English Lab Edition"
    assert ui_text("navigation", "zh_user") == "导航"
    assert ui_text("navigation", "en_user") == "Navigation"


def test_language_edition_markdown_exports_boundaries_and_labels():
    markdown = language_edition_markdown(build_language_edition_contract("en_user"))

    assert "# SportRX Language Edition Contract" in markdown
    assert "English Lab Edition" in markdown
    assert "Internal Mixed Review" not in markdown
    assert "Allowed Shared Terms" in markdown
    assert "`Training Profile`: 中文 `训练画像` / English `Training Profile`" in markdown


def test_chinese_user_copy_does_not_send_people_to_internal_review():
    chinese_scope_copy = ui_text("public_measurement_scope_caption", "zh_user")

    assert "Internal Mixed Review" not in chinese_scope_copy
    assert "内部" not in chinese_scope_copy
    assert "详细原始记录" in chinese_scope_copy
    assert ui_text("public_measurement_scope_caption", "en_user").startswith("This mobile path")
