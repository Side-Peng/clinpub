---
phase: 04-方法增强
plan: 01
subsystem: references
tags: comparison-methods, decision-tree, statistical-tests, effect-size

# Dependency graph
requires:
  - phase: 03-手稿拼接
    provides: 参考文档 convention（analysis_methods.md 格式风格）
provides:
  - 组间对比方法决策树文档 comparison-methods.md，覆盖 2组/3+组 × 连续/分类 × 配对/重复测量
  - analysis_methods.md §3.2 的交叉引用，链接到更细粒度的分支规则
affects: planner-agent, analyst-agent

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "参考文档表格+代码块混合排版（概览树 → 细则 → R 代码参考）"
    - "decision tree 优先用表格呈现，比纯文字更直观"

key-files:
  created:
    - pipeline/references/comparison-methods.md
  modified:
    - pipeline/references/analysis_methods.md

key-decisions:
  - "决策树用概览表 + 逐节细化的双层结构替代单一大表，提高可读性"
  - "每节附带 R 代码参考块，确保 analyst-agent 可直接复制使用"
  - "效应量统一为 Cohen's d / r / η² / Cramer's V，覆盖所有检验场景"

patterns-established:
  - "方法决策树文档模式：概览树 → 分节细则 → R 代码 → 效应量报告标准"

requirements-completed: [METH-02]

# Metrics
duration: 3 min
completed: 2026-05-07
---

# Phase 4 Plan 1: 组间对比方法决策树 Summary

**创建 comparison-methods.md 组间对比方法决策树文档，覆盖 13 个决策分支（D-08 ~ D-13），并在 analysis_methods.md §3.2 追加交叉引用**

## Performance

- **Duration:** 3 min
- **Started:** 2026-05-07T21:50:57+08:00
- **Completed:** 2026-05-07T21:53:59+08:00
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- 创建 `pipeline/references/comparison-methods.md` — 6 章节完整决策树文档：
  - 概览树：2组/3+组 × 连续/分类 共 10 个分支路径的概览表
  - 两组比较细则：正态性+方差齐性驱动的自动分支逻辑 + R 代码
  - 三组以上比较细则：ANOVA/Welch ANOVA/Kruskal-Wallis 三路分支 + 事后比较
  - 配对/重复测量设计：6 种设计场景全覆盖
  - 效应量报告标准：8 种检验方法的效应量公式 + 解释基准
  - 执行步骤：从读数据到输出的标准化 9 步流程
- 在 `analysis_methods.md` §3.2 的三个组间比较小节下方追加了指向 `comparison-methods.md` 的交叉引用（§二/§三/§四）

## Task Commits

Each task was committed atomically:

1. **Task 1: 创建组间对比方法决策树文档** — `afe8701` (feat)
2. **Task 2: 在 analysis_methods.md 中追加交叉引用** — `c90c84d` (feat)

## Files Created/Modified

- `pipeline/references/comparison-methods.md` — 组间对比方法决策树参考文档（新建，7.3KB，206 行）
- `pipeline/references/analysis_methods.md` — 追加 3 处交叉引用（+3 行）

## Decisions Made

- 决策树采用"概览表 + 逐节细则"双层结构，而非单一大表：概览表提供快速查找，每节的细则含前提条件检测逻辑和 R 代码参考，兼顾易用性和实用性
- 每节附加 R 代码块（而非伪代码），确保 analyst-agent 可直接复制修改使用
- 效应量统一用 Cohen's d / r = Z/√N / η² / Cramer's V 四种，覆盖从两组比较到多组分类的所有检验场景
- 引用文献收录 Cohen (1988)、Field (2013)、Lakens (2013) 等经典和方法学标准

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- 组间对比方法决策树已固化，planner-agent 和 analyst-agent 可直接引用
- 所有 13 个决策分支（D-08 ~ D-13）有明确的自动分支规则
- R 代码参考块可执行，覆盖主检验 + 效应量计算
- 下一计划（04-02）可执行：reference-agent method_search 未知方法搜索模式 + 分析工作流集成

---

*Phase: 04-方法增强*
*Completed: 2026-05-07*
