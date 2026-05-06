---
name: analysis
description: "Phase 2 orchestration: Diagnose data structure → discuss with user → propose dynamic analysis plan → execute in dependency order. Each method produces figure + table + README with publication-grade standards."
---

<purpose>
Adaptively determine and execute the optimal analysis plan based on data structure diagnosis and user discussion. Unlike a fixed menu, the analysis plan is built dynamically per project: Claude reads the data, detects its characteristics (groups, timepoints, outcome types), proposes appropriate methods from the reference library, discusses with the user, then executes in computed dependency order.
</purpose>

<required_reading>
@./pipeline/references/analysis_methods.md
@./pipeline/references/r_patterns.md
@./pipeline/references/checkpoints.md
@./agents/analyst-agent.md
</required_reading>

<process>

<step name="diagnose_data_structure" priority="first">
Load cleaned data and diagnose its structure before proposing any methods:

```bash
PROJECT_DIR=$(pwd)
DATA="$PROJECT_DIR/02_PreprocessedData/data/cleaned.csv"
FULL_DATA="$PROJECT_DIR/02_PreprocessedData/data/full_longitudinal.csv"  # may not exist
CONFIG="$PROJECT_DIR/project_config.yml"
```

Diagnose these characteristics from the data:

1. **Group structure**: How many groups? What are their names? Sample per group?
2. **Timepoints**: Single timepoint or repeated measures? Labels?
3. **Outcome variables**: Identify from project_config.yml or profile.
   - Binary (2 unique values) → logistic regression candidate
   - Continuous (many unique values) → linear model / t-test candidate
   - Survival (has time + event columns) → survival analysis candidate
4. **Covariates**: Which variables are demographics? Clinical measures?
5. **Missing pattern**: High missingness? Structural missing (by design)?
6. **Longitudinal flag**: Does each patient appear in multiple rows?
7. **Exposure/treatment**: Which variable represents the intervention?

**Record diagnosis as structured notes:**
```yaml
# Written to .planning/phases/02-analysis/00-DIAGNOSIS.md
data_diagnosis:
  n_patients: 86
  n_rows: 258
  structure: longitudinal  # or cross-sectional
  groups: 2
  group_names: ["Sham", "cTBS"]
  timepoints: ["baseline", "post_treatment", "follow_up"]
  analysis_timepoint: "baseline"  # from data-prep Phase 1 decision
  outcomes:
    - variable: "HAMA_total"
      type: continuous
      distribution: "right-skewed"
    - variable: "HAMD_total"
      type: continuous
      distribution: "right-skewed"
  outcome_type: continuous
  has_covariates: true
  structural_missing: ["cg_factor1", "cg_factor2", "cg_factor3", "cg_factor4", "cg_factor5", "cg_Total_score"]
```
</step>

<step name="propose_analysis_plan" priority="first">
Based on data diagnosis, use the decision tree in `analysis_methods.md §二` to dynamically build a recommended analysis plan.

**Reference the decision tree:**
- Match data characteristics → recommended method directions (analysis_methods.md Step 2 table)
- Organize into dependency waves (analysis_methods.md Step 3)
- Look up detailed technique references in the scenarios library (analysis_methods.md §三)

**Present a structured proposal to the user:**

```markdown
## 推荐分析方案

根据您的数据诊断结果（{n}人，{k}组，{t}个时间点），我建议以下分析方案：

### Wave 1：基线描述 / 数据概览
{method_description}

### Wave 2：{依据方案定标题}
{method_description}

*[更多波次按需追加，无固定数量限制]*

---

**需要您确认：**
1. 这些方法是否符合您的研究问题？
2. 需要增加/删减哪些？
3. 各方法的参数、变量选择是否合适？
4. 颜色方案偏好？（见 r_patterns.md §1.1）
```

**示例（针对一项纵向 RCT 数据）：**
```
### Wave 1：基线描述
1. 基线特征表——比较 cTBS vs Sham 组的人口学和临床特征
2. 各时间点 HAMD 的 mean±SD 描述统计

### Wave 2：组间比较
3. HAMD 在 cTBS vs Sham 组的基线差异（Wilcoxon）
4. 重复测量混合模型——time×group 交互效应 (lme4)

### Wave 3：多因素调整
5. 调整年龄、性别后 Treatment 对 HAMD 变化的线性回归

---

需要您确认以上方案是否合适。
```

**Important**: The Wave labels and count are **dictated by the data, not by the template**. A single-wave project (e.g., "just a baseline table") has 1 wave. A comprehensive project might have 5. The example above is just one possible configuration.
</step>

<step name="discuss_and_confirm" priority="high">
Discuss the proposed plan with user and finalize:

1. **Method list**: User adds, removes, or adjusts methods
2. **Method parameters**: Variable selection strategy, model covariates, reference groups
3. **Figure/table preferences**: Color palette (see r_patterns.md §1.1), output format, dimensions
4. **Train/validation split**: If prediction/ML methods confirmed, discuss ratio
5. **Multiple comparison correction**: FDR vs Bonferroni vs none
6. **Significance level**: default α=0.05
7. **Outcome transformation**: If creating binary cutoffs, discuss threshold basis (median, clinical)

**Write confirmed plan** to `.planning/phases/02-analysis/01-PLAN.md`:

```yaml
analysis_plan:
  summary: "86例 cTBS vs Sham RCT，3时间点，连续结局。共 3 个波次。"
  waves:
    1:
      label: "基线描述"
      methods:
        - id: "01_BaselineTable"
          type: baseline
          data: "cleaned.csv"
          timepoint: "baseline"
          outputs: ["Table1.docx", "Table1.xlsx"]
    2:
      label: "组间比较与纵向分析"
      methods:
        - id: "02_TwoGroupComparison"
          type: comparison
          data: "cleaned.csv"
          timepoint: "baseline"
          method: "wilcox.test"
          grouping: "Treatment"
          outcomes: ["HAMA_total", "HAMD_total"]
          outputs: ["boxplot_*.png", "comparison_table.xlsx"]
        - id: "03_RepeatedMeasures"
          type: longitudinal
          data: "full_longitudinal.csv"
          method: "lme4::lmer()"
          formula: "HAMD_total ~ Treatment * time + (1 | name)"
          outputs: ["fixed_effects_table.docx", "interaction_plot.png"]
    3:
      label: "多因素分析"
      methods:
        - id: "04_LinearRegression"
          type: regression
          data: "cleaned.csv"
          timepoint: "baseline"
          formula: "HAMD_total ~ Treatment + age + sex + BMI"
          outputs: ["regression_table.docx", "forest_plot.png"]
```
</step>

<step name="execute_waves" priority="high">
Execute the confirmed analysis plan **wave by wave, dynamically**.

The plan has `N` waves (N could be 1, 3, 5 — whatever was agreed with the user). Execute them in order:

```python
# Pseudo-logic:
for wave_num in sorted(analysis_plan.waves.keys()):
    wave = analysis_plan.waves[wave_num]
    for method in wave.methods:
        execute_method(method)         # code → run → verify → README
    checkpoint(f"Wave {wave_num} complete — {wave.label}")
    # User confirms before next wave
```

Each method execution:
1. Creates directory `03_AnalysisMethods/{id}/` and `04_Outputs/{id}/` (see r_patterns.md §1.7)
2. Generates R/Python code based on the method's `type`, `method`, and `formula` fields
3. Runs the code, verifies outputs exist, writes README.md

**Wave frequency is not fixed.** If the plan has 1 wave, execute 1. If it has 6 waves, execute 6.

**After all waves execute**, proceed to `verify_outputs`.

**During Phase 3 (writing) or Phase 4 (review):** If the user requests additional analyses, create a new wave and execute it. Append to the plan:
```yaml
# Appended during Phase 4
    4:
      label: "审稿人要求补充分析"
      methods:
        - id: "05_SensitivityAnalysis_E-value"
          type: sensitivity
          data: "cleaned.csv"
          method: "E-value calculation"
```
</step>

<step name="verify_outputs" priority="medium">
After all waves complete, final verification:

1. Each method's figure(s) + table(s) + README exist
2. Figures ≥300 DPI, English labels, publication-grade theme
3. Statistical reports include effect size + 95%CI + exact p-value
4. Code independently runnable from cleaned.csv
5. R version and key package versions documented
6. MANIFEST.yaml exists in `04_Outputs/` listing writer-agent as consumer

If manifest is missing, write it here: `04_Outputs/MANIFEST.yaml` documenting each method's outputs and statistics.
</step>

</process>

<step name="milestone" priority="high">
Execute the milestone workflow to formally close Phase 2 and gate into Phase 3:

```bash
# The milestone workflow will:
# 1. Verify success criteria for Phase 2
# 2. Collect analysis decisions (method selection, parameters)
# 3. Generate .planning/phases/02-analysis/MILESTONE.md
# 4. Update ROADMAP.md: Phase 2 → ✅ Complete, Phase 3 → 🔄 In Progress
# 5. Update STATE.md: current_phase → 3
# 6. Request user sign-off
```

See @./pipeline/workflows/milestone.md for full protocol.
</step>

<statistical_reporting_standards>
- Every analysis: **effect size + 95%CI + exact p-value** (not just "p < 0.05")
- Multiple comparisons: apply FDR/Bonferroni correction
- Report software: R version + key package versions
- Test assumptions: normality, homoscedasticity, proportional hazards
- Flag violations and document mitigations
</statistical_reporting_standards>

<success_criteria>
- Data structure diagnosed and documented
- Analysis plan proposed, discussed, and user-confirmed
- Each confirmed method has complete figure + table + README
- All figures meet publication-grade standards (≥300 DPI, theme_pub)
- Statistical reports complete with effect size + 95%CI + p-value
- Dependency-aware execution order respected (wave N+1 waits for wave N user confirmation)
- Code independently reproducible from cleaned.csv
- User briefed after each wave
</success_criteria>
