---
phase: 05-pre-phase-research
plan: 01
subsystem: pipeline/references
tags:
  - pre-phase-research
  - track-selection
  - research-protocol
  - quality-gate
type: reference-document
dependency_graph:
  requires: []
  provides:
    - "Standardized research workflow definition for phases 6-7"
    - "Track A/B selection rules per D-01"
    - "RESEARCH.md template with 5-section structure per D-03/D-04"
    - "CONTEXT.md mapping rules per D-05"
  affects:
    - agents/reference-agent.md (phase_research mode, Plan 05-02)
    - "Future Phase 6-7 research execution"
tech-stack:
  added: []
  patterns:
    - "Reference document format (frontmatter + chapters + tables)"
    - "Decision table for track selection"
    - "Adaptive depth protocol (summary-first, deep-on-demand)"
key-files:
  created:
    - pipeline/references/pre-phase-research.md
  modified: []
decisions: []
metrics:
  duration_minutes: 0
  completed_date: "2026-05-11"
---

# Phase 5 Plan 1: 创建调研参考文档 — Summary

创建标准化 Phase 前调研流程参考文档 `pipeline/references/pre-phase-research.md`，定义轨道选择规则、Track A/B 调研协议、RESEARCH.md 模板和 quality gate。

## 任务执行

### 任务 1：写文档 frontmatter、轨道选择规则、自适应深度协议

- **文件**：`pipeline/references/pre-phase-research.md`
- **创建内容**：
  - YAML frontmatter
  - 第一章：Phase 前调研流程概览
  - 第二章：轨道选择规则（决策表 + 关键词匹配）
  - 第三章：调研深度自适应协议（摘要级 + 深入层）
  - 第四章：与现有 discuss 步骤的关系（D-06, D-08）
  - 第五章：调研结果流入 CONTEXT.md（D-05）
  - 关联文件参考导航
- **提交**：`f7e3394`

### 任务 2：写 Track A/B 协议、RESEARCH.md 模板、Quality Gate

- **文件**：`pipeline/references/pre-phase-research.md`（追加）
- **追加内容**：
  - 第六章：Track A 领域调研协议（PubMed + Tavily 搜索策略）
  - 第七章：Track B 技术调研协议（codebase 扫描 + Tavily 技术搜索）
  - 第八章：双轨模式（先领域后技术，合并输出规则）
  - 第九章：RESEARCH.md 标准模板（5 节结构 + 模板说明）
  - 第十章：Quality Gate（6 项检查清单）
- **提交**：`5375f56`

## 交付物

| 文件 | 状态 | 行数 |
|------|------|------|
| `pipeline/references/pre-phase-research.md` | 创建完成 | 310 行 |

## 章节结构

| 章节 | 内容 | 对应 D# |
|------|------|---------|
| 第一章 | Phase 前调研流程概览 | D-06, D-12 |
| 第二章 | 轨道选择规则 | D-01 |
| 第三章 | 调研深度自适应协议 | D-02 |
| 第四章 | 与现有 discuss 步骤的关系 | D-06, D-08 |
| 第五章 | 调研结果流入 CONTEXT.md | D-05 |
| 第六章 | Track A 领域调研协议 | D-09 |
| 第七章 | Track B 技术调研协议 | D-09, D-10 |
| 第八章 | 双轨模式 | D-01 |
| 第九章 | RESEARCH.md 标准模板 | D-03, D-04 |
| 第十章 | Quality Gate | D-07 |

## Deviations from Plan

无 — 计划完全按设计执行。

## Known Stubs

无 — 所有内容完整写入。

## 未完成项

- **05-02-PLAN.md**：扩展 reference-agent 添加 phase_research 模式（下一个计划）

## Success Criteria Check

- [x] pre-phase-research.md 包含完整的轨道选择规则（Track A/B/双轨判断条件）
- [x] pre-phase-research.md 包含 Track A 和 Track B 的搜索执行协议
- [x] pre-phase-research.md 包含 RESEARCH.md 的标准模板（5 节结构）
- [x] pre-phase-research.md 包含 quality gate 检查清单
- [x] pre-phase-research.md 说明与现有 discuss 步骤的集成方式

## Self-Check: PASSED

所有文件、提交和内容验证均已确认。
