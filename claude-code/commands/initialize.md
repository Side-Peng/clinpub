---
name: initialize
description: "Phase 0: Initialize or import a clinical research project. Detect existing artifacts and import into clinpub structure, or start fresh. Discuss study design, variables, analysis methods with user, and explicitly ask for the target submission journal (no journal is preset — adapts to any clinical research article); generate project_config.yml, directory structure, and .clinpub/ artifacts."
argument-hint: ""
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
---
<objective>
Phase 0: Initialize a new clinical research project or import an existing one. If research artifacts are detected (data files, analysis outputs, manuscript drafts), enter import mode to scan, infer roles, confirm mapping, and adapt to clinpub structure. Otherwise, discuss the study framework with the user, create the project directory structure, generate project_config.yml, and set up .clinpub/ planning artifacts.
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/init-project.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/templates/project.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/templates/roadmap.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/templates/state.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/templates/method-readme.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/checkpoints.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/r_patterns.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/import-project.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/import-heuristics.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/templates/import-milestone.md"`
</execution_context>

<process>
Execute the workflow from pipeline/workflows/init-project.md

Key steps:
1. Detect import mode: scan project root for existing research artifacts (CSV/XLSX/PNG/MD/BIB/R/Py files, standard clinpub directories)
2. IF import mode detected → execute import-project.md workflow (scan → infer roles → confirm mapping → gap analysis → adapt structure → generate config → milestone)
3. IF no artifacts found → execute standard initialization:
   a. Discuss research framework with user (study type, variables, analysis methods); explicitly ask for the target submission journal (name + tier) — do not preset, this pipeline adapts to any clinical research article type
   b. Create standard project directory structure
   c. Generate project_config.yml
   d. Create .clinpub/ planning artifacts (PROJECT.md, ROADMAP.md, STATE.md)
   e. Confirm setup with user
</process>

<success_criteria>
- project_config.yml exists and is complete
- Standard directory structure created (01_RawData/, 02_PreprocessedData/, etc.)
- Per-method subdirectories created: `03_AnalysisMethods/{method_id}/` and `04_Outputs/{method_id}/` for each confirmed method
- Placeholder `方法说明.md` exists in each `03_AnalysisMethods/{method_id}/`
- .clinpub/STATE.md contains correct Phase marker (import_mode cleared if import was used)
- User has confirmed study design and variable mapping

Import mode additional (if applicable):
- Imported files copied to standard locations
- IMPORT-MILESTONE.md generated with gate status
- Starting phase correctly set based on existing artifacts
- Gap remediation plan documented
</success_criteria>
