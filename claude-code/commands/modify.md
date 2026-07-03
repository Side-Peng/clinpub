---
name: modify
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
