# Phase 2: 断点续做 - Context

**Gathered:** 2026-05-05
**Status:** Ready for planning

<domain>
## Phase Boundary

支持工作中断后恢复，无需从头摸索上下文。添加三个交互优化功能：
1. `/clinpub-do` — 读取工作区状态自动路由到合适的命令
2. `/clinpub-next-step` — 自动推进到下一 Phase 或 Wave
3. Phase/Wave 结束时自动提示 clear 压缩上下文，然后进入下一阶段

</domain>

<decisions>
## Implementation Decisions

### `/clinpub-do` 路由逻辑

- **D-01:** 命令无参数调用时，报告当前状态摘要 + 建议命令，用户确认后执行
- **D-02:** 支持自然语言输入（如 `/clinpub-do 我想改清洗逻辑`），NL 优先于状态检测，直接按意图路由
- **D-03:** 路由依据三合一：STATE.md 状态 + 工件检测 + 可选的 NL 输入
- **D-04:** 输入 NL 但推断不出明确意图时，回退到无参行为（报告摘要）

### `/clinpub-next-step` 推进策略

- **D-05:** 推进粒度自动判断——当前 Phase 还有未完成的 Wave 就推进到下一 Wave，全部完成就推进到下一 Phase
- **D-06:** 推进前先验证当前步骤是否完成（SUMMARY.md 是否存在等），未完成则提示用户
- **D-07:** 每个 Wave/Phase 结束时通过 SUMMARY.md + STATE.md/ROADMAP.md 更新来建立检查点，不需要额外 verify 步骤

### Clear 提示

- **D-08:** 在 STATE.md 的"下一步"部分和各 Phase 命令末尾统一输出（executor 负责在 SUMMARY 后追加）
- **D-09:** 提示内容包含三要素：`/clear` + 下一条命令 + 进度总结

### Claude's Discretion
- `/clinpub-do` 中工件检测的具体逻辑和优先级顺序
- Clear 提示的精确措辞格式
- 时序处理（如推进过程中遇到中途错误的重试策略）

</decisions>

<specifics>
## Specific Ideas

- `/clinpub-do` 的实现参考现有命令模式（`commands/clinpub/*.md` 薄入口格式）
- `/clinpub-next-step` 读 STATE.md 的 `- 阶段：Phase N` + ROADMAP.md 的 Plan checkboxes，找第一个未完成的阶段
- Clear 提示在 STATE.md 的 `## 下一步` 节中自动生成，同时各命令末尾输出

</specifics>

<canonical_refs>
## Canonical References

### 命令模式
- `commands/clinpub/clinpub.md` — 现有命令入口格式和结构
- `commands/clinpub/data-prep.md` — Phase 1 命令入口（带重新进入检测）
- `commands/clinpub/init-project.md` — Phase 0 薄命令入口示例

### 状态跟踪
- `.planning/STATE.md` — Phase 跟踪格式，`- 阶段：Phase N` 标识行
- `.planning/ROADMAP.md` — Phase/Wave 完成状态检查

### 需求定义
- `.planning/REQUIREMENTS.md` — NEXT-01/NEXT-02/NEXT-03 详细定义

</canonical_refs>

<code_context>
## Existing Code Insights

### 可复用模式
- 薄命令入口模式：`frontmatter` + `<objective>` + `<process>` + `<success_criteria>` 结构
- STATE.md `- 阶段：Phase N` 行作为 machine-readable 的阶段标识
- ROADMAP.md 中 Plan 级别的 `[x]`/`[ ]` checkbox 完成状态标记

### 集成点
- `/clinpub-do` 需要读取 STATE.md 和 ROADMAP.md 来确定当前状态
- `/clinpub-next-step` 需要写入 STATE.md 和 ROADMAP.md 来推进进度
- Clear 提示需要在各命令末尾和 STATE.md 中同时维护

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-断点续做*
*Context gathered: 2026-05-05*
