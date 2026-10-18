#!/usr/bin/env rscript
"""把 nature-figure 的审美原则写进 clinpub 的 _figure_config.R（改源文件）。"""
import io
import re

P = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\claude-code\pipeline\templates\_figure_config.R"
t = io.open(P, encoding="utf-8").read()

# ---- 1. 配置读取：base_size 允许为 null，新增 grid 开关 -------------------
old = """theme_base_size    <- if (!is.null(theme_cfg$base_size)) as.numeric(theme_cfg$base_size) else 11
theme_base_family  <- if (!is.null(theme_cfg$base_family)) theme_cfg$base_family else "sans"
theme_legend_pos   <- if (!is.null(theme_cfg$legend_position)) theme_cfg$legend_position else "right"
theme_title_hjust  <- if (!is.null(theme_cfg$title_hjust)) as.numeric(theme_cfg$title_hjust) else 0
theme_panel_border <- if (!is.null(theme_cfg$panel_border)) as.logical(theme_cfg$panel_border) else TRUE"""
new = """theme_base_size    <- if (!is.null(theme_cfg$base_size)) as.numeric(theme_cfg$base_size) else NA_real_
theme_base_family  <- if (!is.null(theme_cfg$base_family)) theme_cfg$base_family else "sans"
theme_legend_pos   <- if (!is.null(theme_cfg$legend_position)) theme_cfg$legend_position else "right"
theme_title_hjust  <- if (!is.null(theme_cfg$title_hjust)) as.numeric(theme_cfg$title_hjust) else 0
theme_panel_border <- if (!is.null(theme_cfg$panel_border)) as.logical(theme_cfg$panel_border) else FALSE
theme_grid         <- if (!is.null(theme_cfg$grid)) as.logical(theme_cfg$grid) else FALSE

# ============================================================
# 画布规格（借自 nature-figure 的排版逻辑）
#
# 核心不是"6.5pt"这个数字，而是：**图表按最终印刷尺寸作画**。
# 期刊栏宽固定，字号必须在 5–7pt 区间才能与栏宽成比例；
# 先画成大图再缩回栏宽，字号比例就全错了，所以尺寸一开始就要定。
#
#   单栏 single  =  89 mm
#   1.5 栏      = 120 mm
#   双栏 double = 183 mm
# ============================================================
FIG_WIDTH_MM <- c(single = 89, onehalf = 120, double = 183)

# 字号随画布推导：栏越窄，相同信息量需要相对更大的字
pub_base_size <- function(width_mm = 183) {
  if (!is.na(theme_base_size)) return(theme_base_size)   # 配置显式指定则优先
  if (width_mm <= 95) 7 else 6.5
}

# 线宽层级：数据 > 轴线 > 参考线。视觉重量应与信息重要度一致。
LW_DATA <- 0.6
LW_AXIS <- 0.35
LW_REF  <- 0.3

# ---- 配色：按**角色**定义，不是按"一组好看的颜色" ----
#
#   main     —— 主要对象（干预组 / 新方法）
#   contrast —— 对照对象（对照组 / 参照）
#   accent   —— 强调（阈值线、异常亚组）
#   neutral  —— 中性（参考线、非重点系列）
#   ink      —— 文字与轴线
# 换配色方案时换的是角色对应的色值，不是打乱角色分工。
PAL_ROLES <- list(
  main     = "#3182BD",
  contrast = "#D24B40",
  accent   = "#33B5A5",
  neutral  = "#767676",
  ink      = "#272727"
)

pal <- function(role = "main") {
  v <- PAL_ROLES[[role]]
  if (is.null(v)) stop(sprintf("未知配色角色: %s", role))
  v
}"""
assert old in t, "配置块未命中"
t = t.replace(old, new)

# ---- 2. DPI / 格式默认值 --------------------------------------------------
t = t.replace(
    'PUBLICATION_DPI <- if (!is.null(cfg$quality$figure_dpi)) as.numeric(cfg$quality$figure_dpi) else 300',
    'PUBLICATION_DPI <- if (!is.null(cfg$quality$figure_dpi)) as.numeric(cfg$quality$figure_dpi) else 600')
t = t.replace(
    'FIGURE_FORMAT   <- if (!is.null(cfg$quality$figure_format)) cfg$quality$figure_format else "png"',
    'FIGURE_FORMAT   <- if (!is.null(cfg$quality$figure_format)) cfg$quality$figure_format else "tiff"')

# ---- 3. theme_pub 重写 ----------------------------------------------------
start = t.index("theme_pub <- function(")
end = t.index("# ---- theme_pub_light()")
new_theme = '''# ---- theme_pub() ----
# 出版级主题。设计原则（借自 nature-figure 的审美，而非抄它的数值）：
#
#   1. 数据墨迹比最大化 —— classic 基底，默认无网格、无面板外框、无分面底色。
#      网格是帮读者对齐的，代价是把注意力从数据上分走；单栏图尤其不需要。
#   2. 线宽分层 —— 数据 > 轴线 > 参考线，视觉重量与信息重要度一致。
#   3. 字重分层 —— 标题/轴标题加粗，刻度与图例常规，读者先抓结构再看数字。
#   4. 字号由画布推导 —— 见 pub_base_size()，不写死。
#   5. 留白克制 —— plot.margin 小；图内不放大段说明，交给图注。
#
# grid / border 保留为可选开关：层级多的复杂图仍可临时开浅网格，但默认关。
theme_pub <- function(base_size = NULL, base_family = theme_base_family,
                      grid = theme_grid, border = theme_panel_border) {
  if (is.null(base_size) || is.na(base_size)) base_size <- pub_base_size()
  theme_classic(base_size = base_size, base_family = base_family) %+replace%
    theme(
      panel.background = element_rect(fill = "white", color = NA),
      plot.background  = element_rect(fill = "white", color = NA),

      plot.title    = element_text(hjust = theme_title_hjust, size = base_size + 0.5,
                                   face = "bold", margin = margin(b = 4)),
      plot.subtitle = element_text(size = base_size - 0.5, colour = "grey35",
                                   margin = margin(b = 6)),
      plot.margin   = margin(3, 3, 3, 3),

      axis.title   = element_text(size = base_size, face = "bold"),
      axis.title.x = element_text(margin = margin(t = 4)),
      axis.title.y = element_text(margin = margin(r = 4)),
      axis.text    = element_text(size = base_size - 0.5, color = "black"),

      axis.line         = element_line(color = "black", linewidth = LW_AXIS),
      axis.ticks        = element_line(color = "black", linewidth = LW_AXIS),
      axis.ticks.length = unit(1.2, "pt"),

      legend.position   = theme_legend_pos,
      legend.title      = element_text(size = base_size - 0.3),
      legend.text       = element_text(size = base_size - 0.7),
      legend.key.size   = unit(0.7, "lines"),
      legend.spacing    = unit(0.2, "cm"),
      legend.background = element_blank(),
      legend.key        = element_blank(),

      panel.grid.major = if (grid) element_line(color = "grey92", linewidth = 0.2) else element_blank(),
      panel.grid.minor = element_blank(),
      panel.border     = if (border) element_rect(color = "black", fill = NA, linewidth = LW_AXIS) else element_blank(),

      strip.background = element_blank(),
      strip.text       = element_text(face = "bold", size = base_size - 0.3)
    )
}

'''
t = t[:start] + new_theme + t[end:]

# ---- 4. 配色函数改为按角色 ------------------------------------------------
t = t.replace('''  if (n_groups == 1) {
    return("#0072B5")
  }''', '''  if (n_groups == 1) {
    return(pal("main"))
  }''')
t = t.replace('"nature"       = c("#0072B5", "#BC3C29")[1:min(n_groups, 2)],',
              '"nature"       = c(pal("main"), pal("contrast"))[1:min(n_groups, 2)],')
t = t.replace('      if (n_groups <= 2) c("#0072B5", "#BC3C29")[1:n_groups]',
              '      if (n_groups <= 2) c(pal("main"), pal("contrast"))[1:n_groups]')
t = t.replace('  low = "#0072B5", mid = "white", high = "#BC3C29",',
              '  low = pal("main"), mid = "white", high = pal("contrast"),')
t = re.sub(r'get_hero_color\s+<- function\(\) "#0072B5"[^\n]*',
           'get_hero_color     <- function() pal("main")      # 主要对象（干预组/新方法）', t)
t = re.sub(r'get_baseline_color\s+<- function\(\) "#BC3C29"[^\n]*',
           'get_baseline_color <- function() pal("contrast")  # 对照对象（对照组/参照）', t)
t = re.sub(r'get_accent_color\s+<- function\(\) "#E69F00"[^\n]*',
           'get_accent_color   <- function() pal("accent")    # 强调（阈值线/异常亚组）', t)

# ---- 5. save_figure 改为 mm 优先 + 三格式 ---------------------------------
s2 = t.index("save_figure <- function(")
e2 = t.index("# ---- 清理临时变量 ----")
new_save = '''# ---- save_figure() ----
# 按物理尺寸一次导出多格式。设计原则：
#
#   1. 入参用 **mm** —— 期刊栏宽是 mm，用英寸会引入换算误差。
#   2. 一次出齐 svg + pdf + tiff —— svg 供后期微调（文字仍是 <text>），
#      pdf 供排版（矢量、字体内嵌），tiff 供投稿系统（600 dpi）。
#   3. 设备要选对 —— svglite 保证文字可编辑，cairo_pdf 保证字体内嵌，
#      ragg 保证位图质量；ggsave 的默认设备在部分平台会丢字体。
#
# width_mm / height_mm：物理尺寸，默认双栏 183 × 120 mm
# width / height：兼容旧调用（英寸）；给了就覆盖 mm
save_figure <- function(plot_obj, filename,
                        width_mm = 183, height_mm = 120,
                        width = NULL, height = NULL,
                        formats = c("svg", "pdf", "tiff"),
                        dpi = PUBLICATION_DPI) {
  w <- if (!is.null(width))  width  else width_mm  / 25.4
  h <- if (!is.null(height)) height else height_mm / 25.4

  for (fmt in formats) {
    out_path <- paste0(filename, ".", fmt)
    dev <- switch(fmt,
      svg  = svglite::svglite,
      pdf  = grDevices::cairo_pdf,
      tiff = ragg::agg_tiff,
      png  = ragg::agg_png,
      NULL
    )
    if (is.null(dev)) {
      warning(sprintf("不支持的导出格式: %s", fmt))
      next
    }
    ggsave(out_path, plot_obj, width = w, height = h, dpi = dpi,
           device = dev, bg = "white")
    message(sprintf("Saved: %s (%.0f x %.0f mm, %d dpi)", out_path,
                    w * 25.4, h * 25.4, as.integer(dpi)))
  }
  invisible(list(width_mm = w * 25.4, height_mm = h * 25.4))
}

'''
t = t[:s2] + new_save + t[e2:]

io.open(P, "w", encoding="utf-8").write(t)
print("  已重写源文件 _figure_config.R")
for k in ["pub_base_size", "FIG_WIDTH_MM", "PAL_ROLES", "LW_AXIS", "theme_classic", "agg_tiff"]:
    print(f"  {k:<16} {'OK' if k in t else 'MISSING'}")
