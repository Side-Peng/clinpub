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
| [Claude Code](claude-code/) | `claude-code/` | v2.2.0 稳定版 | `claude --plugin-dir ./claude-code` 或 marketplace |
| [OpenAI Codex](codex/) | `codex/` | ✅ v2.2.0 稳定版 | `codex plugin install ./codex/clinpub` 或 marketplace |
| [QoderWork](qoder/) | `qoder/` | v1.0.0 首发版 | 复制到 `~/.qoderworkcn/plugins-custom/clinpub` |

## 📋 管线概览

```
Phase 0          Phase 1         Phase 2           Phase 3         Phase 4
项目初始化  →  数据清洗  →  统计分析  →  论文写作  →  同行评审
                ↓             ↓              ↓            ↓
              cleaned.csv    图表+表格     manuscript.md    final/
```

### 核心能力

- **12+ 统计方法**：基线表、组间比较、回归、生存分析、ROC、LASSO、PSM、RCS、MICE、中介/调节、聚类等
- **5 种研究类型**：RCT、队列、病例对照、横断面、描述性
- **双模式写作**：一键成稿 / 逐步写作，内置反 AI 写作规则
- **PubMed 内置检索**：文献搜索、引用管理、Vancouver 格式输出
- **出版级输出**：≥300 DPI 图表、可配置主题/配色、CONSORT/STROBE/PRISMA 规范

## 🚀 快速开始

### Claude Code

```bash
# 开发模式
claude --plugin-dir ./claude-code

# Marketplace
claude plugin install clinpub
```

详见 [claude-code/INSTALL.md](claude-code/INSTALL.md)

### OpenAI Codex

```bash
# 本地安装
cd codex
codex plugin install ./clinpub

# 或添加到个人市场
codex plugin marketplace add ./codex
codex plugin install clinpub
```

详见 [codex/INSTALL.md](codex/INSTALL.md)

### QoderWork

```bash
# 将 qoder/ 目录复制到插件目录
cp -r qoder/ ~/.qoderworkcn/plugins-custom/clinpub
```

安装后在对话中 `@编排器` 启动项目，或 `@项目初始化` 开始新项目。

## 📦 项目结构

```
clinpub/
├── claude-code/    # Claude Code 插件（.claude-plugin 格式）
├── codex/          # Codex 插件（.codex-plugin 格式）
├── qoder/          # QoderWork 插件（.qoder-plugin 格式）
├── docs/           # 通用开发文档
├── CHANGELOG.md    # 版本历史
└── README.md       # 本文件
```

## 🏗️ 架构设计

### 三层架构

```
用户 → 命令 (commands/*.md - 11 个入口)
       → 工作流 (pipeline/workflows/*.md - 10 个编排文件)
         → 智能体 (agents/*.md - 8 个专业智能体，每次独立上下文)
           → 脚本 (scripts/*.py - 数据画像 + 内置 NCBI/PubMed 检索 + R/Python 工具)
           → 钩子 (hooks/ - 3 个 PreToolUse 守卫)
```

### 8 个专业智能体

| 智能体 | 语言 | 职责 |
|--------|------|------|
| Topic Miner Agent | Python | 数据画像、文献扫描、候选课题生成 |
| Analyst Agent | R / Python | 数据清洗、统计分析、图表生成 |
| Reference Agent | Python | 文献搜索（PubMed）、PDF 阅读、引用管理 |
| Writer Agent | — | IMRAD 论文撰写、图表整合、模拟评审 |
| Clinpub Planner | — | 研究分析规划（波次依赖图） |
| Clinpub Executor | R / Python | 计划执行（原子提交） |
| Clinpub Verifier | — | 跨阶段验证（15 种模式） |
| Modify Agent | R | 分析后修改：图表样式、方法、变量 |

## 📚 命令参考

| 命令 | 阶段 | 描述 |
|------|------|------|
| `overview` | — | 命令参考概览 |
| `data2idea <file>` | — | 从数据中挖掘选题 |
| `init` | 0 | 项目设置或导入现有项目 |
| `data-prep` | 1 | 数据清洗 → cleaned.csv |
| `analysis` | 2 | 自适应统计分析 |
| `writing` | 3 | IMRAD 论文撰写 |
| `review` | 4 | 同行评审模拟 + 修改 |
| `milestone <N>` | gate | 阶段关卡验证 |
| `modify` | post-2 | 修改分析输出 |
| `do` | — | 智能路由：自动检测状态并路由 |
| `next-step` | — | 自动推进到下一步 |

## 🔒 质量门控

4 个质量门控确保阶段间质量（见 `pipeline/references/gates.md`）：

| 门控 | 位置 | 核心检查 |
|------|------|----------|
| IRB / 伦理 | Phase 0 → 1 | IRB 批准、去标识化、知情同意 |
| 数据质量 | Phase 1 → 2 | cleaned.csv 完整性、缺失率、样本量 |
| 分析有效性 | Phase 2 → 3 | 所有方法已执行、效应量已报告 |
| 投稿准备 | Phase 4 → 提交 | IMRAD 完整、图表 ≥300 DPI、所有引用有 DOI |

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
| [Codex 转换摘要](codex/CONVERSION_SUMMARY.md) | Claude Code → Codex 转换说明 |
| [Qoder 文档](qoder/README.md) | QoderWork 插件文档 |
| [CHANGELOG.md](CHANGELOG.md) | 版本历史 |

## 🤝 贡献

各平台版本的贡献指南见对应目录：

- [Claude Code 贡献指南](claude-code/CONTRIBUTING.md)
- Codex / Qoder 版本遵循相同的代码独立原则

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
