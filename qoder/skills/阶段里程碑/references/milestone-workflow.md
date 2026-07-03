---
description: "阶段里程碑工作流详细步骤"
---

# 里程碑工作流

## 目的

阶段间正式门评审。确保每个阶段在下一阶段开始前正确完成，所有决策有文档记录，并获得用户签核。

## 必读资料

- 质量检查点：`../知识库/references/checkpoints.md`
- 里程碑模板：`../知识库/references/templates/milestone.md`

## 详细步骤

### 步骤 1：load_phase_context（优先：first）

加载当前阶段和项目上下文：

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
| 0 | init |
| 1 | data-prep |
| 2 | analysis |
| 3 | writing |
| 4 | review |

### 步骤 2：verify_success_criteria（优先：high）

检查已完成阶段的所有成功标准：

**阶段 0（init）**：
- [ ] 项目目录结构已创建
- [ ] project_config.yml 已生成并反映用户决策
- [ ] 研究类型已由用户确认
- [ ] 分析方法已由用户选择
- [ ] 决策日志已写入 00-CONTEXT.md

**阶段 1（data-prep）**：
- [ ] cleaned.csv 存在于 02_PreprocessedData/data/
- [ ] 数据质量报告已生成（HTML）
- [ ] 缺失值按约定策略处理
- [ ] 异常值已记录
- [ ] 衍生变量已创建并编码
- [ ] 清洗代码可独立复现

**阶段 2（analysis）**：
- [ ] 每个确认方法有图表 + 表格 + 方法说明
- [ ] 所有图表 >=300 DPI，英文标签
- [ ] 统计报告含效应量 + 95%CI + 精确 p 值
- [ ] 代码从 cleaned.csv 读取，可独立运行
- [ ] R 版本和关键包版本已记录

**阶段 3（writing）**：
- [ ] IMRAD 结构完整
- [ ] 所有引用有 DOI
- [ ] 文中引用所有图表
- [ ] STROBE/CONSORT 检查清单已覆盖
- [ ] 无 AI 模板模式

**阶段 4（review）**：
- [ ] 审稿意见已生成（Major/Minor）
- [ ] 所有确认项已处理
- [ ] 回复信完整
- [ ] 最终稿件在 05_Manuscript/final/

### 步骤 3：collect_decisions（优先：high）

从以下来源收集关键决策：
- 阶段讨论日志
- STATE.md 决策日志
- 用户确认历史

格式化为决策表：

| 决策 | 选择 | 理由 | 来源 |
|------|------|------|------|

### 步骤 4：generate_milestone（优先：high）

写入 MILESTONE.md 到 `.clinpub/phases/NN-phase-name/MILESTONE.md`：

填充字段：
- phase_number, phase_name
- date: 当天日期
- status: Complete 或 Partial
- deliverables: 产出文件列表
- verification_items: 每个标准的检查结果
- decisions: 关键决策表
- outputs: 输出文件路径表
- blockers: 未解决问题
- next_phase_number, next_phase_name, next_phase_goal, next_steps

### 步骤 5：update_roadmap（优先：high）

更新 ROADMAP.md：

1. 当前阶段状态 -> Complete
2. 下一阶段状态 -> In Progress
3. 更新完成日期或备注

### 步骤 6：user_signoff（优先：high）

向用户展示里程碑摘要请求签核。

如用户批准：
1. 更新 STATE.md: current_phase -> 下一阶段
2. 写入签核确认到 MILESTONE.md
3. 推进到下一阶段

如用户要求修改：
1. 记录 blockers
2. 状态设为 Partial
3. 帮助处理问题
4. 重新验证

## 成功标准

- MILESTONE.md 生成含所有验证结果
- ROADMAP.md 更新含阶段完成状态
- STATE.md 设为下一阶段
- 用户已签核或已记录阻塞原因
- 决策日志完整可审计
