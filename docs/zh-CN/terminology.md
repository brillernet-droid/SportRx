# 术语说明

SportRX 的中文用户版使用中文导航、按钮与解释。下列术语保留英文，以保持运动科学、
设备与测试记录在不同场景中的一致性。

[返回项目主页](../../README.md) · [产品说明](product-guide.md) · [完整受控术语表](../../evidence/glossary.md)

| 术语 | 中文说明 | 当前边界 |
| --- | --- | --- |
| SportRX | 产品品牌。 | Python 包名仍为 `sportrx`。 |
| HYROX | Hybrid endurance / functional training 的赛事语境用语。 | 当前仅支持 HYROX-style Benchmark，不代表官方认证或完赛预测。 |
| RPE | 主观用力程度，使用 0–10 记录测试或训练后的体感强度。 | 不是恢复评分或医学指标。 |
| Benchmark | 可复测的测试记录。 | 需要保留 protocol、原始数据、单位、RPE、设备和日期。 |
| Safety Gate | 训练交接前的基础安全分流。 | 可以阻断自动建议，但不提高或降低 measured performance。 |
| Training Profile | 当前训练画像。 | 显示当前测量画像，不是运动员类型、正式等级或 readiness score。 |
| Starter Path | 满足条件后生成的保守 4 周训练交接。 | 不是医疗建议、比赛预测或私人教练服务。 |
| Not tested | 尚未测试。 | 不用平均值、中位数或默认数值填补。 |
| strongest area | 当前已测维度中的相对强项。 | 至少两个已测表现维度后才能出现。 |
| what needs work | 当前已测维度中最值得优先处理的缺口。 | 数据不足时应改为建议下一项测量，而不是强行判断。 |
| RowErg | 划船测功仪。 | 记录时保留型号、测试路径和原始单位。 |
| SkiErg | 滑雪测功仪。 | 记录时保留型号、测试路径和原始单位。 |

更多字段和证据语言规则保留在英文的 [`evidence/`](../../evidence/) 目录中；中文
说明不替代原始来源、规则 ID 或数据 schema。
