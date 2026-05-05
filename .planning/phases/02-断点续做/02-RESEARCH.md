# Phase 2: 断点续做 - Research

**Researched:** 2026-05-05
**Domain:** Command routing, state detection, phase advancement
**Confidence:** HIGH

## Summary

Phase 2 为 clinpub 添加三个交互优化命令：`/clinpub-do`（自动路由）、`/clinpub-next-step`（自动推进）、以及 Phase/Wave 结束时的 clear 提示。核心挑战在于：如何可靠地读取工作区状态并做出正确的路由/推进决策。

代码库扫描发现三个关键复用基础：
1. **已有的状态检测代码** — `phase-boundary.sh` 已实现了按 Phase 检查工件存在性的逻辑（cleaned.csv、04_Outputs/ 等），可直接复用或参考其检测模式。
2. **命令入口格式固定** — 所有 8 个命令均遵循 `frontmatter` + `<objective>` + `<execution_context>` + `<process>` + `<success_criteria>` 结构。`data-prep.md` 已有"重新进入检测"模式，可作为 `/clinpub-do` 路由逻辑的实现模板。
3. **Wave 进度可通过 project_config.yml 追踪** — `analysis_plan.waves` 字段已定义了 Wave 结构。ROADMAP.md 使用 `[x]`/`[ ]` 标记 Plan 完成度。

**Primary recommendation:** 创建两个新命令文件，复用已有工件检测模式，通过 STATE.md 的 `- 阶段：Phase N` 行 + 工件检测 + 可选的 NL 输入三合一做路由决策。Clear 提示集成到 STATE.md 的 `## 下一步` 节和各命令末尾。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** 命令无参数调用时，报告当前状态摘要 + 建议命令，用户确认后执行
- **D-02:** 支持自然语言输入（如 `/clinpub-do 我想改清洗逻辑`），NL 优先于状态检测，直接按意图路由
- **D-03:** 路由依据三合一：STATE.md 状态 + 工件检测 + 可选的 NL 输入
- **D-04:** 输入 NL 但推断不出明确意图时，回退到无参行为（报告摘要）
- **D-05:** 推进粒度自动判断——当前 Phase 还有未完成的 Wave 就推进到下一 Wave，全部完成就推进到下一 Phase
- **D-06:** 推进前先验证当前步骤是否完成（SUMMARY.md 是否存在等），未完成则提示用户
- **D-07:** 每个 Wave/Phase 结束时通过 SUMMARY.md + STATE.md/ROADMAP.md 更新来建立检查点，不需要额外 verify 步骤
- **D-08:** 在 STATE.md 的"下一步"部分和各 Phase 命令末尾统一输出（executor 负责在 SUMMARY 后追加）
- **D-09:** 提示内容包含三要素：`/clear` + 下一条命令 + 进度总结

### Claude's Discretion
- `/clinpub-do` 中工件检测的具体逻辑和优先级顺序
- Clear 提示的精确措辞格式
- 时序处理（如推进过程中遇到中途错误的重试策略）

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| NEXT-01 | 添加 `/clinpub-do` 命令，读取工作区状态自动路由到合适的命令 | STATE.md 解析模式已验证（workflow-guard.js:31），工件检测模式已验证（phase-boundary.sh:73-104），命令入口格式已验证（commands/clinpub/*.md） |
| NEXT-02 | 添加 `/clinpub-next-step` 命令，自动推进到下一 Phase 或 Wave | ROADMAP.md `[x]`/`[ ]` 模式已确认（Phase 1 plans），Wave 结构在 `project_config.yml` 的 `analysis_plan.waves` 中定义，SUMMARY.md 模式在 agent-contracts.md 中定义 |
| NEXT-03 | Phase 和 Wave 结束时自动提示 clear 压缩上下文，然后进入下一阶段 | STATE.md `## 下一步` 节已有占位格式（第55-60行），checkpoint.md 定义了完成时的 milestone 流程 |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| `/clinpub-do` 状态读取 | Command (clinpub-do.md) | — | D-03 要求三合一读取，命令入口层最合适 |
| `/clinpub-do` NL 意图推断 | Command (clinpub-do.md) | — | NL 解析在命令文本中直接处理，无外部依赖 |
| `/clinpub-do` 路由决策 | Command (clinpub-do.md) | — | 路由逻辑完全由命令的 `<process>` 节控制 |
| `/clinpub-next-step` 完成验证 | Command (clinpub-next-step.md) | — | D-06 要求推进前验证完成状态 |
| `/clinpub-next-step` STATE.md 更新 | Command (clinpub-next-step.md) | — | D-07 要求 Writes STATE.md/ROADMAP.md |
| `/clinpub-next-step` ROADMAP.md 更新 | Command (clinpub-next-step.md) | — | D-07 要求写入 ROADMAP.md 更新完成状态 |
| Clear 提示生成 | Command (各命令末尾) | STATE.md (## 下一步) | D-08 要求统一输出 + D-09 三要素 |
| Wave 完成状态记录 | clinpub-executor (SUMMARY.md) | project_config.yml (analysis_plan) | D-07 明确 executor 负责在 SUMMARY 后追加 |
| 工件存在性检测 | Command (clinpub-do.md) | phase-boundary.sh (复用模式) | phase-boundary.sh:73-104 已有各 Phase 的工件检测逻辑 |

## Standard Stack

### Core

Phase 2 不引入新依赖。所有功能在现有 stack（纯 .md 命令 + 文件系统读取/写入）上实现。

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| 无新依赖 | — | — | 所有操作在命令入口文件内完成（读 STATE.md/ROADMAP.md/project_config.yml + 写 STATE.md/ROADMAP.md） |

### Supporting

| Pattern | Source | Purpose |
|---------|--------|---------|
| `content.match(/阶段：Phase\s*(\d)/)` | `hooks/clinpub-workflow-guard.js:31` | 从 STATE.md 读取当前 Phase 编号 |
| `grep -q "Phase N.*✅\|Phase N.*Complete"` | `hooks/clinpub-phase-boundary.sh:48` | 检查 Phase 完成状态 |
| `-f "02_PreprocessedData/data/cleaned.csv"` | `hooks/clinpub-phase-boundary.sh:84` | 检测 Phase 1 完成后产生的关键工件 |
| `-d "04_Outputs"` + `-nz "$(ls ...)"` | `hooks/clinpub-phase-boundary.sh:90` | 检测 Phase 2 是否有分析输出 |
| `-f "05_Manuscript/manuscript.md"` | `hooks/clinpub-phase-boundary.sh:96` | 检测 Phase 3 是否有手稿 |
| `analysis_plan.waves` 字段 | `pipeline/templates/project_config.yml:41-58` | 追踪 Wave 进度 |
| `[x]` / `[ ]` checkbox | `.planning/ROADMAP.md` | 追踪 Plan 完成状态 |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| 纯 .md 文本命令 | YAML frontmatter + 外部脚本 | 纯文本适合 Claude Code 直接编辑，外部脚本增加复杂度 |
| 自建工件检测 | 复用 phase-boundary.sh 作为库 | phase-boundary.sh 是 Bash hook，不适合直接 source；复用其检测模式更实际 |

## Architecture Patterns

### Phase 2 三个命令的架构关系

```
┌─────────────────────────────┐
│       /clinpub-do            │  ← 新命令：自动路由
│  读取 STATE.md + 工件 + NL   │
│  → 输出状态摘要 + 建议命令    │
└──────────┬──────────────────┘
           │ 路由到：
           ▼
┌─────────────────────┐   ┌─────────────────────────┐
│ /clinpub-init-project │   │  /clinpub-data-prep      │
│ (Phase 0)            │   │  (Phase 1, 含重入检测)    │
├─────────────────────┤   ├─────────────────────────┤
│ /clinpub-analysis     │   │  /clinpub-writing        │
│ (Phase 2, 含 Wave)   │   │  (Phase 3, 含引用)       │
├─────────────────────┤   ├─────────────────────────┤
│ /clinpub-review       │   │  /clinpub-next-step      │
│ (Phase 4)            │   │  (自动推进命令)          │
└─────────────────────┘   └─────────────────────────┘
                                    ▲
                                    │
┌─────────────────────────────┐    │
│      /clinpub-next-step      │────┘  ← 新命令：自动推进
│  验证完成 → 推进 → 更新状态   │
│  粒度判断: Wave vs Phase     │
└─────────────────────────────┘

Clear 提示（D-09 三要素）：
在各命令末尾 + STATE.md「下一步」统一输出
```

### `/clinpub-do` 路由决策树

```
用户输入 /clinpub-do [NL参数]
         │
         ├── NL 参数存在? ──YES──→ 尝试 NL 意图推断
         │                              │
         │                          ┌── 成功推断 → 直接路由到对应命令
         │                          └── 推断失败 → 回退到无参行为
         │
         └── 无参数 ──→ 读取 STATE.md + 工件检测
                              │
                    ┌── 检测结果 ──────────────────┐
                    │                               │
          STATE.md 不存在                 STATE.md 存在
               │                               │
          路由到 init-project           ┌─ 读取 `- 阶段：Phase N`
          (项目未初始化)                │
                                        │
                              ┌── Phase 0 ──→ project_config.yml 存在?
                              │               ├── YES → 建议命令行: 继续 Phase 0? 进入 Phase 1?
                              │               └── NO  → 建议 /clinpub-init-project
                              │
                              ├── Phase 1 ──→ cleaned.csv 存在?
                              │               ├── YES → 建议 /clinpub-data-prep (重入刷新)
                              │               └── NO  → 建议 /clinpub-data-prep (继续清洗)
                              │
                              ├── Phase 2 ──→ 04_Outputs/ 非空?
                              │               ├── YES → 检查 Wave 是否全部完成
                              │               │         ├── 有未完成 Wave → 继续分析
                              │               │         └── 全部完成 → 建议下一 Wave 或 Phase 3
                              │               └── NO  → 建议 /clinpub-analysis
                              │
                              ├── Phase 3 ──→ manuscript.md 存在?
                              │               ├── YES → 建议 /clinpub-writing (继续)
                              │               └── NO  → 建议 /clinpub-writing
                              │
                              └── Phase 4 ──→ review 完成?
                                                ├── YES → 全部完成
                                                └── NO  → 建议 /clinpub-review

路由后: 输出状态摘要 + 建议命令，用户确认后执行
```

### `/clinpub-next-step` 推进策略

```
用户输入 /clinpub-next-step
    │
    ▼
1. 读取 STATE.md: 当前 Phase + 进度
   读取 ROADMAP.md: Phase/Wave 完成状态
    │
    ▼
2. 验证当前步骤完成:
    ├── Phase 0: project_config.yml 关键字段非空?
    ├── Phase 1: cleaned.csv 存在?
    ├── Phase 2: 当前 Wave 的 SUMMARY.md 存在?
    │            (project_config.yml analysis_plan.waves)
    ├── Phase 3: manuscript.md 存在?
    └── Phase 4: final/manuscript.md 存在?
    │
    ├── 未完成 → 提示用户完成当前步骤
    │
    └── 已完成 →
        ├── 当前 Phase 还有未完成 Wave? → 推进到下一 Wave
        │   (D-05: 粒度自动判断)
        │
        └── 全部完成 → 推进到下一 Phase
            ├── 更新 STATE.md: `- 阶段：Phase N` +1
            ├── 更新 ROADMAP.md: 设置完成状态
            ├── 生成 clear 提示 (D-09)
            └── 输出建议的下一条命令
```

### Clear 提示格式

D-09 三要素：`/clear` + 下一条命令 + 进度总结

```markdown
---
## 下一步

/clear 压缩上下文后，执行以下命令继续：

/clinpub-analysis    → 进入 Phase 2 统计分析方法讨论与执行

### 进度总结
- Phase 1 (数据清洗): ✅ 已完成 — cleaned.csv 已就绪
- Phase 2 (统计分析): ⏳ 当前阶段 — Wave 1 基线描述已完成
- Phase 3-4: 待开始
---
```

### Recommended Project Structure (新增文件)

```
commands/clinpub/
├── clinpub.md              # 不变 — 主入口
├── do.md                   # 新增 — `/clinpub-do` 路由命令
├── next-step.md            # 新增 — `/clinpub-next-step` 推进命令
├── init-project.md          # 不变
├── data-prep.md            # 不变 (含重入检测模式，但不清除提示在末尾追加)
├── analysis.md             # 不变 (末尾追加 clear 提示)
├── writing.md              # 不变 (末尾追加 clear 提示)
├── review.md               # 不变 (末尾追加 clear 提示)
├── milestone.md            # 不变
├── data2idea.md            # 不变
.planning/
├── STATE.md                # 更新 — `## 下一步` 节格式标准化（D-08 统一输出）
├── ROADMAP.md              # 不变
```

### Pattern 1: 命令入口的三合一状态检测

**What:** `/clinpub-do` 的核心模式：同时读取 STATE.md、检测工件、处理 NL 输入。
**When to use:** 需要根据当前工作区状态自动路由到合适命令时。
**Example (概念流程):**

```markdown
<process>
## 三合一状态检测

### 1. 读取 STATE.md 获取当前 Phase
```
STATE.md 中匹配 `- 阶段：Phase N` → 获取当前 Phase 编号
```

### 2. 检测关键工件
```
- project_config.yml 存在?               → 项目是否已初始化
- 02_PreprocessedData/data/cleaned.csv?  → Phase 1 是否完成
- 04_Outputs/ 是否有输出?                 → Phase 2 是否完成
- 05_Manuscript/manuscript.md?           → Phase 3 是否完成
```

### 3. 处理 NL 输入（D-02）
```
如果用户输入自然语言（如"我想改清洗逻辑"），
在状态检测之前先尝试 NL → 命令映射：
- "清洗"、"数据"、"clean" → data-prep
- "分析"、"统计"、"analysis" → analysis
- "写"、"手稿"、"writing" → writing
- "初始化"、"init"、"开始" → init-project
- 其他 → 回退到无参行为
```
</process>
```

Source: [VERIFIED: phase-boundary.sh:73-104] — 已有的工件检测模式
[VERIFIED: data-prep.md 第27-36行] — 已有的 re-entry detection 模式
[CITED: D-02, D-03 from CONTEXT.md]

### Pattern 2: ROADMAP.md Plan checkbox 解析

**What:** ROADMAP.md 使用 `[x]`/`[ ]` 标记 Plan 完成状态，可用 grep 读取。
**When to use:** `/clinpub-next-step` 需要判断当前 Phase 的全部 Plan 是否完成时。
**Example:**

```bash
# 读取 Phase 2 的 Plans 完成状态
# ROADMAP.md 格式:
# Plans:
# - [x] 02-01-PLAN.md — Wave 1: 基线描述
# - [ ] 02-02-PLAN.md — Wave 2: 组间比较

# 检查所有 Plan 是否已完成:
completed=$(grep -c "\[x\] 02-" ROADMAP.md)
total=$(grep -c "\-\s*\[[x ]\] 02-" ROADMAP.md)
if [ "$completed" -eq "$total" ]; then
  echo "所有 Plan 已完成，推进到下一 Phase"
else
  echo "还有 $((total - completed)) 个 Plan 未完成"
fi
```

Source: [VERIFIED: ROADMAP.md Plan 行] — Phase 1 的 2 个 Plans 使用 `[x]` 标记完成
[ASSUMED: ROADMAP.md 格式在所有 Phase 保持一致]

### Pattern 3: 命令末尾的 Clear 提示

**What:** 在每个 Phase 命令和 milestone 末尾输出清上下文提示。
**When to use:** Phase/Wave 结束时，在 STATE.md 和各命令末尾同步输出。
**Example:**

```markdown
</process>

<success_criteria>
...
</success_criteria>

<!-- 末尾统一输出：Clear 提示 (D-08, D-09) -->
---

## 下一步

**Phase {N} ({name}) 进度**: {summary}

在 STATE.md 的 `## 下一步` 节中也同步了以上信息。

当需要清理上下文继续时，请使用：
1. `/clear` — 清除当前对话上下文
2. `/clinpub-{next-command}` — 进入下一阶段
```

Source: [CITED: D-08, D-09 from CONTEXT.md]
[VERIFIED: STATE.md 第55-60行] — 已有 `## 下一步` 节格式

### Anti-Patterns to Avoid

- **硬编码命令名称:** 不要将 `/clinpub-do` 的路由命令列表硬编码为字符串数组。应该使用 STATE.md 的 Phase 编号 + 工件检测结果动态决定。命令名称与 Phase 的映射关系见 SKILL.md 的 Commands 表（第19-28行）。
- **NL 推断优先于一切:** D-02 说 "NL 优先于状态检测"，但如果用户输入模糊的 NL（如"帮我看看"），应当合理回退到状态检测结果（D-04），而不是卡住或猜测错误命令。
- **Wave 检测与 Phase 检测混同:** Phase 2 中 Wave 是 Phase 的子任务。`/clinpub-next-step` 需要明确区分"还在 Phase 2 但 Wave 已推进"和"Phase 2 全部完成，要进入 Phase 3"。Wave 完成看 `project_config.yml` 的 `analysis_plan.waves`，Phase 完成看 ROADMAP.md 的 Plan checkboxes。

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| STATE.md Phase 解析 | 自写 YAML parser | `content.match(/阶段：Phase\s*(\d)/)` 单行正则 | workflow-guard.js:31 已验证此正则可靠 |
| 工件存在性检测 | 自写文件扫描函数 | 复用 phase-boundary.sh 的检测模式 | 已有成熟的按 Phase 分组的检测逻辑（phase-boundary.sh:73-104） |
| NL 意图推断模型 | 外部 NLP API | 简单关键词匹配（中文/英文命令名关键词） | 命令输入场景有限（8个命令），关键词匹配足够，无需引入外部依赖 |

**Key insight:** 本 Phase 的核心逻辑是"读文件 → 判断 → 写文件"，全部可在 .md 命令文件的 `<process>` 节中使用内联 Bash/文本处理实现，不需要任何新依赖。

## Common Pitfalls

### Pitfall 1: STATE.md 和 ROADMAP.md 之间的状态不一致

**What goes wrong:** STATE.md 的 `- 阶段：Phase N` 行指向 Phase 2，但 ROADMAP.md 显示 Phase 2 的所有 Plans 已完成（`[x]`），而 STATE.md 的进度百分比还是 0%。

**Why it happens:** 两个文件由不同机制更新——milestone 工作流更新 ROADMAP.md 的 Phase 状态，而 `- 阶段：Phase N` 行由 hook/命令更新。如果 `/clinpub-next-step` 只读一个文件，可能做出错误的推进决策。

**How to avoid:** `/clinpub-next-step` 应以 ROADMAP.md 的 checkboxes 为"源 truth"判断完成状态，以 STATE.md 的 `- 阶段：Phase N` 为当前定位。如果两者不一致，以 ROADMAP.md 为准输出警告。

**Warning signs:** `- 阶段：Phase 2` 但 ROADMAP.md 显示 Phase 2 全部 `[x]`。

### Pitfall 2: Wave 进度检测依赖 project_config.yml 的 `analysis_plan.waves`

**What goes wrong:** Phase 2 的 Wave 进度记录在 `project_config.yml` 的 `analysis_plan.waves` 中。但经分析工作流执行后，该字段可能为空（`waves: {}`）或结构不一致（wave 编号从 0 还是 1 开始？）。

**Why it happens:** `analysis_methods.md:76-97` 描述 Wave 从 1 开始编号，但在 `project_config.yml 模板:53行` 中 waves 默认是 `{}`。如果 Phase 2 从未执行，project_config.yml 中就没有 Wave 数据。

**How to avoid:** 在检测 Wave 状态时，先确认 `analysis_plan.waves` 非空，再按 wave 编号排序检查完成状态。如果 `waves: {}`（空的），视作 Phase 2 尚未开始，推进到 Phase 2 的 Wave 1。

**Warning signs:** `analysis_plan.waves: {}` 但 `- 阶段：Phase 2`。

### Pitfall 3: NL 推断误匹配

**What goes wrong:** 用户说 `/clinpub-do 帮我看看项目状态` — "看"和"状态"匹配到了数据清洗命令的关键词，被路由到 data-prep 而不是输出状态摘要。

**Why it happens:** 关键词匹配过于宽泛，常见的停用词（"看"、"查"、"项目"）与多条命令的关键词重叠。

**How to avoid:** NL 匹配使用"强信号词"优先策略：
- `匹配(清洗|clean|数据质量|缺失|异常)` → data-prep（高特异度）
- `匹配(结果|图|分析|统计|analysis|figure|table)` → analysis（高特异度）
- `匹配(写|稿|引用|文献|reference|writing|IMRAD)` → writing（高特异度）
- `匹配(初始化|init|开始|创建)` → init-project（高特异度）
- `匹配(状态|摘要|总览|当前|see|status|summary)` → 输出摘要（D-04 回退）
- 无强关键词匹配 → 回退到无参行为（D-04）

### Pitfall 4: 推进后增量更新产生的幽灵间隙

**What goes wrong:** `/clinpub-next-step` 推进到 Phase 3 后，STATE.md 更新为 `- 阶段：Phase 3`。但此时 Phase 3 和 Phase 2 之间的 milestone 文件（MILESTONE.md）可能不存在，phase-boundary.sh 会阻止 Phase 3 的工作。

**Why it happens:** phase-boundary.sh:53-61 检查上一 Phase 的 MILESTONE.md 是否存在且标记为 Complete。如果 `/clinpub-next-step` 跳过了 milestone 步骤。

**How to avoid:** `/clinpub-next-step` 在推进到下一 Phase 时，必须先执行 milestone 验证流程（或生成至少一个临时的 milestone 记录），否则 phase-boundary.sh 会阻挡后续操作。确保推进操作包含：
1. 运行成功标准验证
2. 生成 MILESTONE.md
3. 更新 ROADMAP.md 和 STATE.md

（D-07 说"不需要额外 verify 步骤"，但 checkpoints.md 明确要求 milestone 验证）

## Code Examples

### `/clinpub-do` 命令入口骨架

```markdown
---
name: clinpub-do
description: "Read workspace state and auto-route to appropriate clinpub command. With natural language input, routes by intent. With no arguments, shows current state summary and suggestions."
argument-hint: "[your intent or question]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---
<objective>
Workspace state router. Reads STATE.md, detects artifacts, and routes to the correct command. Supports NL input for intent-based routing.
</objective>

<process>
## 1. 解析输入参数

如果提供了参数 NL_INPUT，先尝试意图推断（D-02）：
- 强关键词匹配 → 直接路由到对应命令
- 无匹配 → 回退到无参行为（D-04）

## 2. 无参行为：状态检测（D-01）

### 2.1 读取 STATE.md
- 匹配 `- 阶段：Phase (\d)` 获取当前 Phase
- 如果 STATE.md 不存在 → 项目未初始化

### 2.2 工件检测（复用 phase-boundary.sh 模式）
```bash
# 各 Phase 关键工件
PROJECT_CONFIG=project_config.yml
CLEANED_DATA=02_PreprocessedData/data/cleaned.csv
OUTPUTS_DIR=04_Outputs
MANUSCRIPT=05_Manuscript/manuscript.md
```

| 检测 | 含义 |
|------|------|
| `-f project_config.yml` | 项目已初始化 |
| `-f $CLEANED_DATA` | Phase 1 清洗完成 |
| `-n "$(ls $OUTPUTS_DIR/ 2>/dev/null)"` | Phase 2 有分析输出 |
| `-f $MANUSCRIPT` | Phase 3 有手稿 |

### 2.3 输出状态摘要
根据 Phase + 工件状态，输出摘要和 1-3 条建议命令。

## 3. 路由

输出摘要后，用户可确认执行推荐命令。
</process>

<success_criteria>
- 无参数时输出准确的当前状态摘要
- 带 NL 输入时正确推断意图并路由
- NL 推断失败时正确回退到无参行为
- 路由后用户确认才执行（不自动运行）
</success_criteria>
```

Source: [VERIFIED: commands/clinpub/*.md 命令入口格式]
[VERIFIED: data-prep.md 第27-36行 — 已有 re-entry detection 模式]
[CITED: D-01 through D-04 from CONTEXT.md]

### `/clinpub-next-step` 命令入口骨架

```markdown
---
name: clinpub-next-step
description: "Auto-advance to next Phase or Wave. Verifies current step completion before advancing."
argument-hint: ""
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---
<objective>
Auto-advance to next Phase or Wave. Checks completion status, updates STATE.md and ROADMAP.md.
</objective>

<process>
## 1. 读取当前状态

```bash
# 从 STATE.md 获取当前 Phase
PHASE=$(grep -oP '阶段：Phase\s*\K\d' .planning/STATE.md)

# 从 ROADMAP.md 获取 Plan 完成状态
grep -E "^\*\*Phase $PHASE" .planning/ROADMAP.md
```

## 2. 验证完成状态（D-06）

按当前 Phase 验证：
- Phase 0: project_config.yml 关键字段非空
- Phase 1: cleaned.csv 存在
- Phase 2: 当前 Wave 的 SUMMARY.md 存在（检查 .planning/phases/02-断点续做/）
- Phase 3: manuscript.md 存在
- Phase 4: final/manuscript.md 存在

未完成 → 提示用户，列出未完成项。

## 3. 推进决策（D-05）

已完成 → 判断推进粒度：
- Phase 2 + 还有未完成 Wave → 推进到下一 Wave
- 所有 Plans 已完成 → 推进到下一 Phase
  - 更新 STATE.md: `- 阶段：Phase N` → N+1
  - 更新 ROADMAP.md: 当前 Phase 标记 ✅ Complete，下一 Phase 标记 🔄 In Progress
  - 生成 MILESTONE.md

## 4. 输出下一阶段提示（D-08, D-09）
- /clear 命令提示
- 下一条建议命令
- 进度总结
</process>

<success_criteria>
- 未完成时给出明确提示和未完成列表
- 推进粒度自动判断正确（Wave vs Phase）
- STATE.md 和 ROADMAP.md 同步更新
- 输出包含三要素的 clear 提示
</success_criteria>
```

Source: [VERIFIED: ROADMAP.md Plan checkboxes]
[VERIFIED: phase-boundary.sh 完成检测模式]
[CITED: D-05 through D-09 from CONTEXT.md]

### 各 Phase 命令末尾的 Clear 提示追加

在每个现有命令 data-prep.md、analysis.md、writing.md、review.md 的 `<success_criteria>` 之后追加：

```markdown
## 继续提示

---
**{Phase 名} 工作结束。**

**进度更新**: 已在 STATE.md 的 `## 下一步` 节同步。
**下一步建议**: `/clinpub-next-step` — 自动推进到下一阶段。

当对话上下文太长时，请使用 `/clear` 清除上下文，然后执行：
```
/clinpub-next-step
```
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 无自动路由 — 用户需要知道正确的命令名 | `/clinpub-do` 自动检测状态路由 | Phase 2 | 降低使用门槛，支持工作中断后恢复 |
| 手动进度推进 — 用户自己判断下一步 | `/clinpub-next-step` 自动推进 | Phase 2 | 消除"不知道该执行哪个命令"的困惑 |
| 无 clear 提示 — 上下文膨胀导致 confabulation | 标准化的三要素 clear 提示 | Phase 2 | 减少 long-context 带来的幻觉风险 |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | ROADMAP.md 的 Plan checkbox 格式在所有 Phase 保持一致（`[x]` 标记已完成） | Architecture Patterns / Pattern 2 | 如果后续 Phase 使用不同标记格式（如 `[done]`），grep 计数会出错。Phase 1-2 已验证一致，后续需维护相同格式 |
| A2 | `project_config.yml` 的 `analysis_plan.waves` 字段在 Phase 2 执行后不会被意外清空 | Common Pitfalls / Pitfall 2 | 如果 workflow 或 agent 意外写入了空的 `waves: {}`，Wave 进度会丢失。建议 `/clinpub-do` 同时检查 `04_Outputs/` 作为 fallback 信号 |
| A3 | phase-boundary.sh 的 $ANALYSIS_DIR 等变量是硬编码的，但 production 中路径可能通过 project_config.yml 自定义 | Don't Hand-Roll | 如果用户自定义了路径，phase-boundary.sh 的检测会失效。本项目 paths 字段已在 project_config.yml 中定义但 phase-boundary.sh 未读取它 |

## Open Questions

1. **[/clinpub-do] 状态摘要的输出格式是纯文本还是表格？**
   - What we know: D-01 说"报告当前状态摘要 + 建议命令"
   - What's unclear: 摘要格式（表格？Markdown 列表？XML checkpoint?）在 CONTEXT.md 中未指定，属于 Claude's Discretion
   - Recommendation: 使用 Markdown 表格 + 建议命令列表格式，参考 checkpoints.md 的 verify 模式

2. **[/clinpub-next-step] 遇到未完成时，是否自行执行剩余的 Plan？**
   - What we know: D-06 说"未完成则提示用户"
   - What's unclear: 提示后是等待用户输入命令，还是自动给出"是否执行"/clinpub-X 来继续？D-04 给了 discretion
   - Recommendation: 提示未完成项目 + 建议执行命令，用户确认后调用对应命令。不需要自动执行。

3. **[Clear 提示] 措辞格式是否允许 emoji？**
   - What we know: D-09 要求三要素
   - What's unclear: 措辞风格（CLAUDE.md 说"能玩梗就玩梗"但 SKILL.md 使用 emoji 如 ✅⏳）
   - Recommendation: 使用 ✅/⏳ emoji（与 STATE.md 和 ROADMAP.md 一致），文本描述使用中文

## Environment Availability

> Step 2.6: SKIPPED — Phase 2 只新增 .md 命令文件，无外部工具依赖。所有操作在读/写 .md 和 .yml 文件范围内，依赖已由仓库自身满足。

## Validation Architecture

> Skipped — `workflow.nyquist_validation` is explicitly `false` in `.planning/config.json`.

## Security Domain

> Required: security_enforcement is implicitly enabled (config.json does not disable it)

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | No | — |
| V3 Session Management | No | — |
| V4 Access Control | Yes | Phase 2 的新命令本身不绕过 workflow-guard.js 的 hook 控制。STATE.md/ROADMAP.md 在 `.planning/` 目录下，属于 always-allowed（workflow-guard.js:47-59），所有 Phase 均可写入 |
| V5 Input Validation | Yes | NL 输入解析使用关键词白名单匹配，不需要 sanitize（无外部 API 调用） |
| V6 Cryptography | No | — |

### Known Threat Patterns for clinpub Phase 2

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| NL 输入中的命令注入 | Tampering | 关键词匹配只输出命令名称，不拼接用户输入到 shell 命令。所有路由由命令的 `<process>` 节控制 |
| STATE.md/ROADMAP.md 被意外覆盖 | Denial of Service | 推进操作在 `/clinpub-next-step` 的 `<process>` 节中明确写入，不自动在其他命令中修改 STATE.md 的阶段行（D-08 只说在末尾输出提示，没说修改） |

## Sources

### Primary (HIGH confidence)
- [VERIFIED: commands/clinpub/data-prep.md] — 重入检测模式，作为 `/clinpub-do` 路由逻辑的参考模板
- [VERIFIED: commands/clinpub/clinpub.md] — 薄命令入口格式（frontmatter + objective + process + success_criteria）
- [VERIFIED: hooks/clinpub-workflow-guard.js:31] — STATE.md `- 阶段：Phase N` 正则匹配
- [VERIFIED: hooks/clinpub-phase-boundary.sh:73-104] — 各 Phase 工件检测模式
- [VERIFIED: .planning/ROADMAP.md] — Plan `[x]`/`[ ]` 格式，Phase 状态 emoji 格式
- [VERIFIED: .planning/STATE.md] — 当前 Phase 标识行，`## 下一步` 节格式
- [VERIFIED: pipeline/workflows/analysis.md] — Wave 定义和推进模式
- [VERIFIED: pipeline/templates/project_config.yml:41-58] — `analysis_plan.waves` 字段
- [VERIFIED: pipeline/references/agent-contracts.md] — 7 Agent 角色分工，SUMMARY.md 产生者（clinpub-executor）
- [VERIFIED: pipeline/references/checkpoints.md] — checkpoint/milestone 格式，完成协议

### Secondary (MEDIUM confidence)
- [CITED: CONTEXT.md D-01 through D-09] — 所有锁定决策
- [VERIFIED: SKILL.md:19-28] — 8 个 clinpub 命令的名称为路由提供完整映射表
- [VERIFIED: pipeline/references/manifest-format.md] — MANIFEST.yaml 格式，Agent 间文件交接协议

### Tertiary (LOW confidence)
- [ASSUMED: A1] ROADMAP.md 的 Plan checkbox 格式在所有 Phase 保持一致
- [ASSUMED: A2] `analysis_plan.waves` 不会被意外清空
- [ASSUMED: A3] phase-boundary.sh 路径硬编码不影响 Phase 2

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — 不引入新依赖，完全复用已验证的模式
- Architecture: HIGH — 三合一路由 + 两阶段推进逻辑在 CONTEXT.md 中精确定义
- Pitfalls: MEDIUM — 状态不一致风险是合理推断，基于两个文件由不同机制更新的观察；Wave 检测风险基于 project_config.yml 默认值分析

**Research date:** 2026-05-05
**Valid until:** 在 pipeline 架构不变时有效（预计整个 v1 开发周期内稳定）
