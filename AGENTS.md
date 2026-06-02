# AGENTS.md — clinpub

## What This Is

A Claude Code **skill package** (npm: `clinpub`). Not a traditional app — `bin/install.js` converts `commands/clinpub/*.md` into Claude Code skills and copies shared resources (agents, pipeline, scripts, hooks) to `~/.claude/clinpub/`.

The `SKILL.md` at root is the Claude Code entry point with trigger descriptions.

## Architecture

```
Commands (commands/clinpub/*.md)  → Slash command entry points
  ↓
Workflows (pipeline/workflows/*.md) → Phase orchestration (DISCUSS→PLAN→EXECUTE→VERIFY)
  ↓
Agents (agents/*.md)               → 8 specialized AI role cards
  ↓
Scripts (scripts/*.py)             → R/Python analysis tools
Hooks (hooks/*.js/*.sh)            → Workflow enforcement
```

Three-layer routing: user invokes command → workflow orchestrates → agent executes with fresh context.

## Critical Constraints

### Code Independence (铁律)

Every R/Python script must be **self-contained**. All variables defined locally, no global state, no cross-file implicit dependencies. This is the #1 gotcha — violating it breaks agent isolation.

```r
# ✓ Correct
data_path <- "01_RawData/data.csv"
# ✗ Wrong
data <- read.csv(global_path)
```

### Phase Ordering Enforcement

Hooks in `hooks/` block writes to directories belonging to future phases. The workflow guard reads `.clinpub/STATE.md` for current phase (`阶段：Phase\s*(\d)`). Always-accessible dirs: `.clinpub`, `scripts`, `hooks`, `pipeline`, `agents`, `commands`.

### Agent Independence

Each agent gets fresh context — no shared memory. Data passes through the filesystem, not in-memory. Agents output standardized `MANIFEST.yaml`.

## Key Files

| File | Why It Matters |
|------|----------------|
| `bin/install.js` | The installer — converts commands→skills, copies resources, registers hooks. Core infrastructure. |
| `SKILL.md` | Claude Code skill entry point with trigger descriptions |
| `CLAUDE.md` | Full project context for Claude Code sessions |
| `pipeline/references/gates.md` | 4 quality gates between phases |
| `pipeline/references/analysis_methods.md` | Statistical method specs (read before Phase 2) |
| `pipeline/references/r_patterns.md` | R visualization patterns |
| `hooks/clinpub-workflow-guard.js` | Phase ordering enforcement logic |
| `scripts/data_profiler.py` | Data profiling for topic mining |

## Commands (9 skills installed)

| Command | Phase | What It Does |
|---------|-------|-------------|
| `/clinpub` | — | Command reference overview |
| `/clinpub-data2idea` | — | Topic mining from data |
| `/clinpub-init-project` | 0 | Project setup, config, research framework |
| `/clinpub-data-prep` | 1 | Data cleaning → cleaned.csv |
| `/clinpub-analysis` | 2 | Statistical analysis (methods proposed dynamically) |
| `/clinpub-writing` | 3 | IMRAD manuscript drafting |
| `/clinpub-review` | 4 | Peer review simulation + revision |
| `/clinpub-milestone` | gate | Phase gate verification with user sign-off |
| `/clinpub-modify` | — | Modify analysis outputs (figure style, method, variables) |

## Agent Routing

| Task | Agent | Language |
|------|-------|----------|
| Data cleaning, stats, figures | `analyst-agent` | R primary |
| Literature search, citations | `reference-agent` | Python |
| Manuscript drafting | `writer-agent` | — |
| Topic mining from data | `topic-miner-agent` | Python |
| Research analysis planning | `clinpub-planner` | — |
| Analysis execution (atomic commits) | `clinpub-executor` | R/Python |
| Statistical verification (adversarial) | `clinpub-verifier` | — |
| Analysis output modification | `modify-agent` | R primary |

## Development

### No Test Runner

`package.json` has empty `scripts: {}`. Tests are documented in `docs/TESTING.md` but run manually (`Rscript tests/test_*.R`, `python -m pytest tests/`). No CI test workflow exists — only `release.yml` for GitHub Releases.

### Commit Convention

```
<type>(<scope>): <subject>
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Release Flow

Tag push (`v*`) triggers `.github/workflows/release.yml` → GitHub Release. npm publish is manual (`npm publish`).

### Dependencies

- **R**: dplyr, tidyr, stringr, readr, readxl, survival, lme4, glmnet, pROC, gtsummary, flextable, openxlsx, ggplot2, ggpubr, patchwork, survminer, ggsurvfit, ggsignif, here, fs
- **Python**: pandas, numpy, pymupdf, requests, openpyxl, tavily-python (see `requirements.txt`)
- **Node**: >= 22.0.0
- **Env vars**: `NCBI_API_KEY` (optional, PubMed rate limit), `TAVILY_API_KEY` (Tavily search)

### External Skills

clinpub depends on Claude Code skills installed separately:
- `ncbi-search` — PubMed literature search (sole search入口 since v1.2)
- `pdf-reader` — PDF full-text reading
- `tavily` — supplementary search

## Quirks

- The `commands/clinpub/do.md` and `commands/clinpub/next-step.md` exist but aren't in the main command table — they're routing/advancement helpers
- `.gitignore` blocks all patient data files (CSV, XLSX, SAV, DTA, SAS7BDAT) — never commit clinical data
- `.clinpub/` is the GSD project state directory (PROJECT.md, ROADMAP.md, STATE.md)
- The hook reads phase from STATE.md using regex `阶段：Phase\s*(\d)` — if you change STATE.md format, update the hook
- Literature search scripts were removed in v1.2 — now uses external `ncbi-search` skill exclusively
