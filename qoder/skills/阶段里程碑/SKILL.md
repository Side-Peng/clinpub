---
name: 阶段里程碑
description: "Phase gate review with deliverable verification and user sign-off"
description_zh: "阶段门评审——验证交付物、记录决策、获取用户签核、推进到下一阶段"
version: 1.0.0
user-invocable: true
argument-hint: "<阶段编号>"
---

# 阶段里程碑

阶段门评审流程：验证已完成阶段的交付物，记录关键决策，获取用户签核，推进到下一阶段。

这是 DISCUSS -> PLAN -> EXECUTE -> VERIFY 生命周期中的 VERIFY 步骤。

## 触发方式

- **自动触发**：每个阶段工作流结束时自动调用（初始化、数据清洗、统计分析、论文写作、同行评审）
- **手动触发**：用户可随时调用 `@阶段里程碑 <N>` 检查阶段状态

## 执行流程

### 步骤 1：加载阶段上下文

```bash
PHASE="$ARGUMENTS"  # 如 "0", "1", "2"
PROJECT_DIR=$(pwd)
PLANNING_DIR="$PROJECT_DIR/.clinpub"
PHASE_DIR="$PLANNING_DIR/phases/$(printf '%02d' $PHASE)-*"
```

读取：
- `$PLANNING_DIR/ROADMAP.md` — 确认阶段名称、目标、成功标准
- `$PLANNING_DIR/STATE.md` — 当前状态、决策日志
- `$PLANNING_DIR/PROJECT.md` — 项目愿景、需求

阶段编号映射：

| 阶段 | 名称 |
|------|------|
| 0 | 初始化 (init) |
| 1 | 数据清洗 (data-prep) |
| 2 | 统计分析 (analysis) |
| 3 | 论文写作 (writing) |
| 4 | 同行评审 (review) |

### 步骤 2：验证成功标准

逐阶段检查清单：

**阶段 0（初始化）**：
- [ ] 项目目录结构已创建（.clinpub/, 01_RawData/ 等）
- [ ] project_config.yml 已生成并反映用户决策
- [ ] 研究类型已由用户确认
- [ ] 分析方法已由用户选择
- [ ] 决策日志已写入 00-CONTEXT.md

**阶段 1（数据清洗）**：
- [ ] cleaned.csv 存在于 02_PreprocessedData/data/
- [ ] 数据质量报告已生成（HTML）
- [ ] 缺失值按约定策略处理
- [ ] 异常值已记录
- [ ] 衍生变量已创建并编码
- [ ] 清洗代码可独立复现

**阶段 2（统计分析）**：
- [ ] 每个确认方法在 04_Outputs/ 中有图表 + 表格 + 方法说明
- [ ] 所有图表 >= 300 DPI，英文标签，出版级主题
- [ ] 统计报告包含效应量 + 95%CI + 精确 p 值
- [ ] 代码从 cleaned.csv 读取，可独立运行
- [ ] R 版本和关键包版本已记录

**阶段 3（论文写作）**：
- [ ] IMRAD 结构完整（全部 5 个章节）
- [ ] 所有引用有 DOI
- [ ] 文中引用了所有图表
- [ ] STROBE/CONSORT 检查清单已覆盖
- [ ] 无 AI 模板模式（Humanizer 检查通过）

**阶段 4（同行评审）**：
- [ ] 审稿意见已生成（Major/Minor 分类）
- [ ] 所有确认项已在稿件中处理
- [ ] 回复信完整（逐条）
- [ ] 最终稿件在 05_Manuscript/final/

### 步骤 3：收集决策

从以下来源收集阶段中的关键决策：

- 阶段讨论日志（`.clinpub/phases/NN-phase-name/00-CONTEXT.md`）
- STATE.md 决策日志
- 执行过程中用户确认的 shell 历史

格式化为决策表：

| 决策 | 选择 | 理由 | 来源 |
|------|------|------|------|

### 步骤 4：生成里程碑文档

写入 MILESTONE.md 到 `.clinpub/phases/NN-phase-name/MILESTONE.md`：

填充字段：
- `phase_number`, `phase_name`
- `date`：当天日期
- `status`：Complete 或 Partial（基于验证结果）
- `deliverables`：产出文件/输出列表
- `verification_items`：每个标准的检查结果
- `decisions`：关键决策表
- `outputs`：输出文件路径表
- `blockers`：未解决的问题
- `next_phase_number`, `next_phase_name`, `next_phase_goal`, `next_steps`

### 步骤 5：更新 ROADMAP

1. 将当前阶段状态设为 Complete
2. 将下一阶段状态设为 In Progress
3. 更新完成日期或备注

ROADMAP.md 格式：

```markdown
| Phase | Name | Status | Success Criteria | Notes |
|-------|------|--------|-----------------|-------|
| 0 | init | Complete | ... | Milestone: link |
| 1 | data-prep | In Progress | ... | |
```

### 步骤 6：用户签核

向用户展示里程碑摘要请求签核：

```
阶段：{{phase_number}} — {{phase_name}}
状态：{{status}}
验证：{{checks_summary}}
关键产出：{{outputs_summary}}
下一阶段：Phase {{next}} — {{next_name}}

输入 approved 进入下一阶段，或描述问题
```

**如用户批准**：
1. 更新 STATE.md：设 `current_phase` 为下一阶段，清除阶段特定状态
2. 在 MILESTONE.md 中写入签核确认
3. 推进到下一阶段（或通知用户可用对应命令启动）

**如用户要求修改**：
1. 在 MILESTONE.md 的 blockers 中记录所需修改
2. 状态设为 Partial
3. 帮助用户处理问题
4. 重新运行里程碑验证

## 成功标准

- MILESTONE.md 生成含所有验证结果
- ROADMAP.md 更新含阶段完成状态
- STATE.md 设为下一阶段
- 用户已签核或已记录阻塞原因
- 决策日志完整可审计

## 参考资料

- [里程碑工作流详细步骤](references/milestone-workflow.md)
- [质量门检查点](../知识库/references/checkpoints.md)
- [里程碑模板](../知识库/references/templates/milestone.md)
