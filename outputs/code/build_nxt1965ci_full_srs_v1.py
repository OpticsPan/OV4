"""Generate ASML TWINSCAN NXT:1965Ci Complete 12-Subsystem Overlay Specification SRS Suite (v1).

Produces 14 synchronized, strictly pure-SRS deliverables from `srs_full_data_nxt1965ci_v1.py`:
  1. Complete Full-Machine SRS PDF:
       outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_v1.pdf
  2. Complete Full-Machine Master Word + 12 Standalone Self-Contained Subsystem Word Files (13 DOCX):
       outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/
         00_整机总册_ASML_NXT1965Ci套刻预算规格需求书_v1.docx
         01_WS晶圆台_套刻预算规格需求书_v1.docx
         ...
         12_MF与ENV计量框架及微环境_套刻预算规格需求书_v1.docx

Strict Content Separation Policy:
  - Contains ONLY engineering acceptance specifications (T1/T2/T3), test definitions, dry/wet/on-machine
    fixture boundaries, multi-stage coupling philosophy, physical mechanism notes, and 17 verified
    primary paper figures.
  - Enforces automated ZERO-LEAKAGE assertions ensuring top-down variance allocation math and bottom-up
    machine overlay recovery predictions (DCO/SMO/MMO roll-up) never appear inside ANY SRS deliverable
    (those reside exclusively in `ASML_NXT1965Ci指标规格分配计算报告_v1.pdf` and
    `calc_nxt1965ci_overlay_budget_audit_v1.py`).

Run from repository root in PowerShell:
    $env:PYTHONPATH = "D:/Codex/cache/pdf-python"
    python -B outputs/code/build_nxt1965ci_full_srs_v1.py
"""
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image
import docx
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor
import pymupdf as fitz

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from srs_full_data_nxt1965ci_v1 import (  # noqa: E402
    MASTER_REFS,
    MASTER_STAGE_SUMMARY,
    PAPER_IMGS,
    PHILOSOPHY_PARAS,
    build_all_12_subsystems,
)

REPO = Path(__file__).resolve().parents[2]
OUT_PDF = REPO / "outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_v1.pdf"
OUT_DOCX_DIR = REPO / "outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1"
WORK_DIR = REPO / "work/full-srs-v1"
PDF_PREV_DIR = WORK_DIR / "pdf_preview"
VERIFY_PDF_DIR = WORK_DIR / "docx_verify_pdf"
DOCX_PREV_DIR = WORK_DIR / "docx_preview"

# Forbidden roll-up / variance-allocation leakage strings (MUST NOT appear in any SRS)
FORBIDDEN_SRS_STRINGS = [
    "2.257", "2.26 nm", "2.364", "2.36 nm", "4.291", "4.29 nm",
    "20.24%", "25.38%", "11.99%", "16.58%", "17.61%", "8.21%",
    "Ref009 Fig. 3", "方差份额", "回收预估",
]

# Palette (Matches OV4-SRS Minimalist Engineering Style)
NAVY_DARK = RGBColor(0x10, 0x2A, 0x43)
NAVY_MAIN = RGBColor(0x16, 0x3A, 0x59)
SLATE_SUB = RGBColor(0x48, 0x65, 0x81)
TEXT_MAIN = RGBColor(0x1A, 0x24, 0x30)
TEXT_MUTED = RGBColor(0x36, 0x4B, 0x5E)
HDR_GRAY = RGBColor(0x5C, 0x6F, 0x80)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

HEX_NAVY = "163A59"
HEX_NAVY_BORDER = "2B5275"
HEX_STRIPE = "F6F9FC"
HEX_NOTE_BG = "F7FAFC"
HEX_META_K = "F4F7FA"
HEX_BORDER = "D4DFE8"
HEX_OUTER = "B8C8D6"

# A4 usable width: 21.0 cm - 2 * 1.5 cm = 18.0 cm
PAGE_WIDTH_CM = 18.0

TOKEN_RE = re.compile(r"(\*\*[^*]+?\*\*|\*[^*]+?\*|_\{[^{}]+\}|\^\{[^{}]+\})")
REF_TOKEN_RE = re.compile(r"\[((?:R\d+(?:,\s*)?)+)\]")


# =============================================================================
# CITATION RENUMBERING & RICH TEXT PARSING (HTML & DOCX)
# =============================================================================
def collect_ref_ids(texts: list) -> list:
    seen = []
    for t in texts:
        for m in REF_TOKEN_RE.finditer(str(t)):
            for rid_s in re.findall(r"R(\d+)", m.group(1)):
                rid = int(rid_s)
                if rid not in seen:
                    seen.append(rid)
    return seen


def resolve_citations(text: str, id_map: dict) -> str:
    def _repl(m):
        nums = [str(id_map[int(x)]) for x in re.findall(r"R(\d+)", m.group(1))]
        return "[" + ", ".join(nums) + "]"
    return REF_TOKEN_RE.sub(_repl, str(text))


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def rich_to_html(text: str) -> str:
    """Convert **bold**, *italic*, _{sub}, ^{sup} (including nested sub/sup in bold) to HTML."""
    out = []
    for part in TOKEN_RE.split(str(text)):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append(f"<strong>{rich_to_html(part[2:-2])}</strong>")
        elif part.startswith("*") and part.endswith("*"):
            out.append(f"<em>{esc(part[1:-1])}</em>")
        elif part.startswith("_{") and part.endswith("}"):
            out.append(f"<sub>{esc(part[2:-1])}</sub>")
        elif part.startswith("^{") and part.endswith("}"):
            out.append(f"<sup>{esc(part[2:-1])}</sup>")
        else:
            out.append(esc(part))
    return "".join(out)


def build_dispatch_rows(subsystems: list) -> list:
    rows = []
    for sub in subsystems:
        total_items = sum(len(t[4]) for t in sub["tables"])
        stages = " / ".join(
            re.search(r"(T\d(?:-[A-Z])?)", t[1]).group(1) if re.search(r"(T\d(?:-[A-Z])?)", t[1]) else f"表{t[0]}"
            for t in sub["tables"]
        )
        rows.append((
            sub["code"],
            sub["short_name"],
            f"{stages}（共 {total_items} 项）",
            sub["stage_scope"],
            sub["filename"],
        ))
    return rows


# =============================================================================
# PART A: COMPLETE 12-SUBSYSTEM SRS PDF (Chrome Headless + PyMuPDF 2-Pass TOC)
# =============================================================================
PDF_CSS = r"""
@page {
  size: A4 portrait;
  margin: 17mm 14mm 16mm 14mm;
  @top-left {
    content: "OV4 ASML NXT:1965Ci 套刻预算规格需求书（十二大子系统完整版 v1）";
    font-family: "Times New Roman", "SimSun", "宋体", serif;
    font-size: 8pt;
    color: #5C6F80;
    border-bottom: 0.5pt solid #D4DFE8;
    padding-bottom: 3pt;
    width: 100%;
    vertical-align: bottom;
    margin-bottom: 4pt;
  }
  @bottom-right {
    content: "第 " counter(page) " 页 / 共 " counter(pages) " 页";
    font-family: "Times New Roman", "SimSun", "宋体", serif;
    font-size: 8pt;
    color: #5C6F80;
    padding-top: 3pt;
  }
}

@page :first {
  margin: 14mm 14mm 14mm 14mm;
  @top-left { content: none; border: none; }
  @bottom-right { content: none; }
}

* { box-sizing: border-box; }

body {
  margin: 0;
  padding: 0;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  line-height: 1.46;
  color: #1A2430;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.cover-page { page-break-after: always; }
.toc-page { page-break-after: always; }

.top-rule { height: 2.4pt; background: #163A59; margin-bottom: 12pt; }
.doc-code {
  text-align: center;
  font-size: 9pt;
  font-weight: bold;
  color: #2B5275;
  letter-spacing: 0.4pt;
  margin-bottom: 6pt;
}
.doc-title {
  text-align: center;
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 18pt;
  font-weight: bold;
  color: #102A43;
  margin: 0 0 6pt 0;
  line-height: 1.25;
}
.doc-subtitle {
  text-align: center;
  font-size: 9.2pt;
  color: #486581;
  margin: 0 0 10pt 0;
}
.cover-divider { height: 0.8pt; background: #CBD6E2; margin-bottom: 10pt; }

table.meta-tbl {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 10pt;
  border: 0.7pt solid #C5D2DF;
}
table.meta-tbl td {
  font-size: 8.9pt;
  line-height: 1.40;
  padding: 4.2pt 6.8pt;
  border: 0.5pt solid #D4DFE8;
  vertical-align: top;
}
table.meta-tbl td.m-k {
  width: 15.5%;
  background: #F4F7FA;
  font-weight: bold;
  color: #102A43;
}
table.meta-tbl td.m-v { width: 34.5%; color: #243442; }

.rev-box {
  background: #F7FAFC;
  border: 0.6pt solid #D4DFE8;
  border-left: 2.8pt solid #163A59;
  padding: 6.5pt 9.5pt;
  margin-bottom: 10pt;
  font-size: 8.8pt;
  line-height: 1.46;
  text-align: justify;
  color: #243442;
}
.rev-box p { margin: 0 0 4pt 0; }
.rev-box p:last-child { margin-bottom: 0; }

.cover-map-title {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 9.6pt;
  font-weight: bold;
  color: #102A43;
  border-bottom: 1pt solid #163A59;
  padding-bottom: 2.5pt;
  margin: 8pt 0 5pt 0;
}

.toc-box {
  border: 0.7pt solid #D4DFE8;
  padding: 6.5pt 10pt 5.5pt 10pt;
}
.toc-title {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 11pt;
  font-weight: bold;
  color: #102A43;
  border-bottom: 1.1pt solid #163A59;
  padding-bottom: 3pt;
  margin: 0 0 4pt 0;
}
table.toc-tbl { width: 100%; border-collapse: collapse; }
table.toc-tbl td {
  font-size: 8.1pt;
  line-height: 1.22;
  padding: 0.85pt 0;
  border-bottom: 0.4pt dotted #E2EAF0;
}
tr.toc-ch td {
  font-weight: bold;
  color: #102A43;
  padding-top: 2.0pt;
}
tr.toc-sec td.toc-name { padding-left: 14pt; color: #364B5E; }
td.toc-pg { width: 28pt; text-align: right; font-weight: bold; color: #163A59; }

.chapter { page-break-before: always; }
.chapter.first-ch { page-break-before: auto; }

h1.ch-title {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 12.2pt;
  font-weight: bold;
  color: #102A43;
  border-bottom: 1.2pt solid #163A59;
  padding-bottom: 3.2pt;
  margin: 0 0 6.5pt 0;
  break-after: avoid;
  page-break-after: avoid;
}
h2 {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 9.8pt;
  font-weight: bold;
  color: #163A59;
  margin: 7.5pt 0 4pt 0;
  break-after: avoid;
  page-break-after: avoid;
}

table.spec-tbl {
  width: 100%;
  border-collapse: collapse;
  margin: 2pt 0 7.5pt 0;
  table-layout: fixed;
  border: 0.7pt solid #B8C8D6;
}
table.spec-tbl thead { display: table-header-group; }
table.spec-tbl th {
  background: #163A59;
  color: #FFFFFF;
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 9pt;
  font-weight: bold;
  text-align: left;
  padding: 4pt 4.8pt;
  border: 0.5pt solid #2B5275;
  line-height: 1.28;
}
table.spec-tbl th.th-c { text-align: center; }
table.spec-tbl tr { break-inside: avoid; page-break-inside: avoid; }
table.spec-tbl tbody tr:nth-child(even) { background: #F6F9FC; }
table.spec-tbl td {
  font-size: 9pt;
  line-height: 1.32;
  padding: 2.2pt 4.3pt;
  border: 0.5pt solid #D4DFE8;
  vertical-align: top;
  word-wrap: break-word;
  overflow-wrap: break-word;
}
table.spec-tbl.compact td {
  font-size: 8.6pt;
  line-height: 1.26;
  padding: 2.0pt 4.0pt;
}
td.c-idx { text-align: center; color: #102A43; font-weight: bold; }
table.spec-tbl:not(.compact) td.c-idx { white-space: nowrap; }
td.c-name { color: #102A43; font-weight: bold; }
td.c-spec { text-align: center; color: #102A43; font-weight: bold; }
td.c-def { color: #243442; }

.note-box {
  background: #F7FAFC;
  border: 0.6pt solid #D4DFE8;
  border-left: 2.5pt solid #163A59;
  padding: 5.5pt 9pt;
  margin: 4pt 0 7pt 0;
}
.note-box p {
  margin: 0 0 3.6pt 0;
  font-size: 9pt;
  line-height: 1.42;
  text-align: justify;
}
.note-box p:last-child { margin-bottom: 0; }
.note-box p.indent { padding-left: 10pt; }
.eq-line {
  font-size: 9pt;
  text-align: center;
  background: #FFFFFF;
  border: 0.5pt solid #DCE4EC;
  padding: 3.5pt 6pt;
  margin: 3.5pt 12pt 4.5pt 12pt;
  color: #102A43;
}

.fig-row {
  display: flex;
  gap: 8pt;
  margin: 6pt 0 8pt 0;
  break-inside: avoid;
  page-break-inside: avoid;
}
.fig-cell {
  flex: 1;
  border: 0.6pt solid #D4DFE8;
  background: #FFFFFF;
  padding: 5pt 6pt 4.5pt 6pt;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
}
.fig-cell img, .fig-single img {
  max-width: 100%;
  width: auto;
  height: auto;
  display: block;
  margin: 0 auto;
}
.fig-single {
  border: 0.6pt solid #D4DFE8;
  background: #FFFFFF;
  padding: 5.5pt 8pt 5pt 8pt;
  margin: 6pt 0 8pt 0;
  text-align: center;
  break-inside: avoid;
  page-break-inside: avoid;
}
.fig-cap {
  margin-top: 4pt;
  font-size: 8.2pt;
  line-height: 1.34;
  color: #364B5E;
  text-align: left;
  width: 100%;
}

ol.ref-list { margin: 3pt 0 0 0; padding-left: 20pt; }
ol.ref-list li {
  margin-bottom: 1.6pt;
  font-size: 8.3pt;
  line-height: 1.25;
  word-break: break-word;
}
"""


def render_html_table(headers: list, rows: list, widths_pct: list,
                      center_cols=(0, 2), bold_cols=(0, 1, 2), compact=False) -> str:
    ths = []
    for i, (h, w) in enumerate(zip(headers, widths_pct)):
        cls = ' class="th-c"' if i in center_cols else ""
        ths.append(f'<th{cls} style="width:{w}">{esc(h)}</th>')
    trs = []
    for row in rows:
        tds = []
        for i, val in enumerate(row):
            if i == 0 and i in center_cols:
                cls = "c-idx"
            elif i in center_cols and i in bold_cols:
                cls = "c-spec"
            elif i in bold_cols:
                cls = "c-name"
            else:
                cls = "c-def"
            tds.append(f'<td class="{cls}">{rich_to_html(val)}</td>')
        trs.append("<tr>" + "".join(tds) + "</tr>")
    tcls = "spec-tbl compact" if compact else "spec-tbl"
    return f'<table class="{tcls}"><thead><tr>{"".join(ths)}</tr></thead><tbody>{"".join(trs)}</tbody></table>'


def col_cm_to_pct(col_w: list) -> list:
    s = sum(col_w)
    return [f"{w / s * 100:.1f}%" for w in col_w]


def render_html_notes(notes: list, ref_map: dict) -> str:
    parts = ['<div class="note-box">']
    for kind, txt in notes:
        rtxt = rich_to_html(resolve_citations(txt, ref_map))
        if kind == "p":
            parts.append(f"<p>{rtxt}</p>")
        elif kind == "indent":
            parts.append(f'<p class="indent">{rtxt}</p>')
        elif kind == "eq":
            parts.append(f'<div class="eq-line">{rtxt}</div>')
    parts.append("</div>")
    return "\n".join(parts)


def render_html_figs(figs: list, ref_map: dict) -> str:
    parts = []
    for kind, k1, c1, k2, c2 in figs:
        rc1 = rich_to_html(resolve_citations(c1, ref_map))
        if kind == "pair":
            rc2 = rich_to_html(resolve_citations(c2, ref_map))
            parts.append(
                f'<div class="fig-row">'
                f'<div class="fig-cell"><img src="{PAPER_IMGS[k1].as_uri()}" style="max-height:122pt"/><div class="fig-cap">{rc1}</div></div>'
                f'<div class="fig-cell"><img src="{PAPER_IMGS[k2].as_uri()}" style="max-height:122pt"/><div class="fig-cap">{rc2}</div></div>'
                f'</div>'
            )
        else:
            parts.append(
                f'<div class="fig-single">'
                f'<img src="{PAPER_IMGS[k1].as_uri()}" style="max-height:132pt"/>'
                f'<div class="fig-cap">{rc1}</div>'
                f'</div>'
            )
    return "\n".join(parts)


def build_pdf_chapters(subsystems: list) -> list:
    master_map = {i: i for i in range(1, len(MASTER_REFS) + 1)}
    dispatch_rows = build_dispatch_rows(subsystems)
    chapters = []

    # Chapter 0: Philosophy & 12-Subsystem Dispatch
    ch0_html = f"""
    <h2>0.1 整机设置 T1 / T2 / T3 多阶段验收的核心工程理念</h2>
    {render_html_notes([("p", t) for t in PHILOSOPHY_PARAS], master_map)}

    <h2>0.2 T1 / T2 / T3 多阶段验收职责与耦合边界总表</h2>
    {render_html_table(
        ["验收阶段", "验收定位", "标准测试环境与工装边界", "拦截的耦合风险与整机放行意义"],
        MASTER_STAGE_SUMMARY,
        ["12%", "20%", "30%", "38%"],
        center_cols=(0,), bold_cols=(0, 1), compact=True,
    )}

    <h2>0.3 十二大子系统验收范围与配套独立分册清单</h2>
    {render_html_table(
        ["分册编号", "子系统名称", "验收层级与项数", "多阶段验收路径边界", "对应独立下发 Word 文件"],
        dispatch_rows,
        ["12.5%", "20%", "17.5%", "26%", "24%"],
        center_cols=(0,), bold_cols=(0, 1), compact=True,
    )}
    """
    chapters.append({
        "num": 0, "id": "ch-0",
        "title": "第 0 章　总则：多阶段验收理念与模块-整机耦合边界",
        "toc_title": "第 0 章　总则：多阶段验收理念与模块-整机耦合边界",
        "sections": [
            "0.1 整机设置 T1 / T2 / T3 多阶段验收的核心工程理念",
            "0.2 T1 / T2 / T3 多阶段验收职责与耦合边界总表",
            "0.3 十二大子系统验收范围与配套独立分册清单",
        ],
        "html": ch0_html,
    })

    # Chapters 1..12
    for sub in subsystems:
        sec_list = []
        blocks = []
        for sec_no, sec_title, col2_hdr, col_w, rows in sub["tables"]:
            st = f"{sec_no} {sec_title}"
            sec_list.append(st)
            blocks.append(f"<h2>{esc(st)}</h2>")
            blocks.append(render_html_table(
                ["序号", col2_hdr, "验收规格", "标准测试定义与工装条件"],
                rows, col_cm_to_pct(col_w),
                center_cols=(0, 2), bold_cols=(0, 1, 2),
            ))
        note_no = f"{sub['ch_num']}.{len(sub['tables']) + 1}"
        note_hdr = f"{note_no} 技术注释、测试定义细则与文献图证" if sub["figures"] else f"{note_no} 技术注释与测试定义细则"
        blocks.append(f"<h2>{esc(note_hdr)}</h2>")
        blocks.append(render_html_notes(sub["notes_master"], master_map))
        if sub["figures"]:
            blocks.append(render_html_figs(sub["figures"], master_map))

        chapters.append({
            "num": sub["ch_num"], "id": f"ch-{sub['ch_num']}",
            "title": sub["ch_title"],
            "toc_title": sub["ch_title"],
            "sections": sec_list,
            "html": "\n".join(blocks),
        })

    # Chapter 13: All 33 Verified References
    refs_html = '<ol class="ref-list">' + "".join(
        f"<li>{rich_to_html(MASTER_REFS[i])}</li>" for i in range(1, len(MASTER_REFS) + 1)
    ) + "</ol>"
    chapters.append({
        "num": 13, "id": "ch-13",
        "title": "第 13 章　参考文献",
        "toc_title": "第 13 章　参考文献",
        "sections": [],
        "html": refs_html,
    })
    return chapters


def compose_full_srs_html(subsystems: list, chapters: list, ch_pages: dict, sec_pages: dict) -> str:
    total_items = sum(sum(len(t[4]) for t in s["tables"]) for s in subsystems)

    # Compact 12-subsystem overview table on Cover Page 1
    cover_overview = [
        ("01–03 运动与位置测量", "WS 晶圆台（含 WRS/iHOPC）、RS 掩模台（4×）、ENC 光栅编码器", "T1-A/B（干态）→ T2-A/B（双台同步/Gridplate/Handover）"),
        ("04–05 对准与空间像传感", "AA 晶圆对准（M-side）、TIS + PARIS 空间像传感（E-side 湿区）", "AA：T1→T2→T3（M-to-E）；TIS+PARIS：E 侧实机湿区 T1"),
        ("06 投影光学与操纵器", "Lens 投影物镜（NA = 1.35，30 项奇像差 + 8 项动态 iHOPC）", "T1（局部静态 wet PMI）→ T2-A/B/C（LensModel 与 iHOPC）"),
        ("07–08 浸没液控与晶圆热控", "IH 浸没头与超纯水液控、WT-TC 晶圆台热控与 WH 传片预调温", "T1（离线液控/热控台架）→ T2（水膜/热瞬态）→ T3（批曝）"),
        ("09–10 晶圆与掩模夹持热控", "WC 晶圆夹持与 WT–MB 接口、RC/RH 掩模柔顺夹持、薄膜与 RHC", "T1（离线重夹/微滑移/气幕）→ T2（翘曲/RHC）→ T3（爬坡）"),
        ("11–12 光源照明与整机基盘", "IL/LS 193 nm 光源与 FlexRay 照明、MF/ENV 计量框架、隔振与微环境", "T1（离线光/隔振/环控）→ T2（波长-K3/MF 漂移）→ T3（24 h）"),
    ]

    toc_rows = []
    for ch in chapters:
        pg = ch_pages.get(ch["id"], "—")
        toc_rows.append(
            f'<tr class="toc-ch"><td class="toc-name">{esc(ch["toc_title"])}</td>'
            f'<td class="toc-pg">{pg}</td></tr>'
        )
        for st in ch["sections"]:
            spg = sec_pages.get((ch["id"], st), pg)
            toc_rows.append(
                f'<tr class="toc-sec"><td class="toc-name">{esc(st)}</td>'
                f'<td class="toc-pg">{spg}</td></tr>'
            )

    cover = f"""
    <div class="cover-page">
      <div class="top-rule"></div>
      <div class="doc-code">OV4-SRS-NXT1965Ci-FULL-V1 · 整机全子系统套刻工程规格需求书（完整版）</div>
      <h1 class="doc-title">ASML NXT:1965Ci 套刻预算规格需求书</h1>
      <div class="doc-subtitle">十二大子系统完整验收规格与 T1 / T2 / T3 多阶段模块–整机耦合验收标准</div>
      <div class="cover-divider"></div>

      <table class="meta-tbl">
        <tr>
          <td class="m-k">整机目标定位</td>
          <td class="m-v">ASML TWINSCAN NXT:1965Ci（λ = 193.368 nm，NA = 1.35，β = 1/4）</td>
          <td class="m-k">整机顶层目标</td>
          <td class="m-v">DCO / SMO ≤ 2.50 nm；跨机匹配 MMO ≤ 4.50 nm（≥ 250 wph）</td>
        </tr>
        <tr>
          <td class="m-k">覆盖范围与项数</td>
          <td class="m-v">全机 12 大子系统（共 {total_items} 项独立套刻验收指标，纯套刻专项口径）</td>
          <td class="m-k">曝光狭缝口径</td>
          <td class="m-v">26 × 5.5 mm 真实狭缝（v<sub>w</sub> = 0.70 m/s，τ<sub>slit</sub> = 7.857 ms）</td>
        </tr>
        <tr>
          <td class="m-k">验收分级边界</td>
          <td class="m-v">T1：单件/单台离线；T2：装机解算/同步/调控；T3：跨台整机联调</td>
          <td class="m-k">编制日期与字体</td>
          <td class="m-v">2026-11-27（完整版 v1 · 宋体小五 9 pt / Times New Roman 9 pt）</td>
        </tr>
      </table>

      <div class="rev-box">
        <p><strong>文档定位与边界说明：</strong>本规格需求书面向 ASML TWINSCAN NXT:1965Ci 整机套刻（Overlay）专项验收，按 MECE 原则覆盖光刻机全部 12 大子系统，严格区分 <strong>T1（单件/单台离线）</strong>、<strong>T2（装机解算/同步/调控）</strong> 与 <strong>T3（跨台整机联调）</strong> 三级边界，确保各子系统团队建立模块间耦合与子系统–整机环境耦合意识。纯焦面均匀性指标（Z/Rx/Ry、吸盘平坦度）及成像对比度指标（Sync MSD）不纳入本套刻规格书。</p>
        <p><strong>配套交付物体系：</strong>本文件为整机总体自查完整版（同步提供完整版 Word 总册与 12 份完全自包含的子系统独立下发 Word 分册）。本规格书严格作为工程验收契约文件，仅载明指标限值、标准测试定义、工装边界及一手文献依据，不包含内部预算分配推导与整机误差合成计算过程。</p>
      </div>

      <div class="cover-map-title">十二大子系统架构分组与多阶段验收总览</div>
      {render_html_table(
          ["子系统分组", "涵盖子系统（全机 12 大模块）", "T1 / T2 / T3 验收边界主线"],
          cover_overview,
          ["22.5%", "40.5%", "37%"],
          center_cols=(0,), bold_cols=(0,), compact=True,
      )}
    </div>

    <div class="toc-page">
      <div class="toc-box">
        <div class="toc-title">目　录</div>
        <table class="toc-tbl">{''.join(toc_rows)}</table>
      </div>
    </div>
    """

    parts = [cover]
    for i, ch in enumerate(chapters):
        cls = "chapter first-ch" if i == 0 else "chapter"
        parts.append(
            f'<div class="{cls}" id="{ch["id"]}">'
            f'<h1 class="ch-title">{esc(ch["title"])}</h1>'
            f'{ch["html"]}'
            f'</div>'
        )
    return (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<title>ASML NXT:1965Ci 套刻预算规格需求书（完整版 v1）</title>'
        f'<style>{PDF_CSS}</style></head><body>'
        + "".join(parts) + "</body></html>"
    )


def find_chrome() -> Path:
    for c in (
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        shutil.which("chrome"),
        shutil.which("msedge"),
    ):
        if c and Path(c).is_file():
            return Path(c)
    raise RuntimeError("No Chrome or Edge executable found.")


def render_chrome_pdf(markup: str, work: Path, tag: str) -> Path:
    html_path = work / f"srs-{tag}.html"
    pdf_path = work / f"srs-{tag}.pdf"
    html_path.write_text(markup, encoding="utf-8")
    if pdf_path.exists():
        pdf_path.unlink()
    chrome = find_chrome()
    cmd = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--disable-extensions",
        "--no-first-run",
        "--no-default-browser-check",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        f"--user-data-dir={work / ('prof-' + tag)}",
        f"--print-to-pdf={pdf_path}",
        html_path.as_uri(),
    ]
    res = subprocess.run(cmd, capture_output=True, timeout=180,
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if res.returncode or not pdf_path.is_file():
        raise RuntimeError(res.stderr.decode("utf-8", "replace"))
    return pdf_path


def locate_pdf_headings(doc: fitz.Document, chapters: list):
    ch_pages = {}
    sec_pages = {}
    toc = [[1, "封面", 1], [1, "目录", 2]]

    sec_lookup = {}
    for ch in chapters:
        for st in ch["sections"]:
            code = st.split()[0]
            sec_lookup[code] = (ch["id"], st)

    found_ch = set()
    found_sec = set()

    for p in doc:
        if p.number < 2:  # Skip cover (p.1) & TOC (p.2)
            continue
        pg_num = p.number + 1
        blocks = p.get_text("dict", flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)["blocks"]
        for b in blocks:
            for line in b.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue
                txt = "".join(sp["text"] for sp in spans).strip()
                max_sz = max(sp["size"] for sp in spans)
                m_ch = re.match(r"^第\s*(\d+)\s*章", txt)
                if m_ch and max_sz >= 11.0:
                    num = int(m_ch.group(1))
                    cid = f"ch-{num}"
                    if cid not in found_ch:
                        for ch in chapters:
                            if ch["id"] == cid:
                                ch_pages[cid] = pg_num
                                toc.append([1, ch["toc_title"], pg_num])
                                found_ch.add(cid)
                                break
                m_sec = re.match(r"^(\d+\.\d+)\s+", txt)
                if m_sec and 9.2 <= max_sz < 11.0:
                    code = m_sec.group(1)
                    if code in sec_lookup and code not in found_sec:
                        cid, full_st = sec_lookup[code]
                        sec_pages[(cid, full_st)] = pg_num
                        toc.append([2, full_st, pg_num])
                        found_sec.add(code)

    missing_ch = [ch["id"] for ch in chapters if ch["id"] not in found_ch]
    if missing_ch:
        raise RuntimeError(f"Missing chapters in PDF TOC locate: {missing_ch}; found={ch_pages}")
    return ch_pages, sec_pages, toc


def audit_pdf_quality(doc: fitz.Document, label: str, skip_first_pages: int = 1):
    fonts_9pt = {}
    full_txt_parts = []
    for pg in doc:
        full_txt_parts.append(pg.get_text("text"))
        if pg.number < skip_first_pages:
            continue
        blocks = pg.get_text("dict", flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)["blocks"]
        for b in blocks:
            for line in b.get("lines", []):
                for sp in line.get("spans", []):
                    sz = round(sp["size"], 1)
                    if 8.8 <= sz <= 9.2 and sp["text"].strip():
                        fn = sp["font"]
                        fonts_9pt[fn] = fonts_9pt.get(fn, 0) + len(sp["text"].strip())
    has_simsun = any("SimSun" in k for k in fonts_9pt)
    has_tnr = any("TimesNewRoman" in k for k in fonts_9pt)
    assert has_simsun, f"[{label}] Missing SimSun 9pt! Found: {fonts_9pt}"
    assert has_tnr, f"[{label}] Missing Times New Roman 9pt! Found: {fonts_9pt}"

    full_txt = "\n".join(full_txt_parts)
    assert "{" not in full_txt and "}" not in full_txt, f"[{label}] Raw brace leaked!"
    assert "`" not in full_txt, f"[{label}] Raw backtick leaked!"
    for bad in FORBIDDEN_SRS_STRINGS:
        assert bad not in full_txt, f"[{label}] FORBIDDEN roll-up/allocation string leaked into SRS: {bad!r}"
    return fonts_9pt


def build_complete_srs_pdf(subsystems: list):
    chapters = build_pdf_chapters(subsystems)
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pdf-", dir=WORK_DIR, ignore_cleanup_errors=True) as td:
        work = Path(td)
        p1 = render_chrome_pdf(compose_full_srs_html(subsystems, chapters, {}, {}), work, "p1")
        with fitz.open(p1) as d1:
            ch_p1, sec_p1, _ = locate_pdf_headings(d1, chapters)
        p2 = render_chrome_pdf(compose_full_srs_html(subsystems, chapters, ch_p1, sec_p1), work, "p2")
        with fitz.open(p2) as d2:
            ch_p2, sec_p2, toc = locate_pdf_headings(d2, chapters)
            assert ch_p2 == ch_p1, f"Chapter page shift: {ch_p1} -> {ch_p2}"
            assert ch_p2["ch-0"] == 3, f"Expected Cover=p.1, TOC=p.2, Ch0=p.3; got ch-0=p.{ch_p2['ch-0']}"
            fonts = audit_pdf_quality(d2, OUT_PDF.name, skip_first_pages=2)
            d2.set_toc(toc)
            d2.set_metadata({
                "title": "ASML NXT:1965Ci 套刻预算规格需求书（完整版 v1）",
                "subject": "ASML TWINSCAN NXT:1965Ci 12-Subsystem Complete Overlay SRS (T1/T2/T3)",
                "author": "OpticsPan / OV4",
            })
            OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
            d2.save(OUT_PDF, garbage=3, deflate=True)
            total_pages = len(d2)

            if PDF_PREV_DIR.exists():
                shutil.rmtree(PDF_PREV_DIR)
            PDF_PREV_DIR.mkdir(parents=True, exist_ok=True)
            for pg in d2:
                pg.get_pixmap(dpi=135).save(PDF_PREV_DIR / f"page_{pg.number + 1:02d}.png")

    print(f"[PDF OK] {OUT_PDF.name} | {total_pages} pages | {len(toc)} bookmarks")
    print(f"         9pt fonts: { {k: v for k, v in fonts.items() if 'SimSun' in k or 'TimesNewRoman' in k} }")
    for ch in chapters:
        print(f"         p.{ch_p2[ch['id']]:2d}  {ch['toc_title']}")


# =============================================================================
# PART B: PYTHON-DOCX HELPERS & 13 WORD FILES (1 MASTER + 12 STANDALONE)
# =============================================================================
def set_run_font(run, size_pt=9.0, bold=False, italic=False, color=TEXT_MAIN,
                 zh_font="宋体", en_font="Times New Roman"):
    run.font.name = en_font
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), en_font)
    rFonts.set(qn("w:hAnsi"), en_font)
    rFonts.set(qn("w:cs"), en_font)
    rFonts.set(qn("w:eastAsia"), zh_font)


def add_rich_runs(p, text: str, size_pt=9.0, base_bold=False, color=TEXT_MAIN,
                  zh_font="宋体", en_font="Times New Roman"):
    for part in TOKEN_RE.split(str(text)):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            add_rich_runs(p, part[2:-2], size_pt=size_pt, base_bold=True, color=color,
                          zh_font=zh_font, en_font=en_font)
        elif part.startswith("*") and part.endswith("*"):
            r = p.add_run(part[1:-1])
            set_run_font(r, size_pt=size_pt, bold=base_bold, italic=True, color=color,
                         zh_font=zh_font, en_font=en_font)
        elif part.startswith("_{") and part.endswith("}"):
            r = p.add_run(part[2:-1])
            set_run_font(r, size_pt=size_pt, bold=base_bold, color=color,
                         zh_font=zh_font, en_font=en_font)
            r.font.subscript = True
        elif part.startswith("^{") and part.endswith("}"):
            r = p.add_run(part[2:-1])
            set_run_font(r, size_pt=size_pt, bold=base_bold, color=color,
                         zh_font=zh_font, en_font=en_font)
            r.font.superscript = True
        else:
            r = p.add_run(part)
            set_run_font(r, size_pt=size_pt, bold=base_bold, color=color,
                         zh_font=zh_font, en_font=en_font)


def set_cell_shading(cell, fill_hex: str):
    cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))


def set_cell_margins(cell, top=40, bottom=40, left=70, right=70):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, outer_hex=HEX_OUTER, inner_hex=HEX_BORDER, sz_outer="6", sz_inner="4"):
    table._tbl.tblPr.append(parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz_outer}" w:space="0" w:color="{outer_hex}"/>'
        f'<w:bottom w:val="single" w:sz="{sz_outer}" w:space="0" w:color="{outer_hex}"/>'
        f'<w:left w:val="single" w:sz="{sz_outer}" w:space="0" w:color="{outer_hex}"/>'
        f'<w:right w:val="single" w:sz="{sz_outer}" w:space="0" w:color="{outer_hex}"/>'
        f'<w:insideH w:val="single" w:sz="{sz_inner}" w:space="0" w:color="{inner_hex}"/>'
        f'<w:insideV w:val="single" w:sz="{sz_inner}" w:space="0" w:color="{inner_hex}"/>'
        f'</w:tblBorders>'
    ))


def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side, spec in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        if spec is None:
            continue
        val, sz, color = spec
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), val)
        if val != "none":
            el.set(qn("w:sz"), str(sz))
            el.set(qn("w:space"), "0")
            el.set(qn("w:color"), color)
        tcBorders.append(el)
    tcPr.append(tcBorders)


def set_table_fixed_widths(table, col_widths_cm: list):
    table.autofit = False
    tblPr = table._tbl.tblPr
    tblPr.append(parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>'))
    total_dxa = int(round(sum(col_widths_cm) * 566.929))
    tblPr.append(parse_xml(f'<w:tblW {nsdecls("w")} w:w="{total_dxa}" w:type="dxa"/>'))
    tblGrid = table._tbl.tblGrid
    if tblGrid is not None:
        table._tbl.remove(tblGrid)
    tblGrid = OxmlElement("w:tblGrid")
    for w_cm in col_widths_cm:
        gc = OxmlElement("w:gridCol")
        gc.set(qn("w:w"), str(int(round(w_cm * 566.929))))
        tblGrid.append(gc)
    table._tbl.insert(1, tblGrid)
    for row in table.rows:
        for cell, w_cm in zip(row.cells, col_widths_cm):
            cell.width = Cm(w_cm)
            tcPr = cell._tc.get_or_add_tcPr()
            for old in tcPr.findall(qn("w:tcW")):
                tcPr.remove(old)
            tcW = OxmlElement("w:tcW")
            tcW.set(qn("w:w"), str(int(round(w_cm * 566.929))))
            tcW.set(qn("w:type"), "dxa")
            tcPr.append(tcW)


def set_row_cant_split(row):
    row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))


def set_row_header(row):
    row._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))


def add_p_bottom_border(paragraph, color_hex=HEX_NAVY, sz="12"):
    paragraph._p.get_or_add_pPr().append(parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="3" w:color="{color_hex}"/>'
        f'</w:pBdr>'
    ))


def add_field(paragraph, instr_text: str, size_pt=8.0, color=HDR_GRAY):
    for ftype in ("begin", "instr", "separate", "val", "end"):
        r = paragraph.add_run("1" if ftype == "val" else "")
        set_run_font(r, size_pt=size_pt, color=color)
        if ftype in ("begin", "separate", "end"):
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), ftype)
            r._r.append(fc)
        elif ftype == "instr":
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = f" {instr_text} "
            r._r.append(it)


def init_document(header_text: str) -> Document:
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(9.0)
    normal.font.color.rgb = TEXT_MAIN
    rPr = normal.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for k, v in (("ascii", "Times New Roman"), ("hAnsi", "Times New Roman"), ("cs", "Times New Roman"), ("eastAsia", "宋体")):
        rFonts.set(qn(f"w:{k}"), v)

    for level, sz, clr in ((1, 12.0, NAVY_DARK), (2, 9.8, NAVY_MAIN)):
        st = doc.styles[f"Heading {level}"]
        st.font.name = "Times New Roman"
        st.font.size = Pt(sz)
        st.font.bold = True
        st.font.color.rgb = clr
        srPr = st.element.get_or_add_rPr()
        srFonts = srPr.find(qn("w:rFonts"))
        if srFonts is None:
            srFonts = OxmlElement("w:rFonts")
            srPr.insert(0, srFonts)
        for k, v in (("ascii", "Times New Roman"), ("hAnsi", "Times New Roman"), ("cs", "Times New Roman"), ("eastAsia", "黑体")):
            srFonts.set(qn(f"w:{k}"), v)

    for toc_name, sz, is_b, sb, sa in (("TOC 1", 8.2, True, 1.2, 0.3), ("TOC 2", 7.8, False, 0.1, 0.1)):
        try:
            tst = doc.styles[toc_name]
        except KeyError:
            tst = doc.styles.add_style(toc_name, docx.enum.style.WD_STYLE_TYPE.PARAGRAPH)
        tst.font.name = "Times New Roman"
        tst.font.size = Pt(sz)
        tst.font.bold = is_b
        tst.font.color.rgb = NAVY_DARK if is_b else TEXT_MUTED
        tst.paragraph_format.space_before = Pt(sb)
        tst.paragraph_format.space_after = Pt(sa)
        tst.paragraph_format.line_spacing = 1.04
        trPr = tst.element.get_or_add_rPr()
        trFonts = trPr.find(qn("w:rFonts"))
        if trFonts is None:
            trFonts = OxmlElement("w:rFonts")
            trPr.insert(0, trFonts)
        for k, v in (("ascii", "Times New Roman"), ("hAnsi", "Times New Roman"), ("cs", "Times New Roman"), ("eastAsia", "宋体")):
            trFonts.set(qn(f"w:{k}"), v)

    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(1.55)
    sec.bottom_margin = Cm(1.50)
    sec.left_margin = Cm(1.50)
    sec.right_margin = Cm(1.50)
    sec.header_distance = Cm(0.85)
    sec.footer_distance = Cm(0.85)
    sec.different_first_page_header_footer = True

    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(2)
    set_run_font(hp.add_run(header_text), size_pt=8.0, color=HDR_GRAY)
    add_p_bottom_border(hp, color_hex=HEX_BORDER, sz="4")

    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp.paragraph_format.space_before = Pt(2)
    fp.paragraph_format.space_after = Pt(0)
    set_run_font(fp.add_run("第 "), size_pt=8.0, color=HDR_GRAY)
    add_field(fp, "PAGE", size_pt=8.0, color=HDR_GRAY)
    set_run_font(fp.add_run(" 页 / 共 "), size_pt=8.0, color=HDR_GRAY)
    add_field(fp, "NUMPAGES", size_pt=8.0, color=HDR_GRAY)
    set_run_font(fp.add_run(" 页"), size_pt=8.0, color=HDR_GRAY)

    upd = OxmlElement("w:updateFields")
    upd.set(qn("w:val"), "true")
    doc.settings.element.append(upd)
    return doc


def add_heading_1(doc: Document, text: str, page_break_before=False):
    if page_break_before:
        doc.add_page_break()
    p = doc.add_paragraph(style="Heading 1")
    p.paragraph_format.space_before = Pt(2 if page_break_before else 5.5)
    p.paragraph_format.space_after = Pt(3.5)
    p.paragraph_format.keep_with_next = True
    set_run_font(p.add_run(text), size_pt=12.0, bold=True, color=NAVY_DARK, zh_font="黑体", en_font="Times New Roman")
    add_p_bottom_border(p, color_hex=HEX_NAVY, sz="12")
    return p


def add_heading_2(doc: Document, text: str):
    p = doc.add_paragraph(style="Heading 2")
    p.paragraph_format.space_before = Pt(5.0)
    p.paragraph_format.space_after = Pt(2.8)
    p.paragraph_format.keep_with_next = True
    set_run_font(p.add_run(text), size_pt=9.8, bold=True, color=NAVY_MAIN, zh_font="黑体", en_font="Times New Roman")
    return p


def add_cover_header(doc: Document, doc_code: str, title: str, subtitle: str, meta_rows: list):
    p_rule = doc.add_paragraph()
    p_rule.paragraph_format.space_before = Pt(0)
    p_rule.paragraph_format.space_after = Pt(5)
    add_p_bottom_border(p_rule, color_hex=HEX_NAVY, sz="20")

    p_code = doc.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(2.5)
    set_run_font(p_code.add_run(doc_code), size_pt=8.8, bold=True, color=RGBColor(0x2B, 0x52, 0x75))

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2.5)
    title_sz = 13.4 if len(title) >= 28 else 14.6
    set_run_font(p_title.add_run(title), size_pt=title_sz, bold=True, color=NAVY_DARK, zh_font="黑体", en_font="Times New Roman")

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(4.5)
    set_run_font(p_sub.add_run(subtitle), size_pt=8.8, color=SLATE_SUB)
    add_p_bottom_border(p_sub, color_hex="CBD6E2", sz="6")

    tbl = doc.add_table(rows=len(meta_rows), cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, outer_hex="C5D2DF", inner_hex=HEX_BORDER, sz_outer="6", sz_inner="4")
    for r_idx, (k1, v1, k2, v2) in enumerate(meta_rows):
        row = tbl.rows[r_idx]
        set_row_cant_split(row)
        for c_idx, (txt, is_k) in enumerate(((k1, True), (v1, False), (k2, True), (v2, False))):
            cell = row.cells[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_margins(cell, top=32, bottom=32, left=64, right=64)
            if is_k:
                set_cell_shading(cell, HEX_META_K)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.16
            add_rich_runs(p, txt, size_pt=8.8, base_bold=is_k, color=NAVY_DARK if is_k else TEXT_MAIN)
    set_table_fixed_widths(tbl, [2.7, 6.3, 2.7, 6.3])


def add_callout_box(doc: Document, items: list, compact: bool = False):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    set_cell_shading(cell, HEX_NOTE_BG)
    pad_v = 48 if compact else 70
    set_cell_margins(cell, top=pad_v, bottom=pad_v, left=110, right=95)
    set_cell_borders(
        cell,
        top=("single", 4, HEX_BORDER),
        bottom=("single", 4, HEX_BORDER),
        right=("single", 4, HEX_BORDER),
        left=("single", 20, HEX_NAVY),
    )
    set_table_fixed_widths(tbl, [PAGE_WIDTH_CM])

    for idx, (kind, txt) in enumerate(items):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0 if idx == 0 else (1.5 if compact else 2.5))
        p.paragraph_format.space_after = Pt((1.0 if compact else 1.8) if idx < len(items) - 1 else 0)
        p.paragraph_format.line_spacing = 1.16 if compact else 1.25
        if kind == "p":
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            add_rich_runs(p, txt, size_pt=9.0, color=TEXT_MAIN)
        elif kind == "indent":
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(0.45)
            add_rich_runs(p, txt, size_pt=9.0, color=TEXT_MAIN)
        elif kind == "eq":
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.left_indent = Cm(0.4)
            p.paragraph_format.right_indent = Cm(0.4)
            pPr = p._p.get_or_add_pPr()
            pPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="FFFFFF"/>'))
            pPr.append(parse_xml(
                f'<w:pBdr {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="4" w:space="3" w:color="DCE4EC"/>'
                f'<w:bottom w:val="single" w:sz="4" w:space="3" w:color="DCE4EC"/>'
                f'<w:left w:val="single" w:sz="4" w:space="5" w:color="DCE4EC"/>'
                f'<w:right w:val="single" w:sz="4" w:space="5" w:color="DCE4EC"/>'
                f'</w:pBdr>'
            ))
            add_rich_runs(p, txt, size_pt=9.0, color=NAVY_DARK)


def add_styled_table(doc: Document, headers: list, rows: list, col_widths_cm: list,
                     center_cols=(0, 2), bold_cols=(0, 1, 2), compact: bool = False):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, outer_hex=HEX_OUTER, inner_hex=HEX_BORDER, sz_outer="6", sz_inner="4")

    s = sum(col_widths_cm)
    if abs(s - PAGE_WIDTH_CM) > 0.01:
        col_widths_cm = [round(w * PAGE_WIDTH_CM / s, 3) for w in col_widths_cm]

    hdr_row = tbl.rows[0]
    set_row_header(hdr_row)
    set_row_cant_split(hdr_row)
    hpad = 38 if compact else 48
    for c_idx, htxt in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, HEX_NAVY)
        set_cell_margins(cell, top=hpad, bottom=hpad, left=62, right=62)
        set_cell_borders(
            cell,
            top=("single", 4, HEX_NAVY_BORDER),
            bottom=("single", 4, HEX_NAVY_BORDER),
            left=("single", 4, HEX_NAVY_BORDER),
            right=("single", 4, HEX_NAVY_BORDER),
        )
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in center_cols else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        set_run_font(p.add_run(htxt), size_pt=9.0, bold=True, color=WHITE, zh_font="黑体", en_font="Times New Roman")

    bpad = 26 if compact else 36
    bls = 1.12 if compact else 1.20
    for r_idx, row_vals in enumerate(rows):
        row = tbl.rows[1 + r_idx]
        set_row_cant_split(row)
        stripe = (r_idx % 2 == 1)
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            if stripe:
                set_cell_shading(cell, HEX_STRIPE)
            set_cell_margins(cell, top=bpad, bottom=bpad, left=62, right=62)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in center_cols else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = bls
            is_b = (c_idx in bold_cols)
            add_rich_runs(p, val, size_pt=9.0, base_bold=is_b, color=NAVY_DARK if is_b else TEXT_MAIN)

    set_table_fixed_widths(tbl, col_widths_cm)
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(1.2 if compact else 2.5)
    return tbl


def fit_image_dims_cm(img_path: Path, max_w_cm: float, max_h_cm: float) -> tuple:
    with Image.open(img_path) as im:
        w, h = im.size
    ratio = w / float(h)
    w_cm = max_w_cm
    h_cm = w_cm / ratio
    if h_cm > max_h_cm:
        h_cm = max_h_cm
        w_cm = h_cm * ratio
    return w_cm, h_cm


def add_figure_block(doc: Document, fig_spec: tuple):
    kind, k1, cap1, k2, cap2 = fig_spec
    if kind == "pair":
        tbl = doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, outer_hex=HEX_BORDER, inner_hex=HEX_BORDER, sz_outer="4", sz_inner="4")
        row = tbl.rows[0]
        set_row_cant_split(row)
        for idx, (k, cap) in enumerate(((k1, cap1), (k2, cap2))):
            cell = row.cells[idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
            p_img = cell.paragraphs[0]
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(0)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            w_cm, _ = fit_image_dims_cm(PAPER_IMGS[k], max_w_cm=8.1, max_h_cm=5.0)
            p_img.add_run().add_picture(str(PAPER_IMGS[k]), width=Cm(w_cm))

            p_cap = cell.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_cap.paragraph_format.space_before = Pt(0)
            p_cap.paragraph_format.space_after = Pt(0)
            p_cap.paragraph_format.line_spacing = 1.20
            add_rich_runs(p_cap, cap, size_pt=8.2, color=TEXT_MUTED)
        set_table_fixed_widths(tbl, [PAGE_WIDTH_CM / 2, PAGE_WIDTH_CM / 2])
    else:
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, outer_hex=HEX_BORDER, inner_hex=HEX_BORDER, sz_outer="4", sz_inner="4")
        row = tbl.rows[0]
        set_row_cant_split(row)
        cell = row.cells[0]
        set_cell_margins(cell, top=65, bottom=60, left=95, right=95)
        p_img = cell.paragraphs[0]
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.keep_with_next = True
        w_cm, _ = fit_image_dims_cm(PAPER_IMGS[k1], max_w_cm=13.5, max_h_cm=5.3)
        p_img.add_run().add_picture(str(PAPER_IMGS[k1]), width=Cm(w_cm))

        p_cap = cell.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(0)
        p_cap.paragraph_format.line_spacing = 1.20
        add_rich_runs(p_cap, cap1, size_pt=8.2, color=TEXT_MUTED)
        set_table_fixed_widths(tbl, [PAGE_WIDTH_CM])

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(3.5)


def add_toc_block(doc: Document, title: str = "目　录"):
    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_before = Pt(4)
    p_hdr.paragraph_format.space_after = Pt(4)
    p_hdr.paragraph_format.keep_with_next = True
    set_run_font(p_hdr.add_run(title), size_pt=10.8, bold=True, color=NAVY_DARK, zh_font="黑体", en_font="Times New Roman")
    add_p_bottom_border(p_hdr, color_hex=HEX_NAVY, sz="10")

    p_toc = doc.add_paragraph()
    p_toc.paragraph_format.space_before = Pt(2)
    p_toc.paragraph_format.space_after = Pt(2)
    add_field(p_toc, 'TOC \\o "1-2" \\h \\z \\u', size_pt=8.5, color=TEXT_MAIN)


def add_references_list(doc: Document, ref_ids: list):
    for local_no, rid in enumerate(ref_ids, 1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.2)
        p.paragraph_format.line_spacing = 1.22
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.first_line_indent = Cm(-0.75)
        set_run_font(p.add_run(f"[{local_no}]\t"), size_pt=9.0, bold=True, color=NAVY_DARK)
        add_rich_runs(p, MASTER_REFS[rid], size_pt=9.0, color=TEXT_MAIN)


def build_master_docx(subsystems: list, out_path: Path):
    doc = init_document("OV4 ASML NXT:1965Ci 套刻预算规格需求书（十二大子系统整机总册 v1）")
    master_map = {i: i for i in range(1, len(MASTER_REFS) + 1)}
    total_items = sum(sum(len(t[4]) for t in s["tables"]) for s in subsystems)
    dispatch_rows = build_dispatch_rows(subsystems)

    # Page 1: Cover + Pure SRS Scope Summary + 6-Group Overview
    meta_rows = [
        ("整机目标定位", "ASML TWINSCAN NXT:1965Ci（λ = 193.368 nm，NA = 1.35，β = 1/4）",
         "整机顶层目标", "DCO / SMO ≤ 2.50 nm；跨机匹配 MMO ≤ 4.50 nm（≥ 250 wph）"),
        ("覆盖范围与项数", f"全机 12 大子系统（共 {total_items} 项独立套刻验收指标，纯套刻专项口径）",
         "曝光狭缝口径", "26 × 5.5 mm 真实狭缝（v_{w} = 0.70 m/s，τ_{slit} = 7.857 ms）"),
        ("验收分级边界", "T1：单件/单台离线；T2：装机解算/同步/调控；T3：跨台整机联调",
         "编制日期与字体", "2026-11-27（整机完整版 Word 总册 v1 · 宋体小五 9 pt / Times New Roman 9 pt）"),
    ]
    add_cover_header(
        doc,
        "OV4-SRS-NXT1965Ci-FULL-MASTER-V1 · 整机全子系统工程规格需求总册（套刻专项完整版）",
        "ASML NXT:1965Ci 套刻预算规格需求书（总册）",
        "十二大子系统完整验收规格与 T1 / T2 / T3 多阶段模块–整机耦合验收标准",
        meta_rows,
    )
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(3)
    sp.paragraph_format.space_after = Pt(2)

    add_callout_box(doc, [
        ("p", "**总册使用说明与内容边界：**本总册供整机总体组统筹审阅与接口闭合核验，按 MECE 原则完整覆盖光刻机全部 12 大子系统（WS/WRS、RS、ENC、AA、TIS+PARIS、Lens、IH、WT-TC/WH、WC、RC/RH、IL/LS、MF/ENV），并配套拆分输出 12 份完全自包含的子系统独立下发 Word 分册（01 至 12）。"),
        ("p", "**内容边界原则：**本规格需求书严格作为工程验收契约文件，仅载明各子系统分级验收指标限值、标准测试定义、干/湿/在机工装边界、多阶段耦合要求及一手文献依据，不包含内部预算分配推导与整机误差合成计算过程。"),
    ], compact=True)

    sp2 = doc.add_paragraph()
    sp2.paragraph_format.space_before = Pt(3)
    sp2.paragraph_format.space_after = Pt(1)
    p_ovr = doc.add_paragraph()
    p_ovr.paragraph_format.space_before = Pt(2)
    p_ovr.paragraph_format.space_after = Pt(3)
    p_ovr.paragraph_format.keep_with_next = True
    set_run_font(p_ovr.add_run("十二大子系统架构分组与多阶段验收主线总览"), size_pt=9.6, bold=True, color=NAVY_DARK, zh_font="黑体", en_font="Times New Roman")
    add_p_bottom_border(p_ovr, color_hex=HEX_NAVY, sz="8")

    add_styled_table(
        doc,
        ["子系统分组", "涵盖子系统（全机 12 大模块）", "T1 / T2 / T3 验收边界主线"],
        [
            ("01–03 运动与位置测量", "WS 晶圆台（含 WRS/iHOPC）、RS 掩模台（4×）、ENC 光栅编码器", "T1-A/B（干态）→ T2-A/B（双台同步/Gridplate/Handover）"),
            ("04–05 对准与空间像传感", "AA 晶圆对准（M-side）、TIS + PARIS 空间像传感（E-side 湿区）", "AA：T1→T2→T3（M-to-E）；TIS+PARIS：E 侧实机湿区 T1"),
            ("06 投影光学与操纵器", "Lens 投影物镜（NA = 1.35，30 项奇像差 + 8 项动态 iHOPC）", "T1（局部静态 wet PMI）→ T2-A/B/C（LensModel 与 iHOPC）"),
            ("07–08 浸没液控与晶圆热控", "IH 浸没头与超纯水液控、WT-TC 晶圆台热控与 WH 传片预调温", "T1（离线液控/热控台架）→ T2（水膜/热瞬态）→ T3（批曝）"),
            ("09–10 晶圆与掩模夹持热控", "WC 晶圆夹持与 WT–MB 接口、RC/RH 掩模柔顺夹持、薄膜与 RHC", "T1（离线重夹/微滑移/气幕）→ T2（翘曲/RHC）→ T3（爬坡）"),
            ("11–12 光源照明与整机基盘", "IL/LS 193 nm 光源与 FlexRay 照明、MF/ENV 计量框架、隔振与微环境", "T1（离线光/隔振/环控）→ T2（波长-K3/MF 漂移）→ T3（24 h）"),
        ],
        [3.6, 7.6, 6.8],
        center_cols=(0,), bold_cols=(0,), compact=True,
    )

    # Page 2: Dedicated Live Word TOC
    doc.add_page_break()
    add_toc_block(doc, "目　录")

    # Chapter 0
    add_heading_1(doc, "第 0 章　总则：多阶段验收理念与模块-整机耦合边界", page_break_before=True)
    add_heading_2(doc, "0.1 整机设置 T1 / T2 / T3 多阶段验收的核心工程理念")
    add_callout_box(doc, [("p", t) for t in PHILOSOPHY_PARAS], compact=True)

    add_heading_2(doc, "0.2 T1 / T2 / T3 多阶段验收职责与耦合边界总表")
    add_styled_table(
        doc,
        ["验收阶段", "验收定位", "标准测试环境与工装边界", "拦截的耦合风险与整机放行意义"],
        MASTER_STAGE_SUMMARY,
        [2.1, 3.5, 5.4, 7.0],
        center_cols=(0,), bold_cols=(0, 1), compact=True,
    )

    add_heading_2(doc, "0.3 十二大子系统验收范围与配套独立分册清单")
    add_styled_table(
        doc,
        ["分册编号", "子系统名称", "验收层级与项数", "多阶段验收路径边界", "对应独立下发 Word 文件"],
        dispatch_rows,
        [1.8, 3.6, 3.2, 4.9, 4.5],
        center_cols=(0,), bold_cols=(0, 1), compact=True,
    )

    # Chapters 1..12
    for sub in subsystems:
        add_heading_1(doc, sub["ch_title"], page_break_before=True)
        for sec_no, sec_title, col2_hdr, col_w, rows in sub["tables"]:
            add_heading_2(doc, f"{sec_no} {sec_title}")
            add_styled_table(
                doc,
                ["序号", col2_hdr, "验收规格", "标准测试定义与工装条件"],
                rows, col_w,
                center_cols=(0, 2), bold_cols=(0, 1, 2),
            )
        note_no = f"{sub['ch_num']}.{len(sub['tables']) + 1}"
        note_hdr = f"{note_no} 技术注释、测试定义细则与文献图证" if sub["figures"] else f"{note_no} 技术注释与测试定义细则"
        add_heading_2(doc, note_hdr)
        resolved_notes = [(k, resolve_citations(t, master_map)) for k, t in sub["notes_master"]]
        add_callout_box(doc, resolved_notes)
        if sub["figures"]:
            sp3 = doc.add_paragraph()
            sp3.paragraph_format.space_before = Pt(0)
            sp3.paragraph_format.space_after = Pt(3.5)
            for kind, k1, c1, k2, c2 in sub["figures"]:
                rc1 = resolve_citations(c1, master_map)
                rc2 = resolve_citations(c2, master_map) if c2 else None
                add_figure_block(doc, (kind, k1, rc1, k2, rc2))

    # Chapter 13: All 33 References
    add_heading_1(doc, "第 13 章　参考文献", page_break_before=True)
    add_references_list(doc, list(range(1, len(MASTER_REFS) + 1)))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)


def build_standalone_subsystem_docx(sub: dict, out_path: Path):
    doc = init_document(f"OV4 ASML NXT:1965Ci {sub['short_name']} 套刻预算规格需求书 (v1)")

    all_text_for_refs = [t for _, t in sub["notes_standalone"]]
    for _, _, c1, _, c2 in sub["figures"]:
        all_text_for_refs.append(c1)
        if c2:
            all_text_for_refs.append(c2)
    local_ref_ids = collect_ref_ids(all_text_for_refs)
    local_map = {rid: idx for idx, rid in enumerate(local_ref_ids, 1)}
    total_items = sum(len(t[4]) for t in sub["tables"])

    # Page 1: Cover + Section 1 (Philosophy + Coupling Table — fits 100% cleanly on Page 1!)
    meta_rows = [
        ("发送对象", sub["recipient"],
         "整机顶层目标", "ASML NXT:1965Ci（193.368 nm，NA 1.35，DCO/SMO ≤ 2.50 nm，MMO ≤ 4.50 nm）"),
        ("本分册验收层级", sub["stage_scope"],
         "曝光狭缝口径", "26 × 5.5 mm 真实狭缝（v_{w} = 0.70 m/s，τ_{slit} = 7.857 ms）"),
        ("本分册指标数", f"共 {total_items} 项独立套刻验收指标（纯套刻专项口径）",
         "编制日期与字体", "2026-11-27（子系统独立下发版 v1 · 宋体小五 9 pt / Times New Roman 9 pt）"),
    ]
    add_cover_header(
        doc,
        f"{sub['doc_code']} · 子系统独立验收规格需求书（套刻专项 · 单独下发分册）",
        sub["standalone_title"],
        sub["standalone_subtitle"],
        meta_rows,
    )

    add_heading_1(doc, "1. 总则：多阶段验收理念与本子系统整机耦合边界", page_break_before=False)
    add_heading_2(doc, "1.1 整机设置 T1 / T2 / T3 多阶段验收的核心理念")
    add_callout_box(doc, [("p", t) for t in PHILOSOPHY_PARAS], compact=True)

    add_heading_2(doc, f"1.2 {sub['short_name']} 关键模块耦合与整机环境耦合边界清单")
    add_styled_table(
        doc,
        ["序号", "核心耦合机制", "为何离线合格不能替代多阶段/整机验收（对本子系统的具体要求）"],
        [(f"CP-{i:02d}", k, desc) for i, (k, desc) in enumerate(sub["coupling_rows"], 1)],
        [1.8, 5.2, 11.0],
        center_cols=(0,), bold_cols=(0, 1), compact=True,
    )

    # Page 2+: Section 2 Tiered Acceptance Tables
    add_heading_1(doc, f"2. {sub['short_name']} 分层验收指标要求", page_break_before=True)
    for idx, (_, sec_title, col2_hdr, col_w, rows) in enumerate(sub["tables"], 1):
        add_heading_2(doc, f"2.{idx} {sec_title}")
        add_styled_table(
            doc,
            ["序号", col2_hdr, "验收规格", "标准测试定义与工装条件"],
            rows, col_w,
            center_cols=(0, 2), bold_cols=(0, 1, 2),
        )

    # Section 3: Technical Notes & Figures
    sec3_title = "3. 技术注释、测试定义细则与实测文献图证" if sub["figures"] else "3. 技术注释与测试定义细则"
    add_heading_1(doc, sec3_title, page_break_before=False)
    resolved_notes = [(k, resolve_citations(t, local_map)) for k, t in sub["notes_standalone"]]
    add_callout_box(doc, resolved_notes)

    if sub["figures"]:
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(3.5)
        fig_counter = 1
        for kind, k1, c1, k2, c2 in sub["figures"]:
            rc1 = re.sub(r"^图\s*\d+-\d+：", f"图 3-{fig_counter}：", resolve_citations(c1, local_map))
            fig_counter += 1
            rc2 = None
            if c2:
                rc2 = re.sub(r"^图\s*\d+-\d+：", f"图 3-{fig_counter}：", resolve_citations(c2, local_map))
                fig_counter += 1
            add_figure_block(doc, (kind, k1, rc1, k2, rc2))

    # Section 4: Local Renumbered References
    add_heading_1(doc, "4. 参考文献", page_break_before=False)
    add_references_list(doc, local_ref_ids)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)


def update_and_verify_word_suite(docx_paths: list):
    import win32com.client

    VERIFY_PDF_DIR.mkdir(parents=True, exist_ok=True)
    if DOCX_PREV_DIR.exists():
        shutil.rmtree(DOCX_PREV_DIR)
    DOCX_PREV_DIR.mkdir(parents=True, exist_ok=True)

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    results = []
    try:
        for dp in docx_paths:
            abs_docx = str(dp.resolve())
            pdf_out = VERIFY_PDF_DIR / (dp.stem + ".pdf")
            if pdf_out.exists():
                pdf_out.unlink()

            wdoc = word.Documents.Open(abs_docx)
            try:
                wdoc.Fields.Update()
                for i in range(1, wdoc.TablesOfContents.Count + 1):
                    wdoc.TablesOfContents(i).Update()
                for s_idx in range(1, wdoc.Sections.Count + 1):
                    sec = wdoc.Sections(s_idx)
                    for hf_idx in (1, 2):
                        sec.Headers(hf_idx).Range.Fields.Update()
                        sec.Footers(hf_idx).Range.Fields.Update()
                wdoc.Save()
                wdoc.ExportAsFixedFormat(str(pdf_out.resolve()), 17)
            finally:
                wdoc.Close(False)

            with fitz.open(pdf_out) as pdoc:
                pages = len(pdoc)
                fonts = audit_pdf_quality(pdoc, dp.name, skip_first_pages=0)
                sub_prev = DOCX_PREV_DIR / dp.stem[:7]
                sub_prev.mkdir(parents=True, exist_ok=True)
                for pg in pdoc:
                    # Render pages 1, 2, 3 and last page for quick thorough visual inspection (all pages for small files)
                    if pages <= 6 or pg.number in (0, 1, 2, 3, pages - 1):
                        pg.get_pixmap(dpi=125).save(sub_prev / f"p{pg.number + 1:02d}.png")
                # Check Page 1 fit for all 12 standalone files: Page 2 content (after running header) must start with "2."
                if not dp.name.startswith("00_"):
                    p2_lines = [ln.strip() for ln in pdoc[1].get_text("text").splitlines() if ln.strip()]
                    p1_fit = any(ln.startswith("2.") for ln in p2_lines[:3])
                else:
                    p1_fit = True
                results.append((dp.name, pages, p1_fit, fonts))
    finally:
        word.Quit()
    return results


def main():
    for k, p in PAPER_IMGS.items():
        if not p.is_file():
            raise FileNotFoundError(f"Missing paper image {k}: {p}")

    subsystems = build_all_12_subsystems()
    print(f"Loaded {len(subsystems)} subsystems, {len(PAPER_IMGS)} paper figures, {len(MASTER_REFS)} references.")

    # Part A: Complete SRS PDF
    build_complete_srs_pdf(subsystems)

    # Part B: Master + 12 Standalone Word files
    OUT_DOCX_DIR.mkdir(parents=True, exist_ok=True)
    built_paths = []
    master_path = OUT_DOCX_DIR / "00_整机总册_ASML_NXT1965Ci套刻预算规格需求书_v1.docx"
    build_master_docx(subsystems, master_path)
    built_paths.append(master_path)

    for sub in subsystems:
        sp = OUT_DOCX_DIR / sub["filename"]
        build_standalone_subsystem_docx(sub, sp)
        built_paths.append(sp)

    results = update_and_verify_word_suite(built_paths)
    print("\n=== ALL 13 WORD DELIVERABLES GENERATED, UPDATED & AUDITED ===")
    for name, pages, p1_fit, fonts in results:
        sim = sum(v for k, v in fonts.items() if "SimSun" in k)
        tnr = sum(v for k, v in fonts.items() if "TimesNewRoman" in k)
        tag = "P1-FIT-OK" if p1_fit else "WARN-P1-SPILL!"
        print(f"  [{tag:10s}] {name:56s} | {pages:2d} pages | SimSun={sim:5d}, TNR={tnr:5d}")
        if not p1_fit:
            print(f"               WARNING: Page 1 spilled onto Page 2 in {name}!")


if __name__ == "__main__":
    main()
