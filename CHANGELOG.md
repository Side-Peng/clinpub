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

## [1.1.0] - 2026-05-28

### Added — Phase 1-6 优化（GSD 管线执行）

**Phase 1: Bug Fixes**
- Hook 正则修复（STATE.md 标识行 + getCurrentPhase() 新正则）
- 数据联动更新（data-prep 重新进入检测 + 工作流刷新步骤）

**Phase 2: 断点续做**
- `/clinpub-do` 命令：工作区状态自动检测 + NL 意图路由
- `/clinpub-next-step` 命令 + clear 提示标准化

**Phase 3: 手稿拼接+引用策略**
- 分段撰写流程改造：逐段顺序撰写 + reference-agent 预搜索 + 用户审阅 pause
- 引用管理与交叉引用：shared reference library JSON schema + placeholder 约定 + 去重规则
- 终稿拼接输出：7 步拼接协议（段落合并 + 占位符替换 + 引用统一编号 + YAML frontmatter）
- 命令入口适配：更新 writing.md 描述和引用
- 引用策略标准化：策略参考文档 + writing workflow 插入讨论步 + reference-agent 搜索支持 IF/年份过滤

**Phase 4: 方法增强**
- 组间对比方法决策树文档（comparison-methods.md）：2组/3+组×连续/分类+配对 全覆盖 + 效应量标准
- reference-agent method_search 未知方法搜索模式 + 分析工作流集成

**Phase 5: Phase 前调研流程**
- pre-phase-research.md 参考文档（轨道选择、Track A/B 协议、RESEARCH.md 模板）
- reference-agent 扩展：phase_research 模式

**Phase 6: 图表+文档优化**
- theme_pub() 主题优化：base_size=10, base_family=sans, legend.right, axis.line
- 新增 §2.9 KM 生存曲线美化模板（survminer + theme_pub）
- 新增 §2.10 相关性矩阵热图模板（ggcorrplot + theme_pub）
- 字体族跨平台说明 + Nature 系列尺寸参考
- 方法说明模板（pipeline/templates/method-readme.md）
- 文档中文本地化：6 个管线文档 README→方法说明 + 13 处遗留修复

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
