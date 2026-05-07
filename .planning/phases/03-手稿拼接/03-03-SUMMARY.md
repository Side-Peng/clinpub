---
phase: 03-手稿拼接
plan: 03
subsystem: pipeline
tags: concatenation, manuscript, references, vancouver, placeholder
requires:
  - phase: 03-手稿拼接
    plan: 01
    provides: sequential section writing workflow
  - phase: 03-手稿拼接
    plan: 02
    provides: reference library spec, placeholder patterns, citation conventions
provides:
  - Concatenation protocol specification (7-step merge logic)
  - Updated writing workflow with concatenate_manuscript step
affects: 03-手稿拼接 (subsequent concatenation execution), 04-模拟同行评审 (verifier consumes manuscript + MANIFEST)

tech-stack:
  added: []
  patterns:
    - "Concatenation-first approach: sections written independently with placeholders, then merged mechanically"
    - "Citation renumbering: scan all [id] refs → collect unique → renumber sequentially"
    - "Placeholder replacement: IMRAD-order global numbering for tables/figures"

key-files:
  created:
    - pipeline/references/concatenation-protocol.md
  modified:
    - pipeline/workflows/writing.md

key-decisions:
  - "Concatenation is mechanical merge (no rewriting) — WRITE-02 principle enforced throughout protocol"
  - "Table/Figure global numbering follows IMRAD scan order, independently incremented"
  - "Citation dedup is natural: same reference in multiple sections reuses same new number"
  - "Placeholder replacement covers 4 types: Table, Figure (incl. Supplementary), Method, Section cross-ref"
  - "YAML frontmatter auto-generated with title, target_journal, word_count, reference_count"

patterns-established:
  - "7-step merge protocol: merge → placeholder replace → citation renumber → frontmatter → output → manifest → library update"
  - "Verification checklist ensures no dangling placeholders, sequential numbering, word count > 5000"

requirements-completed: [WRITE-02]
duration: 3min
completed: 2026-05-07
---

# Phase 03 Plan 03: 终稿拼接协议 Summary

**7-step manuscript concatenation protocol (concatenation-protocol.md) + updated writing workflow (concatenate_manuscript replaces placeholder_concatenation)**

## Performance

- **Duration:** 3 min
- **Started:** 2026-05-07T19:05:47Z
- **Completed:** 2026-05-07T19:08:43Z
- **Tasks:** 2 / 2
- **Files modified:** 2

## Accomplishments

- Created `pipeline/references/concatenation-protocol.md` — complete 7-step specification for merging independently-written IMRAD sections into manuscript.md
- Updated `pipeline/workflows/writing.md` — replaced abstract `placeholder_concatenation` step with concrete `concatenate_manuscript` step referencing the protocol
- Added `concatenation_output` step with standardized output format
- Extended `success_criteria` with concatenation-specific checks (manuscript.md, sections/, no dangling placeholders, word_count > 5000, MANIFEST.yaml)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create concatenation-protocol.md** — `7b5a643` (feat)
2. **Task 2: Update writing.md workflow** — `5fd1bdb` (feat)

**Plan metadata:** _(orchestrator-owned)_

## Files Created/Modified

- `pipeline/references/concatenation-protocol.md` — Created. 290 lines. 7-step concatenation protocol: section merge, placeholder replacement (Table/Figure/Method/Section), citation renumbering with dedup, YAML frontmatter generation, combined output, MANIFEST.yaml update, reference library update
- `pipeline/workflows/writing.md` — Modified (+84 / -3 lines). `placeholder_concatenation` replaced with `concatenate_manuscript` (7 sub-steps), new `concatenation_output` step, updated `success_criteria`

## Decisions Made

- **WRITE-02 enforcement**: Protocol explicitly states "拼接而非重写" at multiple points — mechanical merge preserves original section content
- **Citation renumbering algorithm**: Scan all `[id]` refs → collect unique IDs by appearance order → reassign sequential numbers → handle compound groups (`[1-3]`, `[1,4,7]`)
- **Table/Figure numbering**: IMRAD-order global scan, Tables and Figures independently incremented (D-12)
- **Protocol completeness**: 7 comprehensive steps covering end-to-end pipeline from input validation to manifest output

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added reference-library.md link to protocol**
- **Found during:** Task 1 (Create concatenation-protocol.md)
- **Issue:** The plan's `key_links` and `must_haves` require concatenation-protocol.md to reference `reference-library.md` (the citation schema spec), but the written content didn't mention it by filename
- **Fix:** Added a `> 前置规范：参见 pipeline/references/reference-library.md` line in the doc intro
- **Files modified:** `pipeline/references/concatenation-protocol.md`
- **Verification:** `Select-String -Pattern "reference-library.md"` now returns 1 match
- **Committed in:** `7b5a643` (part of Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 missing critical)
**Impact on plan:** Minor — the reference is a documentation link requirement, not a functional gap. Fixed within the Task 1 commit.

## Issues Encountered

None.

## User Setup Required

None — no external service configuration required.

## Self-Check

- [x] `pipeline/references/concatenation-protocol.md` exists on disk
- [x] `pipeline/workflows/writing.md` exists on disk
- [x] Commit `7b5a643` exists (feat: create concatenation-protocol.md)
- [x] Commit `5fd1bdb` exists (feat: update writing.md)
- [x] `03-03-SUMMARY.md` exists on disk
- [x] No stub patterns found — all files are specification/documentation, not implementation
- [x] No new network endpoints, auth paths, or schema changes introduced — threat surface unchanged

**Status: PASSED**

## Next Phase Readiness

- Concatenation protocol is ready for execution. When Plan 03-01/03-02 complete and sections/ are populated, the protocol specifies exactly how to merge.
- Next step: Phase 4 (模拟同行评审) planning or Plan 03-04 (concatenation reference implementation).
