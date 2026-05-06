# SCI Q1/Q2 期刊发表标准参考

## 目标期刊

- **Alzheimer's & Dementia** (IF ~14)
- **Molecular Psychiatry** (IF ~11)

## 方法学要求

- 统计效力分析（power analysis）必须事先报告
- 多中心/多队列设计优先于单中心
- 纵向设计优先于横断面
- 使用经过验证的量表和工具
- 盲法、随机化、对照组必须清晰记录

## 报告规范

| 研究类型 | 报告规范 | 说明 |
|---------|---------|------|
| RCT | CONSORT | 必须附 checklist |
| 观察性研究 | STROBE | 必须附 checklist |
| Meta 分析 | PRISMA | 必须附流程图 |
| 预测模型 | TRIPOD | 必须附 checklist |

- 临床试验必须在 ClinicalTrials.gov 注册
- 参考 EQUATOR Network 指南

## 统计报告要求

- **效应量 + 95% CI**：必须与 p 值一同报告
- **精确 p 值**：报告具体数值，不只写 "p < 0.05"
- **多重比较校正**：FDR / Bonferroni（神经影像、遗传学、多结局研究必须）
- **软件版本**：报告 R/Python 版本及关键包版本
- **假设检验**：报告正态性、方差齐性、比例风险假设等检验结果
- **数据公开**：Molecular Psychiatry 强调 open data/code

## 新颖性与影响力

- 拒绝增量性发现，需要明确的新颖性（新机制、新生物标志物、新临床范式）
- 转化价值至关重要：将发现与临床实践或疾病机制联系
- Alzheimer's & Dementia 优先：生物标志物发现/验证、临床试验结果、流行病学洞察
- Molecular Psychiatry 优先：机制深度、分子/遗传发现、跨疾病相关性

## 常见拒稿原因

1. 样本量小/统计效力不足
2. 新颖性不足
3. 从观察性数据过度推论
4. 关键混杂因素未调整（年龄、性别、APOE、教育程度）
5. 报告规范不完整
6. Methods 部分薄弱/不完整

## 图表技术规范

<!-- FIGURE_DPI is the canonical source for figure resolution across all clinpub artifacts. -->
<!-- When this value changes, r_patterns.md::PUBLICATION_DPI must be updated to match. -->

| 参数 | 值 | 说明 |
|------|-----|------|
| **FIGURE_DPI** | **300** | 所有图表的最低分辨率，R/Python 代码中通过 `PUBLICATION_DPI` 引用 |

### 图表要求

- 分辨率 ≥300 DPI（见上表 FIGURE_DPI）
- 矢量格式优先（PDF/SVG）
- 不接受 Excel 默认图表
- Meta 分析必须有 PRISMA 流程图和森林图
- 限制 6 个图/表（除非有充分理由）

## 写作要点

- Results 以主要结局开头，不要埋没关键发现
- 写结构化摘要——很多审稿人仅凭摘要做决定
- Discussion 聚焦：临床意义 > 统计学意义
- Cover letter 明确说明新颖贡献
- 建议 3-5 位合适的审稿人
- 声明所有利益冲突
