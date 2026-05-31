---
name: clinpub:do
description: "Read workspace state and auto-route to the appropriate clinpub command. With natural language input (e.g., '/clinpub-do 我想改清洗逻辑'), routes by intent. With no arguments, shows current state summary and suggests next commands."
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
Workspace state router. Reads STATE.md, detects artifacts, and routes to the correct Phase command.

## 行为模式

- **无参数**（D-01）: 读取 STATE.md + 检测关键工件 → 输出状态摘要 + 建议 1-3 条命令 → 用户确认后路由
- **有 NL 参数**（D-02）: NL 意图识别优先于状态检测 → 成功则直接路由 → 失败则回退到无参行为（D-04）
- **路由依据**（D-03）: 三合一决策：STATE.md `- 阶段：Phase N` + 工件检测 + 可选 NL 输入
</objective>

<interfaces>
<!-- 关键检测模式，executor 直接使用 -->

STATE.md Phase 读取:
```bash
正则: /阶段：Phase\s*(\d)/
源:   hooks/clinpub-workflow-guard.js:31（已验证）
```

工件检测模式（复用 phase-boundary.sh:73-104）:
```
Phase 0: -f project_config.yml + 验证 project.name != "项目名称"
Phase 1: -f 02_PreprocessedData/data/cleaned.csv
Phase 2: -d 04_Outputs && ls 04_Outputs/ 非空 + project_config.yml analysis_plan.waves
Phase 3: -f 05_Manuscript/manuscript.md
Phase 4: -d 05_Manuscript/final && ls 05_Manuscript/final/ 非空
```
</interfaces>

<execution_context>
@./pipeline/workflows/init-project.md
@./pipeline/workflows/data-prep.md
@./pipeline/workflows/analysis.md
@./pipeline/workflows/writing.md
@./pipeline/workflows/review.md
@./pipeline/workflows/next-step.md
@./pipeline/workflows/milestone.md
@./pipeline/references/checkpoints.md
</execution_context>

<process>

## 1. 解析输入参数

```
如果提供了参数 NL_INPUT：
  1. 提取参数中的自然语言文本（去除非语义的前缀词如 "帮我"、"我想"、"我要"）
  2. 执行 NL 意图推断（见 Step 1.1）
  3. 推断成功 → 直接跳转到「6. 路由到目标命令」
  4. 推断失败 → 跳转到「2. 无参行为：状态检测」（D-04 回退）

如果没有提供参数（无参调用）：
  1. 直接进入「2. 无参行为：状态检测」（D-01）
```

### 1.1 NL 意图推断规则（D-02）

使用强信号关键词优先匹配策略，非简单包含匹配。关键词按优先级从高到低排列：

| 优先级 | 关键词（任一命中即路由） | 路由到 | 特异度 |
|--------|-------------------------|--------|--------|
| 1 | `(初始化\|init\|开始\|创建项目\|新建)` | init-project | 高 — 非清洗/分析语境 |
| 2 | `(清洗\|clean\|数据质量\|缺失\|异常值\|cleaned)` | data-prep | 高 — 特异性数据处理术语 |
| 3 | `(选题\|话题挖掘\|idea\|数据探索\|data2idea)` | data2idea | 高 — 选题挖掘术语 |
| 4 | `(分析\|统计\|结果\|图\|表\|analysis\|figure\|table\|回归\|生存\|ROC)` | analysis | 高 — 分析术语 |
| 5 | `(写\|稿\|手稿\|文献\|引用\|writing\|IMRAD\|论文\|manuscript)` | writing | 高 — 写作术语 |
| 6 | `(审稿\|review\|修订\|修改\|意见\|审阅\|response)` | review | 高 — 审稿术语 |
| 7 | `(推进\|下一步\|继续\|next\|advance)` | next-step | 高 — 推进术语 |
| 8 | `(状态\|摘要\|总览\|当前\|情况\|see\|status\|什么阶段)` | 回退到无参 | 明确表达"查看状态"意图，不是特定命令 |

**匹配规则**:
- 命中高优先级关键词立即路由，不继续检查低优先级（D-02：NL 优先于状态检测）
- 命中第 7 组关键词 → 执行无参状态检测流程（D-04：明确表达查看状态，回退到摘要）
- 没有命中任何关键词组 → 回退到无参行为（D-04：推断不出明确意图）
- **跨组冲突时**（如同时包含"分析"和"写"）：以优先级高的为准（Group 编号小的优先），不按文本位置判断
- **反模式规避**: 不要匹配停用词（"看"、"查"、"项目"、"做"、"搞"、"弄"、"整"），只匹配上表中特异性术语

### 1.2 命令名称映射

路由使用 SKILL.md 定义的命令名称格式：

| 路由目标 Phase | 命令名称 | 执行方式 |
|---------------|---------|---------|
| Phase 0 | `/clinpub-init-project` | 确认后提示用户执行 |
| Phase 1 | `/clinpub-data-prep` | 确认后提示用户执行 |
| Phase 2 | `/clinpub-analysis` | 确认后提示用户执行 |
| Phase 3 | `/clinpub-writing` | 确认后提示用户执行 |
| Phase 4 | `/clinpub-review` | 确认后提示用户执行 |
| 选题挖掘 | `/clinpub-data2idea` | 确认后提示用户执行（无需初始化） |
| 自动推进 | `/clinpub-next-step` | 确认后提示用户执行 |
| Phase 检查 | `/clinpub-milestone N` | 确认后提示用户执行 |

## 2. 无参行为：状态检测（D-01）

### 2.1 读取 STATE.md 获取当前 Phase

```
从 STATE.md 中匹配 `- 阶段：Phase N`（使用正则：/阶段：Phase\s*(\d)/）：
- 匹配成功 → 获取当前 Phase 编号（Phase 0-4）
- 匹配失败 → 检查 STATE.md 是否存在
  - STATE.md 不存在或没有匹配行 → 项目未初始化 → 跳转到「3. 无参路由: 未初始化」
```

**反模式规避**: 不依赖 emoji 计数或自然语言行（如 `**当前状态**: ...`）做判断。只用 `- 阶段：Phase N` 结构化行作为 Phase 的权威来源（与 workflow-guard.js D-02 逻辑一致）。

### 2.2 检测关键工件

```
使用 Bash 检测以下工件是否存在：

1. 检查项目是否已初始化:
   - `-f project_config.yml` — 项目配置存在
   - 验证关键字段非空: project.name != "项目名称", variables.outcome 非空, paths.raw_data 对应目录存在
   （复用 data-prep.md 的重新进入检测模式）

2. 检测各 Phase 完成状态:
   Phase 0: project_config.yml 存在且关键字段有效
   Phase 1: -f 02_PreprocessedData/data/cleaned.csv
   Phase 2: -d 04_Outputs && ls 04_Outputs/ 非空
   Phase 3: -f 05_Manuscript/manuscript.md
   Phase 4: -d 05_Manuscript/final && ls 05_Manuscript/final/ 非空
```

**反模式规避**: 
- 检测 Phase 2 完成状态时同时检查 `04_Outputs/` 和 `project_config.yml analysis_plan.waves`，避免仅依赖 waves 字段判断（Pitfall 2: waves 可能为空对象 `{}`）
- 不硬编码命令名称字符串（Pitfall 1: 使用 Phase 映射表）

### 2.3 路由决策树（D-03 三合一决策）

```
依据 Phase 编号 + 工件检测结果 + (可选的 NL 推断结果)，输出状态摘要和建议命令。

---

**STATE.md 不存在或无法解析 Phase**:

输出来初始化建议:
```
当前状态: 项目未初始化
检测结果: STATE.md 不存在或无 Phase 标识行
建议: /clinpub-init-project  → 初始化项目配置和目录结构
      /clinpub-data2idea    → 从数据中挖掘论文选题（无需初始化）
请输入对应的命令名称继续，或输入 'exit' 取消。
```

---

**Phase 0 检测结果**:

┌──────────────────────────────────────────────────────────────┐
│ 条件: STATE.md 显示 Phase 0                                  │
│                                                              │
│ ┌─ project_config.yml 存在且关键字段有效?                     │
│ │  ├─ YES → 输出:                                            │
│ │  │  当前状态: Phase 0 (项目初始化) — 已完成                │
│ │  │  检测到 project_config.yml，关键字段有效                │
│ │  │  建议:                                                  │
│ │  │    /clinpub-data-prep        → Phase 1 数据清洗         │
│ │  │    /clinpub-next-step        → 自动推进到下一步         │
│ │  │                                                         │
│ │  └─ NO  → 输出:                                           │
│ │     当前状态: Phase 0 (项目初始化) — 未完成                │
│ │     project_config.yml 不存在或关键字段为空                │
│ │     建议:                                                  │
│ │       /clinpub-init-project    → 初始化项目                │
└──────────────────────────────────────────────────────────────┘

**Phase 1 ~ 4 各 Phase 的检测结果格式**
（统一使用以下模板，替换 N 和 name）：

```
当前状态: Phase N (name) — [进行中|已完成]
检测到: [已完成的工件列表] | [缺失的工件列表]
建议:
  /clinpub-{command}    → [做什么]
  /clinpub-{command}    → [做什么]
  /clinpub-next-step    → 自动推进到下一阶段

输入对应的命令名称（如 clinpub-data-prep）执行，或输入 'exit' 取消。
```

具体各 Phase 的路由条件:

| 当前 Phase | 完成条件 | 已完成时建议 | 未完成时建议 |
|------------|---------|-------------|-------------|
| Phase 1 | cleaned.csv 存在 | data-prep (重入刷新), next-step | data-prep (继续清洗) |
| Phase 2 | 04_Outputs/ 非空 | analysis (继续分析), next-step | analysis (开始分析) |
| Phase 3 | manuscript.md 存在 | writing (继续撰写), next-step | writing (开始撰写) |
| Phase 4 | final/ 有输出 | review (继续修改), 全部完成庆祝 | review (开始审稿) |

**Phase 2 的特殊处理:**
在建议 analysis 命令时，检测 `project_config.yml analysis_plan.waves`：如果 `waves: {}`（空），在建议中注明"尚未定义 Wave 结构，需要从基线描述开始"；如果 waves 非空，注明"已有 {N} 个 Wave，继续分析"。

---

### 2.4 输出格式规范

使用统一模板输出状态摘要：

```markdown
---

### 当前状态

| 维度 | 状态 |
|------|------|
| 当前 Phase | Phase {N}: {name} |
| 项目初始化 | ✅ 已完成 / ⏳ 未完成 |
| 关键工件 | {工件状态描述} |
| 建议命令 | 见下方 |

{具体的检测结果和 1-3 条建议命令}

---
```

---

## 3. 用户确认流程（D-01）

输出状态摘要和建议命令后，等待用户输入：

1. 用户输入命令名（如 `data-prep`）→ 提示用户执行 `/clinpub-{name}`
2. 用户输入 `exit` 或 `取消` → 结束命令
3. 用户输入其他内容 → 重新解释可用的命令选项

**重要**: 命令只做路由建议，不自动执行目标命令。用户需要手动输入目标命令执行。
</process>

<success_criteria>
- 无参数时输出准确的当前 Phase 状态摘要 + 1-3 条建议命令
- 带 NL 输入时正确推断意图并路由到对应命令
- NL 推断失败时正确回退到无参行为（显示状态摘要）
- 路由后等待用户确认，不自动执行目标命令
- 所有 8 个命令的路由映射完整（init-project, data-prep, analysis, writing, review, next-step, milestone, data2idea）
- 不匹配停用词（"看"、"查"、"项目"、"做"）
</success_criteria>
