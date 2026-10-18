# UAT: User Acceptance Testing

> Phase: {{phase_number}} — {{phase_name}}
> Date: {{date}}
> Tester: {{tester_name}}

---

## Overview

User Acceptance Testing for Phase {{phase_number}} deliverables. Each item must pass before the phase milestone can be signed off.

---

## Test Cases

### TC-1: Data Integrity

| Item | Expected Result | Actual Result | Status |
|------|-----------------|---------------|--------|
| Row count matches documented exclusions | {{expected_N}} rows | | PASS / FAIL |
| No unexpected missing values in key variables | 0 unexpected missing | | PASS / FAIL |
| Variable types match dictionary | All types correct | | PASS / FAIL |
| Outliers handled per documented strategy | Strategy applied | | PASS / FAIL |

### TC-2: Analysis Outputs

| Item | Expected Result | Actual Result | Status |
|------|-----------------|---------------|--------|
| Each method has figure file | File exists, ≥300 DPI (FIGURE_DPI) | | PASS / FAIL |
| Each method has table file | File exists, readable | | PASS / FAIL |
| Each method has 方法说明 | 方法说明 complete with interpretation | | PASS / FAIL |
| Effect sizes + 95% CI in all analyses | Present in every output | | PASS / FAIL |
| P-values are exact (not just < 0.05) | Exact values reported | | PASS / FAIL |

### TC-3: Manuscript Quality

| Item | Expected Result | Actual Result | Status |
|------|-----------------|---------------|--------|
| IMRAD structure complete | All 4 sections present | | PASS / FAIL |
| Chinese manuscript body | Correct language | | PASS / FAIL |
| English figures/tables | Correct language | | PASS / FAIL |
| All citations have DOIs | Every reference has DOI | | PASS / FAIL |
| Figure/table references in text | All referenced, all exist | | PASS / FAIL |
| No AI-template patterns | Humanizer checklist clear | | PASS / FAIL |

### TC-4: Reproducibility

| Item | Expected Result | Actual Result | Status |
|------|-----------------|---------------|--------|
| Cleaning script runs from raw | No manual steps required | | PASS / FAIL |
| Analysis runs from cleaned.csv | Independent execution | | PASS / FAIL |
| Random seeds set | Seeds documented in code | | PASS / FAIL |
| Software versions recorded | sessionInfo() or equivalent | | PASS / FAIL |

---

## Sign-off

- [ ] All TC-1 items PASS
- [ ] All TC-2 items PASS
- [ ] All TC-3 items PASS
- [ ] All TC-4 items PASS

**Overall Status**: {{overall_status}}

**User Notes**:
{{user_notes}}

**Signed by**: {{signer}}
**Date**: {{sign_date}}
