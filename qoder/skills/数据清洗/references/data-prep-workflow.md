# 数据准备工作流详解

## 目的

将原始患者级数据转化为分析就绪的 cleaned.csv，附带完整的质量文档。处理缺失值、异常值、衍生变量和编码，通过分层决策框架在模糊点与用户确认。

## 前置阅读

- `../知识库/references/analysis_methods.md` — 分析方法参考
- `../知识库/references/checkpoints.md` — 检查点规范

## 重入刷新（D-05/D-06 全链路刷新）

当项目已初始化时执行：

1. **重新运行 profile（更新变量字典）**
   - 定位原始数据文件（从 `project_config.yml` 的 `paths.raw_data` 字段）
   - 执行 `python scripts/data_profiler.py {raw_data} --output {preprocessed}/data_profile.json`
   - 获取最新变量列表、缺失模式、变量角色

2. **重新生成 spec 模板（更新分析规范）**
   - 读取 data_profile.json 的变量摘要和 project_config.yml
   - 填充模板占位符:
     - `{{study_title}}` → `project.name`
     - `{{study_type}}` → `project.design`
     - `{{N}}` → `data_profile.n_rows`
     - `{{primary_outcome}}` → `variables.outcome`
   - 输出到 `03_AnalysisMethods/01-spec.md`（覆盖旧文件）

3. **同步更新 project_config.yml**
   - 根据 profile 的 role_summary 更新变量字段
   - 仅更新变量相关字段，保留用户手动配置

4. **变更摘要报告**

## 清洗策略讨论

与用户确认以下策略：

### 缺失值分层策略

| 缺失率 | 策略 | 详情 |
|--------|------|------|
| <5% | 删除或填充 | 均值/中位数（连续）或众数（分类） |
| 5-20% | MICE 插补 | 多重插补，报告插补模型 |
| >20% | 讨论后处理 | 与用户讨论每个高缺失变量 |

### 异常值检测

| 类型 | 方法 | 阈值 |
|------|------|------|
| 连续变量 | IQR 法 | Q1-1.5*IQR ~ Q3+1.5*IQR |
| 连续变量 | Z-score 法 | |Z| > 3 |
| 分类变量 | 值域检查 | 意外值 |

处理方式: 缩尾（winsorization）或排除（exclusion），与用户确认。

### 衍生变量

常见衍生变量类型：
- 计算得分（BMI = weight/height^2）
- 指数（ Charlson 合并症指数）
- 组合变量（代谢综合征 = 满足 N 项标准）
- 变化分数（post - baseline）

### 变量编码

- 分类变量: 设置因子水平和参考类别
- 连续变量: 变换（log, Box-Cox, 标准化）
- 二分类: 编码方式（0/1, yes/no）

## 数据结构检测

### 纵向数据检测

```
如果 time 列存在且患者 ID 出现多次 → 纵向数据
对每个患者计算时间点数量
如果多数 >1 → 重复测量
```

纵向数据的特殊处理：
- 基线表必须过滤到单一时间点（通常 baseline）
- 重复测量需要混合模型（lme4）
- 区分结构性缺失 vs 随机缺失

### 结局类型检测

```
唯一值 = 2 → binary (二分类)
唯一值 3-20 → 检查分布，可能 categorical 或 continuous
唯一值 >20 → continuous (检查正态性)
```

### 结构性缺失检测

如果特定变量仅在某些时间点缺失 → 标记为 "structurally_missing"

## 执行清洗

### 1. 导入数据

```r
library(readr)
library(dplyr)
library(tidyr)

raw <- read_csv("01_RawData/{filename}")
```

生成变量字典:
- 变量名
- 类型（numeric, character, factor, date）
- 缺失率
- 唯一值数量
- 样本值

### 2. 缺失值处理

按分层策略执行:

```r
# <5%: 均值填充
data$var[is.na(data$var)] <- mean(data$var, na.rm = TRUE)

# 5-20%: MICE
library(mice)
imp <- mice(data, m = 5, method = "pmm", seed = 123)
data <- complete(imp, 1)

# >20%: 与用户讨论
```

### 3. 异常值检测

```r
# IQR 法
Q1 <- quantile(data$var, 0.25, na.rm = TRUE)
Q3 <- quantile(data$var, 0.75, na.rm = TRUE)
IQR_val <- Q3 - Q1
outliers <- data$var < (Q1 - 1.5 * IQR_val) | data$var > (Q3 + 1.5 * IQR_val)

# Z-score 法
z_scores <- scale(data$var)
outliers_z <- abs(z_scores) > 3
```

### 4. 衍生变量 + 编码

```r
# 计算变量
data$BMI <- data$weight / (data$height / 100)^2

# 因子编码
data$group <- factor(data$group, levels = c("Control", "Treatment"))

# 对数变换
data$log_var <- log(data$var + 1)
```

### 5. 数据质量报告

生成 HTML 报告包含:
- 变量摘要表
- 缺失值矩阵（热力图）
- 关键变量分布图（直方图、箱线图）
- 异常值文档
- 训练/验证集拆分摘要

### 6. 保存 cleaned.csv

```r
write_csv(cleaned, "02_PreprocessedData/data/cleaned.csv")
```

如果是纵向数据，同时保存完整纵向数据:
```r
write_csv(full_data, "02_PreprocessedData/data/full_longitudinal.csv")
```

## 验证

1. 验证 cleaned.csv 存在
2. 检查行/列数
3. 确认高缺失率变量已处理
4. 验证数据类型
5. 确保代码可独立复现

## 成功标准

- cleaned.csv 写入 `02_PreprocessedData/data/`
- 数据质量报告已生成（HTML）
- 缺失值按约定策略处理
- 异常值已记录
- 衍生变量已创建和编码
- 清洗代码可独立从原始数据复现
- MANIFEST.yaml 已写入 `02_PreprocessedData/`
