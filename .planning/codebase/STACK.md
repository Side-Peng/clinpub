# Technology Stack

**Analysis Date:** 2026-05-05

## Languages

**Primary (execution):**
- **R >= 4.2** — Statistical analysis execution via `Rscript`. Generates figures, tables, and statistical reports in Phase 2. Referenced in `agents/clinpub-executor.md` and `agents/analyst-agent.md`.
- **Python >= 3.9** — Data profiling (`scripts/data_profiler.py`), PubMed/NCBI searching (`scripts/ncbi_client.py`, `scripts/ncbi_search.py`, `scripts/pubmed_search.py`), Tavily AI search (`scripts/tavily_search.py`).

**Primary (framework/infrastructure):**
- **JavaScript (Node.js >= 22.0.0)** — Installer (`bin/install.js`), hooks (`hooks/clinpub-workflow-guard.js`, `hooks/clinpub-prompt-guard.js`).
- **Shell (Bash)** — Phase boundary hook (`hooks/clinpub-phase-boundary.sh`).
- **Markdown (YAML frontmatter)** — Agent role cards (`agents/*.md`), workflow orchestration (`pipeline/workflows/*.md`), command entry points (`commands/clinpub/*.md`), templates and references (`pipeline/templates/*.md`, `pipeline/references/*.md`). This is the primary "code" of the GSD (Get Shit Done) framework — over 30 `.md` files serve as executable agent instructions.

## Runtime

**Environments:**
| Component | Version | Where Used |
|-----------|---------|------------|
| Node.js | >= 22.0.0 | Hooks, installer (`bin/install.js`) |
| R | >= 4.2 | Analyst Agent (statistical analysis) |
| Python | >= 3.9 | Scripts (profiling, literature search) |
| Claude Code | >= 2.1.88 | Skill host environment |

**Package Managers:**
- **npm** — Node.js packages. Lock file not detected.
- **pip** — Python packages. Requirements file: `requirements.txt`. Lock file not detected.

## Frameworks

**Execution/Orchestration:**
- **GSD Framework** — Custom "Get Shit Done" 5-phase pipeline. Agent-based orchestration via Markdown workflows. Not a traditional framework but the architectural pattern governing all execution.
- **Claude Code Skills System** — Commands registered as Claude Code slash commands via `bin/install.js` converting `commands/clinpub/*.md` into `skills/clinpub-*/SKILL.md` files.

**Testing:**
- **Node.js built-in test runner** (`node --test`) — For JavaScript tests in `tests/*.test.cjs`.
- **pytest** — For Python tests in `tests/test_*.py`. Configured in `.github/workflows/test.yml`.

**CI/CD:**
- **GitHub Actions** — Two workflows: `test.yml` (push/PR), `release.yml` (tag push).

## Key Dependencies

### Python Dependencies (`requirements.txt`)

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | >= 2.0 | Data profiling (`data_profiler.py`), CSV/XLSX reading |
| numpy | >= 1.24 | Numerical computations in data profiling |
| pymupdf | >= 1.23 | PDF reading/full-text extraction from literature |
| requests | >= 2.31 | HTTP client for NCBI E-Utilities API calls |
| openpyxl | >= 3.1 | XLSX file reading |
| tavily-python | >= 0.3 | Tavily AI search client (`tavily_search.py`) |

### R Dependencies (referenced in `README.md`, `SKILL.md`, `pipeline/references/r_patterns.md`)

| Package | Purpose |
|---------|---------|
| dplyr, tidyr, stringr | Data manipulation and cleaning |
| readr, readxl | Data file reading (CSV, XLSX) |
| survival | Survival analysis (KM curves, Cox regression) |
| lme4 | Mixed-effects models (longitudinal/repeated measures) |
| glmnet | LASSO regression (biomarker panel feature selection) |
| pROC | ROC curve analysis (diagnostic performance) |
| gtsummary | Publication-grade baseline tables |
| flextable, openxlsx | Table output to Word/Excel |
| ggplot2, ggpubr, patchwork | Publication-grade figures (>=300 DPI) |
| survminer, ggsurvfit | Survival curve visualization |
| ggsignif | Significance markers on figures |
| here, fs | File path management |

### Node.js Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| clinpub-cc (self) | 1.1.0 | Self-referencing npm package. No external runtime deps. |

The Node.js stack has **zero external runtime dependencies** — only Node.js built-in modules are used (`fs`, `path`, `os`, `readline`, `child_process`).

## Configuration

**Environment:**
- `package.json` — npm package config, scripts, engine requirements, bin entry point.
- `requirements.txt` — Python dependency list.
- `.gitignore` — 19 patterns covering raw data, generated outputs, API keys, R/Python/Node artifacts, OS files.
- `.claude/settings.json` — Created dynamically by installer, registers 3 PreToolUse hooks. Not committed to repo (auto-generated).

**Build/Dev:**
- No build step required (no TypeScript compilation, no bundling).
- `bin/install.js` acts as the installation/activation script.
- CI runs `node --test` and `pytest` directly without transpilation.

## Platform Requirements

**Development (prerequisite check in `bin/install.js` lines 252-323):**
- Node.js >= 22.0.0
- R >= 4.2 (in PATH)
- Python >= 3.9 (in PATH)
- Claude Code >= 2.1.88 (in PATH, optional check)
- OS: Cross-platform (Windows, macOS, Linux). Installer uses `process.platform === 'win32'` branch for `where` vs `which` commands.

**Production:**
- Deployment: npm registry (distribution via `npx clinpub-cc@latest`).
- Runtime: Any machine with Claude Code installed.
- No server/backend required — runs entirely in Claude Code environment.

## Technical Debt

### Detected Issues

**No lock files:** Neither `package-lock.json` nor `requirements.txt` pin down exact dependency versions. `pip install -r requirements.txt` will install whatever satisfies `>=` constraints. Risk of breaking changes on fresh installs.

**No TypeScript/type checking:** All JavaScript files use CommonJS without any type safety. The `scripts/*.py` files have no type stubs or mypy configuration.

**No package.json `files` field refinement:** The `files` field in `package.json` includes 11 top-level items, but `tests/` is not included (intentional for npm publish), while `docs/` and `examples/` are also excluded. This means test execution requires git clone, not just npm install.

**No R package version pinning:** R dependencies are documented in prose (README, SKILL.md) but never pinned to versions. No `renv.lock` or `packrat` configuration.

**Missing lock files for CI:** GitHub Actions workflows install `pytest` via `pip install pytest` without a lockfile, meaning CI and local can differ.

---

*Stack analysis: 2026-05-05*
