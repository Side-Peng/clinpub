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
- `.planning/codebase/` — Track B 使用的代码库地图文件
- `scripts/tavily_search.py` — Tavily 搜索工具
- `scripts/pubmed_search.py` — PubMed 搜索工具
- `scripts/ncbi_search.py` — NCBI 多数据库搜索工具
