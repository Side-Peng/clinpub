# 统计分析工作流详解

## 目的

自适应确定和执行最优分析方案。不同于固定菜单，分析方案按项目动态构建：读取数据、检测特征、从参考库提出适当方法、与用户讨论、按计算的依赖顺序执行。

## 前置阅读

- `../知识库/references/analysis_methods.md` — 分析方法参考（决策树 + 场景库）
- `../知识库/references/r_patterns.md` — R 代码模式（theme_pub, KM 曲线, 热力图）
- `../知识库/references/checkpoints.md` — 检查点规范
- `../知识库/references/comparison-methods.md` — 组间比较决策树

## 数据诊断详解

### 加载数据

```bash
PROJECT_DIR=$(pwd)
DATA="$PROJECT_DIR/02_PreprocessedData/data/cleaned.csv"
FULL_DATA="$PROJECT_DIR/02_PreprocessedData/data/full_longitudinal.csv"
CONFIG="$PROJECT_DIR/project_config.yml"
```

### 诊断矩阵

| 特征 | 检测方法 | 影响 |
|------|---------|------|
| 分组结构 | 分类变量唯一值计数 | 决定组间比较方法 |
| 时间点 | 患者 ID 重复出现 | 纵向 → 混合模型 |
| 结局类型 | 唯一值数量 + 分布 | 回归类型选择 |
| 协变量 | 变量字典分析 | 调整变量集 |
| 缺失模式 | 缺失率矩阵 | 插补策略 |
| 暴露变量 | project_config.yml | 主效应变量 |

### 结局类型决策

```
唯一值 = 2 → binary → logistic regression
唯一值 3-20 → categorical 或 continuous → 检查分布
唯一值 >20 → continuous → 检查正态性
有 time + event 列 → survival → Cox/生存分析
```

## 分析方案决策树

### Wave 组织原则

- **Wave 1**: 基线描述（无依赖，总是第一个执行）
- **Wave 2**: 组间比较（依赖 Wave 1 的基线数据）
- **Wave 3**: 多因素分析（依赖 Wave 2 确定的重要变量）
- **Wave 4+**: 高级分析（亚组、敏感性、ML 等）

Wave 数量由数据决定，不固定。

### 方法类型匹配

根据数据特征从 `analysis_methods.md` 决策树匹配：

| 数据特征 | 推荐方法 |
|---------|---------|
| 任意数据 | 基线特征表 (Wave 1) |
| 2 组 + 连续结局 | t 检验 / Wilcoxon |
| 3+ 组 + 连续结局 | ANOVA / Kruskal-Wallis |
| 纵向数据 | 重复测量混合模型 |
| 二分类结局 + 协变量 | Logistic 回归 |
| 连续结局 + 协变量 | 线性回归 |
| 生存数据 | Kaplan-Meier + Cox |
| 多变量相关性 | 相关矩阵 + 热力图 |
| 诊断/预测 | ROC 分析 |
| 高维 + 预测 | LASSO/弹性网 |

### 方案示例（纵向 RCT 数据）

```yaml
waves:
  1:
    label: "基线描述"
    methods:
      - id: "01_BaselineTable"
        type: baseline
        data: "cleaned.csv"
        timepoint: "baseline"
  2:
    label: "组间比较与纵向分析"
    methods:
      - id: "02_TwoGroupComparison"
        type: comparison
        method: "wilcox.test"
        outcomes: ["outcome_1", "outcome_2"]
      - id: "03_RepeatedMeasures"
        type: longitudinal
        data: "full_longitudinal.csv"
        method: "lme4::lmer()"
        formula: "outcome ~ group * time + (1 | id)"
  3:
    label: "多因素分析"
    methods:
      - id: "04_LinearRegression"
        type: regression
        formula: "outcome ~ group + age + sex + BMI"
```

## 图表配置生成

### _figure_config.R 模板

从 `../知识库/references/templates/_figure_config.R` 复制到 `04_Outputs/_figure_config.R`。

提供的核心函数：
- `apply_theme()` — 应用用户定制的主题参数
- `get_palette(n)` — 获取 n 色的调色板
- `get_continuous_scale()` — 获取连续变量色标
- `save_figure()` — 统一导出函数

### 验证

```bash
Rscript -e 'source("04_Outputs/_figure_config.R"); cat("Figure config OK\n")'
```

## 执行细节

### 方法执行流程

每个方法的执行:

1. **创建目录**:
   ```r
   dir.create("03_AnalysisMethods/01_BaselineTable", recursive = TRUE, showWarnings = FALSE)
   dir.create("04_Outputs/01_BaselineTable", recursive = TRUE, showWarnings = FALSE)
   ```

2. **生成代码**:
   ```r
   library(gtsummary)
   library(dplyr)
   library(readr)
   source("04_Outputs/_figure_config.R")  # 强制！
   
   data <- read_csv("02_PreprocessedData/data/cleaned.csv")
   # ... 分析方法特定代码 ...
   ```

3. **运行并验证**:
   - 检查输出文件存在
   - 检查图表 DPI >= 300
   - 检查统计报告完整性

4. **写入方法说明**:
   ```markdown
   # 01_BaselineTable
   
   ## Purpose
   比较两组的人口学和临床基线特征
   
   ## Statistical Methods
   - gtsummary::tbl_summary() + add_p()
   - 连续变量: t 检验或 Wilcoxon
   - 分类变量: 卡方检验或 Fisher 精确
   
   ## Input Variables
   - 分组: {group_var}
   - 所有基线变量
   
   ## Output Files
   - Table1.docx — 基线特征表
   - Table1.xlsx — 可编辑版本
   ```

### Wave 间检查点

每个 Wave 完成后:
```
Wave {N} ({label}) 完成

已完成方法:
- {method_1}: {outputs_summary}
- {method_2}: {outputs_summary}

请确认结果是否满意，然后进入下一 Wave。
```

## 验证检查清单

- [ ] 每个方法有 figure + table + 方法说明
- [ ] 图表 >=300 DPI
- [ ] 英文标签
- [ ] 出版级主题（theme_pub 通过 _figure_config.R）
- [ ] 统计报告: 效应量 + 95%CI + p 值
- [ ] 代码可从 cleaned.csv 独立运行
- [ ] R 版本和包版本已记录
- [ ] _figure_config.R 被所有脚本 source
- [ ] MANIFEST.yaml 存在于 04_Outputs/

## 后续阶段增补

在 Phase 3（写作）或 Phase 4（审稿）期间，如果用户需要额外分析，创建新 Wave 并追加到方案：

```yaml
    4:
      label: "审稿人要求补充分析"
      methods:
        - id: "05_SensitivityAnalysis_E-value"
          type: sensitivity
          method: "E-value calculation"
```
