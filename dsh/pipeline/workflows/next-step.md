---
name: clinpub next
description: "自动推进到下一步。验证当前阶段完成状态，判断该继续本阶段还是推进到下一阶段，更新 STATE.md 与 ROADMAP.md，阶段切换时生成 MILESTONE.md，并输出明确的下一步提示。"
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
自动推进。检查当前完成状态，决定"继续本阶段"还是"推进到下一阶段"，更新跟踪文件并给出提示。

## 行为模式

- **D-05 推进判断**：本阶段未完成 → 停在当前阶段并说明缺什么；已完成 → 推进到下一阶段
- **D-06 完成验证**：按 3.0 判据验证（见 §2），不只看文件是否存在
- **D-07 检查点**：推进后更新 STATE.md + ROADMAP.md + 生成 MILESTONE.md（防止 `phase-boundary.sh` 阻挡后续操作）

> **3.0 变化**：不再有 Wave 概念。阶段2 的完成判据是 `ANALYSIS_SUMMARY.md` 存在；
> 阶段3 的完成判据是 `sections/` 六节全 `final` 且拼装脚本校验通过。
</objective>

<interfaces>
<!-- 关键检测模式，executor 直接使用 -->

Phase 行读取:
```bash
grep -oP '阶段：Phase\s*\K\d' .clinpub/STATE.md
```

Plan checkbox 读取（ROADMAP.md）:
```bash
# 读取指定 Phase 的 Plan 完成状态
completed=$(grep -c "\[x\] $PHASE-" .clinpub/ROADMAP.md)
total=$(grep -c "\- \[.\] $PHASE-" .clinpub/ROADMAP.md)
```

阶段2 / 阶段3 进度读取（3.0）:
```bash
# 已完成分析批次数量
BATCHES=$(grep -c '^## Batch' .clinpub/ANALYSIS_LOG.md 2>/dev/null || echo 0)
# 分析是否已冻结
test -f .clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md && FROZEN=true || FROZEN=false
# 手稿章节状态
grep -h '^status:' 05_Manuscript/sections/*.md 2>/dev/null | sort | uniq -c
```
</interfaces>

<execution_context>
@./.clinpub/STATE.md
@./.clinpub/ROADMAP.md
@./project_config.yml
@./pipeline/references/checkpoints.md
@./pipeline/templates/milestone.md
</execution_context>

<process>

## 1. 读取当前状态

### 1.1 从 STATE.md 获取当前 Phase

```bash
# 使用正则匹配 `- 阶段：Phase N` 结构化行
# 与 workflow-guard.js D-02 逻辑一致
PHASE=$(grep -oP '阶段：Phase\s*\K\d' .clinpub/STATE.md)

# 如果 PHASE 为空 → STATE.md 没有 Phase 标识行
#   → 输出错误: "STATE.md 未包含 Phase 标识行，项目可能未初始化。请执行 /clinpub-init"
#   → 结束命令

# 如果 PHASE=0 → 项目刚初始化
#   → 输出: "当前阶段0 (初始化阶段)。需要推进到阶段1 数据清洗。"
#   → 直接跳转到「3. 推进决策」
```

### 1.2 从 ROADMAP.md 获取 Plan 完成状态

```bash
# 读取当前 Phase 的所有 Plan checkbox 状态
# 格式: "- [x] 02-01 基线描述"
# 格式: "- [ ] 02-02 组间比较与纵向分析"
COMPLETED=$(grep -c "\[x\] $PHASE-" .clinpub/ROADMAP.md)
TOTAL=$(grep -c "\- \[.\] $PHASE-" .clinpub/ROADMAP.md)

# 如果 TOTAL=0 → 当前 Phase 没有 Plan 定义
#   → 可能是新 Phase 尚未规划
#   → 输出: "Phase $PHASE 尚未规划 Plans。请执行 /gsd-plan-phase $PHASE"
#   → 结束命令
```

**反模式规避（Pitfall 1）**: 以 ROADMAP.md 的 checkboxes 为"源 truth"判断完成状态，以 STATE.md 的 `- 阶段：Phase N` 为当前定位。如果 STATE.md 的 Phase 编号与 ROADMAP.md 最新完成的 Phase 不一致（例如 STATE.md 显示阶段2 但 ROADMAP.md 显示阶段2 全部完成），以 ROADMAP.md 为准输出警告并在推进时自动修正。

### 1.3 从 ANALYSIS_LOG 与 SUMMARY 获取阶段2 进度（3.0）

```bash
# 仅当 PHASE=2 时执行
LOG=".clinpub/ANALYSIS_LOG.md"
SUMMARY=".clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md"

# 已完成批次数量
BATCHES=$(grep -c '^## Batch' "$LOG" 2>/dev/null || echo 0)

# 冻结标记：摘要文件存在 = 分析已收口
if [ -f "$SUMMARY" ]; then FROZEN=true; else FROZEN=false; fi
```

判定：

| 状态 | 含义 | 动作 |
|---|---|---|
| `LOG` 不存在 | 阶段2 未开始 | 推进到阶段2 第一批 |
| `LOG` 存在、`SUMMARY` 不存在 | **迭代进行中** | 提示继续分析，不推进 |
| `SUMMARY` 存在 | 分析已冻结 | 进入「2.3 阶段2 验证」 |

**反模式规避**：不再读 `analysis_plan.waves`（3.0 已废弃）。批次数量只是进度指示，**完成判据是 `ANALYSIS_SUMMARY.md` 是否存在**——它由 `freeze_analysis` 步骤产出。

---

## 2. 验证完成状态（D-06）

推进前验证当前步骤是否完成，按 Phase 分别验证：

### 2.1 阶段0 验证（项目初始化）

```
验证：
  - project_config.yml 存在
  - project.name 非空且不是默认值 "项目名称"
  - 结局已定义：`variables.outcome` 非空 **或** `analysis_mode: exploratory`（探索性研究允许结局待第一批分析确定）
  - paths.raw_data 对应目录存在且有数据文件

通过 → 跳转到「4. 推进到下一 Phase」
不通过 → 输出未完成项列表
```

### 2.2 阶段1 验证（数据清洗）

```
验证：
  - 02_PreprocessedData/data/cleaned.csv 存在
  - 02_PreprocessedData/reports/ 下有数据质量报告

通过 → 跳转到「4. 推进到下一 Phase」
  （阶段1 没有波浪结构，直接推进到阶段2）
不通过 → 输出未完成项列表
```

### 2.3 阶段2 验证（迭代分析）

```
验证：
  1. .clinpub/ANALYSIS_LOG.md 存在
  2. 每个 Batch 六段齐全（依据 / 本批方法 / 结果要点 / 解读 / 下一批决策 / 否决项）
     → 缺段只警告，不阻塞（历史批次可能格式较旧）
  3. .clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md 存在（= 分析已冻结）
  4. 04_Outputs/MANIFEST.yaml 存在
  5. 04_Outputs/ 至少一个方法目录

通过 → 推进到阶段3
不通过 → 输出未完成项列表
```

未完成时输出示例:
```
阶段2 (迭代分析) — 尚未冻结

检测结果:
  - ANALYSIS_LOG.md: 存在，已完成 {BATCHES} 个批次
  - ANALYSIS_SUMMARY.md: 未找到（分析未冻结）
  - 04_Outputs/: 有输出内容

未完成项:
  1. 分析尚未冻结 — 缺少 ANALYSIS_SUMMARY.md

建议:
  - /clinpub-analysis      → 继续下一批分析
  - /clinpub next     → 若认为分析已够，执行冻结与关卡核验
```
```

### 2.4 阶段3 验证（递进式写作）

```
验证：
  1. 05_Manuscript/sections/ 下六节齐全
     （results / methods / discussion / conclusion / introduction / abstract）
  2. 每节 frontmatter 的 status 均为 final
  3. python scripts/assemble_manuscript.py --check 通过
  4. 05_Manuscript/manuscript.md 存在

通过 → 核心管线完成（阶段3 为最后一个编号阶段）。输出完成信息并建议独立工具：
  - /clinpub-improving   → 自审并直接修稿（可反复）
  - /clinpub-coverletter → 按目标期刊生成投稿信
  - /clinpub-review      → 投稿后，录入真实审稿意见并回复 + 修稿
不通过 → 输出未完成项列表
```

未完成时输出示例:
```
阶段3 (写作) — 尚未完成

检测结果:
  - sections/: 6 节存在，其中 2 节非 final
  - 非 final 章节: results(stale), discussion(stale)
  - manuscript.md: 存在（但已落后于 sections）

未完成项:
  1. results 与 discussion 为 stale，需重写
  2. 拼装脚本拒绝在存在 stale 章节时生成

建议:
  - /clinpub-improving     → 按其计划重写 stale 章节并重拼
  - /clinpub-writing       → 或从对应步骤继续写作
```

---

## 3. 推进决策（D-05）

完成验证通过后，自动判断推进粒度。

### 3.1 推进判断逻辑（3.0）

```
CURRENT_PHASE = 从 STATE.md 读取
PHASE_COMPLETE = 按 §2 的对应判据（不是"有文件就算完成"）

if not PHASE_COMPLETE:
  # 本阶段未完成 → 不推进，说明缺什么
  输出未完成项 + 建议命令
  结束

else:
  if CURRENT_PHASE == 0: 推进到阶段1
  elif CURRENT_PHASE == 1: 推进到阶段2
  elif CURRENT_PHASE == 2: 推进到阶段3
  elif CURRENT_PHASE == 3:
     输出: "🎉 核心管线已完成（阶段0-3）。后续可用独立工具：improving / coverletter / review"
```

**阶段2 中间态（迭代进行中）**：`ANALYSIS_LOG.md` 存在但 `ANALYSIS_SUMMARY.md` 不存在 →
`PHASE_COMPLETE = false`，**不推进**。输出：

```
阶段2 (迭代分析) — 进行中

已完成 {BATCHES} 个批次
最后一批的「下一批决策」: {decision}

建议:
  /clinpub-analysis    → 继续下一批分析
  /clinpub next   → 若认为分析已够，执行冻结与关卡核验
```

**阶段3 中间态（有 stale/draft 章节）**：`PHASE_COMPLETE = false`，输出非 final 章节列表，
建议 `/clinpub-improving` 或 `/clinpub-writing`。

### 3.2 阶段2 内部不再有"Wave 推进"

3.0 的分析是迭代的，"下一批做什么"由 `analysis_decision_policy.md` 的规则决定并写入
`ANALYSIS_LOG.md`，**不是**由本命令推进。本命令遇到阶段2 中间态时只报告状态，不替用户决定下一批。

### 3.3 Phase 推进（跨 Phase）

```
更新操作:
  1. 读取下一 Phase 的编号和名称（从 ROADMAP.md 表格获取，或使用 ROADMAP.md `## Phase Details` 节）
  2. 生成 MILESTONE.md（见 Step 4）
  3. 更新 STATE.md:
     - `- 阶段：Phase N` → `- 阶段：Phase N+1`
     - `**当前状态**: ...` → 更新为 "Phase {N+1} ({name}) — 进行中"
  4. 更新 ROADMAP.md:
     - ROADMAP.md Phase 表格的完成状态在"Goal"列，没有独立状态列
     - 当前 Phase 完成: 将 Goal 列设为 "✅ Complete"
     - 下一 Phase 开始: 将 Goal 列设为 "🔄 In Progress"
     - 注意: 不自动勾选 Plan checkboxes（[ ] → [x]），这由 executor 在 Plan 完成时操作
  5. 更新 STATE.md 的 `progress.completed_phases` 计数 +1（frontmatter YAML 中）
  6. 输出 clear 提示（见 Step 5）

**反模式规避（Pitfall 4）**: 推进到新 Phase 时，必须先生成 MILESTONE.md。否则 phase-boundary.sh:48-61 检查上一 Phase 的 MILESTONE.md 时会阻挡后续操作。MILESTONE.md 的生成是 Phase 推进的前提条件，不可跳过。
```

---

## 4. 生成 MILESTONE.md（D-07 检查点）

当推进到新 Phase 时，必须生成 MILESTONE.md 防止 phase-boundary.sh 阻挡（Pitfall 4 规避）。

### 4.1 MILESTONE.md 生成

```
MILESTONE_PATH=".clinpub/phases/{N}-{phase-slug}/MILESTONE.md"

写入内容（参考 checkpoints.md 和 templates/milestone.md）:
---
# Milestone: 阶段{N} — {name}

**完成日期**: {YYYY-MM-DD}
**状态**: ✅ Complete

## 交付物清单
- [x] {Phase N 的关键交付物 1}
- [x] {Phase N 的关键交付物 2}
- [x] {Phase N 的关键交付物 3}

## 关键决策
{如果有记录决策，写入；否则写 "无关键决策记录"}

## 产出文件
{列出关键产出文件路径}

## 用户签字
- [ ] 用户确认进入 Phase {N+1}
---

注意:
- MILESTONE.md 在 Phase 推进时自动生成，但不自动标记用户签字（等待用户确认）
- 标记为 ✅ Complete 表示 Phase 交付物已就绪，等待签字
- 用户签字后，phase-boundary.sh 可以正常通过（其第 48-61 行的检查会看到 ✅ 标记）
```

---

## 5. Clear 提示输出（D-08, D-09）

所有推进操作（Phase 级）完成后，输出标准化的三要素 clear 提示。

### 5.1 输出格式

```markdown
---

## 下一步

对话可能已积累较多上下文。建议先 `/clear` 清除上下文，然后继续：

{下一条建议命令}

### 进度总结
- 阶段1 (数据清洗): {✅ 已完成 / ⏳ 未完成 / —}
- 阶段2 (统计分析): {✅ 已完成 / ⏳ 进行中 / —}
- 阶段3 (手稿撰写): {✅ 已完成 / ⏳ 进行中 / —}
- 独立工具 (改进/投稿信/审稿回复): {可用 / —}

---

**提示**: 以上信息已同步更新到 `.clinpub/STATE.md` 的「下一步」节。
```

### 5.2 各场景的提示内容

| 场景 | `/clear` 后执行 | 进度总结示例 |
|------|----------------|-------------|
| 阶段2 中间态（未冻结） | `/clinpub-analysis` — 继续下一批分析 | 阶段1 ✅ \| 阶段2 ⏳ Batch {N} \| 阶段3 ⏳ |
| 阶段0→1 推进 | `/clinpub-data-prep` — 进入数据清洗 | 阶段1 ⏳ 当前 \| 阶段2-3 ⏳ |
| 阶段1→2 推进 | `/clinpub-analysis` — 进入迭代分析 | 阶段1 ✅ \| 阶段2 ⏳ 当前 \| 阶段3 ⏳ |
| 阶段2→3 推进 | `/clinpub-writing` — 进入递进写作 | 阶段1 ✅ \| 阶段2 ✅ \| 阶段3 ⏳ 当前 |
| 阶段3 完成（核心终点） | `/clinpub-improving`（改进）/ `/clinpub-coverletter`（投稿信）/ `/clinpub-review`（投稿后） | 阶段1-3 ✅ 🎉 核心完成 |
| 阶段签字 | `/clinpub next <N>` — 阶段关卡签字 | 对应 Phase ✅ |

### 5.3 STATE.md 同步

在 STATE.md 的 `## 下一步` 节中同步写入相同的三要素内容（见 Task 3 的 STATE.md 修改）。
</process>

<success_criteria>
- 未完成时给出明确提示和未完成项列表，不自动推进
- 完成时按 3.0 判据推进（阶段2 = `ANALYSIS_SUMMARY.md` 存在；阶段3 = sections 全 final + 拼装校验通过）
- 阶段2 中间态只报告状态（批次数 + 最后一批决策），**不替用户决定下一批**
- Phase 推进: 更新 STATE.md 的 Phase 编号与 ROADMAP.md 完成状态，同时生成 MILESTONE.md
- Phase 推进时生成 MILESTONE.md，防止 `phase-boundary.sh` 阻挡后续操作（Pitfall 4 规避）
- STATE.md 和 ROADMAP.md 同步更新，内容一致
- 输出包含三要素的 clear 提示（/clear + 下一条命令 + 进度总结）
- 以 ROADMAP.md checkboxes 为阶段进度参考，STATE.md 的 `- 阶段：Phase N` 为当前定位（Pitfall 1 规避）
- **不再读取 `analysis_plan.waves`**（3.0 已废弃）
</success_criteria>
