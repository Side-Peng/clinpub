# ClinPub — 临床研究发表管线

端到端临床数据分析与 SCI 发表管线，覆盖从原始数据到论文投稿的完整流程。

> End-to-end clinical data analysis and publication pipeline for SCI Q1/Q2 journals.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

**ClinPub** 扮演**资深医学统计学家 + 学术写作顾问**。处理已整理的患者级数据（每行一个患者，每列一个变量），输出统计结果、出版级图表和可投稿论文。

**目标期刊**: Alzheimer's & Dementia, Molecular Psychiatry 及其他 SCI Q1/Q2 期刊。

## 🚀 平台版本

本仓库包含 ClinPub 在多个 AI 编码平台上的适配版本，各版本共享相同的方法论和流程设计，按平台特性独立实现。

| 平台 | 目录 | 状态 | 安装方式 |
|------|------|------|----------|
| **[DeepSeek Harness](docs/MIGRATION-TO-DSH.md)** | `.dsh/skills/` + `dsh/` | 🚧 **主版本（进行中）** | 仓库内自动发现；跨项目需链接到 `~/.agents/skills` |
| [Claude Code](claude-code/) | `claude-code/` | ✅ v3.0.0 | `claude plugin install clinpub`（Marketplace）或 `claude --plugin-dir ./claude-code`（本地） |
| [OpenAI Codex](codex/) | `codex/clinpub/` | ✅ v3.0.0 | `codex plugin install ./codex/clinpub`（本地）或 Marketplace |

> **Qoder 平台已于 3.0 移除**（2026-10-18）。历史版本可从 git 记录中取回。后续主版本以 DeepSeek Harness 为主，Claude Code / Codex 作为已同步的稳定版保留。

## 📋 管线概览

```
阶段0          阶段1         阶段2             阶段3
项目初始化  →  数据清洗  →  迭代分析  →  递进写作（核心管线终点）
                ↓             ↓                ↓
              cleaned.csv    图表+表格      sections/ → manuscript.md

阶段2 迭代：每批 1–3 个方法 → 看结果 → 据决策规则定下一批 → 饱和后冻结阶段3 递进：图表骨架 → Results → Methods → Discussion → Conclusion → 叙事设计 → Introduction → Abstract

独立工具（不占 Phase）：improving（改进）· coverletter（投稿信）· review（投稿后审稿回复）· modify（分析修改）· data2idea（选题挖掘）
```

### 核心能力

- **12+ 统计方法**：基线表、组间比较、回归、生存分析、ROC、LASSO、PSM、RCS、MICE、中介/调节、聚类等
- **5 种研究类型**：RCT、队列、病例对照、横断面、描述性
- **迭代分析**：方法不是一次定完的，而是每批根据上一批结果与决策规则库推进
- **递进写作**：从结果往回写（Results 先于 Introduction），每节读前节实际内容，改一节自动标脏下游
- **PubMed 内置检索**：文献搜索、引用管理、Vancouver 格式输出
- **出版级输出**：≥300 DPI 图表、可配置主题/配色、CONSORT/STROBE/PRISMA 规范

## 🚀 快速开始

> **前提**：所有命令均在**仓库根目录**执行（先克隆并进入目录）：
>
> ```bash
> git clone https://github.com/Side-Peng/clinpub.git
> cd clinpub
> ```

### Claude Code

**方式一：Marketplace（推荐，正式使用）**

```bash
claude plugin marketplace add Side-Peng/clinpub   # 添加 GitHub 插件源（需联网）
claude plugin install clinpub                     # 安装插件
```

安装后**重启 Claude Code**，输入 `/clinpub help` 验证插件已加载。

**方式二：本地目录（开发调试，免发布）**

```bash
claude --plugin-dir ./claude-code
```

详见 [claude-code/INSTALL.md](claude-code/INSTALL.md)

### OpenAI Codex

**方式一：本地目录**

```bash
codex plugin install ./codex/clinpub
```

**方式二：个人 Marketplace**

```bash
codex plugin marketplace add <本仓库绝对路径>/codex   # 例如 /Users/you/clinpub/codex
codex plugin install clinpub
```

详见 [codex/INSTALL.md](codex/INSTALL.md)

### DeepSeek Harness（主版本）

> 自 3.0 起，**DSH 是主实现**，技能与工作流在此演进，再同步回 claude-code / codex。
> 迁移方案见 [docs/MIGRATION-TO-DSH.md](docs/MIGRATION-TO-DSH.md)（进行中）。

**在仓库内使用（零安装）**：DSH 会自动发现 `.dsh/skills/`，打开本仓库即可看到 14 个 `clinpub-*` 技能。

**跨项目使用**：把技能目录链接到用户技能根（`~/.agents/skills` 或 `~/.dsh/skills`）。

## 📦 项目结构

```
clinpub/
├── .dsh/skills/    # DeepSeek Harness 技能（主版本，仓库内自动生效）
├── dsh/            # DSH 共享核心（pipeline / agents / scripts）
├── claude-code/    # Claude Code 插件（.claude-plugin 格式）
├── codex/          # Codex 插件（.codex-plugin 格式）
├── docs/           # 通用开发文档
├── CHANGELOG.md    # 版本历史
└── README.md       # 本文件
```

## 🏗️ 架构设计

### 三层架构

```
用户 → 命令 (commands/*.md - 10 个入口)
       → 工作流 (pipeline/workflows/*.md - 10 个编排文件)
         → 智能体 (agents/*.md - 6 个专业智能体，每次独立上下文)
           → 脚本 (scripts/*.py - 数据画像 + 内置 NCBI/PubMed 检索 + R/Python 工具)
           → 钩子 (hooks/ - 3 个 PreToolUse 守卫)
```

### 6 个专业智能体

| 智能体 | 语言 | 职责 |
|--------|------|------|
| Topic Miner Agent | Python | 数据画像、文献扫描、候选课题生成 |
| Analyst Agent | R / Python | 数据清洗、迭代统计分析、图表生成 |
| Reference Agent | Python | 文献搜索（PubMed）、PDF 阅读、引用管理 |
| Writer Agent | — | 递进式撰写（R→M→D→C→I→Abstract）、图表整合、改进与投稿后修订 |
| Clinpub Verifier | — | 跨阶段验证（15 种模式） |
| Modify Agent | R | 分析后修改：图表样式、方法、变量、新增方法 |

## 📚 命令参考

> 下表命令行为以 **v3.0.0** 为准，claude-code / codex 已同步；DSH 版为 3.0 主实现（进行中）。Codex 中阶段0 技能名为 `clinpub:init`。

| 命令 | 阶段 | 描述 |
|------|------|------|
| `overview` | — | 命令参考概览 |
| `data2idea <file>` | — | 从数据中挖掘选题 |
| `initialize` | 0 | 项目设置或导入现有项目（询问目标期刊） |
| `data-prep` | 1 | 数据清洗 → cleaned.csv |
| `analysis` | 2 | 自适应统计分析 |
| `writing` | 3 | IMRAD 论文撰写（核心管线终点） |
| `improving` | 工具 | 自审 + 直接改进稿件与分析（可反复） |
| `coverletter` | 工具 | 按目标期刊生成投稿信 |
| `review` | 工具 | 投稿后：处理真实审稿意见 → 回复信 → 调用 improving 修稿 |
| `milestone <N>` | gate | 阶段关卡验证 |
| `modify` | 工具 | 修改分析输出或新增分析方法 |
| `do` | — | 智能路由：自动检测状态并路由 |
| `next-step` | — | 自动推进到下一步 |

## 🔒 质量门控

4 个质量门控确保阶段间质量（见 `pipeline/references/gates.md`）：

| 门控 | 位置 | 核心检查 |
|------|------|----------|
| IRB / 伦理 | 阶段0 → 1 | IRB 批准、去标识化、知情同意 |
| 数据质量 | 阶段1 → 2 | cleaned.csv 完整性、缺失率、样本量 |
| 分析有效性 | 阶段2 → 3 | 所有方法已执行、效应量已报告 |
| 投稿准备 | 阶段3 → 提交 | IMRAD 完整、图表 ≥300 DPI、所有引用有 DOI |

## 📊 支持的研究类型

| 研究类型 | 报告规范 |
|----------|----------|
| 随机对照试验 (RCT) | CONSORT |
| 队列研究 | STROBE |
| 病例对照研究 | STROBE |
| 横断面研究 | STROBE |
| 描述性研究 | STROBE |

## 📈 出版级图表标准

| 要求 | 标准 |
|------|------|
| 分辨率 | ≥300 DPI |
| 格式 | SVG > TIFF > PDF > PNG |
| 字体 | Arial ≥8pt (`theme_pub(base_family = "sans")`) |
| 颜色 | 按组数自动（Nature 双色 / RColorBrewer / viridis），支持自定义颜色和组映射（色盲友好） |
| 尺寸 | 单栏 89mm，双栏 183mm（Nature 系列） |
| 主题 | `theme_pub()` 统一样式，可自定义字体大小、字体族、图例位置、标题对齐等 |

## 🔧 依赖

### R 包

```r
install.packages(c(
  "dplyr", "tidyr", "stringr", "readr", "readxl",
  "survival", "lme4", "glmnet", "pROC",
  "gtsummary", "flextable", "openxlsx",
  "ggplot2", "ggpubr", "patchwork", "survminer", "ggsurvfit", "ggsignif",
  "here", "fs", "yaml", "RColorBrewer", "viridis"
))
```

### Python 包

```bash
pip install pandas numpy requests openpyxl
```

### 环境变量（可选）

| 变量 | 必需 | 用途 |
|------|------|------|
| `NCBI_API_KEY` | 可选 | PubMed API 速率限制提升 |
| `TAVILY_API_KEY` | 可选 | Tavily 搜索 API |
| `UNPAYWALL_EMAIL` | 可选 | Unpaywall PDF 访问 |

## 📖 文档

| 文档 | 描述 |
|------|------|
| [Claude Code 文档](claude-code/CLAUDE.md) | Claude Code 插件详细文档 |
| [Codex 安装指南](codex/INSTALL.md) | Codex 插件安装说明 |
| [DSH 迁移方案](docs/MIGRATION-TO-DSH.md) | DeepSeek Harness 主版本的迁移设计 |
| [CHANGELOG.md](CHANGELOG.md) | 版本历史 |

## 🤝 贡献

各平台版本的贡献指南见对应目录：

- [Claude Code 贡献指南](claude-code/CONTRIBUTING.md)
- Codex 版本遵循相同的代码独立原则

## 📄 License

MIT

## 👨‍💻 Author

**Side-Peng**
- Email: 1304916798@qq.com
- GitHub: [@Side-Peng](https://github.com/Side-Peng)

## 🔗 Links

- [Repository](https://github.com/Side-Peng/clinpub)
- [Issues](https://github.com/Side-Peng/clinpub/issues)
- [Releases](https://github.com/Side-Peng/clinpub/releases)
