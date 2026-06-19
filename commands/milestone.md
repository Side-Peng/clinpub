---
name: milestone
description: "Phase milestone management. Review completed phase deliverables, verify success criteria, record decisions, and gate progression to next phase. Generates MILESTONE.md and updates ROADMAP.md."
argument-hint: "<phase-number>"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---
<objective>
Phase gate review. Verify that the completed phase meets all success criteria, record key decisions and outputs, and obtain user sign-off before progressing to the next phase.

This is the VERIFY step of the DISCUSS → PLAN → EXECUTE → VERIFY lifecycle.
</objective>

<execution_context>
@./pipeline/workflows/milestone.md
@./pipeline/references/checkpoints.md
@./pipeline/templates/milestone.md
</execution_context>

<process>
Execute the milestone workflow from @./pipeline/workflows/milestone.md end-to-end.

Triggers:
- **Auto**: Called at the end of each phase workflow (init-project, data-prep, analysis, writing, review)
- **Manual**: User can invoke `clinpub:milestone <N>` at any time to check phase status
</process>

<success_criteria>
- MILESTONE.md generated in `.clinpub/phases/NN-phase-name/`
- All success criteria verified (or documented exceptions)
- ROADMAP.md updated with phase status
- STATE.md updated to next phase
- User has signed off (or deferred with documented reason)
</success_criteria>
