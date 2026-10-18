"""把正式标题写入 project_config.yml 的 project.title。"""
import io
import re

BASE = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub"
p = BASE + r"\test\project_config.yml"
s = io.open(p, encoding="utf-8-sig").read()

title = "真实临床样本中治疗状态与症状负担的横断面关联：基于基线可比性的探索性分析"

s = re.sub(r'(?m)^(\s*)title:\s*""(.*)$',
           lambda m: f'{m.group(1)}title: "{title}"', s, count=1)

io.open(p, "w", encoding="utf-8").write(s)

import yaml
d = yaml.safe_load(io.open(p, encoding="utf-8-sig"))
print("  project.title:", d["project"]["title"])
