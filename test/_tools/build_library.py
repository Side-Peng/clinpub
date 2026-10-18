"""从 pubmed_fetch 结果构建 reference_library.json。"""
import io
import json
import re
import unicodedata
from pathlib import Path

BASE = Path(r"D:\Projects\Skills_Makeing\02_Gsd Like Scientific pipeline\clinpub\test")
REF = BASE / "Reference"
REF.mkdir(exist_ok=True)

raw = io.open(REF / "_raw.json", encoding="utf-8-sig").read()
i = min([x for x in [raw.find("["), raw.find("{")] if x >= 0])
data = json.loads(raw[i:])
arts = data["articles"]

# 每篇首次进入的章节
SECTION = {
    "36444151": "introduction",   # confounding by indication (SSRI)
    "41667639": "introduction",   # moderators of treatment response in LLD
    "32215634": "introduction",   # symptom burden in late-life depression
    "38812455": "introduction",   # 15-year depressive symptom transitions
    "18313558": "methods",        # STROBE statement
    "31090043": "methods",        # multiple imputation (incomplete data)
    "39846338": "methods",        # multiple imputation tutorial
    "38452496": "discussion",     # predictors of remission after rTMS
    "29100149": "discussion",     # treatment response in LLD
    "41313677": "discussion",     # depression symptom exposure and dementia
    "26474974": "discussion",     # healthy vaccinee bias / confounding by indication
    "23567441": "discussion",     # dynamic prediction of treatment response
}


def surname(author: str) -> str:
    """PubMed 格式为 "Steffens D"（姓 + 名缩写），姓在第一个词。

    带逗号的 "Steffens, D" 走另一分支。变音符号（Göke）做 ASCII 归一化，
    否则会被正则吃掉一个字母变成 "Gke"。
    """
    a = author.strip()
    if "," in a:
        last = a.split(",")[0].strip()
    else:
        parts = a.split()
        if not parts:
            return "Anon"
        particles = {"von", "van", "de", "del", "della", "der", "da", "di", "le", "la", "den"}
        if parts[0].lower() in particles and len(parts) > 1:
            last = parts[0] + parts[1]
        else:
            last = parts[0]
    # Göke → Goke
    last = unicodedata.normalize("NFKD", last).encode("ascii", "ignore").decode()
    last = re.sub(r"[^A-Za-z\-]", "", last)
    return last or "Anon"


lib = []
for n, a in enumerate(arts, start=1):
    authors = a.get("authors") or []
    if isinstance(authors, str):
        authors = [x.strip() for x in authors.split(";") if x.strip()]
    first = surname(authors[0]) if authors else "Anon"
    first = re.sub(r"[^A-Za-z\-]", "", first) or "Anon"
    year = str(a.get("year") or "")
    doi = (a.get("doi") or "").strip()
    lib.append(
        {
            "id": n,
            "citation_key": f"{first}{year}",
            "title": a.get("title", "").strip(),
            "authors": authors,
            "journal": a.get("journal", ""),
            "year": year,
            "volume": "",
            "pages": "",
            "doi": doi if doi else "pending_doi",
            "pmid": a.get("pmid", ""),
            "added_by_section": SECTION.get(a.get("pmid"), "discussion"),
            "sections_used": [SECTION.get(a.get("pmid"), "discussion")],
            "abstract": (a.get("abstract") or "").strip(),
            "added_date": "2026-10-18",
        }
    )

# citation_key 冲突处理
seen = {}
for r in lib:
    k = r["citation_key"]
    if k in seen:
        r["citation_key"] = f"{k}_{seen[k] + 1}"
        seen[k] += 1
    else:
        seen[k] = 0

(REF / "reference_library.json").write_text(
    json.dumps({"library_version": "3.0", "updated": "2026-10-18", "references": lib},
               ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(f"  已写入 {len(lib)} 条")
for r in lib:
    nd = "✅" if r["doi"] != "pending_doi" else "⚠ pending"
    print(f"  [{r['id']:>2}] {r['citation_key']:<22} {r['year']} {nd:<10} {r['title'][:48]}")
