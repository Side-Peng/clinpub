# Phase 6: 图表+文档优化 - Context

**Gathered:** 2026-05-28
**Status:** Ready for planning

<domain>
## Phase Boundary

本 Phase 交付两件事：
1. **R 可视化整体升级** — 更新 `r_patterns.md` 中的 `theme_pub()` 主题、配色规范、图表类型模板，使所有分析输出达到 SCI 期刊投稿级质量
2. **WAVE 文档中文本地化** — 将 `03_AnalysisMethods/XX_MethodName/README.md` 全部改为中文「方法说明」，统一内容结构模板

范围不包括：新增分析方法、修改统计逻辑、改变 Phase 2 执行流程。

</domain>

<decisions>
## Implementation Decisions

### 图表优化范围
- **D-01:** 整体升级所有图表输出，不是局部修补。包括 theme_pub() 主题优化、配色规范更新、新增图表类型模板
- **D-02:** 参考 SCI 期刊风格（Nature/NEJM/Lancet 等顶刊图表规范），不参考 R 社区风格

### 图表输出标准
- **D-03:** 不预设目标期刊。用户在开始写文章时通常不预设期刊，因此默认输出高质量图表即可
- **D-04:** 配色必须在 Phase 2 分析前与用户确认。r_patterns.md 已有选色决策流程（询问用户偏好），保持此流程
- **D-05:** 图表质量标准参照现有规范：≥300 DPI、Arial ≥8pt、单栏 8cm/双栏 17cm、TIFF(PDF/EPS) 格式

### WAVE 文档本地化
- **D-06:** 所有 WAVE 目录（`03_AnalysisMethods/XX_MethodName/`）的 README.md 都需要改造为中文「方法说明」
- **D-07:** 改名为「方法说明」— 具体文件名由 agent 设计（如 `方法说明.md` 或 `README_方法说明.md`），需考虑与现有 MANIFEST.yaml 和 agent-contracts.md 的兼容性
- **D-08:** 统一内容结构模板，由 agent 设计，预期包含：目的、方法、输入数据、输出结果、参数设置、注意事项、软件版本

### the agent's Discretion
- theme_pub() 的具体视觉调整细节（字体大小、边距、网格线等）
- 新增哪些图表类型模板（基于现有 analysis_methods.md 中的方法推断）
- 「方法说明」的最终文件名和内容结构模板设计
- 如何处理与 agent-contracts.md 中 "README must contain Results subsection" 的兼容性

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### R 可视化规范
- `pipeline/references/r_patterns.md` — 当前 theme_pub() 主题、配色规范、图表类型模板、保存规范（核心改造对象）
- `pipeline/references/journal_standards.md` — SCI Q1/Q2 期刊发表标准（图表质量参考基准）

### Agent 输出契约
- `pipeline/references/agent-contracts.md` — Analyst Agent 输出规范（README 必须包含 Results subsection，需与「方法说明」兼容）
- `pipeline/references/gates.md` — Phase 2 质量门（每方法 figure + table + README 三件套）

### 分析方法
- `pipeline/references/analysis_methods.md` — 当前支持的分析方法列表（决定需要哪些图表类型模板）

### 项目配置
- `.planning/REQUIREMENTS.md` — CHART-01, DOC-01, DOC-02 需求定义
- `.planning/PROJECT.md` — 核心价值和项目上下文

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `r_patterns.md` 已有完整的 theme_pub()、配色选色协议、图表保存规范、显著性标注规则 — 这是改造的基础
- `journal_standards.md` 已有 SCI 期刊的图表尺寸标准（单栏 8cm、双栏 17cm、≥300 DPI）
- `analysis_methods.md` 定义了所有分析方法 — 可据此推断需要哪些图表类型模板

### Established Patterns
- 每个分析方法输出 figure + table + README 三件套（agent-contracts.md）
- README 必须包含 `Results` subsection（agent-contracts.md）
- MANIFEST.yaml 记录输出文件清单（manifest-format.md）
- 选色决策流程：询问用户偏好 → 按组数推荐配色（r_patterns.md 1.1）

### Integration Points
- Phase 2 Analyst Agent 读取 `r_patterns.md` 生成图表 — 改造后自动生效
- Phase 3 Writer Agent 读取 `04_Outputs/` 中的图表 — 质量提升自动传递
- `agent-contracts.md` 中的输出规范需要与「方法说明」新命名保持一致

</code_context>

<specifics>
## Specific Ideas

- 用户强调"配色要问清楚" — 保持 r_patterns.md 中的选色决策流程，确保 Phase 2 分析前与用户确认配色方案
- SCI 期刊风格参考：Nature 的简洁风格、NEJM 的规范要求
- 「方法说明」需要中英混排友好（统计术语、R 包名保持英文）

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 6-图表+文档优化*
*Context gathered: 2026-05-28*
