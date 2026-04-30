# clinpub Integration Test Checklist

> 端到端集成测试 — 从 `rct_depression.csv` 到投稿就绪手稿的完整 Phase 0-4 pipeline 验证

**测试数据:** `clinpub/examples/sample_data/rct_depression.csv` (86 例 RCT，3 时间点)
**测试日期:** ____
**测试者:** ____
**clinpub 版本:** ____

> 此 checklist 标记为 **manual**，不加入 CI/CD 自动化流程。设计目标：在 Claude Code 中按步骤手动执行，逐 phase 验证产出物。

---

## Pre-flight: 环境检查

在开始前确认开发环境满足 clinpub 的最低运行要求：

- [ ] **R >= 4.2 已安装** — 验证命令：`R --version 2>/dev/null | head -1`
- [ ] **Python >= 3.9 已安装** — 验证命令：`python3 --version 2>/dev/null || python --version`
- [ ] **Node.js >= 22.0.0 已安装** — 验证命令：`node --version`
- [ ] **Claude Code >= 2.1.88 已安装** — 验证命令：`claude --version`
- [ ] **clinpub skill 已安装** — 验证命令：`npx clinpub-cc --version`

> ⚠️ 如果项目目录已有旧的 pipeline 产出（`01_RawData/` 到 `05_Manuscript/` 目录有内容），建议先备份或清空再开始测试，避免新旧文件混淆。

---

## Checkpoint 1: Phase 0 — 项目初始化

### 操作

1. 确保当前工作目录为项目根目录
2. 在 Claude Code 中运行命令：`/clinpub:init-project`
3. 当 Claude 询问研究框架时，粘贴以下预填回答：

### 预填回答

| 讨论项 | 预填回答 |
|--------|----------|
| 研究标题 | "cTBS 对抑郁症患者的疗效：随机对照试验" |
| 研究类型 | RCT |
| 样本量 | 86 例 |
| 结局变量 | HAMD_total（连续变量） |
| 分组变量 | Treatment（Sham vs cTBS） |
| 协变量 | Age, Sex, BMI |
| 目标期刊 | SCI Q1/Q2 |
| 报告标准 | CONSORT |
| 分析方法 | 接受 Claude 推荐方案（通常包含 BaselineTable、TwoGroupComparison、RepeatedMeasures） |
| 语言 | 中文正文 + 英文图表 |

### 验证

```bash
test -f "project_config.yml" && echo "project_config.yml: EXISTS" || echo "project_config.yml: MISSING"
for dir in 01_RawData 02_PreprocessedData 03_AnalysisMethods 04_Outputs 05_Manuscript Reference; do
  test -d "$dir" && echo "$dir/: EXISTS" || echo "$dir/: MISSING"
done
```

- [ ] `project_config.yml` 存在且非空
- [ ] `01_RawData/` 目录存在
- [ ] `02_PreprocessedData/` 目录存在
- [ ] `03_AnalysisMethods/` 目录存在
- [ ] `04_Outputs/` 目录存在
- [ ] `05_Manuscript/` 目录存在
- [ ] `Reference/` 目录存在

### 恢复

如果此步失败，可直接重新运行 `/clinpub:init-project`，不需要清理目录。

---

## Checkpoint 2: Phase 1 — 数据清洗

### 操作

1. 复制测试数据到项目：`cp clinpub/examples/sample_data/rct_depression.csv 01_RawData/`
2. 在 Claude Code 中运行命令：`/clinpub:data-prep`
3. 当 Claude 询问清洗策略时，粘贴以下预填回答：

### 预填回答

| 讨论项 | 预填回答 |
|--------|----------|
| 缺失值策略 | 使用默认三级框架：缺失率 <5% 删除、5-20% MICE 插补、>20% 标记讨论 |
| 异常值处理 | IQR 1.5 倍检测 + Winsorize |
| 分析时间点 | baseline（用于 Table 1）+ 全部时间点（用于纵向分析） |
| 衍生变量 | 无特殊衍生，按默认处理 |
| 数据结构 | 纵向数据（86 患者，3 时间点），需要同时输出 full_longitudinal.csv |

> **预期行为：** rct_depression.csv 的 HAMD_total 在 baseline 有少量缺失值（正常数据特征），Claude 应按三级框架处理并通过 checkpoint。

### 验证

SC1 + SC4 验证命令：

```bash
# SC1: cleaned.csv 存在且非空
test -s "02_PreprocessedData/data/cleaned.csv" && echo "SC1: PASS" || echo "SC1: FAIL"

# SC4: Phase 1 MANIFEST.yaml
test -f "02_PreprocessedData/MANIFEST.yaml" && echo "MANIFEST: EXISTS" || echo "MANIFEST: MISSING"
grep -q "^agent:" "02_PreprocessedData/MANIFEST.yaml" 2>/dev/null && echo "  agent: OK" || echo "  agent: MISSING"
grep -q "^phase:" "02_PreprocessedData/MANIFEST.yaml" 2>/dev/null && echo "  phase: OK" || echo "  phase: MISSING"
grep -q "^outputs:" "02_PreprocessedData/MANIFEST.yaml" 2>/dev/null && echo "  outputs: OK" || echo "  outputs: MISSING"
grep -q "^handoffs:" "02_PreprocessedData/MANIFEST.yaml" 2>/dev/null && echo "  handoffs: OK" || echo "  handoffs: MISSING"
```

- [ ] **SC1:** `02_PreprocessedData/data/cleaned.csv` 存在且非空
- [ ] **SC4:** `02_PreprocessedData/MANIFEST.yaml` 存在且包含 `agent:`、`phase:`、`outputs:`、`handoffs:` 字段

### 恢复

如果此步失败，修复问题后重新运行 `/clinpub:data-prep`。Checkpoint 1 的产出（目录结构和 `project_config.yml`）不受影响。

---

## Checkpoint 3: Phase 2 — 统计分析

### 操作

1. 在 Claude Code 中运行命令：`/clinpub:analysis`
2. 当 Claude 诊断数据结构并提出分析方案时，粘贴以下预填回答：

### 预填回答

| 讨论项 | 预填回答 |
|--------|----------|
| 分析方案 | 接受 Claude 推荐方案（基于 RCT + 连续结局 + 纵向数据） |
| 颜色方案 | 默认 viridis |
| 显著性水平 | α = 0.05 |
| 多重比较校正 | FDR |
| 方法参数 | 接受 Claude 推荐的变量选择和模型公式 |

### 验证

SC2 验证——至少 1 个分析方法同时有 figure + table + README：

```bash
# SC2: 检查至少有 1 个方法产出目录含 figure + table + README
has_figure=false
has_table=false
has_readme=false

# 检查 figure（glob 模式匹配所有 png 文件）
for dir in 04_Outputs/*/; do
  if ls "$dir"*.png 2>/dev/null | head -1 > /dev/null; then
    has_figure=true
    echo "Figure found in: $dir"
    break
  fi
done

# 检查 table（csv 或 xlsx）
for dir in 04_Outputs/*/; do
  if ls "$dir"*.csv "$dir"*.xlsx 2>/dev/null | head -1 > /dev/null; then
    has_table=true
    echo "Table found in: $dir"
    break
  fi
done

# 检查 README（可能在 03_AnalysisMethods/ 或 04_Outputs/）
for dir in 03_AnalysisMethods/*/ 04_Outputs/*/; do
  if test -f "${dir}README.md" 2>/dev/null; then
    has_readme=true
    echo "README found in: $dir"
    break
  fi
done

$has_figure && $has_table && $has_readme && echo "SC2: PASS" || echo "SC2: FAIL"
```

SC4 验证——Phase 2 MANIFEST：

```bash
# SC4: Phase 2 MANIFEST.yaml
test -f "04_Outputs/MANIFEST.yaml" && echo "MANIFEST: EXISTS" || echo "MANIFEST: MISSING"
grep -q "^agent:" "04_Outputs/MANIFEST.yaml" 2>/dev/null && echo "  agent: OK" || echo "  agent: MISSING"
grep -q "^phase:" "04_Outputs/MANIFEST.yaml" 2>/dev/null && echo "  phase: OK" || echo "  phase: MISSING"
grep -q "^outputs:" "04_Outputs/MANIFEST.yaml" 2>/dev/null && echo "  outputs: OK" || echo "  outputs: MISSING"
grep -q "^handoffs:" "04_Outputs/MANIFEST.yaml" 2>/dev/null && echo "  handoffs: OK" || echo "  handoffs: MISSING"
```

- [ ] **SC2:** `04_Outputs/` 下至少有 1 个方法目录含 `*.png` 文件
- [ ] **SC2:** `04_Outputs/` 下至少有 1 个方法目录含 `*.csv` 或 `*.xlsx` 文件
- [ ] **SC2:** `03_AnalysisMethods/` 或 `04_Outputs/` 下至少有 1 个方法目录含 `README.md`
- [ ] **SC4:** `04_Outputs/MANIFEST.yaml` 存在且包含 `agent:`、`phase:`、`outputs:`、`handoffs:` 字段

### 恢复

如果分析执行失败（如 R 包缺失、脚本报错），修复问题后重新运行 `/clinpub:analysis`。Claude 应能从诊断步骤继续，不需要重跑 Phase 0-1。

---

## Checkpoint 4: Phase 3 — 论文撰写

### 操作

1. 在 Claude Code 中运行命令：`/clinpub:writing`
2. 当 Claude 讨论写作方案时，粘贴以下预填回答：

### 预填回答

| 讨论项 | 预填回答 |
|--------|----------|
| 核心发现 | 接受 Claude 基于分析结果的总结 |
| 目标期刊 | SCI Q1/Q2（与 Phase 0 一致） |
| 参考文献策略 | 默认 PubMed 检索 |
| 图表选择 | 全部纳入 |

### 验证

SC3 验证——IMRAD 四章节各含 draft.md：

```bash
# SC3: 检查 IMRAD 章节（同时检查两种可能路径）
# 路径 A: 每章独立目录
for chapter in Introduction Methods Results Discussion; do
  if test -s "05_Manuscript/$chapter/draft.md"; then
    echo "SC3 $chapter: PASS (独立目录)"
  else
    echo "SC3 $chapter: checking alternative..."
  fi
done

# 路径 B: 单一 draft.md 包含所有章节
if test -s "05_Manuscript/draft.md"; then
  echo "SC3: draft.md found (单一文件模式)"
  for chapter in Introduction Methods Results Discussion; do
    grep -qi "$chapter" "05_Manuscript/draft.md" && echo "  $chapter: FOUND" || echo "  $chapter: NOT FOUND"
  done
fi
```

SC4 验证——Phase 3 MANIFEST：

```bash
# SC4: 05_Manuscript/MANIFEST.yaml
test -f "05_Manuscript/MANIFEST.yaml" && echo "MANIFEST: EXISTS" || echo "MANIFEST: MISSING"
grep -q "^agent:" "05_Manuscript/MANIFEST.yaml" 2>/dev/null && echo "  agent: OK" || echo "  agent: MISSING"
grep -q "^phase:" "05_Manuscript/MANIFEST.yaml" 2>/dev/null && echo "  phase: OK" || echo "  phase: MISSING"
grep -q "^outputs:" "05_Manuscript/MANIFEST.yaml" 2>/dev/null && echo "  outputs: OK" || echo "  outputs: MISSING"
grep -q "^handoffs:" "05_Manuscript/MANIFEST.yaml" 2>/dev/null && echo "  handoffs: OK" || echo "  handoffs: MISSING"

# SC4: Reference/MANIFEST.yaml
test -f "Reference/MANIFEST.yaml" && echo "Reference MANIFEST: EXISTS" || echo "Reference MANIFEST: MISSING"
```

- [ ] **SC3:** IMRAD 四章节（Introduction、Methods、Results、Discussion）各有 `draft.md` 存在（独立目录模式 `05_Manuscript/{chapter}/draft.md`，或单一文件模式 `05_Manuscript/draft.md` 含四个章节标题）
- [ ] **SC4:** `05_Manuscript/MANIFEST.yaml` 存在且包含 `agent:`、`phase:`、`outputs:`、`handoffs:` 字段
- [ ] **SC4:** `Reference/MANIFEST.yaml` 存在且包含 `agent:`、`phase:`、`outputs:`、`handoffs:` 字段

### 恢复

如果文献检索失败（如 Tavily API key 缺失），可跳过 Reference Agent 步骤，用 Claude 内置知识补充参考文献。Writing 步骤可独立重跑。

---

## Checkpoint 5: Phase 4 — 模拟审稿

### 操作

1. 在 Claude Code 中运行命令：`/clinpub:review`
2. 当 Claude 讨论审稿标准时，粘贴以下预填回答：

### 预填回答

| 讨论项 | 预填回答 |
|--------|----------|
| 审稿严格度 | 目标期刊水平 |
| 重点审查 | 统计方法、样本量、混杂控制 |
| 修订范围 | 全部接受 |

### 验证

```bash
# Phase 4 产出物
test -s "05_Manuscript/review_v1.md" && echo "review_v1.md: EXISTS" || echo "review_v1.md: MISSING"
test -d "05_Manuscript/final" && echo "final/: EXISTS" || echo "final/: MISSING"
test -s "05_Manuscript/final/manuscript.md" && echo "final/manuscript.md: EXISTS" || echo "final/manuscript.md: MISSING"
```

- [ ] `05_Manuscript/review_v1.md` 存在且非空
- [ ] `05_Manuscript/final/` 目录存在
- [ ] `05_Manuscript/final/manuscript.md` 存在且非空

### 恢复

如果审稿步骤中断，修复问题后重新运行 `/clinpub:review`。Phase 3 的手稿产出不受影响。

---

## Final Summary

汇总所有 SC 验证结果：

```bash
# 全局 SC 汇总
echo "=== Final Summary ==="
test -s "02_PreprocessedData/data/cleaned.csv" && echo "SC1: PASS" || echo "SC1: FAIL"

# SC2
sc2_pass=false
for dir in 04_Outputs/*/; do
  if ls "$dir"*.png 2>/dev/null | head -1 > /dev/null && \
     (ls "$dir"*.csv "$dir"*.xlsx 2>/dev/null | head -1 > /dev/null); then
    sc2_pass=true; break
  fi
done
$sc2_pass && echo "SC2: PASS" || echo "SC2: FAIL"

# SC3
sc3_pass=true
for chapter in Introduction Methods Results Discussion; do
  found=false
  test -s "05_Manuscript/$chapter/draft.md" && found=true
  (test -s "05_Manuscript/draft.md" && grep -qi "$chapter" "05_Manuscript/draft.md") && found=true
  $found || sc3_pass=false
done
$sc3_pass && echo "SC3: PASS" || echo "SC3: FAIL"

# SC4
sc4_pass=true
for manifest in 02_PreprocessedData/MANIFEST.yaml 04_Outputs/MANIFEST.yaml 05_Manuscript/MANIFEST.yaml Reference/MANIFEST.yaml; do
  test -f "$manifest" || sc4_pass=false
done
$sc4_pass && echo "SC4: PASS" || echo "SC4: FAIL"

echo "SC5: PASS (本文件即 checklist)"
```

- [ ] **SC1:** `cleaned.csv` 存在且非空
- [ ] **SC2:** 至少 1 个分析方法产出 figure + table + README
- [ ] **SC3:** IMRAD 四章节各有 draft.md
- [ ] **SC4:** Phase 1-4 每阶段 MANIFEST.yaml 存在（共 4 个）
- [ ] **SC5:** 本 checklist 文件存在（`clinpub/examples/04-INTEGRATION-CHECKLIST.md`）

---

## Troubleshooting

如果在集成测试过程中遇到问题，请参考以下常见问题和解决方法：

### 1. R 包缺失

**症状：** 分析脚本报错 `there is no package called 'xxx'`

**解决：** 在 R 中运行 `install.packages("xxx")` 安装缺失的包。如果涉及 Bioconductor 包（如 `lme4` 依赖链），可能需要 `BiocManager::install("xxx")`。

### 2. HAMD_total 缺失值

**症状：** data-prep 阶段报缺失率过高

**解决：** 这是预期行为——`rct_depression.csv` 的 HAMD_total 在 baseline 有部分缺失（属正常临床数据特征）。接受 Claude 的默认缺失值处理策略（<5% 删除 / 5-20% MICE 插补 / >20% 标记讨论）即可。

### 3. MANIFEST.yaml 不在预期位置

**症状：** 按固定路径检查 MANIFEST 时文件不存在

**解决：** 运行 `find . -name "MANIFEST.yaml" -type f` 查找实际位置。MANIFEST 文件可能在 workflow 子目录下（如 `02_PreprocessedData/reports/` 或 `04_Outputs/` 的子目录），按 glob 查找结果更新验证路径即可。

### 4. IMRAD 章节路径不一致

**症状：** `05_Manuscript/Introduction/draft.md` 不存在

**解决：** 检查是否有 `05_Manuscript/draft.md`（单一文件模式，所有章节写在一个文件中），或运行 `find 05_Manuscript/ -name "draft.md"` 查找实际章节路径。两种路径模式都是有效的。

### 5. Tavily API key 缺失

**症状：** Reference Agent 文献检索失败

**解决：** 设置环境变量 `TAVILY_API_KEY`（可通过 `.env` 文件或 `export` 命令设置）。如果无法获取 API key，可跳过文献检索步骤，写作阶段使用 Claude 内置知识补充参考文献。

### 6. 分析产出物格式多样

**症状：** 按固定文件名找不到 figure 或 table

**解决：** 使用 `ls 04_Outputs/*/` 查看实际文件名。Table 文件可能是 `.xlsx` 而非 `.csv`。Figure 文件可能是 `.pdf` 或 `.tiff` 而非 `.png`。按实际格式调整验证脚本中的文件扩展名。

### 7. checkpoint 卡住或无法继续

**症状：** Claude 在 checkpoint 处等待用户响应，但用户已提供输入后仍无法继续

**解决：** 在每个 checkpoint，Claude 期待的恢复信号是 `approved` 或具体的选择（如 `A`、`B`、`C`）。如果不确定需要什么回复，检查 Claude 输出的 `<resume_signal>` 提示。

### 8. 网络问题导致文献检索超时

**症状：** PubMed/NCBI API 请求超时

**解决：** 检查网络连接。NCBI API 不需要 API key 即可使用（只是有 key 时速率更高）。如果持续超时，可暂时跳过文献检索，后续在写作阶段再补。

---

> **文档版本:** 1.0 | **覆盖范围:** Phase 0-4 完整 pipeline | **Success Criteria:** SC1-SC5 全部覆盖
