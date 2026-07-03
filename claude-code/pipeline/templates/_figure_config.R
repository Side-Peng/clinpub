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
_config_paths <- c("project_config.yml", "../project_config.yml", "../../project_config.yml")
_config_found <- FALSE
for (_cfg_path in _config_paths) {
  if (file.exists(_cfg_path)) {
    cfg <- yaml::read_yaml(_cfg_path)
    _config_found <- TRUE
    break
  }
}
if (!_config_found) {
  warning("project_config.yml not found. Using default figure configuration.")
  cfg <- list()
}

# ---- Theme 配置 (r_patterns.md §1.2) ----
theme_cfg <- cfg$quality$theme
theme_variant      <- if (!is.null(theme_cfg$variant)) theme_cfg$variant else "theme_pub"
theme_base_size    <- if (!is.null(theme_cfg$base_size)) as.numeric(theme_cfg$base_size) else 11
theme_base_family  <- if (!is.null(theme_cfg$base_family)) theme_cfg$base_family else "sans"
theme_legend_pos   <- if (!is.null(theme_cfg$legend_position)) theme_cfg$legend_position else "right"
theme_title_hjust  <- if (!is.null(theme_cfg$title_hjust)) as.numeric(theme_cfg$title_hjust) else 0
theme_panel_border <- if (!is.null(theme_cfg$panel_border)) as.logical(theme_cfg$panel_border) else TRUE

# ---- Color Palette 配置 (r_patterns.md §1.1) ----
color_cfg <- cfg$quality$color_palette
color_preset     <- if (!is.null(color_cfg$preset)) color_cfg$preset else "auto"
color_custom     <- if (!is.null(color_cfg$custom_colors)) unlist(color_cfg$custom_colors) else c()
color_group_map  <- if (!is.null(color_cfg$group_mapping)) as.character(as.list(color_cfg$group_mapping)) else NULL
color_continuous <- if (!is.null(color_cfg$continuous)) color_cfg$continuous else "viridis"

# ---- 全局常量 (r_patterns.md §1.3) ----
PUBLICATION_DPI <- if (!is.null(cfg$quality$figure_dpi)) as.numeric(cfg$quality$figure_dpi) else 300
FIGURE_FORMAT   <- if (!is.null(cfg$quality$figure_format)) cfg$quality$figure_format else "png"

# ============================================================
# 函数定义
# ============================================================

# ---- theme_pub() (r_patterns.md §1.2) ----
# 出版级 ggplot2 主题，所有 clinpub 图表必须使用
theme_pub <- function(base_size = theme_base_size, base_family = theme_base_family) {
  theme_minimal(base_size = base_size, base_family = base_family) %+replace%
    theme(
      panel.background = element_rect(fill = "white", color = NA),
      plot.background  = element_rect(fill = "white", color = NA),
      legend.position   = theme_legend_pos,
      legend.title      = element_text(face = "bold", size = rel(0.9)),
      legend.text       = element_text(size = rel(0.9)),
      legend.key.size   = unit(0.8, "lines"),
      legend.spacing    = unit(0.3, "cm"),
      legend.background = element_rect(fill = "white", color = NA),
      plot.title        = element_text(hjust = theme_title_hjust, size = rel(1.1), face = "bold",
                                       margin = margin(b = 8)),
      axis.title        = element_text(size = rel(1), face = "bold"),
      axis.title.x      = element_text(margin = margin(t = 8)),
      axis.title.y      = element_text(margin = margin(r = 8)),
      axis.text         = element_text(size = rel(0.9), color = "black"),
      axis.line         = element_line(color = "black", linewidth = 0.4),
      axis.ticks        = element_line(color = "black", linewidth = 0.3),
      panel.grid.major  = element_line(color = "grey92", linewidth = 0.2),
      panel.grid.minor  = element_blank(),
      panel.border      = element_rect(color = "black", fill = NA, linewidth = 0.4),
      strip.background  = element_rect(fill = "grey95", color = "black", linewidth = 0.4),
      strip.text        = element_text(face = "bold", size = rel(0.9)),
      plot.margin       = margin(12, 12, 12, 12)
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
    return("#0072B5")
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
    low = "#0072B5", mid = "white", high = "#BC3C29",
    midpoint = midpoint
  )
}

# ---- 语义色便捷函数 (r_patterns.md §1.1) ----
get_hero_color     <- function() "#0072B5"   # 核心关注色（新方法/干预组）
get_baseline_color <- function() "#BC3C29"   # 对照/参考色（标准治疗/零线）
get_accent_color   <- function() "#E69F00"   # 强调色（阈值线/异常亚组）

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
save_figure <- function(plot_obj, filename, width = 7, height = 6,
                        formats = c("png", "svg", "tiff")) {
  for (fmt in formats) {
    out_path <- paste0(filename, ".", fmt)
    if (fmt == "svg") {
      ggsave(out_path, plot_obj, width = width, height = height)
    } else if (fmt == "tiff") {
      ggsave(out_path, plot_obj, width = width, height = height,
             dpi = PUBLICATION_DPI, compression = "lzw")
    } else if (fmt == "pdf") {
      ggsave(out_path, plot_obj, width = width, height = height)
    } else {
      # png and others
      ggsave(out_path, plot_obj, width = width, height = height,
             dpi = PUBLICATION_DPI)
    }
    message(sprintf("Saved: %s", out_path))
  }
}

# ---- 清理临时变量 ----
rm(list = c("_config_paths", "_config_found", "_cfg_path"))
