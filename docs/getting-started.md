# Getting Started with clinpub

从零到投稿，用你的临床数据跑通完整 5 阶段管线。

> **预计时间**：安装 2 分钟 + 管线运行 20-60 分钟（取决于分析复杂度）

---

## 1. 准备工作

### 系统要求

| 组件        | 最低版本  | 用途               |
| ----------- | --------- | ------------------ |
| Claude Code | >= 2.1.88 | Plugin 宿主环境     |
| Node.js     | >= 22.0.0 | Hook 执行          |
| R           | >= 4.2    | 统计分析           |
| Python      | >= 3.9    | 数据画像、文献检索 |

### API 密钥（可选但推荐）

```bash
export NCBI_API_KEY="your_ncbi_key"    # 提升 PubMed 查询速率 (3→10 req/s)
export TAVILY_API_KEY="your_tavily_key" # Tavily 文献检索（Phase 3 用）
export UNPAYWALL_EMAIL="your@email.com" # Unpaywall PDF 全文获取
```

---

## 2. 安装

```bash
claude plugin install clinpub
```

安装完成后重启 Claude Code，即可在任意项目使用 `/clinpub:overview` 命令。

验证安装：

```bash
# 重启 Claude Code 后，输入 /clinpub:overview 应看到命令参考
/clinpub:overview
```

---

## 3. 开始第一个项目

### 3.1 准备数据

将你的临床数据 CSV 放入 `01_RawData/` 目录。

### 3.2 创建项目配置

在项目根目录创建 `project_config.yml`，根据实际列名填写 `variables` 映射。可参考 `pipeline/templates/` 下的研究类型模板。

### 3.3 启动管线

```bash
/clinpub:overview
```

---

## 4. Phase 0 — 项目初始化

**命令**：`/clinpub:init`

Claude 会与你讨论：

- 研究类型（RCT/Cohort/Case-Control 等）
- 核心变量（结局、暴露、协变量）
- 分析方法候选列表
- 目标期刊

讨论结束后自动生成：

```
Project_Root/
├── .clinpub/
│   ├── PROJECT.md          # 研究框架
│   ├── ROADMAP.md          # 5 阶段路线图
│   ├── STATE.md            # 当前进度
│   └── phases/00-init/
│       └── 00-CONTEXT.md   # 决策记录
├── project_config.yml       # 项目配置
└── 01_RawData/ → ... → 05_Manuscript/  # 目录骨架
```

**你需要做的**：回答 Claude 提出的研究设计问题，确认分析方案。

---

## 5. Phase 1 — 数据准备

**命令**：`/clinpub:data-prep`

Analyst Agent 执行：

1. 读取原始数据，诊断每列变量类型和缺失模式
2. 清洗数据（缺失值处理、异常值检测、变量编码）
3. 生成 `cleaned.csv` 和 `data_quality.html`

产出：

```
02_PreprocessedData/
├── data/
│   └── cleaned.csv              # 清洗后的分析数据集
└── reports/
    └── data_quality.html         # 交互式数据质量报告
```

**你需要做的**：在 checkpoint 确认数据清洗结果，决定缺失值策略。

---

## 6. Phase 2 — 统计分析

**命令**：`/clinpub:analysis`

这是最核心的阶段。Claude 会：

1. **诊断数据** — 读取 `cleaned.csv`，识别分组结构、时间点、结局类型
2. **推荐方案** — 基于数据特征动态构建分析波次（非固定模板！）
3. **与你讨论** — 确认每个波次的方法、参数、配色
4. **逐波执行** — 每波完成后暂停等你确认，再进入下一波
5. **生成产出** — 每个方法产生 figure + table + 方法说明 + MANIFEST.yaml

分析方案将基于你的数据特征动态构建（非固定模板）。

产出：

```
03_AnalysisMethods/       # 代码 + 方法说明（每个方法一个子目录）
04_Outputs/               # 图表（每个方法一个子目录）
  ├── 01_BaselineTable/
  ├── 02_TimepointSummary/
  ├── ...
  └── MANIFEST.yaml       # 产出清单
```

**你需要做的**：每个 checkpoint 确认分析结果，波次间可要求调整方法或参数。

---

## 7. Phase 3 — 论文撰写

**命令**：`/clinpub:writing`

双 Agent 协作：

1. **Reference Agent** 先执行文献检索 → 构建 `Reference/citation_map.md` + `references.bib`
2. **Writer Agent** 验证上游 MANIFEST.yaml 后按 IMRAD 顺序撰写：
   - Methods → Results → Introduction → Discussion → Abstract

每章写完自动执行 Humanizer 检查（防 AI 模板化）。

产出：

```
Reference/
├── references.bib            # Vancouver 格式引用
├── citation_map.md           # 引用-章节映射
├── literature_notes/         # 逐篇论文笔记
└── MANIFEST.yaml

05_Manuscript/
├── draft-methods.md
├── draft-results.md
├── draft-introduction.md
├── draft-discussion.md
├── draft-abstract.md
├── manuscript.md             # 完整编译稿
└── MANIFEST.yaml
```

**你需要做的**：审阅每章草稿，提出修改意见；提供补充检索方向。

---

## 8. Phase 4 — 审稿修稿

**命令**：`/clinpub:review`

Writer Agent 模拟同行评审：

1. 生成 `review_v1.md`（Major + Minor 分类）
2. 你选择要处理的审稿意见
3. Claude 逐条修改并生成 `response_letter.md`
4. 循环至满意，输出 `final/manuscript.md`

---

## 9. 常用命令速查

| 命令                            | 用途                       |
| ------------------------------- | -------------------------- |
| `/clinpub:overview`             | 主入口，查看命令参考       |
| `/clinpub:data2idea data.csv` | 不做分析，先从数据挖掘选题 |
| `/clinpub:init`       | 初始化项目目录和配置       |
| `/clinpub:data-prep`          | 仅跑 Phase 1 数据清洗      |
| `/clinpub:analysis`           | 仅跑 Phase 2 统计分析      |
| `/clinpub:writing`            | 仅跑 Phase 3 论文撰写      |
| `/clinpub:review`             | 仅跑 Phase 4 审稿修稿      |
| `/clinpub:milestone N`        | 查看 Phase N 关卡状态      |

---

## 10. 质量保证

clinpub 内置 4 道质量门控（详见 `pipeline/references/gates.md`）：

| Gate                 | Phase 间 | 检查项                              |
| -------------------- | -------- | ----------------------------------- |
| IRB / Ethics         | 0→1     | 伦理审批、数据脱敏                  |
| Data Quality         | 1→2     | 缺失率受控、样本量充足              |
| Analysis Validity    | 2→3     | 效应量+CI+p 值完整、假设检验        |
| Submission Readiness | 4→终稿  | IMRAD 完整、图表≥300 DPI、DOI 齐全 |

每道门控不通过则无法进入下一阶段。

---

## 11. 常见问题

### R 包安装失败

```r
# 逐个安装，定位失败的具体包
install.packages("gtsummary")
install.packages("flextable")
# 如果 Bioconductor 包缺失：
if (!require("BiocManager")) install.packages("BiocManager")
BiocManager::install("limma")
```

### PubMed 搜索无结果

1. 检查网络连接
2. 设置 `NCBI_API_KEY` 环境变量提升速率
3. 尝试更宽泛的关键词

### 图表中文乱码

R 中安装并指定中文字体：

```r
install.packages("showtext")
library(showtext)
showtext_auto()
font_add("SimHei", "simhei.ttf")
```

### cleaned.csv 生成失败

1. 确认 `01_RawData/` 下有 CSV 文件
2. 检查 `project_config.yml` 中 `variables` 映射是否正确
3. CSV 编码应为 UTF-8

---

## 12. 下一步

- 阅读 `pipeline/references/analysis_methods.md` — 了解完整分析方法库
- 阅读 `pipeline/references/journal_standards.md` — 了解期刊格式要求
- 探索 `agents/` 目录了解各 Agent 详细能力

有问题？检查 `.clinpub/STATE.md` 了解当前进度，或重新运行 `/clinpub:do` 继续。
