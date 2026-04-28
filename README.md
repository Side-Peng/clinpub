# clinpub — 临床数据分析与发表管线

[clínica + publish] 面向 SCI Q1/Q2 期刊的端到端临床数据分析和发表加速器。

## 概述

扮演**资深医学统计学家 + 学术写作顾问**。处理已整理的患者级数据（每行一个患者，每列一个变量），输出统计结果、出版级图表和可投稿论文。

**目标期刊**：Alzheimer's & Dementia、Molecular Psychiatry 等 SCI Q1/Q2 水平。

## 快速开始

```bash
npx clinpub-cc@latest        # 一键安装
/clinpub                     # 启动完整管线
```

完整教程、示例数据和常见问题 → `docs/getting-started.md`

## 架构

```
commands/clinpub/*.md — Thin entry points (user-facing)
agents/*.md            — Specialized AI agent role cards (7 agents)
pipeline/
  workflows/*.md       — Phase orchestration logic
  references/*.md      — Reference documents (8 files)
  templates/*.md       — Templates (13 files including study types)
  contexts/*.md        — Context configurations
scripts/*.py           — Tool scripts (profiling, search, PDF)
hooks/*.js/*.sh        — Claude Code hooks (workflow guard, phase boundary, prompt guard)
docs/                  — Tutorials and guides
examples/              — Sample data and example configs
tests/                 — Test files
```

### 三层架构

```
USER → COMMANDS (commands/clinpub/clinpub.md)
         → WORKFLOWS (pipeline/workflows/*.md)
           → AGENTS (agents/*.md — each with fresh context)
             → SCRIPTS (scripts/*.py — R/Python tools)
             → HOOKS (hooks/*.js/*.sh — workflow enforcement)
```

### Agent 协作

| Agent | 语言 | 职责 |
|-------|------|------|
| **Topic Miner Agent** | Python | 选题挖掘（data2idea）：数据画像、文献扫描、选题生成 |
| **Analyst Agent** | R 为主 / Python 辅助 | 数据清洗、统计分析、出图出表 |
| **Reference Agent** | Python | 文献检索、PDF 全文读取、引用管理 |
| **Writer Agent** | — | IMRAD 撰写、图表整合、模拟审稿 |
| **Clinpub Planner** | — | 研究分析规划，创建可执行的 PLAN.md（波次依赖图） |
| **Clinpub Executor** | R/Python | 分析执行，原子提交，偏差处理，SUMMARY.md 生成 |
| **Clinpub Verifier** | — | 跨阶段验证（Phase 1 数据质量 + Phase 2 统计 + Phase 3 论文），15 种验证模式 |

### 阶段化流程

每个阶段四步：**DISCUSS → PLAN → EXECUTE → VERIFY**。Phase 之间通过 **Milestone** 关卡评审，验证成功标准、记录决策、用户签字后放行。

| Phase | 名称 | 产出 |
|-------|------|------|
| 0 | init | 研究框架、目录结构、项目配置 |
| 1 | data-prep | cleaned.csv + 数据质量报告 |
| 2 | analysis | 按数据特征动态定制的分析方案（图 + 表 + 统计报告） |
| 3 | writing | IMRAD 各章节 draft.md |
| 4 | review | 审稿意见 + response letter + 修订稿 |

### 项目目录结构

```
Project_Root/
├── .planning/                  # 规划层（PROJECT.md / ROADMAP.md / STATE.md）
├── 01_RawData/                 # 原始数据（只读）
├── 02_PreprocessedData/        # Phase 1 产出
├── 03_AnalysisMethods/         # Phase 2 方法目录
├── 04_Outputs/                 # 图表输出
├── Reference/                  # 文献
├── 05_Manuscript/             # 论文各章节 draft.md
└── project_config.yml + run_all.R
```

## 命令参考

| 命令 | 用途 |
|------|------|
| `clinpub` | 主入口：启动完整 5 阶段管线 |
| `clinpub:data2idea` | 选题挖掘：从数据中找论文思路 |
| `clinpub:init-project` | Phase 0：项目初始化 |
| `clinpub:data-prep` | Phase 1：数据准备 |
| `clinpub:analysis` | Phase 2：统计分析 |
| `clinpub:writing` | Phase 3：论文撰写 |
| `clinpub:review` | Phase 4：审稿修稿 |
| `clinpub:milestone <N>` | Phase 关卡评审：验证成功标准、记录决策、用户签字放行 |

## 质量门控

4 道质量门控确保阶段间质量（详见 `pipeline/references/gates.md`）：

| Gate | 位置 | 核心检查 |
|------|------|----------|
| IRB / Ethics Gate | Phase 0 → 1 | IRB 批准、数据去标识化、知情同意 |
| Data Quality Gate | Phase 1 → 2 | cleaned.csv 完整、缺失率受控、样本量充足 |
| Analysis Validity Gate | Phase 2 → 3 | 所有方法已执行、效应量报告、假设检验 |
| Submission Gate | Phase 4 → Submit | IMRAD 完整、图表 >=300 DPI、引用全有 DOI |

## 支持的研究类型

- 随机对照试验（RCT）— CONSORT
- 队列研究（Cohort）— STROBE
- 病例对照研究（Case-Control）— STROBE
- 横断面研究（Cross-Sectional）— STROBE
- 描述性研究（Descriptive）— STROBE

## Hooks（工作流保护）

3 个 Claude Code hooks 保护分析流程（注册在 `.claude/settings.json`）：

| Hook | 触发时机 | 作用 |
|------|----------|------|
| `clinpub-workflow-guard.js` | Write/Edit | 阻止越阶段写文件 |
| `clinpub-phase-boundary.sh` | Bash | 检查前置 milestone 完成状态 |
| `clinpub-prompt-guard.js` | Read | 扫描数据文件中的 prompt injection |

## 依赖

### 关联技能
- ncbi-search — PubMed 文献检索
- tavily — 补充信息检索
- pdf-reader — PDF 全文阅读

### R 包
- **数据处理**：dplyr, tidyr, stringr, readr, readxl
- **统计**：stats, survival, lme4, glmnet, pROC
- **可视化**：ggplot2, ggpubr, patchwork, survminer, ggsurvfit, ggsignif
- **输出**：gtsummary, flextable, openxlsx
- **路径**：here, fs

### Python 包
pandas, numpy, requests, pathlib, openpyxl, tavily-python

## 出版级图表标准

| 要求 | 标准 |
|------|------|
| 分辨率 | ≥300 DPI |
| 格式 | PNG / PDF / TIFF (LZW) |
| 字体 | Arial ≥8pt |
| 配色 | viridis / RColorBrewer（色盲友好） |
| 尺寸 | 单栏 8 cm，双栏 17 cm |

## 许可证

MIT License
