---
name: clinpub
description: "ClinPub 枢纽：查看状态、查看命令参考、关卡核验并推进、按意图路由。无参看状态，help 看参考，next 核验并推进，其余按自然语言意图路由到对应命令。"
argument-hint: "[help | next | 你的意图]"
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
ClinPub 的**单一入口**。四种模式：

| 输入 | 模式 | 做什么 |
|---|---|---|
| 无参数 | **状态** | 读 `STATE.md` + 检测工件 → 输出进度摘要 + 建议命令 |
| `help` / `?` | **参考** | 输出命令参考表 |
| `next` / `推进` | **推进** | 关卡核验 → 生成 `MILESTONE.md` → 用户签字 → 推进阶段 |
| 其他文本 | **路由** | 按意图路由到对应命令（只提示，不代跑） |

> **为什么合并**：原先 `overview` / `do` / `next-step` / `milestone` 四个命令各自维护一份状态判据，
> 改一处要改三处。合并后判据只写一份，且**"推进"与"核验"成为一个原子动作**——
> 不再会出现"推进了但没核验"。
</objective>

<execution_context>
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/next-step.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/workflows/milestone.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/references/checkpoints.md"`
!`cat "${CLAUDE_PLUGIN_ROOT}/pipeline/templates/milestone.md"`
</execution_context>

<process>

## 0. 判定模式

```
无参数            → 模式 1（状态）
help / ? / 参考   → 模式 2（参考）
next / 推进/继续   → 模式 3（推进）
其他非空文本       → 模式 4（路由）
```

---

## 模式 1：状态（无参）

### 1.1 读阶段

```bash
grep -oE '阶段：Phase\s*[0-9]+' .clinpub/STATE.md 2>/dev/null | head -1
```

匹配不到 → 判定"未初始化"，直接给建议。

> 反模式：不要用 emoji 计数或自然语言行判断阶段；`- 阶段：Phase N` 是唯一权威来源
> （与 `hooks/clinpub-workflow-guard.js` 保持一致）。

### 1.2 按 3.0 判据检测

| 阶段 | 完成判据 |
|---|---|
| 阶段0 | `project_config.yml` 存在且 `project.name` 非空，且（`variables.outcome` 非空 **或** `analysis_mode: exploratory`） |
| 阶段1 | `02_PreprocessedData/data/cleaned.csv` 存在 |
| 阶段2 | `.clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md` 存在（分析已冻结） |
| 阶段2 中间态 | `.clinpub/ANALYSIS_LOG.md` 存在但无 `ANALYSIS_SUMMARY.md` |
| 阶段3 | `05_Manuscript/sections/` 六节全 `final` 且 `assemble_manuscript.py --check` 通过 |

**阶段2 中间态额外报告**：已完成批次数（`grep -c '^## Batch' .clinpub/ANALYSIS_LOG.md`）
与最后一批的「下一批决策」内容。

**阶段3 未完成额外报告**：哪些章节非 `final`（`stale` / `draft`）。

### 1.3 输出

```
当前状态: 阶段{N} ({name}) — {已完成 | 进行中 | 未完成}
检测结果: {工件列表}
{中间态: 已完成 {B} 个批次，最后一批决定: {decision}}
{写作未完成: 非 final 章节: {list}}

建议:
  /clinpub-{cmd}   → {做什么}
  /clinpub-{cmd}   → {做什么}

输入命令名继续，或输入 'exit' 取消。
```

未初始化时给 `/clinpub-initialize` 与 `/clinpub-data2idea` 两条建议。

---

## 模式 2：参考（`help`）

输出命令参考（**不执行任何流程**）：

| 命令 | 阶段 | 做什么 |
|---|---|---|
| `/clinpub` | — | 状态 / 参考 / 推进 / 路由 |
| `/clinpub-initialize` | 0 | 研究框架 + 目标期刊 → 配置与目录 |
| `/clinpub-data-prep` | 1 | 数据清洗 → `cleaned.csv` |
| `/clinpub-analysis` | 2 | **迭代分析**：每批 1–3 个方法 |
| `/clinpub-writing` | 3 | **递进写作**：骨架 → R→M→D→C→I → Abstract |
| `/clinpub-modify` | 工具 | 改分析产出（样式/方法/变量/新方法） |
| `/clinpub-improving` | 工具 | 自审 → 修改计划 → 改稿（可反复） |
| `/clinpub-review` | 工具 | 投稿后：真实审稿意见 → 回复信 → 修稿 |
| `/clinpub-coverletter` | 工具 | 按目标期刊生成投稿信 |
| `/clinpub-data2idea` | 工具 | 从数据挖选题 |

**3.0 的两个变化**：分析是迭代的（可反复运行 `/clinpub-analysis`）；写作是递进的（从 Results 往回写，`manuscript.md` 是生成物）。

**不要试图用一条命令跑完所有阶段。**

---

## 模式 3：推进（`next`）

**核验与推进是一个原子动作**，不可分开。

### 3.1 核验

按模式 1 的判据判断当前阶段是否真的完成。

- **未完成** → 列出未完成项，**不推进**，结束。
- **阶段2 中间态** → 不推进，报告批次数与最后一批决策，建议继续分析或收口。
- **完成** → 进入 3.2。

### 3.2 关卡核验

按 `pipeline/workflows/milestone.md` 执行：

1. 逐条核对本阶段 success criteria（`pipeline/references/gates.md` 的门控项）
2. 记录关键决策与产出
3. 生成 `.clinpub/phases/{NN}-{name}/MILESTONE.md`（模板见 `pipeline/templates/milestone.md`）
4. 向用户请求签字：`输入 "approved" 确认，或说明需要调整的地方`

**未签字不推进。**

### 3.3 推进

签字后：

1. `STATE.md`：阶段 `Phase N` → `Phase N+1`，清空本阶段中间态字段
2. `ROADMAP.md`：当前 Phase → ✅，下一 Phase → 🔄
3. 输出 clear 提示：

```
/clear
下一条命令: /clinpub-{next}   → {做什么}
进度: 阶段1 ✅ | 阶段2 ✅ | 阶段3 ⏳ 当前
```

### 3.4 阶段3 之后阶段3 是最后一个编号阶段。完成并签字后输出：

```
🎉 核心管线完成（阶段0–3）
后续可用独立工具：
  /clinpub-improving     自审并改进
  /clinpub-coverletter   生成投稿信
  /clinpub-review        收到审稿意见后处理
```

---

## 模式 4：路由（其他文本）

只做路线建议，**不代跑目标命令**。

按优先级匹配，命中即路由：

| 优先级 | 关键词（任一命中） | 路由到 |
|---|---|---|
| 1 | 初始化/init/开始/创建项目/新建 | `/clinpub-initialize` |
| 2 | 清洗/clean/数据质量/缺失/异常值/cleaned | `/clinpub-data-prep` |
| 3 | 选题/话题挖掘/idea/数据探索/data2idea | `/clinpub-data2idea` |
| 4 | 审稿/审稿意见/reviewer/回复信/rebuttal/返修 | `/clinpub-review` |
| 5 | 投稿信/coverletter | `/clinpub-coverletter` |
| 6 | 改进/润色/自审/修订/改稿/improving | `/clinpub-improving` |
| 7 | 分析/统计/结果/图/表/回归/生存/ROC | `/clinpub-analysis` |
| 8 | 写/手稿/文献/引用/IMRAD/论文 | `/clinpub-writing` |
| 9 | 推进/下一步/继续 | 模式 3（推进） |
| 10 | 状态/摘要/总览/当前/什么阶段 | 模式 1（状态） |

规则：

- 组 4/5/6 必须排在组 8 之前，否则"审稿/投稿信/改稿"会被"稿"抢先命中
- 跨组冲突按**优先级**（组号小者优先），不按文本位置
- 不匹配停用词（"看/查/项目/做/搞/弄/整"），只匹配上表特异性术语
- 全不命中 → 回退到模式 1
- **路由后需用户确认**，确认后才提示其执行该命令

</process>

<success_criteria>
- 模式判定正确（无参 / help / next / 其他文本）
- 状态检测使用 3.0 判据（阶段2 = `ANALYSIS_SUMMARY.md` 存在；阶段3 = sections 全 final + 拼装校验）
- 阶段2 中间态只报告状态，**不替用户决定下一批**
- 推进必须先核验、生成 `MILESTONE.md`、取得签字，然后才更新 `STATE.md` / `ROADMAP.md`
- 未签字不推进
- 路由只提示不代跑，且经用户确认
- 输出包含可复制的命令名
</success_criteria>
