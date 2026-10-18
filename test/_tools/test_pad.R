source("04_Outputs/_figure_config.R")
suppressPackageStartupMessages(library(ggplot2))
d <- read.csv("02_PreprocessedData/data/cleaned.csv", fileEncoding = "UTF-8")
d$group <- factor(d$group, levels = c("Control", "Treatment"))
COL <- get_palette(2); names(COL) <- levels(d$group)

pa <- ggplot(d, aes(group, post_score)) +
  geom_jitter(aes(colour = group), width = 0.14, size = 0.55, alpha = 0.55) +
  geom_boxplot(aes(colour = group), width = 0.34, fill = NA, outlier.shape = NA,
               linewidth = 0.45) +
  scale_colour_manual(values = COL) +
  labs(x = NULL, y = "Symptom score") +
  theme_pub() + theme(legend.position = "none")

# 单独渲染（非 patchwork）
save_figure(pa, "figstyle/_test_single", width_mm = 89, height_mm = 80,
            formats = c("png"), dpi = 300)

cat("panel 边距：\n")
b <- ggplotGrob(pa)
cat("  plot.margin:", pa$theme$plot.margin$top, "\n")
cat("  axis.title.y margin r:", pa$theme$axis.title.y$margin[["r"]], "\n")
