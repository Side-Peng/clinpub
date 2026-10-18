---
name: clinpub-modify
description: "修改已完成的分析输出或新增分析方法。确认改动范围（图表样式/统计方法/变量/新方法）→ 执行 → 校验 → 追加到 ANALYSIS_LOG → 把受影响章节标 stale 并按依赖重写 → 重拼手稿。"
---

# ClinPub Modify（分析修改）

## Execution Context

- Workflow: `pipeline/workflows/modify.md`
- Decision policy: `pipeline/references/analysis_decision_policy.md`
- Methods / patterns: `analysis_methods.md`, `r_patterns.md`
- Agent: `agents/modify-agent.md`

## Process

1. 前置检查：`ANALYSIS_LOG.md` + `cleaned.csv` + `04_Outputs/`
2. 建立方法清单（扫描 `03_AnalysisMethods/*/` + 日志），定义改动 → 用户确认
3. 执行（样式 → 变量 → 方法 → 新增），逐条报告
4. 校验产物（DPI / 英文标注 / 方法说明已更新 / 效应量+CI+p）
5. **追写 `ANALYSIS_LOG.md` 的 `Batch M-{n}（modify）` 六段记录**
6. **按 DAG 标记 stale**（不直接改 `manuscript.md`）
7. 重写 stale 章节 → `python scripts/assemble_manuscript.py`
8. 更新 `STATE.md`

## Success Criteria

- 改动范围经用户确认，逐条有成功/失败报告
- 修改后图达到出版标准（≥300 DPI、英文标注）
- `ANALYSIS_LOG.md` 已追加 modify 批次（六段齐全）
- 受影响章节已标 `stale` 并按 DAG 传播
- 重写并重拼完成，或已明确告知用户待处理
- **未直接修改 `manuscript.md`**
