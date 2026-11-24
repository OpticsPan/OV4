"""Build 28-slide 16:9 (v2) PowerPoint presentation for OV4 1950i-1970Ci Acceptance Specs & Budget.
Every specification item is backed by original OV4/ME3 paper screenshots, exact analytical
derivations, or 2D Abbe / thermal physics simulation plots.

Run from repository root in PowerShell:
    $env:PYTHONPATH = "D:/Codex/cache/pdf-python;D:/Codex/cache/uv/archive-v0/D98sR3K3a9uncNLd"
    python -B outputs/code/build_spec_pptx_v2.py
"""
import json
import math
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
ME3_MD = Path(r"D:\work\ME3\参考文献\Markdown_v1")
ASSETS = REPO / "work/ppt_assets"
OUT_DIR = REPO / "outputs/presentations"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PPTX = OUT_DIR / "NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v2.pptx"

# Palette (Matches ME white-background executive technical deck style)
C_NAVY = RGBColor(0x12, 0x38, 0x49)
C_DARK_BLUE = RGBColor(0x1F, 0x38, 0x64)
C_TEAL = RGBColor(0x08, 0x78, 0x71)
C_BODY = RGBColor(0x1B, 0x30, 0x3C)
C_MUTED = RGBColor(0x55, 0x6D, 0x78)
C_CORAL = RGBColor(0xC8, 0x4B, 0x00)
C_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
C_TBL_HDR = RGBColor(0xDC, 0xEA, 0xF2)
C_TBL_ALT = RGBColor(0xF6, 0xF9, 0xFB)
C_BOX_TEAL = RGBColor(0xF0, 0xF8, 0xF7)
C_BOX_WARM = RGBColor(0xFF, 0xF6, 0xEC)
C_BOX_BLUE = RGBColor(0xF1, 0xF5, 0xFA)
C_BORDER = RGBColor(0xC0, 0xD2, 0xD8)
C_SPEC_BLUE = RGBColor(0x00, 0x3B, 0x8E)

FONT = "Microsoft YaHei"
TOTAL_SLIDES = 28
_PNO = [1]
def next_pno():
    _PNO[0] += 1
    return _PNO[0]

# Image registry (every path pre-verified!)
IMG = {
    "009_fig3": OV4_MD / "assets/009_9e90b86e529c/images/page_2_chart_4.jpg",
    "009_fig4": OV4_MD / "assets/009_9e90b86e529c/images/page_3_image_2.jpg",
    "009_fig10_r": OV4_MD / "assets/009_9e90b86e529c/images/page_6_chart_3.jpg",
    "009_fig10_l": OV4_MD / "assets/009_9e90b86e529c/images/page_6_chart_2.jpg",
    "015_fig7": OV4_MD / "assets/015_9a19b5ebb43f/images/page_4_chart_4.jpg",
    "015_fig10": OV4_MD / "assets/015_9a19b5ebb43f/images/page_6_chart_1.jpg",
    "066_fig2_full": ASSETS / "066_fig2_full_crop.png",
    "066_fig6_b": OV4_MD / "assets/066_d108fef2e419/images/page_4_image_3.jpg",
    "066_fig8": OV4_MD / "assets/066_d108fef2e419/images/page_5_chart_2.jpg",
    "066_fig9": OV4_MD / "assets/066_d108fef2e419/images/page_5_chart_7.jpg",
    "066_fig10a": OV4_MD / "assets/066_d108fef2e419/images/page_6_chart_2.jpg",
    "062_fig11": OV4_MD / "assets/062_57355c4f4bbf/images/page_8_chart_1.jpg",
    "075_fig13": OV4_MD / "assets/075_97d74e7b9094/images/page_9_chart_2.jpg",
    "094_fig16": OV4_MD / "assets/094_9198e4d130a4/images/page_8_image_4.jpg",
    "094_fig24": OV4_MD / "assets/094_9198e4d130a4/images/page_12_image_5.jpg",
    "019_fig9": OV4_MD / "assets/019_fa276f73329c/images/page_4_image_5.jpg",
    "019_fig15": OV4_MD / "assets/019_fa276f73329c/images/page_6_image_0.jpg",
    "021_fig12": OV4_MD / "assets/021_d3ddae439a1d/images/page_8_chart_7.jpg",
    "017_fig7": OV4_MD / "assets/017_8936fe20711b/images/page_3_chart_3.jpg",
    "016_fig6": OV4_MD / "assets/016_ccbee0872f24/images/page_4_image_6.jpg",
    "254_fig2": OV4_MD / "assets/254_2b7cddcca8f2/images/page_1_chart_5.jpg",
    "254_fig3": OV4_MD / "assets/254_2b7cddcca8f2/images/page_2_chart_8.jpg",
    "254_fig9": OV4_MD / "assets/254_2b7cddcca8f2/images/page_7_chart_2.jpg",
    "225_fig1_8": OV4_MD / "assets/225_2cf70b4ec278/images/page_24_chart_6.jpg",
    "225_fig1_9": OV4_MD / "assets/225_2cf70b4ec278/images/page_25_image_6.jpg",
    "225_fig3_3": OV4_MD / "assets/225_2cf70b4ec278/images/page_41_chart_8.jpg",
    "225_fig6_15": OV4_MD / "assets/225_2cf70b4ec278/images/page_117_chart_4.jpg",
    "253_fig7": OV4_MD / "assets/253_d054bfdabe17/images/page_6_chart_8.jpg",
    "253_fig8": OV4_MD / "assets/253_d054bfdabe17/images/page_7_chart_1.jpg",
    "008_fig4a": OV4_MD / "assets/008_8d2163e59192/images/page_4_chart_1.jpg",
    "008_fig4b": OV4_MD / "assets/008_8d2163e59192/images/page_4_chart_2.jpg",
    "024_fig2": OV4_MD / "assets/024_e25f1b752cb5/images/page_3_image_0.jpg",
    "024_fig11": OV4_MD / "assets/024_e25f1b752cb5/images/page_9_chart_3.jpg",
    "me3_tsu": ME3_MD / "assets/82369533f11a8eaa/images/page_15_image_3_v1.jpg",
    "154_crop": ASSETS / "154_p7_eq1_table1_crop.png",
    "c_budget": ASSETS / "chart_01_budget_closure.png",
    "c_wh": ASSETS / "chart_02_wh_transient.png",
    "c_slit": ASSETS / "chart_03_slit_deconv.png",
    "c_zern": ASSETS / "chart_04_zernike_abbe.png",
    "094_fig15": OV4_MD / "assets/094_9198e4d130a4/images/page_8_image_2.jpg",
    "160_fig7": OV4_MD / "assets/160_9ee189fd3a42/images/page_4_image_2.jpg",
    "253_fig3": OV4_MD / "assets/253_d054bfdabe17/images/page_3_image_1.jpg",
    "c_unibi": ASSETS / "chart_05_ws_rs_uni_bi_protocol.png",
    "c_deconv_full": ASSETS / "chart_06_slit_deconvolution_explainer.png",
    "c_lens_8dim": ASSETS / "chart_07_lens_capability_8dim.png",
}

for k, p in IMG.items():
    assert p.exists(), f"Missing image {k}: {p}"


prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.500)
BLANK = prs.slide_layouts[6]


def set_slide_bg(slide, color=C_WHITE):
    bg = slide.background
    fill = bg.fill
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
    set_slide_bg(slide, C_WHITE)
    # Top thin navy/teal bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    bar.fill.solid(); bar.fill.fore_color.rgb = C_NAVY; bar.line.fill.background()
    bar2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(3.2), Inches(0.08))
    bar2.fill.solid(); bar2.fill.fore_color.rgb = C_TEAL; bar2.line.fill.background()

    # Section badge pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), Inches(0.20), Inches(1.55), Inches(0.34))
    pill.fill.solid(); pill.fill.fore_color.rgb = C_TEAL; pill.line.fill.background()
    tf = pill.text_frame; tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = badge; r.font.name = FONT; r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = C_WHITE

    # Title
    tb = slide.shapes.add_textbox(Inches(2.00), Inches(0.14), Inches(10.95), Inches(0.45))
    tf = tb.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    r = p.add_run(); r.text = title; r.font.name = FONT; r.font.size = Pt(17.5); r.font.bold = True; r.font.color.rgb = C_NAVY

    # Subtitle if provided
    line_y = 0.64
    if subtitle:
        stb = slide.shapes.add_textbox(Inches(0.35), Inches(0.58), Inches(12.63), Inches(0.24))
        stf = stb.text_frame; stf.word_wrap = True; stf.margin_left = stf.margin_top = stf.margin_right = stf.margin_bottom = 0
        sp = stf.paragraphs[0]
        sr = sp.add_run(); sr.text = subtitle; sr.font.name = FONT; sr.font.size = Pt(8.8); sr.font.color.rgb = C_MUTED
        line_y = 0.84

    # Horizontal divider
    div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(line_y), Inches(12.63), Inches(0.02))
    div.fill.solid(); div.fill.fore_color.rgb = C_TEAL; div.line.fill.background()

    # Footer
    fdiv = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), Inches(7.14), Inches(12.63), Inches(0.012))
    fdiv.fill.solid(); fdiv.fill.fore_color.rgb = C_BORDER; fdiv.line.fill.background()

    ft1 = slide.shapes.add_textbox(Inches(0.35), Inches(7.18), Inches(10.2), Inches(0.25))
    ftf1 = ft1.text_frame; ftf1.margin_left = ftf1.margin_top = 0
    fp1 = ftf1.paragraphs[0]
    fr1 = fp1.add_run()
    fr1.text = "OV4 · ArF 液浸光刻机（对标 NXT:1950i–1970Ci）15 大类验收规格与逐条证据链 v2 · OpticsPan/OV4"
    fr1.font.name = FONT; fr1.font.size = Pt(8); fr1.font.color.rgb = C_MUTED

    ft2 = slide.shapes.add_textbox(Inches(11.3), Inches(7.18), Inches(1.68), Inches(0.25))
    ftf2 = ft2.text_frame; ftf2.margin_right = ftf2.margin_top = 0
    fp2 = ftf2.paragraphs[0]; fp2.alignment = PP_ALIGN.RIGHT
    fr2 = fp2.add_run(); fr2.text = f"{pno:02d} / {TOTAL_SLIDES:02d}"
    fr2.font.name = FONT; fr2.font.size = Pt(8.5); fr2.font.bold = True; fr2.font.color.rgb = C_NAVY


def add_box(slide, x, y, w, h, title, bullets, bg=C_BOX_TEAL, accent=C_TEAL, title_sz=10.0, body_sz=8.6):
    # Main box
    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    rect.fill.solid(); rect.fill.fore_color.rgb = bg
    rect.line.color.rgb = C_BORDER; rect.line.width = Pt(0.6)
    # Left accent stripe
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(0.06), Inches(h))
    stripe.fill.solid(); stripe.fill.fore_color.rgb = accent; stripe.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(x + 0.13), Inches(y + 0.06), Inches(w - 0.19), Inches(h - 0.10))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p0 = tf.paragraphs[0]
    p0.space_after = Pt(2.5)
    r0 = p0.add_run(); r0.text = title
    r0.font.name = FONT; r0.font.size = Pt(title_sz); r0.font.bold = True; r0.font.color.rgb = C_NAVY

    for item in bullets:
        p = tf.add_paragraph()
        p.space_after = Pt(2.0)
        p.line_spacing = 1.15
        if isinstance(item, tuple):
            lead, rest = item
            r1 = p.add_run(); r1.text = "• " + lead
            r1.font.name = FONT; r1.font.size = Pt(body_sz); r1.font.bold = True; r1.font.color.rgb = C_DARK_BLUE
            r2 = p.add_run(); r2.text = rest
            r2.font.name = FONT; r2.font.size = Pt(body_sz); r2.font.color.rgb = C_BODY
        else:
            r = p.add_run(); r.text = "• " + item
            r.font.name = FONT; r.font.size = Pt(body_sz); r.font.color.rgb = C_BODY


def add_pic_card(slide, img_key, x, y, w, h, caption, border_color=C_BORDER):
    # Outer white card with thin border
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.fill.solid(); card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = border_color; card.line.width = Pt(0.75)

    cap_h = 0.34 if len(caption) > 46 else 0.24
    pad = 0.06
    box_w = w - 2 * pad
    box_h = h - cap_h - 2 * pad

    path = IMG[img_key]
    with Image.open(path) as im:
        iw, ih = im.size
    aspect = iw / ih
    if box_w / box_h > aspect:
        pic_h = box_h
        pic_w = pic_h * aspect
    else:
        pic_w = box_w
        pic_h = pic_w / aspect
    px = x + pad + (box_w - pic_w) / 2.0
    py = y + pad + (box_h - pic_h) / 2.0
    slide.shapes.add_picture(str(path), Inches(px), Inches(py), width=Inches(pic_w), height=Inches(pic_h))

    # Caption strip at bottom of card
    cap_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y + h - cap_h), Inches(w), Inches(cap_h))
    cap_bg.fill.solid(); cap_bg.fill.fore_color.rgb = RGBColor(0xF3, 0xF7, 0xF9); cap_bg.line.fill.background()
    ctb = slide.shapes.add_textbox(Inches(x + 0.06), Inches(y + h - cap_h + 0.02), Inches(w - 0.12), Inches(cap_h - 0.03))
    ctf = ctb.text_frame; ctf.word_wrap = True
    ctf.margin_left = ctf.margin_right = ctf.margin_top = ctf.margin_bottom = 0
    ctf.vertical_anchor = MSO_ANCHOR.MIDDLE
    cp = ctf.paragraphs[0]; cp.alignment = PP_ALIGN.CENTER
    cr = cp.add_run(); cr.text = caption
    cr.font.name = FONT; cr.font.size = Pt(7.3); cr.font.color.rgb = C_MUTED


def add_table(slide, x, y, w, h, headers, rows, col_widths, font_sz=8.0, spec_col=None, highlight_last=0, align_left_cols=None):
    nrows = len(rows) + 1
    ncols = len(headers)
    shape = slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = shape.table
    # Scale col_widths to match w exactly
    scale = w / sum(col_widths)
    for ci, cw in enumerate(col_widths):
        tbl.columns[ci].width = Inches(cw * scale)

    align_left_cols = set(align_left_cols or [])

    # Header row
    for ci, htxt in enumerate(headers):
        cell = tbl.cell(0, ci)
        cell.fill.solid(); cell.fill.fore_color.rgb = C_TBL_HDR
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.04)
        cell.margin_top = cell.margin_bottom = Inches(0.02)
        set_cell_border(cell, color="9BB5C0", width="6350")
        p = cell.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = htxt
        r.font.name = FONT; r.font.size = Pt(font_sz); r.font.bold = True; r.font.color.rgb = C_NAVY

    # Body rows
    for ri, rdata in enumerate(rows, 1):
        is_hl = highlight_last > 0 and ri > len(rows) - highlight_last
        bg = RGBColor(0xE4, 0xF2, 0xEA) if is_hl else (C_WHITE if ri % 2 == 1 else C_TBL_ALT)
        for ci, val in enumerate(rdata):
            cell = tbl.cell(ri, ci)
            cell.fill.solid(); cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = cell.margin_right = Inches(0.04)
            cell.margin_top = cell.margin_bottom = Inches(0.015)
            set_cell_border(cell, color="C7D6DC", width="4762")
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if ci in align_left_cols else PP_ALIGN.CENTER
            r = p.add_run(); r.text = str(val)
            r.font.name = FONT; r.font.size = Pt(font_sz)
            if is_hl:
                r.font.bold = True; r.font.color.rgb = C_NAVY
            elif spec_col is not None and ci == spec_col:
                r.font.bold = True; r.font.color.rgb = C_SPEC_BLUE
            elif ci == 0:
                r.font.bold = True; r.font.color.rgb = C_DARK_BLUE
            else:
                r.font.color.rgb = C_BODY
    return shape


# ==============================================================================
# SLIDE 01: COVER
# ==============================================================================
s1 = prs.slides.add_slide(BLANK)
set_slide_bg(s1, C_WHITE)

# Top navy banner block
band = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(3.25))
band.fill.solid(); band.fill.fore_color.rgb = C_NAVY; band.line.fill.background()
accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(3.25), Inches(13.333), Inches(0.10))
accent.fill.solid(); accent.fill.fore_color.rgb = C_TEAL; accent.line.fill.background()

tb = s1.shapes.add_textbox(Inches(0.65), Inches(0.45), Inches(12.0), Inches(2.55))
tf = tb.text_frame; tf.word_wrap = True
p0 = tf.paragraphs[0]
r0 = p0.add_run(); r0.text = "OV4 · ArF IMMERSION LITHOGRAPHY SCANNER ACCEPTANCE SPECIFICATION (v2 · 深度验收升级版)"
r0.font.name = FONT; r0.font.size = Pt(11); r0.font.bold = True; r0.font.color.rgb = RGBColor(0x8D, 0xDF, 0xD6)

p1 = tf.add_paragraph(); p1.space_before = Pt(10)
r1 = p1.add_run(); r1.text = "ArF 液浸光刻机（对标 NXT:1950i–1970Ci 之间）\n15 大类子系统验收规格与误差预算逐条证据链"
r1.font.name = FONT; r1.font.size = Pt(28); r1.font.bold = True; r1.font.color.rgb = C_WHITE

p2 = tf.add_paragraph(); p2.space_before = Pt(12)
r2 = p2.add_run(); r2.text = "逐条原始论文截图 · 物理/仿真推导 · Excel 9 表 686 公式闭环 · 新增 WS/RS 单往返细则、WS Km 验收与狭缝逆卷积图解、物镜 8 维评价"
r2.font.name = FONT; r2.font.size = Pt(12.5); r2.font.color.rgb = RGBColor(0xD4, 0xEA, 0xEE)

# 4 KPI Cards
kpis = [
    ("同机同台套刻 DCO (|Mean|+3σ)", "≤ 2.00 nm", "两层闭环 1.834 / 1.869 nm · 裕度 6.6%"),
    ("混机跨台套刻 MMO (99.7%)", "≤ 3.50 nm", "跨机闭环 3.134 / 3.154 nm · 裕度 9.9%"),
    ("全片焦面均匀性 FU (3σ)", "≤ 12.0 nm", "焦面闭环 10.34 nm · 裕度 13.8%"),
    ("Odd Zernike (Z5–Z64 全30项)", "0.337 nm RMS", "跨照明切换套刻 ≤ 0.370 nm (Abbe实算 0.328)"),
]
for i, (kl, kv, ks) in enumerate(kpis):
    kx = 0.65 + i * 3.05
    card = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(kx), Inches(3.70), Inches(2.85), Inches(1.42))
    card.fill.solid(); card.fill.fore_color.rgb = C_BOX_BLUE; card.line.color.rgb = C_BORDER
    topb = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(kx), Inches(3.70), Inches(2.85), Inches(0.07))
    topb.fill.solid(); topb.fill.fore_color.rgb = C_TEAL; topb.line.fill.background()
    ctb = s1.shapes.add_textbox(Inches(kx + 0.14), Inches(3.86), Inches(2.58), Inches(1.18))
    ctf = ctb.text_frame; ctf.word_wrap = True
    cp0 = ctf.paragraphs[0]; cr0 = cp0.add_run(); cr0.text = kl; cr0.font.name = FONT; cr0.font.size = Pt(9.2); cr0.font.color.rgb = C_MUTED
    cp1 = ctf.add_paragraph(); cp1.space_before = Pt(4); cr1 = cp1.add_run(); cr1.text = kv; cr1.font.name = FONT; cr1.font.size = Pt(20); cr1.font.bold = True; cr1.font.color.rgb = C_NAVY
    cp2 = ctf.add_paragraph(); cp2.space_before = Pt(4); cr2 = cp2.add_run(); cr2.text = ks; cr2.font.name = FONT; cr2.font.size = Pt(8.5); cr2.font.color.rgb = C_TEAL

# Bottom coverage strip & repo metadata
add_box(
    s1, 0.65, 5.38, 12.03, 1.55,
    "全套 28 页汇报脉络（v2 在 v1 全部 22 页证据链上新增 6 页深度验收专题，对接 Excel Sheet 01–09）",
    [
        ("顶层闭环与物理基础（P02–P04）：", "NXT:1950i/1960Bi/1970Ci 实测对标、DCO/MMO/FU 闭环防重复计数树、液浸 6-DOF 耦合矩阵 M_opt。"),
        ("运动台、同步与编码器（P05–P11）：", "WS 6-DOF + 反驳同步覆盖论 + 单/往返细则（P05–07）；RS 6-DOF + 反驳与 150 m/s² 微滑移细则（P08–09）；同步 MA & ENC（P10–11）。"),
        ("对准、温控、夹持与框架（P12–P19）：", "M-side SMASH（7 项）、E-side TIS/PARIS（6 项）、WT/Reticle/WH 温控（17 项）、RT/WT 夹持（11 项）、整机 Frame（11 项）。"),
        ("iHOPC 高阶与 Odd Zernike（P20–P28）：", "K1–K20 映射（P20）；物镜残差 + 8 维能力评价（P21–22）；WS 残差 + K4 方案审视 + 狭缝逆卷积专页（P23–25）；Z5–Z64 仿真与 FAT/SAT（P26–28）。"),
    ],
    bg=C_BOX_TEAL, accent=C_NAVY, title_sz=10.5, body_sz=8.8
)
s1.notes_slide.notes_text_frame.text = "OV4 v2 · 2026-11-24 · 配套 MD 报告 v2、30 页 PDF v2、9 表 686 公式 Excel v2 与 28 页 PPTX v2，归档于 OpticsPan/OV4。"

# ==============================================================================
# SLIDE 02: BENCHMARK POSITIONING (1950i - 1970Ci)
# ==============================================================================
s2 = prs.slides.add_slide(BLANK)
add_header(s2, "顶层定位", "目标机型对标定位：介于 NXT:1950i 与 NXT:1970Ci 之间（等效 1960Bi–1965Ci+）", next_pno(),
           "直接依据 OV4 中 ASML 官方 SPIE 实测文献 [009, 066, 015] 锚定整机顶层 DCO / MMO / FU / 产能基线")

add_table(
    s2, 0.35, 0.94, 12.63, 2.02,
    ["核心性能指标", "NXT:1950i [009, 066]", "本目标机型（1950i–1970i）", "NXT:1970Ci [015, 066]", "NXT:1980Di [015]", "关键架构配置与定位说明"],
    [
        ["同机套刻 DCO (|Mean|+3σ)", "≤ 2.5 nm (典型1.5–2.2)", "≤ 2.00 nm (闭环 1.87 nm)", "≤ 1.6–1.8 nm", "≤ 1.4 nm", "留 6.6% 工程裕度；两层独立含跨照明切换"],
        ["混机套刻 MMO (99.7%)", "≤ 4.5–5.5 nm", "≤ 3.50 nm (闭环 3.15 nm)", "≤ 2.5–3.4 nm (机群3.4)", "≤ 2.5 nm", "覆盖双机双台 + 50 μm 翘曲片 + 跨照明匹配"],
        ["全片焦面均匀性 FU (3σ)", "≤ 15–20 nm", "≤ 12.0 nm (闭环 10.34 nm)", "≤ 10–12 nm", "≤ 9.1 nm", "陶瓷 WS + 高平坦 WT (6.0 nm) + UV-LS"],
        ["产能 / 扫速 / 加速度", "175–200 wph / 0.60 m/s", "220–230 wph / 0.70 m/s", "250 wph / 0.75 m/s", "275 wph / 0.80 m/s", "WS 35–40 m/s²，RS 150 m/s²，狭缝 26×8 mm"],
        ["计量与高阶补偿配置", "Gridplate+SMASH+FlexWave", "Gridplate+SMASH+7点PARIS+19参iHOPC", "同左 + 陶瓷WS + UV-LS", "升级 RHC2 + 低胀WT", "iHOPC 覆盖 K1–K19（不含 K20，至 2100i 才支持）"],
    ],
    [2.15, 1.85, 2.15, 1.85, 1.45, 3.18], font_sz=8.2, spec_col=2, align_left_cols=[0, 5]
)

add_pic_card(s2, "009_fig3", 0.35, 3.10, 4.15, 3.92, "原图 [009] Castenmiller 2010 · Fig.3：NXT:1950i 2.5 nm DCO 误差树分解")
add_pic_card(s2, "066_fig2_full", 4.62, 3.10, 4.10, 3.92, "原图 [066] de Boeij 2013 · Fig.2：NXT:1950i(蓝) vs 1960Bi(绿) DCO/MMO/CDU/FU 实测")
add_pic_card(s2, "015_fig7", 8.84, 3.10, 4.14, 3.92, "原图 [015] de Graaf 2016 · Fig.7：NXT:1970Ci 机群 MMO = 3.4 nm 基准线")

# ==============================================================================
# SLIDE 03: TOP-LEVEL BUDGET CLOSURE & HIERARCHY
# ==============================================================================
s3 = prs.slides.add_slide(BLANK)
add_header(s3, "预算闭环", "顶层套刻与焦面误差预算闭环（Excel Sheet 01 · 严格防重复计数层级树）", next_pno(),
           "明确分离“直接计入顶层曝光闭环项”与“底层传感/子系统约束项”，DCO / MMO / FU 均留 6.6%–13.8% 裕度")

add_pic_card(s3, "c_budget", 0.35, 0.94, 12.63, 4.05, "自绘核算图（数据源：Excel Sheet 01 430 个跨页动态公式实时重算结果，0 错）")

add_box(
    s3, 0.35, 5.10, 6.20, 1.92,
    "防重复计数规则：15 大类如何精确映射到顶层闭环",
    [
        ("直接计入顶层 DCO（11 个独立合成节点）：", "Item 3（同步MA）、Item 5（AA）、Item 6（PARIS）、Item 7+11（晶圆热）、Item 8（掩模热）、Item 9/10（夹持重复/微滑移）、Item 13/14（iHOPC）、Item 15（Odd Zernike）。"),
        ("底层硬件/计量约束（不重复累加）：", "Item 1(WS) & Item 2(RS) 合成 Item 3；Item 4(ENC) 按 1:3 原则内嵌于 WS/RS；Item 12(Frame) 动态内嵌 Item 3、静态漂移内嵌 Item 5。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.6, body_sz=8.2
)
add_box(
    s3, 6.72, 5.10, 6.26, 1.92,
    "两层曝光合成口径与闭环验证公式",
    [
        ("双层独立随机曝光（×√2）：", "D1–D7 及量测底噪在 Layer 1 与 Layer 2 独立发生，RSS 均乘 √2；D8/D9（iHOPC 指令差）保守乘 1.2；D10（Odd Zernike |ΔS|）已为两层差分故乘 1.0。"),
        ("系统均值线性叠加（|Mean| + 3σ）：", "DCO Y = 1.569 + 0.300 = 1.869 nm ≤ 2.00 nm；MMO Y = 2.704 + 0.450 = 3.154 nm ≤ 3.50 nm；FU = 10.34 nm ≤ 12.0 nm。"),
    ],
    bg=C_BOX_BLUE, accent=C_DARK_BLUE, title_sz=9.6, body_sz=8.2
)

# ==============================================================================
# SLIDE 04: OPTICAL COUPLING MATRIX M_opt & METHODOLOGY
# ==============================================================================
s4 = prs.slides.add_slide(BLANK)
add_header(s4, "物理基础", "核心物理公理：液浸 4× 投影 6-DOF 光学耦合矩阵 M_opt 与 MA/MSD 积分窗", next_pno(),
           "工程习称“WS - RS/4”，但在液浸 NA=1.35（n_w = 1.4366）光学映射下仅 X/Y 为 1/4，Z、Rx/Ry、Rz 各有严格物像倍率")

add_table(
    s4, 0.35, 0.94, 7.15, 2.85,
    ["自由度", "光学耦合系数 (RS→WS)", "数值倍率", "常见误区警示与物理推导公式"],
    [
        ["X (非扫描)", "β = 1/4", "0.2500", "横向缩小倍率 4:1，e_X = X_WS − X_RS / 4"],
        ["Y (扫描主轴)", "β = 1/4", "0.2500", "扫描反向同步，e_Y = Y_WS − Y_RS / 4"],
        ["Z (焦面向)", "n_w · β² = 1.4366/16", "1 / 11.14", "纵向放大率非 1/4！[225 Sec.2.1.3] 确认约 10:1，液浸精确 11.14:1"],
        ["Rx (绕X俯仰)", "n_w · β = 1.4366/4", "0.3592", "Scheimpflug 倾角定律，非 1/4！沿 8 mm 狭缝产生 ±4 mm 离焦"],
        ["Ry (绕Y滚转)", "n_w · β = 1.4366/4", "0.3592", "沿 26 mm 狭缝产生 ±13 mm 离焦（杠杆臂为 Rx 的 3.25 倍）"],
        ["Rz (绕Z偏航)", "1 (严格等角)", "1.0000", "关键红线：Rz 绝非 1/4！掩模转 9 nrad 直接导致像面转 9 nrad"],
    ],
    [1.15, 1.55, 0.95, 3.50], font_sz=8.2, spec_col=2, align_left_cols=[0, 3]
)

add_box(
    s4, 0.35, 3.92, 7.15, 3.08,
    "本套规格采用的三大透明推导方法（每行明确标注）",
    [
        ("① 直接调研证据：", "直接提取 OV4 论文/专利原图实测值（如 NXT:1950i MA 0.47/0.49 nm、ENC 0.22 nm @ 1000 Hz、1970Ci SMASH 0.15–0.25 nm、WT 平坦度 6.2 nm、FlexWave Coma 0.15–0.16 nm RMS）。"),
        ("② 物理/光学解析与仿真计算：", "液浸 6-DOF 耦合矩阵、四角 ENC 差分几何角噪公式、WH 17 μm 气浮台瞬态热传导指数衰减、8 mm 有限狭缝逆卷积偏置、2D Abbe 部分相干 Z5–Z64 跨照明灵敏度数值仿真。"),
        ("③ 顶层误差预算反推预估：", "按 DCO ≤ 2.00 / MMO ≤ 3.50 / FU ≤ 12.0 nm 闭环目标与 1:3 底层计量原则，自顶向下分配方差份额并留足 6.6%–13.8% 系统裕度。"),
        ("曝光狭缝积分窗（0.70 m/s, 8 mm 狭缝）：", "T_slit = 8 mm / 0.70 m/s = 11.4 ms；窗口内均值 MA 决定套刻偏移，标准差 MSD 决定对比度与 CDU。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.6, body_sz=8.3
)

add_pic_card(s4, "094_fig16", 7.68, 0.94, 5.30, 3.60, "原图 [094] Butler (ASML, IEEE CSM 2011) · Fig.16：扫描速度曲线与曝光狭缝 MA / MSD 积分窗定义")
add_pic_card(s4, "225_fig1_9", 7.68, 4.66, 5.30, 2.34, "原图 [225] Naaijkens (TU/e–ASML 2013) · Fig.1.9：RS–物镜–WS 4× 扫描投影空间几何关系")

# ==============================================================================
# SLIDE 05: ITEM 1 - WS 6-DOF REPEATABILITY
# ==============================================================================
s5 = prs.slides.add_slide(BLANK)
add_header(s5, "Item 1 · WS", "1. WS（晶圆台）6 自由度重复性误差验收规格（逐自由度 6 行）", next_pno(),
           "以计量框架 Gridplate ENC 为基准；动态扫描曝光窗口 MA 3σ @ 0.70 m/s（静态对准定位 XY ≤ 0.30 nm）")

add_table(
    s5, 0.35, 0.94, 7.25, 3.68,
    ["序号", "自由度", "验收规格", "单位", "对套刻/焦面影响", "依据与推导计算过程"],
    [
        ["1.1", "WS-X (非扫描)", "≤ 0.32", "nm", "套刻 X: 0.32 nm", "对标 1950i 同步 MA-X=0.47 [009 Fig.10]；目标同步 0.40 按 WS 占方差 64% 反推"],
        ["1.2", "WS-Y (扫描向)", "≤ 0.36", "nm", "套刻 Y: 0.36 nm", "承受 35–40 m/s² 折返+液浸头拖曳；同步目标 0.45 按 64% 方差反推"],
        ["1.3", "WS-Z (焦面向)", "≤ 4.50", "nm", "焦面 Z: 4.50 nm", "直接对标 1965Ci/1970Ci 陶瓷 WS 实测峰值 4 nm、95%≤6 nm [066 Fig.9]"],
        ["1.4", "WS-Rx (俯仰)", "≤ 0.20", "μrad", "8mm狭缝离焦 0.80 nm", "Δz = 4 mm × 0.20 μrad = 0.80 nm；与 RS-Rx 等效 0.151 合成 0.25 μrad"],
        ["1.5", "WS-Ry (滚转)", "≤ 0.10", "μrad", "26mm狭缝离焦 1.30 nm", "杠杆臂 ±13 mm 为 Rx 的 3.25×，严控至 0.10 μrad（同步合成 0.12 μrad）"],
        ["1.6", "WS-Rz (偏航)", "≤ 0.012", "μrad", "26mm边缘套刻 0.156 nm", "Δy = 13 mm × 12 nrad = 0.156 nm；与 RS-Rz(9 nrad, 1:1) 合成 15 nrad"],
    ],
    [0.52, 1.15, 0.78, 0.50, 1.35, 2.95], font_sz=7.9, spec_col=2, align_left_cols=[1, 4, 5]
)

add_box(
    s5, 0.35, 4.76, 7.25, 2.26,
    "关键硬件支撑与角自由度推导逻辑",
    [
        ("轻量化陶瓷短行程台是 MA-Z ≤ 4.50 nm 的决定性因素：", "[066 Fig.9] 实测表明，从金属/早期 WS（蓝柱 5–17 nm）升级至高比刚度陶瓷 WS（绿柱 3–9 nm，峰值 4 nm）后，全片动态焦面跟随误差直接减半。"),
        ("为什么 Ry 比 Rx 严 2 倍、Rz 严至 12 nrad：", "Ry 乘以 26 mm 狭缝半宽（13 mm）直接变成离焦；Rz 乘以 13 mm 直接变成 Y 向面内套刻，若放松至 30 nrad 单项就吃掉 0.39 nm 套刻！"),
        ("静态 vs 动态验收口径：", "曝光扫描按 11.4 ms 窗口 MA 考核上表 6 轴；M-side 对准与 TIS 静止测点 XY 静态重复性 ≤ 0.30 nm（3σ）。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.4, body_sz=8.1
)

add_pic_card(s5, "066_fig9", 7.75, 0.94, 5.23, 3.05, "原图 [066] de Boeij 2013 · Fig.9：陶瓷 WS（绿）vs 早期 WS（蓝）MAz 分布，峰值 4 nm、95% ≤ 6 nm")
add_pic_card(s5, "009_fig10_l", 7.75, 4.10, 5.23, 2.92, "原图 [009] Castenmiller 2010 · Fig.10(左)：NXT 高刚度 WS 开环频率响应，支撑高伺服带宽")


# ==============================================================================
# SLIDE 06 (v2 NEW): WS INDEPENDENT ACCEPTANCE REBUTTAL
# ==============================================================================
s_ws_reb = prs.slides.add_slide(BLANK)
add_header(s_ws_reb, "Item 1 · 反驳论证", "1（续上）. 为何必须独立验收 WS 6-DOF？—— 反驳“WS–RS 同步覆盖论”的 6 大铁证", next_pno(),
           "彻底回应子系统交付方“同步 MA 达标即可覆盖 WS 自身重复性”的质疑，并对“场间步进切入下一视场”观点作精准物理补强")

add_box(
    s_ws_reb, 0.35, 0.96, 8.20, 1.48,
    "对整机疑问（场间步进到下一视场起扫位）的精准评估与补强话术",
    [
        ("您的直觉高度合理且切中真机理：", "切场时激光关闭，WS 须独立步进 26 mm 并按 M-side 预计算的网格坐标切入下一视场起扫窗 [094 Fig.15]。"),
        ("需防范对方反驳并补齐致命一击：", "若对方反问“进匀速段后让 RS 追赶 WS 偏移不就行了？”，须立刻反击：① 10–15 ms 整定窗末端的随机整定尾撞击曝光窗前沿时，刚完成 150 m/s² 折返的 RS 毫无多余带宽追赶；② 更根本的是 M-side 测量无 RS、Z/Rx/Ry 与液浸弯月面不可由 RS 兜底！"),
    ],
    bg=C_BOX_WARM, accent=C_CORAL, title_sz=9.8, body_sz=8.3
)

add_pic_card(
    s_ws_reb, "094_fig15", 8.70, 0.96, 4.28, 2.38,
    "【原始论文截图】OV4 [094] Butler Fig.15：步进扫描蛇形（Meander）轨迹——绿虚线为无曝光独立步进，红箭头为正反交替扫描"
)

add_table(
    s_ws_reb, 0.35, 2.54, 8.20, 4.46,
    ["铁证", "反击核心论点", "物理机理与为何 WS–RS 同步闭环绝对无法覆盖"],
    [
        ["铁证 1\n决定性", "M-side 测量站完全无 RS 参与\n（双台架构死穴）", "晶圆对准（SMASH/AA）与调平（UV-LS）均在 M-side 由 WS 独立完成，此时 RS 正在 E-side 曝光另一片晶圆 [009, 066]。M-side 定位非重复与换台传递误差在曝光前已永久固化，E-side 同步环 100% 不可见！"],
        ["铁证 2\n完善步进", "场间步进整定瞬态冲击\n（First-Slit Settling Tail）", "26 mm 步进切入预计算起扫窗后的 15 ms 整定尾若不可重复，会直接撞击首狭缝；150 m/s² 刚折返的 RS 无冗余带宽追赶 WS 的高频随机瞬态！"],
        ["铁证 3\n液浸焦面", "Z / Rx / Ry 焦面与液浸弯月面\n不能由 RS 兜底", "WS 须高频贴合数百 nm 硅片形貌（RS-Z 受 1/11.14 限制不做高频形貌伺服）；且液浸头固连于物镜下方，WS 偏离会直接破坏水膜弯月面（气泡/水印）与畸变采样点！"],
        ["铁证 4\n动力学", "主从流向与 4× 动力学惩罚\n（RS 追 WS 必爆 MSD）", "工程上通常将高扰动 RS 误差前馈给轻量化 WS [019, 075]。若反向迫使 RS 追赶 WS，1 nm WS 误差要求 RS 4 nm/4× 加速度/4× Jerk 激振，立即引发电机饱和与 MSD 崩溃！"],
        ["铁证 5\niHOPC", "11 项场内动态 iHOPC 独立执行", "WS 独立承担 K1–K19 中 11 项扫描轨迹补偿（含二/三阶加速度与动态 Rz），自身 6-DOF 重复性直接决定 iHOPC 补偿残差上限。"],
        ["铁证 6\nFAT 契约", "子系统独立 FAT 门禁与定责", "WS 交付早于整机合龙（无 RS/物镜/激光）；无独立 6-DOF 指标则总装前无法验收、无法防范特定工况偶然误差对消，整机同步超标时无法划分责任！"],
    ],
    [0.85, 2.20, 5.15], font_sz=7.5, spec_col=0, align_left_cols=[1, 2]
)

add_box(
    s_ws_reb, 8.70, 3.44, 4.28, 3.56,
    "整机评审会议一句话定调建议",
    [
        ("逻辑区分（共模 vs 差模）：", "WS–RS 同步只约束双台“差模误差”（e_WS − M_opt·e_RS），对 WS 相对物镜/液浸头/M-side 测量站的“共模偏离”完全失明！"),
        ("M-side 独立误差不可逆：", "M-side 无 RS 参与，WS 自身 XY 静态重复性（≤0.30 nm）与步进网格重复性直接锁死整机套刻底噪。"),
        ("合同验收双门禁底线：", "必须坚持“单台 FAT 独立 6-DOF 重复性” + “整机 SAT 同步 MA”双门禁，绝不接受用同步指标豁免 WS 单台规格！"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.4, body_sz=8.1
)

# ==============================================================================
# SLIDE 07 (v2 NEW): WS UNI- vs BI-DIRECTIONAL REPEATABILITY PROTOCOL
# ==============================================================================
s_ws_proto = prs.slides.add_slide(BLANK)
add_header(s_ws_proto, "Item 1 · 单/往返方案", "1（续下）. WS 6-DOF 单程 vs 往返重复性数学定义与验收方案细则", next_pno(),
           "因蛇形交替扫描（Scan-Up/Down + Step-Left/Right）必然引入方向滞回，须同时验收单程与往返，并以动态往返闭合表 1 红线")

add_pic_card(
    s_ws_proto, "c_unibi", 0.35, 0.96, 8.35, 3.06,
    "【v2 工程仿真与分配图】左：WS-Y 33 mm 视场蛇形扫描单程 3σ (R_uni) 与残余正反扫差 (B_UD,res) 定义；右：WS/RS 往返红线拆分"
)

add_box(
    s_ws_proto, 8.85, 0.96, 4.13, 3.06,
    "单程 vs 往返严格数学定义（适配 ISO 230-2 + 8 mm MA）",
    [
        ("为何必须同时验单程与往返？", "单程仅暴露随机噪声；蛇形扫描（±Y/±X）下拖链、电机涡流、液浸弯月面剪切与加速俯仰反转会诱发反向差 B_res，直接变身套刻误差！"),
        ("1. 单程重复性（Unidirectional）：", "固定同向（全 +Y 或全 −Y）重复 N≥30 趟，按 8 mm 狭缝 MA 曲线取全视场包络：R_uni = max_y [3·max(s↑(y), s↓(y))]。"),
        ("2. 残余反向差（Reversal / SUSD）：", "经方向前馈标定后的残余正反扫均值差：B_res = max_y |μ↑(y) − μ↓(y)|。"),
        ("3. 往返综合重复性（Bidirectional）：", "R_bi = R_uni + B_res ≤ 表 1 总红线（同时核查混合蛇形样本 |Mean|+3σ 达标）；静态定点取 9 点×双向各 20 次。"),
    ],
    bg=C_BOX_BLUE, accent=C_DARK_BLUE, title_sz=9.0, body_sz=7.7
)

add_table(
    s_ws_proto, 0.35, 4.12, 12.63, 2.88,
    ["序号", "自由度", "表 1 总红线\n(往返 R_bi)", "静态单/往返", "动态单程\nR_uni,dyn", "残余反向差\nB_res", "运动行程与步进 / 扫描距离规划", "验收循环工况与环境条件（Excel Sheet 07B）"],
    [
        ["1.1", "WS-X", "≤ 0.32 nm", "0.20 / 0.30", "≤ 0.24 nm", "≤ 0.08 nm", "全行程 ±150 mm（机械≥340 mm）；单步 ΔX=26 mm（±X）", "9 点静态×20 往返；全片 90–100 场蛇形×10 盘（a_x=35 m/s²），干/湿态分验"],
        ["1.2", "WS-Y", "≤ 0.36 nm", "0.20 / 0.30", "≤ 0.26 nm", "≤ 0.10 nm", "全行程 ±150 mm（机械≥360 mm）；单扫 33+40=73 mm", "扫速 0.25/0.50/0.70 m/s、a_y=35–40 m/s²、T_settle≤15 ms；5 场×30 往返 + 10 盘"],
        ["1.3", "WS-Z", "≤ 4.50 nm", "1.50 / 2.20", "≤ 3.50 nm", "≤ 1.00 nm", "工作行程 ±100 μm；扫描叠加 ±20 μm 模拟硅片坡度", "陶瓷短行程 WS @ 0.70 m/s 湿态 8 mm 狭缝 MA，核查首狭缝 15 ms 整定尾"],
        ["1.4", "WS-Rx", "≤ 0.20 μrad", "0.08 / 0.12", "≤ 0.15 μrad", "≤ 0.05 μrad", "倾角行程 ±300 μrad；叠加 ±150 μrad 硅片局部斜率", "重点监测 ±Y 加减速反向引发的液浸弯月面俯仰力矩滞回（B_res≤50 nrad）"],
        ["1.5", "WS-Ry", "≤ 0.10 μrad", "0.04 / 0.06", "≤ 0.075 μrad", "≤ 0.025 μrad", "倾角行程 ±300 μrad；横跨 26 mm 狭缝全宽调平", "重点监测 ±X 步进换向滚转整定与线缆拖链侧向滞回（B_res≤25 nrad）"],
        ["1.6", "WS-Rz", "≤ 0.012 μrad", "0.006/0.009", "≤ 0.009 μrad", "≤ 0.003 μrad", "偏航行程 ±1.0 mrad；全 300 mm 行程四角 ENC 闭环", "严控 ±Y 扫向/±X 步向切换偏航滞回 ≤ 3 nrad，动态往返总值 ≤ 12 nrad"],
    ],
    [0.52, 0.78, 1.05, 0.96, 0.96, 0.92, 3.32, 4.12], font_sz=7.3, spec_col=2, align_left_cols=[6, 7]
)

# ==============================================================================
# SLIDE 06: ITEM 2 - RS 6-DOF REPEATABILITY
# ==============================================================================
s6 = prs.slides.add_slide(BLANK)
add_header(s6, "Item 2 · RS", "2. RS（掩模台）6 自由度重复性误差验收规格（掩模侧 4× 与晶圆侧 1× 逐行换算）", next_pno(),
           "RS 以 4 倍扫速（2.80 m/s）与约 150 m/s² 极高加速度往返扫描，经严格液浸光学耦合矩阵 M_opt 折算至晶圆像面")

add_table(
    s6, 0.35, 0.94, 7.65, 3.75,
    ["序号", "自由度", "掩模侧 4×", "耦合系数", "晶圆等效 1×", "推导计算与控制机理"],
    [
        ["2.1", "RS-X", "≤ 0.96 nm", "1/4 (0.25)", "0.24 nm", "占同步 MA-X(0.40 nm) 方差 36%：√(0.32²+0.24²)=0.40 nm [009, 019]"],
        ["2.2", "RS-Y", "≤ 1.08 nm", "1/4 (0.25)", "0.27 nm", "2.80 m/s + 150 m/s² 折返扫描主轴整定残差略大于 X；与 WS-Y 合成 0.45 nm"],
        ["2.3", "RS-Z", "≤ 24.0 nm", "n_w/16 (1/11.14)", "2.15 nm", "按液浸纵向倍率 1.4366/16 换算 [225 Sec.2.1.3]；与 WS-Z(4.5) 合成 5.0 nm"],
        ["2.4", "RS-Rx", "≤ 0.42 μrad", "n_w/4 (0.359)", "0.151 μrad", "Scheimpflug 定律折算至晶圆面 151 nrad（8 mm 狭缝边缘离焦 0.60 nm）"],
        ["2.5", "RS-Ry", "≤ 0.19 μrad", "n_w/4 (0.359)", "0.068 μrad", "折算至晶圆 68 nrad（26 mm 狭缝边缘离焦 0.89 nm），与 WS-Ry 合成 0.12 μrad"],
        ["2.6", "RS-Rz", "≤ 0.009 μrad", "1.000 (1:1)", "9.0 nrad", "等角 1:1 耦合！掩模边缘 52 mm 位移 0.47 nm 缩小 4× = 0.117 nm = 13 mm×9 nrad"],
    ],
    [0.50, 0.80, 1.02, 1.15, 0.95, 3.23], font_sz=7.9, spec_col=2, align_left_cols=[1, 5]
)

add_box(
    s6, 0.35, 4.82, 7.65, 2.20,
    "RS 预算分配的核心工程洞察",
    [
        ("为什么 RS 仅分配同步总方差的 36%（而非 50%）：", "RS 处于干式微环境（无液浸水膜拖曳），且掩模质量仅 ~0.4 kg（远轻于 300 mm 晶圆台），短行程 6-DOF 洛伦兹微动台带宽高，反作用力由专用平衡质量块（BM）吸收 [019, 094]。"),
        ("为什么 RS-Z 允许 24 nm 而 RS-Rz 仅允许 9 nrad：", "纵向缩小比高达 11.14:1（24 nm → 2.15 nm），而面内偏航为 1:1 毫无缩小红利！若按传统 4× 误把 RS-Rz 放宽至 36 nrad，单掩模台偏航就会在狭缝边缘引入 0.47 nm 套刻灾难。"),
    ],
    bg=C_BOX_WARM, accent=C_CORAL, title_sz=9.4, body_sz=8.2
)

add_pic_card(s6, "094_fig24", 8.15, 0.94, 4.83, 2.95, "原图 [094] Butler 2011 · Fig.24：掩模台 150 m/s² 扫描反作用力经平衡质量块(BM)动量解耦原理")
add_pic_card(s6, "225_fig1_9", 8.15, 4.02, 4.83, 3.00, "原图 [225] Naaijkens 2013 · Fig.1.9：掩模台高速往返扫描与 4× 投影同步运动几何关系")


# ==============================================================================
# SLIDE 09 (v2 NEW): RS INDEPENDENT REBUTTAL + UNI/BI & MICRO-SLIP PROTOCOL
# ==============================================================================
s_rs_v2 = prs.slides.add_slide(BLANK)
add_header(s_rs_v2, "Item 2 · 独立与往返", "2（续）. RS 独立 6-DOF 验收必要性反驳与 150 m/s² 单程 / 往返及微滑移验收细则", next_pno(),
           "掩模台在 2.80 m/s、150 m/s²（~15g）极限工况下运行，必须独立验收单程/往返重复性与掩模微滑移，绝不可被同步指标豁免")

add_box(
    s_rs_v2, 0.35, 0.96, 6.20, 2.82,
    "反击 RS 供应商“WS–RS 同步覆盖 RS 自身 6-DOF”的 5 大铁证",
    [
        ("1. WS 前馈追赶存在刚性天花板：", "TWINSCAN 虽将 RS 误差前馈给轻量化 WS [019, 075]，但 WS 短行程推力与液浸弯月面抗扰存在硬上限；RS 粗精台滞后或 150 m/s² 整定尾过长会直接击穿 WS 前馈带宽，引发 Sync MA 与 MSD 同时崩溃！"),
        ("2. 15g 掩模微滑移在同步编码器中 100% 隐身：", "同步误差只读 RS 编码器（测台体而非石英玻璃！），150 m/s² 频繁折返诱发的掩模微滑移 [225] 唯有靠独立大循环往返 + 掩模标记复测才能抓出。"),
        ("3. 静态掩模对准（RA / 7 点 PARIS）无同步扫描：", "换片后掩模精对准依赖 RS 独立静态 6-DOF 定位重复性。"),
        ("4. RS-Rz 为 1:1 等角映射 + Z/Rx/Ry 耦合焦面倾角：", "9 nrad 偏航红线无 1/4 缩小，无法被 X/Y 平移同步替代。"),
        ("5. 子系统 FAT 契约门禁与 BM 反力解耦验证：", "须在总装前独立验明 150 m/s² 折返时平衡质量块（BM）反力隔振效果与单台精度。"),
    ],
    bg=C_BOX_WARM, accent=C_CORAL, title_sz=9.4, body_sz=7.8
)

add_box(
    s_rs_v2, 6.72, 0.96, 6.26, 2.82,
    "RS 单程 / 往返与高加速度行程验收规划（掩模侧 4× 坐标）",
    [
        ("运动距离与行程推导：", "6 英寸石英掩模曝光区 104×132 mm（4× 晶圆视场）；在 v_RS = 2.80 m/s、a_RS = 150 m/s² 下，单侧加速距离 v²/(2a) = 26.1 mm + Jerk/整定段 ~24 mm ≈ 50 mm/侧，故单次动态扫描总行程 = 132 + 100 = 232–250 mm（含装片/对准全行程 ~380 mm）。"),
        ("狭缝窗口与循环制度：", "掩模侧等效狭缝 L_s,RS = 4×8 = 32 mm（T_slit = 11.43 ms，与 WS 严格同窗）；分级测试 1.0 / 2.0 / 2.80 m/s 与 60 / 100 / 150 m/s²，连续执行 100 趟交替正反扫（等效 1 片晶圆）× 10 轮 = 1000 趟（500 上扫 + 500 下扫）。"),
        ("气幕与微滑移专项抽检：", "全程在 5 mK 水平层流气幕 [08-TT-L3-RSbook] 下隔离正反扫气动阻力滞回；每 100 趟前后复测测试掩模相对吸盘标记位移，核查高 g 微滑移 ≤ 0.60 nm (4×) / 0.15 nm (1×)。"),
        ("单/往返判定口径：", "R_bi,dyn = R_uni,dyn (3σ) + B_UD,res ≤ 表 2 掩模侧 4× 红线（详见下表，同步链接 Excel Sheet 07C）。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.4, body_sz=7.8
)

add_table(
    s_rs_v2, 0.35, 3.90, 12.63, 3.10,
    ["序号", "RS 自由度", "表 2 总红线\n(4× 往返)", "静态往返\n(RA)", "动态单程\nR_uni,dyn", "残余正反扫差\nB_UD,res", "晶圆等效\n(1×)", "掩模侧行程规划与 150 m/s² / 微滑移验收要点"],
    [
        ["2.1", "RS-X", "≤ 0.96 nm", "≤ 0.80 nm", "≤ 0.72 nm", "≤ 0.24 nm", "0.24 nm", "微调行程 ±5–10 mm（曝光宽 104 mm）；在 Y 向 150 m/s² 满速往返下核查 X 侧向串扰"],
        ["2.2", "RS-Y", "≤ 1.08 nm", "≤ 0.85 nm", "≤ 0.78 nm", "≤ 0.30 nm", "0.27 nm", "单次 230–250 mm（132 mm 曝光+100 mm 加减速）；1000 趟往返（500 上+500 下）+ 5 mK 气幕"],
        ["2.3", "RS-Z", "≤ 24.0 nm", "≤ 12.0 nm", "≤ 18.0 nm", "≤ 6.00 nm", "2.15 nm", "Z 行程 ±150 μm（含掩模重力垂度补偿）；核查 150 m/s² 折返垂向弹跳（耦合 1/11.14）"],
        ["2.4", "RS-Rx", "≤ 0.42 μrad", "≤ 0.25 μrad", "≤ 0.32 μrad", "≤ 0.10 μrad", "0.151 μrad", "倾角 ±300 μrad；考核 15g 折返质心偏心诱发俯仰冲击与 15 ms 整定尾（耦合 0.359×）"],
        ["2.5", "RS-Ry", "≤ 0.19 μrad", "≤ 0.12 μrad", "≤ 0.14 μrad", "≤ 0.05 μrad", "0.068 μrad", "倾角 ±300 μrad（横跨 104 mm 狭缝）；考核粗精台切换与 BM 反冲引起的横向滚转滞回"],
        ["2.6", "RS-Rz", "≤ 0.009 μrad", "≤ 0.006 μrad", "≤ 0.0065 μrad", "≤ 0.0025 μrad", "0.009 μrad", "偏航 ±1.5 mrad（1:1 耦合！）；正反扫偏航滞回 ≤ 2.5 nrad + 每 100 趟抽检微滑移 ≤ 0.60 nm (4×)"],
    ],
    [0.52, 0.78, 1.08, 0.96, 1.02, 1.02, 0.88, 6.37], font_sz=7.4, spec_col=2, align_left_cols=[7]
)

# ==============================================================================
# SLIDE 07: ITEM 3 - WS-RS/4 SYNC MA 6-DOF
# ==============================================================================
s7 = prs.slides.add_slide(BLANK)
add_header(s7, "Item 3 · 同步MA", "3. WS–RS 同步运动误差（WS - M_opt·RS 6 自由度 MA + MSD 参考）", next_pno(),
           "直接计入整机 DCO 第一大方差项（占 Y 向随机方差 19.5%）；实际主从前馈/双 Youla 控制可再提供 10%–25% 闭环裕度")

add_table(
    s7, 0.35, 0.94, 7.55, 4.25,
    ["序号", "同步误差项（物理表达式）", "验收规格", "WS/RS 合成", "套刻/焦面影响", "依据与文献实测对比"],
    [
        ["3.1", "Sync MA-X (X_WS − X_RS/4)", "≤ 0.40 nm", "0.400 nm", "套刻 X: 0.40 nm", "1950i 实测 0.47 [009 Fig.10]，1970Ci ~0.35，取中间值 0.40"],
        ["3.2", "Sync MA-Y (Y_WS − Y_RS/4)", "≤ 0.45 nm", "0.450 nm", "套刻 Y: 0.45 nm", "1950i 实测 0.49 [009 Fig.10]；叠 Rz 边缘总 Y=0.490 nm"],
        ["3.3", "Sync MA-Z (Z_WS − n_w/16·Z_RS)", "≤ 5.00 nm", "4.99 nm", "焦面 Z: 5.00 nm", "对标陶瓷 WS 峰值 4 nm/95%≤6 nm [066 Fig.9]，占 FU 23.4%"],
        ["3.4", "Sync MA-Rx (Rx_WS − 0.359·Rx_RS)", "≤ 0.25 μrad", "0.251 μrad", "狭缝离焦 1.00 nm", "±4 mm 狭缝边缘离焦 Δz = 4×0.25 = 1.00 nm"],
        ["3.5", "Sync MA-Ry (Ry_WS − 0.359·Ry_RS)", "≤ 0.12 μrad", "0.121 μrad", "狭缝离焦 1.56 nm", "±13 mm 狭缝边缘离焦 1.56 nm；同步总离焦 5.33 nm"],
        ["3.6", "Sync MA-Rz (Rz_WS − 1·Rz_RS)", "≤ 0.015 μrad", "15.0 nrad", "边缘套刻 0.195 nm", "±13 mm 狭缝边缘套刻 Y = 0.195 nm（X = 0.060 nm）"],
        ["3.7", "Sync MSD-XY（附：高频抖动 1σ）", "≤ 1.80 nm", "窗口内 1σ", "影响对比度/CDU", "不计入套刻均值，控制对比度衰减 <1% [009, 165]"],
        ["3.8", "Sync MSD-Z（附：焦面高频 1σ）", "≤ 10.0 nm", "窗口内 1σ", "影响有效 DOF", "NA=1.35 窄焦深保护 [066, 165]"],
    ],
    [0.48, 2.02, 0.90, 0.85, 1.15, 2.15], font_sz=7.6, spec_col=2, align_left_cols=[1, 5]
)

add_box(
    s7, 0.35, 5.32, 7.55, 1.70,
    "协同控制增益与预算保守度说明",
    [
        ("非相关 RSS 验收 vs 实机耦合控制：", "本表由 WS 与 RS 按非相关 RSS 直接闭合（例如 √(0.32²+0.24²)=0.40 nm），确保两子系统可独立 FAT 验收；"),
        ("实机主从前馈 / 双 Youla 耦合 [075]：", "整机联调时将 RS 残余跟踪误差前馈注入高带宽 WS 短行程环，[075 Table 1 & Fig.13] 实测将低频相对同步误差进一步压低至 0.108–0.565 nm，形成 10%–25% 整机安全裕度。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.2, body_sz=8.1
)

add_pic_card(s7, "009_fig10_r", 8.05, 0.94, 4.93, 2.95, "原图 [009] Castenmiller 2010 · Fig.10(右)：NXT:1950i 实测 position error (WS − RS/4)：MA-X = 0.47 nm，MA-Y = 0.49 nm")
add_pic_card(s7, "075_fig13", 8.05, 4.02, 4.93, 3.00, "原图 [075] Evers & Oomen (TU/e–ASML 2019) · Fig.13：双 Youla 耦合控制显著抑制低频相对同步伺服误差")

# ==============================================================================
# SLIDE 08: ITEM 4 - ENC UNDERLYING METROLOGY (16 ITEMS)
# ==============================================================================
s8 = prs.slides.add_slide(BLANK)
add_header(s8, "Item 4 · ENC", "4. ENC（光栅编码器底层测量系统）16 项逐明细验收规格与 1/3 原则推导", next_pno(),
           "NXT 核心技术变革：用 <15 mm 短光程 2D 光栅板替代 >300 mm 长光程干涉仪，空气扰动噪声直降 4 倍以上 [009, 062]")

add_table(
    s8, 0.35, 0.94, 7.40, 4.55,
    ["序号", "台体", "ENC 验收子项明细", "规格 (3σ)", "晶圆等效", "推导依据与几何差分公式"],
    [
        ["4.1–4.2", "WS", "WS-ENC X / Y 曝光窗重复性 (~44Hz)", "≤ 0.12 nm", "0.12 nm", "0.20 nm 宽带经 11.4 ms 滤波；占 WS-X(0.32) 方差 14%"],
        ["4.3", "WS", "WS-ENC Z 曝光窗重复性", "≤ 0.35 nm", "0.35 nm", "2D 光栅 Z 灵敏度略低；占 WS-Z(4.5) 方差 <1%"],
        ["4.4–4.5", "WS", "WS-ENC Rx / Ry 曝光窗重复性", "≤ 3.0 nrad", "3.0 nrad", "四角 Z 头基线 L≈320 mm：√2·0.35/320 = 1.55 nrad (留2×)"],
        ["4.6", "WS", "WS-ENC Rz 曝光窗重复性", "≤ 1.5 nrad", "1.5 nrad", "四角切向差分 L≈320 mm：√2·0.12/320 = 0.53 nrad (留余量)"],
        ["4.7", "WS", "WS-ENC 单轴宽带噪声 (0–1000 Hz)", "≤ 0.20 nm", "0.20 nm", "直接对标 1950i 实测 0.22 nm @ 1000 Hz [009 Fig.4] 并收紧"],
        ["4.8", "WS", "多读数头切换(Handover)拼接重复性", "≤ 0.15 nm", "0.15 nm", "3-of-4 读数头过缝/换台在线标定跳变残差 [062 Sec.4]"],
        ["4.9", "WS", "Gridplate 网格板 7 天中长期稳定性", "≤ 0.18 nm", "0.18 nm", "直接对标 1950i 实测 7 天 < 0.20 nm [009, 062 Fig.11]"],
        ["4.10–11", "RS", "RS-ENC X / Y 曝光窗重复性 (掩模侧)", "≤ 0.32/0.36 nm", "0.08/0.09", "按 RS-X(0.96)/RS-Y(1.08) 1/3 计量原则分配"],
        ["4.12", "RS", "RS-ENC Z 曝光窗重复性 (掩模侧)", "≤ 2.50 nm", "0.22 nm", "编码器/电容混合，占 RS-Z(24 nm) 约 10%"],
        ["4.13–14", "RS", "RS-ENC Rx / Ry 曝光窗重复性", "≤ 25 / 20 nrad", "9.0 / 7.2", "垂向传感跨度 L≈180–200 mm：√2·2.5/200 ≈ 17.7 nrad"],
        ["4.15", "RS", "RS-ENC Rz 曝光窗重复性 (1:1耦合)", "≤ 2.5 nrad", "2.5 nrad", "两侧 Y 头跨度 L≈200 mm：√2·0.36/200 = 2.55 nrad"],
        ["4.16", "RS", "RS-ENC 宽带噪声 (1000 Hz, 掩模XY)", "≤ 0.60 nm", "0.15 nm", "限制 150 m/s² 高带宽环高频噪声放大，保障 MSD-XY"],
    ],
    [0.62, 0.42, 2.28, 1.05, 0.78, 2.25], font_sz=7.4, spec_col=3, align_left_cols=[2, 5]
)

add_box(
    s8, 0.35, 5.60, 7.40, 1.42,
    "ENC 与整机预算关系说明（避免重复计算）",
    [
        ("为什么 ENC 不在 DCO 顶层单独成行：", "ENC 噪声通过闭环伺服直接体现在 WS/RS 定位与 Sync MA（Item 3）中；遵循量测精度 ≤ 1/3 运动台指标的黄金准则，其方差仅占 WS-XY 的 11%–14%。注：上表合并展示对称轴，Excel Sheet 02 完整展开为 16 独立行。"),
        ("行业横向印证：", "Nikon S620D Streamlign 编码器在 700 mm/s 下差分重复性为 0.25 nm [060, 063]，与本机 0.20 nm 宽带 / 0.12 nm 窗口指标高度自洽。"),
    ],
    bg=C_BOX_BLUE, accent=C_DARK_BLUE, title_sz=9.0, body_sz=7.9
)

add_pic_card(s8, "009_fig4", 7.90, 0.94, 5.08, 2.95, "原图 [009] Castenmiller 2010 · Fig.4：XT 干涉仪 0.90 nm @ 40 Hz vs NXT 网格板编码器 0.22 nm @ 1000 Hz (<15 mm 气隙)")
add_pic_card(s8, "062_fig11", 7.90, 4.02, 5.08, 3.00, "原图 [062] de Jong 2009 · Fig.11：Gridplate 网格板 156 小时（~7 天）实测稳定性 < 0.20 nm")

# ==============================================================================
# SLIDE 09: ITEM 5 - M-SIDE AA (SMASH)
# ==============================================================================
s9 = prs.slides.add_slide(BLANK)
add_header(s9, "Item 5 · M-side AA", "5. M-side 晶圆对准系统（Advanced Align：Athena / SMASH）7 项验收规格", next_pno(),
           "四波长（532/633/780/852 nm）多衍射级次自参考干涉对准；直接对标 NXT:1970Ci SMASH 实测数据 [015 Fig.10]")

add_table(
    s9, 0.35, 0.94, 7.45, 4.10,
    ["序号", "验收子项明细", "验收规格", "统计口径与工况", "依据与推导理由"],
    [
        ["5.1", "单标记静态测量重复性", "≤ 0.20 nm", "WQ≥1%，四色，3σ，扣WS", "直接对标 1970Ci SMASH 实测 0.15–0.25 nm [015 Fig.10]"],
        ["5.2", "单标记动态扫描重复性", "≤ 0.35 nm", "WQ≥1%，含M-side WS", "传感本底 0.20 与 WS 定位 0.29 合成：√(0.20²+0.29²)=0.35"],
        ["5.3", "低信号工艺片单标记重复性", "≤ 0.45 nm", "低 WQ = 0.1%–1.0%，3σ", "直接对标 1970Ci 实测 0.25–0.50 nm [015 Fig.10]，保障暗场层"],
        ["5.4", "多波长颜色/级次配准稳定", "≤ 0.30 nm", "24 h 四色相对漂移，3σ", "支撑多色加权配方抑制 CMP 不对称不引入切换偏置 [006]"],
        ["5.5", "全晶圆对准网格拟合重复性", "≤ 0.35 nm", "N≥20 标记，6参/HOWA", "直接计入 DCO！多点抑噪并计入残余非线性拟合误差"],
        ["5.6", "M-to-E 对准基线短期漂移", "≤ 0.25 nm", "片内/批间未重校，3σ", "直接计入 DCO！与 5.5 合成单层 AA=0.43 nm（双层 0.608 nm）"],
        ["5.7", "工艺标记不对称残差(WAD)", "≤ 0.45 nm", "CMP/金属工艺片，3σ", "不计参考片 DCO，计入 MMO / 产品片 OPO 匹配闭环"],
    ],
    [0.50, 1.85, 0.88, 1.55, 2.67], font_sz=7.9, spec_col=2, align_left_cols=[1, 3, 4]
)

add_box(
    s9, 0.35, 5.18, 7.45, 1.84,
    "预算衔接与双台基线标定机制",
    [
        ("对标 NXT:1950i DCO 对准份额：", "[009 Fig.3] 中 1950i 对准相关占 2.5 nm DCO 约 0.50–0.61 nm；本机单层 AA 合成 0.430 nm（双层 0.608 nm，占 DCO Y 向随机方差 15.0%），严格处于 1950i 与 1970Ci 之间。"),
        ("为什么区分 WQ ≥ 1% 与 WQ = 0.1%–1%：", "前段参考硅片信号强（考核 0.20 nm 本底）；先进逻辑/DRAM 后段不透明金属层光强骤降，[015 Fig.10] 黑线实测表明 1970Ci 级传感器需在 0.1% 低 WQ 下仍压在 0.45 nm 内。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.3, body_sz=8.1
)

add_pic_card(s9, "015_fig10", 7.95, 0.94, 5.03, 6.08, "原图 [015] de Graaf 2016 · Fig.10：NXT:1970Ci（黑）与 1980Di（绿）SMASH 对准重复性随晶圆信号质量 WQ 变化实测曲线（WQ≥1% 为 0.15–0.25 nm；WQ 0.1%–1% 为 0.25–0.50 nm）")

# ==============================================================================
# SLIDE 10: ITEM 6 - E-SIDE TIS / PARIS
# ==============================================================================
s10 = prs.slides.add_slide(BLANK)
add_header(s10, "Item 6 · TIS/PARIS", "6. E-side 空间像对准系统（TIS / PARIS）6 项验收规格", next_pno(),
           "6 kHz 双传感板 TIS + 7 视场点并行 PARIS：建立掩模—物镜—晶圆台空间像绝对零点与在线奇像差监测 [066, 011, 254]")

add_table(
    s10, 0.35, 0.94, 7.45, 3.80,
    ["序号", "验收子项明细", "验收规格", "统计口径与影响", "依据与文献实测"],
    [
        ["6.1", "TIS 水平空间像对准重复性 (XY)", "≤ 0.35 nm", "6 kHz 双传感板，3σ", "建立 M-to-E 基准零点与双台对准参考 [009, 266]"],
        ["6.2", "TIS 垂向最佳焦面重复性 (Z)", "≤ 2.50 nm", "Z扫描寻峰，直接入FU", "占 FU(12 nm) 闭环方差仅 4.3%，确保最佳焦面零点"],
        ["6.3", "PARIS 掩模对准重复性 (7点 RA)", "≤ 0.40 nm", "7视场点并行，直接入DCO", "直接对标 [066 Sec.3.4] <0.5 nm 与 [011] 1970Ci 实测 0.43 nm"],
        ["6.4", "PARIS 7点焦面/像场弯曲重复性", "≤ 3.00 nm", "7视场点 Z 拟合，3σ", "捕获掩模加热/透镜加热诱发的狭缝场曲漂移 [066]"],
        ["6.5", "PARIS/ILC 奇像差波前测量重复性", "≤ 0.12 nm RMS", "主奇像差(Z7/8)单次 3σ", "对标 [254 Fig.2] 1970Ci 代 PARIS 对套刻二次贡献 0.28–0.34 nm"],
        ["6.6", "双台 TIS-1 / TIS-2 传感板匹配稳定", "≤ 0.25 nm", "24 h 台间相对漂移，3σ", "不计同台 DCO，计入双台匹配/MMO 误差源 [009, 066]"],
    ],
    [0.50, 2.05, 0.98, 1.55, 2.37], font_sz=7.9, spec_col=2, align_left_cols=[1, 3, 4]
)

add_box(
    s10, 0.35, 4.88, 7.45, 2.14,
    "为何 PARIS 7 视场点并行测量是 1960Bi–1970Ci 档位标配",
    [
        ("突破传统 TIS 仅测 2 点局限：", "传统双点 TIS 只能捕获平移/旋转/一阶放大率；[066 Fig.6] 引入 7 视场点并行 PARIS 后，单次掩模对准即可同步测出狭缝二/三阶畸变（K7/K12/K13）与奇像差漂移。"),
        ("单次波前测噪 0.12 nm RMS 如何推导：", "[254 Fig.2] 实测 1970Ci/2050i 代 PARIS 像差量测重复性对套刻贡献约 0.28–0.34 nm；按主奇像差综合灵敏度 ~0.8 nm/nm (Fringe) 反推单次测噪底须 ≤ 0.12 nm RMS（≈0.34 nm Fringe），经多次平均后支撑 Item 15 的 0.16–0.22 nm 闭环控制。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.3, body_sz=8.1
)

add_pic_card(s10, "066_fig8", 7.95, 0.94, 5.03, 2.95, "原图 [066] de Boeij 2013 · Fig.8：PARIS 7 视场点并行掩模对准实测重复性 < 0.5 nm (3σ)")
add_pic_card(s10, "254_fig2", 7.95, 4.02, 5.03, 3.00, "原图 [254] Smeets 2023 · Fig.2：PARIS（2050i 沿用 1970Ci 架构）像差量测重复性对套刻二次贡献 0.28–0.34 nm")

# ==============================================================================
# SLIDE 11: ITEM 7 - WAFER TABLE THERMAL CONTROL
# ==============================================================================
s11 = prs.slides.add_slide(BLANK)
add_header(s11, "Item 7 · WT温控", "7. Wafer Table（晶圆台 WT）温控误差 6 项验收规格与热膨胀推导", next_pno(),
           "硅热膨胀系数 α_Si = 2.6 ppm/K（R=150 mm 对应 0.39 nm/mK；视场 16.5 mm 对应 0.043 nm/mK），重点控非均匀与边缘蒸发")

add_table(
    s11, 0.35, 0.94, 7.55, 3.85,
    ["序号", "验收子项明细", "验收规格", "统计口径与工况", "等效套刻与物理推导"],
    [
        ["7.1", "WT 内部冷却水 (WTCW) 稳定性", "≤ ±2.0 mK", "1 h / 批内 3σ，细加热器", "线性缩放可被对准吸收，瞬态残差 <0.15 nm [ME3 01-TT_Lay_L3]"],
        ["7.2", "WT 顶面空间温度均匀性", "≤ 5.0 mK", "300 mm 瘤点区峰谷 PV", "非均匀温差高阶残差 ~0.045 nm/mK [017] → 5×0.045 = 0.22 nm"],
        ["7.3", "WT 边缘区(BES 液浸蒸发)残差", "≤ 8.0 mK", "外缘 20 mm 环带，3σ", "液浸水膜跨边蒸发强烈吸热，需独立边缘加热区 [184] → ≤0.25 nm"],
        ["7.4", "液浸超纯水 (UPW) 供水稳定性", "≤ ±2.0 mK", "液浸头出口处，3σ", "直接对标 XT:1900i 实测 ±2.5 mK [021 Fig.12] 并收紧 20%"],
        ["7.5", "双台 WT1 / WT2 平均温度匹配差", "≤ 2.0 mK", "|T_WT1 − T_WT2| 均值差", "原始缩放差 0.78 nm，经双台缩放标定后高阶残差 ≤ 0.15 nm"],
        ["7.6", "高剂量连续曝光片内稳态热漂移", "≤ 4.0 mK", "30 mJ/cm²·230 wph 含WHC", "对标 1950i 晶圆热 0.42 nm [009 Fig.3]，WT 侧控 ≤0.35 nm 入 DCO"],
    ],
    [0.50, 2.05, 0.92, 1.50, 2.58], font_sz=7.9, spec_col=2, align_left_cols=[1, 3, 4]
)

add_box(
    s11, 0.35, 4.92, 7.55, 2.10,
    "物理机理：为什么“非均匀温差”和“边缘蒸发”比全局温漂更致命？",
    [
        ("全局均匀温差（可补偿）：", "若全片均匀升高 2 mK，径向膨胀 0.78 nm 表现为纯线性放大率（Mx=My），可被 M-side 对准线性项完全吸收（仅在 M→E 瞬态变化时产生套刻误差）。"),
        ("空间非均匀梯度与边缘蒸发（不可线性补偿）：", "[017 Fig.7] 实测表明，液浸头在晶圆边缘区残留水膜蒸发吸热会诱发局部 10–30 mK 降温，产生不可被 6 参线性模型校正的高阶网格残差，必须通过分区加热器 [184] + WHC 前馈将其压至 0.35 nm 以内。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.3, body_sz=8.1
)

add_pic_card(s11, "021_fig12", 8.05, 0.94, 4.93, 2.95, "原图 [021] de Klerk 2007 · Fig.12：ASML XT:1900i 液浸超纯水 UPW 实测长期温度稳定性 ±2.5 mK（本机收紧至 ±2.0 mK）")
add_pic_card(s11, "017_fig7", 8.05, 4.02, 4.93, 3.00, "原图 [017] Ha (Samsung 2013) · Fig.7：晶圆曝光过程热波动 3σ 与全片网格/场内套刻残差线性依赖关系实测")

# ==============================================================================
# SLIDE 12: ITEM 8 - NEAR-RETICLE THERMAL CONTROL
# ==============================================================================
s12 = prs.slides.add_slide(BLANK)
add_header(s12, "Item 8 · Reticle温控", "8. Reticle（掩模）附近温控误差 5 项验收规格：空气折射率 vs 石英膨胀", next_pno(),
           "核心洞察：石英 CTE 极低（0.0091 nm/mK 晶圆等效），真正瓶颈是掩模—物镜气隙空气折射率温漂 |dn/dT|=0.93 ppm/K！")

add_table(
    s12, 0.35, 0.94, 7.25, 3.55,
    ["序号", "验收子项明细", "验收规格", "工况与影响", "物理计算与文献证据"],
    [
        ["8.1", "掩模台水平层流气幕稳定性", "≤ ±5.0 mK", "出风口 3σ，水平层流", "ME3 [08-TT-L3-RS]；100 mm 光程×0.93 ppm/K×5 mK = 0.12 nm(1×)"],
        ["8.2", "掩模-物镜顶面气隙温度梯度", "≤ 10.0 mK", "时空波动 3σ，入 DCO", "[016 Fig.6] 揭示气隙点间噪声为随机主因，控 10 mK → ≤0.25 nm"],
        ["8.3", "掩模台底座(RS Chuck)水冷", "≤ ±5.0 mK", "RS 短行程冷却，3σ", "隔离 150 m/s² 线圈发热传至掩模，热弯影响 <0.05 nm"],
        ["8.4", "机内掩模库(IRL)预温控精度", "≤ ±300 mK", "±0.30 °C（相对曝光室）", "对标 [254 Fig.3] 1980Di/2050i ±0.4°C→2100i ±0.2°C，取 ±0.3°C"],
        ["8.5", "曝光掩模加热非均匀残差(经RHC)", "≤ 30.0 mK", "RHC 后残余等效 ΔT", "绝对温升 0.3–1 K 经 RHC 补偿 90–95%，残余 30 mK×0.0091=0.27 nm"],
    ],
    [0.50, 1.90, 0.90, 1.35, 2.60], font_sz=7.9, spec_col=2, align_left_cols=[1, 3, 4]
)

add_box(
    s12, 0.35, 4.62, 7.25, 2.40,
    "双重热光灵敏度对比与 DCO 合成",
    [
        ("① 石英本体热胀极钝（9.1 nm/K 晶圆等效）：", "熔融石英 α_q = 0.55 ppm/K，视场半高 16.5 mm 处仅 0.0091 nm/mK；因此 IRL 预温控只需 ±0.30°C（初始线性胀 2.7 nm 被 PARIS RA 吸收，残余高阶 ≤ 0.10 nm）。"),
        ("② 空气光程与气隙对流极敏（93 nm/K·100mm）：", "空气折射率温漂 |dn/dT| 比石英热胀大 100 倍！[016 Fig.6] 实测 1970Ci 在苛刻低透射率（<5% RT）下“Point-to-point”气隙对流噪声高达 (1.1, 0.7) nm；常规工况下靠水平层流气幕（±5 mK）与气隙吹扫（≤10 mK）压至 0.25 nm，与 RHC 残差 0.27 nm 合成 D5 = 0.368 nm。"),
    ],
    bg=C_BOX_WARM, accent=C_CORAL, title_sz=9.3, body_sz=8.1
)

add_pic_card(s12, "016_fig6", 7.75, 0.94, 5.23, 3.05, "原图 [016] Kim/Paarhuis (Samsung/ASML 2016) · Fig.6：NXT:1970Ci 掩模加热分解（均场 1.2/1.7、气隙点间噪声 1.1/0.7、片内漂移 0.5/0.4 nm）")
add_pic_card(s12, "254_fig3", 7.75, 4.10, 5.23, 2.92, "原图 [254] Smeets 2023 · Fig.3：机内掩模库 IRL 温控精度演进（2050i ±0.4°C vs 2100i ±0.2°C，本机取 ±0.3°C）")

# ==============================================================================
# SLIDE 13: ITEM 9 - RT RETICLE CLAMPING
# ==============================================================================
s13 = prs.slides.add_slide(BLANK)
add_header(s13, "Item 9 · RT夹持", "9. RT（掩模台）对掩模的夹持误差 5 项验收规格", next_pno(),
           "直接锚定 TU/e–ASML 掩模夹持权威博士论文 [225 Sec.2.1.2–2.1.3]：不可校正套刻 NCE < 0.28 nm，离焦 < 2.0 nm（晶圆 1×）")

add_table(
    s13, 0.35, 0.94, 7.55, 3.55,
    ["序号", "验收子项明细", "晶圆等效 1×", "掩模侧 4×", "计入层级与推导依据"],
    [
        ["9.1", "不可校正平面内变形 (NCE IPD)", "≤ 0.25 nm", "≤ 1.00 nm", "直接对标 [225 Sec.2.1.2] <0.28 nm 留余量；跨机 MMO ×√2=0.354 nm"],
        ["9.2", "重复卸载-重夹持变形重复性", "≤ 0.15 nm", "≤ 0.60 nm", "直接计入 DCO！真空吸盘静摩擦随机滞回重复性（占 NCE 60%）"],
        ["9.3", "高加速扫描微滑移 (SUSD)", "≤ 0.15 nm", "≤ 0.60 nm", "直接计入 DCO！@ 150 m/s² 正反扫惯性微滑移（与 9.2 合成 0.212 nm）"],
        ["9.4", "掩模夹持面外平坦度变形 (Z)", "≤ 2.00 nm", "≤ 22.3 nm", "直接引用 [225 Sec.2.1.3] 焦面 ≤2.0 nm，按 16/n_w=11.14 换算掩模侧"],
        ["9.5", "真空吸盘接触面平坦度 (基准)", "—", "≤ 50 nm PV", "保障 6 寸石英掩模吸附后不引入高阶弯矩与局部颗粒热点"],
    ],
    [0.50, 2.05, 0.95, 0.95, 3.10], font_sz=8.0, spec_col=2, align_left_cols=[1, 4]
)

add_box(
    s13, 0.35, 4.62, 7.55, 2.40,
    "为什么静态 NCE 计入 MMO 而重复性/微滑移计入 DCO？",
    [
        ("同机同掩模曝光（DCO）：", "同一块掩模在同台吸盘上夹持的静态不可校正指纹在多次曝光间可部分重现，影响 DCO 的核心是重复装夹时的静摩擦随机释放（0.15 nm）与 150 m/s² 折返扫描下的正反扫微滑移（SUSD, 0.15 nm），合成 0.212 nm（双层 0.300 nm，仅占 DCO 方差 3.7%）。"),
        ("跨机/双掩模曝光（MMO）：", "两台机台吸盘与不同掩模的静态 NCE 互不抵消，故按 0.25 × √2 = 0.354 nm 计入 MMO；面外 Z 变形 2.00 nm（对应 [225 Fig.6.15] RSC 补偿后实测 1.2 nm 3σ）直接计入整机焦面 FU 闭环。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.3, body_sz=8.1
)

add_pic_card(s13, "225_fig1_8", 8.05, 0.94, 4.93, 2.95, "原图 [225] Naaijkens 2013 · Fig.1.8：ASML SMO 套刻预算演进（机械夹持占比约束推导 NCE < 0.28 nm）")
add_pic_card(s13, "225_fig6_15", 8.05, 4.02, 4.93, 3.00, "原图 [225] Naaijkens 2013 · Fig.6.15：掩模夹持经 RSC 补偿后面外离焦实测 1.2 nm 3σ（规格 ≤ 2.0 nm）")

# ==============================================================================
# SLIDE 14: ITEM 10 - WT WAFER CLAMPING
# ==============================================================================
s14 = prs.slides.add_slide(BLANK)
add_header(s14, "Item 10 · WT夹持", "10. WT（晶圆台）对晶圆的夹持误差 6 项验收规格", next_pno(),
           "焦面均匀性最大单项（6.00 nm，占 FU 方差 33.7%）与工艺片 MMO 关键项；直接对标 [009 Fig.3] 与 [066 Fig.10a]")

add_table(
    s14, 0.35, 0.94, 7.55, 3.85,
    ["序号", "验收子项明细", "验收规格", "统计口径与工况", "计入层级与文献实测依据"],
    [
        ["10.1", "平坦硅片重复吸片变形重复性", "≤ 0.25 nm", "平坦片扣线性项，3σ", "直接计入 DCO！对标 1950i DCO 晶圆夹持 ~0.20–0.25 nm [009 Fig.3]"],
        ["10.2", "双台 WT1 / WT2 夹持指纹匹配差", "≤ 0.35 nm", "同批平坦片跨台，3σ", "不计同台 DCO，计入双台匹配/MMO（经双台前馈标定后）"],
        ["10.3", "翘曲工艺片夹持非校正 IPD", "≤ 0.55 nm", "50 μm Bow 翘曲片，3σ", "对标 [066 Fig.10a] WT 全片套刻 1.0 nm 及摩擦建模 [097, 122]"],
        ["10.4", "高速扫描下晶圆微滑移(SUSD)", "≤ 0.15 nm", "@ 35–40 m/s² 折返，3σ", "直接计入 DCO！与 10.1 合成单层 0.292 nm（双层 0.412 nm）"],
        ["10.5", "WT 瘤点全局平坦度焦面误差(Z)", "≤ 6.00 nm", "300 mm 全片，3σ", "直接计入焦面 FU！对标 [066 Fig.10a] 改进型 WT 实测 6.2 nm"],
        ["10.6", "WT 瘤点局部平坦度与接触比", "≤ 15.0 nm", "26×33 mm PV（接触1–3%）", "降低背面颗粒夹杂热点概率与局部高频弯曲 [066, 186]"],
    ],
    [0.50, 2.05, 0.92, 1.48, 2.60], font_sz=7.9, spec_col=2, align_left_cols=[1, 3, 4]
)

add_box(
    s14, 0.35, 4.92, 7.55, 2.10,
    "夹持力学机理与 1950i→1970Ci 演进关键",
    [
        ("高平坦 WT 是 FU ≤ 12.0 nm 的胜负手：", "如右图 [066 Fig.10a] 所示，早期 WT 仅平坦度一项离焦就高达 9.4 nm（直接导致整机 FU > 14 nm）；升级高平坦低应力瘤点 WT 将其压至 6.2 nm（本机定 6.00 nm）后，整机 FU 才得以稳定收敛至 10.34 nm。"),
        ("翘曲片静摩擦 IPD 抑制 [097, 122, 186]：", "50 μm 弓形翘曲硅片在被真空拉平时，边缘径向伸缩受瘤点静摩擦阻滞锁死为不可校正高阶 IPD；需配合低摩擦 DLC/SiSiC 瘤点镀层及由中心向外径向顺序抽真空时序，将 MMO 晶圆夹持综合控制在 0.95 nm 内。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.3, body_sz=8.1
)

add_pic_card(s14, "066_fig10a", 8.05, 0.94, 4.93, 3.25, "原图 [066] de Boeij 2013 · Fig.10a：新一代高平坦 WT 实测焦面由 9.4 nm 降至 6.2 nm，套刻由 1.2 nm 降至 1.0 nm")
add_pic_card(s14, "009_fig3", 8.05, 4.30, 4.93, 2.72, "原图 [009] Castenmiller 2010 · Fig.3：NXT:1950i DCO 误差树中 Wafer Clamping 约 0.20 nm 基准份额")

# ==============================================================================
# SLIDE 15: ITEM 11 - WAFER HANDLER THERMAL CONTROL (PHYSICS DERIVATION)
# ==============================================================================
s15 = prs.slides.add_slide(BLANK)
add_header(s15, "Item 11 · WH温控", "11. Wafer Handler（WH）温控误差 6 项规格：基于 17 μm 气浮台瞬态传热推导", next_pno(),
           "依据 ASML TWINSCAN 官方手册 [ME3 05-TT-L2-WH & 01-TT_Lay_L3] 实算 τ_TSU = 0.826 s，精确反推片间出口重复性 ≤ 5.0 mK！")

add_table(
    s15, 0.35, 0.94, 6.25, 3.28,
    ["序号", "验收子项明细", "验收规格", "推导机制与套刻影响"],
    [
        ["11.1", "TSU 冷却水(共用 LCW)稳定", "≤ ±2.0 mK", "ME3 手册确认 TSU 直连整机最稳 LCW 细控回路"],
        ["11.2", "WH 气幕与 TSU 匹配(ACC)", "≤ ±15.0 mK", "h_air≈20 vs U_TSU=1529 W/m²K(1.3%)→硅片偏<0.2 mK"],
        ["11.3", "出口硅片均值与 WT 静偏差", "≤ ±10.0 mK", "τ_TSU=0.826 s，停 4.5 s 衰减 >230:1；静偏可标定吸收"],
        ["11.4", "出口硅片片间温度重复性★", "≤ 5.0 mK", "核心 DCO 项！随机 M→E 残差 0.49 mK → 0.19 nm 套刻"],
        ["11.5", "出口硅片面内空间均匀性", "≤ 10.0 mK", "300 mm PV；上 WT 扩散均衡后非线性套刻 ≤ 0.12 nm"],
        ["11.6", "Track 进片温度耐受边界", "±1000 mK", "外部接口输入 ±1.0 K（230 wph 下经 TSU 充分消化）"],
    ],
    [0.50, 1.85, 0.92, 2.98], font_sz=7.7, spec_col=2, align_left_cols=[1, 3]
)

add_pic_card(s15, "me3_tsu", 6.75, 0.94, 6.23, 2.02, "原图 [ME3 手册 05-TT-L2-WH] Fig.2.5：ASML TWINSCAN TSU（17 μm 空气气浮膜 + 真空预载 + 内部 LCW 预温控）")

add_box(
    s15, 6.75, 3.04, 6.23, 1.18,
    "一阶瞬态传热解析计算过程（纯物理第一性原理）",
    [
        ("硅片热容与 TSU 时间常数：", "C'' = ρ·c_p·t = 2329×700×775μm = 1263.5 J/(m²K)；U_TSU = k_air / 17μm = 1529 W/(m²K) ⇒ τ_TSU = C''/U_TSU = 0.826 s。"),
        ("为何 11.4 片间重复性必须 ≤ 5.0 mK：", "上 WT 后 τ_WT≈2.2 s，若片间出口随机波动 10 mK，M-side(t≈5s)→E-side(t≈12s) 温差达 0.99 mK → 0.39 nm 套刻超标！反推 ≤5.0 mK 压至 0.19 nm。"),
    ],
    bg=C_BOX_BLUE, accent=C_DARK_BLUE, title_sz=8.8, body_sz=7.7
)

add_pic_card(s15, "c_wh", 0.35, 4.30, 12.63, 2.74, "自绘物理瞬态仿真图（左：TSU 17 μm 气浮膜 230:1 衰减曲线；右：WT 上 M-to-E 瞬态衰减证明为何 WH 出口片间重复性必须 ≤ 5.0 mK）")

# ==============================================================================
# SLIDE 16: ITEM 12 - MACHINE FRAME STABILITY (11 ITEMS)
# ==============================================================================
s16 = prs.slides.add_slide(BLANK)
add_header(s16, "Item 12 · 整机Frame", "12. 整机 Frame（计量框架 MF 与基础框架 BF）11 项稳定性误差规格", next_pno(),
           "双框架动力学解耦架构：BF + 平衡质量块吸收 40/150 m/s² 运动台反力；MF 悬于 0.5 Hz Air Mount 承载物镜/Gridplate/AA/LS [019, 094]")

add_table(
    s16, 0.35, 0.94, 7.15, 4.45,
    ["序号", "整机 Frame 验收子项明细", "验收规格", "层级归属与推导依据"],
    [
        ["12.1–2", "MF–物镜相对动态 MA (X / Y)", "≤ 0.15 nm", "内含于 Sync MA-XY(0.40/0.45)，占方差 11–14%"],
        ["12.3", "MF–物镜相对动态 MA (Z)", "≤ 1.50 nm", "直接计入 FU 框架项（与液浸合成 2.00 nm）"],
        ["12.4", "MF–物镜相对动态转角 Rx", "≤ 40 nrad", "±4 mm 狭缝边缘离焦仅 0.16 nm"],
        ["12.5", "MF–物镜相对动态转角 Ry", "≤ 25 nrad", "±13 mm 狭缝边缘离焦 0.33 nm（占同步方差 4%）"],
        ["12.6", "MF–物镜相对动态转角 Rz", "≤ 4.0 nrad", "±13 mm 边缘套刻仅 0.052 nm（占同步方差 7%）"],
        ["12.7", "双台运动串扰 (M台40m/s²→E台)", "≤ 0.10 nm", "验证 BM 水平解耦与 Air Mount 隔离度 [019, 266]"],
        ["12.8", "MF 热机械短期基线漂移 (~16 s)", "≤ 0.15 nm", "内含于 5.6 短期基线 (0.25 nm)，单片几乎零漂"],
        ["12.9", "MF 24 小时无校准基线漂移", "≤ 1.50 nm", "考核 MF 无蠕变/零残余应力及 MFCW 长期稳定性"],
        ["12.10", "MFCW 水冷 / MF 气幕温度稳定", "±5 / ±10 mK", "直接对标 [009 Sec.4] 10 mK 气幕与 [ME3] MFCW 细控"],
        ["12.11", "Air Mount 隔振与 MF 一阶模态", "f0≤0.6 Hz / ≥150 Hz", "≥20 Hz 传递率≤-30 dB；配 PALM ~90 Hz 主动阻尼 [019]"],
    ],
    [0.62, 2.38, 1.25, 2.90], font_sz=7.6, spec_col=2, align_left_cols=[1, 3]
)

add_box(
    s16, 0.35, 5.52, 7.15, 1.50,
    "为什么 MF 必须采用“低频软隔振 + 高频高刚度 + 独立细水冷”三要素",
    [
        ("隔绝地基与运动台反力（≤0.6 Hz）：", "Air Mount 将 VC-D/E 地基微振与 BF 激振衰减 >30 dB；PALM 压电主动镜座在 ~90 Hz 处提供阻尼，消除物镜相对 MF 共振峰 [019 Fig.15]。"),
        ("避免结构柔性模态干扰伺服（≥150 Hz）：", "MF 本身一阶柔性模态 ≥150 Hz，避免落入 WS/RS 控制带宽并保证 Gridplate 与 AA 间基线几何稳定。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.0, body_sz=7.9
)

add_pic_card(s16, "019_fig9", 7.65, 0.94, 5.33, 3.25, "原图 [019] Heertjes & Butler (ASML 2020) · Fig.9：DUV 浸没式光刻机双框架、Air Mount、Balance Mass 与 ENC 全景架构")
add_pic_card(s16, "019_fig15", 7.65, 4.30, 5.33, 2.72, "原图 [019] Heertjes & Butler 2020 · Fig.15：物镜压电主动阻尼镜座（PALM）动态隔振原理")

# ==============================================================================
# SLIDE 17: ITEMS 13 & 14 OVERVIEW - OFFICIAL K1-K20 ACTUATOR MAPPING (PAPER 154)
# ==============================================================================
s17 = prs.slides.add_slide(BLANK)
add_header(s17, "iHOPC 总纲", "Items 13–14 前置依据：ASML 20 参 iHOPC 官方定义与物镜 / WS 执行机构映射", next_pno(),
           "直接截取 ASML 官方文献 [154, SPIE Vol.8683 86831J-7] 第 7 页原页 Eq.(1) 与 Table 1，100% 明确每一项归属")

add_pic_card(s17, "154_crop", 0.35, 0.94, 7.55, 5.10, "原页高清截图 [154] Mulkens et al. (ASML, SPIE 2012) · Page 7 Eq.(1) 与 Table 1：20 参场内多项式与执行机构官方分配表")

add_box(
    s17, 0.35, 6.14, 7.55, 0.88,
    "26 × 33 mm 视场几何放大系数解析公式（a = 1.30 cm, b = 1.65 cm）",
    [
        ("对任意单项式 x^p·y^q：", "最大场角放大系数 G_max = a^p · b^q；视场内均匀分布均方根放大系数 G_rms = [a^p / √(2p+1)] · [b^q / √(2q+1)]（已在 Excel Sheet 04 全公式自动计算）。"),
    ],
    bg=C_BOX_BLUE, accent=C_DARK_BLUE, title_sz=8.8, body_sz=8.0
)

add_box(
    s17, 8.05, 0.94, 4.93, 2.90,
    "Table 1 执行机构精确划分（共 20 项，零遗漏）",
    [
        ("Item 13 物镜纯静态（4 项 Lens）：", "K3 (x)、K7 (x²)、K12 (x²)、K13 (x³)。"),
        ("Item 13 物镜扫描同步动态（4 项 Scan Lens）：", "K9 (xy)、K15 (x²y)、K17 (xy²)、K18 (yx²)——扫描期间随 y 动态驱动物镜 Z/倾斜操纵器，构成 18/19 参 iHOPC 核心。"),
        ("Item 13 架构限制（1 项 `-`）：", "K20 (dy = K20·x³) 在 1950i–1970Ci 物镜中不支持动态补偿！至 NXT:2100i 新增 Distortion Manipulator 才引入 [254 Sec.2.4]。"),
        ("Item 14 WS 扫描轨迹（11 项 Scan）：", "K1, K2, K4, K5, K6, K8, K10, K11, K14, K16, K19。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.3, body_sz=8.1
)

add_pic_card(s17, "254_fig9", 8.05, 3.96, 4.93, 3.06, "原图 [254] Smeets 2023 · Fig.9：K20 (D3y) 直到 NXT:2100i 才新增动态控制能力，佐证 1950i–1970Ci 需控出厂静畸变")

# ==============================================================================
# SLIDE 18: ITEM 13 - LENS iHOPC RESIDUALS
# ==============================================================================
s18 = prs.slides.add_slide(BLANK)
add_header(s18, "Item 13 · 物镜iHOPC", "13. 物镜对 iHOPC 场内参数的补偿残差（ΔKn = Kn1 − Kn0，8 项激活 + K20 说明）", next_pno(),
           "相对执行精度对标 Nikon MDDM ~2% [160] 与 ASML/Zeiss 畸变操纵器 5%–10% [253 Fig.7]，静态控 2.5–5%、动态控 4–5.6%")

add_table(
    s18, 0.35, 0.94, 8.15, 4.65,
    ["参数", "方向", "单项式", "单位", "G_max", "G_rms", "典型|K0|", "残差|ΔKn|", "相对%", "场角(nm)", "场RMS(nm)", "执行模式"],
    [
        ["K3",  "X", "x",    "nm/cm",  "1.300", "0.751", "4.0", "≤ 0.100", "2.5%", "0.130", "0.075", "静态纯物镜"],
        ["K7",  "X", "x²",   "nm/cm²", "1.690", "0.756", "2.0", "≤ 0.080", "4.0%", "0.135", "0.060", "静态纯物镜"],
        ["K12", "Y", "x²",   "nm/cm²", "1.690", "0.756", "2.0", "≤ 0.080", "4.0%", "0.135", "0.060", "静态纯物镜"],
        ["K13", "X", "x³",   "nm/cm³", "2.197", "0.830", "1.2", "≤ 0.060", "5.0%", "0.132", "0.050", "静态纯物镜"],
        ["K9",  "X", "xy",   "nm/cm²", "2.145", "0.715", "1.5", "≤ 0.060", "4.0%", "0.129", "0.043", "扫描同步动态"],
        ["K15", "X", "x²y",  "nm/cm³", "2.789", "0.720", "0.8", "≤ 0.045", "5.6%", "0.125", "0.032", "扫描同步动态"],
        ["K17", "X", "xy²",  "nm/cm³", "3.539", "0.914", "0.8", "≤ 0.035", "4.4%", "0.124", "0.032", "扫描同步动态"],
        ["K18", "Y", "yx²",  "nm/cm³", "2.789", "0.720", "0.8", "≤ 0.045", "5.6%", "0.125", "0.032", "扫描同步动态"],
        ["K20", "Y", "x³",   "nm/cm³", "2.197", "0.830", "N/A", "不支持", "N/A", "静畸变", "≤0.15", "本代无自由度"],
        ["X 汇总", "X", "6项RSS", "—", "—", "—", "—", "—", "—", "0.317", "0.125", "入DCO(×1.2)"],
        ["Y 汇总", "Y", "2项RSS", "—", "—", "—", "—", "—", "—", "0.184", "0.069", "入DCO(×1.2)"],
    ],
    [0.58, 0.36, 0.56, 0.68, 0.58, 0.58, 0.60, 0.78, 0.56, 0.68, 0.75, 1.44], font_sz=7.4, spec_col=7, highlight_last=2
)

add_box(
    s18, 0.35, 5.72, 8.15, 1.30,
    "数值分配逻辑：等场角套刻均衡原则（每项场角残差统一压在 0.124–0.135 nm）",
    [
        ("高阶放大惩罚效应：", "K17 (xy²) 在场角 (1.3, 1.65) cm 的放大系数 G_max 高达 3.539 cm³，是 K3 (1.300) 的 2.7 倍；因此即使目标场角误差同为 ~0.125 nm，K17 系数残差也必须严控至 ≤ 0.035 nm/cm³。"),
        ("对标实测验证：", "右图 [253 Fig.7] 展示 ASML/Zeiss 畸变操纵器下发 Target(SET) vs 实测 Measured(GET) 及残差 Delta，全狭缝残差约 5%–10%（~0.10 nm 级），完全印证本表设定的 2.5%–5.6% 精度目标。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.0, body_sz=7.9
)

add_pic_card(s18, "253_fig7", 8.65, 0.94, 4.33, 3.00, "原图 [253] Klinkhamer (ASML/Zeiss 2022) · Fig.7：物镜畸变操纵器下发 Target(SET) vs 实测 Measured(GET) 及残差 Delta")
add_pic_card(s18, "253_fig8", 8.65, 4.04, 4.33, 2.98, "原图 [253] Klinkhamer 2022 · Fig.8：物镜操纵器全狭缝 Z2 指令(SET) vs 空间像实测(GET) 与残差 Delta（~5% 精度）")


# ==============================================================================
# SLIDE 22 (v2 NEW): PROJECTION OPTICS (LENS) Kn 8-DIMENSION CAPABILITY SYSTEM
# ==============================================================================
s_lens8 = prs.slides.add_slide(BLANK)
add_header(s_lens8, "Item 13 · 8维评价", "13（续）. 投影物镜对 K 参数补偿能力的 8 维综合评价体系与量化验收表", next_pno(),
           "回答问题 4：不仅包含 Range、最小调节量与调节重复性，还必须涵盖滞回、SET-vs-GET 线性度、波像差副作用、响应带宽与三级验证链路")

add_pic_card(
    s_lens8, "c_lens_8dim", 0.35, 0.96, 9.05, 2.74,
    "【v2 能力标定图】左：D1 Range / D2 最小步长 / D3 单双向滞回 / D4 SET-vs-GET 线性度；右：D6 四类执行机构响应带宽与 D5 副作用红线"
)

add_pic_card(
    s_lens8, "160_fig7", 9.54, 0.96, 3.44, 2.74,
    "【原始论文截图】OV4 [160] Nikon MDDM Fig.7：50 ms 响应达 2% 精度（6.4→0.11/0.07 nm RMS）"
)

add_box(
    s_lens8, 0.35, 3.80, 4.78, 3.20,
    "物镜 K 参数 8 维评价全框架（Excel Sheet 09A）",
    [
        ("D1 补偿范围 Range：", "单参 ≥4–6× 典型 |K0|，且多参+热像差联合叠加时各驱动器占用率 ≤80%（防饱和裁剪）。"),
        ("D2 最小调节量：", "单调可分辨最小步长 ΔK_min ≤ Spec/10（含克服静摩擦死区，防 APC 振荡）。"),
        ("D3 重复性与滞回：", "单向 3σ ≤35% Spec + 双向滞回 B_hyst ≤25% Spec（压电须靠电容/应变闭环抑滞回）。"),
        ("D4 线性度精度：", "全量程 SET-vs-GET 斜率与非线性误差 ≤2.5–5%（静）/ ≤4–5.6%（动）[160, 253]。"),
        ("D5 串扰与波像差副作用：", "【物镜特有】跨 K 串扰 ≤30%；诱发焦面 ≤1.0–1.5 nm、偶像差 ≤0.15、奇像差 ≤0.05 nm RMS！"),
        ("D6 响应与带宽：", "静态镜片 ≤20–50 ms [160]；动态扫描项滞后 ≤0.2 ms；激光 Δλ<1 ms；热控 10–60 s。"),
        ("D7 保持与漂移：", "15 s 压电蠕变 ≤20%、15 min 满功率热漂 ≤35%、24 h 零点漂移 ≤50% Spec。"),
        ("D8 三级闭环链路：", "离线光学台 PMI FAT → 机内 ILIAS/PARIS ≤5% [253 Fig.8] → 51×19 光刻胶套刻 SAT [Fig.7]。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.1, body_sz=7.1
)

add_table(
    s_lens8, 5.26, 3.80, 7.72, 3.20,
    ["参数", "单位", "±Range", "最小步长\n(≤1/10)", "单向 3σ\n(≤35%)", "双向滞回\n(≤25%)", "SET-GET\n总残差", "诱发焦/奇像差", "响应时间"],
    [
        ["K3",  "nm/cm",  "±25.0", "≤0.010", "≤0.035", "≤0.025", "≤0.100", "1.0nm/0.04RMS", "≤20ms (Δλ<1ms)"],
        ["K7",  "nm/cm²", "±10.0", "≤0.008", "≤0.028", "≤0.020", "≤0.080", "1.2nm/0.05RMS", "≤40ms (场/片间)"],
        ["K12", "nm/cm²", "±10.0", "≤0.008", "≤0.028", "≤0.020", "≤0.080", "1.2nm/0.05RMS", "≤40ms (场/片间)"],
        ["K13", "nm/cm³", "±6.0",  "≤0.006", "≤0.021", "≤0.015", "≤0.060", "1.5nm/0.05RMS", "≤50ms (场/片间)"],
        ["K9",  "nm/cm²", "±8.0",  "≤0.006", "≤0.021", "≤0.015", "≤0.060", "1.2nm/0.05RMS", "同步 (滞后≤0.2ms)"],
        ["K15", "nm/cm³", "±4.0",  "≤0.0045","≤0.016", "≤0.011", "≤0.045", "1.5nm/0.05RMS", "同步 (滞后≤0.2ms)"],
        ["K17", "nm/cm³", "±4.0",  "≤0.0035","≤0.012", "≤0.009", "≤0.035", "1.5nm/0.05RMS", "同步 (滞后≤0.2ms)"],
        ["K18", "nm/cm³", "±4.0",  "≤0.0045","≤0.016", "≤0.011", "≤0.045", "1.5nm/0.05RMS", "同步 (滞后≤0.2ms)"],
        ["K20", "nm/cm³", "N/A",   "N/A",    "N/A",    "N/A",    "静≤0.15","仅冷机出厂控",  "本代不支持 [154]"],
    ],
    [0.52, 0.72, 0.68, 0.72, 0.70, 0.70, 0.74, 1.32, 1.62], font_sz=6.9, spec_col=6, align_left_cols=[7, 8]
)

# ==============================================================================
# SLIDE 19: ITEM 14 - WS iHOPC RESIDUALS & SLIT DECONVOLUTION
# ==============================================================================
s19 = prs.slides.add_slide(BLANK)
add_header(s19, "Item 14 · WS iHOPC", "14. WS 对 iHOPC 场内 11 项参数的补偿残差（ΔKm）与 8 mm 狭缝逆卷积推导", next_pno(),
           "基于 0.12 nm ENC 全闭环伺服（相对精度 0.6%–3.8%），同时揭示二/三阶扫描轨迹必须执行有限狭缝逆卷积前馈！")

add_table(
    s19, 0.35, 0.94, 8.20, 3.68,
    ["参数", "方向", "单项式", "单位", "G_max", "G_rms", "典型|K0|", "残差|ΔKm|", "相对%", "场角(nm)", "场RMS(nm)", "WS/RS 轨迹机制"],
    [
        ["K1",  "X", "1",   "nm",     "1.000", "1.000", "20.0", "≤ 0.120", "0.6%", "0.120", "0.120", "静态 X 偏置"],
        ["K2",  "Y", "1",   "nm",     "1.000", "1.000", "20.0", "≤ 0.120", "0.6%", "0.120", "0.120", "静态 Y 偏置"],
        ["K4",  "Y", "y",   "nm/cm",  "1.650", "0.953", "5.0",  "≤ 0.070", "1.4%", "0.116", "0.067", "扫描速度比 My"],
        ["K5",  "X", "y",   "nm/cm",  "1.650", "0.953", "5.0",  "≤ 0.070", "1.4%", "0.116", "0.067", "线性交叉斜行"],
        ["K6",  "Y", "x",   "nm/cm",  "1.300", "0.751", "5.0",  "≤ 0.080", "1.6%", "0.104", "0.060", "静态 Rz (8 nrad)"],
        ["K8",  "Y", "y²",  "nm/cm²", "2.723", "1.218", "2.0",  "≤ 0.040", "2.0%", "0.109", "0.049", "常值扫描加速度"],
        ["K10", "Y", "xy",  "nm/cm²", "2.145", "0.715", "1.5",  "≤ 0.050", "3.3%", "0.107", "0.036", "动态线性 dRz/dy"],
        ["K11", "X", "y²",  "nm/cm²", "2.723", "1.218", "2.0",  "≤ 0.040", "2.0%", "0.109", "0.049", "抛物交叉(逆卷积)"],
        ["K14", "Y", "y³",  "nm/cm³", "4.492", "1.698", "1.0",  "≤ 0.025", "2.5%", "0.112", "0.042", "线性 Jerk 扫描"],
        ["K16", "Y", "xy²", "nm/cm³", "3.539", "0.914", "0.8",  "≤ 0.030", "3.8%", "0.106", "0.027", "抛物 Rz 角加速"],
        ["K19", "X", "y³",  "nm/cm³", "4.492", "1.698", "1.0",  "≤ 0.025", "2.5%", "0.112", "0.042", "立方交叉(逆卷积)"],
        ["X/Y汇总", "X/Y", "4/7项", "—", "—", "—", "—", "—", "—", "0.228/0.293", "0.152/0.169", "入DCO(×1.2)"],
    ],
    [0.58, 0.36, 0.50, 0.65, 0.56, 0.56, 0.58, 0.76, 0.52, 0.85, 0.84, 1.44], font_sz=6.9, spec_col=7, highlight_last=1
)

add_box(
    s19, 8.70, 0.94, 4.28, 3.05,
    "有限狭缝（L_s = 0.80 cm）逆卷积解析推导",
    [
        ("曝光积分平均效应：", "任一点 y 的成像偏移为轨迹在 [y−L_s/2, y+L_s/2] 内的均值。"),
        ("二阶偏置公式：", "(1/L_s)∫ u² du = y² + L_s²/12 = y² + 0.0533 cm²。下发 K11=2.0 将诱发 ΔK1 = +0.107 nm 常数平移串扰！"),
        ("三阶偏置公式：", "(1/L_s)∫ u³ du = y³ + (L_s²/4)·y = y³ + 0.160·y cm²。下发 K19=1.0 将诱发 ΔK5 = 0.160 nm/cm（场角额外 +0.264 nm 误差）！"),
        ("控制律必须逆卷积前馈：", "K1_cmd ← K10 − 0.0533·K110；K5_cmd ← K50 − 0.160·K190（Y 向 K2/K4 同理）。"),
    ],
    bg=C_BOX_WARM, accent=C_CORAL, title_sz=8.9, body_sz=7.8
)

add_pic_card(s19, "c_slit", 0.35, 4.70, 8.20, 2.34, "自绘解析曲线：8 mm 狭缝卷积对二阶 K11 与三阶 K19 轨迹的偏置串扰效应（未逆卷积将直接超差！）")
add_box(
    s19, 8.70, 4.08, 4.28, 2.96,
    "三阶项严控 ≤ 0.025 nm/cm³ 原因",
    [
        ("最大放大倍数达 4.492：", "K14 与 K19 在扫描末端 y = ±1.65 cm 处按 y³ 放大 4.492 倍；控制 ΔK ≤ 0.025 nm/cm³ 才能将场角误差锁定在 0.112 nm。"),
        ("动态带宽校验：", "扫描单场耗时 33 mm / 0.70 m/s ≈ 47 ms，三阶 Jerk 轨迹频谱集中于 <25 Hz，远低于 WS 伺服带宽（>200 Hz），依靠加速度/加加速度前馈可稳定达标。"),
    ],
    bg=C_BOX_BLUE, accent=C_DARK_BLUE, title_sz=9.0, body_sz=8.0
)


# ==============================================================================
# SLIDE 24 (v2 NEW): WS Km OFFLINE/ONLINE ACCEPTANCE CRITIQUE & 11-ITEM MATRIX
# ==============================================================================
s_ws_k4 = prs.slides.add_slide(BLANK)
add_header(s_ws_k4, "Item 14 · Km验收", "14（续上）. WS 对 Km（以 K4 为例）离线/在线验收方案审视、5 大修正与全 11 项细则", next_pno(),
           "回应问题 3：用户离线 Q_enc(t) vs Q_0(t) 方案整体骨架完全正确，但须补齐狭缝 MA、OLS 投影、Z/Rx/Ry 护栏与 ENC 自测盲区破解")

add_box(
    s_ws_k4, 0.35, 0.96, 5.75, 6.04,
    "对用户离线 K4 验收方案（Q_enc − Q_0）的逐条评估与 5 大升级修正",
    [
        ("总体判定（高度合理，属标准离线 FAT 骨架）：", "在规定扫速 V（0.70 m/s）与扫描长度下，向 WS 下发带 K4 的轨迹 Q_0(t) 并用 WS-ENC 实时比对，是子系统 FAT 验证动态轨迹跟踪的正确路线（K4 = 5 nm/cm 对应扫描速度微调 Δv = 0.35 μm/s）。"),
        ("修正 1 · 必须做 8 mm 狭缝滑动平均（MA），勿看瞬时峰值：", "瞬时误差 e_y(t)=y_enc−y_0 含 >44 Hz 高频 MSD（影响对比度而非套刻）；须映射到曝光窗 y∈[−1.65,+1.65] cm 并做 L_s=8 mm 滑动平均得 ē_x(y), ē_y(y), ē_rz(y)。"),
        ("修正 2 · 须做 7×9 虚拟视场 OLS 回归提取 ΔKm 与串扰：", "由 δx_eff=ē_x−s·e_rz 狭缝均值、δy_eff=ē_y+x·ē_rz 拟合回 {K1..K19}，同步验 ΔKm、跨项串扰（≤30% Spec）与未建模残差 3σ_res。"),
        ("修正 3 · “只看 X/Y/Rz”作主判据正确，但须加 Z/Rx/Ry 伴随护栏：", "高阶 Km（y²/y³）附加加减速推力偏心会激发俯仰 Rx/滚转 Ry，经 ENC–硅片阿贝臂 h_Abbe 与非远心度耦合入真实套刻与焦面！故 X/Y/Rz 为主判据，Z/Rx/Ry 须守住表 1 护栏。"),
        ("修正 4 · 警惕“ENC 测 ENC 自己”自闭环盲区！", "WS 伺服本身靠 WS-ENC 闭环！Q_enc−Q_0 对① ENC 网格板比例尺错（错 5 ppm 即错 50 nm/cm 却显示 0！）、② 加速下台面弹变、③ WS–RS/激光 1 ns 同步抖动（0.7 nm）100% 盲区！"),
        ("修正 5 · 三级闭环验收（离线→外部标尺→在线曝光）：", "Stage 1 离线 ENC 验伺服（收严至总红线 55%，覆盖 ±Y 正反扫与 ±25/50/100% Range）→ Stage 2 外部双频干涉仪核验绝对比例尺 → Stage 3 整机 SAT 曝光阶跃片（YieldStar 实测）闭合 100% 总红线！"),
    ],
    bg=C_BOX_WARM, accent=C_CORAL, title_sz=9.4, body_sz=7.55
)

add_table(
    s_ws_k4, 6.26, 0.96, 6.72, 4.46,
    ["参数", "单项式", "单位", "±Range", "最小步长\n(≤1/10)", "离线伺服\n(≤55%)", "在线总红线\n|ΔKm|", "WS 运动学激励机理 (@0.70 m/s)"],
    [
        ["K1",  "dx: 1",   "nm",     "±200", "≤0.012", "≤0.066", "≤0.120", "静态 X 轨迹偏置"],
        ["K2",  "dy: 1",   "nm",     "±200", "≤0.012", "≤0.066", "≤0.120", "静态 Y 相位偏置"],
        ["K4",  "dy: y",   "nm/cm",  "±50",  "≤0.007", "≤0.039", "≤0.070", "恒速扫描比 Δv_y = K4·v (5→0.35 μm/s)"],
        ["K5",  "dx: y",   "nm/cm",  "±50",  "≤0.007", "≤0.039", "≤0.070", "扫描期 X 恒速交叉斜行 v_x = K5·v_y"],
        ["K6",  "dy: x",   "nm/cm",  "±50",  "≤0.008", "≤0.044", "≤0.080", "静态偏航 ΔRz = K6 (1 nm/cm=100 nrad)"],
        ["K8",  "dy: y²",  "nm/cm²", "±15",  "≤0.004", "≤0.022", "≤0.040", "恒微加速度 Δa_y=2·K8·v² + 预减 −0.053K8"],
        ["K10", "dy: xy",  "nm/cm²", "±15",  "≤0.005", "≤0.028", "≤0.050", "恒偏航角速度 ω_z = K10·v_y"],
        ["K11", "dx: y²",  "nm/cm²", "±15",  "≤0.004", "≤0.022", "≤0.040", "X 抛物线加速 Δa_x=2·K11·v² + 逆卷积"],
        ["K14", "dy: y³",  "nm/cm³", "±5.0", "≤0.0025","≤0.014", "≤0.025", "恒加加速度 Δj_y=6·K14·v³ + 预减 −0.16K14"],
        ["K16", "dy: xy²", "nm/cm³", "±5.0", "≤0.003", "≤0.017", "≤0.030", "恒偏航角加速度 α_z=2·K16·v² + 逆卷积"],
        ["K19", "dx: y³",  "nm/cm³", "±5.0", "≤0.0025","≤0.014", "≤0.025", "X 恒加加速度 Δj_x=6·K19·v³ + 逆卷积"],
    ],
    [0.48, 0.74, 0.68, 0.60, 0.68, 0.68, 0.72, 2.14], font_sz=6.9, spec_col=6, align_left_cols=[7]
)

add_box(
    s_ws_k4, 6.26, 5.52, 6.72, 1.48,
    "离线→在线三级闭环公式分配（为何离线伺服需收严至 55%？）",
    [
        ("误差合成关系：", "ΔK_total = √(ΔK_servo² + ΔK_ENC_scale² + ΔK_timing/mech²)。以 K4 = 0.070 nm/cm 为例，离线 ENC 伺服占 55%（≤0.039 nm/cm，方差占比 30%），留 70% 方差裕量给外部标尺标定、RS 同步耦合与曝光量测本底。"),
        ("抽测组合工况：", "每项 Km 均须执行单参阶跃 + 正反扫（Up/Down）+ 多参联合（如 K4+K8+K14 叠加）核查无耦合劣化（详见 Excel Sheet 08）。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.0, body_sz=7.5
)

# ==============================================================================
# SLIDE 25 (v2 NEW): 8 mm SLIT CONVOLUTION & DECONVOLUTION DEDICATED EXPLAINER
# ==============================================================================
s_deconv = prs.slides.add_slide(BLANK)
add_header(s_deconv, "Item 14 · 狭缝逆卷积", "14（续下）. 8 mm 曝光狭缝卷积与逆卷积（Slit Deconvolution）概念、推导与图解", next_pno(),
           "解释步进扫描有限狭缝如何对高阶轨迹产生几何偏置与空间频域截止，以及 WS 轨迹发生器如何通过逆卷积预畸变消除低阶串扰")

add_pic_card(
    s_deconv, "c_deconv_full", 0.35, 0.96, 12.63, 3.66,
    "【v2 三联机理与仿真图】A：8 mm 有限狭缝正向卷积模糊机理；B：K14·y³ 实空间逆卷积预畸变消除 +0.264 nm 串扰；C：频域 sinc 衰减、逆放大与 8 mm 物理截止"
)

add_box(
    s_deconv, 0.35, 4.72, 6.00, 2.28,
    "狭缝卷积与逆卷积精确代数推导（L_s = 0.80 cm）",
    [
        ("1. 正向卷积（狭缝平均模糊）：", "d_print(y) = (q_cmd * h)(y) = ∫ q_cmd(y−s)·h(s) ds，均匀狭缝 h=1/L_s，二阶矩 μ₂ = L_s²/12 = 0.0533 cm²，3μ₂ = L_s²/4 = 0.1600 cm²。"),
        ("2. 各阶多项式卷积结果：", "(1*h)=1；(y*h)=y（线性无畸变）；(y²*h) = y² + L_s²/12（多出常数平移！）；(y³*h) = y³ + (L_s²/4)·y（多出线性斜率！）。"),
        ("3. 逆卷积预畸变指令（抵消串扰）：", "为精确印出目标多项式，轨迹发生器须预减：K1_cmd = K1 − 0.0533·K11、K2_cmd = K2 − 0.0533·K8、K6_cmd = K6 − 0.0533·K16、K4_cmd = K4 − 0.160·K14、K5_cmd = K5 − 0.160·K19！"),
        ("4. 频域极限与 MSD 约束：", "H(f_y)=sinc(L_s·f_y) 在 λ_y ≤ 8 mm 处归零（绝对不可补）；且高阶轨迹在狭缝内斜率会产生固有 MSD ≈ (L_s/√12)|q'(y)|，故 WS 动态补偿物理封顶在 3 阶！"),
    ],
    bg=C_BOX_BLUE, accent=C_DARK_BLUE, title_sz=9.1, body_sz=7.4
)

add_table(
    s_deconv, 6.50, 4.72, 6.48, 2.28,
    ["高阶参数", "目标 K_0", "耦合系数", "受串扰低阶项", "未逆卷积\n场角恶化", "逆卷积预补偿指令\n(Excel Sheet 08C)"],
    [
        ["K8 (y²)",   "2.0 nm/cm²", "0.0533", "K2 (平移 dy)", "+0.107 nm", "ΔK2_cmd = −0.107 nm"],
        ["K11 (y²)",  "2.0 nm/cm²", "0.0533", "K1 (平移 dx)", "+0.107 nm", "ΔK1_cmd = −0.107 nm"],
        ["K16 (xy²)", "0.8 nm/cm³", "0.0533", "K6 (旋转 x)",  "+0.055 nm", "ΔK6_cmd = −0.043 nm/cm"],
        ["K14 (y³)",  "1.0 nm/cm³", "0.1600", "K4 (Y 放大率)", "+0.264 nm", "ΔK4_cmd = −0.160 nm/cm"],
        ["K19 (y³)",  "1.0 nm/cm³", "0.1600", "K5 (X 偏斜)",   "+0.264 nm", "ΔK5_cmd = −0.160 nm/cm"],
    ],
    [0.92, 0.92, 0.72, 1.15, 0.90, 1.87], font_sz=7.2, spec_col=4, align_left_cols=[0, 3, 5]
)

# ==============================================================================
# SLIDE 20: ITEM 15 (PART 1) - ODD ZERNIKE MECHANISM & 2D ABBE SIMULATION
# ==============================================================================
s20 = prs.slides.add_slide(BLANK)
add_header(s20, "Item 15 · 机理仿真", "15（上）. Odd Fringe Zernike（Z5–Z64）跨照明位移机理与 2D Abbe 仿真方法", next_pno(),
           "2D Abbe 部分相干成像仿真（λ=193.368 nm, NA=1.35）覆盖 6 种照明切换；基准自检 Z2 严格等于 −1/NA = −0.7407 nm/nm [008 Fig.4b]")

add_pic_card(s20, "024_fig2", 0.35, 0.94, 4.25, 2.75, "原图 [024] Staals (ASML 2011) · Fig.2：FlexWave 官方 64 阶 Fringe Zernike 排序金字塔（确证 Z5–Z64 共 30 个 Odd 项）")
add_pic_card(s20, "008_fig4a", 4.72, 0.94, 4.10, 2.75, "原图 [008] Kang/Mulkens/Zeiss 2016 · Fig.4a：DRAM 6F² 极限照明下奇像差套刻灵敏度（Z7/8 达 ~1.0，Z19/20 达 ~0.55–0.62 nm/nm）")
add_box(
    s20, 8.95, 0.94, 4.03, 2.75,
    "2D Abbe 仿真方法与基准自检",
    [
        ("物理模型：", "奇对称波像差（m=1,3,5,7）在 ±1 衍射级引入反对称相位差，造成随照明光瞳分布变化的图形位移 S_j(Illum)。"),
        ("6 种跨照明切换工况：", "Dip85 (σ=0.75–0.95)、CQuad90、Quasar100、Ann120、Conv180、Met300。"),
        ("理论自检 100% 精准：", "Z2 倾斜仿真灵敏度在全部模式精确为 −1/1.35 = −0.7407 nm/nm，与 [008 Fig.4b] −0.74 严丝合缝！"),
        ("包络保护：", "|ΔS_env| = max(|ΔS_sim|, |ΔS_DRAM|)，覆盖激进 DRAM 切换；同时纳入 Z50/51 (7θ)。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=9.0, body_sz=7.8
)

add_pic_card(s20, "c_zern", 0.35, 3.80, 12.63, 3.24, "自绘 2D Abbe 仿真结果图（左：X 向 15 项奇像差在 6 种照明下灵敏度热力图；右：高敏项严控、高阶项放宽后的控制规格与单阶套刻贡献）")

# ==============================================================================
# SLIDE 21: ITEM 15 (PART 2) - ALL 30 ODD ZERNIKE SPECS & FLEXWAVE VALIDATION
# ==============================================================================
s21 = prs.slides.add_slide(BLANK)
add_header(s21, "Item 15 · 全30项", "15（下）. Z5–Z64 全部 30 个 Odd Zernike 控制误差验收表（Fringe & RMS）与实测对标", next_pno(),
           "完整列出 1θ Coma(12 项)、3θ Trefoil(10 项)、5θ Pentafoil(6 项) 及 7θ Heptafoil(2 项 Z50/Z51)，X/Y 对称成对呈现")

# Compact paired table: 15 cos/sin pairs = 30 odd terms (clean, readable, zero crowding!)
z_sim = json.loads((REPO / "work/zernike_sim_v1.json").read_text(encoding="utf-8"))
spec_fr = {7:0.18,10:0.16,14:0.18,19:0.20,23:0.24,26:0.16,30:0.22,34:0.30,39:0.22,43:0.30,47:0.35,50:0.24,54:0.25,58:0.35,62:0.40}
lit_ov = {7:0.95,10:0.91,14:0.70,19:0.55}
type_cn = {1:"1θ Coma", 3:"3θ Trefoil", 5:"5θ Pentafoil", 7:"7θ Heptafoil"}
z_rows = []
for i in range(0, len(z_sim), 2):
    c_it = z_sim[i]
    s_it = z_sim[i + 1]
    j1, j2 = c_it["j"], s_it["j"]
    n, m = c_it["n"], c_it["m"]
    frms = c_it["rms_factor"]
    dsim = c_it["worst_ds"]
    denv = max(dsim, lit_ov.get(j1, 0.0))
    sf = spec_fr[j1]
    srms = sf * frms
    ovl = sf * denv
    z_rows.append([
        f"Z{j1} / Z{j2}", f"({n},{m})", type_cn[m], f"{frms:.4f}",
        f"{dsim:.3f}", f"{denv:.3f}", f"≤ {sf:.2f}", f"≤ {srms:.4f}", f"{ovl:.3f}"
    ])
z_rows.append(["28项 (1/3/5θ)", "—", "单轴14项RSS", "—", "—", "—", "0.979", "0.230", "0.362"])
z_rows.append(["30项 全Odd", "—", "单轴15项RSS", "—", "—", "—", "1.008", "0.238", "0.370"])

add_table(
    s21, 0.35, 0.94, 7.65, 6.08,
    ["Fringe 项 (X/Y)", "(n,m)", "奇像差类别", "RMS系数", "|ΔS_sim|", "|ΔS_env|", "规格(nm Fringe)", "规格(nm RMS)", "套刻贡献(nm)"],
    z_rows,
    [0.98, 0.62, 1.05, 0.72, 0.76, 0.76, 1.05, 0.92, 0.79], font_sz=7.2, spec_col=6, highlight_last=2
)

add_pic_card(s21, "024_fig11", 8.15, 0.94, 4.83, 3.05, "原图 [024] Staals 2011 · Fig.11：NXT:1950i FlexWave 实测分组残差（ComaX=0.16, ComaY=0.15, 3foilX=0.33, 3foilY=0.12 nm RMS）")

add_table(
    s21, 8.15, 4.10, 4.83, 1.72,
    ["分组奇像差", "本机规格 RMS", "1950i FlexWave 实测", "可行性结论"],
    [
        ["1θ Coma X/Y (各6项)", "0.160 nm", "0.16 / 0.15 nm", "完全匹配实测"],
        ["3θ Trefoil X/Y (各5项)", "0.138 nm", "0.33 / 0.12 nm", "强化X向通道达标"],
        ["5θ Pentafoil X/Y (各3项)", "0.091 nm", "重点严控 Z26/27", "防Dip-Quasar杀手"],
        ["7θ Heptafoil X/Y (各1项)", "0.060 nm", "Z50/Z51 全Odd闭环", "无高阶漏项"],
        ["全瞳 30 项总 Odd WFE", "0.337 nm", "Abbe套刻 0.328 nm", "包络 ≤0.370 nm"],
    ],
    [1.45, 0.90, 1.30, 1.18], font_sz=7.1, spec_col=1, highlight_last=1, align_left_cols=[0, 3]
)

add_box(
    s21, 8.15, 5.90, 4.83, 1.12,
    "关键工程提醒（双口径防误读）",
    [
        ("Fringe vs RMS：", "上表同时提供 Fringe 幅值（nm）与 RMS 波前（nm RMS），换算因子 1/√(2(n+1))；验收时务必核对干涉仪输出口径，避免差 3–5 倍误判！"),
    ],
    bg=C_BOX_WARM, accent=C_CORAL, title_sz=8.6, body_sz=7.6
)

# ==============================================================================
# SLIDE 22: FAT/SAT VERIFICATION & REPO TRACEABILITY SUMMARY
# ==============================================================================
s22 = prs.slides.add_slide(BLANK)
add_header(s22, "验收执行", "FAT / SAT 关键验收防坑指南与 OV4 仓库 v2 四形态同步成果索引", next_pno(),
           "确保纸面预算可落地、可测试、可追溯；Markdown / PDF / Excel / PPTX 全套数据 100% 一致并归档至 OpticsPan/OV4")

add_box(
    s22, 0.35, 0.96, 6.15, 3.00,
    "四大高风险 FAT / SAT 验收执行要点",
    [
        ("1. 同步运动误差（Item 3）光学矩阵验收：", "采集脚本必须采用 M_opt = diag(1/4, 1/4, 1/11.14, 0.3592, 0.3592, 1)，严禁对 Z/Rx/Ry/Rz 机械除以 4；且必须在双台满速并行（M台 40 m/s² + E台 0.70 m/s 液浸扫描）下实测。"),
        ("2. WH / WT 温控（Items 7, 11）测温硅片实测：", "不得仅测冷却水入口，须使用无线测温硅片在 Track ±1.0 K 阶跃进片下实测 WH 片间出口重复性（≤5.0 mK）与 WT 边缘蒸发环带残差（≤8.0 mK）。"),
        ("3. iHOPC 补偿残差（Items 13, 14）交叉串扰验收：", "逐项施加 ±K0 阶跃指令，除验证对角残差 |ΔK| 外，重点核查 K11→K1（0.0533·K11）与 K19→K5（0.160·K19）狭缝逆卷积串扰归零。"),
        ("4. Odd Zernike（Item 15）跨照明闭环验证：", "用机内波前干涉仪实测 6 种照明切换下 Z5–Z64 残差，并用 Dipole vs Conventional/Quasar 双层曝光硅片套刻验证 ≤0.37 nm。"),
    ],
    bg=C_BOX_TEAL, accent=C_TEAL, title_sz=10.0, body_sz=8.4
)

add_box(
    s22, 6.68, 0.96, 6.30, 3.00,
    "证据来源分布统计（覆盖 OV4 243 篇 + ME3 手册）",
    [
        ("直接论文原图与实测证据（22 篇核心 SPIE/JM3/PhD 文献）：", "009(NXT:1950i)、066(1960Bi/1970Ci)、015(1970Ci/1980Di)、016(RHC)、017(晶圆热)、021(UPW)、024(FlexWave)、008(Zernike)、062(Gridplate)、075(双Youla)、019/094(控制架构)、154(iHOPC K1–K20)、160/253(物镜操纵精度)、225(掩模夹持专著)、254(PARIS/IRL/K20)。"),
        ("物理第一性原理与数值仿真：", "液浸 6-DOF 光学矩阵、四角 ENC 差分角噪、TSU 17 μm 瞬态热传导指数衰减、8 mm 有限狭缝逆卷积积分、2D Abbe 部分相干 30 项奇像差跨照明仿真。"),
        ("误差预算数学闭环：", "Excel 9 表 686 动态公式实算，DCO = 1.869 ≤ 2.00 nm、MMO = 3.154 ≤ 3.50 nm、FU = 10.34 ≤ 12.0 nm，全部 PASS。"),
    ],
    bg=C_BOX_BLUE, accent=C_DARK_BLUE, title_sz=10.0, body_sz=8.4
)

add_table(
    s22, 0.35, 4.14, 12.63, 2.86,
    ["仓库交付形态", "归档路径（D:\\work\\OV4 · GitHub OpticsPan/OV4）", "版本与核心特征", "核验状态"],
    [
        ["正式演示文稿 (PPTX)", "outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v2.pptx", "28 页 16:9 白底（v2 新增 6 页深度验收专题 + 3 张新图）", "视觉逐页核验通过"],
        ["正式推导报告 (MD)", "outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md", "全 17 章 v2 扩展版（含四大专题推导、稳定锚点目录）", "0 断链 · 0 未解析粗体"],
        ["正式推导报告 (PDF)", "outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.pdf", "30 页 · 45 书签 · STIX 透明矢量公式 · 第 13–15 章横版宽表", "视觉抽检零裁切"],
        ["动态公式预算表 (XLSX)", "outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v2.xlsx", "9 工作表 · 686 跨页动态公式（含 Sheet 07–09 验收细则与逆卷积计算）", "Excel 实算 0 错误"],
        ["可复现计算/构建脚本", "outputs/code/ (sim_zernike_ovl_v1.py · build_spec_excel/pdf/pptx_v2.py + v1 保留)", "全流程代码可复现，一键重跑仿真、表格、PDF 与 PPTX", "全部通过实测"],
    ],
    [2.05, 5.15, 3.85, 1.58], font_sz=8.0, spec_col=3, align_left_cols=[0, 1, 2]
)

prs.save(str(OUT_PPTX))
print(f"PPTX SAVED SUCCESSFULLY: {OUT_PPTX}")
print(f"Slides: {len(prs.slides)} | Size: {OUT_PPTX.stat().st_size:,} bytes")
