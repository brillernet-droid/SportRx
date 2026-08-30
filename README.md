# SportRX

> **一次标准化测量，形成可解释训练起点，并用复测证明变化。**

SportRX 是面向健身房、跑团与训练营的运动表现测量与训练决策原型。
它不把自己做成 AI 健身教练，也不把问卷伪装成体能评估；它先记录当前真实
测到的表现，再决定是否可以进入保守的训练起点，并在后续通过完成情况、RPE
和同协议复测观察变化。

**测得准，开得稳，讲得清，能复测。**

[English](README.en.md) · [3 分钟开始体验](docs/zh-CN/quickstart.md) · [公开示例站边界](docs/zh-CN/public-preview.md) · [场馆测试前确认](docs/zh-CN/venue-entry.md) · [产品说明](docs/zh-CN/product-guide.md) · [术语说明](docs/zh-CN/terminology.md) · [产品边界](docs/zh-CN/claim-boundaries.md) · [数据治理](evidence/data_governance.md)

## SportRX 解决什么问题

许多运动参与者已经有目标：开始规律训练、加入跑团、准备 HYROX-style
challenge，或在健身房进行更系统的训练。但他们常常不知道：

- 当前已经测到了哪些能力；
- 哪些能力还没有测，不能假装知道；
- 是否适合自动进入训练；
- 第一阶段训练应该从哪里开始；
- 什么时候、以什么条件复测才有意义。

SportRX 将这些问题组织成一条可追溯的闭环，而不是先给一份看似个性化的计划。

```text
外部筛查路径 → Safety Gate → Hybrid Benchmark → Training Profile → Starter Path → RPE / Completion → Retest
```

## 核心体验

| 价值 | SportRX 的做法 |
| --- | --- |
| 测得准 | 通过 Hybrid Benchmark 的标准路径或低器械路径，记录原始结果、协议、RPE、设备/场地和偏差。 |
| 开得稳 | Safety Gate 与表现数据分开；规则引擎决定 FITT-VP 起点与进阶，而不是让模型自由生成剂量。 |
| 讲得清 | Training Profile 显示已测、`Not tested`、strongest area、what needs work 与下一步。 |
| 能复测 | 仅在同协议、相近条件下解释变化；不强行比较不同测试路径。 |

## 3 分钟体验

```bash
python3 -m pip install -e ".[dev,app]"
python3 scripts/smoke_check.py
bash scripts/run_local.sh
```

打开终端显示的本地地址后，选择 **中文版**。第一次体验推荐从工作台的
“完整示例”开始，按下面的顺序浏览：

1. 从 **测试前确认** 开始：它只记录外部筛查的最小路由元数据，不收集筛查题目或健康细节。
2. 只有 Safety Gate 明确允许时，进入 **Benchmark 流程**；否则结果仅用于分流，不打开自动测试或训练内容。
3. 查看 **Training Profile**：理解当前测量画像和下一步测量动作。
4. 在满足数据门槛时查看 **Starter Path** 与 4 周训练交接。
5. 查看训练完成情况、RPE 与 **Retest**：理解何时维持、谨慎进阶或暂停自动调整。

完整说明见 [首次体验与本地运行](docs/zh-CN/quickstart.md)。

## 产品能力地图

| 阶段 | 面向用户或机构的能力 | 当前原则 |
| --- | --- | --- |
| 1. 训练前分流 | 外部筛查路径、Safety Gate | 只记录最小路由元数据；可阻断 Benchmark 与自动训练交接，但不提高或降低表现画像。 |
| 2. 粗筛与测量 | Quick Match、Hybrid Benchmark | 自报用于分流；表现比较依赖实测与协议来源。 |
| 3. 当前画像 | Training Profile | 至少两个已测表现维度后，才比较 strongest area 与 what needs work。 |
| 4. 训练交接 | Starter Path、4 周训练块 | 规则决定频率、强度、时间、类型、总量与渐进。 |
| 5. 反馈与复测 | RPE、完成率、Retest | 计划不在第一天写死；同协议复测才解释变化。 |

机构交付、测试员操作与复测逻辑见 [产品说明](docs/zh-CN/product-guide.md)。

## 当前状态与验证计划

SportRX 目前是一个**测量优先的原型**，不是已完成验证的医疗、预测或赛事系统。
当前工作重点是验证一条现场流程能否被正确使用：

1. 自用：完成基线、每周 RPE/完成记录与同协议复测。
2. 小样本试用：观察首次设置、测试、结果理解与复测意愿。
3. 机构试点：观察测试员执行、协议偏差、交付成本和机构复用。

在积累足够真实数据与正式验证之前，SportRX 不会将内部规则、原型排序或测试
流程称为人群常模、运动准备度评分、风险预测或赛事能力预测。

## 安全与产品边界

SportRX 不提供疾病诊断、医疗清除、伤病风险百分比、完赛概率、假百分位或官方
赛事认证。场馆模式仅通过已配置的外部筛查路径分流；默认中国路径仍为
`research_required`，不开展真实试点。出现需要进一步专业评估的信息时，Safety Gate
会停止 Benchmark 与自动训练交接。
AI 也不决定安全状态、训练强度、周运动量或进阶。

完整边界见 [产品边界](docs/zh-CN/claim-boundaries.md)。

## 语言与术语

中文用户版的导航、按钮和解释使用中文；为保持体育科学与设备语境的一致性，
`SportRX`、`HYROX`、`RPE`、`Benchmark`、`Safety Gate`、`Training Profile`、
`Starter Path`、`RowErg` 和 `SkiErg` 保留英文术语。术语对照见
[中文术语说明](docs/zh-CN/terminology.md)。

## 项目结构

```text
SportRX/
├── app/          # Streamlit 本地演示
├── sportrx/      # 规则引擎、测量记录、报告与导出
├── evidence/     # 证据库、结构化规则记录与内部审阅检索评测
├── docs/zh-CN/   # 面向中文使用者的公开说明
├── examples/     # 示例输入与输出
└── tests/        # 本地验证测试
```

证据库、规则 ID、数据 schema 和原始文献链接继续使用英文，避免维护两套逐字
技术文件。中文页面提供产品层说明，并链接到对应的公开技术材料。

内部循证记录将来源、可支持结论、产品规则和测试协议连成可审阅链条。它只用于
规则审阅与未来的受限解释，不是用户聊天机器人，也不会改变 Safety Gate 或训练剂量。
组件级证据状态与不可声称内容见
[Benchmark 组件证据台账](evidence/source_notes/006_benchmark_component_evidence.md)。

## 内部知识 RAG

SportRX 另有一个内部研究型 Knowledge Lab，用于检索已审核的运动科学知识卡并
在通过门槛后生成带引用和局限的中文研究摘要。它与产品规则库分开：知识 RAG
不能改变 Safety Gate、测试解释、训练剂量或进阶，也不会作为公开用户聊天功能。
其公开元数据与审核规则见 [Knowledge Corpus](evidence/knowledge/README.md)。

## 开发与验证

运行全部测试：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider
```

生成公开发布包时，内部审阅材料、缓存、审阅压缩包和本机生成内容会被排除。
该发布包是代码与公开文档的交付物，不构成科学验证。

## 贡献与讨论

欢迎对测试协议、字段设计、产品交付和循证边界提出问题。请不要提交会让系统
产生医疗诊断、风险预测、完赛预测、假常模或 AI 自动处方的功能建议。

许可证见 [LICENSE](LICENSE)。
