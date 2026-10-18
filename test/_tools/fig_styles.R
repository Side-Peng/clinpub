# ============================================================
# 图表风格探索：同一份数据（post_score by group）的 6 种画法
# 输出：test/figstyle/v0..v6_*.png + styles_contact.png
# 目的：给用户挑选，不进入正式产出
# ============================================================

suppressPackageStartupMessages({
  library(ggplot2)
  library(patchwork)
  library(ggbeeswarm)
  library(ggtext)
  library(scales)
})

root <- normalizePath(".")
d <- read.csv(file.path(root, "02_PreprocessedData/data/cleaned.csv"),
              fileEncoding = "UTF-8", check.names = FALSE)
d$group <- factor(d$group, levels = c("Control", "Treatment"))
out <- file.path(root, "figstyle")
dir.create(out, recursive = TRUE, showWarnings = FALSE)

# ---- 统计量 --------------------------------------------------------------
agg <- aggregate(post_score ~ group, d, function(x) c(m = mean(x), s = sd(x), n = length(x)))
agg <- data.frame(group = agg$group, m = agg$post_score[, "m"],
                  s = agg$post_score[, "s"], n = agg$post_score[, "n"])
agg$se <- agg$s / sqrt(agg$n)
agg$lo <- agg$m - qt(0.975, agg$n - 1) * agg$se
agg$hi <- agg$m + qt(0.975, agg$n - 1) * agg$se
diff_m <- agg$m[agg$group == "Treatment"] - agg$m[agg$group == "Control"]

OKABE <- c(Control = "#0072B2", Treatment = "#D55E00")
GREY  <- c(Control = "#8C8C8C", Treatment = "#2B2B2B")

# ---- 通用主题 ------------------------------------------------------------
minimal_theme <- function(base = 11) {
  theme_minimal(base_size = base, base_family = "sans") +
    theme(
      panel.grid = element_blank(),
      panel.border = element_blank(),
      axis.line.x  = element_blank(),
      axis.line.y  = element_line(colour = "grey20", linewidth = 0.4),
      axis.ticks.y = element_line(colour = "grey20", linewidth = 0.4),
      axis.ticks.x = element_blank(),
      axis.text  = element_text(colour = "grey20"),
      plot.title = element_text(face = "bold", hjust = 0, size = base + 2,
                                margin = margin(b = 4)),
      plot.subtitle = element_text(colour = "grey45", size = base - 2,
                                   margin = margin(b = 10)),
      plot.caption = element_text(colour = "grey55", size = base - 3, hjust = 0),
      plot.title.position = "plot",
      plot.caption.position = "plot",
      legend.position = "none",
      plot.margin = margin(12, 16, 10, 10)
    )
}

save_png <- function(p, name, w = 7, h = 5) {
  ggsave(file.path(out, paste0(name, ".png")), p, width = w, height = h,
         dpi = 300, device = ragg::agg_png, bg = "white")
}

# ============================================================
# V0 — 现状（对照）
# ============================================================
apply_theme_v0 <- function() {
  theme_bw(base_size = 11) +
    theme(panel.grid.minor = element_blank(), legend.position = "none")
}

v0 <- ggplot(d, aes(group, post_score, fill = group)) +
  geom_boxplot(width = 0.55, outlier.shape = NA, alpha = 0.85) +
  geom_jitter(width = 0.12, size = 0.9, alpha = 0.35, colour = "grey25") +
  scale_fill_manual(values = c("#3B8FC4", "#C0504D")) +
  labs(title = "V0 现状：默认箱线 + 抖动点", y = "post_score", x = NULL) +
  apply_theme_v0()
save_png(v0, "v0_current")

# ============================================================
# V1 — 期刊极简（Nature 风）
# ============================================================
v1 <- ggplot(d, aes(group, post_score)) +
  geom_boxplot(width = 0.42, outlier.shape = NA,
               fill = "grey94", colour = "grey25", linewidth = 0.45) +
  geom_point(position = position_jitter(width = 0.16, height = 0, seed = 1),
             size = 1.1, alpha = 0.45, colour = "grey35") +
  geom_pointrange(data = agg,
                  aes(y = m, ymin = lo, ymax = hi),
                  colour = "black", linewidth = 0.5, size = 0.45) +
  labs(title = "V1 期刊极简",
       subtitle = "去网格、去边框、去图例；均值与 95%CI 叠在分布上",
       y = "Post-treatment symptom score", x = NULL,
       caption = "点为个体观测；箱为中位数与四分位；黑点为均值 ± 95% CI") +
  minimal_theme()
save_png(v1, "v1_minimal")

# ============================================================
# V2 — 色盲友好（Okabe-Ito + beeswarm）
# ============================================================
v2 <- ggplot(d, aes(group, post_score, colour = group, fill = group)) +
  geom_boxplot(width = 0.40, alpha = 0.18, outlier.shape = NA,
               linewidth = 0.55) +
  geom_beeswarm(size = 1.1, alpha = 0.55, cex = 1.4, priority = "density") +
  stat_summary(fun = median, geom = "crossbar", width = 0.30,
               linewidth = 0.7, show.legend = FALSE) +
  scale_colour_manual(values = OKABE) +
  scale_fill_manual(values = OKABE) +
  annotate("text", x = 2.42, y = agg$m[2], label = "Treatment",
           hjust = 0, colour = OKABE[["Treatment"]], fontface = "bold", size = 3.6) +
  annotate("text", x = 1.42, y = agg$m[1], label = "Control",
           hjust = 0, colour = OKABE[["Control"]], fontface = "bold", size = 3.6) +
  coord_cartesian(xlim = c(0.5, 2.95)) +
  labs(title = "V2 色盲友好",
       subtitle = "Okabe-Ito 双色 + swarm 排布，组名直接标在图上",
       y = "Post-treatment symptom score", x = NULL) +
  minimal_theme() +
  theme(axis.text.x = element_blank())
save_png(v2, "v2_colorblind")

# ============================================================
# V3 — 小提琴 + 内嵌窄箱
# ============================================================
v3 <- ggplot(d, aes(group, post_score, fill = group)) +
  geom_violin(width = 0.85, alpha = 0.32, colour = NA, trim = TRUE) +
  geom_boxplot(width = 0.13, outlier.shape = NA, fill = "white",
               colour = "grey15", linewidth = 0.45) +
  stat_summary(fun = median, geom = "point", size = 1.6, colour = "grey15") +
  scale_fill_manual(values = OKABE) +
  labs(title = "V3 小提琴 + 内嵌箱",
       subtitle = "看整体形状；内嵌窄箱保留中位数与四分位",
       y = "Post-treatment symptom score", x = NULL) +
  minimal_theme() +
  coord_cartesian(ylim = c(0, 100))
save_png(v3, "v3_violin")

# ============================================================
# V4 — 雨云（半小提琴 + 箱 + 散点）
# ============================================================
v4 <- ggplot(d, aes(group, post_score, fill = group, colour = group)) +
  geom_violin(aes(x = as.numeric(group) - 0.14, group = group),
              width = 0.52, alpha = 0.30, colour = NA, trim = TRUE) +
  geom_boxplot(aes(x = as.numeric(group) + 0.02), width = 0.09,
               outlier.shape = NA, fill = "white", linewidth = 0.45) +
  geom_jitter(aes(x = as.numeric(group) + 0.20),
              width = 0.045, height = 0, size = 1.0, alpha = 0.5, seed = 2) +
  scale_fill_manual(values = OKABE) +
  scale_colour_manual(values = OKABE) +
  scale_x_continuous(breaks = 1:2, labels = levels(d$group), limits = c(0.5, 2.55)) +
  labs(title = "V4 雨云图",
       subtitle = "左半小提琴（形状）+ 中箱（分位）+ 右侧散点（个体）",
       y = "Post-treatment symptom score", x = NULL) +
  minimal_theme() +
  coord_cartesian(ylim = c(0, 100))
save_png(v4, "v4_raincloud")

# ============================================================
# V5 — 估计图（以效应为中心）
# ============================================================
v5 <- ggplot() +
  geom_jitter(data = d, aes(group, post_score), width = 0.13,
              size = 0.9, alpha = 0.22, colour = "grey55") +
  geom_errorbar(data = agg, aes(x = group, ymin = lo, ymax = hi),
                width = 0.10, linewidth = 0.9, colour = "grey10") +
  geom_point(data = agg, aes(group, m), size = 4.2, colour = "grey10") +
  geom_text(data = agg, aes(group, m, label = sprintf("%.1f", m)),
            vjust = -1.6, size = 3.4, fontface = "bold", colour = "grey10") +
  annotate("label", x = 1.5, y = 92, hjust = 0.5,
           label = sprintf("Delta = %.1f  (95%% CI %.1f, %.1f)", diff_m, -15.5, -2.6),
           size = 3.3, colour = "grey15", fill = "white", label.size = 0.2) +
  labs(title = "V5 估计导向",
       subtitle = "个体点淡化，视觉焦点放在均值差与区间上",
       y = "Post-treatment symptom score", x = NULL,
       caption = "圆点为组均值，误差条为 95% CI") +
  minimal_theme() +
  coord_cartesian(ylim = c(0, 100))
save_png(v5, "v5_estimate")

# ============================================================
# V6 — 经验累积分布（ECDF）
# ============================================================
v6 <- ggplot(d, aes(post_score, colour = group)) +
  stat_ecdf(linewidth = 1.0) +
  geom_vline(xintercept = agg$m[1], linetype = "22", colour = OKABE[["Control"]],
             linewidth = 0.4, alpha = 0.7) +
  geom_vline(xintercept = agg$m[2], linetype = "22", colour = OKABE[["Treatment"]],
             linewidth = 0.4, alpha = 0.7) +
  scale_colour_manual(values = OKABE) +
  scale_y_continuous(labels = percent_format(accuracy = 1)) +
  labs(title = "V6 累积分布",
       subtitle = "曲线整体左移 = 治疗组更多落在低分区",
       x = "Post-treatment symptom score", y = "Cumulative proportion",
       caption = "虚线为各组的均值位置") +
  minimal_theme(base = 11) +
  theme(legend.position = c(0.02, 0.98),
        legend.justification = c(0, 1),
        legend.title = element_blank(),
        legend.background = element_blank(),
        legend.key = element_blank())
save_png(v6, "v6_ecdf")

# ============================================================
# 汇总联系表
# ============================================================
contact <- (v0 | v1) / (v2 | v3) / (v4 | v5) / (v6 | plot_spacer()) +
  plot_annotation(
    title = "ClinPub 图表风格候选（同一数据：治疗后症状评分 by 组）",
    subtitle = "请指出偏好与要挑刺的地方",
    theme = theme(
      plot.title = element_text(face = "bold", size = 15),
      plot.subtitle = element_text(colour = "grey45", size = 10)
    )
  )
ggsave(file.path(out, "styles_contact.png"), contact,
       width = 15, height = 20, dpi = 150, device = ragg::agg_png, bg = "white")

cat("已生成：\n")
for (f in list.files(out, pattern = "\\.png$")) cat("  ", f, "\n")
