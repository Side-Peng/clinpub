---
name: pre-phase-research
description: "标准化 Phase 前调研流程：根据 Phase 类型自动选择调研轨道，执行搜索，产出 RESEARCH.md，为 discuss-phase 提供信息基础。配合 agents/reference-agent.md 的 phase_research 模式使用。"
---

# Phase 前调研流程参考文档

> 本文件定义 clinpub 开发 Phase（6、7 及后续）的标准化前调研流程。
> 配合 `agents/reference-agent.md` 的 `phase_research` 模式使用。

---

## 第一章：Phase 前调研流程概览

### 流程定位

调研在 GSD discuss-phase **之前**执行，作为 Phase 工作流的 Step 0 前置步骤（per D-06, D-12）。

**完整流程顺序：**

```
调研（产出 RESEARCH.md）
  → GSD discuss-phase（基于调研结果讨论）
    → GSD plan-phase（规划）
      → GSD execute-phase（执行）
```

### 调研定位

- 为讨论提供**信息基础**，不替代讨论
- 调研范围限定在当前即将执行的 Phase 所需**领域/技术背景**
- 调研产出为讨论提供客观依据，让用户基于数据做出知情的决策

### 调研触发

- 调研步骤在 GSD `/gsd-plan-phase` 之前执行
- 当 planner agent 开始规划某个 Phase 时，先读取本参考文档，触发调研流程
- 不创建新 command（per D-06）：通过现有 GSD 管理流程的状态检测触发

---

## 第二章：轨道选择规则

> per D-01 双轨调研制

根据 Phase 特征自动选择调研轨道。以下决策表定义了匹配规则：

| Phase 特征 | 选择轨道 | 说明 |
|-----------|---------|------|
| 涉及临床分析方法、文献引用、研究设计 | **Track A**（领域调研） | 搜索领域背景、最佳实践、文献 |
| 涉及 command、hook、workflow 改造 | **Track B**（技术调研） | 扫描 codebase + 搜索技术方案 |
| 同时涉及以上两者 | **双轨** | 先 Track A 再 Track B，优先综述性建议 |
| 纯配置、工具链升级 | **Track B** | 侧重技术对比选型 |
| 新统计方法、分析范式 | **Track A** | 侧重方法学文献和应用案例 |

### 关键词自动匹配

根据 Phase 名称和描述中的关键词自动判断轨道：

- **Track A 关键词**：分析、方法、文献、引用、统计、研究、临床、期刊、方法学、综述
- **Track B 关键词**：命令、钩子、workflow、配置、工具、重构、脚本、文档、集成、CI/CD

### 判断流程

1. 读取 Phase 名称和 ROADMAP.md 的 Goal 描述
2. 扫描关键词匹配
3. 如仅匹配 Track A 关键词 → Track A
4. 如仅匹配 Track B 关键词 → Track B
5. 如两者都匹配 → 双轨
6. 如两者都不匹配 → 检查 Phase 上下文，联系用户确认

---

## 第三章：调研深度自适应协议

> per D-02

### 第一轮：摘要级发现（默认输出）

- 产出 3-5 个关键信息点
- 附带 2-3 篇参考来源（DOI/URL）
- 控制在"够做决策"的量级，不做过度调研

### 用户追问时：深入层

- 展开原理说明
- 提供代码示例或实现细节
- 补充更多参考文献

### 核心规则

**首轮输出必须控制在摘要级**，禁止一次性输出全部调研内容。用户没有追问时不得自动展开。

---

## 第四章：与现有 discuss 步骤的关系

> per D-06, D-08

### 不变的部分

现有 GSD 的 discuss-phase / plan-phase / execute-phase 流程保持**不变**（per D-08）。调研不替代任何现有步骤。

### 新增的部分

调研作为 **Step 0 前置步骤** 在 discuss 之前执行（per D-06）。

### 执行顺序

```
调研（Step 0）→ discuss-phase（Step 1）→ plan-phase（Step 2）→ execute-phase（Step 3）
```

### 集成细节

- 不创建新 command（D-06）：通过现有 GSD 管理流程的状态检测触发
- 调研产出 RESEARCH.md 后，planner agent 读取该文件作为 discuss 环节的上下文
- 调研结果仅作为讨论的基础，**不替代**用户决策

---

## 第五章：调研结果流入 CONTEXT.md

> per D-05

RESEARCH.md 的内容映射到 CONTEXT.md 的对应节，标记方式为**追加/补充**，不覆盖 CONTEXT.md 中已存在的用户决策。

| RESEARCH.md 节 | CONTEXT.md 目标节 | 映射方式 |
|---------------|-------------------|---------|
| 关键发现 | `<specifics>` | 追加为 Specific Ideas |
| 参考来源 | `<canonical_refs>` | 追加到参考列表 |
| 建议下游操作 | 讨论重点 | 转化为 discuss 讨论议题 |

### 映射规则

1. RESEARCH.md 的"关键发现" → 追加到 CONTEXT.md 的 `<specifics>` 节，标记来源为 research
2. RESEARCH.md 的"参考来源" → 追加到 CONTEXT.md 的 `<canonical_refs>` 节
3. RESEARCH.md 的"建议下游操作" → 作为 discuss 阶段的讨论重点
4. **不覆盖**：CONTEXT.md 中已存在的用户决策（`<decisions>` 节）不受影响

---

## 关联文件

### 执行入口

本文件定义调研流程规范。执行调研时调用 `agents/reference-agent.md` 的 `phase_research` 模式。

### 关联文件

- `agents/reference-agent.md` — phase_research 模式（定义 Track A/Track B 的具体搜索执行逻辑）
- `.clinpub/codebase/` — Track B 使用的代码库地图文件
- `ncbi-search` skill — PubMed 文献搜索（ncbi-search 技能，用户自行安装）

---

## 第六章：Track A — 领域调研协议

### 调研目标

搜索 Phase 相关的临床/方法学领域的背景知识、最佳实践、现有文献。

### 搜索策略

1. 调用 reference-agent 的 `phase_research` 模式（Track A 子模式）
2. 搜索渠道：
   - **学术文献搜索**：使用 `ncbi-search` 技能搜索 PubMed（关键词: "{phase_keywords}"，类型: review，最大 5 篇）
   - ncbi-search 技能由用户自行安装，clinpub 不捆绑内置
3. 搜索关键词构建规则：从 Phase 名称和 ROADMAP.md 的 Goal 描述提取核心关键词

### 产出格式

- **调研主题与范围**：一句话概括该 Phase 的调研范围
- **关键发现列表**：3-5 条，按重要性和置信度排序
- **关键参考文献列表**：2-3 篇，含 DOI/PMID

### 注意事项

- 参考文献必须有**真实 DOI**，禁止编造（继承 reference-agent 的核心规则）
- 如果搜索结果不足（<2 篇有效文献），标注"搜索结果有限，建议手动补充"
- 不修改 reference-agent 的输出格式，直接消费其搜索结果

---

## 第七章：Track B — 技术调研协议

### 调研目标

搜索 Phase 相关的工程技术方案、库选型、最佳实践。

### 搜索策略

1. **读取项目上下文文件**：
   - `project_config.yml` — 了解当前项目配置
   - `.clinpub/STATE.md` — 了解当前阶段
   - `.clinpub/ROADMAP.md` — 了解路线图
   - 无需额外扫描逻辑（per D-10）
2. **ncbi-search 搜索技术文献**：使用 `ncbi-search` 技能在 PubMed 中搜索技术方案文献（关键词: "{technology_keyword}"，最大 5 篇）

### 产出格式（与 Track A 统一）

- **调研主题与范围**
- **关键发现列表**：3-5 条
- **可选方案对比表**：如涉及选型

---

## 第八章：双轨模式

当 Phase 同时需要领域调研和技术调研时：

### 执行顺序

1. 先执行 **Track A**（领域优先，确定临床方向）
2. 再执行 **Track B**（技术方案基于领域方向选择）

### 合并输出

输出合并为一个 RESEARCH.md：

- **主题部分**：说明该 Phase 的双轨性质
- **关键发现**：合并排序（领域发现在前，技术发现在后）
- **对比表**：优先展示领域选项（如研究设计选择），再展示技术选项（如工具选型）

---

## 第九章：RESEARCH.md 标准模板

> per D-03, D-04

每次调研时直接填充以下模板：

```markdown
---
phase: {NN}-{name}
type: research
generated: {date}
track: {A / B / 双轨}
---

# {Phase 名称} — 调研报告

## 调研主题与范围

{一句话概括调研范围}

## 关键发现

按重要性和置信度排序：

1. **{发现 1}** — {说明，含证据来源}
2. **{发现 2}** — {说明，含证据来源}
3. **{发现 3}** — {说明，含证据来源}
4. **{发现 4}** — {说明，含证据来源}
5. **{发现 5}** — {说明，含证据来源}

## 可选方案对比

| 选项 | 优点 | 缺点 | 推荐 |
|------|------|------|------|
| {方案 A} | {优点 1}, {优点 2} | {缺点 1}, {缺点 2} | ⭐ 推荐（{理由}） |
| {方案 B} | {优点 1}, {优点 2} | {缺点 1}, {缺点 2} | — |
| {方案 C} | {优点 1}, {优点 2} | {缺点 1}, {缺点 2} | — |

## 参考来源

1. {Author Year}. {Title}. *{Journal}*. DOI: {doi} / URL: {url}
2. {Author Year}. {Title}. *{Journal}*. DOI: {doi} / URL: {url}
3. {Author Year}. {Title}. *{Journal}*. DOI: {doi} / URL: {url}

## 建议下游操作

在 discuss-phase 中应重点讨论：

1. **{讨论点 1}** — {说明为什么需要讨论，有什么选项}
2. **{讨论点 2}** — {说明为什么需要讨论，有什么选项}
3. **{讨论点 3}** — {说明为什么需要讨论，有什么选项}
```

### 模板说明

- 对比表行数 2-4 个选项
- 有推荐标记的选项必须附理由
- 参考来源必须有可访问的标识符（DOI/URL）
- 建议下游操作直接映射到 CONTEXT.md 的讨论重点

---

## 第十章：Quality Gate

RESEARCH.md 产出后必须满足以下条件方可进入 discuss 步骤：

- [ ] 调研主题与范围清晰定义
- [ ] 关键发现 ≥ 3 条
- [ ] 可选方案对比表（如涉及选型）或说明"不涉及选型"
- [ ] 参考来源 ≥ 2 个（或说明"搜索结果有限"）
- [ ] 建议下游操作 ≥ 2 条
- [ ] 所有引用有可追溯来源（DOI/URL）

检查方式：在生成 RESEARCH.md 后由 reference-agent 的 `phase_research` 模式自动执行 checklist 验证。不满足条件的调研报告不得进入 discuss 步骤。
