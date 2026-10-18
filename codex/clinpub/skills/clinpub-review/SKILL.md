---
name: clinpub-review
description: "投稿后：处理期刊的真实审稿意见。录入用户提供的审稿意见 → 起草逐条回复信与改进方向 → 用户确认 → 交 improving 执行修稿。按轮次循环。不模拟审稿人。触发：收到审稿意见、返修、回复审稿人、rebuttal。"
---

# ClinPub Review（投稿后审稿回复）

## Execution Context

- Workflow: `pipeline/workflows/review.md`
- Delegates to: `pipeline/workflows/improving.md`

## Process

1. 前置：`05_Manuscript/manuscript.md` 与 `05_Manuscript/sections/` 可用；**必须**由用户提供真实审稿意见（粘贴或文件路径），否则停止
2. 结构化：编号、原文引用、Major/Minor、动作类型（文本/补分析/补文献/澄清/反驳）、**受影响章节 key**
   - 用 3.0 章节键定位（`results`/`methods`/`discussion`/`conclusion`/`introduction`/`abstract`），不要用页码段落
3. 起草回复信 + 改进方向，用户确认
4. 委派 `clinpub-improving` 执行（跳过其开放式自审，直接进执行）
5. 重拼后把 `manuscript.md` 复制到 `05_Manuscript/final/`，完成回复信中的改动定位

## Success Criteria

- 审稿意见为真实输入（绝不伪造）
- 每条意见映射到具体章节 key
- 回复信逐条回应（含不改的理由）
- 修订经 improving 执行，改在 `sections/` 并重拼
- `final/` 下有修订稿与回复信；支持多轮
