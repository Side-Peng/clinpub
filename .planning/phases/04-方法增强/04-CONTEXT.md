# Phase 4: 方法增强 - Context

**Gathered:** 2026-05-07
**Status:** Ready for planning

<domain>
## Phase Boundary

增强 clinpub 的统计方法处理能力，两个独立功能：

1. **METH-01**: 用户在全管线任何阶段提到未知统计方法时，自动搜索资料总结后再与用户讨论
2. **METH-02**: 组间对比方法固化——根据组数（2组 vs 3+组）和结局类型（连续/分类）自动选择标准检验流程

不涉及新增统计方法实现，只做方法检索、推荐和标准流程固化。

</domain>

<decisions>
## Implementation Decisions

### 触发与检测（METH-01）

- **D-01 (触发范围):** 全管线通用。不限于 Phase 2 分析阶段，任何 Phase 中用户提到未知统计方法时均自动触发搜索
- **D-02 (方法检测):** 不维护白名单。由 reference-agent 每次搜索时动态判断方法是否已掌握，无需维护已知方法列表
- **D-03 (触发模式):** 仅当用户明确提及方法名称时触发（如"这个方法我不太熟悉"、"帮我查一下 X 方法"），不主动猜测

### 搜索策略（METH-01）

- **D-04 (搜索来源):** Tavily 优先 → PubMed 补充。先使用 Tavily 搜索网络获取方法概览和应用场景，学术资料不足时再用 PubMed 找学术引用
- **D-05 (呈现深度):** 自适应模式。首次输出方法简介 + 适用场景 + 2-3 篇关键参考文献（摘要级），用户追问更多细节时再深入（原理、R 实现、示例代码）

### 流程集成

- **D-06 (集成策略):** 双轨制。搜索结果总结直接替换原 analysis spec 的方法描述部分；详细教程作为附件文档单独输出，不修改原方案
- **D-07 (输出位置):** 新增独立参考文档 `pipeline/references/comparison-methods.md`，不修改 `analysis_methods.md` 也不内联到 workflow

### 组间对比方法树（METH-02）

- **D-08 (两组—连续):** 正态+方差齐 → 独立样本 t 检验；正态+方差不齐 → Welch t 检验；非正态 → Mann-Whitney U 检验
- **D-09 (两组—分类):** 理论频数 >=5 → 卡方检验；理论频数 <5 → Fisher 精确检验
- **D-10 (三组+—连续):** 正态+方差齐 → 单因素 ANOVA + 事后多重比较（Bonferroni/Tukey）；正态+方差不齐 → Welch ANOVA + Games-Howell；非正态 → Kruskal-Wallis 检验 + Dunn 事后比较
- **D-11 (三组+—分类):** 同两组逻辑：卡方检验 / Fisher 精确检验 + 必要时列联表事后分析
- **D-12 (配对/重复测量):** 两组配对连续 → paired t 检验 / Wilcoxon 符号秩检验；多组重复测量 → 重复测量 ANOVA / Friedman 检验
- **D-13 (效应量报告):** t 检验 → Cohen's d；Mann-Whitney → r = Z/√N；ANOVA → η² / partial η²；卡方 → Cramer's V / φ

### Agent's Discretion
- 搜索结果的精确格式化（渲染模板、段落组织）
- reference-agent 调用 Tavily/PubMed 时的具体 prompt 策略
- `comparison-methods.md` 中决策树的精确文档结构和示例代码呈现方式

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 现有方法参考
- `pipeline/references/analysis_methods.md` — 现有统计方法决策树（需参考但本次不修改）
- `pipeline/references/r_patterns.md` — R 可视化核心标准
- `pipeline/references/agent-contracts.md` §Agent 输出目录矩阵

### 搜索工具
- `scripts/tavily_search.py` — Tavily AI 搜索工具
- `scripts/ncbi_search.py` — NCBI/PubMed 搜索工具
- `scripts/pubmed_search.py` — PubMed 搜索封装

### 现有命令与工作流
- `commands/clinpub/analysis.md` — Phase 2 分析命令入口
- `pipeline/workflows/analysis.md` — Phase 2 分析工作流（方法选择逻辑在此定义，需了解但本次不大改）

### 需求定义
- `.planning/REQUIREMENTS.md` — METH-01/METH-02 详细定义

### Agent 合约
- `agents/reference-agent.md` — 文献搜索 Agent（搜索执行者）
- `agents/clinpub-planner.md` — 分析方案规划 Agent（结果消费方）
- `agents/analyst-agent.md` — 执行分析的统计师 Agent（方法执行方）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `scripts/tavily_search.py` — 已有 Tavily 搜索封装，可直接用来搜索方法概览
- `scripts/ncbi_search.py` / `scripts/pubmed_search.py` — PubMed 学术搜索
- `agents/reference-agent.md` — 文献搜索 Agent，可扩展搜索策略后复用
- `pipeline/references/analysis_methods.md` — 已有统计方法参考文档，作为对比方法文档的风格参考

### Established Patterns
- Agent 轮次调用模式（Phase 2/3 已建立）：子任务 → 独立调用 Agent → 检查输出
- 命令入口 frontmatter 中 argument-hint / allowed-tools 标准格式
- 参考文档均使用 Markdown + 二级标题分隔章节 + 表格结构化数据

### Integration Points
- `pipeline/workflows/analysis.md` — 方法选择逻辑需要感知新的搜索能力（METH-01）和标准对比方法（METH-02）
- `pipeline/references/comparison-methods.md` — 新增参考文档，供 planner/analyst-agent 在规划/执行时查阅
- analysis spec 生成时需要集成搜索结果的摘要替换逻辑

</code_context>

<specifics>
## Specific Ideas

- 搜索结果的"摘要级"呈现可参考 Tavily 的 AI 回答格式：先给结论再列引用
- 组间对比决策树用流程图或表格呈现，比文字描述更清晰（可参考 analysis_methods.md 的格式风格）
- reference-agent 在搜索方法时可以复用 Phase 3 的文献预搜索模式（但搜索目标不同）
- 方法增强能力应让 `/clinpub-analysis` 的诊断阶段自动提建议："检测到 3 组比较，是否需要使用标准组间对比流程？"

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 04-方法增强*
*Context gathered: 2026-05-07*
