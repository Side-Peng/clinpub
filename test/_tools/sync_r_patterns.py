"""把 r_patterns.md 的 §1.2 / §1.3 从"代码副本"改为"契约"。"""
import io

P = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\claude-code\pipeline\references\r_patterns.md"
lines = io.open(P, encoding="utf-8").read().split("\n")

# 定位 §1.2 与 §1.4（1-indexed → 0-indexed）
start = next(i for i, l in enumerate(lines) if l.startswith("## 1.2 "))
end = next(i for i, l in enumerate(lines) if l.startswith("## 1.4 "))

NEW = '''## 1.2 出版级主题与风格包

> 实现只有一份：`pipeline/templates/_figure_config.R`（生成到项目的 `04_Outputs/_figure_config.R`）。
> 本节只写**契约**，不复制代码——复制出来的副本必然与实现漂移。

### 1.2.1 三条硬约束

1. **画布优先**：先定印刷尺寸（mm），字号随之推导；不是先设字号再缩放。
2. **字号 5–7 pt**：低于 5pt 印不清，高于 7pt 挤不进栏宽。
3. **线宽分层**：数据线 > 轴线 > 参考线。视觉重量应与信息重要度一致。

### 1.2.2 风格包（`quality.style`）

| 包 | 单栏 mm | 双栏 mm | 轴线 | 数据线 | 主色 / 对比色 |
|---|---|---|---|---|---|
| `nature`（默认） | 89 | 183 | 0.35 | 0.60 | `#0072B2` / `#D55E00`（Okabe-Ito） |
| `lancet` | 90 | 190 | 0.50 | 0.75 | `#00468B` / `#ED0000` |
| `jama` | 86 | 178 | 0.45 | 0.70 | `#374E55` / `#B24745` |
| `nejm` | 86 | 173 | 0.45 | 0.70 | `#0072B5` / `#BC3C29` |

> **只有 `nature`** 的栏宽、字号、配色来自 Nature 官方 figure guide
> （89/183 mm、5–7 pt、Okabe-Ito 色盲友好色）。其余三个包的栏宽为常见值，
> 投稿前须对照目标期刊 Guide for Authors 核对。

### 1.2.3 覆盖与派生

```yaml
quality:
  style: "nature"
  style_overrides:            # 只写要改的项，命名向量按名字覆盖
    line: {axis: 0.5}
    palette: {main: "#123456"}
```

派生项（不要在方法脚本里手写死值）：

| 变量 / 函数 | 含义 |
|---|---|
| `FIG_WIDTH_MM` | 当前包的栏宽命名向量（single / double） |
| `pub_base_size(width_mm)` | 单栏 → `base_size.single`；双栏 → `.double`；配置显式给了就优先 |
| `LW_DATA` / `LW_AXIS` / `LW_REF` | 当前包的线宽层级 |
| `TICK_LENGTH_PT` | 刻度长度 |
| `pal("main"\|"contrast"\|"accent"\|"neutral"\|"ink")` | 按**角色**取色 |
| `get_palette(n)` | 按分组数取色（角色驱动的预设） |

### 1.2.4 禁止事项

- 在方法脚本里重定义 `theme_pub()` / `get_palette()` / `save_figure()`
- 写死字号（如 `base_size = 11`）——必须走 `pub_base_size()`
- 覆盖 `axis.title.y` 时不带 `angle = 90`——`element_text()` 的 angle 默认 0，
  会把继承来的竖排标题转平

---

## 1.3 图表保存规范

**主图默认 `pdf + svg`（矢量）**。Nature 的 figure guide 明确不接受 tiff/png 作主图；
tiff 仅用于 Extended Data（300 dpi，≤ 10 MB）。

```r
save_figure(p, "04_Outputs/01_xxx/fig1",
            width_mm = FIG_WIDTH_MM[["single"]], height_mm = 80)
# → fig1.pdf + fig1.svg（格式由 STYLE$main_formats 决定）
```

| 场景 | formats | dpi |
|---|---|---|
| 正文主图 | `c("pdf", "svg")`（默认） | 不适用（矢量） |
| 补充材料 | `c("tiff")` | 300 |
| 预览 / 汇报 | `c("png")` | 300 |

**为什么指定设备**：`svglite` 保留可编辑文字（投稿要求文字可编辑）、
`cairo_pdf` 内嵌字体（TrueType 42）、`ragg` 保证位图质量。
`ggsave` 的默认设备在部分平台会丢字体或把文字转曲。

---

'''

lines[start:end] = NEW.split("\n")
io.open(P, "w", encoding="utf-8").write("\n".join(lines))
print(f"  已替换 §1.2/§1.3（原 {end - start} 行 → 新 {len(NEW.split(chr(10)))} 行）")
