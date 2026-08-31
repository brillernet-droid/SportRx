# SportRX 动作内容库

`catalogue.json` 是 SportRX 的本地动作内容层。它保存动作名称、训练部位、所需器械及中英文操作说明，供用户浏览和选择训练动作。

它不保存或展示上游项目的图片、GIF 或其他媒体文件，也不负责决定训练量、强度、进阶或运动风险。

## 来源与更新

- 上游：[`hasaneyldrm/exercises-dataset`](https://github.com/hasaneyldrm/exercises-dataset)
- 同步命令：`python3 scripts/sync_exercise_dataset.py`
- 只允许已同步的本地快照进入 SportRX 界面；运行时不会向第三方传输用户资料。

上游项目的数据结构和文字说明采用 MIT 许可；图片和 GIF 属于 Gym visual 的独立媒体授权，未被同步到本项目。完整说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
上游文字内容的完整许可文本见 [LICENSE-upstream-MIT.md](LICENSE-upstream-MIT.md)。

## 产品边界

动作库回答“某个动作是什么、需要什么器械、上游说明如何操作”。

处方引擎回答“谁、在什么条件下、做多少、以什么强度、何时调整”。目前只有有氧 FITT-VP 引擎可以自动产生处方；新增训练模块必须先有独立规则、证据映射和测试，不能因为动作已收录就自动开启。
