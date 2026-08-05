---
name: modify
description: "Modify completed analysis outputs or add new analysis methods. Clarifies scope (figure style, statistical method, variables, new method), executes changes, verifies outputs, and records history in PLAN.md. Can be invoked from any phase. Triggers: modify figures, change analysis method, adjust chart style, replace variables, add new analysis method."
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
Modify completed Phase 2 analysis outputs or add new analysis methods. Two core purposes:
1. **Modify existing methods**: style modifications (color, font, chart type, layout adjustments — re-render figures) and method modifications (statistical test change, variable replacement, parameter adjustment — re-run analysis)
2. **Add new methods**: read the current analysis code (`03_AnalysisMethods/`) and cleaned data (`cleaned.csv`), combine with the user's requirements, then design and implement a new analysis method that conforms to clinpub conventions (method ID format, figure config, publication standards)
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/modify.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/analysis_methods.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/r_patterns.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/agents/modify-agent.md"`
</execution_context>

<process>
Execute the modification workflow from pipeline/workflows/modify.md end-to-end.
</process>

<success_criteria>
- Modification scope defined and user-confirmed
- All modifications executed and verified
- Modified figures meet publication standards (>=300 DPI, English labels)
- Statistical reports include effect size + 95%CI + exact p-value
- Modification history appended to PLAN.md
- User informed about manuscript update requirement
</success_criteria>
