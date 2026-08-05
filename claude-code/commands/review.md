---
name: review
description: "Post-submission: handle the journal's real reviewer comments. Intake the reviewers' comments provided by the user, draft a point-by-point response letter and improvement directions, confirm with the user, then delegate the actual revision to /clinpub:improving. Loops per revision round. Triggers: reviewer comments, revise-and-resubmit, response to reviewers, rebuttal."
argument-hint: "[paste reviewer comments or a file path, optional]"
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
Post-submission peer-review response. After the manuscript has been submitted and the journal returns reviewer comments:
1. **Intake** the reviewers' REAL comments provided by the user (this command does not simulate reviewers).
2. **Draft** a point-by-point response letter plus concrete improvement directions.
3. **Confirm** the response strategy with the user.
4. **Revise** by delegating the actual manuscript + analysis changes to the improving workflow.

For self-improving a draft without reviewers, use `/clinpub:improving`.
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/review.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/improving.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/journal_standards.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/agents/writer-agent.md"`
</execution_context>

<process>
Execute the review workflow from pipeline/workflows/review.md end-to-end.

Prerequisite: a submitted manuscript exists (`05_Manuscript/manuscript.md`) AND the user provides the journal's reviewer comments (pasted or as a file path). If no comments are provided, stop and explain that this command handles real post-submission feedback.
</process>

<success_criteria>
- Real reviewer comments collected from the user (never simulated) and normalized to 05_Manuscript/reviewer_comments.md
- Point-by-point response letter drafted with improvement directions
- User confirmed the response strategy and revision scope
- Actual revisions executed via the improving workflow (single source of revision logic)
- Revised manuscript + response letter in 05_Manuscript/final/
- Supports multiple revision rounds until the user is satisfied
</success_criteria>
