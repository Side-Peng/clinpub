# Phase 2: 断点续做 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-05
**Phase:** 02-断点续做
**Areas discussed:** `/clinpub-do` 路由逻辑, `/clinpub-next-step` 推进策略, Clear 提示设计

---

## `/clinpub-do` 路由逻辑

| Option | Description | Selected |
|--------|-------------|----------|
| 直接执行 | 无参时自动执行当前 Phase 对应的命令 | |
| 报告摘要 | 输出当前状态摘要 + 建议命令，让用户确认后再执行 | ✓ |
| 看情况 | Phase 当前任务明确时自动执行，不确定时报告摘要 | |

**User's choice:** 报告摘要
**Notes:** 有自然语言输入时 NL 优先于状态检测。推断不出明确意图时回退到报告摘要。

---

## 检查点定义

| Option | Description | Selected |
|--------|-------------|----------|
| 已有机制足够 | SUMMARY.md + STATE.md/ROADMAP.md 标记完成就够了 | ✓ |
| 需要用户确认 | 额外加一个 verify 步骤让用户确认是否要继续 | |

**User's choice:** 已有机制足够
**Notes:** 不需要额外 verify 步骤。

---

## 推进前验证

| Option | Description | Selected |
|--------|-------------|----------|
| 先验证再推进 | 先检查 SUMMARY.md 是否存在等完成证据，没完成则提示用户 | ✓ |
| 不验证直接推进 | 假设用户已手动完成，直接推进到下一步 | |
| 先完成再推进 | 检查完成状态，已完成就推进，没完成就自动执行当前步骤再推进 | |

**User's choice:** 先验证再推进

---

## NL 推理策略

| Option | Description | Selected |
|--------|-------------|----------|
| NL 优先于状态 | 如果有 NL 输入，直接按 NL 意图路由，忽略状态检测 | ✓ |
| 状态 + NL 结合 | 先跑状态检测得到上下文，再结合 NL 输入一起推断意图 | |
| 状态优先，NL 辅助 | NL 输入只做微调，主要路由逻辑由状态和工件检测决定 | |

**User's choice:** NL 优先于状态

---

## 推进粒度

| Option | Description | Selected |
|--------|-------------|----------|
| Phase 级 | 逐 Phase 推进（Phase 1 → Phase 2 → ...） | |
| Wave 级 | 逐 Wave 推进（Phase 1 Plan 01 → Plan 02 → Phase 2...） | |
| 自动判断粒度 | 两者都支持：当前 Phase 还有未完成的 Wave 就推进到下一 Wave，全部完成就推进到下一 Phase | ✓ |

**User's choice:** 自动判断粒度

---

## Claude's Discretion

- `/clinpub-do` 中工件检测的具体逻辑和优先级顺序
- Clear 提示的精确措辞格式
- 时序处理（如推进过程中遇到中途错误的重试策略）
- Clear 提示的触发方式

## Deferred Ideas

None — discussion stayed within phase scope.
