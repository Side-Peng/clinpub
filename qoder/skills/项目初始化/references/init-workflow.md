# 标准初始化工作流

## 目的

初始化一个全新的临床研究项目：讨论研究框架、创建目录结构、生成配置文件。

## 前置阅读

- `../知识库/references/templates/project_config.yml` — 配置文件模板
- `../知识库/references/templates/project.md` — PROJECT.md 模板
- `../知识库/references/templates/roadmap.md` — ROADMAP.md 模板
- `../知识库/references/templates/state.md` — STATE.md 模板
- `../知识库/references/templates/method-readme.md` — 方法说明模板
- `../知识库/references/checkpoints.md` — 检查点规范
- `../知识库/references/r_patterns.md` — R 代码模式

## 步骤详解

### 1. 讨论研究框架

与用户讨论以下内容（在创建任何文件之前）：

1. **研究基础**: 标题、研究类型、目标、假设
2. **数据概览**: 来源、样本量、关键变量（结局、暴露、协变量）
3. **分析方法**: 从候选池中选择
   - 基线特征表、组间比较、回归分析、生存分析
   - 亚组分析、敏感性分析、相关性分析、ROC 分析
   - 标志物组合、机器学习
4. **期望输出**: 目标期刊、所需图表类型、语言偏好

**研究类型自动推断**（当用户不确定时）：

| 数据特征 | 建议类型 |
|---------|---------|
| 随机分组变量 | RCT |
| 时间-事件 + 暴露 | 队列研究 |
| 病例/对照 + 匹配 ID | 病例对照 |
| 单一时间点 + 暴露 + 结局 | 横断面 |
| 人口学 + 临床特征 | 描述性研究 |
| 多生物标志物 + 结局 | 标志物组合 |

自动推断仅为建议——最终类型必须用户确认。

### 2. 创建项目目录结构

讨论完成后创建标准目录结构。

**重要**: `03_AnalysisMethods/` 和 `04_Outputs/` 必须为每个用户确认的方法创建子目录。

```
Project_Root/
├── .clinpub/
│   ├── PROJECT.md              ← 从 project.md 模板
│   ├── ROADMAP.md              ← 从 roadmap.md 模板
│   ├── STATE.md                ← 从 state.md 模板
│   └── phases/
│       └── 00-init/
│           └── 00-CONTEXT.md   ← 讨论日志
├── 01_RawData/                 ← 原始数据（只读）
├── 02_PreprocessedData/
│   ├── data/                   ← cleaned.csv
│   └── reports/
├── 03_AnalysisMethods/         ← 每个方法一个子目录
│   ├── 01_BaselineTable/
│   │   └── 方法说明.md          ← 占位符
│   ├── 02_GroupComparison/
│   │   └── 方法说明.md
│   └── ...
├── 04_Outputs/                 ← 每个方法一个子目录
│   ├── 01_BaselineTable/
│   ├── 02_GroupComparison/
│   └── ...
├── Reference/                  ← 文献
├── 05_Manuscript/             ← 章节草稿
│   └── response_letters/
└── project_config.yml          ← 配置
```

**方法子目录规则**:
1. 为每个确认的方法创建 `03_AnalysisMethods/{method_id}/` 和 `04_Outputs/{method_id}/`
2. 每个 `03_AnalysisMethods/{method_id}/` 中创建占位符 `方法说明.md`
3. `04_Outputs/{method_id}/` 创建为空
4. `_figure_config.R` 不在 Phase 0 创建

### 3. 生成配置文件

根据讨论结果生成 `project_config.yml`：

```yaml
project:
  name: "{study_title}"
  description: "{study_description}"
  design: "{study_type}"
  sample_size: {N}
  target_journal: "{journal}"
  reporting_standard: "STROBE"  # or CONSORT, CARE, etc.

variables:
  outcome: "{outcome_var}"
  outcome_type: "{type}"  # binary, continuous, survival
  exposure: "{exposure_var}"
  covariates:
    - "{cov1}"
    - "{cov2}"
  time_variable: "{time_var}"
  event_variable: "{event_var}"
  group_variable: "{group_var}"
  id_variable: "{id_var}"

paths:
  raw_data: "01_RawData"
  preprocessed_data: "02_PreprocessedData"
  analysis_methods: "03_AnalysisMethods"
  outputs: "04_Outputs"
  reference: "Reference"
  manuscript: "05_Manuscript"

methods_to_run:
  - id: "01_BaselineTable"
    name: "基线特征表"
  - id: "02_GroupComparison"
    name: "组间比较"
  # ... 动态添加

language:
  manuscript: "zh-CN"
  figures_tables: "en"
  statistics: "en"

quality:
  journal_level: "Q1"
  figure_dpi: 300
  figure_format: "png"
  font: "Arial"
  font_size: 11

analysis:
  missing_threshold:
    delete: 0.05
    impute: 0.20
  significance_level: 0.05
  multiple_comparison: "fdr"
```

### 4. 记录决策

在 `.clinpub/phases/00-init/00-CONTEXT.md` 中记录：
- 研究类型和理由
- 变量角色和定义
- 选定的分析方法
- 目标期刊和质量要求
- 推迟或开放问题

### 5. 检查点确认

```
- [ ] 项目结构按约定创建
- [ ] project_config.yml 反映所有决策
- [ ] ROADMAP.md 显示 Phase 0 状态
```

### 6. 里程碑

生成 `.clinpub/phases/00-init/MILESTONE.md`，更新 ROADMAP.md 和 STATE.md。

## 成功标准

- 研究框架充分讨论并记录
- 项目目录结构已创建（含 .clinpub/ 层）
- project_config.yml 反映所有用户决策
- 每个确认方法有方法目录和输出目录
- 每个方法目录有占位符方法说明
- 决策日志已写入 00-CONTEXT.md
