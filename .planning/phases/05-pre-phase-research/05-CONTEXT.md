# Phase 5: Phase 前调研流程 - Context

**Gathered:** 2026-05-07 (assumptions mode)
**Status:** Ready for planning

<domain>
## Phase Boundary

创建标准化的 Phase 前调研流程，覆盖后续所有 clinpub 开发 Phase（6、7 及后续）。每个 Phase 执行前：自动调研相关领域和技术方案 → 以建议方式与用户讨论 → 收集反馈后再执行。

不涉及：
- 修改 GSD 框架本身的 discuss/plan/execute 流程
- 新增统计方法或分析能力
- 具体的引用策略或图表优化（那是 Phase 6/7 的 scope）
</domain>

<decisions>
## Implementation Decisions

### 调研范围（Research Scope）

- **D-01:** 双轨调研制。根据 Phase 类型自动选择轨道：
  - **Track A（领域调研）**：面向临床/方法类 Phase（如涉及分析方法、文献引用），使用 reference-agent + PubMed/Tavily 搜索领域背景、最佳实践
  - **Track B（技术调研）**：面向工程类 Phase（如涉及 command、hook、workflow 改造），使用 codebase 扫描 + Tavily 搜索技术方案、库选型
  - **双轨模式**：混合类 Phase 同时执行两个 Track，优先输出综述性建议
- **D-02:** 调研深度自适应。首轮输出摘要级发现（3-5 个关键信息点 + 2-3 篇参考），用户追问时深入展开（原理、实现细节、代码示例）

### 输出格式（Research Output）

- **D-03:** 每个调研 Phase 产出 `RESEARCH.md` 文件，位于该 Phase 目录下（如 `.planning/phases/06-引用策略/06-RESEARCH.md`），在 CONTEXT.md 之前生成
- **D-04:** RESEARCH.md 标准结构：
  - 调研主题与范围
  - 关键发现（按重要性排序）
  - 可选方案对比表（2-4 个选项 + 优缺点 + 推荐标记）
  - 参考来源（DOI / URL）
  - 建议的下游操作（discuss 时应重点讨论的点）
- **D-05:** 调研结果自动流入 CONTEXT.md 的 `<specifics>` 和 `<canonical_refs>` 节，减少重复讨论

### 集成方式（Integration）

- **D-06:** 不创建新 command。调研作为现有 Phase 工作流的 Step 0 前置步骤，由每条命令的 workflow 自动触发
- **D-07:** 创建 `pipeline/references/pre-phase-research.md` 作为调研流程的标准化参考文档，定义：
  - 轨道选择规则（根据 Phase 特征自动匹配 Track A/B/双轨）
  - 搜索执行协议（调用 reference-agent 的哪个模式）
  - 输出标准化模板
  - quality gate：RESEARCH.md 产出后方可进入 discuss 步骤
- **D-08:** 当前已存在的 discuss 步骤不变，调研作为新增前置步骤执行

### 工具复用（Tool Reuse）

- **D-09:** 复用全部现有搜索基础设施：
  - `scripts/tavily_search.py` — 技术/领域搜索（Tavily AI Search）
  - `scripts/ncbi_search.py` / `scripts/pubmed_search.py` — 学术文献搜索
  - `agents/reference-agent.md` — 增加 `phase_research` 模式，扩展现有 `literature_search` 和 `method_search` 模式的能力
- **D-10:** codebase 扫描使用现有 `.planning/codebase/` 地图文件（ARCHITECTURE.md, CONVENTIONS.md, STRUCTURE.md, INTEGRATIONS.md），无需额外扫描逻辑

### 与 GSD 框架的关系（GSD Relationship）

- **D-11:** Phase 5 操作在 clinpub 产品层，不修改 GSD 框架。调研流程被组织为 clinpub 的内部 `pipeline/references/pre-phase-research.md` 文档和 reference-agent 扩展
- **D-12:** 调研流程与 GSD 的 discuss-phase 互补：GSD discuss-phase 负责开发流程的讨论环节，clinpub 的调研流程负责在讨论前提供信息基础

### Agent's Discretion
- RESEARCH.md 中选项对比表的具体格式和视觉风格
- Track 选择规则的精确判断条件（关键词匹配 vs 标记配置）
- reference-agent `phase_research` 模式的具体 prompt 策略
- 调研结果自动流入 CONTEXT.md 的精确替换/追加逻辑

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 现有搜索基础设施
- `scripts/tavily_search.py` — Tavily AI 搜索工具
- `scripts/ncbi_search.py` — NCBI 多数据库搜索
- `scripts/pubmed_search.py` — PubMed 搜索封装
- `agents/reference-agent.md` — 文献搜索 Agent（含 literature_search / method_search 模式）

### 现有工作流模式（需了解但本次不重构）
- `pipeline/workflows/init-project.md` — Phase 0 工作流，有 `discuss_research_framework` 步骤
- `pipeline/workflows/analysis.md` — Phase 2 工作流，有 `diagnose_data_structure` + `discuss_and_confirm` 模式
- `pipeline/workflows/writing.md` — Phase 3 工作流，有 `discuss_writing_plan` + `reference_pre_search` 模式

### 代码库地图
- `.planning/codebase/ARCHITECTURE.md` — 系统架构概览
- `.planning/codebase/CONVENTIONS.md` — 代码规范与约定
- `.planning/codebase/STRUCTURE.md` — 目录结构
- `.planning/codebase/INTEGRATIONS.md` — 外部集成与工具

### Phase 4 方法增强参考
- `pipeline/references/comparison-methods.md` — 组间对比决策树（Phase 4 交付物，作为调研产出文档的风格参考）
- `pipeline/templates/context.md` — 现有 context 模板（调研结果需与此模板兼容）

### 需求定义
- `.planning/REQUIREMENTS.md` §FLOW-01 — 每个 Phase 前先调研，以建议方式与用户讨论，结合用户反馈再执行

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/tavily_search.py` — 已有 Tavily 搜索封装，可直接用于技术和领域调研
- `scripts/ncbi_search.py` / `scripts/pubmed_search.py` — 已有 PubMed 搜索，用于学术文献调研
- `agents/reference-agent.md` — 已有文献搜索 Agent，扩展 `phase_research` 模式即可覆盖调研需求
- `pipeline/references/comparison-methods.md` — Phase 4 的参考文档格式可作为 RESEARCH.md 格式参考
- `.planning/codebase/*.md` — 6 个代码库地图文件，直接用于 Track B 的技术调研

### Established Patterns
- Agent 模式扩展模式：Phase 4 在 reference-agent 中添加了 `method_search` 模式，Phase 5 可遵循相同模式添加 `phase_research` 模式
- 参考文档创建模式：新功能先在 `pipeline/references/` 下创建标准化参考文档（如 comparison-methods.md、concatenation-protocol.md）
- 薄命令入口模式：`commands/clinpub/*.md` 的 frontmatter + XML 标签结构

### Integration Points
- `agents/reference-agent.md` — 需增加 `phase_research` 模式
- `pipeline/references/pre-phase-research.md` — 新增参考文档
- 各 Phase 工作流的 discuss 步骤前插入调研步骤

</code_context>

<specifics>
## Specific Ideas

- 调研流程可复用 Phase 4 `method_search` 模式的"自适应深度"设计：先摘要后深度
- GSD 的 discuss-phase / plan-phase 模式可作为调研→讨论→执行流程的设计参考
- RESEARCH.md 的选项对比表可参考 `comparison-methods.md` 的决策树表格格式
- 调研范围选择可通过 frontmatter 标记或工作流步骤中的关键词匹配实现

</specifics>

<deferred>
## Deferred Ideas

None — analysis stayed within phase scope

</deferred>

---

*Phase: 05-pre-phase-research*
*Context gathered: 2026-05-07*
