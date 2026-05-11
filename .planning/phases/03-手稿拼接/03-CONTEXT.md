# Phase 3: 手稿拼接 - Context

**Gathered:** 2026-05-06
**Status:** Ready for planning

<domain>
## Phase Boundary

IMRAD 各段（Introduction/Methods/Results/Discussion）独立撰写引用后拼接为终稿。各段由 writer-agent 分轮调用完成，终稿拼接生成而非重写。全文 >5000 字，语言流畅成段论述。

</domain>

<decisions>
## Implementation Decisions

### 撰写流程

- **D-01 (顺序):** IMRAD 顺序流水线（Intro → Methods → Results → Discussion），每段写完 pause 用户审阅后再继续下一段
- **D-02 (Agent 模式):** 同一个 writer-agent，分 4 轮对话分别写 4 段，每轮只给该段需要的上下文。不扩展 writer-agent role，不改 agent 定义文件
- **D-03 (上下文来源):** 自动读取项目数据（spec → Methods 上下文，analysis outputs → Results 上下文，文献库 → Intro/Discussion 上下文）
- **D-04 (篇幅):** 不设段字数上限，但全文必须 >5000 字。语言要求流畅自然、成段论述（非 bullet point）
- **D-05 (Methods 来源):** 从 spec + analysis pipeline outputs 自动生成初稿，用户审阅时修改
- **D-06 (文献搜索):** 每段撰写前自动调用 reference-agent 搜索文献，为 writer-agent 提供引用资料

### 引用管理

- **D-07 (去重策略):** 末尾统一 References 区，正文标编号，自然去重
- **D-08 (引用格式):** Vancouver 编号制，正文 [1][2]，末尾列表
- **D-09 (编号策略):** 全局统一编号，共享引用库。写任何段时都查询已有引用，已存在就复用编号
- **D-10 (引用量):** 常规学术量：Intro 10-15 篇，Methods 3-5 篇，Results 0-3 篇，Discussion 15-25 篇

### 段间交叉引用

- **D-11 (交叉引用):** 写前段时用占位符（{{Table1}} {{MethodX}}），终稿拼接时统一替换为真实编号
- **D-12 (图表编号):** Table/Figure 全局统一编号，按 IMRAD 顺序（Table 1 in Methods, Table 2 in Results...）
- **D-13 (Results 风格):** 描述关键发现 + 指向对应图表（如 "Baseline characteristics were similar between groups (Table 1)"）

### 终稿输出格式

- **D-14 (文件格式):** Markdown
- **D-15 (文件组织):** `05_Manuscript/manuscript.md` 完整终稿 + `05_Manuscript/sections/` 下各段独立文件
- **D-16 (元数据):** manuscript.md 开头 YAML frontmatter：title, target_journal, word_count, reference_count

### Claude's Discretion

- 引用搜索的具体执行参数（库的选择、搜索策略）
- 占位符的具体命名模式和替换实现细节
- 各段 split 在 writer-agent 对话中的具体 prompt 分界策略

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 现有命令与工作流

- `commands/clinpub/writing.md` — Phase 3 现有命令入口
- `pipeline/workflows/writing.md` — 现有撰写工作流（需扩展分段+拼接逻辑）
- `pipeline/contexts/writing.md` — 现有撰写上下文配置

### Agent 合约

- `agents/writer-agent.md` — Writer Agent role 定义（分轮调用，暂不扩展）
- `agents/reference-agent.md` — Reference Agent（每段前自动搜索文献）

### 需求定义

- `.planning/REQUIREMENTS.md` — WRITE-01/WRITE-02 详细定义

### 项目输出目录规范

- `pipeline/references/agent-contracts.md` §Agent 输出目录矩阵 — `05_Manuscript` 目录为 writer-agent 写入区域

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- 薄命令入口模式：`commands/clinpub/writing.md` 已有 frontmatter + process 结构，可直接扩展
- Writer Agent (`agents/writer-agent.md`) 已完成整篇撰写逻辑，需调整支持分段调用
- Reference Agent 的文献搜索能力可直接复用

### Established Patterns

- Agent 轮次调用模式（参考 Phase 2 的 WAVE 子任务机制）：每轮独立调用，传递必要上下文
- 命令入口 frontmatter 中 `argument-hint` 和 `allowed-tools` 已有标准格式

### Integration Points

- `05_Manuscript/` 目录为 writer-agent 的输出目录（agent-contracts.md 定义）
- Literature 搜索结果需在 Reference 目录或 inline context 中传递给 writer-agent
- 用户审阅环节需要在每段完成后 pause workflow，等待用户反馈

</code_context>

<specifics>
## Specific Ideas

- 引用库用 JSON 文件维护全局引用列表，writer-agent 写各段时读写同一个引用库
- 各段独立文件命名：`sections/01-introduction.md`, `sections/02-methods.md`, `sections/03-results.md`, `sections/04-discussion.md`
- manuscript.md frontmatter 示例：`---\ntitle: ""\ntarget_journal: ""\nword_count: 0\nreference_count: 0\n---`

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

---

<expanded_scope>

## Phase 3 引用策略扩展（CITE-01, CITE-02）

**来源:** Phase 6 (引用策略) 于 2026-05-11 讨论后合并入 Phase 3

### 引用总量

- **D-17:** 引用总量为 30-55 篇范围制，不设硬性 50 篇目标，讨论时根据实际情况确定
- **D-18:** 各段保留 Phase 3 原有参考配比（Intro 10-15, Methods 3-5, Results 0-3, Discussion 15-25），但作为弹性建议，总量 30-55 为硬约束
- **D-19:** FlO-01（来自旧 Phase 6）规则写入 writing workflow 前置步骤

### 讨论时机

- **D-20:** 引用策略讨论发生在写手稿前（Phase 3 writing.md workflow 的前置步骤），而非作为一个独立 Phase
- **D-21:** 讨论内容涵盖各段引用数量、时间范围（近 5 年）、IF 偏好
- **D-22:** 讨论结果写入 `project_config.yml` 或共享引用库配置，供后续各段引用用

### 实施范围

- Phase 3 新增 plan `03-05-PLAN.md` 涵盖：
  - 引用策略参考文档（默认规则、讨论流程）
  - writing workflow 插入讨论步骤
  - reference-agent 搜索支持 IF/年份过滤参数

</expanded_scope>

*Phase: 03-手稿拼接*
*Context gathered: 2026-05-06 (expanded 2026-05-11 for citation strategy)*
