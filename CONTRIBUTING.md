# 贡献指南

感谢你对 clinpub 项目的关注！本指南帮助你参与项目开发。

## 快速开始

### 1. Fork 并克隆

```bash
# Fork 项目到你的 GitHub 账号
# 然后克隆
git clone https://github.com/YOUR_USERNAME/clinpub.git
cd clinpub
```

### 2. 安装依赖

```bash
# Node.js 依赖
npm install

# R 依赖
Rscript -e 'install.packages(c("dplyr", "tidyr", "ggplot2", "gtsummary"))'

# Python 依赖
pip install -r requirements.txt
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
```

## 开发规范

### 代码独立性原则

**每段代码必须独立运行，不依赖其他代码。**

- 所有变量必须在单个代码文件内定义
- 禁止使用全局变量或跨文件依赖
- 每个脚本必须可直接运行

```r
# ✓ 正确
data_path <- "01_RawData/data.csv"  # 脚本内定义
data <- read.csv(data_path)

# ✗ 错误
data <- read.csv(global_path)  # 依赖全局变量
```

### 代码风格

#### R 代码

- 使用 `snake_case` 命名变量
- 使用 `camelCase` 命名函数
- 每个函数不超过 50 行
- 添加注释说明意图

```r
# 计算基线特征表
generate_baseline_table <- function(data, group_var) {
  # 参数验证
  stopifnot(is.data.frame(data))
  stopifnot(group_var %in% names(data))
  
  # 核心逻辑
  table <- data %>%
    group_by(across(all_of(group_var))) %>%
    summarise(
      n = n(),
      mean_age = mean(age, na.rm = TRUE)
    )
  
  return(table)
}
```

#### Python 代码

- 使用 `snake_case` 命名变量和函数
- 使用 `UPPER_SNAKE_CASE` 命名常量
- 添加 docstring 说明功能
- 使用类型注解

```python
def profile_data(data: pd.DataFrame) -> dict:
    """生成数据画像
    
    Args:
        data: 输入数据框
        
    Returns:
        包含数据统计信息的字典
    """
    return {
        'shape': data.shape,
        'dtypes': data.dtypes.to_dict()
    }
```

### 提交规范

#### Commit Message 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

#### 示例

```
feat(analysis): 添加生存分析模块

- 实现 Kaplan-Meier 曲线
- 实现 Cox 回归分析
- 添加 Log-rank 检验

Closes #123
```

## 贡献流程

### 1. 报告 Bug

使用 GitHub Issues 报告 Bug，包含：

- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息

### 2. 提交代码

```bash
# 1. 确保代码符合规范
Rscript tests/test_all.R

# 2. 提交更改
git add .
git commit -m "feat(analysis): 添加生存分析模块"

# 3. 推送到远程
git push origin feature/your-feature-name

# 4. 创建 Pull Request
```

### 3. Pull Request 规范

PR 描述应包含：

- 变更说明
- 相关 Issue 编号
- 测试结果
- 截图（如适用）

## 开发环境

### 推荐工具

- **R**: RStudio 或 VS Code + R 扩展
- **Python**: VS Code + Python 扩展
- **Git**: GitHub Desktop 或命令行
- **编辑器**: VS Code

### 调试技巧

```r
# R 调试
options(error = recover)  # 错误时进入调试
browser()                  # 设置断点

# 查看函数定义
args(function_name)
body(function_name)
```

```python
# Python 调试
import pdb; pdb.set_trace()  # 设置断点

# 使用 logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 项目结构

```
clinpub/
├── commands/          # 用户命令入口
├── agents/            # AI Agent 角色卡片
├── pipeline/          # 管线配置
│   ├── workflows/     # 阶段编排
│   ├── references/    # 参考文档
│   ├── templates/     # 模板文件
│   └── contexts/      # 上下文配置
├── scripts/           # 工具脚本
├── hooks/             # Claude Code Hooks
├── docs/              # 文档
├── examples/          # 示例数据
└── tests/             # 测试文件
```

## 发布流程

### 版本号规范

使用语义化版本：`MAJOR.MINOR.PATCH`

- `MAJOR`: 不兼容的 API 变更
- `MINOR`: 向后兼容的功能添加
- `PATCH`: 向后兼容的 Bug 修复

### 发布步骤

```bash
# 1. 更新版本号
npm version patch  # 或 minor, major

# 2. 更新 CHANGELOG
# 手动编辑 CHANGELOG.md

# 3. 提交并推送
git push origin main --tags

# 4. 发布到 npm
npm publish
```

## 社区

### 沟通渠道

- **GitHub Issues**: Bug 报告和功能请求
- **GitHub Discussions**: 一般讨论和问题

### 行为准则

- 尊重他人
- 建设性反馈
- 包容不同观点
- 专注技术讨论

## 常见问题

### 如何添加新的分析方法？

1. 在 `pipeline/templates/study_types/` 添加模板
2. 在 `agents/analyst-agent.md` 添加方法说明
3. 在 `pipeline/references/analysis_methods.md` 添加文档
4. 添加测试用例

### 如何添加新的 Agent？

1. 在 `agents/` 创建 Agent 角色卡片
2. 更新相关 Workflow 的 Agent 引用
3. 在 `pipeline/references/agent-contracts.md` 添加契约
4. 添加集成测试

### 如何修改质量门控？

1. 在 `pipeline/references/gates.md` 修改门控规则
2. 更新相关 Workflow 的检查逻辑
3. 添加测试验证门控行为
