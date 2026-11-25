"""Build 18-slide 16:9 executive technical PPTX for ASML TWINSCAN NXT:1965Ci
(SMO <= 2.50 nm, MMO <= 4.50 nm, FU <= 14.0 nm) Overlay L0-L3 Decomposition &
Subsystem Acceptance Specifications.

Strictly sourced from:
- OV4 v2 baseline: outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md
- OV4 primary literature ([003-266], [N1-N8], [S1-S14]) & ME3 manuals
- Overlay3 allowed survey ONLY: reports/md/143_scanner_overlay_control_survey.md
- Overlay3 primary literature: Ref146 Fig. 3 (INCOSE 2006), Ref009, Ref066, Ref165, Ref167, Ref168
- Public ASML NXT:1965Ci specifications

Run from repository root in PowerShell:
    $env:PYTHONPATH = "D:/Codex/cache/pdf-python;D:/Codex/cache/uv/archive-v0/D98sR3K3a9uncNLd"
    python -B outputs/code/build_nxt1965ci_pptx_v1.py
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

REPO = Path(__file__).resolve().parents[2]
OV4_MD = REPO / "参考文献-整理版-Markdown"
PPT_A = REPO / "work/nxt1965ci_ppt_assets"
OLD_A = REPO / "work/ppt_assets"
OUT_DIR = REPO / "outputs/presentations"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PPTX = OUT_DIR / "NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与子系统验收规格_v1.pptx"

# Color Palette (Clean White-Background Executive Lithography Style)
C_NAVY = RGBColor(0x12, 0x38, 0x49)
C_DARK = RGBColor(0x1B, 0x30, 0x3C)
C_TEAL = RGBColor(0x08, 0x78, 0x71)
C_MUTED = RGBColor(0x55, 0x6D, 0x78)
C_CORAL = RGBColor(0xC8, 0x4B, 0x00)
C_BLUE = RGBColor(0x1D, 0x5F, 0xA8)
C_OLIVE = RGBColor(0x5B, 0x7B, 0x1D)
C_PURPLE = RGBColor(0x5B, 0x4B, 0xB7)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_TBL_HDR = RGBColor(0xDC, 0xEA, 0xF2)
C_TBL_ALT = RGBColor(0xF6, 0xF9, 0xFB)
C_BOX_TEAL = RGBColor(0xF0, 0xF8, 0xF7)
C_BOX_WARM = RGBColor(0xFF, 0xF6, 0xEC)
C_BOX_BLUE = RGBColor(0xF1, 0xF5, 0xFA)
C_BORDER = RGBColor(0xC0, 0xD2, 0xD8)
C_SPEC = RGBColor(0x00, 0x3B, 0x8E)

FONT = "Microsoft YaHei"
TOTAL = 18

IMG = {
    "l0_l3":       REPO / "outputs/images/NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.png",
    "c_closure":   PPT_A / "chart_1965ci_closure_ref009.png",
    "c_delta":     PPT_A / "chart_1965ci_vs_v2_delta.png",
    "c_corr_slit": PPT_A / "chart_1965ci_corr_and_slit.png",
    "c_zern":      PPT_A / "chart_1965ci_zernike_z5_z64.png",
    "146_fig3":    REPO / "work/Overlay3_ref/literature/md/assets/146/mineru/images/page_8_image_0.jpg",
    "009_fig3":    OV4_MD / "assets/009_9e90b86e529c/images/page_2_chart_4.jpg",
    "009_fig4":    OV4_MD / "assets/009_9e90b86e529c/images/page_3_image_2.jpg",
    "009_fig10_r": OV4_MD / "assets/009_9e90b86e529c/images/page_6_chart_3.jpg",
    "015_fig10":   OV4_MD / "assets/015_9a19b5ebb43f/images/page_6_chart_1.jpg",
    "066_fig4":    OV4_MD / "assets/066_d108fef2e419/images/page_2_image_5.jpg",
    "066_fig5":    OV4_MD / "assets/066_d108fef2e419/images/page_3_image_1.jpg",
    "066_fig6":    OV4_MD / "assets/066_d108fef2e419/images/page_4_image_3.jpg",
    "066_fig9":    OV4_MD / "assets/066_d108fef2e419/images/page_5_chart_7.jpg",
    "066_fig10a":  OV4_MD / "assets/066_d108fef2e419/images/page_6_chart_2.jpg",
    "017_fig7":    OV4_MD / "assets/017_8936fe20711b/images/page_3_chart_2.jpg",
    "021_fig12":   OV4_MD / "assets/021_d3ddae439a1d/images/page_8_chart_7.jpg",
    "022_fig1":    OV4_MD / "assets/022_1aa75fc49631/images/page_1_image_23.jpg",
    "024_fig11":   OV4_MD / "assets/024_e25f1b752cb5/images/page_9_chart_3.jpg",
    "075_fig13":   OV4_MD / "assets/075_97d74e7b9094/images/page_9_chart_2.jpg",
    "098_fig15":   OV4_MD / "assets/098_76219de6435f/images/page_13_image_0.jpg",
    "100_fig9":    OV4_MD / "assets/100_cb2cee4b24c6/images/page_6_image_7.jpg",
    "123_fig14":   OV4_MD / "assets/123_67b8041faadd/images/page_8_chart_0.jpg",
    "147_fig6":    OV4_MD / "assets/147_66d774abc526/images/page_4_image_4.jpg",
    "253_fig8":    OV4_MD / "assets/253_d054bfdabe17/images/page_7_chart_1.jpg",
    "008_fig4b":   OV4_MD / "assets/008_8d2163e59192/images/page_4_chart_2.jpg",
    "154_crop":    OLD_A / "154_p7_eq1_table1_crop.png",
    "c_lens8":     PPT_A / "chart_1965ci_lens_8dim.png",
}
for k, p in IMG.items():
    assert p.exists(), f"Missing asset {k}: {p}"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.500)
BLANK = prs.slide_layouts[6]


def set_bg(slide, color=C_WHITE):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def set_cell_border(cell, color="B8CAD0", width="6350"):
    tcPr = cell._tc.get_or_add_tcPr()
    for edge in ("lnL", "lnR", "lnT", "lnB"):
        for old in tcPr.findall(f"{{http://schemas.openxmlformats.org/drawingml/2006/main}}{edge}"):
            tcPr.remove(old)
        ln = parse_xml(
            f'<a:{edge} {nsdecls("a")} w="{width}" cap="flat" cmpd="sng" algn="ctr">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:{edge}>'
        )
        tcPr.append(ln)


def add_header(slide, badge, title, pno, subtitle=None):
    set_bg(slide, C_WHITE)
    b1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    b1.fill.solid(); b1.fill.fore_color.rgb = C_NAVY; b1.line.fill.background()
    b2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(3.2), Inches(0.08))
    b2.fill.solid(); b2.fill.fore_color.rgb = C_TEAL; b2.line.fill.background()

    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), Inches(0.18), Inches(1.60), Inches(0.34))
    pill.fill.solid(); pill.fill.fore_color.rgb = C_TEAL; pill.line.fill.background()
    tf = pill.text_frame; tf.margin_left = tf.margin_right = Inches(0.04); tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = badge; r.font.name = FONT; r.font.size = Pt(9.2); r.font.bold = True; r.font.color.rgb = C_WHITE

    tb = slide.shapes.add_textbox(Inches(2.05), Inches(0.13), Inches(10.92), Inches(0.44))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = title; r.font.name = FONT; r.font.size = Pt(17.0); r.font.bold = True; r.font.color.rgb = C_NAVY

    line_y = 0.62
    if subtitle:
        stb = slide.shapes.add_textbox(Inches(0.35), Inches(0.56), Inches(12.63), Inches(0.24))
        stf = stb.text_frame; stf.word_wrap = True; stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0
        sp = stf.paragraphs[0]
        sr = sp.add_run(); sr.text = subtitle; sr.font.name = FONT; sr.font.size = Pt(8.6); sr.font.color.rgb = C_MUTED
        line_y = 0.82

    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(line_y), Inches(12.63), Inches(0.02))
    div.fill.solid(); div.fill.fore_color.rgb = C_TEAL; div.line.fill.background()

    # Footer
    fdiv = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(7.14), Inches(12.63), Inches(0.012))
    fdiv.fill.solid(); fdiv.fill.fore_color.rgb = C_BORDER; fdiv.line.fill.background()

    ft1 = slide.shapes.add_textbox(Inches(0.35), Inches(7.18), Inches(10.5), Inches(0.24))
    ftf1 = ft1.text_frame; ftf1.margin_left = ftf1.margin_top = 0
    r1 = ftf1.paragraphs[0].add_run()
    r1.text = "OV4 · ASML TWINSCAN NXT:1965Ci（SMO ≤ 2.50 / MMO ≤ 4.50 nm）L0–L3 套刻拆解与子系统验收规格 v1 · OpticsPan/OV4"
    r1.font.name = FONT; r1.font.size = Pt(7.8); r1.font.color.rgb = C_MUTED

    ft2 = slide.shapes.add_textbox(Inches(11.4), Inches(7.18), Inches(1.58), Inches(0.24))
    ftf2 = ft2.text_frame; ftf2.margin_right = ftf2.margin_top = 0
    fp2 = ftf2.paragraphs[0]; fp2.alignment = PP_ALIGN.RIGHT
    r2 = fp2.add_run(); r2.text = f"{pno:02d} / {TOTAL:02d}"
    r2.font.name = FONT; r2.font.size = Pt(8.5); r2.font.bold = True; r2.font.color.rgb = C_NAVY


def add_box(slide, x, y, w, h, title, bullets, bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.8, body_sz=8.4):
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    rect.fill.solid(); rect.fill.fore_color.rgb = bg
    rect.line.color.rgb = C_BORDER; rect.line.width = Pt(0.6)
    rect.shadow.inherit = False
    st = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.055), Inches(h))
    st.fill.solid(); st.fill.fore_color.rgb = accent; st.line.fill.background(); st.shadow.inherit = False

    tb = slide.shapes.add_textbox(Inches(x + 0.12), Inches(y + 0.05), Inches(w - 0.17), Inches(h - 0.08))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p0 = tf.paragraphs[0]; p0.space_after = Pt(2.2)
    r0 = p0.add_run(); r0.text = title
    r0.font.name = FONT; r0.font.size = Pt(title_sz); r0.font.bold = True; r0.font.color.rgb = C_NAVY
    for b in bullets:
        p = tf.add_paragraph(); p.space_after = Pt(1.8)
        if isinstance(b, tuple):
            r1 = p.add_run(); r1.text = "• " + b[0]
            r1.font.name = FONT; r1.font.size = Pt(body_sz); r1.font.bold = True; r1.font.color.rgb = C_DARK
            r2 = p.add_run(); r2.text = b[1]
            r2.font.name = FONT; r2.font.size = Pt(body_sz); r2.font.color.rgb = C_DARK
        else:
            r = p.add_run(); r.text = "• " + b
            r.font.name = FONT; r.font.size = Pt(body_sz); r.font.color.rgb = C_DARK


def add_img_box(slide, key, x, y, w, h, caption=None, border=True):
    p = IMG[key]
    cap_h = 0.24 if caption else 0.0
    box_h = h - cap_h
    if border:
        fr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(box_h))
        fr.fill.solid(); fr.fill.fore_color.rgb = C_WHITE
        fr.line.color.rgb = C_BORDER; fr.line.width = Pt(0.6)
        fr.shadow.inherit = False
    im = Image.open(p)
    iw, ih = im.size
    ar = iw / ih
    pad = 0.04
    aw, ah = w - 2 * pad, box_h - 2 * pad
    if aw / ah > ar:
        dh = ah; dw = ah * ar
    else:
        dw = aw; dh = aw / ar
    px = x + (w - dw) / 2.0
    py = y + (box_h - dh) / 2.0
    slide.shapes.add_picture(str(p), Inches(px), Inches(py), Inches(dw), Inches(dh))
    if caption:
        ctb = slide.shapes.add_textbox(Inches(x), Inches(y + box_h + 0.01), Inches(w), Inches(cap_h))
        ctf = ctb.text_frame; ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = ctf.margin_top = ctf.margin_bottom = 0
        cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
        cr = cp.add_run(); cr.text = caption
        cr.font.name = FONT; cr.font.size = Pt(7.5); cr.font.color.rgb = C_MUTED


def add_table(slide, x, y, w, h, headers, rows, col_widths=None, font_sz=8.0, hdr_sz=8.2, bold_cols=None, spec_cols=None):
    bold_cols = set(bold_cols or [])
    spec_cols = set(spec_cols or [])
    nrows, ncols = len(rows) + 1, len(headers)
    tbl_shape = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = tbl_shape.table
    if col_widths:
        s = sum(col_widths)
        for j, cw in enumerate(col_widths):
            tbl.columns[j].width = Inches(w * cw / s)
    # Header
    for j, htxt in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid(); cell.fill.fore_color.rgb = C_NAVY
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.04)
        cell.margin_top = cell.margin_bottom = Inches(0.02)
        set_cell_border(cell, "123849", "6350")
        p = cell.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = htxt
        r.font.name = FONT; r.font.size = Pt(hdr_sz); r.font.bold = True; r.font.color.rgb = C_WHITE
    # Data rows
    for i, row in enumerate(rows):
        is_tot = (i == len(rows) - 1 and any(k in str(row[0]) for k in ("合计", "汇总", "闭环", "总计", "MMO", "SMO")))
        bg = C_TBL_HDR if is_tot else (C_TBL_ALT if i % 2 == 1 else C_WHITE)
        for j, val in enumerate(row):
            cell = tbl.cell(i + 1, j)
            cell.fill.solid(); cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = cell.margin_right = Inches(0.04)
            cell.margin_top = cell.margin_bottom = Inches(0.015)
            set_cell_border(cell, "C0D2D8", "5080")
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == len(headers) - 1 or j == 0 else PP_ALIGN.CENTER
            r = p.add_run(); r.text = str(val)
            r.font.name = FONT; r.font.size = Pt(font_sz)
            r.font.bold = is_tot or (j in bold_cols) or (j in spec_cols)
            r.font.color.rgb = C_SPEC if (j in spec_cols and not is_tot) else (C_NAVY if is_tot else C_DARK)
    return tbl


# =============================================================================
# SLIDE 01 — COVER
# =============================================================================
s = prs.slides.add_slide(BLANK)
set_bg(s, C_WHITE)
# Left deep navy architectural accent band
band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.45), Inches(7.50))
band.fill.solid(); band.fill.fore_color.rgb = C_NAVY; band.line.fill.background()
band2 = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), Inches(0), Inches(0.10), Inches(7.50))
band2.fill.solid(); band2.fill.fore_color.rgb = C_TEAL; band2.line.fill.background()

# Top tag pill
tag = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.95), Inches(0.65), Inches(5.30), Inches(0.38))
tag.fill.solid(); tag.fill.fore_color.rgb = C_BOX_TEAL; tag.line.color.rgb = C_TEAL; tag.line.width = Pt(1.0)
tf = tag.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "OV4 先进光刻机套刻工程体系  |  目标机型正式锚定版 v1"
r.font.name = FONT; r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = C_TEAL

# Main title
tb = s.shapes.add_textbox(Inches(0.95), Inches(1.25), Inches(11.8), Inches(1.45))
tf = tb.text_frame; tf.word_wrap = True
p1 = tf.paragraphs[0]
r1 = p1.add_run(); r1.text = "ASML TWINSCAN NXT:1965Ci\n"
r1.font.name = FONT; r1.font.size = Pt(34); r1.font.bold = True; r1.font.color.rgb = C_NAVY
r2 = p1.add_run(); r2.text = "套刻指标 L0–L3 全链路拆解与核心子系统验收规格"
r2.font.name = FONT; r2.font.size = Pt(25); r2.font.bold = True; r2.font.color.rgb = C_TEAL

# Subtitle
stb = s.shapes.add_textbox(Inches(0.95), Inches(2.85), Inches(11.7), Inches(0.75))
stf = stb.text_frame; stf.word_wrap = True
sp = stf.paragraphs[0]
sr = sp.add_run()
sr.text = (
    "基于 Ref009 Fig. 3 预算占比与 Ref-146 Fig. 3 左→右拆解语法  |  融合 Overlay3 报告 143 与一手文献\n"
    "覆盖 26×5.5 mm 真实狭缝、WS=Master 同步核定、18 项 L3 原生指标与九大核心子系统（+6 辅助域）完整闭环"
)
sr.font.name = FONT; sr.font.size = Pt(11.5); sr.font.color.rgb = C_MUTED

# 4 Executive KPI Cards
kpis = [
    ("单机套刻 SMO 红线", "≤ 2.50 nm", "双卡盘闭环 2.36 nm (裕度 5.4%)\n同卡盘 DCO 2.26 nm (裕度 9.7%)", C_TEAL),
    ("混机套刻 MMO 红线", "≤ 4.50 nm", "跨机闭环 4.29 nm (裕度 4.6%)\n含 BMMO / 无K20静NCE / 50μm翘曲", C_NAVY),
    ("全片焦面均匀性 FU", "≤ 14.0 nm", "焦面闭环 11.48 nm (裕度 18.0%)\n轻量化陶瓷 WS + 6.5 nm WT", C_BLUE),
    ("光学与产能基准", "1.35 NA · 250 wph", "193.368 nm / 真实狭缝 26×5.5 mm\n38 nm 偶极 · 6 kHz · 7 点 PARIS", C_CORAL),
]
for idx, (k_t, k_v, k_sub, k_col) in enumerate(kpis):
    kx = 0.95 + idx * 3.00
    card = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(kx), Inches(3.90), Inches(2.82), Inches(1.65))
    card.fill.solid(); card.fill.fore_color.rgb = C_TBL_ALT
    card.line.color.rgb = k_col; card.line.width = Pt(1.2); card.shadow.inherit = False
    topb = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(kx), Inches(3.90), Inches(2.82), Inches(0.08))
    topb.fill.solid(); topb.fill.fore_color.rgb = k_col; topb.line.fill.background(); topb.shadow.inherit = False
    ctb = s.shapes.add_textbox(Inches(kx + 0.14), Inches(4.06), Inches(2.58), Inches(1.42))
    ctf = ctb.text_frame; ctf.word_wrap = True
    p_a = ctf.paragraphs[0]
    ra = p_a.add_run(); ra.text = k_t; ra.font.name = FONT; ra.font.size = Pt(9.5); ra.font.bold = True; ra.font.color.rgb = C_MUTED
    p_b = ctf.add_paragraph(); p_b.space_before = Pt(5); p_b.space_after = Pt(5)
    rb = p_b.add_run(); rb.text = k_v; rb.font.name = FONT; rb.font.size = Pt(17.5); rb.font.bold = True; rb.font.color.rgb = k_col
    p_c = ctf.add_paragraph()
    rc = p_c.add_run(); rc.text = k_sub; rc.font.name = FONT; rc.font.size = Pt(8.2); rc.font.color.rgb = C_DARK

# Bottom Lineage Bar
lin = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.95), Inches(5.90), Inches(11.82), Inches(1.05))
lin.fill.solid(); lin.fill.fore_color.rgb = C_BOX_BLUE; lin.line.color.rgb = C_BORDER; lin.line.width = Pt(0.8)
ltb = s.shapes.add_textbox(Inches(1.12), Inches(6.00), Inches(11.50), Inches(0.88))
ltf = ltb.text_frame; ltf.word_wrap = True
lp = ltf.paragraphs[0]
lr1 = lp.add_run(); lr1.text = "严格溯源声明与配套交付（2026-11-25）：\n"
lr1.font.name = FONT; lr1.font.size = Pt(9.5); lr1.font.bold = True; lr1.font.color.rgb = C_NAVY
lr2 = lp.add_run()
lr2.text = (
    "• 演进起点：OV4《九大核心子系统验收指标推导与计算说明书 v2》+ 265 份本机一手文献/专利 + ME3 官方培训手册；\n"
    "• 新增权威输入：仅限 @github/Overlay3 报告 143（143_scanner_overlay_control_survey.md）及原始一手文献（Ref146 / Ref009 / Ref066 / Ref165 / 167 / 168）+ ASML 公开规格；\n"
    "• 同步交付：完整 Markdown 报告 + 可编辑 draw.io 源图 + 180 DPI 全景 PNG + 单一事实源 Python 校验脚本（OpticsPan/OV4）。"
)
lr2.font.name = FONT; lr2.font.size = Pt(8.5); lr2.font.color.rgb = C_DARK


# =============================================================================
# SLIDE 02 — TARGET RE-ANCHORING & SUBSYSTEM DELTA VS V2
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "01 整机定位", "目标重锚定：ASML NXT:1965Ci 参数对标与相对历史 v2 基线科学回松", 2,
           "相比历史 v2（2.00/3.50 nm 中间档），锚定 NXT:1965Ci（SMO 2.50 / MMO 4.50 nm）使九大核心子系统直对 Ref009/066 实测、消除 8%–19% 过设计")

add_table(s, 0.35, 0.94, 12.63, 2.15,
          ["性能维度", "NXT:1950i [009]", "本目标：NXT:1965Ci", "历史 v2 基线", "NXT:1970Ci/1980Di", "工程核定说明"],
          [
              ["单机套刻 SMO / DCO", "DCO ≤ 2.50 nm", "SMO ≤ 2.50 (闭环 2.36)", "DCO ≤ 2.00 (1.87)", "≤ 1.4–1.8 nm", "全片覆盖；同卡盘 DCO 闭环 2.26 nm，显式拆出双卡盘 ΔC2C 0.48 nm"],
              ["混机套刻 MMO", "≤ 4.5–5.5 nm", "MMO ≤ 4.50 (闭环 4.29)", "MMO ≤ 3.50 (3.15)", "≤ 2.5–3.4 nm", "对标 BMMO 全片 3.4 nm [066 Fig.4] 与 5 机 3.0–3.8 nm [N7]"],
              ["焦面均匀性 FU (3σ)", "≤ 15–20 nm", "≤ 14.0 (闭环 11.48)", "≤ 12.0 (10.31)", "≤ 9.1–12.0 nm", "陶瓷轻量化短行程 WS（MAz 峰 4 nm [066 Fig.9]）+ 6.5 nm WT"],
              ["光学 / 狭缝 / 产能", "1.35 NA / 175–200 wph", "1.35 NA · 26×5.5 mm · ≥250 wph", "220–230 wph", "250–275 wph", "38 nm 偶极 / 40 nm C-quad；6 kHz；核算扫速 0.70 m/s（附 0.75/0.80 外推）"],
              ["关键计量与补偿", "Gridplate+SMASH+TIS", "Gridplate+SMASH+7点PARIS+FlexWave+RHC+19参iHOPC", "同左", "+RHC2+ORION+UV-LS", "同步主从核定为 WS=Master、RS=Slave（修正旧 v2 表述）"],
          ],
          col_widths=[1.7, 1.5, 2.3, 1.5, 1.6, 4.0], font_sz=7.6, hdr_sz=8.0, bold_cols=[0], spec_cols=[2])

add_img_box(s, "c_delta", 0.35, 3.22, 8.65, 3.82,
            "图 2-1  目标锚定至 NXT:1965Ci 后九大核心子系统关键验收规格对比（由过紧的 1970Ci 级回松 +8%~+19%，精准落入 1950i/1965Ci 实测窗）")

add_box(s, 9.15, 3.22, 3.83, 3.82, "核心决策：为何新建报告与新 PPT？", [
    ("顶层红线根本变化：", "由 2.00/3.50 nm 改为明确商规 NXT:1965Ci（SMO 2.50 / MMO 4.50 nm），并严格锚定 Ref009 Fig. 3 占比。"),
    ("消除 8%–19% 过设计：", "WS-X (0.32→0.38)、Sync MA (0.40→0.47)、ENC 宽带 (0.20→0.22)、PARIS RA (0.40→0.47) 均直对 Ref009/066 一手实测。"),
    ("统一口径与纠偏：", "旧 v2 PPTX 残留 8.0 mm 旧狭缝与主从方向旧表述，本次全新 18 页 PPTX 全面统一至 5.5 mm 狭缝与 WS=Master。"),
    ("历史完整保留：", "原 v2 说明书/PPTX 依 UP-008 完整保留；错误指令 v1 产物已归档冻结不再作为后续参考。"),
], bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.6, body_sz=8.2)


# =============================================================================
# SLIDE 03 — METHODOLOGY: REF146 + OVERLAY3 REPORT 143 UPGRADES
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "02 方法论升级", "方法论跃升：融合 Ref-146 预算架构与 Overlay3 报告 143 六大工程机理", 3,
           "左图承袭 Ref-146 Fig. 3 原版左→右树状拆解 + 共享物理源虚线语法；右列吸收报告 143 揭示的 6 条易漏跨支路误差耦合机制")

add_img_box(s, "146_fig3", 0.35, 0.96, 6.45, 3.85,
            "原件基准：Ref-146 Fig. 3 (Freriks et al., INCOSE 2006, p. 8) — Wafer-stepper overlay budget")

add_box(s, 0.35, 4.92, 6.45, 2.12, "Ref-146 预算设计 4 项黄金法则（本次全量落地）", [
    ("左→右逐级分解：", "Matched Machine → Single Machine + Matching → 功能域 → 执行动作 → 原生非套刻量纲（如原图最右列 phi 75 nrad）。"),
    ("三类合成规则（§3.3）：", "独立随机项走 RSS（原图 4²+4²+2²=6²）；系统偏置走线性叠加（原图 7+5=12）；共享源走相干/相关校验。"),
    ("共享源防重复计数：", "用灰/虚线将 interferometer / frame stability 跨支路连至多条父链，直面相关性（§2.4）。"),
    ("半静态工况预算（§4.5）：", "不把预算做成失控动态黑箱，而是冻结 4 套固定配方 (p, P) 工况分别闭环。"),
], bg=C_BOX_BLUE, accent=C_NAVY, title_sz=9.4, body_sz=8.0)

add_box(s, 6.98, 0.96, 6.00, 6.08, "从 Overlay3 报告 143 吸收的 6 项硬核物理升级", [
    ("1. 掩模 Pellicle 装配 + 扫描动态路径（143 §2.1, Ref098/104/106）：", "除 RT 重夹与 150 m/s² 滑移外，NXT:1970Ci 实测装膜扫描吹扫可引入 0.30–0.40 nm 高阶动态残差；本次在 S5 显式拆分 Pellicle 动态项 0.14 nm 并引入软热熔胶垫控制。"),
    ("2. 双卡盘 SYCO/LOCO 计量参考偏置（143 §4.6, Ref100 Fig. 9）：", "SYCO 固定卡盘 1、LOCO 随批首片卡盘，换卡盘诱发 K7/K12/K13 零点偏置；双卡盘 ΔC2C（S7）须同步管控机械夹持与计量零点匹配。"),
    ("3. 浸没 UPW 流量 → TIS 测位隐藏耦合（143 §4.2.1, Ref164）：", "供水流量不仅改水膜 n(T) 与残液冷缩，还直接调制 TIS X/Y/Z 重复性；全景图显式增绘 x11 → f4 跨支路共享虚线。"),
    ("4. SUSD 正反扫三处机械接口与 WT–MB 长柱（143 §5.3, US8269949B2）：", "沿图案到计量块（MB）传力链增设 WT–MB 柔顺长柱微滞回（0.15 nm 入 S6）与掩模分段叶簧夹持（JP5809458B2）。"),
    ("5. 方向采样混叠进 HOWA 跨层累积（143 §6.3, Ref123 Fig. 10–14）：", "不平衡扫向采样会把 SUSD 误差混叠为 Gy20 > 3.5 nm 并逐层放大；AA 验收强制增加正反扫与步进配平采样。"),
    ("6. 靶标-器件残差边界与四层验收金字塔（143 §1.2 & §7.2, Ref008）：", "器件与靶标残差需 < 0.5 nm；建立部件→子系统→参考片(DCO/SMO/MMO)→产品片(ADI/AEI)四层验证链。"),
], bg=C_BOX_WARM, accent=C_CORAL, title_sz=9.8, body_sz=8.2)


# =============================================================================
# SLIDE 04 — FULL-WIDTH L0 -> L1 -> L2 -> L3 PANORAMA DIAGRAM
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "03 全景拆解图", "NXT:1965Ci 套刻指标 L0 → L1 → L2 → L3 全链路拆解图（Ref-146 Fig. 3 风格）", 4,
           "左→右：预算自顶向下拆解（MMO 4.50 / SMO 2.50 → 六大域 → 14 项执行层 → 18 项原生 L3） | 右→左：物理误差上溯传递（橙/青虚线=共享源）")

add_img_box(s, "l0_l3", 0.30, 0.88, 12.73, 5.88, None, border=True)

# Compact bottom callout strip
strip = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.30), Inches(6.80), Inches(12.73), Inches(0.30))
strip.fill.solid(); strip.fill.fore_color.rgb = C_BOX_TEAL; strip.line.color.rgb = C_TEAL; strip.line.width = Pt(0.6)
stb = s.shapes.add_textbox(Inches(0.42), Inches(6.82), Inches(12.50), Inches(0.25))
stf = stb.text_frame; stf.vertical_anchor = MSO_ANCHOR.MIDDLE
sr = stf.paragraphs[0].add_run()
sr.text = "可编辑源文件：outputs/images/NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.drawio   |   单一事实源校验脚本：build_nxt1965ci_budget_and_diagram_v1.py"
sr.font.name = FONT; sr.font.size = Pt(8.2); sr.font.bold = True; sr.font.color.rgb = C_NAVY


# =============================================================================
# SLIDE 05 — REF009 FIG. 3 CALIBRATION & DUAL-AXIS CLOSURE
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "04 闭环总账", "Ref009 Fig. 3 精确像素核定与 SMO 2.50 / MMO 4.50 nm 双轴闭环", 5,
           "通过方差份额投影 w_k = R_k² / ΣR_m² 将 Ref009 堆叠柱统一至物理两层 RSS，六大核心域占比偏差全部控制在 ±0.30% 以内")

add_img_box(s, "009_fig3", 0.35, 0.94, 5.75, 2.85,
            "原图：Ref009 Fig. 3 (ASML SPIE 7640) — 77.80 px/nm 像素标定 NXT:1950i 2.50 nm 六大域")

add_img_box(s, "c_closure", 6.25, 0.94, 6.73, 2.85,
            "图 5-1  六域方差占比对齐验证（左）与 DCO 2.26 / SMO 2.36 / MMO 4.29 nm 闭环（右）")

add_table(s, 0.35, 3.88, 12.63, 3.16,
          ["L1 节点", "Ref009 像素读数 (占比)", "NXT:1965Ci 两层 X / Y (nm)", "模型方差占比 (偏差)", "主要 L2 组成与顶层闭环说明"],
          [
              ["S1 运动台定位与同步", "0.501 nm (20.16%)", "0.744 / 0.867", "20.24% (+0.08%)", "f1 Sync MA (X 0.671 / Y 0.760) + f2 WS-iHOPC (X 0.323 / Y 0.416)"],
              ["S2 晶圆与掩模对准",   "0.636 nm (25.58%)", "0.970 / 0.970", "25.38% (−0.20%)", "f3 M-side AA 网格+基线 (0.707) + f4 E-side TIS/PARIS RA (0.665)"],
              ["S3 光学柱与动态像差", "0.302 nm (12.14%)", "0.667 / 0.557", "11.99% (−0.15%)", "f5 Lens-iHOPC (X 0.450 / Y 0.260) + f6 Odd Zernike (0.437) + 热声阻尼 (0.226)"],
              ["S4 晶圆热与浸没流场", "0.411 nm (16.54%)", "0.784 / 0.784", "16.58% (+0.04%)", "f7 晶圆实体热/蒸发+WH (0.677) + f8 浸没水膜 n(T) 与流场 (0.396)"],
              ["S5 掩模夹持与热变形", "0.431 nm (17.31%)", "0.809 / 0.809", "17.61% (+0.30%)", "f9 RHC 残差+气隙 (0.696) + f10 重夹/150m/s²微滑移/Pellicle动态 (0.411)"],
              ["S6 晶圆夹持与接口",   "0.206 nm (8.27%)",  "0.552 / 0.552", "8.21% (−0.06%)",  "f11 WT 吸片重复 (0.30) + 滑移 (0.20) + WT–MB 柔顺长柱微滞回 (0.15) × √2"],
              ["S7 ΔC2C + 验证底噪",  "双台新增 / 同台仅底噪", "0.588 / 0.588 (同台 0.340)", "双台外加项", "双卡盘 ΔC2C (SYCO/LOCO + TIS1/2 + WT1/2 = 0.48) + 量测 TMU 0.34 nm"],
              ["顶层 SMO / DCO / MMO 闭环", "Ref009 六域 RSS = 1.926", "SMO: X 2.32 / Y 2.33 (包络 2.36)", "MMO: 4.29 ≤ 4.50", "同卡盘 DCO = 2.26 ≤ 2.50 (裕度 9.7%) | 双台 SMO 裕度 5.4% | MMO 裕度 4.6%"],
          ],
          col_widths=[1.85, 1.85, 2.05, 1.65, 5.23], font_sz=7.4, hdr_sz=7.8, bold_cols=[0], spec_cols=[2])


# =============================================================================
# SLIDE 06 — 4-LAYER ERROR PROPAGATION EVALUATION & STRESS TEST
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "05 传递建模", "四层误差传递思路（x → f(x;p) → F(f,x;P) → L0）评价、工程补强与压力校验", 6,
           "完全认可“先理清底层原生指标上溯拓扑比写出解析闭式更核心”；叠加 4 项工程补强后即可直接转化为子系统 FAT 验收模型")

add_box(s, 0.35, 0.94, 12.63, 1.05, "四层误差传递数学表达与核心价值确认", [
    ("完整上溯链：", "L3 原生非套刻物理量 x = (x01..x18)  →  L2 中间执行层 y_j = f_j(x; p_j)  →  L1 功能域 z_k = F_k(f, x; P_k)  →  两遍差分 Δz = z_2 − z_1  →  L0 = |Mean|_线性 + RSS(3σ_k)。"),
    ("四大工程优势：", "① 强制分离 FAT 原生量纲（mK/nrad/ppm/nm RMS）与套刻 nm；② 显露配方杠杆 p/P（扫速/狭缝/标记数/照明切换）；③ 允许 F 含直连快捷边 x_i；④ 拓扑先于闭式，支撑跨部门并行开发。"),
], bg=C_BOX_BLUE, accent=C_NAVY, title_sz=9.4, body_sz=8.2)

add_table(s, 0.35, 2.08, 12.63, 1.92,
          ["工程补强机制", "若停留在概念框图的风险", "NXT:1965Ci 落地数学与验收方法"],
          [
              ["1. 两遍曝光差分算子", "混淆同机共模抵消与两遍 √2 随机放大", "引入两遍相关系数 ρ_12：σ_Δ² = σ₁² + σ₂² − 2ρ_12·σ₁σ₂（独立 √2；共模 0；反相热漂 >√2）"],
              ["2. 黑箱 f/F 三阶代理", "写不出闭式便陷入“画完图分不出数字”", "① 局部雅可比 Δq ≈ J(p₀)Δx [143 Eq.3]；② 阶跃实验斜率 ΔOVL/Δx [017/164]；③ 狭缝/热卷积 [N8]"],
              ["3. 共享源相干+相关压测", "同源跨支路误做独立 RSS 导致严重低估", "同像点同源先代数合并 (a+b)x_i；域间做 ρ 压测：SMO(ρ) = |Mean| + √[(1−ρ)ΣR² + ρ(ΣR)²]"],
              ["4. 半静态工况冻结", "单一模型涵盖全工艺沦为难维护仿真器", "按 Ref146 §4.5 冻结 4 套工况：冷机 DCO / 标准双台 SMO / 高剂量跨照明热态 / 跨机 MMO"],
          ],
          col_widths=[2.0, 3.0, 7.63], font_sz=7.6, hdr_sz=8.0, bold_cols=[0])

add_img_box(s, "c_corr_slit", 0.35, 4.10, 12.63, 2.95,
            "图 6-1  左：Ref146 §2.4 域间相关性压测（ρ=0.025 触 2.50 红线，ρ=0.05 达 2.63 超标，强制共享源隔离 ρ<0.025）；右：NA=1.35 真实 5.5 mm 狭缝 MA/MSD 互补滤波 [N1/N8]")


# =============================================================================
# SLIDE 07 — WS & RS 6-DOF SPECS & SYNC CLOSURE
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "06 WS / RS", "L1-S1（一）：WS / RS 6-DOF 验收规格、液浸光学耦合矩阵与 Sync MA 闭环", 7,
           "直对 Ref009 Fig. 10 实测（Sync MA-X 0.47 / MA-Y 0.49 nm）与 Ref066 Fig. 9 陶瓷 WS（MAz 峰 4 nm），严格执行液浸 6-DOF 耦合矩阵")

add_table(s, 0.35, 0.94, 8.20, 3.55,
          ["自由度", "WS 旧v2", "WS (1965Ci)", "RS 4× (1965Ci)", "光学耦合 M_opt", "Sync MA (1965Ci)", "5.5 mm 狭缝单层影响"],
          [
              ["X (非扫描)", "≤ 0.32 nm", "≤ 0.38 nm", "≤ 1.12 nm", "1/4 (0.250)", "≤ 0.47 nm (0.472)", "套刻 X：0.472 nm"],
              ["Y (扫描轴)", "≤ 0.36 nm", "≤ 0.39 nm", "≤ 1.18 nm", "1/4 (0.250)", "≤ 0.49 nm (0.489)", "套刻 Y：0.489 nm"],
              ["Z (焦面)",   "≤ 4.50 nm", "≤ 4.80 nm", "≤ 26.0 nm", "n_w/16 (1/11.14)", "≤ 5.35 nm (5.34)", "焦面 Z：5.34 nm"],
              ["Rx (俯仰)",  "≤ 0.20 μrad", "≤ 0.20 μrad", "≤ 0.42 μrad", "n_w/4 (0.359)", "≤ 0.25 μrad", "边缘离焦：0.69 nm"],
              ["Ry (滚转)",  "≤ 0.10 μrad", "≤ 0.10 μrad", "≤ 0.19 μrad", "n_w/4 (0.359)", "≤ 0.12 μrad", "边缘离焦：1.56 nm"],
              ["Rz (偏航)",  "≤ 12 nrad",  "≤ 14 nrad",  "≤ 10 nrad",  "1 : 1 (等角!)", "≤ 17 nrad (17.2)", "边缘套刻 Y：0.224 nm"],
              ["MSD-XY/Z",   "≤ 1.8/10",   "—",          "—",          "7.86 ms 窗 1σ", "≤ 2.0 / 11 nm", "对比度与有效 DOF"],
          ],
          col_widths=[1.15, 0.95, 1.15, 1.15, 1.25, 1.25, 1.30], font_sz=7.5, hdr_sz=7.8, bold_cols=[0], spec_cols=[2, 3, 5])

add_box(s, 0.35, 4.60, 8.20, 2.42, "关键物理机理与分配逻辑（WS 64% : RS/4 36% 保守独立 RSS）", [
    ("液浸 6-DOF 光学矩阵红线：", "仅 X/Y 为 1/4；Z 向为 n_w/16 = 1/11.14（非 1/16）；Rx/Ry 为 n_w/4 = 0.359；Rz 为严格 1:1 等角耦合（RS 偏 10 nrad 直接在 26 mm 边诱发 0.13 nm 套刻）。"),
    ("Sync MA 合成至 L1-S1：", "单层 Y = √(0.489² + 0.224²) = 0.538 nm → 两层 0.760 nm；单层 X = √(0.472² + 0.047²) = 0.474 nm → 两层 0.671 nm；叠加 WS-iHOPC 后精确闭合 L1-S1 = 0.867 nm（20.2%）。"),
    ("速度/加速度工况：", "WS 0.70 m/s（35–40 m/s²），RS 2.80 m/s（150 m/s²，单次扫描行程 230–250 mm，4× 狭缝 22 mm = 7.86 ms 同窗 [ME3]）。"),
], bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.4, body_sz=8.1)

add_img_box(s, "009_fig10_r", 8.70, 0.94, 4.28, 2.95,
            "一手实测：Ref009 Fig. 10 (NXT:1950i Sync MA-X 0.47 / MA-Y 0.49 nm)")
add_img_box(s, "066_fig9", 8.70, 4.02, 4.28, 3.00,
            "一手实测：Ref066 Fig. 9 (陶瓷短行程 WS MAz 峰 4 nm / 95% ≤ 6 nm)")


# =============================================================================
# SLIDE 08 — WS=MASTER SYNC STRATEGY & INDEPENDENT FAT NECESSITY
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "07 同步与独立验收", "WS = Master 同步控制架构核定（纠偏 v2）与单台独立 FAT 验收铁律", 8,
           "结合报告 143 §5.1、ASML 奠基专利 US 6,373,072 B1 与 Double-Youla 研究，彻底厘清主从方向与单/往返独立验收边界")

add_img_box(s, "022_fig1", 0.35, 0.94, 4.15, 2.75,
            "Ref022 Fig. 1：WS(Master) 误差经双前馈送入 RS(Slave)")
add_img_box(s, "147_fig6", 4.65, 0.94, 4.15, 2.75,
            "Ref147 Fig. 6：ASML/TUe 双路前馈（带宽 543–588 Hz）")
add_img_box(s, "075_fig13", 8.95, 0.94, 4.03, 2.75,
            "Ref075 Fig. 13：WS 无耦合 0.48 vs 同步耦合 0.11–0.20 nm")

add_box(s, 0.35, 3.82, 6.20, 3.22, "同步主从核定与 v2 勘误同步（横向 vs 轴向严格区分）", [
    ("横向（X / Y / Rz）：WS = Master，RS = Slave：", "质量更轻、带宽更高的 RS 主动复现并追随 WS 误差（经 ASML US 6,373,072 B1、ME3 TSPE Stages Error Coupling、Nikon US 2012/0319637 A1 及报告 143 §5.1 四重实锤）。"),
    ("为何 WS 独立误差可大于同步 MA？", "σ²_sync = σ²_WS + (σ_RS/4)² − 2ρ·σ_WS(σ_RS/4)，正相关耦合 ρ→0.8–0.9 时相消降噪 2.4–4.4×（[075] 实测 WS 0.48 → 同步 0.20 nm）；ASML 进一步引入双向 Double-Youla。"),
    ("轴向（Z / Rx / Ry）：WS 独立调平：", "RS-Z 缩小 1/11.14 且行程受限，无法高速跟踪硅片起伏，故 Z/Rx/Ry 由 WS 独立伺服。"),
    ("纠偏声明：", "正式修正旧 v2 说明书 §1.3 第 ④ 条关于“RS 前馈给 WS”的表述，全仓口径彻底统一。"),
], bg=C_BOX_WARM, accent=C_CORAL, title_sz=9.5, body_sz=8.0)

add_box(s, 6.72, 3.82, 6.26, 3.22, "为何不能用“同步指标”取消 WS/RS 独立 FAT？（5 大铁律 + 单往返细则）", [
    ("① M-side 量测无 RS 参与：", "SMASH 对准与调平全在 M-side 由 WS 独立完成，同步环 100% 不可见。"),
    ("② 切场步进整定尾与弯月面：", "26 mm 步进 15 ms 整定尾及浸没头水膜剪切扰动不能指望 RS 兜底。"),
    ("③ 150 m/s² 石英微滑移隐身：", "RS 编码器测台体不测石英掩模，须独立连续跑 1000 趟测滑移 ≤ 0.72 nm (4×)。"),
    ("④ WS 独立承担 11 参 iHOPC：", "动态轨迹精度与 1:1 等角 RS-Rz (10 nrad) 必须单台锁死合同门禁。"),
    ("⑤ 单程 + 残余反向差并行验收：", "蛇形扫描（SUSD）存在拖链/涡流/弯月面换向差，强制 R_bi = R_uni (75%) + B_UD,res (25%) ≤ Spec（如 WS-X: 0.29 + 0.09 = 0.38 nm；RS-X: 0.84 + 0.28 = 1.12 nm）。"),
], bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.5, body_sz=8.0)


# =============================================================================
# SLIDE 09 — ENC 2D GRIDPLATE MEASUREMENT SYSTEM
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "08 ENC 编码器", "L1-S1（三）：2D 光栅编码器（ENC）— 0.22 nm 实测宽带、5.5 mm 狭缝滤波与 EMSI", 9,
           "直接对齐 Ref009 Fig. 4 实测 0.22 nm @ 1 kHz，用 Heertjes 2024 ECC 定理严格区分白噪下限（0.056 nm）与有色噪声带内规格（0.13 nm）")

add_table(s, 0.35, 0.94, 7.65, 3.80,
          ["ENC 验收子项", "旧 v2", "NXT:1965Ci 规格", "依据与 1:3 计量核算"],
          [
              ["WS-ENC X/Y 曝光窗 (~64 Hz)", "≤ 0.12 nm", "≤ 0.13 nm", "0.22 宽带 30/70 有色滤波=0.130 nm；1:3 匹配 WS-X(0.38)"],
              ["WS-ENC Z 曝光窗重复性",      "≤ 0.35 nm", "≤ 0.38 nm", "Z 轴光栅衍射灵敏度约 XY 的 1/3（0.13×3≈0.39）"],
              ["WS-ENC Rx / Ry 曝光窗",      "≤ 3.0 nrad", "≤ 3.2 nrad", "四角基线 320 mm 差分 √2×0.38/320 = 1.68 → 2×余量"],
              ["WS-ENC Rz 曝光窗",           "≤ 1.5 nrad", "≤ 1.6 nrad", "四角基线 320 mm 差分 √2×0.13/320 = 0.57 → 2.8×余量"],
              ["WS-ENC 宽带噪声 (1000 Hz)",  "≤ 0.20 nm", "≤ 0.22 nm", "直对 Ref009 Fig. 4 实测 0.22 nm（光程 < 15 mm）"],
              ["WS-ENC 切换 (EMSI Handover)", "≤ 0.15 nm", "≤ 0.15 nm", "4 读数头重叠区在线一致性校准 [009 Fig.7, 143 §5.2]"],
              ["Gridplate 7 天网格稳定性",   "≤ 0.18 nm", "≤ 0.20 nm", "直对 Ref009 §4 实测 < 0.20 nm（10 mK 气幕；<15 mm 标定）"],
              ["RS-ENC X / Y (4× 曝光窗)",   "≤ 0.32/0.36", "≤ 0.37 / 0.39 nm", "严格按 RS-X(1.12)/RS-Y(1.18) 1:3 分配；Rz ≤ 2.8 nrad"],
              ["RS-ENC Z / 宽带 (4×)",       "≤ 2.50/0.60", "≤ 2.60 / 0.68 nm", "晶圆侧等效 0.23 / 0.17 nm，防止 150 m/s² 放大高频噪"],
          ],
          col_widths=[2.25, 0.95, 1.35, 3.10], font_sz=7.4, hdr_sz=7.8, bold_cols=[0], spec_cols=[2])

add_img_box(s, "009_fig4", 8.15, 0.94, 4.83, 3.00,
            "一手实测：Ref009 Fig. 4 (干涉仪 0.9 nm @ 40Hz → NXT 短光程 ENC 0.22 nm @ 1kHz)")

add_box(s, 0.35, 4.86, 7.65, 2.18, "Heertjes [N8] 5.5 mm 狭缝频域滤波：为何白噪下限 0.056 nm ≠ 真实规格 0.13 nm？", [
    ("精确传递函数（[N8] Thm 2.1）：", "5.5 mm @ 0.70 m/s → τ_slit = 7.857 ms，MA 权函数 sinc²(f·τ)，首零点 f1 = 127.3 Hz，ENBW = 63.64 Hz（若提速至 0.75/0.80 m/s，ENBW 增至 68.2/72.7 Hz，带内合成仍 ≤ 0.132 nm）。"),
    ("纯白噪下限偏乐观：", "若误假定 0–1000 Hz 全白噪，0.22×√(63.64/1000) = 0.0555 nm（93.6% 能量被滤）；但真实 ENC 含 0.1–30 Hz 气隙湍流与 1/f 噪声，30% 低频落在通带内滤不掉 → 合成 0.130 nm！"),
    ("FAT 强制交付条款：", "供应商必须交付 0.1 Hz–2 kHz 实测 PSD 与累积功率谱 CPS，直接积分 ∫G_ee(f)sinc²(fτ)df 判定。"),
], bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.1, body_sz=7.9)

add_box(s, 8.15, 4.06, 4.83, 2.98, "Gridplate 空间尺度双标定分工（[N7] & 143 §5.2）", [
    ("< 15 mm 短尺度误差：", "由超低膨胀栅格供应商预标定 + 机内四头 45° 切向 EMSI 重叠区在线自标定闭环消除。"),
    ("> 15 mm 长尺度与跨机：", "通过 13×19 校准参考片多移位（multishift）曝光闭环标定，进入 L1-M1（BMMO 匹配）。"),
    ("45° 切向布局红利：", "四角测头切向测量，天然对卡盘均匀热膨胀一阶不敏感（Ref009 Fig. 5–6）。"),
    ("共享源警示（x03 ★）：", "ENC 同时进入 Sync、WS-iHOPC、AA、TIS/PARIS 与 BMMO，严禁在顶层重复计账。"),
], bg=C_BOX_BLUE, accent=C_NAVY, title_sz=9.1, body_sz=7.9)


# =============================================================================
# SLIDE 10 — M-SIDE WAFER ALIGNMENT (AA / SMASH) & SUSD SAMPLING
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "09 AA 晶圆对准", "L1-S2（一）：M-side 晶圆对准系统（SMASH）与 143 SUSD 方向配平采样", 10,
           "直对 Ref015 Fig. 10 实测重复性，并依据报告 143 §6.1 & §6.3 引入 OCW 颜色加权与防 Gy20 混叠的正反扫方向配平约束")

add_table(s, 0.35, 0.94, 7.35, 3.65,
          ["AA (SMASH) 验收子项", "旧 v2", "NXT:1965Ci", "推导来源与 143 约束"],
          [
              ["单标记静态重复性 (WQ ≥ 1%)", "≤ 0.20 nm", "≤ 0.22 nm", "直对 Ref015 Fig. 10 实测 0.15–0.25 nm 中上值"],
              ["单标记动态扫描 (含 M-side WS)", "≤ 0.35 nm", "≤ 0.38 nm", "静态 0.22 + M-side WS 0.31 RSS = 0.380 nm"],
              ["低信号工艺片 (WQ 0.1%–1%)",  "≤ 0.45 nm", "≤ 0.50 nm", "直对 Ref015 Fig. 10 实测 0.25–0.50 nm 上限"],
              ["四色/多级次配准稳定性 (24h)", "≤ 0.30 nm", "≤ 0.32 nm", "支撑 532/633/780/852 nm OCW 颜色加权 [006/252]"],
              ["全晶圆网格拟合重复性 (HOWA)", "≤ 0.35 nm", "≤ 0.40 nm", "N≥20 对标记统计平均 + HOWA 拟合残差（直入 f3）"],
              ["M-to-E 对准基线短期漂移",    "≤ 0.25 nm", "≤ 0.30 nm", "内含 MF 短期 0.18 nm；与网格合成 0.500 nm (2L 0.707)"],
              ["工艺标记不对称残差 (WAD)",    "≤ 0.45 nm", "≤ 0.50 nm", "不入参考片 SMO，入产品片 OPO 与跨机 M3"],
          ],
          col_widths=[2.15, 0.90, 1.05, 3.25], font_sz=7.5, hdr_sz=7.8, bold_cols=[0], spec_cols=[2])

add_img_box(s, "015_fig10", 7.85, 0.94, 5.13, 2.85,
            "一手实测：Ref015 Fig. 10 (SMASH 正常片 0.15–0.25 nm / 低 WQ 0.25–0.50 nm)")

add_img_box(s, "123_fig14", 7.85, 3.92, 5.13, 3.10,
            "报告 143 §6.3 铁证：Ref123 Fig. 14 (偏置扫向采样 C 组在 M3–M5 跨层累积放大！)")

add_box(s, 0.35, 4.72, 7.35, 2.30, "报告 143 §6.1 & §6.3 注入的两条强制工程红线", [
    ("强制方向配平采样（Ref123 Fig. 10–14）：", "若 HOWA 对准点在扫描方向（Scan Up/Down）或步进方向上不对称分布，高阶拟合会将机台方向差虚假映射为晶圆二阶项 Gy20（> 3.5 nm）并在多层曝光中逐层累积！验收方案必须锁定 A 组方向配平布点，并同步核验 Ref151 场内对称覆盖。"),
    ("标记不对称与产率权衡（Ref252 / Ref107）：", "CMP/刻蚀引发侧壁倾斜时，须用多色 C2A 差异配合 OCW 权重降偏（实测降 0.8–1.2 nm）；标记数由 26 增至 47 对约增耗 1.35 s/片（−6% wph），需在配方层权衡。"),
], bg=C_BOX_WARM, accent=C_CORAL, title_sz=9.3, body_sz=8.0)


# =============================================================================
# SLIDE 11 — E-SIDE AERIAL IMAGE SENSORS (TIS 6 kHz & 7-PT PARIS)
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "10 TIS / PARIS", "L1-S2（二）：E-side 空间像传感（TIS 6 kHz & 7 点 PARIS）与跨支路耦合", 11,
           "PARIS 7 点 RA 直接锚定 Ref066 §3.4（< 0.50 nm），并吸收 143 §4.6 SYCO/LOCO 双卡盘偏置与 §4.2.1 UPW 流量耦合")

add_table(s, 0.35, 0.94, 7.35, 3.25,
          ["子系统与验收子项", "旧 v2", "NXT:1965Ci", "推导依据与闭环定位"],
          [
              ["TIS 水平空间像重复性 XY (6 kHz)", "≤ 0.35 nm", "≤ 0.40 nm", "充当 M-to-E 基线与掩模-物镜-台零点基准（优于 PARIS 0.47）"],
              ["TIS 垂向最佳焦面重复性 Z",       "≤ 2.50 nm", "≤ 2.80 nm", "占 FU 14.0 nm 限值方差仅 4.0%（闭环 FU 11.48 nm）"],
              ["双台 TIS-1 / TIS-2 匹配稳定性",  "≤ 0.25 nm", "≤ 0.28 nm", "24h 相对漂移，直接计入双卡盘 L1-S7 (ΔC2C = 0.48 nm)"],
              ["PARIS 7 视场点 RA 重复性 (XY)",  "≤ 0.40 nm", "≤ 0.47 nm", "直对 Ref066 §3.4 < 0.50 nm（011 实测 0.43）；2L 0.665 → L1-S2 0.970"],
              ["PARIS 7 点场曲焦面重复性 Z",     "≤ 3.00 nm", "≤ 3.20 nm", "兼顾 7 视场边缘 SNR 衰减（约 TIS-Z × 1.15）"],
              ["PARIS/ILC 奇像差波前测噪",       "≤ 0.12 RMS", "≤ 0.14 nm RMS", "支撑每片 3 扫热波前闭环（254 Fig.2 二次套刻贡献反推）"],
          ],
          col_widths=[2.35, 0.85, 1.10, 3.05], font_sz=7.5, hdr_sz=7.8, bold_cols=[0], spec_cols=[2])

add_img_box(s, "066_fig6", 7.85, 0.94, 5.13, 2.85,
            "一手原图：Ref066 Fig. 6 (NXT 7 视场点 PARIS 并行扫描布局 — 每片 3 扫测 14 参 + 64 Zernike)")

add_img_box(s, "100_fig9", 7.85, 3.92, 5.13, 3.10,
            "报告 143 §4.6 铁证：Ref100 Fig. 9 (SYCO 卡盘1 vs LOCO 首片卡盘诱发 K7/K12/K13 偏置)")

add_box(s, 0.35, 4.32, 7.35, 2.70, "为什么 PARIS/TIS 是全景图最关键的共享枢纽之一（x07 ★）？", [
    ("四路并发耦合（f4 / f6 / f9 / f12）：", "每片曝光前 3 次 PARIS 扫描同时输出：① 14 参高阶掩模对准（f4）；② 64 项 Zernike 供 FlexWave 闭环（f6）；③ 掩模桶形热形变供 RHC 更新（f9）；④ 双卡盘 TIS-1/2 基准一致性（f12）。"),
    ("双卡盘 SYCO/LOCO 匹配强制启用（Ref100 Fig. 9）：", "拆分批次首片切换卡盘时，未匹配校准会引入 K7 −1.2、K13 +2.0、K12 +1.5 偏置，验收须核验跨卡盘匹配选项生效。"),
    ("浸没 UPW 流量联合窗口标定（Ref164 Fig. 4–5）：", "报告 143 §4.2.1 证明 UPW 供水流量直接改变 TIS X/Y/Z 3σ（且 X 与 Y/Z 最优流量点不同），须联合锁定工艺流量窗。"),
], bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.3, body_sz=8.0)


# =============================================================================
# SLIDE 12 — WS-iHOPC (11 PARAMS) & 5.5 mm SLIT DECONVOLUTION
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "11 WS-iHOPC", "L1-S1（四）：WS-iHOPC 全 11 项参数与 5.5 mm 真实狭缝逆卷积验证", 12,
           "单层场角预算由 v2 (X 0.228 / Y 0.293) 回松至 NXT:1965Ci (X 0.269 / Y 0.347 nm)；5.5 mm 狭缝逆卷积串扰虽减半但仍强制必需")

add_table(s, 0.35, 0.94, 7.45, 4.10,
          ["参数", "方向/单项式", "G_max", "量程 (±)", "旧 v2", "1965Ci 总残差", "离线(55%)", "场角(nm)"],
          [
              ["K1 / K2", "dx(1) / dy(1)", "1.000", "±200 nm", "≤ 0.120", "≤ 0.140", "≤ 0.077", "0.140"],
              ["K4 / K5", "dy(y) / dx(y)", "1.650", "±50 /cm", "≤ 0.070", "≤ 0.080", "≤ 0.044", "0.132"],
              ["K6",      "dy(x)",         "1.300", "±50 /cm", "≤ 0.080", "≤ 0.095", "≤ 0.052", "0.124"],
              ["K8 / K11","dy(y²)/dx(y²)", "2.723", "±15 /cm²","≤ 0.040", "≤ 0.048", "≤ 0.026", "0.131"],
              ["K10",     "dy(xy)",        "2.145", "±15 /cm²","≤ 0.050", "≤ 0.060", "≤ 0.033", "0.129"],
              ["K14/K19", "dy(y³)/dx(y³)", "4.492", "±5.0 /cm³","≤ 0.025","≤ 0.030", "≤ 0.017", "0.135"],
              ["K16",     "dy(xy²)",       "3.539", "±5.0 /cm³","≤ 0.030","≤ 0.036", "≤ 0.020", "0.127"],
              ["RSS 汇总","4项X / 7项Y",   "—",     "5.5 mm 狭缝", "0.228/0.293", "X 0.269 / Y 0.347", "1.2×两层", "0.323/0.416"],
          ],
          col_widths=[0.90, 1.15, 0.68, 0.92, 0.85, 1.25, 0.85, 0.85], font_sz=7.4, hdr_sz=7.7, bold_cols=[0], spec_cols=[5])

add_img_box(s, "154_crop", 7.95, 0.94, 5.03, 2.55,
            "官方标准：Ref154 p.7 Eq.1 & Table 1 (ASML 20 参场内多项式，WS 承担 11 项)")

add_box(s, 7.95, 3.60, 5.03, 3.42, "5.5 mm 真实狭缝逆卷积推导（vs 旧 8.0 mm）", [
    ("二阶矩精确减半（−52.7%）：", "真实 NA=1.35 狭缝 L_s = 0.55 cm [N1 Table 3]，μ₂ = L_s²/12 = 0.0252 cm²（旧 8 mm 为 0.0533），3μ₂ = L_s²/4 = 0.0756 cm²（旧为 0.1600）。"),
    ("逆卷积预畸变公式（强制内置）：", "K1_cmd = K1 − 0.0252·K11；K2_cmd = K2 − 0.0252·K8；K6_cmd = K6 − 0.0252·K16；K4_cmd = K4 − 0.0756·K14；K5_cmd = K5 − 0.0756·K19。"),
    ("为何减半后仍不可省略？", "若下发 K14 = 1.0 nm/cm³ 而不逆卷积，场角仍诱发 +0.125 nm 额外串扰（几乎等于 K14 自身 0.135 nm 整项预算！）。"),
    ("空间截止频率提升：", "f_c = 1/5.5 = 0.182 mm⁻¹（λ_y ≤ 5.5 mm 不可补），较 8 mm 拓宽 45%。"),
], bg=C_BOX_WARM, accent=C_CORAL, title_sz=9.3, body_sz=7.9)

add_box(s, 0.35, 5.16, 7.45, 1.86, "破解“ENC 测 ENC 自己”盲区的三级验收闭环与双档 |K0| 指令", [
    ("三级验收闭环：", "Stage 1 离线 ENC 伺服（经 5.5 mm MA + OLS 回归 ≤ 55% Spec，加 Z/Rx/Ry 阿贝护栏）→ Stage 2 外部激光干涉仪核验网格板比例尺与触发同步 → Stage 3 在线双层阶跃曝光 SAT（≤ 100% Spec）。"),
    ("双档典型指令 |K0|：", "常规稳态层抽测 K4/K5/K6 = 5.0 nm/cm，满热态/高应力严苛层抽测 15.0 nm/cm，同步考核绝对残差与比例斜率。"),
], bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.1, body_sz=7.9)


# =============================================================================
# SLIDE 13 — LENS ODD ZERNIKE (Z5-Z64 ALL 30 TERMS)
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "12 Odd Zernike", "L1-S3（一）：物镜奇对称波像差（Z5–Z64 全 30 项）2D Abbe 仿真与实证闭环", 13,
           "NXT:1965Ci 单轴跨照明包络 0.437 nm（全瞳 0.400 nm RMS / Coma 0.190 nm），Abbe 仿真 Z10=0.905 与 IBM/ASML 实证 0.88 误差仅 2.8%")

add_img_box(s, "c_zern", 0.35, 0.92, 8.35, 3.15,
            "图 13-1  NXT:1965Ci 全 30 项 Odd Zernike 控制规格（nm Fringe）、跨照明包络灵敏度与单轴套刻贡献（RSS = 0.437 nm）")

add_img_box(s, "024_fig11", 8.85, 0.92, 4.13, 2.00,
            "Ref024 Fig. 11：NXT:1950i FlexWave Coma 0.15–0.16 nm RMS")
add_img_box(s, "008_fig4b", 8.85, 3.00, 4.13, 1.98,
            "Ref008 Fig. 4b：Z2 = −0.74 nm/nm 与 DRAM 奇像差灵敏度")

add_table(s, 0.35, 4.16, 8.35, 2.88,
          ["高敏重点 Odd 项 (X/Y)", "类别", "|ΔS_env|", "旧 v2 (Fr)", "1965Ci (Fr)", "等效 RMS (nm)", "套刻 (nm)", "实证校核来源"],
          [
              ["Z7 / Z8  (3,1)",   "1θ Coma",   "0.950", "≤ 0.18", "≤ 0.21", "≤ 0.0742", "0.199", "包络 [008]；IBM [N6] 差分 0.83"],
              ["Z10 / Z11 (3,3)",  "3θ Trefoil","0.910", "≤ 0.16", "≤ 0.19", "≤ 0.0672", "0.173", "Abbe 0.905 vs [N6] 0.88 (差 2.8%!)"],
              ["Z14 / Z15 (5,1)",  "1θ Coma",   "0.700", "≤ 0.18", "≤ 0.21", "≤ 0.0606", "0.147", "次阶彗差 Abbe 0.671 ([N6] 0.38)"],
              ["Z19 / Z20 (5,3)",  "3θ Trefoil","0.550", "≤ 0.20", "≤ 0.24", "≤ 0.0693", "0.132", "DRAM 旋转切换峰值包络 [008]"],
              ["Z26 / Z27 (5,5)",  "5θ Penta",  "0.843", "≤ 0.16", "≤ 0.19", "≤ 0.0548", "0.160", "Dipole-Quasar 强耦合，必须严控"],
              ["Z30/31, Z39/40, Z50/51", "3θ/5θ/7θ", "0.32–0.46", "≤ 0.22–0.24", "≤ 0.26–0.28", "≤ 0.065–0.070", "0.09–0.12", "含 7θ Heptafoil Z50/51 不可漏控"],
              ["其余 12 项高径向项", "1θ/3θ/5θ", "0.09–0.31", "≤ 0.24–0.40", "≤ 0.28–0.48", "≤ 0.067–0.091", "0.04–0.09", "反灵敏度放宽，控 RMS ≤ 0.09 nm"],
              ["全 30 项 RSS 汇总", "Z5–Z64",    "Abbe 实算 0.388", "0.370", "单轴 1.196 Fr", "全瞳 0.400 nm", "0.437 nm", "叠加热声 0.226 → f6 = 0.492 nm"],
          ],
          col_widths=[1.45, 0.80, 0.72, 0.78, 0.88, 0.92, 0.70, 2.10], font_sz=7.0, hdr_sz=7.3, bold_cols=[0], spec_cols=[4, 5])

add_box(s, 8.85, 5.08, 4.13, 1.96, "高透 NTD 热漂与 FlexWave 闭环 [N5/N6]", [
    ("未控高透热漂 > 6 nm：", "78% 亮场 NTD 掩模热漂可致奇像差位移 > 6 nm（偶项致 8–10 nm CD 漂移）[N5/N6]。"),
    ("FlexWave + PARIS 闭环：", "将热漂奇像差压至 < 2 nm，配合 Ref009 声学减振将常规两层热声残差锁在 0.226 nm。"),
], bg=C_BOX_TEAL, accent=C_OLIVE, title_sz=9.0, body_sz=7.8)


# =============================================================================
# SLIDE 14 — LENS-iHOPC (8 PARAMS, K3 RANGE & 8-DIM EVALUATION)
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "13 Lens-iHOPC", "L1-S3（二）：物镜场内补偿（8 激活参 + K20 边界）、K3 行程重估与 8 维评价", 14,
           "第一性核定 K3 硬件总 Range ±15–25 ppm（用户 ±5–10 ppm）；NXT:1965Ci 激活 8 参闭环 X 0.375 / Y 0.216 nm，不含 K20")

add_table(s, 0.35, 0.94, 7.65, 3.85,
          ["参数", "单项式", "G_max", "硬件/用户 Range", "旧 v2", "1965Ci 残差", "单向/滞回", "场角(nm)"],
          [
              ["K3",  "dx(x)",   "1.300", "±150–250 / ±50–100", "≤ 0.100", "≤ 0.120", "0.042/0.030", "0.156"],
              ["K7",  "dx(x²)",  "1.690", "±10.0 /cm²",         "≤ 0.080", "≤ 0.092", "0.032/0.023", "0.155"],
              ["K12", "dy(x²)",  "1.690", "±10.0 /cm²",         "≤ 0.080", "≤ 0.092", "0.032/0.023", "0.155"],
              ["K13", "dx(x³)",  "2.197", "±6.0 /cm³",          "≤ 0.060", "≤ 0.070", "0.025/0.018", "0.154"],
              ["K9",  "dx(xy)",  "2.145", "±8.0 (动态)",         "≤ 0.060", "≤ 0.072", "0.025/0.018", "0.154"],
              ["K15", "dx(x²y)", "2.789", "±4.0 (动态)",         "≤ 0.045", "≤ 0.054", "0.019/0.014", "0.151"],
              ["K17", "dx(xy²)", "3.539", "±4.0 (动态)",         "≤ 0.035", "≤ 0.042", "0.015/0.011", "0.149"],
              ["K18", "dy(yx²)", "2.789", "±4.0 (动态)",         "≤ 0.045", "≤ 0.054", "0.019/0.014", "0.151"],
              ["K20*", "dy(x³)", "2.197", "1965Ci 不支持",        "静≤0.15", "静≤0.18", "冷机出厂控", "入 M2"],
              ["RSS 汇总", "6X / 2Y", "—", "SET-GET 3–5.6%", "0.317/0.184", "X 0.375 / Y 0.216", "1.2×两层", "0.450/0.260"],
          ],
          col_widths=[0.68, 0.78, 0.65, 1.55, 0.80, 1.15, 1.12, 0.92], font_sz=7.2, hdr_sz=7.5, bold_cols=[0], spec_cols=[5])

add_img_box(s, "c_lens8", 8.15, 0.94, 4.83, 2.95,
            "物镜 K_n 补偿能力 8 维综合评价体系（行程/步长/滞回/线性/串扰/带宽/漂移/三级闭环）")
add_img_box(s, "253_fig8", 8.15, 4.00, 4.83, 3.02,
            "行业基准：Ref253 Fig. 8 (ASML/Zeiss 机内空间像 SET-vs-GET 精度 ≤ 5%)")

add_box(s, 0.35, 4.90, 7.65, 2.12, "K3 硬件 Range 第一性核定与双平面操纵器代际边界（[N1, N4, N7]）", [
    ("K3 硬件 Range ±15–25 ppm（1 ppm = 10 nm/cm）：", "由工艺应力 (±5–10 ppm) + 镜头热漂 (±1–5 ppm) + 掩模 RWE/加热 (±0.6–1.5 ppm) + 晶圆温差/跨机 (±0.5–2 ppm) + 气压 (1–3 ppm/mbar [ME3]) + 20% 裕量合成；用户层开放 ±5–10 ppm（多参联合行程占用 ≤ 80%）。"),
    ("光瞳面 vs 像场面正交边界 [N4 Fig.5]：", "NXT:1965Ci 采用 FlexWave（光瞳面，Z2–Z64 × X⁰–X²），架构不支持 K20；至 NXT:2050i/2100i 新增像场面 Distortion Manipulator（7–9 阶扫描实时）+ 79×17 密网格调校。"),
], bg=C_BOX_BLUE, accent=C_NAVY, title_sz=9.1, body_sz=7.9)


# =============================================================================
# SLIDE 15 — THERMAL, IMMERSION UPW, RHC & PELLICLE DYNAMICS (S4 & S5)
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "14 热控与掩模", "L1-S4 & S5：晶圆热/浸没流场（0.784 nm）与掩模热/夹持/Pellicle（0.809 nm）", 15,
           "完整落地报告 143 第 2、4 章的三条热扰动路径（水膜/气隙/晶圆实体）、RHC 前馈控制及 Pellicle 动态扫描误差")

add_img_box(s, "017_fig7", 0.35, 0.94, 3.05, 2.35, "Ref017 Fig.7：片温与网格 R²=0.92")
add_img_box(s, "021_fig12", 3.52, 0.94, 3.05, 2.35, "Ref021 Fig.12：浸没水温 ±2.5 mK")
add_img_box(s, "066_fig5", 6.69, 0.94, 3.05, 2.35, "Ref066 Fig.5：RHC 6.2→1.8 nm")
add_img_box(s, "098_fig15", 9.86, 0.94, 3.12, 2.35, "Ref098 Fig.15：Pellicle 动态高阶")

add_table(s, 0.35, 3.42, 12.63, 2.48,
          ["L1 / L2 节点", "2L 预算 (nm)", "底层 L3 原生验收规格（FAT）", "报告 143 与一手文献工程依据"],
          [
              ["S4 / f7 晶圆实体热与 WH", "0.677", "WT 温控 ≤ ±3 mK，边缘分区加热面内 3σ < 80 mK；WH 出口片温差 ≤ ±15 mK", "Ref017 MK4.0 3σ=80 mK、R²=0.92；Si α=2.6 ppm/K (0.39 nm/mK)；片序/场序反转 [021/050]"],
              ["S4 / f8 浸没水膜 n(T)",  "0.396", "UPW 供回水 ≤ ±3 mK；0.75 m/s 弯月面+气幕无残水滴；UPW 流量联合 TIS 标定", "Ref021 ±2.5 mK；Ref040 300 μm 边界层；Ref164 UPW 流量→TIS；Ref167 批变 < 2%"],
              ["S5 / f9 掩模热 RHC+气隙","0.696", "掩模上表面冷却 + 下方 5 mK 水平气幕；RTS + TPM/MPM 每场 RHC 前馈残差 ≤ 0.43 (1L)", "Ref016/066 极热 6.2→1.8 nm；Ref025 掩模下气隙折射率 1.1→0.7 nm；Ref110 前 20 片瞬态"],
              ["S5 / f10 RT夹持+Pellicle","0.411", "分段叶簧夹持重夹 ≤ 0.72 nm(4×)；150m/s² 千趟滑移 ≤ 0.72(4×)；软胶垫 Pellicle ≤ 0.14(1×)", "Ref104 380 μm 软胶垫；Ref106/098 扫描吹扫动态高阶；JP5809458B2 分段叶簧 [225]"],
          ],
          col_widths=[1.85, 1.00, 4.88, 4.90], font_sz=7.5, hdr_sz=7.8, bold_cols=[0], spec_cols=[1])

add_box(s, 0.35, 6.00, 12.63, 1.04, "热—液—机跨支路耦合设计提醒（对应全景图共享源 x10 / x11 / x07）", [
    ("区分“改新图形像点” vs “改已有图形坐标”（143 §4.2）：", "浸没水膜与掩模气隙折射率改变的是新曝光像点坐标；残液蒸发与 WT/WH 热边界改变的是硅片已有图案坐标，验收时必须分别用测温片（Ref017）与像点/TIS 读数（Ref164）解耦分离。"),
    ("小场局部加热风险（Ref254）：", "常规全场验收达标不代表窄场/小场无热漂，建议在 RHC 验收中同步加入 19×32 mm 窄场工况（Ref066 Fig. 5）。"),
], bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.0, body_sz=7.9)


# =============================================================================
# SLIDE 16 — WAFER CLAMPING, SUSD INTERFACES & DUAL-CHUCK ΔC2C (S6 & S7)
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "15 夹持与双卡盘", "L1-S6 & S7：晶圆夹持、SUSD 三大机械接口（0.552 nm）与双卡盘 ΔC2C（0.588 nm）", 16,
           "融合报告 143 §4.4/4.6/5.3，完整打通“硅片—WT—柔顺长柱—计量块(MB)”传力接口与双台生产套刻边界")

add_table(s, 0.35, 0.94, 7.65, 2.70,
          ["节点与细分项", "单层/双台规格", "两层贡献", "机理与文献依据"],
          [
              ["S6.1 WT 真空吸片重复性",     "≤ 0.30 nm", "0.424 nm", "瘤点接触摩擦 + 吸附序列重复性 [066, 097]"],
              ["S6.2 扫描期硅片背面微滑移",  "≤ 0.20 nm", "0.283 nm", "35–40 m/s² 加减速切向牵引应力 [122]"],
              ["S6.3 WT–MB 柔顺长柱微滞回",  "≤ 0.15 nm", "0.212 nm", "US 8,269,949 B2 长柱/细颈传力路径 SUSD 滞回"],
              ["S6 晶圆夹持域 RSS 合计",     "0.390 (1L)", "0.552 nm", "占六域方差 8.21%（vs Ref009 8.27%，差 −0.06%）"],
              ["S7.1 双卡盘 ΔC2C 总计",      "≤ 0.48 nm", "0.480 nm", "TIS1/2 (0.28) + WT1/2 指纹 (0.35) + SYCO/LOCO (0.17)"],
              ["S7.2 离线量测与验证底噪",    "≤ 0.34 nm", "0.340 nm", "TMU + 未建模底噪；与 ΔC2C 合成 S7 = 0.588 nm"],
          ],
          col_widths=[1.95, 1.05, 0.95, 3.70], font_sz=7.5, hdr_sz=7.8, bold_cols=[0], spec_cols=[1, 2])

add_img_box(s, "066_fig10a", 8.15, 0.94, 4.83, 3.05,
            "一手原图：Ref066 Fig. 10a (更平坦 WT 对 Focus 6.2 nm 与 50 μm 翘曲片 Overlay 1.0 nm 收益)")

add_box(s, 0.35, 3.76, 7.65, 3.26, "报告 143 §5.3 & §4.6 的三接口 + 三指纹定位体系", [
    ("沿图案→计量参考的三处机械接口：", "① 晶圆背面↔WT 瘤点（吸片重复与滑移）；② WT↔编码器计量块 MB（US 8,269,949 B2 柔顺长柱：即使 MB 回到同一坐标，WT 相对 MB 若有滞回仍生 SUSD 偏移）；③ 掩模↔RS 夹持（JP 5,809,458 B2 分段叶簧）。"),
    ("三类指纹独立识别实验（143 §4.6）：", "Wafer 指纹（换台/旋转跟随硅片）、Field 指纹（跨场平均/按扫向剂量分组）、Chuck 指纹（同片换卡盘 + 单独检查 SYCO/LOCO 计量参考）。"),
    ("同卡盘 DCO vs 双卡盘 SMO 验收边界：", "Ref009 Fig. 3 原口径为同卡盘 DCO（闭环 2.26 nm ≤ 2.50 nm）；量产双台交替曝光显式加计 ΔC2C = 0.48 nm 后 SMO = 2.36 nm ≤ 2.50 nm，仍留 5.4% 安全裕度！"),
], bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.3, body_sz=8.0)

add_box(s, 8.15, 4.10, 4.83, 2.92, "WT 平坦度与高翘曲工艺片能力边界", [
    ("WT 瘤点平坦度 ≤ 6.5 nm：", "对标 Ref066 Fig. 10a（6.2 nm），为整机 Focus Uniformity 11.48 ≤ 14.0 nm 提供最大单一硬件基石。"),
    ("50 μm 翘曲片夹持残差 ≤ 1.00 nm：", "自由态碗/鞍形硅片压平后产生面内畸变 IPD（Ref097/118）；在双机 MMO 中单列 1.00 nm 预算（M3）。"),
    ("前馈扩展接口（Ref112/117）：", "极端非均匀应力层可接入曝光前 PWG 几何量测（PIR 前馈 iHOPC/CPE）。"),
], bg=C_BOX_BLUE, accent=C_NAVY, title_sz=9.1, body_sz=7.9)


# =============================================================================
# SLIDE 17 — CROSS-MACHINE MMO <= 4.50 nm & FOCUS UNIFORMITY <= 14.0 nm
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "16 MMO 与焦面", "L1-M1..M3：混机套刻 MMO ≤ 4.50 nm（闭环 4.29 nm）与焦面 FU ≤ 14.0 nm", 17,
           "承袭 Ref-146 Fig. 3 顶层分叉（MMO = SMO + 网格匹配 + 光学匹配 + 卡盘/热匹配），结合 Ref066 BMMO 与 Ref167/168 边界")

add_table(s, 0.35, 0.94, 7.55, 3.10,
          ["MMO 顶层分支", "3σ RSS (nm)", "构成明细与对标依据"],
          [
              ["SMO 双卡盘随机基线", "2.015", "X 1.965 / Y 1.981 nm（完整包含 S1–S7 七大单机域）"],
              ["M1 跨机网格匹配 (BMMO)", "2.000", "13×19 多移位标定 + 校准参考片 + Gridplate >15 mm 尺度匹配 [066 Fig.4, N7]"],
              ["M2 光学跨机匹配", "1.887", "静态高阶 NCE（无 K20）1.60 + 第 2 台 Odd Zernike 0.437 + 跨机 iHOPC/APC 0.90"],
              ["M3 卡盘/对准/热/掩模匹配", "1.658", "50 μm 翘曲 WT 1.00 [066] + 对准/WAD/TIS 0.95 + 跨机热/RHC 0.85 + 掩模 NCE 0.354"],
              ["MMO 随机 RSS 合计", "3.792", "X 3.765 / Y 3.773 nm（Matching 净增 RSS = 3.211 nm）"],
              ["MMO 闭环（+|Mean| 0.50）", "4.291 nm", "X 4.265 / Y 4.273 nm ≤ 4.50 nm PASS（工程裕度 0.209 nm / 4.6%）"],
          ],
          col_widths=[2.10, 1.05, 4.40], font_sz=7.5, hdr_sz=7.8, bold_cols=[0], spec_cols=[1])

add_img_box(s, "066_fig4", 8.05, 0.94, 4.93, 3.10,
            "一手实测：Ref066 Fig. 4 (BMMO 校准将全片跨机 MMO 由 7.0 nm 压至 3.4 nm)")

add_table(s, 0.35, 4.18, 7.55, 2.84,
          ["全片焦面均匀性 FU 分量 (3σ)", "预算 (nm)", "方差占比", "硬件支撑与文献依据"],
          [
              ["Sync MA-Z + 倾角边缘离焦", "5.34 / 1.71", "23.9%", "陶瓷 WS 4.80 + RS-Z 26/11.14 + 5.5 mm 狭缝 Rx/Ry"],
              ["WT 瘤点平坦度",            "6.50",        "32.1%", "对标 Ref066 Fig. 10a (6.2 nm)，最大单一焦面项"],
              ["物镜场曲与热离焦残差",     "4.80",        "17.5%", "PARIS 每片 7 点场曲监测 + FlexWave 偶项抑制"],
              ["调平传感 (LS/AGILE) 残差", "4.20",        "13.4%", "工艺膜栈形貌跟随（可选升级 UV-LS [066 §4.2]）"],
              ["TIS-Z / RT 夹持 / 框架浸没","2.8 / 2.2 / 2.2", "13.1%", "TIS 最佳焦面 + 石英弯曲 (1/11.14) + 水膜 Δn"],
              ["整机 FU 闭环汇总 (目标 ≤ 14.0)", "11.48 nm", "100.0%", "PASS（留 2.52 nm / 18.0% 裕度；1950i 15–20 nm）"],
          ],
          col_widths=[2.25, 1.15, 0.85, 3.30], font_sz=7.3, hdr_sz=7.6, bold_cols=[0], spec_cols=[1])

add_box(s, 8.05, 4.18, 4.93, 2.84, "机台 MMO vs 工艺/掩模总 OPO 边界（Ref165/167/168）", [
    ("Ref168（掩模与自定位剥离）：", "双图形掩模套刻约占总 OPO 12%；通过单层相邻间距自定位测试可分离 10%–30% 的刻蚀与量测非对准贡献。"),
    ("Ref167（浸没批变边界）：", "实测浸没指纹批内波动仅 0.18/0.22 nm（< 2%），验证 CPE 批级前馈物理可行。"),
    ("Ref165（LELE 耦合约束）：", "双图形中套刻误差直接转化为空间 CDU，需以高阶网格与跨机匹配保底。"),
], bg=C_BOX_WARM, accent=C_CORAL, title_sz=9.0, body_sz=7.8)


# =============================================================================
# SLIDE 18 — 4-TIER VERIFICATION PYRAMID & SEMI-STATIC EXECUTION ROADMAP
# =============================================================================
s = prs.slides.add_slide(BLANK)
add_header(s, "17 验证闭环", "NXT:1965Ci 四层验证金字塔（143 §7.2）与四套半静态工况验收计划（Ref146 §4.5）", 18,
           "从部件级 L3 原生指标逐级攀升至整机 DCO/SMO/MMO 与产品片 ADI/AEI，确保所有子系统规格可测、可追责、可闭环")

tiers = [
    ("Tier 1 · 部件级 FAT\n(L3 原生指标 x01–x18)",
     "• ENC：0.1 Hz–2 kHz 实测 PSD/CPS 积分判定 0.13 nm\n• Lens-iHOPC：离线 PMI 8 维（滞回≤25%/串扰≤30%）\n• RT/WT：150 m/s² 千趟滑移 ≤0.72(4×)；平坦度 ≤6.5 nm\n• 流体/热：UPW ±3 mK & 流量—TIS 曲线；Pellicle PROVE", C_BLUE, C_BOX_BLUE),
    ("Tier 2 · 子系统级验证\n(L2 执行动作 f1–f14)",
     "• WS/RS：单程+往返（75%+25%）；WS=Master 耦合带宽\n• WS-iHOPC：离线 55% → 激光干涉仪 → 5.5 mm 逆卷积曝光\n• 对准/PARIS：SUSD 方向配平 HOWA；每片 3 扫 7 点 RA≤0.47\n• 热补偿：RHC 满/窄场剂量阶跃（6.2→≤1.8 nm）", C_TEAL, C_BOX_TEAL),
    ("Tier 3 · 整机参考片 SAT\n(L0 四套半静态工况)",
     "• 工况① 冷机同卡盘 DCO：实测 ≤ 2.50 nm（预算 2.26）\n• 工况② 生产双卡盘 SMO：启 SYCO/LOCO ≤ 2.50（预算 2.36）\n• 工况③ 高剂量+跨照明热态：片序/场序反转验证 ρ < 0.025\n• 工况④ 跨机匹配 MMO：BMMO+50 μm 翘曲片 ≤ 4.50（4.29）", C_NAVY, C_TBL_ALT),
    ("Tier 4 · 产品多层 OPO\n(工艺/量测/APC 闭环)",
     "• 靶标 vs 器件：CD-SEM 校验全狭缝预测差 < 0.5 nm [008]\n• 工艺剥离：ADI vs AEI 同靶差分 + 新参考层测应力释放 [102]\n• 批间 APC：接入 LIS/R2R 监控退化批与采样代表性 [100/115]\n• 持续维护：按 Ref146 §2.3 随实测更新活预算表", C_CORAL, C_BOX_WARM),
]
for idx, (tt, tb_txt, col, bg) in enumerate(tiers):
    tx = 0.35 + idx * 3.20
    card = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(tx), Inches(0.96), Inches(3.04), Inches(3.70))
    card.fill.solid(); card.fill.fore_color.rgb = bg
    card.line.color.rgb = col; card.line.width = Pt(1.2); card.shadow.inherit = False
    hdr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(tx), Inches(0.96), Inches(3.04), Inches(0.62))
    hdr.fill.solid(); hdr.fill.fore_color.rgb = col; hdr.line.fill.background(); hdr.shadow.inherit = False
    htf = hdr.text_frame; htf.vertical_anchor = MSO_ANCHOR.MIDDLE
    hp = htf.paragraphs[0]; hp.alignment = PP_ALIGN.CENTER
    hr = hp.add_run(); hr.text = tt; hr.font.name = FONT; hr.font.size = Pt(9.8); hr.font.bold = True; hr.font.color.rgb = C_WHITE

    btb = s.shapes.add_textbox(Inches(tx + 0.10), Inches(1.66), Inches(2.84), Inches(2.92))
    btf = btb.text_frame; btf.word_wrap = True
    for li, line in enumerate(tb_txt.split("\n")):
        bp = btf.paragraphs[0] if li == 0 else btf.add_paragraph()
        bp.space_after = Pt(5.0)
        br = bp.add_run(); br.text = line
        br.font.name = FONT; br.font.size = Pt(8.1); br.font.color.rgb = C_DARK

    if idx < 3:
        arr = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(tx + 3.06), Inches(2.65), Inches(0.12), Inches(0.28))
        arr.fill.solid(); arr.fill.fore_color.rgb = C_MUTED; arr.line.fill.background()

add_box(s, 0.35, 4.82, 12.63, 2.20, "NXT:1965Ci 完整交付物与严格仓库治理总览（OpticsPan/OV4）", [
    ("主技术报告（MD，遵循 UP-010/011）：", "outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v1.md（含全 6 章推导、双轴总账与 18 项 L3 台账）。"),
    ("全景拆解图（可编辑 draw.io + 高清 PNG）：", "outputs/images/NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.drawio 与同名 .png（由 build_nxt1965ci_budget_and_diagram_v1.py 单一事实源生成）。"),
    ("本汇报演示文稿（18 页 PPTX）：", "outputs/presentations/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与子系统验收规格_v1.pptx（全片统一 1965Ci、5.5 mm 狭缝与 WS=Master）。"),
    ("严格溯源与历史归档边界：", "仅参考 OV4 v2 基线 + Overlay3 报告 143 + 一手原件（Ref146/009/066/165/167/168/[N1–N8]/[S1–S14]）+ ME3；旧 v2 基线完整保留，误引用 v1 已冻结归档不再作为后续参考。"),
], bg=C_BOX_TEAL, accent=C_NAVY, title_sz=9.6, body_sz=8.2)


prs.save(str(OUT_PPTX))
print(f"[OK] Saved {TOTAL}-slide NXT:1965Ci PPTX -> {OUT_PPTX} ({OUT_PPTX.stat().st_size:,} bytes)")
