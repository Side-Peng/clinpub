# clinpub 开发指南

## 核心原则

### 代码独立性原则

**每段代码必须独立运行，不依赖其他代码。**

- 所有变量必须在单个代码文件内定义，禁止使用全局变量
- 每个 R/Python 脚本必须是自包含的，可以直接运行
- 禁止跨文件的隐式依赖（如全局环境变量、共享状态）

```r
# ✓ 正确：所有变量在脚本内定义
data_path <- "01_RawData/clinical_data.csv"
output_dir <- "04_Outputs/01_BaselineTable"
significance_level <- 0.05

data <- read.csv(data_path)
# ... 分析代码 ...
```

```r
# ✗ 错误：依赖外部变量或全局状态
data <- read.csv(global_data_path)  # 全局变量
# ... 分析代码 ...
```

## 开发环境

### 系统要求

| 组件        | 版本      | 用途               |
| ----------- | --------- | ------------------ |
| Claude Code | >= 2.1.88 | Skill 宿主环境     |
| Node.js     | >= 22.0.0 | Hook 执行          |
| R           | >= 4.2    | 统计分析           |
| Python      | >= 3.9    | 数据画像、文献检索 |

### R 开发环境

```r
# 安装所有必需包
install.packages(c(
  "dplyr", "tidyr", "stringr", "readr", "readxl",
  "survival", "lme4", "glmnet", "pROC",
  "ggplot2", "ggpubr", "patchwork", "survminer", "ggsurvfit", "ggsignif",
  "gtsummary", "flextable", "openxlsx",
  "here", "fs"
))
```

### Python 开发环境

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## 代码规范

### R 代码规范

#### 文件结构

```r
# ============================================================
# 文件名：01_BaselineTable.R
# 描述：生成基线特征表
# 作者：clinpub
# 日期：2024-01-01
# ============================================================

# 1. 依赖加载（仅声明，不依赖外部加载）
library(dplyr)
library(gtsummary)

# 2. 参数定义（所有变量在脚本内定义）
data_path <- "02_PreprocessedData/data/cleaned.csv"
output_dir <- "04_Outputs/01_BaselineTable"
significance_level <- 0.05

# 3. 数据读取
data <- read.csv(data_path)

# 4. 核心逻辑
baseline_table <- data %>%
  select(age, gender, bmi, smoking_status) %>%
  tbl_summary(
    by = treatment,
    statistic = list(
      all_continuous() ~ "{mean} ({sd})",
      all_categorical() ~ "{n} ({p}%)"
    ),
    pvalue_fun = ~style_pvalue(.x, digits = 2)
  )

# 5. 输出保存
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
gtsave(baseline_table, file.path(output_dir, "BaselineTable.png"))
```

#### 命名规范

- 变量名：`snake_case`（例：`data_path`, `output_dir`）
- 函数名：`camelCase`（例：`generateBaselineTable`）
- 常量：`UPPER_SNAKE_CASE`（例：`SIGNIFICANCE_LEVEL`）

### Python 代码规范

#### 文件结构

```python
"""
文件名：data_profiler.py
描述：数据画像脚本
作者：clinpub
日期：2024-01-01
"""

# 1. 依赖导入
import pandas as pd
import numpy as np

# 2. 参数定义（所有变量在脚本内定义）
DATA_PATH = "01_RawData/clinical_data.csv"
OUTPUT_DIR = "04_Outputs/DataProfile"
SIGNIFICANCE_LEVEL = 0.05

# 3. 核心逻辑
def profile_data(data_path: str) -> dict:
    """生成数据画像"""
    df = pd.read_csv(data_path)
  
    profile = {
        "shape": df.shape,
        "dtypes": df.dtypes.to_dict(),
        "missing": df.isnull().sum().to_dict(),
        "describe": df.describe().to_dict()
    }
  
    return profile

# 4. 主函数
def main():
    profile = profile_data(DATA_PATH)
    # ... 输出保存 ...

if __name__ == "__main__":
    main()
```

## Agent 开发

### Agent 角色卡片结构

每个 Agent 是一个 Markdown 文件，定义了：

```markdown
# Agent 名称

## 角色定位
简短描述 Agent 的职责

## 输入规范
- 输入数据格式
- 必需参数

## 输出规范
- 输出文件格式
- 产出目录

## 工具权限
- 允许使用的工具列表

## 质量标准
- 输出必须满足的条件
```

### Agent 独立性

每个 Agent 必须：

- 拥有独立的上下文（不共享状态）
- 通过文件系统传递数据（不通过内存）
- 输出标准化的 MANIFEST.yaml

## Workflow 开发

### Workflow 文件结构

```markdown
# Workflow 名称

## 触发条件
何时调用此 workflow

## 执行步骤
1. 步骤 1
2. 步骤 2
...

## 产出
- 输出文件列表

## 前置条件
- 必须完成的前置步骤
```

## 测试

### 测试原则

- 每个脚本必须可独立运行
- 测试数据必须在脚本内定义
- 禁止依赖外部测试环境

### 测试脚本示例

```r
# test_baseline_table.R

# 测试数据（脚本内定义）
test_data <- data.frame(
  age = c(25, 30, 35, 40, 45),
  gender = c("M", "F", "M", "F", "M"),
  treatment = c("A", "B", "A", "B", "A")
)

# 测试函数
test_baseline_table <- function() {
  # ... 测试逻辑 ...
  stopifnot(nrow(test_data) == 5)
}

# 执行测试
test_baseline_table()
```

## 版本控制

### Git 提交规范

```
<type>(<scope>): <subject>

类型：
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 构建/工具

示例：
feat(analysis): 添加生存分析模块
fix(data-prep): 修复缺失值处理 bug
docs(readme): 更新安装说明
```

### 分支策略

- `main`: 稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复

## 调试

### R 调试

```r
# 启用调试模式
options(error = recover)

# 使用 browser()
debug(generateBaselineTable)
undebug(generateBaselineTable)
```

### Python 调试

```python
# 使用 pdb
import pdb; pdb.set_trace()

# 使用 logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 性能优化

### R 性能优化

```r
# 使用 data.table 替代 data.frame
library(data.table)
data <- fread("large_data.csv")

# 使用并行处理
library(parallel)
mclapply(1:100, function(i) {...}, mc.cores = 4)
```

### Python 性能优化

```python
# 使用 chunking 处理大文件
for chunk in pd.read_csv("large_data.csv", chunksize=10000):
    process(chunk)

# 使用 multiprocessing
from multiprocessing import Pool
with Pool(4) as p:
    p.map(process, data_chunks)
```
