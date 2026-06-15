# Verification Patterns

> Patterns for verifying statistical analysis validity and reproducibility in clinical research.

---

## Statistical Verification Patterns

### Pattern 1: Descriptive Statistics Cross-Check

**Purpose**: Verify baseline table matches raw data summary.

**Steps:**
1. Load cleaned.csv
2. Compute key statistics independently (N, mean, SD, median, IQR, proportions)
3. Compare against Table 1 output values
4. Tolerance: floating-point difference < 1e-6

**Failure indicators:**
- N mismatch between data and table
- Mean/SD discrepancy > 0.01
- Proportion rounding errors

---

### Pattern 2: Model Output Verification

**Purpose**: Verify regression model results are internally consistent.

**Steps:**
1. Check OR/HR direction matches coefficient sign
2. Verify 95% CI = estimate +/- 1.96 * SE (for normal-approximated models)
3. Confirm p-value consistency with CI (significant p ↔ CI excludes null)
4. Check VIF < 10 for all predictors (multicollinearity)
5. Verify sample size in model matches cleaned data (minus missing cases)

**Failure indicators:**
- OR > 1 but coefficient negative
- CI includes null but p < 0.05
- VIF > 10 without documented justification
- N in model output != N in cleaned data minus excluded cases

---

### Pattern 3: Survival Analysis Verification

**Purpose**: Ensure KM curves and Cox regression are consistent.

**Steps:**
1. Compare KM median survival time with raw event/censor data
2. Verify risk table N at each time point matches Kaplan-Meier estimate
3. Check log-rank p-value from KM matches Cox univariate p-value for same variable
4. Confirm PH assumption test (Schoenfeld) is reported for each covariate
5. Verify event count in Cox output matches data

**Failure indicators:**
- Median survival outside observed range
- Risk table N mismatch
- log-rank vs Cox p-value discrepancy > 0.01
- PH assumption violated without sensitivity analysis

---

### Pattern 4: ROC/AUC Verification

**Purpose**: Ensure diagnostic accuracy metrics are correct.

**Steps:**
1. Verify AUC is between 0 and 1
2. Check sensitivity + specificity values at Youden threshold
3. Confirm 95% CI for AUC is symmetric around point estimate
4. Cross-validate: Wilson CI for sensitivity/specificity matches reported values
5. Verify combined panel AUC > max individual AUC (or explain if not)

**Failure indicators:**
- AUC outside [0, 1]
- CI bounds inverted (lower > upper)
- Sensitivity or specificity outside [0, 1]
- Combined AUC < best individual AUC without explanation

---

### Pattern 5: Multiple Comparison Verification

**Purpose**: Ensure appropriate correction for multiple testing.

**Steps:**
1. Count total number of tests within each analysis family
2. If > 3 tests: verify FDR or Bonferroni correction applied
3. Check corrected p-values <= raw p-values
4. Verify correction method documented in 方法说明
5. Confirm significant results survive correction (or note which do not)

**Failure indicators:**
- No correction when > 3 tests performed
- Corrected p > raw p
- Significant result claimed without correction

---

## Reproducibility Verification Patterns

### Pattern 6: Code Reproducibility

**Purpose**: Ensure analysis can be independently reproduced.

**Steps:**
1. Verify all R/Python scripts read from `cleaned.csv` (not hardcoded paths)
2. Check no manual steps between script sections
3. Confirm random seeds set for any stochastic methods (ML, imputation)
4. Verify package versions documented (sessionInfo() or requirements.txt)
5. Check output file paths use relative references

**Required evidence:**
- Script runs from top to bottom without error
- Output files match previously generated results
- sessionInfo() or equivalent captured

---

### Pattern 7: Data Integrity Chain

**Purpose**: Verify data flows correctly through pipeline stages.

**Steps:**
1. Raw data row/column count matches data profile
2. Cleaned data row count = raw count - documented exclusions
3. Variable transformations are reversible or documented
4. No data leakage between train/validation splits
5. Imputed values flagged or in separate column

**Failure indicators:**
- Row count discrepancy without documented exclusion
- Train/validation overlap detected
- Imputed values mixed with observed values without flag

---

### Pattern 8: Figure-Table Consistency

**Purpose**: Ensure figures and tables tell the same story.

**Steps:**
1. Compare key values in figure annotations with table data
2. Check axis ranges cover all data points
3. Verify N in figure caption matches N in analysis
4. Confirm significance annotations match reported p-values
5. Check color coding is consistent across figures

**Failure indicators:**
- Figure shows significance but table p > 0.05
- Figure N differs from table N
- Axis truncation hides data points
- Inconsistent color scheme across related figures

---

## Phase 1: Data Quality Verification Patterns

### Pattern 9: Data Quality Verification

**Purpose**: Verify cleaned data meets quality standards for downstream analysis.

**Steps:**
1. Load cleaned.csv and check row/column counts match expectations
2. Compare cleaned row count = raw row count - documented exclusions (tolerance: 0)
3. Verify variable types match project_config.yml specification (numeric, factor, ordered)
4. Check all categorical variables have expected levels (no unexpected values)
5. Confirm derived variables compute correctly when re-calculated from source variables
6. Verify data quality report HTML exists and is non-empty at `02_PreprocessedData/reports/`

**Failure indicators:**
- Row count mismatch without corresponding exclusion documentation
- Variable type mismatch with project_config.yml (e.g., continuous variable stored as factor)
- Categorical variable has unexpected levels (suggesting encoding error)
- Derived variable cannot be reproduced from source variables
- Data quality report missing or empty

---

### Pattern 10: Missing Value Handling Verification

**Purpose**: Ensure missing data strategy was applied correctly and transparently.

**Steps:**
1. Check high-missingness variables (>20%) have user-confirmed handling strategy documented in 方法说明
2. For MICE imputed variables: verify imputation model is documented (method, iterations, predictor variables)
3. Verify imputed values are flagged or tracked (separate column or imputation log)
4. For deletion strategy (<5%): confirm number of rows removed matches expected
5. For test/validation sets: verify they were imputed using training-set imputation model (no data leakage)
6. Confirm missing value report in data quality report matches actual cleaned data

**Required evidence:**
- Missing value handling strategy documented in method directory 方法说明
- Imputation log or flag column present in cleaned data structure
- Cleaning code shows correct deletion/imputation decision flow

**Failure indicators:**
- >20% missing variable handled without user confirmation
- MICE parameters not documented
- Imputed values indistinguishable from observed values
- Train/test split used separate imputation models
- Row deletion count contradicts documented exclusion criteria

---

### Pattern 11: Data Split Integrity

**Purpose**: Verify train/validation/test splits are valid and reproducible.

**Steps:**
1. Confirm stratification variable distribution is preserved across splits (proportion within 1% of original)
2. Check no overlap between train and validation/test sets (unique patient IDs)
3. Verify split ratio matches project_config.yml specification (tolerance: 1%)
4. Confirm random seed is set and documented for reproducibility
5. Check each split is saved as a separate file with clear naming

**Failure indicators:**
- Stratification variable proportion deviates >1% between splits
- Overlapping patient IDs between train and validation sets
- Split ratio differs from specified ratio by >1%
- No random seed set
- Missing split files

---

## Phase 3: Manuscript Verification Patterns

### Pattern 12: Manuscript Structure Verification

**Purpose**: Ensure IMRAD manuscript is structurally complete and follows target journal requirements.

**Steps:**
1. Verify all IMRAD chapters exist: Introduction, Methods, Results, Discussion, Abstract
2. Check Introduction follows funnel structure: broad background → known evidence → research gap → objective
3. Verify Discussion contains all 6 required elements: summary, comparison, mechanisms, implications, limitations, conclusion
4. Confirm word count is within target journal limits (check project_config.yml target_journal)
5. Verify STROBE/CONSORT checklist items are addressed in manuscript text
6. Check language split: Chinese for body text, English for figure/table titles

**Required artifacts:**
- `05_Manuscript/manuscript.md` (compiled full manuscript)
- Individual chapter drafts if applicable

**Failure indicators:**
- Missing one or more IMRAD sections
- Introduction lacks explicit research gap or objective
- Discussion missing limitations section
- Word count significantly over target journal limit
- STROBE/CONSORT items not addressed

---

### Pattern 13: Citation Integrity Verification

**Purpose**: Verify all citations are valid, traceable, and properly formatted.

**Steps:**
1. Check every entry in `references.bib` has a DOI field (non-empty, valid format)
2. Cross-reference in-text citations against `references.bib` — every citation in text must have a matching entry
3. Verify total reference count (aim for 30-50 for original research; adjust per target journal)
4. Check for duplicate references (same DOI appearing multiple times)
5. Confirm citation format is Vancouver (numbered style matching target journal convention)
6. Flag any citations without DOIs for user action — no DOI, no citation

**Required artifacts:**
- `Reference/references.bib` — all entries
- `Reference/citation_map.md` — mapping table
- Manuscript text — in-text citation markers

**Failure indicators:**
- Reference missing DOI
- In-text citation with no matching entry in references.bib
- Duplicate references (same DOI listed twice)
- Citation count significantly below journal minimum
- Non-Vancouver format detected

---

### Pattern 14: Figure-Table Reference Verification

**Purpose**: Verify all figures and tables referenced in the manuscript actually exist and meet standards.

**Steps:**
1. Extract all figure/table references from manuscript text (e.g., "Figure 1", "Table 2")
2. Check each referenced figure/table exists in `04_Outputs/` as a file
3. Verify figure number order in text matches sequential ordering (no missing numbers, no jumps)
4. Check figure/table captions include: N, statistical method, significance notation
5. Verify all figures meet minimum resolution: ≥300 DPI (FIGURE_DPI) (check with `identify -verbose` or `file` command)
6. Confirm figure titles and table headers are in English (per Chinese/English split convention)

**Failure indicators:**
- Manuscript references a figure/table that does not exist in output directory
- Figure numbering skips or is out of order
- Missing captions or captions missing required elements
- Figure resolution below 300 DPI
- Figure title in Chinese instead of English

---

### Pattern 15: Humanizer Anti-AI-Pattern Check

**Purpose**: Ensure manuscript reads like an experienced researcher's writing, not AI-generated template text.

**Steps:**
1. Check paragraph openings: scan for sequential markers (First/.../Second/.../Finally) — flag if found in 2+ consecutive paragraphs
2. Check transition word variety: count occurrences of Moreover/Furthermore/Additionally — flag if any single word used >3 times
3. Check sentence structure variety: if 3+ consecutive sentences share the same grammatical structure, flag for rewrite
4. Check conclusion section: look for "more research is needed" or equivalent hollow phrases — flag if found
5. Check citation integration: look for paragraph-openers like "As shown in Table X" or "Studies show that..." — flag if used in 2+ paragraphs
6. Check method over-explanation: look for parenthetical explanations of standard statistical terms — flag if found

**Self-check reference:**

| Check | AI Pattern | Pass Criteria |
|-------|-----------|--------------|
| Paragraph openings | Sequential markers | No more than 1 paragraph uses sequential openers |
| Transition words | Repeated formulaic | No single transition word used >3 times |
| Sentence structure | Identical patterns | No 3+ consecutive sentences with same structure |
| Conclusions | Hollow/generic | Conclusion includes specific future research direction |
| Citations | Impersonal | At least 50% of citations give specific author context |
| Explanations | Over-explaining | No parenthetical explanation of standard terms |

**Failure indicators:**
- 3 or more of the 6 checks fail → manuscript needs revision
- 1-2 checks fail → flagged as WARNING, user to decide
- All pass → passed

---

### Pattern 16: Modify Agent Output Consistency

**Purpose**: After modify-agent adjusts analysis outputs, verify that modifications are consistent and did not introduce regressions.

**Steps:**
1. Compare modified output files against PLAN.md modification record — verify all requested changes were applied
2. Check unmodified outputs remain unchanged (no accidental overwrites)
3. Verify all figures still meet ≥300 DPI threshold
4. Verify modified tables still have correct column counts and variable names
5. Check that method documentation (方法说明) was updated if statistical method changed
6. Verify MANIFEST.yaml in modified directories reflects updated file timestamps

**Self-check reference:**

| Check | Pass Criteria |
|-------|--------------|
| Requested changes applied | All items in modification scope present in output |
| Unmodified files intact | MD5/size match pre-modification baseline |
| Figure resolution | All figures ≥300 DPI |
| Table structure | Column names and row counts consistent with data |
| 方法说明 sync | If method changed, 方法说明 updated accordingly |
| MANIFEST updated | Timestamps and file list reflect current state |

**Failure indicators:**
- Any unmodified file changed → CRITICAL (regression)
- Figure below 300 DPI → CRITICAL
- 方法说明 not updated after method change → WARNING
- MANIFEST not updated → INFO

Each verification produces a structured report:

```markdown
# Verification Report: [Method Name]

**Date**: YYYY-MM-DD
**Verified by**: clinpub-verifier
**Status**: PASS / FAIL / CONDITIONAL

## Checks Performed

| # | Pattern | Check | Status | Notes |
|---|---------|-------|--------|-------|
| 1 | Pattern 1 | Descriptive cross-check | PASS | All values within tolerance |
| 2 | Pattern 2 | Model output check | FAIL | VIF = 12.5 for variable X |

## Issues Found

### Issue 1: [Title]
- **Severity**: Critical / Warning / Info
- **Pattern**: Pattern N
- **Description**: [What was found]
- **Recommendation**: [How to fix]

## Sign-off
- [ ] All critical issues resolved
- [ ] All warnings acknowledged
- [ ] Reproducibility confirmed
```
