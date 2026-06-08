# Contributing to clinpub

感谢你关注 clinpub！本文档说明如何参与贡献。

## 核心原则：自包含

> **clinpub 产出的任何代码，必须自包含、可独立运行。**

clinpub 是一个 AI Agent 驱动的科研流水线。每个 Agent 在**隔离的上下文**中工作——没有共享内存、没有全局环境、没有隐式依赖。因此，无论是分析脚本、数据处理、图表生成还是工具函数，都必须满足：

1. **所有依赖在文件内声明**：library/import 写在文件顶部
2. **所有变量在文件内定义**：路径、参数、配置不外求
3. **所有辅助函数在文件内实现**：不 source/import 项目内其他文件
4. **丢到任意机器上，装好依赖包即可运行**

这条原则适用于所有语言：

<details>
<summary>R 示例</summary>

```r
# ✓ 正确
library(dplyr)
library(ggplot2)

data_path <- "01_RawData/data.csv"
data <- read.csv(data_path)

# 辅助函数直接写在文件里
format_pvalue <- function(p) {
  if (p < 0.001) return("<0.001")
  sprintf("%.3f", p)
}

# ✗ 错误
source("scripts/utils.R")           # 跨文件依赖
data <- read.csv(global_path)        # 未定义的外部变量
```

</details>

<details>
<summary>Python 示例</summary>

```python
# ✓ 正确
import pandas as pd
import numpy as np

DATA_PATH = "01_RawData/data.csv"
df = pd.read_csv(DATA_PATH)

# 辅助函数直接写在文件里
def format_pvalue(p: float) -> str:
    return "<0.001" if p < 0.001 else f"{p:.3f}"

# ✗ 错误
from clinpub.utils import helpers    # 跨模块依赖
df = pd.read_csv(config.data_path)   # 未定义的外部状态
```

</details>

<details>
<summary>JavaScript / Shell 示例</summary>

```javascript
// ✓ 正确 — Node.js 脚本
const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join('.clinpub', 'STATE.md');
const state = fs.readFileSync(STATE_FILE, 'utf8');

// ✗ 错误
const utils = require('./lib/utils');  // 跨文件依赖
```

```bash
# ✓ 正确 — Shell 脚本自包含所有逻辑
STATE_FILE=".clinpub/STATE.md"
PHASE=$(grep -oP '阶段：Phase\s*\K\d' "$STATE_FILE")

# ✗ 错误
source ./shared/helpers.sh            # 跨文件依赖
```

</details>

## 开发环境

```bash
git clone https://github.com/Side-Peng/clinpub.git
cd clinpub

# Node.js >= 22
npm install

# R
Rscript -e 'install.packages(c("dplyr","tidyr","ggplot2","gtsummary","survival","lme4","glmnet","pROC","ggpubr","patchwork","survminer","ggsurvfit","ggsignif","flextable","openxlsx","here","fs","stringr","readr","readxl"))'

# Python
pip install -r requirements.txt
```

## 项目结构

```
clinpub/
├── commands/clinpub/   # 命令入口（YAML frontmatter + @-references）
├── agents/             # AI Agent 角色卡片（每个 Agent 独立上下文）
├── pipeline/
│   ├── workflows/      # 阶段编排（DISCUSS → PLAN → EXECUTE → VERIFY）
│   ├── references/     # 参考文档（标准、方法、模式）
│   ├── templates/      # 研究类型模板 + 项目配置
│   └── contexts/       # 上下文配置
├── scripts/            # 工具脚本（必须自包含）
├── hooks/              # 工作流守卫钩子（必须自包含）
├── bin/                # 安装脚本
└── docs/               # 项目文档
```

## 提交规范

```
<type>(<scope>): <subject>
```

| Type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `refactor` | 重构（不改行为） |
| `test` | 测试相关 |
| `chore` | 构建/工具/CI |

示例：
```
feat(r_patterns): 添加森林图模板
fix(workflow-guard): 修复 Phase 2 目录判定逻辑
docs(agents): 更新 analyst-agent 的方法选择说明
```

## 贡献流程

1. **Fork → 克隆 → 创建分支**
   ```bash
   git checkout -b feat/your-feature
   ```

2. **开发**
   - 写代码前先问自己：这个文件能独立运行吗？
   - 新增了辅助函数？确认它在同一个文件内
   - 修改了现有脚本？确认改完仍能独立运行
   - 改了 Agent / Workflow？确认 `@-references` 路径正确

3. **提交 & 推送**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   git push origin feat/your-feature
   ```

4. **创建 Pull Request**，说明变更内容

## 注意事项

- **不要提交患者数据**：`.gitignore` 已排除 CSV/XLSX/SAV/DTA 等格式
- **不要修改已发布版本的 API**：破坏性变更请先开 Issue 讨论
- **Agent 间只通过文件通信**：一个 Agent 读另一个 Agent 的输出文件，不做内存级协作
- **单目录单写者**：每个输出目录只由一个 Agent 负责写入
