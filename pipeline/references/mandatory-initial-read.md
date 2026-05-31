# Mandatory Initial Read

> Every clinpub agent MUST read this file at the start of execution before performing any action.

---

## Required Context Files

Before any analysis, writing, or planning action, load these files in order:

```bash
PROJECT_DIR=$(pwd)
CONFIG="$PROJECT_DIR/project_config.yml"
STATE="$PROJECT_DIR/.clinpub/STATE.md"
```

### 1. Project Configuration (`project_config.yml`)

Read the full project config to understand:

- **Study type**: RCT / cohort / case-control / cross-sectional / descriptive
- **Variables**: outcome, exposure, covariates, subgroup, time
- **Target journal**: journal name, impact factor tier, reporting standard
- **Analysis methods**: user-confirmed method list with wave assignments
- **Data path**: location of raw and cleaned data files
- **Output settings**: language, figure format, table style

### 2. Pipeline State (`.clinpub/STATE.md`)

Read the state file to understand:

- **Current phase**: which phase the project is in (0-4)
- **Completed milestones**: what has been verified and signed off
- **Pending decisions**: unresolved user decisions
- **Blockers**: any known blockers or missing dependencies

### 3. Phase-Specific Context

Depending on the current phase, also load:

| Phase | Additional Context Files |
|-------|--------------------------|
| Phase 0 — init | `.clinpub/PROJECT.md`, `.clinpub/ROADMAP.md` |
| Phase 1 — data-prep | `01_RawData/data_profile.json`, variable dictionary |
| Phase 2 — analysis | `02_PreprocessedData/data/cleaned.csv` (header only), `03_AnalysisMethods/` 方法说明 list |
| Phase 3 — writing | `Reference/citation_map.md`, `04_Outputs/` directory listing, study type template |
| Phase 4 — review | `05_Manuscript/manuscript.md`, `Reference/references.bib` |

---

## Mandatory Checks

After loading context, verify these before proceeding:

1. **project_config.yml exists** — If missing, error: "Project not initialized. Run `/clinpub init` first."
2. **Current phase is valid** — Cross-reference STATE.md phase against ROADMAP.md
3. **Required data files exist** — Check paths from project_config.yml
4. **Previous phase complete** — Cannot start Phase N without Phase N-1 milestone signoff

---

## Agent Routing

Based on loaded context, determine which agent(s) are needed:

| Task | Agent |
|------|-------|
| Data cleaning, statistical analysis, figures | `analyst-agent` |
| Literature search, citation management | `reference-agent` |
| Manuscript drafting, peer review simulation | `writer-agent` |
| Topic mining from data | `topic-miner-agent` |
| Research planning | `clinpub-planner` |
| Analysis execution with commits | `clinpub-executor` |
| Statistical verification | `clinpub-verifier` |

---

## Error Handling

If any mandatory file is missing or corrupted:

1. **Log the error** with the exact file path
2. **Report to user** with a clear message explaining what is missing
3. **Do NOT proceed** with partial context — clinical analysis requires complete configuration
4. **Suggest remediation**: "Run `/clinpub init` to create project configuration" or "Check `.clinpub/STATE.md` for current phase"
