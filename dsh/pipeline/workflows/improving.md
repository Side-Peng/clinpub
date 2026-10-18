---
name: improving
description: "Standalone manuscript improvement tool: 自审稿件 → 产出具体修改计划 → 用户确认 → 直接改稿（章节文件 + 必要时重跑分析并级联数值）→ 按依赖标 stale → 重拼手稿。不写回复信、不模拟审稿人。可反复调用。"
---

<purpose>
在写作过程中或完稿后持续改进手稿。做结构化自审 → 给出逐条修改计划 → 用户确认后**同时**改正文与底层分析（必要时重跑 R/Python 并级联数值）。

与 2.x 的差异：正文改动落在 `05_Manuscript/sections/*.md`（不再直接改 `manuscript.md`），改完后按依赖把下游章节标 `stale` 并重写，最后由脚本重拼。

这是**可反复调用**的工具，不是阶段；不模拟审稿人，不写回复信。
</purpose>

<required_reading>
@./pipeline/references/writing_standards.md
@./pipeline/references/journal_standards.md
@./pipeline/references/checkpoints.md
@./pipeline/references/analysis_methods.md
@./pipeline/references/analysis_decision_policy.md
@./pipeline/references/r_patterns.md
@./agents/writer-agent.md
@./agents/modify-agent.md
</required_reading>

<process>

<step name="validate_prerequisites" priority="first">
```bash
PROJECT_DIR=$(pwd)
SECTIONS="$PROJECT_DIR/05_Manuscript/sections"
MANUSCRIPT="$PROJECT_DIR/05_Manuscript/manuscript.md"
```

检查：

1. `05_Manuscript/sections/` 下至少有一节 `.md`（若只有 `manuscript.md` 而无所属 sections → 提示这是 3.0 之前的手稿，需先迁移到 sections 结构）
2. `project_config.yml` 存在（取 journal tier、language、变量名）——缺失时警告并继续

`improving` 可反复调用。
</step>

<step name="self_review" priority="high">
对当前稿件做结构化自审。这是**内部质量评估**，不是模拟审稿人、不写回复信。

评审严格度取目标期刊层级：读 `project_config.yml` 的 `journal.name` + `journal.tier`；未配置时按 Q2 标准（见 `journal_standards.md`）。

**必须同时读取的上下文**（只说"读稿件"是不够的）：

- `05_Manuscript/sections/*.md`（六节现状与各节 status）
- `05_Manuscript/FIGURE_SKELETON.md`（Results 是否与骨架一致）
- `.clinpub/ANALYSIS_LOG.md`（**分析方法与实际执行**是否对得上；有哪些敏感性分析/否决项没写进稿件）
- `Reference/reference_library.json`

按维度评估，每条标注 Major / Minor：

**Major（实质）**
- 统计方法与研究问题是否匹配；是否缺关键分析
- 样本量 / 统计功效是否足够
- 混杂控制是否充分
- 结果解释是否越界（结论超出证据）
- 研究设计局限是否被回避

**Minor（呈现）**
- 语言、语法、行文流畅度
- 引用完整性、相关性、时效性
- 图表格式、清晰度、正文引用
- 报告规范符合度（STROBE / CONSORT / PRISMA）
- 交叉引用与占位符一致性

**3.0 专项检查**（必做）

| 检查 | 判定 |
|---|---|
| Results 是否混入解释 | 有即 Major |
| Methods 与 `ANALYSIS_LOG` 是否双向一致 | 不一致即 Major |
| Introduction 的 Gap 能否被实际分析填上 | 不能即 Major |
| Discussion 是否用上了敏感性分析 / 被否决备选 | 未用即 Major（丢素材） |
| 各节 `status` 是否与内容一致 | stale 却当 final 即 Major |

写入 `05_Manuscript/improvement_plan.md`，每条含：位置（章节/段落）、问题、建议、严重度、**是否需要重跑分析**。
</step>

<step name="propose_plan" priority="high">
把自审转成可执行的逐条计划，按执行类型分组：

1. **纯文本修改**：改哪几节/哪几段（委派 writer-agent）
2. **分析重跑**：哪些 `03_AnalysisMethods/{method_id}/` 要改代码 / 新增方法（委派 modify-agent），以及会级联影响哪些数值
3. **图表调整**：`04_Outputs/*` 的样式或内容
4. **文献补充**：缺口需要新引用（委派 reference-agent）

呈现给用户确认。
</step>

<step name="checkpoint_confirm" priority="high">
逐条呈现计划并取得明确确认：

1. 列出所有条目（严重度 + 执行类型）
2. 用户选择现在执行哪些（可推迟）
3. 用户可追加改进要求
4. 在动手前确定范围

用户拒绝 → 停止，不做任何改动。
</step>

<step name="execute_revisions" priority="high">
按"先改数字、后改文字"的顺序执行，减少级联失败。

1. **分析重跑**（若有）：委派 modify-agent（`execute_modifications` + `verify_modifications`）
   - 改动前记录 commit hash 以便回滚
   - 新方法 ID 用 `{NN}_{MethodName}`；`03_AnalysisMethods/{id}/` 与 `04_Outputs/{id}/` 必须同时建
   - 缺包时报告并跳过，**不自动安装**
   - **完成后在 `.clinpub/ANALYSIS_LOG.md` 追加 `Batch M-{n}（improving）`**
2. **图表调整**：走 modify-agent 样式路径（≥300 DPI、英文标注）
3. **文献补充**：委派 reference-agent；更新 `Reference/reference_library.json` + `references.bib`（去重、必须有 DOI）
4. **文本修改**：委派 writer-agent 逐节修
   - **改 `sections/{key}.md` 的正文**（不写 `## 标题`，不动 frontmatter 以外的结构）
   - 改完把该节 `status` 改回 `final`
   - **数值级联**：分析重跑后，`results` 段必须重写（不是"打补丁改数字"——数字与叙述要一起对）
   - 内联执行 Humanizer 检查

逐条报告成功/失败。
</step>

<step name="cascade_stale" priority="high">
任何章节被改后，按 DAG 把下游置 `stale`：

```
RESULTS    改 → DISCUSSION / CONCLUSION / INTRODUCTION / ABSTRACT
METHODS    改 → DISCUSSION / INTRODUCTION / ABSTRACT
DISCUSSION 改 → CONCLUSION / INTRODUCTION / ABSTRACT
CONCLUSION 改 → ABSTRACT
INTRODUCTION 改 → ABSTRACT
```

**分析重跑时**：`results` 与 `methods` 都置 `stale`（方法变了，Methods 的 Statistical Analysis 也要改）。

下游章节必须重写，不能只改 status——把 stale 当 final 会让拼装脚本拒绝生成。
</step>

<step name="reassemble" priority="high">
```bash
python scripts/assemble_manuscript.py --check
python scripts/assemble_manuscript.py
```

若仍有 stale/draft，脚本会列出具体章节并拒绝生成——按提示重写后再跑。
</step>

<step name="verify" priority="medium">
**手稿**

1. 六节齐全，`status` 全为 `final`
2. 所有引用有 DOI；引用库已去重
3. 正文引用的图/表都存在于 `04_Outputs/`
4. 无残留占位符（`{{Table:N}}` 等）
5. 字数在期刊限制内；Humanizer 检查通过

**分析（若有重跑）**

6. 图文件存在、非空、≥300 DPI、英文标注
7. 统计报告含效应量 + 95%CI + 精确 p
8. 变更方法的 `方法说明.md` 已更新
9. `ANALYSIS_LOG.md` 已追加重跑批次

失败项报告具体原因，并给出重跑/跳过的选择。
</step>

<step name="record" priority="high">
记录本轮改进（不关闭阶段、不触发 milestone）：

1. 更新 `05_Manuscript/improvement_plan.md`：每条标 `done` / `deferred` / `failed`，追加带时间戳的轮次标题
2. 更新 `.clinpub/STATE.md` 的「最近决策」

```
─────────────────────────────────────────
 Improving 完成（第 {N} 轮）
─────────────────────────────────────────
执行：{N} 项   推迟：{M}   失败：{K}
分析重跑：{A} 次   修改章节：{S} 节
手稿：05_Manuscript/manuscript.md（已重拼）
计划：05_Manuscript/improvement_plan.md
─────────────────────────────────────────
下一步：
- 继续改进 → 再次运行 /clinpub-improving
- 准备投稿信 → /clinpub-coverletter
- 投稿后收到审稿意见 → /clinpub-review
```

需要继续修改时回到 `self_review`（或 `propose_plan` 做聚焦一轮）。
</step>

</process>

<success_criteria>
- 前置检查通过（`sections/` 存在）
- 自审在 `improvement_plan.md` 中产出 Major/Minor 条目，且包含 3.0 专项五项检查
- 逐条计划经用户确认后才动手
- 已确认项全部执行：文本改在 `sections/*.md`，必要的分析已重跑，数值已级联
- 受影响章节按 DAG 标记 `stale` 并重写回 `final`
- `python scripts/assemble_manuscript.py` 通过，`manuscript.md` 已重拼
- 新引用有 DOI；引用库去重
- 未产出回复信、未模拟审稿人
- 本轮已记录；工具保持可反复调用（不关阶段）
</success_criteria>
