# 终稿拼接协议 (Concatenation Protocol)

> Phase 3: 各段独立撰写完成后，执行本协议合并为终稿。
> 原则：拼接而非重写（WRITE-02），引用统一整理，占位符替换。
> 前置规范：参见 `pipeline/references/reference-library.md` 获取引用库 JSON schema、占位符正则模式和 Vancouver 格式规范。

## 输入输出

### 输入（由分段撰写流程 `sequential_section_writing` 产生）

| 文件 | 来源 |
|------|------|
| `05_Manuscript/sections/01-introduction.md` | writer-agent 撰写 |
| `05_Manuscript/sections/02-methods.md` | writer-agent 撰写 |
| `05_Manuscript/sections/03-results.md` | writer-agent 撰写 |
| `05_Manuscript/sections/04-discussion.md` | writer-agent 撰写 |
| `Reference/reference_library.json` | reference-agent 逐段更新 |

### 输出

| 文件 | 说明 |
|------|------|
| `05_Manuscript/manuscript.md` | 完整终稿（YAML frontmatter + 合并且重编号） |
| `05_Manuscript/sections/*.md` | 各段独立文件（保留原始文件，不做修改，与 manuscript.md 内的段内容一致） |

---

## 拼接步骤

### Step 1: 段落合并

按 IMRAD 顺序读取各段文件并拼接：

```
merged_content = ""
for section in [introduction, methods, results, discussion]:
    filepath = "05_Manuscript/sections/{序号}-{段名}.md"
    content = read(filepath)
    merged_content += content + "\n\n"
```

段间用一个空行分隔。不修改原文内容——拼接而非重写（WRITE-02）。

各段 IMRAD 顺序（引入到 discussion，与撰写顺序 D-01 一致）：
1. Introduction（01-introduction.md）
2. Methods（02-methods.md）
3. Results（03-results.md）
4. Discussion（04-discussion.md）

注意：不包含 Abstract——Abstract 在 manuscript.md 完成后由 writer-agent 最后撰写（遵循 writer-agent.md 的 `draft_abstract` 步骤）。

### Step 2: 占位符替换

扫描全文中所有占位符，按以下规则替换：

#### 2a. Table/Figure 全局编号（D-12）

Table 和 Figure 各自独立编号，按 IMRAD 段顺序扫描：

```
table_counter = 1
figure_counter = 1

for section in [introduction, methods, results, discussion]:
    content = sections[section]
    
    # 替换 Table 占位符
    while content contains {{Table:\d+}}:
        replace {{Table:N}} → Table {table_counter}
        table_counter += 1
    
    # 替换 Figure 占位符
    while content contains {{Figure:\d+}}:
        replace {{Figure:N}} → Figure {figure_counter}
        figure_counter += 1
```

**示例**:
- Methods 段 `{{Table:1}}` → 全文第 1 个 Table → `Table 1`
- Results 段 `{{Table:1}}` → 全文第 2 个 Table（Methods 已有 Table 1）→ `Table 2`
- Results 段 `{{Figure:1}}` → 全文第 1 个 Figure → `Figure 1`

#### 2b. Supplementary Table/Figure 编号

与 Table/Figure 一样独立编号，按出现顺序：
```
supp_table_counter = 1
supp_figure_counter = 1
```
处理方式同主 Table/Figure。

#### 2c. Method 引用替换

```
方法引用映射:
- {{Method:BaselineTable}} → "the baseline characteristics analysis (as described in Methods)"
- {{Method:TwoGroupComparison}} → "the two-group comparison analysis"
- {{Method:SurvivalAnalysis}} → "the survival analysis"
- {{Method:CorrelationAnalysis}} → "the correlation analysis"
- {{Method:SubgroupAnalysis}} → "the subgroup analysis"

默认规则: {{Method:CamelCaseName}} → "the {Name in lowercase} analysis"
```

从 `project_config.yml` 的 `analysis_plan.waves[*].methods[*].id` 读取分析方法名列表，建立映射。

#### 2d. Section 交叉引用替换

```
{{Section:methods}} → "Methods"
{{Section:results}} → "Results"
{{Section:introduction}} → "Introduction"
{{Section:discussion}} → "Discussion"
```

### Step 3: 引用统一编号

引用重编号是拼接的核心——这是 WRITE-02 的"引用在合并时统一整理"。

#### 3a. 扫描全文收集引用

```python
# 扫描正文中所有 [id] 引用标记，如 [1], [2,3], [1-3], [1,4,7]
# 提取所有 unique 的引用 ID
# 从 Reference/reference_library.json 读取每个 ID 对应的引用条目

citation_map = {}  # old_id -> new_id (sequential)

# 按正文出现顺序收集所有引用 ID
all_ids = []
for match in regex_find_all(/\[(\d+(?:[-,]\d+)*)\]/):
    ids = parse_id_group(match)  # [1,4,7] → [1,4,7], [1-3] → [1,2,3]
    for id in ids:
        if id not in all_ids:
            all_ids.append(id)

# 分配连续编号
for i, old_id in enumerate(all_ids):
    citation_map[old_id] = i + 1  # [1] 开始
```

#### 3b. 替换正文中所有引用编号

```python
for each [old_id] in manuscript:
    new_id = citation_map[old_id]
    replace [old_id] → [new_id]
    
# 处理组合: [1,2,3] → 如果新编号分别为 [4,5,6]
# 组合编号在替换后重新格式化，保持原有分组
# [1-3] → [new(1)-new(3)], [1,4,7] → [new(1),new(4),new(7)]
```

#### 3c. 生成 References 区

```python
# 按新编号顺序生成 References 列表
references_section = "## References\n\n"

for new_id in 1..len(all_ids):
    old_id = reverse_map[new_id]
    entry = library.references[old_id]
    
    # Vancouver 格式: [N] Authors. Title. Journal. Year;Vol(Issue):Pages. doi:DOI
    authors = format_authors(entry.authors)  # "Author A, Author B, et al."
    ref_text = f"[{new_id}] {authors}. {entry.title}. {entry.journal}. {entry.year}"
    if entry.volume:
        ref_text += f";{entry.volume}"
        if entry.issue:
            ref_text += f"({entry.issue})"
    if entry.pages:
        ref_text += f":{entry.pages}"
    ref_text += f". doi:{entry.doi}\n"
    
    references_section += ref_text
```

#### 3d. 去重处理（D-07, D-09）

同一引用在多个段落出现使用同一新编号，自然完成去重。`reference_library.json` 已经保证了库级别的去重（citation_key 主键），拼接时只做编号重排以保持连续性。

### Step 4: 生成 YAML Frontmatter（D-16）

```yaml
---
title: ""  # 由用户在最终审阅时填写
target_journal: ""  # 从 project_config.yml 读取
word_count: 0  # 由协议自动计算（正文 + 参考文献字数）
reference_count: 0  # 引用条目总数
---
```

计算方式：
- `target_journal` → `project_config.yml` 的 `target_journal` 字段
- `word_count` → 统计合并后正文（不含 YAML frontmatter 和 References 部分）的字数：
  - `zh-CN` 模式：中文字符数 + 英文单词数
  - `en-US` 模式：英文单词数
  - 语言模式从 `project_config.yml` 的 `language.manuscript` 读取
- `reference_count` → 最终 References 区的条目总数

### Step 5: 合并输出

最终 manuscript.md 结构：

```markdown
---
title: ""
target_journal: ""
word_count: 0
reference_count: 0
---

# {Title from project_config.yml 或留空}

## Introduction

{Introduction 段内容，引用已重编号为 [1] 开始}

## Methods

{Methods 段内容}

## Results

{Results 段内容}

## Discussion

{Discussion 段内容}

## References

[1] Author A, ...  (Vancouver 格式)
[2] Author B, ...
...
```

### Step 6: 更新 MANIFEST.yaml（D-15）

在 `05_Manuscript/MANIFEST.yaml` 写入（参考 manifest-format.md）：

```yaml
agent: writer-agent
phase: 3
type: manuscript
outputs:
  - directory: 05_Manuscript/
    files:
      - name: manuscript.md
        format: md
      - name: sections/01-introduction.md
        format: md
      - name: sections/02-methods.md
        format: md
      - name: sections/03-results.md
        format: md
      - name: sections/04-discussion.md
        format: md
handoffs:
  - consumer: clinpub-verifier
    required_files:
      - 05_Manuscript/manuscript.md
    required_quality:
      - "all citations have DOIs"
      - "IMRAD structure complete (5 sections: I/M/R/D + References)"
      - "word_count > 5000"
      - "reference_count >= 20"
```

### Step 7: 更新引用库

拼接后更新 `Reference/reference_library.json`：
- 追加 `"concatenated": true` 标记
- 更新 `"last_updated"` 时间戳
- 可选的 `"final_reference_count"` 字段记录最终引用数

---

## 验证检查清单

拼接完成后验证：

- [ ] 各段内容完整引入，无段落遗漏
- [ ] `{{Table:\d+}}` 和 `{{Figure:\d+}}` 全部替换，无残留占位符（regex scan 确认）
- [ ] `{{Method:\w+}}` 全部替换
- [ ] Table/Figure 编号连续无跳跃（1,2,3... 非 1,3,5）
- [ ] 引用编号从 [1] 开始连续
- [ ] References 区每个条目对应正文中出现的引用
- [ ] YAML frontmatter 字段非空
- [ ] word_count > 5000
- [ ] reference_count 正确
- [ ] MANIFEST.yaml 声明了所有输出文件
- [ ] 05_Manuscript/sections/ 下各段文件保留
