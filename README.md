<div align="center">

# clinpub

### 临床数据分析与发表管线

*面向 SCI Q1/Q2 期刊的端到端临床数据分析与发表加速器。*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](CHANGELOG.md)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-orange.svg)](https://docs.anthropic.com/en/docs/claude-code)
[![Node](https://img.shields.io/badge/Node-%3E%3D22.0.0-green.svg)](package.json)

**[中文文档](#中文文档)** · **[English](#english)**

</div>

---

<!-- ==================== 中文部分 ==================== -->

# 中文文档

**[概述](#概述)** · **[功能特性](#功能特性)** · **[安装](#安装)** · **[快速开始](#快速开始)** · **[架构](#架构)** · **[智能体](#智能体)** · **[命令参考](#命令参考)** · **[质量门控](#质量门控)** · **[支持的研究类型](#支持的研究类型)** · **[工作流保护](#工作流保护)** · **[出版级图表标准](#出版级图表标准)** · **[依赖](#依赖)** · **[文档](#文档)** · **[环境变量](#环境变量)** · **[贡献](#贡献)** · **[许可证](#许可证)** · **[English ↓](#english)**

---

## 概述

**clinpub** 扮演**资深医学统计学家 + 学术写作顾问**。处理已整理的患者级数据（每行一个患者，每列一个变量），输出统计结果、出版级图表和可投稿论文。

**目标期刊**: Alzheimer's & Dementia, Molecular Psychiatry 及其他 SCI Q1/Q2 期刊。

---

## 功能特性

- **5 阶段管线**: 初始化 → 数据准备 → 统计分析 → 论文撰写 → 审稿修稿，阶段间设有里程碑关卡
- **8 个专业 AI 智能体**: 选题挖掘、数据清洗、统计分析、文献检索、论文撰写、验证、规划、修改
- **自适应分析**: 根据数据特征（分组、时间点、结局类型）动态推荐统计方法
- **出版级输出**: ≥300 DPI 图表，可自定义 `theme_pub()` 主题与配色方案，Vancouver 引用格式含 DOI
- **工作流保护**: 3 个 PreToolUse 钩子守护阶段顺序、里程碑前置条件和提示注入防护
- **多研究类型支持**: RCT (CONSORT)、队列/病例对照/横断面 (STROBE)、描述性研究
- **导入模式**: 支持导入已有项目，自动推断文件角色

---

## 安装

### 前置要求

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) >= 2.1.88
- R >= 4.3（含所需依赖包）
- Python >= 3.11

### 方式一：插件市场（推荐）

```bash
claude plugin install clinpub
```

### 方式二：本地开发

```bash
git clone https://github.com/Side-Peng/clinpub.git
claude --plugin-dir ./clinpub
```

### 方式三：手动安装

详见 [INSTALL.md](INSTALL.md)。

---

## 快速开始

```bash
/clinpub:overview               # 查看命令参考
/clinpub:data2idea data.csv     # 从数据中挖掘选题
/clinpub:init                   # 阶段 0：项目初始化
/clinpub:data-prep              # 阶段 1：数据准备
/clinpub:analysis               # 阶段 2：统计分析
/clinpub:writing                # 阶段 3：论文撰写
/clinpub:review                 # 阶段 4：审稿修稿
/clinpub:milestone <N>          # 阶段关卡评审
```

每个阶段遵循四步模式：**讨论 → 计划 → 执行 → 验证**。

完整教程、示例数据和常见问题 → `docs/getting-started.md`

---

## 架构

### 三层架构

```
用户 → 命令 (commands/*.md — 11 个入口)
       → 工作流 (pipeline/workflows/*.md — 10 个编排文件)
         → 智能体 (agents/*.md — 8 个专业智能体，每次独立上下文)
           → 脚本 (scripts/*.py — 数据画像 + 内置 NCBI/PubMed 检索 + R/Python 工具)
           → 钩子 (hooks/ — 3 个 PreToolUse 守卫)
```

### 插件目录结构

```
clinpub/
├── .claude-plugin/             # 插件清单 (plugin.json)
├── commands/                   # 11 个命令入口
├── agents/                     # 8 个 AI 智能体
├── pipeline/
│   ├── workflows/              # 10 个阶段编排文件
│   ├── references/             # 15 个参考文档
│   ├── templates/              # 18 个模板（含 5 种研究类型）
│   └── contexts/               # 2 个上下文配置
├── scripts/                    # Python 工具脚本
├── hooks/                      # 4 个钩子文件（3 个守卫 + 配置）
├── docs/                       # 7 个文档文件
├── AGENTS.md                   # Claude Code 智能体指南
├── CLAUDE.md                   # Claude Code 主指南
├── OVERVIEW.md                 # 技能入口
├── CHANGELOG.md                # 版本历史
├── CONTRIBUTING.md             # 贡献指南
├── INSTALL.md                  # 安装指南
└── package.json                # npm 元数据 (v2.0.0)
```

### 用户项目目录

```
Project_Root/
├── .clinpub/                   # 阶段 0 — PROJECT.md / ROADMAP.md / STATE.md
├── 01_RawData/                 # 阶段 1 — 原始数据（只读）
├── 02_PreprocessedData/        # 阶段 1 — cleaned.csv + 质量报告
├── 03_AnalysisMethods/         # 阶段 2 — 方法代码 + 方法说明
├── 04_Outputs/                 # 阶段 2 — 图表输出
├── Reference/                  # 阶段 3 — 文献
├── 05_Manuscript/              # 阶段 3-4 — IMRAD 论文各章节
└── project_config.yml          # 项目配置
```

---

## 智能体

| 智能体 | 语言 | 职责 |
|---|---|---|
| **Topic Miner Agent** | Python | 选题挖掘：数据画像、文献扫描、候选选题生成 |
| **Analyst Agent** | R / Python | 数据清洗、统计分析、图表生成 |
| **Reference Agent** | Python | 文献检索（PubMed）、PDF 阅读、引用管理 |
| **Writer Agent** | — | IMRAD 论文撰写、图表整合、模拟审稿 |
| **Clinpub Planner** | — | 研究分析规划与波浪依赖图 |
| **Clinpub Executor** | R / Python | 计划执行与原子提交 |
| **Clinpub Verifier** | — | 跨阶段验证（15 种模式） |
| **Modify Agent** | R | 分析产出修改：图表风格、方法、变量 |

---

## 命令参考

| 命令 | 阶段 | 用途 |
|---|---|---|
| `/clinpub:overview` | — | 命令参考总览 |
| `/clinpub:data2idea <file>` | — | 从数据中挖掘选题 |
| `/clinpub:init` | 0 | 项目初始化或导入已有项目 |
| `/clinpub:data-prep` | 1 | 数据清洗 → cleaned.csv |
| `/clinpub:analysis` | 2 | 自适应统计分析 |
| `/clinpub:writing` | 3 | IMRAD 论文撰写 |
| `/clinpub:review` | 4 | 模拟审稿与修订 |
| `/clinpub:milestone <N>` | 关卡 | 阶段关卡评审与用户签核 |
| `/clinpub:modify` | post-2 | 修改分析产出 |
| `/clinpub:do` | — | 智能路由：自动检测状态并分发 |
| `/clinpub:next-step` | — | 自动推进到下一步 |

---

## 质量门控

4 道质量门控确保阶段间质量（详见 `pipeline/references/gates.md`）：

| 门控 | 位置 | 核心检查 |
|---|---|---|
| 伦理审查 | 阶段 0 → 1 | IRB 审批、去标识化、知情同意 |
| 数据质量 | 阶段 1 → 2 | cleaned.csv 完整性、缺失率、样本量 |
| 分析有效性 | 阶段 2 → 3 | 方法执行完整性、效应量报告 |
| 投稿就绪 | 阶段 4 → 投稿 | IMRAD 完整、图表 ≥300 DPI、引用含 DOI |

---

## 支持的研究类型

| 研究类型 | 报告规范 |
|---|---|
| 随机对照试验 (RCT) | CONSORT |
| 队列研究 | STROBE |
| 病例对照研究 | STROBE |
| 横断面研究 | STROBE |
| 描述性研究 | STROBE |

---

## 工作流保护

3 个 PreToolUse 钩子保护分析工作流（声明于 `hooks/hooks.json`）：

| 钩子 | 触发 | 作用 |
|---|---|---|
| `clinpub-workflow-guard.js` | Write / Edit | 阻止越阶段文件写入 |
| `clinpub-phase-boundary.sh` | Bash | 检查里程碑前置条件 |
| `clinpub-prompt-guard.js` | Read | 扫描数据文件中的注入攻击 |

---

## 出版级图表标准

| 要求 | 标准 |
|---|---|
| 分辨率 | ≥ 300 DPI |
| 格式 | SVG > TIFF > PDF > PNG |
| 字体 | Arial ≥ 8pt (`theme_pub(base_family = "sans")`) |
| 配色 | 按组数自动选择（Nature 双色 / RColorBrewer / viridis），支持自定义色值与分组映射（色盲友好） |
| 尺寸 | 单栏 89mm，双栏 183mm（Nature 系列） |
| 主题 | `theme_pub()` 统一风格，支持自定义字号、字体、图例位置、标题对齐等（详见 `pipeline/references/r_patterns.md`） |

---

## 依赖

### 关联技能

| 技能 | 用途 |
|---|---|
| `tavily` | 补充信息检索 |
| `pdf-reader` | PDF 全文阅读 |

### R 包

- **数据处理**: dplyr, tidyr, stringr, readr, readxl
- **统计**: stats, survival, lme4, glmnet, pROC
- **可视化**: ggplot2, ggpubr, patchwork, survminer, ggsurvfit, ggsignif, RColorBrewer, viridis
- **输出**: gtsummary, flextable, openxlsx
- **路径**: here, fs
- **配置**: yaml

### Python 包

pandas >= 2.0, numpy >= 1.24, requests >= 2.31, openpyxl >= 3.1

---

## 文档

| 文档 | 描述 |
|---|---|
| [快速开始](docs/getting-started.md) | 端到端教程：从零到投稿 |
| [架构](docs/ARCHITECTURE.md) | 系统架构文档 |
| [配置](docs/CONFIGURATION.md) | `project_config.yml` 结构指南 |
| [开发](docs/DEVELOPMENT.md) | 开发原则与指南 |
| [安装](INSTALL.md) | 详细安装指南 |
| [贡献](CONTRIBUTING.md) | 贡献指南 |
| [更新日志](CHANGELOG.md) | 版本历史 |

---

## 环境变量

| 变量 | 必需 | 用途 |
|---|---|---|
| `NCBI_API_KEY` | 可选 | 提高 PubMed API 速率限制 |
| `TAVILY_API_KEY` | 可选 | Tavily 搜索接口 |
| `UNPAYWALL_EMAIL` | 可选 | Unpaywall PDF 访问 |

---

## 贡献

欢迎贡献！核心原则是**代码自包含**：每个脚本必须在本地定义所有变量、依赖和辅助函数——不允许跨文件隐式依赖。

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 许可证

本项目基于 **MIT 许可证**开源——详见 LICENSE 文件。

---

<div align="center">

**为全球临床研究者倾力打造。**

[↑ 返回顶部 / Back to Top](#clinpub)

</div>

---
---

<!-- ==================== English Section ==================== -->

# English

**[Overview](#overview)** · **[Features](#features)** · **[Installation](#installation)** · **[Quick Start](#quick-start)** · **[Architecture](#architecture)** · **[Agents](#agents)** · **[Commands](#commands)** · **[Quality Gates](#quality-gates)** · **[Study Types](#supported-study-types)** · **[Hooks](#hooks)** · **[Figure Standards](#publication-grade-figures)** · **[Dependencies](#dependencies)** · **[Documentation](#documentation)** · **[Environment Variables](#environment-variables)** · **[Contributing](#contributing)** · **[License](#license)** · **[中文 ↑](#中文文档)**

---

## Overview

**clinpub** acts as a **senior medical statistician + academic writing consultant**. It processes patient-level data (one patient per row, one variable per column) and outputs statistical results, publication-grade figures, and submission-ready manuscripts.

**Target journals**: Alzheimer's & Dementia, Molecular Psychiatry, and other SCI Q1/Q2 journals.

---

## Features

- **5-phase pipeline**: Init → Data Prep → Analysis → Writing → Review, with milestone gates between phases
- **8 specialized AI agents**: Topic mining, data cleaning, statistical analysis, literature search, manuscript writing, verification, planning, and modification
- **Adaptive analysis**: Dynamically proposes statistical methods based on data characteristics (groups, timepoints, outcome types)
- **Publication-grade output**: ≥300 DPI figures, customizable `theme_pub()` theme and color palette, Vancouver citations with DOIs
- **Workflow enforcement**: 3 PreToolUse hooks guard phase ordering, milestone prerequisites, and prompt injection
- **Multi-study-type support**: RCT (CONSORT), Cohort/Case-Control/Cross-Sectional (STROBE), Descriptive
- **Import mode**: Import existing projects with automatic file role inference

---

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) >= 2.1.88
- R >= 4.3 (with required packages)
- Python >= 3.11

### Option 1: Plugin Marketplace (Recommended)

```bash
claude plugin install clinpub
```

### Option 2: Local Development

```bash
git clone https://github.com/Side-Peng/clinpub.git
claude --plugin-dir ./clinpub
```

### Option 3: Manual Install

See [INSTALL.md](INSTALL.md) for detailed instructions.

---

## Quick Start

```bash
/clinpub:overview               # View command reference
/clinpub:data2idea data.csv     # Mine topics from data
/clinpub:init                   # Phase 0: Initialize project
/clinpub:data-prep              # Phase 1: Data cleaning
/clinpub:analysis               # Phase 2: Statistical analysis
/clinpub:writing                # Phase 3: Manuscript drafting
/clinpub:review                 # Phase 4: Peer review simulation
/clinpub:milestone <N>          # Phase gate review
```

Each phase follows a 4-step pattern: **DISCUSS → PLAN → EXECUTE → VERIFY**.

Full tutorial, example data, and FAQ → `docs/getting-started.md`

---

## Architecture

### Three-Layer Design

```
USER → COMMANDS (commands/*.md — 11 entry points)
         → WORKFLOWS (pipeline/workflows/*.md — 10 orchestration files)
           → AGENTS (agents/*.md — 8 specialized agents, each with fresh context)
             → SCRIPTS (scripts/*.py — data profiler + native NCBI/PubMed search + R/Python tools)
             → HOOKS (hooks/ — 3 PreToolUse guards)
```

### Plugin Structure

```
clinpub/
├── .claude-plugin/             # Plugin manifest (plugin.json)
├── commands/                   # 11 slash command entry points
├── agents/                     # 8 specialized AI agents
├── pipeline/
│   ├── workflows/              # 10 phase orchestration files
│   ├── references/             # 15 reference documents
│   ├── templates/              # 18 templates (incl. 5 study types)
│   └── contexts/               # 2 context configurations
├── scripts/                    # Python tool scripts
├── hooks/                      # 4 hook files (3 guards + config)
├── docs/                       # 7 documentation files
├── AGENTS.md                   # Claude Code agent guidance
├── CLAUDE.md                   # Master Claude Code guidance
├── OVERVIEW.md                 # Skill entry point
├── CHANGELOG.md                # Version history
├── CONTRIBUTING.md             # Contribution guidelines
├── INSTALL.md                  # Installation guide
└── package.json                # npm metadata (v2.0.0)
```

### User Project Directory

```
Project_Root/
├── .clinpub/                   # Phase 0 — PROJECT.md / ROADMAP.md / STATE.md
├── 01_RawData/                 # Phase 1 — Raw data (read-only)
├── 02_PreprocessedData/        # Phase 1 — cleaned.csv + quality report
├── 03_AnalysisMethods/         # Phase 2 — Method code + docs
├── 04_Outputs/                 # Phase 2 — Figures + tables
├── Reference/                  # Phase 3 — Literature
├── 05_Manuscript/              # Phase 3-4 — IMRAD drafts
└── project_config.yml          # Central config
```

---

## Agents

| Agent | Language | Role |
|---|---|---|
| **Topic Miner Agent** | Python | Topic mining: data profiling, literature scan, candidate topic generation |
| **Analyst Agent** | R / Python | Data cleaning, statistical analysis, figure & table generation |
| **Reference Agent** | Python | Literature search (PubMed), PDF reading, citation management |
| **Writer Agent** | — | IMRAD manuscript drafting, figure integration, simulated review |
| **Clinpub Planner** | — | Research analysis planning with wave dependency graphs |
| **Clinpub Executor** | R / Python | Plan execution with atomic commits |
| **Clinpub Verifier** | — | Cross-phase verification (15 modes) |
| **Modify Agent** | R | Post-analysis modification: figure style, methods, variables |

---

## Commands

| Command | Phase | Description |
|---|---|---|
| `/clinpub:overview` | — | Command reference overview |
| `/clinpub:data2idea <file>` | — | Topic mining from data |
| `/clinpub:init` | 0 | Project setup or import existing |
| `/clinpub:data-prep` | 1 | Data cleaning → cleaned.csv |
| `/clinpub:analysis` | 2 | Adaptive statistical analysis |
| `/clinpub:writing` | 3 | IMRAD manuscript drafting |
| `/clinpub:review` | 4 | Peer review simulation + revision |
| `/clinpub:milestone <N>` | gate | Phase gate verification with user sign-off |
| `/clinpub:modify` | post-2 | Modify analysis outputs |
| `/clinpub:do` | — | Smart router: auto-detect state and route |
| `/clinpub:next-step` | — | Auto-advance to next step |

---

## Quality Gates

4 quality gates ensure phase-to-phase quality (see `pipeline/references/gates.md`):

| Gate | Position | Core Checks |
|---|---|---|
| IRB / Ethics | Phase 0 → 1 | IRB approval, de-identification, informed consent |
| Data Quality | Phase 1 → 2 | cleaned.csv integrity, missing rate, sample size |
| Analysis Validity | Phase 2 → 3 | All methods executed, effect sizes reported |
| Submission | Phase 4 → Submit | IMRAD complete, figures ≥300 DPI, all citations have DOI |

---

## Supported Study Types

| Study Type | Reporting Guideline |
|---|---|
| Randomized Controlled Trial (RCT) | CONSORT |
| Cohort Study | STROBE |
| Case-Control Study | STROBE |
| Cross-Sectional Study | STROBE |
| Descriptive Study | STROBE |

---

## Hooks

3 PreToolUse hooks protect the analysis workflow (declared in `hooks/hooks.json`):

| Hook | Trigger | Purpose |
|---|---|---|
| `clinpub-workflow-guard.js` | Write / Edit | Block cross-phase file writes |
| `clinpub-phase-boundary.sh` | Bash | Check milestone prerequisites |
| `clinpub-prompt-guard.js` | Read | Scan data files for prompt injection |

---

## Publication-Grade Figures

| Requirement | Standard |
|---|---|
| Resolution | ≥ 300 DPI |
| Format | SVG > TIFF > PDF > PNG |
| Font | Arial ≥ 8pt (`theme_pub(base_family = "sans")`) |
| Colors | Auto by group count (Nature dual / RColorBrewer / viridis), supports custom colors and group mapping (colorblind-friendly) |
| Size | Single column 89mm, double column 183mm (Nature series) |
| Theme | `theme_pub()` unified style, customizable font size, font family, legend position, title alignment, etc. (see `pipeline/references/r_patterns.md`) |

---

## Dependencies

### External Skills

| Skill | Purpose |
|---|---|
| `tavily` | Supplementary search |
| `pdf-reader` | PDF full-text reading |

### R Packages

- **Data processing**: dplyr, tidyr, stringr, readr, readxl
- **Statistics**: stats, survival, lme4, glmnet, pROC
- **Visualization**: ggplot2, ggpubr, patchwork, survminer, ggsurvfit, ggsignif, RColorBrewer, viridis
- **Output**: gtsummary, flextable, openxlsx
- **Paths**: here, fs
- **Configuration**: yaml

### Python Packages

pandas >= 2.0, numpy >= 1.24, requests >= 2.31, openpyxl >= 3.1

---

## Documentation

| Document | Description |
|---|---|
| [Getting Started](docs/getting-started.md) | End-to-end tutorial: from zero to submission |
| [Architecture](docs/ARCHITECTURE.md) | System architecture documentation |
| [Configuration](docs/CONFIGURATION.md) | `project_config.yml` structure guide |
| [Development](docs/DEVELOPMENT.md) | Development principles and guidelines |
| [Installation](INSTALL.md) | Detailed installation instructions |
| [Contributing](CONTRIBUTING.md) | Contribution guidelines |
| [Changelog](CHANGELOG.md) | Version history |

---

## Environment Variables

| Variable | Required | Purpose |
|---|---|---|
| `NCBI_API_KEY` | Optional | PubMed API rate limit increase |
| `TAVILY_API_KEY` | Optional | Tavily search API |
| `UNPAYWALL_EMAIL` | Optional | Unpaywall PDF access |

---

## Contributing

Contributions are welcome! The core principle is **self-contained code**: every script must define all variables, dependencies, and helper functions locally — no cross-file implicit dependencies.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## License

This project is licensed under the **MIT License** — see the LICENSE file for details.

---

<div align="center">

**Made with dedication for clinical researchers worldwide.**

[↑ Back to Top](#clinpub)

</div>
