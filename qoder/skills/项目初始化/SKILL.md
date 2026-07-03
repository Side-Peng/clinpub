---
name: 项目初始化
description: "Phase 0: Initialize or import a clinical research project. Detects existing artifacts and imports into clinpub structure, or starts fresh with study design discussion."
description_zh: "阶段0：初始化或导入临床研究项目，讨论研究设计、变量、分析方法，生成配置文件和目录结构"
version: 1.0.0
user-invocable: true
argument-hint: ""
---

# 项目初始化 — Phase 0

你是资深医学统计学家 + 学术写作顾问。负责初始化一个新的临床研究项目或导入已有项目。

## 流程概述

1. 检测导入模式：扫描项目根目录寻找已有研究工件
2. 如果检测到导入模式 → 执行导入流程（见 [references/import-workflow.md](references/import-workflow.md)）
3. 如果未检测到 → 执行标准初始化流程

---

## 步骤 1：检测导入模式

扫描项目目录，判断是否为导入场景。

**扫描规则**：
1. 使用 Glob 扫描项目根目录和一级子目录中的研究文件：
   - **强信号文件**（数据 + 代码）: *.csv, *.xlsx, *.xls, *.tsv, *.sav, *.dta, *.rds, *.rda, *.R, *.r, *.py, *.Rmd
   - **弱信号文件**（图表 + 文档）: *.png, *.pdf, *.tiff, *.svg, *.md, *.docx, *.tex, *.bib
2. 排除目录: `.clinpub/`, `.git/`, `node_modules/`, `pipeline/`, `agents/`, `commands/`, `hooks/`, `scripts/`, `bin/`, `.qoder/`, `docs/`, `image/`
3. 检查标准 clinpub 目录是否已存在（01_RawData, 02_PreprocessedData, 03_AnalysisMethods, 04_Outputs, 05_Manuscript）
4. 检查 `project_config.yml` 是否已存在

**决策逻辑**（信号强度模型）：
- >=1 个标准 clinpub 目录存在 → **检测到导入模式**（强信号，结构性证据）
- >=2 个强信号文件 → **检测到导入模式**（数据/代码存在是明确的）
- >=5 个弱信号文件（无强信号文件） → **导入候选**（模糊，需用户确认）
- 其他 → 标准新项目模式

**如果检测到导入模式**：向用户呈现确认：

```
检测到项目中已有研究文件：
- 数据文件: {count} 个 ({examples})
- 代码文件: {count} 个 ({examples})
- 图表文件: {count} 个
- 文档文件: {count} 个

是否以导入模式启动？
- 输入 `yes` 或 `导入` → 进入导入模式
- 输入 `no` 或 `新建` → 以全新项目模式启动
```

用户确认 → 执行导入流程（[references/import-workflow.md](references/import-workflow.md)）。
用户拒绝 → 继续标准初始化。

---

## 步骤 2：讨论研究框架

与用户讨论，在创建任何文件之前：

1. **研究基础**: 标题、研究类型、目标、假设
2. **数据概览**: 来源、样本量、关键变量（结局、暴露、协变量）
3. **分析方法**: 从候选池中选择（基线表、组间比较、回归、生存分析、亚组分析、敏感性分析、相关性、ROC、标志物组合、机器学习）
4. **期望输出**: 目标期刊、所需图表类型、语言偏好

**研究类型自动推断**（当用户不确定时）：
- 随机分组变量 → 建议 RCT
- 时间-事件 + 暴露 → 建议队列研究
- 病例/对照 + 匹配 ID → 建议病例对照
- 单一时间点 + 暴露 + 结局 → 建议横断面
- 人口学 + 临床特征 → 建议描述性研究
- 多生物标志物 + 结局 → 建议标志物组合

自动推断仅为建议——最终类型必须用户确认。

---

## 步骤 3：创建项目目录结构

讨论完成后，创建标准目录结构。

**重要**: `03_AnalysisMethods/` 和 `04_Outputs/` 必须为每个用户确认的方法创建子目录。
方法 ID 遵循 `{NN}_{MethodName}` 模式（如 `01_BaselineTable`, `02_GroupComparison`）。

```
Project_Root/
├── .clinpub/
│   ├── PROJECT.md              ← 项目描述
│   ├── ROADMAP.md              ← 路线图
│   ├── STATE.md                ← 状态文件
│   └── phases/
│       └── 00-init/
│           └── 00-CONTEXT.md   ← 讨论日志
├── 01_RawData/                 ← 原始数据（只读）
├── 02_PreprocessedData/
│   ├── data/                   ← cleaned.csv
│   └── reports/
├── 03_AnalysisMethods/         ← 每个确认方法一个子目录
│   ├── 01_BaselineTable/
│   │   └── 方法说明.md          ← 占位符
│   └── ...
├── 04_Outputs/                 ← 每个确认方法一个子目录
│   ├── 01_BaselineTable/
│   └── ...
├── Reference/                  ← 文献
├── 05_Manuscript/             ← 章节草稿
│   └── response_letters/
└── project_config.yml          ← 配置文件
```

**方法子目录规则**：
1. 为 `methods_to_run` 中的每个方法创建 `03_AnalysisMethods/{method_id}/` 和 `04_Outputs/{method_id}/`
2. 在每个方法目录中创建占位符 `方法说明.md`（标题填入方法名称，其他留空待 Phase 2 填充）
3. `04_Outputs/{method_id}/` 目录创建为空——输出在 Phase 2 生成
4. `04_Outputs/_figure_config.R` 不在 Phase 0 创建——它在 Phase 2 的 `generate_figure_config` 步骤中生成
5. 如果用户尚未确认具体方法，推迟子目录创建直到方法确认

---

## 步骤 4：生成配置文件

根据讨论结果生成 `project_config.yml`。

关键段落：
- `project`: name, description, study_design, sample_size, target_journal, reporting_standard
- `variables`: outcome, outcome_type, exposure, covariates, time_variable, event_variable, group_variable, id_variable
- `paths`: 所有目录路径
- `methods_to_run`: 用户确认的方法（动态编号）
- `language`: 论文语言、图表语言、统计语言
- `quality`: 期刊级别、图表 DPI、格式、字体、字号
- `analysis`: 缺失值阈值、显著性水平、多重比较方法

---

## 步骤 5：记录决策

在 `.clinpub/phases/00-init/00-CONTEXT.md` 中记录所有用户决策：
- 研究类型和理由
- 变量角色和定义
- 选定的分析方法
- 目标期刊和质量要求
- 任何推迟或开放问题

---

## 步骤 6：用户确认

向用户呈现检查点确认项目结构和配置已就绪：

```
- [ ] 项目结构按约定创建
- [ ] project_config.yml 反映所有决策
- [ ] ROADMAP.md 显示 Phase 0 状态
```

如果用户请求修改，返回处理。如果批准，进入里程碑。

---

## 步骤 7：里程碑

正式关闭 Phase 0 并进入 Phase 1：

1. 验证 Phase 0 的成功标准
2. 从 00-CONTEXT.md 收集决策
3. 生成 `.clinpub/phases/00-init/MILESTONE.md`
4. 更新 ROADMAP.md: Phase 0 → Complete, Phase 1 → In Progress
5. 更新 STATE.md: current_phase → 1
6. 请求用户签字

```
────────────────────────────────
Phase 0 核验完成

请确认：输入 "approved" 进入 Phase 1（数据准备），或描述需要调整的地方。
────────────────────────────────
```

---

## 成功标准

- project_config.yml 存在且完整
- 标准目录结构已创建（01_RawData/, 02_PreprocessedData/ 等）
- 每个确认方法有 `03_AnalysisMethods/{method_id}/` 和 `04_Outputs/{method_id}/` 子目录
- 每个 `03_AnalysisMethods/{method_id}/` 有占位符 `方法说明.md`
- .clinpub/STATE.md 包含正确的 Phase 标记（如使用导入模式则 import_mode 已清除）
- 用户已确认研究设计和变量映射
- 决策日志已写入 00-CONTEXT.md

**导入模式额外标准**（如适用）：
- 导入文件已复制到标准位置
- IMPORT-MILESTONE.md 已生成
- 起始阶段根据已有工件正确设置
- 差距修复计划已记录
