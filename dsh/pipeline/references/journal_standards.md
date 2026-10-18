# 期刊发表标准框架

> 本文件定义 clinpub 的通用期刊发表标准。采用 4 级分层默认标准，适配不同层次期刊的要求。
> 具体期刊要求通过 `project_config.yml` 的 `journal:` 段配置覆盖。

---

## 分级默认标准

### Q1 期刊 (IF > 10)

- **方法创新性**：需要新方法或现有方法的新应用场景
- **补充材料**：完整补充材料（补充表、补充图、代码、数据集）
- **数据共享**：数据可用性声明 + 公开数据集/代码（GitHub/Zenodo）
- **统计要求**：完整敏感性分析、多重比较校正、效力分析
- **报告规范**：严格遵循对应研究类型的报告规范（CONSORT/STROBE/PRISMA/TRIPOD），checklist 必须逐条标注
- **临床试验注册**：ClinicalTrials.gov 或同类注册平台（RCT 必须）
- **参考 EQUATOR Network 指南**

### Q2 期刊 (IF 5-10)

- **方法扎实**：标准方法即可，但需要充分论证方法选择的合理性
- **关键补充**：至少核心补充表和方法代码
- **数据共享**：数据可用性声明（可共享但非强制公开）
- **统计要求**：效应量 + 95%CI + 精确 p 值、基本假设检验
- **报告规范**：遵循报告规范，checklist 附在补充材料

### Q3 期刊 (IF 2-5)

- **标准方法**：标准统计方法即可
- **基础报告**：关键图表和简要补充
- **统计要求**：效应量 + p 值、基本报告
- **报告规范**：参考报告规范但不强制逐条 checklist

### Q4 期刊 (IF < 2)

- **描述性可接受**：描述性研究或小型案例研究可发表
- **简化补充**：按期刊要求提供
- **统计要求**：基础统计报告即可

---

## 报告规范矩阵

| 研究类型 | 报告规范 | 说明 |
|---------|---------|------|
| RCT | CONSORT | 必须附 checklist |
| 观察性研究 | STROBE | 必须附 checklist |
| Meta 分析 | PRISMA | 必须附流程图 |
| 预测模型 | TRIPOD | 必须附 checklist |
| 诊断准确性 | STARD | 必须附 checklist |
| 病例报告 | CARE | 必须附 checklist |

---

## 统计报告通用要求

以下要求适用于所有级别期刊：

- **效应量 + 95% CI**：必须与 p 值一同报告（Q3+ 强制，Q4 推荐）
- **精确 p 值**：报告具体数值，不只写 "p < 0.05"（p < 0.001 除外）
- **多重比较校正**：FDR / Bonferroni（多结局研究、高维数据必须）
- **软件版本**：报告 R/Python 版本及关键包版本
- **假设检验**：报告正态性、方差齐性、比例风险假设等检验结果
- **样本量论证**：Q1/Q2 需要事先 power analysis；Q3 至少说明样本量合理性

---

## 图表技术规范

<!-- FIGURE_DPI is the canonical source for figure resolution across all clinpub artifacts. -->
<!-- When this value changes, r_patterns.md::PUBLICATION_DPI must be updated to match. -->

| 参数 | 值 | 说明 |
|------|-----|------|
| **FIGURE_DPI** | **300** | 所有图表的最低分辨率，R/Python 代码中通过 `PUBLICATION_DPI` 引用 |

### 图表要求

- 分辨率 ≥300 DPI（见上表 FIGURE_DPI）
- 矢量格式优先（PDF/SVG），位图使用 TIFF（LZW 压缩）
- 不接受 Excel 默认图表
- Meta 分析必须有 PRISMA 流程图和森林图
- 图表数量限制：Q1/Q2 通常限制 6 个图/表（除非有充分理由）
- 字体：Arial ≥ 8pt（或等效无衬线字体）
- 色盲友好配色推荐（见 `r_patterns.md` §1.1）

---

## 常见拒稿原因（通用）

1. 样本量小/统计效力不足
2. 新颖性不足（增量性发现）
3. 从观察性数据过度推论因果
4. 关键混杂因素未调整
5. 报告规范不完整（缺少 checklist/流程图）
6. Methods 部分薄弱/不完整
7. 数据分析方法与研究问题不匹配
8. 图表质量不达标
9. 参考文献过时或不相关
10. 语言质量不足（非英语母语期刊）

---

## 写作要点

- Results 以主要结局开头，不要埋没关键发现
- 写结构化摘要——很多审稿人仅凭摘要做决定
- Discussion 聚焦：临床意义 > 统计学意义
- Cover letter 明确说明新颖贡献
- 建议 3-5 位合适的审稿人
- 声明所有利益冲突

---

## AI 工具声明要求（2024-2026 趋势）

越来越多的 SCI 期刊要求作者声明 AI 工具的使用情况。clinpub 用户应在手稿中包含以下声明：

### 声明模板

**中文版（手稿正文末尾或投稿系统）：**
> 在本研究的准备过程中，作者使用了 AI 辅助工具（Claude Code）进行数据清洗、统计分析和手稿润色。所有分析结果均经作者独立审核和验证。作者对文章的全部内容承担最终责任。

**英文版（Cover Letter 或投稿系统）：**
> During the preparation of this work, the author(s) used AI-assisted tools (Claude Code) for data cleaning, statistical analysis, and manuscript polishing. All results were independently reviewed and verified by the author(s). The author(s) take(s) full responsibility for the content of the article.

### 注意事项

- 具体声明措辞以目标期刊的 Author Guidelines 为准
- 部分期刊要求在 Methods 而非 Acknowledgments 中声明
- 部分期刊（如 Nature 系列）有专门的 AI 声明表格
- 投稿前务必查阅目标期刊最新的 AI policy

---

## 期刊自定义覆盖

### 在 project_config.yml 中配置期刊要求

通过 `journal:` 顶级段指定目标期刊及其特定要求：

```yaml
journal:
  name: "Journal Name"          # 期刊名称
  tier: "Q1"                    # Q1/Q2/Q3/Q4 — 决定应用哪级默认标准
  word_limit: 5000              # 正文字数限制
  abstract_limit: 300           # 摘要字数限制
  reference_style: "vancouver"  # 参考文献格式
  figure_limit: 6               # 图表数量限制
  data_sharing: "required"      # 数据共享要求
  specific_requirements: []     # 期刊特定要求（覆盖默认标准）
```

当 `journal.tier` 指定后，系统应用对应级别的默认标准。`journal.specific_requirements` 中的条目可覆盖任何默认值。

如果未配置 `journal:` 段，默认应用 Q2 标准。
