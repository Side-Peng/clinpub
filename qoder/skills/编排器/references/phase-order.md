# Phase 顺序与依赖关系

## Phase 总览

```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4
初始化     数据清洗    统计分析    论文写作    同行评审
```

## Phase 0：项目初始化
- **输入**: 用户的研究想法、原始数据文件（可选）
- **输出**: `project_config.yml`、`.clinpub/`（PROJECT.md, ROADMAP.md, STATE.md）、标准目录结构
- **前置条件**: 无
- **完成标志**: project_config.yml 存在且关键字段有效（project.name 非默认值, variables.outcome 非空, paths.raw_data 目录存在）
- **支持导入模式**: 检测到已有研究工件时自动进入

## Phase 1：数据清洗
- **输入**: `01_RawData/` 中的原始数据文件、`project_config.yml`
- **输出**: `02_PreprocessedData/data/cleaned.csv`、数据质量报告（HTML）
- **前置条件**: Phase 0 完成（project_config.yml 完整）
- **完成标志**: cleaned.csv 存在于 `02_PreprocessedData/data/`，reports/ 下有质量报告
- **支持重入**: 如果 project_config.yml 已存在，自动刷新 profile 和 spec

## Phase 2：统计分析
- **输入**: `cleaned.csv`、`project_config.yml`
- **输出**: `04_Outputs/` 下的图表文件、`03_AnalysisMethods/` 下的方法代码和说明
- **前置条件**: Phase 1 完成（cleaned.csv 存在）
- **完成标志**: 04_Outputs/ 非空，每个方法有 figure + table + 方法说明
- **Wave 结构**: 按依赖关系分为多个 Wave，Wave 1 → Wave 2 → ... → Wave N
  - Wave 1: 基线描述（无依赖）
  - Wave 2: 组间比较（依赖 Wave 1 的基线数据）
  - Wave 3: 多因素分析（依赖 Wave 2 的分组信息）
  - Wave 4+: 高级分析（依赖前序 Wave）
- **共享配置**: `_figure_config.R` 在 Phase 2 开始时生成，所有方法脚本必须 source 它

## Phase 3：论文写作
- **输入**: `04_Outputs/`（图表）、`03_AnalysisMethods/`（方法说明）、`Reference/`（文献）
- **输出**: `05_Manuscript/manuscript.md`、`05_Manuscript/sections/`（各段独立文件）
- **前置条件**: Phase 2 完成（04_Outputs/ 有输出）
- **完成标志**: manuscript.md 存在，包含完整 IMRAD 结构 + YAML frontmatter
- **写作模式**: 一键成稿（batch）或逐步写作（sequential）
- **引用管理**: 共享引用库 `Reference/reference_library.json`，占位符交叉引用

## Phase 4：同行评审
- **输入**: `05_Manuscript/manuscript.md`
- **输出**: `05_Manuscript/final/`（终稿）、响应函
- **前置条件**: Phase 3 完成（manuscript.md 存在）
- **完成标志**: final/ 下有修改后终稿 + 响应函

## 阶段间通信规则

1. **仅通过文件系统**: 阶段间通过文件传递数据，无直接消息
2. **无循环依赖**: 下游阶段读取上游输出，不反向
3. **单写者原则**: 每个输出目录只有一个作者代理
4. **共享读、独占写**: `project_config.yml` 所有代理可读，仅编排器可写
5. **MANIFEST 合约**: 每个阶段完成后写 `MANIFEST.yaml`，下游阶段验证后才消费

## 目录结构

```
Project_Root/
├── .clinpub/                  # Phase 0 — PROJECT.md / ROADMAP.md / STATE.md
├── 01_RawData/                # Phase 1 — 原始数据（只读）
├── 02_PreprocessedData/       # Phase 1 — cleaned.csv + 数据质量报告
├── 03_AnalysisMethods/        # Phase 2 — 方法代码 + 方法说明
├── 04_Outputs/                # Phase 2 — 图表 + MANIFEST.yaml
├── Reference/                 # Phase 3 — 文献（references.bib, citation_map.md）
├── 05_Manuscript/             # Phase 3-4 — IMRAD 草稿、审稿、终稿
└── project_config.yml         # Phase 0 — 中央配置
```

## MILESTONE.md 的作用

每个 Phase 推进到下一 Phase 时，必须生成 MILESTONE.md。它记录：
- 交付物清单
- 关键决策
- 产出文件列表
- 用户签字确认

MILESTONE.md 是阶段门控的前提条件，确保后续阶段可以正常访问文件。
