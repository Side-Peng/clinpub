# clinpub Installation Guide

## Install as Claude Code Plugin

### From Plugin Marketplace (Recommended)

> 以下命令在仓库根目录（克隆后的 `clinpub/`）执行。

```bash
# Add the marketplace source first
claude plugin marketplace add Side-Peng/clinpub
# Install the plugin
claude plugin install clinpub
```

安装后重启 Claude Code，输入 `/clinpub help` 验证插件已加载。

### From Local Source (Development)

```bash
# 在仓库根目录执行
git clone https://github.com/Side-Peng/clinpub.git
cd clinpub
claude --plugin-dir ./claude-code
```

### From Git Repository

```bash
git clone https://github.com/Side-Peng/clinpub.git
cd clinpub/claude-code
claude --plugin-dir .
```

## Validate Installation

```bash
claude plugin validate . --strict
```

## Usage

After installation, restart Claude Code, then:

```bash
/clinpub help                  # Command reference overview
/clinpub:data2idea data.csv       # Topic mining from data
/clinpub:initialize                     # Phase 0: Project initialization
/clinpub:data-prep                # Phase 1: Data preparation
/clinpub:analysis                 # Phase 2: Statistical analysis
/clinpub:writing                  # Phase 3: Manuscript writing (core pipeline终点)
/clinpub:improving                # Tool: self-review + directly revise manuscript & analysis
/clinpub:coverletter              # Tool: cover letter for the target journal
/clinpub:review                   # Tool: post-submission — handle real reviewer comments
/clinpub next <N>            # Phase gate verification
/clinpub:modify                   # Modify analysis outputs or add new analysis methods
/clinpub                       # Breakpoint resume (work-in-progress)
/clinpub next                # Advance to next step
```

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Claude Code | >= 2.1.88 | Plugin support |
| Node.js | >= 22.0.0 | Hook execution |
| R | >= 4.2 | Statistical analysis |
| Python | >= 3.9 | Data profiling, search scripts |

### R Packages

```r
install.packages(c(
  "dplyr", "tidyr", "stringr", "readr", "readxl",
  "survival", "lme4", "glmnet", "pROC",
  "ggplot2", "ggpubr", "patchwork", "survminer", "ggsurvfit", "ggsignif",
  "gtsummary", "flextable", "openxlsx",
  "here", "fs"
))
```

### Python Packages

```bash
pip install -r requirements.txt
```

### Environment Variables

```bash
export NCBI_API_KEY="your_key"       # Optional, improves PubMed rate limit
export TAVILY_API_KEY="your_key"     # Required for Tavily search
export UNPAYWALL_EMAIL="your@email.com"  # Optional, Unpaywall PDF access
```

## Updating

```bash
claude plugin update clinpub
```

Or re-install from source:

```bash
git pull origin main
claude --plugin-dir ./claude-code
```

## Uninstalling

```bash
claude plugin uninstall clinpub
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Commands not found after install | Restart Claude Code to reload plugins |
| `/clinpub help` not appearing | Run `claude --plugin-dir ./claude-code` (from repo root) again, then restart |
| R package errors | Run the `install.packages()` command above |
| Python import errors | Run `pip install -r requirements.txt` |
| PubMed search fails | Set `NCBI_API_KEY` env var |
| Tavily search fails | Set `TAVILY_API_KEY` env var |
| Plugin validation fails | Ensure `.claude-plugin/plugin.json` exists and is valid |

## Development

For developers contributing to clinpub:

- **Development Guide**: See `docs/DEVELOPMENT.md` for coding standards and architecture
- **Contributing**: See `CONTRIBUTING.md` for contribution guidelines
- **Testing**: See `docs/TESTING.md` for testing procedures

### Code Independence Rule

Each script must be self-contained with all variables defined locally:

```r
# ✓ Correct: All variables defined in script
data_path <- "01_RawData/data.csv"
output_dir <- "04_Outputs/Results"

# ✗ Wrong: Using global variables
data <- read.csv(global_path)
```
