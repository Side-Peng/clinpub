# clinpub 测试指南

> **注意**：以下测试示例为模板参考，展示推荐的测试模式和结构。当前项目尚未建立完整的测试套件。示例中引用的函数和文件名用于说明目的，实际实现时需根据当前代码调整。

## 测试原则

### 独立性原则

每段测试代码必须独立运行，不依赖外部环境或其他测试。

- 测试数据在脚本内定义
- 测试环境在脚本内配置
- 测试结果在脚本内验证

## 测试类型

### 1. 单元测试

测试单个函数或模块的功能。

#### R 单元测试示例

```r
# test_data_cleaning.R

# 测试数据（脚本内定义）
test_data <- data.frame(
  id = 1:10,
  age = c(25, 30, NA, 40, 45, 50, NA, 60, 65, 70),
  gender = c("M", "F", "M", NA, "M", "F", "M", "F", "M", "F")
)

# 测试函数
test_impute_missing <- function() {
  source("03_AnalysisMethods/data_cleaning.R")
  
  result <- impute_missing(test_data, method = "median")
  
  stopifnot(!any(is.na(result$age)))
  stopifnot(!any(is.na(result$gender)))
  cat("✓ impute_missing 测试通过\n")
}

test_encode_categorical <- function() {
  source("03_AnalysisMethods/data_cleaning.R")
  
  result <- encode_categorical(test_data, cols = c("gender"))
  
  stopifnot(is.numeric(result$gender))
  cat("✓ encode_categorical 测试通过\n")
}

# 执行所有测试
test_impute_missing()
test_encode_categorical()
```

#### Python 单元测试示例

```python
# test_data_profiler.py

import pandas as pd
import numpy as np

# 测试数据（脚本内定义）
TEST_DATA = pd.DataFrame({
    'id': range(1, 11),
    'age': [25, 30, None, 40, 45, 50, None, 60, 65, 70],
    'gender': ['M', 'F', 'M', None, 'M', 'F', 'M', 'F', 'M', 'F']
})

def test_profile_data():
    """测试数据画像函数"""
    from scripts.data_profiler import profile_data
    
    result = profile_data(TEST_DATA)
    
    assert 'shape' in result
    assert 'missing' in result
    assert result['shape'] == (10, 3)
    print("✓ profile_data 测试通过")

def test_detect_outliers():
    """测试异常值检测"""
    from scripts.data_profiler import detect_outliers
    
    result = detect_outliers(TEST_DATA, column='age')
    
    assert isinstance(result, pd.Series)
    print("✓ detect_outliers 测试通过")

if __name__ == "__main__":
    test_profile_data()
    test_detect_outliers()
```

### 2. 集成测试

测试多个模块协同工作的功能。

```r
# test_analysis_pipeline.R

# 测试数据
test_data <- data.frame(
  id = 1:50,
  age = rnorm(50, 50, 10),
  gender = sample(c("M", "F"), 50, replace = TRUE),
  treatment = sample(c("A", "B"), 50, replace = TRUE),
  outcome = rbinom(50, 1, 0.3)
)

test_full_analysis <- function() {
  # 1. 数据清洗
  source("03_AnalysisMethods/data_cleaning.R")
  cleaned <- clean_data(test_data)
  
  # 2. 基线表
  source("03_AnalysisMethods/baseline_table.R")
  baseline <- generate_baseline_table(cleaned)
  
  # 3. 回归分析
  source("03_AnalysisMethods/regression.R")
  model <- run_regression(cleaned, outcome ~ treatment + age + gender)
  
  stopifnot(!is.null(baseline))
  stopifnot(!is.null(model))
  cat("✓ 完整分析流程测试通过\n")
}

test_full_analysis()
```

### 3. 端到端测试

测试完整的用户工作流。

```r
# test_e2e_workflow.R

test_complete_workflow <- function() {
  # 1. 准备测试数据
  test_dir <- tempdir()
  dir.create(file.path(test_dir, "01_RawData"), recursive = TRUE)
  
  write.csv(mtcars, file.path(test_dir, "01_RawData", "test_data.csv"))
  
  # 2. 创建配置
  config <- list(
    variables = list(
      outcome = "mpg",
      exposure = "cyl",
      covariates = c("hp", "wt")
    )
  )
  yaml::write_yaml(config, file.path(test_dir, "project_config.yml"))
  
  # 3. 执行 Phase 1
  source("commands/data-prep.R")
  run_data_prep(test_dir)
  
  # 4. 验证输出
  stopifnot(file.exists(file.path(test_dir, "02_PreprocessedData", "data", "cleaned.csv")))
  
  cat("✓ 端到端工作流测试通过\n")
}

test_complete_workflow()
```

## 测试数据管理

### 测试数据原则

1. **脚本内定义**：测试数据直接在测试脚本中定义
2. **最小化**：只包含测试必需的数据
3. **代表性**：覆盖正常、边界、异常情况
4. **可重复**：使用固定随机种子

```r
# 使用固定随机种子
set.seed(123)

# 生成测试数据
test_data <- data.frame(
  id = 1:100,
  age = rnorm(100, 50, 10),
  gender = sample(c("M", "F"), 100, replace = TRUE),
  outcome = rbinom(100, 1, 0.3)
)
```

### 边界条件测试

```r
test_boundary_conditions <- function() {
  # 空数据
  empty_data <- data.frame()
  result <- tryCatch(
    clean_data(empty_data),
    error = function(e) NULL
  )
  stopifnot(is.null(result))
  cat("✓ 空数据处理测试通过\n")
  
  # 单行数据
  single_row <- data.frame(id = 1, age = 25, gender = "M")
  result <- clean_data(single_row)
  stopifnot(nrow(result) == 1)
  cat("✓ 单行数据处理测试通过\n")
  
  # 全部缺失
  all_na <- data.frame(id = 1:5, age = rep(NA, 5), gender = rep(NA, 5))
  result <- tryCatch(
    clean_data(all_na),
    error = function(e) NULL
  )
  cat("✓ 全部缺失处理测试通过\n")
}
```

## 测试运行

### R 测试运行

```bash
# 运行单个测试
Rscript tests/test_data_cleaning.R

# 运行所有测试
for test in tests/test_*.R; do
  Rscript "$test"
done
```

### Python 测试运行

```bash
# 运行单个测试
python tests/test_data_profiler.py

# 运行所有测试
python -m pytest tests/

# 运行并显示覆盖率
python -m pytest tests/ --cov=scripts --cov-report=html
```

## 测试覆盖率

### 覆盖率目标

- 单元测试：>= 80%
- 集成测试：>= 60%
- 端到端测试：关键路径 100%

### 覆盖率报告

```r
# 使用 covr 包
library(covr)
coverage <- package_coverage()
report(coverage)
```

```python
# 使用 coverage.py
coverage run -m pytest
coverage report
coverage html
```

## 持续集成

### GitHub Actions 示例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up R
      uses: r-lib/actions/setup-r@v2
      
    - name: Install dependencies
      run: |
        Rscript -e 'install.packages(c("dplyr", "tidyr", "ggplot2"))'
        
    - name: Run tests
      run: |
        for test in tests/test_*.R; do
          Rscript "$test"
        done
```

## 测试最佳实践

### 1. 测试命名

```r
# ✓ 好的命名
test_impute_missing_values_median_method()
test_baseline_table_with_grouping()

# ✗ 不好的命名
test1()
test_function()
```

### 2. 测试隔离

```r
# 每个测试独立运行
test_a <- function() {
  data <- prepare_test_data()
  result <- function_a(data)
  verify(result)
}

test_b <- function() {
  data <- prepare_test_data()  # 重新准备，不依赖 test_a
  result <- function_b(data)
  verify(result)
}
```

### 3. 测试清理

```r
test_with_cleanup <- function() {
  # 准备
  test_dir <- tempdir()
  dir.create(test_dir)
  
  # 执行
  tryCatch({
    run_analysis(test_dir)
    cat("✓ 测试通过\n")
  }, finally = {
    # 清理
    unlink(test_dir, recursive = TRUE)
  })
}
```

## 调试测试

### 调试失败的测试

```r
# 添加详细输出
test_with_debug <- function() {
  data <- prepare_test_data()
  cat("输入数据:", nrow(data), "行\n")
  
  result <- function_under_test(data)
  cat("输出结果:", length(result), "个\n")
  
  if (!verify(result)) {
    cat("验证失败\n")
    cat("期望:", expected, "\n")
    cat("实际:", result, "\n")
    browser()  # 进入调试模式
  }
}
```
