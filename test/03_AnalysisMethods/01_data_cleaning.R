# ============================================================
# Phase 1 — 数据清洗
# 项目：【暂定】共病与症状负担的横断面关联
# 生成物：02_PreprocessedData/data/cleaned.csv
#         02_PreprocessedData/data/cleaned_with_missing.csv
#         02_PreprocessedData/reports/data_quality_report.html
#
# 本脚本可独立复现：只依赖 01_RawData/patients.csv 与本文件的常量。
# 运行：Rscript 03_AnalysisMethods/01_data_cleaning.R
# ============================================================
#
# 清洗决策（2026-10-18，经用户确认）
# D1 缺失处理：完整病例为主分析（N≈105）；保留含缺失副本供 Phase 2 做 MICE 敏感性
# D2 异常值：IQR 离群 11 例**保留**（生理学区间内，属分布尾部），仅记录
# D3 comorbidity 编码：四分类因子，参照水平 = "None"
# D4 不创建衍生变量：横断面设计下 baseline_score 与 post_score 的关系
#    留待 Phase 2 判断，不在清洗阶段臆断为"变化量"
# D5 "None" 是**合法分类**（无共病），不是缺失值——读入时不得进入 NA 表
# ============================================================

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

root <- normalizePath(".")
raw_path <- file.path(root, "01_RawData", "patients.csv")
out_data <- file.path(root, "02_PreprocessedData", "data")
out_rep  <- file.path(root, "02_PreprocessedData", "reports")
dir.create(out_data, recursive = TRUE, showWarnings = FALSE)
dir.create(out_rep,  recursive = TRUE, showWarnings = FALSE)

# ---- D5：显式 NA 记号；绝不能包含 "None" -------------------------------
na_tokens <- c("", "NA", "N/A", "n/a", "NaN", "nan", "NULL", "null",
               "-", ".", "缺失", "不详")

raw <- read_csv(raw_path, na = na_tokens, show_col_types = FALSE,
                progress = FALSE)

cat("== 读入 ==\n")
cat(sprintf("  行数 %d | 列数 %d\n", nrow(raw), ncol(raw)))

# ---- 断言：None 必须是分类，不是缺失 -----------------------------------
stopifnot(
  "comorbidity 不应有缺失（'None' 是合法分类）" =
    !any(is.na(raw$comorbidity)),
  "comorbidity 应含 'None' 水平" =
    "None" %in% unique(raw$comorbidity),
  "group 只能有 Treatment/Control" =
    all(unique(raw$group) %in% c("Treatment", "Control"))
)
cat("  断言通过：comorbidity 无缺失，含 'None' 水平\n")

# ---- 变量类型与因子水平（D3） ------------------------------------------
analysis_vars <- c("patient_id", "age", "sex", "bmi", "group",
                   "baseline_score", "post_score", "egfr", "comorbidity")

clean <- raw %>%
  mutate(
    sex         = factor(sex, levels = c("Female", "Male")),
    group       = factor(group, levels = c("Control", "Treatment")),
    comorbidity = factor(comorbidity,
                         levels = c("None", "Hypertension", "Diabetes", "Both")),
    patient_id  = as.integer(patient_id)
  )

# ---- D1：完整病例（限定在分析变量上） ----------------------------------
complete_mask <- stats::complete.cases(clean[, analysis_vars])
clean_cc <- clean[complete_mask, ]

dropped <- sum(!complete_mask)
cat("\n== 缺失与完整病例 ==\n")
cat(sprintf("  含缺失行 %d 例；完整病例 %d 例（%.1f%%）\n",
            dropped, nrow(clean_cc), 100 * nrow(clean_cc) / nrow(clean)))

miss_tbl <- sapply(clean[, analysis_vars], function(x) sum(is.na(x)))
miss_tbl <- miss_tbl[miss_tbl > 0]
for (nm in names(miss_tbl)) {
  cat(sprintf("    %-16s 缺失 %d (%.1f%%)\n",
              nm, miss_tbl[[nm]], 100 * miss_tbl[[nm]] / nrow(clean)))
}

# ---- D2：离群值记录（保留） --------------------------------------------
outlier_rows <- list()
for (v in c("age", "bmi", "baseline_score", "post_score", "egfr")) {
  x  <- clean_cc[[v]]
  q  <- stats::quantile(x, c(.25, .75), na.rm = TRUE)
  iqr <- q[[2]] - q[[1]]
  lo <- q[[1]] - 1.5 * iqr
  hi <- q[[2]] + 1.5 * iqr
  n_out <- sum(x < lo | x > hi, na.rm = TRUE)
  outlier_rows[[v]] <- data.frame(
    variable = v, n_outlier = n_out,
    lower = round(lo, 2), upper = round(hi, 2),
    min = round(min(x, na.rm = TRUE), 2), max = round(max(x, na.rm = TRUE), 2)
  )
}
outlier_tbl <- do.call(rbind, outlier_rows)
cat("\n== 离群值（IQR 1.5x，保留不处理）==\n")
print(outlier_tbl, row.names = FALSE)

# ---- 生理学区间检查 -----------------------------------------------------
bounds <- list(
  bmi            = c(10, 60),
  age            = c(18, 110),
  egfr           = c(5, 200),
  baseline_score = c(0, 100),
  post_score     = c(0, 100)
)
cat("\n== 生理学区间 ==\n")
viol <- 0
for (v in names(bounds)) {
  b <- bounds[[v]]
  n_bad <- sum(clean_cc[[v]] < b[1] | clean_cc[[v]] > b[2], na.rm = TRUE)
  viol <- viol + n_bad
  cat(sprintf("  %-16s 越界 %d 例\n", v, n_bad))
}
cat(sprintf("  合计越界 %d 例\n", viol))

# ---- 写出 ---------------------------------------------------------------
write.csv(clean_cc, file.path(out_data, "cleaned.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")
write.csv(clean, file.path(out_data, "cleaned_with_missing.csv"),
          row.names = FALSE, fileEncoding = "UTF-8")

cat("\n== 输出 ==\n")
cat(sprintf("  cleaned.csv              %d 行 × %d 列\n",
            nrow(clean_cc), ncol(clean_cc)))
cat(sprintf("  cleaned_with_missing.csv %d 行 × %d 列\n",
            nrow(clean), ncol(clean)))

# ---- 质量报告（HTML） ---------------------------------------------------
esc <- function(x) {
  x <- as.character(x)
  x[is.na(x)] <- "-"
  gsub("&", "&amp;", gsub("<", "&lt;", gsub(">", "&gt;", x)))
}
html_table <- function(df) {
  head <- paste0("<tr>", paste0("<th>", esc(names(df)), "</th>", collapse = ""), "</tr>")
  rows <- apply(df, 1, function(r) {
    paste0("<tr>", paste0("<td>", esc(r), "</td>", collapse = ""), "</tr>")
  })
  paste0("<table>", head, paste(rows, collapse = ""), "</table>")
}

num_summary <- data.frame(
  variable = c("age", "bmi", "baseline_score", "post_score", "egfr"),
  n        = sapply(clean_cc[c("age","bmi","baseline_score","post_score","egfr")],
                    function(x) sum(!is.na(x))),
  mean     = sapply(clean_cc[c("age","bmi","baseline_score","post_score","egfr")],
                    function(x) round(mean(x, na.rm = TRUE), 1)),
  sd       = sapply(clean_cc[c("age","bmi","baseline_score","post_score","egfr")],
                    function(x) round(stats::sd(x, na.rm = TRUE), 1)),
  median   = sapply(clean_cc[c("age","bmi","baseline_score","post_score","egfr")],
                    function(x) round(stats::median(x, na.rm = TRUE), 1)),
  min      = sapply(clean_cc[c("age","bmi","baseline_score","post_score","egfr")],
                    function(x) round(min(x, na.rm = TRUE), 1)),
  max      = sapply(clean_cc[c("age","bmi","baseline_score","post_score","egfr")],
                    function(x) round(max(x, na.rm = TRUE), 1)),
  row.names = NULL
)

cat_levels <- do.call(rbind, lapply(c("sex", "group", "comorbidity"), function(v) {
  t <- table(clean_cc[[v]])
  data.frame(variable = v, level = names(t),
             n = as.integer(t),
             pct = round(100 * as.integer(t) / sum(t), 1),
             row.names = NULL)
}))

miss_df <- data.frame(
  variable = names(miss_tbl),
  n_missing = as.integer(miss_tbl),
  pct = round(100 * as.integer(miss_tbl) / nrow(clean), 1),
  row.names = NULL
)
if (nrow(miss_df) == 0) {
  miss_df <- data.frame(variable = "（无）", n_missing = 0L, pct = 0)
}

html <- paste0(
  "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>",
  "<title>数据质量报告 — Phase 1</title>",
  "<style>",
  "body{font-family:-apple-system,'Segoe UI',Arial,sans-serif;max-width:1000px;margin:40px auto;padding:0 20px;color:#222}",
  "h1{font-size:22px;border-bottom:2px solid #333;padding-bottom:8px}",
  "h2{font-size:17px;margin-top:28px;color:#111}",
  "table{border-collapse:collapse;width:100%;margin:10px 0;font-size:13px}",
  "th,td{border:1px solid #ddd;padding:6px 10px;text-align:left}",
  "th{background:#f5f5f5}",
  ".warn{background:#fff8e1;border-left:4px solid #f0ad4e;padding:10px 14px;margin:12px 0}",
  ".ok{color:#2e7d32}",
  "</style></head><body>",
  "<h1>数据质量报告 — Phase 1（数据准备）</h1>",
  sprintf("<p>生成时间：%s ｜ 原始文件：<code>%s</code></p>",
          format(Sys.time(), "%Y-%m-%d %H:%M"), esc(basename(raw_path))),
  "<h2>1. 概览</h2>",
  sprintf("<p>原始 <b>%d</b> 行 × <b>%d</b> 列；完整病例 <b>%d</b> 例（%.1f%%），剔除 <b>%d</b> 例。</p>",
          nrow(raw), ncol(raw), nrow(clean_cc),
          100 * nrow(clean_cc) / nrow(clean), dropped),
  "<h2>2. 缺失情况</h2>",
  html_table(miss_df),
  "<div class='warn'><b>注意：</b><code>comorbidity</code> 的取值 <code>None</code>（无共病）",
  "是<b>合法分类</b>，不是缺失值。读取时已显式排除出 NA 记号表，",
  "否则 36 例（30%）会被静默当成缺失。</div>",
  "<h2>3. 连续变量分布（完整病例）</h2>",
  html_table(num_summary),
  "<h2>4. 分类变量分布（完整病例）</h2>",
  html_table(cat_levels),
  "<h2>5. 离群值（IQR 1.5×，未处理）</h2>",
  html_table(outlier_tbl),
  sprintf("<p class='ok'>生理学区间检查：合计越界 <b>%d</b> 例。离群值予以保留，属分布尾部。</p>", viol),
  "<h2>6. 清洗决策</h2><ul>",
  "<li><b>D1 缺失</b>：完整病例为主（N=", nrow(clean_cc), "）；保留含缺失副本供 MICE 敏感性分析</li>",
  "<li><b>D2 离群</b>：保留，仅记录</li>",
  "<li><b>D3 编码</b>：<code>comorbidity</code> 四分类，参照 <code>None</code>；",
  "<code>group</code> 参照 <code>Control</code>；<code>sex</code> 参照 <code>Female</code></li>",
  "<li><b>D4 衍生变量</b>：不创建（横断面设计下不臆断变化量）</li>",
  "<li><b>D5 None 语义</b>：合法分类，非缺失</li>",
  "</ul>",
  "<h2>7. 复现</h2>",
  "<p><code>Rscript 03_AnalysisMethods/01_data_cleaning.R</code></p>",
  "</body></html>"
)
writeLines(html, file.path(out_rep, "data_quality_report.html"), useBytes = TRUE)
cat(sprintf("  data_quality_report.html\n"))
cat("\n完成。\n")
