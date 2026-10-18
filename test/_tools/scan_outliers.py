"""Phase 1：离群值扫描（IQR 1.5×）与分布摘要，供清洗策略讨论。"""
import io

import pandas as pd

BASE = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub"
NA_VALUES = ["", "NA", "N/A", "n/a", "NaN", "nan", "NULL", "null", "-", ".", "缺失", "不详"]

df = pd.read_csv(
    BASE + r"\test\01_RawData\patients.csv",
    keep_default_na=False,
    na_values=NA_VALUES,
)

print("行数:", len(df), "| 列数:", len(df.columns))
print()
print(f"{'变量':<16}{'n':>5}{'缺失':>6}{'均值':>9}{'SD':>8}{'中位':>8}{'最小':>8}{'最大':>8}{'离群':>6}")
for col in ["age", "bmi", "baseline_score", "post_score", "followup_months", "egfr"]:
    s = pd.to_numeric(df[col], errors="coerce")
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_out = int(((s < lo) | (s > hi)).sum())
    print(
        f"{col:<16}{s.notna().sum():>5}{s.isna().sum():>6}"
        f"{s.mean():>9.1f}{s.std():>8.1f}{s.median():>8.1f}"
        f"{s.min():>8.1f}{s.max():>8.1f}{n_out:>6}"
    )

print()
print("分类变量分布（含 None 作为合法分类）:")
for col in ["sex", "group", "comorbidity"]:
    vc = df[col].value_counts(dropna=False)
    parts = [f"{k}={v}" for k, v in vc.items()]
    print(f"  {col:<14}" + " | ".join(parts))

print()
print("生理学合理性检查:")
checks = [
    ("bmi", 10, 60, "BMI 合理区间 10–60"),
    ("age", 18, 110, "年龄合理区间 18–110"),
    ("egfr", 5, 200, "eGFR 合理区间 5–200"),
    ("baseline_score", 0, 100, "评分区间 0–100"),
    ("post_score", 0, 100, "评分区间 0–100"),
]
for col, lo, hi, label in checks:
    s = pd.to_numeric(df[col], errors="coerce")
    bad = int(((s < lo) | (s > hi)).sum())
    print(f"  {label:<22} 越界 {bad} 例")
