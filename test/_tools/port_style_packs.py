"""把风格包机制写进 _figure_config.R（改源文件）。"""
import io
import re

P = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\claude-code\pipeline\templates\_figure_config.R"
t = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------- 风格包
STYLE_BLOCK = r'''# ============================================================
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
'''

# 替换从「画布规格」到「pal 函数」的整块
start = t.index("# ============================================================\n# 画布规格")
end = t.index("color_cfg <- cfg$quality$color_palette")
t = t[:start] + STYLE_BLOCK + "\n" + t[end:]

# 主题里的硬编码线宽/刻度改为风格包派生
t = t.replace('axis.ticks.length = unit(1.8, "pt"),',
              'axis.ticks.length = unit(TICK_LENGTH_PT, "pt"),')

# save_figure 默认改矢量优先
t = t.replace('formats = c("svg", "pdf", "tiff")',
              'formats = STYLE$main_formats')

# 注释里说明格式选择
t = t.replace('#   2. 一次出齐 svg + pdf + tiff —— svg 供后期微调（文字仍是 <text>），\n#      pdf 供排版（矢量、字体内嵌），tiff 供投稿系统（600 dpi）。',
              '#   2. 主图默认 **pdf + svg**（矢量） —— Nature 明确不接受 tiff/png 作主图；\n#      tiff 只在补材（Extended Data）需要时显式指定 formats = "tiff"。')

io.open(P, "w", encoding="utf-8").write(t)

print("  已写入风格包机制")
for k in ["BUILTIN_STYLES", "style_ov", "STYLE <-", "pub_base_size", "STYLE$main_formats"]:
    print(f"  {k:<20} {'OK' if k in t else 'MISSING'}")
