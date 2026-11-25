"""Export OV4 formal Markdown report to a publication-grade PDF with cover, TOC,
STIX vector math, landscape wide-table chapters, and embedded PDF bookmarks.

Run from repository root in PowerShell:
    $env:PYTHONPATH = "D:/Codex/cache/pdf-python"
    python -B outputs/code/build_9subsys_doc_pdf_v2.py
"""
import argparse
import hashlib
import html
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

repo = Path(__file__).resolve().parents[2]
workspace = repo / "work/spec-pdf-export"
workspace.mkdir(parents=True, exist_ok=True)
session = tempfile.TemporaryDirectory(prefix="export-", dir=workspace, ignore_cleanup_errors=True)
work = Path(session.name)
reports = repo / "outputs/reports"
assets = work / "assets"
assets.mkdir(exist_ok=True, parents=True)
os.environ.setdefault("MPLCONFIGDIR", str(workspace / "matplotlib"))
os.environ["TMP"] = os.environ["TEMP"] = str(work)

import pymupdf as fitz
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from matplotlib import rc_context
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import math_to_image

DEFAULT_MD = reports / "NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md"
DEFAULT_PDF = reports / "NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.pdf"


def escaped(text):
    return html.escape(str(text), quote=True)


def normalize_mathtext(expr):
    s = " ".join(expr.split())
    s = s.replace(r"\operatorname{diag}", r"\mathrm{diag}")
    s = re.sub(r"\\text\{([^}]*)\}", r"\\mathrm{\1}", s)
    s = re.sub(r"\\ge(?![a-zA-Z])", r"\\geq", s)
    s = re.sub(r"\\le(?![a-zA-Z])", r"\\leq", s)
    s = s.replace(r"\implies", r"\Rightarrow")
    s = s.replace(r"\qquad", r"\quad\quad")
    s = s.replace(r"\!", "")
    s = s.replace(r"\,", r"\ ")
    s = s.replace(r"\;", r"\ ")
    s = s.replace(r"\big(", "(").replace(r"\big)", ")")
    s = s.replace(r"\big[", "[").replace(r"\big]", "]")
    s = s.replace(r"\big|", "|")
    s = s.replace(r"\Big(", "(").replace(r"\Big)", ")")
    s = s.replace(r"\vec{f}", r"\mathbf{f}")
    s = s.replace(r"\cdot", r"\times") if r"\mathbf" in s and r"\cdot" in s else s
    # Handle Chinese characters inside \mathrm{} if any
    if re.search(r"[\u4e00-\u9fff]", s):
        return None
    return s


def clean_toc_title(title):
    t = title.replace("`", "")
    t = t.replace(r"$\Delta K_n = K_{n1} - K_{n0}$", "ΔK_n = K_n1 − K_n0")
    t = t.replace(r"$\Delta K_m = K_{m1} - K_{m0}$", "ΔK_m = K_m1 − K_m0")
    t = re.sub(r"\$([^$]+)\$", r"\1", t)
    return t


def vector_math(expr, display):
    norm = normalize_mathtext(expr)
    if norm is None:
        return f'<code class="math-fallback">{escaped(expr)}</code>'
    name = hashlib.sha256((("D:" if display else "I:") + norm).encode("utf-8")).hexdigest()[:18]
    target = assets / f"eq-{name}.svg"
    size = 11.5 if display else 10.5
    if not target.exists():
        try:
            with rc_context({"mathtext.fontset": "stix", "svg.hashsalt": "ov4spec"}):
                math_to_image(
                    "$" + norm + "$",
                    target,
                    prop=FontProperties(size=size),
                    format="svg",
                    color="#142d42",
                )
        except Exception as exc:
            print(f"[WARN] mathtext fallback for {norm!r}: {exc}")
            return f'<code class="math-fallback">{escaped(expr)}</code>'
    svg = target.read_text(encoding="utf-8")
    # Remove opaque white background patch emitted by matplotlib so SVG blends cleanly into tinted boxes & headers
    svg_clean = re.sub(r'<g id="patch_1">.*?</g>', '', svg, flags=re.S)
    if svg_clean != svg:
        target.write_text(svg_clean, encoding="utf-8")
        svg = svg_clean
    m = re.search(r'<svg[^>]+width="([\d.]+)pt" height="([\d.]+)pt"', svg)
    w = float(m.group(1))
    scale = (w / size) * (0.95 if display else 0.90)
    return (
        f'<img class="math {"block-math" if display else "inline-math"}" '
        f'style="width:{scale:.4f}em" src="{target.as_uri()}" alt="{escaped(norm)}">'
    )


def convert_markdown(md):
    resources = []

    def store(match, display):
        n = len(resources)
        resources.append(vector_math(match.group(1), display))
        key = f"MATHRENDERPLACEHOLDER{n:04d}END"
        return f"\n\n{key}\n\n" if display else key

    md = re.sub(r"```math\s*\r?\n(.*?)\r?\n```", lambda m: store(m, True), md, flags=re.S)
    md = re.sub(r"\$\$\s*(.*?)\s*\$\$", lambda m: store(m, True), md, flags=re.S)
    md = re.sub(r"(?<!`)\$`([^`\r\n]+?)`\$", lambda m: store(m, False), md)
    md = re.sub(r"(?<!\\)\$(?!\$)([^$\r\n]+?)\$", lambda m: store(m, False), md)
    rendered = MarkdownIt("commonmark", {"html": True}).enable("table").render(md)
    for n, markup in enumerate(resources):
        rendered = rendered.replace(f"MATHRENDERPLACEHOLDER{n:04d}END", markup)
    return rendered


def gh_link(path, anchor=""):
    try:
        ref = path.resolve().relative_to(repo.resolve()).as_posix()
        return (
            "https://github.com/OpticsPan/OV4/blob/main/"
            + quote(ref)
            + ("#" + quote(unquote(anchor)) if anchor else "")
        )
    except Exception:
        return path.as_uri()


def prepare(md_path):
    raw = md_path.read_text(encoding="utf-8")
    # Slice from Chapter 0 onward (cover + generated TOC replaces markdown header/TOC)
    m0 = re.search(r'<a name="sec-0"></a>', raw)
    assert m0, "Cannot find sec-0 anchor in Markdown"
    body_md = raw[m0.start():]
    # Remove [返回目录](#contents) lines for clean print PDF (PDF has bookmarks + cover TOC)
    body_md = re.sub(r"^\[返回目录\]\(#contents\)\s*$", "", body_md, flags=re.M)

    # Split into per-chapter chunks so we can wrap wide chapters (13, 14, 15) in landscape sections!
    parts = re.split(r'(?=<a name="sec-\d+"></a>)', body_md)
    parts = [p.strip() for p in parts if p.strip()]

    chapters = []
    sections_html = []
    for chunk in parts:
        m_anc = re.search(r'<a name="(sec-(\d+))"></a>', chunk)
        m_h2 = re.search(r"^## (\d+)\.\s+(.+)$", chunk, flags=re.M)
        if not (m_anc and m_h2):
            continue
        sec_id = m_anc.group(1)
        sec_num = int(m_anc.group(2))
        sec_title = m_h2.group(2).strip()
        # Strip raw anchor line before rendering so we attach id cleanly to h2
        chunk_clean = re.sub(r'^<a name="sec-\d+"></a>\s*', "", chunk, count=1)
        html_body = convert_markdown(chunk_clean)
        soup = BeautifulSoup(html_body, "html.parser")

        h2 = soup.find("h2")
        if h2:
            h2["id"] = sec_id

        # Mark block math paragraphs
        for im in soup.select("img.block-math"):
            if im.parent and im.parent.name == "p":
                im.parent["class"] = "equation display-equation"

        # Rewrite relative links to GitHub URLs or internal anchors
        for a in soup.find_all("a", href=True):
            u = urlsplit(a["href"])
            if u.scheme:
                continue
            if not u.path and u.fragment:
                a["href"] = "#" + u.fragment
            else:
                target_path = (md_path.parent / unquote(u.path)).resolve()
                a["href"] = gh_link(target_path, u.fragment)

        # Auto-classify wide tables (>= 11 columns)
        is_landscape = sec_num in (7, 8, 9)
        for tbl in soup.find_all("table"):
            ncols = len(tbl.find_all("th"))
            if ncols >= 15:
                tbl["class"] = "ultra-wide-table"
            elif ncols >= 11:
                tbl["class"] = "wide-table"
            elif ncols >= 8:
                tbl["class"] = "medium-table"

        # Gather h3 subsections for PDF outline
        sub_h3 = []
        for idx_h3, h3 in enumerate(soup.find_all("h3"), 1):
            h3_id = f"{sec_id}-sub-{idx_h3}"
            h3["id"] = h3_id
            sub_h3.append((h3_id, h3.get_text(strip=True)))

        cls = "chapter landscape-chapter" if is_landscape else "chapter portrait-chapter"
        # Force page break before landscape chapters and right after chapter 15, plus clean chapter starts for major sections
        if sec_num in (0, 1, 2, 3, 4, 5, 7, 8, 9, 10):
            cls += " page-break-before"

        sections_html.append(f'<section class="{cls}" id="wrap-{sec_id}">{str(soup)}</section>')
        chapters.append((sec_num, sec_id, clean_toc_title(sec_title), sub_h3, is_landscape))

    return "\n".join(sections_html), chapters


CSS = r"""
@page {
  size: A4 portrait;
  margin: 14mm 12mm 15mm 12mm;
  @top-left { content: "OV4 · ArF 液浸光刻机验收规格推导报告 (1950i–1970i)"; font: 7.5pt "Microsoft YaHei"; color: #52727c; }
  @top-right { content: "九大子系统说明书 v2 · 2026-11-24"; font: 7.5pt "Microsoft YaHei"; color: #52727c; }
  @bottom-left { content: "OpticsPan/OV4 · Overlay & Subsystem Acceptance Spec"; font: 7.5pt "Microsoft YaHei"; color: #617680; }
  @bottom-right { content: "第 " counter(page) " 页"; font: bold 8.5pt "Microsoft YaHei"; color: #173d50; }
}
@page :first {
  @top-left { content: none; }
  @top-right { content: none; }
  @bottom-left { content: "D:\\work\\OV4 · OpticsPan/OV4"; font: 7.5pt "Microsoft YaHei"; color: #617680; }
  @bottom-right { content: none; }
}
@page wide {
  size: A4 landscape;
  margin: 12mm 10mm 13mm 10mm;
  @top-left { content: "OV4 · ArF 液浸光刻机验收规格推导报告 (宽表横版页)"; font: 7.5pt "Microsoft YaHei"; color: #52727c; }
  @top-right { content: "九大子系统说明书 v2 · 2026-11-24"; font: 7.5pt "Microsoft YaHei"; color: #52727c; }
  @bottom-left { content: "OpticsPan/OV4 · iHOPC & Odd Zernike (Z5–Z64)"; font: 7.5pt "Microsoft YaHei"; color: #617680; }
  @bottom-right { content: "第 " counter(page) " 页"; font: bold 8.5pt "Microsoft YaHei"; color: #173d50; }
}

* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; color: #1b303c; font: 9.2pt/1.58 "Microsoft YaHei", "SimSun", sans-serif; }

.portrait-chapter { page: auto; }
.landscape-chapter { page: wide; }
.page-break-before { break-before: page; page-break-before: always; }

h1, h2, h3, h4 { font-family: "Microsoft YaHei", sans-serif; color: #123849; break-after: avoid; page-break-after: avoid; line-height: 1.3; }
h2 { border-bottom: 2.2pt solid #087871; font-size: 15.5pt; margin: 2mm 0 3mm; padding: 1mm 0 2mm; }
h3 { font-size: 11.5pt; border-bottom: 0.6pt solid #9dbbb9; margin: 4mm 0 2mm; padding-bottom: 1mm; color: #174e62; }
h4 { font-size: 10pt; margin: 3mm 0 1.2mm; color: #1b4d63; }

p { margin: 1.4mm 0 2mm; orphans: 2; widows: 2; overflow-wrap: anywhere; }
strong { font-weight: 700; color: #122b3d; }
a { color: #006677; text-decoration: none; }
ul, ol { padding-left: 6mm; margin: 1.5mm 0 2mm; }
li { margin: 0.7mm 0; }
hr { border: none; border-top: 0.6pt solid #c8d6da; margin: 3mm 0; }

blockquote {
  border-left: 2.5pt solid #087871;
  background: #f2f8f7;
  padding: 1.5mm 3.5mm;
  margin: 2mm 0 2.5mm;
  font-size: 8.8pt;
}
blockquote p { margin: 0.8mm 0; }

code {
  font: 8.3pt/1.45 Consolas, "Microsoft YaHei", monospace;
  color: #1f3d4d;
  background: #edf2f5;
  padding: 0.2mm 0.8mm;
  border-radius: 1.5pt;
  overflow-wrap: anywhere;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 2mm 0 3mm;
  font-size: 7.7pt;
  line-height: 1.42;
  table-layout: auto;
}
table.medium-table { font-size: 7.2pt; line-height: 1.38; }
table.wide-table { font-size: 7.4pt; line-height: 1.38; }
table.ultra-wide-table { font-size: 6.7pt; line-height: 1.32; }

thead { display: table-header-group; }
tr { break-inside: avoid; page-break-inside: avoid; }
th, td {
  border: 0.45pt solid #b9cbd0;
  padding: 1.1mm 1.3mm;
  vertical-align: middle;
  overflow-wrap: break-word;
}
#wrap-sec-10 table { font-size: 6.85pt; line-height: 1.26; margin: 1.2mm 0 1.8mm; }
#wrap-sec-10 th, #wrap-sec-10 td { padding: 0.6mm 1.0mm; }
#wrap-sec-10 th:nth-child(3), #wrap-sec-10 td:nth-child(1), #wrap-sec-10 td:nth-child(3) { white-space: nowrap; }
#wrap-sec-10 td:nth-child(2) code { word-break: break-all; }
#wrap-sec-10 ul { font-size: 7.9pt; line-height: 1.38; margin: 0.8mm 0; }
#wrap-sec-10 h3 { margin: 1.8mm 0 1mm; }
table.ultra-wide-table th, table.ultra-wide-table td {
  padding: 0.75mm 0.9mm;
  text-align: center;
}
th {
  background: #dceaf2;
  color: #123849;
  font-weight: 700;
  text-align: center;
  border-bottom: 1.4pt solid #1f3864;
}
th strong { color: #0b2c44; }
th code { background: #c5dceb; color: #123849; }
tbody tr:nth-child(even) { background: #f7fafc; }

.equation { text-align: center; margin: 2mm 0; break-inside: avoid; }
.display-equation { padding: 1.8mm 2.5mm; background: #f0f6f7; border-radius: 2pt; border: 0.4pt solid #d2e2e5; }
.inline-math { height: auto; vertical-align: -0.18em; }
.block-math { max-width: 98%; height: auto; vertical-align: middle; }

/* Cover Page */
.cover { padding: 6mm 2mm 0; break-after: page; page-break-after: always; }
.cover-band {
  background: linear-gradient(135deg, #16324f 0%, #0b5d69 100%);
  color: #ffffff;
  padding: 8mm 7mm 7mm;
  border-radius: 3pt;
  margin-bottom: 5mm;
}
.cover-band .eyebrow { font-size: 9pt; letter-spacing: 1pt; color: #a7e4de; margin: 0 0 2mm; font-weight: 700; }
.cover-band h1 { font-size: 19pt; line-height: 1.32; margin: 0 0 2.5mm; color: #ffffff; border: none; }
.cover-band .subtitle { font-size: 9.8pt; color: #d8eff1; margin: 0; }

.kpi-grid { display: flex; gap: 3mm; margin: 0 0 5mm; }
.kpi-card {
  flex: 1;
  background: #f3f8f9;
  border: 0.6pt solid #c0d6dc;
  border-top: 2.2pt solid #087871;
  border-radius: 2pt;
  padding: 2.5mm 3mm;
}
.kpi-card .k-label { font-size: 7.5pt; color: #476470; margin-bottom: 0.8mm; }
.kpi-card .k-val { font-size: 12pt; font-weight: 700; color: #123849; }
.kpi-card .k-sub { font-size: 7.2pt; color: #087871; margin-top: 0.6mm; }

.toc-box h3 { font-size: 11.5pt; margin: 2mm 0 2mm; border-bottom: 1.2pt solid #1f3864; padding-bottom: 1mm; }
.toc-grid { display: grid; grid-template-columns: 1fr 1fr; column-gap: 6mm; row-gap: 1.2mm; }
.toc-row {
  display: flex;
  align-items: baseline;
  border-bottom: 0.4pt dotted #b9cbd0;
  padding: 0.8mm 0;
  font-size: 8.3pt;
}
.toc-row .t-num { font-weight: 700; color: #087871; min-width: 7mm; }
.toc-row .t-name { flex: 1; color: #16324f; }
.toc-row .t-pg { font: bold 8.3pt Arial, sans-serif; color: #1f3864; margin-left: 2mm; }
.cover-meta {
  margin-top: 5mm;
  padding-top: 2.5mm;
  border-top: 0.6pt solid #c6d4d8;
  font-size: 7.8pt;
  color: #4c6670;
  line-height: 1.55;
}
"""


def compose_html(body_html, chapters, pages):
    toc_rows = []
    for num, sec_id, title, _, is_land in chapters:
        tag = " [横版]" if is_land else ""
        pg = pages.get(sec_id, "")
        toc_rows.append(
            f'<div class="toc-row">'
            f'<span class="t-num">{num}.</span>'
            f'<a class="t-name" href="#{sec_id}">{escaped(title)}{tag}</a>'
            f'<a class="t-pg" href="#{sec_id}">{pg}</a>'
            f'</div>'
        )
    cover = f"""
    <section class="cover" id="cover-toc">
      <div class="cover-band">
        <p class="eyebrow">OV4 · NINE CORE SUBSYSTEMS ACCEPTANCE SPECIFICATION & CALCULATION MANUAL (v2 · 8 NEW PRIMARY REFS VERIFIED)</p>
        <h1>ArF 液浸光刻机（对标 NXT:1950i–1970Ci 之间）<br>九大核心子系统验收指标推导与计算说明书</h1>
        <p class="subtitle">覆盖 WS · RS · ENC · AA · TIS · PARIS · WS-iHOPC · Lens Zernike (Z5–Z64) · Lens-iHOPC | 新增 8 篇一手文献全核验 [N1–N8] | 确证 26×5.5 mm 狭缝 · Heertjes 频域定理 · IBM/ASML 实证</p>
      </div>
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="k-label">同机套刻 DCO (|Mean|+3σ)</div>
          <div class="k-val">≤ 2.00 nm</div>
          <div class="k-sub">闭环 1.832 / 1.869 nm (5.5mm狭缝)</div>
        </div>
        <div class="kpi-card">
          <div class="k-label">混机套刻 MMO (99.7%)</div>
          <div class="k-val">≤ 3.50 nm</div>
          <div class="k-sub">闭环 3.134 / 3.154 nm (裕度 9.9%)</div>
        </div>
        <div class="kpi-card">
          <div class="k-label">全片焦面均匀性 FU (3σ)</div>
          <div class="k-val">≤ 12.0 nm</div>
          <div class="k-sub">闭环 10.31 nm (裕度 14.1%)</div>
        </div>
        <div class="kpi-card">
          <div class="k-label">Odd Zernike (Z5–Z64 全 30 项)</div>
          <div class="k-val">0.337 nm RMS</div>
          <div class="k-sub">照明切换套刻 ≤ 0.370 nm (包络)</div>
        </div>
      </div>
      <div class="toc-box">
        <h3>目录（全 11 章 · 第 7–9 章采用横向 A4 宽页确保 iHOPC 与 Zernike 宽表清晰无裁切）</h3>
        <div class="toc-grid">
          {"".join(toc_rows)}
        </div>
      </div>
      <div class="cover-meta">
        <strong>文档版本：</strong>v2（2026-11-24，已完成 参考文献_新增 全部 8 篇一手论文/专利全文核验 [N1–N8] 并更新推导证据链）　|　<strong>仓库归属：</strong>D:\work\OV4（对应 GitHub <code>OpticsPan/OV4</code>）<br>
        <strong>配套文件：</strong>Markdown 网页版 v2（<code>..._v2.md</code>）、Excel 动态预算表 v2（<code>..._v2.xlsx</code>，9 表 686 公式 0 错）、28 页证据链 PPTX v2（<code>..._v2.pptx</code>）<br>
        <strong>依据来源：</strong>本机只读文献库 <code>OV4</code>（243 篇 + 新增 8 篇一手核心论文/专利 [N1–N8]）与 <code>ME3</code>（ASML TWINSCAN Level 2/3 官方手册）。
      </div>
    </section>
    """
    return (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<title>ArF 液浸光刻机(1950i–1970i)九大核心子系统验收指标推导与计算说明书 v2</title>'
        f"<style>{CSS}</style></head><body>{cover}{body_html}</body></html>"
    )


def chrome_binary():
    paths = [
        os.environ.get("CHROME"),
        shutil.which("google-chrome"),
        shutil.which("chrome"),
    ]
    for d in ("ProgramFiles", "ProgramFiles(x86)"):
        base = Path(os.environ.get(d, "C:/Program Files"))
        paths.extend([
            base / "Google/Chrome/Application/chrome.exe",
            base / "Microsoft/Edge/Application/msedge.exe",
        ])
    return next(Path(p) for p in paths if p and Path(p).is_file())


def print_pdf(markup, tag="pass"):
    pre = work / f"report-{tag}.html"
    pre.write_text(markup, encoding="utf-8")
    pdf = work / f"printed-{tag}.pdf"
    if pdf.exists():
        pdf.unlink()
    chrome = chrome_binary()
    args = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--no-default-browser-check",
        "--no-first-run",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        f"--user-data-dir={work / ('chrome-profile-' + tag)}",
        f"--disk-cache-dir={work / ('chrome-cache-' + tag)}",
        f"--print-to-pdf={pdf}",
        pre.as_uri(),
    ]
    res = subprocess.run(
        args,
        capture_output=True,
        timeout=120,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    if res.returncode or not pdf.is_file():
        raise RuntimeError(res.stderr.decode("utf-8", "replace"))
    return pdf


def locate_chapters(doc, chapters):
    pages = {}
    toc = [[1, "封面与目录", 1]]
    chapter_map = {num: (sec_id, title) for num, sec_id, title, _, _ in chapters}
    found_nums = set()
    for p in doc:
        if p.number == 0:
            continue
        blocks = p.get_text("dict", flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)["blocks"]
        for b in blocks:
            for line in b.get("lines", []):
                spans = line["spans"]
                if not spans:
                    continue
                txt = "".join(sp["text"] for sp in spans).strip()
                sz = max(sp["size"] for sp in spans)
                m = re.match(r"^(\d+)\.\s+(.+)$", txt)
                if m and sz >= 13.5:
                    num = int(m.group(1))
                    if num in chapter_map and num not in found_nums:
                        sec_id, full_title = chapter_map[num]
                        pages[sec_id] = p.number + 1
                        toc.append([1, f"{num}. {full_title}", p.number + 1])
                        found_nums.add(num)
                elif sz >= 10.5 and sz < 13.5 and re.match(r"^\d+\.\d+\s+", txt):
                    toc.append([2, txt, p.number + 1])
    if len(found_nums) != len(chapters):
        missing = sorted(set(chapter_map.keys()) - found_nums)
        raise RuntimeError(f"Missing chapters in PDF locate: {missing}; found={pages}")
    return pages, toc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_MD)
    parser.add_argument("--target", type=Path, default=DEFAULT_PDF)
    args = parser.parse_args()

    body_html, chapters = prepare(args.source)
    first_pdf = print_pdf(compose_html(body_html, chapters, {}), tag="p1")
    with fitz.open(first_pdf) as doc1:
        pages, _ = locate_chapters(doc1, chapters)

    second_pdf = print_pdf(compose_html(body_html, chapters, pages), tag="p2")
    with fitz.open(second_pdf) as doc2:
        final_pages, toc = locate_chapters(doc2, chapters)
        assert final_pages == pages, f"Page shift between passes: {pages} vs {final_pages}"
        doc2.set_toc(toc)
        meta = doc2.metadata
        meta.update(
            title="ArF 液浸光刻机（对标 NXT:1950i–1970Ci 之间）九大核心子系统验收指标推导与计算说明书 v2",
            subject="DCO<=2.0nm, MMO<=3.5nm, FU<=12nm, WS/RS/ENC/AA/TIS-PARIS/Thermal/Clamping/Frame/iHOPC/Odd Zernike Z5-Z64",
            author="OpticsPan / OV4",
        )
        doc2.set_metadata(meta)
        fd, tmp_name = tempfile.mkstemp(dir=args.target.parent, suffix=".pdf", prefix=".ov4-spec-")
        os.close(fd)
        tmp_path = Path(tmp_name)
        try:
            doc2.save(tmp_path, garbage=3, deflate=True)
            with fitz.open(tmp_path) as chk:
                assert len(chk) == len(doc2)
                assert chk.get_toc() == toc
                assert all(1 <= entry[2] <= len(chk) for entry in chk.get_toc())
                total_pages = len(chk)
            os.replace(tmp_path, args.target)
        finally:
            tmp_path.unlink(missing_ok=True)

    print(f"PDF EXPORTED SUCCESSFULLY: {args.target}")
    print(f"Total pages: {total_pages} | Bookmarks: {len(toc)}")
    for num, sec_id, title, _, is_land in chapters:
        print(f"  Ch {num:2d} (p.{final_pages[sec_id]:2d}, {'LAND' if is_land else 'PORT'}): {title}")


if __name__ == "__main__":
    main()
