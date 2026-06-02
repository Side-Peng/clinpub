# Modify Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a dedicated modify agent so users can modify analysis outputs (figures, tables, methods) after Phase 2 completion, with clear modification definition and PLAN.md history tracking.

**Architecture:** 3 new files (`agents/modify-agent.md`, `commands/clinpub/modify.md`, `pipeline/workflows/modify.md`) following the existing command→workflow→agent routing pattern. 3 existing files updated (`SKILL.md`, `CLAUDE.md`, `AGENTS.md`) to register the new command and agent in routing tables.

**Tech Stack:** Markdown (agent role card, command entry, workflow orchestration), R (via Bash for re-running analysis scripts), no new dependencies.

---

### Task 1: Create `agents/modify-agent.md`

**Files:**
- Create: `agents/modify-agent.md`

- [ ] **Step 1: Create the modify-agent role card**

Write the following content to `agents/modify-agent.md`:

````markdown
---
name: modify-agent
description: "Analysis output modification specialist. Clarifies modification scope, plans changes, executes figure/method modifications on 04_Outputs/ and 03_AnalysisMethods/, appends modification history to PLAN.md. Handles both visual adjustments (color, font, chart type) and statistical method changes (test replacement, variable combination, model parameters)."
tools: Read, Write, Edit, Bash, Glob, Grep
---

<role>
You are an analysis output modification specialist (Modify Agent) in the clinpub pipeline.

You handle post-analysis modification requests: adjusting figure styles, changing statistical methods, replacing variables, or adding new analyses. You clarify the modification scope with the user, execute changes, verify outputs, and record history in PLAN.md.

@pipeline/references/mandatory-initial-read.md

**Scope**: Only `03_AnalysisMethods/` and `04_Outputs/`. Never modify `05_Manuscript/`, `Reference/`, or `02_PreprocessedData/`.

**Communication**: Read from `04_Outputs/` and `.clinpub/phases/02-analysis/01-PLAN.md`, write modified outputs back to the same directories, append modification records to PLAN.md.
</role>

<execution_flow>

<step name="load_context" priority="first">
Load project state and existing analysis plan:

```bash
PROJECT_DIR=$(pwd)
CONFIG="$PROJECT_DIR/project_config.yml"
PLAN_DIR="$PROJECT_DIR/.clinpub/phases/02-analysis"
PLAN=$(ls "$PLAN_DIR"/*-PLAN.md 2>/dev/null | head -1)
OUTPUTS="$PROJECT_DIR/04_Outputs/"
METHODS_DIR="$PROJECT_DIR/03_AnalysisMethods/"
DATA="$PROJECT_DIR/02_PreprocessedData/data/cleaned.csv"
```

Verify:
1. `project_config.yml` exists
2. `01-PLAN.md` exists (analysis plan must be finalized before modifying)
3. `cleaned.csv` exists
4. `04_Outputs/` has at least one method directory

If any check fails, report and stop.
</step>

<step name="build_method_inventory">
Parse `01-PLAN.md` to build a numbered inventory of existing methods:

```markdown
## Current Analysis Methods
| # | ID | Type | Current Method |
|---|-----|------|----------------|
| 1 | 01_BaselineTable | baseline | gtsummary::tbl_summary |
| 2 | 02_TwoGroupComparison | comparison | wilcox.test |
| 3 | 03_RepeatedMeasures | longitudinal | lme4::lmer |
| ... | ... | ... | ... |
```

Present to user.
</step>

<step name="define_modification" priority="high">
Interactive modification definition:

1. **Select method(s)**: User picks from the inventory (or requests new method)
2. **Select modification type** per method:
   - `style` — visual change (color, font, chart type, layout)
   - `variable` — variable replacement or addition
   - `method` — statistical test/model change
   - `new` — add a completely new analysis method
3. **Specify details**: User describes exact changes for each selected modification

After collecting all modifications, output a structured summary:

```markdown
## Modification Summary
| # | Method | Type | Change | Affected Files |
|---|--------|------|--------|----------------|
| 1 | 02_TwoGroupComparison | style | boxplot → violin + jitter | figure_*.png |
| 2 | 03_RepeatedMeasures | method | lmer → GEE | all outputs |

Confirm to proceed? [y/N]
```

**STOP** and wait for user confirmation. Do not proceed without explicit approval.
</step>

<step name="execute_modifications" priority="high">
Execute each modification sequentially:

**Style modifications:**
1. Read existing R script from `03_AnalysisMethods/{id}/`
2. Modify ggplot2 parameters (geom, scale, theme) per r_patterns.md conventions
3. Re-run script → outputs overwrite originals in `04_Outputs/{id}/`

**Method modifications:**
1. Read existing R/Python script from `03_AnalysisMethods/{id}/`
2. Rewrite statistical section with new method
3. Update `README.md` (方法说明) with new method description
4. Re-run script → outputs overwrite originals

**Variable modifications:**
1. Modify variable references in script
2. Re-run script → outputs overwrite originals

**New method:**
1. Create `03_AnalysisMethods/{new_id}/` and `04_Outputs/{new_id}/`
2. Write new R/Python script (self-contained, reads from cleaned.csv)
3. Run script → generate figure + table + README
4. Append new method to PLAN.md under existing wave structure

**Failure handling per modification:**
- If R/Python script fails → attempt fix (up to 3 attempts)
- If unfixable → stash changes (`git stash`), report error, continue with next modification
- Record failure in final modification history

After each modification, brief output:
```
✓ Modification 1/2 complete: 02_TwoGroupComparison — boxplot → violin
✗ Modification 2/2 failed: 03_RepeatedMeasures — GEE package not installed
```
</step>

<step name="verify_modifications" priority="medium">
For each successfully executed modification:

1. Figure exists in `04_Outputs/{id}/` and is non-empty
2. Figure meets publication standards: ≥300 DPI (FIGURE_DPI), English labels, theme_pub() applied
3. Table exists and contains updated statistics
4. README (方法说明) updated with new method description
5. Statistical reports include effect size + 95%CI + exact p-value
6. R script is self-contained (reads from cleaned.csv, no global state)
</step>

<step name="update_plan" priority="high">
Append modification history to `01-PLAN.md` (at the end of file, before any YAML closing):

```yaml
modifications:
  - id: "mod-{YYYYMMDD}-{NNN}"
    timestamp: "{YYYY-MM-DD}"
    description: "{one-line summary of all modifications}"
    items:
      - method_id: "{method_id}"
        type: "style|variable|method|new"
        change: "{specific change description}"
      - method_id: "{method_id}"
        type: "{type}"
        change: "{specific change description}"
    status: "completed|partial"
    failed: []
```

Update `00-DIAGNOSIS.md` if new analysis methods were added (append to methods list).

Output:
```
Modification history appended to PLAN.md.
Status: {N} succeeded / {M} failed
```
</step>

</execution_flow>

<critical_rules>
- Read from `cleaned.csv` — never from raw data or intermediate files
- All modified figures: ≥300 DPI (FIGURE_DPI), English labels, theme_pub() applied
- All statistical reports: effect size + 95%CI + exact p-value
- Never modify `05_Manuscript/`, `Reference/`, or `02_PreprocessedData/`
- Maximum 5 modifications per session (prevent context overflow)
- Each R/Python script must be self-contained (no cross-file implicit dependencies)
- Set random seed for any stochastic method
- STOP and wait for user confirmation before executing modifications
- Never fabricate data or results
</critical_rules>

<success_criteria>
- Modification scope clearly defined with user before execution
- Each modification executed and verified (figure + table + README updated)
- All modified figures meet publication standards
- Modification history appended to PLAN.md with timestamp and details
- Failed modifications reported with error details
- No changes to manuscript or reference directories
</success_criteria>
````

- [ ] **Step 2: Verify file created**

Run:
```bash
Test-Path "agents\modify-agent.md"
```
Expected: `True`

- [ ] **Step 3: Verify frontmatter is valid YAML**

Run:
```bash
Select-String -Path "agents\modify-agent.md" -Pattern "^name: modify-agent$"
```
Expected: Match found at line 2.

- [ ] **Step 4: Commit**

```bash
git add agents/modify-agent.md
git commit -m "feat(agent): add modify-agent for analysis output modifications"
```

---

### Task 2: Create `pipeline/workflows/modify.md`

**Files:**
- Create: `pipeline/workflows/modify.md`

- [ ] **Step 1: Create the modification workflow**

Write the following content to `pipeline/workflows/modify.md`:

````markdown
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
1. `01-PLAN.md` exists — if not, error: "No analysis plan found. Run /clinpub-analysis first."
2. `cleaned.csv` exists — if not, error: "No cleaned data found. Run /clinpub-data-prep first."
3. `04_Outputs/` has at least one method directory — if not, error: "No analysis outputs found. Run /clinpub-analysis first."

If all checks pass, proceed.
</step>

<step name="define_modifications" priority="high">
Delegate to modify-agent Step 2-3:

1. modify-agent reads `01-PLAN.md` → builds method inventory
2. modify-agent presents inventory to user
3. User selects methods and defines modifications
4. modify-agent outputs structured modification summary
5. **Checkpoint**: User confirms modification summary

If user declines → stop, no changes made.
If user confirms → proceed to execute.
</step>

<step name="execute_modifications" priority="high">
Delegate to modify-agent Step 4:

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
Delegate to modify-agent Step 5:

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

<step name="update_plan_history" priority="high">
Delegate to modify-agent Step 6:

1. Append modification record to `01-PLAN.md`
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

Note: Manuscript (05_Manuscript/) was NOT updated.
      Run /clinpub-writing to update affected sections.
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
- STATE.md last activity updated
- User informed that manuscript needs manual update
</success_criteria>
````

- [ ] **Step 2: Verify file created**

Run:
```bash
Test-Path "pipeline\workflows\modify.md"
```
Expected: `True`

- [ ] **Step 3: Verify frontmatter**

Run:
```bash
Select-String -Path "pipeline\workflows\modify.md" -Pattern "^name: modify$"
```
Expected: Match found at line 2.

- [ ] **Step 4: Commit**

```bash
git add pipeline/workflows/modify.md
git commit -m "feat(workflow): add modify workflow for analysis output changes"
```

---

### Task 3: Create `commands/clinpub/modify.md`

**Files:**
- Create: `commands/clinpub/modify.md`

- [ ] **Step 1: Create the command entry point**

Write the following content to `commands/clinpub/modify.md`:

````markdown
---
name: clinpub:modify
description: "Modify completed analysis outputs. Clarifies modification scope (figure style, statistical method, variables), executes changes, verifies outputs, and records history in PLAN.md. Can be invoked from any phase. Triggers: modify figures, change analysis method, adjust chart style, replace variables."
argument-hint: "[method ID or brief description, leave empty for interactive selection]"
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
Modify completed Phase 2 analysis outputs. Support two categories:
1. **Style modifications**: color, font, chart type, layout adjustments (re-render figures)
2. **Method modifications**: statistical test change, variable replacement, parameter adjustment, new method addition (re-run analysis)
</objective>

<execution_context>
@./pipeline/workflows/modify.md
@./pipeline/references/analysis_methods.md
@./pipeline/references/r_patterns.md
@./agents/modify-agent.md
</execution_context>

<process>
Execute the modification workflow from @./pipeline/workflows/modify.md end-to-end.
</process>

<success_criteria>
- Modification scope defined and user-confirmed
- All modifications executed and verified
- Modified figures meet publication standards (>=300 DPI, English labels)
- Statistical reports include effect size + 95%CI + exact p-value
- Modification history appended to PLAN.md
- User informed about manuscript update requirement
</success_criteria>
````

- [ ] **Step 2: Verify file created**

Run:
```bash
Test-Path "commands\clinpub\modify.md"
```
Expected: `True`

- [ ] **Step 3: Verify frontmatter matches existing command pattern**

Run:
```bash
Select-String -Path "commands\clinpub\modify.md" -Pattern "^name: clinpub:modify$"
```
Expected: Match found at line 2.

- [ ] **Step 4: Verify allowed-tools matches other commands**

Run:
```bash
Select-String -Path "commands\clinpub\modify.md" -Pattern "AskUserQuestion"
```
Expected: Match found.

- [ ] **Step 5: Commit**

```bash
git add commands/clinpub/modify.md
git commit -m "feat(command): add /clinpub-modify command entry point"
```

---

### Task 4: Update `SKILL.md` — add command table entry

**Files:**
- Modify: `SKILL.md:28`

- [ ] **Step 1: Add modify command to the Commands table**

In `SKILL.md`, after the line:
```
| `/clinpub-milestone <N>` | Phase gate — Verify success criteria, record decisions, user sign-off |
```

Insert:
```
| `/clinpub-modify` | **Modify** — Adjust analysis outputs (figure style, statistical method, variables) post-analysis |
```

- [ ] **Step 2: Verify the table renders correctly**

Read the Commands section of SKILL.md and confirm:
1. The new row is between `/clinpub-milestone` and `## Quick Start`
2. The markdown table formatting matches existing rows (pipe alignment)

- [ ] **Step 3: Commit**

```bash
git add SKILL.md
git commit -m "docs(skill): add /clinpub-modify to command table"
```

---

### Task 5: Update `CLAUDE.md` — add to Key Directory + Agent Routing

**Files:**
- Modify: `CLAUDE.md:38`, `CLAUDE.md:71`

- [ ] **Step 1: Add modify-agent to Key Directory table**

In `CLAUDE.md`, after the line:
```
| `agents/clinpub-verifier.md` | Statistical verification agent (adversarial) |
```

Insert:
```
| `agents/modify-agent.md` | Analysis output modification agent |
```

- [ ] **Step 2: Add modify workflow reference to Key Directory**

After the line:
```
| `pipeline/workflows/` | Phase 0-4 orchestration + data2idea |
```

Change to:
```
| `pipeline/workflows/` | Phase 0-4 orchestration + data2idea + modify |
```

- [ ] **Step 3: Add modify-agent to Agent Routing table**

After the line:
```
| Statistical verification (adversarial) | `clinpub-verifier` |
```

Insert:
```
| Analysis output modification | `modify-agent` | R primary |
```

- [ ] **Step 4: Verify changes**

Read CLAUDE.md and confirm:
1. `agents/modify-agent.md` row appears after `clinpub-verifier.md` in Key Directory
2. `modify-agent` row appears after `clinpub-verifier` in Agent Routing
3. Table formatting is consistent

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude): register modify-agent in directory and routing tables"
```

---

### Task 6: Update `AGENTS.md` — add to Commands + Agent Routing

**Files:**
- Modify: `AGENTS.md:69`, `AGENTS.md:81`

- [ ] **Step 1: Add /clinpub-modify to Commands table**

In `AGENTS.md`, after the line:
```
| `/clinpub-milestone` | gate | Phase gate verification with user sign-off |
```

Insert:
```
| `/clinpub-modify` | — | Modify analysis outputs (figure style, method, variables) |
```

- [ ] **Step 2: Update Commands count header**

Change:
```
## Commands (8 skills installed)
```

To:
```
## Commands (9 skills installed)
```

- [ ] **Step 3: Add modify-agent to Agent Routing table**

After the line:
```
| Statistical verification (adversarial) | `clinpub-verifier` | — |
```

Insert:
```
| Analysis output modification | `modify-agent` | R primary |
```

- [ ] **Step 4: Update Architecture agent count**

Change:
```
Agents (agents/*.md)               → 7 specialized AI role cards
```

To:
```
Agents (agents/*.md)               → 8 specialized AI role cards
```

- [ ] **Step 5: Verify changes**

Read AGENTS.md and confirm:
1. Commands count shows 9
2. `/clinpub-modify` row present in Commands table
3. `modify-agent` row present in Agent Routing table
4. Architecture section shows 8 agents

- [ ] **Step 6: Commit all remaining changes**

```bash
git add AGENTS.md docs/superpowers/specs/2026-06-02-modify-agent-design.md docs/superpowers/plans/2026-06-02-modify-agent.md
git commit -m "docs(agents): register modify command and agent in AGENTS.md"
```
