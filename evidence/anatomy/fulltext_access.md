# 全文与访问管理

## 已下载到本机私有库

以下论文经 Europe PMC 标记为开放获取并提供 PDF，使用
`python3 scripts/fetch_open_access_hypertrophy_reviews.py` 下载到被 Git 忽略的
`evidence/private/fulltext/hypertrophy/`：

| Source ID | PMCID | 内容 |
|---|---|---|
| `RT-FREE-MACHINE-SR-2023` | `PMC10426227` | 自由重量与器械训练的系统综述和 Meta 分析 |
| `RT-ROM-SR-2020` | `PMC6977096` | 动作幅度与肌肉发展的系统综述 |

脚本同时在私有目录生成 `manifest.json`，保存文件大小、SHA-256、下载地址和获取日期。

## 仅保存元数据与人工摘要

以下来源在 Europe PMC 中没有开放获取 PDF 标记，因此没有自动下载全文：

- `RT-VARIATION-SR-2022`
- `RT-MUSCLE-LENGTH-SR-2025`
- `RT-ORDER-SR-2021`
- `RT-SJMJ-REVIEW-2017`

它们继续以 DOI、PMID、引用、人工摘要和限制进入知识库。通过个人或机构合法访问
获得的文件，也只能进入私有目录，不得提交 GitHub。

## OpenStax 处理

OpenStax Anatomy and Physiology 2e 页面明确限制未经许可用于训练或摄入 LLM。
SportRX 因此只保留引用和人工整理的结构化短摘要，不下载、复制或把其全文加入
检索语料。

