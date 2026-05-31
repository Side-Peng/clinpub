# Phase 6 Research: 图表+文档优化

**Researched:** 2026-05-28
**Status:** Complete

## RESEARCH COMPLETE

---

## 1. 当前状态分析

### r_patterns.md 现状

**Core Standards（第一部分）已有：**
- §1.1 色彩规范 — Okabe-Ito、Nature 双色、RColorBrewer、viridis，按组数推荐
- §1.2 `theme_pub()` — 基于 theme_minimal，有 panel.border、bold 轴标签
- §1.3 保存规范 — 300 DPI、TIFF/PDF/PNG、单栏 8cm/双栏 17cm
- §1.4 显著性标注 — p 值格式化、ggsignif 动态位置
- §1.5 Wilson Score CI
- §1.6 patchwork 拼图布局
- §1.7 目录先行规则

**Analysis Patterns（第二部分）已有：**
- 2.1 三层绘图法（箱线图+散点）
- 2.2 Z-score 标准化
- 2.3 ROC 双模式
- 2.4 LASSO 特征选择
- 2.5 混淆矩阵热图
- 2.6 森林图
- 2.7 风险分层 jitter plot
- 2.8 训练集/验证集分割

**缺失项（需补充）：**
- 生存曲线（KM 曲线）美化模板 — analysis_methods.md §3.4 提到但 r_patterns.md 无对应模式
- 相关性矩阵热图 — analysis_methods.md §3.6 提到但无专用模式
- 亚组森林图 — analysis_methods.md §3.5 提到但无专用模式（现有 2.6 是通用森林图）
- 回归诊断图（残差图、QQ 图）— 线性回归/混合模型需要
- 火山图 / 效应量图 — 多标志物比较场景

### journal_standards.md 现状

已有：
- 目标期刊：Alzheimer's & Dementia (IF~14)、Molecular Psychiatry (IF~11)
- 报告规范：CONSORT/STROBE/PRISMA/TRIPOD
- 图表规范：≥300 DPI、矢量优先、不接受 Excel 默认图、限制 6 个图/表
- FIGURE_DPI = 300（与 r_patterns.md PUBLICATION_DPI 一致）

---

## 2. SCI 期刊图表规范调研

### Nature 系列图表要求

| 参数 | 要求 |
|------|------|
| 分辨率 | ≥300 DPI |
| 格式 | TIFF, EPS, PDF（优先矢量） |
| 字体 | Arial, Helvetica, 或 Times New Roman ≥6pt（建议 ≥8pt） |
| 线宽 | ≥0.5 pt（建议 ≥1 pt） |
| 颜色模式 | CMYK（投稿时）/ RGB（屏幕预览） |
| 单栏宽度 | 89 mm (~3.5 in) |
| 双栏宽度 | 183 mm (~7.2 in) |

### NEJM 图表要求

| 参数 | 要求 |
|------|------|
| 分辨率 | ≥300 DPI |
| 格式 | TIFF, EPS |
| 字体 | Arial ≥8pt |
| 线条 | ≥1 pt |
| 颜色 | 色盲友好，避免纯红绿 |

### Lancet 图表要求

| 参数 | 要求 |
|------|------|
| 分辨率 | ≥300 DPI |
| 格式 | TIFF, EPS, PDF |
| 字体 | Arial ≥7pt |
| 颜色 | 提供 CMYK 色值 |

### 共性要求总结

1. **≥300 DPI** — 所有期刊一致
2. **Arial 字体** — 所有期刊一致（当前 theme_pub() 未强制字体族）
3. **矢量格式优先** — PDF/EPS
4. **色盲友好** — 避免红绿组合
5. **线宽 ≥1 pt** — 当前 theme_pub() 的 linewidth=1 已满足
6. **panel.border** — Nature/NEJM 风格常用黑色边框（当前已有）

---

## 3. theme_pub() 改进建议

### 当前不足

1. **未指定字体族** — SCI 期刊要求 Arial，但 R 默认使用 sans（可能不是 Arial）
2. **base_size=14 偏大** — 期刊通常要求 6-8pt 字体，图表内文字不宜过大
3. **legend.position="none" 默认隐藏图例** — 多数图表需要图例
4. **缺少 aspect ratio 控制** — 不同图表类型需要不同宽高比

### 建议改进

```r
theme_pub <- function(base_size = 10, base_family = "sans") {
  # base_size=10 更适合出版级图表（约 7-8pt 在最终排版中）
  # base_family="sans" 在 Windows 上默认映射到 Arial
  theme_minimal(base_size = base_size, base_family = base_family) %+replace%
    theme(
      # 图例
      legend.position = "right",  # 改为右侧显示（更通用）
      legend.title = element_text(face = "bold", size = rel(0.9)),
      legend.text = element_text(size = rel(0.85)),
      # 标题
      plot.title = element_text(hjust = 0.5, size = rel(1.1), face = "bold"),
      # 轴
      axis.title = element_text(size = rel(1), face = "bold"),
      axis.text = element_text(size = rel(0.9), face = "bold"),
      axis.line = element_line(color = "black", linewidth = 0.5),
      # 网格
      panel.grid = element_blank(),
      panel.border = element_rect(color = "black", fill = NA, linewidth = 1),
      # 刻度
      axis.ticks = element_line(color = "black", linewidth = 0.5),
      # 分面
      strip.background = element_rect(fill = "grey95", color = "black"),
      strip.text = element_text(face = "bold", size = rel(0.9))
    )
}
```

### 关键变化

| 改动 | 原因 |
|------|------|
| base_size 14→10 | 适配 6-8pt 出版要求 |
| base_family = "sans" | 明确字体族（Arial 在 Windows 上的映射） |
| legend.position "none"→"right" | 多数图表需要图例 |
| 新增 axis.line | SCI 期刊常用轴线 |
| linewidth 细化 | 区分边框和刻度线粗细 |

---

## 4. 新增图表类型建议

### 4.1 KM 生存曲线美化（§3.4 需要）

```r
library(survival)
library(survminer)

fit <- survfit(Surv(time, event) ~ group, data = df)

ggsurvplot(fit, data = df,
  pval = TRUE, pval.method = TRUE,
  risk.table = TRUE, risk.table.col = "strata",
  palette = c("#0072B5", "#BC3C29"),  # Nature 配色
  xlab = "Time (months)", ylab = "Survival probability",
  legend.title = "Group",
  ggtheme = theme_pub())
```

### 4.2 相关性矩阵热图（§3.6 需要）

```r
library(ggcorrplot)

corr_matrix <- cor(data, method = "spearman", use = "pairwise.complete.obs")
ggcorrplot(corr_matrix,
  type = "lower",
  lab = TRUE, lab_size = 3,
  colors = c("#0072B5", "white", "#BC3C29"),
  ggtheme = theme_pub())
```

### 4.3 亚组森林图（§3.5 需要）

```r
ggplot(subgroup_df, aes(x = hr, y = reorder(subgroup, hr))) +
  geom_point(size = 3, color = "#0072B5") +
  geom_errorbarh(aes(xmin = lower, xmax = upper), height = 0.2, color = "#0072B5") +
  geom_vline(xintercept = 1, linetype = "dashed", color = "grey50") +
  scale_x_log10() +
  labs(x = "Hazard Ratio (95% CI)", y = "") +
  theme_pub()
```

### 4.4 回归诊断图

```r
# 四格诊断图
par(mfrow = c(2, 2))
plot(model)  # Residuals vs Fitted, Normal Q-Q, Scale-Location, Cook's distance
```

---

## 5. 方法说明模板设计

### 当前 README 结构（agent-contracts.md）

- 必须包含 `Results` subsection
- 注明图例、表注、方法参数
- 软件版本

### 建议「方法说明」模板

```markdown
# [方法名称] — 方法说明

## 目的
[一句话说明本分析的目标]

## 方法
[使用的统计方法、公式、假设条件]

## 输入数据
- 数据文件：`cleaned.csv` / `full_longitudinal.csv`
- 使用变量：[变量列表]
- 样本量：[N]
- 时间点：[baseline / post_treatment / follow_up]

## 输出结果
### 图表
| 文件 | 说明 |
|------|------|
| figure_1.png | [图例说明] |

### 表格
| 文件 | 说明 |
|------|------|
| table_1.docx | [表注说明] |

## 参数设置
- [关键参数及其取值]
- [如：显著性水平 α=0.05, 校正方法 FDR]

## 注意事项
- [方法适用条件]
- [不适用条件]
- [已知局限性]

## 软件版本
- R {version}
- {包名} {版本}
```

### 与 agent-contracts.md 的兼容性

- 当前要求 "README must contain Results subsection"
- 「方法说明」的 "输出结果" section 等价于 Results
- 需要更新 agent-contracts.md 中的 README 引用为「方法说明」
- MANIFEST.yaml 中的文件引用也需要同步更新

---

## 6. 文件改造影响范围

### 需要修改的文件

| 文件 | 改动类型 | 说明 |
|------|---------|------|
| `pipeline/references/r_patterns.md` | 大改 | 更新 theme_pub()、新增图表类型、更新配色说明 |
| `pipeline/references/agent-contracts.md` | 小改 | README → 方法说明，更新输出规范 |
| `pipeline/references/gates.md` | 小改 | README → 方法说明 |
| `pipeline/references/analysis_methods.md` | 小改 | README → 方法说明 |
| `pipeline/references/verification-patterns.md` | 小改 | README → 方法说明 |
| `pipeline/references/mandatory-initial-read.md` | 小改 | README → 方法说明 |
| `pipeline/references/manifest-format.md` | 可能小改 | 如果 MANIFEST.yaml 引用 README |

### 不需要修改的文件

- `pipeline/workflows/analysis.md` — 引用的是 "README" 概念，不涉及文件名
- `pipeline/references/journal_standards.md` — 图表规范已较完善

---

## 7. 实施建议

### 优先级

1. **r_patterns.md 改造** — 核心，影响所有图表输出
2. **方法说明模板** — 需要设计并更新所有引用
3. **agent-contracts.md 更新** — 确保契约一致

### 风险

- **向后兼容**：改名 README→方法说明 需要同步更新所有引用，否则 Phase 2 执行会找不到文件
- **字体可用性**：R 在 Linux/macOS 上 "sans" 可能不是 Arial，需要 `extrafont` 包
- **现有输出**：已完成的 Phase 1-5 输出中的 README 不受影响（历史产物）
