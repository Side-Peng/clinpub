# Agent Contracts

> Each clinpub agent has a defined role, scope, inputs, outputs, and completion markers.

---

## Contract Structure

Each agent contract defines:

- **Role**: One-sentence summary of what the agent does
- **Scope**: What the agent is responsible for (and what it is NOT)
- **Inputs**: Files and context the agent reads
- **Outputs**: Files and artifacts the agent produces
- **Communication**: How the agent shares results with other agents
- **Completion markers**: Observable signs that the agent has finished its work

---

## Analyst Agent

| Field | Definition |
|-------|------------|
| **Role** | Senior medical statistician for R/Python data analysis and publication-grade visualization |
| **Scope** | Phase 1 (data prep) + Phase 2 (statistical analysis). NOT responsible for writing or literature. |
| **Inputs** | `01_RawData/*.csv`, `project_config.yml`, `pipeline/references/r_patterns.md`, `pipeline/references/analysis_methods.md` |
| **Outputs** | `02_PreprocessedData/data/cleaned.csv`, `02_PreprocessedData/reports/data_quality.html`, `04_Outputs/XX_MethodName/` (figures + tables), `03_AnalysisMethods/XX_MethodName/README.md` |
| **Communication** | Writes to filesystem only. No direct agent-to-agent messaging. |
| **Completion markers** | `cleaned.csv` exists, each method directory has figure + table + README, all figures ≥300 DPI (FIGURE_DPI) |

---

## Reference Agent

| Field | Definition |
|-------|------------|
| **Role** | Literature search and citation management specialist |
| **Scope** | PubMed/NCBI search, reference organization, citation mapping. NOT responsible for writing manuscript text. |
| **Inputs** | `project_config.yml` (study topic, keywords), user-provided seed papers |
| **Outputs** | `Reference/references.bib`, `Reference/citation_map.md`, `Reference/literature_notes/` |
| **Communication** | Writes to `Reference/`. Writer Agent reads from `Reference/`. |
| **Completion markers** | `references.bib` has >= 20 entries, `citation_map.md` maps each reference to manuscript section, all entries have DOIs |

---

## Writer Agent

| Field | Definition |
|-------|------------|
| **Role** | IMRAD manuscript drafting specialist for SCI Q1/Q2 journals |
| **Scope** | Phase 3 (manuscript writing) + Phase 4 (review simulation). NOT responsible for statistical analysis. |
| **Inputs** | `04_Outputs/` (analysis results), `Reference/` (citations), `project_config.yml`, study type template, `pipeline/references/journal_standards.md` |
| **Outputs** | `05_Manuscript/manuscript.md`, `05_Manuscript/abstract.md`, `05_Manuscript/review_v1.md`, `05_Manuscript/response_letter.md`, `05_Manuscript/final/` |
| **Communication** | Reads from `04_Outputs/` and `Reference/`. Writes to `05_Manuscript/`. |
| **Completion markers** | Complete IMRAD structure, all citations have DOIs, Humanizer checklist passed, simulated review completed |

---

## Topic Miner Agent

| Field | Definition |
|-------|------------|
| **Role** | Data-driven research topic discovery from clinical datasets |
| **Scope** | Pre-analysis topic mining (data2idea flow). NOT responsible for executing analysis or writing. |
| **Inputs** | Raw data file (CSV/XLSX), `scripts/data_profiler.py` output |
| **Outputs** | `idea/data_profile.json`, `idea/idea_report.md` (3 candidate topics) |
| **Communication** | Standalone agent. Output feeds into Phase 0 init. |
| **Completion markers** | 3 candidate topics with feasibility scores, variable mapping, and recommended methods |

---

## Clinpub Planner

| Field | Definition |
|-------|------------|
| **Role** | Research analysis planning agent (analogous to gsd-planner) |
| **Scope** | Creates executable phase plans for analysis workflows. NOT responsible for executing analysis. |
| **Inputs** | `project_config.yml`, `.planning/STATE.md`, `.planning/ROADMAP.md`, phase-specific context |
| **Outputs** | `.planning/phases/XX-name/XX-01-PLAN.md` (executable plans with tasks) |
| **Communication** | Plans consumed by clinpub-executor. |
| **Completion markers** | PLAN.md exists with frontmatter, tasks, verification criteria, and success criteria |

---

## Clinpub Executor

| Field | Definition |
|-------|------------|
| **Role** | Analysis execution agent with atomic commits (analogous to gsd-executor) |
| **Scope** | Executes PLAN.md files, creates per-task commits, handles checkpoints. NOT responsible for planning or verification. |
| **Inputs** | PLAN.md from clinpub-planner, `project_config.yml`, `.planning/STATE.md` |
| **Outputs** | Analysis files per plan tasks, SUMMARY.md per plan, updated STATE.md |
| **Communication** | Writes analysis outputs, creates git commits. Results verified by clinpub-verifier. |
| **Completion markers** | All plan tasks committed, SUMMARY.md created with deviation record, STATE.md updated |

---

## Clinpub Verifier

| Field | Definition |
|-------|------------|
| **Role** | Statistical verification agent with adversarial mindset (analogous to gsd-verifier) |
| **Scope** | Goal-backward verification of analysis results. NOT responsible for executing analysis. |
| **Inputs** | SUMMARY.md from clinpub-executor, `pipeline/references/verification-patterns.md`, `pipeline/references/gates.md`, analysis output files |
| **Outputs** | `VERIFICATION.md` with pass/fail verdicts per verification pattern |
| **Communication** | Reads outputs from executor, writes VERIFICATION.md. Orchestrator handles routing. |
| **Completion markers** | VERIFICATION.md exists, all patterns checked, overall status is pass/gaps_found/human_needed |

---

## Cross-Agent Communication Rules

1. **Filesystem-only**: Agents communicate through files, never direct messages
2. **No circular dependencies**: Agent A reads from Agent B's output, never vice versa
3. **Single writer per directory**: Each output directory has exactly one author agent
4. **Shared read, exclusive write**: Multiple agents can read `project_config.yml`, only the orchestrator writes to it
5. **State updates through orchestrator**: Agents do not update STATE.md directly; the orchestrator handles state transitions
