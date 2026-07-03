# Import Heuristics — File Role Inference Rules

> Reference document for `import-project.md` workflow. Defines heuristic rules for inferring the role of existing files when importing a project into clinpub.

---

## Inference Priority

Signals are evaluated in this order (highest weight first):

1. **Directory location** — file is already in a standard clinpub directory → confidence: `definite`
2. **Filename pattern** — strong keyword match in filename → confidence: `high`
3. **Content sampling** — reading first N lines reveals function → confidence: `medium`
4. **Extension only** — weak signal from file type alone → confidence: `low`

**Conflict resolution**:
- Same file matches multiple roles → take highest confidence match
- Multiple files compete for same role → present all candidates, let user choose
- Cannot infer role → mark as `unclassified`

---

## Data Files (.csv, .xlsx, .xls, .tsv, .sav, .dta, .rds, .rda)

### Role: `raw_data` → `01_RawData/`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `01_RawData/` | definite |
| Filename | Contains: `raw`, `original`, `原始`, `未处理`, `source`, `input` | high |
| Filename | Contains: `患者`, `patient`, `enrollment`, `入组` | medium |
| Extension | `.sav`, `.dta`, `.rda` (common raw data formats) | medium |
| Content | Has columns that look like patient IDs, timestamps | medium |
| Default | CSV/XLSX with >50 rows and no other strong signal | low |

### Role: `cleaned_data` → `02_PreprocessedData/data/cleaned.csv`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `02_PreprocessedData/data/` | definite |
| Filename | Contains: `cleaned`, `clean`, `final`, `清洗`, `处理后`, `processed`, `ready` | high |
| Filename | Contains: `analysis_ready`, `analytic`, `work_data` | high |
| Content | No columns with >30% missing values (suggests cleaning done) | medium |
| Filename | Exactly `cleaned.csv` | definite |

### Role: `variable_dictionary` → `02_PreprocessedData/data/`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Filename | Contains: `dictionary`, `codebook`, `data_dict`, `变量`, `字典`, `编码` | high |
| Content | Two-column structure: variable name + description | high |

### Role: `data_quality_report` → `02_PreprocessedData/reports/`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `02_PreprocessedData/reports/` | definite |
| Filename | Contains: `quality`, `质量`, `report`, `报告`, `profiling`, `summary` | medium |
| Content | Contains sections like "missing values", "outliers", "distributions" | high |

---

## Figure/Chart Files (.png, .pdf, .tiff, .svg, .jpg, .jpeg)

### Role: `analysis_output_figure` → `04_Outputs/{method_id}/`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `04_Outputs/` or its subdirectories | definite |
| Filename | Contains: `fig`, `figure`, `plot`, `chart`, `图`, `曲线` | high |
| Filename | Contains: `survival`, `kaplan`, `km`, `生存` → method: SurvivalAnalysis | high |
| Filename | Contains: `boxplot`, `violin`, `箱线` → method: GroupComparison | medium |
| Filename | Contains: `forest`, `森林图` → method: RegressionAnalysis | medium |
| Filename | Contains: `heatmap`, `热图`, `correlation`, `相关` → method: CorrelationAnalysis | medium |
| Filename | Contains: `roc`, `auc` → method: ROCAnalysis | medium |
| Filename | Contains: `scatter`, `散点` → method: RegressionAnalysis | medium |
| Directory | Located in `results/`, `output/`, `figures/` | medium |
| Extension | `.tiff`, `.svg` (publication formats) | low |

### Role: `analysis_output_table` → `04_Outputs/{method_id}/`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `04_Outputs/` subdirectory | definite |
| Filename | Contains: `table`, `表`, `tab` | high |
| Filename | Contains: `table1`, `table 1`, `baseline`, `基线`, `demographics` → method: BaselineTable | high |
| Extension | `.docx`, `.xlsx` with "table"/"表" in name | medium |

### Role: `manuscript_figure` → `05_Manuscript/`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `05_Manuscript/` or subdirectories | definite |
| Filename | Contains: `fig1`, `fig2`, `figure1` (numbered manuscript figures) | medium |

---

## Document Files (.md, .docx, .doc, .tex, .bib, .ris)

### Role: `manuscript_introduction` → `05_Manuscript/sections/01-introduction.md`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `05_Manuscript/sections/` | definite |
| Filename | Contains: `intro`, `introduction`, `引言`, `前言`, `背景` | high |
| Content | First paragraph cites multiple references, discusses disease burden | high |
| Content | Has subsection headings like "Background", "Rationale" | medium |

### Role: `manuscript_methods` → `05_Manuscript/sections/02-methods.md`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `05_Manuscript/sections/` | definite |
| Filename | Contains: `method`, `methods`, `方法`, `材料`, `材料与方法` | high |
| Content | Describes study design, participants, statistical methods | high |

### Role: `manuscript_results` → `05_Manuscript/sections/03-results.md`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `05_Manuscript/sections/` | definite |
| Filename | Contains: `result`, `results`, `结果`, `发现` | high |
| Content | Contains statistical values (p=, CI=, HR=, OR=) and figure references | high |

### Role: `manuscript_discussion` → `05_Manuscript/sections/04-discussion.md`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `05_Manuscript/sections/` | definite |
| Filename | Contains: `discussion`, `讨论`, `conclusion`, `结论` | high |
| Content | Compares with other studies, discusses limitations and implications | high |

### Role: `manuscript_abstract` → `05_Manuscript/sections/00-abstract.md`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Filename | Contains: `abstract`, `摘要` | high |
| Content | Short text (<500 words) with Background/Methods/Results/Conclusion structure | high |

### Role: `manuscript_full` → `05_Manuscript/manuscript.md`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Filename | Contains: `manuscript`, `full`, `complete`, `手稿`, `全文`, `终稿` | high |
| Content | Contains multiple IMRAD sections in one file | high |

### Role: `reference_library` → `Reference/references.bib`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Extension | `.bib` | definite |
| Directory | Located in `Reference/` | definite |
| Extension | `.ris` | high (note: needs conversion to .bib) |
| Filename | Contains: `references`, `bibliography`, `引用`, `文献` | high |

### Role: `citation_map` → `Reference/citation_map.md`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Filename | Contains: `citation_map`, `citation`, `引用映射` | high |
| Content | Table with PMID, DOI, citation reason columns | high |

### Role: `method_description` → `03_AnalysisMethods/{method_id}/方法说明.md`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `03_AnalysisMethods/` subdirectory | definite |
| Filename | Contains: `方法说明`, `method_readme`, `方法描述` | high |

---

## Code Files (.R, .r, .Rmd, .py, .ipynb)

### Role: `cleaning_code` → `02_PreprocessedData/`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `02_PreprocessedData/` | definite |
| Content | Contains `read.csv`/`readxl`/`read_excel` + data manipulation (filter, mutate, na.omit, fillna) | high |
| Filename | Contains: `clean`, `preprocess`, `prepare`, `清洗`, `预处理` | high |

### Role: `analysis_code` → `03_AnalysisMethods/{method_id}/`

| Signal type | Pattern | Confidence |
|------------|---------|------------|
| Directory | Located in `03_AnalysisMethods/` subdirectory | definite |
| Content | Contains statistical functions: `lm(`, `glm(`, `coxph(`, `t.test(`, `wilcox.test(`, `survfit(` | high |
| Content | Contains plotting: `ggplot(`, `plot(`, `ggsave(`, `plt.plot(`, `plt.savefig(` | medium |
| Filename | Contains: `analysis`, `stat`, `model`, `分析`, `统计` | medium |

---

## Method Grouping Rules

When multiple analysis output files are detected, group them by method:

| Filename pattern | Method ID | Method name |
|-----------------|-----------|-------------|
| `table1`, `baseline`, `demographics`, `基线` | `01_BaselineTable` | 基线特征表 |
| `survival`, `kaplan`, `km_curve`, `生存` | `02_SurvivalAnalysis` | 生存分析 |
| `regression`, `logistic`, `cox`, `回归` | `03_RegressionAnalysis` | 回归分析 |
| `comparison`, `t_test`, `wilcox`, `组间`, `比较` | `04_GroupComparison` | 组间比较 |
| `correlation`, `heatmap`, `相关`, `热图` | `05_CorrelationAnalysis` | 相关分析 |
| `roc`, `auc`, `diagnostic`, `诊断` | `06_ROCAnalysis` | ROC分析 |
| `subgroup`, `forest`, `亚组`, `森林` | `07_SubgroupAnalysis` | 亚组分析 |
| `sensitivity`, `敏感性` | `08_SensitivityAnalysis` | 敏感性分析 |
| `ml`, `machine_learning`, `random_forest`, `机器学习` | `09_MLAnalysis` | 机器学习分析 |
| Other/unmatched | `NN_CustomMethod{N}` | 用户自定义方法 |

**Grouping logic**:
1. Check filename against patterns above
2. If match found, assign to corresponding method group
3. Files in same directory with similar names → same method group
4. Unmatched files → present to user for manual grouping
5. User can rename/reassign during `present_mapping` step

---

## Confidence Level Summary

| Level | Icon | Meaning | Action |
|-------|------|---------|--------|
| Definite | 🟢 | Directory location match | Auto-accept, no confirmation |
| High | 🟢 | Strong filename/content match | Present, default accept |
| Medium | 🟡 | Multi-signal weighted | Present, recommend confirmation |
| Low | 🔴 | Weak or ambiguous signal | Present, require user input |

---

## Edge Cases

1. **File is a symlink or shortcut**: resolve to actual path before scanning
2. **Duplicate files** (same content, different names): detect by size + first 5 rows comparison; flag for user
3. **Very large files** (>100MB): skip content sampling, rely on filename/directory only
4. **Password-protected files**: flag as `inaccessible`, ask user to provide access
5. **Non-standard encodings** (GB2312, Shift-JIS): detect encoding, note in import log
6. **Mixed language filenames** (e.g., `最终版_改改改_v3.csv`): strip version suffix, match against core name
