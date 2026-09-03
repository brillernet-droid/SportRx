# SportRX 增肌动作知识层

这一目录回答的是“某个肌群可以通过哪些动作家族获得覆盖，以及不同变式为什么
不能被随意混为一谈”。它不负责决定组数、次数、负荷、频率或进阶。

## 数据链

```text
功能解剖与训练综述
→ SourceRecord
→ ClaimRecord（可说 / 不可说）
→ KnowledgeCard（研究解释）
→ Hypertrophy Movement Atlas（肌群区域 ↔ 动作模式）
→ 现有动作库中的代表性 Exercise ID
```

## 本轮内容

- 16 个肌群区域，包括胸、背、三角肌三束、手臂、股四头肌、腘绳肌、臀肌、
  小腿、躯干和前臂等。
- 21 个动作家族，包括水平推、垂直拉、膝主导、髋铰链、屈膝、髋伸和躯干
  稳定任务等。
- 62 个指向 `data/exercises/catalogue.json` 的代表性动作 ID。
- 8 个新增来源、8 条原子结论和 18 张已审核知识卡。

## 文件

- `manifest.json`：本知识层的机器可读清单。
- `movement_taxonomy.md`：为什么按动作模式组织，而不是直接罗列动作。
- `muscle_regions.md`：主要肌群、动作家族和覆盖边界。
- `exercise_selection.md`：动作选择、替代、顺序、ROM 与变化原则。
- `review_log.md`：本轮纳入与仍缺少的证据。
- `../../data/exercises/hypertrophy_atlas.json`：可检索的结构化图谱。

## 关键边界

- `primary region` 表示主要训练覆盖，不是肌肉受力测量。
- `secondary region` 表示协同参与，不等于相同的有效组数。
- 代表动作不是“最佳动作”，也不是自动处方结果。
- 上游动作名称与 target 标签仅用于内容发现，不能作为临床或生理证据。
- 疼痛、康复、动作禁忌和个体适用性不由本图谱判断。

