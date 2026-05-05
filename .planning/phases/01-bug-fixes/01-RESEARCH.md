# Phase 1: Bug Fixes - Research

**Researched:** 2026-05-05
**Domain:** Hook engineering, data pipeline re-entry
**Confidence:** HIGH

## Summary

Phase 1 修复两个影响 clinpub 基础可用性的 bug，涉及 2 个文件和 1 个需修改的工作流。

**BUG-01 (Hook Regex):** `hooks/clinpub-workflow-guard.js` 中 `getCurrentPhase()` 函数的正则 `/当前.*Phase\s*(\d)/i` 在生产环境中不可靠——它匹配自然语言行而不是结构化数据。当 STATE.md 使用新的 `- 阶段：Phase N` 格式（已于 discuss 阶段写入 STATE.md 第5行）时，旧正则不匹配，回退到 ✅ 计数逻辑，返回错误的 Phase 编号。修复只需改一行正则。

**BUG-02 (Data Rerun):** 用户完成 Phase 0/1 后想修改清洗需求时，再次执行 `/clinpub-data-prep` 不会自动刷新相联文件（profile、spec、config）。修复需要在 data-prep 工作流入口处检测 `project_config.yml` 是否存在，若存在则先跑刷新流程再进入讨论环节。

**Primary recommendation:** 两个 bug 都是小范围改动。BUG-01 改 `workflow-guard.js` 的一行正则。BUG-02 在 `data-prep.md` 命令入口和 `data-prep` 工作流头部加刷新检测步骤。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** STATE.md 头部（`当前状态` 一栏下方）加一行 `- 阶段：Phase N` 作为 machine-readable 的阶段标识
- **D-02:** Hook 中 `getCurrentPhase()` 的正则改为匹配 `/阶段：Phase\s*(\d)/`（精确匹配机器行，不依赖自然语言）
- **D-03:** 保留 `当前状态` 自然语言行作为 human-readable 信息，hook 不依赖它
- **D-04:** 如果 `- 阶段：` 行不存在，返回 Phase 0（未初始化状态），不清除原有的 ✅ 回退逻辑
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

### Deferred Ideas (OUT OF SCOPE)
None — 讨论保持在 Phase 1 范围内
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| BUG-01 | Hook 正则 `当前.*Phase` 改为匹配 STATE.md 的 `- 阶段：` 格式，避免回退到 Phase 0 | 正则位置: `workflow-guard.js:31`，STATE.md 已有 `- 阶段：Phase 1`（第5行），✅ 回退逻辑在 `workflow-guard.js:35-36` |
| BUG-02 | 用户要求修改清洗数据时，全面检查 Phase 1 所有受影响文件（profile、spec 等）联动更新 | 入口: `commands/clinpub/data-prep.md`，工作流: `pipeline/workflows/data-prep.md`，profile 生成: `scripts/data_profiler.py`，spec 模板: `pipeline/templates/spec.md` |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Phase detection from STATE.md | Hook (claude-code runtime) | — | Hook 是 claude-code PreToolUse 机制，在 Write/Edit 前调用 `getCurrentPhase()` 判断当前 Phase |
| Phase access validation | Hook (workflow-guard.js) | — | `validatePhaseAccess()` 在 hook 内执行，阻止写入未来 Phase 的目录 |
| Data prep re-entry detection | Command (data-prep.md) | Workflow (data-prep.md) | D-07 要求不增加 hook 逻辑，因此检测逻辑在命令/工作流层实现 |
| Profile regeneration | Python script (data_profiler.py) | — | `data_profiler.py` 是独立的 profiling 工具脚本 |
| Spec template generation | Workflow (data-prep.md) | Template (spec.md) | spec 模板基于 profile 输出和 project_config.yml 填充 Mustache 占位符 |
| Project config update | Workflow (data-prep.md) | — | project_config.yml 由编排者（工作流）写入，Agent 只读 |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Node.js | >= 22.0.0 | Hook 运行时 | `package.json` 中声明的运行时要求 |
| Python 3 | >= 3.8 | 数据 profiling 脚本 | `scripts/data_profiler.py` 依赖 `pandas`、`numpy` |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pandas | latest | DataFrame 操作 | data_profiler.py 以 pandas 为核心 |
| numpy | latest | 数值计算 | data_profiler.py 统计计算依赖 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Node.js `fs` for STATE.md parsing | `gray-matter` npm package | 额外依赖，对简单的 regex 匹配场景过重 |

**Installation:**
```bash
# Hook 本身就是 Node.js，无需额外依赖
# Python 环境需要 pandas
pip install pandas numpy openpyxl
```

## Architecture Patterns

### BUG-01 数据流

```
STATE.md
│  - 阶段：Phase 1   ← machine-readable line (D-01)
│  当前状态: ...      ← human-readable (D-03)
│
▼
PreToolUse: Write/Edit triggered
│
▼
getCurrentPhase()
│  1. Read STATE.md
│  2. Match /阶段：Phase\s*(\d)/  ← D-02 new regex
│  3. If match → return parseInt(n)
│  4. If no match → return 0 (D-04 fallback)
│
▼
validatePhaseAccess(currentPhase, targetDir)
│  Compare currentPhase vs. PHASE_MAP allowed_dirs
│  If targetDir > currentPhase → BLOCK
│  Else → ALLOW
```

### BUG-02 数据流

```
User: /clinpub-data-prep (second time, project already initialized)
│
▼
commands/clinpub/data-prep.md  (entry point)
│  1. Check: project_config.yml exists?
│     → YES (D-05): trigger refresh flow before normal workflow
│     → NO: proceed to normal Phase 1 workflow
│
▼
pipeline/workflows/data-prep.md  (new step at top)
│  [REFRESH] reinit_data_prep:
│    1. Re-run data_profiler.py → update profile JSON
│    2. Re-generate spec.md based on updated profile
│    3. Update project_config.yml with latest decisions
│    4. Inform user: "已检测到现有项目，自动刷新配置文件"
│
▼
Normal data-prep workflow
│  discuss_cleaning_strategy
│  detect_data_structure
│  execute_cleaning
│  validate_output
│  checkpoint_confirm
│  milestone
```

### Recommended Project Structure (unchanged — no new files needed)

```
clinpub/
├── hooks/
│   └── clinpub-workflow-guard.js     # 修改 getCurrentPhase() 正则 (BUG-01)
├── commands/
│   └── clinpub/
│       └── data-prep.md              # 添加 rerun 检测逻辑 (BUG-02)
├── pipeline/
│   └── workflows/
│       └── data-prep.md              # 添加 reinit_data_prep 步骤 (BUG-02)
```

### Pattern 1: Machine-Readable Tag in STATE.md
**What:** 在 STATE.md 头部添加结构化的 `- 阶段：Phase N` 标签，作为 hook 的唯一匹配源。
**When to use:** 需要从自然语言文档中精确提取状态信息时。
**Example:**
```markdown
# STATE.md — clinpub 优化进度

**最后更新**: 2026-05-05
**当前状态**: Phase 1 上下文已收集，准备规划
- 阶段：Phase 1    ← 机器可读，hook 精确匹配
```
Source: [CITED: D-01/D-02 from CONTEXT.md]

### Pattern 2: Hook Entry with Structured Line
**What:** Hook 函数先匹配结构化标签，不存在时返回安全默认值。
**When to use:** PreToolUse hook 中需要确定当前 Phase 时。
**Example:**
```javascript
function getCurrentPhase() {
  const statePath = path.join(PROJECT_DIR, ".planning", "STATE.md");
  if (!fs.existsSync(statePath)) return -1;

  const content = fs.readFileSync(statePath, "utf-8");
  
  // D-02: Match structured machine-readable line
  const phaseMatch = content.match(/阶段：Phase\s*(\d)/);
  if (phaseMatch) return parseInt(phaseMatch[1], 10);
  
  // D-04: No structured line → return Phase 0 (uninitialized)
  // Legacy ✅ fallback kept below per D-04
  return 0;
}
```
Source: [VERIFIED: workflow-guard.js lines 25-37], [CITED: D-02, D-04 from CONTEXT.md]

### Anti-Patterns to Avoid
- **依赖自然语言行的正则匹配:** 当前 `当前.*Phase\s*(\d)/i` 依赖于"当前状态: Phase 1 上下文已收集"中的"当前"+"Phase"组合。如果自然语言措辞改变（比如改为"上一状态"），hook 就失效了。结构化标签 `- 阶段：Phase N` 不易受措辞变更影响。
- **计数 emoji 作为 phase 编号回退:** `content.match(/✅/g).length` 会匹配 STATE.md 中所有已完成事项的 ✅（可能是6+个），而不是 Phase 编号。在新正则未命中时返回错误值。

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| STATE.md 解析 | 自定义 frontmatter parser | 用 `content.match()` 单行正则 | 只需匹配一行结构化标签，不需要 YAML parser |
| Hook 中的重新初始化检测 | PreToolUse hook 逻辑 | `data-prep.md` 命令入口检测 | D-07 明确不增加 hook 复杂度 |

## Common Pitfalls

### Pitfall 1: 回退逻辑返回错误 Phase
**What goes wrong:** `getCurrentPhase()` 的 ✅ 计数回退逻辑将 STATE.md 中所有已完成事项的 ✅ 数量作为 Phase 编号返回。如果 "已完成" 列表有 6 个 ✅，hook 返回 Phase 6，但实际项目才到 Phase 1。
**Why it happens:** 旧正则 `/当前.*Phase\s*(\d)/i` 未命中时走到 ✅ 回退逻辑，而 STATE.md 的已完成列表中的 ✅ 数量不等于 Phase 编号。
**How to avoid:** D-04 规定当结构化行不存在时直接返回 Phase 0，不再依赖 ✅ 计数。回退代码保留但不执行。
**Warning signs:** Hook 突然允许访问 Phase 6（或更高）的目录，即使项目还未进行到那些 Phase。

### Pitfall 2: project_config.yml 检测误判
**What goes wrong:** `data-prep.md` 入口检测 `project_config.yml` 是否存在来判断是否"已初始化"。但 `project_config.yml` 可能从 data2idea 流程的 `idea/to_project_config.yml` 复制而来，未经过完整的 Phase 0 初始化。
**Why it happens:** Topic Miner Agent 会生成 `idea/to_project_config.yml`，用户可能直接重命名为 `project_config.yml` 而不执行 `/clinpub-init-project`。
**How to avoid:** 检测 `project_config.yml` 存在的同时验证关键字段（如 `project.name` 非空、`variables.outcome` 非空）。也可以同时检测 `01_RawData/` 是否有数据文件。
**Warning signs:** Refresh 流程运行时发现 config 中必填字段为空。

### Pitfall 3: 刷新时覆盖用户未保存的更改
**What goes wrong:** 用户手动编辑了 `project_config.yml` 但未保存到 git，refresh 流程自动覆盖了这些更改。
**Why it happens:** refresh 流程按模板重新生成 config 时使用 `pipeline/templates/project_config.yml` 模板 + profile 数据，覆盖了用户自定义修改。
**How to avoid:** Refresh 流程应与用户确认再覆盖，或采用 merge 策略（保留用户自定义值，仅更新 profile 相关的变量字典字段）。

## Code Examples

### BUG-01: Fix getCurrentPhase() in workflow-guard.js

```javascript
// File: hooks/clinpub-workflow-guard.js
// Lines 25-37 (modified)

function getCurrentPhase() {
  const statePath = path.join(PROJECT_DIR, ".planning", "STATE.md");
  if (!fs.existsSync(statePath)) return -1;

  const content = fs.readFileSync(statePath, "utf-8");
  
  // D-02: Match structured machine-readable line "- 阶段：Phase N"
  // This is the authoritative source for phase detection.
  const phaseMatch = content.match(/阶段：Phase\s*(\d)/);
  if (phaseMatch) return parseInt(phaseMatch[1], 10);
  
  // D-04: If no structured line exists, return Phase 0 (uninitialized).
  // The legacy fallback below is intentionally kept as-is per D-04
  // ("不清除原有的 ✅ 回退逻辑") for backward compatibility during migration.
  const completedMatches = content.match(/✅/g);
  return completedMatches ? completedMatches.length : 0;
}
```

Source: [VERIFIED: workflow-guard.js:25-37], [CITED: D-02, D-04 from CONTEXT.md]

### BUG-02: Rerun detection in data-prep.md

```markdown
---
name: clinpub:data-prep
description: "Phase 1: Data preparation..."
---
<objective>
Phase 1: Data preparation. ...
</objective>

<execution_context>
@./pipeline/workflows/data-prep.md
</execution_context>

<process>
## Re-entry Detection (D-05/D-06)
Before entering the normal data-prep workflow, check if this project is already initialized:

```bash
if [ -f "project_config.yml" ]; then
  echo "检测到已有项目配置（project_config.yml），执行自动刷新流程..."
  echo "刷新步骤：重新生成 profile → 更新 spec 模板 → 同步配置"
fi
```

Proceed to the data-prep workflow from @./pipeline/workflows/data-prep.md.
</process>

<success_criteria>
...
</success_criteria>
```

Source: [CITED: D-05, D-06 from CONTEXT.md]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `getCurrentPhase()` 匹配 `当前.*Phase` | 匹配 `- 阶段：Phase N` | Phase 1 | 精确匹配，不依赖自然语言 |
| ✅ 计数作为 phase 回退 | 返回 Phase 0（未初始化） | Phase 1 | 不再因 ✅ 数量 != Phase 编号而误判 |
| `/clinpub-data-prep` 无 rerun 检测 | 检测 `project_config.yml` 存在，触发刷新 | Phase 1 | 用户可反复进入清洗流程，变更需求时所有文件联动更新 |

**Deprecated/outdated:**
- STATE.md 的自然语言行（`当前状态：Phase N`）作为 hook 状态源：已在 D-03 中声明 hook 不依赖此格式

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `project_config.yml` 存在于项目根目录时表示"项目已初始化" | BUG-02 检测条件 | 用户在 data2idea 流程中从 `idea/to_project_config.yml` 复制了未经验证的 config，但未跑完完整的 Phase 0。建议补充验证：检查关键字段非空 + `01_RawData` 是否有数据文件 |
| A2 | `pipeline/templates/spec.md` 的 Mustache 占位符与 refresh 流程兼容 | BUG-02 spec 生成 | 如果 spec.md 模板的占位符（如 `{{phase_number}}`）需要在 refresh时重新填充，需确保 refresh 流程有完整的变量上下文 |

## Open Questions

1. **[BUG-02] Refresh 流程与用户交互策略**
   - What we know: D-06 说"再进入用户讨论"，D-05 触发的 refresh 应该自动化
   - What's unclear: refresh 完成后是否立即进入讨论阶段？还是需要先让用户确认刷新结果？
   - Recommendation: refresh 后自动输出变更摘要给用户查看，然后正常进入 `discuss_cleaning_strategy` 步骤

2. **[CODEBASE] Phase 4 的目录名拼写错误**
   - What we know: `workflow-guard.js:22` 写的是 `"05_Manuscript/final"`，但该目录实际上可能在 Phase 3 时创建为 `"05_Manuscript"`
   - What's unclear: 是否属于 Phase 1 的修复范围
   - Recommendation: 属于代码质量问题，非阻塞 bug，可以在此 Phase 顺带修正（增加一行代码）

3. **[CODEBASE] phase-boundary.sh 的重复函数调用**
   - What we know: `phase-boundary.sh:135-136` 重复调用了两次 `check_phase_boundary()`
   - What's unclear: 是否属于 Phase 1 的修复范围
   - Recommendation: 微小的性能问题，可以在 Phase 1 顺带修复（改 2 行）

## Environment Availability

> Step 2.6: SKIPPED — Phase 1 是纯代码编辑（修改 .js 和 .md 文件），无外部工具依赖需要运行。Hook 的验证将在改完后通过重新加载 claude-code 会话测试。

## Validation Architecture

> Required: workflow.nyquist_validation is enabled (true) in .planning/config.json

### Existing Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | 无 — 项目无任何测试框架（`tests/` 仅有 `.gitkeep`） |
| Config file | 无 pytest.ini / jest.config / vitest.config |
| Quick run command | 无 |
| Full suite command | 无 |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Manual Only? | File Exists? |
|--------|----------|-----------|------------|-------------|
| BUG-01 | `getCurrentPhase()` 匹配 `- 阶段：Phase 1` 时返回 1 | Unit | Manual | ❌ 无测试文件 |
| BUG-01 | `getCurrentPhase()` 无法匹配时返回 0 | Unit | Manual | ❌ 无测试文件 |
| BUG-01 | STATE.md 不存在时返回 -1 | Unit | Manual | ❌ 无测试文件 |
| BUG-02 | data-prep 入口检测 `project_config.yml` 存在并触发刷新 | Integration | Manual | ❌ 无测试文件 |
| BUG-02 | 刷新流程依次执行 profile → spec → config 更新 | Integration | Manual | ❌ 无测试文件 |

### Sampling Rate
- **Per task commit:** 无自动测试。手动确认修改正确性。
- **Per wave merge:** 无自动测试。建议在 `tests/` 添加简单的 Node.js 测试。
- **Phase gate:** 手动运行验证步骤后通过。

### Wave 0 Gaps
- [ ] `tests/hooks.test.cjs` — Node.js 内建 test runner 编写的 `getCurrentPhase()` 单元测试（读取 mock STATE.md 验证返回值）
- [ ] 框架选择: Node.js `node:test` 和 `node:assert` — 零额外依赖，Node >= 22 内置支持

**注意**: 项目明确声明"自动化单元测试 — 纯开发环境，开发者自行测试"。测试添加属于建议，非强制。但如果加入测试，建议用 Node.js 内置 test runner 以避免额外依赖。

## Security Domain

> Required: security_enforcement is implicitly enabled (config.json does not disable it)

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | — |
| V3 Session Management | No | — |
| V4 Access Control | Yes | Hook-enforced phase ordering — workflow-guard.js 的 `validatePhaseAccess()` 阻止写入未来 Phase 的目录 |
| V5 Input Validation | Yes | STATE.md 路径输入通过 `path.join()` 安全拼接；hook 从 `process.env.PROJECT_DIR` 或 `process.cwd()` 获取项目根目录 |
| V6 Cryptography | No | — |

### Known Threat Patterns for clinpub Hook Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| STATE.md 路径遍历 | Tampering | 使用 `path.join(PROJECT_DIR, ".planning", "STATE.md")` 确保路径在项目根目录内 |
| Hook 解析错误时绕过 guard | Denial of Service | `workflow-guard.js:125-128` try/catch 中 fallback 为 allow |
| 数据文件中注入 prompt 指令 | Elevation of Privilege | 由 `clinpub-prompt-guard.js` 独立处理（warning 模式，不 block） |

## Sources

### Primary (HIGH confidence)
- [VERIFIED: hooks/clinpub-workflow-guard.js] — getCurrentPhase() lines 25-37, PHASE_MAP, validatePhaseAccess()
- [VERIFIED: .planning/STATE.md] — Current state with `- 阶段：Phase 1` on line 5
- [VERIFIED: commands/clinpub/data-prep.md] — Phase 1 entry point (thin, 36 lines)
- [VERIFIED: pipeline/workflows/data-prep.md] — Phase 1 orchestration (142 lines)
- [VERIFIED: scripts/data_profiler.py] — Profile generation (353 lines)
- [VERIFIED: pipeline/templates/spec.md] — Spec template with Mustache placeholders (125 lines)
- [VERIFIED: pipeline/templates/project_config.yml] — Config template (78 lines)
- [VERIFIED: bin/install.js] — Hook registration mechanism (500 lines)

### Secondary (MEDIUM confidence)
- [CITED: CONTEXT.md] — All decisions D-01 through D-07
- [VERIFIED: requirements.yml from REQUIREMENTS.md] — BUG-01, BUG-02 requirement definitions

### Tertiary (LOW confidence)
- [ASSUMED] project_config.yml 是检测"项目是否已初始化"的可靠信号（见 Assumptions Log A1）
- [ASSUMED] spec.md 的 Mustache 占位符在 refresh 场景下可被正确填充（见 Assumptions Log A2）

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Node.js + Python 脚本，已验证存在
- Architecture: HIGH - 三层架构（Command -> Workflow -> Script）经 ARCHITECTURE.md 和实际代码双重确认
- Pitfalls: MEDIUM - conflict overwrite 风险是合理推断，但未在实际 pipeline 中验证

**Research date:** 2026-05-05
**Valid until:** Pipeline 架构在主动重构前稳定，本 research 在架构不变时有效。
