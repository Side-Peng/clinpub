"""生成干净的 release notes：短前言 + CHANGELOG 的 3.0.0-preview.1 段。"""
import io

ROOT = r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub"

t = io.open(ROOT + "/CHANGELOG.md", encoding="utf-8").read()
i = t.index("## [3.0.0-preview.1]")
j = t.index("## [Unreleased]")
body = t[i:j].rstrip()
# 去掉段标题行（release 标题已给）与紧随其后的重复警告块引号
lines = body.split("\n")
lines = [l for l in lines if not l.startswith("## [3.0.0-preview.1]")]
while lines and (not lines[0].strip() or lines[0].startswith("> **破坏性变更**")):
    lines.pop(0)
body = "\n".join(lines).lstrip("\n")

head = """## ClinPub 3.0.0-preview.1

> **预发布版，请勿用于正式项目。** 3.0 不兼容 2.x 的项目状态——
> `.clinpub/` 结构与流程语义均改变，已有项目需重新初始化，或用 `import-project` 采纳现有材料。

**平台**：主版本转向 DeepSeek Harness；Qoder 移除。
**命令**：14 → 10（`overview`/`do`/`next-step`/`milestone` 合并为 `/clinpub` 枢纽）。
**验证**：阶段0–3 端到端跑通（120 例合成数据），修复 11 项缺陷。

---

"""

io.open(ROOT + "/.release-notes.md", "w", encoding="utf-8").write(head + body + "\n")
print("  行数:", len((head + body).splitlines()))
print("  首行:", (head + body).splitlines()[0])
