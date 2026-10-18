# 把新导出的 PDF 转成 PNG 预览（仅用于查看，不进交付）
suppressPackageStartupMessages(library(magick))

files <- c(
  "04_Outputs/02_OutcomeScreening/fig1_candidates_by_group.pdf",
  "04_Outputs/03_AdjustedModel/fig2_adjusted_effects.pdf",
  "04_Outputs/04_SensitivityAnalysis/fig3_sensitivity_forest.pdf"
)

for (f in files) {
  if (!file.exists(f)) { cat("  缺失:", f, "\n"); next }
  out <- sub("\\.pdf$", "_preview.png", f)
  img <- image_read_pdf(f, density = 300)
  image_write(img, out, format = "png")
  cat(sprintf("  %s  (%d x %d)\n", basename(out),
              image_info(img)$width, image_info(img)$height))
}
