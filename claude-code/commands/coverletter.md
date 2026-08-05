---
name: coverletter
description: "Generate a submission cover letter tailored to the target journal. Reads the target journal defined at initialization, gathers the journal's official submission requirements (author guidelines) via web search, then drafts a tailored cover letter. Falls back to journal-tier best practices if the web is unavailable. Standalone tool — invocable anytime a manuscript exists. Triggers: write cover letter, prepare submission letter."
argument-hint: ""
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - AskUserQuestion
---
<objective>
Produce a submission-ready cover letter tailored to the target journal:
1. Resolve the target journal from `project_config.yml` (`journal.name` / `project.target_journal`), set at initialization; ask the user if it is missing.
2. Gather the journal's official submission requirements and aims & scope from its website (WebSearch + WebFetch), with graceful fallback to journal-tier best practices when the web is unavailable.
3. Draft a tailored cover letter (significance/fit, key findings, and the journal's required compliance statements) to `05_Manuscript/cover_letter.md`.
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/coverletter.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/journal_standards.md"`
</execution_context>

<process>
Execute the coverletter workflow from pipeline/workflows/coverletter.md end-to-end.

Prerequisite: a manuscript exists (`05_Manuscript/manuscript.md`). If not, tell the user to run `/clinpub:writing` first.
</process>

<success_criteria>
- Target journal resolved (asked if missing)
- Journal submission requirements gathered from the official site, or graceful fallback clearly noted
- Cover letter written to 05_Manuscript/cover_letter.md, tailored to the journal's aims & scope
- All journal-required cover-letter elements and compliance statements included
- Key findings consistent with the manuscript; no overclaiming
- User-specific fields (editor name, dates, affiliations) clearly marked as placeholders
</success_criteria>
