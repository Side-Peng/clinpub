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
| **Communication** | Writes to filesystem only. No direct agent-to-agent messaging. Writes MANIFEST.yaml in output directories after completion. |
| **Output naming conventions** | Figures: `figure_N.png` (N from 1, sequential per method). Tables: `table_N.docx`. README: must contain `Results` subsection. Data quality report: `data_quality.html`. All outputs in `04_Outputs/XX_MethodName/`. MANIFEST.yaml written to method directory root. |
| **Pre-conditions** | `project_config.yml` exists with confirmed variable mappings and method list. For Phase 2: `02_PreprocessedData/data/cleaned.csv` exists and is validated. |
| **Completion markers** | `cleaned.csv` exists, each method directory has figure + table + README, all figures ≥300 DPI (FIGURE_DPI) |

---

## Reference Agent

| Field | Definition |
|-------|------------|
| **Role** | Literature search and citation management specialist |
| **Scope** | PubMed/NCBI search, reference organization, citation mapping. NOT responsible for writing manuscript text. |
| **Inputs** | `project_config.yml` (study topic, keywords), user-provided seed papers |
| **Outputs** | `Reference/references.bib`, `Reference/citation_map.md`, `Reference/literature_notes/` |
| **Communication** | Writes to `Reference/`. Writer Agent reads from `Reference/`. Writes MANIFEST.yaml in `Reference/` after completion. |
| **Output naming conventions** | `references.bib`: Vancouver format, every entry MUST have DOI. `citation_map.md`: table with PMID, DOI, manuscript section, citation reason, supported argument columns. Literature notes: `Reference/literature_notes/` as individual .md files per paper. |
| **Pre-conditions** | User-confirmed search keywords (from Phase 0 discussion or Phase 3 planning). `NCBI_API_KEY` checked and reported (optional, improves rate limit). |
| **Completion markers** | `references.bib` has >= 20 entries, `citation_map.md` maps each reference to manuscript section, all entries have DOIs |

---

## Writer Agent

| Field | Definition |
|-------|------------|
| **Role** | IMRAD manuscript drafting specialist for SCI Q1/Q2 journals |
| **Scope** | Phase 3 (manuscript writing) + Phase 4 (review simulation). NOT responsible for statistical analysis. |
| **Inputs** | `04_Outputs/` (analysis results), `Reference/` (citations), `project_config.yml`, study type template, `pipeline/references/journal_standards.md` |
| **Outputs** | `05_Manuscript/manuscript.md`, `05_Manuscript/abstract.md`, `05_Manuscript/review_v1.md`, `05_Manuscript/response_letter.md`, `05_Manuscript/final/` |
| **Communication** | Reads from `04_Outputs/` and `Reference/` (validates their MANIFEST.yaml first). Writes to `05_Manuscript/` (writes MANIFEST.yaml after completion). |
| **Output naming conventions** | Chapter drafts: `draft-{chapter}.md` (one per IMRAD section). Compiled manuscript: `manuscript.md`. Review output: `review_v{N}.md`. Response letter: `response_letter.md`. Final: `final/manuscript.md`. |
| **Pre-conditions** | `04_Outputs/` non-empty with at least BaselineTable and GroupComparison outputs. `Reference/citation_map.md` exists with >= 10 entries. `project_config.yml` has target_journal set. |
| **Completion markers** | Complete IMRAD structure, all citations have DOIs, Humanizer checklist passed, simulated review completed |

---

## Topic Miner Agent

| Field | Definition |
|-------|------------|
| **Role** | Data-driven research topic discovery from clinical datasets |
| **Scope** | Pre-analysis topic mining (data2idea flow). NOT responsible for executing analysis or writing. |
| **Inputs** | Raw data file (CSV/XLSX), `scripts/data_profiler.py` output |
| **Outputs** | `idea/data_profile.json`, `idea/idea_report.md` (3 candidate topics), `idea/to_project_config.yml` (after user selects topic) |
| **Communication** | Standalone agent. Writes MANIFEST.yaml in `idea/` after completion. `idea/to_project_config.yml` feeds into Phase 0 init (user renames to `project_config.yml`). |
| **Output naming conventions** | Data profile: `idea/data_profile.md` (human-readable) + `idea/data_profile.json` (structured). Literature scan: `idea/literature_scan.md`. Topic report: `idea/选题报告.md` (Chinese, comparison table at end). Project config: `idea/to_project_config.yml` (auto-generated from selected topic, user renames to `project_config.yml` to start pipeline). |
| **Pre-conditions** | Input data file exists and is readable. Python environment available for `data_profiler.py`. `NCBI_API_KEY` checked before PubMed search. |
| **Completion markers** | 3 candidate topics with feasibility scores, variable mapping, and recommended methods |

---

## Clinpub Planner

| Field | Definition |
|-------|------------|
| **Role** | Research analysis planning agent (analogous to gsd-planner) |
| **Scope** | Creates executable phase plans for analysis workflows. NOT responsible for executing analysis. |
| **Inputs** | `project_config.yml`, `.planning/STATE.md`, `.planning/ROADMAP.md`, phase-specific context |
| **Outputs** | `.planning/phases/XX-name/XX-01-PLAN.md` (executable plans with tasks) |
| **Communication** | Plans consumed by clinpub-executor. Writes MANIFEST.yaml alongside PLAN.md. |
| **Output naming conventions** | Plan file: `{phase-number}-{plan-number}-PLAN.md` (e.g., `02-01-PLAN.md`) in `.planning/phases/XX-name/`. Follows frontmatter format: phase, plan, type, wave, depends_on. |
| **Pre-conditions** | `project_config.yml` exists with confirmed methods. `.planning/STATE.md` and `.planning/ROADMAP.md` exist. User-confirmed method list available. |
| **Completion markers** | PLAN.md exists with frontmatter, tasks, verification criteria, and success criteria |

---

## Clinpub Executor

| Field | Definition |
|-------|------------|
| **Role** | Analysis execution agent with atomic commits (analogous to gsd-executor) |
| **Scope** | Executes PLAN.md files, creates per-task commits, handles checkpoints. NOT responsible for planning or verification. |
| **Inputs** | PLAN.md from clinpub-planner, `project_config.yml`, `.planning/STATE.md` |
| **Outputs** | Analysis files per plan tasks, SUMMARY.md per plan, updated STATE.md |
| **Communication** | Writes analysis outputs, creates git commits. Writes MANIFEST.yaml per output directory. Results verified by clinpub-verifier. |
| **Output naming conventions** | SUMMARY: `{phase-number}-{plan-number}-SUMMARY.md` in `.planning/phases/XX-name/`. Git commits: `analysis({phase}-{plan}): {task description}`. |
| **Pre-conditions** | PLAN.md exists and is parsed. `02_PreprocessedData/data/cleaned.csv` exists. Git repo initialized. |
| **Completion markers** | All plan tasks committed, SUMMARY.md created with deviation record, STATE.md updated |

---

## Clinpub Verifier

| Field | Definition |
|-------|------------|
| **Role** | Cross-phase verification agent with adversarial mindset (analogous to gsd-verifier). Covers Phase 1 (data quality), Phase 2 (statistical), Phase 3 (manuscript) verification. |
| **Scope** | Goal-backward verification of data quality (Phase 1), analysis results (Phase 2), and manuscript integrity (Phase 3). NOT responsible for executing analysis or writing. |
| **Inputs** | SUMMARY.md from clinpub-executor, `pipeline/references/verification-patterns.md`, `pipeline/references/gates.md`, analysis output files, cleaned.csv, manuscript files |
| **Outputs** | `VERIFICATION.md` with pass/fail verdicts per verification pattern |
| **Communication** | Reads outputs from executor, validates MANIFEST.yaml against actual files, writes VERIFICATION.md. Orchestrator handles routing. |
| **Output naming conventions** | Report: `{phase-number}-VERIFICATION.md` in `.planning/phases/XX-name/`. Status: passed / gaps_found / human_needed. |
| **Pre-conditions** | Phase 1: `cleaned.csv` and `data_quality.html` exist. Phase 2: SUMMARY.md and all method output dirs exist. Phase 3: `05_Manuscript/manuscript.md` and `Reference/citation_map.md` exist. |
| **Completion markers** | VERIFICATION.md exists, all patterns checked, overall status is pass/gaps_found/human_needed |

---

## Cross-Agent Communication Rules

1. **Filesystem-only**: Agents communicate through files, never direct messages
2. **No circular dependencies**: Agent A reads from Agent B's output, never vice versa
3. **Single writer per directory**: Each output directory has exactly one author agent
4. **Shared read, exclusive write**: Multiple agents can read `project_config.yml`, only the orchestrator writes to it
5. **State updates through orchestrator**: Agents do not update STATE.md directly; the orchestrator handles state transitions
6. **Manifest contract**: Each agent writes MANIFEST.yaml after completing its outputs. Downstream agents read and validate the manifest before consuming. See `pipeline/references/manifest-format.md`.

---

## Cross-Agent Read/Write Matrix

Shows which agent reads (R) and writes (W) to each directory. Agents only read from directories they have R access to and write to directories they have W access to.

| Agent \ Directory | `01_RawData` | `02_Preprocessed` | `03_AnalysisMethods` | `04_Outputs` | `05_Manuscript` | `Reference/` | `.planning/` | `idea/` |
|---|---|---|---|---|---|---|---|---|
| **analyst-agent** | R | W | W | W | - | - | - | - |
| **reference-agent** | - | - | - | - | - | W | - | - |
| **writer-agent** | - | - | R | R | W | R | - | - |
| **topic-miner-agent** | R | - | - | - | - | - | - | W |
| **clinpub-planner** | - | - | - | - | - | - | W | - |
| **clinpub-executor** | - | R | R | W | - | - | W | - |
| **clinpub-verifier** | - | R | R | R | R | R | R | - |

**Rules:**
- `-` = no access (agent should not read from or write to this directory)
- **R** = read access (agent may read files from this directory)
- **W** = write access (agent may create or modify files in this directory; implies read access)
- Multi-agent write to the same directory is NOT allowed (single writer per directory)
- Exception: `02_Preprocessed` is written by analyst-agent (Phase 1) and read by analyst-agent (Phase 2) — same agent, different phases
