# Phase 4: 方法增强 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in CONTEXT.md — this log preserves the discussion.

**Date:** 2026-05-07
**Phase:** 04-方法增强
**Mode:** discuss (interactive)

## Areas Discussed

### 1. 触发场景 (Trigger Scope)
- **Q:** METH-01 中，"未知统计方法"触发搜索的场景范围？
- **Options:** 仅 Phase 2 / 全管线通用 / 用户主动请求
- **Selected:** 全管线通用
- **Notes:** 用户明确要求任何 Phase 中提及未知方法都触发搜索

### 2. 呈现深度 (Presentation Depth)
- **Q:** 搜索后呈现的内容深度？
- **Options:** 摘要级 / 教程级 / 自适应
- **Selected:** 自适应
- **Notes:** 首次输出摘要，用户追问再深入

### 3. 方法覆盖度 (Method Coverage)
- **Q:** 组间对比是否需要覆盖非参数检验等特殊情况？
- **Options:** 仅参数 / 参数+非参数完整版 / 自适应决策树
- **Selected:** 参数+非参数完整版
- **Notes:** 包含正态性检验驱动的自动选择逻辑，含配对/重复测量场景

### 4. 流程集成 (Pipeline Integration)
- **Q:** 搜索结果如何整合到 Phase 2 分析流程？
- **Options:** 修改分析方案 / 单独方法说明文档 / 双轨制
- **Selected:** 双轨制
- **Notes:** 搜索结果替换方案方法描述 + 详细教程附件

### 5. 输出形式 (Output Format)
- **Q:** 组间对比方法固化输出到哪里？
- **Options:** 更新 analysis_methods.md / 新增独立参考文档 / Phase 2 workflow 内联
- **Selected:** 新增独立参考文档
- **Notes:** 创建 `pipeline/references/comparison-methods.md`

### 6. 搜索来源 (Search Source)
- **Q:** 搜索优先级？
- **Options:** PubMed 优先→Tavily / Tavily 优先→PubMed / 仅 PubMed
- **Selected:** Tavily 优先→PubMed 补充

### 7. 方法检测 (Method Detection)
- **Q:** 是否需要维护已知方法白名单？
- **Options:** 需要白名单 / 不需要白名单 / 混合策略（仅用户明确请求时触发）
- **Selected:** 不需要白名单
- **Notes:** 动态判断，由 reference-agent 决定

## Decisions Captured
- D-01: 全管线通用触发
- D-02: 不维护白名单，动态判断
- D-03: 仅用户明确提及方法名称时触发
- D-04: Tavily 优先 → PubMed 补充
- D-05: 自适应呈现深度
- D-06: 双轨制流程集成
- D-07: 新增独立参考文档
- D-08 ~ D-13: 组间对比方法树（含效应量）
