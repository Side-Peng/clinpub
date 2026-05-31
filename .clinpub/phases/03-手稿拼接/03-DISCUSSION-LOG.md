# Phase 3: 手稿拼接 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-06
**Phase:** 03-手稿拼接
**Areas discussed:** 撰写流程与 Agent 模式, 引用去重策略, 段间交叉引用, 终稿输出格式

---

## 撰写流程与 Agent 模式

### Q1: 四段撰写顺序

| Option | Description | Selected |
|--------|-------------|----------|
| IMRAD 顺序流水线 | Intro → Methods → Results → Discussion 依次写 | ✓ |
| 先写 Methods + Results | 数据驱动的实证论文常见写法 | |
| 你决定 | 每段开始前指定 | |

**User's choice:** IMRAD 顺序流水线
**Notes:** 无特殊说明

### Q2: 审阅节奏

| Option | Description | Selected |
|--------|-------------|----------|
| 逐段审阅 | 每段写完后 pause 让用户过目确认 | ✓ |
| 全部写完再审 | 终稿拼好后再一起看 | |
| 混合模式 | 关键段落逐段审，Methods/Results 直接跑 | |

**User's choice:** 逐段审阅（推荐）

### Q3: Agent 调用策略

| Option | Description | Selected |
|--------|-------------|----------|
| 单 Agent 分轮调用 | 同一个 writer-agent 分 4 轮对话分别写 4 段 | ✓ |
| 扩展 Agent role | 增加分段撰写和拼接能力 | |
| 不碰 Agent，纯 workflow 控制 | 不改 agent，workflow 层控制 | |

**User's choice:** 单 Agent 分轮调用（推荐）

### Q4: 上下文来源

| Option | Description | Selected |
|--------|-------------|----------|
| 自动读取项目数据 | 各段自动从项目目录读取所需数据 | ✓ |
| 你手动投喂 | 手动把分析结果贴给 writer-agent | |

**User's choice:** 自动读取项目数据（推荐）

### Q5: 篇幅

| Option | Description | Selected |
|--------|-------------|----------|
| 写到完整为止 | 不设限，写到内容完整 | ✓ |
| 大致字数目标 | 设目标字数 | |

**User's choice:** 写到完整为止（全文 >5000 字，语言流畅成段论述）

### Q6: Methods 来源

| Option | Description | Selected |
|--------|-------------|----------|
| Spec + analysis outputs | 自动生成 | |
| 自动生成 + 你修改 | 初稿后你审阅修改 | ✓ |

**User's choice:** 自动生成 + 你修改（推荐）

### Q7: 文献搜索

| Option | Description | Selected |
|--------|-------------|----------|
| 每段前自动跑 | 每段前 reference-agent 搜索文献 | ✓ |
| 不搜直接写 | writer-agent 直接用已有知识 | |
| 仅 Intro 和 Discussion 前搜 | 仅关键段落搜索 | |

**User's choice:** 每段前自动跑文献搜索（推荐）

---

## 引用去重策略

### Q1: 去重方式

| Option | Description | Selected |
|--------|-------------|----------|
| 自动去重 | 保留首次出现，后续改为"如前所述" | |
| 合并时人工审 | 全部保留，给重复列表你决定 | |
| 末尾统一 References 区 | 正文只标编号，自然去重 | ✓ |

**User's choice:** 末尾统一 References 区

### Q2: 引用格式

| Option | Description | Selected |
|--------|-------------|----------|
| Vancouver 编号制 | 正文 [1][2]，末尾列表 | ✓ |
| Harvard 作者年份制 | 正文 (Author, Year) | |

**User's choice:** Vancouver 编号制（推荐）

### Q3: 编号策略

| Option | Description | Selected |
|--------|-------------|----------|
| 全局统一编号 | 写任何段时查已有引用库，复用编号 | ✓ |
| 分段独立编号 | 各段独立编，合并时重排 | |

**User's choice:** 全局统一编号

### Q4: 引用量

| Option | Description | Selected |
|--------|-------------|----------|
| 常规学术量 | Intro 10-15, Methods 3-5, Results 0-3, Discussion 15-25 | ✓ |
| 写到够用为止 | 不限量 | |

**User's choice:** 常规学术量（推荐）

---

## 段间交叉引用

### Q1: 交叉引用处理

| Option | Description | Selected |
|--------|-------------|----------|
| 占位符 + 拼接时替换 | 写时用 {{Table1}}，拼时统一替换 | ✓ |
| 写完后人工补 | 人工逐一检查补充 | |
| 终稿后 AI 自动补 | 所有段写完后扫描全文补全 | |

**User's choice:** 占位符 + 拼接时替换（推荐）

### Q2: 图表编号

| Option | Description | Selected |
|--------|-------------|----------|
| 全局统一编号 | Table 1/2/3, Figure 1/2/3 按 IMRAD 顺序 | ✓ |
| 分段独立编号 | 各段独立编，拼时重排 | |

**User's choice:** 全局统一编号（推荐）

### Q3: Results 风格

| Option | Description | Selected |
|--------|-------------|----------|
| 描述 + 指向图表 | "Baseline characteristics were similar (Table 1)" | ✓ |
| 文字为主，表作附录 | Results 只写文字解读 | |

**User's choice:** 描述 + 指向图表（推荐）

---

## 终稿输出格式

### Q1: 输出格式

| Option | Description | Selected |
|--------|-------------|----------|
| Markdown | 纯 Markdown，带标题层级 | ✓ |
| DOCX | 可直接投稿 | |
| MD + 自动转 DOCX | 两个都要 | |

**User's choice:** Markdown（推荐）

### Q2: 文件组织

| Option | Description | Selected |
|--------|-------------|----------|
| 终稿 + 各段独立保留 | manuscript.md + sections/ 目录 | ✓ |
| 仅终稿 | 只输出完整终稿 | |
| 仅各段独立 | 只输出各段文件 | |

**User's choice:** 终稿 + 各段独立保留（推荐）

### Q3: 元数据

| Option | Description | Selected |
|--------|-------------|----------|
| YAML frontmatter | title, target_journal, word_count 等 | ✓ |
| 纯内容 | 无元数据 | |

**User's choice:** YAML frontmatter 元数据（推荐）

---

## Claude's Discretion

- 引用搜索的具体执行参数（库的选择、搜索策略）
- 占位符的具体命名模式和替换实现细节
- 各段 split 在 writer-agent 对话中的具体 prompt 分界策略

## Deferred Ideas

None
