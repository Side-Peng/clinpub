---
name: modify
description: "Ad-hoc modification orchestration: Load analysis context → define modifications with user → execute changes → verify outputs → update PLAN.md. Supports figure style adjustments and statistical method changes on completed Phase 2 outputs."
---

<purpose>
Enable targeted modifications to analysis outputs after Phase 2 completion. Orchestrate the modify-agent through a structured define→execute→verify→record cycle. Can be invoked from any phase (Phase 2, 3, or 4) when the user needs to adjust analysis results.
</purpose>

<required_reading>
@./pipeline/references/analysis_methods.md
@./pipeline/references/r_patterns.md
@./agents/modify-agent.md
</required_reading>

<process>

<step name="validate_prerequisites" priority="first">
Before proceeding, verify the analysis phase has been completed:

```bash
PROJECT_DIR=$(pwd)
PLAN=$(ls "$PROJECT_DIR/.clinpub/phases/02-analysis/"*-PLAN.md 2>/dev/null | head -1)
DATA="$PROJECT_DIR/02_PreprocessedData/data/cleaned.csv"
OUTPUTS="$PROJECT_DIR/04_Outputs/"
```

Checks:
1. `*-PLAN.md` exists under `.clinpub/phases/02-analysis/` — if not, error: "No analysis plan found. Run /clinpub-analysis first."
2. `cleaned.csv` exists — if not, error: "No cleaned data found. Run /clinpub-data-prep first."
3. `04_Outputs/` has at least one method directory — if not, error: "No analysis outputs found. Run /clinpub-analysis first."

If all checks pass, proceed.
</step>

<step name="define_modifications" priority="high">
Delegate to modify-agent steps `build_method_inventory` and `define_modification`:

1. modify-agent reads `*-PLAN.md` → builds method inventory
2. modify-agent presents inventory to user
3. User selects methods and defines modifications
4. modify-agent outputs structured modification summary
5. **Checkpoint**: User confirms modification summary

If user declines → stop, no changes made.
If user confirms → proceed to execute.
</step>

<step name="execute_modifications" priority="high">
Delegate to modify-agent step `execute_modifications`:

For each modification in the confirmed summary:

1. **Backup**: Before modifying, record current commit hash for rollback reference
2. **Modify**: Execute the change (R script modification + re-run)
3. **Brief**: Report success/failure per modification

```bash
# Record current state before modifications
PRE_MODIFY_HASH=$(git rev-parse --short HEAD)
echo "Pre-modification baseline: $PRE_MODIFY_HASH"
```

Execution order: style changes first (low risk), then variable changes, then method changes, then new methods. This ordering minimizes cascading failures.

If a modification requires a package not installed, report and skip. Do not auto-install packages.
</step>

<step name="verify_outputs" priority="medium">
Delegate to modify-agent step `verify_modifications`:

For each successfully modified method:

1. Check figure file exists and is non-zero bytes
2. Verify figure DPI ≥ 300 (FIGURE_DPI from r_patterns.md)
3. Check English labels on all figures
4. Verify table file exists and contains updated statistics
5. Verify README (方法说明) has been updated
6. Confirm statistical reports include effect size + 95%CI + exact p-value

If verification fails for any modification:
- Report the specific failure
- Offer to re-run that modification or skip it
</step>

<step name="cascade_manuscript_update" priority="medium">
If `05_Manuscript/` exists, delegate to modify-agent step `cascade_to_manuscript`:

1. Patch affected numerical values in Results section (effect sizes, p-values, CI bounds)
2. Update Methods section if statistical method changed
3. Report which manuscript sections were updated

If `05_Manuscript/` does not exist, skip silently.
</step>

<step name="update_plan_history" priority="high">
Delegate to modify-agent step `update_plan`:

1. Append modification record to `*-PLAN.md`
2. Update STATE.md "Last activity" line

```bash
DATE=$(date +%Y-%m-%d)
```

Modification record format (appended to PLAN.md):
```yaml
modifications:
  - id: "mod-{YYYYMMDD}-{NNN}"
    timestamp: "{YYYY-MM-DD}"
    description: "{summary}"
    items:
      - method_id: "{id}"
        type: "{style|variable|method|new}"
        change: "{description}"
    status: "completed|partial"
    failed: [{list of failed method_ids}]
```

Output completion summary:
```
─────────────────────────────────────────
 Modify Complete
─────────────────────────────────────────
Succeeded: {N} modification(s)
Failed: {M} modification(s)
PLAN.md updated with modification history
Manuscript cascade: {K} section(s) updated / Skipped (no manuscript found)
─────────────────────────────────────────
```
</step>

</process>

<success_criteria>
- Prerequisites validated (analysis plan + data + outputs exist)
- Modification scope clearly defined and user-confirmed
- Each modification executed with success/failure reporting
- Modified outputs meet publication standards
- Modification history appended to PLAN.md
- Affected manuscript sections patched if manuscript exists (numerical values and method descriptions)
- STATE.md last activity updated
</success_criteria>
