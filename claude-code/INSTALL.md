# clinpub Installation Guide

## Install as Claude Code Plugin

### From Plugin Marketplace (Recommended)

```bash
# Add the marketplace first
claude plugin marketplace add Side-Peng/clinpub
# Install the plugin
claude plugin install clinpub@clinpub
```

### From Local Source (Development)

```bash
claude --plugin-dir ./clinpub
```

### From Git Repository

```bash
git clone https://github.com/Side-Peng/clinpub.git
claude --plugin-dir ./clinpub
```

## Validate Installation

```bash
claude plugin validate . --strict
```

## Usage

After installation, restart Claude Code, then:

```bash
/clinpub:overview                  # Command reference overview
/clinpub:data2idea data.csv       # Topic mining from data
/clinpub:initialize                     # Phase 0: Project initialization
/clinpub:data-prep                # Phase 1: Data preparation
/clinpub:analysis                 # Phase 2: Statistical analysis
/clinpub:writing                  # Phase 3: Manuscript writing
/clinpub:review                   # Phase 4: Peer review simulation
/clinpub:milestone <N>            # Phase gate verification
/clinpub:modify                   # Modify analysis outputs
/clinpub:do                       # Breakpoint resume (work-in-progress)
/clinpub:next-step                # Advance to next step
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
claude plugin update clinpub@clinpub
```

Or re-install from source:

```bash
git pull origin main
claude --plugin-dir ./clinpub
```

## Uninstalling

```bash
claude plugin uninstall clinpub@clinpub
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Commands not found after install | Restart Claude Code to reload plugins |
| `/clinpub:overview` not appearing | Run `claude --plugin-dir ./clinpub` again, then restart |
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
