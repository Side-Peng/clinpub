# CLAUDE.md — clinpub

This file provides guidance to Claude Code when working with the `clinpub` project.

## Overview

`clinpub` is a structured clinical data analysis and publication pipeline. It acts as a **senior medical statistician + academic writing consultant**, processing patient-level data through 5 phases to produce publication-ready manuscripts targeting SCI Q1/Q2 journals.

## Architecture

The project follows the GSD (Get Shit Done) layered architecture:

```
commands/clinpub/*.md → Thin entry points (user-facing)
agents/*.md            → Specialized AI agent role cards (7 agents)
pipeline/
  workflows/*.md       → Phase orchestration logic
  references/*.md      → Reference documents (standards, methods, patterns, gates)
  templates/*.md       → Study type templates + project config + verification
  contexts/*.md        → Context configurations
scripts/*.py           → Tool scripts (data profiling, PDF reading)
hooks/*.js/*.sh        → Claude Code hooks (workflow guard, phase boundary, prompt guard)
```

## Key Directory Reference

| Path | Purpose |
|------|---------|
| `commands/clinpub/clinpub.md` | Main pipeline entry point |
| `commands/clinpub/data2idea.md` | Topic mining entry point |
| **Agents** | |
| `agents/analyst-agent.md` | R/Python statistician agent |
| `agents/reference-agent.md` | Literature search agent |
| `agents/writer-agent.md` | Manuscript writing agent |
| `agents/topic-miner-agent.md` | Topic mining agent (data2idea) |
| `agents/clinpub-planner.md` | Research analysis planning agent |
| `agents/clinpub-executor.md` | Analysis execution agent (atomic commits) |
| `agents/clinpub-verifier.md` | Statistical verification agent (adversarial) |
| **Pipeline** | |
| `pipeline/workflows/` | Phase 0-4 orchestration + data2idea |
| `pipeline/references/analysis_methods.md` | Statistical method specifications |
| `pipeline/references/journal_standards.md` | SCI Q1/Q2 publication standards |
| `pipeline/references/r_patterns.md` | R visualization patterns |
| `pipeline/references/checkpoints.md` | Checkpoint & milestone protocol |
| `pipeline/references/gates.md` | Quality gates (IRB, data, analysis, submission) |
| `pipeline/references/verification-patterns.md` | Statistical verification patterns |
| `pipeline/references/agent-contracts.md` | Agent role contracts |
| `pipeline/references/mandatory-initial-read.md` | Mandatory initial context loading |
| `pipeline/templates/study_types/` | RCT, cohort, case_control, cross_sectional, descriptive |
| `pipeline/templates/milestone.md` | Phase gate review template |
| `pipeline/templates/UAT.md` | User acceptance testing template |
| `pipeline/templates/VALIDATION.md` | Statistical validation checklist |
| `pipeline/templates/verification-report.md` | Reproducibility verification report |
| `pipeline/templates/spec.md` | Analysis specification template |
| `pipeline/templates/context.md` | Research context template |
| `pipeline/contexts/` | Analysis and writing context configs |
| **Hooks** | |
| `hooks/clinpub-workflow-guard.js` | Enforce analysis workflow phase ordering |
| `hooks/clinpub-phase-boundary.sh` | Phase boundary prerequisite checks |
| `hooks/clinpub-prompt-guard.js` | Data file prompt injection detection |
| **Other** | |
| `commands/clinpub/milestone.md` | Milestone review command |
| `scripts/` | Python tool scripts |
| `.claude/settings.json` | Hook registration |

## Agent Routing

| Task | Agent |
|------|-------|
| Data cleaning, statistical analysis, figures | `analyst-agent` |
| Literature search, citation management | `reference-agent` |
| Manuscript drafting, peer review simulation | `writer-agent` |
| Topic mining from data | `topic-miner-agent` |
| Research analysis planning (PLAN.md creation) | `clinpub-planner` |
| Analysis execution with atomic commits | `clinpub-executor` |
| Statistical verification (adversarial) | `clinpub-verifier` |

## Dependencies

- **R**: dplyr, tidyr, stringr, readr, readxl, survival, lme4, glmnet, pROC, gtsummary, flextable, openxlsx, ggplot2, ggpubr, patchwork, survminer, ggsurvfit, ggsignif, here, fs
- **Python**: pandas, numpy, requests, openpyxl
- **Claude Code skills**: ncbi-search (文献检索，用户自行安装), pdf-reader
- **Env vars**: `NCBI_API_KEY` (optional, improves PubMed rate)
