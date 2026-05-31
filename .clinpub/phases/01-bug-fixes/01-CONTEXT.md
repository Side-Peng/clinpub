# Phase 1: Bug Fixes - Context

**Gathered:** 2026-05-05
**Status:** Ready for planning

<domain>
## Phase Boundary

修复影响 clinpub 基础可用性的两个 bug：
1. Hook 正则在 STATE.md 写 `- 阶段：Phase N` 时正确识别，不回退到 Phase 0
2. 用户修改清洗数据需求时，Phase 1 所有关联文件联动更新

</domain>

<decisions>
## Implementation Decisions

### BUG-01：STATE.md 阶段标识格式

- **D-01:** STATE.md 头部（`当前状态` 一栏下方）加一行 `- 阶段：Phase N` 作为 machine-readable 的阶段标识
- **D-02:** Hook 中 `getCurrentPhase()` 的正则改为匹配 `/阶段：Phase\s*(\d)/`（精确匹配机器行，不依赖自然语言）
- **D-03:** 保留 `当前状态` 自然语言行作为 human-readable 信息，hook 不依赖它
- **D-04:** 如果 `- 阶段：` 行不存在，返回 Phase 0（未初始化状态），不清除原有的 ✅ 回退逻辑

### BUG-02：数据联动更新机制

- **D-05:** 联动更新通过命令入口触发：用户执行 `/clinpub-data-prep`（修改清洗需求）时，检测项目是否已初始化（`project_config.yml` 是否存在）
- **D-06:** 如果已初始化，自动执行全链路文件刷新流程再进入用户讨论：
  - 重新运行 profile（更新变量字典）
  - 重新生成 spec 模板（更新分析规范）
  - 同步更新 project_config.yml
- **D-07:** 不增加 PreToolUse hook 逻辑（避免不必要的 hook 复杂度）

### Claude's Discretion
- STATE.md 中 `- 阶段：` 行的精确插入位置
- 全链路刷新时中间文件的具体生成逻辑
- 刷新流程中与用户交互的策略

</decisions>

<specifics>
## Specific Ideas

- BUG-01 的两个相关代码位置：
  - `hooks/clinpub-workflow-guard.js` 第25-37行（`getCurrentPhase()` 函数）
  - `.clinpub/STATE.md`（需要新增阶段标识行的文件）
- BUG-02 的关联文件：
  - `pipeline/templates/project_config.yml`（项目配置模板）
  - `scripts/data_profiler.py` 输出的 profile
  - `pipeline/templates/spec.md`（分析规范）

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Bug 1：Hook 正则
- `hooks/clinpub-workflow-guard.js` — 需要修复的 hook 文件，`getCurrentPhase()` 在第25-37行
- `.clinpub/STATE.md` — 需要新增 `- 阶段：Phase N` 行

### Bug 2：数据联动更新
- `commands/clinpub/data-prep.md` — 数据清洗命令入口，联动更新的触发点
- `pipeline/workflows/data-prep.md` — 清洗流程定义，需要嵌入刷新步骤
- `scripts/data_profiler.py` — profile 生成脚本
- `pipeline/templates/spec.md` — 分析规范模板
- `pipeline/templates/project_config.yml` — 项目配置模板

</canonical_refs>

<code_context>
## Existing Code Insights

### 可复用代码
- `getCurrentPhase()` 函数在 `workflow-guard.js` 中实现，修改范围小，只需改正则和加回退策略

### 问题代码
- 第31行 `const phaseMatch = content.match(/当前.*Phase\s*(\d)/i);` — 需要改为匹配 `- 阶段：Phase N`
- 第32-36行 fallback 逻辑 — 需要对 count 做合理性判断（如 count===0 才返回 0，否则继续返回未知状态）

### 集成点
- STATE.md 更新时（包括 `/gsd-next`、`/gsd-execute-phase` 等命令）需要同步维护 `- 阶段：Phase N` 行
- data-prep 命令入口处需要检测 `project_config.yml` 是否已存在来决定是否触发刷新

</code_context>

<deferred>
## Deferred Ideas

None — 讨论保持在 Phase 1 范围内

</deferred>

---

*Phase: 01-bug-fixes*
*Context gathered: 2026-05-05*
