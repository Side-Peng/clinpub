---
name: clinpub-do
description: "Read workspace state and auto-route to the appropriate clinpub command. With natural language input (e.g., '/clinpub:do 我想改清洁逻辑'), routes by intent. With no arguments, shows current state summary and suggests next commands."
---

# ClinPub Do

Workspace state router. Reads STATE.md, detects artifacts, and routes to the correct Phase command.

## 行为模式

- **无参数** (D-01): 读取 STATE.md + 检测关键工件 → 输出状态摘要 + 建议 1-3 条命令 → 用户确认后路由
- **有 NL 参数** (D-02): NL 意图识别优先于状态检测 → 成功则直接路由 → 失败则回退到无参行为（D-04）
- **路由依据** (D-03): 三合一决策：STATE.md `- 阶段：Phase N` + 工件检测 + 可选 NL 输入

## NL 意图推断规则

使用强信号关键词优先匹配策略，非简单包含匹配。关键词按优先级从高到低排列：

| 优先级 | 关键词（任一命中即路由） | 路由到 | 特异度 |
|--------|-------------------------|--------|--------|
| 1 | `(初始化\|init\|开始\|创建项目\|新建)` | init | 高 — 非清洁/分析语境 |
| 2 | `(清洁\|clean\|数据质量\|缺失\|异常值\|cleaned)` | data-prep | 高 — 特异性数据处理术语 |
| 3 | `(选题\|话题挖掘\|idea\|数据探索\|data2idea)` | data2idea | 高 — 选题挖掘术语 |
| 4 | `(分析\|统计\|结果\|图\|表\|analysis\|figure\|table\|回归\|生存\|ROC)` | analysis | 高 — 分析术语 |
| 5 | `(写\|稿\|手稿\|文献\|引用\|writing\|IMRAD\|论文\|manuscript)` | writing | 高 — 写作术语 |
| 6 | `(审稿\|review\|修订\|修改\|意见\|审阅\|response)` | review | 高 — 审稿术语 |
| 7 | `(推进\|下一步\|继续\|next\|advance)` | next-step | 高 — 推进术语 |
| 8 | `(状态\|摘要\|总览\|当前\|情况\|see\|status\|什么阶段)` | 回退到无参 | 明确表达"查看状态"意图，不是特定命令 |

**匹配规则**:
- 命中高优先级关键词立即路由，不继续检查低优先级（D-02：NL 优先于状态检测）
- 命中第 7 组关键词 → 执行无参状态检测流程（D-04：明确表达查看状态，回退到摘要）
- 没有命中任何关键词组 → 回退到无参行为（D-04：推断不出明确意图）
- **跨组冲突时**（如同时包含"分析"和"写"）：以优先级高的为准（Group 编号小的优先），不按文本位置判断
- **反模式规避**: 不要匹配停用词（"看"、"查"、"项目"、"做"）

## 工件检测模式

```
Phase 0: -f project_config.yml + 验证 project.name != "项目名称"
Phase 1: -f 02_PreprocessedData/data/cleaned.csv
Phase 2: -d 04_Outputs && ls 04_Outputs/ 非空 + project_config.yml analysis_plan.waves
Phase 3: -f 05_Manuscript/manuscript.md
Phase 4: -d 05_Manuscript/final && ls 05_Manuscript/final/ 非空
```

## Process

1. 解析输入参数（NL 或无参）
2. 执行工件检测
3. 输出状态摘要和建议命令
4. 等待用户确认路由

## Success Criteria

- 无参数时输出准确的当前 Phase 状态摘要 + 1-3 条建议命令
- 带 NL 输入时正确推断意图并路由到对应命令
- NL 推断失败时正确回退到无参行为（显示状态摘要）
- 路由后等待用户确认，不自动执行目标命令
- 所有 8 个命令的路由映射完整（init, data-prep, analysis, writing, review, next-step, milestone, data2idea）
- 不匹配停用词（"看"、"查"、"项目"、"做"）
