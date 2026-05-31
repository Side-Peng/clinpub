# clinpub

## What This Is

clinpub 是一个临床数据分析与稿件自动生成管线。它扮演资深医学统计师 + 学术写作顾问的角色，处理患者级数据，经过数据清洗、统计分析、话题挖掘、IMRAD 手稿撰写、模拟同行评审五个阶段，产出面向 SCI Q1/Q2 期刊的投稿级稿件。

## Core Value

用户提供原始临床数据，clinpub 输出结构化的分析结果和可投稿的 IMRAD 手稿。分析可复现、方法可追溯、引用有依据。

## Requirements

### Validated

- ✓ 完整的 GSD 分层架构（commands → agents → pipeline）— 现有
- ✓ 7 个专化 Agent（analyst, reference, writer, topic-miner, planner, executor, verifier）— 现有
- ✓ Phase 0-4 管线编排（init-project, data-prep, analysis, writing, review）— 现有
- ✓ 5 个 Python 工具脚本（data_profiler, ncbi_search, pubmed_search, ncbi_client, tavily_search）— 现有
- ✓ 3 个 Claude Code hooks（workflow-guard, phase-boundary, prompt-guard）— 现有
- ✓ Phase 2 Analysis 支持 WAVE 子任务机制 — 现有
- ✓ 研究类型模板（RCT, cohort, case_control, cross_sectional, descriptive）— 现有
- ✓ Phase 前调研流程标准化（FLOW-01）：轨道选择 + Track A/B 搜索 + RESEARCH.md 模板 — Phase 5
- ✓ BUG-01: Hook 正则修复 — Phase 1
- ✓ BUG-02: 数据联动更新 — Phase 1
- ✓ NEXT-01: `/clinpub-do` 命令 — Phase 2
- ✓ NEXT-02: `/clinpub-next-step` 命令 — Phase 2
- ✓ NEXT-03: Phase/Wave 结束 clear 提示 — Phase 2
- ✓ WRITE-01: IMRAD 各段独立撰写 — Phase 3
- ✓ WRITE-02: 终稿拼接（非重写）— Phase 3
- ✓ CITE-01: 引用策略 30-55 篇 — Phase 3
- ✓ CITE-02: 引用前用户讨论 — Phase 3
- ✓ METH-01: 未知方法自动搜索 — Phase 4
- ✓ METH-02: 组间对比方法固化 — Phase 4
- ✓ CHART-01: 图表质量优化（theme_pub + KM 曲线 + 热图）— Phase 6
- ✓ DOC-01: 方法说明中文撰写 — Phase 6
- ✓ DOC-02: README→方法说明改名 — Phase 6

### Active

（无待办需求，全部已验证或归档）

### Out of Scope

- npm 包发布 — 开发到满意后再发版
- 自动化单元测试 — 纯开发环境，开发者自行测试
- CI/CD 测试流水线 — 同上

## Context

- 项目已通过 Must Have 重构，架构稳定
- 最近一次用户实测暴露了 11 个改进点，需要分批优化
- 开发环境为 Windows，需考虑 CRLF 兼容性
- R 代码由 Analyst Agent 分析时动态生成，仓库中无静态 R 文件

## Constraints

- **环境**: Node >= 22.0.0
- **语言**: R 包依赖 18+ 个 CRAN 包（无版本锁定）
- **数据**: .gitignore 全局忽略 `*.csv`/`*.xlsx`，示例数据无法提交
- **平台**: Windows 开发为主，部分文件存在 CRLF/LF 问题

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| WAVE = Phase 2 的子任务 | 每个统计方法独立执行单元 | ✓ Phase 2 |
| 手稿拼接策略 IMRAD 各段独立 | 各段独立引用后再合并，避免终稿重写产生格式漂移 | ✓ Phase 3 |
| Bug 修复立即执行 | 影响基础可用性，不等 roadmap 排期 | ✓ Phase 1 |
| 测试由开发者外部完成 | 纯开发环境，不设自动化测试 | — Pending |
| 方法说明替代 README | 中文本地化，模板统一 | ✓ Phase 6 |
| theme_pub() 统一图表风格 | Nature 配色 + Arial + 标准尺寸 | ✓ Phase 6 |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition**:
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone**:
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-28 after Phase 6 completion (图表+文档优化)*
