# 分析方法参考库

> 本文件不是固定菜单，而是 Claude 在 Phase 2 讨论时**按数据特征动态推荐分析方法**的参考知识库。
> **不要直接列出所有方法让用户打勾，而是根据数据特征诊断后给出定制建议。**

---

## 一、通用要求（所有分析必须遵守）

- 全部读取 `cleaned.csv`，写入 `04_Outputs/XX_MethodName/`
- 统一应用 `theme_pub()`（见 `r_patterns.md §1.2`）
- 每方法生成 `方法说明.md`（注明图例、表注、方法参数，使用模板 `pipeline/templates/method-readme.md`）
- 报告效应量 + 95%CI + 精确 p 值
- 目录编号按协议顺序动态编号（`01_`, `02_`, ...）

---

## 二、方法选择决策树

Phase 2 讨论时，Claude 必须按此流程分析数据特征，**然后**给出方法建议。

### Step 1: 诊断数据结构

```yaml
data_structure:
  n_patients: 86
  n_timepoints: 3           # 若 > 1 则标记为 longitudinal
  time_labels: ["baseline", "post_treatment", "follow_up"]
  groups:
    count: 2
    names: ["{group_A}", "{group_B}"]  # 实际名称来自用户数据
  outcomes:
    - name: "{outcome_1}"    # 实际变量名来自 cleaned.csv
      type: continuous       # binary / continuous / survival / categorical
      distribution: "略偏态"  # 正态 / 偏态 / 双峰
    - name: "{outcome_2}"
      type: continuous
  has_id: true               # 有患者标识符
  missing_pattern: "{variable} 在 follow_up 缺失（结构性缺失）"
```

> **多领域示例**：上述结构适用于任何临床领域——肿瘤（group_A=化疗 vs group_B=安慰剂）、心血管（降压方案 A vs B）、内分泌（胰岛素 vs 口服药）、骨科（手术 vs 保守治疗）、精神科（干预 vs 对照）。实际变量名和分组来自用户的 `cleaned.csv`。

### Step 2: 按特征匹配分析策略

| 数据特征 | 推荐方法方向 | 原因 |
|---------|-------------|------|
| 2 组 + 连续结局 | t检验 / Wilcoxon + 混合模型 | 基础比较 + 纵向需重复测量 |
| 2 组 + 二分类结局 | Logistic 回归 | OR 可解释性强 |
| 2 组 + 生存时间 | KM曲线 + Cox 回归 | 时间-事件数据标准方法 |
| 3+ 组 | ANOVA / Kruskal-Wallis + 事后比较 | 多重比较 |
| 纵向（同一人多时间点） | **混合模型**（lme4）代替独立 t 检验 | 处理组内相关性 |
| 多标志物 + 诊断 | ROC + LASSO + 分类模型 | 诊断价值评估 |
| 无分组/无结局 | 描述性统计 + 相关性 | 仅可做相关性/聚类 |
| 连续变量间关系 | 线性回归 + 相关性矩阵 | 关联分析 |
| 观察性研究 + 混杂控制需求 | PSM/IPTW + 匹配后分析 (§3.8) | 减少选择偏倚 |
| 生存数据 + 多种互斥事件 | 竞争风险模型 Fine-Gray (§3.8) | 标准 Cox 高估主要事件风险 |
| 连续暴露 + 疑似非线性关系 | RCS 样条 + 非线性检验 (§3.9) | 避免线性假设偏差 |
| 5%-20% 缺失率 | MICE 多重插补 (§3.10) | 比完整病例分析更优的效力和偏倚控制 |
| 暴露→中介→结局路径 | 中介分析 causal mediation (§3.11) | 分解直接/间接效应 |
| 暴露效应受第三变量影响 | 调节分析 交互项+简单斜率 (§3.11) | 识别效应异质性 |
| 人群异质性 + 无预设分组 | 聚类分析 k-means/LCA (§3.12) | 发现潜在表型亚型 |
| 计数结局（罕见事件） | Poisson / 负二项回归 | 事件率建模 |
| 配对/匹配设计 | 条件 Logistic / 配对检验 | 控制匹配因素 |

> **💡 未知方法？** 如果用户提到的统计方法不在本决策树中，系统会自动搜索方法概览并与用户讨论。
> 参见 `agents/reference-agent.md` 的 `method_search` 模式。

### Step 3: 组织成方案 + 依赖顺序

将推荐的分析组织为**波次（wave）**，保证前序结果可供后续使用。

**波次数量不固定**——取决于方案复杂度：
- 简单描述性项目 → 可能只有 1 个波次
- 标准 RCT 分析 → 通常 2-3 个波次
- 含预测建模的全面分析 → 可能 4-5 个波次

波次划分规则（一般为基线描述 → 单变量比较 → 多变量模型 → 预测/诊断）：

| 波次 | 类型 | 示例方法 | 依赖 |
|------|------|---------|------|
| Wave 1 | 描述性（无依赖） | 基线表、描述统计 | 无 |
| Wave 2 | 比较性 | t检验、回归、混合模型 | 可能依赖 W1 的基线结果指导协变量选择 |
| Wave 3+ | 调整模型 | 多因素回归、亚组分析 | 依赖前序单变量结果 |
| 最后一波 | 预测/诊断 | ROC、LASSO、ML | 需训练/验证集划分 |

**如果项目只需要 1 个波次（如"只要一个描述统计"），那就只执行 1 个波次。**
**如果审稿阶段要求新增分析，就追加一个新波次。**

### Step 4: 输出方案给用户确认

```markdown
## 推荐分析方案

基于数据诊断，建议以下分析方案：

### Wave 1：基线特征描述
1. **基线表** — 比较 {group_A} vs {group_B} 组的人口学和临床特征（t检验 / 卡方）
2. **描述性统计** — 各时间点 {outcome_1}/{outcome_2} 的 mean±SD

### Wave 2：组间比较与纵向分析
3. **基线组间比较** — {outcome_1}/{outcome_2} 在 {group_A} vs {group_B} 的差异（Wilcoxon，因数据偏态）
4. **重复测量混合模型** — time×group 交互效应（lme4），评估干预是否随时间改善更显著

### Wave 3：多因素分析
5. **线性回归** — 调整年龄、性别、BMI 后干预对 {outcome} 变化的效应

---

**请确认：**
- 这些方法是否符合您的研究问题？
- 需要增加/删减哪些分析？
- 协变量选择是否合适？
```

---

## 三、分析场景参考库（按场景组织）

以下是常见分析场景的技术参考。**不是逐条执行清单**，而是在确定分析方案后，查阅对应条目的实现细节。

### 3.1 基线/描述性分析

#### BaselineTable（基线特征表）
- **用途**：按分组展示人口学和临床特征
- **输出**：Table 1（docx 三线表）
- **统计量**：连续变量 mean±SD 或 median(IQR)；分类变量 n(%)
- **组间比较**：t检验/卡方检验/Wilcoxon（根据分布选择）
- **实现**：`gtsummary::tbl_summary()` + `add_p()`

#### DescriptiveStats（描述性统计）
- **用途**：展示全样本的变量分布特征
- **输出**：描述统计表（Excel）+ 分布图
- **内容**：N, mean, SD, median, IQR, min, max, 缺失率

### 3.2 组间比较

#### TwoGroupComparison（两组比较）
- **用途**：比较两组在一个或多个结局上的差异
- **输出**：箱线图/小提琴图 + 统计结果表
- **方法选择**：
  - 正态分布 + 方差齐 → 独立样本 t 检验
  - 偏态分布 → Wilcoxon 秩和检验
  - 配对设计 → 配对 t 检验 / Wilcoxon 符号秩检验
- **完整决策树**：参见 `comparison-methods.md §二` — 含正态性检验驱动的自动分支、方差不齐处理、效应量公式。
- **绘图**：三层绘图法（见 `r_patterns.md §2.1`）+ 动态显著性标注（见 `r_patterns.md §1.4`）

#### MultiGroupComparison（多组比较）
- **用途**：比较三组及以上
- **方法选择**：
  - 正态 + 方差齐 → ANOVA + Tukey HSD
  - 偏态 → Kruskal-Wallis + Dunn 事后比较
- **完整决策树**：参见 `comparison-methods.md §三` — 含 Welch ANOVA、Games-Howell、Kruskal-Wallis+Dunn 分支。

#### RepeatedMeasures（重复测量）
- **用途**：同一患者在多个时间点的测量（纵向数据）
- **方法选择**：
  - 两组 + 两个时间点：混合模型（`lme4::lmer()`），关注 time×group 交互项
  - 两组 + 多时间点：混合模型 + 时间趋势对比
  - 多组 + 多时间点：混合模型 + 简单效应分析
- **完整决策树**：参见 `comparison-methods.md §四` — 含配对 t 检验、Wilcoxon 符号秩、重复测量 ANOVA、Friedman 检验分支。
- **模型规范**：
  ```r
  library(lme4)
  # 随机截距模型：每个患者有自己的基线水平
  m <- lmer(HAMD_total ~ Treatment * time + age + sex + (1 | name), data = full_data)
  # 输出：固定效应表 + 交互作用 p 值 + 边际均值（emmeans）
  library(emmeans)
  emmeans(m, ~ Treatment | time)
  ```
- **关键细节**：
  - `(1 | name)` 处理组内相关性
  - 交互项 `Treatment * time` 是核心检验
  - 检查残差正态性（`qqnorm(resid(m))`）
  - 报告边际均值（`emmeans`）而非原始均值

#### ChangeScore（变化量分析）
- **用途**：比较两组在干预前后的变化量
- **输出**：变化量箱线图 + 统计表
- **构造**：`change = post_treatment - baseline`，然后做两组比较

### 3.3 回归/关联分析

#### LinearRegression（线性回归）
- **用途**：连续结局的多因素关联分析
- **输出**：回归系数表（β, 95%CI, p）+ 诊断图
- **流程**：单因素筛选（p<0.20）→ 多因素 → 模型诊断（残差正态性、VIF、异方差）

#### LogisticRegression（Logistic 回归）
- **用途**：二分类结局的多因素关联分析
- **输出**：OR + 95%CI + p 值表 + 森林图
- **流程**：单因素 → 多因素 → Hosmer-Lemeshow 检验 → VIF → ROC
- **结局要求**：因变量必须是二分类（0/1）
  - 连续变量 → 线性回归，或创建有临床意义的二分类切点（记录切点依据）

#### OrdinalRegression（有序回归）
- **用途**：有序多分类结局（如轻度/中度/重度）
- **实现**：`MASS::polr()`

#### MixedModel（混合效应模型）
- **用途**：纵向数据或聚类数据的多因素分析
- **关键**：纳入随机效应处理组内相关性

### 3.4 生存分析

#### SurvivalAnalysis（生存分析）
- **用途**：时间-事件数据
- **输出**：KM 曲线（风险表）+ Cox 回归表 + 森林图
- **流程**：KM → Log-rank → 单因素 Cox → 多因素 Cox → PH 假设检验（Schoenfeld 残差）
- **推荐包**：`survival`, `survminer`, `ggsurvfit`

### 3.5 亚组与敏感性分析

#### SubgroupAnalysis（亚组分析）
- **用途**：检验效应是否在特定亚组中一致
- **输出**：亚组森林图 + 交互作用 p 值表
- **实现**：`bregr` 或手动分层回归

#### SensitivityAnalysis（敏感性分析）
- **用途**：检验结果对分析假设的稳健性
- **常见方案**：排除特殊人群、不同定义、E-value、不同模型

### 3.6 相关性

#### CorrelationAnalysis（相关性分析）
- **用途**：变量间关联方向和强度
- **输出**：相关系数矩阵热图 + 散点图矩阵
- **方法**：正态 → Pearson；偏态 → Spearman
- **实现**：`cor()` + `ggcorrplot` / `GGally::ggpairs`

### 3.7 诊断/预测

#### ROCAnalysis（ROC 分析）
- **用途**：评估标志物/模型的区分能力
- **输出**：ROC 曲线 + AUC 表 + 森林图（AUC 汇总）
- **两种模式**：
  - Unadjusted：`pROC::roc(outcome ~ biomarker)`
  - Adjusted：Logistic 回归预测概率做 ROC
- **关键计算**：Wilson Score CI（敏感度/特异度）、Youden 指数最佳阈值

#### MarkerPanel（标志物面板建模）
- **用途**：多标志物联合诊断价值
- **流程**：LASSO 特征选择 → 面板 ROC → 混淆矩阵 → 风险分层
- **依赖**：需要训练/验证集划分

#### SimpleML（机器学习）
- **用途**：预测建模（当预测而非解释为主要目标时）
- **方法**：随机森林 / XGBoost / SVM
- **输出**：特征重要性 + ROC + 混淆矩阵

### 3.8 因果推断与混杂控制

#### PropensityScoreMethods（倾向性评分方法）
- **用途**：观察性研究中控制混杂偏倚
- **子类型**：PSM（1:1 / 1:N 匹配）、IPTW（逆概率加权）、PS 分层
- **输出**：Love plot（匹配前后 SMD 对比）+ 加权后基线表 + 处理效应估计
- **R 代码模式**：
  ```r
  # PSM
  library(MatchIt)
  m_out <- matchit(treatment ~ age + sex + bmi + comorbidity,
                   data = cleaned, method = "nearest", ratio = 1)
  matched_data <- match.data(m_out)
  # 平衡诊断
  library(cobalt)
  bal_tab <- bal.tab(m_out)
  love.plot(bal_tab, threshold = 0.1)  # 见 r_patterns §2.12
  # IPTW
  library(WeightIt)
  w_out <- weightit(treatment ~ age + sex + bmi, data = cleaned, method = "ps")
  ```
- **关键细节**：
  - 匹配质量报告：SMD < 0.1 为平衡
  - 加权后样本量变化
  - 敏感性分析配合 E-value
  - 参见图表：r_patterns §2.12 Love Plot

#### CompetingRisks（竞争风险模型）
- **用途**：当研究对象可能经历多种互斥事件时（如死亡 vs 复发 vs 失访）
- **输出**：累积发生率函数（CIF）曲线 + Fine-Gray 回归表（SHR + 95%CI）
- **R 代码模式**：
  ```r
  library(cmprsk)
  # Fine-Gray 模型
  fg_model <- crr(ftime, fstatus, cov1 = model.matrix(~ treatment + age, data)[, -1])
  summary(fg_model)  # SHR + 95%CI + p-value
  # 可视化
  library(ggsurvfit)
  cuminc(Surv(time, status) ~ treatment, data = cleaned) %>%
    ggcuminc(outcome = "event_of_interest") + theme_pub()
  ```
- **关键细节**：
  - 与标准 Cox 的区别：subdistribution hazard vs cause-specific hazard
  - Gray 检验做组间比较
  - 依赖 SurvivalAnalysis 的结果作为前序参考

### 3.9 非线性与剂量反应分析

#### RCSAnalysis（限制性立方样条分析）
- **用途**：探索连续暴露与结局之间的非线性剂量反应关系
- **输出**：RCS 曲线图（含 95%CI 带）+ 非线性检验 p 值
- **R 代码模式**：
  ```r
  library(rms)
  dd <- datadist(cleaned); options(datadist = "dd")
  # RCS 模型（通常 3-5 个 knots，按 Harrell 推荐百分位数）
  fit <- ols(outcome ~ rcs(exposure, 4) + age + sex, data = cleaned)
  anova(fit)  # 非线性检验
  # 可视化
  p <- Predict(fit, exposure, ref.zero = TRUE)
  ggplot(p, aes(exposure, yhat)) +
    geom_line(color = "#0072B5") +
    geom_ribbon(aes(ymin = lower, ymax = upper), alpha = 0.2, fill = "#0072B5") +
    geom_rug(data = cleaned, aes(x = exposure), sides = "b") +
    theme_pub() +
    labs(x = "Exposure", y = "Adjusted Effect (95% CI)",
         title = paste0("P for non-linearity = ", round(anova(fit)["exposure", "P"], 4)))
  ```
- **关键细节**：
  - 参考值选取：中位数或临床有意义的值
  - knot 敏感性分析（3/4/5 个 knots 比较）
  - 参见图表：r_patterns §2.13 RCS 曲线

### 3.10 缺失数据处理

#### MICEImputation（多重插补）
- **用途**：处理 5%-20% 缺失率的变量（与 data-prep 三级策略配合）
- **输出**：插补收敛诊断图（trace plot）+ 插补前后分布对比图 + 汇集（pooled）分析结果
- **R 代码模式**：
  ```r
  library(mice)
  # 插补（m=5 为默认，method='pmm' 适用于连续+分类混合）
  imp <- mice(cleaned, m = 5, method = "pmm", seed = 42,
              predictorMatrix = quickpred(cleaned, mincor = 0.1))
  # 诊断：收敛性
  plot(imp, c("exposure", "outcome"))  # trace plot
  # 诊断：分布对比
  densityplot(imp)  # 插补值 vs 观测值
  # 汇集分析
  fit_imp <- with(imp, lm(outcome ~ treatment + age + sex))
  pooled <- pool(fit_imp)
  summary(pooled, conf.int = TRUE, exponentiate = FALSE)
  ```
- **关键细节**：
  - m=5 为默认插补次数，缺失率 >20% 时建议 m=20
  - 预测矩阵设计：排除 ID 变量和不相关变量
  - Rubin 规则汇集
  - 与完整病例分析的敏感性比较
  - 依赖 Phase 1 data-prep 的缺失值诊断结果

### 3.11 中介与调节分析

#### MediationAnalysis（中介分析）
- **用途**：检验暴露是否通过某个中介变量间接影响结局
- **输出**：中介效应路径图 + 直接效应/间接效应/总效应表 + Bootstrap CI
- **R 代码模式**：
  ```r
  library(mediation)
  # 中介模型：exposure → mediator → outcome
  med_fit <- lm(mediator ~ exposure + age + sex, data = cleaned)
  out_fit <- lm(outcome ~ exposure + mediator + age + sex, data = cleaned)
  # 因果中介分析
  med_result <- mediate(med_fit, out_fit, treat = "exposure",
                        mediator = "mediator", sims = 1000, boot = TRUE)
  summary(med_result)
  # 报告：ACME（平均因果中介效应）、ADE（平均直接效应）、总效应、比例中介
  ```
- **关键细节**：
  - 因果中介分析的前提假设：无未测量混杂
  - 报告 ACME、ADE、总效应、proportion mediated
  - Bootstrap 法（sims=1000）估计间接效应 CI

#### ModerationAnalysis（调节分析）
- **用途**：检验某变量是否改变暴露-结局关系的强度或方向
- **输出**：交互效应表 + 简单斜率图（在调节变量不同水平下的效应）
- **R 代码模式**：
  ```r
  # 交互项模型
  fit <- lm(outcome ~ exposure * moderator + age + sex, data = cleaned)
  summary(fit)  # 交互项系数 + p 值
  # 简单斜率
  library(emmeans)
  emtrends(fit, ~ moderator, var = "exposure",
           at = list(moderator = c(mean - sd, mean, mean + sd)))
  # Johnson-Neyman 区间（连续调节变量）
  library(interactions)
  sim_slopes(fit, pred = exposure, modx = moderator, plot = TRUE) + theme_pub()
  ```
- **关键细节**：
  - 区分调节（moderation）和中介（mediation）的概念
  - 连续调节变量时 J-N 区间的解读
  - 调节变量在 ± 1 SD 处的简单斜率

### 3.12 聚类与模式识别

#### ClusterAnalysis（聚类分析）
- **用途**：识别研究人群中的潜在亚型或表型模式
- **子类型**：k-means / 层次聚类 / LCA（潜在类别分析）
- **输出**：轮廓系数/肘部法则图（最优聚类数）+ 聚类特征热图 + 各聚类人群描述表
- **R 代码模式**：
  ```r
  library(factoextra)
  # 标准化聚类变量
  cluster_vars <- scale(cleaned[, c("var1", "var2", "var3")])
  # 最优 k 选择
  fviz_nbclust(cluster_vars, kmeans, method = "silhouette") + theme_pub()
  # k-means 聚类
  set.seed(42)
  km <- kmeans(cluster_vars, centers = 3, nstart = 25)
  cleaned$cluster <- as.factor(km$cluster)
  # 聚类特征描述
  library(gtsummary)
  tbl_summary(cleaned, by = cluster, include = c(var1, var2, var3, age, sex)) %>%
    add_p()
  # LCA（潜在类别分析）
  library(poLCA)
  lca_model <- poLCA(cbind(item1, item2, item3) ~ 1, data = cleaned, nclass = 3)
  ```
- **关键细节**：
  - 聚类数选择标准：BIC/AIC/轮廓系数
  - 聚类可解释性（临床意义 > 统计指标）
  - 聚类结果稳定性检验（bootstrap resampling）

---

## 四、依赖关系与执行顺序

### 动态波次规则

每次讨论确认分析方法后，按此规则自动计算依赖顺序：

```
1. 如果方法 A 的输出是方法 B 的输入 → B 在 A 之后
2. 基线描述（基线表、描述统计）→ 无依赖，最先执行
3. 单变量分析（t检验、相关）→ 无依赖，随基线后
4. 多变量模型（回归）→ 依赖单变量结果（变量筛选依据）
5. 诊断/预测（ROC、ML）→ 依赖模型结果
```

每个波次在输出完整后向用户呈现检查点，**用户确认后才进入下一波次**。

### 波次数量完全由方案决定

不是固定的 4 波：

| 项目类型 | 波次数 | 说明 |
|---------|--------|------|
| 仅描述性报告 | 1 波 | BaselineTable 即可 |
| 两组比较 | 2 波 | Wave 1: 基线表 | Wave 2: 组间比较 |
| 完整 RCT | 3-4 波 | 基线表 → 组间比较 → 多因素回归 |
| 探索性+诊断 | 4-5 波 | 基线 → 比较 → 回归 → ROC → ML |
| 审稿补充分析 | N+1 波 | 在已有方案最后追加新波次 |

- 基线表/描述统计：**仅使用 baseline 时间点**
- 重复测量模型：**使用所有时间点的完整数据**（`full_longitudinal.csv`）
- 基线组间比较：**仅使用 baseline**，与基线表一致
- 变化量分析：**使用 baseline + post_treatment**

每个方法在执行前应明确标注使用哪个时间点的数据。

---

## 五、讨论话术（与用户沟通的参考）

### 开场白
```
我分析了您的数据：
- {N} 个患者，{K} 个变量
- {分组变量} 分 {M} 组：{组名}
- {时间点数量} 个时间点：{时间点标签}
- 结局变量：{结局变量名}（{binary/continuous/survival}）

基于这些特征，我建议的分析方案是...
```

### 当用户不确定时
```
您的研究问题是比较两组差异，还是评估某个变量的预测价值？
从数据来看，您的结局变量是连续型（HAMD 评分范围 6-26），
建议优先做：
1. 基线表（了解两组是否均衡）
2. 组间比较（cTBS 是否优于 Sham）
3. 如果存在时间点，还可以做重复测量模型

您觉得这个方向合适吗？
```

### 当数据不适合某种方法时
```
我注意到您的结局变量是连续型的，
所以 Logistic 回归不太适合（它要求二分类结局）。
建议改为线性回归，或者如果您有临床公认的切点，
可以把连续评分转为高低分组再使用 Logistic 回归。
```
