---
name: improving
description: "Continuously improve a manuscript draft. Self-review the draft, produce a concrete revision plan, confirm with user, then directly revise the manuscript (full text + analysis code re-run + numeric cascade). No response letter, no simulated reviewers. Standalone tool — invocable anytime a manuscript exists; repeatable. Triggers: improve/polish/refine the paper, self-review before submission."
argument-hint: "[focus area or brief description, leave empty for full self-review]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---
<objective>
Standalone manuscript improvement tool. Help the researcher continuously improve the paper during or after writing:
1. **Self-review**: assess the current draft (statistics, sample size, confounding, interpretation, language, citations, figures, reporting standards) and classify findings Major/Minor.
2. **Revision plan**: turn findings into a concrete, itemized plan (text edits, analysis re-runs, figure changes, new citations).
3. **Direct revision**: after user confirmation, execute changes across BOTH the manuscript text AND the underlying analysis code (re-run + numeric cascade).

Does NOT write a response letter and does NOT simulate reviewers. For post-submission reviewer comments, use `/clinpub:review`.
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/improving.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/modify.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/journal_standards.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/agents/writer-agent.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/agents/modify-agent.md"`
</execution_context>

<process>
Execute the improving workflow from pipeline/workflows/improving.md end-to-end.

Prerequisite: a manuscript draft exists (`05_Manuscript/manuscript.md` or `05_Manuscript/sections/`). If not, tell the user to run `/clinpub:writing` first.
</process>

<success_criteria>
- Self-review findings (Major/Minor) recorded in 05_Manuscript/improvement_plan.md
- Itemized revision plan confirmed by user before any change
- Text revised and, where needed, analysis re-run with numbers cascaded into the manuscript
- New citations (if any) added with DOIs; reference library de-duplicated
- Revised manuscript passes integrity checks (IMRAD, DOIs, figures exist, no placeholders, Humanizer)
- No response letter / no simulated reviewers; tool remains repeatable
</success_criteria>
