# ClinPub - Clinical Publication Pipeline

End-to-end clinical data analysis and publication pipeline for SCI Q1/Q2 journals.

## Overview

ClinPub is a structured clinical data analysis and publication pipeline that acts as a senior medical statistician and academic writing consultant. It processes patient-level data through 5 phases to produce publication-ready manuscripts targeting SCI Q1/Q2 journals.

## Pipeline Phases

| Phase | Command | Purpose | Key Output |
|-------|---------|---------|------------|
| 0 | `clinpub:init` | Project initialization or import | `project_config.yml` |
| 1 | `clinpub:data-prep` | Data cleaning and EDA | `cleaned.csv` |
| 2 | `clinpub:analysis` | Statistical analysis | `04_Outputs/` |
| 3 | `clinpub:writing` | IMRAD manuscript writing | `manuscript.md` |
| 4 | `clinpub:review` | Peer review simulation | `final/` |

## Installation

### As Codex Plugin

```bash
# From local path
codex plugin install ./clinpub

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

# Continue one phase at a time...
clinpub:analysis
clinpub:writing
clinpub:review

# Topic mining from data
clinpub:data2idea <file>

# Check phase status
clinpub:milestone <N>

# Auto-advance to next step
clinpub:next-step

# Route to appropriate command
clinpub:do [intent]

# Modify analysis outputs
clinpub:modify [method ID]
```

## Architecture

```
skills/*/SKILL.md          → Skill definitions (11 skills)
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
| Manuscript drafting, peer review simulation | `writer-agent` |
| Topic mining from data | `topic-miner-agent` |
| Research analysis planning | `clinpub-planner` |
| Analysis execution with atomic commits | `clinpub-executor` |
| Statistical verification | `clinpub-verifier` |
| Analysis output modification | `modify-agent` |

## License

MIT

## Author

Side-Peng (1304916798@qq.com)

## Repository

https://github.com/Side-Peng/clinpub
