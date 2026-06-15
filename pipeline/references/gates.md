# Quality Gates

> Phase transitions require passing specific quality gates. No gate can be bypassed.

---

## Gate Types

### Gate 1: IRB / Ethics Gate (Phase 0 → Phase 1)

**Purpose**: Ensure ethical compliance before any data handling.

| Check | Required | Pass Condition |
|-------|----------|----------------|
| IRB approval number | Yes | Valid IRB ID in project_config.yml |
| Data de-identification | Yes | No PHI columns (name, ID, DOB, address, phone, email) detected |
| Informed consent reference | Yes | Consent document path exists or waived with justification |
| Data use agreement | Conditional | Required if multi-center or shared data |
| Clinical trial registration | Conditional | Required for RCT: registration ID in project_config.yml |

**Gate passage**: All "Required" checks pass + applicable "Conditional" checks addressed.

**Failure action**: Block Phase 1. Report missing items with remediation steps.

---

### Gate 2: Data Quality Gate (Phase 1 → Phase 2)

**Purpose**: Ensure cleaned data is analysis-ready.

| Check | Required | Pass Condition |
|-------|----------|----------------|
| cleaned.csv exists | Yes | File at `02_PreprocessedData/data/cleaned.csv` |
| Variable dictionary complete | Yes | Every column has name, type, missing%, description |
| Missing rate within tolerance | Yes | No variable >20% missing without documented decision |
| Sample size adequate | Yes | N >= minimum per power analysis (or documented justification) |
| Outliers documented | Yes | All flagged outliers have handling decision recorded |
| Data quality report | Yes | HTML report generated in `02_PreprocessedData/reports/` |
| Reproducible cleaning code | Yes | Cleaning script runs from raw → cleaned without manual steps |

**Gate passage**: All checks pass.

**Failure action**: Return to Phase 1. Document which checks failed.

---

### Gate 3: Analysis Validity Gate (Phase 2 → Phase 3)

**Purpose**: Ensure statistical analysis is valid and complete.

| Check | Required | Pass Condition |
|-------|----------|----------------|
| All confirmed methods executed | Yes | Every method in project_config.yml has output in `04_Outputs/` |
| Each method has figure + table + 方法说明 | Yes | Three artifacts per method directory |
| Effect size + 95% CI reported | Yes | Every analysis includes effect size, CI, and exact p-value |
| Assumptions tested | Yes | Normality, homoscedasticity, PH assumptions checked and reported |
| Multiple comparison correction | Conditional | Applied when >3 tests in single analysis |
| Software versions documented | Yes | R/Python version + key packages in method 方法说明 |
| Code reproducible | Yes | Analysis runs from cleaned.csv without manual intervention |

**Gate passage**: All checks pass.

**Failure action**: Return to Phase 2. Specify which analyses failed validity.

---

### Gate 3.5: Writing Quality Gate (Phase 3 → Phase 4)

**Purpose**: Manuscript draft is complete enough for peer review simulation.

| Check | Required | Pass Condition |
|-------|----------|----------------|
| IMRAD structure complete | Yes | All four sections (Introduction, Methods, Results, Discussion) present with substantive content |
| Methods section reproducible | Yes | Contains software versions, statistical parameters, sample sizes |
| Results match analysis outputs | Yes | All figures/tables in manuscript reference existing `04_Outputs/` files |
| Citation-map alignment | Yes | Every in-text citation has bib entry and vice versa |
| Manuscript language consistent | Yes | Chinese body, English figure/table labels |

**Gate passage**: All checks pass.

**Failure action**: Return to Phase 3. Specify which sections need revision.

---

### Gate 4: Submission Gate (Phase 4 → Submit)

**Purpose**: Manuscript meets journal submission requirements.

| Check | Required | Pass Condition |
|-------|----------|----------------|
| IMRAD structure complete | Yes | All sections present with substantive content |
| Reporting standard checklist | Yes | STROBE/CONSORT/TRIPOD checklist completed |
| All figures ≥300 DPI (FIGURE_DPI) | Yes | No figure below threshold |
| English figure/table labels | Yes | All axis labels, legends, annotations in English |
| Manuscript language consistent | Yes | Chinese manuscript body, English figures/tables |
| All citations have DOIs | Yes | Every reference entry has valid DOI |
| Citation-map alignment | Yes | Every in-text citation has bib entry and vice versa |
| Cover letter complete | Yes | Addresses novelty, significance, conflict of interest |
| Simulated peer review | Yes | review_v1.md exists with response letter |
| No AI-template patterns | Yes | Humanizer checklist all clear |

**Gate passage**: All checks pass.

**Failure action**: Return to Phase 3/4. Specify which items need revision.

---

## Gate Enforcement Protocol

1. **Automated first**: Run automated checks (file existence, line counts, grep patterns) before manual review
2. **Decision checkpoint**: Present gate results to user with pass/fail status
3. **User signoff**: Even if all automated checks pass, user must confirm gate passage
4. **Record in milestone**: Gate passage recorded in MILESTONE.md with timestamp
5. **No skipping**: A failed gate blocks the next phase regardless of partial completion

---

## Gate Override

In exceptional cases, a gate can be overridden with:

1. User explicitly requests override
2. Written justification for why the check can be deferred
3. Target phase number where the deferred check will be resolved
4. Override recorded in MILESTONE.md with `OVERRIDE` tag

Overrides are NOT allowed for:
- Gate 1 (IRB/Ethics) — no exceptions
- Data de-identification check — no exceptions
