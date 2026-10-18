---
name: data-prep
description: "阶段1：数据准备与探索性分析。清洗原始数据、处理缺失值、检测异常值、创建衍生变量、生成数据质量报告，产出 cleaned.csv。"
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
阶段1: Data preparation. Transform raw data into analysis-ready cleaned.csv with full data quality documentation.

Handles: missing value imputation, outlier detection, derived variable creation, encoding, train/validation split.
Supports re-entry: if project_config.yml exists with valid fields, auto-refreshes profiles and specs before entering discussion.
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/data-prep.md"`
</execution_context>

<process>
## 重新进入检测（D-05/D-07）

执行工作流之前，检查项目是否已初始化：

1. 检查 `project_config.yml` 是否存在于项目根目录
2. 如果存在，验证关键字段是否有效：
   - `project.name` 非空（不是默认值 "项目名称"）
   - `variables.outcome` 非空，**或** `analysis_mode: exploratory`（探索性研究允许结局未定）
   - `paths.raw_data` 对应的目录存在且有数据文件
3. **如果所有检查通过** -> 输出 "检测到已有项目配置（project_config.yml），执行自动刷新流程..."，然后执行下面的 step `reinit_data_prep`（D-06 全链路刷新）
4. **如果任何检查不通过** -> 输出 "未检测到完整项目配置，进入全新数据清洗流程"，然后进入正常的 data-prep 工作流
5. 注意：不添加任何 PreToolUse hook 逻辑（D-07），所有检测在命令层面完成

Execute the data-prep workflow from pipeline/workflows/data-prep.md end-to-end.
</process>

<success_criteria>
- cleaned.csv exists at 02_PreprocessedData/data/
- Data quality report generated (HTML)
- Missing values handled per tiered strategy
- Outliers documented
- Derived variables created and encoded
- Cleaning code independently reproducible
</success_criteria>
