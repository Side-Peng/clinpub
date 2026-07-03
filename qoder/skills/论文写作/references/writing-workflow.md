# 论文写作工作流详解

## 目的

以中文（英文图表）撰写完整 IMRAD 论文，目标 SCI Q1/Q2 期刊。支持一键成稿和逐步写作双模式。

## 前置阅读

- `../知识库/references/journal_standards.md` — 期刊标准
- `../知识库/references/checkpoints.md` — 检查点规范
- `../知识库/references/reference-library.md` — 引用库规范
- `../知识库/references/citation-strategy.md` — 引用策略

## 引用策略详解

### 各段引用配比

| 段落 | 默认引用量 | 搜索关键词 |
|------|-----------|-----------|
| Introduction | 10-15 篇 | disease + exposure + outcome + population |
| Methods | 3-5 篇 | methodology + standard guidelines + published protocols |
| Results | 0-3 篇 | 仅在有对比需求时 |
| Discussion | 15-25 篇 | 对比同类研究 + 机制解释 + 临床意义 |

**总量硬约束**: 30-55 篇
**弹性**: 各段 +/-20%

### 搜索过滤参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| max_years_ago | 5 | 最大文献年限 |
| landmark_exceptions | [] | 经典文献例外列表 |
| min_if | null | 最小影响因子（null=不过滤） |

### 引用库管理

共享引用库 `Reference/reference_library.json`：

```json
{
  "references": [
    {
      "id": 1,
      "citation_key": "Smith2024",
      "title": "...",
      "authors": ["Smith A", "Jones B"],
      "journal": "Lancet",
      "year": 2024,
      "doi": "10.1016/...",
      "pmid": "12345678",
      "abstract": "Full abstract text...",
      "section": "introduction",
      "citation_reason": "Establishes disease burden",
      "supported_argument": "Background statistics"
    }
  ]
}
```

**关键规则**:
- 每条记录必须包含 `abstract` 字段
- 新引用逐条去重（检查 citation_key）
- 分配连续 ID（max_id + 1）
- 无 DOI 的引用标记为用户操作项

## 各段撰写上下文

### Introduction

**读取**:
- `Reference/reference_library.json`（已有引用 + 摘要）
- `Reference/citation_map.md`
- `Reference/literature_notes/`

**写作结构** — 漏斗:
1. 广泛背景（疾病负担、临床重要性）
2. 已知证据（已确立的发现）
3. 研究空白（未知或有争议的）
4. 研究目标和假设

### Methods

**读取**:
- `project_config.yml`（study_type, variables）
- study type template
- `03_AnalysisMethods/*/方法说明.md`

**写作要素** — 遵循 STROBE/CONSORT:
- 研究设计和设置
- 人群和抽样
- 变量和定义
- 统计方法
- 软件版本（R, 关键包）

### Results

**读取**:
- `04_Outputs/*/`（所有 figure + table + 方法说明）
- 方法说明中必须有「输出结果」小节

**写作风格**:
- 描述关键发现 + 指向图表
- 不使用 "As shown in Table X" 作为段落开头
- 报告: 效应量 + 95%CI + 精确 p 值
- 主结局在先，次要分析随后

### Discussion

**读取**:
- `Reference/reference_library.json`
- `Reference/citation_map.md`
- `project_config.yml`（target_journal, scope）

**写作结构**:
1. 关键发现总结（开头段）
2. 与既往文献比较
3. 可能机制
4. 临床意义
5. 局限性（诚实但不防御）
6. 结论和未来方向（具体，非 "more research is needed"）

## 占位符系统

### 占位符类型

| 占位符 | 拼接时替换为 |
|--------|-------------|
| `{{Table:N}}` | Table 1, Table 2...（全局编号） |
| `{{Figure:N}}` | Figure 1, Figure 2...（全局编号） |
| `{{SupplementaryTable:N}}` | Supplementary Table 1...（独立编号） |
| `{{SupplementaryFigure:N}}` | Supplementary Figure 1...（独立编号） |
| `{{Method:name}}` | "the {name} analysis" |
| `{{Section:name}}` | 段落名 |

### 编号规则

- 按 IMRAD 顺序全局编号
- Introduction 中首次出现的 Table/Figure 编号最小
- 同一 Table/Figure 在多段引用时复用编号

## 终稿拼接协议

### 1. 段落合并

按顺序读取:
1. `05_Manuscript/sections/01-introduction.md`
2. `05_Manuscript/sections/02-methods.md`
3. `05_Manuscript/sections/03-results.md`
4. `05_Manuscript/sections/04-discussion.md`

### 2. 占位符替换

扫描全文，按 IMRAD 出现顺序分配编号。

### 3. 引用重编号

```
读取 reference_library.json
扫描全文中所有 [id] 引用
按正文出现顺序重新分配 [1], [2], [3]...
同一引用多段出现 → 复用已分配编号
文末生成 References 区（Vancouver 格式）
```

### 4. YAML Frontmatter

```yaml
---
title: "{title}"
target_journal: "{journal}"
word_count: {auto_calculated}
reference_count: {auto_counted}
---
```

### 5. 验证

- 无 `{{Table:\d+}}` 或 `{{Figure:\d+}}` 残留
- word_count > 5000
- reference_count >= 20
- 所有引用有 DOI
- IMRAD 结构完整

## 文献搜索协议

### 搜索工具

使用内置搜索脚本（PubMed E-Utilities）：

```bash
python scripts/ncbi_search.py "<query>" --db pubmed --years {N} --max {N}
```

### 摘要获取

搜索结果使用 ESummary API，不返回摘要。必须额外获取：

```bash
python scripts/pubmed_fetch.py <PMID1> <PMID2> ... --format json
```

将摘要文本写入 `reference_library.json` 的 `abstract` 字段。

### 全文获取

对关键引用：
1. 使用 DOI 通过 Unpaywall 检查开放获取状态
2. 如果 OA 可用：下载 PDF → 提取全文
3. 如果非 OA：请求用户提供 PDF

## Humanizer 详细规则

### 段落流规则

**禁止**:
- bullet-point 式段落
- "第一...第二...最后..." 平行列举
- "it is worth noting", "it is noteworthy", "as is well known"

**要求**:
- 每段一个核心句 + 逻辑推进
- 使用具体逻辑连接词: "This result aligns with Smith et al. (2023), but differs in that..."

### 句子多样性规则

如果 3+ 连续句子共享相同结构，重写：
- 混合短句直接表达
- 带括号插入的句子
- 带破折号或冒号的句子

### 引用整合规则

- 不以 "As shown in Table X" 开头
- 给具体作者上下文: "Smith et al. reported..." 而非 "Studies show..."

### 自检清单

| 检查项 | AI 模式 | 修正 |
|--------|---------|------|
| 段落开头 | 顺序标记 | 内容逻辑 |
| 过渡词 | 重复 Moreover/Furthermore | 具体因果/对比 |
| 句子结构 | 统一 "X is a Y of Z" | 混合句式 |
| 结论 | "More research needed" | 具体方向 |
| 引用 | "Studies show..." | 具体作者 |
| 解释 | 过度解释方法 | 只说做了什么 |

## 成功标准

- IMRAD 完整
- 所有引用有 DOI
- 所有图表在正文中被引用
- STROBE/CONSORT 覆盖
- Humanizer 通过
- 语言一致
- 不编造引用或数据
- 各段 sections/ 文件保留
- 终稿 manuscript.md 存在
- 无残留占位符
- 引用连续编号
- word_count > 5000, reference_count >= 20
