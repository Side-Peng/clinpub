---
name: init-project
description: "Phase 0 orchestration: Discuss research framework with user, infer study type if needed, generate project directory structure and project_config.yml."
---

<purpose>
Initialize a clinical research project by discussing the study framework with the user, creating the project directory structure, and generating project configuration.
</purpose>

<required_reading>
@./pipeline/templates/project_config.yml
@./pipeline/templates/project.md
@./pipeline/templates/roadmap.md
@./pipeline/templates/state.md
@./pipeline/references/checkpoints.md
</required_reading>

<process>

<step name="discuss_research_framework" priority="first">
Discuss with user before creating anything:

1. **Study basics**: title, research type, objectives, hypotheses
2. **Data overview**: source, sample size, key variables (outcome, exposure, covariates)
3. **Analysis methods**: select from candidate pool (baseline table, group comparison, regression, survival, subgroup, sensitivity, correlation, ROC, marker panel, ML)
4. **Expected output**: target journal, needed figure/table types, language preferences

**Study type auto-inference** (when user is uncertain):
- Randomized group variable → suggest RCT
- Time-to-event + exposure → suggest cohort
- Case/control group + matching ID → suggest case-control
- Single time point + exposure + outcome → suggest cross-sectional
- Demographics + clinical features only → suggest descriptive
- Multiple biomarkers + outcome → suggest biomarker panel

Auto-inference is advisory only — final type must be user-confirmed.
</step>

<step name="create_project_structure" priority="high">
After discussion, create the project directory structure:

```
Project_Root/
├── .clinpub/
│   ├── PROJECT.md              ← from project.md template
│   ├── ROADMAP.md              ← from roadmap.md template
│   ├── STATE.md                ← from state.md template
│   └── phases/
│       └── 00-init/
│           └── 00-CONTEXT.md   ← discussion log
├── 01_RawData/                 ← raw data (read-only)
├── 02_PreprocessedData/
│   ├── data/                   ← cleaned.csv lives here
│   └── reports/
├── 03_AnalysisMethods/         ← only user-confirmed method dirs
├── 04_Outputs/                 ← figures + tables
├── Reference/                  ← literature
├── 05_Manuscript/             ← chapter drafts
│   └── response_letters/
├── project_config.yml          ← configuration
└── run_all.R                   ← master R script
```

**Important**: `03_AnalysisMethods/` and `04_Outputs/` should only contain directories for user-confirmed analysis methods.
</step>

<step name="generate_config" priority="high">
Generate `project_config.yml` based on discussion outcomes. See template for full structure.

Key sections:
- `project`: name, description, study_design, sample_size, target_journal, reporting_standard
- `variables`: outcome, outcome_type, exposure, covariates, time_variable, event_variable, group_variable, id_variable
- `paths`: all directory paths
- `methods_to_run`: user-confirmed methods (dynamically numbered)
- `language`: manuscript language, figures/tables language, statistics language
- `quality`: journal level, figure DPI, format, font, font size
- `analysis`: missing value thresholds, significance level, multiple comparison method
</step>

<step name="log_decisions" priority="medium">
Record all user decisions in `.clinpub/phases/00-init/00-CONTEXT.md`:
- Study type and rationale
- Variable roles and definitions
- Selected analysis methods
- Target journal and quality requirements
- Any deferrals or open questions
</step>

<step name="checkpoint_confirm" priority="medium">
Present a `checkpoint:verify` to user confirming the project structure and config are ready before proceeding:

- [ ] Project structure created as agreed
- [ ] project_config.yml reflects all decisions
- [ ] ROADMAP.md shows Phase 0 status

If user requests changes, go back. If approved, proceed to milestone.
</step>

<step name="milestone" priority="high">
Execute the milestone workflow to formally close Phase 0 and gate into Phase 1:

```bash
# The milestone workflow will:
# 1. Verify success criteria for Phase 0
# 2. Collect decisions from 00-CONTEXT.md
# 3. Generate .clinpub/phases/00-init/MILESTONE.md
# 4. Update ROADMAP.md: Phase 0 → ✅ Complete, Phase 1 → 🔄 In Progress
# 5. Update STATE.md: current_phase → 1
# 6. Request user sign-off
```

See @./pipeline/workflows/milestone.md for full protocol.
</step>

</process>

<success_criteria>
- Study framework fully discussed and documented
- Project directory structure created with .clinpub/ layer
- project_config.yml reflects all user decisions
- Only user-confirmed analysis method directories created
- Decision log written to 00-CONTEXT.md
</success_criteria>
