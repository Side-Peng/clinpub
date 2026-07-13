# AGENTS.md

This file provides guidance to Claude Code when working with code in this repository.

## What This Is

A Claude Code **Plugin** (`clinpub`). End-to-end clinical data analysis and publication pipeline for SCI Q1/Q2 journals. Distributed via the Claude Code plugin system (`.claude-plugin/plugin.json`).

## Build, Install & Test Commands

```bash
# Install as Claude Code Plugin (development)
claude --plugin-dir ./clinpub

# Install from marketplace (production)
claude plugin install clinpub

# Validate plugin structure
claude plugin validate . --strict

# Run a single R test
Rscript tests/test_data_cleaning.R
# Run a single Python test
python tests/test_data_profiler.py
# Run all Python tests
python -m pytest tests/

# Install R dependencies
Rscript -e 'install.packages(c("dplyr","tidyr","ggplot2","gtsummary","survival","lme4","glmnet","pROC","ggpubr","patchwork","survminer","ggsurvfit","ggsignif","flextable","openxlsx","here","fs","stringr","readr","readxl","yaml","RColorBrewer","viridis"))'
# Install Python dependencies
pip install -r requirements.txt
```

## Architecture

```
Commands (commands/*.md)           → Slash command entry points (frontmatter + @-references)
  ↓
Workflows (pipeline/workflows/*.md) → Phase orchestration (DISCUSS→PLAN→EXECUTE→VERIFY)
  ↓
Agents (agents/*.md)               → 8 specialized AI role cards (fresh context each)
  ↓
Scripts (scripts/*.py)             → R/Python analysis tools
Hooks (hooks/hooks.json + *.js/*.sh) → Workflow enforcement (phase guard, prompt injection)
```

**Three-layer routing**: user invokes command → workflow orchestrates → agent executes with fresh context.

### Plugin Structure

```
.claude-plugin/plugin.json  → Plugin manifest (identity + metadata)
commands/*.md               → 11 flat command files (auto-discovered by plugin system)
agents/*.md                 → 8 specialized agents (auto-discovered)
hooks/hooks.json            → Declarative hook configuration (3 PreToolUse hooks)
pipeline/                   → Workflows, references, templates (loaded via @./ references)
```

`@./` references in command files resolve to the plugin root at runtime via `${CLAUDE_PLUGIN_ROOT}` substitution.

### Command File Format

Each command file (`commands/*.md`) has YAML frontmatter + structured body:

```yaml
---
name: analysis
description: "..."
argument-hint: ""
allowed-tools:
  - Read
  - Write
  - Bash
---
<objective>...</objective>
<execution_context>
@./pipeline/workflows/analysis.md
@./pipeline/references/r_patterns.md
</execution_context>
<process>Execute the workflow from @./pipeline/workflows/analysis.md</process>
```

The `<execution_context>` block lists files the agent must read before executing. The `@./` prefix means "relative to the clinpub resource root."

### Workflow Orchestration Pattern

Each phase workflow (`pipeline/workflows/*.md`) follows a 4-step pattern:

1. **DISCUSS** — Load data/context, discuss options with user
2. **PLAN** — Create structured plan document in `.clinpub/phases/XX-name/`
3. **EXECUTE** — Run analysis/writing per plan, produce outputs
4. **VERIFY** — Check outputs meet success criteria, write MANIFEST.yaml

Steps are defined in `<step name="..." priority="...">` blocks with YAML-structured outputs.

## Critical Constraints

### Code Independence (铁律)

Every R/Python script must be **self-contained**. All variables defined locally, no global state, no cross-file implicit dependencies. This is the #1 gotcha — violating it breaks agent isolation.

```r
# ✓ Correct
data_path <- "01_RawData/data.csv"
# ✗ Wrong
data <- read.csv(global_path)
```

**Exception**: `_figure_config.R` is the only permitted shared script — all method R scripts `source("04_Outputs/_figure_config.R")` to import visualization configuration (theme, color palette, DPI). This is a "global configuration" pattern, not "global state". The script is generated once during Phase 2 setup from `pipeline/templates/_figure_config.R`.

### Phase Ordering Enforcement

Hooks in `hooks/` block writes to directories belonging to future phases:

- `clinpub-workflow-guard.js` — PreToolUse hook for Write/Edit. Reads `.clinpub/STATE.md` for current phase via regex `阶段：Phase\s*(\d)`. Blocks writes to directories owned by later phases. When `import_mode: true` is present in STATE.md **and** a valid Phase line exists, returns phase 99 (all directories accessible). If STATE.md lacks Phase info (crash residue), falls through to normal phase detection.
- `clinpub-phase-boundary.sh` — PreToolUse hook for Bash. Checks prerequisite milestone completion and data file existence before allowing phase-specific commands. Skips all checks when `import_mode: true` is detected in STATE.md **with** a valid Phase line. Crash residue (import_mode without Phase info) does not bypass checks.
- `clinpub-prompt-guard.js` — PreToolUse hook for Read. Scans data files for prompt injection patterns.

**Always-accessible dirs** (exempt from phase guard): `.clinpub`, `scripts`, `hooks`, `pipeline`, `agents`, `commands`, `.gitignore`, `CHANGELOG.md`, `package.json`, `CLAUDE.md`, `README.md`.

**If you change STATE.md format**, you must also update the regex in `clinpub-workflow-guard.js` (line: `阶段：Phase\s*(\d)`) and the grep patterns in `clinpub-phase-boundary.sh`.

### Agent Independence

Each agent gets fresh context — no shared memory. Data passes through the filesystem, not in-memory. Agents output standardized `MANIFEST.yaml` per output directory. Cross-agent communication is filesystem-only with single-writer-per-directory rule (see `pipeline/references/agent-contracts.md`).

### Project Directory Layout (enforced by hooks)

```
Project_Root/
├── .clinpub/                  # Phase 0 — PROJECT.md / ROADMAP.md / STATE.md
├── 01_RawData/                # Phase 1 — Raw data (read-only)
├── 02_PreprocessedData/       # Phase 1 — cleaned.csv + data quality report
├── 03_AnalysisMethods/        # Phase 2 — Method code + 方法说明 docs
├── 04_Outputs/                # Phase 2 — Figures + tables + MANIFEST.yaml
├── Reference/                 # Phase 3 — Literature (references.bib, citation_map.md)
├── 05_Manuscript/             # Phase 3-4 — IMRAD drafts, review, final
└── project_config.yml         # Phase 0 — Central config (study type, variables, journal)
```

## Commands (11 plugin commands)

| Command | Phase | What It Does |
|---------|-------|-------------|
| `/clinpub:overview` | — | Command reference overview |
| `/clinpub:data2idea` | — | Topic mining from data |
| `/clinpub:initialize` | 0 | Project setup or import existing project (auto-detects artifacts) |
| `/clinpub:data-prep` | 1 | Data cleaning → cleaned.csv |
| `/clinpub:analysis` | 2 | Statistical analysis (methods proposed dynamically) |
| `/clinpub:writing` | 3 | IMRAD manuscript drafting |
| `/clinpub:review` | 4 | Peer review simulation + revision |
| `/clinpub:milestone` | gate | Phase gate verification with user sign-off |
| `/clinpub:modify` | — | Modify analysis outputs (figure style, method, variables) |

`commands/do.md` and `commands/next-step.md` are routing/advancement helpers (breakpoint resume and step advancement), not in the main command table.

## Agent Routing

| Task | Agent | Phase | Language | 备注 |
|------|-------|-------|----------|------|
| 数据清洗 + 质量报告 | `analyst-agent` | 1 | R primary | 默认执行者 |
| 方法设计 + 代码执行 | `analyst-agent` | 2 | R primary | 默认执行者 |
| 文献检索 + 引用 | `reference-agent` | 3 | Python | 内置 `scripts/ncbi_search.py` |
| 论文撰写 | `writer-agent` | 3 | — | |
| 选题挖掘 | `topic-miner-agent` | — | Python | |
| 分析规划 | `clinpub-planner` | 2 | — | 可选高级模式 |
| 计划执行 | `clinpub-executor` | 2 | R/Python | 可选高级模式 |
| 统计验证 | `clinpub-verifier` | 1-3 | — | |
| 分析修改 | `modify-agent` | post-2 | R primary | |

## Cross-Agent Communication Rules

1. **Filesystem-only**: Agents communicate through files, never direct messages
2. **No circular dependencies**: Agent A reads from Agent B's output, never vice versa
3. **Single writer per directory**: Each output directory has exactly one author agent
4. **Shared read, exclusive write**: `project_config.yml` is readable by all agents, only the orchestrator writes to it
5. **Manifest contract**: Each agent writes `MANIFEST.yaml` after completing outputs. Downstream agents validate the manifest before consuming. See `pipeline/references/manifest-format.md`.

## Key Pipeline Reference Files

| File | When to Read |
|------|-------------|
| `pipeline/references/analysis_methods.md` | Before running Phase 2 statistical analysis |
| `pipeline/references/journal_standards.md` | Before Phase 3 writing (journal requirements) |
| `pipeline/references/gates.md` | At phase transitions (4 quality gates: IRB, data, analysis, submission) |
| `pipeline/references/r_patterns.md` | When writing R visualization code (theme_pub, KM curves, heatmap) |
| `pipeline/templates/_figure_config.R` | Phase 2 setup: shared figure config template (copied to `04_Outputs/_figure_config.R`) |
| `pipeline/references/agent-contracts.md` | Agent roles, I/O contracts, read/write matrix |
| `pipeline/references/mandatory-initial-read.md` | Required context loading sequence for every agent |
| `pipeline/references/comparison-methods.md` | Group comparison decision tree (2-group, 3+ group, paired) |
| `pipeline/references/import-heuristics.md` | When importing existing projects (file role inference rules) |
| `agents/analyst-agent.md` | When delegating statistical analysis |
| `agents/writer-agent.md` | When delegating manuscript writing |

## Dependencies

- **R**: dplyr, tidyr, stringr, readr, readxl, survival, lme4, glmnet, pROC, gtsummary, flextable, openxlsx, ggplot2, ggpubr, patchwork, survminer, ggsurvfit, ggsignif, here, fs, yaml, RColorBrewer, viridis
- **Python**: pandas, numpy, requests, openpyxl (see `requirements.txt`)
- **Node**: >= 22.0.0
- **Env vars**: `NCBI_API_KEY` (optional, PubMed rate limit), `TAVILY_API_KEY` (Tavily search), `UNPAYWALL_EMAIL` (Unpaywall PDF access)

## External Skills

clinpub depends on Claude Code skills installed separately:
- `pdf-reader` — PDF full-text reading
- `tavily` — supplementary search

## Quirks

- `.gitignore` blocks all patient data files (CSV, XLSX, SAV, DTA, SAS7BDAT) — never commit clinical data
- `.clinpub/` is the GSD project state directory (PROJECT.md, ROADMAP.md, STATE.md)
- The hook reads phase from STATE.md using regex `阶段：Phase\s*(\d)` — if you change STATE.md format, update the hook
- Literature search is native since v2.1 — `scripts/ncbi_search.py` is vendored from github.com/Side-Peng/ncbi-search (MIT)
- Commit convention: `<type>(<scope>): <subject>` — Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
