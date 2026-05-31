---
phase: 04-方法增强
plan: 02
subsystem: agents
tags: [reference-agent, method-search, tavily, pubmed, analysis-workflow, methods-reference]
requires:
  - phase: 04-方法增强
    provides: 04-CONTEXT.md 决策定义 (D-01~D-07)
provides:
  - reference-agent 的 method_search 模式（触发条件、搜索策略、自适应呈现、双轨制）
  - analysis.md 讨论环节的方法搜索触发提示
  - analysis_methods.md 的未知方法注记
affects: [05-前调研流程, 02-analysis]
tech-stack:
  added: []
  patterns:
    - "unknown statistical method auto-search with adaptive depth levels"
    - "dual-track output: summary replaces spec, tutorial goes to attachment"
    - "search priority: Tavily first → PubMed supplement"
key-files:
  created: []
  modified:
    - agents/reference-agent.md
    - pipeline/workflows/analysis.md
    - pipeline/references/analysis_methods.md
key-decisions:
  - "method_search 步在 literature_search 之后插入，不修改已有步骤"
  - "搜索策略严格 Tavily 优先→PubMed 补充（D-04），不可跳步"
  - "双轨制输出：摘要轨替换 spec 方法描述，附件轨输出详细教程（D-06）"
patterns-established:
  - "自适应方法搜索：摘要级（默认）→ 深入层（用户追问触发）"
  - "参考 comparison-methods.md 标准化组间对比决策"
requirements-completed: [METH-01]
duration: 2 min
completed: 2026-05-07
---

# Phase 04: 方法增强 Summary — Plan 02

**reference-agent 扩展 method_search 模式 + 集成到分析工作流和方法参考库**

## Performance

- **Duration:** 2 min
- **Started:** 2026-05-07T21:55:25+08:00
- **Completed:** 2026-05-07T21:58:19+08:00
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- reference-agent 新增完整的 method_search 模式：触发条件、搜索策略、自适应呈现格式、双轨制输出
- analysis.md 的 discuss_and_confirm 步新增方法搜索触发提示，包含 Tavily→PubMed 搜索路径和 comparison-methods.md 引用
- analysis_methods.md §二 Step 2 方法选择表下方增加"未知方法可动态搜索"注记
- 所有变更遵循已有的 YAML frontmatter + XML 标签 + Markdown 混合格式

## Task Commits

Each task was committed atomically:

1. **Task 1: 扩展 reference-agent 增加 method_search 模式** — `7415280` (feat)
2. **Task 2: 集成到分析工作流 + 更新方法选择表** — `6155bd7` (feat)

## Files Created/Modified

- `agents/reference-agent.md` — 新增 method_search 步（line 57-129）、critical_rules 方法搜索规则（line 176-180）、success_criteria 方法搜索标准（line 190-194）
- `pipeline/workflows/analysis.md` — 在 discuss_and_confirm 步中新增方法搜索触发提示和 comparison-methods.md 引用（line 130-142）
- `pipeline/references/analysis_methods.md` — §二 Step 2 方法选择表下方新增"未知方法"注记（line 55-56）

## Decisions Made

- method_search 步放在 literature_search 之后、full_text_retrieval 之前，保持 logical flow
- 搜索策略严格遵循 D-04：Tavily 优先，PubMed 仅在 Tavily 学术引用不足（<2 篇 DOI）时补充
- 双轨制输出（D-06）：摘要轨直接替换 spec 方法描述，附件轨输出到 attachments/ 目录
- comparison-methods.md 引用仅出现在 analysis.md 讨论提示中，不修改 comparison-methods.md 本身

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## Next Phase Readiness

- METH-01（未知统计方法自动搜索）已完成
- 下一步可以开始 Phase 5（Phase 前调研流程）或继续 Phase 6（引用策略）的规划
- method_search 模式在 Phase 2 分析时即可发挥作用，不需要额外 Phase

---

## Self-Check: PASSED

- ✅ SUMMARY.md exists: `.clinpub/phases/04-方法增强/04-02-SUMMARY.md`
- ✅ All 3 modified files exist on disk
- ✅ Commits verified: `7415280`, `6155bd7`
- ✅ All acceptance criteria met for both tasks
- ✅ All 5 plan-level verification checks passed

---

*Phase: 04-方法增强*
*Completed: 2026-05-07*
