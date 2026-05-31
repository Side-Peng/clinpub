# clinpub 配置指南

## 项目配置

### project_config.yml

每个 clinpub 项目都需要一个 `project_config.yml` 文件，定义研究参数和变量映射。

```yaml
# 基本信息
study:
  title: "研究标题"
  type: "cohort"  # rct, cohort, case_control, cross_sectional, descriptive
  target_journal: "Alzheimer's & Dementia"

# 变量映射
variables:
  id: "patient_id"           # 患者唯一标识
  outcome: "diagnosis"       # 结局变量
  exposure: "treatment"      # 暴露变量
  time: "follow_up_days"     # 时间变量（生存分析）
  covariates:                # 协变量列表
    - "age"
    - "gender"
    - "bmi"
    - "smoking_status"

# 数据路径
paths:
  raw_data: "01_RawData/"
  preprocessed: "02_PreprocessedData/"
  analysis: "03_AnalysisMethods/"
  outputs: "04_Outputs/"
  manuscript: "05_Manuscript/"
  reference: "Reference/"

# 分析配置
analysis:
  significance_level: 0.05
  confidence_level: 0.95
  multiple_comparison: "bonferroni"  # bonferroni, fdr, holm
  imputation_method: "mice"          # mice, mean, median, listwise

# 图表配置
figures:
  dpi: 300
  format: "png"              # png, pdf, tiff
  font: "Arial"
  font_size: 8
  color_palette: "viridis"   # viridis, RColorBrewer
  width_single: 8            # 单栏宽度 (cm)
  width_double: 17           # 双栏宽度 (cm)
```

## 环境变量

### 必需变量

无（所有必需配置在 project_config.yml 中）

### 可选变量

| 变量 | 用途 | 默认值 |
|------|------|--------|
| `NCBI_API_KEY` | PubMed API 密钥（提升查询速率） | 无 |
| `TAVILY_API_KEY` | Tavily 搜索 API 密钥 | 无 |
| `UNPAYWALL_EMAIL` | Unpaywall PDF 全文获取 | 无 |

### 设置方法

```bash
# 临时设置（当前会话）
export NCBI_API_KEY="your_key"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export NCBI_API_KEY="your_key"' >> ~/.bashrc
source ~/.bashrc
```

## R 配置

### 必需 R 包

```r
install.packages(c(
  # 数据处理
  "dplyr", "tidyr", "stringr", "readr", "readxl",
  
  # 统计分析
  "survival", "lme4", "glmnet", "pROC",
  
  # 可视化
  "ggplot2", "ggpubr", "patchwork", "survminer", "ggsurvfit", "ggsignif",
  
  # 输出
  "gtsummary", "flextable", "openxlsx",
  
  # 路径
  "here", "fs"
))
```

### R 版本要求

- R >= 4.2
- 建议使用 RStudio 或 VS Code + R 扩展

## Python 配置

### 必需 Python 包

```bash
pip install pandas numpy requests openpyxl
```

### requirements.txt

```txt
pandas>=1.5.0
numpy>=1.23.0
requests>=2.28.0
openpyxl>=3.0.10
```

### Python 版本要求

- Python >= 3.9
- 建议使用虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Claude Code 配置

### 安装 clinpub

```bash
npx clinpub@latest
```

### 安装位置

- **全局安装**：`~/.claude/`（所有项目可用）
- **本地安装**：`./.claude/`（仅当前项目）

### 验证安装

```bash
# 重启 Claude Code 后
/clinpub  # 应显示主菜单
```

## Hooks 配置

Hooks 自动注册在 `.claude/settings.json`：

```json
{
  "hooks": {
    "Write": [
      {
        "matcher": "*.R",
        "command": "node hooks/clinpub-workflow-guard.js"
      }
    ],
    "Bash": [
      {
        "matcher": "*",
        "command": "bash hooks/clinpub-phase-boundary.sh"
      }
    ],
    "Read": [
      {
        "matcher": "*.csv",
        "command": "node hooks/clinpub-prompt-guard.js"
      }
    ]
  }
}
```

## 目录结构配置

### 标准项目目录

```
Project_Root/
├── .clinpub/                  # 规划层
│   ├── PROJECT.md              # 研究框架
│   ├── ROADMAP.md              # 路线图
│   ├── STATE.md                # 当前状态
│   └── phases/                 # 阶段详情
├── 01_RawData/                 # 原始数据（只读）
├── 02_PreprocessedData/        # Phase 1 产出
│   ├── data/
│   │   └── cleaned.csv
│   └── reports/
│       └── data_quality.html
├── 03_AnalysisMethods/         # Phase 2 方法目录
├── 04_Outputs/                 # 图表输出
├── Reference/                  # 文献
├── 05_Manuscript/             # 论文各章节
├── project_config.yml          # 项目配置
└── run_all.R                   # R 脚本入口
```

## 研究类型配置

### RCT（随机对照试验）

```yaml
study:
  type: "rct"
  consort_checklist: true
  randomization_method: "block"  # block, stratified, adaptive
```

### 队列研究

```yaml
study:
  type: "cohort"
  follow_up_time: "months"
  censoring_variable: "censored"
```

### 病例对照研究

```yaml
study:
  type: "case_control"
  matching_variables:
    - "age"
    - "gender"
  matching_ratio: 1:2
```

### 横断面研究

```yaml
study:
  type: "cross_sectional"
  sampling_method: "random"  # random, stratified, cluster
```

## 输出配置

### 图表标准

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `dpi` | 300 | 分辨率 |
| `format` | png | 输出格式 |
| `font` | Arial | 字体 |
| `font_size` | 8 | 字号 |
| `color_palette` | viridis | 配色方案 |
| `width_single` | 8 cm | 单栏宽度 |
| `width_double` | 17 cm | 双栏宽度 |

### 文件命名规范

- 图表：`{方法编号}_{描述}.{格式}`（例：`01_BaselineTable.png`）
- 表格：`{方法编号}_{描述}.xlsx`（例：`01_BaselineTable.xlsx`）
- 脚本：`{方法编号}_{描述}.R`（例：`01_BaselineTable.R`）
