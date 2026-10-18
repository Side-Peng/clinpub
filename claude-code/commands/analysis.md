---
name: analysis
description: "阶段2：迭代式统计分析。诊断数据结构后，每批提出 1–3 个方法，执行并记录结果与解读，再据结果决定下一批，直到饱和或触及预算。每个方法产出版级图 + 表格 + 方法说明。"
argument-hint: ""
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---
<objective>
阶段2：**迭代式**统计分析。

与 2.x 的关键差异：不再"一次确认全部分析方法"。每批只提出 1–3 个方法，执行后记录结果与解读，再依据 `analysis_decision_policy.md` 的规则决定下一批。所有决策写入 `.clinpub/ANALYSIS_LOG.md`，作为阶段3 写作时 Discussion 的输入。

共享图表配置脚本 `04_Outputs/_figure_config.R` 在第一批执行前一次性生成，所有方法 R 脚本必须 `source()` 它。
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/analysis.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/analysis_decision_policy.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/analysis_methods.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/r_patterns.md"`
</execution_context>

<process>
Execute the analysis workflow from pipeline/workflows/analysis.md end-to-end.

核心循环（详见 workflow 的 `iterative_loop` 步骤）：

```
诊断 → 初始化会话（预算 / 续跑检查 / 图表配置）
     → 循环：提议一批 → 分叉判断 → 执行 → 记录 → 饱和判断
     → 冻结分析（ANALYSIS_SUMMARY）→ 满意度确认 → 里程碑
```

三个不可省略的产物：

1. `.clinpub/ANALYSIS_LOG.md` —— 每批六段（依据 / 方法 / 结果要点 / 解读 / 下一批决策 / 否决项）
2. `.clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md` —— 冻结时的收敛摘要
3. `04_Outputs/MANIFEST.yaml` —— 输出清单与下游消费者
</process>

<success_criteria>
- `ANALYSIS_LOG.md` 存在，每个 Batch 六段齐全（含否决项）
- 每批方法的选择可追溯到 `analysis_decision_policy.md` 的具体规则编号（R/D/U）
- 分叉情形按策略 §5 停下询问用户；退出循环时写明命中的饱和判据（S1–S5）
- `04_Outputs/_figure_config.R` 存在且被所有方法 R 脚本 `source()`
- 每个确认的方法都有图 + 表 + `方法说明.md` 在 `04_Outputs/`
- 图 ≥300 DPI、英文标注、出版级主题，全方法风格一致
- 统计报告含效应量 + 95%CI + 精确 p 值（禁止 `p = 0.000`）
- 代码从 `cleaned.csv` 独立可运行，记录 R 版本与关键包版本
- `ANALYSIS_SUMMARY.md` 已生成
</success_criteria>
