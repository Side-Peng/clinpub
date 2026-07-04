# ClinPub Codex Plugin - Installation Guide

## Overview

ClinPub has been successfully converted from Claude Code plugin format to Codex plugin format.

## Changes Made

1. **Plugin Manifest**: Converted from `.claude-plugin/plugin.json` to `.codex-plugin/plugin.json`
2. **Skills Structure**: Converted `commands/*.md` to `skills/*/SKILL.md` format
3. **Preserved Components**: 
   - All pipeline workflows, references, and templates
   - All agent definitions
   - All Python scripts
   - All hook implementations
   - Requirements file

## Installation

### Option 1: Local Development Installation

```bash
# Navigate to the codex directory
cd "D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\codex"

# Install as local plugin
codex plugin install ./clinpub
```

### Option 2: Add to Personal Marketplace

```bash
# Add to personal marketplace
codex plugin marketplace add "D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\codex"

# Then install from marketplace
codex plugin install clinpub
```

## Plugin Structure

```
clinpub/
├── .codex-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/                  # 11 skills (converted from commands)
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
├── agents/                  # 8 specialized agents
├── pipeline/                # Workflows, references, templates
├── scripts/                 # Python scripts
├── hooks/                   # Hook implementations
├── requirements.txt         # Python dependencies
└── README.md               # Documentation
```

## Skills (11 total)

| Skill | Description |
|-------|-------------|
| `clinpub-overview` | Command reference overview |
| `clinpub-data2idea` | Topic mining from data |
| `clinpub-init` | Phase 0: Project initialization |
| `clinpub-data-prep` | Phase 1: Data cleaning |
| `clinpub-analysis` | Phase 2: Statistical analysis |
| `clinpub-writing` | Phase 3: IMRAD manuscript writing |
| `clinpub-review` | Phase 4: Peer review simulation |
| `clinpub-milestone` | Phase gate review |
| `clinpub-modify` | Modify analysis outputs |
| `clinpub-do` | Workspace state router |
| `clinpub-next-step` | Auto-advance to next phase |

## Usage

After installation, use the skills in Codex:

```bash
# Start with project initialization
clinpub:init

# Or check current status
clinpub:do

# Or auto-advance to next step
clinpub:next-step
```

## Dependencies

Install R and Python dependencies:

```bash
# Python dependencies
pip install -r requirements.txt

# R dependencies (run in R)
install.packages(c("dplyr","tidyr","ggplot2","gtsummary","survival","lme4","glmnet","pROC","ggpubr","patchwork","survminer","ggsurvfit","ggsignif","flextable","openxlsx","here","fs","stringr","readr","readxl","yaml","RColorBrewer","viridis"))
```

## Environment Variables (Optional)

- `NCBI_API_KEY` - Improves PubMed rate limit
- `TAVILY_API_KEY` - For Tavily search
- `UNPAYWALL_EMAIL` - For Unpaywall PDF access

## Validation

The plugin has been validated and passes all checks:

```bash
python "C:\Users\13049\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py" ".\codex\clinpub"
# Output: Plugin validation passed
```

## Next Steps

1. Install the plugin using one of the methods above
2. Test the plugin with a sample clinical dataset
3. Report any issues to the repository

## Repository

https://github.com/Side-Peng/clinpub

## Author

Side-Peng (1304916798@qq.com)
