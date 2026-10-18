# ClinPub 3.0 设计（管线重构）

> 状态：**设计待审**（design, not implemented）
> 基线：clinpub v2.3.0（13 命令 / 12 workflow / 8 智能体）
> 目标：把"一站式生成"改成"迭代分析 + 递进写作"
> 兼容性：**不兼容 2.x 项目状态**（`.clinpub/` 可自由改），但**保留 `import-project` 功能**（导入已有研究材料 ≠ 读取 2.x 状态）

---

## 0. 一句话

2.x 的假设是「分析方法先定完，然后一次成文」。3.0 的假设是：

> **方法是逐轮涌现的；文章是从结果往回、一节压着一节写出来的。**

"往回"指顺序（Results 先于 Introduction），"压着"指依赖（每一节必须读前面各节的实际内容，不是各写各的最后拼接）。

---

## 1. 两条主线

### A. 分析：从"一次规划"到"迭代决策"

**2.x 现状**（`workflows/analysis.md`）：

```
诊断 → 提出全部方法 → 讨论并确认 → 执行波次 → 验证 → 满意度检查 → 里程碑
                      ↑
            所有方法在此定死
```

**3.0 目标**：

```
诊断 → 建立 ANALYSIS_LOG → ┌─────────────────────────┐
                            │  迭代循环                  │
                            │  1. 提出下批方法（1–3 个）  │
                            │  2. 分叉判断 → 需要就问用户  │
                            │  3. 执行该批               │
                            │  4. 记录结果与解读          │
                            │  5. 饱和/预算判断 → 继续或退出│
                            └─────────────────────────┘
                                        ↓
                              冻结分析 → ANALYSIS_SUMMARY → 里程碑
```

### B. 写作：**递进式**，不是"分别写完再拼"

**2.x 现状**（`workflows/writing.md`）：`Introduction → Methods → Results → Discussion`，各节独立起草，最后拼接。

**3.0 的核心区别**：每一节**必须读前面的节**，后一节建立在前一节的实际内容上。拼接只是最后的排版动作，**不是写作方式**。

```
0. 图表骨架 FIGURE_SKELETON ← 04_Outputs（图表 + 方法说明）
1. Results      ← 骨架 + 04_Outputs + ANALYSIS_LOG     【如实陈述，不解释】
2. Methods      ← ANALYSIS_LOG + 方法说明 + 配置        【如实还原"实际怎么做的"】
3. Discussion   ← Results + Methods + ANALYSIS_LOG + 文献【从分析过程展开】
4. Conclusion   ← Discussion
5. 叙事设计     ← Results + Methods + Discussion        【先想清楚怎么引人入胜】
6. Introduction ← 叙事设计 + 上述三节 + 文献
7. Abstract + Title ← 全文
8. 全文一致性复核
9. 拼装 manuscript.md（纯排版）
```

#### 每节的输入契约

| 节 | 必须读取 | 依据 |
|---|---|---|
| **Results** | `FIGURE_SKELETON`、`04_Outputs/*`、`ANALYSIS_LOG` | 图表与统计量必须与分析产出一一对应；**只陈述事实，禁止解释**（解释属 Discussion） |
| **Methods** | `ANALYSIS_LOG`、`03_AnalysisMethods/*/方法说明.md`、`project_config.yml`、研究类型模板 | 采用**标准三段式**（Participants / Measures / Statistical Analysis）；"如实"落在 Statistical Analysis 小节：与 `ANALYSIS_LOG` **双向一致**，计划但未做的分析不写，事后追加的标注 post hoc |
| **Discussion** | **Results + Methods + `ANALYSIS_LOG`** + 文献 | 用户强调的"根据分析过程展开"——不仅解释结果，还要能解释**为什么这样设计、敏感性分析说了什么、哪些备选被否决**。这些只有 `ANALYSIS_LOG` 有。 |
| **Conclusion** | Discussion | 两句话，不再报统计量 |
| **叙事设计** | Results + Methods + Discussion | 见下 |
| **Introduction** | 叙事设计 + R/M/D + 文献 | Gap 必须能被"实际发现"填上；且要**引人入胜** |

#### 第 5 步「叙事设计」是新增的关键

Introduction 最难的不是信息，是**说服力**。所以在动笔前先产出一份 `NARRATIVE.md`（半页）：

- **一句话卖点**：读者为什么要读这篇？（不是"我们研究了 X"，而是"我们发现了 Y，它改变了 Z 的理解"）
- **Gap 表述**：现有知识缺哪一块 → 直接指向我们做的分析
- **叙事弧**：从临床痛点 → 已知 → 未知 → 本研究如何补上
- **目标读者与期刊调性**：决定语气与篇幅

Introduction 从这份叙事稿展开，而不是从零硬写。

#### 写作可以反哺分析（反馈边）

递进式写作会暴露分析缺口：写到 Discussion 时发现"机制解释缺少一个中介分析"，或 Results 里某张图撑不起核心论点。

因此 3.0 允许**写作退回阶段2**：

```
Discussion 起草 → 发现缺口 → 追加一批分析（更新 ANALYSIS_LOG）
               → 标记受影响章节 stale → 重写该节 → 继续
```

这不是异常路径，而是**正常质量控制**：写不出来，往往说明分析还没做完。

#### 为什么这个顺序更重要

先写 Results 定死"我发现了什么"，Introduction 的 Gap 与假设就**必须服务于已有发现**。反过来最容易出的事故是「引言承诺的分析没做或做出来不显著」，只能在 Discussion 里打补丁——这是审稿意见的高频项。

---

## 2. 新增工件

| 工件 | 位置 | 作用 | 生命周期 |
|---|---|---|---|
| `ANALYSIS_LOG.md` | `.clinpub/ANALYSIS_LOG.md` | 每批：方法、结果要点、**下一批理由**、被否决项及原因。**写作时 Discussion 的主要输入** | 阶段2 全程追加 |
| `ANALYSIS_SUMMARY.md` | `.clinpub/phases/02-analysis/` | 冻结分析时的收敛摘要 | 阶段2 结束一次 |
| `analysis_decision_policy.md` | `pipeline/references/` | 决策规则库（见 §3） | 静态参考 |
| **`writing_standards.md`** | `pipeline/references/` | **写作规范唯一标准**：事实/解释分层、各节结构、句式模板、统计量格式、报告规范对照、交付前检查 | 静态参考（**已创建**） |
| `FIGURE_SKELETON.md` | `05_Manuscript/FIGURE_SKELETON.md` | 图表顺序 + 每图一句结论 = 全文骨架 | 阶段3 第 0 步 |
| `sections/*.md` | `05_Manuscript/sections/` | 逐节草稿，**带 frontmatter 声明依赖与状态** | 阶段3 |
| `NARRATIVE.md` | `05_Manuscript/NARRATIVE.md` | 叙事设计：一句话卖点 / Gap / 叙事弧 / 目标读者 | Introduction 之前 |
| `manuscript.md` | `05_Manuscript/manuscript.md` | **生成物**，按 IMRAD 顺序拼装，禁止手改 | 阶段3 末 |

#### 章节文件的 frontmatter 约定

```yaml
---
section: results
status: final            # draft | final | stale
inputs:                  # 这一节据以写成的内容源
  - 04_Outputs/**
  - 05_Manuscript/FIGURE_SKELETON.md
  - .clinpub/ANALYSIS_LOG.md
depends_on: []           # 章节级依赖（用于 stale 传播）
---
```

#### 依赖 DAG 与 stale 传播

```
RESULTS      ← (分析产出)
METHODS      ← (分析产出)
DISCUSSION   ← RESULTS, METHODS
CONCLUSION   ← DISCUSSION
INTRODUCTION ← RESULTS, METHODS, DISCUSSION
ABSTRACT     ← 全部
```

任一节被改 → **下游全部标 `stale`**。例：`modify` 改了图 → `results` stale → `discussion` / `conclusion` / `introduction` / `abstract` 依次 stale。拼装时若有任何 `stale` 或 `draft`，拒绝生成 `manuscript.md`。

> `sections/` 是对 v2.3.0「单一 manuscript.md」决定的**有意识回退**：写作顺序 ≠ 输出顺序，且需要章节级的依赖与失效追踪，单文件做不到。

---

## 3. 分析决策规则库（新增核心资产）

`analysis_decision_policy.md` 把"先验知识"从模型即兴发挥变成可复用规则。初始条目（按结果形态分支）：

| 观察到的结果 | 候选下一步 |
|---|---|
| 组间差异不显著 | 查统计功效 / 换终点 / 非劣效 / 亚组探索（需声明探索性） |
| 组间差异显著 | 敏感性分析 / 协变量调整 / 剂量-反应 |
| 相关性显著 | 中介或调节分析 |
| 事件数充足 | 生存分析（KM + Cox） |
| 基线不均衡 | PSM / IPTW 后重做主要分析 |
| 连续变量非线性 | RCS |
| 缺失率 > 10% | 多重插补（MICE）后复算主分析 |
| 多重比较 | FDR / Bonferroni 校正 |

规则库不规定顺序，只提供"看到 X 时值得考虑 Y"的映射。**每批的最终决定仍要写入 `ANALYSIS_LOG.md` 并说明理由。**

---

## 4. 命令与 workflow 变更矩阵

| 命令 | 变更 | 说明 |
|---|---|---|
| `initialize` | 调整 | 去掉 `r_patterns` 注入；新增初始化 `ANALYSIS_LOG.md` |
| `data-prep` | 不变 | — |
| `analysis` | **重写** | 改为迭代循环；不再"一次确认全部方法" |
| `writing` | **重写** | 图表骨架 → Results → Methods → Discussion → Conclusion → **叙事设计** → Introduction → Abstract → 复核 → 拼装（递进式，每节读前节） |
| `improving` | 调整 | 改 `sections/*` 的具体节 → 按 DAG 向下游传播 stale → 重拼 |
| `review` | 调整 | 通过 `improving` 生效；审稿意见需能定位到具体章节 |
| `modify` | **调整** | 改分析后必须更新 `ANALYSIS_LOG`，并把 `results` 标 stale，依次传播到 discussion/conclusion/introduction/abstract |
| `coverletter` | 不变 | 消费 `manuscript.md` |
| `milestone` | 调整 | 门控项与 3.0 工件对齐 |
| `do` | **简化** | 只路由，不注入 workflow（无损优化 P1） |
| `next-step` | **重写** | 推进逻辑要理解"迭代中"与"章节写作中"两种中间态 |
| `data2idea` | 不变 | — |
| `overview` | 更新 | 反映新流程 |

workflow 文件：

| 文件 | 变更 |
|---|---|
| `workflows/analysis.md` | 重写为迭代循环 |
| `workflows/writing.md` | 重写为反向流水线 |
| `workflows/next-step.md` | 重写 |
| `workflows/improving.md` / `review.md` / `modify.md` | 适配 sections |
| `workflows/milestone.md` | 门控项更新 |
| 其余 | 保留 |

---

## 5. 状态与钩子

因为**不兼容 2.x**，可以简化：

| 项 | 2.x | 3.0 |
|---|---|---|
| `STATE.md` 阶段行 | `- 阶段：Phase N` | 保留同格式（钩子改动最小），但新增 `- 分析轮次：N` 与 `- 写作节：results` |
| `project_config.yml` 的 `analysis_plan.waves` | 预定义波次 | 废弃，改为 `ANALYSIS_LOG.md` 逐批追加 |
| 阶段守卫 | 目录 → 阶段映射 | **保留原逻辑**（目录归属不变），但允许阶段2 内写 `03_AnalysisMethods` + `04_Outputs`，阶段3 内写 `05_Manuscript/**` |
| `import_mode` 崩溃残留分支 | 有兼容逻辑 | **删除**（不兼容 2.x，简化） |

> 注意：`do.md`、`next-step.md`、`phase-boundary.sh` 都读取 `analysis_plan.waves`，必须同步改。

---

## 6. 并入的上下文优化（P1–P4）

| # | 优化 | 并入方式 |
|---|---|---|
| P1 | `do` 不注入 10 个 workflow | 简化 `do` 时一并做（−92 KB/次） |
| P2 | `initialize` 去掉 `r_patterns` | 改阶段0 时一并做（−55 KB/次） |
| P3 | "要读什么"单一来源 | 重写 analysis/writing 时统一为 workflow 内 `<required_reading>` 唯一来源，命令层不再重复 `!cat` |
| P4 | `r_patterns` 拆分 | 拆为 `r_patterns_core.md`（约定，~12KB）+ `r_patterns_methods.md`（模板库，~43KB），核心必注入、模板按需读 |

**P3 的具体约定**（避免重演双份维护）：

- workflow 文件的 `<required_reading>` 是**唯一真源**
- 命令文件只写 `<process>` 与 `<success_criteria>`，**不再列文件**
- 命令通过 `!`cat workflow`` 引入 workflow 后，workflow 内的 `@./` 引用**不生效**（在 cat 输出中是纯文本）→ 因此**要么全部用命令层 `!cat`，要么全部用 `@`**

> 这条二选一是关键：现在的混乱正来自两种机制混用。3.0 统一选 **命令层 `!cat`**（因为 `!cat` 可执行、可校验），workflow 里的 `@` 行降级为"人读的清单"并标注。

---

## 7. 波及的工具链

| 场景 | 2.x 行为 | 3.0 需要 |
|---|---|---|
| `modify` 改了图/方法 | 更新 `04_Outputs` + 手稿 | 更新 `04_Outputs` → 追加 `ANALYSIS_LOG` → `results` 标 stale → DAG 下游依次 stale → 重写 → 重拼 |
| `improving` 改稿 | 直接改 `manuscript.md` | 定位到具体节 → 改 `sections/*.md` → 下游 stale → 重拼 |
| `review` 处理审稿意见 | 调 `improving` | 同上，且要能定位到具体章节 |
| `coverletter` | 读 `manuscript.md` | 不变 |

---

## 8. 实施顺序

| 步骤 | 内容 | 可独立验收 |
|---|---|---|
| **S1** | 新增 `analysis_decision_policy.md`；重写 `workflows/analysis.md` 为迭代循环；`analysis` 命令同步 | ✅ 能跑完一次多轮分析 |
| **S2** | 重写 `workflows/writing.md` 为**递进式流水线**（含依赖契约、叙事设计、stale 传播）；新增 `FIGURE_SKELETON` / `NARRATIVE` / `sections`；`writing` 命令同步；接入 `writing_standards.md` | ✅ 能从分析产出递进成文，且改一节能正确向下游传播 |
| **S3** | 适配 `modify` / `improving` / `review` / `milestone` / `next-step` / `do`；状态与钩子同步 | ✅ 改了分析能正确级联 |
| **S4** | 上下文优化收尾（P3/P4）、`overview` 更新、四平台同步、CHANGELOG | ✅ 各命令注入量达标 |

---

## 9. 验收点

| # | 验收项 | 判定 |
|---|---|---|
| 1 | 分析可分多轮推进 | 第 2 批方法的选择**明确引用了第 1 批结果** |
| 2 | 分叉时确实停下问 | 出现"不显著 → 换策略"分支时用户被询问 |
| 3 | 分析预算生效 | 超过上限会停并提示 |
| 4 | `ANALYSIS_LOG` 可独立读懂 | 只读该文件能复原整条分析脉络 |
| 5 | **写作是递进的** | 每节 frontmatter 的 `inputs` 都真实读取了前节内容，而非各写各的 |
| 6 | **Methods 如实** | 方法顺序/参数与 `ANALYSIS_LOG` 记录的**实际执行**一致，无"计划但没做"的方法 |
| 7 | **Results 如实** | 每个统计量与 `04_Outputs` 对应，且**不含因果解释** |
| 8 | **Discussion 用上分析过程** | 引用了敏感性分析、被否决的备选、方法选择的理由 |
| 9 | 叙事设计先行 | `NARRATIVE.md` 在 Introduction 之前存在且含一句话卖点与 Gap |
| 10 | 引言与结果一致 | 引言假设能在结果中找到对应分析 |
| 11 | **stale 传播正确** | 改 `results` → discussion/conclusion/introduction/abstract 全变 stale |
| 12 | 拼装受控 | 有 `draft`/`stale` 时拒绝生成 `manuscript.md` |
| 13 | 拼装正确 | `manuscript.md` 为 IMRAD 顺序且各节完整 |
| 14 | 上下文达标 | 单命令注入量较 2.x 下降 ≥ 30% |

---

## 10. 风险

| # | 风险 | 对策 |
|---|---|---|
| 1 | 迭代循环失控（无限分析） | 硬预算 + 饱和判据 + 每批必须写理由 |
| 2 | 多轮后上下文丢失 | `ANALYSIS_LOG.md` 作为唯一记忆，每轮先读它 |
| 3 | **递进写作导致内容重复**（Discussion 复述 Results、Intro 复述 Discussion） | 每节模板明确"本节只做什么"；一致性复核专查重复段落 |
| 4 | **章节间术语/变量名漂移** | 一致性复核以 `project_config.yml` 的变量名为唯一真源，逐节比对 |
| 5 | **写作反复退回分析，循环不收敛** | 退回需显式理由并计入分析预算；同一缺口不得退回两次 |
| 6 | 拼装产物被手改 | `manuscript.md` 顶部标注"生成物，勿手改"；拼装前校验各节 status |
| 7 | 四平台同步漏改 | S4 单列，用脚本比对三个平台的文件清单 |
| 8 | 删除 waves 后旧脚本引用断裂 | 全仓搜 `analysis_plan` / `waves` 逐一清理 |

---

## 11. 明确不做

- 不改阶段0–3 的编号与含义
- **智能体由 8 个减为 6 个**：停用 `clinpub-planner` 与 `clinpub-executor`——迭代循环本身承担了规划职能，"先规划全部再执行"的原子提交模式在 3.0 中已无位置；原子提交能力由 `analyst-agent` 承担
- 不做 2.x 状态迁移（需要用户在 3.0 下重新初始化，或用 `import-project` 采纳现有材料）
- 不在本次引入新统计方法（方法库沿用 2.x）
- **不把 `sections/` 当成"可独立成文的文件"**——它只是递进写作的中间产物，单独看某一节不应是完整文章
