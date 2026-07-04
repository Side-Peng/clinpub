# Analysis Context

Use this context during Phase 2 statistical analysis.

## Key Principles

- **CSV tray**: Always read from `02_PreprocessedData/data/cleaned.csv`
- **Figure-first**: Every method must output BOTH figure(s) and table(s)
- **Publication-grade**: ≥300 DPI, English labels, color-blind friendly, theme_pub()
- **Effect size + 95%CI + exact p-value**: report for every analysis
- **Assumption tests**: normality, homoscedasticity, proportional hazards — report and flag violations

## Wave Dependency Order

1. Wave 1: BaselineTable, GroupComparison — no dependencies
2. Wave 2: LogisticRegression, SurvivalAnalysis — depends on Wave 1
3. Wave 3: SubgroupAnalysis, SensitivityAnalysis — depends on Wave 2 models
4. Wave 4: CorrelationAnalysis, ROCAnalysis, MarkerPanel, SimpleML — depends on data partitioning

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
