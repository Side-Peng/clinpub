#!/usr/bin/env python3
"""Assemble ClinPub 3.0 manuscript from section files.

Why this exists
---------------
ClinPub 3.0 writes sections in *progressive* order (Results → Methods →
Discussion → Conclusion → Introduction → Abstract) but the manuscript must be
emitted in IMRAD order. This script is the only writer of ``manuscript.md``.

It refuses to assemble when the section set is incomplete, when any section is
still ``draft``, or when a section is ``final`` while one of its upstream
dependencies is ``stale`` — that last check is what keeps a changed Results
from silently coexisting with an outdated Discussion.

Usage
-----
    python scripts/assemble_manuscript.py                  # assemble
    python scripts/assemble_manuscript.py --check           # validate only
    python scripts/assemble_manuscript.py --root <projdir>  # explicit project root
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

# (section key, heading used in manuscript.md) in output order.
ORDER = [
    ("abstract", "Abstract"),
    ("introduction", "Introduction"),
    ("methods", "Methods"),
    ("results", "Results"),
    ("discussion", "Discussion"),
    ("conclusion", "Conclusion"),
]

# Default dependency graph, used when a section omits ``depends_on``.
DEFAULT_DEPS: dict[str, list[str]] = {
    "results": [],
    "methods": [],
    "discussion": ["results", "methods"],
    "conclusion": ["discussion"],
    "introduction": ["results", "methods", "discussion"],
    "abstract": ["introduction", "methods", "results", "discussion", "conclusion"],
}

VALID_STATUS = {"draft", "final", "stale"}

CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")
LATIN_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse the small YAML subset used by section files.

    Supports ``key: value``, block lists (``key:`` followed by ``- item``) and
    inline lists (``key: [a, b]``). Anything else is ignored rather than
    raising, so a malformed optional field cannot block the pipeline.

    A leading BOM is stripped first: Windows editors and PowerShell's
    ``-Encoding UTF8`` write one, and without this the opening ``---`` would
    never match while every section silently fell back to ``draft``.
    """
    text = text.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text

    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    head = text[3:end]
    body = text[end + 4 :].lstrip("\n")
    meta: dict = {}
    current_list: str | None = None

    for raw_line in head.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue

        stripped = line.strip()
        if stripped.startswith("- ") and current_list is not None:
            meta[current_list].append(stripped[2:].strip().strip("'\""))
            continue

        if ":" not in stripped:
            continue

        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        current_list = None

        if not value:
            meta[key] = []
            current_list = key
        elif value.startswith("[") and value.endswith("]"):
            items = [item.strip().strip("'\"") for item in value[1:-1].split(",")]
            meta[key] = [item for item in items if item]
        else:
            meta[key] = value.strip("'\"")

    return meta, body


def count_words(text: str) -> int:
    """Count CJK characters plus Latin words — an approximate 字数."""
    return len(CJK.findall(text)) + len(LATIN_WORD.findall(text))


def load_sections(sections_dir: Path) -> dict[str, dict]:
    sections: dict[str, dict] = {}
    if not sections_dir.is_dir():
        return sections

    for path in sorted(sections_dir.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        key = meta.get("section") or path.stem
        key = str(key).strip()

        deps = meta.get("depends_on")
        if not isinstance(deps, list) or not deps:
            deps = DEFAULT_DEPS.get(key, [])

        sections[key] = {
            "key": key,
            "path": path,
            "status": str(meta.get("status", "draft")).strip(),
            "inputs": meta.get("inputs") or [],
            "depends_on": deps,
            "body": body.strip(),
            "words": count_words(body),
        }

    return sections


def validate(sections: dict[str, dict]) -> list[str]:
    problems: list[str] = []

    missing = [key for key, _ in ORDER if key not in sections]
    if missing:
        problems.append("缺少章节：" + ", ".join(missing))

    for key, info in sections.items():
        if key not in dict(ORDER):
            problems.append(f"未知章节 `{key}`（不在 IMRAD 顺序表中）")
        if info["status"] not in VALID_STATUS:
            problems.append(f"`{key}` 的 status 非法：`{info['status']}`（应为 draft/final/stale）")

    # A final section must not sit on top of a stale upstream section.
    for key, info in sections.items():
        if info["status"] != "final":
            continue
        for dep in info["depends_on"]:
            upstream = sections.get(dep)
            if upstream and upstream["status"] != "final":
                problems.append(
                    f"`{key}` 标记为 final，但上游 `{dep}` 是 "
                    f"{upstream['status']}——必须先把 `{dep}` 改回 final"
                )

    # Refuse to emit while anything is unfinished.
    unfinished = [
        f"{key}({info['status']})"
        for key, info in sections.items()
        if info["status"] != "final"
    ]
    if unfinished:
        problems.append("未完成的章节：" + ", ".join(sorted(unfinished)))

    return problems


def read_project_title(project_root: Path) -> str:
    """读取 project_config.yml 的 project.title。

    标题由 Phase 3 的 write_abstract_title 写入——**先写完全文再定标题**，
    因此这里允许为空（此时 manuscript.md 不含标题，仅在 stderr 警告）。
    不依赖 PyYAML：只做本文件需要的极简解析。
    """
    cfg = project_root / "project_config.yml"
    if not cfg.exists():
        return ""
    try:
        # utf-8-sig：Windows 编辑器的 BOM 会让首行的 "project:" 匹配失败
        text = cfg.read_text(encoding="utf-8-sig")
    except OSError:
        return ""
    in_project = False
    for line in text.splitlines():
        stripped = line.rstrip()
        if stripped.startswith("project:"):
            in_project = True
            continue
        if in_project:
            if stripped and not stripped[0].isspace() and not stripped.startswith("#"):
                break  # 离开 project 块
            m = re.match(r'^\s+title:\s*(.*)$', stripped)
            if m:
                value = m.group(1).strip().strip('"').strip("'")
                return value
    return ""


# 占位符 → 最终写法。figure/table 用英文（图表语言为 en），其余按正文语言。
PLACEHOLDER_PATTERNS = [
    (re.compile(r"\{\{Table:(\d+)\}\}"), r"Table \1"),
    (re.compile(r"\{\{Figure:(\d+)\}\}"), r"Figure \1"),
    (re.compile(r"\{\{SupplementaryTable:(\d+)\}\}"), r"Supplementary Table S\1"),
    (re.compile(r"\{\{SupplementaryFigure:(\d+)\}\}"), r"Supplementary Figure S\1"),
    (re.compile(r"\{\{Method:([^}]+)\}\}"), r"the \1 analysis"),
    (re.compile(r"\{\{Section:([^}]+)\}\}"), r"\1"),
]

LEFTOVER = re.compile(r"\{\{[^}]+\}\}")


def resolve_placeholders(text: str) -> str:
    """把 {{Table:N}} 之类替换成最终写法。

    为什么要脚本做而不是让 agent 手改：manuscript.md 是生成物，
    手改会在下次拼装时被覆盖——两处规则互相冲突，统一由脚本承担。
    """
    for pattern, repl in PLACEHOLDER_PATTERNS:
        text = pattern.sub(repl, text)
    return text


CITE_RE = re.compile(r"\{\{cite:([^}]+)\}\}")


def load_library(project_root: Path) -> dict:
    """读 Reference/reference_library.json，返回 citation_key → 记录。"""
    p = project_root / "Reference" / "reference_library.json"
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}
    return {r.get("citation_key", ""): r for r in data.get("references", [])}


def format_authors(authors: list, limit: int = 6) -> str:
    if not authors:
        return "Anonymous"
    if len(authors) > limit:
        return ", ".join(authors[:limit]) + ", et al"
    return ", ".join(authors)


def format_reference(n: int, ref: dict) -> str:
    """Vancouver 风格：作者. 标题. 期刊. 年份. doi:…"""
    title = (ref.get("title") or "").strip().rstrip(".")
    authors = format_authors(ref.get("authors") or [])
    journal = (ref.get("journal") or "").strip()
    year = (ref.get("year") or "").strip()
    line = f"{n}. {authors}. {title}."
    if journal:
        line += f" {journal}."
    if year:
        line += f" {year}."
    doi = (ref.get("doi") or "").strip()
    if doi and doi != "pending_doi":
        line += f" doi:{doi}"
    return line


def number_citations(body: str, library: dict, order: list) -> str:
    """把 {{cite:Key,Key}} 换成 [n]，编号按首次出现顺序分配。

    `order` 跨章节共享，因此编号在整个手稿内连续——这正是 Vancouver
    的编号规则（按正文出现顺序，而不是文献库 id）。
    """

    def repl(match: re.Match) -> str:
        keys = [k.strip() for k in match.group(1).split(",") if k.strip()]
        nums = []
        for k in keys:
            if k not in library:
                nums.append(None)
                continue
            if k not in order:
                order.append(k)
            nums.append(order.index(k) + 1)
        missing = [k for k, n in zip(keys, nums) if n is None]
        if missing:
            print(
                f"[WARN] 引用键不在文献库中：{', '.join(missing)}",
                file=sys.stderr,
            )
        got = sorted({n for n in nums if n is not None})
        if not got:
            return ""
        if len(got) == 1:
            return f"[{got[0]}]"
        return "[" + ",".join(str(n) for n in got) + "]"

    return CITE_RE.sub(repl, body)


def render(sections: dict[str, dict], project_root: Path) -> str:
    total = sum(sections[key]["words"] for key, _ in ORDER if key in sections)
    today = _dt.date.today().isoformat()
    title = read_project_title(project_root)
    library = load_library(project_root)
    cited: list[str] = []

    parts = [
        "---",
        "generated_by: scripts/assemble_manuscript.py",
        f"generated_at: {today}",
        f"word_count: {total}",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        "---",
        "",
        "<!-- 本文件是生成物，请勿手改。",
        "     要修改内容，请编辑 05_Manuscript/sections/*.md 后重新运行：",
        "       python scripts/assemble_manuscript.py",
        "-->",
        "",
    ]

    if title:
        parts.append(f"# {title}")
        parts.append("")
    else:
        print(
            "[WARN] project_config.yml 的 project.title 为空——manuscript.md 不含标题。"
            "标题应在 Phase 3 的 write_abstract_title 步骤写入。",
            file=sys.stderr,
        )

    for key, heading in ORDER:
        info = sections.get(key)
        if not info:
            continue
        body = resolve_placeholders(info["body"])
        # 引用编号必须按"正文出现顺序"分配（Vancouver），且跨章节连续，
        # 因此在拼装阶段统一处理，不能由各节自行编号。
        body = number_citations(body, library, cited)
        # 章节文件可能自带一级标题（`# Results`），拼装时又会加 `## Results`，
        # 生成重复标题。这里统一剥掉章节自带的首个 H1。
        body = re.sub(r"\A\s*#\s+[^\n]*\n+", "", body, count=1)
        # 章节内部的小标题下移一级（## → ###，### → ####），
        # 否则小节标题与章节标题同级，目录层级会乱掉。
        for level in range(5, 1, -1):
            body = re.sub(
                rf"^{'#' * level} ",
                f"{'#' * (level + 1)} ",
                body,
                flags=re.M,
            )
        leftovers = sorted(set(LEFTOVER.findall(body)))
        if leftovers:
            print(
                f"[WARN] {key} 存在未解析占位符：{', '.join(leftovers)}",
                file=sys.stderr,
            )
        parts.append(f"## {heading}")
        parts.append("")
        parts.append(body)
        parts.append("")

    parts.append("## References")
    parts.append("")
    if cited:
        for i, k in enumerate(cited, start=1):
            parts.append(format_reference(i, library[k]))
            parts.append("")
    else:
        parts.append("<!-- 未检测到引用：sections 中没有 {{cite:...}} 标记 -->")
        parts.append("")

    return "\n".join(parts)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Assemble manuscript.md from sections/")
    parser.add_argument("--root", default=".", help="项目根目录（默认当前目录）")
    parser.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = parser.parse_args(argv)

    project_root = Path(args.root).resolve()
    manuscript_dir = project_root / "05_Manuscript"
    sections_dir = manuscript_dir / "sections"
    target = manuscript_dir / "manuscript.md"

    sections = load_sections(sections_dir)
    if not sections:
        print(f"[FAIL] 未找到章节文件：{sections_dir}", file=sys.stderr)
        print("       请先执行 writing workflow 的 results 步骤。", file=sys.stderr)
        return 2

    problems = validate(sections)
    if problems:
        print("[FAIL] 无法拼装：", file=sys.stderr)
        for item in problems:
            print(f"  - {item}", file=sys.stderr)
        return 1

    if args.check:
        print("[OK] 章节校验通过")
        for key, heading in ORDER:
            info = sections[key]
            print(f"  {heading:<14} {info['status']:<6} {info['words']:>6} 字")
        return 0

    manuscript_dir.mkdir(parents=True, exist_ok=True)
    target.write_text(render(sections, project_root), encoding="utf-8")

    total = sum(sections[key]["words"] for key, _ in ORDER)
    print(f"[OK] 已生成 {target}")
    print(f"     总字数约 {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
