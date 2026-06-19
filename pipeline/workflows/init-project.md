---
name: init-project
description: "Phase 0 orchestration: Detect import mode or discuss research framework with user, infer study type if needed, generate project directory structure and project_config.yml. Supports importing existing projects at any stage."
---

<purpose>
Initialize a clinical research project by discussing the study framework with the user, creating the project directory structure, and generating project configuration.
</purpose>

<required_reading>
@./pipeline/templates/project_config.yml
@./pipeline/templates/project.md
@./pipeline/templates/roadmap.md
@./pipeline/templates/state.md
@./pipeline/templates/method-readme.md
@./pipeline/references/checkpoints.md
@./pipeline/references/r_patterns.md
@./pipeline/workflows/import-project.md
@./pipeline/references/import-heuristics.md
@./pipeline/templates/import-milestone.md
</required_reading>

<process>

<step name="detect_import_mode" priority="first">
Before starting standard initialization, scan the project directory to determine if this is an import scenario.

**Scan rules**:
1. Use Glob to scan the project root and first-level subdirectories for research files:
   - **Strong-signal files** (data + code): *.csv, *.xlsx, *.xls, *.tsv, *.sav, *.dta, *.rds, *.rda, *.R, *.r, *.py, *.Rmd
   - **Weak-signal files** (figures + docs): *.png, *.pdf, *.tiff, *.svg, *.md, *.docx, *.tex, *.bib
2. Exclude from scan: `.clinpub/`, `.git/`, `.claude/`, `node_modules/`, `pipeline/`, `agents/`, `commands/`, `hooks/`, `scripts/`, `bin/`, `.qoder/`, `docs/`, `image/`
3. Check if standard clinpub directories already exist (01_RawData, 02_PreprocessedData, 03_AnalysisMethods, 04_Outputs, 05_Manuscript)
4. Check if `project_config.yml` already exists

**Decision logic** (signal-strength model):
- ≥1 standard clinpub directory → **import mode detected** (strong signal, structural evidence)
- ≥2 strong-signal files → **import mode detected** (data/code presence is unambiguous)
- ≥5 weak-signal files (without strong-signal files) → **import mode candidate** (ambiguous, requires user confirmation)
- Otherwise → standard new project mode

**IF import mode detected** (clinpub directory or strong-signal): **Before executing import workflow**, present confirmation to user:

```
检测到项目中已有研究文件：
- 数据文件: {{data_count}} 个 ({{data_examples}})
- 代码文件: {{code_count}} 个 ({{code_examples}})
- 图表文件: {{figure_count}} 个
- 文档文件: {{doc_count}} 个

是否以导入模式启动？
- 输入 `yes` 或 `导入` → 进入导入模式
- 输入 `no` 或 `新建` → 以全新项目模式启动
```

On user confirmation → Execute `@./pipeline/workflows/import-project.md` instead of the steps below.
On user rejection → Continue with standard initialization below.

**IF import mode candidate** (weak-signal only): Prompt user with the same confirmation but note that signal is ambiguous. Only enter import mode if user explicitly confirms.

**IF no artifacts found**: Continue with the standard initialization steps below.
</step>

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
After discussion, create the project directory structure.

**Important**: `03_AnalysisMethods/` and `04_Outputs/` must contain one subdirectory per user-confirmed method.
Method IDs follow the pattern `{NN}_{MethodName}` (e.g., `01_BaselineTable`, `02_GroupComparison`),
matching the `methods_to_run` list in `project_config.yml`.

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
├── 03_AnalysisMethods/         ← one subdirectory per confirmed method
│   ├── 01_BaselineTable/
│   │   └── 方法说明.md          ← placeholder from method-readme.md template
│   ├── 02_GroupComparison/
│   │   └── 方法说明.md
│   └── ...                     ← additional confirmed methods
├── 04_Outputs/                 ← one subdirectory per confirmed method
│   ├── 01_BaselineTable/
│   ├── 02_GroupComparison/
│   └── ...                     ← additional confirmed methods
├── Reference/                  ← literature
├── 05_Manuscript/             ← chapter drafts
│   └── response_letters/
└── project_config.yml          ← configuration
```

**Per-method subdirectory rules:**

1. For each method in `methods_to_run` (confirmed by user in step 1), create:
   - `03_AnalysisMethods/{method_id}/` — will hold R/Python code and `方法说明.md`
   - `04_Outputs/{method_id}/` — will hold figures and tables
2. In each `03_AnalysisMethods/{method_id}/`, create a placeholder `方法说明.md` using the template from `pipeline/templates/method-readme.md`. The placeholder should have the method title filled in (e.g., `# 基线特征表 — 方法说明`) and all other sections left as template stubs (to be filled by Phase 2).
3. `04_Outputs/{method_id}/` directories are created empty — outputs are generated in Phase 2.
4. If the user has not yet confirmed specific methods at this point, defer subdirectory creation until methods are confirmed (but they must exist before Phase 0 milestone closes).
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

<output name="signoff_prompt" format="user_facing">
────────────────────────────────
✅ Phase 0 核验完成

请确认：输入 "approved" 进入 Phase 1（数据准备），或描述需要调整的地方。
────────────────────────────────
</output>
</step>

</process>

<success_criteria>
- Study framework fully discussed and documented
- Project directory structure created with .clinpub/ layer
- project_config.yml reflects all user decisions
- Each user-confirmed method has `03_AnalysisMethods/{method_id}/` and `04_Outputs/{method_id}/` subdirectories
- Each `03_AnalysisMethods/{method_id}/` contains a placeholder `方法说明.md` from template
- Decision log written to 00-CONTEXT.md
</success_criteria>
