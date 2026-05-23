---
phase: 03-手稿拼接
reviewed: 2026-05-11T19:00:00Z
depth: standard
files_reviewed: 4
files_reviewed_list:
  - agents/reference-agent.md
  - pipeline/workflows/writing.md
  - pipeline/templates/project_config.yml
  - pipeline/references/citation-strategy.md
findings:
  critical: 1
  warning: 3
  info: 2
  total: 6
status: issues_found
---

# Phase 3: Code Review Report

**Reviewed:** 2026-05-11T19:00:00Z
**Depth:** standard
**Files Reviewed:** 4
**Status:** issues_found

## Summary

Reviewed 4 files defining the Phase 3 (手稿拼接) manuscript writing workflow: the reference agent specification, the writing workflow orchestration, the project config template, and the citation strategy reference document. Cross-referenced against 2 actual Python scripts (pubmed_search.py, tavily_search.py) and 2 supporting documents (concatenation-protocol.md, reference-library.md).

**Key finding:** The reference agent documentation specifies CLI flags (`--max_year`, `--min_if`) for `pubmed_search.py` that do not exist in the actual script — these commands will fail at runtime. Three other consistency/quality issues found across configuration thresholds, section counting, and API key handling.

---

## Critical Issues

### CR-01: `pubmed_search.py` CLI flags do not match actual script arguments

**File:** `agents/reference-agent.md:54`
**Issue:** The documented command uses two flags that do not exist in `pubmed_search.py`:

```bash
# Documented (will FAIL):
python scripts/pubmed_search.py "{keywords}" --max 10 --max_year 5 --min_if 3.0
```

**Problem 1 — `--max_year`**: The actual script (scripts/pubmed_search.py, line 481) defines `--years`, not `--max_year`. An unrecognized argument error will be raised at runtime.

**Problem 2 — `--min_if`**: The actual script has no IF (impact factor) filtering capability at all. No `--min_if`, `--min-if`, or any IF-related argument exists anywhere in the script. The entire IF filtering strategy described in `citation-strategy.md` (section 4) and `reference-agent.md` (lines 42-43, 52-57) has no backend implementation.

**Impact:** 
- The reference agent cannot execute the documented search command — it will crash.
- IF-based filtering (a core part of the citation strategy) has no implementation in any script or tool.
- This affects all steps that depend on IF filtering: `literature_search`, `method_search`, `phase_research` (Track A), and the entire `citation-strategy.md` section 4.

**Fix:**
1. In `reference-agent.md:54`, change `--max_year 5` to `--years 5`:
   ```bash
   python scripts/pubmed_search.py "{keywords}" --max 10 --years 5
   ```
2. Either implement IF filtering in `pubmed_search.py` (add `--min-if` parameter + journal IF lookup) OR document in `citation-strategy.md` and `reference-agent.md` that IF filtering is a manual/user-side process, not automated. If removing IF automation, update:
   - `agents/reference-agent.md` lines 42-43, 52-57 (IF parameter table and example command)
   - `pipeline/references/citation-strategy.md` section 4 (IF preference discussion)
   - `pipeline/templates/project_config.yml` lines 94-96 (`citation_strategy.if_preference` section)

---

## Warnings

### WR-01: Missing data thresholds have ambiguous boundary at 20%

**File:** `pipeline/templates/project_config.yml:73-75`
**Issue:** Three missing-data thresholds where `missing_threshold_mid` and `missing_threshold_high` share the same value (0.20) but describe different ranges:

```yaml
missing_threshold_low: 0.05       # Comment: < 5% -> delete/impute
missing_threshold_mid: 0.20       # Comment: 5-20% -> impute
missing_threshold_high: 0.20      # Comment: > 20% -> discuss retention
```

At exactly 20% missing rate, the behavior is undefined. If a consumer uses `<= mid` for mid-range and `> high` for high-range, then 20% falls into mid-range (impute). But if a consumer uses `>= high` for high-range, then 20% falls into high-range (discuss retention). Both scenarios are equally plausible given the YAML structure. Additionally, `missing_threshold_high` being identical to `missing_threshold_mid` means the "high" value is not a distinct threshold but a redundant copy.

**Fix:** Either:
- Change `missing_threshold_high` to `0.20` with a clear documentation comment that comparison is strict-greater-than (`>`), and add explicit comparison logic documentation, OR
- Change the value to `0.21` (removing ambiguity) if that better reflects the intended ">20%" boundary, OR
- Restructure to a single threshold value with named bands:
  ```yaml
  missing_data:
    low_max: 0.05
    mid_max: 0.20
    # rates > mid_max are "high"
  ```

### WR-02: Inconsistent section count ("5 sections" vs "4 sections")

**File:** `pipeline/workflows/writing.md:183` and `pipeline/references/concatenation-protocol.md:262`
**Issue:** The writing workflow verification step claims "IMRAD structure complete (all 5 sections present)" (line 183), while:
- The same file lists exactly 4 section files at lines 133-137 (01-introduction through 04-discussion)
- Line 192-193 correctly states "4 个段文件"
- The concatenation protocol (line 262) says "5 sections: I/M/R/D + References"

IMRAD stands for Introduction, Methods, Results, Discussion — exactly 4 sections. References are back matter, not a manuscript section. If an automated verification script checks for 5 section files, it will fail. If a human reads the checklist, the "5" will confuse against the 4 actual section files.

**Fix:** Standardize on 4 sections (IMRAD) across all files. The References section is generated during concatenation and should be verified separately (word count, DOI presence), not counted as a manuscript section. Update:
- `pipeline/workflows/writing.md:183`: change "all 5 sections present" to "all 4 IMRAD sections present"
- `pipeline/references/concatenation-protocol.md:262`: change to "IMRAD structure complete (4 sections: I/M/R/D)"

### WR-03: Missing TAVILY_API_KEY does not halt Tavily-dependent steps

**File:** `agents/reference-agent.md:17-33`
**Issue:** The `check_api_keys` step prints a warning when `TAVILY_API_KEY` is not set but continues execution. Several downstream steps depend on Tavily being available:

- `method_search` (line 88): `Tavily 优先` — defaults to Tavily, falls back to PubMed only if Tavily has <2 DOI results. But if Tavily is unavailable, it skips rather than falling through.
- `phase_research` Track B (line 206-208): Requires Tavily for technology searches. No PubMed fallback for Track B.
- `critical_rules` section (line 282): "方法搜索优先 Tavily 再 PubMed（D-04），不能跳过 Tavily 直接搜 PubMed" — This explicitly forbids skipping Tavily, even when the API key is missing.

The combination of "do not skip Tavily" and "do not block on missing key" creates a contradictory state where the agent halts (cannot proceed without Tavily) but no hard error was raised.

**Fix:** Make `TAVILY_API_KEY` handling explicit for each search mode:
- For `method_search`: if key is missing, use PubMed-only fallback (update the rule in line 282)
- For `phase_research` Track B: if key is missing, report the limitation to the user and offer PubMed alternatives
- Document fallback behavior clearly in each step rather than only warning at the top

---

## Info

### IN-01: Inconsistent file reference format in writing.md

**File:** `pipeline/workflows/writing.md:105`
**Issue:** The workflow file consistently uses `@./path/to/file.md` format for cross-references (lines 11-16, 27, 56, 201, 259, 303), but line 105 references `agents/reference-agent.md` without the `@./` prefix. This is a minor inconsistency that could confuse automated link-checking or tooling.

**Fix:**
```markdown
- 搜索策略（参考 `@./agents/reference-agent.md`）:
```

### IN-02: `pubmed_search.py` has no DOI validation despite being required by every agent

**File:** `scripts/pubmed_search.py` (implicitly referenced by all reviewed files)
**Issue:** Every reviewed document mandates that "every citation MUST have a DOI" (reference-agent.md line 273, writing.md line 185, citation-strategy.md line 53, concatenation-protocol.md line 261). However, `pubmed_search.py` does not filter or validate DOIs — it extracts DOI when available (line 371-373) but does not reject articles without DOIs. Articles without DOIs silently pass through to the reference library, only to be flagged later as `pending_doi`. 

**Suggestion:** Add a `--require-doi` flag to `pubmed_search.py` that excludes results without DOIs when set, reducing manual cleanup work. This aligns with the "every citation must have a DOI" hard requirement stated everywhere in the documentation.

---

*Reviewed: 2026-05-11T19:00:00Z*
*Reviewer: Claude (gsd-code-reviewer)*
*Depth: standard*
