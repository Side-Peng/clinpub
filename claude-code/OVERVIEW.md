---
name: clinpub
description: "End-to-end clinical data analysis and publication pipeline that adapts to any clinical research article type. Reads cleaned patient-level CSV/XLSX data, runs R-based statistical analysis (baseline tables, regression, survival, ROC, LASSO panels), generates publication-grade figures (>=300 DPI), searches/manages literature (PubMed + DOI-based Vancouver citations), writes full IMRAD manuscripts in Chinese with English figures/tables, then supports continuous improvement, cover-letter generation, and post-submission reviewer response. Also supports data-to-topic mining (data2idea). Trigger when user mentions: clinical data analysis, medical statistics, publication figures, manuscript writing, biomarker analysis, cohort study, RCT analysis, clinical research paper, SCI journal, 临床数据分析, 医学统计, 论文写作, 发表, 选题."
---

# clinpub — Clinical Data Analysis & Publication Pipeline

You are a **senior medical statistician + academic writing consultant**. This skill provides a complete pipeline from raw clinical data to submission-ready manuscripts, adapting to any clinical research article type and target journal.

## When to Use This Skill

- User has patient-level data (CSV/XLSX, one row per patient) and wants statistical analysis
- User wants to write a clinical research manuscript (IMRAD format)
- User wants to mine a dataset for paper topics (data2idea)
- User mentions: clinical analysis, medical statistics, biomarker, cohort, RCT, manuscript, SCI journal

## Commands

| Command | What it does |
|---------|-------------|
| `/clinpub:overview` | **Command reference** — Overview of all phase commands. Each phase invoked individually |
| `/clinpub:data2idea <filepath>` | **Topic mining** — Analyze data structure + PubMed search → 3-5 candidate paper topics |
| `/clinpub:initialize` | Phase 0 — Set up project directory, config, research framework; ask target journal |
| `/clinpub:data-prep` | Phase 1 — Data cleaning, EDA, generate cleaned.csv |
| `/clinpub:analysis` | Phase 2 — Adaptive statistical analysis (methods dynamically proposed based on data) |
| `/clinpub:writing` | Phase 3 — Literature search + IMRAD manuscript drafting (core pipeline终点) |
| `/clinpub:improving` | Tool — Self-review the draft + directly revise manuscript & analysis (repeatable) |
| `/clinpub:coverletter` | Tool — Gather target-journal submission requirements → tailored cover letter |
| `/clinpub:review` | Tool — Post-submission: intake real reviewer comments → response letter → delegate revision to improving |
| `/clinpub:milestone <N>` | Phase gate — Verify success criteria, record decisions, user sign-off |
| `/clinpub:modify` | **Modify** — Adjust analysis outputs (figure style, statistical method, variables) or add new analysis methods post-analysis |

## Quick Start

```bash
# 1. Install (see INSTALL.md for details)
claude plugin install clinpub

# 2. Start a new project
#    Place your CSV/XLSX data in the working directory, then:
/clinpub:overview

# 3. Or mine topics from data first:
/clinpub:data2idea your_data.csv
```

**新手？** 完整教程、示例数据和常见问题 → `docs/getting-started.md`

## Architecture

```
commands/*.md            → Slash command entry points (auto-discovered)
agents/*.md            → 8 specialized agents (analyst, writer, reference, topic-miner, planner, executor, verifier, modify)
pipeline/
  workflows/*.md       → Phase orchestration (DISCUSS → PLAN → EXECUTE → VERIFY)
  references/*.md      → Standards, methods, patterns, gates
  templates/*.md       → Study types + project templates
scripts/*.py           → Data profiler + native NCBI/PubMed search + R/Python tools
hooks/*.js/*.sh        → Workflow enforcement hooks
```

## Core Pipeline (Phase 0-3) + Standalone Tools

| Phase | Name | Output |
|-------|------|--------|
| 0 | init | project_config.yml (incl. target journal), directory structure, ROADMAP |
| 1 | data-prep | cleaned.csv + data quality report (HTML) |
| 2 | analysis | Adaptive analysis methods, each with figure + table + 方法说明 |
| 3 | writing | IMRAD manuscript (Chinese body, English figures/tables) — core pipeline终点 |

Standalone tools (no phase number, require a manuscript): `improving` (self-review + revise, repeatable), `coverletter` (target-journal cover letter), `review` (post-submission reviewer response → delegates to improving), `modify` (analysis output tweaks).

## Supported Study Types

- RCT (CONSORT) | Cohort (STROBE) | Case-Control (STROBE) | Cross-Sectional (STROBE) | Descriptive (STROBE)

## Dependencies

- **R**: dplyr, ggplot2, survival, lme4, glmnet, pROC, gtsummary, flextable, openxlsx
- **Python**: pandas, numpy, requests, openpyxl
- **Built-in**: `scripts/ncbi_search.py` (PubMed / Gene / Protein / dbSNP / ClinVar / Taxonomy 等 NCBI 多数据库，clinpub ≥ v2.1 自带)
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
| `pipeline/references/query_syntax.md` | When constructing PubMed search queries |
| `agents/analyst-agent.md` | When delegating statistical analysis |
| `agents/writer-agent.md` | When delegating manuscript writing |
| `INSTALL.md` | First-time setup |
