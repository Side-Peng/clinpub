---
phase: 06-图表文档优化
plan: 01
subsystem: visualization
tags: [ggplot2, theme_pub, survminer, ggcorrplot, r-patterns, sci-journal]

# Dependency graph
requires:
  - phase: 05-Phase前调研流程
    provides: research workflow and context gathering
provides:
  - 优化后的 theme_pub() 主题（base_size=10, base_family=sans, legend.right）
  - KM 生存曲线美化模板（§2.9）
  - 相关性矩阵热图模板（§2.10）
  - 字体跨平台说明和 Nature 系列尺寸参考
affects: [06-02, analysis, visualization]

# Tech tracking
tech-stack:
  added: [extrafont]
  patterns: [theme_pub with base_family, ggsurvplot integration, ggcorrplot integration]

key-files:
  created: []
  modified:
    - pipeline/references/r_patterns.md

key-decisions:
  - "theme_pub() base_size 从 14 改为 10，适配 SCI 期刊 6-8pt 出版要求"
  - "legend.position 默认改为 right，更通用；单图需隐藏时用 theme(legend.position='none') 覆盖"
  - "KM 曲线使用 survminer::ggsurvplot() 而非手动 ggplot，因其内置风险表和 p 值标注"
  - "相关性矩阵默认使用 Spearman（偏态数据更常见），仅正态时用 Pearson"

patterns-established:
  - "theme_pub(base_size=10, base_family='sans') 作为所有 clinpub 图表的统一主题"
  - "Nature 双色 #0072B5/#BC3C29 作为 2 组配色默认方案"

requirements-completed: [CHART-01]

# Metrics
duration: 2min
completed: 2026-05-28
---

# Phase 6 Plan 01: R 可视化规范升级 Summary

**theme_pub() 主题优化（base_size=10/sans字体/legend.right）+ KM 生存曲线和相关性热图两个新图表模板 + 字体跨平台指南**

## Performance

- **Duration:** 2 min
- **Started:** 2026-05-28T02:40:57Z
- **Completed:** 2026-05-28T02:43:54Z
- **Tasks:** 4
- **Files modified:** 1

## Accomplishments
- theme_pub() 全面升级：base_size 14→10、base_family="sans"、legend.right、新增 axis.line/legend.title/legend.text
- 新增 §2.9 KM 生存曲线美化模板（survminer::ggsurvplot + theme_pub + Nature 双色 + 风险表）
- 新增 §2.10 相关性矩阵热图模板（ggcorrplot + theme_pub + 蓝白红三色 + Spearman/Pearson 选择）
- §1.3 补充字体族跨平台说明（Windows Arial 自动映射、Linux/macOS extrafont 方案）和 Nature 系列尺寸参考

## Task Commits

Each task was committed atomically:

1. **Task 1: 优化 theme_pub() 主题** - `18843a7` (feat)
2. **Task 2: 新增 KM 生存曲线美化模板** - `0fa79f9` (feat)
3. **Task 3: 新增相关性矩阵热图模板** - `88ea628` (feat)
4. **Task 4: 更新字体和尺寸规范** - `c0f3d0b` (feat)

## Files Created/Modified
- `pipeline/references/r_patterns.md` — theme_pub() 主题优化、新增 §2.9 KM 曲线、§2.10 相关性热图、§1.3 字体/尺寸规范更新

## Decisions Made
- base_size 14→10：适配 SCI 期刊 6-8pt 出版要求，最终排版约 7-8pt
- legend.position "none"→"right"：多数图表需要图例，单图隐藏时显式覆盖
- KM 曲线使用 survminer 而非手动 ggplot：内置风险表、p 值标注、log-rank 方法
- 相关性默认 Spearman：临床数据偏态更常见，Pearson 仅限正态分布

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- r_patterns.md 已升级完成，Phase 2 Analyst Agent 生成的图表将自动应用新主题和模板
- 06-02 计划（WAVE 文档中文本地化）可继续执行

---
*Phase: 06-图表文档优化*
*Completed: 2026-05-28*

## Self-Check: PASSED

- ✅ pipeline/references/r_patterns.md exists
- ✅ 06-01-SUMMARY.md exists
- ✅ Commit 18843a7 (Task 1) found
- ✅ Commit 0fa79f9 (Task 2) found
- ✅ Commit 88ea628 (Task 3) found
- ✅ Commit c0f3d0b (Task 4) found
- ✅ Commit dc6e4e2 (SUMMARY) found
