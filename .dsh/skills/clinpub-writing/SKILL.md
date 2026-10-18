---
name: clinpub-writing
description: "阶段3：递进式 IMRAD 写作。图表骨架 → Results → Methods → Discussion → Conclusion → 叙事设计 → Introduction → Abstract → 一致性复核 → 拼装。每节读前节的实际内容，产物落 05_Manuscript/sections/*.md，由脚本按 IMRAD 顺序生成 manuscript.md。"
whenToUse: "阶段3：分析已冻结，需要写 IMRAD 手稿。从图表骨架和 Results 开始。"
---

# clinpub-writing

## 目标
阶段3：**递进式** IMRAD 写作。

与 2.x 的三点差异：

1. **顺序**：Results → Methods → Discussion → Conclusion → 叙事设计 → Introduction → Abstract（不再从 Introduction 开始）
2. **依赖**：每一节必须读前面各节的实际内容；写作标准见 `writing_standards.md`
3. **载体**：单节写 `05_Manuscript/sections/{key}.md`，`manuscript.md` 是**生成物**

为什么从结果往回写：先写 Results 定死"发现了什么"，Introduction 的 Gap 与假设就必须服务于已有发现。反过来最容易出的事故是"引言承诺的分析没做"，只能在 Discussion 里打补丁。

## 流程
Execute the writing workflow from pipeline/workflows/writing.md end-to-end.

写作顺序（不可打乱）：

```
0. 图表骨架 FIGURE_SKELETON      ← 定海神针，先排图表 + 一句结论
1. Results                       ← 骨架 + 04_Outputs + ANALYSIS_LOG（只陈述，不解释）
2. Methods                       ← ANALYSIS_LOG + 方法说明 + 配置（三段式，如实）
3. Discussion                    ← Results + Methods + ANALYSIS_LOG + 文献
4. Conclusion                    ← Discussion
5. 叙事设计 NARRATIVE            ← R + M + D（想清楚怎么引人入胜）
6. Introduction                  ← 叙事设计 + R/M/D + 文献
7. Abstract + Title
8. 一致性复核（10 项）
9. 拼装 manuscript.md（脚本生成，禁止手改）
```

三个不可省略的规则：

1. **暂停点**由 `project_config.yml` 的 `writing.pause_after` 控制（默认 `[results, discussion]`），其余章节自动推进
2. **任何章节被改** → 按 stale 规则把下游置 `stale`；有 stale/draft 时拼装脚本会**拒绝**生成
3. **写作可反哺分析**：若发现分析缺口（如 Discussion 缺机制解释所需的中介分析），走 `feedback_to_analysis` 退回阶段2 补分析

## 成功标准
- `FIGURE_SKELETON.md` 存在，每张图有一句不含统计量的结论
- `NARRATIVE.md` 存在，Gap 能被实际做过的分析填上
- `sections/` 六节齐全，`status` 全为 `final`，且 `inputs` 真实读取过上游
- Results 早于 Introduction 产出（递进而非并行）
- Methods 的 Statistical Analysis 与 `ANALYSIS_LOG.md` 双向一致
- Results 无解释性语句；Discussion 引用了敏感性分析或被否决备选
- `python scripts/assemble_manuscript.py` 通过，`manuscript.md` 按 IMRAD 顺序生成
- 无占位符残留；引用从 [1] 连续编号且全部含 DOI
- 字数 ≥ `writing.min_words`；引用数在 `citation_strategy.total_range` 内
- 一致性复核 10 项全部通过

---

## 执行流程（内联自 pipeline/workflows/writing.md）

用**递进**方式产出 IMRAD 手稿。

与 2.x 的关键差异：
1. **顺序**：不再 Introduction → Methods → Results → Discussion，而是从结果往回写
2. **依赖**：每一节必须读取前面各节的实际内容，不是各写各的最后拼接
3. **载体**：单节写入 `05_Manuscript/sections/{key}.md`，`manuscript.md` 由脚本生成

写作标准一律以 `pipeline/references/writing_standards.md` 为准。

<process>

### setup_writing_session
### 1. 前置检查阶段2 必须已冻结。确认以下存在，缺一即停：

| 必需 | 路径 |
|---|---|
| 分析摘要 | `.clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md` |
| 分析日志 | `.clinpub/ANALYSIS_LOG.md` |
| 输出清单 | `04_Outputs/MANIFEST.yaml` |
| 共享图表配置 | `04_Outputs/_figure_config.R` |

缺失则提示用户先执行 `/clinpub-analysis` 或 `/clinpub next`。

### 2. 读取写作配置

从 `project_config.yml`：

```yaml
writing:
  pause_after: [results, discussion]   # 在这些章节后暂停审阅
  min_words: 5000
  abstract_words: [250, 300]
```

缺失则用默认值并写回。

### 3. 引用策略讨论（per D-17~D-22）

与用户确认（默认值见 `citation-strategy.md`）：

1. **各段引用量**：Intro 10–15、Methods 3–5、Results 0–3、Discussion 15–25；总量 30–55 为硬约束
2. **时间范围**：默认近 5 年；是否有需要例外的 landmark 研究
3. **IF 偏好**：目标期刊影响因子下限

写入 `project_config.yml` 的 `citation_strategy`：

```yaml
citation_strategy:
  section_targets:
    introduction: {count}
    methods: {count}
    results: {count}
    discussion: {count}
  total_range: [30, 55]
  year_range:
    max_years_ago: 5
    landmark_exceptions: []
  if_preference:
    min_if: null
    note: ""
```

### 4. 建目录

```bash
mkdir -p 05_Manuscript/sections
```

### build_figure_skeleton
**在写任何正文之前**，先把图表排定。这是全文的定海神针。

1. 读取 `04_Outputs/MANIFEST.yaml` 与各方法目录的 `方法说明.md`
2. 按**研究类型 + 报告规范**确定图表清单（不套固定三件套）：

   | 研究类型 | 图表清单 |
   |---|---|
   | RCT | CONSORT 流程图 + 主要终点表 + 安全性表 |
   | 队列 / 病例对照 / 横断面 | STROBE 参与者流程图 + 基线表 + 主要分析表 + 敏感性分析 |
   | 描述性 | 基线表 + 分布/趋势图 |

3. 排序：**顺序 = Results 叙述顺序 = 读者理解顺序**（不是分析执行顺序）
4. 为每张图写**一句大白话结论**（不含统计量）
5. 按 `pipeline/templates/figure-skeleton.md` 写入 `05_Manuscript/FIGURE_SKELETON.md`

**自检**：把「一句话结论」按顺序连读，若不能构成完整故事，说明排序或选图有问题，先调整再往下走。

**暂停**：把骨架呈现给用户确认。骨架一旦定稿，Results 就有了唯一依据，后续不再随意增删图表。

### write_results
### 输入（必须真实读取）

- `05_Manuscript/FIGURE_SKELETON.md`
- `04_Outputs/*/`（图、表、`方法说明.md` 的「输出结果」小节）
- `.clinpub/ANALYSIS_LOG.md`（了解实际做了什么分析）

### 写法（见 writing_standards.md §3）

- **一段对应一张图表**，顺序与骨架完全一致
- 三段式：指路 → 核心趋势 → 必要细节（样本量、缺失、亚组）
- 统计量格式：效应量 + 95%CI + 精确 p（禁 `p = 0.000`）
- **禁止任何解释**——因果、机制、意义全部留给 Discussion
- 禁段落开头写 "As shown in Table X"

### 输出

`05_Manuscript/sections/results.md`，frontmatter：

```yaml
---
section: results
status: final
inputs:
  - 05_Manuscript/FIGURE_SKELETON.md
  - 04_Outputs/
  - .clinpub/ANALYSIS_LOG.md
depends_on: []
---
```

### 暂停

若 `results` ∈ `writing.pause_after` → 停下让用户审阅；否则继续。

### write_methods
### 输入

- `.clinpub/ANALYSIS_LOG.md`（**实际执行了什么**）
- `03_AnalysisMethods/*/方法说明.md`
- `project_config.yml`（study_type、variables）
- `pipeline/templates/study_types/{type}.md`
- `05_Manuscript/sections/results.md`（确保方法覆盖面与结果对得上）

### 写法（见 writing_standards.md §4）

**标准三段式**：

1. **Participants / Study design** — 设计类型、入组/排除、时间地点、伦理批号与知情同意
2. **Measures / Variables** — 评估工具（版本、信效度）、终点定义
3. **Statistical Analysis** — 软件版本、正态性检验、比较方法、协变量、缺失处理、多重比较、敏感性分析

**"如实"的判定标准（双向一致）**：

- `ANALYSIS_LOG` 里做了的，这里必须写
- 这里写了的，日志里必须真做过
- **计划但被否决的方法不写进 Methods**（写进 Discussion 局限性）
- 事后追加的分析标注 `post hoc / exploratory`

### 输出

`05_Manuscript/sections/methods.md`，frontmatter `depends_on: []`。

### 暂停

不在默认 `pause_after` 中 → 自动继续。

### write_discussion
### 文献搜索

调用 reference-agent 搜索：对比同类研究 + 机制解释 + 临床意义。

搜索后更新 `Reference/reference_library.json`：

1. 读已有库 → 按 `citation_key` 去重
2. 新引用取摘要（有 PMID 用 `pubmed_fetch.py`，否则 DOI 解析），写入 `abstract`；取不到标 `"pending"`
3. 分配新 ID（max_id + 1）→ 写回 → 更新 `Reference/MANIFEST.yaml`

### 输入

- `sections/results.md`
- `sections/methods.md`
- `.clinpub/ANALYSIS_LOG.md`（**分析过程**：为什么这样做、敏感性分析、被否决的备选）
- `Reference/reference_library.json`、`Reference/citation_map.md`

### 写法（见 writing_standards.md §5）

四段式：

| 段 | 内容 |
|---|---|
| 1 | 核心发现（3–4 句，不复述统计量） |
| 2 | 逐条解释：重申 → 与既往比较 → 机制 → 临床意义（每个核心发现一段） |
| 3 | 局限性（独立段；按研究类型选，不抄空话） |
| 4 | 结论（2 句，不再报数字） |

**必须是"从分析过程展开"**：引用敏感性分析结果、被否决的备选方案及其原因——这些只有 `ANALYSIS_LOG.md` 有，是局限性段最好的素材。

### 输出

`sections/discussion.md`，`depends_on: [results, methods]`。

### 暂停

若 `discussion` ∈ `pause_after` → 停下审阅。

### write_conclusion
### 输入

- `sections/discussion.md`

### 写法

2 句：第一句重申核心发现（不带数字），第二句给临床或研究启示。
**不要**与 Discussion 第 1 段重复措辞。

### 输出

`sections/conclusion.md`，`depends_on: [discussion]`。自动继续。

### narrative_design
**Introduction 动笔之前的半步。** 先想清楚怎么引人入胜。

### 输入

- `sections/results.md`、`sections/methods.md`、`sections/discussion.md`

### 产出

按 `pipeline/templates/narrative.md` 写入 `05_Manuscript/NARRATIVE.md`：

1. **一句话卖点** — 不是"我们研究了 X"，而是"我们发现了 Y，它改变了 Z 的理解"
2. **Gap 的精确表述** — 必须能被**实际做过的分析**填上
3. **叙事弧** — 临床痛点 → 已知 → 未知 → 本研究
4. **目标读者与期刊调性**

**自检**：Gap 若指向一个没做过的分析，改 Gap，不要改结论。

### 暂停

把 `NARRATIVE.md` 呈现给用户确认。这是 Introduction 的唯一依据。

### write_introduction
### 文献搜索

同 Discussion 的搜索与入库流程，目标引用量取 `citation_strategy.section_targets.introduction`。

### 输入

- `05_Manuscript/NARRATIVE.md`（**主依据**）
- `sections/results.md`、`sections/methods.md`、`sections/discussion.md`
- `Reference/reference_library.json`

### 写法（见 writing_standards.md §7）

倒金字塔 3–4 段：

| 段 | 内容 |
|---|---|
| 1 | 临床背景：疾病负担、异质性 → 具体临床痛点 |
| 2 | 已知与 Gap：前人做到哪 → **还缺什么** |
| 3 | 本研究：纳入了谁、做了什么、**先验假设** |

**禁止**：文献综述式逐篇罗列；第一段就报本研究结果；Gap 与实际分析不对应。

### 输出

`sections/introduction.md`，`depends_on: [results, methods, discussion]`。

### 暂停

把 Introduction 与 NARRATIVE 的对照呈现给用户（Gap 是否被填上、卖点是否立住）。

### write_abstract_title
### 输入

全部已完成的章节。

### 写法

**Abstract**（结构式四段，取句来源）：

| 段 | 取自 |
|---|---|
| Background | Introduction 第 2 段的 Gap |
| Methods | Methods 的 Statistical Analysis + Participants |
| Results | Results 的主要统计量（**必须带数字**） |
| Conclusions | Conclusion |

词数取 `writing.abstract_words`（默认 250–300）。

**Title**：优先"发现型"标题（点出结论方向），含研究设计或人群关键词。

### 输出

- `sections/abstract.md`，`depends_on: [introduction, methods, results, discussion, conclusion]`
- 标题写入 `project_config.yml` 的 `project.title`（供拼装读取）

### consistency_review
拼装**之前**的一致性检查（`writing_standards.md §10` 的 10 项）：

1. 每个 Results 段落对得上骨架里的一张图表
2. Methods 的 Statistical Analysis 与 `ANALYSIS_LOG` **双向**一致
3. Introduction 的每个假设能在 Results 找到对应分析
4. Discussion 不引入新结果
5. 变量名/方法名全文一致（以 `project_config.yml` 为真源）
6. 图表编号连续、正文引用与图注一一对应
7. 所有统计量都有效应量 + 95%CI + 精确 p
8. 报告规范清单无缺项（或缺项已在局限性说明）
9. 摘要数字与正文一致
10. 引用全有 DOI，正文引用与文献表一一对应

**发现问题时**：定位到具体章节 → 修改该节 → 按 stale 规则把下游改回 `draft` → 重写下游。

**若发现的是分析缺口**（如 Discussion 无法解释机制，因为少做了一个中介分析）：

```
写作暴露分析缺口 → 记录到 ANALYSIS_LOG → 提示用户执行 /clinpub-modify
                → 补完分析后把 results 置 draft → 下游全部 stale → 重写
```

这是**正常质量控制**，不是异常路径。

### assemble
### 1. 校验并拼装

```bash
python scripts/assemble_manuscript.py --check   # 先只校验
python scripts/assemble_manuscript.py           # 通过后生成
```

脚本会拒绝三类情况：

- 章节缺失
- 任何章节不是 `final`
- 某节 `final` 但其上游是 `stale`

### 2. 终稿处理（`concatenation-protocol.md`）

1. **占位符替换 —— 由脚本完成，不要手改**
   - `assemble_manuscript.py` 在拼装时已把 `{{Table:N}}` → `Table N`、
     `{{Figure:N}}` → `Figure N`、`{{SupplementaryTable:N}}` → `Supplementary Table S{N}`、
     `{{Method:name}}` → `the {name} analysis`、`{{Section:name}}` → 段落名
   - 若仍有残留，脚本会在 stderr 给出 `[WARN] … 存在未解析占位符`
   - **不要手工编辑 `manuscript.md`**：它是生成物，下次拼装会覆盖
2. **引用编号与 References —— 同样由脚本完成**
   - 章节里写 `{{cite:CitationKey}}` 或 `{{cite:Key1,Key2}}`（键来自 `reference_library.json` 的 `citation_key`）
   - `assemble_manuscript.py` 按**正文首次出现顺序**统一编号（跨章节连续），替换为 `[n]` / `[n,m]`
   - 文末据此生成 Vancouver 格式 References，每条带 `doi:`
   - 键不在库中时脚本给 `[WARN] 引用键不在文献库中`；不要手写编号，改了章节顺序后编号会错乱
3. **补充 frontmatter**：`assemble_manuscript.py` 已写入 `generated_by` / `generated_at` / `word_count` / `title`（读取 `project_config.yml` 的 `project.title`）。此步只**追加** `target_journal` 与 `reference_count`，不要重写已有字段
4. **写回 `05_Manuscript/manuscript.md`**（脚本已生成骨架，此步补充引用区与缺失的 frontmatter 字段）
5. **更新 `05_Manuscript/MANIFEST.yaml`**（consumer: clinpub-verifier）

### 3. 拼装后验证

- 无 `{{Table:\d+}}` / `{{Figure:\d+}}` 残留
- `word_count ≥ writing.min_words`
- `reference_count` 在 `citation_strategy.total_range` 内
- 所有引用有 DOI
- IMRAD 六节齐全

### milestone
执行 milestone workflow 正式关闭阶段3（核心管线终点）：

```bash
# 1. 验证阶段3 成功标准
# 2. 收集写作决策（研究类型模板、目标期刊、引用策略）
# 3. 生成 .clinpub/phases/03-writing/MILESTONE.md
# 4. 更新 ROADMAP.md：阶段3 → ✅（核心管线完成）
# 5. 更新 STATE.md
# 6. 请求用户签字
```

见 `pipeline/workflows/milestone.md`。

<output name="signoff_prompt" format="user_facing">
────────────────────────────────
✅ 阶段3 核验完成 — 核心管线完成（阶段0–3）

请确认：输入 "approved" 收尾。手稿完成后可按需使用独立工具：
- /clinpub:improving   → 自审并直接改进稿件（可反复）
- /clinpub:coverletter → 按目标期刊生成投稿信
- /clinpub:review      → 投稿后，录入真实审稿意见并回复 + 修稿
────────────────────────────────
</output>

</process>

<stale_propagation>
**任何章节被修改后，必须执行：**

```
RESULTS   被改 → DISCUSSION / CONCLUSION / INTRODUCTION / ABSTRACT 全部置 stale
METHODS   被改 → DISCUSSION / INTRODUCTION / ABSTRACT 置 stale
DISCUSSION 被改 → CONCLUSION / INTRODUCTION / ABSTRACT 置 stale
CONCLUSION 被改 → ABSTRACT 置 stale
INTRODUCTION 被改 → ABSTRACT 置 stale
ABSTRACT  被改 → 无下游
```

改完并重写完下游后，把它们的 `status` 改回 `final`。
**只要存在 stale 或 draft，拼装脚本就会拒绝生成 `manuscript.md`。**
</stale_propagation>

<feedback_to_analysis>
写作阶段允许退回阶段2，条件是发现了**真实的分析缺口**：

| 触发 | 例 |
|---|---|
| Discussion 无法解释机制 | 缺中介/调节分析 |
| Results 撑不起核心论点 | 缺关键比较或敏感性分析 |
| Methods 与 Results 对不上 | 实际做过的分析没记录 |

处理：

1. 把缺口写入 `.clinpub/ANALYSIS_LOG.md`（作为新批次的「依据」）
2. 提示用户执行 `/clinpub-modify` 补分析
3. 补完后把 `results` 置 `draft`，按 stale 规则向下游传播
4. 重写受影响章节

**限制**：同一缺口不得退回两次；退回计入 `analysis_budget`。
</feedback_to_analysis>

<success_criteria>
- `05_Manuscript/FIGURE_SKELETON.md` 存在，每张图有一句不含统计量的结论
- `05_Manuscript/NARRATIVE.md` 存在，含一句话卖点与可被实际分析填上的 Gap
- `05_Manuscript/sections/` 下六节齐全，每节 frontmatter 的 `status` 均为 `final`
- 每节 `inputs` 真实读取过上游内容（Results 早于 Introduction 产出）
- Methods 的 Statistical Analysis 与 `ANALYSIS_LOG.md` 双向一致
- Results 无任何解释性语句
- Discussion 引用了敏感性分析或被否决备选
- `python scripts/assemble_manuscript.py` 通过并生成 `manuscript.md`
- 无占位符残留；引用从 [1] 连续编号，全部含 DOI
- `word_count ≥ writing.min_words`；`reference_count` 在 `total_range` 内
- `05_Manuscript/MANIFEST.yaml` 存在且声明 clinpub-verifier 为消费者
- 用户已完成审阅并签字
</success_criteria>

---

## 参考资源

路径相对本技能目录（`../../../dsh/` 指向仓库共享核心）。**按需读取**，不要一次全读。

- `../../../dsh/pipeline/references/writing_standards.md`
- `../../../dsh/pipeline/references/journal_standards.md`
- `../../../dsh/pipeline/references/citation-strategy.md`
- `../../../dsh/pipeline/references/reference-library.md`
- `../../../dsh/pipeline/references/concatenation-protocol.md`
- `../../../dsh/pipeline/templates/section.md`
- `../../../dsh/pipeline/templates/figure-skeleton.md`
- `../../../dsh/pipeline/templates/narrative.md`
- `../../../dsh/agents/writer-agent.md`
- `../../../dsh/agents/reference-agent.md`

---

> 本文件由 `node dsh/build.mjs` 生成，请勿手改。修改源文件：`claude-code/commands/` 与 `claude-code/pipeline/workflows/`。
