---
name: 同行评审
description: "Phase 4: Simulated peer review and manuscript revision"
description_zh: "阶段4：模拟同行评审与稿件修改——按目标期刊级别生成审稿意见，迭代修改稿件，生成逐条回复信"
version: 1.0.0
user-invocable: true
argument-hint: ""
---

# 同行评审（Phase 4）

模拟目标期刊级别的严格同行评审，迭代修改稿件，直至用户满意。

## 评审范围

### 主要问题（Major）
- 统计方法的适当性与完整性
- 样本量与统计功效
- 混杂因素控制的充分性
- 结果解读与过度推断
- 研究设计局限性

### 次要问题（Minor）
- 语言与语法问题
- 引用完整性与相关性
- 图表格式与清晰度
- 报告规范合规性（STROBE/CONSORT）

## 执行流程

### 步骤 1：讨论评审范围

1. **评审严格度**：默认按目标期刊级别——从 `project_config.yml` 的 `journal.name` + `journal.tier` 读取；如未配置，应用 Q2 标准
2. **重点关注领域**：用户是否有特定方面希望审稿人重点关注
3. **补充检索**：是否需要根据评审方向检索新文献

### 步骤 2：生成模拟审稿意见

生成 `05_Manuscript/review_v1.md`，每条意见包含：

- **位置**：章节、行号
- **问题描述**：具体问题说明
- **修改建议**：推荐的修改方式
- **严重程度**：Major / Minor

**Major 意见优先关注**：
- 统计方法是否适当、是否遗漏关键分析
- 样本量是否足以支撑结论
- 混杂控制是否充分
- 结果是否存在过度推断
- 研究设计是否有未讨论的局限

**Minor 意见**：
- 语言和语法改进
- 引用格式和完整性
- 图表清晰度和格式
- STROBE/CONSORT 检查清单合规性

### 步骤 3：确认修改项

1. 向用户展示所有审稿意见及分类
2. 用户确认哪些需要修改（可推迟部分）
3. 用户可追加额外修改请求
4. 在开始修改前就修改范围达成一致

### 步骤 4：修改稿件

系统性处理每条确认的意见：

1. 逐条处理审稿意见
2. 追踪每条修改
3. 如新增引用则更新文献列表
4. 保留原始版 + 修改版以供对比

**Major 意见**：可能需要补充分析（回到阶段2重跑）或额外文献检索
**Minor 意见**：直接编辑稿件

### 步骤 5：生成逐条回复信

格式：

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

### 步骤 6：验证与循环

1. 验证所有确认项已处理
2. 检查回复信完整性
3. 提交给用户审阅
4. 如用户要求更多修改 -> 循环回步骤 2
5. 如用户满意 -> 进入里程碑

### 步骤 7：里程碑签核

执行阶段里程碑流程，正式关闭阶段 4（项目完成）：

1. 验证阶段 4 的成功标准
2. 收集评审决策
3. 生成 `.clinpub/phases/04-review/MILESTONE.md`
4. 更新 ROADMAP.md：Phase 4 -> Complete
5. 更新 STATE.md：current_phase -> complete
6. 向用户展示项目完成总结

## 反 AI 模板规则（Humanizer）

修改稿件时须遵守：

| 检查项 | AI 模式 | 修正 |
|--------|---------|------|
| 段落开头 | "首先...其次...最后" | 使用内容逻辑，去除序列标记 |
| 过渡词 | 反复使用 "Moreover/Furthermore" | 替换为具体因果/对比连接词 |
| 句式 | 每句都是 "X is a Y factor of Z" | 混合句式 |
| 空洞结论 | "More research is needed" | 替换为具体未来方向 |
| 引用生硬 | "Studies show..." | 给出具体作者或上下文 |
| 过度解释 | 逐一解释统计方法 | 只说明做了什么 |

## 关键规则

- 完整 IMRAD 结构
- 每个引用需要 DOI
- 文中引用的所有图表必须存在于 04_Outputs/
- STROBE/CONSORT 检查清单必须覆盖
- 稿件语言按 `language.manuscript` 配置（默认 zh-CN），图表英文
- 每章撰写后应用 Humanizer 检查
- 不得捏造引用或数据

## 最终交付物

- `05_Manuscript/review_v1.md` — 审稿意见
- `05_Manuscript/final/manuscript.md` — 最终稿件
- `05_Manuscript/final/response_letter.md` — 审稿回复信
- 更新 `Reference/references.bib`（如有新引用）

## 成功标准

- 审稿意见按 Major/Minor 分类生成
- 用户确认修改项
- 所有确认项在稿件中得到处理
- 逐条回复信完整
- 新引用添加到 references.bib
- 最终稿件存入 `05_Manuscript/final/`
- 用户对修改满意

## 参考资料

- [评审工作流详细步骤](references/review-workflow.md)
- [期刊标准](../知识库/references/journal_standards.md)
- [质量门检查点](../知识库/references/checkpoints.md)
