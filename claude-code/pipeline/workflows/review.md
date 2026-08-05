---
name: review
description: "Post-submission peer-review response workflow. Intake the reviewers' real comments provided by the user, draft a point-by-point response letter and improvement directions, confirm with the user, then delegate the actual revision to the improving workflow. Loops per revision round until the user is satisfied."
---

<purpose>
Handle the post-submission phase: after the manuscript has been submitted and the journal returns reviewer comments, this workflow ingests the reviewers' real comments (provided by the user), drafts a point-by-point response letter plus concrete improvement directions, gets user confirmation, and then delegates the actual manuscript + analysis revision to the `improving` workflow. It does NOT simulate reviewers — real reviewer comments are required input.
</purpose>

<required_reading>
@./pipeline/references/journal_standards.md
@./pipeline/references/checkpoints.md
@./pipeline/workflows/improving.md
@./agents/writer-agent.md
</required_reading>

<process>

<step name="validate_prerequisites" priority="first">
Verify a submitted manuscript exists to revise:

```bash
PROJECT_DIR=$(pwd)
MANUSCRIPT="$PROJECT_DIR/05_Manuscript/manuscript.md"
```

Checks:
1. `05_Manuscript/manuscript.md` exists (the submitted draft) — if not, error: "No manuscript found. This command is for handling reviewer comments after submission. Run /clinpub:writing first."
2. `project_config.yml` exists (journal name/tier, language) — if not, warn and continue.
</step>

<step name="collect_reviewer_comments" priority="first">
Reviewer comments are REQUIRED input — do not fabricate or simulate them.

Prompt the user to provide the journal's reviewer comments in one of two ways:
1. Paste the full reviewer/editor comments directly into the conversation, or
2. Provide a file path (e.g., a saved decision letter under `05_Manuscript/`).

If the user provides neither, stop and explain: this command handles real post-submission reviewer feedback; to self-improve a draft without reviewers, use `/clinpub:improving`.

Optionally capture the editor's decision (major revision / minor revision / reject & resubmit) to calibrate tone and scope.
</step>

<step name="parse_comments" priority="high">
Normalize the raw comments into a structured list and save to `05_Manuscript/reviewer_comments.md`:

For each comment record:
- Reviewer number and comment number (e.g., Reviewer 2, Comment 3)
- Verbatim comment text (quoted)
- Category: Major / Minor
- Required action type: text edit / additional analysis / new literature / clarification / rebuttal (disagree with justification)
- Affected manuscript location(s) if identifiable

Present a concise summary table (reviewer x comment count, Major/Minor split) to the user.
</step>

<step name="draft_response_and_directions" priority="high">
For every comment, draft two linked artifacts:

1. **Point-by-point response letter** (`05_Manuscript/final/response_letter.md`):
```markdown
## Reviewer 1, Comment 1
> [Reviewer's comment, verbatim]

**Response**: [How the concern is addressed — or a respectful rebuttal with rationale]
**Changes**: [What will change in the manuscript, and where (section, line/page)]

## Reviewer 1, Comment 2
...
```
Each response must: thank the reviewer, state what will change and why, and — if not changing — give a clear justification.

2. **Improvement directions**: a concrete mapping from each comment to the revision actions `improving` will execute (text edits, analysis re-runs, figure changes, new citations). This becomes the confirmed scope handed to `improving`.

Present both to the user.
</step>

<step name="checkpoint_confirm" priority="high">
Get explicit user confirmation before revising:

1. Show the response letter draft + improvement directions
2. User edits/approves the response strategy (may adjust rebuttals, defer items, add requests)
3. Agree on the revision scope for this round

If user declines → stop (response letter draft is kept for manual use).
If user confirms → proceed to execute.
</step>

<step name="execute_revisions" priority="high">
Delegate the actual manuscript + analysis revision to the improving workflow, scoped to the confirmed reviewer-driven directions:

Execute `@./pipeline/workflows/improving.md` with the confirmed improvement directions as the pre-agreed plan:
- Skip improving's open-ended `self_review` (scope is already defined by reviewer comments); enter at its `execute_revisions` with the confirmed items.
- improving handles: analysis re-runs (modify-agent), figure/table adjustments, literature additions (reference-agent), text revision (writer-agent), numeric cascade, and integrity verification.

This keeps a single implementation of the revision logic (no duplication).
</step>

<step name="finalize" priority="high">
Assemble the revision package and loop if needed:

1. Write the revised manuscript to `05_Manuscript/final/manuscript.md` (keep the pre-revision version for comparison).
2. Finalize `05_Manuscript/final/response_letter.md` with the actual change locations filled in from the improving pass.
3. Update `Reference/references.bib` if new citations were added.
4. Present to the user:
   - If the user requests more changes → loop back to `parse_comments` / `draft_response_and_directions` for another revision round (e.g., a second reviewer round).
   - If the user is satisfied → done.

Final deliverables:
- `05_Manuscript/reviewer_comments.md` — normalized reviewer comments
- `05_Manuscript/final/manuscript.md` — revised manuscript
- `05_Manuscript/final/response_letter.md` — point-by-point response to reviewers

<output name="done_prompt" format="user_facing">
────────────────────────────────
审稿意见处理完成（本轮）

已生成：
- 修订稿：05_Manuscript/final/manuscript.md
- 回复信：05_Manuscript/final/response_letter.md

请确认：输入 "approved" 结束本轮，或提供下一轮审稿意见继续。
────────────────────────────────
</output>
</step>

</process>

<success_criteria>
- Manuscript prerequisite validated
- Real reviewer comments collected from the user (never simulated) and normalized to `05_Manuscript/reviewer_comments.md`
- Point-by-point response letter drafted with improvement directions
- User confirmed the response strategy and revision scope
- Actual revisions executed via the improving workflow (single source of revision logic)
- Revised manuscript + response letter in `05_Manuscript/final/`
- New citations (if any) added to references.bib
- Supports multiple revision rounds until the user is satisfied
</success_criteria>
