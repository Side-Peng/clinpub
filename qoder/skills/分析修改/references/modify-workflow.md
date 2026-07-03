---
description: "分析修改工作流详细步骤"
---

# 分析修改工作流

## 目的

在阶段 2 完成后启用对分析输出的定向修改。通过结构化的 定义->执行->验证->记录 周期编排修改流程。可在阶段 2、3、4 中调用。

## 必读资料

- 分析方法：`../知识库/references/analysis_methods.md`
- R 图表模式：`../知识库/references/r_patterns.md`

## 详细步骤

### 步骤 1：validate_prerequisites（优先：first）

验证分析阶段已完成：

```bash
PROJECT_DIR=$(pwd)
PLAN=$(ls "$PROJECT_DIR/.clinpub/phases/02-analysis/"*-PLAN.md 2>/dev/null | head -1)
DATA="$PROJECT_DIR/02_PreprocessedData/data/cleaned.csv"
OUTPUTS="$PROJECT_DIR/04_Outputs/"
```

检查：
1. `*-PLAN.md` 存在 — 否则报错："未找到分析计划。请先运行统计分析。"
2. `cleaned.csv` 存在 — 否则报错："未找到清洗数据。请先运行数据清洗。"
3. `04_Outputs/` 有至少一个方法目录 — 否则报错："未找到分析输出。请先运行统计分析。"

### 步骤 2：define_modifications（优先：high）

1. 解析 `*-PLAN.md` 构建方法清单
2. 向用户展示清单
3. 用户选择方法并定义修改
4. 输出结构化修改摘要
5. **检查点**：用户确认修改摘要

如用户拒绝 -> 停止。
如用户确认 -> 继续执行。

### 步骤 3：execute_modifications（优先：high）

对确认摘要中的每项修改：

1. **备份**：记录当前 commit hash
2. **修改**：执行变更（R 脚本修改 + 重跑）
3. **简报**：报告每项成功/失败

执行顺序：样式修改（低风险）-> 变量修改 -> 方法修改 -> 新方法。

如修改需要未安装的包，报告并跳过。不自动安装包。

### 步骤 4：verify_outputs（优先：medium）

对每条成功修改：

1. 图表文件存在且非空
2. 图表 DPI >= 300
3. 英文标签
4. 表格文件存在且包含更新统计
5. 方法说明已更新
6. 统计报告含效应量 + 95%CI + 精确 p 值

验证失败：报告具体失败，提供重跑或跳过选项。

### 步骤 5：cascade_manuscript_update（优先：medium）

如 `05_Manuscript/` 存在：

1. 修补 Results 章节中受影响的数值
2. 如方法变更，更新 Methods 章节
3. 报告更新了哪些章节

如稿件不存在，静默跳过。

### 步骤 6：update_plan_history（优先：high）

1. 追加修改记录到 `*-PLAN.md`
2. 更新 STATE.md "最近活动" 行

修改记录格式：
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
    failed: []
```

## 成功标准

- 前提条件已验证
- 修改范围明确并经用户确认
- 每项修改有成功/失败报告
- 修改后输出达到出版标准
- 修改历史追加到 PLAN.md
- 稿件受影响章节已修补（如存在）
- STATE.md 最近活动已更新
