"""把主结局写入 project_config.yml（保留 exploratory 模式并记录 post hoc 事实）。"""
import io
import re

BASE = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub"
p = BASE + r"\test\project_config.yml"
s = io.open(p, encoding="utf-8-sig").read()

s = s.replace(
    '  outcome: ""                          # 待定：候选为 baseline_score（症状负担）',
    '  outcome: "post_score"                # 2026-10-18 经 Batch 1 筛查后由用户确定（post hoc）',
)
s = s.replace(
    '  outcome_type: ""                     # 待定',
    '  outcome_type: "continuous"           # 连续（0–100）',
)
# 记录 post hoc 事实
s = s.replace(
    'analysis_mode: "exploratory"',
    'analysis_mode: "exploratory"          # 主结局在看过数据后确定 → 全文按探索性/pothoc 声明',
)

io.open(p, "w", encoding="utf-8").write(s)

# 回读校验
import yaml
d = yaml.safe_load(io.open(p, encoding="utf-8-sig"))
print("  outcome     :", d["variables"]["outcome"])
print("  outcome_type:", d["variables"]["outcome_type"])
print("  analysis_mode:", d["analysis_mode"])
