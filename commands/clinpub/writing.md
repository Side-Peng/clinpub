---
name: clinpub:writing
description: "Phase 3: IMRAD sequential manuscript writing. Sections written one-by-one (Introduction → Methods → Results → Discussion) with reference-agent pre-search before each section, writer-agent per-section drafting, and user review pause between sections. Shared reference library for deduplication. Placeholder-based cross-references. Final concatenation produces manuscript.md with YAML frontmatter."
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
Phase 3: Sequential IMRAD manuscript writing with per-section review.

## 流程概述

四段（Introduction → Methods → Results → Discussion）按顺序独立撰写引用后拼接为终稿。每段三段式：Reference Agent 文献预搜索 → Writer Agent 撰写 → 用户审阅 pause，确认后再进入下一段。

## 核心约束

- **D-01 顺序**: IMRAD 顺序（Intro → Methods → Results → Discussion），每段写完 pause 用户审阅
- **D-02 Agent 模式**: 同一个 writer-agent，4 轮对话分别写 4 段，不扩展 agent role 定义
- **D-03 上下文**: 自动读取项目数据（spec → Methods, analysis outputs → Results, 文献 → Intro/Discussion）
- **D-04 篇幅**: 全文 >5000 字，自然成段论述（非 bullet point）
- **D-05 Methods**: 从 spec + analysis pipeline outputs 自动生成初稿
- **D-06 文献搜索**: 每段前 reference-agent 搜索文献，更新共享引用库
- **D-09 引用库**: 全局统一编号，共享引用库（Reference/reference_library.json），写各段时查询已有引用
- **D-11 占位符**: 使用 {{Table:N}} {{Figure:N}} {{Method:name}} {{Section:name}} 进行交叉引用
- **D-15 输出**: 05_Manuscript/manuscript.md 最终稿 + 05_Manuscript/sections/ 各段独立文件
</objective>

<execution_context>
@./pipeline/workflows/writing.md
@./pipeline/references/journal_standards.md
@./pipeline/references/reference-library.md
@./pipeline/contexts/writing.md
</execution_context>

<process>
Execute the writing workflow from @./pipeline/workflows/writing.md end-to-end.
</process>

<success_criteria>
- 四个 IMRAD 段按顺序独立完成撰写（Intro → Methods → Results → Discussion）
- 每段撰写前 reference-agent 完成文献搜索，引用库不重复
- 每段撰写后用户完成审阅确认后才进入下一段
- 各段写入 05_Manuscript/sections/ 独立文件
- 各段使用占位符进行交叉引用（{{Table:N}} {{Figure:N}} {{Method:name}}）
- 各段引用通过共享引用库管理，不重复
- 所有引用有 DOI
- 全文 >5000 字，自然成段论述
- 无 AI-template 模式（Humanizer 自检通过）
</success_criteria>
