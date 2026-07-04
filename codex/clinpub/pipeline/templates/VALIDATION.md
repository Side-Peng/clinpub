# VALIDATION: Statistical Validation Checklist

> Phase: {{phase_number}} — {{phase_name}}
> Analysis Method: {{method_name}}
> Date: {{date}}

---

## Prerequisites

- [ ] `cleaned.csv` loaded (N = {{sample_size}}, M = {{variable_count}} variables)
- [ ] Project config loaded (study type: {{study_type}})
- [ ] Analysis method confirmed by user

---

## 1. Assumption Checks

### Normality

| Variable | Test Used | Statistic | P-value | Decision |
|----------|-----------|-----------|---------|----------|
| {{var_1}} | Shapiro-Wilk / Q-Q plot | | | Normal / Non-normal |
| {{var_2}} | | | | |
| {{var_3}} | | | | |

**If non-normal**: Applied {{transformation}} or switched to non-parametric test.

### Homoscedasticity

| Comparison | Levene's Test P-value | Decision |
|------------|----------------------|----------|
| {{group_comparison}} | | Equal / Unequal variances |

### Proportional Hazards (if survival analysis)

| Covariate | Schoenfeld Test P-value | PH Assumption |
|-----------|------------------------|---------------|
| {{covariate_1}} | | Met / Violated |

**If violated**: Applied {{stratification / time-varying covariate}}.

---

## 2. Model Diagnostics (if regression)

### Multicollinearity

| Variable | VIF | Tolerance | Flag |
|----------|-----|-----------|------|
| {{var_1}} | | | OK / HIGH |

**Threshold**: VIF > 10 flagged. Action: {{remove / combine / document}}.

### Model Fit

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Hosmer-Lemeshow p-value | | Good fit if > 0.05 |
| AUC (if applicable) | | Discrimination quality |
| Nagelkerke R² | | Variance explained |

### Influential Observations

| Criterion | Threshold | N Flagged | Action |
|-----------|-----------|-----------|--------|
| Cook's D | > 4/n | | |
| DFBetas | > 2/sqrt(n) | | |

---

## 3. Multiple Comparisons

| # Tests | Correction Method | # Significant Before | # Significant After |
|---------|-------------------|---------------------|---------------------|
| {{n_tests}} | FDR / Bonferroni / None (<=3) | | |

---

## 4. Effect Size Reporting

| Outcome | Effect Size | 95% CI | Exact P-value | Interpretation |
|---------|------------|--------|---------------|----------------|
| {{outcome_1}} | | | | |
| {{outcome_2}} | | | | |

---

## 5. Software Environment

| Component | Version |
|-----------|---------|
| R / Python | {{version}} |
| Key packages | {{package_list_with_versions}} |
| OS | {{os_info}} |

---

## Validation Summary

| Category | Items | Passed | Failed | N/A |
|----------|-------|--------|--------|-----|
| Assumption checks | | | | |
| Model diagnostics | | | | |
| Multiple comparisons | | | | |
| Effect size reporting | | | | |
| Software documentation | | | | |

**Overall**: {{PASS / FAIL}}

**Notes**: {{validation_notes}}

**Validated by**: {{validator_name}}
**Date**: {{validation_date}}
