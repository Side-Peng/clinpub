# Modify Agent 设计规格

**日期**: 2026-06-02
**状态**: 已批准
**范围**: 分析阶段产出修改（`03_AnalysisMethods/`, `04_Outputs/`）

## 1. 背景与动机

现有 clinpub 管线（Phase 0-4）能够比较完整地运行数据分析→写作→审稿流程。但在实际使用中，用户经常需要在完成分析后对产出进行局部修改：

- **图表样式**: 配色、字体、图表类型（箱线图→小提琴图）
- **统计方法**: 更换检验方法、修改变量组合、调整模型参数

当前缺少专职智能体处理此类修改请求，导致修改流程不清晰、历史记录缺失。

## 2. 设计决策

### 2.1 修改范围

**决策**: 仅覆盖分析阶段产出（`03_AnalysisMethods/`, `04_Outputs/`）

**理由**: 
- 手稿（`05_Manuscript/`）由用户手动触发 `/clinpub-writing` 更新，保持职责分离
- 不自动级联更新下游文件，避免意外覆盖用户已审阅的手稿

### 2.2 修改类型

**决策**: 同时支持图表样式调整和统计方法变更

**理由**: 
- 样式修改（重绘图表）和方法变更（重跑分析）是两类常见需求
- 统一由同一智能体处理，减少用户认知负担

### 2.3 触发方式

**决策**: 新增独立斜杠命令 `/clinpub-modify`

**理由**: 
- 用户可在任何阶段手动调用
- 交互式选择修改范围，适合复杂修改场景
- 不污染现有分析/写作工作流

### 2.4 修改记录

**决策**: 追加修改历史到现有 `01-PLAN.md`

**理由**: 
- 保持单一真相源（分析计划 + 修改历史在同一文件）
- 便于追溯修改动机和执行状态
- 不新增独立日志文件

### 2.5 架构方案

**决策**: 方案 A — 独立 modify-agent

**理由**: 
- 职责清晰，不污染现有智能体
- 轻量级修改协议（定义→计划→执行→更新）
- 可独立演进

**排除的方案**:
- B（复用 analyst-agent）: analyst-agent 已负责 Phase 1+2，修改逻辑混入增加认知负担
- C（修改编排器）: 过度工程化，修改任务通常是单方法的小操作

## 3. 架构

### 3.1 新增文件

| 文件 | 用途 |
|------|------|
| `agents/modify-agent.md` | 修改智能体角色卡 |
| `commands/clinpub/modify.md` | 斜杠命令入口 |
| `pipeline/workflows/modify.md` | 修改工作流编排 |

### 3.2 数据流

```
用户调用 /clinpub-modify
  ↓
modify-agent 读取项目上下文:
  - project_config.yml
  - .clinpub/phases/02-analysis/01-PLAN.md
  - 04_Outputs/ 目录列表
  ↓
与用户交互明确修改定义:
  - 选择方法（从 PLAN.md methods 列表）
  - 选择修改类型（样式 / 方法 / 变量）
  - 输入具体修改内容
  ↓
生成修改摘要（结构化列表）
  ↓
用户确认修改摘要
  ↓
逐条执行修改:
  - 样式修改 → 修改 R 脚本参数 → 重绘
  - 方法修改 → 重写脚本 → 重新运行
  ↓
验证每条修改的产出
  ↓
追加修改记录到 PLAN.md
```

### 3.3 与其他智能体的关系

- **不替换 analyst-agent**: modify-agent 自身具备 R/Python 执行能力
- **不调用 writer-agent**: 手稿更新由用户手动触发
- **不更新 MANIFEST.yaml**: 产出文件路径不变

## 4. modify-agent 角色卡

### 4.1 核心定义

```yaml
name: modify-agent
description: |
  分析产出修改专家。明确修改定义、制定修改计划、执行图表/方法修改、
  更新 PLAN.md 修改历史。处理两类修改：图表样式调整（配色、字体、布局）
  和统计方法变更（检验方法、变量组合、模型参数）。
tools: Read, Write, Edit, Bash, Glob, Grep
```

### 4.2 执行流

**Step 1: 加载上下文**

读取:
- `project_config.yml`
- `.clinpub/phases/02-analysis/01-PLAN.md`（现有方法清单）
- `04_Outputs/` 目录列表

构建可修改方法列表（id + 类型 + 当前方法名）。

**Step 2: 明确修改定义（与用户交互）**

呈现现有方法列表:

```markdown
## 当前分析方法列表
1. 01_BaselineTable — 基线特征表 (gtsummary)
2. 02_TwoGroupComparison — 两组比较 (Wilcoxon)
3. 03_RepeatedMeasures — 重复测量 (lme4::lmer)
4. 04_LinearRegression — 线性回归 (lm)

请选择要修改的方法编号（可多选）。
```

逐条确认修改细节:
- **样式修改**: 新配色、字体、尺寸、图表类型
- **方法修改**: 新检验/模型、变量替换、参数调整

输出修改摘要供用户确认:

```markdown
## 修改摘要
| # | 方法 | 类型 | 修改内容 | 影响文件 |
|---|------|------|----------|----------|
| 1 | 02_TwoGroupComparison | 样式 | 箱线图→小提琴图+散点 | figure_*.png |
| 2 | 03_RepeatedMeasures | 方法 | lmer→GEE | 全部产出 |

确认后将逐条执行修改。
```

**Step 3: 执行修改**

按修改摘要逐条执行:

| 修改类型 | 执行策略 |
|----------|----------|
| 图表样式 | 读取现有 R 脚本 → 修改 ggplot 参数 → 重绘 → 覆盖原图 |
| 变量替换 | 修改脚本变量引用 → 重新运行 |
| 方法变更 | 重写分析脚本 → 运行 → 生成新图表+表格 |
| 新增方法 | 创建新目录 → 编写新脚本 → 运行 → 生成产出 |

失败时回退该条修改的产出文件（git stash），继续下一条。

**Step 4: 验证 + 更新 PLAN.md**

验证标准:
- 图表 ≥300 DPI
- 统计报告含效应量 + 95%CI + exact p-value
- 代码可独立运行（从 cleaned.csv）

追加修改记录到 `01-PLAN.md`:

```yaml
modifications:
  - id: "mod-20260602-001"
    timestamp: "2026-06-02"
    phase: 2
    description: "箱线图→小提琴图+散点覆盖；lmer→GEE模型"
    items:
      - method_id: "02_TwoGroupComparison"
        type: style
        change: "geom_boxplot → geom_violin + geom_jitter"
      - method_id: "03_RepeatedMeasures"
        type: method
        change: "lme4::lmer → geepack::geeglm"
        reason: "用户要求考虑组内相关性"
    status: completed
```

### 4.3 关键约束

- 从 `cleaned.csv` 读取，不碰原始数据
- 修改图表保持英文标签、≥300 DPI、theme_pub() 主题
- 统计报告保持 effect size + 95%CI + exact p-value
- 不修改 `05_Manuscript/` 或 `Reference/`
- 每次修改会话最多处理 5 个修改项（防止上下文溢出）

## 5. 命令与工作流

### 5.1 命令文件 `commands/clinpub/modify.md`

```yaml
---
name: clinpub:modify
description: |
  分析产出修改。明确修改定义（图表样式/统计方法/变量），制定修改计划，
  执行修改，验证产出，更新 PLAN.md。支持箱→小提琴、检验方法替换、
  变量调整、新增分析方法等操作。
argument-hint: "[方法编号或修改描述，留空则交互式选择]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---
```

### 5.2 工作流 `pipeline/workflows/modify.md`

| Step | 名称 | 内容 |
|------|------|------|
| 1 | load_context | 读取 CONFIG + PLAN.md + 04_Outputs 目录树 |
| 2 | define_modification | 与用户交互：选择方法→类型→内容→确认摘要 |
| 3 | execute_modifications | 逐条执行修改 |
| 4 | verify_modifications | 验证每条修改的产出质量 |
| 5 | update_plan | 追加修改记录到 PLAN.md，更新 STATE.md |

**Checkpoint 策略**:
- 修改定义确认后：checkpoint（用户确认才继续）
- 每条方法变更完成后：brief 输出，不阻塞
- 修改类型变更时：如发现需要变更方法，STOP 并询问

**错误处理**:
- 修改执行失败 → 回退该条产出 → 报告错误 → 继续下一条
- 全部完成后 → 汇总报告：N 成功 / M 失败

### 5.3 install.js 适配

`bin/install.js` 自动将 `commands/clinpub/modify.md` 转为 `clinpub-modify` 技能，无需额外改动。

## 6. 系统集成

### 6.1 对现有文件的影响

| 文件 | 变更 | 说明 |
|------|------|------|
| `SKILL.md` | 新增一行 | 命令表增加 `/clinpub-modify` |
| `CLAUDE.md` | 新增两行 | Key Directory 表 + Agent Routing 表 |
| `AGENTS.md` | 新增一行 | Commands 表 |
| `bin/install.js` | **无变更** | 已有逻辑自动扫描 |
| `hooks/` | **无变更** | 不触发阶段边界守卫 |

### 6.2 Agent Routing 表更新

```
| 修改已完成的分析产出 | `modify-agent` | R primary |
```

### 6.3 与 hooks 的兼容性

`hooks/clinpub-workflow-guard.js` 通过 `STATE.md` 的 `阶段：Phase\s*(\d)` 判断当前阶段。`/clinpub-modify` 可在任何阶段调用（Phase 2/3/4），不需要修改 hook。

修改操作仅涉及 `03_AnalysisMethods/`、`04_Outputs/` — 在 hook 允许写入范围内。

## 7. 文件清单

**新增（3 个文件）**:
```
agents/modify-agent.md
commands/clinpub/modify.md
pipeline/workflows/modify.md
```

**更新（3 个文件）**:
```
SKILL.md      — 命令表新增一行
CLAUDE.md     — Key Directory + Agent Routing
AGENTS.md     — Commands 表新增一行
```

**不变更**:
- `05_Manuscript/` — 手稿不自动更新
- `Reference/` — 参考文献不变更
- `MANIFEST.yaml` — 产出文件路径不变
- `analyst-agent.md` — 不被修改
- `clinpub-executor.md` — 不被修改
- `hooks/*.js` — 阶段守卫不需要变

## 8. 成功标准

- [ ] `/clinpub-modify` 命令可在任何阶段调用
- [ ] modify-agent 能够读取现有分析计划和方法列表
- [ ] 用户可通过交互式选择明确修改定义
- [ ] 图表样式修改能够正确重绘并覆盖原图
- [ ] 统计方法修改能够重新运行并生成新产出
- [ ] 所有修改后的图表 ≥300 DPI、英文标签、theme_pub()
- [ ] 所有修改后的统计报告含效应量 + 95%CI + p-value
- [ ] 修改记录追加到 PLAN.md，包含时间戳和修改内容
- [ ] STATE.md 最后活动行更新
- [ ] 不修改 `05_Manuscript/` 或 `Reference/`
