---
name: milestone
description: "Phase auto-verification. Review completed phase deliverables, verify success criteria, record decisions, and auto-advance to next phase. Generates MILESTONE.md and updates ROADMAP.md."
argument-hint: "<phase-number>"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

<objective>
Automated phase verification. Check all success criteria, record key decisions and outputs, and auto-advance to the next phase.

This is the VERIFY step of the DISCUSS → PLAN → EXECUTE → VERIFY lifecycle.
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/milestone.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/checkpoints.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/templates/milestone.md"`
</execution_context>

<process>
Execute the milestone workflow from pipeline/workflows/milestone.md end-to-end.

Triggers:
- **Auto**: Called at the end of each phase workflow (init-project, data-prep, analysis, writing, review)
- **Manual**: User can invoke clinpub:milestone <N> at any time to check phase status
</process>

<success_criteria>
- MILESTONE.md generated in .clinpub/phases/NN-phase-name/
- All success criteria verified (or documented exceptions)
- ROADMAP.md updated with phase completion status
- STATE.md auto-advanced to next phase
- No blocking user confirmation required
</success_criteria>
