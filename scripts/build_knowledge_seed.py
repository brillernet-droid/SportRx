"""Build the reviewed Knowledge RAG foundation from existing reviewed sources.

This is a one-way seed generator. It creates concise educational cards only;
it does not download papers, infer new findings, or promote discovery results.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence/knowledge/cards.json"


SPECS = [
    ("PA-WHO-2020", "training_principles", "physical_activity", "身体活动指南如何用于训练语境", "Physical activity guidance as training context", "身体活动指南可提供总体健康活动背景，但不能替代个人表现测试或赛事准备判断。", "Public-health activity guidance is contextual, not a performance or event-readiness threshold."),
    ("PA-CDC-ADULT", "training_principles", "adult_activity", "成年人身体活动建议的边界", "Adult activity guidance boundaries", "成年人活动建议适合用于理解一般健康活动量，不应用来给个人贴上运动能力标签。", "Population guidance does not determine an individual's sport performance or dose."),
    ("PA-ACSM-GETP12", "training_principles", "fitt_vp", "FITT-VP 是什么", "FITT-VP framework", "FITT-VP 用频率、强度、时间、类型、总量与进阶组织训练思路；在 SportRX 中它仍需受 Safety Gate 和实际测量约束。", "FITT-VP is a prescription framework, not validation of a SportRX-specific outcome."),
    ("PA-ACSM-CDC", "training_principles", "activity_context", "为什么活动建议不是能力评分", "Why activity guidance is not a fitness score", "满足一般活动建议不等于已具备 HYROX、跑步或其他赛事能力。", "Public-health guidance is not a validated readiness score."),
    ("PA-AHA", "training_principles", "cardiovascular_context", "心血管健康建议与运动表现的区别", "Cardiovascular guidance versus performance", "面向心血管健康的活动建议可以解释健康背景，但不预测个人比赛表现。", "Health recommendations cannot be converted into race predictions."),
    ("PA-CHINA-2021", "training_principles", "china_local_context", "中国身体活动指南如何在 SportRX 中使用", "Chinese physical activity guidance context", "中国人群身体活动指南在 SportRX 中只提供成年人的健康活动语境，不用于生成官方体质等级。", "No Chinese national grade, norm, or composite score is mapped into SportRX."),
    ("SAFE-EIM", "sports_medicine_injury_rehab", "preparticipation_screening", "运动前筛查为什么独立于表现", "Why screening is separate from performance", "运动前筛查用于决定是否需要进一步专业评估；它不提高或降低任何已测表现。", "Research-only safety context; it is not medical clearance."),
    ("SAFE-EIM-SCREEN", "sports_medicine_injury_rehab", "screening_questionnaire", "筛查问卷能说明什么", "What screening questionnaires can and cannot show", "筛查问卷帮助识别是否需要暂停自动训练交接，但不能替代临床诊断或医疗许可。", "Research-only clinical boundary; no diagnostic interpretation is enabled."),
    ("SAFE-PARQ", "sports_medicine_injury_rehab", "readiness_screening", "PAR-Q 类工具的用途边界", "PAR-Q style tool boundary", "运动准备筛查工具用于提示进一步评估，不应用于判定个人医疗风险百分比。", "Research-only clinical context; no personal risk estimate is supported."),
    ("SAFE-ACSM-ALGO", "sports_medicine_injury_rehab", "screening_algorithm", "运动筛查算法不能变成自动医疗结论", "Screening algorithms are not automated clearance", "即使有筛查算法，SportRX 也只将其用于分流边界，而不输出医疗清除结论。", "The study population and clinical context do not validate automated SportRX clearance."),
    ("TEST-6MWT-ATS", "testing", "six_minute_protocol", "六分钟测试为什么需要固定流程", "Why six-minute tests require a fixed protocol", "六分钟测试的解释依赖固定流程和一致记录；SportRX 不把临床六分钟步行测试直接等同于跑步或跑走表现。", "Clinical walk-test guidance is not a HYROX or SportRX validation study."),
    ("TEST-FIELD-ADULT", "testing", "field_test_validity", "场地测试的效度问题", "Field-test validity", "场地测试需要明确自己测量的是什么，并区分“可记录”与“已经验证可解释”。", "The review does not validate the SportRX benchmark battery."),
    ("TEST-FIELD-SAFETY", "testing", "field_test_feasibility", "场地测试的可行性与安全性", "Field-test feasibility and safety", "场地测试应记录停止条件、偏离和完成情况；有限证据意味着产品需要自己的试用数据。", "This does not establish safety or reliability for every SportRX component."),
    ("TEST-FIELD-RELIABILITY", "testing", "retest_reliability", "为什么复测必须保持条件一致", "Why retest conditions must match", "复测时路线、设备、流程、单位和测试顺序变化，会削弱数值变化的解释意义。", "Reliability principles do not create a SportRX minimal meaningful-change threshold."),
    ("MON-RPE-ACSM", "monitoring_recovery", "rpe", "RPE 是什么", "Rating of perceived exertion", "RPE 是主观用力感，可帮助描述一次训练或测试有多难，但不能独立证明体能变化或安全。", "RPE is subjective and should not be used as an injury-risk estimate."),
    ("MON-SRPE-FOSTER", "monitoring_recovery", "session_rpe", "session-RPE 如何记录训练负荷", "Session-RPE for training monitoring", "session-RPE 将一次训练的主观强度与训练时长结合，用于回顾训练负荷，而不是预测伤病。", "Consistent timing and participant understanding are needed; it is not an injury-prediction method."),
    ("MON-SRPE-REVIEW", "monitoring_recovery", "monitoring_limits", "主观训练监测的局限", "Limits of subjective training monitoring", "主观训练监测应与完成情况、症状记录和复测一起看，不能单独成为训练剂量或恢复结论。", "Context sensitivity prevents session-RPE from independently validating physiological change."),
    ("HYROX-PHYS-2025", "hiit_hift_hybrid", "hyrox_physiology", "HYROX 生理研究目前能说明什么", "What early HYROX physiology research can show", "早期 HYROX 研究支持关注跑步、站点与工作能力，但不足以预测个人完赛、成绩或制定阈值。", "Early, sample-specific evidence cannot validate SportRX cutoffs or race prediction."),
    ("HIFT-HYBRID-REVIEW", "hiit_hift_hybrid", "hybrid_training", "混合赛事训练研究的边界", "Hybrid competition training evidence", "HIFT 与混合赛事文献可帮助理解训练组成，但不能直接变成某个人的保证性方案。", "Scoping or narrative evidence is not SportRX validation."),
    ("HIFT-DEFINITION", "hiit_hift_hybrid", "hif_definition", "HIFT 是什么", "What high-intensity functional training means", "HIFT 是广义训练概念，不等同于 HYROX，也不能自动生成赛事专项阈值。", "The definition is broader than any single hybrid event."),
    ("HIFT-FITNESS", "hiit_hift_hybrid", "hif_fitness", "HIFT 与体适能变化", "HIFT and physical fitness", "HIFT 干预研究可以提示多维体适能可能变化，但不同人群和训练方案差异较大。", "Intervention heterogeneity prevents individual outcome or event-readiness claims."),
    ("CONCURRENT-TRAINING", "strength_power", "concurrent_training", "力量与耐力并行训练", "Concurrent strength and endurance training", "力量与耐力并行训练是混合训练的重要背景，但不自动确定个人训练频率、顺序或总量。", "The review is not HYROX-specific and does not determine an individual dose."),
    ("INJ-CROSSFIT-SR", "sports_medicine_injury_rehab", "injury_research", "CrossFit 伤病文献如何谨慎阅读", "How to read CrossFit injury literature", "CrossFit 相关伤病研究的定义与报告不一，不能被转换为某个人的伤病风险百分比。", "CrossFit is not HYROX and heterogeneous estimates are not imported into SportRX."),
    ("INJ-HIFT-SR", "sports_medicine_injury_rehab", "injury_research", "HIFT 伤病研究如何谨慎阅读", "How to read HIFT injury literature", "HIFT 伤病研究可用于识别研究不确定性，但不支持对个人做概率化伤病预测。", "Definitions and reporting vary; this is research-only context."),
    ("TEST-1000M-ADULT-2000", "testing", "one_km_walk_run", "1,000 米测试的证据范围", "Evidence scope for a 1,000 m test", "成人 1,000 米 walk-run 研究可支持保留测试类型和复测条件；它不验证 SportRX 的硬跑条件、常模或评分。", "One healthy-adult walk-run study does not validate a SportRX hard-run score."),
    ("TEST-6MRT-ADULT-2023", "testing", "six_minute_run", "六分钟跑与跑走不可混同", "Six-minute running versus run/walk", "标准化六分钟跑研究不能自动覆盖自由跑走；SportRX 必须记录测试类型，且不能把六分钟距离换算成 1 km 时间。", "SportRX does not import reference equations or validate unrestricted run/walk."),
    ("ERG-SKIERG-1000M-2025", "testing", "skierg", "SkiErg 1 km 的个人复测价值", "SkiErg 1 km as a personal retest", "SkiErg 1 km 可作为同设备、同设置下的个人复测记录；不能据此给大众使用者生成常模。", "The study is a small national-level skier case study."),
    ("ERG-ROWERG-ACCURACY-2022", "testing", "rowerg_measurement", "RowErg 设备测量的注意点", "RowErg measurement context", "RowErg 设备研究提示起始划桨和不稳定划法会影响测量；应记录设备与测试条件，而不是夸大为人体表现验证。", "A motorized rig study is not human performance validation."),
    ("ERG-ROWERG-RELIABILITY-1999", "testing", "rowerg_retest", "RowErg 复测证据的适用范围", "RowErg retest evidence scope", "训练有素划船者的 2,000 米可靠性研究支持同条件复测思路，但不能直接代表 1,000 米大众测试。", "Distance and population differ from SportRX 1 km recreational use."),
    ("ERG-CONCEPT2-PM5", "testing", "erg_settings", "为什么记录 Erg 设置", "Why record ergometer settings", "设备型号和阻尼等设置有助于个人复测保持条件一致，但厂商资料不构成独立的表现验证或常模依据。", "Manufacturer documentation supports context capture only."),
    ("CN-NPFS-2023", "testing", "china_measurement_boundary", "中国体质测定标准与 SportRX 的边界", "China national measurement boundary", "中国本地官方材料可作为测量术语与方法边界参考；SportRX 不导入官方等级、综合评分或人群常模。", "SportRX Hybrid Benchmark differs in purpose and protocol from the national standard."),
]


TOPIC_KEYWORDS = {
    "training_principles": (["training principles", "FITT-VP", "physical activity"], ["训练原则", "身体活动", "运动处方"]),
    "strength_power": (["strength", "power", "concurrent training"], ["力量", "爆发力", "并行训练"]),
    "hiit_hift_hybrid": (["HIIT", "HIFT", "HYROX", "hybrid"], ["高强度功能训练", "混合赛事", "HYROX"]),
    "testing": (["testing", "retest", "field test", "ergometer"], ["测试", "复测", "场地测试", "测量"]),
    "monitoring_recovery": (["RPE", "session-RPE", "monitoring"], ["RPE", "主观用力感", "训练监测"]),
    "sports_medicine_injury_rehab": (["screening", "injury", "sports medicine"], ["筛查", "伤病", "运动医学"]),
}


def main() -> None:
    source_payload = json.loads((ROOT / "evidence/records/sources.json").read_text(encoding="utf-8"))
    sources = {item["id"]: item for item in source_payload["records"]}
    cards = []
    for index, (source_id, topic, subtopic, title_zh, title_en, summary_zh, technical_summary_en) in enumerate(SPECS, start=1):
        source = sources[source_id]
        keywords_en, keywords_zh = TOPIC_KEYWORDS[topic]
        cards.append({
            "id": f"K-CARD-{index:03d}",
            "topic": topic,
            "subtopic": subtopic,
            "title_en": title_en,
            "title_zh": title_zh,
            "keywords_en": keywords_en,
            "keywords_zh": keywords_zh,
            "source_ids": [source_id],
            "evidence_tier": source["evidence_tier"],
            "population": source["population"],
            "summary_zh": summary_zh,
            "technical_summary_en": technical_summary_en,
            "limitations": source["limitations"],
            "review_status": "reviewed",
            "reviewed_by": "SportRX knowledge review",
            "reviewed_at": "2026-08-28",
            "access_tier": "public_metadata",
            "question_policy": "research_only" if topic == "sports_medicine_injury_rehab" else "education",
        })
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({"schema": "sportrx.knowledge_cards", "schema_version": "0.1", "records": cards}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(cards)} reviewed knowledge cards to {OUTPUT}")


if __name__ == "__main__":
    main()
