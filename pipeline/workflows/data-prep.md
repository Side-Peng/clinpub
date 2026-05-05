---
name: data-prep
description: "Phase 1 orchestration: Load raw data, discuss cleaning strategy with user, execute data preparation pipeline, produce cleaned.csv and data quality report."
---

<purpose>
Transform raw patient-level data into analysis-ready cleaned.csv with full quality documentation. Handle missing values, outliers, derived variables, and encoding through a tiered decision framework with user confirmation at ambiguity points.
Supports re-entry refresh: re-runs profile, spec, and config when project is already initialized.
</purpose>

<required_reading>
@./pipeline/references/analysis_methods.md
@./agents/analyst-agent.md
@./pipeline/references/checkpoints.md
</required_reading>

<process>

<step name="reinit_data_prep" priority="first">
当检测到项目已初始化时（由命令入口 data-prep.md 触发），执行全链路文件刷新：

1. **重新运行 profile（更新变量字典）**
   - 定位原始数据文件（从 `project_config.yml` 的 `paths.raw_data` 字段获取路径，查找 `01_RawData/` 下的第一个 CSV/XLSX 文件）
   - 执行：`python scripts/data_profiler.py {raw_data_filepath} --output {preprocessed_path}/data_profile.json`
   - 读取输出的 `data_profile.json`，获取最新的变量列表、缺失模式、变量角色等

2. **重新生成 spec 模板（更新分析规范）**
   - 读取 `data_profile.json` 的变量摘要和 `project_config.yml` 的项目配置
   - 基于 `pipeline/templates/spec.md` 模板，填充以下 Mustache 占位符：
     - `{{study_title}}` -> 从 `project_config.yml` 的 `project.name` 读取
     - `{{study_type}}` -> 从 `project_config.yml` 的 `project.design` 读取
     - `{{N}}` -> 从 `data_profile.json` 的 `n_rows` 读取
     - `{{primary_outcome}}` -> 从 `project_config.yml` 的 `variables.outcome` 读取
     - `{{phase_number}}` -> "1"
     - `{{phase_name}}` -> "Data Preparation"
     - `{{date}}` -> 当前日期
   - 未更改的占位符保持原样（留给 Phase 2 填充）
   - 输出到 `03_AnalysisMethods/01-spec.md`（覆盖旧文件）

3. **同步更新 project_config.yml**
   - 读取当前 `project_config.yml`
   - 根据 `data_profile.json` 的 `role_summary` 更新：
     - `variables.outcome`：如果 profile 检测到 outcome 角色变量且当前 config 中 outcome 为空，填充第一个 outcome 变量名
     - `variables.covariates`：从 profile 的 covariate 角色变量更新列表
     - `variables.group_variable`：从 profile 的 exposure 角色变量更新
   - 仅更新变量相关字段，保留用户自定义的 `project.name`、`analysis` 阈值等手动配置
   - 写回 `project_config.yml`（覆盖但不破坏用户手动编辑的非变量字段）

4. **向用户报告变更摘要**
   - 输出格式：
     ```
     ### 刷新完成
     - Profile 更新: {n_variables} 个变量，{n_rows} 行
     - Spec 更新: 填充了 {n_filled_fields} 个字段
     - Config 更新: {changed_fields} 字段已同步
     - 下一步: 清理策略讨论
     ```
</step>

<step name="discuss_cleaning_strategy" priority="first">
Discuss with user before any data transformation:

1. **Missing value strategy**: confirm tiered thresholds (<5% delete/fill, 5-20% MICE imputation, >20% flag for discussion)
2. **Outlier handling**: IQR vs Z-score thresholds, winsorization vs exclusion
3. **Variable encoding**: categorical reference levels, continuous variable transformations
4. **Derived variables**: any calculated scores, indices, or composite variables needed
5. **Train/validation split**: needed? Ratio? Stratification variables?
</step>

<step name="detect_data_structure" priority="first">
Before cleaning, detect data structure characteristics that affect downstream analysis:

1. **Longitudinal detection**: Check for repeated patients (same `name`/`id` with different `time` values)
   - If `time` column exists AND patient ID appears multiple times → **longitudinal data**
   - For each patient, count timepoints; if majority have >1 → **repeated measures**
2. **Outcome type detection**: Infer `outcome_type` from variable values:
   - Unique values = 2 → binary
   - Unique values 3-20 → could be categorical/continuous
   - Unique values >20 → continuous (check distribution)
3. **Structural missingness**: If specific variables are missing only at certain timepoints → flag as "structurally missing" (not data quality issue)

**If longitudinal data detected**: Discuss with user:
   - Which timepoint(s) to use for analysis (e.g., "baseline only", "change scores", "all timepoints")
   - Store decision as `analysis_timepoint: "baseline"` in processing notes
   - For Table 1/BaselineTable: **must filter to a single timepoint** (typically baseline) to avoid duplicate patient counting
   - For repeated measures analysis: note that mixed models (lme4) will be needed instead of standard t-tests

**Recording**: Write structural notes to `.planning/phases/01-data-prep/00-STRUCTURE.md`:
```yaml
data_structure:
  type: longitudinal | cross-sectional
  n_patients: 86
  n_timepoints: 3
  timepoint_labels: ["baseline", "post_treatment", "follow_up"]
  analysis_timepoint: "baseline"
  structural_missing: ["cg_factor1", "cg_factor2"]
```
</step>

<step name="execute_cleaning" priority="high">
Load raw data from `01_RawData/` and execute cleaning pipeline:

1. **Import data** → generate variable dictionary (name, type, missing rate, unique values, sample values)
2. **Missing value handling**
   - <5%: delete rows or fill with mean/median/mode
   - 5-20%: MICE imputation (report imputation model)
   - >20%: discuss with user before proceeding
3. **Outlier detection**
   - Continuous: IQR (1.5×) or Z-score (|Z|>3)
   - Categorical: check for unexpected values
   - Flag and document all outliers found
4. **Derived variables** + encoding
   - Create calculated variables
   - Set factor levels and reference categories
   - Apply any transformations (log, Box-Cox, etc.)
5. **Data quality report** (HTML):
   - Variable summary table
   - Missing value matrix
   - Distribution plots for key variables
   - Outlier documentation
   - Training/validation split summary (if applicable)
   - **If longitudinal**: include missing pattern by timepoint to distinguish structural vs random missingness

6. **Filter to analysis timepoint** (if longitudinal):
   - Use the user-confirmed `analysis_timepoint` (typically "baseline")
   - Filter cleaned data to that timepoint before saving as `cleaned.csv`
   - Save the full longitudinal data as `02_PreprocessedData/data/full_longitudinal.csv` (for mixed models later)

All ambiguous handling points must be confirmed with user.
</step>

<step name="validate_output" priority="high">
After cleaning:

1. Verify `cleaned.csv` exists at `02_PreprocessedData/data/`
2. Check row/column counts match expectations
3. Confirm high-missingness variables are handled
4. Verify data types are correct
5. Ensure cleaning code is independently reproducible
6. Report cleaning summary to user:
   - Rows removed/retained
   - Variables modified/created
   - Missing values imputed
   - Outliers detected and handled
</step>

<step name="checkpoint_confirm" priority="medium">
Present a `checkpoint:verify` to user confirming the cleaned data is ready:

- [ ] cleaned.csv validated with expected dimensions
- [ ] Data quality report generated
- [ ] All ambiguous decisions confirmed during cleaning

If user requests changes, address them. If approved, proceed to milestone.
</step>

<step name="milestone" priority="high">
Execute the milestone workflow to formally close Phase 1 and gate into Phase 2:

```bash
# The milestone workflow will:
# 1. Verify success criteria for Phase 1
# 2. Collect data cleaning decisions
# 3. Generate .planning/phases/01-data-prep/MILESTONE.md
# 4. Update ROADMAP.md: Phase 1 → ✅ Complete, Phase 2 → 🔄 In Progress
# 5. Update STATE.md: current_phase → 2
# 6. Request user sign-off
```

See @./pipeline/workflows/milestone.md for full protocol.
</step>

</process>

<success_criteria>
- cleaned.csv written to 02_PreprocessedData/data/
- Data quality report generated (HTML)
- Missing values handled per agreed strategy
- Outliers documented
- Derived variables created and encoded
- Cleaning code independently reproducible from raw data
- User briefed on cleaning summary
</success_criteria>
