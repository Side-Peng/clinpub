---
phase: 03-手稿拼接
plan: 02
subsystem: writing
tags: [reference-library, vancouver, cross-reference, placeholder, citation-management]
requires:
  - phase: 03-手稿拼接
    provides: D-07 to D-12 decisions from phase context
provides:
  - Reference library JSON schema for shared citation management
  - Vancouver citation format specification (D-07, D-08)
  - Citation deduplication rules with citation_key primary key (D-09)
  - 6-type cross-reference placeholder convention (Table, Figure, Method, Section, SupplementaryTable, SupplementaryFigure)
  - Table/Figure global numbering strategy per IMRAD order (D-12)
  - Reference library read/write workflow for pre-section and merge stages
  - Citation quantity guide per IMRAD section (D-10)
affects: [03-手稿拼接 plan 03 (分段撰写), 03-手稿拼接 plan 04 (终稿拼接)]

tech-stack:
  added: []
  patterns:
    - "JSON-based shared reference library for cross-section citation deduplication"
    - "Structured placeholder naming convention for cross-references ({{Type:identifier}})"
    - "Vancouver [id] citation format with global sequential numbering"
    - "MANIFEST.yaml handoff contract including reference_library.json"

key-files:
  created:
    - pipeline/references/reference-library.md (213 lines, 5 sections)
  modified: []

key-decisions:
  - "citation_key (AuthorYear) as primary deduplication key with AuthorYear suffix strategy for collisions"
  - "sections_used array tracks which sections reference each citation for cross-section reuse tracking"
  - "6 placeholder types: Table, Figure, Method, Section, SupplementaryTable, SupplementaryFigure"
  - "Tables and Figures independently numbered, sequenced by IMRAD order (Methods → Results → Discussion → Intro)"
  - "Pre-section workflow: reference-agent searches → checks existing library → appends new entries"

patterns-established:
  - "citation_key-based deduplication: check before add, reuse existing id, append to sections_used"
  - "Placeholder naming: {{Type:identifier}} with regex patterns for automated replacement"
  - "Vancouver format: [id] in body, sequential listing in end References section"
  - "MANIFEST.yaml inclusion: reference_library.json registered as output with writer-agent handoff"

requirements-completed: [WRITE-01, WRITE-02]

duration: 10 min
completed: 2026-05-07
---

# Phase 3 Plan 2: 引用管理与交叉引用规范 Summary

**Shared Reference Library JSON schema with Vancouver citation format, 6-type cross-reference placeholder convention, deduplication rules, and Table/Figure global numbering strategy**

## Performance

- **Duration:** 10 min
- **Started:** 2026-05-07T18:57:27Z
- **Completed:** 2026-05-07T19:07:00Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments

- Defined complete JSON schema for `Reference/reference_library.json` with id, citation_key, sections_used, and 12 metadata fields
- Standardized Vancouver citation format for body references [1][2][1-3] and end References section (D-07, D-08)
- Implemented D-09 citation deduplication strategy: citation_key primary key, AuthorYear suffix disambiguation, sections_used tracking
- Created 6-type cross-reference placeholder system (Table, Figure, Method, Section, SupplementaryTable, SupplementaryFigure) with regex patterns
- Specified Table/Figure independent global numbering per IMRAD section order (D-12)
- Documented full read/write workflow for reference library: pre-section search → dedup append → writer-agent consumption → final merge renumbering
- Added citation quantity guidelines per section (D-10: Intro 10-15, Methods 3-5, Results 0-3, Discussion 15-25)
- Included MANIFEST.yaml update instructions for Reference Agent handoff

## Task Commits

Each task was committed atomically:

1. **Task 1: Shared Reference Library JSON Schema 定义** - `cb4db21` (feat)

**Plan metadata:** _(orchestrator-owned, not committed in sequential mode)_

## Files Created/Modified

- `pipeline/references/reference-library.md` — Comprehensive reference management specification (213 lines, 5 sections: JSON schema, Vancouver format, cross-reference placeholders, read/write workflow, citation quantity guide)

## Decisions Made

- **Deduplication key**: `citation_key` (AuthorYear) as primary key with `Author2024a`/`Author2024b` suffix for same-AuthorYear collisions; optional DOI secondary check
- **sections_used tracking**: Array field per reference records all sections that cite it, enabling both deduplication and cross-section reuse visibility
- **Placeholder naming**: Structured `{{Type:identifier}}` format (not `{{Table1}}` as initially proposed in CONTEXT.D-11) to support automated regex replacement — `{{Table:N}}`, `{{Figure:N}}`, `{{Method:name}}`, etc.
- **Table/Figure numbering**: Independent sequences, ordered by IMRAD section appearance (Methods first, then Results, etc.)
- **Pre-section workflow**: Reference agent searches → checks existing library → appends new entries with `added_by_section` → writes updated library before writer-agent uses it

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None

## User Setup Required

None - this is a specification document, no external service configuration required.

## Next Phase Readiness

- ✅ Reference library schema and cross-reference specification complete and committed
- ✅ All D-07 through D-12 decisions formalized into implementable rules
- ✅ Ready for Plan 03 (分段撰写) where writer-agent will use these conventions to draft IMRAD sections
- ✅ Ready for Plan 04 (终稿拼接) where placeholders are resolved and references renumbered

## Self-Check: PASSED

- ✅ `pipeline/references/reference-library.md` exists
- ✅ `03-02-SUMMARY.md` exists
- ✅ Commit `cb4db21` confirmed in git log
- ✅ No accidental deletions detected

---

*Phase: 03-手稿拼接*
*Completed: 2026-05-07*
