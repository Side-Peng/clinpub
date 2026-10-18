---
name: clinpub-analysis
description: "阶段2: 迭代式统计分析。诊断数据结构后，每批提出 1–3 个方法，执行并记录结果与解读，再据结果决定下一批，直到饱和或触及预算。每方法产出版图 + 表格 + 方法说明。"
---

# ClinPub Analysis（迭代分析）

阶段2 采用**迭代**而非一次性规划：每批只提出 1–3 个方法，执行后记录结果与解读，
再依据 `pipeline/references/analysis_decision_policy.md` 的规则决定下一批。

所有批次记录写入 `.clinpub/ANALYSIS_LOG.md`（六段：依据 / 本批方法 / 结果要点 / 解读 / 下一批决策 / 否决项）。

共享图表配置脚本 `04_Outputs/_figure_config.R` 在首批执行前一次性生成，所有方法 R 脚本必须 `source()` 它。

## Execution Context

- Workflow: `pipeline/workflows/analysis.md`
- Decision policy: `pipeline/references/analysis_decision_policy.md`
- Methods: `pipeline/references/analysis_methods.md`
- R patterns: `pipeline/references/r_patterns.md`

## Process

```
诊断 → 初始化会话（预算 / 续跑检查 / 图表配置）
     → 循环：提议一批 → 分叉判断 → 执行 → 记录 → 饱和判断
     → 冻结分析（ANALYSIS_SUMMARY）→ 满意度确认 → 里程碑
```

三个不可省略的产物：

1. `.clinpub/ANALYSIS_LOG.md` —— 每批六段记录
2. `.clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md` —— 冻结时的收敛摘要
3. `04_Outputs/MANIFEST.yaml` —— 输出清单与下游消费者

## Success Criteria

- `ANALYSIS_LOG.md` 每个 Batch 六段齐全（含否决项）
- 每批方法选择可追溯到决策规则编号（R/D/U）
- 分叉情形按策略 §5 停下询问；退出循环时写明命中的饱和判据（S1–S5）
- `04_Outputs/_figure_config.R` 存在且被所有方法 R 脚本 `source()`
- 每个方法有图 + 表 + `方法说明.md`
- 图 ≥300 DPI、英文标注、出版级主题，全方法风格一致
- 统计报告含效应量 + 95%CI + 精确 p 值（禁止 `p = 0.000`）
- 代码从 `cleaned.csv` 独立可运行，记录 R 版本与关键包版本
- `ANALYSIS_SUMMARY.md` 已生成
