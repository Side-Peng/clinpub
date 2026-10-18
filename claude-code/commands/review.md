---
name: review
description: "投稿后：处理期刊的真实审稿意见。录入用户提供的审稿意见 → 起草逐条回复信与改进方向 → 用户确认 → 交 improving 执行修稿。按轮次循环。不模拟审稿人。触发：收到审稿意见、返修、回复审稿人、rebuttal。"
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

Prerequisite: 已投稿的手稿存在（`05_Manuscript/manuscript.md` 且 `05_Manuscript/sections/` 可用），**并且**用户提供了真实的审稿意见（粘贴或文件路径）。未提供审稿意见则停止，并说明本命令处理的是**投稿后**的真实反馈；若只想自审改进，用 `/clinpub:improving`。
</process>

<success_criteria>
- Real reviewer comments collected from the user (never simulated) and normalized to 05_Manuscript/reviewer_comments.md
- Point-by-point response letter drafted with improvement directions
- User confirmed the response strategy and revision scope
- Actual revisions executed via the improving workflow (single source of revision logic)
- Revised manuscript + response letter in 05_Manuscript/final/
- Supports multiple revision rounds until the user is satisfied
</success_criteria>
