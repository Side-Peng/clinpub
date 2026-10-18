# Verification Report: {{method_name}}

> Phase: {{phase_number}} — {{phase_name}}
> Date: {{date}}
> Verified by: clinpub-verifier
> Status: {{PASS / FAIL / CONDITIONAL}}

---

## Checks Performed

| # | Pattern | Check Description | Status | Notes |
|---|---------|-------------------|--------|-------|
| 1 | Descriptive cross-check | Baseline stats match cleaned data | {{status}} | |
| 2 | Model output consistency | OR/HR direction, CI, p-values consistent | {{status}} | |
| 3 | Survival consistency (if applicable) | KM median, risk table, log-rank vs Cox | {{status}} | |
| 4 | ROC/AUC validity | AUC bounds, CI symmetry, Youden threshold | {{status}} | |
| 5 | Multiple comparison correction | FDR/Bonferroni applied when > 3 tests | {{status}} | |
| 6 | Code reproducibility | Scripts run from cleaned.csv, seeds set | {{status}} | |
| 7 | Data integrity chain | Row counts, exclusions, train/val split | {{status}} | |
| 8 | Figure-table consistency | Values, N, significance annotations match | {{status}} | |

---

## Issues Found

{{#if issues}}

### Issue 1: {{issue_title}}

- **Severity**: Critical / Warning / Info
- **Pattern**: Pattern {{N}}
- **Description**: {{what_was_found}}
- **Evidence**: {{specific_values_or_output}}
- **Recommendation**: {{how_to_fix}}

### Issue 2: {{issue_title}}

{{/if}}

{{#if no_issues}}
No issues found. All verification patterns passed.
{{/if}}

---

## Reproducibility Confirmation

| Item | Status | Evidence |
|------|--------|----------|
| Raw → Cleaned reproducible | {{status}} | {{script_name}} runs without manual steps |
| Cleaned → Analysis reproducible | {{status}} | {{analysis_script}} runs from cleaned.csv |
| Random seeds documented | {{status}} | Seeds in {{line_numbers}} |
| Package versions captured | {{status}} | sessionInfo() / requirements.txt at {{path}} |
| Output files match expectations | {{status}} | File counts and sizes verified |

---

## Data Flow Verification

```
Raw Data ({{raw_N}} rows)
    ↓ [cleaning_script.R — documented exclusions]
Cleaned Data ({{cleaned_N}} rows)
    ↓ [analysis_script.R — no manual steps]
Output Figures ({{figure_count}} files) + Tables ({{table_count}} files)
    ↓ [writer-agent — reads from 04_Outputs/]
Manuscript References (all figures/tables cited)
```

**Chain integrity**: {{VERIFIED / BROKEN at stage}}

---

## Sign-off

- [ ] All critical issues resolved
- [ ] All warnings acknowledged and documented
- [ ] Reproducibility confirmed end-to-end
- [ ] Data flow chain verified

**Verified by**: {{verifier_name}}
**Date**: {{verification_date}}
**Result**: {{PASS / FAIL / CONDITIONAL}}
