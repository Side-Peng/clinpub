---
name: analysis
description: "Phase 2 orchestration: Diagnose data structure → discuss with user → propose dynamic analysis plan → execute in dependency order. Each method produces figure + table + 方法说明 with publication-grade standards."
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
# Written to .clinpub/phases/02-analysis/00-DIAGNOSIS.md
# 变量名和分组名来自用户的 cleaned.csv，以下为示例结构：
data_diagnosis:
  n_patients: 86
  n_rows: 258
  structure: longitudinal  # or cross-sectional
  groups: 2
  group_names: ["{group_A}", "{group_B}"]
  timepoints: ["baseline", "post_treatment", "follow_up"]
  analysis_timepoint: "baseline"  # from data-prep Phase 1 decision
  outcomes:
    - variable: "{outcome_1}"
      type: continuous
      distribution: "right-skewed"
    - variable: "{outcome_2}"
      type: continuous
      distribution: "right-skewed"
  outcome_type: continuous
  has_covariates: true
  structural_missing: ["{variable_1}", "{variable_2}"]
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
1. 基线特征表——比较 {group_A} vs {group_B} 组的人口学和临床特征
2. 各时间点 {outcome} 的 mean±SD 描述统计

### Wave 2：组间比较
3. {outcome} 在 {group_A} vs {group_B} 组的基线差异（Wilcoxon）
4. 重复测量混合模型——time×group 交互效应 (lme4)

### Wave 3：多因素调整
5. 调整年龄、性别后干预对 {outcome} 变化的线性回归

---

需要您确认以上方案是否合适。
```

**Important**: The Wave labels and count are **dictated by the data, not by the template**. A single-wave project (e.g., "just a baseline table") has 1 wave. A comprehensive project might have 5. The example above is just one possible configuration.
</step>

<step name="discuss_and_confirm" priority="high">
Discuss the proposed plan with user and finalize:

1. **Method list**: User adds, removes, or adjusts methods
2. **Method parameters**: Variable selection strategy, model covariates, reference groups
3. **Figure/table preferences**: Color palette (see r_patterns.md §1.1 Color Config Protocol), output format, dimensions, **theme style** (see r_patterns.md §1.2 Config Protocol). Confirmed theme/color settings will be written into `_figure_config.R` — a shared configuration script sourced by all method R scripts to ensure visual consistency.
4. **Train/validation split**: If prediction/ML methods confirmed, discuss ratio
5. **Multiple comparison correction**: FDR vs Bonferroni vs none
6. **Significance level**: default α=0.05
7. **Outcome transformation**: If creating binary cutoffs, discuss threshold basis (median, clinical)
8. **Theme customization**: `theme_pub()` parameters (see r_patterns.md §1.2 Config Protocol)
   - Present current defaults and ask: "您希望调整图表主题样式吗？"
   - Show configurable parameters:

   | 参数 | 默认值 | 说明 |
   |------|--------|------|
   | `variant` | `theme_pub` | `theme_pub`（标准带边框）或 `theme_pub_light`（轻量无边框） |
   | `base_size` | 11 | 基础字号（影响所有文本元素实际 pt） |
   | `base_family` | "sans" | 字体族（Windows=Arial） |
   | `legend_position` | "right" | 图例位置：right / bottom / top / none |
   | `title_hjust` | 0 | 标题对齐：0=左对齐(Nature风格), 0.5=居中 |
   | `panel_border` | true | 是否有数据区黑色边框 |

   - If user has no preference, keep all defaults (backward compatible)
   - Write confirmed values to `project_config.yml` under `quality.theme`
9. **Color palette customization**: (see r_patterns.md §1.1 Color Config Protocol)
   - Present current defaults and ask: "您希望调整图表配色吗？"
   - Show configurable parameters:

   | 参数 | 默认值 | 说明 |
   |------|--------|------|
   | `preset` | `auto` | 预设方案：`auto`(按组数自动选择) / `nature` / `okabe-ito` / `brewer-set1` / `brewer-dark2` / `custom` |
   | `custom_colors` | `[]` | 自定义色值列表，如 `["#FF6B6B", "#4ECDC4"]` |
   | `group_mapping` | `{}` | 分组名→色值映射，如 `{Treatment: "#0072B5", Control: "#BC3C29"}` |
   | `continuous` | `viridis` | 连续变量色标：viridis / magma / plasma / inferno |

   - Default `auto` behavior: 2 groups → Nature dual-color; 3-4 → Set1; 5-8 → Set2; continuous → viridis
   - If user has no preference, keep `auto` (backward compatible)
   - Write confirmed values to `project_config.yml` under `quality.color_palette`

<!-- 方法搜索触发（Phase 4 方法增强） -->
**方法搜索提示：**
如果用户提到不熟悉的统计方法（如"这个方法我不太熟悉"、"帮我查一下 XX 检验"），
在讨论过程中自动触发 `reference-agent` 的 `method_search` 模式（见 `agents/reference-agent.md §method_search`）：

1. 调用 Tavily 搜索方法概览 + 适用场景
2. 学术引用不足时用 PubMed 补充
3. 输出摘要级结果直接替换 spec 的方法描述部分
4. 用户追问时输出详细教程到 `attachments/{method-name}-tutorial.md`

如果用户确认的对比方法涉及 2 组或 3+ 组比较，提示用户：
1. 对比方法已标准化到 `pipeline/references/comparison-methods.md`
2. 给出标准检验树（正态性→方差齐性→具体方法→效应量）

**Write confirmed plan** to `.clinpub/phases/02-analysis/01-PLAN.md`:

```yaml
# 变量名、分组名和文件名来自用户数据和 project_config.yml
analysis_plan:
  summary: "86例 {group_A} vs {group_B} RCT，3时间点，连续结局。共 3 个波次。"
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
          grouping: "{grouping_variable}"
          outcomes: ["{outcome_1}", "{outcome_2}"]
          outputs: ["boxplot_*.png", "comparison_table.xlsx"]
        - id: "03_RepeatedMeasures"
          type: longitudinal
          data: "full_longitudinal.csv"
          method: "lme4::lmer()"
          formula: "{outcome} ~ {grouping_variable} * time + (1 | id)"
          outputs: ["fixed_effects_table.docx", "interaction_plot.png"]
    3:
      label: "多因素分析"
      methods:
        - id: "04_LinearRegression"
          type: regression
          data: "cleaned.csv"
          timepoint: "baseline"
          formula: "{outcome} ~ {grouping_variable} + age + sex + BMI"
          outputs: ["regression_table.docx", "forest_plot.png"]
# Theme configuration (from discuss_and_confirm step 8)
theme_config:
  variant: "theme_pub"
  base_size: 11
  base_family: "sans"
  legend_position: "right"
  title_hjust: 0
  panel_border: true
# Color palette configuration (from discuss_and_confirm step 9)
color_palette_config:
  preset: "auto"
  custom_colors: []
  group_mapping: {}
  continuous: "viridis"
```
</step>

<step name="generate_figure_config" priority="high">
After discussing and confirming theme/color configuration, before executing analysis waves, generate the shared figure configuration script:

1. Read `project_config.yml` sections `quality.theme` and `quality.color_palette`
2. Copy `pipeline/templates/_figure_config.R` template to `04_Outputs/_figure_config.R`
3. Verify the script can be sourced without errors:
   ```bash
   Rscript -e 'source("04_Outputs/_figure_config.R"); cat("Figure config OK\n")'
   ```

**Mandatory rules for all subsequent method R scripts:**
- `source("04_Outputs/_figure_config.R")` must appear immediately after `library()` calls
- Use `apply_theme()` instead of manual `theme_pub()` calls
- Use `get_palette(n)` instead of hand-picked colors
- Use `save_figure()` for unified export
- Do NOT redefine `theme_pub`, `get_palette`, or other functions already defined in `_figure_config.R`
</step>

<step name="execute_waves" priority="high">
Execute the confirmed analysis plan **wave by wave, dynamically**.

The plan has `N` waves (N could be 1, 3, 5 — whatever was agreed with the user). Execute them in order:

```python
# Pseudo-logic:
for wave_num in sorted(analysis_plan.waves.keys()):
    wave = analysis_plan.waves[wave_num]
    for method in wave.methods:
        execute_method(method)         # code → run → verify → 方法说明
    checkpoint(f"Wave {wave_num} complete — {wave.label}")
    # User confirms before next wave
```

Each method execution:
1. Creates directory `03_AnalysisMethods/{id}/` and `04_Outputs/{id}/` (see r_patterns.md §1.7)
2. Generates R/Python code based on the method's `type`, `method`, and `formula` fields
   - **Mandatory**: Every R script must `source("04_Outputs/_figure_config.R")` after `library()` calls
   - **Prohibited**: Redefining `theme_pub`, `get_palette`, `save_figure` etc. in method scripts
3. Runs the code, verifies outputs exist, writes 方法说明.md

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

1. Each method's figure(s) + table(s) + 方法说明 exist
2. Figures ≥300 DPI, English labels, publication-grade theme
3. Statistical reports include effect size + 95%CI + exact p-value
4. Code independently runnable from cleaned.csv
5. R version and key package versions documented
6. MANIFEST.yaml exists in `04_Outputs/` listing writer-agent as consumer
7. **Shared config check**: `04_Outputs/_figure_config.R` exists and every R script in `03_AnalysisMethods/` contains `source("04_Outputs/_figure_config.R")` (verify via grep)

If manifest is missing, write it here: `04_Outputs/MANIFEST.yaml` documenting each method's outputs and statistics.
</step>

<step name="user_satisfaction_check" priority="high">
所有 waves 执行完毕、即将进入 milestone 关闭 Phase 2 之前，先向用户确认对当前分析结果是否满意：

```
✅ Phase 2 分析已完成全部 wave，结果已保存至 04_Outputs/。

请确认：
- 满意 → 继续执行 `/clinpub-milestone` 关闭 Phase 2，进入 Phase 3 写作
- 不满意 → 使用 `/clinpub-modify` 调整分析方法、变量、图表样式等
```

按用户反馈分支：
- 选择「满意」→ 继续 `milestone` 步骤
- 选择「不满意」→ 引导用户调用 `/clinpub-modify`；修改完成后回到 `verify_outputs` 复检
</step>

<step name="milestone" priority="high">
Execute the milestone workflow to formally close Phase 2 and gate into Phase 3:

```bash
# The milestone workflow will:
# 1. Verify success criteria for Phase 2
# 2. Collect analysis decisions (method selection, parameters)
# 3. Generate .clinpub/phases/02-analysis/MILESTONE.md
# 4. Update ROADMAP.md: Phase 2 → ✅ Complete, Phase 3 → 🔄 In Progress
# 5. Update STATE.md: current_phase → 3
# 6. Request user sign-off
```

See @./pipeline/workflows/milestone.md for full protocol.

<output name="signoff_prompt" format="user_facing">
────────────────────────────────
✅ Phase 2 核验完成

请确认：输入 "approved" 进入 Phase 3（论文写作），或描述需要调整的地方。
────────────────────────────────
</output>
</step>

</process>

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
- Shared figure config script (`_figure_config.R`) generated and sourced by all method R scripts
- Each confirmed method has complete figure + table + 方法说明
- All figures meet publication-grade standards (≥300 DPI, theme_pub)
- All method figures share consistent style (theme, color palette, DPI) via `_figure_config.R`
- Statistical reports complete with effect size + 95%CI + p-value
- Dependency-aware execution order respected (wave N+1 waits for wave N user confirmation)
- Code independently reproducible from cleaned.csv
- User briefed after each wave
</success_criteria>
