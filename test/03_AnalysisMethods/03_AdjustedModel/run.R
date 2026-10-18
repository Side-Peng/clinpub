# ============================================================
# Batch 2 / Method 03 — 主分析：调整后的组间差异
# 主结局：post_score（连续）
# 目的：在 age / sex / bmi 调整下估计 Treatment − Control 的均值差
# 输入：02_PreprocessedData/data/cleaned.csv
# 输出：04_Outputs/03_AdjustedModel/{model_table.csv, diag.txt,
#        fig2_adjusted_effects.{png,svg,tiff}, 方法说明.md}
# ============================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
})

source("04_Outputs/_figure_config.R")

root <- normalizePath(".")
d <- read.csv(file.path(root, "02_PreprocessedData/data/cleaned.csv"),
              fileEncoding = "UTF-8", check.names = FALSE)
d$group <- factor(d$group, levels = c("Control", "Treatment"))
d$sex   <- factor(d$sex, levels = c("Female", "Male"))

out_dir <- file.path(root, "04_Outputs/03_AdjustedModel")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

# ---- 未调整 vs 调整 ------------------------------------------------------
fit_unadj <- lm(post_score ~ group, data = d)
fit_adj   <- lm(post_score ~ group + age + sex + bmi, data = d)

tidy_lm <- function(fit, label) {
  cf <- summary(fit)$coefficients
  ci <- confint(fit)
  data.frame(
    model   = label,
    term    = rownames(cf),
    estimate = round(cf[, 1], 2),
    ci_low   = round(ci[, 1], 2),
    ci_high  = round(ci[, 2], 2),
    p        = signif(cf[, 4], 3),
    stringsAsFactors = FALSE
  )
}

tab <- rbind(tidy_lm(fit_unadj, "Unadjusted"),
             tidy_lm(fit_adj,   "Adjusted"))

# 标准化系数（调整模型）便于比较协变量相对重要性
sd_y <- sd(d$post_score)
adj_terms <- c("groupTreatment", "age", "sexMale", "bmi")
std <- data.frame(
  model = "Adjusted (std. beta)",
  term = adj_terms,
  estimate = round(coef(fit_adj)[adj_terms] * c(
    sd(d$group == "Treatment"), sd(d$age), sd(d$sex == "Male"), sd(d$bmi)
  ) / sd_y, 3),
  ci_low = NA, ci_high = NA, p = NA,
  stringsAsFactors = FALSE
)
tab <- rbind(tab, std)

write.csv(tab, file.path(out_dir, "model_table.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")

cat("== 模型结果 ==\n")
print(tab[tab$model == "Adjusted", ], row.names = FALSE)

# ---- 模型诊断 ------------------------------------------------------------
sink(file.path(out_dir, "diag.txt"))
cat("== 调整模型诊断 ==\n")
cat(sprintf("R 版本: %s\n\n", R.version.string))
cat("残差正态性 (Shapiro):\n"); print(shapiro.test(residuals(fit_adj)))
cat("\n残差同方差 (Breusch-Pagan 近似：残差与拟合值相关):\n")
print(cor.test(fitted(fit_adj), abs(residuals(fit_adj))))
cat("\n方差膨胀因子 (VIF):\n")
vif <- sapply(c("group", "age", "sex", "bmi"), function(v) {
  f2 <- as.formula(paste("post_score ~", paste(setdiff(c("group", "age", "sex", "bmi"), v), collapse = " + ")))
  1 / (1 - summary(lm(f2, data = d))$r.squared)
})
print(round(vif, 3))
cat("\n影响点 (Cook's D > 4/n):\n")
cd <- cooks.distance(fit_adj)
cat(sprintf("  阈值 %.4f，超阈值 %d 例\n", 4 / nrow(d), sum(cd > 4 / nrow(d))))
cat("\n模型摘要:\n"); print(summary(fit_adj))
sink()

cat("\n== 诊断摘要 ==\n")
cat(sprintf("  Shapiro p = %.3f\n", shapiro.test(residuals(fit_adj))$p.value))
cat(sprintf("  VIF: %s\n", paste(sprintf("%s=%.2f", names(vif), vif), collapse = ", ")))
cat(sprintf("  Cook's D 超阈值: %d 例\n", sum(cd > 4 / nrow(d))))

# ---- 图 2：效应量森林图 --------------------------------------------------
plot_df <- tab %>%
  filter(term %in% c("groupTreatment", "age", "sexMale", "bmi"),
         model == "Adjusted") %>%
  mutate(term_label = recode(term,
    groupTreatment = "Treatment vs Control",
    age            = "Age (per year)",
    sexMale        = "Male vs Female",
    bmi            = "BMI (per kg/m2)"
  ),
  term_label = factor(term_label, levels = rev(c(
    "Treatment vs Control", "Age (per year)", "Male vs Female", "BMI (per kg/m2)"))))

p <- ggplot(plot_df, aes(x = estimate, y = term_label)) +
  geom_vline(xintercept = 0, linetype = "22", colour = pal("neutral"),
             linewidth = LW_REF) +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high),
                orientation = "y", width = 0.14, colour = "black",
                linewidth = LW_DATA * 0.65) +
  geom_point(size = 1.8, colour = pal("main")) +
  labs(x = "Adjusted mean difference in symptom score (95% CI)", y = NULL) +
  theme_pub(width_mm = FIG_WIDTH_MM[["single"]])

save_figure(p, file.path(out_dir, "fig2_adjusted_effects"),
            width_mm = FIG_WIDTH_MM[["single"]], height_mm = 52)
cat("\n已写出 model_table.csv / diag.txt / fig2_adjusted_effects.{png,svg,tiff}\n")
