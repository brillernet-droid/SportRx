from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DOCS = [
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "docs/zh-CN/quickstart.md",
    ROOT / "docs/zh-CN/product-guide.md",
    ROOT / "docs/zh-CN/claim-boundaries.md",
    ROOT / "docs/zh-CN/terminology.md",
    ROOT / "docs/zh-CN/venue-entry.md",
    ROOT / "docs/zh-CN/public-preview.md",
]
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _local_targets(document: Path) -> list[Path]:
    targets = []
    for target in MARKDOWN_LINK.findall(document.read_text(encoding="utf-8")):
        target = target.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        targets.append((document.parent / target).resolve())
    return targets


def test_chinese_readme_leads_with_product_value_and_trial_path():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert readme.startswith("# SportRX")
    assert "一次标准化测量，形成可解释训练起点，并用复测证明变化。" in readme
    assert "测得准，开得稳，讲得清，能复测。" in readme
    assert "外部筛查路径 → Safety Gate → Hybrid Benchmark → Training Profile → Starter Path → RPE / Completion → Retest" in readme
    assert "python3 -m pip install -e \".[dev,app]\"" in readme
    assert "docs/zh-CN/quickstart.md" in readme


def test_public_docs_have_valid_local_links_and_no_internal_references():
    forbidden_fragments = ("docs/internal/", "/Users/", ".tmp_sportrx_bp", ".codex/")

    for document in PUBLIC_DOCS:
        content = document.read_text(encoding="utf-8")
        assert not any(fragment in content for fragment in forbidden_fragments), document
        for target in _local_targets(document):
            assert target.exists(), f"{document.relative_to(ROOT)} links to missing {target}"


def test_public_docs_keep_ai_and_validation_claims_bounded():
    content = "\n".join(document.read_text(encoding="utf-8") for document in PUBLIC_DOCS)

    assert "AI 自动处方" in content
    assert "不提供疾病诊断" in content
    assert "完赛概率" in content
    assert "正式验证" in content
    assert "research_required" in content
    assert "合成数据示例站" in content
