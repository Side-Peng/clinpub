---
name: next-step
description: "Auto-advance to the next Phase or Wave. Verifies current step completion, auto-detects granularity (Wave vs Phase), updates STATE.md and ROADMAP.md, generates MILESTONE.md for phase transitions, and outputs clear prompt with next steps."
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
Phase/Wave auto-advancement. Checks current completion status, decides whether to advance to next Wave (within same Phase) or next Phase (all Waves done), updates tracking files, and outputs clear prompt.

## 行为模式

- **D-05 粒度自动判断**: 同 Phase 还有未完成 Wave → 推进到下一 Wave；全部完成 → 推进到下一 Phase
- **D-06 完成验证**: 推进前验证当前步骤是否完成（SUMMARY.md 存在性、工件存在性等）
- **D-07 检查点**: 推进后更新 STATE.md + ROADMAP.md + 生成 MILESTONE.md（防止 phase-boundary.sh 阻挡后续操作）
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

Wave 进度读取（project_config.yml）:
```bash
# 读取 analysis_plan.waves 字段
grep -A 100 "analysis_plan:" project_config.yml | grep -E "^\s+\d+:" | wc -l
```
</interfaces>

<execution_context>
@./pipeline/references/checkpoints.md
@./pipeline/templates/milestone.md
</execution_context>

<process>

## 0. 加载项目状态文件

在执行后续步骤前，先用 Read 工具读取以下项目文件作为上下文：
- `.clinpub/STATE.md`
- `.clinpub/ROADMAP.md`
- `project_config.yml`

这三个文件包含当前阶段状态、Plan 完成进度和分析 Wave 定义，是后续步骤的输入。

## 1. 读取当前状态

### 1.1 从 STATE.md 获取当前 Phase

```bash
# 使用正则匹配 `- 阶段：Phase N` 结构化行
# 与 workflow-guard.js D-02 逻辑一致
PHASE=$(grep -oP '阶段：Phase\s*\K\d' .clinpub/STATE.md)

# 如果 PHASE 为空 → STATE.md 没有 Phase 标识行
#   → 输出错误: "STATE.md 未包含 Phase 标识行，项目可能未初始化。请执行 /clinpub:init"
#   → 结束命令

# 如果 PHASE=0 → 项目刚初始化，没有 Wave 需要推进
#   → 输出: "当前 Phase 0 (初始化阶段)。需要推进到 Phase 1 数据清洗。"
#   → 直接跳转到「3. 推进决策」
```

### 1.2 从 ROADMAP.md 获取 Plan 完成状态

```bash
# 读取当前 Phase 的所有 Plan checkbox 状态
# 格式: "- [x] 02-01-PLAN.md — Wave 1: 基线描述"
# 格式: "- [ ] 02-02-PLAN.md — Wave 2: 组间比较"
COMPLETED=$(grep -c "\[x\] $PHASE-" .clinpub/ROADMAP.md)
TOTAL=$(grep -c "\- \[.\] $PHASE-" .clinpub/ROADMAP.md)

# 如果 TOTAL=0 → 当前 Phase 没有 Plan 定义
#   → 可能是新 Phase 尚未规划
#   → 输出: "Phase $PHASE 尚未规划 Plans。请执行 /gsd-plan-phase $PHASE"
#   → 结束命令
```

**反模式规避（Pitfall 1）**: 以 ROADMAP.md 的 checkboxes 为"源 truth"判断完成状态，以 STATE.md 的 `- 阶段：Phase N` 为当前定位。如果 STATE.md 的 Phase 编号与 ROADMAP.md 最新完成的 Phase 不一致（例如 STATE.md 显示 Phase 2 但 ROADMAP.md 显示 Phase 2 全部完成），以 ROADMAP.md 为准输出警告并在推进时自动修正。

### 1.3 从 project_config.yml 获取 Wave 进度（针对 Phase 2）

```bash
# 仅当 PHASE=2 时执行
# 读取 analysis_plan.waves 字段
WAVES=$(grep -A 100 "analysis_plan:" project_config.yml 2>/dev/null | grep -E "^\s+\d+:" | wc -l)

# 如果 WAVES=0（即 waves: {} 或字段不存在）
#   → Phase 2 尚未定义 Wave → 视为 Wave 0（未开始）
#   → 跳转到「2.3 Phase 2 验证」
# 如果 WAVES>0
#   → 检查最后一个 Wave 的 SUMMARY.md 是否存在
#   → 存在 → 所有 Wave 完成 → 推进到 Phase 3
#   → 不存在 → 当前 Wave 未完成 → 提示继续
```

**反模式规避（Pitfall 2）**: 当 `analysis_plan.waves: {}`（空对象）时，视作 Phase 2 尚未开始，不因此判定出错。同时检查 `04_Outputs/` 目录内容作为 Phase 2 完成度的辅助信号。

---

## 2. 验证完成状态（D-06）

推进前验证当前步骤是否完成，按 Phase 分别验证：

### 2.1 Phase 0 验证（项目初始化）

```
验证：
  - project_config.yml 存在
  - project.name 非空且不是默认值 "项目名称"
  - variables.outcome 非空
  - paths.raw_data 对应目录存在且有数据文件

通过 → 跳转到「4. 推进到下一 Phase」
不通过 → 输出未完成项列表
```

### 2.2 Phase 1 验证（数据清洗）

```
验证：
  - 02_PreprocessedData/data/cleaned.csv 存在
  - 02_PreprocessedData/reports/ 下有数据质量报告

通过 → 跳转到「4. 推进到下一 Phase」
  （Phase 1 没有波浪结构，直接推进到 Phase 2）
不通过 → 输出未完成项列表
```

### 2.3 Phase 2 验证（统计分析，有 Wave 结构）

```
验证（按从上一步读取的 Wave 信息）:
  如果 WAVES=0 → Phase 2 尚未有 Wave 定义
    → 验证 04_Outputs/ 是否有任何输出
      → 有输出 → 但无 Wave 结构，输出警告"04_Outputs/ 有内容但 project_config.yml 未定义 Wave 结构"
      → 无输出 → 一切正常，Phase 2 尚未开始

  如果 WAVES>0:
    # 读取最后一个 Wave 的完成状态
    LAST_WAVE=$(grep -E "^\s+\d+:" project_config.yml | tail -1 | tr -d ' :')
    # 检查最后一个 Wave 的 SUMMARY.md 是否存在
    # (SUMMARY.md 由 clinpub-executor 在每个 Wave 结束时生成)
    WAVE_SUMMARY=$(find .clinpub/phases -name "02-${LAST_WAVE}-SUMMARY.md" 2>/dev/null | wc -l)
    
    if [ "$WAVE_SUMMARY" -gt 0 ]; then
      WAVE_COMPLETE=true
      ALL_WAVES_COMPLETE=true
    else
      WAVE_COMPLETE=false
      ALL_WAVES_COMPLETE=false
    fi

通过条件：
  - WAVES=0 且 04_Outputs/ 无输出 → 未开始，推进到 Wave 1
  - WAVES=0 但 04_Outputs/ 有输出 → 警告但可推进（用户确认后进入「3. 推进决策」）
  - WAVES>0 且最后一个 Wave 有 SUMMARY.md → 所有 Wave 完成，推进到 Phase 3
  - WAVES>0 但最后一个 Wave 无 SUMMARY.md → 当前 Wave 未完成，输出提示

未完成时输出示例:
```
Phase 2 (统计分析) — 当前 Wave 未完成

检测结果:
  - 04_Outputs/: 有输出内容
  - Wave 结构: 已定义 {WAVES} 个 Wave
  - 最后一个 Wave's SUMMARY.md: 未找到

未完成项:
  1. 当前 Wave 的 SUMMARY.md 不存在 — 表示分析工作流未完成

建议:
  - /clinpub:analysis      → 继续当前 Wave 的分析
  - 手动检查 04_Outputs/  → 确认所有 Wave 任务是否确实完成
```
```

### 2.4 Phase 3 验证（手稿撰写）

```
验证：
  - 05_Manuscript/manuscript.md 存在
  - 05_Manuscript/ 下至少有一个完整的 IMRAD 章节

通过 → 跳转到「4. 推进到下一 Phase」
不通过 → 输出未完成项列表
```

### 2.5 Phase 4 验证（同行评审）

```
验证：
  - 05_Manuscript/final/ 下至少有一个经过修改的终稿
  - 响应函（response letter）存在

通过 → 输出庆祝信息: "所有 Phase 已完成！🎉"
不通过 → 输出未完成项列表
```

---

## 3. 推进决策（D-05）

完成验证通过后，自动判断推进粒度。

### 3.1 粒度自动判断逻辑

```
CURRENT_PHASE = 从 STATE.md 读取
ALL_COMPLETED = (COMPLETED == TOTAL)  # 所有 Plan checkbox 已勾选
HAS_WAVE_STRUCTURE = (WAVES > 0)      # project_config.yml 有 Wave 定义

if CURRENT_PHASE == 0:
  # Phase 0 → Phase 1
  推进到下一 Phase（Phase 1）

elif CURRENT_PHASE == 1:
  # Phase 1 无 Wave 结构 → 直接推进到 Phase 2
  推进到下一 Phase（Phase 2）

elif CURRENT_PHASE == 2:
  # Phase 2 有 Wave 结构 → 检查 Wave 完成状态
  if HAS_WAVE_STRUCTURE and not ALL_WAVES_COMPLETE:
    推进到下一 Wave（Wave +1）
  elif HAS_WAVE_STRUCTURE and ALL_WAVES_COMPLETE:
    推进到下一 Phase（Phase 3）
  elif not HAS_WAVE_STRUCTURE:
    # 没有 Wave 结构但有 04_Outputs/ 内容
    # → 输出警告后推进到 Phase 3
    推进到下一 Phase（Phase 3）+ 警告

elif CURRENT_PHASE == 3:
  # Phase 3 无 Wave 结构 → 直接推进到 Phase 4
  推进到下一 Phase（Phase 4）

elif CURRENT_PHASE == 4:
  # Phase 4 是最后一个 Phase
  if ALL_COMPLETED:
    输出: "🎉 恭喜！所有 Phase 已完成！"
  else:
    输出: "Phase 4 未完成，请继续 /clinpub:review"
```

### 3.2 Wave 推进（同 Phase 内）

```
更新操作:
  1. 输出: "推进到 Phase {N} 的下一 Wave（当前 Wave {W} → Wave {W+1}）"
  2. 不需要更新 STATE.md 的 `- 阶段：Phase N`（同 Phase 内不改变 Phase 编号）
  3. 更新 ROADMAP.md：
     - 将当前 Wave 对应的 Plan checkbox 标记为 [x]（如果未标记）
     - 不操作 — Plan checkbox 由 executor 在完成每个 Plan 时标记
  4. 输出下一 Wave 的提示:
     - 如果 project_config.yml 中定义了下一 Wave → 读取 wave.label 和 wave.methods 作为提示
     - 如果未定义 → 提示"需要先定义下一 Wave 的分析方法"
  5. 输出 clear 提示（见 Step 5）
```

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
# Milestone: Phase {N} — {name}

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

所有推进操作（Wave 或 Phase）完成后，输出标准化的三要素 clear 提示。

### 5.1 输出格式

```markdown
---

## 下一步

对话可能已积累较多上下文。建议先 `/clear` 清除上下文，然后继续：

{下一条建议命令}

### 进度总结
- Phase 1 (数据清洗): {✅ 已完成 / ⏳ 未完成 / —}
- Phase 2 (统计分析): {✅ 已完成 / ⏳ 进行中 / —}
- Phase 3 (手稿撰写): {✅ 已完成 / ⏳ 进行中 / —}
- Phase 4 (同行评审): {✅ 已完成 / ⏳ 进行中 / —}

---

**提示**: 以上信息已同步更新到 `.clinpub/STATE.md` 的「下一步」节。
```

### 5.2 各场景的提示内容

| 场景 | `/clear` 后执行 | 进度总结示例 |
|------|----------------|-------------|
| Wave 推进 (Phase 2) | `/clinpub:analysis` — 继续下一 Wave 分析 | Phase 1 ✅ \| Phase 2 ⏳ Wave 2 \| Phase 3-4 ⏳ |
| Phase 0→1 推进 | `/clinpub:data-prep` — 进入数据清洗 | Phase 1 ⏳ 当前 \| Phase 2-4 ⏳ |
| Phase 1→2 推进 | `/clinpub:analysis` — 进入统计分析 | Phase 1 ✅ \| Phase 2 ⏳ 当前 \| Phase 3-4 ⏳ |
| Phase 2→3 推进 | `/clinpub:writing` — 进入手稿撰写 | Phase 1 ✅ \| Phase 2 ✅ \| Phase 3 ⏳ 当前 \| Phase 4 ⏳ |
| Phase 3→4 推进 | `/clinpub:review` — 进入同行评审 | Phase 1-3 ✅ \| Phase 4 ⏳ 当前 |
| 全部完成 | `/clinpub:milestone 4` — 最终签字 | 全部 ✅ 🎉 |

### 5.3 STATE.md 同步

在 STATE.md 的 `## 下一步` 节中同步写入相同的三要素内容（见 Task 3 的 STATE.md 修改）。
</process>

<success_criteria>
- 未完成时给出明确提示和未完成项列表，不自动推进
- 完成时自动判断推进粒度（Wave vs Phase），正确遵循 D-05 规则
- Wave 推进: 同 Phase 内 Wave+1，不需要更新 STATE.md Phase 编号
- Phase 推进: STATE.md 更新 Phase 编号，ROADMAP.md 更新完成状态，同时生成 MILESTONE.md
- Phase 推进时生成 MILESTONE.md，防止 phase-boundary.sh 阻挡后续操作（Pitfall 4 规避）
- STATE.md 和 ROADMAP.md 同步更新，内容一致
- 输出包含三要素的 clear 提示（/clear + 下一条命令 + 进度总结）
- Wave 推进和 Phase 推进有不同的 clear 提示内容
- 以 ROADMAP.md checkboxes 为源 truth，STATE.md 为当前定位（Pitfall 1 规避）
- analysis_plan.waves 为空时特殊处理（Pitfall 2 规避）
</success_criteria>
