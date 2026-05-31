---
name: clinpub:init-project
description: "Phase 0: Initialize clinical research project. Discuss study design, variables, analysis methods with user; generate project_config.yml, directory structure, and .clinpub/ artifacts."
argument-hint: ""
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
Phase 0: Project initialization. Discuss research framework with user, then generate the complete project directory structure and configuration.

Must discuss with user before creating anything: study type, core variables, analysis methods, target journal.
</objective>

<execution_context>
@./pipeline/workflows/init-project.md
</execution_context>

<process>
Execute the init-project workflow from @./pipeline/workflows/init-project.md end-to-end.
</process>

<success_criteria>
- Research framework discussed and documented
- Project directory structure created (.clinpub/, 01_RawData/, 02_PreprocessedData/, etc.)
- project_config.yml generated with all user decisions
- User decisions logged in .clinpub/
</success_criteria>
