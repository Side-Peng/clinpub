# Analysis Context

Use this context during Phase 2 statistical analysis.

## Key Principles

- **CSV tray**: Always read from `02_PreprocessedData/data/cleaned.csv`
- **Figure-first**: Every method must output BOTH figure(s) and table(s)
- **Publication-grade**: ≥300 DPI, English labels, color-blind friendly, theme_pub()
- **Effect size + 95%CI + exact p-value**: report for every analysis
- **Assumption tests**: normality, homoscedasticity, proportional hazards — report and flag violations

## Batch Structure（3.0 迭代模型）

分析不再预定义"波次"。每批 1–3 个方法，依据上一批结果与决策规则库推进：

1. **首批**：基线表 + 描述统计（无依赖）
2. **后续批**：比较 / 回归 / 生存等，取决于上一批结果（见 `analysis_decision_policy.md`）
3. **亚组 / 敏感性**：依赖主分析模型已建立
4. **相关 / ROC / 预测**：依赖数据划分与主变量确定

批次划分由饱和判据与预算决定，不写死。每批记录写入 `.clinpub/ANALYSIS_LOG.md`。

## File References

- `pipeline/references/analysis_methods.md` — detailed method specs
- `pipeline/references/r_patterns.md` — R code patterns (12 patterns)
- `agents/analyst-agent.md` — analyst agent role card

## Output Standards

| Format | Resolution | Use Case |
|--------|-----------|----------|
| TIFF (LZW) | ≥300 DPI | Journal submission |
| PNG | ≥300 DPI | Preview |
| PDF | Vector | Layout/editing |
| XLSX | — | Data tables |
| DOCX | — | Table 1 (3-line style) |
