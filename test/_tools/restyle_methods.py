"""把三个方法脚本的绘图段换成新风格（不改任何统计计算）。"""
import io
import re

BASE = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\test\03_AnalysisMethods"

# ---------------------------------------------------------------- 02 筛查图
P2 = BASE + r"\02_OutcomeScreening\run.R"
t = io.open(P2, encoding="utf-8").read()

old_p1 = """p1 <- ggplot(long, aes(x = group, y = value, fill = group)) +
  geom_boxplot(width = 0.55, outlier.shape = NA, alpha = 0.85) +
  geom_jitter(width = 0.12, size = 0.9, alpha = 0.35, colour = "grey25") +
  facet_wrap(~ variable, scales = "free_y", nrow = 1) +
  scale_fill_manual(values = get_palette(2)) +
  labs(x = NULL, y = "Value", title = "A  Candidate outcomes by group") +
  apply_theme() +
  theme(legend.position = "none")"""

new_p1 = """COL2 <- get_palette(2)
names(COL2) <- levels(long$group)

p1 <- ggplot(long, aes(x = group, y = value)) +
  geom_jitter(aes(colour = group), width = 0.14, height = 0,
              size = 1.05, alpha = 0.55) +
  geom_boxplot(aes(colour = group), width = 0.30, fill = NA,
               outlier.shape = NA, linewidth = LW_DATA * 0.65,
               fatten = 2.2) +
  facet_wrap(~ variable, scales = "free_y", nrow = 1) +
  scale_colour_manual(values = COL2) +
  labs(x = NULL, y = "Value") +
  theme_pub(width_mm = FIG_WIDTH_MM[["double"]]) +
  theme(legend.position = "none")"""

assert old_p1 in t, "02 p1 未命中"
t = t.replace(old_p1, new_p1)

old_p2 = """  geom_text(aes(label = sprintf("%.2f", r)), size = 3, colour = "grey10") +"""
new_p2 = """  geom_text(aes(label = sprintf("%.2f", r)), size = 2.2, colour = "black",
            fontface = "bold") +"""
assert old_p2 in t, "02 p2 未命中"
t = t.replace(old_p2, new_p2)

old_lab = """  labs(x = NULL, y = NULL, title = "B  Correlation (Pearson)",
       fill = "r") +
  apply_theme() +"""
new_lab = """  labs(x = NULL, y = NULL, fill = "r") +
  theme_pub(width_mm = FIG_WIDTH_MM[["double"]]) +"""
assert old_lab in t, "02 p2 labs 未命中"
t = t.replace(old_lab, new_lab)

old_save = """save_figure(fig, save_path, width = 10, height = 8)"""
new_save = """save_figure(fig, save_path,
            width_mm = FIG_WIDTH_MM[["double"]], height_mm = 150)"""
assert old_save in t, "02 save 未命中"
t = t.replace(old_save, new_save)
io.open(P2, "w", encoding="utf-8").write(t)
print("  02_OutcomeScreening 已改")

# ---------------------------------------------------------------- 03 调整模型
P3 = BASE + r"\03_AdjustedModel\run.R"
t = io.open(P3, encoding="utf-8").read()

old = """  geom_vline(xintercept = 0, linetype = "dashed", colour = "grey50") +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high),
                orientation = "y", width = 0.18, colour = get_hero_color(), linewidth = 0.8) +
  geom_point(size = 3.2, colour = get_hero_color()) +"""
new = """  geom_vline(xintercept = 0, linetype = "22", colour = pal("neutral"),
             linewidth = LW_REF) +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high),
                orientation = "y", width = 0.14, colour = "black",
                linewidth = LW_DATA * 0.65) +
  geom_point(size = 1.8, colour = pal("main")) +"""
assert old in t, "03 图层未命中"
t = t.replace(old, new)

old = """  labs(x = "Adjusted mean difference in post_score (95% CI)", y = NULL,
       title = "Adjusted associations with post-intervention symptom score",
       subtitle = sprintf("Linear model adjusted for age, sex and BMI (n = %d)", nrow(d))) +
  apply_theme()"""
new = """  labs(x = "Adjusted mean difference in symptom score (95% CI)", y = NULL) +
  theme_pub(width_mm = FIG_WIDTH_MM[["single"]])"""
assert old in t, "03 labs 未命中"
t = t.replace(old, new)

t = t.replace(
    'save_figure(p, file.path(out_dir, "fig2_adjusted_effects"), width = 8, height = 4.6)',
    'save_figure(p, file.path(out_dir, "fig2_adjusted_effects"),\n            width_mm = FIG_WIDTH_MM[["single"]], height_mm = 70)')
io.open(P3, "w", encoding="utf-8").write(t)
print("  03_AdjustedModel 已改")

# ---------------------------------------------------------------- 04 敏感性
P4 = BASE + r"\04_SensitivityAnalysis\run.R"
t = io.open(P4, encoding="utf-8").read()

old = """  geom_vline(xintercept = 0, linetype = "dashed", colour = "grey50") +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high),
                orientation = "y", width = 0.18,
                colour = get_hero_color(), linewidth = 0.8) +
  geom_point(size = 3.2, colour = get_hero_color()) +
  geom_text(aes(label = sprintf("%.2f", estimate)),
            vjust = -1.1, size = 3.2, colour = "grey20") +"""
new = """  geom_vline(xintercept = 0, linetype = "22", colour = pal("neutral"),
             linewidth = LW_REF) +
  geom_errorbar(aes(xmin = ci_low, xmax = ci_high),
                orientation = "y", width = 0.14,
                colour = "black", linewidth = LW_DATA * 0.65) +
  geom_point(size = 1.8, colour = pal("main")) +
  geom_text(aes(label = sprintf("%.2f", estimate)),
            vjust = -1.0, size = 2.2, fontface = "bold", colour = "black") +"""
assert old in t, "04 图层未命中"
t = t.replace(old, new)

old = """  labs(x = "Difference in post_score (95% CI)", y = NULL,
       title = "Sensitivity of the group effect across analytic approaches",
       subtitle = sprintf("Primary analysis: adjusted complete-case model (n = %d)",
                          nrow(clean))) +
  apply_theme()"""
new = """  labs(x = "Difference in symptom score (95% CI)", y = NULL) +
  theme_pub(width_mm = FIG_WIDTH_MM[["single"]])"""
assert old in t, "04 labs 未命中"
t = t.replace(old, new)

t = t.replace(
    'save_figure(p, file.path(out_dir, "fig3_sensitivity_forest"), width = 9, height = 4.4)',
    'save_figure(p, file.path(out_dir, "fig3_sensitivity_forest"),\n            width_mm = FIG_WIDTH_MM[["single"]], height_mm = 62)')
io.open(P4, "w", encoding="utf-8").write(t)
print("  04_SensitivityAnalysis 已改")
