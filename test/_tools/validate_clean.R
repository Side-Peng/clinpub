# Phase 1 输出校验（validate_output）
d <- read.csv("02_PreprocessedData/data/cleaned.csv",
              fileEncoding = "UTF-8", check.names = FALSE)
w <- read.csv("02_PreprocessedData/data/cleaned_with_missing.csv",
              fileEncoding = "UTF-8", check.names = FALSE)

cat("== cleaned.csv ==\n")
cat(sprintf("  维度 %d x %d\n", nrow(d), ncol(d)))
cat(sprintf("  缺失总数 %d\n", sum(is.na(d))))
cat(sprintf("  comorbidity: %s\n", paste(levels(d$comorbidity), collapse = " / ")))
cat(sprintf("  group      : %s\n", paste(levels(d$group), collapse = " / ")))
cat(sprintf("  sex        : %s\n", paste(levels(d$sex), collapse = " / ")))
cat("  comorbidity 计数:\n")
print(table(d$comorbidity))
cat("  group 计数:\n")
print(table(d$group))

cat("\n== cleaned_with_missing.csv ==\n")
cat(sprintf("  维度 %d x %d\n", nrow(w), ncol(w)))
cat(sprintf("  缺失总数 %d（bmi %d / baseline_score %d / egfr %d）\n",
            sum(is.na(w)),
            sum(is.na(w$bmi)), sum(is.na(w$baseline_score)), sum(is.na(w$egfr))))
cat(sprintf("  comorbidity 缺失 %d（应为 0）\n", sum(is.na(w$comorbidity))))

cat("\n== 断言 ==\n")
# 注意：read.csv 读出的是 character 而非 factor，levels() 返回 NULL；
# 用 NULL 做相等比较得 logical(0)，stopifnot 会**空转通过**。
# 因此这里断言取值集合，而不是因子水平。
stopifnot(
  nrow(d) == 102,
  sum(is.na(d)) == 0,
  nrow(w) == 120,
  sum(is.na(w$comorbidity)) == 0,
  identical(sort(unique(d$comorbidity)),
            sort(c("Both", "Diabetes", "Hypertension", "None"))),
  identical(sort(unique(d$group)), sort(c("Control", "Treatment"))),
  identical(sort(unique(d$sex)), sort(c("Female", "Male")))
)
cat("  全部通过 ✅\n")

cat("\n== 参照水平（写入 codebook，Phase 2 建模时用）==\n")
cat("  comorbidity: None（参照） / Hypertension / Diabetes / Both\n")
cat("  group      : Control（参照） / Treatment\n")
cat("  sex        : Female（参照） / Male\n")
