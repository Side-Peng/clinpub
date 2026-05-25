# Changelog

All notable changes to the clinpub project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.2.0] - 2026-05-25

### Changed
- **README**: 命令参考移除被废弃的 `clinpub` 一键入口，改为独立 Phase 命令参考
- **文献检索**：移除内置 ncbi_search.py/pubmed_search.py，统一使用 ncbi-search skill

### Removed
- **`/clinpub` 一键五阶段执行**：改为独立 Phase 命令参考（见 commit 0866e2b）
- **内置文献检索脚本**：ncbi_search.py, pubmed_search.py, ncbi_client.py, tavily_search.py — 统一由外部 skill 替代

### Docs
- `docs/getting-started.md` 泛化：移除示例数据具体引用，教程改为通用描述

## [1.1.0] - 2026-04-27

### Added — Must Have 补全
- **3 new agents**: Clinpub Planner, Clinpub Executor (atomic commits), Clinpub Verifier (adversarial verification)
- **4 new references**: mandatory-initial-read, gates (IRB/data/analysis/submission), verification-patterns (8 patterns), agent-contracts (7 agents)
- **5 new templates**: UAT, VALIDATION, verification-report, spec, context
- **3 hooks**: workflow-guard (JS), phase-boundary (SH), prompt-guard (JS for injection detection)
- **`.claude/settings.json`**: Hook registration for Claude Code

### Added — GitHub 发布准备
- **SKILL.md**: Claude Code skill 入口文件（触发描述 + 命令参考 + 架构说明）
- **INSTALL.md**: 安装指南（npx clinpub-cc 一键安装 + 依赖说明 + 故障排除）
- **requirements.txt**: Python 依赖清单
- **`bin/install.js`**: npm 安装器（复刻 GSD 模式：commands → skills 转换 + 资源复制 + 路径重写）
- **`.github/workflows/release.yml`**: 自动发布工作流（打 tag → npm publish → GitHub Release）

### Updated
- **CLAUDE.md**: Added agents, hooks, references, templates, agent routing table
- **README.md**: Added quality gates, hooks, 7-agent collaboration table

## [1.0.0] - 2026-04-27

### Added
- **Phase 0 — init**: Project initialization with research framework discussion
- **Phase 1 — data-prep**: Data cleaning, EDA, cleaned.csv generation
- **Phase 2 — analysis**: Wave-based statistical analysis (10 methods)
- **Phase 3 — writing**: IMRAD manuscript writing with Humanizer rules
- **Phase 4 — review**: Simulated peer review and revision
- **Topic mining** (`clinpub:data2idea`): Data-driven paper topic discovery
- **Milestone system**: Phase-gate verification with user sign-off
- **Checkpoint system**: In-phase decision points and verification gates
- **4 Agents**: Topic Miner, Analyst, Reference, Writer
- **5 study type templates**: RCT, cohort, case-control, cross-sectional, descriptive
- **12 analysis methods**: Baseline table, group comparison, regression, survival, etc.
- **GSD architecture**: Commands → Workflows → Agents → Scripts layered design
