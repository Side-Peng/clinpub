---
name: writing
description: "阶段3：递进式 IMRAD 写作。图表骨架 → Results → Methods → Discussion → Conclusion → 叙事设计 → Introduction → Abstract → 一致性复核 → 拼装。每节读前节的实际内容，产物落 05_Manuscript/sections/*.md，由脚本按 IMRAD 顺序生成 manuscript.md。"
argument-hint: ""
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---
<objective>
阶段3：**递进式** IMRAD 写作。

与 2.x 的三点差异：

1. **顺序**：Results → Methods → Discussion → Conclusion → 叙事设计 → Introduction → Abstract（不再从 Introduction 开始）
2. **依赖**：每一节必须读前面各节的实际内容；写作标准见 `writing_standards.md`
3. **载体**：单节写 `05_Manuscript/sections/{key}.md`，`manuscript.md` 是**生成物**

为什么从结果往回写：先写 Results 定死"发现了什么"，Introduction 的 Gap 与假设就必须服务于已有发现。反过来最容易出的事故是"引言承诺的分析没做"，只能在 Discussion 里打补丁。
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/writing.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/writing_standards.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/journal_standards.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/citation-strategy.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/reference-library.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/concatenation-protocol.md"`
</execution_context>

<process>
Execute the writing workflow from pipeline/workflows/writing.md end-to-end.

写作顺序（不可打乱）：

```
0. 图表骨架 FIGURE_SKELETON      ← 定海神针，先排图表 + 一句结论
1. Results                       ← 骨架 + 04_Outputs + ANALYSIS_LOG（只陈述，不解释）
2. Methods                       ← ANALYSIS_LOG + 方法说明 + 配置（三段式，如实）
3. Discussion                    ← Results + Methods + ANALYSIS_LOG + 文献
4. Conclusion                    ← Discussion
5. 叙事设计 NARRATIVE            ← R + M + D（想清楚怎么引人入胜）
6. Introduction                  ← 叙事设计 + R/M/D + 文献
7. Abstract + Title
8. 一致性复核（10 项）
9. 拼装 manuscript.md（脚本生成，禁止手改）
```

三个不可省略的规则：

1. **暂停点**由 `project_config.yml` 的 `writing.pause_after` 控制（默认 `[results, discussion]`），其余章节自动推进
2. **任何章节被改** → 按 stale 规则把下游置 `stale`；有 stale/draft 时拼装脚本会**拒绝**生成
3. **写作可反哺分析**：若发现分析缺口（如 Discussion 缺机制解释所需的中介分析），走 `feedback_to_analysis` 退回阶段2 补分析
</process>

<success_criteria>
- `FIGURE_SKELETON.md` 存在，每张图有一句不含统计量的结论
- `NARRATIVE.md` 存在，Gap 能被实际做过的分析填上
- `sections/` 六节齐全，`status` 全为 `final`，且 `inputs` 真实读取过上游
- Results 早于 Introduction 产出（递进而非并行）
- Methods 的 Statistical Analysis 与 `ANALYSIS_LOG.md` 双向一致
- Results 无解释性语句；Discussion 引用了敏感性分析或被否决备选
- `python scripts/assemble_manuscript.py` 通过，`manuscript.md` 按 IMRAD 顺序生成
- 无占位符残留；引用从 [1] 连续编号且全部含 DOI
- 字数 ≥ `writing.min_words`；引用数在 `citation_strategy.total_range` 内
- 一致性复核 10 项全部通过
</success_criteria>
