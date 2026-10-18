---
name: clinpub
description: "ClinPub 枢纽：查看状态、查看命令参考、关卡核验并推进、按意图路由。无参看状态，help 看参考，next 核验并推进，其余按自然语言意图路由。"
---

# ClinPub 枢纽

ClinPub 的**单一入口**，四种模式：

| 输入 | 模式 | 做什么 |
|---|---|---|
| 无参数 | 状态 | 读 `STATE.md` + 检测工件 → 进度摘要 + 建议命令 |
| `help` / `?` | 参考 | 输出命令参考表 |
| `next` / `推进` | 推进 | 关卡核验 → `MILESTONE.md` → 签字 → 推进阶段 |
| 其他文本 | 路由 | 按意图路由到对应技能（只提示，不代跑） |

> 3.0 起合并了原 `overview` / `do` / `next-step` / `milestone` 四个命令。状态判据只维护一份，
> 且"推进"与"核验"成为原子动作——未签字不推进。

## Execution Context

- Advance workflow: `pipeline/workflows/next-step.md`
- Milestone workflow: `pipeline/workflows/milestone.md`
- Gates / checkpoints: `pipeline/references/gates.md`, `checkpoints.md`
- Template: `pipeline/templates/milestone.md`

## Process

### 模式 1：状态（无参）

读 `.clinpub/STATE.md` 的 `- 阶段：Phase N` 行（唯一权威来源），按 3.0 判据检测：

| 阶段 | 完成判据 |
|---|---|
| 阶段0 | `project_config.yml` 关键字段有效（`project.name` 非空，且 `variables.outcome` 非空或 `analysis_mode: exploratory`）+ 原始数据存在 |
| 阶段1 | `02_PreprocessedData/data/cleaned.csv` 存在 |
| 阶段2 | `.clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md` 存在 |
| 阶段2 中间态 | `ANALYSIS_LOG.md` 存在但无 `ANALYSIS_SUMMARY.md` |
| 阶段3 | `sections/` 六节全 `final` 且 `assemble_manuscript.py --check` 通过 |

阶段2 中间态额外报告批次数与最后一批的「下一批决策」；阶段3 未完成额外报告非 `final` 章节。

### 模式 2：参考（`help`）

| 技能 | 阶段 | 做什么 |
|---|---|---|
| `clinpub` | — | 状态 / 参考 / 推进 / 路由 |
| `clinpub-init` | 0 | 研究框架 + 目标期刊 → 配置与目录 |
| `clinpub-data-prep` | 1 | 数据清洗 → `cleaned.csv` |
| `clinpub-analysis` | 2 | 迭代分析：每批 1–3 个方法 |
| `clinpub-writing` | 3 | 递进写作：骨架 → R→M→D→C→I → Abstract |
| `clinpub-modify` | 工具 | 改分析产出 |
| `clinpub-improving` | 工具 | 自审 → 修改计划 → 改稿 |
| `clinpub-review` | 工具 | 投稿后：真实审稿意见 → 回复信 → 修稿 |
| `clinpub-coverletter` | 工具 | 按目标期刊生成投稿信 |
| `clinpub-data2idea` | 工具 | 从数据挖选题 |

### 模式 3：推进（`next`）

**核验与推进是原子动作**：

1. 按模式 1 判据核验；未完成 → 列出缺项，不推进
2. 阶段2 中间态 → 不推进，报告批次数与最后一批决策
3. 完成 → 按 `milestone.md` 逐条核对 success criteria、生成 `MILESTONE.md`、请求签字
4. 签字后才更新 `STATE.md` 与 `ROADMAP.md`，输出 `/clear` + 下一条命令 + 进度阶段3 之后输出"核心管线完成"，并建议 `improving` / `coverletter` / `review`。

### 模式 4：路由（其他文本）

| 优先级 | 关键词 | 路由到 |
|---|---|---|
| 1 | 初始化/init/开始/创建项目/新建 | `clinpub-init` |
| 2 | 清洗/clean/数据质量/缺失/cleaned | `clinpub-data-prep` |
| 3 | 选题/话题挖掘/idea/data2idea | `clinpub-data2idea` |
| 4 | 审稿/审稿意见/reviewer/回复信/rebuttal/返修 | `clinpub-review` |
| 5 | 投稿信/coverletter | `clinpub-coverletter` |
| 6 | 改进/润色/自审/修订/改稿/improving | `clinpub-improving` |
| 7 | 分析/统计/结果/图/表/回归/生存/ROC | `clinpub-analysis` |
| 8 | 写/手稿/文献/引用/IMRAD/论文 | `clinpub-writing` |
| 9 | 推进/下一步/继续 | 模式 3 |
| 10 | 状态/摘要/总览/当前/什么阶段 | 模式 1 |

组 4/5/6 必须排在组 8 之前；跨组冲突按优先级；不匹配停用词；全不命中回退模式 1。路由后需用户确认。

## Success Criteria

- 模式判定正确，状态检测使用 3.0 判据
- 阶段2 中间态只报告，不替用户决定下一批
- 推进必须先核验、生成 `MILESTONE.md`、取得签字，才更新 `STATE.md` / `ROADMAP.md`
- 未签字不推进；路由只提示不代跑
