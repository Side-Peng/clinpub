# ClinPub Installation Guide

## 🚀 Installation

### OpenAI Codex

#### Option 1: Local Development

```bash
# Clone the repository
git clone https://github.com/Side-Peng/clinpub.git
cd clinpub/codex

# Install as local plugin
codex plugin install ./clinpub
```

#### Option 2: Add to Personal Marketplace

```bash
# Add to personal marketplace
codex plugin marketplace add /path/to/clinpub/codex

# Then install from marketplace
codex plugin install clinpub
```

### Claude Code

#### Option 1: Plugin Marketplace (Recommended)

```bash
# Add marketplace
claude plugin marketplace add Side-Peng/clinpub

# Install plugin
claude plugin install clinpub@clinpub
```

#### Option 2: Local Development

```bash
git clone https://github.com/Side-Peng/clinpub.git
claude --plugin-dir ./clinpub
```

## 📦 Dependencies

### R Packages

```r
install.packages(c(
  "dplyr", "tidyr", "stringr", "readr", "readxl",
  "survival", "lme4", "glmnet", "pROC",
  "gtsummary", "flextable", "openxlsx",
  "ggplot2", "ggpubr", "patchwork", "survminer", "ggsurvfit", "ggsignif",
  "here", "fs", "yaml", "RColorBrewer", "viridis"
))
```

### Python Packages

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pandas numpy requests openpyxl
```

## 🔧 Environment Variables (Optional)

| Variable | Required | Purpose |
|----------|----------|---------|
| `NCBI_API_KEY` | Optional | PubMed API rate limit increase |
| `TAVILY_API_KEY` | Optional | Tavily search API |
| `UNPAYWALL_EMAIL` | Optional | Unpaywall PDF access |

### Setting Environment Variables

#### Windows (PowerShell)

```powershell
# Temporary
$env:NCBI_API_KEY="your_api_key"

# Permanent
[Environment]::SetEnvironmentVariable("NCBI_API_KEY", "your_api_key", "User")
```

#### macOS/Linux

```bash
# Add to ~/.bashrc or ~/.zshrc
export NCBI_API_KEY="your_api_key"
export TAVILY_API_KEY="your_api_key"
export UNPAYWALL_EMAIL="your_email@example.com"
```

## ✅ Verification

### For Codex Plugin

```bash
# Validate plugin structure
codex plugin validate ./clinpub

# Check installed plugins
codex plugin list
```

### For Claude Code Plugin

```bash
# Validate plugin structure
claude plugin validate ./clinpub --strict

# Check installed plugins
claude plugin list
```

## 🔍 Testing

### Test R Installation

```bash
Rscript -e 'library(dplyr); library(ggplot2); cat("R packages OK\n")'
```

### Test Python Installation

```bash
python -c "import pandas; import numpy; print('Python packages OK')"
```

### Test PubMed Search

```bash
python scripts/ncbi_search.py "clinical trial" --database pubmed --max-results 5
```

## 🐛 Troubleshooting

### Common Issues

#### 1. R Package Installation Fails

```bash
# Install dependencies
sudo apt-get install libcurl4-openssl-dev libssl-dev libxml2-dev

# Then retry
Rscript -e 'install.packages(c("httr", "xml2"))'
```

#### 2. Python Module Not Found

```bash
# Ensure you're using the right Python
which python
python --version

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

#### 3. PubMed API Rate Limit

Set your NCBI API key:

```bash
export NCBI_API_KEY="your_api_key_here"
```

Get your API key at: https://www.ncbi.nlm.nih.gov/account/settings/

#### 4. Plugin Validation Fails

```bash
# Check JSON syntax
python -c "import json; json.load(open('.codex-plugin/plugin.json'))"

# Check for BOM
python -c "with open('.codex-plugin/plugin.json', 'rb') as f: print(f.read(3))"
```

## 📚 Next Steps

After installation:

1. **Read the documentation**: [README.md](README.md)
2. **Start with Phase 0**: `clinpub:init`
3. **Check current status**: `clinpub:do`
4. **View command reference**: `clinpub:overview`

## 🆘 Getting Help

- **Issues**: https://github.com/Side-Peng/clinpub/issues
- **Discussions**: https://github.com/Side-Peng/clinpub/discussions
- **Email**: 1304916798@qq.com

## 📄 License

MIT License - see [LICENSE](LICENSE) for details
