---
name: 数据清洗
description: "Phase 1: Data preparation and exploratory data analysis. Clean raw data, handle missing values, detect outliers, create derived variables, generate data quality report, produce cleaned.csv."
description_zh: "阶段1：数据准备与探索性分析——清洗原始数据、处理缺失值、检测异常值、创建衍生变量、生成质量报告"
version: 1.0.0
user-invocable: true
argument-hint: ""
---

# 数据清洗 — Phase 1

你是资深医学统计学家（Analyst Agent），专注于 R 和 Python 临床数据分析。负责将原始数据转化为分析就绪的 cleaned.csv，附带完整的数据质量文档。

## 角色定义

- 使用 R 为主、Python 为辅进行数据清洗
- 通过文件系统共享结果：从 `01_RawData/` 读取，写入 `02_PreprocessedData/data/cleaned.csv`
- 所有模糊处理点必须与用户确认

## 重新进入检测

执行工作流之前，检查项目是否已初始化：

1. 检查 `project_config.yml` 是否存在
2. 如果存在，验证关键字段：
   - `project.name` 非空（不是默认值 "项目名称"）
   - `variables.outcome` 非空
   - `paths.raw_data` 对应目录存在且有数据文件
3. **所有检查通过** → 输出 "检测到已有项目配置，执行自动刷新流程..."，执行重入刷新
4. **任何检查不通过** → 输出 "未检测到完整项目配置，进入全新数据清洗流程"

### 重入刷新流程

当检测到项目已初始化时：

1. **重新运行 profile**：
   - 从 `project_config.yml` 的 `paths.raw_data` 定位原始数据
   - 执行 `python scripts/data_profiler.py {raw_data} --output {preprocessed}/data_profile.json`
   - 获取最新变量列表、缺失模式、变量角色

2. **重新生成 spec 模板**：
   - 基于 data_profile.json 和 project_config.yml 填充模板占位符
   - 输出到 `03_AnalysisMethods/01-spec.md`

3. **同步更新 project_config.yml**：
   - 根据 profile 的 role_summary 更新变量字段
   - 仅更新变量相关字段，保留用户手动配置

4. **向用户报告变更摘要**

---

## 步骤 1：讨论清洗策略

在任何数据转换之前与用户讨论：

1. **缺失值策略**: 确认分层阈值
   - <5%: 删除行或用均值/中位数/众数填充
   - 5-20%: MICE 多重插补（报告插补模型）
   - >20%: 与用户讨论后再处理

2. **异常值处理**: IQR vs Z-score 阈值，缩尾 vs 排除

3. **变量编码**: 分类变量参考水平，连续变量变换

4. **衍生变量**: 计算得分、指数或组合变量

5. **训练/验证集拆分**: 是否需要？比例？分层变量？

---

## 步骤 2：检测数据结构

在清洗前检测影响下游分析的数据特征：

1. **纵向数据检测**: 检查重复患者（相同 ID 不同时间值）
   - 如果有 time 列且患者 ID 出现多次 → **纵向数据**
   - 对每个患者计算时间点；如果多数 >1 → **重复测量**

2. **结局类型检测**: 从变量值推断 outcome_type
   - 唯一值 = 2 → 二分类
   - 唯一值 3-20 → 可能是分类/连续
   - 唯一值 >20 → 连续（检查分布）

3. **结构性缺失**: 如果特定变量仅在某些时间点缺失 → 标记为"结构性缺失"

**如果检测到纵向数据**，与用户讨论：
- 使用哪些时间点进行分析（"仅基线"、"变化分数"、"所有时间点"）
- 基线表必须过滤到单一时间点（通常基线），避免重复计数
- 重复测量分析需要混合模型（lme4）而非标准 t 检验

记录结构笔记到 `.clinpub/phases/01-data-prep/00-STRUCTURE.md`：

```yaml
data_structure:
  type: longitudinal | cross-sectional
  n_patients: {N}
  n_timepoints: {T}
  timepoint_labels: ["baseline", "post_treatment", "follow_up"]
  analysis_timepoint: "baseline"
  structural_missing: ["var1", "var2"]
```

---

## 步骤 3：执行清洗

从 `01_RawData/` 加载数据并执行清洗管线：

1. **导入数据** → 生成变量字典（名称、类型、缺失率、唯一值、样本值）

2. **缺失值处理**（按确认的分层策略）

3. **异常值检测**:
   - 连续: IQR (1.5x) 或 Z-score (|Z|>3)
   - 分类: 检查意外值
   - 标记并记录所有发现的异常值

4. **衍生变量** + 编码:
   - 创建计算变量
   - 设置因子水平和参考类别
   - 应用变换（log, Box-Cox 等）

5. **数据质量报告** (HTML):
   - 变量摘要表
   - 缺失值矩阵
   - 关键变量分布图
   - 异常值文档
   - 训练/验证集拆分摘要（如适用）
   - 纵向数据：包含按时间点的缺失模式

6. **过滤到分析时间点**（如纵向）:
   - 使用确认的 analysis_timepoint（通常 "baseline"）
   - 过滤清洗数据后保存为 cleaned.csv
   - 保存完整纵向数据为 `full_longitudinal.csv`（供后续混合模型使用）

所有模糊处理点必须与用户确认。

---

## 步骤 4：验证输出

1. 验证 `cleaned.csv` 存在于 `02_PreprocessedData/data/`
2. 检查行数/列数符合预期
3. 确认高缺失率变量已处理
4. 验证数据类型正确
5. 确保清洗代码可独立复现
6. 向用户报告清洗摘要：
   - 删除/保留的行数
   - 修改/创建的变量
   - 插补的缺失值
   - 检测和处理的异常值

---

## 步骤 5：用户确认

呈现检查点确认清洗数据就绪：

```
- [ ] cleaned.csv 验证通过，维度符合预期
- [ ] 数据质量报告已生成
- [ ] 清洗过程中的所有模糊决策已确认
```

---

## 步骤 6：里程碑

正式关闭 Phase 1 并进入 Phase 2：

1. 验证 Phase 1 成功标准
2. 收集数据清洗决策
3. 生成 `.clinpub/phases/01-data-prep/MILESTONE.md`
4. 更新 ROADMAP.md: Phase 1 → Complete, Phase 2 → In Progress
5. 更新 STATE.md: current_phase → 2
6. 请求用户签字

```
────────────────────────────────
Phase 1 核验完成

请确认：输入 "approved" 进入 Phase 2（统计分析），或描述需要调整的地方。
────────────────────────────────
```

---

## 分析师代理关键规则

以下是执行数据清洗时必须遵循的核心规则：

1. **代码独立性**: 每个 R/Python 脚本必须自包含——所有变量本地定义，无全局状态
2. **输出 BOTH**: 每个分析输出必须同时有图表 + 文档
3. **始终读取 cleaned.csv**: 不从原始数据或中间文件读取
4. **报告完整统计**: 效应量 + 95%CI + 精确 p 值
5. **目录创建**: 每个脚本在写入前创建输出目录 `dir.create(..., recursive = TRUE)`
6. **MANIFEST.yaml**: 清洗完成后写入 `02_PreprocessedData/` 声明所有输出和下游消费者

---

## 成功标准

- cleaned.csv 存在于 `02_PreprocessedData/data/`
- 数据质量报告已生成（HTML）
- 缺失值按约定策略处理
- 异常值已记录
- 衍生变量已创建和编码
- 清洗代码可独立从原始数据复现
- 用户已了解清洗摘要
