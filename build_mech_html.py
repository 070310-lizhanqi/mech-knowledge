# -*- coding: utf-8 -*-
"""把 mech-formula-sources 下的 markdown 公式库编译成自包含单文件 HTML 速查手册。

输入：_header.md（目录 + 交叉核对差异汇总）、part1.md~part4.md（四篇正文）
输出：mech-formula-handbook.html
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "mech-formula-sources")
OUT = os.path.join(BASE, "mech-formula-handbook.html")

# ---------------------------------------------------------------- markdown 工具


def split_row(line):
    """按 | 切分表格行，跳过 $...$ 数学段内部的 |。"""
    cells, buf, depth, i = [], "", 0, 0
    while i < len(line):
        c = line[i]
        if c == "$":
            depth ^= 1
        if c == "|" and depth == 0:
            cells.append(buf)
            buf = ""
        else:
            buf += c
        i += 1
    cells.append(buf)
    if cells and not cells[0].strip():
        cells = cells[1:]
    if cells and not cells[-1].strip():
        cells = cells[:-1]
    return [c.strip() for c in cells]


def is_sep_row(line):
    body = line.strip().strip("|").strip()
    if not body:
        return False
    return bool(re.fullmatch(r"[\s:\-|]+", body)) and "-" in body


def md_inline(text):
    """行内 markdown：代码段 / 粗体 / 斜体 / 链接 -> HTML（数学 $..$ 留给 JS 渲染）。"""
    out, i, n = "", 0, len(text)
    while i < n:
        c = text[i]
        if c == "`":
            j = text.find("`", i + 1)
            if j > i:
                code = text[i + 1 : j]
                cls = "cm" if ("\\" in code or "_" in code or "^" in code) else "cd"
                out += '<code class="%s">%s</code>' % (cls, esc(code))
                i = j + 1
                continue
        if c == "*" and text[i : i + 2] == "**":
            j = text.find("**", i + 2)
            if j > i:
                out += "<strong>%s</strong>" % md_inline(text[i + 2 : j])
                i = j + 2
                continue
        if c == "[" and text[i : i + 4] == "[待":
            j = text.find("]", i)
            if j > i:
                out += '<span class="tbd">%s</span>' % esc(text[i : j + 1])
                i = j + 1
                continue
        if c == "[":
            j = text.find("]", i)
            k = text.find("(", j)
            if j > i and k == j + 1 and text.find(")", k) > k:
                label = text[i + 1 : j]
                href = text[k + 1 : text.find(")", k)]
                out += '<a href="%s" target="_blank" rel="noopener">%s</a>' % (
                    esc(href),
                    md_inline(label),
                )
                i = text.find(")", k) + 1
                continue
        out += esc(c)
        i += 1
    return out


def esc(s):
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


def latex_of(s):
    """取出 $...$ / $$...$$ 中的 LaTeX 源码。"""
    s = s.strip()
    if s.startswith("$$") and s.endswith("$$") and len(s) > 4:
        return s[2:-2].strip()
    if s.startswith("$") and s.endswith("$") and len(s) > 2:
        return s[1:-1].strip()
    return None


# ---------------------------------------------------------------- 解析 part 文件


def parse_blocks(lines):
    """把一段行切成有序块：('h', text) ('p', text) ('ul', [items]) ('table', rows) ('quote', text)"""
    blocks, i, n = [], 0, len(lines)
    while i < n:
        raw = lines[i]
        line = raw.rstrip("\n")
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i].rstrip("\n")))
                i += 1
            if rows and is_sep_row("|".join(rows[1])) if len(rows) > 1 else False:
                pass
            body = [r for r in rows if not is_sep_row("|".join(r))]
            if body:
                head, data = body[0], body[1:]
                blocks.append(("table", {"head": head, "rows": data}))
            continue
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            blocks.append(("quote", " ".join(x for x in buf if x)))
            continue
        if re.match(r"^[-*+]\s+", s):
            items = []
            while i < n and re.match(r"^\s*[-*+]\s+", lines[i].rstrip("\n")):
                items.append(re.sub(r"^\s*[-*+]\s+", "", lines[i].rstrip("\n")).strip())
                i += 1
            blocks.append(("ul", items))
            continue
        if re.match(r"^\d+[.)]\s+", s):
            items = []
            while i < n and re.match(r"^\s*\d+[.)]\s+", lines[i].rstrip("\n")):
                items.append(re.sub(r"^\s*\d+[.)]\s+", "", lines[i].rstrip("\n")).strip())
                i += 1
            blocks.append(("ol", items))
            continue
        if s.startswith("---") or s.startswith("==="):
            i += 1
            continue
        if s.startswith("#"):
            blocks.append(("h", s))
            i += 1
            continue
        buf = []
        while i < n:
            t = lines[i].rstrip("\n").strip()
            if (
                not t
                or t.startswith("|")
                or t.startswith(">")
                or t.startswith("#")
                or re.match(r"^[-*+]\s+", t)
                or re.match(r"^\d+[.)]\s+", t)
                or t.startswith("---")
            ):
                break
            buf.append(t)
            i += 1
        blocks.append(("p", " ".join(buf)))
    return blocks


def clean_formula_blocks(blocks):
    """公式条目块 -> 结构化 dict。"""
    formulas = []  # 依序的 LaTeX 源码
    desc, notes, conds, sources, tables, lists, paras = [], [], [], [], [], [], []
    for kind, val in blocks:
        if kind == "p":
            tex = latex_of(val)
            if tex is not None:
                formulas.append(tex)
            else:
                paras.append(val)
        elif kind == "quote":
            notes.append(val)
        elif kind == "ul":
            for it in val:
                if it.startswith("> "):
                    notes.append(it[2:].strip())
                    continue
                m = re.match(r"^\*\*适用条件\*\*[：:]\s*(.*)$", it)
                if m:
                    conds.append(m.group(1).strip())
                    continue
                if re.match(r"^\[来源[：:]", it):
                    sources.append(it.strip("[]"))
                    continue
                m = re.match(r"^\*\*(.*?)\*\*[：:]\s*(.*)$", it)
                if m:
                    lists.append({"k": m.group(1).strip(), "v": m.group(2).strip()})
                    continue
                lists.append({"k": "", "v": it})
        elif kind == "ol":
            for it in val:
                lists.append({"k": "", "v": it})
        elif kind == "table":
            tables.append(val)
        elif kind == "h":
            paras.append(val.lstrip("#").strip())
    return {
        "f": formulas,
        "d": paras,
        "n": notes,
        "c": conds,
        "s": sources,
        "t": tables,
        "l": lists,
    }


def parse_part(path, pid):
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    part = {"id": pid, "title": "", "src": "", "sections": []}
    sec = None
    card = None
    i = 0

    def flush_card():
        nonlocal card
        if card is None:
            return
        sec["cards"].append(
            {
                "id": card["id"],
                "t": card["title"],
                "body": clean_formula_blocks(parse_blocks(card["lines"])),
            }
        )
        card = None

    def flush_sec():
        nonlocal sec
        flush_card()
        if sec is not None:
            part["sections"].append(sec)
            sec = None

    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("# ") and not s.startswith("## "):
            flush_sec()
            part["title"] = s[2:].strip()
            i += 1
            continue
        if s.startswith("## "):
            flush_sec()
            sec = {"id": s[3:].strip(), "cards": []}
            i += 1
            continue
        if s.startswith("### "):
            flush_card()
            m = re.match(r"^###\s+((?:F\d+-\d+)|(?:\d+(?:\.\d+)+))\s+(.*)$", s)
            cid = m.group(1) if m else s[4:].strip()
            title = m.group(2).strip() if m else ""
            card = {"id": cid, "title": title, "lines": []}
            i += 1
            continue
        if sec is not None and card is not None:
            card["lines"].append(lines[i])
        elif sec is not None:
            # 节内直接内容（无卡片标题）
            if s:
                card = {"id": sec["id"] + "-intro", "title": "", "lines": [lines[i]]}
        elif part["title"] and s.startswith(">"):
            part["src"] = s.lstrip("> ").strip()
        i += 1
    flush_sec()
    return part


def parse_header(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()
    # 交叉核对差异汇总：从 '## 交叉核对差异汇总' 到下一个 '---'
    diffs = []
    try:
        st = next(i for i, l in enumerate(lines) if l.strip() == "## 交叉核对差异汇总")
    except StopIteration:
        st = None
    if st is not None:
        i = st + 1
        group = None
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith("### "):
                group = s[4:].strip()
            elif s.startswith("|") and group:
                rows = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    rows.append(split_row(lines[i]))
                    i += 1
                body = [r for r in rows if not is_sep_row("|".join(r))]
                if len(body) > 1:
                    diffs.append({"g": group, "head": body[0], "rows": body[1:]})
                continue
            elif s.startswith("# ") and i > st:
                break
            i += 1
    # 来源清单
    sources = []
    m = re.search(r"## 阅读约定(.*?)\n## ", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            t = line.strip()
            if t.startswith("- **") and "=" in t:
                sources.append(t.lstrip("- ").strip())
    # 统计口径
    return diffs, sources


# ---------------------------------------------------------------- 主流程


def main():
    parts = [parse_part(os.path.join(SRC, "part%d.md" % k), "p%d" % k) for k in range(1, 5)]
    diffs, header_sources = parse_header(os.path.join(SRC, "_header.md"))

    n_formulas = sum(
        1 for p in parts for s in p["sections"] for c in s["cards"] if c["body"]["f"]
    )
    n_cards = sum(len(s["cards"]) for p in parts for s in p["sections"])
    n_sections = sum(len(p["sections"]) for p in parts)

    data = {
        "parts": parts,
        "diffs": diffs,
        "stats": {
            "formulas": n_formulas,
            "cards": n_cards,
            "sections": n_sections,
            "parts": len(parts),
        },
    }

    tpl = open(os.path.join(BASE, "mech-template.html"), encoding="utf-8").read()
    html = tpl.replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("OK  %s" % OUT)
    print("formulas=%d cards=%d sections=%d parts=%d diffs=%d size=%.1fKB"
          % (n_formulas, n_cards, n_sections, len(parts), len(diffs), len(html.encode("utf-8")) / 1024))


if __name__ == "__main__":
    main()
