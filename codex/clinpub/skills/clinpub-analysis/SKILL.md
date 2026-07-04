---
name: clinpub-analysis
description: "Phase 2: Adaptive statistical analysis. Claude diagnoses data structure (groups, timepoints, outcome types), proposes a customized analysis plan, discusses with user, and executes in dependency order. Each method outputs figure + table + README with publication-grade standards."
---

# ClinPub Analysis

Phase 2: Statistical analysis. Execute selected analysis methods in wave order, each producing publication-grade figures (≥300 DPI), formatted tables, and method documentation.

A shared figure configuration script (`_figure_config.R`) is generated at the start of Phase 2 to ensure all method figures share consistent theme, color palette, and DPI. Every method R script must `source("04_Outputs/_figure_config.R")` after `library()` calls.

Wave 1 → Wave 2 → Wave 3 → Wave 4 with dependency tracking. Only execute user-confirmed methods.

## Execution Context

- Workflow: `pipeline/workflows/analysis.md`
- References: `pipeline/references/analysis_methods.md`, `r_patterns.md`

## Process

Execute the analysis workflow from `pipeline/workflows/analysis.md` end-to-end.

## Success Criteria

- Shared figure config script (`_figure_config.R`) exists in `04_Outputs/` and is sourced by all method R scripts
- Each confirmed method has figure + table + README in 04_Outputs/
- Figures at ≥300 DPI, English labels, publication-grade theme
- All method figures share consistent style (theme, color palette, DPI) via `_figure_config.R`
- Statistical reports include effect size + 95%CI + exact p-value
- Code reads from cleaned.csv, independently runnable
- R version and key package versions documented
