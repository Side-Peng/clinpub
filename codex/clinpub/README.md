# ClinPub - Clinical Publication Pipeline

End-to-end clinical data analysis and publication pipeline. Adapts to any clinical research article type.

## Overview

ClinPub is a structured clinical data analysis and publication pipeline that acts as a senior medical statistician and academic writing consultant. Core pipeline Phase 0-3 processes patient-level data through initialization, data cleaning, adaptive statistical analysis, and IMRAD manuscript writing; standalone tools handle manuscript improvement, cover-letter generation, and post-submission reviewer response.

## Pipeline Phases

| Phase | Command | Purpose | Key Output |
|-------|---------|---------|------------|
| 0 | `clinpub:init` | Project initialization or import (target journal explicitly asked) | `project_config.yml` |
| 1 | `clinpub:data-prep` | Data cleaning and EDA | `cleaned.csv` |
| 2 | `clinpub:analysis` | Statistical analysis | `04_Outputs/` |
| 3 | `clinpub:writing` | IMRAD manuscript writing (core pipeline end) | `manuscript.md` |

## Standalone Tools

Invocable anytime the prerequisite exists (do not occupy a phase number):

| Tool | Purpose | Key Output |
|------|---------|------------|
| `clinpub` | **Hub**: status / `help` / `next` (gate verify + advance) / intent routing | — |
| `clinpub:improving` | Self-review draft → revision plan → direct revision (text + analysis re-run) | updated `sections/*.md` + reassembled `manuscript.md` |
| `clinpub:coverletter` | Tailored submission cover letter from target-journal requirements | `cover_letter.md` |
| `clinpub:review` | Post-submission: real reviewer comments → response letter + revision | `final/` |
| `clinpub:modify` | Modify completed analyses or add new analysis methods | updated `04_Outputs/` + `ANALYSIS_LOG` |
| `clinpub:data2idea` | Topic mining from data | idea report |

## Installation

### As Codex Plugin

```bash
# From local path (run from the repository root)
codex plugin install ./codex/clinpub

# From marketplace
codex plugin install clinpub
```

### Dependencies

**R**: dplyr, tidyr, stringr, readr, readxl, survival, lme4, glmnet, pROC, gtsummary, flextable, openxlsx, ggplot2, ggpubr, patchwork, survminer, ggsurvfit, ggsignif, here, fs, yaml, RColorBrewer, viridis

**Python**: pandas, numpy, requests, openpyxl (see `requirements.txt`)

**Environment Variables**:
- `NCBI_API_KEY` (optional, improves PubMed rate)
- `TAVILY_API_KEY` (Tavily search)
- `UNPAYWALL_EMAIL` (Unpaywall PDF access)

## Usage

```bash
# Start with Phase 0
clinpub:init

# After Phase 0 completes and user signs off, proceed to Phase 1
clinpub:data-prep

# Continue one phase at a time until the manuscript is drafted
clinpub:analysis
clinpub:writing

# After drafting, use standalone tools as needed
clinpub:improving
clinpub:coverletter
clinpub:review

# Topic mining from data
clinpub:data2idea <file>

# Check status / view reference
clinpub
clinpub help

# Verify the gate and advance to the next phase
clinpub next

# Route to appropriate command
clinpub [intent]

# Modify analysis outputs or add new analysis methods
clinpub:modify [method ID]
```

## Architecture

```
skills/*/SKILL.md          → Skill definitions (10 skills)
agents/*.md                → Specialized AI agent role cards (8 agents)
pipeline/
  workflows/*.md           → Phase orchestration logic
  references/*.md          → Reference documents (standards, methods, patterns, gates)
  templates/*.md           → Study type templates + project config + verification
  contexts/*.md            → Context configurations
scripts/*.py               → Tool scripts (data profiling, PubMed search)
hooks/*.js/*.sh            → Hook implementation scripts
.codex-plugin/plugin.json  → Plugin manifest
```

## Agent Routing

| Task | Agent |
|------|-------|
| Data cleaning, statistical analysis, figures | `analyst-agent` |
| Literature search, citation management | `reference-agent` |
| Progressive manuscript drafting (R→M→D→C→I→Abstract), improvement, revision | `writer-agent` |
| Topic mining from data | `topic-miner-agent` |
| Statistical verification | `clinpub-verifier` |
| Analysis output modification / method addition | `modify-agent` |

## License

MIT

## Author

Side-Peng (1304916798@qq.com)

## Repository

https://github.com/Side-Peng/clinpub
