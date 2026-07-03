---
name: import-project
description: "Import mode: scan existing project artifacts, infer file roles, confirm mapping with user, gap analysis, adapt directory structure, set correct starting phase."
---

<purpose>
Allow clinpub to take over an existing clinical research project at any stage. Detect files, infer roles, confirm mapping with user, analyze gaps, migrate files to standard clinpub directory structure, and set the correct starting phase.
</purpose>

<required_reading>
@./pipeline/references/import-heuristics.md
@./pipeline/references/gates.md
@./pipeline/templates/import-milestone.md
@./pipeline/templates/project_config.yml
@./pipeline/templates/state.md
@./pipeline/templates/roadmap.md
@./pipeline/references/checkpoints.md
</required_reading>

<process>

<step name="detect_import_resume" priority="first">
Check for incomplete import from previous session:

1. Read `.clinpub/STATE.md`
2. If `import_mode: true` is present → previous import was interrupted
   - Prompt user: "检测到上次导入未完成。输入 `continue` 继续上次导入，或输入 `restart` 重新开始。"
   - `continue` → jump to `gap_analysis` step
   - `restart` → clear import_mode flag and proceed from `scan_artifacts`
3. If no STATE.md or no import_mode → fresh import, proceed to `scan_artifacts`
</step>

<step name="scan_artifacts" priority="first">
Scan the project root directory and first-level subdirectories for research artifacts.

**Scan scope**:
- Project root (cwd) and first-level subdirectories
- **Exclude**: `.clinpub/`, `.git/`, `.claude/`, `node_modules/`, `pipeline/`, `agents/`, `commands/`, `hooks/`, `scripts/`, `bin/`, `.qoder/`, `docs/`, `image/`

**Scan categories and file extensions**:

| Category | Extensions | Extra patterns |
|----------|-----------|----------------|
| Data files | .csv, .xlsx, .xls, .tsv, .sav, .dta, .rds, .rda | Check filename for "cleaned", "raw", "data" |
| Figure files | .png, .pdf, .tiff, .svg, .jpg, .jpeg | Exclude .clinpub/ images |
| Document files | .md, .docx, .doc, .tex, .bib, .ris | Read first 10 lines of .md to determine type |
| Code files | .R, .r, .Rmd, .py, .ipynb | Read first 20 lines to determine function |
| Config files | project_config.yml, MANIFEST.yaml | Direct recognition |

**Scan execution**:
1. Use Glob to find all matching files
2. For each file, record: path, size, extension, filename
3. For .md files: read first 10 lines to detect IMRAD section markers
4. For code files (.R/.py): read first 20 lines to detect function (cleaning/analysis/plotting)
5. For data files (.csv): if feasible, read header row to get column count and variable names

**Also check for standard clinpub directories**:
- Does `01_RawData/` exist?
- Does `02_PreprocessedData/data/cleaned.csv` exist?
- Does `03_AnalysisMethods/` have subdirectories?
- Does `04_Outputs/` have files?
- Does `05_Manuscript/sections/` have files?
- Does `Reference/` have a .bib file?

Store all findings for role inference in next step.
</step>

<step name="infer_roles" priority="first">
Apply heuristic rules from `@./pipeline/references/import-heuristics.md` to each scanned file.

**Inference priority** (high → low):
1. **Directory location** — files already in standard clinpub directories are assigned their role directly (confidence: `definite`)
2. **Filename pattern** — strong keyword matches in filename (confidence: `high`)
3. **Content sampling** — reading first N lines for additional signals (confidence: `medium`)
4. **Weak signals** — extension-only matches or ambiguous patterns (confidence: `low`)

**Conflict resolution**:
- Same file matches multiple roles → take highest confidence match
- Multiple files compete for same role → present all, let user choose
- Cannot infer role → mark as `unclassified`

**Role → target directory mapping**:

| Role | Target directory |
|------|-----------------|
| `raw_data` | `01_RawData/` |
| `cleaned_data` | `02_PreprocessedData/data/cleaned.csv` |
| `variable_dictionary` | `02_PreprocessedData/data/` |
| `data_quality_report` | `02_PreprocessedData/reports/` |
| `cleaning_code` | `02_PreprocessedData/` |
| `analysis_code` | `03_AnalysisMethods/{method_id}/` |
| `method_description` | `03_AnalysisMethods/{method_id}/方法说明.md` |
| `analysis_output_figure` | `04_Outputs/{method_id}/` |
| `analysis_output_table` | `04_Outputs/{method_id}/` |
| `reference_library` | `Reference/references.bib` |
| `citation_map` | `Reference/citation_map.md` |
| `manuscript_introduction` | `05_Manuscript/sections/01-introduction.md` |
| `manuscript_methods` | `05_Manuscript/sections/02-methods.md` |
| `manuscript_results` | `05_Manuscript/sections/03-results.md` |
| `manuscript_discussion` | `05_Manuscript/sections/04-discussion.md` |
| `manuscript_abstract` | `05_Manuscript/sections/00-abstract.md` |
| `manuscript_full` | `05_Manuscript/manuscript.md` |

**Special handling for method subdirectories**:
When multiple analysis output files are detected, attempt to group them by method type:
- Files with "baseline"/"table1"/"table 1" → `01_BaselineTable`
- Files with "survival"/"kaplan"/"km" → `02_SurvivalAnalysis`
- Files with "regression"/"logistic"/"cox" → `03_RegressionAnalysis`
- Files with "comparison"/"t-test"/"wilcox" → `04_GroupComparison`
- Other patterns → assign sequential method IDs (`NN_MethodName`)
- Files that cannot be grouped → present to user for manual assignment

Store inferred roles for presentation.
</step>

<step name="present_mapping" priority="high">
Present the inferred file mapping to user in a clear table format for confirmation/correction.

**Output format**:

```
═══════════════════════════════════════════════════════════════
  clinpub 导入扫描结果
═══════════════════════════════════════════════════════════════

  检测到 {{total_count}} 个研究文件，已自动推断角色：

  数据文件 ({{count}}):
  ─────────────────────────────────────────────────
  #  | 文件                    | 推断角色        | 置信度 | 目标位置
  1  | data/patients.csv       | 原始数据        | 🟡 中  | 01_RawData/
  2  | cleaned_final.csv       | 清洗后数据      | 🟢 高  | 02_PreprocessedData/data/cleaned.csv

  图表文件 ({{count}}):
  ─────────────────────────────────────────────────
  3  | results/table1.docx     | 基线表          | 🟢 高  | 04_Outputs/01_BaselineTable/
  4  | results/boxplot.png     | 分析图表        | 🟡 中  | 04_Outputs/??

  文档文件 ({{count}}):
  ─────────────────────────────────────────────────
  5  | draft_v2.docx           | 手稿(部分)      | 🟡 中  | 05_Manuscript/
  6  | references.bib          | 参考文献库      | 🟢 确定| Reference/

  代码文件 ({{count}}):
  ─────────────────────────────────────────────────
  7  | analysis.R              | 分析代码        | 🟡 中  | 03_AnalysisMethods/

  未分类文件 ({{count}}):
  ─────────────────────────────────────────────────
  8  | notes.txt               | ❓ 未分类       | 🔴 低  | (请指定)

  ─────────────────────────────────────────────────
  ⚠ 标记为 🟡/🔴 的项目建议确认。
  输入序号修正角色（如 "3:raw_data"），输入 "confirm" 全部接受。
═══════════════════════════════════════════════════════════════
```

**Confidence indicators**:
- 🟢 `确定` (definite) — directory location match, no confirmation needed
- 🟢 `高` (high) — strong filename match, default accept
- 🟡 `中` (medium) — multi-signal weighted, recommend confirmation
- 🔴 `低` (low) — weak signal or ambiguous, require user input

**User interaction**:
- User can correct any file's role by typing `#N:new_role`
- User can exclude a file by typing `#N:skip`
- User can accept all by typing `confirm`
- After corrections, re-present updated mapping until user confirms
</step>

<step name="gap_analysis" priority="high">
Analyze completeness of each Phase based on confirmed file mapping.

**Phase completeness checks**:

**Phase 0 (init)**:
- Required: `project_config.yml`, `.clinpub/` directory
- Detection: If missing, clinpub will generate during import (always created)

**Phase 1 (data-prep)**:
- Required: `cleaned.csv` (mapped file)
- Optional: raw data, variable dictionary, data quality report, cleaning code
- Logic:
  - `cleaned.csv` exists → PASS (core)
  - Data quality report missing → WARN: "数据质量报告缺失，建议在导入后补做"
  - Cleaning code missing → WARN: "清洗代码缺失，数据可复现性无法保证"
  - Variable dictionary missing → INFO: "无变量字典，将从数据自动推断"
  - Raw data missing → INFO: "无原始数据文件，跳过 Gate 2 中的可复现性检查"

**Phase 2 (analysis)**:
- For each inferred method group: check for figure + table + 方法说明
- Logic:
  - Figure/table exists but 方法说明 missing → WARN: "方法说明缺失，Gate 3 必需"
  - Analysis code exists → PASS
  - Analysis code missing → INFO: "分析代码缺失，已导入的图表仍可使用"
  - MANIFEST.yaml missing → INFO: "将在后续自动生成"

**Phase 3 (writing)**:
- Check for Introduction / Methods / Results / Discussion sections
- Logic:
  - All 4 sections present → PASS
  - Partial sections → mark existing sections, suggest continuation for missing
  - Reference library (.bib) exists → PASS
  - citation_map.md missing → WARN: "引用映射缺失，将在 Phase 3 生成"

**Phase 4 (review)**:
- Typically no existing artifacts; skip

**Starting Phase determination** (based on highest Phase with core artifacts):
- Has cleaned.csv (Phase 1 core) but no analysis outputs → suggest Phase 2
- Has analysis outputs (Phase 2 core) but no manuscript → suggest Phase 3
- Has manuscript sections (Phase 3 core) → suggest Phase 3 (续写) or Phase 4 (if complete)

**Present gap analysis report**:

```
═══════════════════════════════════════════════════════════════
  差距分析报告
═══════════════════════════════════════════════════════════════

  Phase 1 (数据准备):
  ─────────────────────────────────────────
  ✅ cleaned.csv — 已检测到 (cleaned_final.csv → 485行 × 32列)
  ❌ 数据质量报告 — 缺失
  ❌ 清洗代码 — 缺失
  ⚠️ 建议: 数据质量报告可在导入后补做

  Phase 2 (统计分析):
  ─────────────────────────────────────────
  ✅ 基线表 — 已检测到 (table1.docx)
  ✅ 箱线图 — 已检测到 (boxplot.png)
  ❌ 方法说明 — 全部缺失 (Gate 3 必需)
  ⚠️ 建议: 方法说明需在分析阶段补做

  ═══════════════════════════════════════════
  综合判断: 建议从 Phase 2 开始
  ═══════════════════════════════════════════

  选项:
  A: 从 Phase 2 开始（推荐）
  B: 从 Phase 3 开始
  C: 自定义起始 Phase

  请输入选择:
═══════════════════════════════════════════════════════════════
```

**User confirms starting phase**. Record as `starting_phase`.
</step>

<step name="discuss_framework_partial" priority="high">
Based on existing artifacts, auto-infer as much of the research framework as possible, then discuss only missing parts with user.

**Auto-inference from artifacts**:
- If `cleaned.csv` exists: run `python scripts/data_profiler.py {cleaned.csv_path} --output .clinpub/tmp/import_profile.json` to get variable list, types, missing patterns
- From profile: infer study type (using existing init-project.md auto-inference rules), outcome variable, covariates
- From figure/table filenames: infer analysis methods already performed
- From manuscript content (if exists): infer research title, study design, target journal
- From existing `project_config.yml` (if present): read and use all filled fields

**Discussion scope** (only ask what couldn't be auto-inferred):
1. **Study basics**: title, research type (if not inferred), objectives
2. **Variable roles**: outcome, exposure, covariates (confirm profiler output)
3. **Target journal**: name, tier, language
4. **IRB information** (MANDATORY — Gate 1 cannot be skipped):
   - IRB approval number
   - Data de-identification confirmation
   - Informed consent status
5. **Analysis methods**: confirm which methods correspond to imported outputs, identify additional methods needed

**If existing project_config.yml found**:
- Read all fields
- Only ask about empty/missing fields
- Preserve all user-filled values

Record all decisions for config generation.
</step>

<step name="create_adapted_structure" priority="high">
Create the standard clinpub directory structure and migrate imported files.

**Execution steps**:

1. **Set import_mode flag in STATE.md** (before any writes):
   Write a minimal STATE.md:
   ```markdown
   # STATE
   import_mode: true
   ```
   This tells workflow-guard.js to allow writes to all phase directories.

2. **Create standard directory structure** (only missing directories):
   ```
   .clinpub/phases/00-init/
   01_RawData/
   02_PreprocessedData/data/
   02_PreprocessedData/reports/
   03_AnalysisMethods/{method_id}/    ← for each confirmed method group
   04_Outputs/{method_id}/            ← for each confirmed method group
   Reference/
   05_Manuscript/sections/
   05_Manuscript/response_letters/
   ```

3. **Copy (never move) files to standard locations**:
   - Use the confirmed mapping from `present_mapping` step
   - Always copy, never move — preserve original files in place
   - Rename if needed to match clinpub conventions (e.g., `cleaned_final.csv` → `cleaned.csv`)
   - For .docx/.tex files: copy as-is, conversion happens in later phases

4. **Create placeholder 方法说明.md** for each method group:
   In each `03_AnalysisMethods/{method_id}/`, create `方法说明.md` from template with:
   - Method title filled in (inferred from file grouping)
   - Status marked as `⚠️ 导入项目 — 方法说明待补全`
   - All other sections as template stubs

5. **Handle special file conversions** (if needed):
   - `.xlsx` data file intended as `cleaned.csv` → inform user, offer to convert via Python:
     ```python
     import pandas as pd; df = pd.read_excel("source.xlsx"); df.to_csv("02_PreprocessedData/data/cleaned.csv", index=False)
     ```
   - `.ris` reference file → inform user, will be converted by reference-agent in Phase 3

6. **Clear import_mode flag** (after all writes complete):
   Update STATE.md to remove `import_mode: true`
</step>

<step name="generate_import_config" priority="high">
Generate project configuration and state files for the imported project.

**project_config.yml**:
- Generate from `@./pipeline/templates/project_config.yml` template
- Fill inferred values, mark unfilled fields as empty
- Add `import` section:
  ```yaml
  import:
    mode: true
    date: "{{today}}"
    source_description: "{{user_description}}"
    starting_phase: {{starting_phase}}
    skipped_phases: {{skipped_phases_list}}
    imported_files:
      - source: "{{original_path}}"
        target: "{{clinpub_path}}"
        role: "{{role}}"
    unverified_gates:
      - gate: {{gate_number}}
        reason: "{{reason}}"
        status: "imported_unverified"
  ```
- If existing `project_config.yml` found: merge — preserve user-filled values, fill empty fields, add import section

**STATE.md**:
- Generate from `@./pipeline/templates/state.md` template
- Set `phase_number` to `starting_phase`
- Set `phase_name` to corresponding name
- Set `current_step` to "import_complete"
- Add import metadata section:
  ```markdown
  ## 导入信息
  - 导入日期：{{today}}
  - 起始阶段：Phase {{starting_phase}}
  - 跳过阶段：{{skipped_phases}}
  - 已导入文件：{{imported_count}} 个
  - 未验证 Gate 项：{{unverified_count}} 个
  ```
- Ensure `import_mode: false` (cleared)

**ROADMAP.md**:
- Generate from `@./pipeline/templates/roadmap.md` template
- Mark skipped phases as `⏩ 已跳过（导入）`
- Mark starting phase as `🔄 In Progress`
- Mark phases before starting phase (if not skipped) as `✅ Complete`

**PROJECT.md**:
- Generate from `@./pipeline/templates/project.md` template with inferred values

**Decision log**:
- Write all import decisions to `.clinpub/phases/00-init/00-IMPORT-CONTEXT.md`:
  - Scan results and file mapping
  - User corrections
  - Gap analysis results
  - Chosen starting phase and rationale
  - IRB information provided
</step>

<step name="import_milestone" priority="high">
Generate import milestone to formally record the import and transition to normal workflow.

**Generate IMPORT-MILESTONE.md** at `.clinpub/phases/00-init/IMPORT-MILESTONE.md`:

Use template from `@./pipeline/templates/import-milestone.md` with:

1. **Import summary**: date, mode, starting phase
2. **Imported files table**: source → target → role → status
3. **Skipped phases gate status**:
   For each skipped phase, evaluate gate checks:
   - Items that can be verified on imported artifacts → `PASS`
   - Items that cannot be verified → `UNVERIFIED` with reason
   - Items that are verified and fail → `FAIL` (block import)
4. **Gap remediation plan**: list missing items with priority and suggested remediation
5. **User sign-off checklist**:
   - [ ] 我确认文件映射正确
   - [ ] 我了解跳过的 Gate 的风险
   - [ ] 我已提供 IRB/伦理信息（Gate 1 不可跳过）
   - [ ] 我同意从 Phase {{starting_phase}} 开始

**Present to user**:
```
────────────────────────────────
✅ 导入完成 — 请确认

已将 {{file_count}} 个文件导入 clinpub 项目结构。
起始阶段: Phase {{starting_phase}} — {{phase_name}}

⚠️ 未验证的 Gate 项 ({{unverified_count}}):
{{unverified_items_summary}}

请确认:
- 输入 "approved" 确认导入，开始 Phase {{starting_phase}}
- 或描述需要调整的地方
────────────────────────────────
```

**On user approval**:
1. Clear `import_mode` from STATE.md (ensure it's `false`)
2. Update STATE.md to starting phase
3. Record sign-off in IMPORT-MILESTONE.md

**On user requests changes**:
1. Address corrections
2. Re-present updated mapping
3. Re-run gap analysis if mapping changed significantly

</step>

</process>

<success_criteria>
- All scanned files have confirmed roles (no unclassified files remain, or user explicitly skipped them)
- Files copied to standard clinpub directory structure
- project_config.yml generated with import section
- STATE.md set to correct starting phase (import_mode cleared)
- ROADMAP.md shows skipped phases as `⏩ 已跳过`
- IMPORT-MILESTONE.md generated with gate status and remediation plan
- Gate 1 (IRB/Ethics) information provided — import blocked if not
- User has signed off on import mapping and starting phase
- Decision log written to 00-IMPORT-CONTEXT.md
</success_criteria>
