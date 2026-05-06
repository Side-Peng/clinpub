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
theme_pub <- function(base_size = 14) {
  theme_minimal(base_size = base_size) %+replace%
    theme(
      legend.position = "none",
      plot.title = element_text(hjust = 0.5, size = rel(1.2), face = "bold"),
      axis.title = element_text(size = rel(1), face = "bold"),
      axis.text = element_text(size = rel(1), face = "bold"),
      panel.grid = element_blank(),
      panel.border = element_rect(color = "black", fill = NA, linewidth = 1),
      axis.ticks = element_line(color = "black"),
      strip.background = element_rect(fill = "grey95", color = "black"),
      strip.text = element_text(face = "bold")
    )
}
```

**应用方式：** `+ theme_pub()`。如需图例，覆盖 `legend.position`。

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

所有输出必须 **≥300 DPI**，**Arial ≥8pt**。

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
| README 文件 | 作为最后一步写入 | `writeLines(readme, "03_AnalysisMethods/XX_MethodName/README.md")` |

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
- 分割信息写入 README
