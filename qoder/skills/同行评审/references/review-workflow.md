---
description: "Phase 4 评审工作流详细步骤"
---

# 同行评审工作流

## 目的

模拟目标期刊级别的严格同行评审，迭代修改稿件。每个周期：生成评审 -> 用户确认项 -> 修改稿件 -> 生成回复信 -> 循环直至用户满意。

## 必读资料

- 期刊标准：`../知识库/references/journal_standards.md`
- 质量检查点：`../知识库/references/checkpoints.md`

## 详细步骤

### 步骤 1：discuss_review_scope（优先：first）

与用户讨论评审标准：

1. **评审严格度**（默认：目标期刊级别——从 `project_config.yml` 的 `journal.name` + `journal.tier` 读取；如未配置，应用 Q2 标准）
2. **重点关注领域**：用户是否有特定方面希望审稿人重点关注
3. **补充检索**：是否需要根据评审方向检索新文献

### 步骤 2：generate_review（优先：high）

生成模拟审稿意见 `05_Manuscript/review_v1.md`：

**Major 意见**（优先）：
- 统计方法的适当性与完整性
- 样本量与统计功效
- 混杂因素控制的充分性
- 结果解读与过度推断
- 研究设计局限性

**Minor 意见**：
- 语言与语法问题
- 引用完整性与相关性
- 图表格式与清晰度
- 报告规范合规性（STROBE/CONSORT）

每条意见包含：
- 位置（章节、行号）
- 问题描述
- 修改建议
- 严重程度

### 步骤 3：confirm_revision_items（优先：high）

向用户展示审稿意见：

1. 展示所有审稿意见及分类
2. 用户确认哪些需要修改（可推迟部分）
3. 用户可追加额外修改请求
4. 在开始修改前就修改范围达成一致

### 步骤 4：revise_manuscript（优先：high）

系统性修改稿件处理确认项：

1. 逐条处理审稿意见
2. 追踪每条修改
3. 如新增引用则更新文献列表
4. 保留原始版 + 修改版以供对比

**Major 意见**：可能需要补充分析（回到阶段2重跑）或额外文献检索（Reference Agent）
**Minor 意见**：直接编辑稿件

### 步骤 5：generate_response_letter（优先：high）

撰写逐条回复信：

```markdown
## Reviewer 1, Comment 1
> [审稿人意见原文]

**Response**: [修改说明]
**Changes**: [稿件中修改位置，行号/页码]

## Reviewer 1, Comment 2
...
```

每条回复必须：
- 感谢审稿人的意见
- 说明修改内容和理由
- 如未修改，提供理由
- 指向修改后稿件中的具体位置

### 步骤 6：verify_and_loop（优先：medium）

修改后：

1. 验证所有确认项已处理
2. 检查回复信完整性
3. 提交给用户审阅
4. 如用户要求更多修改 -> 循环回步骤 2
5. 如用户满意 -> 进入里程碑

最终交付物：
- `05_Manuscript/review_v1.md` — 审稿意见
- `05_Manuscript/final/manuscript.md` — 最终接受的稿件
- `05_Manuscript/final/response_letter.md` — 审稿回复信
- 更新 `Reference/references.bib`（如有新引用）

### 步骤 7：milestone（优先：high）

执行里程碑工作流正式关闭阶段 4（项目完成）：

1. 验证阶段 4 的成功标准
2. 收集评审决策（处理的意见、回复信）
3. 生成 `.clinpub/phases/04-review/MILESTONE.md`
4. 更新 ROADMAP.md：Phase 4 -> Complete
5. 更新 STATE.md：current_phase -> complete
6. 向用户展示项目完成总结

签核提示：
```
────────────────────────────────
  Phase 4 核验完成

请确认：输入 "approved" 完成全部流程，或描述需要调整的地方。
────────────────────────────────
```

## 成功标准

- 审稿意见按 Major/Minor 分类生成
- 用户确认修改项
- 所有确认项在稿件中得到处理
- 逐条回复信完整
- 新引用添加到 references.bib
- 最终稿件存入 `05_Manuscript/final/`
- 用户对修改满意
