---
name: review
description: "Phase 4 orchestration: Simulated peer review and iterative manuscript revision. Generate review, confirm items with user, revise, produce response letter. Loop until user satisfaction."
---

<purpose>
Simulate rigorous peer review at target journal level, then iteratively revise the manuscript. Each cycle: generate review → user confirms items → revise manuscript → produce response letter → loop until user is satisfied.
</purpose>

<required_reading>
@./pipeline/references/journal_standards.md
@./pipeline/references/checkpoints.md
@./agents/writer-agent.md
</required_reading>

<process>

<step name="discuss_review_scope" priority="first">
Discuss review standards with user:

1. **Review rigor level** (default: target journal level — Alzheimer's & Dementia / Molecular Psychiatry)
2. **Focus areas**: any specific concerns the user wants reviewers to examine
3. **Supplementary search**: any new literature to search based on review direction
</step>

<step name="generate_review" priority="high">
Generate simulated peer review as `05_Manuscript/review_v1.md`:

**Major comments** (prioritize):
- Statistical methods appropriateness and completeness
- Sample size and statistical power
- Confounding control adequacy
- Result interpretation and overclaiming
- Study design limitations

**Minor comments**:
- Language and grammar issues
- Citation completeness and relevance
- Figure/table formatting and clarity
- Reporting standard compliance (STROBE/CONSORT)

Each comment includes:
- Location (section, line)
- Issue description
- Suggested revision
- Severity
</step>

<step name="confirm_revision_items" priority="high">
Present review to user:

1. Show all review comments with categorization
2. User confirms which items to address (may defer some)
3. User may add additional revision requests
4. Agree on revision scope before starting
</step>

<step name="revise_manuscript" priority="high">
Revise manuscript addressing confirmed items:

1. Address each comment systematically
2. Track changes per comment
3. Update citations if new references added
4. Keep original + revised versions for comparison

**For major comments**: may need supplementary analysis (re-run from Phase 2) or additional literature search (Reference Agent).
**For minor comments**: direct edits to manuscript.
</step>

<step name="generate_response_letter" priority="high">
Write point-by-point response letter:

```markdown
## Reviewer 1, Comment 1
> [Reviewer's comment]

**Response**: [Explanation of changes made]
**Changes**: [Location of changes in manuscript, line/page]

## Reviewer 1, Comment 2
...
```

Each response must:
- Thank the reviewer for the comment
- Explain what was changed and why
- If not changed, provide rationale
- Reference specific locations in revised manuscript
</step>

<step name="verify_and_loop" priority="medium">
After revision:

1. Verify all confirmed items are addressed
2. Check response letter completeness
3. Present to user for review
4. If user requests more changes → loop back to step 2
5. If user satisfied → proceed to milestone

Final deliverables:
- `05_Manuscript/review_v1.md` — review comments
- `05_Manuscript/final/manuscript.md` — final accepted manuscript
- `05_Manuscript/final/response_letter.md` — response to reviewers
- Updated `Reference/references.bib` with any new citations
</step>

<step name="milestone" priority="high">
Execute the milestone workflow to formally close Phase 4 (project completion):

```bash
# The milestone workflow will:
# 1. Verify success criteria for Phase 4
# 2. Collect review decisions (comments addressed, response letter)
# 3. Generate .clinpub/phases/04-review/MILESTONE.md
# 4. Update ROADMAP.md: Phase 4 → ✅ Complete
# 5. Update STATE.md: current_phase → complete
# 6. Present project completion summary to user
```

See @./pipeline/workflows/milestone.md for full protocol.
</step>

</process>

<success_criteria>
- Review generated with Major and Minor categories
- User confirmed revision items
- All confirmed items addressed in manuscript
- Point-by-point response letter complete
- New citations added to references.bib
- Final manuscript in 05_Manuscript/final/
- User satisfied with revision
</success_criteria>
