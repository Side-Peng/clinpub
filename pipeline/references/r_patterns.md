# R 可视化核心标准与分析模式

> 第一部分（Core Standards）是所有 clinpub R 代码生成必须遵守的强制标准。第二部分（Analysis Patterns）是按需取用的图类型代码，每种标注了适用条件和禁忌。

---

# 第一部分：Core Standards（强制标准）

以下规则适用于 clinpub 生成的所有 R 可视化代码，无论何种分析方法。

---

## 1.0 Figure Contract（绘图契约）

> 在生成任何图表代码之前，必须先完成以下契约定义。这确保每张图都有明确的叙事目的，避免“先画再想”的常见错误。

### 契约模板

在规划每张 Figure 时，填写以下表格：

| 字段 | 说明 | 示例 |
|------|------|------|
| **核心结论** | 该图要传达的一句话结论（必须含动词） | “Biomarker X 在 Case 组显著升高，且与预后相关” |
| **证据层级** | 该图在论文中的角色 | Main Figure 2 / Supplementary Fig. S3 |
| **面板映射** | 每个子图回答的具体问题 | (a) 组间比较 (b) 时间趋势 (c) 亚组效应 |
| **布局原型** | 选择的 patchwork 布局类型（见 §1.6） | quantitative-grid / clinical-triptych |
| **色彩语义** | 颜色分配的角色含义（见 §1.1） | blue=干预组, red=对照组, grey=参考 |
| **目标尺寸** | 单栏/双栏/全幅 | 双栏 (183mm) |

### 契约填写规则

1. **一图一结论**: 每张 Figure 必须有一个核心结论。多结论应拆分为多张图
2. **面板问题唯一性**: 每个面板必须回答一个独特问题，与反冗余检查清单（§1.8）互验
3. **先定布局再写代码**: 布局原型确定后，按 §1.6 的 patchwork 模板实施
4. **颜色一致性**: 语义颜色一旦在契约中确定，所有面板和后续修改必须保持一致
5. **主要证据优先**: 主证据获得最佳面板位置和最醒目的色彩；对照组/稳健性检查面板应视觉更安静

### 面板逻辑顺序

除非论文叙事明确要求其他顺序，否则按以下顺序排列面板：

1. **建立系统**: 样本、方法、队列或实验设计
2. **展示主效应**: 主要比较或核心发现
3. **机制/定位**: 深入分析或亚组探索
4. **量化验证**: 对定性观察的定量确认
5. **稳健性/对照**: 敏感性分析、对照组或亚组分析

---

## 1.1 色彩规范与选色协议

### 核心原则

在生成任何图表**之前**，必须与用户沟通颜色方案：

1. **询问用户偏好**："您倾向于使用预设配色，还是指定具体颜色？"
2. **默认推荐色盲友好方案**（viridis / Okabe-Ito / RColorBrewer Set 系列）
3. **避免红绿组合**（红绿色盲最常见）

### 语义色彩角色

颜色不只是区分组别，更要传达角色含义。在 Figure Contract（§1.0）中确定每个颜色的语义角色。

| 语义角色 | 含义 | 推荐色值 | 使用场景 |
|----------|------|----------|----------|
| **Hero** | 核心关注的方法/组别 | `"#0072B5"` (蓝) | 新提出的诊断方法、干预组 |
| **Baseline** | 对照/基线/参考 | `"#BC3C29"` (红) 或 `"grey50"` | 标准治疗、安慰剂组 |
| **Positive** | 正向/显著/成功 | `"#009E73"` (绿) | 阳性结果、缓解组 |
| **Neutral** | 背景/辅助/次要 | `"grey70"` | 参考线、非焦点组 |
| **Accent** | 强调/异常值 | `"#E69F00"` (橙) | 关键阈值线、异常亚组 |

以上所有语义色值均为色盲友好色，与 Okabe-Ito / Nature 双色系兼容。

### 克制配色原则（Restrained Palette）

每张图最多使用三个色系家族：

1. **Neutral family**: 灰色系 — 背景、辅助元素、参考线
2. **Signal family**: 蓝/红双色系 — 主比较（干预 vs 对照）
3. **Accent family**: 橙/绿 — 仅在需要特别强调时使用（每张图最多 1 个 accent）

规则：
- 同一图中不超过 5 种语义色彩角色
- 如果分组 > 5，回退到 Okabe-Ito 或 viridis 离散版（保留色盲友好）
- 语义优先级：Hero 和 Baseline 必须有明确色值，其余角色按需分配
- 绿色/红色保留给有方向性含义的场景（如升高/降低、阳性/阴性），不要仅因“组别不同”而使用

### 按分组数推荐配色

| 组数 | 推荐方案 | 示例代码 |
|------|---------|----------|
| **2组** | `c("#0072B5", "#BC3C29")` — Nature 风格，色盲友好 | `scale_fill_manual(values = c("#0072B5", "#BC3C29"))` |
| **3-4组** | RColorBrewer `"Set1"` 或 `"Dark2"` | `scale_fill_brewer(palette = "Set1")` |
| **5-8组** | RColorBrewer `"Set2"` 或 `"Paired"` | `scale_fill_brewer(palette = "Paired")` |
| **连续变量/热图** | viridis（默认方向） | `scale_fill_viridis_c(option = "D")` |
| **多标志物（>10）** | viridis `option = "D"` 或 `"G"` | `scale_color_viridis_d(option = "G")` |

### 色盲友好方案速查

```r
# Okabe-Ito 配色（8 种，色盲友好首选）
okabe_ito <- c("#E69F00", "#56B4E9", "#009E73", "#F0E442",
               "#0072B2", "#D55E00", "#CC79A7", "#000000")

# Nature 期刊双色（退而求其次）
nature_colors <- c("#0072B5", "#BC3C29")

# 当组数 > 8 时，使用 viridis 离散版
scale_color_viridis_d(option = "D", begin = 0.1, end = 0.9)
```

### 选色决策流程

```
颜色是否承载语义角色（如 Hero vs Baseline）？
├── 是 → 使用语义色彩角色表（见上方）
└── 否 → 数据有分组变量？
    ├── 是 → 用户有颜色偏好吗？
    │   ├── 有 → 使用用户指定颜色
    │   └── 没有 → 按组数套用推荐方案（见上表）
    └── 否（连续变量/热图）
        └── 使用 viridis 连续色标
```

### 颜色一致性规则

- 同一分析方法内的多张图，**相同分组必须使用相同颜色映射**
- 若一个变量在正文和补充材料中均出现，颜色必须一致
- 多个 biomarker 之间使用同一色系区分强度，而非不同色系

### 配色配置协议（Color Config Protocol）

> **强制规则**：在生成任何使用 `scale_fill_*` / `scale_color_*` 的 R 代码之前，必须先读取 `project_config.yml` 的 `quality.color_palette` 段，并根据用户配置生成配色。

#### 读取逻辑

在 R 脚本的初始化部分（紧随 `library()` 加载之后），加入配色读取代码：

```r
# ---- Color Palette Configuration (from project_config.yml) ----
cfg <- yaml::read_yaml("project_config.yml")
color_cfg <- cfg$quality$color_palette  # may be NULL if not configured

# 解析参数（NULL-safe，回退到默认值）
color_preset       <- if (!is.null(color_cfg$preset)) color_cfg$preset else "auto"
color_custom       <- if (!is.null(color_cfg$custom_colors)) unlist(color_cfg$custom_colors) else c()
color_group_map    <- if (!is.null(color_cfg$group_mapping)) as.character(as.list(color_cfg$group_mapping)) else NULL
color_continuous   <- if (!is.null(color_cfg$continuous)) color_cfg$continuous else "viridis"
```

#### 应用方式

使用 `get_palette()` 辅助函数根据配置动态生成配色：

```r
# get_palette() — 配置驱动的配色生成器
# n_groups: 当前图的分组数
get_palette <- function(n_groups) {
  # 0. 单色场景直接返回 Hero 色
  if (n_groups == 1) {
    return("#0072B5")  # Hero color for single-color plots
  }
  # 1. 优先使用用户指定分组映射
  if (!is.null(color_group_map) && length(color_group_map) >= n_groups) {
    return(color_group_map)
  }
  # 2. 优先使用自定义色值列表
  if (length(color_custom) >= n_groups) {
    return(color_custom[1:n_groups])
  }
  # 3. 按 preset 方案选择
  switch(color_preset,
    "nature"       = c("#0072B5", "#BC3C29")[1:min(n_groups, 2)],
    "okabe-ito"    = c("#E69F00", "#56B4E9", "#009E73", "#F0E442",
                       "#0072B2", "#D55E00", "#CC79A7", "#000000")[1:n_groups],
    "brewer-set1"  = RColorBrewer::brewer.pal(max(3, n_groups), "Set1")[1:n_groups],
    "brewer-dark2" = RColorBrewer::brewer.pal(max(3, n_groups), "Dark2")[1:n_groups],
    "brewer-set2"  = RColorBrewer::brewer.pal(max(3, n_groups), "Set2")[1:n_groups],
    "viridis"      = viridis::viridis(n_groups),
    # auto: 按组数自动选择（默认行为）
    {
      if (n_groups <= 2) c("#0072B5", "#BC3C29")[1:n_groups]
      else if (n_groups <= 4) RColorBrewer::brewer.pal(max(3, n_groups), "Set1")[1:n_groups]
      else if (n_groups <= 8) RColorBrewer::brewer.pal(max(3, n_groups), "Set2")[1:n_groups]
      else viridis::viridis(n_groups)
    }
  )
}

# get_continuous_scale() — 连续变量色标
get_continuous_scale <- function() {
  switch(color_continuous,
    "viridis" = scale_fill_viridis_c(option = "D"),
    "magma"   = scale_fill_viridis_c(option = "A"),
    "plasma"  = scale_fill_viridis_c(option = "C"),
    "inferno" = scale_fill_viridis_c(option = "B"),
    scale_fill_viridis_c(option = "D")
  )
}

# get_diverging_scale() — 发散色标（相关性矩阵等有正负方向的连续变量）
# midpoint: 发散中心值，相关性矩阵默认为 0
get_diverging_scale <- function(midpoint = 0) {
  scale_fill_gradient2(
    low = "#0072B5", mid = "white", high = "#BC3C29",
    midpoint = midpoint
  )
}

# 语义色便捷函数 — 用于单色图表（森林图、RCS、趋势图等）
get_hero_color     <- function() "#0072B5"   # 核心关注色（新方法/干预组）
get_baseline_color <- function() "#BC3C29"   # 对照/参考色（标准治疗/零线）
get_accent_color   <- function() "#E69F00"   # 强调色（阈值线/异常亚组）
```

然后在 ggplot2 调用中使用：

```r
# 分组图表
p + scale_fill_manual(values = get_palette(n_groups))
# 或分组颜色
p + scale_color_manual(values = get_palette(n_groups))
# 连续变量
p + get_continuous_scale()
```

#### 默认值速查

| 参数 | 默认值 | config 路径 | 说明 |
|------|--------|-------------|------|
| `preset` | `"auto"` | `quality.color_palette.preset` | 预设配色方案 |
| `custom_colors` | `[]` | `quality.color_palette.custom_colors` | 自定义色值列表 |
| `group_mapping` | `{}` | `quality.color_palette.group_mapping` | 分组→色值映射 |
| `continuous` | `"viridis"` | `quality.color_palette.continuous` | 连续变量色标 |

**向后兼容**：如果 `project_config.yml` 中不存在 `quality.color_palette` 段（旧项目），上述代码全部回退到默认值，行为与改动前完全一致（`auto` 模式按组数自动选择）。

---

## 1.2 出版级主题 `theme_pub()`

所有 ggplot2 图表**必须**应用此主题。

```r
theme_pub <- function(base_size = 11, base_family = "sans") {
  # base_size=11：保证屏幕阅读和出版均清晰（≥8pt 期刊底线由 rel() 缩放保证）
  # base_family="sans" 在 Windows 上默认映射到 Arial
  theme_minimal(base_size = base_size, base_family = base_family) %+replace%
    theme(
      # 背景
      panel.background = element_rect(fill = "white", color = NA),
      plot.background = element_rect(fill = "white", color = NA),
      # 图例
      legend.position = "right",
      legend.title = element_text(face = "bold", size = rel(0.9)),
      legend.text = element_text(size = rel(0.9)),
      legend.key.size = unit(0.8, "lines"),
      legend.spacing = unit(0.3, "cm"),
      legend.background = element_rect(fill = "white", color = NA),
      # 标题（左对齐，Nature 风格）
      plot.title = element_text(hjust = 0, size = rel(1.1), face = "bold",
                                margin = margin(b = 8)),
      # 轴
      axis.title = element_text(size = rel(1), face = "bold"),
      axis.title.x = element_text(margin = margin(t = 8)),
      axis.title.y = element_text(margin = margin(r = 8)),
      axis.text = element_text(size = rel(0.9), color = "black"),
      axis.line = element_line(color = "black", linewidth = 0.4),
      axis.ticks = element_line(color = "black", linewidth = 0.3),
      # 网格（仅保留主网格线，极淡，辅助读数）
      panel.grid.major = element_line(color = "grey92", linewidth = 0.2),
      panel.grid.minor = element_blank(),
      # 边框
      panel.border = element_rect(color = "black", fill = NA, linewidth = 0.4),
      # 分面
      strip.background = element_rect(fill = "grey95", color = "black",
                                      linewidth = 0.4),
      strip.text = element_text(face = "bold", size = rel(0.9)),
      # 外边距（稍宽松，避免多图拼接时挤压）
      plot.margin = margin(12, 12, 12, 12)
    )
}

# 轻量变体：无边框，适用于流程图、示意图等不需要数据边框的图
theme_pub_light <- function(base_size = 11, base_family = "sans") {
  theme_pub(base_size = base_size, base_family = base_family) +
    theme(
      panel.border = element_blank(),
      axis.line = element_line(color = "black", linewidth = 0.4),
      panel.grid.major = element_blank()
    )
}
```

### `theme_pub()` 字号速查（base_size = 11）

| 元素 | `rel()` | 实际 pt | 说明 |
|------|---------|---------|------|
| `plot.title` | 1.1 | 12.1 | 图表主标题 |
| `axis.title` | 1.0 | 11.0 | 轴标题 |
| `axis.text` | 0.9 | 9.9 | 轴刻度标签 |
| `legend.title` | 0.9 | 9.9 | 图例标题 |
| `legend.text` | 0.9 | 9.9 | 图例文本 |
| `strip.text` | 0.9 | 9.9 | 分面标签 |

所有元素均满足 **≥ 8pt** 的期刊最低字号要求，且在屏幕上阅读舒适。

**应用方式：** `+ apply_theme()`（配置驱动，见下方 Config Protocol）或直接 `+ theme_pub()`（标准）/ `+ theme_pub_light()`（轻量无边框）。当 `project_config.yml` 包含 `quality.theme` 配置时，**必须**使用 `apply_theme()` 方式。

- 默认显示右侧图例（`legend.position = "right"`）。如需隐藏图例（如单组柱状图），覆盖为 `theme(legend.position = "none")`。
- 如需图例放在顶部：`theme(legend.position = "top")`。
- 标题默认左对齐（Nature 风格）。如需居中，覆盖为 `theme(plot.title = element_text(hjust = 0.5))`。
- 字体族 `"sans"` 在 Windows 上映射到 Arial；Linux/macOS 可能需要 `extrafont` 包（见 §1.3）。

### 配置读取协议（Config Protocol）

> **强制规则**：在生成任何使用 `theme_pub()` 的 R 代码之前，必须先读取 `project_config.yml` 的 `quality.theme` 段，并将用户配置值注入主题函数调用。

#### 读取逻辑

在 R 脚本的初始化部分（紧随 `library()` 加载之后），加入配置读取代码：

```r
# ---- Theme Configuration (from project_config.yml) ----
# 读取配置；如果 quality.theme 段不存在，使用默认值
cfg <- yaml::read_yaml("project_config.yml")
theme_cfg <- cfg$quality$theme  # may be NULL if not configured

# 解析参数（NULL-safe，回退到默认值）
theme_variant      <- if (!is.null(theme_cfg$variant)) theme_cfg$variant else "theme_pub"
theme_base_size    <- if (!is.null(theme_cfg$base_size)) theme_cfg$base_size else 11
theme_base_family  <- if (!is.null(theme_cfg$base_family)) theme_cfg$base_family else "sans"
theme_legend_pos   <- if (!is.null(theme_cfg$legend_position)) theme_cfg$legend_position else "right"
theme_title_hjust  <- if (!is.null(theme_cfg$title_hjust)) theme_cfg$title_hjust else 0
theme_panel_border <- if (!is.null(theme_cfg$panel_border)) theme_cfg$panel_border else TRUE
```

#### 应用方式

使用 `apply_theme()` 包装器替代直接 `+ theme_pub()` 调用：

```r
# apply_theme() — 配置驱动的主题包装器
apply_theme <- function() {
  base_theme <- if (theme_variant == "theme_pub_light") {
    theme_pub_light(base_size = theme_base_size, base_family = theme_base_family)
  } else {
    theme_pub(base_size = theme_base_size, base_family = theme_base_family)
  }
  # 叠加用户自定义覆盖
  base_theme + theme(
    legend.position = theme_legend_pos,
    plot.title = element_text(hjust = theme_title_hjust),
    panel.border = if (theme_panel_border) {
      element_rect(color = "black", fill = NA, linewidth = 0.4)
    } else {
      element_blank()
    }
  )
}
```

然后在所有 ggplot2 调用中使用 `+ apply_theme()` 替代 `+ theme_pub()`。

#### 默认值速查

| 参数 | 默认值 | config 路径 | 说明 |
|------|--------|-------------|------|
| `variant` | `"theme_pub"` | `quality.theme.variant` | 主题变体 |
| `base_size` | `11` | `quality.theme.base_size` | 基础字号 |
| `base_family` | `"sans"` | `quality.theme.base_family` | 字体族 |
| `legend_position` | `"right"` | `quality.theme.legend_position` | 图例位置 |
| `title_hjust` | `0` | `quality.theme.title_hjust` | 标题水平对齐 |
| `panel_border` | `TRUE` | `quality.theme.panel_border` | 是否有边框 |

**向后兼容**：如果 `project_config.yml` 中不存在 `quality.theme` 段（旧项目），上述代码全部回退到默认值，行为与硬编码 `theme_pub(base_size=11, base_family="sans")` 完全一致。

### 主题强制执行规则（Theme Enforcement）

> **⚠️ 强制规则**：以下规则不可跳过、不可降级。每张由 clinpub 生成的 ggplot2 图表**必须**满足所有检查项。

#### 必须遵守

1. **`theme_pub()` 或 `apply_theme()` 必须出现在每个 `ggplot()` 调用链的最后一层。** 任何其他 `theme()` 调用必须放在 `theme_pub()` **之前**（通过 `+ theme(...)` 在 `theme_pub()` 之前添加），否则会被 `theme_pub()` 的 `%+replace%` 覆盖。
2. **禁止使用 ggplot2 内置主题替代 `theme_pub()`。** 以下调用一律禁止出现在 clinpub 生成的代码中：
   - `theme_grey()` / `theme_gray()`
   - `theme_bw()`
   - `theme_classic()`
   - `theme_minimal()`（直接调用，不通过 `theme_pub()`）
   - `theme_dark()` / `theme_void()`（除 CONSORT 流程图等特殊情况）
   - `theme_light()`
3. **禁止在 `theme_pub()` 之后添加覆盖背景的 `theme()` 调用。** 如 `+ theme(panel.background = element_rect(fill = "grey92"))` 是严格禁止的——这会导致灰色背景，与 `theme_pub()` 的白色背景设计冲突。
4. **x 轴标签必须使用人类可读的标签名**，不能直接暴露变量名（如 `sleep_group_label`）。必须使用 `labs(x = "Sleep Quality")` 或 `scale_x_discrete(labels = c(...))` 进行映射。
5. **配色必须来自 Color Config Protocol**（§1.1），不能硬编码 "steelblue"、"coral"、"pink"、"lightblue" 等临时颜色。

#### 常见错误与修正

| 错误代码 | 症状 | 正确写法 |
|---------|------|---------|
| `ggplot(...) + geom_xxx() + theme_grey()` | 灰色背景 + 白色网格 | `ggplot(...) + geom_xxx() + theme_pub()` |
| `ggplot(...) + theme_pub() + theme_bw()` | `theme_bw` 覆盖 `theme_pub`，风格不一致 | `ggplot(...) + theme_pub()` （去掉 `theme_bw`） |
| `ggplot(...) + theme_pub() + theme(panel.background = ...)` | 背景色被意外修改 | 将 `theme()` 放在 `theme_pub()` 之前，或仅覆盖允许的少量参数 |
| `labs(x = "variable_name")` 直接写变量名 | x 轴暴露代码变量名 | `labs(x = "Human Readable Label")` |
| `scale_fill_manual(values = c("pink", "cyan"))` | 配色脱离语义色板 | `scale_fill_manual(values = get_palette(2))` |
| `geom_boxplot(fill = "lightblue")` | 硬编码颜色 | 使用 `aes(fill = group)` + `scale_fill_manual(values = get_palette(n))` |

#### 出图前自检清单（每次生成图表代码前必须逐项核对）

在生成任何 ggplot2 图表的 R 代码时，**必须**确认以下 6 项全部通过。任何一项不通过，生成的图表将不符合 clinpub 出版标准：

- [ ] ① `theme_pub()` 或 `apply_theme()` 出现在 ggplot 调用链中
- [ ] ② 没有 `theme_grey` / `theme_bw` / `theme_classic` 等内置主题
- [ ] ③ 背景为白色（无灰色背景）
- [ ] ④ 配色来自 `get_palette()` / 语义色，无硬编码临时颜色
- [ ] ⑤ x/y 轴标签为人类可读英文（非变量名）
- [ ] ⑥ 线宽规范：结构线（`axis.line`、`panel.border`）= 0.4，`axis.ticks` = 0.3；数据线常规 0.4，主曲线/主趋势可加粗至 0.8，辅助线保持 0.4

### 数据线宽度约定

结构线（轴、边框、刻度）由 `theme_pub()` 统一控制，不可覆盖。数据线（`geom_line`、`geom_segment` 等）按视觉层次分三档：

| 层级 | 宽度 | 适用场景 |
|------|------|---------|
| 常规 | 0.4 | 辅助参考线、CI 边界、个体轨迹、次要趋势 |
| 加粗 | 0.8 | 主曲线（RCS、KM）、主趋势线、组均值线 |
| 强调 | 1.2 | 仅限全幅单线核心图（极少使用） |

---

## 1.3 图表保存规范

```r
# 出版级分辨率常量 — 与 journal_standards.md::FIGURE_DPI 保持一致
PUBLICATION_DPI <- 300

# SVG（首选可编辑矢量格式，适合后期 Illustrator/Inkscape 微调）
ggsave("figure.svg", p, width = 7, height = 6)
# 使用 svglite 可获得更好的字体嵌入效果：
# svglite::svglite("figure.svg", width = 7, height = 6); print(p); dev.off()

# TIFF（LZW 压缩，投稿提交首选位图格式）
ggsave("figure.tiff", p, width = 7, height = 6, dpi = PUBLICATION_DPI, compression = "lzw")

# PDF（矢量，排版和预览）
ggsave("figure.pdf", p, width = 7, height = 6)

# PNG（快速预览，非投稿用）
ggsave("figure.png", p, width = 7, height = 6, dpi = PUBLICATION_DPI)
```

### 导出优先级

| 优先级 | 格式 | 用途 |
|--------|------|------|
| 1 | SVG | 可编辑矢量，期刊后期制作首选 |
| 2 | TIFF (LZW) | 投稿提交，位图标准 |
| 3 | PDF | 矢量，排版和预览 |
| 4 | PNG | 快速预览，非投稿用 |

**推荐同时导出**：SVG（编辑备份）+ TIFF（投稿提交）。

> **SVG 中文字体注意**：ggplot2 的 SVG 输出中中文字体可能不嵌入，需在 Illustrator 中手动修复。`svglite::svglite()` 提供更好的字体嵌入支持。投稿时以 TIFF/PDF 为主，SVG 留作编辑备份。

### 尺寸标准

| 用途 | 宽度 | 高度 | 格式 |
|------|------|------|------|
| 单栏图 | 8 cm (~3.15 in) | ≤ 20 cm | TIFF/PDF |
| 双栏图 | 17 cm (~6.7 in) | ≤ 20 cm | TIFF/PDF |
| 森林图/长图 | 17 cm | 自适应 | PDF |
| Nature 单栏 | 89 mm (~3.5 in) | 自适应 | TIFF/PDF |
| Nature 双栏 | 183 mm (~7.2 in) | 自适应 | TIFF/PDF |

所有输出必须 **≥300 DPI**，**Arial ≥8pt**。

### 字体族说明

`theme_pub(base_family = "sans")` 的字体族在不同平台上映射不同：

- **Windows**：`"sans"` 默认映射到 **Arial**，无需额外配置
- **Linux / macOS**：`"sans"` 可能映射到 DejaVu Sans 或 Helvetica，**不是 Arial**。如需严格使用 Arial：

```r
# 安装 extrafont（首次使用时）
install.packages("extrafont")
extrafont::font_import()   # 扫描系统字体（耗时较长，仅需一次）
extrafont::loadfonts()     # 加载字体到 R 会话

# 然后在 theme_pub() 中使用
theme_pub(base_family = "Arial")
```

> **注意：** `font_import()` 首次运行会扫描整个系统字体目录，可能需要几分钟。后续会话只需 `loadfonts()` 即可。在 Linux 上如果系统未安装 Arial，需先通过包管理器安装（如 `apt install ttf-mscorefonts-installer`）。

---

## 1.4 显著性标注规则

### p 值格式化

```r
format_pval <- function(p) {
  case_when(
    p < 0.001 ~ "italic(p) < 0.001",
    p < 0.01  ~ sprintf("italic(p) == %.3f", p),
    TRUE      ~ sprintf("italic(p) == %.3f", p)
  )
}
```

### 标注位置动态计算

```r
# 计算 y 轴范围，自动留空
y_range <- max(data$value, na.rm = TRUE) - min(data$value, na.rm = TRUE)
y_max <- max(data$value, na.rm = TRUE) + y_range * 0.1  # 留 10% 空白
y_step <- y_range * 0.08  # 多组比较时阶梯间距

# 使用 ggsignif（当需要显式标注比较时）
geom_signif(
  comparisons = list(c("Group1", "Group2")),
  map_signif_level = format_pval,
  test = "t.test",
  textsize = 3.5,
  parse = TRUE,
  y_position = y_max + seq(0, by = y_step, length.out = n_comparisons)
)
```

### 标注规则

- p < 0.001 写为 `p < 0.001`，不要写具体值
- p ≥ 0.001 写为 `p = 0.XXX`
- 仅标注主要比较，不要对每个子组对比都加星号
- 若比较 > 5 对，考虑用表格替代图中标注

---

## 1.5 比例指标的置信区间（Wilson Score）

用于敏感度、特异度、患病率等比例指标的 CI 计算。（优于正态近似法，尤其样本量较小时。）

```r
wilson_ci <- function(p, n, z_alpha = 1.96) {
  denominator <- 1 + z_alpha^2 / n
  centre <- (p + z_alpha^2 / (2 * n)) / denominator
  margin <- z_alpha * sqrt(p * (1 - p) / n + z_alpha^2 / (4 * n^2)) / denominator
  c(lower = centre - margin, upper = centre + margin)
}
```

**何时必须使用：** ROC 分析中的敏感度/特异度 CI、任何比例指标的置信区间。

---

## 1.6 拼图布局规范

```r
library(patchwork)

# 基础多图组合
combined <- wrap_plots(plot_list, ncol = 2) +
  plot_annotation(tag_levels = "a") &
  theme(plot.tag = element_text(size = 10, face = "bold"),
        plot.tag.position = c(0.02, 0.98),
        legend.position = "bottom")
```

### 基础规范

- 使用 `wrap_plots()` 而非 `grid.arrange()`（自动对齐）
- `&` 统一所有子图的主题和图例位置
- 同一主题的多张子图共享统一配色

### 面板标签

- 标签格式：**小写加粗** a, b, c（Nature 期刊风格）
- 实现：`plot_annotation(tag_levels = "a")`，配合 `theme(plot.tag = ...)` 调整样式
- 标签位置：左上角，`plot.tag.position = c(0.02, 0.98)`
- 大写 A/B/C 也可接受，但同一手稿内保持一致

### 布局原型（Layout Archetypes）

根据图的叙事目的选择 patchwork 布局：

| 原型 | 适用场景 | patchwork 代码 |
|------|----------|----------------|
| **定量网格** (quantitative-grid) | 多个同类定量比较 | `wrap_plots(p1, p2, p3, p4, ncol = 2)` |
| **示意图主导** (schematic-led) | 1 个核心大图 + 辅助小图 | `p_main + (p_aux1 / p_aux2) + plot_layout(widths = c(2, 1))` |
| **临床三联画** (clinical-triptych) | 基线 → 干预 → 结局的三阶段 | `p1 + p2 + p3 + plot_layout(ncol = 3, widths = c(1, 1.5, 1))` |
| **非对称英雄** (asymmetric-hero) | 1 个核心面板占主导 + 补充面板 | `p_hero + (p1 / p2 / p3) + plot_layout(widths = c(3, 1))` |

**布局选择流程**：
- 所有面板回答同类问题？→ **quantitative-grid**
- 有一个核心结论面板？→ **schematic-led** 或 **asymmetric-hero**
- 时间/流程叙事？→ **clinical-triptych**

**非等面板原则**：不要强制所有面板等宽等高。如果证据不是同等重要，让主证据面板占据更大面积。

```r
# 示意图主导：核心面板占 60% 宽度
design <- "
AAAA
BBCD
"
fig <- p_schematic + p_b + p_c + p_d +
  plot_layout(design = design, heights = c(1.8, 1))

# 定量网格 + 共享图例
fig <- (p_a | p_b) / (p_c | p_d) +
  plot_layout(guides = "collect") &
  theme(legend.position = "bottom")

# 非对称英雄
fig <- p_hero + (p1 / p2 / p3) +
  plot_layout(widths = c(3, 1))
```

### 图例经济（Legend Economy）

优先级从高到低：

1. **直接标注 (Direct Labels)**: 用 `geom_text()` 或 `ggrepel::geom_text_repel()` 直接在图上标注组名，省去图例
2. **共享图例条 (Shared Legend Strip)**: 多面板共享同一图例，用 `plot_layout(guides = "collect")` 收集
3. **单面板图例**: 仅在一个子图保留图例，其余用 `theme(legend.position = "none")` 隐藏

```r
# 方式 1: 共享图例（推荐）
combined <- (p1 + p2 + p3) +
  plot_layout(guides = "collect") &
  theme(legend.position = "bottom")

# 方式 2: 直接标注（无图例）
p + ggrepel::geom_text_repel(aes(label = group), size = 3) +
  theme(legend.position = "none")

# 方式 3: 仅保留一个面板的图例
(p1 & theme(legend.position = "none")) + p2 + plot_layout(ncol = 2)
```

**图例规则**：
- 多面板图**禁止**每个面板重复相同图例
- 图例位置优先底部 (`"bottom"`)，其次顶部 (`"top"`)
- 避免右侧图例在多面板布局中浪费水平空间

---

## 1.7 目录先行规则

**所有生成输出文件的 R 代码必须在使用路径前确保目录存在。**

```r
# 正确：写入前创建目录
dir.create("04_Outputs/01_BaselineTable", recursive = TRUE, showWarnings = FALSE)
ggsave("04_Outputs/01_BaselineTable/Table1.png", p, dpi = PUBLICATION_DPI)

# 错误：假设目录已存在（会因路径不存在而报错）
ggsave("04_Outputs/01_BaselineTable/Table1.png", p, dpi = PUBLICATION_DPI)  # 可能失败
```

### 目录创建规范

| 输出类型 | 创建模式 | 示例 |
|---------|---------|------|
| `04_Outputs/XX_MethodName/` | 每次 script 运行时创建 | `dir.create("04_Outputs/02_GroupComparison", recursive = TRUE, showWarnings = FALSE)` |
| `03_AnalysisMethods/XX_MethodName/` | 每次 script 运行时创建 | 同上 |
| 方法说明 文件 | 作为最后一步写入 | `writeLines(readme, "03_AnalysisMethods/XX_MethodName/方法说明.md")` |

- 使用 `recursive = TRUE` 确保父目录自动创建
- 使用 `showWarnings = FALSE` 避免目录已存在时的警告
- **不在 script 外假设目录已存在**

---

## 1.8 反冗余检查清单

> 每张图的每个面板必须回答一个独特的问题。在生成多面板图之前，逐项检查以下清单。

### 检查项

| # | 检查项 | 不通过的典型症状 | 修正方案 |
|---|--------|-----------------|----------|
| 1 | 每个面板是否回答一个不同的分析问题？ | 两个面板展示同一变量的不同切面 | 合并为一个综合面板 |
| 2 | 是否可以在不损失信息的前提下删除某个面板？ | 删除后核心结论不变 | 删除冗余面板 |
| 3 | 是否存在可以用表格替代的面板？ | 面板仅展示 2-3 个数值 | 用表格替代，图让位给更有信息量的面板 |
| 4 | 两个面板是否仅因分组方式不同而重复？ | 同一变量按性别和年龄各画一次 | 选信息量更大的分组，或合并为分面 |
| 5 | 面板数量是否超过期刊限制？ | 6 面板但期刊限制 4 张主图 | 拆入补充材料 |

### 使用方式

在 Figure Contract（§1.0）的“面板映射”字段中，为每个面板写出独特问题。如果发现两个面板的问题重叠，必须合并或删除。

### 常见冗余陷阱

| 陷阱 | 示例 | 修正 |
|------|------|------|
| 绝对值 + 绝对值 | 堆积柱状图(%) + 同一 % 的热图 | 热图改为 Z-score 偏差视图 |
| 子集与父集 | 总体排名柱状图 + 某亚组的同样排名 | 替换为散点图展示亚组与总体关系 |
| 两个排名 | 两个相关指标的排名柱状图 | 其中一个改为气泡散点图 |
| 同数据不同图 | 饼图 + 堆积柱状图 | 合并或替换为关系图 |

---

## 1.9 Y 轴紧缩与坐标规范

### 核心规则

永远不要让 Y 轴范围远大于数据实际范围。如果数据集中在 80-95，不要画 0-100 的轴。

```r
# ✘ 错误：Y 轴 0-100，但数据范围是 82-94
ggplot(df, aes(x, y)) + geom_point() + scale_y_continuous(limits = c(0, 100))

# ✔ 正确：自动紧缩 + 适度留白
y_range <- range(df$y, na.rm = TRUE)
y_pad <- diff(y_range) * 0.08  # 8% 留白
ggplot(df, aes(x, y)) + geom_point() +
  coord_cartesian(ylim = c(y_range[1] - y_pad, y_range[2] + y_pad))
```

### 留白计算规则

```r
# 通用留白：数据范围的 5-10%
y_range <- range(data$value, na.rm = TRUE)
y_pad <- diff(y_range) * 0.08  # 8% 留白
y_limits <- c(y_range[1] - y_pad, y_range[2] + y_pad)

# 比例数据 (0-1)：留白不超过 0.05
# 百分比数据 (0-100)：留白不超过 5%
```

### 例外情况

| 场景 | 是否允许 0 起点 | 理由 |
|------|----------------|------|
| 柱状图（展示计数/频数） | **是，必须** | 柱高编码量级，截断会误导 |
| 折线图/散点图（展示趋势） | 否，紧缩 | 点位置编码值，截断不影响 |
| 森林图（效应量） | 否，以 null 值为中心 | 展示 CI 跨越 null 值 |
| 生存曲线 | **是，必须 0-1** | 概率轴标准化 |
| ROC 曲线 | **是，必须 0-1** | 概率轴标准化 |

### `coord_cartesian` vs `scale_y_continuous`

- `coord_cartesian(ylim = ...)`: 放大视图，不丢弃数据（**推荐**）
- `scale_y_continuous(limits = ...)`: 先裁剪数据再绘图（可能导致 geom 丢失）
- 默认使用 `coord_cartesian`，仅在需要显式排除异常值时使用 `scale_y_continuous`

---

# 第二部分：Analysis Patterns（按需选用的分析模式）

以下代码模式针对特定分析方法。**仅在对应方法被确认需要时使用。** 每种模式标注了适用条件和（更重要的）不适用条件。

---

## 2.1 三层绘图法（箱线图 + 散点叠加）

### 意图
既展示数据分布的整体概览（箱线图），又展示每个个体的具体数值（散点），避免箱线图掩盖数据特征。

### 模式
```r
ggplot(data, aes(x = group, y = value)) +
  geom_jitter(aes(color = group), alpha = 0.6,
              width = 0.2, size = 2) +
  geom_boxplot(aes(fill = group), alpha = 0.3, color = "black",
               outlier.shape = NA, width = 0.5, linewidth = 0.4) +
  scale_color_manual(values = get_palette(length(unique(data$group)))) +
  scale_fill_manual(values = get_palette(length(unique(data$group)))) +
  labs(x = "Group", y = "Value") +
  theme_pub()
```

### 适用条件
- 组间比较，且样本量 < 200
- 需要展示个体变异时

### 不适用条件
- 样本量 ≥ 200：仅用箱线图或小提琴图，省略散点
- 分组数 > 6：改用小提琴图 + 简明箱线图

### 变体
- 小提琴图替代箱线图：`geom_violin(alpha = 0.3)` + `geom_boxplot(width = 0.1)`

---

## 2.2 Z-score 标准化可视化

### 意图
将不同量纲的变量统一到同一尺度上进行可视化比较。

### 模式
```r
scale_this <- function(x) {
  (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)
}
```

### 适用条件
- 同一图中展示多个不同量纲的变量（如将 IL-6、CRP、TNF-α 放在一起比较）
- 热图中统一色标范围
- 比较不同标志物在组间的相对差异倍数

### ⚠️ 不适用条件（重要）
- 变量单位一致或天然可比（如多个血压指标，单位均为 mmHg）—— 标准化会丢失原始尺度信息
- 需要报告原始单位以保持临床可解释性（如 "BMI 每增加 1 kg/m² 的风险"）
- 仅展示单个变量时 —— 不需要标准化
- 受众为临床医生时优先保留原始值

---

## 2.3 ROC 分析双模式

### 意图
区分"仅标志物"（Unadjusted）和"调整协变量后"（Adjusted）的区分能力。

### 模式
```r
# Unadjusted：直接基于标志物值
library(pROC)
roc_obj <- roc(outcome ~ biomarker, data = df)
auc_obj <- auc(roc_obj)
ci_obj <- ci.auc(roc_obj)

# Adjusted：先做 Logistic 回归，用预测概率做 ROC
model <- glm(Outcome ~ biomarker + age + sex, data = df, family = binomial)
pred_prob <- predict(model, type = "response")
roc_adjusted <- roc(df$Outcome, pred_prob)

# 最佳阈值选取
coords_best <- coords(roc_obj, "best",
  ret = c("threshold", "sensitivity", "specificity",
          "ppv", "npv", "accuracy"))
```

### 可视化
```r
# ROC 曲线绘制模板
roc_df <- data.frame(
  FPR = 1 - roc_obj$specificities,
  TPR = roc_obj$sensitivities
)
p <- ggplot(roc_df, aes(x = FPR, y = TPR)) +
  geom_line(color = get_hero_color(), linewidth = 0.8) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed",
              color = "grey50", linewidth = 0.4) +
  labs(x = "1 - Specificity (FPR)",
       y = "Sensitivity (TPR)",
       title = sprintf("ROC Curve (AUC = %.3f)", as.numeric(auc_obj))) +
  coord_equal() +
  theme_pub()

# 多模型对比（Unadjusted vs Adjusted）
roc_adj_df <- data.frame(
  FPR = 1 - roc_adjusted$specificities,
  TPR = roc_adjusted$sensitivities
)
p_compare <- ggplot() +
  geom_line(data = roc_df, aes(x = FPR, y = TPR),
            color = get_hero_color(), linewidth = 0.8) +
  geom_line(data = roc_adj_df, aes(x = FPR, y = TPR),
            color = get_baseline_color(), linewidth = 0.8) +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed",
              color = "grey50", linewidth = 0.4) +
  labs(x = "1 - Specificity (FPR)", y = "Sensitivity (TPR)",
       color = "Model") +
  scale_color_manual(values = c(get_hero_color(), get_baseline_color()),
                     labels = c("Unadjusted", "Adjusted")) +
  coord_equal() +
  theme_pub()
```

### 适用条件
- 生物标志物诊断价值评估
- 需要对比"单纯标志物" vs "综合模型"的 AUC
- 需要报告最佳阈值和对应的诊断性能

---

## 2.4 LASSO 特征选择流程

### 意图
从高维生物标志物中筛选最具有区分能力的特征子集。

### 模式
```r
library(glmnet)
cv_model <- cv.glmnet(X_train, Y_train, family = "binomial", alpha = 1)
best_lambda <- cv_model$lambda.min

final_model <- glmnet(X_train, Y_train, family = "binomial", alpha = 1,
                      lambda = best_lambda)

coef_matrix <- as.matrix(coef(final_model))
non_zero_coefs <- coef_matrix[coef_matrix[, 1] != 0 &
                                rownames(coef_matrix) != "(Intercept)", , drop = FALSE]
```

### 关键细节
- 训练集/验证集分割先行，避免数据泄露
- `lambda.min` 是最小交叉验证误差，`lambda.1se` 更保守（选入更少变量）
- 提取的特征用于下游建模，而非直接解释系数大小

---

## 2.5 混淆矩阵热图

### 意图
直观展示分类结果的混淆情况，同时显示频数和百分比。

### 模式
```r
ggplot(cm_df, aes(x = Actual, y = Predicted)) +
  geom_tile(aes(fill = Freq), color = "white", linewidth = 1) +
  geom_text(aes(label = sprintf("%d\n(%.1f%%)", Freq, Percent)),
            size = 4, fontface = "bold") +
  scale_fill_gradient(low = "white", high = get_hero_color()) +
  coord_fixed() +
  theme_pub()
```

### 适用条件
- 分类模型性能展示
- ROC 分析中阈值确定后的分类结果
- 训练集 vs 验证集对比

---

## 2.6 森林图（AUC/OR/HR 汇总）

### 意图
在一个图中汇总多个指标的效应量和置信区间。

### 模式
```r
ggplot(df, aes(x = estimate, y = reorder(label, estimate))) +
  geom_point(size = 4, color = get_hero_color()) +
  geom_errorbarh(aes(xmin = lower, xmax = upper),
                 height = 0.2, color = get_hero_color()) +
  geom_vline(xintercept = reference, linetype = "dashed",
             color = get_baseline_color(), linewidth = 0.4) +
  labs(x = "AUC (95% CI)", y = "") +
  theme_pub()
```

### 适用条件
- 多标志物 AUC 汇总
- 亚组分析结果汇总
- 多因素回归结果可视化

---

## 2.7 风险分层 jitter plot

### 意图
展示每个个体的预测概率，按真实结局分组，便于目测模型分离效果。

### 模式
```r
ggplot(df, aes(x = jitter(as.numeric(factor(outcome)), amount = 0.1),
               y = predicted_prob, color = as.factor(outcome))) +
  geom_jitter(size = 2.5, alpha = 0.7, width = 0.15) +
  geom_hline(yintercept = cutoff, linetype = "dashed",
             color = get_accent_color(), linewidth = 0.4) +
  scale_color_manual(values = get_palette(2)) +
  labs(x = "Actual Group", y = "Predicted Probability") +
  theme_pub()
```

### 适用条件
- 展示模型预测概率在两组间的分布
- 验证集上展示分类效果

---

## 2.8 训练集/验证集分割模式

### 意图
从数据中识别训练集和验证集（当 TYPE 列存在时），fallback 到随机分割。

### 模式
```r
train_set <- df %>%
  filter(grepl("TRAIN|TRANNING", toupper(.data[[type_col]])))
validation_set <- df %>%
  filter(grepl("VAL|VALIDATION", toupper(.data[[type_col]])))

# fallback：随机 70/30 分割（当无 TYPE 列时）
if (nrow(train_set) == 0 || nrow(validation_set) == 0) {
  set.seed(42)
  train_idx <- sample(1:nrow(df), size = round(0.7 * nrow(df)))
  train_set <- df[train_idx, ]
  validation_set <- df[-train_idx, ]
}
```

### 注意
- 容错匹配（大小写不敏感，支持缩写）
- 随机分割必须设 `set.seed()` 并记录种子值
- 分割信息写入 方法说明

---

## 2.9 KM 生存曲线美化

### 意图
展示生存函数随时间的变化，比较两组或多组的生存率差异。生存分析（§3.4）的标准可视化输出。

### 模式
```r
library(survival)
library(survminer)

fit <- survfit(Surv(time, event) ~ group, data = df)

ggsurvplot(fit, data = df,
  pval = TRUE, pval.method = TRUE,
  risk.table = TRUE, risk.table.col = "strata",
  palette = c("#0072B5", "#BC3C29"),  # Nature 双色，色盲友好
  xlab = "Time (months)", ylab = "Survival probability",
  legend.title = "Group",
  ggtheme = theme_pub())
```

### 适用条件
- 时间-事件数据（生存时间 + 事件状态）
- 两组或多组生存率比较
- 需要同时展示风险表（number at risk）

### 不适用条件
- 非生存数据（连续结局用箱线图/散点图）
- 仅关注终点事件发生率而非时间过程（用 Logistic 回归 + 柱状图）
- 样本量极小（<10 per group）时 KM 曲线不稳定，需谨慎解读

---

## 2.10 相关性矩阵热图

### 意图
展示多个连续变量间的相关性结构，快速识别强关联变量对，辅助回归建模的变量筛选。

### 模式
```r
library(ggcorrplot)

corr_matrix <- cor(data, method = "spearman", use = "pairwise.complete.obs")
ggcorrplot(corr_matrix,
  type = "lower",
  lab = TRUE, lab_size = 3,
  colors = c(get_hero_color(), "white", get_baseline_color()),  # 蓝白红三色
  ggtheme = theme_pub())
```

### 方法选择
- **Spearman**（默认）：适用于偏态分布或有序变量，不需要正态性假设
- **Pearson**：仅当所有变量均满足正态分布时使用

### 适用条件
- 多变量关联探索（≥3 个连续变量）
- 回归建模前的变量筛选（识别多重共线性）
- 展示相关系数的方向和强度

### 不适用条件
- 仅两个变量：用散点图更直观（可叠加回归线和 CI）
- 分类变量间的关联：用卡方检验或 mosaic plot
- 因果推断需要：相关不等于因果

---

## 2.11 CONSORT 流程图

### 意图
RCT 受试者筛选、随机化、干预和随访各阶段的人数与脱落原因可视化。CONSORT 声明的必备图表。

### 模式
```r
library(consort)

# 构建 CONSORT 图
g <- consort_plot(
  screening   = "Screened\nn = 320",
  randomized  = "Randomized\nn = 200",
  allocation  = list(
    "Treatment A\nn = 100",
    "Treatment B\nn = 100"
  ),
  follow_up   = list(
    "Completed\nn = 88",
    "Completed\nn = 91"
  ),
  analysis    = list(
    "ITT analysis\nn = 100",
    "ITT analysis\nn = 100"
  ),
  side_boxes  = list(
    "Excluded (n = 120):\n  Not meeting criteria (n = 85)\n  Declined (n = 25)\n  Other (n = 10)",
    "Lost to follow-up (n = 12)",
    "Lost to follow-up (n = 9)",
    "Discontinued (n = 5)",
    "Discontinued (n = 3)"
  ),
  cex         = 0.8
)

# 保存
ggsave("CONSORT_flow.tiff", g, width = 10, height = 8, dpi = PUBLICATION_DPI, compression = "lzw")
```

### 适用条件
- RCT 研究设计
- 需要展示受试者流程的 CONSORT 声明要求

### 不适用条件
- 观察性研究（改用 STROBE 流程图，可用 `DiagrammeR` 自定义）
- 回顾性研究（无需 CONSORT 图）

---

## 2.12 Love Plot（PSM 平衡诊断）

### 意图
展示倾向性评分匹配/加权前后协变量标准化均值差（SMD）的变化，判断平衡是否达标（|SMD| < 0.1）。

### 模式
```r
library(cobalt)

# 匹配前平衡
bal_before <- bal.tab(
  treatment ~ age + sex + bmi + education + comorbidity_score,
  data = data,
  stats = "mmd"
)

# 匹配后平衡（MatchIt 输出）
library(MatchIt)
m_out <- matchit(treatment ~ age + sex + bmi + education + comorbidity_score,
                 data = data, method = "nearest", ratio = 1)
bal_after <- bal.tab(m_out, stats = "mmd")

# Love Plot
love.plot(bal_after,
  threshold = 0.1,
  stars = "raw",
  colors = c("gray70", "#0072B5"),
  shapes = c(16, 17),
  ggtheme = theme_pub()) +
  labs(title = "Covariate Balance Before and After PSM")
```

### 适用条件
- 倾向性评分匹配（PSM）或逆概率加权（IPTW）后
- 需要证明匹配/加权成功改善协变量平衡

### 不适用条件
- 无倾向性评分分析时
- RCT 研究（随机化已保证平衡）

---

## 2.13 剂量反应 / RCS 曲线

### 意图
用限制性立方样条（Restricted Cubic Splines）展示连续暴露变量与结局的非线性剂量反应关系。

### 模式
```r
library(rms)
library(ggplot2)

# 拟合 RCS 模型
dd <- datadist(data)
options(datadist = "dd")

# 连续结局（线性回归）
fit_ols <- ols(outcome ~ rcs(exposure, 4) + age + sex, data = data)
anova(fit_ols)  # 检验非线性 P 值

# 二分类结局（Logistic 回归）
fit_glm <- lrm(outcome ~ rcs(exposure, 4) + age + sex, data = data)

# 可视化 RCS 曲线
p <- Predict(fit_ols, exposure, fun = function(x) x,
             ref.zero = FALSE)
plot(p, xlab = "Exposure (units)", ylab = "Adjusted outcome",
     col = get_hero_color(), lwd = 2)
# 或用 ggplot2:
ggplot(data = p, aes(exposure, yhat)) +
  geom_ribbon(aes(ymin = lower, ymax = upper), fill = get_hero_color(), alpha = 0.2) +
  geom_line(color = get_hero_color(), linewidth = 0.8) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray50") +
  labs(x = "Exposure", y = "Adjusted effect (95% CI)",
       title = "Non-linear dose-response relationship") +
  theme_pub()
```

### 适用条件
- 连续暴露变量（如 BMI、血压、生物标志物浓度）
- 疑似非线性剂量反应关系
- 探索性分析或主分析的补充

### 不适用条件
- 暴露已二分类化（丢失连续信息）
- 样本量过小（< 100）时 RCS 不稳定

---

## 2.14 瀑布图（Waterfall Plot）

### 意图
展示每个受试者对治疗的最佳反应（如肿瘤缩小百分比），常用于肿瘤疗效评估（RECIST 标准）。

### 模式
```r
# 数据准备：每人一行，包含最佳变化百分比
df <- data.frame(
  patient_id = 1:40,
  best_change = runif(40, -100, 50),  # 负值=缩小，正值=增大
  group = rep(c("Treatment", "Control"), each = 20)
)

# 按变化幅度排序
df <- df[order(df$best_change), ]
df$patient_id <- factor(df$patient_id, levels = df$patient_id)

# 反应分类
response_threshold <- -30   # PR: ≥ 30% 缩小
progression_threshold <- 20 # PD: ≥ 20% 增大

p <- ggplot(df, aes(x = patient_id, y = best_change, fill = group)) +
  geom_bar(stat = "identity", width = 0.8) +
  geom_hline(yintercept = 0, color = "black", linewidth = 0.4) +
  geom_hline(yintercept = response_threshold,
             linetype = "dashed", color = get_hero_color()) +
  geom_hline(yintercept = progression_threshold,
             linetype = "dashed", color = get_baseline_color()) +
  scale_fill_manual(values = get_palette(2)) +
  labs(x = "", y = "Best % change from baseline",
       title = "Waterfall plot of best tumor response") +
  theme_pub() +
  theme(axis.text.x = element_blank(),
        legend.position = "top")
```

### 适用条件
- 肿瘤疗效反应评估（RECIST / iRECIST）
- 每个受试者的最佳变化百分比可视化

### 不适用条件
- 非肿瘤疗效研究（改用配对连线图）
- 仅展示组均值时（用箱线图）

---

## 2.15 漏斗图（Funnel Plot）

### 意图
Meta 分析中检测发表偏倚，判断小样本研究是否偏向阳性结果。

### 模式
```r
library(meta)
library(ggplot2)

# Meta 分析模型
m <- metagen(TE, seTE, data = meta_data, sm = "OR", method.tau = "REML")

# 基础漏斗图（base R）
funnel(m, pch = 16, col = get_hero_color(),
       studlab = TRUE, xlab = "Effect size (log OR)")

# ggplot2 版本
funnel_data <- data.frame(
  effect = m$TE,
  se     = m$seTE,
  study  = m$studlab
)

p <- ggplot(funnel_data, aes(x = effect, y = se)) +
  geom_point(size = 3, color = get_hero_color(), alpha = 0.7) +
  geom_vline(xintercept = m$TE.random, linetype = "dashed",
             color = get_baseline_color()) +
  geom_segment(
    aes(x = m$TE.random - 1.96 * se, xend = m$TE.random + 1.96 * se,
        y = se, yend = se),
    data = data.frame(se = seq(0.05, max(funnel_data$se), length.out = 100)),
    color = "grey70", alpha = 0.5, linewidth = 0.4
  ) +
  scale_y_reverse() +
  labs(x = "Effect size (log OR)", y = "Standard error",
       title = "Funnel plot for publication bias") +
  theme_pub()

# Egger 检验（统计检测）
metabias(m, method = "Egger", plotit = FALSE)
```

### 适用条件
- Meta 分析发表偏倚检测
- 研究数量 ≥ 10（少于 10 时漏斗图无法可靠判断）

### 不适用条件
- 研究数量 < 10
- 非 Meta 分析场景

---

## 2.16 UpSet / Venn 图

### 意图
展示多个集合的交叉关系，如共病模式、药物联用、多标志物共现等。UpSet 图在集合数 > 3 时优于 Venn 图。

### 模式
```r
library(ComplexUpset)

# 数据准备：每行一个受试者，每列一个条件（0/1）
conditions <- c("Hypertension", "Diabetes", "Obesity", "Dyslipidemia", "Smoking")

# UpSet 图
upset(data, conditions,
  base_annotations = list(
    "Intersection size" = intersection_size(
      counts = TRUE,
      text = list(size = 3)
    )
  ),
  set_sizes = upset_set_size(
    geom = geom_bar(fill = get_hero_color(), width = 0.6)
  ),
  stripes = upset_stripes(
    geom = geom_segment(color = "gray90"),
    aes = aes(fill = "gray95")
  ),
  min_size = 5,
  width_ratio = 0.2,
  themes = upset_default_themes(theme_pub())
)
```

### 适用条件
- 多集合交叉关系可视化（≥ 3 个集合）
- 共病模式、药物联用、多标志物共现分析

### 不适用条件
- 仅 2 个集合（用简单条形图或表格即可）
- 集合数 > 10（图表过于复杂）

---

## 2.17 Sankey / Alluvial 图

### 意图
展示分类变量在不同时间点或条件下的变化流，如治疗反应转移、疾病状态转变。

### 模式
```r
library(ggalluvial)

# 数据准备：每人一行，包含基线和随访的分类状态
df <- data.frame(
  baseline = c("Remission", "Remission", "Active", "Active", "Active"),
  followup = c("Remission", "Active", "Active", "Remission", "Remission"),
  count = c(45, 12, 8, 18, 25)
)

p <- ggplot(df, aes(y = count, axis1 = baseline, axis2 = followup)) +
  geom_alluvium(aes(fill = baseline), width = 0.3, alpha = 0.7) +
  geom_stratum(width = 0.3, fill = "white", color = "black") +
  geom_text(stat = "stratum", aes(label = afterglow(stratum)), size = 3) +
  scale_fill_manual(values = get_palette(3)) +
  labs(x = "", y = "Number of patients",
       title = "Treatment response transition from baseline to follow-up") +
  theme_pub() +
  theme(legend.position = "top")
```

### 适用条件
- 分类状态在两个或多个时间点的变化流
- 治疗反应转移、疾病分期变化、诊断重分类

### 不适用条件
- 连续变量变化（用配对连线图或斜率图）
- 状态类别 > 6（图表过于复杂）

---

## 2.18 配对连线图

### 意图
展示纵向设计中每个受试者的个体轨迹（前后比较），直观呈现组内变化和组间差异。

### 模式
```r
library(ggplot2)

# 数据准备：长格式，每人多行
# df: id, time, value, group
p <- ggplot(df, aes(x = time, y = value, group = id, color = group)) +
  geom_line(alpha = 0.3, linewidth = 0.4) +
  geom_point(size = 2, alpha = 0.6) +
  # 叠加组均值趋势（粗线）
  stat_summary(aes(group = group), fun = mean,
               geom = "line", linewidth = 0.8, color = "black") +
  stat_summary(aes(group = group), fun = mean,
               geom = "point", size = 4, shape = 18, color = "black") +
  scale_color_manual(values = get_palette(2)) +
  labs(x = "Time point", y = "Outcome value",
       title = "Individual trajectories with group means") +
  theme_pub() +
  theme(legend.position = "top")

# 简化版：仅前后配对（2 个时间点）
p_simple <- ggplot(df_wide, aes(x = 1, y = pre_value)) +
  geom_segment(aes(xend = 2, yend = post_value, color = group),
               alpha = 0.4, linewidth = 0.4) +
  geom_point(aes(color = group), size = 3) +
  geom_point(aes(x = 2, y = post_value, color = group), size = 3) +
  scale_color_manual(values = get_palette(2)) +
  scale_x_continuous(breaks = c(1, 2), labels = c("Pre", "Post")) +
  labs(x = "", y = "Outcome value",
       title = "Paired pre-post comparison") +
  theme_pub() +
  theme(legend.position = "top")
```

### 适用条件
- 纵向/配对设计，样本量 < 100
- 展示个体轨迹和组均值趋势
- 前后比较的干预效果可视化

### 不适用条件
- 样本量 ≥ 100（线条过于密集，改用均值±CI 趋势图）
- 仅 2 时间点且样本量大（改用配对差异的分布图）

---

## 2.19 日历 / 趋势图

### 意图
展示某指标随时间的变化趋势，如患病率时间趋势、入院率变化、治疗方案转变等。

### 模式
```r
library(ggplot2)

# 数据准备：每行一个时间点 + 汇总指标
df <- data.frame(
  year = 2010:2024,
  prevalence = c(12.3, 12.8, 13.1, 13.5, 14.0, 14.2, 14.8, 15.1,
                 15.5, 15.9, 16.3, 16.0, 16.5, 17.1, 17.5),
  lower = c(11.5, 12.0, 12.3, 12.7, 13.2, 13.4, 14.0, 14.3,
            14.7, 15.1, 15.5, 15.2, 15.7, 16.3, 16.7),
  upper = c(13.1, 13.6, 13.9, 14.3, 14.8, 15.0, 15.6, 15.9,
            16.3, 16.7, 17.1, 16.8, 17.3, 17.9, 18.3)
)

p <- ggplot(df, aes(x = year, y = prevalence)) +
  geom_ribbon(aes(ymin = lower, ymax = upper), fill = get_hero_color(), alpha = 0.2) +
  geom_line(color = get_hero_color(), linewidth = 0.8) +
  geom_point(size = 3, color = get_hero_color()) +
  # 可选：添加趋势线
  geom_smooth(method = "lm", se = FALSE, linetype = "dashed",
              color = get_baseline_color(), linewidth = 0.4) +
  scale_x_continuous(breaks = seq(2010, 2024, 2)) +
  labs(x = "Year", y = "Prevalence (%)",
       title = "Temporal trend of prevalence (95% CI)") +
  theme_pub()
```

### 适用条件
- 时间趋势分析（患病率、发病率、死亡率、入院率等）
- 多时点数据的纵向趋势可视化
- 需要展示置信区间的趋势变化

### 不适用条件
- 仅 2 个时间点（用配对比较或差异图）
- 非时间序列数据
