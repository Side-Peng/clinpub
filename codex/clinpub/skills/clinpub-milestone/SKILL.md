---
name: clinpub-milestone
description: "Phase milestone management. Review completed phase deliverables, verify success criteria, record decisions, and gate progression to next phase. Generates MILESTONE.md and updates ROADMAP.md."
---

# ClinPub Milestone

Phase gate review. Verify that the completed phase meets all success criteria, record key decisions and outputs, and obtain user sign-off before progressing to the next phase.

This is the VERIFY step of the DISCUSS → PLAN → EXECUTE → VERIFY lifecycle.

## Execution Context

- Workflow: `pipeline/workflows/milestone.md`
- References: `pipeline/references/checkpoints.md`
- Templates: `pipeline/templates/milestone.md`

## Process

Execute the milestone workflow from `pipeline/workflows/milestone.md` end-to-end.

Triggers:
- **Auto**: Called at the end of each phase workflow (init-project, data-prep, analysis, writing, review)
- **Manual**: User can invoke `clinpub:milestone <N>` at any time to check phase status

## Success Criteria

- MILESTONE.md generated in `.clinpub/phases/NN-phase-name/`
- All success criteria verified (or documented exceptions)
- ROADMAP.md updated with phase status
- STATE.md updated to next phase
- User has signed off (or deferred with documented reason)
