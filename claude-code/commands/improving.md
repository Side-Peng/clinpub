---
name: improving
description: "持续改进手稿。自审稿件 → 产出具体修改计划 → 用户确认 → 直接改章节文件（必要时重跑分析并级联数值）→ 按依赖把下游标为 stale → 重拼手稿。不写回复信、不模拟审稿人，可反复调用。触发：改进、润色、精修论文，投稿前自审。"
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

Prerequisite: 章节文件存在（`05_Manuscript/sections/*.md`）。若只有 `manuscript.md` 而无 sections，说明是 3.0 之前的手稿，需先迁移到 sections 结构。缺失时提示用户先运行 `/clinpub:writing`。
</process>

<success_criteria>
- Self-review findings (Major/Minor) recorded in 05_Manuscript/improvement_plan.md
- Itemized revision plan confirmed by user before any change
- Text revised and, where needed, analysis re-run with numbers cascaded into the manuscript
- New citations (if any) added with DOIs; reference library de-duplicated
- Revised manuscript passes integrity checks (IMRAD, DOIs, figures exist, no placeholders, Humanizer)
- No response letter / no simulated reviewers; tool remains repeatable
</success_criteria>
