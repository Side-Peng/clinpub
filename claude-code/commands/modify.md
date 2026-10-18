---
name: modify
description: "修改已完成的分析输出或新增分析方法。确认改动范围（图表样式/统计方法/变量/新方法）→ 执行 → 校验 → 追加到 ANALYSIS_LOG → 把受影响章节标 stale 并按依赖重写 → 重拼手稿。可在任意阶段调用。"
argument-hint: "[方法 ID 或简短描述，留空则交互选择]"
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
修改阶段2 的分析输出，或新增分析方法。两类用途：

1. **修改现有方法**：样式（颜色、字体、图表类型、版式——重绘）与实质（换检验、换变量、调参数——重跑）
2. **新增方法**：读现有代码（`03_AnalysisMethods/`）与 `cleaned.csv`，按 clinpub 约定（方法 ID 格式、图表配置、出版标准）设计并实现

**3.0 关键约束**：改动记录写进 `.clinpub/ANALYSIS_LOG.md`；手稿不直接改数字，而是把受影响章节标 `stale` 后重写，再由脚本重拼。
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/modify.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/analysis_methods.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/analysis_decision_policy.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/r_patterns.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/agents/modify-agent.md"`
</execution_context>

<process>
Execute the modification workflow from pipeline/workflows/modify.md end-to-end.

关键顺序：

1. 前置检查（`ANALYSIS_LOG.md` + `cleaned.csv` + `04_Outputs/`）
2. 定义改动 → 用户确认
3. 执行（样式 → 变量 → 方法 → 新增），逐条报告
4. 校验产物（DPI / 英文标注 / 方法说明已更新 / 效应量+CI+p）
5. **追写 `ANALYSIS_LOG.md` 的 `Batch M-{n}（modify）` 六段记录**
6. **按 DAG 标记 stale**（不改 `manuscript.md`）
7. 重写 stale 章节 → `python scripts/assemble_manuscript.py`
8. 更新 `STATE.md`
</process>

<success_criteria>
- 改动范围经用户确认，逐条有成功/失败报告
- 修改后的图达到出版标准（≥300 DPI、英文标注）
- 统计报告含效应量 + 95%CI + 精确 p
- `ANALYSIS_LOG.md` 已追加 modify 批次（六段齐全）
- 受影响章节已标 `stale` 并按 DAG 传播
- 重写并重拼完成，或已明确告知用户待处理
- 用户已知悉手稿需要重新拼装
</success_criteria>
