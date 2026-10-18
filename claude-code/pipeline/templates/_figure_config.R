# ============================================================
# clinpub 共享图表配置脚本 (_figure_config.R)
# 所有分析方法的 R 脚本必须 source() 此文件
# 由 Phase 2 的 generate_figure_config 步骤自动生成
#
# 使用方式（在每个方法 R 脚本开头）：
#   library(ggplot2)
#   library(dplyr)
#   source("04_Outputs/_figure_config.R")
#
# 提供以下函数/常量：
#   - theme_pub() / theme_pub_light() / apply_theme()
#   - get_palette() / get_continuous_scale() / get_diverging_scale()
#   - get_hero_color() / get_baseline_color() / get_accent_color()
#   - format_pval() / wilson_ci()
#   - save_figure() — 统一导出函数
#   - PUBLICATION_DPI / FIGURE_FORMAT 常量
# ============================================================

# ---- 依赖加载 ----
suppressPackageStartupMessages({
  library(ggplot2)
  library(yaml)
})

# ---- 读取 project_config.yml ----
# 支持从脚本所在目录或工作目录查找
config_paths <- c("project_config.yml", "../project_config.yml", "../../project_config.yml")
config_found <- FALSE
for (cfg_path in config_paths) {
  if (file.exists(cfg_path)) {
    cfg <- yaml::read_yaml(cfg_path)
    config_found <- TRUE
    break
  }
}
if (!config_found) {
  warning("project_config.yml not found. Using default figure configuration.")
  cfg <- list()
}

# ---- Theme 配置 (r_patterns.md §1.2) ----
theme_cfg <- cfg$quality$theme
theme_variant      <- if (!is.null(theme_cfg$variant)) theme_cfg$variant else "theme_pub"
theme_base_size    <- if (!is.null(theme_cfg$base_size)) as.numeric(theme_cfg$base_size) else NA_real_
theme_base_family  <- if (!is.null(theme_cfg$base_family)) theme_cfg$base_family else NA_character_
theme_legend_pos   <- if (!is.null(theme_cfg$legend_position)) theme_cfg$legend_position else "right"
theme_title_hjust  <- if (!is.null(theme_cfg$title_hjust)) as.numeric(theme_cfg$title_hjust) else 0
theme_panel_border <- if (!is.null(theme_cfg$panel_border)) as.logical(theme_cfg$panel_border) else FALSE
theme_grid         <- if (!is.null(theme_cfg$grid)) as.logical(theme_cfg$grid) else FALSE

# ============================================================
# 风格包（style pack）
#
# 为什么是"包"而不是一堆散参数：期刊的排版是一整套约定——
# 栏宽、字号、线宽、配色、导出格式互相牵连，单独调一个会破坏比例。
# 所以按期刊整包切换，需要微调时再写 style_overrides。
#
# 数据来源：
#   nature —— Nature 官方 figure guide（89/183mm、5–7pt、矢量主图、Okabe-Ito 色）
#   lancet / jama / nejm —— ggsci 的官方配色 + 各自常见栏宽
#   注：除 nature 外，栏宽为常见值，投稿前请对照目标期刊 Guide for Authors。
# ============================================================
BUILTIN_STYLES <- list(
  nature = list(
    label           = "Nature（官方规格）",
    widths_mm       = c(single = 89, double = 183),
    base_size       = c(single = 7, double = 6.5),
    font            = "Arial",
    grid            = FALSE,
    panel_border    = FALSE,
    line            = c(axis = 0.35, data = 0.60, ref = 0.30),
    tick_length_pt  = 1.8,
    main_formats    = c("pdf", "svg"),
    extended_formats = c("tiff"),
    palette         = c(main = "#0072B2", contrast = "#D55E00",
                        accent = "#009E73", neutral = "#999999",
                        ink = "#000000")
  ),
  lancet = list(
    label           = "The Lancet 风格",
    widths_mm       = c(single = 90, double = 190),
    base_size       = c(single = 7, double = 6.5),
    font            = "Arial",
    grid            = FALSE,
    panel_border    = FALSE,
    line            = c(axis = 0.50, data = 0.75, ref = 0.35),
    tick_length_pt  = 2.2,
    main_formats    = c("pdf", "svg"),
    extended_formats = c("tiff"),
    palette         = c(main = "#00468B", contrast = "#ED0000",
                        accent = "#42B540", neutral = "#ADB6B6",
                        ink = "#1B1919")
  ),
  jama = list(
    label           = "JAMA 风格",
    widths_mm       = c(single = 86, double = 178),
    base_size       = c(single = 7, double = 6.5),
    font            = "Arial",
    grid            = FALSE,
    panel_border    = FALSE,
    line            = c(axis = 0.45, data = 0.70, ref = 0.35),
    tick_length_pt  = 2.0,
    main_formats    = c("pdf", "svg"),
    extended_formats = c("tiff"),
    palette         = c(main = "#374E55", contrast = "#B24745",
                        accent = "#00A1D5", neutral = "#80796B",
                        ink = "#000000")
  ),
  nejm = list(
    label           = "NEJM 风格",
    widths_mm       = c(single = 86, double = 173),
    base_size       = c(single = 7, double = 6.5),
    font            = "Arial",
    grid            = FALSE,
    panel_border    = FALSE,
    line            = c(axis = 0.45, data = 0.70, ref = 0.35),
    tick_length_pt  = 2.0,
    main_formats    = c("pdf", "svg"),
    extended_formats = c("tiff"),
    palette         = c(main = "#0072B5", contrast = "#BC3C29",
                        accent = "#E18727", neutral = "#7876B1",
                        ink = "#000000")
  )
)

# ---- 选中风格包 ----------------------------------------------------------
style_name <- if (!is.null(cfg$quality$style)) cfg$quality$style else "nature"
STYLE <- BUILTIN_STYLES[[style_name]]
if (is.null(STYLE)) {
  warning(sprintf("未知风格包 '%s'，回退到 nature。可选：%s",
                  style_name, paste(names(BUILTIN_STYLES), collapse = ", ")))
  style_name <- "nature"
  STYLE <- BUILTIN_STYLES[["nature"]]
}

# ---- 局部覆盖（只写要改的项）--------------------------------------------
style_ov <- cfg$quality$style_overrides
if (!is.null(style_ov)) {
  for (k in names(style_ov)) {
    v <- style_ov[[k]]
    if (k %in% c("line", "palette", "base_size", "widths_mm")) {
      # 这些是命名向量：按名字逐个覆盖，不是整块替换
      cur <- STYLE[[k]]
      for (nm in names(v)) cur[[nm]] <- v[[nm]]
      STYLE[[k]] <- cur
    } else {
      STYLE[[k]] <- v
    }
  }
}

# ---- 字族：未显式配置时取风格包的 font（默认 Arial）-----------------------
# 期刊要求 Arial / Helvetica。用 "sans" 会让不同平台落到 DejaVu / Helvetica，
# 排版后字宽不一致，所以这里钉死具体字体名。
if (is.na(theme_base_family)) theme_base_family <- STYLE$font

# ---- 由风格包派生的常量 --------------------------------------------------
# 画布：风格包各自的栏宽（Nature 89/183、Science 55/174……不能写死一套）
FIG_WIDTH_MM <- STYLE$widths_mm

# 字号：由画布推导，落在期刊要求的 5–7pt 区间
pub_base_size <- function(width_mm = NULL) {
  if (!is.null(theme_base_size) && !is.na(theme_base_size)) return(theme_base_size)
  if (is.null(width_mm)) width_mm <- FIG_WIDTH_MM[["double"]]
  if (width_mm <= (FIG_WIDTH_MM[["single"]] + 10)) {
    as.numeric(STYLE$base_size[["single"]])
  } else {
    as.numeric(STYLE$base_size[["double"]])
  }
}

# 线宽层级：数据 > 轴线 > 参考线
LW_DATA <- STYLE$line[["data"]]
LW_AXIS <- STYLE$line[["axis"]]
LW_REF  <- STYLE$line[["ref"]]
TICK_LENGTH_PT <- STYLE$tick_length_pt

# 配色按角色，不按色值
PAL_ROLES <- as.list(STYLE$palette)

pal <- function(role = "main") {
  v <- PAL_ROLES[[role]]
  if (is.null(v)) stop(sprintf("未知配色角色: %s", role))
  v
}

color_cfg <- cfg$quality$color_palette
color_preset     <- if (!is.null(color_cfg$preset)) color_cfg$preset else "auto"
color_custom     <- if (!is.null(color_cfg$custom_colors)) unlist(color_cfg$custom_colors) else c()
color_group_map  <- if (!is.null(color_cfg$group_mapping)) as.character(as.list(color_cfg$group_mapping)) else NULL
color_continuous <- if (!is.null(color_cfg$continuous)) color_cfg$continuous else "viridis"

# ---- 全局常量 (r_patterns.md §1.3) ----
PUBLICATION_DPI <- if (!is.null(cfg$quality$figure_dpi)) as.numeric(cfg$quality$figure_dpi) else 600
FIGURE_FORMAT   <- if (!is.null(cfg$quality$figure_format)) cfg$quality$figure_format else "tiff"

# ============================================================
# 函数定义
# ============================================================

# ---- theme_pub() (r_patterns.md §1.2) ----
# 出版级 ggplot2 主题，所有 clinpub 图表必须使用
# ---- theme_pub() ----
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
                      grid = theme_grid, border = theme_panel_border,
                      width_mm = NULL) {
  # width_mm 传了就按该画布推导字号。单栏图必须传 FIG_WIDTH_MM[["single"]]，
  # 否则 89mm 的画布会按双栏取 6.5pt（应为 7pt）。
  if (is.null(base_size) || is.na(base_size)) base_size <- pub_base_size(width_mm)
  theme_classic(base_size = base_size, base_family = base_family) %+replace%
    theme(
      panel.background = element_rect(fill = "white", color = NA),
      plot.background  = element_rect(fill = "white", color = NA),

      plot.title    = element_text(hjust = theme_title_hjust, size = base_size + 0.5,
                                   face = "bold", margin = margin(b = 4)),
      plot.subtitle = element_text(size = base_size - 0.5, face = "bold", colour = "grey35",
                                   margin = margin(b = 6)),
      plot.margin   = margin(3, 3, 3, 3),

      axis.title   = element_text(size = base_size, face = "bold"),
      axis.title.x = element_text(size = base_size, face = "bold", margin = margin(t = 4)),
      axis.title.y = element_text(size = base_size, face = "bold", angle = 90,
                                  margin = margin(r = 4)),
      # 全图文字统一：同字号 + 同字重（bold）。层级靠位置区分，不靠字重差。
      axis.text    = element_text(size = base_size, face = "bold", color = "black"),

      axis.line         = element_line(color = "black", linewidth = LW_AXIS),
      axis.ticks        = element_line(color = "black", linewidth = LW_AXIS),
      axis.ticks.length = unit(TICK_LENGTH_PT, "pt"),

      legend.position   = theme_legend_pos,
      legend.title      = element_text(size = base_size, face = "bold"),
      legend.text       = element_text(size = base_size, face = "bold"),
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

# ---- theme_pub_light() (r_patterns.md §1.2) ----
# 轻量变体：无边框，适用于流程图、示意图
theme_pub_light <- function(base_size = theme_base_size, base_family = theme_base_family) {
  theme_pub(base_size = base_size, base_family = base_family) +
    theme(
      panel.border      = element_blank(),
      axis.line         = element_line(color = "black", linewidth = 0.4),
      panel.grid.major  = element_blank()
    )
}

# ---- apply_theme() (r_patterns.md §1.2 Config Protocol) ----
# 配置驱动的主题包装器，推荐使用方式：ggplot(...) + ... + apply_theme()
apply_theme <- function() {
  base_theme <- if (theme_variant == "theme_pub_light") {
    theme_pub_light(base_size = theme_base_size, base_family = theme_base_family)
  } else {
    theme_pub(base_size = theme_base_size, base_family = theme_base_family)
  }
  base_theme + theme(
    legend.position = theme_legend_pos,
    plot.title      = element_text(hjust = theme_title_hjust),
    panel.border    = if (theme_panel_border) {
      element_rect(color = "black", fill = NA, linewidth = 0.4)
    } else {
      element_blank()
    }
  )
}

# ---- get_palette() (r_patterns.md §1.1 Color Config Protocol) ----
# 配置驱动的配色生成器
# n_groups: 当前图的分组数
get_palette <- function(n_groups) {
  # 0. 单色场景直接返回 Hero 色
  if (n_groups == 1) {
    return(pal("main"))
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
    "nature"       = c(pal("main"), pal("contrast"))[1:min(n_groups, 2)],
    "okabe-ito"    = c("#E69F00", "#56B4E9", "#009E73", "#F0E442",
                       "#0072B2", "#D55E00", "#CC79A7", "#000000")[1:n_groups],
    "brewer-set1"  = RColorBrewer::brewer.pal(max(3, n_groups), "Set1")[1:n_groups],
    "brewer-dark2" = RColorBrewer::brewer.pal(max(3, n_groups), "Dark2")[1:n_groups],
    "brewer-set2"  = RColorBrewer::brewer.pal(max(3, n_groups), "Set2")[1:n_groups],
    "viridis"      = viridis::viridis(n_groups),
    # auto: 按组数自动选择（默认行为）
    {
      if (n_groups <= 2) c(pal("main"), pal("contrast"))[1:n_groups]
      else if (n_groups <= 4) RColorBrewer::brewer.pal(max(3, n_groups), "Set1")[1:n_groups]
      else if (n_groups <= 8) RColorBrewer::brewer.pal(max(3, n_groups), "Set2")[1:n_groups]
      else viridis::viridis(n_groups)
    }
  )
}

# ---- get_continuous_scale() (r_patterns.md §1.1) ----
# 连续变量色标
get_continuous_scale <- function() {
  switch(color_continuous,
    "viridis" = scale_fill_viridis_c(option = "D"),
    "magma"   = scale_fill_viridis_c(option = "A"),
    "plasma"  = scale_fill_viridis_c(option = "C"),
    "inferno" = scale_fill_viridis_c(option = "B"),
    scale_fill_viridis_c(option = "D")
  )
}

# ---- get_diverging_scale() (r_patterns.md §1.1) ----
# 发散色标（相关性矩阵等有正负方向的连续变量）
# midpoint: 发散中心值，相关性矩阵默认为 0
get_diverging_scale <- function(midpoint = 0) {
  scale_fill_gradient2(
    low = pal("main"), mid = "white", high = pal("contrast"),
    midpoint = midpoint
  )
}

# ---- 语义色便捷函数 (r_patterns.md §1.1) ----
get_hero_color     <- function() pal("main")      # 主要对象（干预组/新方法）
get_baseline_color <- function() pal("contrast")  # 对照对象（对照组/参照）
get_accent_color   <- function() pal("accent")    # 强调（阈值线/异常亚组）

# ---- format_pval() (r_patterns.md §1.4) ----
# p 值格式化，用于显著性标注
format_pval <- function(p) {
  dplyr::case_when(
    p < 0.001 ~ "italic(p) < 0.001",
    p < 0.01  ~ sprintf("italic(p) == %.3f", p),
    TRUE      ~ sprintf("italic(p) == %.3f", p)
  )
}

# ---- wilson_ci() (r_patterns.md §1.5) ----
# 比例指标的 Wilson Score 置信区间
# 用于敏感度、特异度、患病率等比例指标的 CI 计算
wilson_ci <- function(p, n, z_alpha = 1.96) {
  denominator <- 1 + z_alpha^2 / n
  centre      <- (p + z_alpha^2 / (2 * n)) / denominator
  margin      <- z_alpha * sqrt(p * (1 - p) / n + z_alpha^2 / (4 * n^2)) / denominator
  c(lower = centre - margin, upper = centre + margin)
}

# ---- save_figure() (r_patterns.md §1.3) ----
# 统一图表导出函数，根据项目配置自动设置 DPI 和格式
# plot_obj: ggplot2 对象
# filename: 输出文件名（不含扩展名，函数自动添加扩展名）
# width: 宽度（英寸），默认双栏 7in
# height: 高度（英寸），默认 6in
# formats: 导出格式向量，默认 c("png", "svg", "tiff")
# ---- save_figure() ----
# 按物理尺寸一次导出多格式。设计原则：
#
#   1. 入参用 **mm** —— 期刊栏宽是 mm，用英寸会引入换算误差。
#   2. 主图默认 **pdf + svg**（矢量） —— Nature 明确不接受 tiff/png 作主图；
#      tiff 只在补材（Extended Data）需要时显式指定 formats = "tiff"。
#   3. 设备要选对 —— svglite 保证文字可编辑，cairo_pdf 保证字体内嵌，
#      ragg 保证位图质量；ggsave 的默认设备在部分平台会丢字体。
#
# width_mm / height_mm：物理尺寸，默认双栏 183 × 120 mm
# width / height：兼容旧调用（英寸）；给了就覆盖 mm
save_figure <- function(plot_obj, filename,
                        width_mm = 183, height_mm = 120,
                        width = NULL, height = NULL,
                        formats = STYLE$main_formats,
                        dpi = PUBLICATION_DPI) {
  w <- if (!is.null(width))  width  else width_mm  / 25.4
  h <- if (!is.null(height)) height else height_mm / 25.4

  # 预览开关：审阅时设 CLINPUB_FIG_PREVIEW=1，额外导出一张 png。
  # 默认不产出位图——主图应为矢量，png/tiff 只在需要肉眼检查时生成。
  if (identical(Sys.getenv("CLINPUB_FIG_PREVIEW"), "1") && !("png" %in% formats)) {
    formats <- c(formats, "png")
  }

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

# ---- 清理临时变量 ----
rm(list = c("config_paths", "config_found", "cfg_path"))
