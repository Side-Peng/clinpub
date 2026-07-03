# 组间对比方法决策树

> 本文件定义组间对比的标准化方法选择流程，供 clinpub-planner 和 analyst-agent 在分析规划/执行时查阅。
> 配合 `analysis_methods.md` §3.2 使用，提供更细粒度的分支规则。

---

## 一、方法选择概览树

| 组数 | 结局类型 | 正态性 | 方差齐性 | 推荐方法 | 事后比较 | 效应量 |
|------|---------|--------|---------|---------|---------|-------|
| 2组 | 连续 | 正态 | 齐 | 独立样本 t 检验 | — | Cohen's d |
| 2组 | 连续 | 正态 | 不齐 | Welch t 检验 | — | Cohen's d |
| 2组 | 连续 | 非正态 | — | Mann-Whitney U 检验 | — | r = Z/√N |
| 2组 | 分类 | — | 理论频数≥5 | 卡方检验 | — | Cramer's V / φ |
| 2组 | 分类 | — | 理论频数<5 | Fisher 精确检验 | — | Cramer's V / φ |
| 3+组 | 连续 | 正态 | 齐 | 单因素 ANOVA | Bonferroni / Tukey | η² / partial η² |
| 3+组 | 连续 | 正态 | 不齐 | Welch ANOVA | Games-Howell | η² / partial η² |
| 3+组 | 连续 | 非正态 | — | Kruskal-Wallis 检验 | Dunn 检验 | η² (H 统计量) |
| 3+组 | 分类 | — | 理论频数≥5 | 卡方检验 | 列联表事后分析 | Cramer's V |
| 3+组 | 分类 | — | 理论频数<5 | Fisher 精确检验 | 列联表事后分析 | Cramer's V |

**决策流程：** 组数（2 vs 3+）→ 结局类型（连续/分类）→ 前提条件检验（正态性/方差齐性/理论频数）→ 选择方法 → 事后比较（若组数>2且显著）→ 效应量报告。

---

## 二、两组比较细则（D-08, D-09）

### 2.1 两组—连续结局（D-08）

自动检测流程：
1. **正态性检验**：Shapiro-Wilk 检验（每组 N<50）或 Kolmogorov-Smirnov（N≥50）
   - 两组均正态 → 走参数路径
   - 任一组非正态 → 走非参数路径
2. **方差齐性检验**（仅参数路径）：Levene 检验或 F 检验
   - 方差齐 → 独立样本 t 检验
   - 方差不齐 → Welch t 检验
3. **非参数路径** → Mann-Whitney U 检验

**R 代码参考：**
```r
# 正态性检验
shapiro.test(data$value[data$group == "A"])
shapiro.test(data$value[data$group == "B"])

# 方差齐性检验（参数路径）
car::leveneTest(value ~ group, data = data)

# 执行
if (both_normal && var_equal) {
  t.test(value ~ group, data = data, var.equal = TRUE)
} else if (both_normal && !var_equal) {
  t.test(value ~ group, data = data, var.equal = FALSE)  # Welch
} else {
  wilcox.test(value ~ group, data = data)  # Mann-Whitney U
}
```

### 2.2 两组—分类结局（D-09）

1. 构建列联表：`table(group, outcome)`
2. 计算理论频数：`chisq.test(tbl)$expected`
3. 所有格理论频数 ≥5 → Pearson 卡方检验
4. 任一理论频数 <5 → Fisher 精确检验

```r
tbl <- table(data$group, data$outcome)
chisq_test <- chisq.test(tbl)
if (any(chisq_test$expected < 5)) {
  fisher.test(tbl)  # Fisher 精确检验
} else {
  chisq_test       # 卡方检验
}
```

---

## 三、三组以上比较细则（D-10, D-11）

### 3.1 三组+—连续结局（D-10）

自动检测流程：
1. **正态性检验**：每组的 Shapiro-Wilk 或 K-S
2. **方差齐性检验**（仅参数路径）：Levene 检验或 Bartlett 检验
3. **分支路径**：
   - 全部正态 + 方差齐 → **单因素 ANOVA** + Tukey HSD 事后比较（平衡设计）或 Bonferroni 校正（非平衡）
   - 全部正态 + 方差不齐 → **Welch ANOVA** + Games-Howell 事后比较
   - 任一组非正态 → **Kruskal-Wallis 检验** + Dunn 事后比较（Bonferroni 校正）

```r
# 正态性：对每组做
by(data$value, data$group, shapiro.test)

# 方差齐性
car::leveneTest(value ~ group, data = data)

# 执行
if (all_normal && var_equal) {
  fit <- aov(value ~ group, data = data)
  TukeyHSD(fit)
} else if (all_normal && !var_equal) {
  oneway.test(value ~ group, data = data)  # Welch ANOVA
  # Games-Howell: 需 PMCMRplus 包或手动计算
} else {
  kruskal.test(value ~ group, data = data)
  # Dunn 事后: FSA::dunnTest(value ~ group, data = data, method = "bonferroni")
}
```

### 3.2 三组+—分类结局（D-11）

逻辑同两组分类（§2.2），加列联表事后分析：
- 卡方检验显著 → 做标准化残差分析或两两列联表比较（Bonferroni 校正）

```r
tbl <- table(data$group, data$outcome)
chisq_test <- chisq.test(tbl)
if (any(chisq_test$expected < 5)) {
  fisher.test(tbl, simulate.p.value = TRUE)
} else {
  chisq_test
  # 事后分析：标准化残差
  round(chisq_test$residuals, 2)
}
```

---

## 四、配对/重复测量设计（D-12）

| 设计 | 变量类型 | 正态性 | 方法 |
|------|---------|--------|------|
| 两组配对 | 连续 | 正态 | 配对 t 检验 |
| 两组配对 | 连续 | 非正态 | Wilcoxon 符号秩检验 |
| 两组配对 | 分类 | — | McNemar 检验 |
| 多组重复测量 | 连续 | 正态+球性 | 重复测量 ANOVA |
| 多组重复测量 | 连续 | 非正态/球性不齐 | Friedman 检验 |
| 多组重复测量 | 分类 | — | 广义估计方程 (GEE) / Cochran's Q |

```r
# 配对 t 检验
t.test(pre, post, paired = TRUE)

# Wilcoxon 符号秩检验
wilcox.test(pre, post, paired = TRUE)

# 重复测量 ANOVA
library(lme4)
m <- lmer(value ~ time * group + (1 | subject), data = data)
anova(m)

# Friedman 检验
friedman.test(value ~ time | subject, data = data)
```

---

## 五、效应量报告标准（D-13）

| 检验方法 | 效应量 | 公式 | 解释基准 |
|---------|--------|------|---------|
| 独立样本 t 检验 | Cohen's d | d = (M₁−M₂) / SD_pooled | 0.2小/0.5中/0.8大 |
| Mann-Whitney U | r | r = Z/√N | 0.1小/0.3中/0.5大 |
| 单因素 ANOVA | η² / partial η² | η² = SS_效应 / SS_总 | 0.01小/0.06中/0.14大 |
| Welch ANOVA | η² | 同上 | 同上 |
| Kruskal-Wallis | η² (H) | η² = (H−k+1)/(N−k) | 同上 |
| 卡方检验 | Cramer's V / φ | V = √(χ²/(N·min(r−1,c−1))) | 0.1小/0.3中/0.5大 |
| 配对 t 检验 | Cohen's d_z | d_z = t/√n | 同上 Cohen's d |
| Wilcoxon 符号秩 | r | r = Z/√N | 0.1小/0.3中/0.5大 |
| PSM/IPTW | SMD (Standardized Mean Difference) | SMD = (M₁−M₂) / SD_pooled | <0.1 平衡良好, <0.2 可接受 |
| Fine-Gray 竞争风险 | SHR (Subdistribution HR) | SHR = exp(β) from Fine-Gray model | 同 HR 解释，但针对亚分布风险 |
| 中介分析 | ACME / ADE | ACME: 平均因果中介效应; ADE: 平均直接效应 | ACME 显著 → 中介路径成立 |
| Meta 分析 | 合并效应量 (pooled d / OR / HR) | 随机/固定效应模型加权合并 | 异质性 I² < 50% 可接受 |

```r
# Cohen's d
library(effsize)
cohens_d(data$value, data$group)

# η²
library(lsr)
etaSquared(aov_model)

# Cramer's V
library(rcompanion)
cramerV(tbl)

# PSM 平衡诊断 — SMD
library(cobalt)
bal.tab(formula, data = data, method = "weighting")
love.plot(bal.tab_obj, threshold = 0.1)

# Fine-Gray 竞争风险
library(cmprsk)
fg_model <- crr(ftime = data$time, fstatus = data$status,
                cov1 = model.matrix(~ exposure + age + sex, data)[, -1])
summary(fg_model)  # SHR + 95% CI

# 中介分析
library(mediation)
med_fit <- lm(outcome ~ exposure + mediator + covariates, data = data)
med_result <- mediate(med_fit, treat = "exposure", mediator = "mediator",
                      boot = TRUE, sims = 1000)
summary(med_result)  # ACME, ADE, total effect, proportion mediated

# Meta 分析合并效应量
library(meta)
m <- metagen(TE, seTE, data = meta_data, sm = "OR", method.tau = "REML")
summary(m)  # pooled OR + 95% CI + I²
```

---

## 六、执行步骤（供 clinpub-executor 使用）

1. **读数据**：从 cleaned.csv 读取结局变量和分组变量
2. **检测组数**：unique(group) 的长度 → 2组 或 3+组
3. **检测结局类型**：unique(outcome) 的数量 + 数据类型 → 连续/分类
4. **按决策树选择方法**（查上面各节）
5. **检验前提条件**（正态性、方差齐性、理论频数）
6. **执行主检验**
7. **若显著且组数>2 → 事后比较**
8. **计算效应量 + 95% CI**
9. **输出**：统计结果表 + 效应量 + 可视化（箱线图/柱状图 + 显著性标注）

---

## 引用文献

- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
- Field, A. (2013). *Discovering Statistics Using IBM SPSS Statistics* (4th ed.). Sage Publications.
- Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science: a practical primer for t-tests and ANOVAs. *Frontiers in Psychology*, 4, 863. https://doi.org/10.3389/fpsyg.2013.00863
- Tomczak, M., & Tomczak, E. (2014). The need to report effect size estimates revisited. An overview of some recommended measures of effect size. *Trends in Sport Sciences*, 1(21), 19-25.
