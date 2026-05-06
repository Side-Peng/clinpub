---
name: clinpub:analysis
description: "Phase 2: Adaptive statistical analysis. Claude diagnoses data structure (groups, timepoints, outcome types), proposes a customized analysis plan, discusses with user, and executes in dependency order. Each method outputs figure + table + README with publication-grade standards."
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
Phase 2: Statistical analysis. Execute selected analysis methods in wave order, each producing publication-grade figures (≥300 DPI), formatted tables, and method documentation.

Wave 1 → Wave 2 → Wave 3 → Wave 4 with dependency tracking. Only execute user-confirmed methods.
</objective>

<execution_context>
@./pipeline/workflows/analysis.md
@./pipeline/references/analysis_methods.md
@./pipeline/references/r_patterns.md
</execution_context>

<process>
Execute the analysis workflow from @./pipeline/workflows/analysis.md end-to-end.
</process>

<success_criteria>
- Each confirmed method has figure + table + README in 04_Outputs/
- Figures at ≥300 DPI, English labels, publication-grade theme
- Statistical reports include effect size + 95%CI + exact p-value
- Code reads from cleaned.csv, independently runnable
- R version and key package versions documented
</success_criteria>
