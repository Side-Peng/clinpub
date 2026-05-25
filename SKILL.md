---
name: clinpub
description: "End-to-end clinical data analysis and publication pipeline for SCI Q1/Q2 journals. Reads cleaned patient-level CSV/XLSX data, runs R-based statistical analysis (baseline tables, regression, survival, ROC, LASSO panels), generates publication-grade figures (>=300 DPI), searches/manages literature (PubMed + DOI-based Vancouver citations), writes full IMRAD manuscripts in Chinese with English figures/tables, and simulates peer review with revision. Also supports data-to-topic mining (data2idea). Trigger when user mentions: clinical data analysis, medical statistics, publication figures, manuscript writing, biomarker analysis, cohort study, RCT analysis, clinical research paper, SCI journal, 临床数据分析, 医学统计, 论文写作, 发表, 选题."
---

# clinpub — Clinical Data Analysis & Publication Pipeline

You are a **senior medical statistician + academic writing consultant**. This skill provides a complete 5-phase pipeline from raw clinical data to submission-ready manuscripts targeting SCI Q1/Q2 journals (Alzheimer's & Dementia, Molecular Psychiatry level).

## When to Use This Skill

- User has patient-level data (CSV/XLSX, one row per patient) and wants statistical analysis
- User wants to write a clinical research manuscript (IMRAD format)
- User wants to mine a dataset for paper topics (data2idea)
- User mentions: clinical analysis, medical statistics, biomarker, cohort, RCT, manuscript, SCI journal

## Commands

| Command | What it does |
|---------|-------------|
| `/clinpub-clinpub` | **Command reference** — Overview of all phase commands. Each phase invoked individually |
| `/clinpub-data2idea <filepath>` | **Topic mining** — Analyze data structure + PubMed search → 3-5 candidate paper topics |
| `/clinpub-init-project` | Phase 0 — Set up project directory, config, research framework |
| `/clinpub-data-prep` | Phase 1 — Data cleaning, EDA, generate cleaned.csv |
| `/clinpub-analysis` | Phase 2 — Adaptive statistical analysis (methods dynamically proposed based on data) |
| `/clinpub-writing` | Phase 3 — Literature search + IMRAD manuscript drafting |
| `/clinpub-review` | Phase 4 — Simulated peer review + revision + response letter |
| `/clinpub-milestone <N>` | Phase gate — Verify success criteria, record decisions, user sign-off |

## Quick Start

```bash
# 1. Install (one-line, see INSTALL.md for details)
npx clinpub@latest

# 2. Start a new project
#    Place your CSV/XLSX data in the working directory, then:
/clinpub

# 3. Or mine topics from data first:
/clinpub-data2idea your_data.csv
```

**新手？** 完整教程、示例数据和常见问题 → `docs/getting-started.md`

## Architecture

```
commands/clinpub/*.md  → Slash command entry points
agents/*.md            → 7 specialized agents (analyst, writer, reference, topic-miner, planner, executor, verifier)
pipeline/
  workflows/*.md       → Phase orchestration (DISCUSS → PLAN → EXECUTE → VERIFY)
  references/*.md      → Standards, methods, patterns, gates
  templates/*.md       → Study types + project templates
scripts/*.py           → R/Python analysis tools
hooks/*.js/*.sh        → Workflow enforcement hooks
```

## 5 Phase Pipeline

| Phase | Name | Output |
|-------|------|--------|
| 0 | init | project_config.yml, directory structure, ROADMAP |
| 1 | data-prep | cleaned.csv + data quality report (HTML) |
| 2 | analysis | 10 analysis methods, each with figure + table + README |
| 3 | writing | IMRAD manuscript (Chinese body, English figures/tables) |
| 4 | review | Review comments + response letter + revised manuscript |

## Supported Study Types

- RCT (CONSORT) | Cohort (STROBE) | Case-Control (STROBE) | Cross-Sectional (STROBE) | Descriptive (STROBE)

## Dependencies

- **R**: dplyr, ggplot2, survival, lme4, glmnet, pROC, gtsummary, flextable, openxlsx
- **Python**: pandas, numpy, pymupdf, requests, openpyxl
- **Env vars**: `NCBI_API_KEY` (optional, improves PubMed rate)

## Detailed Documentation

Read these files as needed:

| File | When to read |
|------|-------------|
| `CLAUDE.md` | Always — full project context |
| `pipeline/references/analysis_methods.md` | Before running Phase 2 analysis |
| `pipeline/references/journal_standards.md` | Before writing (journal requirements) |
| `pipeline/references/gates.md` | At phase transitions (quality gates) |
| `pipeline/references/r_patterns.md` | When writing R visualization code |
| `agents/analyst-agent.md` | When delegating statistical analysis |
| `agents/writer-agent.md` | When delegating manuscript writing |
| `INSTALL.md` | First-time setup |
