---
name: 选题挖掘
description: "Topic mining from clinical data tables with PubMed gap analysis"
description_zh: "从临床数据表（CSV/XLSX）出发，分析变量结构与文献空白，生成3-5个候选研究课题及可行性评分"
version: 1.0.0
user-invocable: true
argument-hint: "<数据文件路径>"
---

# 选题挖掘

从临床数据表出发，通过变量画像和 PubMed 文献空白扫描，发现 3-5 个候选研究课题。

**不涉及统计分析或论文写作——仅做选题发现。**

## 执行流程

### 步骤 1：数据画像

读取用户提供的 CSV 或 XLSX，生成综合数据画像：

```bash
python scripts/data_profiler.py <filepath> --output idea/data_profile.json
```

画像内容：

1. **变量清单**：名称、数据类型、缺失率、唯一值数
2. **分布摘要**：连续变量五数概括（Min/Q1/Median/Q3/Max），分类变量频率
3. **缺失模式**：高缺失（>20%）标记、中缺失（5-20%）提示
4. **相关矩阵**：数值变量 Spearman 相关（>30列时警告）
5. **变量角色检测**（自动推断）：

| 角色 | 名称模式 |
|------|----------|
| 结局变量 | outcome, 结局, diagnosis, status, death, event |
| 暴露/分组 | group, treatment, arm, exposure, 暴露, trt, 随机 |
| 时间变量 | time, follow, survival, months, days, 随访 |
| 协变量 | age, sex, gender, bmi, smoke 等 |
| 生物标志物 | biomarker, 蛋白, gene, serum, plasma, score 等 |

6. **研究类型预测**：

| 数据特征 | 建议设计 |
|----------|----------|
| 随机分组 + 基线 + 随访数据 | RCT |
| 事件时间 + 暴露分组 | 队列研究 |
| 病例/对照 + 匹配ID | 病例对照 |
| 单一时间点 + 暴露 + 结局 | 横断面 |
| 仅描述性变量，无分组 | 描述性 |
| 多个生物标志物 + 结局 | 标志物组合/诊断 |

7. **样本量评估**：

| 样本量 | 建议 |
|--------|------|
| <50 | 仅描述性 |
| 50-200 | 简单比较或描述性 |
| 200-500 | 可进行回归分析 |
| 500-2000 | 大多数分析方法适用 |
| >2000 | 复杂建模 + 亚组分析 |

向用户展示画像，确认变量角色后再继续。

### 步骤 2：并行文献扫描

基于数据画像，按变量组分派并行 PubMed 检索。

#### 阶段 1：变量分组

从 `idea/data_profile.json` 提取可检索的变量组：

1. **疾病背景**：用户描述 + 变量名 -> 基础疾病关键词
2. **生物标志物/暴露变量**：每个检测到的标志物或暴露 -> 一个检索任务
3. **结局变量**：结局相关检索
4. **组合检索**：前 2-3 个变量对（如标志物 + 结局）-> 交叉参考检索

跳过患病率 <5% 或纯描述性（ID、日期）的变量。

#### 阶段 2：并行检索

每个检索任务执行：

1. 运行 PubMed 检索脚本：
   ```bash
   python scripts/ncbi_search.py "<检索词>" --db pubmed --years 5 --max 20
   ```
2. 统计近 5 年相关论文数
3. 识别前 3 篇高影响力论文（期刊、年份）
4. 判断发表趋势：上升/下降/稳定
5. 识别研究空白：尚未研究的内容

返回结构化摘要：
- 变量名
- 使用的检索词
- 近 5 年论文数
- 代表性论文：[PMID, 标题, 期刊, 年份]
- 发表趋势：上/下/稳
- 发现的空白：一句话描述
- 新颖度评分：高/中/已充分研究

#### 阶段 3：汇总结果

1. 汇总所有摘要到 `idea/literature_scan.md`
2. 交叉参考各变量空白——识别**复合新颖性**（变量 A 单独有研究，变量 B 单独有研究，但 A+B 从未组合）
3. 按新颖度排序
4. 标记已充分研究的变量——建议差异化策略

### 步骤 3：生成候选课题

综合数据画像 + 文献扫描，生成 3-5 个候选课题：

**选题策略**：
- 大样本（>5000行）-> 优先队列或 RCT
- 多标志物（>10个）-> 优先标志物组合或 LASSO
- 无分组/结局变量 -> 仅描述性研究
- 用户指定方向 -> 优先匹配

**每个课题包含**：
- 工作标题
- 可行性评分（1-5星）
- 研究类型（队列/RCT/横断面/病例对照/诊断/描述性）
- 核心研究问题 + 假设
- 变量映射（结局、暴露、协变量、亚组）
- 拟采用的分析方法
- 需要的关键图表
- 新颖性/空白理由
- 推荐目标期刊
- 风险提示（样本量、混杂、变量局限）

**每个课题结构**：

```markdown
## 课题 N：<工作标题>

**可行性**：<N>星（1-5）
**类型**：队列 / RCT / 横断面 / 病例对照 / 诊断 / 描述性

### 研究问题与假设
一句话核心问题 + 具体统计假设。

### 变量映射
- **结局**：<变量> — 描述
- **暴露/分组**：<变量> — 描述
- **协变量**：<变量列表>
- **亚组**：<变量>（如适用）

### 拟采用的分析方法
- 主要统计方法
- 辅助敏感性分析
- 需生成的图表

### 新颖性 / 研究空白
- 创新点（人群？标志物？关联？方法？）

### 推荐目标期刊
- 期刊名 + 理由 + 难度评估

### 风险与注意事项
- 变量局限、混杂风险、样本量充分性
```

写入完整报告到 `idea/选题报告.md`。末尾包含所有课题的对比排序表。

### 步骤 4：选题后引导

用户选定课题后：

1. 生成 `idea/to_project_config.yml`，映射选题结果到项目配置
2. 用户确认变量映射和分析方法
3. 引导用户将文件重命名为 `project_config.yml` 并启动管线

**字段映射**：

| 选题字段 | 配置字段 |
|----------|----------|
| 研究问题与假设 | project.description |
| 类型 | project.design |
| 变量映射 -> 结局 | variables.outcome |
| 变量映射 -> 暴露/分组 | variables.exposure / variables.group_variable |
| 变量映射 -> 协变量 | variables.covariates |
| 拟采用方法 | methods_to_run |
| 目标期刊 | project.target_journal |

**各研究类型默认方法**：

| 研究类型 | 默认方法 |
|----------|----------|
| 队列 | BaselineTable, GroupComparison, LogisticRegression, SurvivalAnalysis, SubgroupAnalysis |
| RCT | BaselineTable, GroupComparison, LogisticRegression, SubgroupAnalysis, SensitivityAnalysis |
| 病例对照 | BaselineTable, GroupComparison, LogisticRegression, ROCAnalysis |
| 横断面 | BaselineTable, GroupComparison, LogisticRegression, CorrelationAnalysis |
| 描述性 | BaselineTable, GroupComparison, CorrelationAnalysis |
| 诊断/标志物 | BaselineTable, GroupComparison, ROCAnalysis, MarkerPanel, SimpleML |

## 关键规则

- 不做统计分析——仅画像（分布、计数、缺失率）
- 每个课题必须通过 PubMed 初步检索验证
- 变量角色自动检测仅供参考——用户必须确认
- 不得捏造变量或数据特征
- 如实报告数据能力——如果数据不支持某类选题，直接说明
- 不得覆盖已有 `project_config.yml`——始终写入 `idea/to_project_config.yml`
- 无法确定的配置字段标记 `# TODO: user confirmation needed`

## 成功标准

- 数据画像生成（变量清单、缺失报告、研究类型预测、样本量评估）
- 文献扫描完成含空白分析（新颖度标注）
- 3-5 个候选课题含可行性评分、变量映射和目标期刊
- 课题对比排序表
- 用户已选定课题（或返回优化）
- `idea/to_project_config.yml` 生成含变量映射、方法和期刊推荐
- 用户了解后续步骤

## 参考资料

- [选题挖掘工作流](references/data2idea-workflow.md)
- [选题挖掘专家指南](references/topic-miner-guide.md)
- [研究类型模板](../知识库/references/templates/study_types/)
