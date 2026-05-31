# Codebase Structure

**Analysis Date:** 2026-05-05

## Directory Layout

```
clinpub/                                    # npm package root (clinpub-cc v1.1.0)
├── .github/
│   └── workflows/
│       ├── release.yml                     # GitHub Release automation
│       └── test.yml                        # CI test workflow
├── .clinpub/                              # Project management artifacts
│   ├── PROJECT.md                          # Project vision and requirements
│   ├── ROADMAP.md                          # 8-phase roadmap
│   ├── STATE.md                            # Current progress tracking
│   ├── config.json                         # Workflow preferences
│   ├── research/                           # Domain research docs
│   └── codebase/                           # Codebase analysis documents (this directory)
├── agents/                                 # 7 AI agent role contracts
│   ├── analyst-agent.md                    # R/Python statistician
│   ├── reference-agent.md                  # Literature search specialist
│   ├── writer-agent.md                     # IMRAD manuscript drafter
│   ├── topic-miner-agent.md                # Data-driven topic discovery
│   ├── clinpub-planner.md                  # Analysis PLAN.md creator
│   ├── clinpub-executor.md                 # Analysis executor (atomic commits)
│   └── clinpub-verifier.md                 # Cross-phase adverserial verifier
├── bin/
│   └── install.js                          # npm CLI installer (500 lines)
├── commands/
│   └── clinpub/                            # 8 slash command entry points
│       ├── clinpub.md                      # Main: full 5-phase pipeline
│       ├── init-project.md                 # Phase 0: project init
│       ├── data-prep.md                    # Phase 1: data cleaning
│       ├── analysis.md                     # Phase 2: statistical analysis
│       ├── writing.md                      # Phase 3: manuscript writing
│       ├── review.md                       # Phase 4: peer review
│       ├── milestone.md                    # Phase gate review
│       └── data2idea.md                    # Topic mining (standalone)
├── docs/
│   └── getting-started.md                  # Tutorial and quick start guide
├── examples/
│   ├── 04-INTEGRATION-CHECKLIST.md         # E2E integration test checklist
│   ├── project_config.example.yml          # Example project config
│   └── sample_data/                        # Sample datasets (if any)
├── hooks/                                  # 3 Claude Code PreToolUse hooks
│   ├── clinpub-workflow-guard.js           # Phase ordering enforcement (Write/Edit)
│   ├── clinpub-phase-boundary.sh           # Milestone prerequisite check (Bash)
│   └── clinpub-prompt-guard.js             # Prompt injection detection (Read)
├── pipeline/
│   ├── workflows/                          # 7 phase orchestration workflows
│   │   ├── init-project.md                 # Phase 0
│   │   ├── data-prep.md                    # Phase 1
│   │   ├── analysis.md                     # Phase 2
│   │   ├── writing.md                      # Phase 3
│   │   ├── review.md                       # Phase 4
│   │   ├── milestone.md                    # Phase gate verification
│   │   └── data2idea.md                    # Topic mining workflow
│   ├── references/                         # 9 reference knowledge documents
│   │   ├── agent-contracts.md              # 7 agent contracts + read/write matrix
│   │   ├── analysis_methods.md             # Statistical method reference library
│   │   ├── checkpoints.md                  # Checkpoint & milestone protocol
│   │   ├── gates.md                        # 4 quality gates
│   │   ├── journal_standards.md            # SCI Q1/Q2 publication standards
│   │   ├── manifest-format.md              # MANIFEST.yaml contract specification
│   │   ├── mandatory-initial-read.md       # Agent context loading protocol
│   │   ├── r_patterns.md                   # R visualization core standards
│   │   └── verification-patterns.md        # 15 verification patterns
│   ├── templates/                          # 15 template files
│   │   ├── context.md                      # Research context template
│   │   ├── idea_report.md                  # Topic mining report template
│   │   ├── milestone.md                    # Phase gate milestone report
│   │   ├── project.md                      # PROJECT.md template
│   │   ├── project_config.yml              # project_config.yml template
│   │   ├── roadmap.md                      # ROADMAP.md template
│   │   ├── spec.md                         # Analysis specification template
│   │   ├── state.md                        # STATE.md template
│   │   ├── UAT.md                          # User acceptance testing template
│   │   ├── VALIDATION.md                   # Statistical validation checklist
│   │   ├── verification-report.md          # Reproducibility verification report
│   │   └── study_types/                    # 5 study type templates
│   │       ├── rct.md                      # RCT (CONSORT)
│   │       ├── cohort.md                   # Cohort (STROBE)
│   │       ├── case_control.md             # Case-control (STROBE)
│   │       ├── cross_sectional.md          # Cross-sectional (STROBE)
│   │       └── descriptive.md              # Descriptive (STROBE)
│   └── contexts/                           # Context configuration files
│       ├── analysis.md                     # Analysis context (Phase 2)
│       └── writing.md                      # Writing context (Phase 3)
├── scripts/                                # 5 Python tool scripts
│   ├── data_profiler.py                    # Variable profiling & data quality
│   ├── ncbi_client.py                      # NCBI API client
│   ├── ncbi_search.py                      # PubMed/NCBI search
│   ├── pubmed_search.py                    # PubMed search wrapper
│   └── tavily_search.py                    # Tavily web search
├── tests/
│   └── .gitkeep                            # Tests directory (skeleton)
├── bin/install.js                          # (already listed above)
├── CHANGELOG.md                            # Version history
├── CLAUDE.md                               # Project CLAUDE.md
├── INSTALL.md                              # Installation instructions
├── package.json                            # npm package config (node >= 22)
├── README.md                               # Project README
└── SKILL.md                                # Claude Code skill definition
```

## Directory Purposes

**`commands/clinpub/`:**
- Purpose: User-facing entry points for all pipeline operations
- Contains: 8 Markdown files with YAML frontmatter (name, description, allowed-tools)
- Key files: `clinpub.md` (main pipeline entry)
- Naming: Hyphenated lowercase matching Claude Code command names

**`agents/`:**
- Purpose: Specialized AI agent role contracts defining scope, inputs, outputs
- Contains: 7 Markdown files, one per agent
- Key files: All 7 agents are equally important
- Naming: `{role}-agent.md` (e.g., `analyst-agent.md`, `clinpub-planner.md`)

**`pipeline/workflows/`:**
- Purpose: Phase orchestration logic with step-by-step process definitions
- Contains: 7 Markdown files with `<process>` blocks
- Key files: All workflow files
- Naming: Lowercase hyphenated, matching phase names (e.g., `data-prep.md`, `init-project.md`)

**`pipeline/references/`:**
- Purpose: Domain knowledge references and governance documentation
- Contains: 9 Markdown + YAML files
- Key files: `agent-contracts.md` (agent system), `gates.md` (quality governance), `analysis_methods.md` (statistical knowledge)

**`pipeline/templates/`:**
- Purpose: Reusable templates for project artifacts and study types
- Contains: 10 root-level templates + 5 study type templates in `study_types/`
- Key files: `project_config.yml` (project configuration), `milestone.md` (phase gate report)

**`hooks/`:**
- Purpose: PreToolUse hooks for pipeline governance
- Contains: 2 JavaScript hooks + 1 Bash hook
- Key files: All 3 hooks

**`scripts/`:**
- Purpose: Python tool scripts for data operations and search
- Contains: 5 Python scripts
- Key files: `data_profiler.py` (variable profiling), `ncbi_search.py` (literature search)

**`bin/`:**
- Purpose: npm package binary
- Contains: `install.js` (500 lines) — installer, hook registrar, environment checker

**`docs/`:**
- Purpose: User documentation
- Contains: `getting-started.md` (tutorial) — currently a single file

**`.clinpub/`:**
- Purpose: GSD project management artifacts
- Contains: PROJECT.md, ROADMAP.md, STATE.md, config.json, research/, codebase/

## Key File Locations

**Entry Points:**
- `commands/clinpub/clinpub.md`: Main pipeline entry
- `commands/clinpub/data2idea.md`: Topic mining entry
- `commands/clinpub/milestone.md`: Phase gate review entry
- `bin/install.js`: npm installer entry
- `SKILL.md`: Claude Code skill registration

**Configuration:**
- `package.json`: npm package configuration (name, version, bin, scripts, engines)
- `pipeline/templates/project_config.yml`: Project configuration template (used in Phase 0)
- `.claude/settings.json`: Hook registration (generated by installer)

**Core Logic:**
- `commands/clinpub/*.md`: 8 command entries
- `pipeline/workflows/*.md`: 7 workflow orchestrations
- `pipeline/references/agent-contracts.md`: Agent contract definitions
- `pipeline/references/gates.md`: Quality gate definitions
- `pipeline/references/checkpoints.md`: Checkpoint protocol

**Agent Contracts:**
- `pipeline/references/agent-contracts.md`: Complete contract definitions for all 7 agents, including read/write matrix

**Testing:**
- `tests/.gitkeep`: Tests directory exists but is a skeleton
- `.github/workflows/test.yml`: CI test workflow

**Scripts:**
- `scripts/data_profiler.py`: Variable profiling (used by topic-miner-agent)
- `scripts/ncbi_search.py`, `scripts/pubmed_search.py`: PubMed search (used by reference-agent)
- `scripts/tavily_search.py`: Web search

**Hooks:**
- `hooks/clinpub-workflow-guard.js`: Phase ordering guard (Write/Edit)
- `hooks/clinpub-phase-boundary.sh`: Phase boundary check (Bash)
- `hooks/clinpub-prompt-guard.js`: Prompt injection detection (Read)

## Naming Conventions

**Files:**
- Commands: `lowercase-with-hyphens.md` (e.g., `data-prep.md`, `init-project.md`)
- Agents: `{role}-agent.md` (e.g., `analyst-agent.md`, `topic-miner-agent.md`)
- Scripts: `snake_case.py` (e.g., `data_profiler.py`, `ncbi_search.py`)
- Hooks: `clinpub-{purpose}.js` or `.sh` (e.g., `clinpub-workflow-guard.js`)

**Directories:**
- Pipeline layers: `pipeline/{category}/` where category is `workflows`, `references`, `templates`, `contexts`
- Commands: `commands/clinpub/` (single namespace directory)
- Agents: `agents/` (flat directory)
- Hooks: `hooks/` (flat directory)
- Scripts: `scripts/` (flat directory)

**Templates (project output directories):**
- Data directories: numbered prefix + descriptive name: `01_RawData`, `02_PreprocessedData`, `03_AnalysisMethods`, `04_Outputs`, `05_Manuscript`
- Planning phase directories: `.clinpub/phases/NN-phase-name/` (e.g., `00-init`, `01-data-prep`, `02-analysis`)
- Method output directories: `NN_MethodName/` (e.g., `01_BaselineTable`, `02_TwoGroupComparison`)

## Where to Add New Code

**New Feature (new phase or sub-workflow):**
1. Command entry: `commands/clinpub/{name}.md` with frontmatter (name, description, allowed-tools)
2. Workflow orchestration: `pipeline/workflows/{name}.md` with `<process>` steps
3. Agent (if new role needed): `agents/{name}-agent.md` with contract following `agent-contracts.md` format
4. Update `pipeline/references/agent-contracts.md` with new agent's read/write matrix entry

**New Script/Tool:**
- Python scripts: `scripts/{name}.py`
- Update `requirements.txt` or note in SKILL.md

**New Hook:**
- Hook file: `hooks/clinpub-{purpose}.js` or `.sh`
- Registration: update `bin/install.js` (hook definition array around line 149)
- Update `pipeline/references/mandatory-initial-read.md` if hook affects agent behavior

**New Study Type:**
- Template: `pipeline/templates/study_types/{name}.md`
- Update project_config.yml template to include new type in study_type options

**New Template:**
- Template file: `pipeline/templates/{name}.md`
- Follow existing template structure (YAML frontmatter, sections)

**New Tests:**
- Test files: `tests/` directory (currently a skeleton, `.gitkeep` only)
- Follow naming pattern: `{module}.test.cjs` (Node.js test runner)
- CI config: `.github/workflows/test.yml`

## Special Directories

**`.clinpub/`:**
- Purpose: GSD project management artifacts (PROJECT.md, ROADMAP.md, STATE.md)
- Generated: No (manually maintained by orchestrator)
- Committed: Yes

**`01_RawData/`, `02_PreprocessedData/`, etc. (project output):**
- Purpose: Pipeline data directories (created during Phase 0 init)
- Generated: Yes (by pipeline execution)
- Committed: No (project-specific data)
- Note: These directories do NOT exist in the repository (they are created at project init time)

**`node_modules/`:**
- Purpose: npm dependencies
- Generated: Yes (by npm install)
- Committed: No (in `.gitignore`)

## Structural Observations

### Strengths
1. **Clear layer separation**: Commands (entry) -> Workflows (orchestration) -> Agents (execution) -> Scripts (tools). Each layer has a well-defined responsibility.
2. **Consistent file naming**: Command files match runtime names, agent files follow `{role}-agent.md` pattern, workflows match phase names.
3. **Flat directory structure**: No deep nesting. Each major category (agents, hooks, scripts, commands) is a flat directory.
4. **Self-contained references**: All domain knowledge is in `pipeline/references/`, all templates in `pipeline/templates/`.
5. **Numbered output directories**: The `XX_Name/` pattern in project output ensures consistent ordering.

### Weaknesses
1. **Tests directory is a skeleton**: `/tests/` contains only `.gitkeep`. No test infrastructure beyond CI workflow. Testing gaps exist.
2. **Dual agent documentation**: Agent contracts exist in both `agents/*.md` (individual files) and `pipeline/references/agent-contracts.md` (consolidated). Risk of drift.
3. **Hook configuration embedded in installer**: Hook file paths and matchers are hard-coded in `bin/install.js` (lines 149-167). Adding/removing hooks requires updating both the hook file and the installer logic.
4. **docs/ directory is thin**: Only `getting-started.md` exists. Missing API reference, agent reference, or hook reference documentation.
5. **No TypeScript/type system**: Entirely Markdown-based architecture. No type checking, no import validation. Contracts are human-enforced.
6. **examples/sample_data/ directory exists but may be empty**: The directory structure exists but lacks populated sample data files for tutorials.

---

*Structure analysis: 2026-05-05*
