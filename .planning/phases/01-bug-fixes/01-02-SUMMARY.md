---
phase: 01-bug-fixes
plan: 02
subsystem: pipeline
tags: data-prep, re-entry, refresh, project-config, profile, spec

requires:
  - phase: 00-init-project
    provides: "project_config.yml template and project initialization structure"
provides:
  - "Re-entry detection for /clinpub-data-prep when project is already initialized"
  - "Full refresh flow: profile → spec → config sync"
affects: [pipeline/workflows/data-prep.md, all agents using data-prep entry point]

tech-stack:
  added: []
  patterns:
    - "Command-level re-entry detection (no hook involvement per D-07)"
    - "Field-level merge strategy for project_config.yml updates"

key-files:
  created: []
  modified:
    - commands/clinpub/data-prep.md
    - pipeline/workflows/data-prep.md

key-decisions:
  - "D-05: Re-entry triggered by command entry, detecting project_config.yml"
  - "D-06: Full refresh: profile → spec → config, then enter discussion"
  - "D-07: No PreToolUse hook — all detection at command level"

requirements-completed: [BUG-02]

duration: 5min
completed: 2026-05-05
---

# Phase 1 Plan 02: Bug Fixes — 数据联动更新

**data-prep 命令入口添加重新进入检测 + 工作流头部添加 reinit_data_prep 全链路刷新步骤**

## Performance

- **Duration:** 5 min
- **Completed:** 2026-05-05
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Task 1: data-prep 命令入口 `commands/clinpub/data-prep.md`
  - 添加重现进入检测逻辑：检查 `project_config.yml` 存在性 + 关键字段验证
  - 双向路由：已初始化→刷新流程，未初始化→全新流程
- Task 2: data-prep 工作流 `pipeline/workflows/data-prep.md`
  - 添加 `reinit_data_prep` 步骤（profile 重跑 → spec 重生成 → config 同步 → 用户通知）
  - 步骤位于 `discuss_cleaning_strategy` 之前

## Task Commits

1. **Task 1: data-prep 命令入口重新进入检测** — `9cd7a0d` (fix)
2. **Task 2: reinit_data_prep 工作流步骤** — `1767432` (fix)

**Plan metadata:** (pending)

## Files Modified
- `commands/clinpub/data-prep.md` — 新增重新进入检测逻辑
- `pipeline/workflows/data-prep.md` — 新增 `reinit_data_prep` 刷新步骤

## Decisions Made
- 严格遵循 D-05/D-06/D-07：全在命令层面检测，不涉及 hook
- 字段级 merge 策略：仅更新 profile 相关变量字段，保留用户手动配置

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None

## Next Phase Readiness

Phase 1 (Bug Fixes) 两计划全部完成。准备执行 Phase 2（断点续做）。

---
*Phase: 01-bug-fixes*
*Completed: 2026-05-05*
