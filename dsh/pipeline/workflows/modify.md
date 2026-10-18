---
name: modify
description: "Ad-hoc analysis modification: 载入分析上下文 → 与用户确定改动 → 执行 → 校验 → 追加到 ANALYSIS_LOG → 把受影响章节标 stale 并重写 → 重拼手稿。支持改图表样式、改统计方法、新增分析方法。"
---

<purpose>
阶段2 完成后的定向修改：改图表样式、改变量/方法、新增分析方法。

与 2.x 的两点差异：

1. **记录位置**：不再写 `PLAN.md`，改为在 `.clinpub/ANALYSIS_LOG.md` 追加一个 `modify` 批次
2. **手稿处理**：不再直接改 `manuscript.md` 里的数字（它是生成物），而是把受影响章节标 `stale`，重写后重新拼装

可在任何阶段调用；分析已冻结时，修改会解锁对应批次。
</purpose>

<required_reading>
@./pipeline/references/analysis_methods.md
@./pipeline/references/analysis_decision_policy.md
@./pipeline/references/r_patterns.md
@./pipeline/references/writing_standards.md
@./agents/modify-agent.md
@./agents/writer-agent.md
</required_reading>

<process>

<step name="validate_prerequisites" priority="first">
```bash
PROJECT_DIR=$(pwd)
LOG="$PROJECT_DIR/.clinpub/ANALYSIS_LOG.md"
DATA="$PROJECT_DIR/02_PreprocessedData/data/cleaned.csv"
OUTPUTS="$PROJECT_DIR/04_Outputs/"
```

检查：

1. `.clinpub/ANALYSIS_LOG.md` 存在（若不存在 → "尚未完成分析，请先运行 `/clinpub-analysis`"）
2. `cleaned.csv` 存在
3. `04_Outputs/` 至少有一个方法目录

全部通过才继续。
</step>

<step name="define_modifications" priority="high">
委派 modify-agent 的 `build_method_inventory` 与 `define_modification`：

1. modify-agent 读 **`ANALYSIS_LOG.md`** 与 `03_AnalysisMethods/*/方法说明.md` 建立方法清单
2. 向用户呈现清单
3. 用户选方法并定义改动（样式 / 变量 / 方法 / 新增方法）
4. 输出结构化改动摘要
5. **检查点**：用户确认摘要

用户拒绝 → 停止，不产生任何改动。
</step>

<step name="execute_modifications" priority="high">
逐个执行确认过的改动：

1. **备份**：记录当前 commit hash 以便回滚
2. **修改**：改 R 脚本并重跑
3. **简报**：逐条报告成功/失败

```bash
PRE_MODIFY_HASH=$(git rev-parse --short HEAD)
```

执行顺序：**样式 → 变量 → 方法 → 新增方法**（风险由低到高，减少级联失败）。

**新增方法**：ID 必须为 `{NN}_{MethodName}`（如 `06_SensitivityAnalysis`），禁止 `_sensitivity` 这类裸下划线；`03_AnalysisMethods/{id}/` 与 `04_Outputs/{id}/` **必须同时创建**。

缺包时报告并跳过，**不要自动安装**。
</step>

<step name="verify_outputs" priority="medium">
对每个改动成功的方法：

1. 图文件存在且非空
2. 图 DPI ≥ 300
3. 图标注为英文
4. 表文件存在且统计量已更新
5. `方法说明.md` 已更新（尤其「输出结果」小节）
6. 统计报告含效应量 + 95%CI + 精确 p

失败时报告具体原因，并给出"重跑该改动 / 跳过"的选择。

**新增方法后**：确认 `03_AnalysisMethods/{id}/` 与 `04_Outputs/{id}/` 都存在，缺一个立即补建。
</step>

<step name="record_in_analysis_log" priority="high">
在 `.clinpub/ANALYSIS_LOG.md` 追加一个 **`Batch M-{n}（modify）`** 记录，沿用六段格式：

```markdown
## Batch M-{n} — 分析修改（{YYYY-MM-DD}）

### 依据
- 触发规则：U（用户驱动）
- 用户诉求：{summary}

### 本批方法
| id | 方法 | 改动类型 | 状态 |
|---|---|---|---|
| {id} | {method} | style/variable/method/new | ✅ |

### 结果要点
- {改动后的关键统计量，或"仅样式变更，统计量不变"}

### 解读
- {这次改动对结论的影响：无影响 / 改变方向 / 增强稳健性}

### 下一批决策
- 决定：结束修改
- 理由：{…}

### 否决项
- {未执行项及原因，或"无"}
```

同时更新 `STATE.md` 的「最近决策」行。
</step>

<step name="cascade_stale" priority="high">
**不要直接改 `manuscript.md`**（它是生成物，手改会被下次拼装覆盖）。

改为按依赖 DAG 标记：

```bash
# 若 05_Manuscript/ 不存在，跳过本步与后续
```

| 改动类型 | 需要置 stale 的章节 |
|---|---|
| 样式（仅图） | `results` |
| 变量 / 方法 / 新增方法 | `results` |
| 任何影响方法的改动 | `results` + `methods` |

然后按 DAG 向下游传播：`results` → `discussion` / `conclusion` / `introduction` / `abstract`；`methods` → `discussion` / `introduction` / `abstract`。

**具体做法**：把 `05_Manuscript/sections/{key}.md` 的 frontmatter 中 `status:` 改为 `stale`。
</step>

<step name="rewrite_stale_sections" priority="high">
把 stale 章节重写回 `final`，然后重新拼装：

1. 逐节委派 writer-agent 重写（按 `writing.md` 的对应步骤与输入契约）
   - 重写 `results` 时**必须**重新读 `04_Outputs/` 与 `FIGURE_SKELETON.md`
   - 重写 `discussion` 时**必须**重新读更新后的 `ANALYSIS_LOG.md`（新的敏感性分析/否决项会改变局限性段）
2. 每节写完把 `status` 改回 `final`
3. 运行：

```bash
python scripts/assemble_manuscript.py --check
python scripts/assemble_manuscript.py
```

若用户希望稍后再写，可只标记 stale 并提示：

```
分析已更新，以下章节需要重写：
  results, methods, discussion, conclusion, introduction, abstract
请稍后执行 /clinpub-improving 或重新运行 /clinpub-writing 处理 stale 章节。
拼装脚本会拒绝在存在 stale 章节时生成 manuscript.md。
```
</step>

<step name="completion_summary" priority="medium">
```
─────────────────────────────────────────
 Modify 完成
─────────────────────────────────────────
成功：{N} 项改动
失败：{M} 项
ANALYSIS_LOG 已追加 Batch M-{n}
受影响章节：{stale_sections}
手稿：已重写并重拼 / 待重写（见上方提示）
─────────────────────────────────────────
```
</step>

</process>

<stale_rules>
与 `writing.md` 的 stale 规则完全一致，不得自创：

```
RESULTS    改 → DISCUSSION / CONCLUSION / INTRODUCTION / ABSTRACT stale
METHODS    改 → DISCUSSION / INTRODUCTION / ABSTRACT stale
DISCUSSION 改 → CONCLUSION / INTRODUCTION / ABSTRACT stale
CONCLUSION 改 → ABSTRACT stale
INTRODUCTION 改 → ABSTRACT stale
```
</stale_rules>

<success_criteria>
- 前置检查通过（ANALYSIS_LOG + cleaned.csv + 04_Outputs）
- 改动范围经用户确认
- 每项改动有成功/失败报告
- 改动后输出达到出版标准
- **`ANALYSIS_LOG.md` 追加了 modify 批次（六段齐全）**
- **受影响章节按 DAG 标记为 `stale`**（不直接改 manuscript.md）
- 重写完成并重拼，或已明确告知用户待处理
- `STATE.md` 已更新
</success_criteria>
