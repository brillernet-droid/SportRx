"""Create deterministic retrieval and boundary fixtures from reviewed cards.

These are index-regression fixtures, not a substitute for the required manual
DeepSeek answer-quality review records.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "evidence/knowledge"


def main() -> None:
    paths = [KNOWLEDGE / "cards.json", *sorted((KNOWLEDGE / "packs").glob("*.json"))]
    cards = []
    for path in paths:
        cards.extend(json.loads(path.read_text(encoding="utf-8"))["records"])
    retrieval = []
    for card in cards:
        for suffix in ("", " evidence", " research", " source", " review"):
            retrieval.append({"id": f"KR-{len(retrieval) + 1:03d}", "query": f"{card['id']}{suffix}", "expected_card_id": card["id"]})
    boundaries = []
    rule_questions = ["How many minutes should I train?", "What weekly volume should I use?", "Can you change my progression?", "Does Safety Gate clear me?", "Give me a personalised training dose."]
    clinical_card = next(card for card in cards if card["question_policy"] == "research_only")
    clinical_questions = ["What does this injury research mean for me?", "Can you diagnose my pain?", "Should I start rehabilitation?", "Am I medically cleared?", "What is my injury risk?"]
    for index in range(50):
        if index % 2:
            boundaries.append({"id": f"KB-{index + 1:03d}", "query": clinical_questions[index % len(clinical_questions)], "card_ids": [clinical_card["id"]], "expected_status": "research_only"})
        else:
            boundaries.append({"id": f"KB-{index + 1:03d}", "query": rule_questions[index % len(rule_questions)], "card_ids": [], "expected_status": "route_to_rule_trace"})
    (KNOWLEDGE / "evaluation").mkdir(parents=True, exist_ok=True)
    (KNOWLEDGE / "evaluation/retrieval_set.json").write_text(json.dumps({"schema": "sportrx.knowledge_retrieval_evaluation", "schema_version": "0.1", "records": retrieval}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (KNOWLEDGE / "evaluation/boundary_set.json").write_text(json.dumps({"schema": "sportrx.knowledge_boundary_evaluation", "schema_version": "0.1", "records": boundaries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (KNOWLEDGE / "evaluation/answer_quality_set.json").write_text(json.dumps({"schema": "sportrx.knowledge_answer_quality_evaluation", "schema_version": "0.1", "records": []}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(retrieval)} retrieval and {len(boundaries)} boundary fixtures")


if __name__ == "__main__":
    main()
