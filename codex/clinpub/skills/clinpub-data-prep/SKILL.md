---
name: clinpub-data-prep
description: "Phase 1: Data preparation and exploratory data analysis. Clean raw data, handle missing values, detect outliers, create derived variables, generate data quality report, and produce cleaned.csv."
---

# ClinPub Data Prep

Phase 1: Data preparation. Transform raw data into analysis-ready cleaned.csv with full data quality documentation.

Handles: missing value imputation, outlier detection, derived variable creation, encoding, train/validation split.
Supports re-entry: if project_config.yml exists with valid fields, auto-refreshes profiles and specs before entering discussion.

## Execution Context

- Workflow: `pipeline/workflows/data-prep.md`

## Process

Execute the data-prep workflow end-to-end.

## Re-entry Detection

Before executing the workflow, check if the project is already initialized:

1. Check if `project_config.yml` exists in project root
2. If exists, verify key fields are valid:
   - `project.name` non-empty (not default "项目名称")
   - `variables.outcome` non-empty
   - `paths.raw_data` corresponds to existing directory with data files
3. **If all checks pass** → Output "检测到已有项目配置（project_config.yml），执行自动刷新流程..." then execute `reinit_data_prep` (full refresh)
4. **If any check fails** → Output "未检测到完整项目配置，进入全新数据清洁流程" then enter normal data-prep workflow
5. Note: No PreToolUse hook logic added (all detection at command level)

## Success Criteria

- cleaned.csv exists at 02_PreprocessedData/data/
- Data quality report generated (HTML)
- Missing values handled per tiered strategy
- Outliers documented
- Derived variables created and encoded
- Cleaning code independently reproducible
