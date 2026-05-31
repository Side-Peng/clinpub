---
phase: 06-图表文档优化
plan: 02
subsystem: documentation
tags: [method-readme, agent-contracts, gates, analysis-methods, verification, manifest, localization]

# Dependency graph
requires: []
provides:
  - method-readme.md 中文方法说明模板
  - 管线文档中所有 README 引用统一改为「方法说明」
  - agent-contracts.md 输出规范与方法说明模板对齐
affects: [phase-2-analysis, phase-3-writing]

# Tech tracking
tech-stack:
  added: []
  patterns: [方法说明模板替代 README.md]

key-files:
  created:
    - pipeline/templates/method-readme.md
  modified:
    - pipeline/references/agent-contracts.md
    - pipeline/references/gates.md
    - pipeline/references/analysis_methods.md
    - pipeline/references/verification-patterns.md
    - pipeline/references/mandatory-initial-read.md
    - pipeline/references/manifest-format.md

key-decisions:
  - "方法说明.md 作为 WAVE 方法目录的中文文档文件名，替代 README.md"
  - "输出结果 section 等价于原 Results subsection，保持兼容性"
  - "模板使用中文撰写，统计术语和 R 包名保持英文"

patterns-established:
  - "方法说明模板: 7 个标准 section（目的、方法、输入数据、输出结果、参数设置、注意事项、软件版本）"

requirements-completed: [DOC-01, DOC-02]

# Metrics
duration: 5min
completed: 2026-05-28
---

# Phase 6 Plan 02: WAVE 文档中文本地化 Summary

**统一「方法说明」模板并更新 6 个管线文档中所有 README 引用为中文「方法说明」**

## Performance

- **Duration:** 5 min
- **Started:** 2026-05-28T10:41:34Z
- **Completed:** 2026-05-28T10:47:04Z
- **Tasks:** 7
- **Files modified:** 7

## Accomplishments

- 创建 `pipeline/templates/method-readme.md` 中文方法说明模板（7 个标准 section）
- 更新 agent-contracts.md：Analyst Agent 输出规范从 README 改为方法说明，引用新模板
- 更新 gates.md：Phase 2 质量门三件套从 README 改为方法说明
- 更新 analysis_methods.md、verification-patterns.md、mandatory-initial-read.md、manifest-format.md 中所有 README 引用

## Task Commits

Each task was committed atomically:

1. **Task 1: 设计「方法说明」模板** - `2fb41d9` (docs)
2. **Task 2: 更新 agent-contracts.md** - `763f9f4` (docs)
3. **Task 3: 更新 gates.md** - `c67bfb9` (docs)
4. **Task 4: 更新 analysis_methods.md** - `59d03dd` (docs)
5. **Task 5: 更新 verification-patterns.md** - `2cee24b` (docs)
6. **Task 6: 更新 mandatory-initial-read.md** - `93deea4` (docs)
7. **Task 7: 更新 manifest-format.md** - `05a1377` (docs)

**Plan metadata:** (pending)

## Files Created/Modified

- `pipeline/templates/method-readme.md` - 中文方法说明模板，7 个标准 section
- `pipeline/references/agent-contracts.md` - Analyst Agent 输出规范：README→方法说明，添加模板引用
- `pipeline/references/gates.md` - Phase 2 质量门：README→方法说明
- `pipeline/references/analysis_methods.md` - 通用要求：README.md→方法说明.md，添加模板引用
- `pipeline/references/verification-patterns.md` - 验证模式：3 处 README→方法说明
- `pipeline/references/mandatory-initial-read.md` - Phase 2 必读列表：README→方法说明
- `pipeline/references/manifest-format.md` - MANIFEST 说明：README→方法说明

## Decisions Made

- 方法说明.md 作为 WAVE 方法目录的中文文档文件名，替代 README.md
- 输出结果 section 等价于原 Results subsection，保持与 MANIFEST.yaml 和 agent-contracts.md 的兼容性
- 模板使用中文撰写，统计术语和 R 包名保持英文

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- WAVE 文档中文本地化完成，Phase 2 Analyst Agent 执行时将使用新模板生成方法说明
- 与 06-01 plan 的 r_patterns.md 改造互补，共同构成 Phase 6 的图表+文档优化交付

## Self-Check: PASSED

- `pipeline/templates/method-readme.md` — FOUND
- `.clinpub/phases/06-图表文档优化/06-02-SUMMARY.md` — FOUND
- 8 commits with `06-02` tag found in git log

---
*Phase: 06-图表文档优化*
*Completed: 2026-05-28*
