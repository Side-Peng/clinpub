---
phase: 02-断点续做
reviewed: 2026-05-05T18:30:00Z
depth: standard
files_reviewed: 2
files_reviewed_list:
  - commands/clinpub/do.md
  - commands/clinpub/next-step.md
findings:
  critical: 5
  warning: 7
  info: 3
  total: 15
status: issues_found
---

# Phase 2: 断点续做 — Code Review Report

**Reviewed:** 2026-05-05T18:30:00Z
**Depth:** standard
**Files Reviewed:** 2
**Status:** issues_found

## Summary

Reviewed two AI agent instruction files (`do.md`, `next-step.md`) for the Phase 2 breakpoint-resume feature. Both files are well-structured with clear frontmatter, interfaces, process steps, and success criteria. Anti-pattern awareness (Pitfall 1-4) is commendable.

However, several critical issues were found: contradictory NL routing rules, undefined variables in decision logic, broken cross-references that skip validation steps, execution context pointing to template files instead of live data, and ROADMAP.md update instructions that don't match the actual file format. The MILESTONE.md generation format also diverges from the canonical template.

---

## Critical Issues

### CR-01: NL 关键词 — 冲突解决规则矛盾（优先级优先 vs 最先出现优先）

**File:** `commands/clinpub/do.md:84,88`
**Issue:** Line 84 声明"命中高优先级关键词立即路由，不继续检查低优先级"，但 Line 88 声明"跨组冲突时...检测文本中最先出现的关键词组"。两条规则在同一个输入上可能产生不同路由结果。

举例：用户输入"写分析"：
- **按优先级规则（line 84）**：Group 3（分析，优先级 3）高于 Group 4（写，优先级 4），应路由到 `analysis`。
- **按位置规则（line 88）**："写"（Group 4）在文本中先于"分析"（Group 3）出现，应路由到 `writing`。

两条规则无法同时成立。AI 在解释矛盾规则时行为不可预测，会导致路由结果不稳定。

**Fix:** 删除 line 88 的位置规则，或明确说明其只在同优先级内起作用。建议保持优先级优先策略：
```
- **跨组冲突时**（如同时包含"分析"和"写"）：以优先级高的为准（Group 编号小的优先），不按文本位置判断。
```

---

### CR-02: next-step.md execution_context 引用 project_config.yml 模板文件而非实际项目文件

**File:** `commands/clinpub/next-step.md:50`
**Issue:** execution_context 使用 `@./pipeline/templates/project_config.yml` 加载的是**模板**文件，其 `waves: {}` 始终为空。AI 读到该引用后会加载模板内容，而非项目根目录的实际 `project_config.yml`。当实际项目已定义 Wave 结构时，AI 会误认为 `waves: {}` 导致 Phase 2 状态判断完全错误。

Section 1.3（line 97-98）的 shell 命令正确地从 `project_config.yml`（根目录）读取，但 execution_context 的 `@` 引用在 context 加载阶段就已经喂给 AI 了错误的数据。

**Fix:** 将 line 50 改为引用实际项目配置：
```
@./project_config.yml
```
或移除该引用，只在 shell 命令中使用（line 97-98 已正确引用根目录文件）。

---

### CR-03: next-step.md Phase 2 推进决策使用未定义变量 `ALL_WAVES_COMPLETE`

**File:** `commands/clinpub/next-step.md:232-233`
**Issue:** Section 3.1 的决策逻辑（line 232）中使用 `ALL_WAVES_COMPLETE` 变量，但该变量在整个文档中从未被赋值。Section 2.3（line 163-164）只定义了 `WAVE_COMPLETE`（最后一个 Wave 的完成状态），但决策逻辑需要的是"所有 Wave 都完成"的布尔值。

```
if HAS_WAVE_STRUCTURE and not ALL_WAVES_COMPLETE:
  推进到下一 Wave（Wave +1）
elif HAS_WAVE_STRUCTURE and ALL_WAVES_COMPLETE:
  推进到下一 Phase（Phase 3）
```

如果 `ALL_WAVES_COMPLETE` 始终为 undefined（falsy），则分支永远进入"推进到下一 Wave"，即使所有 Wave 已完成也无法推进到 Phase 3。

**Fix:** 在 Section 2.3 验证逻辑末尾赋值 `ALL_WAVES_COMPLETE`：
```
if [ "$WAVE_SUMMARY" -gt 0 ]; then
  WAVE_COMPLETE=true
  ALL_WAVES_COMPLETE=true     # <-- 新增：最后一个 Wave 有 SUMMARY → 全部完成
else
  WAVE_COMPLETE=false
  ALL_WAVES_COMPLETE=false    # <-- 新增
fi
```

并在 Section 2.3 通过条件说明中同步引用 `ALL_WAVES_COMPLETE`。

---

### CR-04: next-step.md PHASE=0 跳转到不存在的节，跳过验证流程

**File:** `commands/clinpub/next-step.md:73`
**Issue:** Line 70-73 指令：当 PHASE=0 时，"直接跳转到「4. 推进到下一 Phase」"。但该文档的 section 4 是"生成 MILESTONE.md"，不含任何"推进到下一 Phase"的逻辑。推进逻辑在 section 3（推进决策）。

此错误导致两个后果：
1. **跳过 validation**：Section 2.1（Phase 0 验证）检查 project_config.yml 的完整性和字段有效性，被完全跳过。如果项目初始化不完整（如 project.name 仍为默认值），推进仍然发生。
2. **跳转到错误节**：Section 4（MILESTONE.md 生成）在没有任何决策上下文的情况下执行，生成的 MILESTONE 缺少 Phase 0 交付物信息。

**Fix:** 将 line 73 修正为：
```
→ 直接跳转到「3. 推进决策」
```
并确认 section 3 的 Phase 0→1 推进逻辑已包含必要的验证。

---

### CR-05: next-step.md ROADMAP.md 更新指令与实际文件格式不匹配

**File:** `commands/clinpub/next-step.md:278-280`
**Issue:** 指令要求更新 ROADMAP.md 的 Phase 状态 emoji（✅ Complete → 🔄 In Progress），但实际 ROADMAP.md（`.clinpub/ROADMAP.md`）的 Phase 表格没有独立的"状态"列。状态信息嵌入在"Goal"列中：

```
| # | Phase | Goal | Requirements | 工作量 |
| 1 | Bug Fixes | ✅ Complete | 2026-05-05 |
| 2 | 断点续做 | `/clinpub-do` + ... | NEXT-01... | 中 |
```

按指令修改 emoji 在 ROADMAP.md 中不可行——表格结构不同，没有"状态"列的 emoji 标记可供更新。AI 执行时可能破坏表格结构或错误修改。

**Fix:** 明确 ROADMAP.md 的更新方式。建议使用以下精确指令：
```
更新 ROADMAP.md Phase 表格中当前 Phase 对应的行：
- 将 "Goal" 列设为 "🔄 In Progress"（移除旧的 emoji/状态标记）
- 不修改其他列
```

或重新设计 ROADMAP.md 表格增加独立状态列，使更新规则可程式化。

---

## Warnings

### WR-01: do.md data2idea 命令缺少 NL 关键词路由

**File:** `commands/clinpub/do.md:74-82`
**Issue:** 成功标准要求"所有 8 个命令的路由映射完整"，且未初始化提示（line 155）建议用户使用 `/clinpub-data2idea`。但 NL 关键词表（line 74-82）中没有能路由到 `data2idea` 的关键词组——唯一的 data2idea 入口是 STATE.md 不存在时的硬编码建议。用户输入"选题"、"话题挖掘"、"data2idea"等意图时无法通过 NL 路由到达 data2idea 命令。

**Fix:** 在关键词表中新增一组（优先级介于当前 Group 1-2 或其它合适位置）：
```
| 1.5 | (选题|话题挖掘|data2idea|idea|矿) | data2idea | 中 |
```

用户如果未初始化项目又需要"选题"，NL 直接路由到 data2idea 比回退到无参状态检测更符合预期。

---

### WR-02: do.md Phase 2 完成条件在 interfaces 和路由表中定义不一致

**File:** `commands/clinpub/do.md:37-39,131,196-201`
**Issue:** Interfaces 节（line 38）定义 Phase 2 检测模式为两个条件：`04_Outputs/` 非空 **AND** `project_config.yml analysis_plan.waves`。反模式规避说明（line 136-137）也强调"同时检查两者"。但路由表（line 200）的"完成条件"列只写了 `04_Outputs/ 非空`，不包含 waves 检查。

这种不一致导致 AI 无法确定 Phase 2 完成的完整判定标准：是只靠 `04_Outputs/`，还是必须两者皆满足？

**Fix:** 统一两者的定义。路由表 Phase 2 完成条件改为：`04_Outputs/ 非空 且 analysis_plan.waves 有定义`。同时将 line 204-205 的"Phase 2 的特殊处理"整合到路由条件中，使 waves 成为判定依据而非仅增强建议文本。

---

### WR-03: next-step.md Wave SUMMARY.md 搜索使用脆弱的子串匹配

**File:** `commands/clinpub/next-step.md:155-156`
**Issue:** `find .clinpub/phases -name "*SUMMARY.md" -path "*/02*" | grep -c "$LAST_WAVE"` 存在以下问题：
1. `grep -c "$LAST_WAVE"` 是子串匹配：LAST_WAVE=2 会匹配 `02-02-SUMMARY.md`（正确），也会匹配 `02-20-SUMMARY.md`（如果存在，错误）。
2. `-path "*/02*"` 只要求路径中包含"02"，可能在深度嵌套的目录结构中产生误匹配。
3. `find` 命令在 Wave 数量较多时可能产生误中。

**Fix:** 使用精确匹配模式之一：
```
# 方案 A：精确文件名匹配
WAVE_SUMMARY=$(find .clinpub/phases -name "02-${LAST_WAVE}-SUMMARY.md" 2>/dev/null | wc -l)

# 方案 B：全路径精确匹配（注意转义）
WAVE_SUMMARY=$(find .clinpub/phases -path "*/02-${LAST_WAVE}-SUMMARY.md" 2>/dev/null | wc -l)

# 方案 C：使用 test -f 直接检查
if [ -f ".clinpub/phases/02-断点续做/02-${LAST_WAVE}-SUMMARY.md" ]; then
  WAVE_COMPLETE=true
fi
```

---

### WR-04: next-step.md Section 1.3 WAVES=0 跳转到错误节

**File:** `commands/clinpub/next-step.md:101`
**Issue:** Line 101 指令："→ 跳转到「4. 推进到下一 Phase」的 Phase 2 特殊处理"。但 section 4 是"生成 MILESTONE.md"，不含"推进到下一 Phase"的逻辑。Phase 2 的 WAVES=0 情况需要在 section 2.3（验证）和 section 3.1（决策）中处理，而非 MILESTONE.md 生成阶段。

**Fix:** 改为跳转到 section 2（验证完成状态）的 Phase 2 验证子节：
```
→ 跳转到「2.3 Phase 2 验证」
```

或直接继续顺序执行到 section 2（因为 WAVES=0 不需要特殊跳过 validation）。

---

### WR-05: next-step.md MILESTONE.md 生成格式与模板不一致

**File:** `commands/clinpub/next-step.md:296-323`
**Issue:** 生成的 MILESTONE.md 使用简化格式，与 `pipeline/templates/milestone.md` 的完整格式不一致：

| 差异项 | 模板格式 | 生成格式 |
|--------|---------|---------|
| 成功标准验证 | 有 `## 成功标准验证` 节 | 缺失 |
| 产出文件格式 | 表格（文件、位置、说明） | 简单列表 |
| 未解决问题 | 有 `## 未解决问题 / 阻塞项` | 缺失 |
| 下一步节 | 有 `## 下一步` | 缺失 |

格式不一致可能导致 milestone 审查流程（checkpoints.md）无法正确解析后续 Phase 的 MILESTONE.md 内容。

**Fix:** 统一使用模板格式生成 MILESTONE.md，包括：
1. 新增 `## 成功标准验证` 节
2. 产出文件改为表格格式
3. 新增 `## 未解决问题` 节
4. 新增 `## 下一步` 节

---

### WR-06: next-step.md Phase 4 响应函路径未指定

**File:** `commands/clinpub/next-step.md:200-206`
**Issue:** Phase 4 验证要求"响应函（response letter）存在"，但没有指定文件路径或命名约定。AI 不确定应查找 `05_Manuscript/response-letter.md`、`05_Manuscript/final/response-letter.md` 还是其他路径。路径不明确导致验证结果不可复现。

**Fix:** 指定响应函的标准路径和命名格式：
```
验证（Phase 4 同行评审）:
  - 05_Manuscript/final/ 下至少有一个 .md 文件（修改后终稿）
  - 05_Manuscript/response-letter.md 存在（响应函）
```

---

### WR-07: do.md NL "继续" 关键词与特定命令关键词的优先级递补问题

**File:** `commands/clinpub/do.md:81,84,88`
**Issue:** "继续"（Group 6，路由到 next-step）是一个低特异性的常见词。按位置优先规则（line 88），如果用户输入"继续写稿"，"继续"出现在"写"之前，路由到 next-step 而非 writing。但用户的明确意图是"写稿"（writing）。

按优先级规则（line 84），"写"（Group 4）优先级高于"继续"（Group 6），路由到 writing。两条规则矛盾（见 CR-01）。即使在优先级规则下，"继续分析"（继续出现在分析之前）也能正确路由到 analysis，因为"分析"（Group 3）优先级高于"继续"（Group 6）。

但"继续推进"中，"继续"（Group 6）== "推进"（也在 Group 6），正确路由到 next-step。

该问题的根因仍是 CR-01 的规则矛盾。在 CR-01 修复后，此问题自然解决。

**Fix:** 与 CR-01 相同——明确优先级优先，删除位置规则。

---

## Info

### IN-01: do.md 命令名称映射表缺少 data2idea 和 do 自身

**File:** `commands/clinpub/do.md:93-103`
**Issue:** 命令名称映射表列出了 init-project、data-prep、analysis、writing、review、next-step、milestone 共 7 个目标命令，但缺少 data2idea 和 do 自身。成功标准要求"所有 8 个命令的路由映射完整"，但映射表只有 7 个。

data2idea 仅在未初始化建议（line 155）中出现，不在映射表中。do 自身也不在映射表中（虽然正常情况不需要路由到自身）。

**建议:** 在映射表中增加 data2idea 行并注明其使用场景（无需初始化的选题挖掘）。

---

### IN-02: next-step.md MILESTONE_PATH 的 phase-slug 推导未说明

**File:** `commands/clinpub/next-step.md:295`
**Issue:** `MILESTONE_PATH=".clinpub/phases/{N}-{phase-slug}/MILESTONE.md"` 中的 `{phase-slug}` 没有推导方式说明。AI 需要从 Phase 编号获得中文 slug（如 Phase 2 → "断点续做"），但文档没有提供映射表或推导方法。

实际引用 ROADMAP.md 可以获得 Phase 名称，但在指令中明确说明来源会更可靠。

**建议:** 在 MILESTONE_PATH 定义前增加一行："从 ROADMAP.md 的 Phase 表格读取 Phase N 对应的名称作为 slug"。

---

### IN-03: do.md/NL 规则中停用词表可能漏掉常见无意义词

**File:** `commands/clinpub/do.md:89`
**Issue:** 反模式规避列出的停用词为"看"、"查"、"项目"、"做"。但中文 NL 中还有一些常见高频无意义词如"搞"、"弄"、"整"、"来"、"去"等，用户可能用于特定短语中（"搞分析"、"弄个图"）。

**建议:** 增加以下停用词："搞"、"弄"、"整"、"来"、"去"、"给"、"把"、"用"。

---

_Reviewed: 2026-05-05T18:30:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
