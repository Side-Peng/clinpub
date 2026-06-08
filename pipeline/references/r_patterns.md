# R 可视化核心标准与分析模式

> 第一部分（Core Standards）是所有 clinpub R 代码生成必须遵守的强制标准。第二部分（Analysis Patterns）是按需取用的图类型代码，每种标注了适用条件和禁忌。

---

# 第一部分：Core Standards（强制标准）

以下规则适用于 clinpub 生成的所有 R 可视化代码，无论何种分析方法。

---

## 1.1 色彩规范与选色协议

### 核心原则

在生成任何图表**之前**，必须与用户沟通颜色方案：

1. **询问用户偏好**："您倾向于使用预设配色，还是指定具体颜色？"
2. **默认推荐色盲友好方案**（viridis / Okabe-Ito / RColorBrewer Set 系列）
3. **避免红绿组合**（红绿色盲最常见）

### 按分组数推荐配色

| 组数 | 推荐方案 | 示例代码 |
|------|---------|----------|
| **2组** | `c("#0072B5", "#BC3C29")` — Nature 风格，色盲友好 | `scale_fill_manual(values = c("#0072B5", "#BC3C29"))` |
| **3-4组** | RColorBrewer `"Set1"` 或 `"Dark2"` | `scale_fill_brewer(palette = "Set1")` |
| **5-8组** | RColorBrewer `"Set2"` 或 `"Paired"` | `scale_fill_brewer(palette = "Paired")` |
| **连续变量/热图** | viridis（默认方向） | `scale_fill_viridis_c(option = "D")` |
| **多标志物（>10）** | viridis `option = "D"` 或 `"G"` | `scale_color_viridis_d(option = "G")` |

### 色盲友好方案速查

```r
# Okabe-Ito 配色（8 种，色盲友好首选）
okabe_ito <- c("#E69F00", "#56B4E9", "#009E73", "#F0E442",
               "#0072B2", "#D55E00", "#CC79A7", "#000000")

# Nature 期刊双色（退而求其次）
nature_colors <- c("#0072B5", "#BC3C29")

# 当组数 > 8 时，使用 viridis 离散版
scale_color_viridis_d(option = "D", begin = 0.1, end = 0.9)
```

### 选色决策流程

```
数据有分组变量？
├── 是 → 用户有颜色偏好吗？
│   ├── 有 → 使用用户指定颜色
│   └── 没有 → 按组数套用推荐方案（见上表）
└── 否（连续变量/热图）
    └── 使用 viridis 连续色标
```

### 颜色一致性规则

- 同一分析方法内的多张图，**相同分组必须使用相同颜色映射**
- 若一个变量在正文和补充材料中均出现，颜色必须一致
- 多个 biomarker 之间使用同一色系区分强度，而非不同色系

---

## 1.2 出版级主题 `theme_pub()`

所有 ggplot2 图表**必须**应用此主题。

```r
theme_pub <- function(base_size = 10, base_family = "sans") {
  # base_size=10 更适合出版级图表（约 7-8pt 在最终排版中）
  # base_family="sans" 在 Windows 上默认映射到 Arial
  theme_minimal(base_size = base_size, base_family = base_family) %+replace%
    theme(
      # 图例
      legend.position = "right",
      legend.title = element_text(face = "bold", size = rel(0.9)),
      legend.text = element_text(size = rel(0.85)),
      # 标题
      plot.title = element_text(hjust = 0.5, size = rel(1.1), face = "bold"),
      # 轴
      axis.title = element_text(size = rel(1), face = "bold"),
      axis.text = element_text(size = rel(0.9), face = "bold"),
      axis.line = element_line(color = "black", linewidth = 0.5),
      # 网格
      panel.grid = element_blank(),
      panel.border = element_rect(color = "black", fill = NA, linewidth = 1),
      # 刻度
      axis.ticks = element_line(color = "black", linewidth = 0.5),
      # 分面
      strip.background = element_rect(fill = "grey95", color = "black"),
      strip.text = element_text(face = "bold", size = rel(0.9))
    )
}
```

**应用方式：** `+ theme_pub()`。

- 默认显示右侧图例（`legend.position = "right"`）。如需隐藏图例（如单组柱状图），覆盖为 `theme(legend.position = "none")`。
- 如需图例放在顶部：`theme(legend.position = "top")`。
- 字体族 `"sans"` 在 Windows 上映射到 Arial；Linux/macOS 可能需要 `extrafont` 包（见 §1.3）。

---

## 1.3 图表保存规范

```r
# 出版级分辨率常量 — 与 journal_standards.md::FIGURE_DPI 保持一致
PUBLICATION_DPI <- 300

# TIFF（LZW 压缩，投稿首选）
ggsave("figure.tiff", p, width = 7, height = 6, dpi = PUBLICATION_DPI, compression = "lzw")

# PNG（预览/网页）
ggsave("figure.png", p, width = 7, height = 6, dpi = PUBLICATION_DPI)

# PDF（矢量，排版）
ggsave("figure.pdf", p, width = 7, height = 6)
```

### 尺寸标准

| 用途 | 宽度 | 高度 | 格式 |
|------|------|------|------|
| 单栏图 | 8 cm (~3.15 in) | ≤ 20 cm | TIFF/PDF |
| 双栏图 | 17 cm (~6.7 in) | ≤ 20 cm | TIFF/PDF |
| 森林图/长图 | 17 cm | 自适应 | PDF |
| Nature 单栏 | 89 mm (~3.5 in) | 自适应 | TIFF/PDF |
| Nature 双栏 | 183 mm (~7.2 in) | 自适应 | TIFF/PDF |

所有输出必须 **≥300 DPI**，**Arial ≥8pt**。

### 字体族说明

`theme_pub(base_family = "sans")` 的字体族在不同平台上映射不同：

- **Windows**：`"sans"` 默认映射到 **Arial**，无需额外配置
- **Linux / macOS**：`"sans"` 可能映射到 DejaVu Sans 或 Helvetica，**不是 Arial**。如需严格使用 Arial：

```r
# 安装 extrafont（首次使用时）
install.packages("extrafont")
extrafont::font_import()   # 扫描系统字体（耗时较长，仅需一次）
extrafont::loadfonts()     # 加载字体到 R 会话

# 然后在 theme_pub() 中使用
theme_pub(base_family = "Arial")
```

> **注意：** `font_import()` 首次运行会扫描整个系统字体目录，可能需要几分钟。后续会话只需 `loadfonts()` 即可。在 Linux 上如果系统未安装 Arial，需先通过包管理器安装（如 `apt install ttf-mscorefonts-installer`）。

---

## 1.4 显著性标注规则

### p 值格式化

```r
format_pval <- function(p) {
  case_when(
    p < 0.001 ~ "italic(p) < 0.001",
    p < 0.01  ~ sprintf("italic(p) == %.3f", p),
    TRUE      ~ sprintf("italic(p) == %.3f", p)
  )
}
```

### 标注位置动态计算

```r
# 计算 y 轴范围，自动留空
y_range <- max(data$value, na.rm = TRUE) - min(data$value, na.rm = TRUE)
y_max <- max(data$value, na.rm = TRUE) + y_range * 0.1  # 留 10% 空白
y_step <- y_range * 0.08  # 多组比较时阶梯间距

# 使用 ggsignif（当需要显式标注比较时）
geom_signif(
  comparisons = list(c("Group1", "Group2")),
  map_signif_level = format_pval,
  test = "t.test",
  textsize = 3.5,
  parse = TRUE,
  y_position = y_max + seq(0, by = y_step, length.out = n_comparisons)
)
```

### 标注规则

- p < 0.001 写为 `p < 0.001`，不要写具体值
- p ≥ 0.001 写为 `p = 0.XXX`
- 仅标注主要比较，不要对每个子组对比都加星号
- 若比较 > 5 对，考虑用表格替代图中标注

---

## 1.5 比例指标的置信区间（Wilson Score）

用于敏感度、特异度、患病率等比例指标的 CI 计算。（优于正态近似法，尤其样本量较小时。）

```r
wilson_ci <- function(p, n, z_alpha = 1.96) {
  denominator <- 1 + z_alpha^2 / n
  centre <- (p + z_alpha^2 / (2 * n)) / denominator
  margin <- z_alpha * sqrt(p * (1 - p) / n + z_alpha^2 / (4 * n^2)) / denominator
  c(lower = centre - margin, upper = centre + margin)
}
```

**何时必须使用：** ROC 分析中的敏感度/特异度 CI、任何比例指标的置信区间。

---

## 1.6 拼图布局规范

```r
library(patchwork)

# 多图组合
combined <- wrap_plots(plot_list, ncol = 3) +
  plot_annotation(tag_levels = "A") &
  theme(legend.position = "bottom")
```

### 规范

- 使用 `wrap_plots()` 而非 `grid.arrange()`（自动对齐）
- `tag_levels = "A"` 生成 A/B/C 标签
- `&` 统一所有子图的图例位置
- 同一主题的多张子图共享统一配色

---

## 1.7 目录先行规则

**所有生成输出文件的 R 代码必须在使用路径前确保目录存在。**

```r
# 正确：写入前创建目录
dir.create("04_Outputs/01_BaselineTable", recursive = TRUE, showWarnings = FALSE)
ggsave("04_Outputs/01_BaselineTable/Table1.png", p, dpi = PUBLICATION_DPI)

# 错误：假设目录已存在（会因路径不存在而报错）
ggsave("04_Outputs/01_BaselineTable/Table1.png", p, dpi = PUBLICATION_DPI)  # 可能失败
```

### 目录创建规范

| 输出类型 | 创建模式 | 示例 |
|---------|---------|------|
| `04_Outputs/XX_MethodName/` | 每次 script 运行时创建 | `dir.create("04_Outputs/02_GroupComparison", recursive = TRUE, showWarnings = FALSE)` |
| `03_AnalysisMethods/XX_MethodName/` | 每次 script 运行时创建 | 同上 |
| 方法说明 文件 | 作为最后一步写入 | `writeLines(readme, "03_AnalysisMethods/XX_MethodName/方法说明.md")` |

- 使用 `recursive = TRUE` 确保父目录自动创建
- 使用 `showWarnings = FALSE` 避免目录已存在时的警告
- **不在 script 外假设目录已存在**

---

# 第二部分：Analysis Patterns（按需选用的分析模式）

以下代码模式针对特定分析方法。**仅在对应方法被确认需要时使用。** 每种模式标注了适用条件和（更重要的）不适用条件。

---

## 2.1 三层绘图法（箱线图 + 散点叠加）

### 意图
既展示数据分布的整体概览（箱线图），又展示每个个体的具体数值（散点），避免箱线图掩盖数据特征。

### 模式
```r
ggplot(data, aes(x = group, y = value)) +
  geom_jitter(aes(fill = group), color = alpha("gray50", 0.4),
              shape = 21, width = 0.2, size = 2) +
  geom_boxplot(aes(fill = group), alpha = 0.0, color = "black",
               outlier.shape = NA, width = 0.5)
```

### 适用条件
- 组间比较，且样本量 < 200
- 需要展示个体变异时

### 不适用条件
- 样本量 ≥ 200：仅用箱线图或小提琴图，省略散点
- 分组数 > 6：改用小提琴图 + 简明箱线图

### 变体
- 小提琴图替代箱线图：`geom_violin(alpha = 0.3)` + `geom_boxplot(width = 0.1)`

---

## 2.2 Z-score 标准化可视化

### 意图
将不同量纲的变量统一到同一尺度上进行可视化比较。

### 模式
```r
scale_this <- function(x) {
  (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)
}
```

### 适用条件
- 同一图中展示多个不同量纲的变量（如将 IL-6、CRP、TNF-α 放在一起比较）
- 热图中统一色标范围
- 比较不同标志物在组间的相对差异倍数

### ⚠️ 不适用条件（重要）
- 变量单位一致或天然可比（如多个血压指标，单位均为 mmHg）—— 标准化会丢失原始尺度信息
- 需要报告原始单位以保持临床可解释性（如 "BMI 每增加 1 kg/m² 的风险"）
- 仅展示单个变量时 —— 不需要标准化
- 受众为临床医生时优先保留原始值

---

## 2.3 ROC 分析双模式

### 意图
区分"仅标志物"（Unadjusted）和"调整协变量后"（Adjusted）的区分能力。

### 模式
```r
# Unadjusted：直接基于标志物值
library(pROC)
roc_obj <- roc(outcome ~ biomarker, data = df)
auc_obj <- auc(roc_obj)
ci_obj <- ci.auc(roc_obj)

# Adjusted：先做 Logistic 回归，用预测概率做 ROC
model <- glm(Outcome ~ biomarker + age + sex, data = df, family = binomial)
pred_prob <- predict(model, type = "response")
roc_adjusted <- roc(df$Outcome, pred_prob)

# 最佳阈值选取
coords_best <- coords(roc_obj, "best",
  ret = c("threshold", "sensitivity", "specificity",
          "ppv", "npv", "accuracy"))
```

### 适用条件
- 生物标志物诊断价值评估
- 需要对比"单纯标志物" vs "综合模型"的 AUC
- 需要报告最佳阈值和对应的诊断性能

---

## 2.4 LASSO 特征选择流程

### 意图
从高维生物标志物中筛选最具有区分能力的特征子集。

### 模式
```r
library(glmnet)
cv_model <- cv.glmnet(X_train, Y_train, family = "binomial", alpha = 1)
best_lambda <- cv_model$lambda.min

final_model <- glmnet(X_train, Y_train, family = "binomial", alpha = 1,
                      lambda = best_lambda)

coef_matrix <- as.matrix(coef(final_model))
non_zero_coefs <- coef_matrix[coef_matrix[, 1] != 0 &
                                rownames(coef_matrix) != "(Intercept)", , drop = FALSE]
```

### 关键细节
- 训练集/验证集分割先行，避免数据泄露
- `lambda.min` 是最小交叉验证误差，`lambda.1se` 更保守（选入更少变量）
- 提取的特征用于下游建模，而非直接解释系数大小

---

## 2.5 混淆矩阵热图

### 意图
直观展示分类结果的混淆情况，同时显示频数和百分比。

### 模式
```r
ggplot(cm_df, aes(x = Actual, y = Predicted)) +
  geom_tile(aes(fill = Freq), color = "white", linewidth = 1) +
  geom_text(aes(label = sprintf("%d\n(%.1f%%)", Freq, Percent)),
            size = 4, fontface = "bold") +
  scale_fill_gradient(low = "white", high = "steelblue") +
  coord_fixed()
```

### 适用条件
- 分类模型性能展示
- ROC 分析中阈值确定后的分类结果
- 训练集 vs 验证集对比

---

## 2.6 森林图（AUC/OR/HR 汇总）

### 意图
在一个图中汇总多个指标的效应量和置信区间。

### 模式
```r
ggplot(df, aes(x = estimate, y = reorder(label, estimate))) +
  geom_point(size = 4, color = "steelblue") +
  geom_errorbarh(aes(xmin = lower, xmax = upper),
                 height = 0.2, color = "steelblue") +
  geom_vline(xintercept = reference, linetype = "dashed", color = "red") +
  labs(x = "AUC (95% CI)", y = "")
```

### 适用条件
- 多标志物 AUC 汇总
- 亚组分析结果汇总
- 多因素回归结果可视化

---

## 2.7 风险分层 jitter plot

### 意图
展示每个个体的预测概率，按真实结局分组，便于目测模型分离效果。

### 模式
```r
ggplot(df, aes(x = jitter(as.numeric(factor(outcome)), amount = 0.1),
               y = predicted_prob, color = as.factor(outcome))) +
  geom_jitter(size = 2.5, alpha = 0.7, width = 0.15) +
  geom_hline(yintercept = cutoff, linetype = "dashed", color = "red") +
  scale_color_manual(values = c("steelblue", "coral")) +
  labs(x = "Actual Group", y = "Predicted Probability")
```

### 适用条件
- 展示模型预测概率在两组间的分布
- 验证集上展示分类效果

---

## 2.8 训练集/验证集分割模式

### 意图
从数据中识别训练集和验证集（当 TYPE 列存在时），fallback 到随机分割。

### 模式
```r
train_set <- df %>%
  filter(grepl("TRAIN|TRANNING", toupper(.data[[type_col]])))
validation_set <- df %>%
  filter(grepl("VAL|VALIDATION", toupper(.data[[type_col]])))

# fallback：随机 70/30 分割（当无 TYPE 列时）
if (nrow(train_set) == 0 || nrow(validation_set) == 0) {
  set.seed(42)
  train_idx <- sample(1:nrow(df), size = round(0.7 * nrow(df)))
  train_set <- df[train_idx, ]
  validation_set <- df[-train_idx, ]
}
```

### 注意
- 容错匹配（大小写不敏感，支持缩写）
- 随机分割必须设 `set.seed()` 并记录种子值
- 分割信息写入 方法说明

---

## 2.9 KM 生存曲线美化

### 意图
展示生存函数随时间的变化，比较两组或多组的生存率差异。生存分析（§3.4）的标准可视化输出。

### 模式
```r
library(survival)
library(survminer)

fit <- survfit(Surv(time, event) ~ group, data = df)

ggsurvplot(fit, data = df,
  pval = TRUE, pval.method = TRUE,
  risk.table = TRUE, risk.table.col = "strata",
  palette = c("#0072B5", "#BC3C29"),  # Nature 双色，色盲友好
  xlab = "Time (months)", ylab = "Survival probability",
  legend.title = "Group",
  ggtheme = theme_pub())
```

### 适用条件
- 时间-事件数据（生存时间 + 事件状态）
- 两组或多组生存率比较
- 需要同时展示风险表（number at risk）

### 不适用条件
- 非生存数据（连续结局用箱线图/散点图）
- 仅关注终点事件发生率而非时间过程（用 Logistic 回归 + 柱状图）
- 样本量极小（<10 per group）时 KM 曲线不稳定，需谨慎解读

---

## 2.10 相关性矩阵热图

### 意图
展示多个连续变量间的相关性结构，快速识别强关联变量对，辅助回归建模的变量筛选。

### 模式
```r
library(ggcorrplot)

corr_matrix <- cor(data, method = "spearman", use = "pairwise.complete.obs")
ggcorrplot(corr_matrix,
  type = "lower",
  lab = TRUE, lab_size = 3,
  colors = c("#0072B5", "white", "#BC3C29"),  # 蓝白红三色
  ggtheme = theme_pub())
```

### 方法选择
- **Spearman**（默认）：适用于偏态分布或有序变量，不需要正态性假设
- **Pearson**：仅当所有变量均满足正态分布时使用

### 适用条件
- 多变量关联探索（≥3 个连续变量）
- 回归建模前的变量筛选（识别多重共线性）
- 展示相关系数的方向和强度

### 不适用条件
- 仅两个变量：用散点图更直观（可叠加回归线和 CI）
- 分类变量间的关联：用卡方检验或 mosaic plot
- 因果推断需要：相关不等于因果

---

## 2.11 CONSORT 流程图

### 意图
RCT 受试者筛选、随机化、干预和随访各阶段的人数与脱落原因可视化。CONSORT 声明的必备图表。

### 模式
```r
library(consort)

# 构建 CONSORT 图
g <- consort_plot(
  screening   = "Screened\nn = 320",
  randomized  = "Randomized\nn = 200",
  allocation  = list(
    "Treatment A\nn = 100",
    "Treatment B\nn = 100"
  ),
  follow_up   = list(
    "Completed\nn = 88",
    "Completed\nn = 91"
  ),
  analysis    = list(
    "ITT analysis\nn = 100",
    "ITT analysis\nn = 100"
  ),
  side_boxes  = list(
    "Excluded (n = 120):\n  Not meeting criteria (n = 85)\n  Declined (n = 25)\n  Other (n = 10)",
    "Lost to follow-up (n = 12)",
    "Lost to follow-up (n = 9)",
    "Discontinued (n = 5)",
    "Discontinued (n = 3)"
  ),
  cex         = 0.8
)

# 保存
ggsave("CONSORT_flow.tiff", g, width = 10, height = 8, dpi = PUBLICATION_DPI, compression = "lzw")
```

### 适用条件
- RCT 研究设计
- 需要展示受试者流程的 CONSORT 声明要求

### 不适用条件
- 观察性研究（改用 STROBE 流程图，可用 `DiagrammeR` 自定义）
- 回顾性研究（无需 CONSORT 图）

---

## 2.12 Love Plot（PSM 平衡诊断）

### 意图
展示倾向性评分匹配/加权前后协变量标准化均值差（SMD）的变化，判断平衡是否达标（|SMD| < 0.1）。

### 模式
```r
library(cobalt)

# 匹配前平衡
bal_before <- bal.tab(
  treatment ~ age + sex + bmi + education + comorbidity_score,
  data = data,
  stats = "mmd"
)

# 匹配后平衡（MatchIt 输出）
library(MatchIt)
m_out <- matchit(treatment ~ age + sex + bmi + education + comorbidity_score,
                 data = data, method = "nearest", ratio = 1)
bal_after <- bal.tab(m_out, stats = "mmd")

# Love Plot
love.plot(bal_after,
  threshold = 0.1,
  stars = "raw",
  colors = c("gray70", "#0072B5"),
  shapes = c(16, 17),
  ggtheme = theme_pub()) +
  labs(title = "Covariate Balance Before and After PSM")
```

### 适用条件
- 倾向性评分匹配（PSM）或逆概率加权（IPTW）后
- 需要证明匹配/加权成功改善协变量平衡

### 不适用条件
- 无倾向性评分分析时
- RCT 研究（随机化已保证平衡）

---

## 2.13 剂量反应 / RCS 曲线

### 意图
用限制性立方样条（Restricted Cubic Splines）展示连续暴露变量与结局的非线性剂量反应关系。

### 模式
```r
library(rms)
library(ggplot2)

# 拟合 RCS 模型
dd <- datadist(data)
options(datadist = "dd")

# 连续结局（线性回归）
fit_ols <- ols(outcome ~ rcs(exposure, 4) + age + sex, data = data)
anova(fit_ols)  # 检验非线性 P 值

# 二分类结局（Logistic 回归）
fit_glm <- lrm(outcome ~ rcs(exposure, 4) + age + sex, data = data)

# 可视化 RCS 曲线
p <- Predict(fit_ols, exposure, fun = function(x) x,
             ref.zero = FALSE)
plot(p, xlab = "Exposure (units)", ylab = "Adjusted outcome",
     col = "#0072B5", lwd = 2)
# 或用 ggplot2:
ggplot(data = p, aes(exposure, yhat)) +
  geom_ribbon(aes(ymin = lower, ymax = upper), fill = "#0072B5", alpha = 0.2) +
  geom_line(color = "#0072B5", linewidth = 1) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray50") +
  labs(x = "Exposure", y = "Adjusted effect (95% CI)",
       title = "Non-linear dose-response relationship") +
  theme_pub()
```

### 适用条件
- 连续暴露变量（如 BMI、血压、生物标志物浓度）
- 疑似非线性剂量反应关系
- 探索性分析或主分析的补充

### 不适用条件
- 暴露已二分类化（丢失连续信息）
- 样本量过小（< 100）时 RCS 不稳定

---

## 2.14 瀑布图（Waterfall Plot）

### 意图
展示每个受试者对治疗的最佳反应（如肿瘤缩小百分比），常用于肿瘤疗效评估（RECIST 标准）。

### 模式
```r
# 数据准备：每人一行，包含最佳变化百分比
df <- data.frame(
  patient_id = 1:40,
  best_change = runif(40, -100, 50),  # 负值=缩小，正值=增大
  group = rep(c("Treatment", "Control"), each = 20)
)

# 按变化幅度排序
df <- df[order(df$best_change), ]
df$patient_id <- factor(df$patient_id, levels = df$patient_id)

# 反应分类
response_threshold <- -30   # PR: ≥ 30% 缩小
progression_threshold <- 20 # PD: ≥ 20% 增大

p <- ggplot(df, aes(x = patient_id, y = best_change, fill = group)) +
  geom_bar(stat = "identity", width = 0.8) +
  geom_hline(yintercept = 0, color = "black", linewidth = 0.5) +
  geom_hline(yintercept = response_threshold,
             linetype = "dashed", color = "#0072B5") +
  geom_hline(yintercept = progression_threshold,
             linetype = "dashed", color = "#BC3C29") +
  scale_fill_manual(values = c("#0072B5", "#BC3C29")) +
  labs(x = "", y = "Best % change from baseline",
       title = "Waterfall plot of best tumor response") +
  theme_pub() +
  theme(axis.text.x = element_blank(),
        legend.position = "top")
```

### 适用条件
- 肿瘤疗效反应评估（RECIST / iRECIST）
- 每个受试者的最佳变化百分比可视化

### 不适用条件
- 非肿瘤疗效研究（改用配对连线图）
- 仅展示组均值时（用箱线图）

---

## 2.15 漏斗图（Funnel Plot）

### 意图
Meta 分析中检测发表偏倚，判断小样本研究是否偏向阳性结果。

### 模式
```r
library(meta)
library(ggplot2)

# Meta 分析模型
m <- metagen(TE, seTE, data = meta_data, sm = "OR", method.tau = "REML")

# 基础漏斗图（base R）
funnel(m, pch = 16, col = "#0072B5",
       studlab = TRUE, xlab = "Effect size (log OR)")

# ggplot2 版本
funnel_data <- data.frame(
  effect = m$TE,
  se     = m$seTE,
  study  = m$studlab
)

p <- ggplot(funnel_data, aes(x = effect, y = se)) +
  geom_point(size = 3, color = "#0072B5", alpha = 0.7) +
  geom_vline(xintercept = m$TE.random, linetype = "dashed", color = "red") +
  geom_segment(
    aes(x = m$TE.random - 1.96 * se, xend = m$TE.random + 1.96 * se,
        y = se, yend = se),
    data = data.frame(se = seq(0.05, max(funnel_data$se), length.out = 100)),
    color = "gray70", alpha = 0.5
  ) +
  scale_y_reverse() +
  labs(x = "Effect size (log OR)", y = "Standard error",
       title = "Funnel plot for publication bias") +
  theme_pub()

# Egger 检验（统计检测）
metabias(m, method = "Egger", plotit = FALSE)
```

### 适用条件
- Meta 分析发表偏倚检测
- 研究数量 ≥ 10（少于 10 时漏斗图无法可靠判断）

### 不适用条件
- 研究数量 < 10
- 非 Meta 分析场景

---

## 2.16 UpSet / Venn 图

### 意图
展示多个集合的交叉关系，如共病模式、药物联用、多标志物共现等。UpSet 图在集合数 > 3 时优于 Venn 图。

### 模式
```r
library(ComplexUpset)

# 数据准备：每行一个受试者，每列一个条件（0/1）
conditions <- c("Hypertension", "Diabetes", "Obesity", "Dyslipidemia", "Smoking")

# UpSet 图
upset(data, conditions,
  base_annotations = list(
    "Intersection size" = intersection_size(
      counts = TRUE,
      text = list(size = 3)
    )
  ),
  set_sizes = upset_set_size(
    geom = geom_bar(fill = "#0072B5", width = 0.6)
  ),
  stripes = upset_stripes(
    geom = geom_segment(color = "gray90"),
    aes = aes(fill = "gray95")
  ),
  min_size = 5,
  width_ratio = 0.2,
  themes = upset_default_themes(theme_pub())
)
```

### 适用条件
- 多集合交叉关系可视化（≥ 3 个集合）
- 共病模式、药物联用、多标志物共现分析

### 不适用条件
- 仅 2 个集合（用简单条形图或表格即可）
- 集合数 > 10（图表过于复杂）

---

## 2.17 Sankey / Alluvial 图

### 意图
展示分类变量在不同时间点或条件下的变化流，如治疗反应转移、疾病状态转变。

### 模式
```r
library(ggalluvial)

# 数据准备：每人一行，包含基线和随访的分类状态
df <- data.frame(
  baseline = c("Remission", "Remission", "Active", "Active", "Active"),
  followup = c("Remission", "Active", "Active", "Remission", "Remission"),
  count = c(45, 12, 8, 18, 25)
)

p <- ggplot(df, aes(y = count, axis1 = baseline, axis2 = followup)) +
  geom_alluvium(aes(fill = baseline), width = 0.3, alpha = 0.7) +
  geom_stratum(width = 0.3, fill = "white", color = "black") +
  geom_text(stat = "stratum", aes(label = afterglow(stratum)), size = 3) +
  scale_fill_manual(values = c("#0072B5", "#BC3C29", "#009E73")) +
  labs(x = "", y = "Number of patients",
       title = "Treatment response transition from baseline to follow-up") +
  theme_pub() +
  theme(legend.position = "top")
```

### 适用条件
- 分类状态在两个或多个时间点的变化流
- 治疗反应转移、疾病分期变化、诊断重分类

### 不适用条件
- 连续变量变化（用配对连线图或斜率图）
- 状态类别 > 6（图表过于复杂）

---

## 2.18 配对连线图

### 意图
展示纵向设计中每个受试者的个体轨迹（前后比较），直观呈现组内变化和组间差异。

### 模式
```r
library(ggplot2)

# 数据准备：长格式，每人多行
# df: id, time, value, group
p <- ggplot(df, aes(x = time, y = value, group = id, color = group)) +
  geom_line(alpha = 0.3, linewidth = 0.8) +
  geom_point(size = 2, alpha = 0.6) +
  # 叠加组均值趋势（粗线）
  stat_summary(aes(group = group), fun = mean,
               geom = "line", linewidth = 1.5, color = "black") +
  stat_summary(aes(group = group), fun = mean,
               geom = "point", size = 4, shape = 18, color = "black") +
  scale_color_manual(values = c("#0072B5", "#BC3C29")) +
  labs(x = "Time point", y = "Outcome value",
       title = "Individual trajectories with group means") +
  theme_pub() +
  theme(legend.position = "top")

# 简化版：仅前后配对（2 个时间点）
p_simple <- ggplot(df_wide, aes(x = 1, y = pre_value)) +
  geom_segment(aes(xend = 2, yend = post_value, color = group),
               alpha = 0.4, linewidth = 0.8) +
  geom_point(aes(color = group), size = 3) +
  geom_point(aes(x = 2, y = post_value, color = group), size = 3) +
  scale_color_manual(values = c("#0072B5", "#BC3C29")) +
  scale_x_continuous(breaks = c(1, 2), labels = c("Pre", "Post")) +
  labs(x = "", y = "Outcome value",
       title = "Paired pre-post comparison") +
  theme_pub() +
  theme(legend.position = "top")
```

### 适用条件
- 纵向/配对设计，样本量 < 100
- 展示个体轨迹和组均值趋势
- 前后比较的干预效果可视化

### 不适用条件
- 样本量 ≥ 100（线条过于密集，改用均值±CI 趋势图）
- 仅 2 时间点且样本量大（改用配对差异的分布图）

---

## 2.19 日历 / 趋势图

### 意图
展示某指标随时间的变化趋势，如患病率时间趋势、入院率变化、治疗方案转变等。

### 模式
```r
library(ggplot2)

# 数据准备：每行一个时间点 + 汇总指标
df <- data.frame(
  year = 2010:2024,
  prevalence = c(12.3, 12.8, 13.1, 13.5, 14.0, 14.2, 14.8, 15.1,
                 15.5, 15.9, 16.3, 16.0, 16.5, 17.1, 17.5),
  lower = c(11.5, 12.0, 12.3, 12.7, 13.2, 13.4, 14.0, 14.3,
            14.7, 15.1, 15.5, 15.2, 15.7, 16.3, 16.7),
  upper = c(13.1, 13.6, 13.9, 14.3, 14.8, 15.0, 15.6, 15.9,
            16.3, 16.7, 17.1, 16.8, 17.3, 17.9, 18.3)
)

p <- ggplot(df, aes(x = year, y = prevalence)) +
  geom_ribbon(aes(ymin = lower, ymax = upper), fill = "#0072B5", alpha = 0.2) +
  geom_line(color = "#0072B5", linewidth = 1.2) +
  geom_point(size = 3, color = "#0072B5") +
  # 可选：添加趋势线
  geom_smooth(method = "lm", se = FALSE, linetype = "dashed",
              color = "#BC3C29", linewidth = 0.8) +
  scale_x_continuous(breaks = seq(2010, 2024, 2)) +
  labs(x = "Year", y = "Prevalence (%)",
       title = "Temporal trend of prevalence (95% CI)") +
  theme_pub()
```

### 适用条件
- 时间趋势分析（患病率、发病率、死亡率、入院率等）
- 多时点数据的纵向趋势可视化
- 需要展示置信区间的趋势变化

### 不适用条件
- 仅 2 个时间点（用配对比较或差异图）
- 非时间序列数据
