# clinpub Installation Guide

## One-Line Install (Recommended)

```bash
npx clinpub@latest
```

The installer prompts you to choose:
1. **Global** — All projects (`~/.claude/`)
2. **Local** — Current project only (`./.claude/`)

### Non-interactive (CI / Scripts)

```bash
npx clinpub --global    # Global install
npx clinpub --local     # Local install
```

### What Gets Installed

The installer converts each command file into a Claude Code skill:

```
commands/clinpub/clinpub.md          → ~/.claude/skills/clinpub-clinpub/SKILL.md
commands/clinpub/data2idea.md        → ~/.claude/skills/clinpub-data2idea/SKILL.md
commands/clinpub/analysis.md         → ~/.claude/skills/clinpub-analysis/SKILL.md
commands/clinpub/writing.md          → ~/.claude/skills/clinpub-writing/SKILL.md
commands/clinpub/review.md           → ~/.claude/skills/clinpub-review/SKILL.md
commands/clinpub/init-project.md     → ~/.claude/skills/clinpub-init-project/SKILL.md
commands/clinpub/data-prep.md        → ~/.claude/skills/clinpub-data-prep/SKILL.md
commands/clinpub/milestone.md        → ~/.claude/skills/clinpub-milestone/SKILL.md
```

Shared resources (agents, pipeline, scripts, hooks) are copied to:

```
~/.claude/clinpub/                   # Shared resource directory
├── agents/                          # 7 specialized agents
├── pipeline/                        # Workflows, references, templates
├── scripts/                         # Python tools
├── hooks/                           # Workflow enforcement
└── CLAUDE.md                        # Reference documentation
```

## Usage

After installation, restart Claude Code, then:

```bash
/clinpub                    # Full 5-phase pipeline
/clinpub-data2idea data.csv # Topic mining from data
/clinpub-analysis           # Statistical analysis
/clinpub-writing            # Manuscript writing
/clinpub-review             # Peer review simulation
```

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| Claude Code | >= 2.1.88 | Skill support |
| Node.js | >= 22.0.0 | Installer + hook execution |
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
```

## Updating

```bash
npx clinpub@latest       # Re-run installer with latest version
```

## Uninstalling

```bash
npx clinpub --global --uninstall
npx clinpub --local --uninstall
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Skills not found after install | Restart Claude Code to reload skills |
| `/clinpub` not appearing | Run `npx clinpub@latest` again, then restart |
| R package errors | Run the `install.packages()` command above |
| Python import errors | Run `pip install -r requirements.txt` |
| PubMed search fails | Set `NCBI_API_KEY` env var |
| Tavily search fails | Set `TAVILY_API_KEY` env var |

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
