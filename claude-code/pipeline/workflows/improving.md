---
name: improving
description: "Standalone manuscript improvement tool: self-review the draft, produce a concrete revision plan, confirm with user, then directly revise the manuscript (full text + analysis code re-run + numeric cascade). No response letter, no simulated reviewers. Invocable anytime a manuscript draft exists; repeatable."
---

<purpose>
Help the researcher continuously improve the manuscript during or after writing. Perform a structured self-review of the current draft, propose a concrete itemized revision plan, and — after user confirmation — directly execute the revisions across BOTH the manuscript text AND the underlying analysis (re-run R/Python where needed, cascade updated numbers). This is a repeatable improvement tool (like `modify`), not a phase; it does not simulate reviewers and does not write a response letter.
</purpose>

<required_reading>
@./pipeline/references/journal_standards.md
@./pipeline/references/checkpoints.md
@./pipeline/references/analysis_methods.md
@./pipeline/references/r_patterns.md
@./agents/writer-agent.md
@./agents/modify-agent.md
</required_reading>

<process>

<step name="validate_prerequisites" priority="first">
Before proceeding, verify a manuscript draft exists to improve:

```bash
PROJECT_DIR=$(pwd)
MANUSCRIPT="$PROJECT_DIR/05_Manuscript/manuscript.md"
SECTIONS="$PROJECT_DIR/05_Manuscript/sections/"
OUTPUTS="$PROJECT_DIR/04_Outputs/"
```

Checks:
1. `05_Manuscript/manuscript.md` OR at least one file under `05_Manuscript/sections/` exists — if neither, error: "No manuscript found. Run /clinpub:writing first."
2. `project_config.yml` exists (for journal tier, language, variables) — if not, warn and continue with defaults.

If checks pass, proceed. `improving` can be invoked repeatedly.
</step>

<step name="self_review" priority="high">
Perform a structured self-review of the current draft. This is an internal quality assessment — NOT a simulated reviewer persona and NOT a response-letter exercise. Frame findings as concrete improvement opportunities.

Review rigor defaults to the target journal level — read `journal.name` + `journal.tier` from `project_config.yml`; if unconfigured, apply Q2 standards (see `journal_standards.md`).

Assess these dimensions and classify each finding as Major or Minor:

**Major (substance):**
- Statistical methods appropriateness and completeness (missing key analyses, wrong test choice)
- Sample size / statistical power adequacy
- Confounding control adequacy
- Result interpretation and overclaiming (conclusions exceeding evidence)
- Study design limitations not addressed

**Minor (presentation):**
- Language, grammar, and flow issues
- Citation completeness, relevance, and currency
- Figure/table formatting, clarity, and referencing
- Reporting-standard compliance (STROBE/CONSORT/PRISMA)
- Cross-reference and placeholder consistency

Write the assessment to `05_Manuscript/improvement_plan.md`. Each finding includes:
- Location (section, and line/paragraph where possible)
- Issue description
- Suggested improvement
- Severity (Major / Minor)
- Requires analysis re-run? (yes/no) — flags whether Phase 2 code must change
</step>

<step name="propose_plan" priority="high">
Turn the assessment into a concrete, itemized revision plan (in `05_Manuscript/improvement_plan.md`), grouping items by execution type:

1. **Text-only edits**: which sections/paragraphs to rewrite or tighten (delegate to writer-agent)
2. **Analysis re-runs**: which `03_AnalysisMethods/{method_id}/` need code changes / new methods / re-render (delegate to modify-agent) and the downstream numbers they affect
3. **Figure/table adjustments**: style or content changes to `04_Outputs/*`
4. **Literature additions**: gaps requiring new citations (delegate to reference-agent)

Present the plan to the user for confirmation.
</step>

<step name="checkpoint_confirm" priority="high">
Present the itemized plan and get explicit user confirmation on scope:

1. Show all improvement items with severity and execution type
2. User confirms which items to execute now (may defer some)
3. User may add additional improvement requests
4. Agree on the revision scope before making any change

If user declines → stop, no changes made.
If user confirms → proceed to execute.
</step>

<step name="execute_revisions" priority="high">
Execute the confirmed items. Order minimizes cascading failures: analysis re-runs first (they change numbers), then figure/table adjustments, then literature, then text.

1. **Analysis re-runs** (if any item requires it): delegate to modify-agent (`execute_modifications` + `verify_modifications`).
   - Record current commit hash before modifying for rollback reference.
   - New method IDs must follow `{NN}_{MethodName}`; create both `03_AnalysisMethods/{id}/` and `04_Outputs/{id}/`.
   - Do not auto-install missing packages — report and skip.
2. **Figure/table adjustments**: re-render via modify-agent style path (≥300 DPI, English labels).
3. **Literature additions**: delegate to reference-agent; update `Reference/reference_library.json` + `references.bib` (dedupe, DOIs required).
4. **Text revision**: delegate to writer-agent for each affected section.
   - Edit `05_Manuscript/sections/*` and re-concatenate / patch `05_Manuscript/manuscript.md`.
   - **Numeric cascade**: patch affected effect sizes, p-values, CI bounds in Results; update Methods if a statistical method changed.
   - Apply the Humanizer checklist inline (no AI-template patterns).

Report success/failure per item.
</step>

<step name="verify" priority="medium">
After revisions, verify integrity:

**Manuscript:**
1. IMRAD structure complete (Introduction, Methods, Results, Discussion)
2. All citations have DOIs; reference library de-duplicated
3. All referenced figures/tables exist in `04_Outputs/`
4. No residual placeholders (`{{Table:N}}`, `{{Figure:N}}`, etc.)
5. Word count within target journal limits; Humanizer check passes

**Analysis (for any re-run):**
6. Figure files exist, non-zero, ≥300 DPI, English labels
7. Statistical reports include effect size + 95%CI + exact p-value
8. `方法说明.md` updated for changed methods

If verification fails for an item, report the specific failure and offer to re-run or skip it.
</step>

<step name="record" priority="high">
Record the improvement round (no milestone / no phase close — this tool is repeatable):

1. Update `05_Manuscript/improvement_plan.md`: mark each item `done` / `deferred` / `failed`, append a timestamped round header.
2. Update `.clinpub/STATE.md` "Last activity" line.

```bash
DATE=$(date +%Y-%m-%d)
```

Output completion summary:
```
─────────────────────────────────────────
 Improving Complete (round {N})
─────────────────────────────────────────
Executed: {N} item(s)   Deferred: {M}   Failed: {K}
Analysis re-runs: {A}    Sections revised: {S}
Manuscript: 05_Manuscript/manuscript.md updated
Plan/log: 05_Manuscript/improvement_plan.md
─────────────────────────────────────────
下一步：
- 继续改进 → 再次运行 /clinpub:improving
- 准备投稿信 → /clinpub:coverletter
- 投稿后收到审稿意见 → /clinpub:review
```

If the user wants more changes, loop back to `self_review` (or `propose_plan` for a focused pass).
</step>

</process>

<success_criteria>
- Prerequisites validated (a manuscript draft exists)
- Self-review produced with Major/Minor findings in `05_Manuscript/improvement_plan.md`
- Concrete itemized revision plan confirmed by user before any change
- Confirmed items executed: text revised, analysis re-run where needed, numbers cascaded into manuscript
- New citations (if any) added with DOIs; reference library de-duplicated
- Revised manuscript passes integrity checks (IMRAD, DOIs, figures exist, no placeholders, Humanizer)
- No response letter and no simulated reviewers produced
- Improvement round logged; tool remains repeatable (no phase/milestone closure)
</success_criteria>
