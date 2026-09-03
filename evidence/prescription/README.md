# SportRX 目标导向处方知识层

这里整理“为什么某个训练目标需要某种训练组成”的公开循证材料。它是人读得懂的
审阅层，不直接生成用户处方。

## 数据链

```text
PubMed / 官方指南
→ SourceRecord（来源与适用范围）
→ ClaimRecord（允许说与禁止说）
→ KnowledgeCard（可检索解释）
→ manifest.json（目标与当前产品状态）
→ Program Pack（独立规则、测试通过后才可启用）
```

规则与知识库严格分开：Knowledge RAG 可以解释研究，但不能开启 Pack、改变 Safety
Gate、选择个人剂量或覆盖进阶规则。

## 文件

- `manifest.json`：六个用户目标的来源、结论、知识卡、规则与产品状态总表。
- `01_general_principles.md`：目标优先、综合计划和完成率边界。
- `02_cardiorespiratory.md`：有氧 FITT-VP、连续训练和 HIIT。
- `03_resistance_training.md`：力量、增肌、功率、力竭、RIR、频率与最小剂量。
- `04_body_composition.md`：减脂、腰围、瘦体重和结果承诺边界。
- `05_concurrent_training.md`：有氧与抗阻并行训练的安排逻辑。
- `review_log.md`：本批次检索、纳入和后续复核记录。

结构化原始记录位于：

- `evidence/records/packs/goal_prescription_sources.json`
- `evidence/records/packs/goal_prescription_claims.json`
- `evidence/knowledge/packs/goal_prescription_v1.json`

## 当前结论

- 已运行：建立习惯、提升心肺适能的有氧基础处方。
- 有限运行：综合体能目前仍是有氧基础版，不能称为完整综合处方。
- 仅评估：增肌与减脂已有证据知识层，但尚未具备可发布的自动剂量规则。
- 测量优先：专项表现必须先完成足够的 Benchmark 测量。

## 版权与访问

仓库只保存引用、DOI/PMID、稳定链接、人工摘要和产品边界。论文全文、付费书籍或
机构授权材料不进入 Git 历史；私有全文只能放在被忽略的 `evidence/private/`。
