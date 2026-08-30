# 首次体验与本地运行

SportRX 当前以本地 Streamlit 原型形式运行。它用于产品体验、协议审阅和小样本
试用，不是医疗服务或已验证的赛事评估工具。

[返回项目主页](../../README.md) · [产品说明](product-guide.md) · [产品边界](claim-boundaries.md)

## 运行环境

需要 Python 3 和本项目声明的依赖。进入项目根目录后运行：

```bash
python3 -m pip install -e ".[dev,app]"
python3 scripts/smoke_check.py
bash scripts/run_local.sh
```

浏览器打开终端输出的本地地址。默认使用 `127.0.0.1:8501`；如端口被占用，可使用
`SPORTRX_PORT=8502 bash scripts/run_local.sh`。

进入后选择 **中文版**。`English Lab Edition` 用于英文文案审阅；`Internal Mixed
Review` 只用于内部 QA，不是普通用户体验。

## 三种体验路径

### 3 分钟：完整示例

适合第一次了解产品闭环。进入工作台后加载完整示例，按以下顺序浏览：

1. Quick Match：近期训练行为和现实时间约束。
2. HYROX 检查：已测、未测与安全信息的分离。
3. Benchmark 流程：测试路径、设备、RPE、停止条件与记录要求。
4. Training Profile：当前测量画像、strongest area、what needs work 与下一步。
5. 训练、RPE 和复测：训练交接如何随完成情况调整。

示例数据只用于产品浏览，不是常模、验证数据或真实运动员记录。

### 5 分钟：Quick Match 粗筛

适合快速建立近期训练与时间约束的记录。填写过去 4 周的训练次数、分钟数、连续
跑/走情况、力量训练日和可用时间。

Quick Match 只能帮助粗略分流和说明下一步；它不收集 1 km 或 5 km 成绩，也不能
代替表现测试、训练画像或定制 Starter Path。

### 15 分钟以上：一次本地 Benchmark

适合准备进行真实记录的使用者或测试员。先确认 Safety Gate、设备条件与测试路径，
再按 Benchmark 流程完成组件测试。每个组件至少记录：

- 原始结果与单位；
- RPE（0–10）；
- 设备、场地、路线或负荷；
- 替代动作、未完成原因与现场偏差；
- 测试日期与协议路径。

未完成或未做的项目保留为 `Not tested`。只有满足测量门槛时，系统才会比较
strongest area 与 what needs work，或生成保守的 Starter Path。

## 复测

复测尽量使用相同路径、器械、场地、顺序和记录口径。不同协议的结果仍可保留为
原始记录，但不应被解释为直接可比的能力变化。

训练期间记录完成情况与 RPE。完成率低、RPE 偏高或出现异常时，不应自动进阶。
更多交付与复测说明见 [产品说明](product-guide.md)。
