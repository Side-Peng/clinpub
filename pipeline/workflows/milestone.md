---
name: milestone
description: "Phase gate review workflow. Verify success criteria, record decisions and outputs, generate MILESTONE.md, update ROADMAP.md and STATE.md, obtain user sign-off."
---

<purpose>
Formal phase-gate review between clinpub phases. Ensures each phase is properly completed before the next begins, with all decisions documented and user sign-off obtained.
</purpose>

<required_reading>
@./pipeline/references/checkpoints.md
@./pipeline/templates/milestone.md
</required_reading>

<process>

<step name="load_phase_context" priority="first">
Load the current phase and project context:

```bash
PHASE="$ARGUMENTS"  # e.g., "0", "1", "2"
PROJECT_DIR=$(pwd)
PLANNING_DIR="$PROJECT_DIR/.planning"
PHASE_DIR="$PLANNING_DIR/phases/$(printf '%02d' $PHASE)-*"
```

Read:
- `$PLANNING_DIR/ROADMAP.md` — confirm phase name, goal, success criteria
- `$PLANNING_DIR/STATE.md` — current state, decisions log
- `$PLANNING_DIR/PROJECT.md` — project vision, requirements

Determine phase name from ROADMAP:
| Phase | Name |
|-------|------|
| 0 | init |
| 1 | data-prep |
| 2 | analysis |
| 3 | writing |
| 4 | review |
</step>

<step name="verify_success_criteria" priority="high">
Check all success criteria for the completed phase:

**Phase 0 (init):**
- [ ] Project directory structure created (.planning/, 01_RawData/, etc.)
- [ ] project_config.yml generated and reflects user decisions
- [ ] Study type confirmed by user
- [ ] Analysis methods selected by user
- [ ] Decision log written to 00-CONTEXT.md

**Phase 1 (data-prep):**
- [ ] cleaned.csv exists at 02_PreprocessedData/data/
- [ ] Data quality report generated (HTML)
- [ ] Missing values handled per agreed strategy
- [ ] Outliers documented
- [ ] Derived variables created and encoded
- [ ] Cleaning code independently reproducible

**Phase 2 (analysis):**
- [ ] Each confirmed method has figure + table + 方法说明 in 04_Outputs/
- [ ] All figures ≥300 DPI, English labels, publication-grade theme
- [ ] Statistical reports include effect size + 95%CI + exact p-value
- [ ] Code reads from cleaned.csv, independently runnable
- [ ] R version and key package versions documented

**Phase 3 (writing):**
- [ ] IMRAD structure complete (all 5 sections)
- [ ] All citations have DOIs
- [ ] All figures/tables referenced in text
- [ ] STROBE/CONSORT checklist covered
- [ ] No AI-template patterns (Humanizer check passed)

**Phase 4 (review):**
- [ ] Review comments generated (Major/Minor)
- [ ] All confirmed items addressed in manuscript
- [ ] Response letter complete (point-by-point)
- [ ] Final manuscript in 05_Manuscript/final/

Use `checkpoint:verify` to present results to user.
</step>

<step name="collect_decisions" priority="high">
Gather all key decisions made during the phase:

Source from:
- Phase discussion logs (`.planning/phases/NN-phase-name/00-CONTEXT.md`)
- STATE.md decision log
- Shell history of user confirmations during execution

Format as a decision table:
| Decision | Choice | Rationale | Source |
|----------|--------|-----------|--------|
</step>

<step name="generate_milestone" priority="high">
Write MILESTONE.md to `.planning/phases/NN-phase-name/MILESTONE.md`:

Use the milestone template from `@./pipeline/templates/milestone.md` with filled fields:

- `phase_number`, `phase_name`
- `date`: today's date
- `status`: ✅ Complete or ⚠️ Partial (based on verification results)
- `deliverables`: list of produced files/outputs
- `verification_items`: checklist with [x] or [ ] for each criterion
- `decisions`: table of key decisions
- `outputs`: table of output files with paths
- `blockers`: any unresolved issues
- `next_phase_number`, `next_phase_name`, `next_phase_goal`, `next_steps`
</step>

<step name="update_roadmap" priority="high">
Update ROADMAP.md:

1. Set current phase status to `✅ Complete`
2. Set next phase status to `🔄 In Progress`
3. Update any completion dates or notes

Format in ROADMAP.md:
```markdown
| Phase | Name | Status | Success Criteria | Notes |
|-------|------|--------|-----------------|-------|
| 0 | init | ✅ Complete | ... | Milestone: link |
| 1 | data-prep | 🔄 In Progress | ... | |
```
</step>

<step name="user_signoff" priority="high">
Present milestone summary to user for sign-off using `checkpoint:milestone`:

```xml
<milestone gate="blocking">
  <phase>{{phase_number}} — {{phase_name}}</phase>
  <status>{{status}}</status>
  <verification>{{summary_of_checks}}</verification>
  <key_outputs>{{outputs_summary}}</key_outputs>
  <next_phase>Phase {{next}} — {{next_name}}</next_phase>
  <signoff>输入 approved 进入下一 Phase，或描述问题</signoff>
</milestone>
```

If user approves:
1. Update STATE.md: set `current_phase` to next phase, clear phase-specific state
2. Write sign-off confirmation to MILESTONE.md
3. Proceed to next phase (or inform user they can start with `clinpub:xxx`)

If user requests changes:
1. Note required changes in MILESTONE.md under blockers
2. Set status to ⚠️ Partial
3. Help user address issues
4. Re-run milestone verification
</step>

</process>

<success_criteria>
- MILESTONE.md generated with all verification results
- ROADMAP.md updated with phase completion status
- STATE.md set to next phase
- User has signed off or blockers documented
- Decision log complete and auditable
</success_criteria>
