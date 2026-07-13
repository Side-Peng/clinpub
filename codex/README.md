# ClinPub - Clinical Publication Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

End-to-end clinical data analysis and publication pipeline for SCI Q1/Q2 journals.

## 🎯 Overview

ClinPub is a structured clinical data analysis and publication pipeline that acts as a **senior medical statistician + academic writing consultant**. It processes patient-level data through 5 phases to produce publication-ready manuscripts targeting SCI Q1/Q2 journals.

## 🚀 Platform Support

ClinPub is available for multiple AI coding assistants:

| Platform | Status | Location |
|----------|--------|----------|
| **Claude Code** | ✅ Stable | `claude-code/` |
| **OpenAI Codex** | ✅ Stable | `codex/clinpub/` |
| **Qoder** | ✅ Stable | `qoder/` |

## 📦 Installation

### OpenAI Codex

```bash
# From local path
cd codex
codex plugin install ./clinpub

# Or add to personal marketplace
codex plugin marketplace add ./codex
codex plugin install clinpub
```

### Claude Code

```bash
# Install as Claude Code Plugin (development)
claude --plugin-dir ./claude-code

# Install from marketplace (production)
claude plugin install clinpub
```

## 📋 Pipeline Phases

| Phase | Command | Purpose | Key Output |
|-------|---------|---------|------------|
| 0 | `init` | Project initialization or import | `project_config.yml` |
| 1 | `data-prep` | Data cleaning and EDA | `cleaned.csv` |
| 2 | `analysis` | Statistical analysis | `04_Outputs/` |
| 3 | `writing` | IMRAD manuscript writing | `manuscript.md` |
| 4 | `review` | Peer review simulation | `final/` |

### Additional Commands

| Command | Purpose |
|---------|---------|
| `data2idea` | Topic mining from data |
| `milestone` | Phase gate review |
| `next-step` | Auto-advance to next phase |
| `do` | Workspace state router |
| `modify` | Modify analysis outputs |
| `overview` | Command reference |

## 🏗️ Architecture

```
clinpub/
├── .codex-plugin/plugin.json    # Plugin manifest
├── skills/                      # 11 skills
│   ├── clinpub-overview/
│   ├── clinpub-data2idea/
│   ├── clinpub-init/
│   ├── clinpub-data-prep/
│   ├── clinpub-analysis/
│   ├── clinpub-writing/
│   ├── clinpub-review/
│   ├── clinpub-milestone/
│   ├── clinpub-modify/
│   ├── clinpub-do/
│   └── clinpub-next-step/
├── agents/                      # 8 specialized agents
├── pipeline/                    # Workflows, references, templates
├── scripts/                     # Python scripts
├── hooks/                       # Hook implementations
└── requirements.txt             # Python dependencies
```

## 🤖 Agent Routing

| Task | Agent | Phase |
|------|-------|-------|
| Data cleaning, statistical analysis, figures | `analyst-agent` | 1-2 |
| Literature search, citation management | `reference-agent` | 3 |
| Manuscript drafting, peer review simulation | `writer-agent` | 3-4 |
| Topic mining from data | `topic-miner-agent` | - |
| Research analysis planning | `clinpub-planner` | 2 |
| Analysis execution with atomic commits | `clinpub-executor` | 2 |
| Statistical verification | `clinpub-verifier` | 1-3 |
| Analysis output modification | `modify-agent` | post-2 |

## 📚 Dependencies

### R Packages

```r
install.packages(c("dplyr","tidyr","ggplot2","gtsummary","survival","lme4","glmnet","pROC","ggpubr","patchwork","survminer","ggsurvfit","ggsignif","flextable","openxlsx","here","fs","stringr","readr","readxl","yaml","RColorBrewer","viridis"))
```

### Python Packages

```bash
pip install -r requirements.txt
```

### Environment Variables (Optional)

- `NCBI_API_KEY` - Improves PubMed rate limit
- `TAVILY_API_KEY` - For Tavily search
- `UNPAYWALL_EMAIL` - For Unpaywall PDF access

## 📖 Usage Example

```bash
# 1. Initialize project
clinpub:init

# 2. Clean data
clinpub:data-prep

# 3. Run analysis
clinpub:analysis

# 4. Write manuscript
clinpub:writing

# 5. Peer review
clinpub:review

# Or check current status
clinpub:do

# Auto-advance to next step
clinpub:next-step
```

## 🔍 Key Features

- **5-Phase Pipeline**: Structured workflow from data to publication
- **Publication-Grade Output**: ≥300 DPI figures, formatted tables
- **Adaptive Analysis**: Automatically diagnoses data structure and proposes methods
- **IMRAD Writing**: Full manuscript with proper academic structure
- **Peer Review Simulation**: Mock review with revision tracking
- **Topic Mining**: Generate research ideas from raw data
- **Multi-Agent Architecture**: Specialized agents for each task
- **Quality Gates**: Phase transitions require user sign-off

## 📄 Documentation

- [Codex Installation Guide](codex/INSTALL.md)
- [Conversion Summary](codex/CONVERSION_SUMMARY.md)
- [Claude Code Documentation](claude-code/CLAUDE.md)
- [Qoder Documentation](qoder/README.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) for details

## 👨‍💻 Author

**Side-Peng**
- Email: 1304916798@qq.com
- GitHub: [@Side-Peng](https://github.com/Side-Peng)

## 🔗 Links

- [Repository](https://github.com/Side-Peng/clinpub)
- [Issues](https://github.com/Side-Peng/clinpub/issues)
- [Releases](https://github.com/Side-Peng/clinpub/releases)
