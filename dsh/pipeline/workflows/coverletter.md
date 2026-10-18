---
name: coverletter
description: "Cover letter generation tool. Based on the target journal defined at initialization, gather the journal's official submission requirements (author guidelines / submission page) via web search, then draft a tailored cover letter. Falls back to journal-tier best practices if the web is unavailable. Output: 05_Manuscript/cover_letter.md."
---

<purpose>
Produce a submission-ready cover letter tailored to the target journal. Read the target journal from `project_config.yml` (set at initialization), gather the journal's official submission requirements from its website, and draft a cover letter that matches the journal's cover-letter expectations and aims & scope. Invocable anytime a manuscript draft exists.
</purpose>

<required_reading>
@./pipeline/references/journal_standards.md
@./pipeline/references/checkpoints.md
</required_reading>

<process>

<step name="validate_prerequisites" priority="first">
Verify inputs:

```bash
PROJECT_DIR=$(pwd)
MANUSCRIPT="$PROJECT_DIR/05_Manuscript/manuscript.md"
```

Checks:
1. `05_Manuscript/manuscript.md` exists — if not, error: "No manuscript found. Run /clinpub:writing first."
2. Read target journal from `project_config.yml`: `journal.name` (preferred) or `project.target_journal`.
   - If the journal is empty or "待定" → ask the user for the target journal (name + tier) now, and write it back to `project_config.yml` so downstream steps and future tools stay consistent.
</step>

<step name="gather_journal_info" priority="high">
Collect the journal's official submission requirements. Prefer live sources; degrade gracefully.

1. **Locate official guidelines** (WebSearch): search for the journal's "author guidelines" / "guide for authors" / "submission guidelines" / "cover letter requirements" on the official publisher domain.
2. **Extract requirements** (WebFetch on the best-matching official page):
   - Cover-letter specific requirements (required statements, addressee/editor, length, format)
   - Aims & scope (to tailor the fit/significance argument)
   - Submission checklist items relevant to the cover letter (originality, no concurrent submission, ethics/IRB, data sharing, suggested/opposed reviewers, conflict of interest, authorship, corresponding author)
3. **Record findings** briefly (source URLs) for transparency.

**Fallback (web unavailable or journal not found)**: inform the user, then use `journal_standards.md` for the journal tier plus general clinical cover-letter best practices. Clearly note in the output that requirements were not verified against the live journal site.
</step>

<step name="draft_cover_letter" priority="high">
Draft a tailored cover letter and write it to `05_Manuscript/cover_letter.md`. Pull manuscript title, key findings, and study type from `05_Manuscript/manuscript.md` + `project_config.yml`.

Structure (adapt to the journal's specific requirements gathered above):
1. Date, corresponding author details, editor/journal addressee
2. Manuscript title and article type; statement of submission to this journal
3. Significance & novelty — why the study matters and how it fits the journal's aims & scope
4. Concise summary of key findings (2-4 sentences, no overclaiming)
5. Compliance statements required by the journal: originality / not under concurrent consideration / all authors approved / ethics approval (IRB) & informed consent / data availability / conflict of interest
6. Suggested (and, if requested, opposed) reviewers — only if the journal invites them
7. Corresponding author contact block and closing

Write in the language configured in `language.manuscript` (default zh-CN) unless the journal requires English; keep it concise (typically < 1 page).
</step>

<step name="verify" priority="medium">
Check the draft:
1. Every journal-required cover-letter element is present (or explicitly marked as not applicable)
2. Title and key findings match the manuscript
3. No overclaiming beyond the manuscript's evidence
4. Placeholders for user-specific fields (editor name, dates, author affiliations) are clearly marked for the user to fill

Present the cover letter to the user and iterate on request.

<output name="done_prompt" format="user_facing">
────────────────────────────────
Cover Letter 已生成

文件：05_Manuscript/cover_letter.md
目标期刊：{journal}
来源：{已核对期刊官网 / 未联网，使用通用标准（请自行核对）}

请检查署名、编辑姓名、日期等占位项，并确认或提出修改意见。
────────────────────────────────
</output>
</step>

</process>

<success_criteria>
- Manuscript prerequisite validated; target journal resolved (asked if missing)
- Journal submission requirements gathered from the official site (or graceful fallback noted)
- Cover letter written to `05_Manuscript/cover_letter.md`, tailored to the journal's aims & scope
- All journal-required cover-letter elements and compliance statements included
- Key findings consistent with the manuscript; no overclaiming
- User-specific fields clearly marked as placeholders for completion
</success_criteria>
