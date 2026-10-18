# ============================================================
# 同一张图 × 4 个风格包，用于挑选默认风格
# 每个包只改「风格」，数据、几何、标签完全一致。
# 预览用 png；正式导出走 save_figure 默认（pdf+svg）。
# ============================================================

suppressPackageStartupMessages({
  library(ggplot2)
})

source("04_Outputs/_figure_config.R")

root <- normalizePath(".")
d <- read.csv(file.path(root, "02_PreprocessedData/data/cleaned.csv"),
              fileEncoding = "UTF-8", check.names = FALSE)
d$group <- factor(d$group, levels = c("Control", "Treatment"))

out <- file.path(root, "figstyle")
dir.create(out, recursive = TRUE, showWarnings = FALSE)

build_panel <- function() {
  COL <- get_palette(2)
  names(COL) <- levels(d$group)
  ggplot(d, aes(group, post_score)) +
    geom_jitter(aes(colour = group), width = 0.14, height = 0,
                size = 1.05, alpha = 0.55) +
    geom_boxplot(aes(colour = group), width = 0.30, fill = NA,
                 outlier.shape = NA, linewidth = LW_DATA * 0.65,
                 fatten = 2.2) +   # 中位线加粗靠 fatten，不再叠一层 crossbar
    scale_colour_manual(values = COL) +
    scale_y_continuous(limits = c(0, 100),
                       expand = expansion(mult = c(0.02, 0.04))) +
    labs(x = NULL, y = "Symptom score") +
    theme_pub(width_mm = FIG_WIDTH_MM[["single"]]) +
    theme(legend.position = "none")
}

for (p in names(BUILTIN_STYLES)) {
  STYLE         <- BUILTIN_STYLES[[p]]
  FIG_WIDTH_MM  <- STYLE$widths_mm
  LW_DATA       <- STYLE$line[["data"]]
  LW_AXIS       <- STYLE$line[["axis"]]
  LW_REF        <- STYLE$line[["ref"]]
  TICK_LENGTH_PT <- STYLE$tick_length_pt
  PAL_ROLES     <- as.list(STYLE$palette)

  p_obj <- build_panel()
  save_figure(p_obj, file.path(out, paste0("style_", p)),
              width_mm = FIG_WIDTH_MM[["single"]], height_mm = 80,
              formats = c("pdf", "svg", "png"), dpi = 300)
  cat(sprintf("  [%s] %s  单栏 %d mm\n", p, STYLE$label, FIG_WIDTH_MM[["single"]]))
}

cat("\n  预览图：\n")
for (f in list.files(out, pattern = "^style_.*png$")) cat("   ", f, "\n")
