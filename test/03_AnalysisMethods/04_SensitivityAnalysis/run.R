# ============================================================
# Batch 2 / Method 04 — 敏感性分析
# 目的：检验主分析（完整病例 + 调整模型）的结论是否稳健
# 输入：cleaned.csv（N=102）、cleaned_with_missing.csv（N=120）
# 输出：04_Outputs/04_SensitivityAnalysis/{sensitivity.csv,
#        fig3_sensitivity_forest.{png,svg,tiff}, 方法说明.md}
# ============================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(ggplot2)
  library(mice)
})

source("04_Outputs/_figure_config.R")

root <- normalizePath(".")
clean <- read.csv(file.path(root, "02_PreprocessedData/data/cleaned.csv"),
                  fileEncoding = "UTF-8", check.names = FALSE)
full  <- read.csv(file.path(root, "02_PreprocessedData/data/cleaned_with_missing.csv"),
                  fileEncoding = "UTF-8", check.names = FALSE)

for (df_name in c("clean", "full")) {
  df <- get(df_name)
  df$group <- factor(df$group, levels = c("Control", "Treatment"))
  df$sex   <- factor(df$sex,   levels = c("Female", "Male"))
  df$comorbidity <- factor(df$comorbidity,
                           levels = c("None", "Hypertension", "Diabetes", "Both"))
  assign(df_name, df)
}

out_dir <- file.path(root, "04_Outputs/04_SensitivityAnalysis")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

rows <- list()
add <- function(...) rows[[length(rows) + 1]] <<- data.frame(..., stringsAsFactors = FALSE)

# ---- S1 未调整（完整病例） ----------------------------------------------
fit1 <- lm(post_score ~ group, data = clean)
ci1 <- confint(fit1)
add(approach = "Unadjusted (complete case)", n = nrow(clean),
    estimate = round(coef(fit1)["groupTreatment"], 2),
    ci_low = round(ci1["groupTreatment", 1], 2),
    ci_high = round(ci1["groupTreatment", 2], 2),
    p = signif(summary(fit1)$coefficients["groupTreatment", 4], 3))

# ---- S2 调整（完整病例，主分析） ----------------------------------------
fit2 <- lm(post_score ~ group + age + sex + bmi, data = clean)
ci2 <- confint(fit2)
add(approach = "Adjusted (complete case)", n = nrow(clean),
    estimate = round(coef(fit2)["groupTreatment"], 2),
    ci_low = round(ci2["groupTreatment", 1], 2),
    ci_high = round(ci2["groupTreatment", 2], 2),
    p = signif(summary(fit2)$coefficients["groupTreatment", 4], 3))

# ---- S3 非参数（Wilcoxon 秩和，完整病例） -------------------------------
# 注意：wilcox.test(y ~ g) 的位置差是"第一组 − 第二组"（Control − Treatment），
# 与其它方法（Treatment − Control）方向相反，这里统一取负号再报告。
wt <- wilcox.test(post_score ~ group, data = clean, conf.int = TRUE)
add(approach = "Wilcoxon rank-sum (complete case)", n = nrow(clean),
    estimate = round(-as.numeric(wt$estimate), 2),
    ci_low = round(-as.numeric(wt$conf.int[2]), 2),
    ci_high = round(-as.numeric(wt$conf.int[1]), 2),
    p = signif(wt$p.value, 3))

# ---- S4 MICE 多重插补（全部 120 例） ------------------------------------
imp_vars <- c("post_score", "group", "age", "sex", "bmi", "comorbidity")
imp <- mice(full[, imp_vars], m = 20, seed = 20261018,
            printFlag = FALSE, quiet = TRUE)
fit_imp <- with(imp, lm(post_score ~ group + age + sex + bmi))
pooled  <- summary(pool(fit_imp), conf.int = TRUE)
pooled$term <- gsub("^group", "", pooled$term)
row <- pooled[pooled$term == "Treatment", ]
add(approach = "MICE pooled (n = 120)", n = nrow(full),
    estimate = round(row$estimate, 2),
    ci_low = round(row[["2.5 %"]], 2),
    ci_high = round(row[["97.5 %"]], 2),
    p = signif(row$p.value, 3))

sens <- do.call(rbind, rows)
write.csv(sens, file.path(out_dir, "sensitivity.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")

cat("== 敏感性分析（Treatment − Control，post_score）==\n")
print(sens, row.names = FALSE)

# ---- 图 3：跨方法估计对比 ------------------------------------------------
sens$approach <- factor(sens$approach, levels = rev(sens$approach))

p <- ggplot(sens, aes(x = estimate, y = approach)) +
  geom_vline(xintercept = 0, linetype = "22", colour = pal("neutral"),
             linewidth = LW_REF) +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high),
                orientation = "y", width = 0.14,
                colour = "black", linewidth = LW_DATA * 0.65) +
  geom_point(size = 1.8, colour = pal("main")) +
  geom_text(aes(label = sprintf("%.2f", estimate)),
            vjust = -1.0, size = 2.2, fontface = "bold", colour = "black") +
  labs(x = "Difference in symptom score (95% CI)", y = NULL) +
  theme_pub(width_mm = FIG_WIDTH_MM[["single"]])

save_figure(p, file.path(out_dir, "fig3_sensitivity_forest"),
            width_mm = FIG_WIDTH_MM[["single"]], height_mm = 54)
cat("\n已写出 sensitivity.csv / fig3_sensitivity_forest.{png,svg,tiff}\n")
