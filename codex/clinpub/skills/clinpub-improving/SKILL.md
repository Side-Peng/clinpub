---
name: clinpub-improving
description: "持续改进手稿。自审稿件 → 产出具体修改计划 → 用户确认 → 直接改章节文件（必要时重跑分析并级联数值）→ 按依赖把下游标为 stale → 重拼手稿。不写回复信、不模拟审稿人，可反复调用。触发：改进、润色、精修论文，投稿前自审。"
---

# ClinPub Improving（持续改进）

## Execution Context

- Workflow: `pipeline/workflows/improving.md`
- Standards: `pipeline/references/writing_standards.md`
- Journal: `pipeline/references/journal_standards.md`
- Agents: `agents/writer-agent.md`, `agents/modify-agent.md`

## Process

1. 前置检查：`05_Manuscript/sections/*.md` 存在（只有 `manuscript.md` 说明是 3.0 前的手稿）
2. 自审（读 sections + `FIGURE_SKELETON.md` + `.clinpub/ANALYSIS_LOG.md` + 引用库），标注 Major/Minor
3. 转成逐条计划（纯文本 / 分析重跑 / 图表 / 文献），用户确认
4. 执行：先分析重跑（并追加 `ANALYSIS_LOG` 批次），再图表，再文献，最后文本
   - **改 `sections/{key}.md`**，不写 `## 标题`；数值变化时 `results` 必须整节重写
5. 按 DAG 标 stale（`results`→下游；`methods`→discussion/intro/abstract）
6. 重写 stale → `python scripts/assemble_manuscript.py`
7. 记录本轮（`improvement_plan.md` + `STATE.md`）

**3.0 专项自审**：Results 是否混入解释 / Methods 与日志是否双向一致 / Introduction 的 Gap 能否被实际分析填上 / Discussion 是否用上敏感性分析与否决项 / 各节 status 是否与内容一致。

## Success Criteria

- 自审含 3.0 专项五项检查，产出 Major/Minor 条目
- 计划经用户确认后才动手
- 文本改在 `sections/*.md`；受影响章节按 DAG 标 stale 并重写回 `final`
- `assemble_manuscript.py` 通过，`manuscript.md` 已重拼
- 未产出回复信、未模拟审稿人；本轮已记录
