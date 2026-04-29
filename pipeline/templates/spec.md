# Analysis Specification

> Phase: {{phase_number}} — {{phase_name}}
> Study: {{study_title}}
> Date: {{date}}

---

## Study Overview

| Field | Value |
|-------|-------|
| Study type | {{study_type}} |
| Design | {{design_description}} |
| Target journal | {{journal_name}} (IF {{impact_factor}}) |
| Reporting standard | {{STROBE / CONSORT / TRIPOD / PRISMA}} |
| Sample size | {{N}} |
| Primary outcome | {{primary_outcome}} |
| Primary exposure | {{primary_exposure}} |

---

## Variable Specification

### Primary Variables

| Role | Variable | Type | Description | Coding |
|------|----------|------|-------------|--------|
| Outcome | {{var}} | {{continuous/binary/time}} | | |
| Exposure | {{var}} | | | |

### Covariates

| Variable | Type | Rationale for Adjustment |
|----------|------|--------------------------|
| {{age}} | Continuous | Standard demographic confounder |
| {{sex}} | Binary | Standard demographic confounder |
| {{var}} | {{type}} | {{clinical_rationale}} |

### Subgroup Variable

| Variable | Levels | Rationale |
|----------|--------|-----------|
| {{subgroup}} | {{level_list}} | {{why_subgroup}} |

---

## Analysis Methods

### Wave 1 (No Dependencies)

| # | Method | Purpose | Input Variables | Output Artifacts |
|---|--------|---------|-----------------|------------------|
| 01 | Baseline Table | Describe cohort characteristics | All variables | Table 1 (docx) |
| 02 | Group Comparison | Compare groups on key variables | Group var + continuous/categorical vars | Comparison table + box/violin plots |

### Wave 2 (Depends on Wave 1)

| # | Method | Purpose | Input Variables | Output Artifacts |
|---|--------|---------|-----------------|------------------|
| 03 | Logistic Regression | Identify independent predictors | Outcome + exposure + covariates | Regression table + forest plot |
| 04 | Survival Analysis | Time-to-event analysis | Time + event + covariates | KM curves + Cox table + forest plot |

### Wave 3 (Depends on Wave 2)

| # | Method | Purpose | Input Variables | Output Artifacts |
|---|--------|---------|-----------------|------------------|
| 05 | Subgroup Analysis | Treatment effect by subgroups | Exposure + subgroup var | Subgroup forest plot |
| 06 | Sensitivity Analysis | Robustness of findings | Per sensitivity scenario | Comparison table |

### Wave 4 (Depends on Data Partitioning)

| # | Method | Purpose | Input Variables | Output Artifacts |
|---|--------|---------|-----------------|------------------|
| 07 | Correlation Analysis | Variable relationships | All continuous vars | Heatmap + scatter matrix |
| 08 | ROC Analysis | Diagnostic accuracy | Biomarkers + outcome | ROC curves + AUC table |
| 09 | Marker Panel | Multi-biomarker model | Selected biomarkers | LASSO + ROC + confusion matrix |
| 10 | Simple ML | Predictive modeling | Feature set + outcome | RF/XGBoost/SVM comparison |

---

## Statistical Thresholds

| Criterion | Threshold | Correction |
|-----------|-----------|------------|
| Significance level | alpha = 0.05 | FDR for > 3 tests |
| Effect size reporting | Required | 95% CI always reported |
| VIF threshold | < 10 | Remove or combine variables |
| Sample size per event | >= 10 (logistic), >= 15 (Cox) | Document if violated |

---

## Figures and Tables Plan

| # | Artifact | Type | Content |
|---|----------|------|---------|
| Table 1 | docx | Baseline characteristics by group |
| Table 2 | xlsx | Group comparison results |
| Table 3 | xlsx | Logistic regression results |
| Table 4 | xlsx | Cox regression results |
| Figure 1 | png/pdf | Group comparison plots |
| Figure 2 | png/pdf | KM survival curves |
| Figure 3 | png/pdf | Forest plot (subgroup/sensitivity) |
| Figure 4 | png/pdf | Correlation heatmap |
| Figure 5 | png/pdf | ROC curves |
| Figure 6 | png/pdf | Marker panel performance |

---

## Success Criteria

- [ ] All 10 analysis methods executed per wave order
- [ ] Each method produces figure + table + README
- [ ] All figures ≥300 DPI (FIGURE_DPI), English labels, color-blind friendly
- [ ] All statistical reports include effect size + 95% CI + exact p-value
- [ ] Assumptions tested and documented for each method
- [ ] Multiple comparison correction applied where applicable
- [ ] Code reproducible from cleaned.csv without manual steps

---

**Spec author**: {{author}}
**Approved by**: {{approver}}
**Date**: {{approval_date}}
