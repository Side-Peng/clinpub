---
name: analysis
description: "阶段2 编排：迭代式统计分析。诊断数据结构 → 每批提出 1–3 个方法 → 执行 → 记录结果与解读 → 据结果决定下一批 → 饱和后冻结。每方法产出版图 + 表格 + 方法说明，全部方法共享 _figure_config.R。"
---

<purpose>
用**迭代**而非一次性规划的方式完成临床数据分析。

2.x 假设"分析计划一次定完"；3.0 假设"方法是逐轮涌现的"：每一批的结果会改变下一批的选择。因此本 workflow 的核心不是"执行一个计划"，而是**维护一条可审计的决策链**。

所有决策写入 `.clinpub/ANALYSIS_LOG.md`；写作阶段的 Discussion 依赖它来解释"为什么这样分析"。
</purpose>

<required_reading>
<!-- 人读清单。真正的注入由 commands/analysis.md 的 !`cat` 完成 -->
@./pipeline/workflows/analysis.md
@./pipeline/references/analysis_methods.md
@./pipeline/references/analysis_decision_policy.md
@./pipeline/references/r_patterns.md
@./pipeline/references/checkpoints.md
@./pipeline/references/comparison-methods.md
@./agents/analyst-agent.md
</required_reading>

<process>

<step name="diagnose_data_structure" priority="first">
在提出任何方法之前，先诊断数据结构：

```bash
PROJECT_DIR=$(pwd)
DATA="$PROJECT_DIR/02_PreprocessedData/data/cleaned.csv"
FULL_DATA="$PROJECT_DIR/02_PreprocessedData/data/full_longitudinal.csv"  # 可能不存在
CONFIG="$PROJECT_DIR/project_config.yml"
```

诊断项：

1. **分组结构**：几组？组名？每组样本量？
2. **时间点**：单时点还是重复测量？标签？
3. **结局变量**：从 `project_config.yml` 或数据画像识别
   - 二分类 → logistic 候选
   - 连续 → 线性模型 / t 检验候选
   - 时间+事件 → 生存分析候选
4. **协变量**：人口学 / 临床测量
5. **缺失模式**：缺失率？是否有结构性缺失？
6. **纵向标记**：同一患者是否多行？
7. **暴露/干预变量**

**记录为结构化诊断**，写入 `.clinpub/phases/02-analysis/00-DIAGNOSIS.md`：

```yaml
data_diagnosis:
  n_patients: 86
  n_rows: 258
  structure: longitudinal        # or cross-sectional
  groups: 2
  group_names: ["{group_A}", "{group_B}"]
  timepoints: ["baseline", "post_treatment", "follow_up"]
  analysis_timepoint: "baseline"
  outcomes:
    - variable: "{outcome_1}"
      type: continuous
      distribution: "right-skewed"
  outcome_type: continuous
  has_covariates: true
  structural_missing: ["{variable_1}"]
  missing_rate_key_vars: 0.08
```
</step>

<step name="setup_analysis_session" priority="high">
一次性初始化本次分析会话。

### 1. 读取分析预算

从 `project_config.yml` 读：

```yaml
analysis_budget:
  max_batches: 6        # 0 = 不限
  max_methods: 12       # 0 = 不限
  ask_on_branch: true   # 分叉时是否停下询问
```

缺失则用默认值（`max_batches: 6`, `max_methods: 12`, `ask_on_branch: true`）并写回配置。

### 2. 恢复检查

若 `.clinpub/ANALYSIS_LOG.md` 已存在且含批次记录 → 这是**续跑**，不是新开始：

- 先完整读一遍 `ANALYSIS_LOG.md`
- 从最后一个 `Batch N` 之后继续
- 不要重复已执行的批次

### 3. 一次性确认图表主题与配色

与用户确认（可全用默认）：

| 主题参数 | 默认值 | 说明 |
|---|---|---|
| `variant` | `theme_pub` | 或 `theme_pub_light` |
| `base_size` | 11 | 基础字号 |
| `base_family` | `sans` | Windows=Arial |
| `legend_position` | `right` | right/bottom/top/none |
| `title_hjust` | 0 | 0=左对齐，0.5=居中 |
| `panel_border` | true | 数据区黑色边框 |

| 配色参数 | 默认值 | 说明 |
|---|---|---|
| `preset` | `auto` | auto/nature/okabe-ito/brewer-set1/brewer-dark2/custom |
| `custom_colors` | `[]` | 自定义色值 |
| `group_mapping` | `{}` | 分组名→色值 |
| `continuous` | `viridis` | viridis/magma/plasma/inferno |

写入 `project_config.yml` 的 `quality.theme` 与 `quality.color_palette`。

### 4. 生成共享图表配置

```bash
cp pipeline/templates/_figure_config.R 04_Outputs/_figure_config.R
Rscript -e 'source("04_Outputs/_figure_config.R"); cat("Figure config OK\n")'
```

**此后所有方法 R 脚本的强制规则**：

- `source("04_Outputs/_figure_config.R")` 必须紧跟 `library()` 之后
- 用 `apply_theme()` 而非手写 `theme_pub()`
- 用 `get_palette(n)` 而非手挑颜色
- 用 `save_figure()` 统一导出
- **禁止**在方法脚本里重定义 `theme_pub` / `get_palette` / `save_figure`
</step>

<step name="iterative_loop" priority="high">
核心循环。每一轮 = 一个 **Batch**。

```
while (未饱和 且 未超预算):
    propose_batch()     # 提出 1–3 个方法
    branch_gate()       # 自动推进 or 停下来问
    execute_batch()     # 执行并产出
    record_batch()      # 写入 ANALYSIS_LOG
    check_continue()    # 饱和/预算判断
```

---

<substep name="propose_batch">
基于三样东西提出本批方法：

1. **上一批的结果**（见 `ANALYSIS_LOG.md` 最近一批的「结果要点」与「解读」）
2. **决策规则库**（`analysis_decision_policy.md`）
3. **数据诊断**（`00-DIAGNOSIS.md`）

**首批特殊**：没有上一批结果，按数据诊断 + 研究问题提出，通常包含：

- 基线特征表（几乎所有研究都需要）
- 主分析（对应主要终点）

**每批 1–3 个方法**，围绕一个研究问题。不要一次提 5 个。

输出给用户的提议必须包含**触发规则编号**：

```markdown
## Batch {N} 提议

**依据**：{触发规则编号} — {一句话}
（例：R01 — 上一批主要终点组间差异 p = 0.21，需判断是否效能不足）

**本批方法**：
1. `{id}` {方法名} — {目的}
2. `{id}` {方法名} — {目的}

**为什么是这几个**：{一段说明}
```

若方法涉及 2 组或 3+ 组比较，先查 `comparison-methods.md` 的标准检验树（正态性 → 方差齐性 → 具体方法 → 效应量）。

**遇到不熟悉的统计方法**：触发 `reference-agent` 的 `method_search`（见 `agents/reference-agent.md §method_search`），输出摘要级说明再继续。
</substep>

<substep name="branch_gate">
按 `analysis_decision_policy.md §5` 判断是否停下来问用户。

**自动推进**（全部满足）：
- 只有一条明确路径
- 不改变已有结论方向
- 方法数 < 2

**必须停下询问**（任一成立）——对应 `analysis_decision_policy.md §5` 的六种情形：

1. ≥ 2 条规则指向互斥动作
2. 会推翻已有结论
3. 需改变主要终点或主要人群
4. 属探索性/事后分析（需用户同意标注）
5. 预算即将耗尽
6. 数据质量不足以支撑该动作

停下来时用 `AskUserQuestion`，给出**选项而非开放问题**：

```
Batch {N} 出现分叉，需要你决定：
A. {动作1} — 优点…，代价…
B. {动作2} — 优点…，代价…
C. 停止分析，把当前发现写入局限性
```

`ask_on_branch: false` 时只打印提议不阻塞，但仍要写入日志。
</substep>

<substep name="execute_batch">
执行本批每个方法。**方法执行的强制规则（与 2.x 一致）**：

1. **同时创建两个目录**：`03_AnalysisMethods/{id}/` 与 `04_Outputs/{id}/`
   - 方法 ID 格式 `{NN}_{MethodName}`（如 `06_SensitivityAnalysis`）
   - **禁止** `_sensitivity` 这类裸下划线前缀
2. 生成 R/Python 代码
   - 必须 `source("04_Outputs/_figure_config.R")`
   - **禁止**重定义 `_figure_config.R` 里的函数
   - 代码必须**自包含**：所有变量在脚本内定义，不依赖全局状态
3. 运行、验证产物存在、写 `方法说明.md`

**方法说明.md 至少包含**：

- 分析目的
- 数据与变量
- 方法与参数（含软件版本）
- **输出结果**（供阶段3 的 Results 直接引用）
- 假设检验与偏倚说明
</substep>

<substep name="record_batch">
把本批写入 `.clinpub/ANALYSIS_LOG.md`，格式严格按 `analysis_decision_policy.md §7`：

```markdown
## Batch {N} — {标签}（{日期}）

### 依据
- 触发规则：{R01/D03/U}
- 上一批观察：…
- 决策来源：自动推进 / 用户确认

### 本批方法
| id | 方法 | 目的 | 状态 |

### 结果要点
- {method}: 效应量 = …，95%CI …，p = …

### 解读
- {判断，不是复述数字}

### 下一批决策
- 决定 / 理由 / 候选

### 否决项
- {方法}: 否决原因
```

**六段缺一不可。**「否决项」为空也要写"无"。
</substep>

<substep name="check_continue">
按 `analysis_decision_policy.md §6` 判断是否退出循环：

| 编号 | 判据 |
|---|---|
| S1 | 核心假设已验/证伪，效应量与 CI 稳定 |
| S2 | 连续两批无新实质发现 |
| S3 | 触及 `analysis_budget` 上限 |
| S4 | 用户要求停止 |
| S5 | 数据质量已成限制（写入局限性，不再分析） |

**退出时必须在日志里写明命中的判据编号与理由。**

未退出 → 回到 `propose_batch` 开始下一批。
</substep>
</step>

<step name="verify_outputs" priority="medium">
循环结束后统一验证：

1. 每个方法的图 + 表 + `方法说明.md` 齐全
2. 图 ≥300 DPI、英文标注、`theme_pub` 风格
3. 统计报告含**效应量 + 95%CI + 精确 p 值**
4. 代码可从 `cleaned.csv` 独立运行
5. R 版本与关键包版本已记录
6. `04_Outputs/MANIFEST.yaml` 存在，标注 writer-agent 为消费者
7. **共享配置检查**：`04_Outputs/_figure_config.R` 存在，且 `03_AnalysisMethods/` 下每个 R 脚本都含 `source("04_Outputs/_figure_config.R")`（grep 验证）
8. **目录一致性**：`03_AnalysisMethods/` 与 `04_Outputs/` 的子目录名必须一一对应
9. **日志完整性**：`ANALYSIS_LOG.md` 每个 Batch 六段齐全，且方法清单与 `03_AnalysisMethods/` 实际目录一致

缺 MANIFEST 则在此补写。
</step>

<step name="freeze_analysis" priority="high">
冻结分析，产出供阶段3 消费的收敛摘要 `.clinpub/phases/02-analysis/ANALYSIS_SUMMARY.md`：

```markdown
# 分析摘要

## 核心发现
（3–5 条，每条：发现 + 效应量 + CI）

## 分析方法总览
（按实际执行顺序，供 Methods 的 Statistical Analysis 小节直接对应）

## 关键分析决策
（为什么选这些方法；哪些备选被否决及原因 → Discussion 的局限性素材）

## 稳健性证据
（敏感性分析结果）

## 已知局限
（数据层面的，供 Discussion 引用）
```

**冻结的含义**：此后新增分析必须走 `modify` 或写作阶段的反馈边（见 `writing.md`），
且必须更新 `ANALYSIS_LOG.md` 与本节摘要。
</step>

<step name="user_satisfaction_check" priority="high">
进入 milestone 前确认用户满意度：

```
✅ 阶段2 分析已冻结，共 {N} 批 {M} 个方法，结果保存于 04_Outputs/。

请确认：
- 满意 → 继续 `/clinpub next` 关闭阶段2，进入阶段3 写作
- 不满意 → 用 `/clinpub-modify` 调整方法、变量或图表样式
```

- 选「满意」→ 进入 `milestone`
- 选「不满意」→ 引导 `/clinpub-modify`；修改完成后回到 `verify_outputs` 复检
</step>

<step name="milestone" priority="high">
执行 milestone workflow 正式关闭阶段2：

```bash
# 1. 验证阶段2 成功标准
# 2. 收集分析决策（方法选择、参数、否决项）
# 3. 生成 .clinpub/phases/02-analysis/MILESTONE.md
# 4. 更新 ROADMAP.md：阶段2 → ✅，阶段3 → 🔄
# 5. 更新 STATE.md：阶段 → 3
# 6. 请求用户签字
```

见 `pipeline/workflows/milestone.md`。

<output name="signoff_prompt" format="user_facing">
────────────────────────────────
✅ 阶段2 核验完成

请确认：输入 "approved" 进入阶段3（论文写作），或描述需要调整的地方。
────────────────────────────────
</output>
</step>

</process>

<statistical_reporting_standards>
- 每个分析：**效应量 + 95%CI + 精确 p 值**（不是只写 "p < 0.05"）
- p 值写精确值，极小写 `p < 0.001`，**禁止** `p = 0.000`
- 多重比较：FDR / Bonferroni 校正
- 报告软件：R 版本 + 关键包版本
- 检验假设：正态性、方差齐性、比例风险
- 违反假设时必须记录并说明缓解措施
- 事后分析必须标注 `post hoc / exploratory`
</statistical_reporting_standards>

<success_criteria>
- 数据结构已诊断并写入 `00-DIAGNOSIS.md`
- `ANALYSIS_LOG.md` 存在，每个 Batch 六段齐全（含否决项）
- 批次选择可追溯到 `analysis_decision_policy.md` 的具体规则编号
- 分叉情形按 `§5` 停下询问（或 `ask_on_branch: false` 时已记录）
- 退出循环时写明命中的饱和判据编号
- `_figure_config.R` 已生成且被所有方法脚本 `source()`
- 每个方法有完整的图 + 表 + 方法说明
- 所有图达到出版级（≥300 DPI、theme_pub、英文标注）
- 统计报告含效应量 + 95%CI + p 值
- 代码可从 `cleaned.csv` 独立复现
- `04_Outputs/MANIFEST.yaml` 存在
- `ANALYSIS_SUMMARY.md` 已生成（供阶段3 使用）
- 用户已知悉并确认相位结束
</success_criteria>
