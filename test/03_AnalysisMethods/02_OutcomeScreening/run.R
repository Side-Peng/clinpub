# ============================================================
# Batch 1 / Method 02 — 结局候选筛选
# 目的：在未预设主要结局时，评估哪个候选变量可支撑主分析
# 输入：02_PreprocessedData/data/cleaned.csv
# 输出：04_Outputs/02_OutcomeScreening/{outcome_screening.csv,
#        fig1_candidates_by_group.{png,svg,tiff}, fig2_correlation.{png,svg,tiff},
#        方法说明.md}
# ============================================================

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(patchwork)
})

source("04_Outputs/_figure_config.R")

root <- normalizePath(".")
d <- read.csv(file.path(root, "02_PreprocessedData/data/cleaned.csv"),
              fileEncoding = "UTF-8", check.names = FALSE)
d$group <- factor(d$group, levels = c("Control", "Treatment"))

out_dir <- file.path(root, "04_Outputs/02_OutcomeScreening")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

cand <- c("baseline_score", "post_score", "egfr")

# ---- 组间比较：均值差 + 95%CI + Cohen's d --------------------------------
res <- lapply(cand, function(v) {
  x <- d[[v]]; g <- d$group
  a <- x[g == "Control"]; b <- x[g == "Treatment"]
  tt <- t.test(b, a)                      # Treatment - Control
  sp <- sqrt((var(a) + var(b)) / 2)
  dd <- (mean(b) - mean(a)) / sp
  sh_p <- tryCatch(shapiro.test(x)$p.value, error = function(e) NA_real_)
  data.frame(
    candidate   = v,
    control_m   = round(mean(a), 2),
    treatment_m = round(mean(b), 2),
    diff        = round(mean(b) - mean(a), 2),
    ci_low      = round(tt$conf.int[1], 2),
    ci_high     = round(tt$conf.int[2], 2),
    cohens_d    = round(dd, 2),
    p           = signif(tt$p.value, 3),
    shapiro_p   = signif(sh_p, 3),
    stringsAsFactors = FALSE
  )
})
scr <- do.call(rbind, res)

# 分类候选：comorbidity
tb <- table(d$comorbidity, d$group)
chi <- suppressWarnings(chisq.test(tb))
n <- sum(tb)
cramers_v <- sqrt(as.numeric(chi$statistic) / (n * (min(dim(tb)) - 1)))
cat_row <- data.frame(
  candidate = "comorbidity", control_m = NA, treatment_m = NA,
  diff = round(cramers_v, 3), ci_low = NA, ci_high = NA,
  cohens_d = NA, p = signif(chi$p.value, 3),
  shapiro_p = NA, stringsAsFactors = FALSE
)
scr <- rbind(scr, cat_row)

write.csv(scr, file.path(out_dir, "outcome_screening.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")

cat("== 结局候选筛选（Treatment - Control）==\n")
print(scr, row.names = FALSE)
cat("\n注：comorbidity 行的 diff 列是 Cramer's V，不是均值差。\n")

# ---- 图 1：三个候选的组间分布 -------------------------------------------
long <- d %>%
  select(all_of(cand), group) %>%
  pivot_longer(cols = all_of(cand), names_to = "variable", values_to = "value") %>%
  mutate(variable = factor(variable, levels = cand))   # 保持候选顺序，不按字母排

COL2 <- get_palette(2)
names(COL2) <- levels(long$group)

p1 <- ggplot(long, aes(x = group, y = value)) +
  geom_jitter(aes(colour = group), width = 0.14, height = 0,
              size = 1.05, alpha = 0.55) +
  geom_boxplot(aes(colour = group), width = 0.30, fill = NA,
               outlier.shape = NA, linewidth = LW_DATA * 0.65,
               fatten = 2.2) +
  facet_wrap(~ variable, scales = "free_y", nrow = 1) +
  scale_colour_manual(values = COL2) +
  labs(x = NULL, y = "Value") +
  theme_pub(width_mm = FIG_WIDTH_MM[["double"]]) +
  theme(legend.position = "none")

# ---- 图 2：相关矩阵 ------------------------------------------------------
num <- d %>% select(age, bmi, baseline_score, post_score, egfr)
cormat <- cor(num, use = "complete.obs", method = "pearson")
cm <- as.data.frame(as.table(cormat))
names(cm) <- c("var1", "var2", "r")

p2 <- ggplot(cm, aes(x = var1, y = var2, fill = r)) +
  geom_tile(colour = "white", linewidth = 0.6) +
  geom_text(aes(label = sprintf("%.2f", r)), size = 2.2, colour = "black",
            fontface = "bold") +
  get_diverging_scale(midpoint = 0) +
  coord_equal() +
  labs(x = NULL, y = NULL, fill = "r") +
  theme_pub(width_mm = FIG_WIDTH_MM[["double"]]) +
  theme(axis.text.x = element_text(angle = 30, hjust = 1))

fig <- p1 / p2 + plot_layout(heights = c(1, 1.15))

save_path <- file.path(out_dir, "fig1_candidates_by_group")
save_figure(fig, save_path,
            width_mm = FIG_WIDTH_MM[["double"]], height_mm = 150)

cat(sprintf("\n已写出：\n  %s\n  %s.{png,svg,tiff}\n",
            file.path(out_dir, "outcome_screening.csv"), save_path))
