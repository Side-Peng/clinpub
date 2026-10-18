# ============================================================
# 按新规范出图：**每个面板单独成文件**，不带 A/B 序号
# 用户自行在 PPT/AI 里拼图，所以这里只负责单面板的印刷质量。
# ============================================================

suppressPackageStartupMessages({
  library(ggplot2)
})

source("04_Outputs/_figure_config.R")

root <- normalizePath(".")
d <- read.csv(file.path(root, "02_PreprocessedData/data/cleaned.csv"),
              fileEncoding = "UTF-8", check.names = FALSE)
d$group <- factor(d$group, levels = c("Control", "Treatment"))

sens <- read.csv(file.path(root, "04_Outputs/04_SensitivityAnalysis/sensitivity.csv"),
                 fileEncoding = "UTF-8", check.names = FALSE)
sens$short <- c("Unadjusted", "Adjusted (primary)", "Wilcoxon", "MICE (n = 120)")
sens$short <- factor(sens$short, levels = rev(sens$short))

out <- file.path(root, "figstyle")
dir.create(out, recursive = TRUE, showWarnings = FALSE)

COL <- get_palette(2)
names(COL) <- levels(d$group)

# ---- 面板 1：组间分布（单栏 89 mm）--------------------------------------
p1 <- ggplot(d, aes(group, post_score)) +
  geom_jitter(aes(colour = group), width = 0.14, height = 0,
              size = 1.05, alpha = 0.55) +
  geom_boxplot(aes(colour = group), width = 0.32, fill = NA,
               outlier.shape = NA, linewidth = LW_DATA * 0.65) +
  stat_summary(fun = mean, geom = "point", shape = 18, size = 2.0,
               colour = pal("ink")) +
  scale_colour_manual(values = COL) +
  scale_y_continuous(limits = c(0, 100),
                     expand = expansion(mult = c(0.02, 0.04))) +
  labs(x = NULL, y = "Symptom score") +
  theme_pub(width_mm = FIG_WIDTH_MM[["single"]]) +
  theme(legend.position = "none")

save_figure(p1, file.path(out, "panel_distribution"),
            width_mm = FIG_WIDTH_MM[["single"]], height_mm = 82,
            formats = c("svg", "pdf", "tiff", "png"), dpi = 300)

# ---- 面板 2：稳健性森林图（单栏 89 mm）-----------------------------------
p2 <- ggplot(sens, aes(estimate, short)) +
  geom_vline(xintercept = 0, linetype = "22", linewidth = LW_REF,
             colour = pal("neutral")) +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high), orientation = "y",
                width = 0.12, linewidth = LW_DATA * 0.75, colour = pal("ink")) +
  geom_point(size = 2.0, colour = pal("main")) +
  scale_x_continuous(limits = c(-18.5, 2.5), breaks = c(-15, -10, -5, 0)) +
  labs(x = "Difference in symptom score (95% CI)", y = NULL) +
  theme_pub(width_mm = FIG_WIDTH_MM[["single"]]) +
  theme(axis.line.y = element_blank(), axis.ticks.y = element_blank(),
        plot.margin = margin(3, 5, 3, 10))   # 留出左侧长标签的空间

save_figure(p2, file.path(out, "panel_sensitivity"),
            width_mm = FIG_WIDTH_MM[["single"]], height_mm = 62,
            formats = c("svg", "pdf", "tiff", "png"), dpi = 300)

cat("\n  已生成单面板：\n")
for (f in list.files(out, pattern = "^panel_")) cat("   ", f, "\n")
