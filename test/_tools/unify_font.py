"""统一字号（轴标签 = 轴标题）并把默认字族固定为 Arial。"""
import io

P = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\claude-code\pipeline\templates\_figure_config.R"
t = io.open(P, encoding="utf-8").read()

# 1) 字族默认值改为「未指定」，等风格包确定后再回填
t = t.replace(
    'theme_base_family  <- if (!is.null(theme_cfg$base_family)) theme_cfg$base_family else "sans"',
    'theme_base_family  <- if (!is.null(theme_cfg$base_family)) theme_cfg$base_family else NA_character_'
)

# 2) 风格包确定后回填字族：默认取包里的 font（Arial）
t = t.replace(
    '# ---- 由风格包派生的常量 --------------------------------------------------',
    '''# ---- 字族：未显式配置时取风格包的 font（默认 Arial）-----------------------
# 期刊要求 Arial / Helvetica。用 "sans" 会让不同平台落到 DejaVu / Helvetica，
# 排版后字宽不一致，所以这里钉死具体字体名。
if (is.na(theme_base_family)) theme_base_family <- STYLE$font

# ---- 由风格包派生的常量 --------------------------------------------------'''
)

# 3) 轴标签与轴标题统一字号
t = t.replace(
    '      axis.text    = element_text(size = base_size - 0.5, color = "black"),',
    '''      # 轴标签与轴标题同磅值：竖排标题和横排标签视觉重量一致，图面才不"一头轻一头重"
      axis.text    = element_text(size = base_size, color = "black"),'''
)

# 4) 图例文字沿用同一字号阶梯（标题略大、正文同字号）
t = t.replace(
    '      legend.title      = element_text(size = base_size - 0.3),',
    '      legend.title      = element_text(size = base_size),')
t = t.replace(
    '      legend.text       = element_text(size = base_size - 0.7),',
    '      legend.text       = element_text(size = base_size),')

io.open(P, "w", encoding="utf-8").write(t)

for k in ['else NA_character_', 'theme_base_family <- STYLE$font', 'axis.text    = element_text(size = base_size,']:
    print(f"  {k[:46]:<48} {'OK' if k in t else 'MISSING'}")
