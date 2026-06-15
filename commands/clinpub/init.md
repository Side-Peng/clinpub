---
name: clinpub:init
description: "Phase 0: Initialize clinical research project. Discuss study design, variables, analysis methods with user; generate project_config.yml, directory structure, and .clinpub/ artifacts."
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
Phase 0: Initialize a new clinical research project. Discuss the study framework with the user, create the project directory structure, generate project_config.yml, and set up .clinpub/ planning artifacts (PROJECT.md, ROADMAP.md, STATE.md).
</objective>

<execution_context>
@./pipeline/workflows/init-project.md
@./pipeline/templates/project.md
@./pipeline/templates/roadmap.md
@./pipeline/templates/state.md
@./pipeline/references/checkpoints.md
</execution_context>

<process>
Execute the workflow from @./pipeline/workflows/init-project.md

Key steps:
1. Discuss research framework with user (study type, variables, analysis methods, target journal)
2. Create standard project directory structure
3. Generate project_config.yml
4. Create .clinpub/ planning artifacts (PROJECT.md, ROADMAP.md, STATE.md)
5. Confirm setup with user
</process>

<success_criteria>
- project_config.yml exists and is complete
- Standard directory structure created (01_RawData/, 02_PreprocessedData/, etc.)
- .clinpub/STATE.md contains Phase 0 marker
- User has confirmed study design and variable mapping
</success_criteria>
