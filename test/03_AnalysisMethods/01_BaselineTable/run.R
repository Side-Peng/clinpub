# ============================================================
# Batch 1 / Method 01 — 基线特征表（Table 1，按 group 分组）
# 输入：02_PreprocessedData/data/cleaned.csv
# 输出：04_Outputs/01_BaselineTable/table1.csv
# 运行：Rscript 03_AnalysisMethods/01_BaselineTable/run.R
# ============================================================

suppressPackageStartupMessages({
  library(dplyr)
})

source("04_Outputs/_figure_config.R")

root <- normalizePath(".")
d <- read.csv(file.path(root, "02_PreprocessedData/data/cleaned.csv"),
              fileEncoding = "UTF-8", check.names = FALSE)
d$group <- factor(d$group, levels = c("Control", "Treatment"))
d$sex <- factor(d$sex, levels = c("Female", "Male"))
d$comorbidity <- factor(d$comorbidity,
                        levels = c("None", "Hypertension", "Diabetes", "Both"))

out_dir <- file.path(root, "04_Outputs/01_BaselineTable")
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)

fmt_p <- function(p) {
  if (is.na(p)) return("-")
  if (p < 0.001) return("<0.001")
  sprintf("%.3f", p)
}

smd_cont <- function(x, g) {
  a <- x[g == levels(g)[1]]; b <- x[g == levels(g)[2]]
  sp <- sqrt((var(a) + var(b)) / 2)
  if (is.na(sp) || sp == 0) return(NA_real_)
  (mean(b) - mean(a)) / sp
}

rows <- list()
add <- function(...) rows[[length(rows) + 1]] <<- data.frame(..., stringsAsFactors = FALSE)

# ---- 连续变量 ------------------------------------------------------------
cont_vars <- c("age", "bmi", "baseline_score", "post_score", "egfr")
for (v in cont_vars) {
  x <- d[[v]]; g <- d$group
  m1 <- mean(x[g == "Control"]); s1 <- sd(x[g == "Control"])
  m2 <- mean(x[g == "Treatment"]); s2 <- sd(x[g == "Treatment"])
  p  <- tryCatch(t.test(x ~ g)$p.value, error = function(e) NA_real_)
  add(variable = v, level = "",
      control = sprintf("%.1f (%.1f)", m1, s1),
      treatment = sprintf("%.1f (%.1f)", m2, s2),
      p = fmt_p(p), smd = sprintf("%.2f", smd_cont(x, g)))
}

# ---- 分类变量 ------------------------------------------------------------
cat_vars <- c("sex", "comorbidity")
for (v in cat_vars) {
  tb <- table(d[[v]], d$group)
  p  <- tryCatch(suppressWarnings(chisq.test(tb)$p.value), error = function(e) NA_real_)
  lv <- levels(d[[v]])
  for (i in seq_along(lv)) {
    n1 <- sum(d[[v]] == lv[i] & d$group == "Control")
    n2 <- sum(d[[v]] == lv[i] & d$group == "Treatment")
    tot1 <- sum(d$group == "Control"); tot2 <- sum(d$group == "Treatment")
    add(variable = if (i == 1) v else "",
        level = lv[i],
        control = sprintf("%d (%.1f%%)", n1, 100 * n1 / tot1),
        treatment = sprintf("%d (%.1f%%)", n2, 100 * n2 / tot2),
        p = if (i == 1) fmt_p(p) else "",
        smd = "")
  }
}

tbl <- do.call(rbind, rows)
names(tbl) <- c("Variable", "Level",
                sprintf("Control (n=%d)", sum(d$group == "Control")),
                sprintf("Treatment (n=%d)", sum(d$group == "Treatment")),
                "P", "SMD")

write.csv(tbl, file.path(out_dir, "table1.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")

cat("== Table 1 ==\n")
print(tbl, row.names = FALSE)
cat(sprintf("\n已写出 %s\n", file.path(out_dir, "table1.csv")))
