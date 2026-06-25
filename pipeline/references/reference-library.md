# Reference Library 规范和交叉引用约定

> Phase 3 spec: 分段撰写时管理文献引用和段间交叉引用的统一规范。
> Writer Agent 和 Reference Agent 共同遵守。

## 文件位置

- **引用库文件**: `Reference/reference_library.json`（工作流运行时生成/更新）
- **本规范文档**: `pipeline/references/reference-library.md`

---

## 1. Shared Reference Library

### 1.1 JSON 整体结构

```json
{
  "version": "1.0",
  "last_updated": "2026-05-07",
  "references": [
    {
      "id": 1,
      "citation_key": "Author2024",
      "title": "Article Title",
      "authors": ["Author A", "Author B", "Author C"],
      "journal": "Journal Name",
      "year": 2024,
      "volume": "10",
      "issue": "3",
      "pages": "100-110",
      "doi": "10.xxx/xxxxx",
      "pmid": "12345678",
      "sections_used": ["introduction", "discussion"],
      "added_by_section": "introduction",
      "citation_reason": "Supports the association between X and Y",
      "abstract": "Full abstract text of the article, obtained from PubMed EFetch. Used by writer-agent for accurate citation context and by reference-agent for relevance filtering."
    }
  ]
}
```

### 1.2 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `id` | 是 | 全局唯一编号，Vancouver 正文编号 [id]。只增不减，删除保留 ID 但标记删除 |
| `citation_key` | 是 | BibTeX 风格 key（AuthorYear），用于去重判断 |
| `title` | 是 | 论文标题 |
| `authors` | 是 | 作者列表，首人姓在前名在后，后续人标准格式 |
| `journal` | 是 | 期刊名缩写或全称 |
| `year` | 是 | 发表年份 |
| `volume` | 否 | 卷号（无则留空） |
| `issue` | 否 | 期号（无则留空） |
| `pages` | 否 | 页码（无则留空） |
| `doi` | 是 | DOI。无 DOI 的引用标记为 `pending_doi`，由用户提供 |
| `pmid` | 否 | PubMed ID |
| `sections_used` | 是 | 该引用被哪些段引用的列表（["introduction", "discussion"]）。去重时检查此字段 |
| `added_by_section` | 是 | 首次添加该引用的段落名称 |
| `citation_reason` | 是 | 引用此文献的原因描述 |
| `abstract` | 是 | 论文摘要全文。从 PubMed EFetch 获取（通过 `pubmed_fetch.py`）。writer-agent 用于精准引用上下文，reference-agent 用于相关性筛选。无法获取时标记为 `"abstract": "pending"` |

### 1.3 每次写入引用库的规则（D-09）

1. **查询在先**: 添加新引用前，先搜索 `reference_library.json` 的 `citation_key`（AuthorYear）字段
2. **复用编号**: 如果 `citation_key` 已存在 → 复用其 `id`，在 `sections_used` 追加当前段落名。不做重复条目
3. **追加新条目**: 如果 `citation_key` 不存在 → 分配下一个最大 `id+1`，追加到库中
4. **去重键策略**: 以 `citation_key`（AuthorYear）为主键。如果不同论文同 AuthorYear（极少数重复引用场景），加后缀区分：`Author2024a`, `Author2024b`
5. **DOI 必填**: 任何无 DOI 的引用标记为 `pending_doi` 并在段落末尾标注 ⚠️。不可跳过
6. **摘要必填**: 每条新引用必须包含 `abstract` 字段。获取方式：对有 PMID 的文献，调用 `pubmed_fetch.py` 获取完整摘要（EFetch XML）；对无 PMID 但有 DOI 的文献，通过 DOI 解析获取摘要文本。无法获取时标记为 `"abstract": "pending"`，由后续补充搜索或用户手动补全

---

## 2. Vancouver 引用格式

### 2.1 正文内引用（D-08）

使用上标或方括号编号：

- 单篇：`[1]`, `[2]`
- 多篇连续：`[1-3]`
- 多篇不连续：`[1,4,7]`
- 作者融入正文：`Smith et al. [1] reported that...`

### 2.2 末尾 References 区格式（D-07）

末尾统一 References 区，格式如下（Vancouver 风格）：

```
References

[1] Author A, Author B, Author C. Title of the article. Journal Abbreviation. 2024;10(3):100-110. doi:10.xxx/xxxxx
[2] Author D, Author E. Another title. Journal Name. 2023;15(2):50-60. doi:10.yyy/yyyyy
```

### 2.3 段落引用量指南（D-10）

| 段落 | 建议引用数 | 说明 |
|------|-----------|------|
| Introduction | 10-15 篇 | 背景(3-5) + 已知证据(3-5) + gap(2-3) + 目的(1) |
| Methods | 3-5 篇 | 方法学来源、已发表协议、诊断标准引用 |
| Results | 0-3 篇 | 仅当结果需要与已有文献对比时引用 |
| Discussion | 15-25 篇 | 对比(8-12) + 机制(3-5) + 临床意义(2-3) + 局限(1-2) |

---

## 3. 交叉引用占位符

### 3.1 占位符命名规则（D-11）

各段撰写时使用以下占位符格式，终稿拼接时统一替换为真实编号：

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{{Table:N}}` | 表格 N (N 为顺序号) | `{{Table:1}}`, `{{Table:2}}` |
| `{{Figure:N}}` | 图 N (N 为顺序号) | `{{Figure:1}}`, `{{Figure:2}}` |
| `{{SupplementaryTable:N}}` | 补充表 N | `{{SupplementaryTable:1}}` |
| `{{SupplementaryFigure:N}}` | 补充图 N | `{{SupplementaryFigure:1}}` |
| `{{Method:name}}` | 方法引用（name 为分析方法名） | `{{Method:BaselineTable}}`, `{{Method:SurvivalAnalysis}}` |
| `{{Section:name}}` | 段间引用（跨段交叉引用） | `{{Section:methods}}`, `{{Section:results}}` |

### 3.2 占位符使用规则

1. **主观顺序编号**: 写段时不关心全局编号。在 Methods 的 Table 填 `{{Table:1}}`，在 Results 的 Table 填 `{{Table:2}}` 等。主观编号以段内出现顺序为准
2. **全局重编号**: 拼接时扫描全文所有 `{{Table:N}}`，按 IMRAD 段出现顺序（Methods → Results → Discussion → Intro）重新分配全局编号
3. **Methods 占位符**: Methods 段涉及的分析方法引用用 `{{Method:MethodName}}`，拼接时替换为方法名的真实表述（如 "the baseline characteristics analysis"）
4. **Section 占位符**: 段间交叉引用（如 Discussion 中"详见 Method section"）用 `{{Section:methods}}`，拼接时保留为纯文本
5. **占位符不嵌套**: 不在一个占位符内包含另一个占位符

### 3.3 Table/Figure 全局编号策略（D-12）

Table 和 Figure 各自独立编号，按 IMRAD 顺序：

| 段落顺序 | Table 编号示例 | Figure 编号示例 |
|----------|---------------|-----------------|
| Methods 段第 1 个表 | Table 1 | — |
| Methods 段第 2 个表 | Table 2 | — |
| Results 段第 1 个表 | Table 3 | Figure 1 |
| Results 段第 1 个图 | — | Figure 2 |
| Results 段第 2 个表 | Table 4 | — |

Tables 和 Figures 各自独立递增，不交叉编号。

### 3.4 占位符正则模式（供自动化替换使用）

```
Table:       /{{Table:(\d+)}}/
Figure:      /{{Figure:(\d+)}}/
Method:      /{{Method:(\w+)}}/
Section:     /{{Section:(\w+)}}/
Supplementary Table: /{{SupplementaryTable:(\d+)}}/
Supplementary Figure: /{{SupplementaryFigure:(\d+)}}/
```

---

## 4. Reference Library 读写流程

### 4.1 每段前的操作流程（由 workflow 编排）

每段撰写开始前（D-06 reference-agent pre-search）：

1. Reference Agent 执行文献搜索（参见 `agents/reference-agent.md`）
2. 如果 `Reference/reference_library.json` 不存在 → 创建初始空库 `{"version":"1.0","last_updated":"...","references":[]}`
3. 读取已有库内容
4. 对新找到的引用逐条检查 `citation_key` 去重（规则见 1.3）
5. 对每条新引用获取摘要：通过 `pubmed_fetch.py`（有 PMID 时）或 DOI 解析获取完整摘要文本，写入 `abstract` 字段
6. 新引用分配 `id`（max_id + 1），写入库（含 `abstract` 字段）
7. 更新 `last_updated` 字段
8. 保存 `Reference/reference_library.json`

### 4.2 各段撰写时的引用使用规则（writer-agent）

Writer Agent 写入某段正文时：

1. 阅读 `Reference/reference_library.json` 获取所有引用库条目
2. 对每个要引用的文献，使用 `{{ref:citation_key}}` 标记（如 `{{ref:Smith2024}}`）
3. 段内引用在正文中以 `[id]` 格式使用（如 Previous studies show that... [1,3-5]）
4. 不用关心 `citation_key` 对应的 id 号是否发生变化，拼接时会统一重编号

### 4.3 终稿拼接时的引用处理（由拼接协议执行）

拼接时：

1. 扫描全文所有 `[id]` 引用标记
2. 解析每个编号对应的引用条目（从 `reference_library.json`）
3. 按正文出现顺序重新分配连续编号（从 [1] 开始）
4. 对使用同一引用的不同段落，复用同一编号（自然去重，D-07）
5. 在全文末尾生成 References 区
6. 更新 `reference_library.json` 的 `sections_used`

### 4.4 MANIFEST.yaml 更新

Reference Agent 完成搜索后，更新 `Reference/MANIFEST.yaml`（参见 `pipeline/references/manifest-format.md`）：
- 在 outputs 中加入 `Reference/reference_library.json`
- 在 handoffs 中声明 writer-agent 为消费者

---

## 5. 引用量指南

（D-10 规定：常规学术量）

| 段落 | 数量 | 功能分布 |
|------|------|---------|
| Introduction | 10-15 | 疾病负担 3-5, 现有证据 3-5, gap 2-3, 目的 1 |
| Methods | 3-5 | 方法来源 1-2, 诊断标准 1-2, 统计方法 1 |
| Results | 0-3 | 仅需与已有结果对比时引用 |
| Discussion | 15-25 | 对比讨论 8-12, 机制解释 3-5, 临床意义 2-3, 局限 1-2 |

Reference Agent 搜索时遵循此量级控制，不超标。
writer-agent 写引用时注意段落量级约束。

---

*Created: 2026-05-07*
*Part of Phase 3: 手稿拼接, Plan 02: 引用管理与交叉引用规范*
