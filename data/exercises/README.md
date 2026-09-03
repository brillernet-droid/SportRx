# SportRX 动作内容库

`catalogue.json` 是 SportRX 的本地动作内容层。它保存动作名称、训练部位、所需器械及中英文操作说明，供用户浏览和选择训练动作。

`hypertrophy_atlas.json` 是经过审阅的增肌动作知识层。它把 16 个肌群区域连接到
21 个动作家族和 62 个代表动作 ID，用于解释覆盖关系与器械替代，不复制上游媒体，
也不生成训练剂量。人工说明见
[`evidence/hypertrophy/README.md`](../../evidence/hypertrophy/README.md)。

`training_anatomy.json` 保存 34 条主要训练肌肉或功能肌群的起止点摘要、跨关节、
主要动作、训练角色和图谱链接。它是人工审阅的运动解剖学教育层，详细说明见
[`evidence/anatomy/README.md`](../../evidence/anatomy/README.md)。

它不保存或展示上游项目的图片、GIF 或其他媒体文件，也不负责决定训练量、强度、进阶或运动风险。

## 来源与更新

- 上游：[`hasaneyldrm/exercises-dataset`](https://github.com/hasaneyldrm/exercises-dataset)
- 同步命令：`python3 scripts/sync_exercise_dataset.py`
- 只允许已同步的本地快照进入 SportRX 界面；运行时不会向第三方传输用户资料。

上游项目的数据结构和文字说明采用 MIT 许可；图片和 GIF 属于 Gym visual 的独立媒体授权，未被同步到本项目。完整说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
上游文字内容的完整许可文本见 [LICENSE-upstream-MIT.md](LICENSE-upstream-MIT.md)。

## 产品边界

动作库回答“某个动作是什么、需要什么器械、上游说明如何操作”。增肌动作图谱
进一步回答“它属于什么动作家族、主要覆盖哪些区域、有哪些可追踪的器械变式”。

处方引擎回答“谁、在什么条件下、做多少、以什么强度、何时调整”。目前只有有氧 FITT-VP 引擎可以自动产生处方；新增训练模块必须先有独立规则、证据映射和测试，不能因为动作已收录就自动开启。
