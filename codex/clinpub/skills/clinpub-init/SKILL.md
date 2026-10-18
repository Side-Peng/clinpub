---
name: clinpub-init
description: "阶段0：初始化或导入临床研究项目。检测已有研究材料并导入 clinpub 结构，或从零开始。与用户讨论研究设计、变量与分析方法，并明确询问目标投稿期刊（不预设，适配任意临床研究类型）；生成 project_config.yml、目录结构与 .clinpub/ 状态文件。"
---

# ClinPub Init

阶段0: Initialize a new clinical research project or import an existing one. If research artifacts are detected (data files, analysis outputs, manuscript drafts), enter import mode to scan, infer roles, confirm mapping, and adapt to clinpub structure. Otherwise, discuss the study framework with the user, create the project directory structure, generate project_config.yml, and set up .clinpub/ planning artifacts.

## Execution Context

- Workflow: `pipeline/workflows/init-project.md`
- Templates: `pipeline/templates/project.md`, `roadmap.md`, `state.md`, `method-readme.md`
- References: `pipeline/references/checkpoints.md`, `r_patterns.md`
- Import: `pipeline/workflows/import-project.md`, `pipeline/references/import-heuristics.md`

## Process

Execute the workflow from `pipeline/workflows/init-project.md`:

1. Detect import mode: scan project root for existing research artifacts (CSV/XLSX/PNG/MD/BIB/R/Py files, standard clinpub directories)
2. IF import mode detected → execute import-project.md workflow (scan → infer roles → confirm mapping → gap analysis → adapt structure → generate config → milestone)
3. IF no artifacts found → execute standard initialization:
   a. Discuss research framework with user (study type, variables, analysis methods); explicitly ask for the target submission journal (name + tier) — do not preset, this pipeline adapts to any clinical research article type
   b. Create standard project directory structure
   c. Generate project_config.yml
   d. Create .clinpub/ planning artifacts (PROJECT.md, ROADMAP.md, STATE.md)
   e. Confirm setup with user

## Success Criteria

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
