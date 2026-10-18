# 变量字典与编码说明（Codebook）

> 数据集：`02_PreprocessedData/data/cleaned.csv`（102 × 11，完整病例）
> 副本：`02_PreprocessedData/data/cleaned_with_missing.csv`（120 × 11，供 MICE 敏感性分析）
> 生成脚本：`03_AnalysisMethods/01_data_cleaning.R`

## 1. 变量

| 变量 | 类型 | 水平 / 范围 | 缺失（原始 120 例） | 说明 |
|---|---|---|---|---|
| `patient_id` | 整数 | 1–120 | 0 | 患者标识符，分析中不进入模型 |
| `age` | 连续 | 32–78 | 0 | 岁 |
| `sex` | 分类 | Female（参照）/ Male | 0 | |
| `bmi` | 连续 | 14.3–33.6 | 9 (7.5%) | |
| `group` | 分类 | Control（参照）/ Treatment | 0 | **横断面分组比较变量**，非干预效应 |
| `baseline_score` | 连续 | 17–100 | 6 (5.0%) | 症状评分，越高越重 |
| `post_score` | 连续 | 3–99 | 0 | 干预后评分；横断面下**不建变化量** |
| `egfr` | 连续 | 49.4–131.8 | 5 (4.2%) | 估算肾小球滤过率 |
| `comorbidity` | 分类 | None（参照）/ Hypertension / Diabetes / Both | 0 | **`None` = 无共病，是合法分类，不是缺失** |
| `followup_months` | 整数 | 6–57 | 0 | 横断面主分析不使用 |
| `event` | 二分类 | 0 / 1 | 0 | 横断面主分析不使用 |

## 2. 参照水平

| 变量 | 参照水平 | 其余水平 |
|---|---|---|
| `comorbidity` | **None** | Hypertension / Diabetes / Both |
| `group` | **Control** | Treatment |
| `sex` | **Female** | Male |

> CSV 中以字符串存储；R 建模时须显式设因子，例如：
> ```r
> d$comorbidity <- factor(d$comorbidity,
>                         levels = c("None", "Hypertension", "Diabetes", "Both"))
> ```

## 3. 清洗决策

| 编号 | 决策 | 依据 |
|---|---|---|
| D1 | 完整病例为主（N=102），保留含缺失副本做 MICE 敏感性 | 缺失均 <8%；N=120 时 MICE 收益有限，完整性优先 |
| D2 | IQR 离群值**保留**，仅记录 | 生理学区间 0 越界，属分布尾部而非录入错误 |
| D3 | `comorbidity` 四分类哑变量，`None` 为参照 | 保留"几种病"的信息 |
| D4 | 不创建衍生变量 | 横断面设计下不臆断 `post - baseline` 为变化量 |
| D5 | `None` 视为合法分类 | 否则 36 例（30%）被误当缺失 |

## 4. 缺失明细

| 变量 | 原始缺失 | 占比 |
|---|---|---|
| `bmi` | 9 | 7.5% |
| `baseline_score` | 6 | 5.0% |
| `egfr` | 5 | 4.2% |

完整病例剔除 18 行（占 15.0%）；`cleaned_with_missing.csv` 保留全部 120 行、20 个缺失单元。

## 5. 复现

```bash
Rscript 03_AnalysisMethods/01_data_cleaning.R
Rscript test/_tools/validate_clean.R     # 校验（本仓库内）
```

脚本内含断言：`comorbidity` 不得有缺失、必须含 `None` 水平、`group` 只能有 Treatment/Control。
