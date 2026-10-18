# ClinPub - Clinical Publication Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

End-to-end clinical data analysis and publication pipeline. Adapts to any clinical research article type.

## 🎯 Overview

ClinPub is a structured clinical data analysis and publication pipeline that acts as a **senior medical statistician + academic writing consultant**. Core pipeline Phase 0-3 processes patient-level data through initialization, data cleaning, adaptive statistical analysis, and IMRAD manuscript writing; standalone tools handle manuscript improvement, cover-letter generation, and post-submission reviewer response.

## 🚀 Platform Support

ClinPub is available for multiple AI coding assistants:

| Platform | Status | Location |
|----------|--------|----------|
| **Claude Code** | ✅ Stable | `claude-code/` |
| **OpenAI Codex** | ✅ Stable | `codex/clinpub/` |
| **Qoder** | ✅ Stable | `qoder/` |

## 📦 Installation

### OpenAI Codex

> 以下命令在仓库根目录（克隆后的 `clinpub/`）执行。

```bash
# From local path
codex plugin install ./codex/clinpub

# Or add to personal marketplace (use absolute path)
codex plugin marketplace add /path/to/clinpub/codex
codex plugin install clinpub
```

### Claude Code

```bash
# Install as Claude Code Plugin (development, from repo root)
claude --plugin-dir ./claude-code

# Install from marketplace (production)
claude plugin marketplace add Side-Peng/clinpub
claude plugin install clinpub
```

## 📋 Pipeline Phases

| Phase | Command | Purpose | Key Output |
|-------|---------|---------|------------|
| 0 | `init` | Project initialization or import (target journal explicitly asked) | `project_config.yml` |
| 1 | `data-prep` | Data cleaning and EDA | `cleaned.csv` |
| 2 | `analysis` | Statistical analysis | `04_Outputs/` |
| 3 | `writing` | IMRAD manuscript writing (core pipeline end) | `manuscript.md` |

### Additional Skills

| Skill | Purpose |
|---------|---------|
| `clinpub` | **Hub**: status / `help` / `next` (verify & advance) / intent routing |
| `clinpub-modify` | Modify analysis outputs or add new analysis methods |
| `clinpub-improving` | Continuously improve a draft (self-review → plan → direct revision) |
| `clinpub-review` | Post-submission: real reviewer comments → response letter + revision |
| `clinpub-coverletter` | Tailored submission cover letter for the target journal |
| `clinpub-data2idea` | Topic mining from data |

> Former `overview` / `do` / `next-step` / `milestone` are merged into `clinpub` since 3.0:
> one shared set of state criteria, and "advance" is atomic with gate verification.

## 🏗️ Architecture

```
clinpub/
├── .codex-plugin/plugin.json    # Plugin manifest
├── skills/                      # 10 skills
│   ├── clinpub/                 # hub: status / help / next / routing
│   ├── clinpub-init/
│   ├── clinpub-data-prep/
│   ├── clinpub-data2idea/
│   ├── clinpub-analysis/
│   ├── clinpub-writing/
│   ├── clinpub-modify/
│   ├── clinpub-improving/
│   ├── clinpub-review/
│   └── clinpub-coverletter/
├── agents/                      # 6 specialized agents
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
| Manuscript drafting, improvement, revision | `writer-agent` | 3, post-writing |
| Topic mining from data | `topic-miner-agent` | - |
| Statistical verification | `clinpub-verifier` | 1-3 |
| Analysis output modification / method addition | `modify-agent` | post-2 |

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

# 4. Write manuscript (core pipeline ends here)
clinpub:writing

# 5. Use standalone tools as needed
clinpub:improving     # self-review and directly revise the draft
clinpub:coverletter   # prepare the submission cover letter
clinpub:review        # after submission, handle real reviewer comments

# Check current status
clinpub

# Verify the gate and advance to the next phase
clinpub next
```

## 🔍 Key Features

- **Phase 0-3 Pipeline + Standalone Tools**: Structured workflow from data to manuscript, with post-writing tools
- **Publication-Grade Output**: ≥300 DPI figures, formatted tables
- **Iterative Analysis**: 1–3 methods per batch; the next batch is decided from results via a decision-rule library
- **Progressive Writing**: Skeleton → Results → Methods → Discussion → Conclusion → Introduction → Abstract
- **Post-Submission Review Response**: Handle real reviewer comments with point-by-point responses
- **Topic Mining**: Generate research ideas from raw data
- **Multi-Agent Architecture**: 6 specialized agents
- **Quality Gates**: Phase transitions require gate verification + user sign-off

## 📄 Documentation

- [Codex Installation Guide](INSTALL.md)
- [Claude Code Documentation](../claude-code/CLAUDE.md)
- [Qoder Documentation](../qoder/README.md)

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
