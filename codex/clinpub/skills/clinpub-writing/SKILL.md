---
name: clinpub-writing
description: "阶段3: 递进式 IMRAD 写作。图表骨架 → Results → Methods → Discussion → Conclusion → 叙事设计 → Introduction → Abstract → 一致性复核 → 拼装。每节读前节的实际内容，产物落 05_Manuscript/sections/*.md，由脚本按 IMRAD 顺序生成 manuscript.md。"
---

# ClinPub Writing（递进写作）

与 2.x 的三点差异：

1. **顺序**：从 Results 往回写，不再从 Introduction 开始
2. **依赖**：每节必须读前面各节的实际内容
3. **载体**：单节写 `05_Manuscript/sections/{key}.md`，`manuscript.md` 是**生成物**

写作标准以 `pipeline/references/writing_standards.md` 为准。

## Execution Context

- Workflow: `pipeline/workflows/writing.md`
- Standards: `pipeline/references/writing_standards.md`
- Journal: `pipeline/references/journal_standards.md`
- Citation: `pipeline/references/citation-strategy.md`, `reference-library.md`
- Concatenation: `pipeline/references/concatenation-protocol.md`

## Process

```
0. 图表骨架 FIGURE_SKELETON      ← 定海神针
1. Results      ← 骨架 + 04_Outputs + ANALYSIS_LOG（只陈述，不解释）
2. Methods      ← ANALYSIS_LOG + 方法说明 + 配置（三段式，如实）
3. Discussion   ← Results + Methods + ANALYSIS_LOG + 文献
4. Conclusion   ← Discussion
5. 叙事设计 NARRATIVE            ← R + M + D
6. Introduction ← 叙事设计 + R/M/D + 文献
7. Abstract + Title
8. 一致性复核（10 项）
9. 拼装（python scripts/assemble_manuscript.py）
```

## Success Criteria

- `FIGURE_SKELETON.md` 每张图有一句不含统计量的结论
- `NARRATIVE.md` 的 Gap 能被实际分析填上
- `sections/` 六节齐全，`status` 全为 `final`
- Results 早于 Introduction 产出（递进而非并行）
- Methods 与 `ANALYSIS_LOG.md` 双向一致；Results 无解释性语句
- `assemble_manuscript.py` 通过，`manuscript.md` 按 IMRAD 顺序生成
- 无占位符残留；引用从 [1] 连续编号且全部含 DOI
