---
name: 分析修改
description: "Modify completed analysis outputs -- figure style or statistical method changes"
description_zh: "修改已完成的分析输出——支持图表样式调整（颜色/字体/布局）和统计方法变更（检验更换/变量替换/参数调整）"
version: 1.0.0
user-invocable: true
argument-hint: "[方法ID或简要描述，留空则交互选择]"
---

# 分析修改

修改已完成的阶段 2 分析输出。支持两类修改：图表样式调整和统计方法变更。

可在任何阶段（阶段 2、3、4）调用，当用户需要调整分析结果时使用。

## 修改类别

### 1. 样式修改（style）
- 配色方案调整
- 字体/字号变更
- 图表类型更换（如 boxplot -> violin）
- 布局调整（合并/拆分面板）
- 全局风格修改（编辑 `_figure_config.R` 后重跑所有受影响脚本）

### 2. 方法修改（method/variable/new）
- **变量替换（variable）**：变量更换或新增
- **方法变更（method）**：统计检验/模型更换
- **新方法（new）**：添加全新分析方法

## 执行流程

### 步骤 1：验证前提条件

```bash
PROJECT_DIR=$(pwd)
PLAN_DIR="$PROJECT_DIR/.clinpub/phases/02-analysis"
PLAN=$(ls "$PLAN_DIR"/*-PLAN.md 2>/dev/null | head -1)
DATA="$PROJECT_DIR/02_PreprocessedData/data/cleaned.csv"
OUTPUTS="$PROJECT_DIR/04_Outputs/"
```

检查：
1. `*-PLAN.md` 存在于 `.clinpub/phases/02-analysis/` — 否则报错："未找到分析计划，请先运行统计分析"
2. `cleaned.csv` 存在 — 否则报错："未找到清洗数据，请先运行数据清洗"
3. `04_Outputs/` 有至少一个方法目录 — 否则报错："未找到分析输出，请先运行统计分析"

### 步骤 2：构建方法清单并定义修改

1. 解析 `*-PLAN.md` 构建编号方法清单：

| # | ID | 类型 | 当前方法 |
|---|-----|------|----------|
| 1 | 01_BaselineTable | baseline | gtsummary::tbl_summary |
| 2 | 02_TwoGroupComparison | comparison | wilcox.test |
| 3 | ... | ... | ... |

2. 向用户展示清单
3. 用户选择方法并定义修改：
   - `style` — 视觉变更（配色、字体、图表类型、布局）
   - `variable` — 变量替换或新增
   - `method` — 统计检验/模型变更
   - `new` — 添加全新分析方法
4. 输出结构化修改摘要：

| # | 方法 | 类型 | 变更 | 影响文件 |
|---|------|------|------|----------|
| 1 | 02_TwoGroupComparison | style | boxplot -> violin + jitter | figure_*.png |
| 2 | 03_RepeatedMeasures | method | lmer -> GEE | all outputs |

5. **检查点**：用户确认修改摘要。**必须等待用户明确批准后才执行。**

如用户拒绝 -> 停止，不做任何修改。
如用户确认 -> 继续执行。

### 步骤 3：执行修改

**执行前备份**：记录当前 git commit hash 供回滚参考。

**执行顺序**（由低风险到高风险）：
1. 样式修改（低风险）
2. 变量修改
3. 方法修改
4. 新方法

**样式修改**：
1. 读取 `03_AnalysisMethods/{id}/` 中的 R 脚本
2. 修改 ggplot2 参数（geom, scale, theme）
3. 重跑脚本 -> 覆盖 `04_Outputs/{id}/` 中的输出

> **全局风格修改**：如用户要求修改所有图表的配色/主题/DPI，优先编辑 `04_Outputs/_figure_config.R` 然后重跑所有受影响的方法脚本。这确保风格一致性。

**方法修改**：
1. 读取 `03_AnalysisMethods/{id}/` 中的 R/Python 脚本
2. 用新方法重写统计部分
3. 更新方法说明（README）
4. 重跑脚本 -> 覆盖输出

**变量修改**：
1. 修改脚本中的变量引用
2. 重跑脚本 -> 覆盖输出

**新方法**：
1. 创建 `03_AnalysisMethods/{new_id}/` 和 `04_Outputs/{new_id}/`
2. 编写新的 R/Python 脚本（自包含，从 cleaned.csv 读取）
3. 运行脚本 -> 生成图表 + 表格 + 方法说明
4. 将新方法追加到 PLAN.md

**失败处理**：
- R/Python 脚本失败 -> 尝试修复（最多 3 次）
- 无法修复 -> 暂存变更，报告错误，继续下一个修改
- 在最终修改历史中记录失败

每条修改完成后输出：
```
[OK] 修改 1/2 完成：02_TwoGroupComparison — boxplot -> violin
[FAIL] 修改 2/2 失败：03_RepeatedMeasures — GEE 包未安装
```

### 步骤 4：验证输出

对每条成功修改：

1. 图表文件存在于 `04_Outputs/{id}/` 且非空
2. 图表 DPI >= 300，英文标签，主题一致
3. 主题自检：无灰色背景、无内置 ggplot 主题、语义配色、可读轴标签、统一线宽
4. 表格文件存在且包含更新统计
5. 方法说明（README）已更新
6. 统计报告包含效应量 + 95%CI + 精确 p 值
7. R 脚本自包含（从 cleaned.csv 读取，无全局状态）

验证失败时：报告具体失败项，提供重跑或跳过选项。

### 步骤 5：级联更新稿件

如 `05_Manuscript/` 存在：

1. 修补 Results 章节中受影响的数值（效应量、p 值、CI 边界）
2. 如统计方法变更，更新 Methods 章节
3. 报告更新了哪些章节

如稿件不存在（仅阶段 2），静默跳过。

### 步骤 6：更新修改历史

追加修改记录到 `*-PLAN.md` 末尾：

```yaml
modifications:
  - id: "mod-{YYYYMMDD}-{NNN}"
    timestamp: "{YYYY-MM-DD}"
    description: "{摘要}"
    items:
      - method_id: "{id}"
        type: "{style|variable|method|new}"
        change: "{描述}"
    status: "completed|partial"
    failed: [{失败方法列表}]
```

更新 STATE.md "最近活动" 行。

输出完成摘要：
```
─────────────────────────────────────────
 修改完成
─────────────────────────────────────────
成功：{N} 项修改
失败：{M} 项修改
PLAN.md 已更新修改历史
稿件级联：{K} 个章节已更新 / 跳过（未找到稿件）
─────────────────────────────────────────
```

## 关键规则

- 从 `cleaned.csv` 读取——不从原始数据或中间文件
- 所有修改后图表：>=300 DPI，英文标签，统一主题
- 所有统计报告：效应量 + 95%CI + 精确 p 值
- 稿件修改仅限修补数值和方法描述——不重写整个章节
- 不修改 `Reference/` 或 `02_PreprocessedData/`
- 每次会话最多 5 项修改（防止上下文溢出）
- 每个 R/Python 脚本必须自包含
- 例外：所有方法 R 脚本 `source("04_Outputs/_figure_config.R")` 是设计意图的共享配置
- 随机方法设置随机种子
- **必须等待用户确认后才执行修改**
- 不得捏造数据或结果

## 成功标准

- 修改范围明确定义并经用户确认
- 每项修改执行并验证（图表 + 表格 + 方法说明更新）
- 所有修改后图表达到出版标准
- 修改历史追加到 PLAN.md 含时间戳和详情
- 失败的修改已报告含错误详情
- 如稿件存在，受影响章节已修补

## 参考资料

- [修改工作流详细步骤](references/modify-workflow.md)
- [修改专家指南](references/modify-agent-guide.md)
- [分析方法参考](../知识库/references/analysis_methods.md)
- [R 图表模式参考](../知识库/references/r_patterns.md)
