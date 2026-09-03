import json
import shutil
from pathlib import Path

from sportrx.knowledge_rag import (
    build_knowledge_index,
    evaluate_knowledge_boundary_set,
    evaluate_knowledge_equivalence_set,
    evaluate_knowledge_retrieval_set,
    ingest_candidates,
    knowledge_corpus_summary,
    knowledge_evaluation_status,
    review_knowledge_card,
    search_knowledge,
    synthesize_knowledge,
    validate_knowledge_records,
)


ROOT = Path(__file__).resolve().parents[1]


def test_reviewed_knowledge_cards_validate_but_do_not_overstate_v1_readiness():
    validation = validate_knowledge_records(ROOT)
    summary = knowledge_corpus_summary(ROOT)

    assert validation["valid"]
    assert validation["reviewed_card_count"] == 96
    assert summary["status"] == "foundation_in_progress"
    assert summary["synthesis_enabled"] is False
    assert "sports_medicine_injury_rehab" in validation["covered_topics"]
    assert "does not make medical diagnoses" in validation["claim_boundary"]


def test_search_returns_reviewed_bilingual_card_and_excludes_candidates(tmp_path):
    result = search_knowledge("六分钟跑 测试", root=ROOT)
    index = build_knowledge_index(ROOT, tmp_path / "knowledge.sqlite")

    assert result["status"] == "ready"
    assert result["results"][0]["id"] == "K-CARD-026"
    assert "Six-minute" in result["results"][0]["title_en"]
    assert result["results"][0]["sources"][0]["stable_url"].startswith("https://")
    assert index["document_count"] == 96


def test_search_retrieves_reviewed_hypertrophy_movement_knowledge():
    shoulders = search_knowledge("肩部 动作模式", root=ROOT)
    equipment = search_knowledge("自由重量 器械 增肌", root=ROOT)

    assert shoulders["results"][0]["id"] == "K-CARD-061"
    assert "K-CARD-071" in {item["id"] for item in shoulders["results"][:3]}
    assert equipment["results"][0]["id"] == "K-CARD-064"
    assert equipment["results"][0]["sources"][0]["stable_url"].startswith("https://")


def test_validator_rejects_private_path_or_unknown_source(tmp_path):
    shutil.copytree(ROOT / "evidence", tmp_path / "evidence")
    cards_path = tmp_path / "evidence/knowledge/cards.json"
    payload = json.loads(cards_path.read_text(encoding="utf-8"))
    payload["records"][0]["source_ids"] = ["NOT-A-SOURCE"]
    payload["records"][0]["limitations"] = "See evidence/private/licensed.pdf"
    cards_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    validation = validate_knowledge_records(tmp_path)

    assert not validation["valid"]
    assert any("unknown source" in error for error in validation["errors"])
    assert any("private path" in error for error in validation["errors"])


def test_candidate_intake_deduplicates_and_never_promotes_to_reviewed():
    intake = ingest_candidates(
        [
            {"id": "C-1", "title": "Example endurance review", "doi": "10.1000/example", "topic": "endurance"},
            {"id": "C-2", "title": "Example endurance review", "doi": "10.1000/example", "topic": "endurance"},
        ],
        ROOT,
    )

    assert intake["status"] == "review_required"
    assert len(intake["candidates"]) == 1
    assert intake["candidates"][0]["review_status"] == "candidate"
    assert intake["duplicate_ids"] == ["C-2"]


def test_review_operation_is_explicit_and_does_not_touch_product_rules():
    cards = [{"id": "K-TEST", "review_status": "candidate"}]
    review = review_knowledge_card(cards, "K-TEST", "reviewed", "Reviewer", "2026-08-28")

    assert review["status"] == "review_recorded"
    assert review["cards"][0]["review_status"] == "reviewed"
    assert "cannot change SportRX product rules" in review["claim_boundary"]


def test_synthesis_stays_disabled_until_answer_quality_gate_passes():
    result = synthesize_knowledge("什么是 RPE？", ["K-CARD-015"], ROOT)

    assert result["status"] == "evaluation_not_ready"
    assert "暂不生成" in result["answer_zh"]


def test_retrieval_and_boundary_fixtures_pass_but_do_not_enable_synthesis():
    retrieval = evaluate_knowledge_retrieval_set(ROOT)
    boundary = evaluate_knowledge_boundary_set(ROOT)
    equivalence = evaluate_knowledge_equivalence_set(ROOT)
    status = knowledge_evaluation_status(ROOT)

    assert retrieval["status"] == "passed"
    assert retrieval["query_count"] >= 150
    assert boundary["status"] == "passed"
    assert boundary["query_count"] >= 50
    assert equivalence["status"] == "passed"
    assert equivalence["query_count"] >= 30
    assert status["answer_quality_passed_count"] == 0
    assert status["synthesis_gate_passed"] is False
