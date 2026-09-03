# SportRX Training Anatomy v0.1

这一层为 SportRX 提供训练相关的运动解剖学基础：肌肉名称、起止点摘要、跨关节、
主要动作、训练中的角色，以及它与动作模式和代表动作的关系。

## 当前规模

- 34 条肌肉或功能肌群记录。
- 覆盖现有 Hypertrophy Movement Atlas 的 16 个训练区域。
- 连接 21 个动作模式中的主要抗阻训练模式。
- 18 张中英文 Training Anatomy KnowledgeCard。
- 4 个新增解剖来源与 3 条可审查的解剖解释边界。

## 结构

```text
公开解剖来源
→ SourceRecord
→ ClaimRecord（结构能说明什么 / 不能说明什么）
→ TrainingAnatomyRecord
→ Muscle region
→ Movement pattern
→ Representative exercise ID
→ KnowledgeCard
```

## 文件

- `data/exercises/training_anatomy.json`：34 条结构化记录。
- `sportrx/training_anatomy.py`：校验、单条查询和中文检索接口。
- `coverage.md`：当前肌肉与功能群覆盖。
- `fulltext_access.md`：论文下载、访问与版权处理。
- `review_log.md`：人工审阅状态和后续缺口。

## 边界

- 这不是覆盖人体 600 余块肌肉的医学解剖数据库。
- 起止点与关节动作不能证明某个动作“激活最高”或“增肌最好”。
- 原动肌、协同肌和稳定肌角色会随任务改变，不能固定换算成有效组数。
- 肩痛、腰痛、肌肉失衡、康复和动作禁忌不由本知识层判断。
- OpenStax 页面只用于引用和人工摘要，不下载或摄入全文到 LLM/RAG。

