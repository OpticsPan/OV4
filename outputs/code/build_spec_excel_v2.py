import json
import math
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRATCH = os.path.join(REPO, "work")
OUT_XLSX = r"D:\work\OV4\outputs\tables\NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v2.xlsx"

with open(os.path.join(SCRATCH, "zernike_sim_v1.json"), "r", encoding="utf-8") as f:
    z_sim = json.load(f)

# ==============================================================================
# Styling Palette (Clean Engineering Navy/Slate Theme)
# ==============================================================================
FONT_NAME = "Microsoft YaHei"
NAVY = "1F3864"
MED_BLUE = "2F5597"
LIGHT_BLUE = "D9E1F2"
SUBHDR_BLUE = "E9EDF4"
ZEBRA = "F7F9FC"
ACCENT_GREEN = "E2EFDA"
ACCENT_AMBER = "FFF2CC"
ACCENT_GRAY = "EDEDED"
BORDER_COLOR = "BFBFBF"
DARK_BORDER = "44546A"

thin_side = Side(style="thin", color=BORDER_COLOR)
med_dark = Side(style="medium", color=DARK_BORDER)
double_bottom = Side(style="double", color=NAVY)

border_cell = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
border_hdr = Border(left=thin_side, right=thin_side, top=med_dark, bottom=med_dark)
border_total = Border(left=thin_side, right=thin_side, top=thin_side, bottom=double_bottom)

font_title = Font(name=FONT_NAME, size=14, bold=True, color="FFFFFF")
font_subtitle = Font(name=FONT_NAME, size=10, italic=True, color="1F3864")
font_sec = Font(name=FONT_NAME, size=11, bold=True, color="1F3864")
font_hdr = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFF")
font_body = Font(name=FONT_NAME, size=9.5, bold=False, color="000000")
font_bold = Font(name=FONT_NAME, size=9.5, bold=True, color="000000")
font_spec = Font(name=FONT_NAME, size=9.5, bold=True, color="003399")
font_note = Font(name=FONT_NAME, size=9, italic=True, color="595959")
font_na = Font(name=FONT_NAME, size=9.5, italic=True, color="7F7F7F")

fill_title = PatternFill("solid", fgColor=NAVY)
fill_hdr = PatternFill("solid", fgColor=MED_BLUE)
fill_sec = PatternFill("solid", fgColor=LIGHT_BLUE)
fill_subhdr = PatternFill("solid", fgColor=SUBHDR_BLUE)
fill_zebra = PatternFill("solid", fgColor=ZEBRA)
fill_white = PatternFill("solid", fgColor="FFFFFF")
fill_total = PatternFill("solid", fgColor=ACCENT_GREEN)
fill_warn = PatternFill("solid", fgColor=ACCENT_AMBER)
fill_gray = PatternFill("solid", fgColor=ACCENT_GRAY)

al_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
al_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
al_right = Alignment(horizontal="right", vertical="center", wrap_text=True)

def style_banner(ws, row, ncols, text):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
    c = ws.cell(row=row, column=1, value=text)
    c.font = font_title
    c.fill = fill_title
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 28

def style_section(ws, row, ncols, text):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
    c = ws.cell(row=row, column=1, value=text)
    c.font = font_sec
    c.fill = fill_sec
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    for col in range(1, ncols + 1):
        ws.cell(row=row, column=col).border = border_hdr
        ws.cell(row=row, column=col).fill = fill_sec
    ws.row_dimensions[row].height = 22

def write_header_row(ws, row, headers):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = font_hdr
        c.fill = fill_hdr
        c.alignment = al_center
        c.border = border_hdr
    ws.row_dimensions[row].height = 26

def set_col_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

wb = openpyxl.Workbook()
# Remove default sheet
wb.remove(wb.active)

# Create all 6 sheets in order
ws1 = wb.create_sheet("01_总览与套刻焦面预算闭环")
ws2 = wb.create_sheet("02_1-4_运动台同步与ENC规格")
ws3 = wb.create_sheet("03_5-12_对准温控夹持框架规格")
ws4 = wb.create_sheet("04_13-14_iHOPC物镜与WS残差")
ws5 = wb.create_sheet("05_15_Odd_Zernike(Z5-Z64)")
ws6 = wb.create_sheet("06_参考文献与证据索引")
ws7 = wb.create_sheet("07_WS与RS独立验收及往返方案")
ws8 = wb.create_sheet("08_WS_iHOPC验收与狭缝逆卷积")
ws9 = wb.create_sheet("09_物镜Kn八维能力评价体系")

for ws in [ws1, ws2, ws3, ws4, ws5, ws6]:
    ws.views.sheetView[0].showGridLines = True

# ==============================================================================
# SHEET 2: Items 1-4 (WS 6-DOF, RS 6-DOF, WS-RS/4 Sync MA 6-DOF, ENC 16 rows)
# ==============================================================================
style_banner(ws2, 1, 10, "大类 1–4：晶圆台(WS)、掩模台(RS)、WS-RS同步运动误差(MA)与编码器(ENC)逐明细验收规格")
ws2.merge_cells("A2:J2")
c = ws2.cell(2, 1, "光学耦合基准：ArF液浸 λ=193.368 nm，NA=1.35，液浸水折射率 n_w=1.4366，4×缩小投影（β=1/4）；物理耦合矩阵 M_opt = diag(1/4, 1/4, n_w/16=1/11.14, n_w/4=0.3592, n_w/4=0.3592, 1)。狭缝 26×8 mm，扫速 0.70 m/s（MA窗口 11.4 ms）。")
c.font = font_subtitle
c.alignment = al_left
ws2.row_dimensions[2].height = 24

# Put constants in hidden/reference cells? Better: put explicit Optical Parameter mini-table in rows 3-4 or use exact constants in formulas so transparent!
hdr2 = ["序号", "大类", "子项 / 自由度", "验收规格值\n(主量纲)", "单位", "晶圆等效值\n(1× 换算)", "统计口径 / 验收工况", "对套刻/焦面影响", "依据类型", "数值推导理由与文献依据"]
write_header_row(ws2, 4, hdr2)

# Track exact row indices for cross-sheet linking!
row = 5

# --- Item 1: WS 6-DOF ---
style_section(ws2, row, 10, "1. WS（晶圆台）6自由度重复性误差验收规格（逐自由度6行，以Gridplate ENC为参考基准）")
row += 1
ws_start = row
item1_rows = [
    ("1.1", "1. WS 6-DOF", "WS-X 重复性误差 (非扫描向)", 0.32, "nm", "=D6", "曝光窗口 MA 3σ @ 0.70 m/s（静态定位≤0.30 nm）", "套刻 X: 0.32 nm", "调研+预算反推",
     "对标NXT:1950i同步MA-X实测0.47 nm [009 Fig.10]，目标机型同步MA-X收紧至0.40 nm；按WS占同步方差约64%（RS/4占36%）反推 sqrt(0.32²+0.24²)=0.40 nm。"),
    ("1.2", "1. WS 6-DOF", "WS-Y 重复性误差 (扫描向)", 0.36, "nm", "=D7", "曝光窗口 MA 3σ @ 0.70 m/s（静态定位≤0.30 nm）", "套刻 Y: 0.36 nm", "调研+预算反推",
     "Y向为高速扫描轴（30–40 m/s²折返+液浸头弯月面拖拽扰动），对标NXT:1950i同步MA-Y实测0.49 nm [009 Fig.10]，目标同步MA-Y=0.45 nm，按WS占64%反推0.36 nm。"),
    ("1.3", "1. WS 6-DOF", "WS-Z 重复性误差 (焦面向)", 4.50, "nm", "=D8", "曝光窗口 MA 3σ @ 0.70 m/s（陶瓷WS动态跟随）", "焦面 Z: 4.50 nm", "直接调研+预算",
     "直接对标NXT:1965Ci/1970Ci陶瓷WS实测MAz峰值4 nm、95%≤6 nm [066 Fig.9]；考虑同步MA-Z目标5.0 nm与RS-Z贡献2.15 nm，反推WS-Z=4.50 nm。"),
    ("1.4", "1. WS 6-DOF", "WS-Rx 重复性误差 (绕X轴俯仰)", 0.20, "μrad", "=D9", "曝光窗口 MA 3σ @ 0.70 m/s（200 nrad）", "8mm狭缝边缘离焦: 0.80 nm", "解析计算+预估",
     "Rx沿8 mm狭缝半宽(4 mm)产生离焦 Δz=4 mm×Rx；取0.20 μrad对应0.80 nm离焦，满足与RS-Rx合成后同步Rx≤0.25 μrad（边缘离焦1.00 nm）。"),
    ("1.5", "1. WS 6-DOF", "WS-Ry 重复性误差 (绕Y轴滚转)", 0.10, "μrad", "=D10", "曝光窗口 MA 3σ @ 0.70 m/s（100 nrad）", "26mm狭缝边缘离焦: 1.30 nm", "解析计算+预估",
     "Ry沿26 mm狭缝半宽(13 mm)产生离焦 Δz=13 mm×Ry，杠杆臂为Rx的3.25倍，故规格须严格收紧至0.10 μrad（对应边缘离焦1.30 nm，同步合成后1.56 nm）。"),
    ("1.6", "1. WS 6-DOF", "WS-Rz 重复性误差 (绕Z轴偏航)", 0.012, "μrad", "=D11", "曝光窗口 MA 3σ @ 0.70 m/s（12 nrad）", "26mm狭缝边缘套刻Y: 0.156 nm", "解析计算+预算",
     "Rz直接在26 mm狭缝半宽(13 mm)诱发面内套刻 Δy=13 mm×Rz；12 nrad对应0.156 nm，与RS-Rz(9 nrad, 1:1耦合)合成15 nrad（边缘套刻0.195 nm）。"),
]
for idx, rdata in enumerate(item1_rows):
    fill = fill_white if idx % 2 == 0 else fill_zebra
    for col, val in enumerate(rdata, 1):
        cell = ws2.cell(row, col, val)
        cell.fill = fill
        cell.border = border_cell
        cell.font = font_spec if col == 4 else font_body
        cell.alignment = al_center if col in (1, 4, 5, 6, 9) else al_left
        if col in (4, 6):
            cell.number_format = "0.000" if rdata[3] < 0.05 else "0.00"
    ws2.row_dimensions[row].height = 34
    row += 1

# --- Item 2: RS 6-DOF ---
style_section(ws2, row, 10, "2. RS（掩模台）6自由度重复性误差验收规格（逐自由度6行；同时给出掩模侧4×与晶圆等效1×值）")
row += 1
rs_start = row
# Rows will be 13..18
item2_rows = [
    ("2.1", "2. RS 6-DOF", "RS-X 重复性误差 (掩模非扫描向)", 0.96, "nm", "=D13/4", "曝光窗口 MA 3σ @ 2.80 m/s，光学耦合系数 1/4", "晶圆套刻 X: 0.24 nm", "调研+预算反推",
     "掩模侧X经4×物镜缩小为1/4；RS短行程采用微动洛伦兹电机+空气轴承/平衡质量块，0.96 nm（晶圆侧0.24 nm）占同步MA-X(0.40 nm)方差36% [009, 019, 075]。"),
    ("2.2", "2. RS 6-DOF", "RS-Y 重复性误差 (掩模扫描向)", 1.08, "nm", "=D14/4", "曝光窗口 MA 3σ @ 2.80 m/s、150 m/s²折返，耦合 1/4", "晶圆套刻 Y: 0.27 nm", "调研+预算反推",
     "RS以4倍扫速(2.6–3.0 m/s)与约150 m/s²极高加速度往返扫描 [019, 094]，Y向整定残差略大于X向；1.08 nm（晶圆侧0.27 nm）与WS-Y合成0.45 nm。"),
    ("2.3", "2. RS 6-DOF", "RS-Z 重复性误差 (掩模焦面向)", 24.00, "nm", "=D15*1.4366/16", "曝光窗口 MA 3σ，液浸纵向耦合 n_w/16 = 1/11.14", "晶圆焦面 Z: 2.15 nm", "解析计算+调研",
     "液浸光刻纵向放大率为 β²·n_w = 1.4366/16 = 1/11.14 [225 Sec.2.1.3]（非1/4！）；RS-Z=24 nm折算晶圆仅2.15 nm，与WS-Z(4.5 nm)合成5.0 nm。"),
    ("2.4", "2. RS 6-DOF", "RS-Rx 重复性误差 (掩模绕X轴俯仰)", 0.42, "μrad", "=D16*1.4366/4", "曝光窗口 MA 3σ，Scheimpflug倾角耦合 n_w/4 = 0.359", "晶圆等效 0.151 μrad (离焦0.60 nm)", "解析计算+预估",
     "根据Scheimpflug物像倾角关系，掩模倾角耦合至液浸晶圆面系数为 β·n_w = 1.4366/4 = 0.3592；RS-Rx=0.42 μrad等效晶圆0.151 μrad，与WS-Rx合成0.25 μrad。"),
    ("2.5", "2. RS 6-DOF", "RS-Ry 重复性误差 (掩模绕Y轴滚转)", 0.19, "μrad", "=D17*1.4366/4", "曝光窗口 MA 3σ，Scheimpflug倾角耦合 n_w/4 = 0.359", "晶圆等效 0.068 μrad (离焦0.89 nm)", "解析计算+预估",
     "沿104 mm掩模狭缝(晶圆26 mm)的横向滚转倾角，按0.3592系数耦合至晶圆面0.068 μrad，与WS-Ry(0.10 μrad)合成0.12 μrad（边缘离焦1.56 nm）。"),
    ("2.6", "2. RS 6-DOF", "RS-Rz 重复性误差 (掩模绕Z轴偏航)", 0.009, "μrad", "=D18*1", "曝光窗口 MA 3σ（9 nrad），面内转角耦合 1:1", "晶圆边缘套刻 Y: 0.117 nm", "解析计算+预算",
     "关键物理约束：面内偏航Rz在物像面为1:1严格等角耦合（非1/4！掩模52 mm边缘位移0.47 nm缩小4×即0.117 nm=13 mm×9 nrad）；与WS-Rz(12 nrad)合成15 nrad。"),
]
for idx, rdata in enumerate(item2_rows):
    fill = fill_white if idx % 2 == 0 else fill_zebra
    for col, val in enumerate(rdata, 1):
        cell = ws2.cell(row, col, val)
        cell.fill = fill
        cell.border = border_cell
        cell.font = font_spec if col == 4 else font_body
        cell.alignment = al_center if col in (1, 4, 5, 6, 9) else al_left
        if col in (4, 6):
            cell.number_format = "0.000" if rdata[3] < 0.05 or col == 6 and idx >= 3 else "0.00"
    ws2.row_dimensions[row].height = 36
    row += 1

# --- Item 3: WS-RS/4 Sync MA 6-DOF (+ MSD ref) ---
style_section(ws2, row, 10, "3. WS-RS 同步运动误差（物理定义 e = WS - M_opt·RS，工程习称 WS-RS/4 的 6自由度 MA；附 MSD 参考）")
row += 1
sync_start = row
# Rows will be 20..27 (20..25 are 6-DOF MA, 26..27 are MSD ref)
item3_rows = [
    ("3.1", "3. WS-RS同步MA", "Sync MA-X = MA(X_WS - X_RS/4)", 0.40, "nm", "=SQRT(F6^2+F13^2)", "曝光窗口 11.4 ms MA 3σ @ 0.70 m/s（全片扫描）", "直接套刻 X: 0.40 nm", "直接调研+闭环",
     "NXT:1950i实测0.47 nm [009 Fig.10]，NXT:1970Ci/1980Di达~0.30–0.35 nm；目标定0.40 nm。F列为WS与RS/4非相关RSS合成值（实际主从前馈/双Youla控制[075]可再降10–25%留裕度）。"),
    ("3.2", "3. WS-RS同步MA", "Sync MA-Y = MA(Y_WS - Y_RS/4)", 0.45, "nm", "=SQRT(F7^2+F14^2)", "曝光窗口 11.4 ms MA 3σ @ 0.70 m/s（扫描主轴）", "直接套刻 Y: 0.45 nm", "直接调研+闭环",
     "NXT:1950i实测0.49 nm [009 Fig.10]，目标机型在0.65–0.75 m/s扫速下收紧至0.45 nm（叠加Rz边缘套刻0.195 nm后综合Y向同步套刻0.49 nm）。"),
    ("3.3", "3. WS-RS同步MA", "Sync MA-Z = MA(Z_WS - (n_w/16)·Z_RS)", 5.00, "nm", "=SQRT(F8^2+F15^2)", "曝光窗口 MA 3σ（纵向耦合系数 1/11.14，非1/4）", "直接焦面 Z: 5.00 nm", "直接调研+解析",
     "直接对标NXT:1965Ci/1970Ci陶瓷WS实测MAz峰值4 nm、95%≤6 nm [066 Fig.9]；由WS-Z(4.50 nm)与RS-Z等效(2.15 nm)合成4.99 nm，支撑整机FU≤12.0 nm。"),
    ("3.4", "3. WS-RS同步MA", "Sync MA-Rx = MA(Rx_WS - (n_w/4)·Rx_RS)", 0.25, "μrad", "=SQRT(F9^2+F16^2)", "曝光窗口 MA 3σ（250 nrad，倾角耦合 0.359）", "8mm狭缝边缘离焦: 1.00 nm", "解析计算+预算",
     "由WS-Rx(0.20 μrad)与RS-Rx等效(0.151 μrad)合成0.251 μrad；在±4 mm狭缝边缘产生1.00 nm离焦。"),
    ("3.5", "3. WS-RS同步MA", "Sync MA-Ry = MA(Ry_WS - (n_w/4)·Ry_RS)", 0.12, "μrad", "=SQRT(F10^2+F17^2)", "曝光窗口 MA 3σ（120 nrad，倾角耦合 0.359）", "26mm狭缝边缘离焦: 1.56 nm", "解析计算+预算",
     "由WS-Ry(0.10 μrad)与RS-Ry等效(0.068 μrad)合成0.121 μrad；在±13 mm狭缝边缘产生1.56 nm离焦，与MA-Z/MA-Rx合成同步焦面总贡献5.33 nm。"),
    ("3.6", "3. WS-RS同步MA", "Sync MA-Rz = MA(Rz_WS - 1·Rz_RS)", 0.015, "μrad", "=SQRT(F11^2+F18^2)", "曝光窗口 MA 3σ（15 nrad，面内转角 1:1耦合）", "26mm狭缝边缘套刻Y: 0.195 nm", "解析计算+预算",
     "由WS-Rz(12 nrad)与RS-Rz(9 nrad)按1:1耦合合成15.0 nrad；在±13 mm狭缝边缘产生0.195 nm Y向套刻（±4 mm产生0.060 nm X向套刻）。"),
    ("3.7", "3. WS-RS同步(附)", "Sync MSD-XY (曝光窗口内高频抖动参考)", 1.80, "nm", "=D26", "曝光窗口内移动标准差 MSD 1σ（不影响套刻均值）", "主要影响对比度/CDU，不计入OVL", "直接调研+预估",
     "对标NXT:1950i–1970Ci及Arnold 3nm预算 [009, 060, 165]，MSD-XY≤1.8 nm保证成像对比度衰减<1%且不劣化线宽均匀性CDU。"),
    ("3.8", "3. WS-RS同步(附)", "Sync MSD-Z (焦面高频抖动参考)", 10.00, "nm", "=D27", "曝光窗口内移动标准差 MSD 1σ", "影响有效DOF与对比度", "直接调研+预估",
     "高频Z向残余振动控制在≤10 nm(1σ)，保证NA=1.35高数值孔径下有效焦深(DOF)不显著损失 [066, 165]。"),
]
for idx, rdata in enumerate(item3_rows):
    fill = fill_gray if idx >= 6 else (fill_white if idx % 2 == 0 else fill_zebra)
    for col, val in enumerate(rdata, 1):
        cell = ws2.cell(row, col, val)
        cell.fill = fill
        cell.border = border_cell
        cell.font = font_spec if (col == 4 and idx < 6) else (font_note if idx >= 6 else font_body)
        cell.alignment = al_center if col in (1, 4, 5, 6, 9) else al_left
        if col in (4, 6):
            cell.number_format = "0.000" if rdata[3] < 0.05 else "0.00"
    ws2.row_dimensions[row].height = 38 if idx < 6 else 28
    row += 1

# --- Item 4: ENC Metrology Repeatability (16 rows) ---
style_section(ws2, row, 10, "4. ENC（光栅编码器底层测量系统）测量重复性误差验收规格（涵盖 WS 6-DOF、宽带/拼接/网格板稳定性及 RS 6-DOF）")
row += 1
enc_start = row
item4_rows = [
    ("4.1", "4. ENC(WS)", "WS-ENC X 曝光窗口测量重复性", 0.12, "nm", "=D29", "曝光MA等效带宽(~44 Hz), 3σ（不含伺服跟踪）", "底层量测：占WS-X(0.32)方差14%", "直接调研+预算",
     "遵循量测精度为运动台1/3原则；NXT网格板编码器气隙<15 mm，1000 Hz宽带噪声0.22 nm [009 Fig.4]，经11.4 ms曝光窗口平均滤波后低频残余重复性≤0.12 nm。"),
    ("4.2", "4. ENC(WS)", "WS-ENC Y 曝光窗口测量重复性", 0.12, "nm", "=D30", "曝光MA等效带宽(~44 Hz), 3σ", "底层量测：占WS-Y(0.36)方差11%", "直接调研+预算",
     "同WS-ENC X，采用四角落45°切向二维光栅读数头消除阿贝误差，Y向扫描期间有效重复性≤0.12 nm [009, 062]。"),
    ("4.3", "4. ENC(WS)", "WS-ENC Z 曝光窗口测量重复性", 0.35, "nm", "=D31", "曝光MA等效带宽(~44 Hz), 3σ", "底层量测：占WS-Z(4.5)方差<1%", "直接调研+预估",
     "2D干涉编码器Z向读数灵敏度略低于XY平面向；0.35 nm(3σ)远低于4.5 nm的WS-Z动态误差，不构成焦面瓶颈 [062]。"),
    ("4.4", "4. ENC(WS)", "WS-ENC Rx 曝光窗口测量重复性", 0.003, "μrad", "=D32", "曝光MA等效带宽, 3σ（3 nrad）", "底层量测：占WS-Rx(200 nrad) 1.5%", "解析计算",
     "由4个角落读数头Z向差分计算（基线跨度L≈320 mm）：理论噪声 σ_Rx ≈ √2·0.35/320 = 1.55 nrad，留2×工程余量定为3.0 nrad。"),
    ("4.5", "4. ENC(WS)", "WS-ENC Ry 曝光窗口测量重复性", 0.003, "μrad", "=D33", "曝光MA等效带宽, 3σ（3 nrad）", "底层量测：占WS-Ry(100 nrad) 3%", "解析计算",
     "同WS-ENC Rx，四角Z通道差分基线L≈320 mm，角度测量噪声底≤3.0 nrad，充分支撑100 nrad闭环控制。"),
    ("4.6", "4. ENC(WS)", "WS-ENC Rz 曝光窗口测量重复性", 0.0015, "μrad", "=D34", "曝光MA等效带宽, 3σ（1.5 nrad）", "底层量测：占WS-Rz(12 nrad) 12.5%", "解析计算",
     "由四角XY切向读数头差分计算（基线L≈320 mm）：理论噪声 √2·0.12/320 = 0.53 nrad，计入头间标定与气隙扰动留余量定为1.5 nrad。"),
    ("4.7", "4. ENC(WS)", "WS-ENC 单轴宽带测量噪声 (1000 Hz)", 0.20, "nm", "=D35", "0–1000 Hz 宽带噪声 3σ（动态控制环输入）", "决定伺服高频噪声注入与MSD", "直接调研",
     "直接对标NXT:1950i实测编码器宽带噪声0.22 nm (3σ @ 1000 Hz，相较XT干涉仪0.90 nm @ 40 Hz提升4×以上) [009 Fig.4] 及Nikon S620D 0.25 nm [060, 063]，收紧至0.20 nm。"),
    ("4.8", "4. ENC(WS)", "WS-ENC 多读数头切换(Handover)拼接重复性", 0.15, "nm", "=D36", "测量/曝光切换及读数头过缝瞬间 3σ", "影响全片网格局部连续性", "调研+预估",
     "NXT四读数头系统在300 mm大行程与M/E换台时动态切换3-of-4有效读数头 [062 Sec.4]，在线自标定拼接残差须≤0.15 nm以避免全片跳变。"),
    ("4.9", "4. ENC(WS)", "Gridplate 光栅网格板中长期稳定性 (7天)", 0.18, "nm", "=D37", "7天网格漂移 3σ（含MF 10 mK温控）", "决定机台网格校准周期与MMO稳定", "直接调研",
     "直接对标NXT:1950i实测网格板7天稳定性<0.20 nm [009 Sec.4]；采用超低膨胀微晶玻璃(Zerodur/ULE, CTE≤20 ppb/K)配合10 mK气幕温控实现。"),
    ("4.10", "4. ENC(RS)", "RS-ENC X 曝光窗口测量重复性 (掩模侧)", 0.32, "nm", "=D38/4", "曝光MA等效带宽, 3σ，掩模侧4×", "晶圆等效 0.08 nm（占RS-X 1/3）", "预算反推",
     "按底层量测为RS-X(0.96 nm)的1/3分配；掩模侧短程光栅尺/干涉混合测量在5 mK层流气幕下确保0.32 nm（晶圆侧0.08 nm）。"),
    ("4.11", "4. ENC(RS)", "RS-ENC Y 曝光窗口测量重复性 (掩模侧)", 0.36, "nm", "=D39/4", "曝光MA等效带宽, 3σ @ 2.80 m/s 扫速", "晶圆等效 0.09 nm（占RS-Y 1/3）", "预算反推",
     "掩模高速扫描轴(2.6–3.0 m/s)读数头插补与高速细分误差略高于X轴，按RS-Y(1.08 nm)的1/3分配为0.36 nm（晶圆等效0.09 nm）。"),
    ("4.12", "4. ENC(RS)", "RS-ENC Z 曝光窗口测量重复性 (掩模侧)", 2.50, "nm", "=D40*1.4366/16", "曝光MA等效带宽, 3σ，掩模侧4×", "晶圆等效 0.22 nm（占RS-Z 10%）", "解析+预估",
     "RS垂向采用编码器/电容传感器组合，2.50 nm(3σ)折算至晶圆焦面仅0.22 nm，占RS-Z(24 nm)的10%。"),
    ("4.13", "4. ENC(RS)", "RS-ENC Rx 曝光窗口测量重复性 (掩模侧)", 0.025, "μrad", "=D41*1.4366/4", "曝光MA等效带宽, 3σ（25 nrad）", "晶圆等效 9.0 nrad", "解析计算",
     "基于RS垂向传感器基线L≈180 mm，√2·2.5/180 ≈ 19.6 nrad，留余量定25 nrad（远小于RS-Rx 420 nrad）。"),
    ("4.14", "4. ENC(RS)", "RS-ENC Ry 曝光窗口测量重复性 (掩模侧)", 0.020, "μrad", "=D42*1.4366/4", "曝光MA等效带宽, 3σ（20 nrad）", "晶圆等效 7.2 nrad", "解析计算",
     "基于RS横向传感器跨度L≈200 mm，√2·2.5/200 ≈ 17.7 nrad，定20 nrad（占RS-Ry 190 nrad 的10.5%）。"),
    ("4.15", "4. ENC(RS)", "RS-ENC Rz 曝光窗口测量重复性 (掩模侧)", 0.0025, "μrad", "=D43*1", "曝光MA等效带宽, 3σ（2.5 nrad，1:1耦合）", "晶圆等效 2.5 nrad（占RS-Rz 28%）", "解析计算",
     "RS面内偏航由两侧Y/X读数头差分测得（跨度L≈200 mm）：√2·0.36/200 = 2.55 nrad，严格控制≤2.5 nrad以支撑RS-Rz≤9 nrad闭环。"),
    ("4.16", "4. ENC(RS)", "RS-ENC 宽带测量噪声 (1000 Hz, 掩模XY)", 0.60, "nm", "=D44/4", "0–1000 Hz 宽带噪声 3σ，掩模侧4×", "晶圆等效 0.15 nm（支撑MSD-XY）", "调研+预算",
     "掩模台高速运行下读数头宽带噪声≤0.60 nm（折算晶圆0.15 nm），避免高频噪声经150 m/s²控制带宽放大劣化MSD-XY。"),
]
for idx, rdata in enumerate(item4_rows):
    fill = fill_white if idx % 2 == 0 else fill_zebra
    for col, val in enumerate(rdata, 1):
        cell = ws2.cell(row, col, val)
        cell.fill = fill
        cell.border = border_cell
        cell.font = font_spec if col == 4 else font_body
        cell.alignment = al_center if col in (1, 4, 5, 6, 9) else al_left
        if col in (4, 6):
            cell.number_format = "0.0000" if rdata[3] < 0.005 else ("0.000" if rdata[3] < 0.05 else "0.00")
    ws2.row_dimensions[row].height = 35
    row += 1

set_col_widths(ws2, [7, 15, 32, 12, 8, 12, 26, 24, 13, 52])
ws2.freeze_panes = "A5"

# ==============================================================================
# SHEET 3: Items 5-12 (AA, TIS/PARIS, WT Temp, Reticle Temp, RT Clamp, WT Clamp, WH Temp, Frame)
# ==============================================================================
style_banner(ws3, 1, 9, "大类 5–12：对准系统(AA / TIS-PARIS)、温控(WT / Reticle / WH)、夹持(RT / WT)与整机框架(Frame)逐明细验收规格")
ws3.merge_cells("A2:I2")
c = ws3.cell(2, 1, "物性常数基准：单晶硅热膨胀系数 α_Si = 2.6 ppm/K（300 mm 半径 150 mm 对应 0.39 nm/mK；视场半高 16.5 mm 对应 0.043 nm/mK）；石英掩模 α_q = 0.55 ppm/K（晶圆侧视场半高 16.5 mm 对应 0.0091 nm/mK）；空气折射率温漂 |dn/dT| = 0.93 ppm/K。")
c.font = font_subtitle
c.alignment = al_left
ws3.row_dimensions[2].height = 24

hdr3 = ["序号", "大类", "验收子项明细", "验收规格值", "单位", "统计口径 / 验收工况", "等效套刻 / 焦面影响", "依据类型", "数值推导理由与文献依据"]
write_header_row(ws3, 4, hdr3)

row3 = 5
# Dictionary to capture exact row numbers for linking into Sheet 1!
s3_rows = {}

sections_s3 = [
    ("5. M-side 晶圆对准系统（Advanced Align：Athena / SMASH 四色多级次）测量重复性误差", [
        ("5.1", "5. M-side AA", "单标记静态测量重复性 (标准参考硅片)", 0.20, "nm", "WQ ≥ 1%，四色(532/633/780/852 nm)，3σ，X/Y", "传感本底噪声 0.20 nm", "直接调研",
         "直接对标NXT:1970Ci SMASH实测数据：WQ≥1%时单标记REPRO=0.15–0.25 nm [015 Fig.10]；取0.20 nm作为静态传感本底规格。"),
        ("5.2", "5. M-side AA", "单标记动态扫描测量重复性 (含WS定位)", 0.35, "nm", "WQ ≥ 1%，测量侧动态扫瞄，3σ，X/Y", "单标记动态误差 0.35 nm", "调研+合成",
         "包含M-side WS定位误差(~0.29 nm)与光学本底(0.20 nm)合成：sqrt(0.20²+0.29²)=0.35 nm [009, 015]。"),
        ("5.3", "5. M-side AA", "低信号工艺硅片单标记重复性", 0.45, "nm", "低WQ = 0.1%–1.0%，工艺不透明膜层，3σ，X/Y", "工艺片抗衰减能力", "直接调研",
         "直接对标NXT:1970Ci SMASH在WQ=0.1%–1%区间的实测REPRO=0.25–0.50 nm [015 Fig.10]，确保先进逻辑/DRAM后段暗场工艺层对准精度。"),
        ("5.4", "5. M-side AA", "多波长颜色间/衍射级次间配准稳定性", 0.30, "nm", "24 h 内四色(532–852 nm)及多级次相对偏移，3σ", "支撑工艺不对称加权配方", "调研+预估",
         "SMASH/ORION通过多颜色多级次线性组合抑制CMP/刻蚀造成的标记不对称 [006, 009]；颜色间漂移≤0.30 nm保证配方切换不引入偏置。"),
        ("5.5", "5. M-side AA", "全晶圆对准网格拟合重复性 (Wafer Grid Repro)", 0.35, "nm", "N≥20 标记，6参/高阶HOWA模型全片3σ，X/Y", "计入DCO直接项: 0.35 nm", "调研+预算反推",
         "对标NXT:1950i对准占DCO约0.50–0.61 nm [009 Fig.3]；经多标记平均抑噪并含残余非线性网格拟合误差，分配0.35 nm(单次曝光)。"),
        ("5.6", "5. M-side AA", "M-to-E 对准基线短期漂移 (Baseline Drift)", 0.25, "nm", "片内/批间未重校时段(~10–30 min)，3σ，X/Y", "计入DCO直接项: 0.25 nm (与5.5合成0.43 nm)", "调研+预算反推",
         "计量框架(MF)上AA传感器与物镜相对短期漂移；每片/每批经TIS/PARIS校准清零，残余短期基线漂移≤0.25 nm，与5.5合成AA总项0.43 nm。"),
        ("5.7", "5. M-side AA", "工艺标记不对称诱发对准残差 (WAD 抑制)", 0.45, "nm", "典型工艺片(CMP/金属层)四色优化后残差，3σ", "计入MMO/OPO匹配项(不计DCO)", "调研+预估",
         "对标NXT:1960Bi–1970Ci SMASH对工艺不对称的抑制能力 [006, 015]，用于整机MMO/产品片套刻闭环。"),
    ]),
    ("6. E-side 空间像对准系统（TIS / PARIS）重复性误差", [
        ("6.1", "6. E-side TIS/PARIS", "TIS 水平空间像对准重复性 (XY)", 0.35, "nm", "6 kHz双传感板，重复测量3σ，X/Y", "支撑双台基准零点与RA平移", "直接调研+预算",
         "NXT平台升级6 kHz高吞吐量TIS双传感板 [009, 266]，单点水平重复性≤0.35 nm，保障M-to-E基准标定精度。"),
        ("6.2", "6. E-side TIS/PARIS", "TIS 垂向最佳焦面测量重复性 (Z)", 2.50, "nm", "空间像Z扫描寻峰，重复测量3σ", "计入焦面FU闭环: 2.50 nm", "调研+预算反推",
         "直接决定E-side最佳焦面(Best Focus)标定基准；控制在2.50 nm仅占12.0 nm整机焦面预算方差的4.3%。"),
        ("6.3", "6. E-side TIS/PARIS", "PARIS 掩模对准重复性 (RA, 7视场点并行)", 0.40, "nm", "7视场点并行曝光空间像拟合，3σ，X/Y", "计入DCO直接项: 0.40 nm", "直接调研",
         "直接对标NXT:1960Bi–1970Ci PARIS 7点平行测量规格 <0.5 nm (3σ) [066 Sec.3.4] 及NXT:1970Ci实测RA重复性~0.43 nm [011]，定为0.40 nm。"),
        ("6.4", "6. E-side TIS/PARIS", "PARIS 7视场点焦面/像场弯曲测量重复性 (Z)", 3.00, "nm", "7视场点Z向焦面/场曲测量，3σ", "支撑镜头/掩模热场曲补偿", "调研+预估",
         "实时捕获掩模加热与物镜加热导致的狭缝像场弯曲变化，为动态焦面补偿提供高可靠反馈 [066]。"),
        ("6.5", "6. E-side TIS/PARIS", "PARIS/ILC 奇像差波前测量重复性 (Z7/Z8等效)", 0.12, "nm RMS", "奇像差主阶单次测量3σ（约0.34 nm Fringe）", "对套刻二次贡献 ≤ 0.28 nm", "直接调研",
         "直接对标NXT:2050i(沿用1970Ci代PARIS架构)实测PARIS像差测量对套刻二次贡献0.28–0.34 nm [254 Fig.2]，反推单次主奇像差测量噪底≤0.12 nm RMS。"),
        ("6.6", "6. E-side TIS/PARIS", "双台 TIS-1 / TIS-2 传感板匹配稳定性 (24h)", 0.25, "nm", "24 h 双台参考板相对偏移，3σ，X/Y", "计入双台匹配/MMO(不计同台DCO)", "调研+预估",
         "防止双台交替曝光产生系统性台间偏置(Chuck-to-Chuck Offset)，保障双台同批生产一致性 [009, 066]。"),
    ]),
    ("7. Wafer Table（晶圆台 WT）温控误差", [
        ("7.1", "7. WT温控", "WT 内部冷却水(WTCW)供水温度短期稳定性", 2.0, "mK", "±2.0 mK（1 h / 连续批内 3σ），细加热器闭环", "全局线性膨胀可补偿，瞬态残差<0.15 nm", "调研+物理推导",
         "参考ME3 TWINSCAN细加热器水控架构(分辨<0.1 mK [01-TT_Lay_L3])与液浸热控要求 [017, 184]，±2.0 mK保证硅片热基线高度稳定。"),
        ("7.2", "7. WT温控", "WT 顶面空间温度均匀性 (300 mm全片区)", 5.0, "mK", "300 mm 瘤点接触区峰谷值 PV（径向/周向）", "不可校高阶热变形残差 ≤ 0.22 nm", "物理仿真+调研",
         "硅CTE=2.6 ppm/K，径向/周向非均匀温差产生不可被线性放大率吸收的高阶网格畸变（敏感度~0.045 nm/mK [017]），5 mK PV对应≤0.22 nm。"),
        ("7.3", "7. WT温控", "WT 边缘区(Edge/BES液浸蒸发)局部温控残差", 8.0, "mK", "晶圆外缘20 mm环带(R=130–150 mm)，3σ", "晶圆边缘局部套刻残差 ≤ 0.25 nm", "调研+物理推导",
         "液浸头跨过晶圆边缘时残留水膜蒸发吸热导致局部降温 [017, 184]；须配备独立边缘加热区(Zone Heater)将边缘温降残差抑至≤8 mK（局部套刻≤0.25 nm）。"),
        ("7.4", "7. WT温控", "液浸超纯水(UPW)供水温度稳定性", 2.0, "mK", "±2.0 mK（液浸头出口 3σ）", "消除水膜对硅片局部热冲击(<0.12 nm)", "直接调研",
         "直接对标ASML XT:1900i实测UPW温控±2.5 mK [021, 057]；针对1950i–1970i套刻收紧20%至±2.0 mK，同时抑制水折射率热扰动对焦面的影响。"),
        ("7.5", "7. WT温控", "双台 WT1 与 WT2 平均温度匹配差", 2.0, "mK", "|T_WT1 - T_WT2| 稳态均值差", "未校差0.78 nm，经双台缩放标定后残差≤0.15 nm", "物理计算+预估",
         "双台温差直接造成300 mm硅片0.39 nm/mK的台间缩放差；控制≤2.0 mK可使系统性差异轻松被双台校准吸收且不引入高阶失配。"),
        ("7.6", "7. WT温控", "高剂量连续曝光片内稳态热漂移残差 (含WHC)", 4.0, "mK", "30 mJ/cm²、230 wph 首场至末场等效非均匀残差", "WT+液浸综合套刻残差 ≤ 0.35 nm (计入DCO)", "调研+预算反推",
         "对标NXT:1950i晶圆加热+液浸占DCO约0.42 nm [009 Fig.3]；经WHC前馈补偿后WT热残差控制在0.35 nm（与WH 0.20 nm合成总晶圆热项0.40 nm）。"),
    ]),
    ("8. Reticle（掩模）附近温控误差", [
        ("8.1", "8. Reticle温控", "掩模台水平层流气幕(RS Air Shower)温度稳定性", 5.0, "mK", "±5.0 mK（出风口 3σ），水平层流风场", "保护RS光学测量光路(≤0.12 nm晶圆等效)", "直接调研+解析",
         "ME3手册 [08-TT-L3-RSbook] 指出水平层流气幕保护RS测量光路并避免冲击物镜表面；空气|dn/dT|=0.93 ppm/K，100 mm光程下5 mK对应0.47 nm(掩模)/0.12 nm(晶圆)。"),
        ("8.2", "8. Reticle温控", "掩模-物镜顶面气隙温度梯度波动", 10.0, "mK", "气隙内时空温差波动 3σ（配合微环境吹扫）", "气隙折射率扰动引起视场点间套刻 ≤ 0.25 nm", "直接调研+解析",
         "NXT:1970Ci/1980Di掩模加热研究 [016 Fig.2] 揭示气隙对流湍流(Air point-to-point noise)是重要随机误差源；压制气隙温差≤10 mK使点间噪声≤0.25 nm。"),
        ("8.3", "8. Reticle温控", "掩模台夹持底座(RS Chuck)冷却水温控稳定性", 5.0, "mK", "±5.0 mK（RS冷却回路 3σ）", "阻隔RS短行程线圈热传导至掩模(<0.05 nm)", "调研+物理计算",
         "防止RS 150 m/s²高加速驱动电机发热通过底座传导造成石英掩模边缘非均匀翘曲；石英α_q=0.55 ppm/K，5 mK热传导影响可忽略(<0.05 nm)。"),
        ("8.4", "8. Reticle温控", "机内掩模库(IRL)预温控精度", 300.0, "mK", "±0.30 °C（相对曝光室基准温度）", "初始线性热胀≤2.7 nm(被RA吸收)，高阶残差≤0.10 nm", "直接调研",
         "对标ASML掩模库温控演进：1980Di/2050i为±0.4°C、2100i升级至±0.2°C [254 Sec.2.2]；取±0.3°C(±300 mK)保障换片初期无剧烈热瞬态。"),
        ("8.5", "8. Reticle温控", "曝光过程掩模加热片内非均匀温升残差 (经RHC)", 30.0, "mK", "经RHC前馈补偿后不可校高阶等效ΔT，3σ", "掩模加热片内套刻残差 ≤ 0.27 nm (与8.2合成0.37 nm)", "直接调研+解析",
         "石英掩模α_q=0.55 ppm/K，在晶圆侧16.5 mm视场半高敏感度仅0.0091 nm/mK；强紫外吸收绝对温升可达0.3–1 K，经RHC补偿90–95%后残余30 mK对应0.27 nm [016]。"),
    ]),
    ("9. RT（掩模台）对掩模的夹持误差", [
        ("9.1", "9. RT夹持", "掩模夹持不可校正平面内变形 (NCE IPD)", 0.25, "nm", "晶圆等效1×（掩模侧≤1.00 nm），扣除线性项，3σ", "计入MMO跨机夹持匹配(×√2=0.35 nm)", "直接调研",
         "直接对标ASML/TU/e掩模夹持专著目标：掩模夹持不可校正套刻变形NCE < 0.28 nm（晶圆1×）[225 Sec.2.1.2]；目标留微余量定0.25 nm。"),
        ("9.2", "9. RT夹持", "掩模重复卸载-重夹持变形重复性", 0.15, "nm", "晶圆等效1×（掩模侧≤0.60 nm），同片重装，3σ", "计入DCO直接项: 0.15 nm", "调研+预估",
         "表征真空吸盘静摩擦力随机释放与掩模重装一致性；重夹持重复性为NCE的60%(0.15 nm)，支撑同机DCO≤2.0 nm [225]。"),
        ("9.3", "9. RT夹持", "高加速度扫描下掩模微滑移 (SUSD方向差)", 0.15, "nm", "晶圆等效1×（掩模侧≤0.60 nm），@ 150 m/s²，3σ", "计入DCO直接项: 0.15 nm (与9.2合成0.21 nm)", "调研+预估",
         "掩模台在150 m/s²折返加速度下承受极高惯性剪切力 [019, 225]，正反扫(Scan-Up/Down)微滑移滞回须≤0.15 nm（晶圆1×）。"),
        ("9.4", "9. RT夹持", "掩模夹持面外平坦度变形 (Out-of-plane Z)", 2.00, "nm", "晶圆等效1×（掩模侧≤22.3 nm，按n_w/16换算），3σ", "计入焦面FU闭环: 2.00 nm", "直接调研",
         "直接引用ASML/TU/e专著焦面预算目标：掩模夹持引起的晶圆面离焦 ≤ 2.0 nm [225 Sec.2.1.3]；按液浸纵向放大率16/1.4366=11.14折算掩模侧22.3 nm。"),
        ("9.5", "9. RT夹持", "掩模真空吸盘接触面平坦度 (机械基准)", 50.0, "nm", "吸盘接触面全局峰谷平坦度 PV", "支撑9.1/9.4实现的基础形位公差", "工程预估",
         "控制真空吸盘支撑面机械平坦度≤50 nm PV及低颗粒污染设计，确保6寸石英掩模在重力与真空吸附下不发生高阶弯曲。"),
    ]),
    ("10. WT（晶圆台）对晶圆的夹持误差", [
        ("10.1", "10. WT夹持", "平坦硅片重复吸片不可校正变形重复性", 0.25, "nm", "参考平坦硅片，扣除线性项，3σ，X/Y", "计入DCO直接项: 0.25 nm", "直接调研+预算",
         "直接对标NXT:1950i DCO分解中晶圆夹持占比~0.20–0.25 nm [009 Fig.3]；衡量瘤点静摩擦随机滞回与抽真空时序重复性 [097, 122]。"),
        ("10.2", "10. WT夹持", "双台 WT1 与 WT2 夹持指纹匹配差", 0.35, "nm", "同批次平坦硅片跨台差，3σ，X/Y", "计入双台匹配/MMO(不计同台DCO)", "调研+预估",
         "反映两块瘤点台面几何分布与摩擦系数一致性；经双台夹持指纹前馈标定后残差控制在≤0.35 nm [066, 186]。"),
        ("10.3", "10. WT夹持", "翘曲工艺硅片夹持平面内变形残差 (50 μm Bow)", 0.55, "nm", "标称50 μm弓形翘曲硅片，非校正IPD，3σ", "计入MMO晶圆夹持项(综合可达0.95 nm)", "直接调研+建模",
         "对标NXT:1965Ci/1970Ci实测WT全片套刻影响由1.2 nm降至1.0 nm [066 Fig.10a] 及Turner/ASML夹持模型 [097, 122]，需低摩擦DLC瘤点与分区抽真空优化。"),
        ("10.4", "10. WT夹持", "高速扫描下晶圆微滑移 (SUSD / SLSR)", 0.15, "nm", "@ 35–40 m/s²步进/扫描折返，3σ，X/Y", "计入DCO直接项: 0.15 nm (与10.1合成0.29 nm)", "调研+预估",
         "晶圆台在35–40 m/s²加速度下，硅片与瘤点间弹性微剪切及微滑移引起的正反扫/左右步进方向差须≤0.15 nm [122]。"),
        ("10.5", "10. WT夹持", "WT 瘤点全局平坦度引起的焦面误差 (Z)", 6.00, "nm", "300 mm全片有效曝光区焦面分布，3σ", "计入焦面FU闭环: 6.00 nm (最大单项)", "直接调研",
         "直接对标NXT:1965Ci/1970Ci新一代高平坦WT实测焦面贡献由9.4 nm大幅改善至6.2 nm [066 Fig.10a]；定6.00 nm以保证整机FU≤12.0 nm。"),
        ("10.6", "10. WT夹持", "WT 瘤点局部平坦度与接触面积比 (结构基准)", 15.0, "nm", "26×33 mm 视场内局部PV（接触面积比1%–3%）", "抑制局部颗粒热点(Hotspot)离焦", "直接调研+预估",
         "低接触面积比(1%–3%)降低背面颗粒夹杂概率，视场内局部瘤点顶面PV≤15 nm以控制高频离焦与局部弯曲IPD [066, 186]。"),
    ]),
    ("11. Wafer Handler（晶圆传输单元 WH）温控误差", [
        ("11.1", "11. WH温控", "TSU 预温控台冷却水(共用LCW)温度稳定性", 2.0, "mK", "±2.0 mK（与物镜冷却水LCW共用高稳回路，3σ）", "提供全机最稳定热参考基准", "直接调研",
         "ME3 TWINSCAN手册 [01-TT_Lay_L3, 05-TT-L2-WH] 明确说明TSU直接通入LCW回路，是整机最稳定的温度参考基准，细加热器稳至±2.0 mK。"),
        ("11.2", "11. WH温控", "WH 洁净气幕与 TSU 水温匹配偏差 (ACC Offset)", 15.0, "mK", "±15.0 mK（经NTC实测标定ACC偏置后残差）", "对硅片平衡温度偏移 < 0.20 mK", "直接调研+物理推导",
         "ME3 [01-TT_Lay_L3] 要求用NTC将气幕与TSU温差校零；因空气对流换热(h≈20 W/m²K)远弱于TSU 17 μm气浮导热(U=1529 W/m²K)，15 mK气幕差仅导致0.2 mK偏移。"),
        ("11.3", "11. WH温控", "WH 出口硅片平均温度与 WT 目标静态偏差", 10.0, "mK", "±10.0 mK（在Track进片±1.0 K范围内）", "系统偏置可被M-to-E标定吸收(残差<0.08 nm)", "物理传热仿真",
         "由300 mm硅片热容C''=1263.5 J/(m²K)与TSU 17 μm气隙导热U=1529 W/(m²K) [05-TT-L2-WH] 得 τ_TSU=0.826 s；停留4.5 s衰减e^-5.4≈1/230，±1 K进片可稳至±10 mK内。"),
        ("11.4", "11. WH温控", "WH 出口硅片片间温度重复性 (核心DCO项)", 5.0, "mK", "片间随机出口温度波动 3σ", "M-to-E瞬态残差 ≤ 0.20 nm (计入DCO)", "物理传热仿真",
         "核心物理推导：硅片上WT后时间常数τ_WT≈2.0–2.5 s，M-side平均对准(t≈5 s)至E-side曝光(t≈12 s)残余衰减比约8%–13%；随机5 mK出口波动导致ΔT_M→E≈0.4–0.5 mK → 0.16–0.20 nm套刻！"),
        ("11.5", "11. WH温控", "WH 出口硅片面内空间温度均匀性", 10.0, "mK", "300 mm 硅片面内径向/周向温度峰谷 PV", "WT上快速热扩散后残余非线性套刻 ≤ 0.12 nm", "物理传热仿真",
         "避免硅片离开预对准台时带有明显径向温度梯度（如边缘与中心温差过大），10 mK PV经WT快速热均衡后对曝光套刻影响≤0.12 nm。"),
        ("11.6", "11. WH温控", "涂胶显影机(Track)进片温度接口耐受范围", 1000.0, "mK", "±1.0 K（系统外部接口验收边界条件）", "边界输入条件（非机内误差）", "工程规范",
         "在230 wph节拍(15.6 s/片、TSU停留≥4.5 s)下，TSU 200:1 以上的热衰减能力可充分消化Track传片±1.0 K波动。"),
    ]),
    ("12. 整机 Frame（计量框架 MF 与基础框架 BF）稳定性误差", [
        ("12.1", "12. 整机Frame", "计量框架(MF)-物镜相对动态定位误差 X", 0.15, "nm", "曝光窗口 MA 3σ（含VC-D地基与双台运动）", "底层约束：已包含在Sync MA-X(0.40)中", "调研+预算反推",
         "MF同时承载物镜、Gridplate、AA与LS [009, 019]；MF与物镜间高频相对变形直接进入Sync MA，须控制在0.15 nm(占0.40 nm方差14%)。"),
        ("12.2", "12. 整机Frame", "计量框架(MF)-物镜相对动态定位误差 Y", 0.15, "nm", "曝光窗口 MA 3σ（含双台高加速扫描）", "底层约束：已包含在Sync MA-Y(0.45)中", "调研+预算反推",
         "扫描向反作用力由Balance Mass吸收并通过Air Mount阻隔，MF-物镜相对Y向动态MA残余≤0.15 nm [019, 094]。"),
        ("12.3", "12. 整机Frame", "计量框架(MF)-物镜相对动态定位误差 Z", 1.50, "nm", "曝光窗口 MA 3σ", "计入焦面FU框架动态项(≤2.0 nm)", "调研+预算反推",
         "控制MF与物镜垂向相对动态呼吸变形≤1.50 nm，仅占5.0 nm同步MA-Z方差的9%，保证NA=1.35焦面稳定。"),
        ("12.4", "12. 整机Frame", "计量框架(MF)-物镜相对动态转角 Rx", 0.040, "μrad", "曝光窗口 MA 3σ（40 nrad）", "8mm狭缝边缘离焦: 0.16 nm", "解析计算+预估",
         "MF微俯仰振动经4 mm狭缝半宽仅引入0.16 nm离焦，远小于同步Rx(250 nrad)预算。"),
        ("12.5", "12. 整机Frame", "计量框架(MF)-物镜相对动态转角 Ry", 0.025, "μrad", "曝光窗口 MA 3σ（25 nrad）", "26mm狭缝边缘离焦: 0.33 nm", "解析计算+预估",
         "MF微滚转振动经13 mm狭缝半宽引入0.33 nm离焦，占同步Ry(120 nrad)方差约4%。"),
        ("12.6", "12. 整机Frame", "计量框架(MF)-物镜相对动态转角 Rz", 0.004, "μrad", "曝光窗口 MA 3σ（4 nrad）", "26mm狭缝边缘套刻Y: 0.052 nm", "解析计算+预估",
         "MF扭转模态残余≤4 nrad，仅占同步Rz(15 nrad)方差7%，边缘套刻影响仅0.052 nm。"),
        ("12.7", "12. 整机Frame", "双台协同运动串扰残差 (M台对E台)", 0.10, "nm", "Measure台40 m/s²步进时Expose台XY MA 3σ", "底层约束：验证BM+Air Mount解耦效果", "调研+预算",
         "TWINSCAN双台架构要求测量台高加速步进不干扰曝光台 [019, 094, 266]；依靠水平平衡质量块(BM)与主动空气弹簧解耦将串扰压至≤0.10 nm。"),
        ("12.8", "12. 整机Frame", "MF 热机械短期基线漂移 (片内 ~16 s)", 0.15, "nm", "单晶圆曝光周期(~16 s)内M-to-E基线漂移，3σ", "底层约束：包含在5.6短期基线(0.25 nm)内", "调研+物理推导",
         "MF采用高热容低膨胀结构并通入MFCW精密水冷，保证单晶圆曝光周期内AA相对物镜的热机械漂移≤0.15 nm。"),
        ("12.9", "12. 整机Frame", "MF 热机械24小时无校准基线漂移", 1.50, "nm", "24 h 连续运行不重校TIS/PARIS时的M-to-E漂移，3σ", "约束整机长期热结构稳定性与校准频次", "调研+工程预估",
         "实际量产每片/每批经TIS/PARIS自动重校清零，但无校准24h本底漂移≤1.50 nm是验收MF结构零应力设计与MFCW温控的核心考核指标。"),
        ("12.10", "12. 整机Frame", "MF 水冷(MFCW)与框架周边气幕温度稳定性", 5.0, "mK", "±5.0 mK(MFCW水冷) / ±10.0 mK(MF气幕)，3σ", "支撑Gridplate 7天<0.18 nm与MF零漂移", "直接调研",
         "直接对标NXT:1950i光栅网格板/计量框架气幕10 mK温控指标 [009 Sec.4] 及ME3 MFCW独立细加热器水控回路 [03-TT-L2-LO]。"),
        ("12.11", "12. 整机Frame", "主动隔振(Air Mount)与框架动态刚度", 0.60, "Hz", "Air Mount垂向/水平固有频率 ≤0.6 Hz；≥20 Hz传递率≤-30 dB；MF首阶模态≥150 Hz", "隔绝地基VC-D/E振动并避免伺服共振", "直接调研",
         "直接对标ASML控制综述 [019, 094] 与ME3 Air Mount手册 [11-TT-L3-AM]：Air Mount f_0≈0.5 Hz主动隔振，物镜配PALM主动阻尼(~90 Hz)，确保伺服高带宽稳定。"),
    ]),
]

for sec_title, items in sections_s3:
    style_section(ws3, row3, 9, sec_title)
    row3 += 1
    for idx, rdata in enumerate(items):
        s3_rows[rdata[0]] = row3
        fill = fill_white if idx % 2 == 0 else fill_zebra
        for col, val in enumerate(rdata, 1):
            cell = ws3.cell(row3, col, val)
            cell.fill = fill
            cell.border = border_cell
            cell.font = font_spec if col == 4 else font_body
            cell.alignment = al_center if col in (1, 4, 5, 8) else al_left
            if col == 4:
                if rdata[3] < 0.01:
                    cell.number_format = "0.000"
                elif rdata[3] < 1.0:
                    cell.number_format = "0.00"
                elif rdata[3] >= 100:
                    cell.number_format = "0.0"
                else:
                    cell.number_format = "0.00" if rdata[4] == "nm" else "0.0"
        ws3.row_dimensions[row3].height = 38
        row3 += 1

set_col_widths(ws3, [7, 17, 34, 11, 9, 28, 26, 14, 56])
ws3.freeze_panes = "A5"

# ==============================================================================
# SHEET 4: Items 13 & 14 (iHOPC Lens & WS Compensation Residuals K1-K20)
# ==============================================================================
style_banner(ws4, 1, 14, "大类 13–14：物镜(Item 13)与晶圆台WS(Item 14)对 iHOPC 场内20参(K1–K20)补偿残差 ΔK = K1 - K0 验收规格")
ws4.merge_cells("A2:N2")
c = ws4.cell(2, 1, "视场坐标定义（遵循 ASML 20参标准 [154 Eq.1 & Table 1]）：狭缝半宽 a = x_max = 1.30 cm（26 mm），扫描半长 b = y_max = 1.65 cm（33 mm）。单相式 x^p·y^q 场角放大系数 G_max = a^p·b^q，场内均匀分布均方根系数 G_rms = [a^p/√(2p+1)]·[b^q/√(2q+1)]。")
c.font = font_subtitle
c.alignment = al_left
ws4.row_dimensions[2].height = 24

# Reference field dimensions in Row 3 so formulas are 100% transparent & editable!
ws4.cell(3, 1, "视场参数:").font = font_bold
ws4.cell(3, 2, "a = x_max (cm)").font = font_body
ws4.cell(3, 3, 1.30).font = font_spec
ws4.cell(3, 3).number_format = "0.00"
ws4.cell(3, 4, "b = y_max (cm)").font = font_body
ws4.cell(3, 5, 1.65).font = font_spec
ws4.cell(3, 5).number_format = "0.00"
ws4.cell(3, 6, "狭缝宽 L_s (cm)").font = font_body
ws4.cell(3, 7, 0.80).font = font_spec
ws4.cell(3, 7).number_format = "0.00"
for col in range(1, 15):
    ws4.cell(3, col).fill = fill_subhdr
    ws4.cell(3, col).border = border_cell
ws4.row_dimensions[3].height = 20

hdr4 = [
    "参数\n编号", "作用\n方向", "单项式\nx^p·y^q", "p\n(x阶)", "q\n(y阶)",
    "物理含义与执行机制", "参数单位", "场角放大\nG_max", "场RMS放大\nG_rms",
    "典型下发\n|K0|", "验收残差规格\n|ΔK|=|K1-K0|", "相对精度\n|ΔK/K0|",
    "最大场角套刻\n残差 (nm)", "场内RMS套刻\n残差 (nm)"
]
write_header_row(ws4, 5, hdr4)

row4 = 6
# --- Item 13: Projection Lens iHOPC ---
style_section(ws4, row4, 14, "13. 物镜（Projection Lens）执行的 iHOPC 场内参数补偿残差（4项纯静态物镜 + 4项扫描同步动态物镜 + K20架构限制说明）")
row4 += 1

lens_ihopc = [
    ("K3",  "dx (X)", "x",     1, 0, "狭缝向放大率 Mx（纯静态物镜：Z向镜片操纵器/波长微调）",        "nm/cm",  4.0, 0.100, True),
    ("K7",  "dx (X)", "x²",    2, 0, "狭缝向二阶梯形/不对称畸变 D2x（纯静态物镜：倾斜/偏心操纵器）",   "nm/cm²", 2.0, 0.080, True),
    ("K12", "dy (Y)", "x²",    2, 0, "狭缝向笑脸弯曲 Bow-Y（纯静态物镜：镜片倾斜/非球面操纵器）",     "nm/cm²", 2.0, 0.080, True),
    ("K13", "dx (X)", "x³",    3, 0, "狭缝向三阶枕形/桶形畸变 D3x（纯静态物镜：球差/Z向镜片组）",      "nm/cm³", 1.2, 0.060, True),
    ("K9",  "dx (X)", "x·y",   1, 1, "X向梯形畸变 Trap-X（动态物镜+扫描：扫描中线性调节Mx/掩模Z倾角）", "nm/cm²", 1.5, 0.060, True),
    ("K15", "dx (X)", "x²·y",  2, 1, "X向手风琴畸变 Acc-X（动态物镜+扫描：扫描中线性调节K7操纵器）",   "nm/cm³", 0.8, 0.045, True),
    ("K17", "dx (X)", "x·y²",  1, 2, "X向C形/桶形畸变 C-X（动态物镜+扫描：扫描中二阶调节Mx/掩模Z轨迹）","nm/cm³", 0.8, 0.035, True),
    ("K18", "dy (Y)", "y·x²",  2, 1, "Y向C形/桶形畸变 C-Y（动态物镜+扫描：扫描中线性调节K12操纵器）",  "nm/cm³", 0.8, 0.045, True),
    ("K20", "dy (Y)", "x³",    3, 0, "【架构限制】狭缝三阶S形畸变 D3y：1950i–1970Ci物镜不支持动态补偿 [154 Table 1]（至NXT:2100i新增Distortion Manipulator支持 [254]）；出厂静畸变控≤0.15", "nm/cm³", 0.0, 0.000, False),
]

lens_start = row4
lens_x_rows = []
lens_y_rows = []
for idx, (K, ax, mono, p, q, desc, unit, k0, dk, active) in enumerate(lens_ihopc):
    r = row4
    fill = fill_warn if not active else (fill_white if idx % 2 == 0 else fill_zebra)
    ws4.cell(r, 1, K)
    ws4.cell(r, 2, ax)
    ws4.cell(r, 3, mono)
    ws4.cell(r, 4, p)
    ws4.cell(r, 5, q)
    ws4.cell(r, 6, desc)
    ws4.cell(r, 7, unit)
    ws4.cell(r, 8, f"=($C$3^D{r})*($E$3^E{r})")
    ws4.cell(r, 9, f"=($C$3^D{r}/SQRT(2*D{r}+1))*($E$3^E{r}/SQRT(2*E{r}+1))")
    if active:
        ws4.cell(r, 10, k0)
        ws4.cell(r, 11, dk)
        ws4.cell(r, 12, f"=K{r}/J{r}")
        ws4.cell(r, 13, f"=K{r}*H{r}")
        ws4.cell(r, 14, f"=K{r}*I{r}")
        if "X" in ax:
            lens_x_rows.append(r)
        else:
            lens_y_rows.append(r)
    else:
        ws4.cell(r, 10, "N/A")
        ws4.cell(r, 11, "N/A (静畸变≤0.15)")
        ws4.cell(r, 12, "N/A")
        ws4.cell(r, 13, 0.0)
        ws4.cell(r, 14, 0.0)

    for col in range(1, 15):
        cell = ws4.cell(r, col)
        cell.fill = fill
        cell.border = border_cell
        cell.font = font_na if not active else (font_spec if col == 11 else font_body)
        cell.alignment = al_left if col == 6 else al_center
    ws4.cell(r, 8).number_format = "0.000"
    ws4.cell(r, 9).number_format = "0.000"
    if active:
        ws4.cell(r, 10).number_format = "0.0"
        ws4.cell(r, 11).number_format = "0.000"
        ws4.cell(r, 12).number_format = "0.0%"
        ws4.cell(r, 13).number_format = "0.000"
        ws4.cell(r, 14).number_format = "0.000"
    ws4.row_dimensions[r].height = 30 if active else 38
    row4 += 1

# Lens X & Y Summary rows
lens_sum_x_row = row4
ws4.merge_cells(start_row=row4, start_column=1, end_row=row4, end_column=12)
ws4.cell(row4, 1, "【Item 13 汇总 — X向】物镜 iHOPC 补偿残差 RSS 合成（K3, K7, K13, K9, K15, K17 共6项）")
ws4.cell(row4, 13, "=SQRT(" + "+".join(f"M{x}^2" for x in lens_x_rows) + ")")
ws4.cell(row4, 14, "=SQRT(" + "+".join(f"N{x}^2" for x in lens_x_rows) + ")")
for col in range(1, 15):
    c = ws4.cell(row4, col)
    c.fill = fill_total; c.border = border_total; c.font = font_bold
    c.alignment = al_right if col == 1 else al_center
ws4.cell(row4, 13).number_format = "0.000"; ws4.cell(row4, 14).number_format = "0.000"
ws4.row_dimensions[row4].height = 24
row4 += 1

lens_sum_y_row = row4
ws4.merge_cells(start_row=row4, start_column=1, end_row=row4, end_column=12)
ws4.cell(row4, 1, "【Item 13 汇总 — Y向】物镜 iHOPC 补偿残差 RSS 合成（K12, K18 共2项，不含不支持的K20）")
ws4.cell(row4, 13, "=SQRT(" + "+".join(f"M{y}^2" for y in lens_y_rows) + ")")
ws4.cell(row4, 14, "=SQRT(" + "+".join(f"N{y}^2" for y in lens_y_rows) + ")")
for col in range(1, 15):
    c = ws4.cell(row4, col)
    c.fill = fill_total; c.border = border_total; c.font = font_bold
    c.alignment = al_right if col == 1 else al_center
ws4.cell(row4, 13).number_format = "0.000"; ws4.cell(row4, 14).number_format = "0.000"
ws4.row_dimensions[row4].height = 24
row4 += 2

# --- Item 14: WS iHOPC ---
style_section(ws4, row4, 14, "14. 晶圆台（WS，配合RS同步扫描轨迹）执行的 iHOPC 场内参数补偿残差（11项全覆盖；含狭缝卷积偏置前馈说明）")
row4 += 1

ws_ihopc = [
    ("K1",  "dx (X)", "1",     0, 0, "X向视场平移 Tx（WS/RS 静态X轨迹偏置；受ENC/零点精度约束）",       "nm",     20.0, 0.120),
    ("K2",  "dy (Y)", "1",     0, 0, "Y向视场平移 Ty（WS/RS 静态Y轨迹偏置；受扫描相位标定约束）",       "nm",     20.0, 0.120),
    ("K4",  "dy (Y)", "y",     0, 1, "扫描向放大率 My（WS/RS 恒速扫描速度比微调 v_WS / (v_RS/4)）",     "nm/cm",   5.0, 0.070),
    ("K5",  "dx (X)", "y",     0, 1, "扫描正交性/偏斜 Skew-X（扫描期间WS线性交叉斜行轨迹 dx/dy）",      "nm/cm",   5.0, 0.070),
    ("K6",  "dy (Y)", "x",     1, 0, "狭缝旋转 Rot-Y（WS相对RS静态Rz偏角 dy = Rz·x；8 nrad级）",       "nm/cm",   5.0, 0.080),
    ("K8",  "dy (Y)", "y²",    0, 2, "Y向二阶放大率 2nd-My（曝光扫描期间施加微小常值加速度偏移；需狭缝偏置前馈）","nm/cm²", 2.0, 0.040),
    ("K10", "dy (Y)", "x·y",   1, 1, "Y向梯形畸变 Trap-Y（扫描期间WS动态线性角速度 dRz/dy）",           "nm/cm²",  1.5, 0.050),
    ("K11", "dx (X)", "y²",    0, 2, "扫描向弓形畸变 Bow-X（扫描期间WS抛物线交叉轨迹；需预补 -L_s²/12·K11）","nm/cm²", 2.0, 0.040),
    ("K14", "dy (Y)", "y³",    0, 3, "Y向三阶放大率 3rd-My（曝光扫描期间施加线性加加速度/Jerk轨迹）",     "nm/cm³",  1.0, 0.025),
    ("K16", "dy (Y)", "x·y²",  1, 2, "Y向手风琴畸变 Acc-Y（扫描期间WS动态抛物线Rz角加速度轨迹）",        "nm/cm³",  0.8, 0.030),
    ("K19", "dx (X)", "y³",    0, 3, "X向三阶S形畸变 3rd-Flow-X（扫描期间WS三次方交叉轨迹；需预补 -L_s²/4·K19）","nm/cm³", 1.0, 0.025),
]

ws_x_rows = []
ws_y_rows = []
for idx, (K, ax, mono, p, q, desc, unit, k0, dk) in enumerate(ws_ihopc):
    r = row4
    fill = fill_white if idx % 2 == 0 else fill_zebra
    ws4.cell(r, 1, K)
    ws4.cell(r, 2, ax)
    ws4.cell(r, 3, mono)
    ws4.cell(r, 4, p)
    ws4.cell(r, 5, q)
    ws4.cell(r, 6, desc)
    ws4.cell(r, 7, unit)
    ws4.cell(r, 8, f"=($C$3^D{r})*($E$3^E{r})")
    ws4.cell(r, 9, f"=($C$3^D{r}/SQRT(2*D{r}+1))*($E$3^E{r}/SQRT(2*E{r}+1))")
    ws4.cell(r, 10, k0)
    ws4.cell(r, 11, dk)
    ws4.cell(r, 12, f"=K{r}/J{r}")
    ws4.cell(r, 13, f"=K{r}*H{r}")
    ws4.cell(r, 14, f"=K{r}*I{r}")
    if "X" in ax:
        ws_x_rows.append(r)
    else:
        ws_y_rows.append(r)

    for col in range(1, 15):
        cell = ws4.cell(r, col)
        cell.fill = fill
        cell.border = border_cell
        cell.font = font_spec if col == 11 else font_body
        cell.alignment = al_left if col == 6 else al_center
    ws4.cell(r, 8).number_format = "0.000"
    ws4.cell(r, 9).number_format = "0.000"
    ws4.cell(r, 10).number_format = "0.0"
    ws4.cell(r, 11).number_format = "0.000"
    ws4.cell(r, 12).number_format = "0.0%"
    ws4.cell(r, 13).number_format = "0.000"
    ws4.cell(r, 14).number_format = "0.000"
    ws4.row_dimensions[r].height = 30
    row4 += 1

ws_sum_x_row = row4
ws4.merge_cells(start_row=row4, start_column=1, end_row=row4, end_column=12)
ws4.cell(row4, 1, "【Item 14 汇总 — X向】WS iHOPC 补偿残差 RSS 合成（K1, K5, K11, K19 共4项）")
ws4.cell(row4, 13, "=SQRT(" + "+".join(f"M{x}^2" for x in ws_x_rows) + ")")
ws4.cell(row4, 14, "=SQRT(" + "+".join(f"N{x}^2" for x in ws_x_rows) + ")")
for col in range(1, 15):
    c = ws4.cell(row4, col)
    c.fill = fill_total; c.border = border_total; c.font = font_bold
    c.alignment = al_right if col == 1 else al_center
ws4.cell(row4, 13).number_format = "0.000"; ws4.cell(row4, 14).number_format = "0.000"
ws4.row_dimensions[row4].height = 24
row4 += 1

ws_sum_y_row = row4
ws4.merge_cells(start_row=row4, start_column=1, end_row=row4, end_column=12)
ws4.cell(row4, 1, "【Item 14 汇总 — Y向】WS iHOPC 补偿残差 RSS 合成（K2, K4, K6, K8, K10, K14, K16 共7项）")
ws4.cell(row4, 13, "=SQRT(" + "+".join(f"M{y}^2" for y in ws_y_rows) + ")")
ws4.cell(row4, 14, "=SQRT(" + "+".join(f"N{y}^2" for y in ws_y_rows) + ")")
for col in range(1, 15):
    c = ws4.cell(row4, col)
    c.fill = fill_total; c.border = border_total; c.font = font_bold
    c.alignment = al_right if col == 1 else al_center
ws4.cell(row4, 13).number_format = "0.000"; ws4.cell(row4, 14).number_format = "0.000"
ws4.row_dimensions[row4].height = 24
row4 += 1

ws4.merge_cells(start_row=row4, start_column=1, end_row=row4, end_column=14)
c = ws4.cell(row4, 1, "注：1) 物镜相对精度对标 Nikon MDDM ~2% [160] 与 ASML/Zeiss Distortion Manipulator 5–10% [253]，静态项控 2.5%–5%，动态项控 4%–5.6%；2) WS闭环精度受ENC与轨迹前馈相位延迟约束，控 0.6%–3.8%；3) 二/三阶扫描轨迹经 8 mm 狭缝卷积会产生 ΔK1 = (L_s²/12)·K11 = 0.0533·K11 及 ΔK5 = (L_s²/4)·K19 = 0.16·K19 几何偏置，必须在轨迹发生器中精确逆卷积预补偿。")
c.font = font_note; c.alignment = al_left
ws4.row_dimensions[row4].height = 30

set_col_widths(ws4, [7, 8, 8, 5, 5, 42, 9, 9, 9, 9, 13, 9, 12, 12])
ws4.freeze_panes = "A6"

# ==============================================================================
# SHEET 5: Item 15 (Odd Fringe Zernike Z5-Z64, all 30 odd terms)
# ==============================================================================
style_banner(ws5, 1, 18, "大类 15：物镜对 Odd 类型 Fringe Zernike 波像差（Z5–Z64，全部30个奇像差项）控制误差验收规格与跨照明切换套刻仿真")
ws5.merge_cells("A2:R2")
c = ws5.cell(2, 1, "仿真模型：2D Abbe 部分相干标量/高NA成像（λ=193.368 nm，NA=1.35），对比6种典型 ArFi 照明/特征切换（Dipole 85nm、CQuad 90nm、Quasar 100nm、Annular 120nm、Conv 180nm、Metrology 300nm）；Z2倾斜验证严格等于 -1/NA = -0.7407 nm/nm（与[008 Fig.4b]完全一致）。表中同时提供 Fringe幅值(nm) 与 RMS波前(nm RMS) 两种工程口径，并单独区分 1θ/3θ/5θ(28项) 与含 7θ Z50/Z51 全奇项(30项)。")
c.font = font_subtitle; c.alignment = al_left
ws5.row_dimensions[2].height = 30

hdr5 = [
    "Fringe\n序号", "径向\n阶n", "角向\n频m", "cos/\nsin", "奇像差\n类别", "主轴\n方向",
    "RMS换算\n系数", "Dip85\n灵敏度", "CQuad90\n灵敏度", "Quasar100\n灵敏度", "Ann120\n灵敏度", "Conv180\n灵敏度", "Met300\n灵敏度",
    "仿真最大差分\n|ΔS_sim|", "DRAM包络差分\n|ΔS_env|",
    "控制误差规格\n(nm Fringe)", "等效控制误差\n(nm RMS)", "照明切换套刻\n贡献 (nm, 包络)"
]
write_header_row(ws5, 4, hdr5)

# Tuned Fringe Zernike specs [nm Fringe amplitude, 3-sigma control residual across illumination switch]
# Calibrated so:
# - Abbe Sim OVL RSS <= 0.32 nm, DRAM Envelope OVL RSS <= 0.36 nm (28-term 0.351 nm, 30-term 0.359 nm!)
# - ComaX/Y RMS = 0.155 nm RMS (matches 024_79731G Fig 11 FlexWave NXT:1950i 0.15-0.16 nm RMS!)
# - TrefoilX/Y RMS = 0.135 nm RMS (improves on NXT:1950i 0.12-0.33 nm RMS!)
# - Total Odd WFE RMS (30 terms) = 0.334 nm RMS
spec_fringe_tuned = {
    7: 0.18, 8: 0.18,
    10: 0.16, 11: 0.16,
    14: 0.18, 15: 0.18,
    19: 0.20, 20: 0.20,
    23: 0.24, 24: 0.24,
    26: 0.16, 27: 0.16,
    30: 0.22, 31: 0.22,
    34: 0.30, 35: 0.30,
    39: 0.22, 40: 0.22,
    43: 0.30, 44: 0.30,
    47: 0.35, 48: 0.35,
    50: 0.24, 51: 0.24,
    54: 0.25, 55: 0.25,
    58: 0.35, 59: 0.35,
    62: 0.40, 63: 0.40,
}

lit_override = {
    7: 0.95, 8: 0.95,
    10: 0.91, 11: 0.91,
    14: 0.70, 15: 0.70,
    19: 0.55, 20: 0.55,
}

type_label = {1: "1θ 彗差(Coma)", 3: "3θ 三叶(Trefoil)", 5: "5θ 五叶(Pentafoil)", 7: "7θ 七叶(Heptafoil)"}

row5 = 5
z_x_rows_30, z_y_rows_30 = [], []
z_x_rows_28, z_y_rows_28 = [], []
z_group_rows = {k: [] for k in ["1X", "1Y", "3X", "3Y", "5X", "5Y", "7X", "7Y"]}

# Verify numbers in Python concurrently
py_ovl_x_env30 = 0.0; py_ovl_y_env30 = 0.0
py_ovl_x_sim30 = 0.0; py_ovl_y_sim30 = 0.0
py_ovl_x_env28 = 0.0; py_ovl_y_env28 = 0.0
py_wfe_30 = 0.0; py_wfe_28 = 0.0
py_grp = {k: 0.0 for k in z_group_rows}

for idx, item in enumerate(z_sim):
    r = row5
    j = item["j"]; n = item["n"]; m = item["m"]; trig = item["trig"]
    axis = "X" if trig == "cos" else "Y"
    sdict = item["sx"] if axis == "X" else item["sy"]
    k_dip = "DipX_85" if axis == "X" else "DipY_85"
    vals6 = [sdict[k_dip], sdict["CQuad_90"], sdict["Quasar_100"], sdict["Ann_120"], sdict["Conv_180"], sdict["Met_300"]]
    sim_ds = max(vals6) - min(vals6)
    env_ds = max(sim_ds, lit_override.get(j, 0.0))
    sf = spec_fringe_tuned[j]
    f_rms = 1.0 / math.sqrt(2 * (n + 1))
    s_rms = sf * f_rms

    if axis == "X":
        z_x_rows_30.append(r)
        py_ovl_x_env30 += (env_ds * sf)**2
        py_ovl_x_sim30 += (sim_ds * sf)**2
        if m != 7:
            z_x_rows_28.append(r)
            py_ovl_x_env28 += (env_ds * sf)**2
    else:
        z_y_rows_30.append(r)
        py_ovl_y_env30 += (env_ds * sf)**2
        py_ovl_y_sim30 += (sim_ds * sf)**2
        if m != 7:
            z_y_rows_28.append(r)
            py_ovl_y_env28 += (env_ds * sf)**2
    py_wfe_30 += s_rms**2
    if m != 7: py_wfe_28 += s_rms**2
    gk = f"{m}{axis}"
    z_group_rows[gk].append(r)
    py_grp[gk] += s_rms**2

    fill = fill_warn if m == 7 else (fill_white if idx % 2 == 0 else fill_zebra)
    ws5.cell(r, 1, f"Z{j}")
    ws5.cell(r, 2, n)
    ws5.cell(r, 3, m)
    ws5.cell(r, 4, trig)
    ws5.cell(r, 5, type_label[m])
    ws5.cell(r, 6, axis)
    ws5.cell(r, 7, f"=1/SQRT(2*(B{r}+1))")
    for ci, sv in enumerate(vals6, 8):
        ws5.cell(r, ci, round(sv, 4))
    ws5.cell(r, 14, f"=MAX(H{r}:M{r})-MIN(H{r}:M{r})")
    if j in lit_override:
        ws5.cell(r, 15, f"=MAX(N{r},{lit_override[j]})")
    else:
        ws5.cell(r, 15, f"=N{r}")
    ws5.cell(r, 16, sf)
    ws5.cell(r, 17, f"=P{r}*G{r}")
    ws5.cell(r, 18, f"=P{r}*O{r}")

    for col in range(1, 19):
        cell = ws5.cell(r, col)
        cell.fill = fill; cell.border = border_cell
        cell.font = font_spec if col == 16 else font_body
        cell.alignment = al_center
    ws5.cell(r, 7).number_format = "0.0000"
    for col in range(8, 16):
        ws5.cell(r, col).number_format = "0.000"
    ws5.cell(r, 16).number_format = "0.00"
    ws5.cell(r, 17).number_format = "0.0000"
    ws5.cell(r, 18).number_format = "0.000"
    ws5.row_dimensions[r].height = 20
    row5 += 1

# Summary block in Sheet 5
row5 += 1
style_section(ws5, row5, 18, "Item 15 奇像差控制误差与跨照明套刻 RSS 汇总（区分 1θ/3θ/5θ 与 含7θ全奇项，对标 FlexWave 实测 [024 Fig.11]）")
row5 += 1

z_sum_28_x = row5
ws5.merge_cells(start_row=row5, start_column=1, end_row=row5, end_column=15)
ws5.cell(row5, 1, "【28项 1θ/3θ/5θ 汇总 — X向 (14项 cos)】总 Odd 波前 RMS / 照明切换套刻 RSS")
ws5.cell(row5, 16, "=SQRT(" + "+".join(f"P{x}^2" for x in z_x_rows_28) + ")")
ws5.cell(row5, 17, "=SQRT(" + "+".join(f"Q{x}^2" for x in z_x_rows_28) + ")")
ws5.cell(row5, 18, "=SQRT(" + "+".join(f"R{x}^2" for x in z_x_rows_28) + ")")
for col in range(1, 19):
    c = ws5.cell(row5, col); c.fill = fill_subhdr; c.border = border_cell; c.font = font_bold
    c.alignment = al_right if col == 1 else al_center
ws5.cell(row5, 16).number_format = "0.000"; ws5.cell(row5, 17).number_format = "0.000"; ws5.cell(row5, 18).number_format = "0.000"
ws5.row_dimensions[row5].height = 22
row5 += 1

z_sum_28_y = row5
ws5.merge_cells(start_row=row5, start_column=1, end_row=row5, end_column=15)
ws5.cell(row5, 1, "【28项 1θ/3θ/5θ 汇总 — Y向 (14项 sin)】总 Odd 波前 RMS / 照明切换套刻 RSS")
ws5.cell(row5, 16, "=SQRT(" + "+".join(f"P{y}^2" for y in z_y_rows_28) + ")")
ws5.cell(row5, 17, "=SQRT(" + "+".join(f"Q{y}^2" for y in z_y_rows_28) + ")")
ws5.cell(row5, 18, "=SQRT(" + "+".join(f"R{y}^2" for y in z_y_rows_28) + ")")
for col in range(1, 19):
    c = ws5.cell(row5, col); c.fill = fill_subhdr; c.border = border_cell; c.font = font_bold
    c.alignment = al_right if col == 1 else al_center
ws5.cell(row5, 16).number_format = "0.000"; ws5.cell(row5, 17).number_format = "0.000"; ws5.cell(row5, 18).number_format = "0.000"
ws5.row_dimensions[row5].height = 22
row5 += 1

z_sum_30_x = row5
ws5.merge_cells(start_row=row5, start_column=1, end_row=row5, end_column=15)
ws5.cell(row5, 1, "【30项 全部Odd Z5–Z64 (含7θ Z50/51) — X向 (15项)】总 Odd 波前 RMS / 照明切换套刻 RSS")
ws5.cell(row5, 16, "=SQRT(" + "+".join(f"P{x}^2" for x in z_x_rows_30) + ")")
ws5.cell(row5, 17, "=SQRT(" + "+".join(f"Q{x}^2" for x in z_x_rows_30) + ")")
ws5.cell(row5, 18, "=SQRT(" + "+".join(f"R{x}^2" for x in z_x_rows_30) + ")")
for col in range(1, 19):
    c = ws5.cell(row5, col); c.fill = fill_total; c.border = border_total; c.font = font_bold
    c.alignment = al_right if col == 1 else al_center
ws5.cell(row5, 16).number_format = "0.000"; ws5.cell(row5, 17).number_format = "0.000"; ws5.cell(row5, 18).number_format = "0.000"
ws5.row_dimensions[row5].height = 24
row5 += 1

z_sum_30_y = row5
ws5.merge_cells(start_row=row5, start_column=1, end_row=row5, end_column=15)
ws5.cell(row5, 1, "【30项 全部Odd Z5–Z64 (含7θ Z50/51) — Y向 (15项)】总 Odd 波前 RMS / 照明切换套刻 RSS")
ws5.cell(row5, 16, "=SQRT(" + "+".join(f"P{y}^2" for y in z_y_rows_30) + ")")
ws5.cell(row5, 17, "=SQRT(" + "+".join(f"Q{y}^2" for y in z_y_rows_30) + ")")
ws5.cell(row5, 18, "=SQRT(" + "+".join(f"R{y}^2" for y in z_y_rows_30) + ")")
for col in range(1, 19):
    c = ws5.cell(row5, col); c.fill = fill_total; c.border = border_total; c.font = font_bold
    c.alignment = al_right if col == 1 else al_center
ws5.cell(row5, 16).number_format = "0.000"; ws5.cell(row5, 17).number_format = "0.000"; ws5.cell(row5, 18).number_format = "0.000"
ws5.row_dimensions[row5].height = 24
row5 += 1

z_sum_all_wfe = row5
ws5.merge_cells(start_row=row5, start_column=1, end_row=row5, end_column=15)
ws5.cell(row5, 1, "【全部30项 Odd Z5–Z64 总波前误差 RSS (X+Y全瞳)】| X/Y 最大照明切换套刻(包络) 见右列")
ws5.cell(row5, 16, f"=SQRT(P{z_sum_30_x}^2+P{z_sum_30_y}^2)")
ws5.cell(row5, 17, f"=SQRT(Q{z_sum_30_x}^2+Q{z_sum_30_y}^2)")
ws5.cell(row5, 18, f"=MAX(R{z_sum_30_x},R{z_sum_30_y})")
for col in range(1, 19):
    c = ws5.cell(row5, col); c.fill = fill_total; c.border = border_total; c.font = font_bold
    c.alignment = al_right if col == 1 else al_center
ws5.cell(row5, 16).number_format = "0.000"; ws5.cell(row5, 17).number_format = "0.000"; ws5.cell(row5, 18).number_format = "0.000"
ws5.row_dimensions[row5].height = 24
row5 += 2

# Grouped Wavefront RMS Verification Table vs FlexWave [024 Fig.11]
style_section(ws5, row5, 18, "分组奇像差波前 RMS 核验表（公式实时汇总，直接对标 NXT:1950i FlexWave 实测 [024 Fig.11]）")
row5 += 1
grp_meta = [
    ("1θ 彗差 Coma-X (Z7,14,23,34,47,62)", "1X", "0.16 nm RMS (NXT:1950i FlexWave 实测 [024 Fig.11])"),
    ("1θ 彗差 Coma-Y (Z8,15,24,35,48,63)", "1Y", "0.15 nm RMS (NXT:1950i FlexWave 实测 [024 Fig.11])"),
    ("3θ 三叶 Trefoil-X (Z10,19,30,43,58)", "3X", "0.33 nm RMS (NXT:1950i FlexWave 实测 [024 Fig.11]，本机收紧至~0.14)"),
    ("3θ 三叶 Trefoil-Y (Z11,20,31,44,59)", "3Y", "0.12 nm RMS (NXT:1950i FlexWave 实测 [024 Fig.11])"),
    ("5θ 五叶 Pentafoil-X/Y (Z26/27,39/40,54/55)", "5X", "每轴 0.091 nm RMS（高阶对称项，对Dipole/Quasar切换关键）"),
    ("7θ 七叶 Heptafoil-X/Y (Z50/Z51)", "7X", "每轴 0.060 nm RMS（Z5–Z64额外奇像差项，计入全Odd闭环）"),
]
for idx, (gtitle, gkey, gbench) in enumerate(grp_meta):
    ws5.merge_cells(start_row=row5, start_column=1, end_row=row5, end_column=7)
    ws5.merge_cells(start_row=row5, start_column=8, end_row=row5, end_column=15)
    ws5.cell(row5, 1, gtitle)
    ws5.cell(row5, 8, gbench)
    ws5.cell(row5, 16, "=SQRT(" + "+".join(f"P{r}^2" for r in z_group_rows[gkey]) + ")")
    ws5.cell(row5, 17, "=SQRT(" + "+".join(f"Q{r}^2" for r in z_group_rows[gkey]) + ")")
    ws5.cell(row5, 18, "=SQRT(" + "+".join(f"R{r}^2" for r in z_group_rows[gkey]) + ")")
    fill = fill_white if idx % 2 == 0 else fill_zebra
    for col in range(1, 19):
        c = ws5.cell(row5, col); c.fill = fill; c.border = border_cell; c.font = font_bold if col in (1, 17) else font_body
        c.alignment = al_left if col in (1, 8) else al_center
    ws5.cell(row5, 16).number_format = "0.000"; ws5.cell(row5, 17).number_format = "0.000"; ws5.cell(row5, 18).number_format = "0.000"
    ws5.row_dimensions[row5].height = 21
    row5 += 1

set_col_widths(ws5, [7, 5, 5, 6, 15, 6, 9, 8.5, 8.5, 9, 8.5, 8.5, 8.5, 10.5, 10.5, 11.5, 11.5, 12.5])
ws5.freeze_panes = "A5"

# ==============================================================================
# SHEET 1: Executive Benchmark & Live Cross-Sheet Budget Closure (DCO/MMO/FU)
# ==============================================================================
style_banner(ws1, 1, 9, "ArF 液浸光刻机（对标 NXT:1950i – NXT:1970Ci 之间）整机定位与套刻/焦面误差预算闭环总览")
ws1.merge_cells("A2:I2")
c = ws1.cell(2, 1, "【v2 升级版】本表误差预算实时链接至 Sheet 02–05（100% 保持 v1 闭环一致），并新增 Sheet 07–09（WS/RS 独立验收反驳与单/往返方案、WS iHOPC 离线/在线验收与狭缝逆卷积计算、物镜 Kn 八维能力评价体系），严格区分“顶层套刻/焦面直接贡献项”与“底层子系统约束项”，杜绝重复计算。验收顶层目标：DCO (|Mean|+3σ) ≤ 2.00 nm，MMO (99.7%) ≤ 3.50 nm，Focus Uniformity (3σ) ≤ 12.0 nm。")
c.font = font_subtitle; c.alignment = al_left
ws1.row_dimensions[2].height = 28

# Section A: Positioning Table
style_section(ws1, 4, 9, "一、目标机型对标定位（NXT:1950i vs 本目标机型 vs NXT:1970Ci vs NXT:1980Di）")
write_header_row(ws1, 5, ["核心性能维度", "NXT:1950i [009, 066]", "本目标机型 (1950i–1970i之间)", "NXT:1970Ci [015, 016, 066]", "NXT:1980Di [015, 016]", "本机架构与关键技术配置说明", "数据来源", "", ""])
ws1.merge_cells("F5:H5")
ws1.cell(5, 6, "本机架构与关键技术配置说明")
ws1.cell(5, 9, "文献参考")

bench_rows = [
    ("同机套刻 DCO / SMO (Mean+3σ)", "≤ 2.5 nm (典型1.5–2.2)", "≤ 2.00 nm (闭环设计 1.87 nm)", "≤ 1.6–1.8 nm", "≤ 1.4 nm", "对应 NXT:1960Bi–1965Ci+ 档位，留 6.6% 工程裕度", "[009, 066, 015]"),
    ("混机套刻 MMO (99.7%)", "≤ 4.5–5.5 nm", "≤ 3.50 nm (闭环设计 3.15 nm)", "≤ 2.5–3.4 nm (机群3.4)", "≤ 2.5 nm", "覆盖双机双台+50μm工艺片翘曲+跨照明切换场景，留 9.9% 裕度", "[066, 015 Fig.7]"),
    ("全片焦面均匀性 FU (3σ)", "≤ 15–20 nm", "≤ 12.0 nm (闭环设计 10.34 nm)", "≤ 10–12 nm", "≤ 9.1 nm", "陶瓷WS + 高平坦WT(6.0 nm) + UV-LS + 7点PARIS，留 13.8% 裕度", "[066 Fig.9/10a, 015]"),
    ("产能与扫描速度", "175–200 wph / 0.60 m/s", "220–230 wph / 0.70 m/s", "250 wph / 0.75 m/s", "275 wph / 0.80 m/s", "WS加速度 35–40 m/s²，RS加速度 150 m/s²，狭缝 26×8 mm", "[009, 066, 015]"),
    ("光学/对准/高阶补偿配置", "Gridplate+SMASH+TIS+FlexWave", "Gridplate+SMASH+7点PARIS+19参iHOPC+64阶Zernike", "同左 + 陶瓷WS + UV-LS", "增强RHC2 + 低热膨胀WT", "iHOPC覆盖K1–K19（不含K20，K20至2100i才支持）", "[024, 066, 154, 254]"),
]
r1 = 6
for idx, (k, v50, vt, v70, v80, note, ref) in enumerate(bench_rows):
    ws1.merge_cells(start_row=r1, start_column=6, end_row=r1, end_column=8)
    ws1.cell(r1, 1, k); ws1.cell(r1, 2, v50); ws1.cell(r1, 3, vt); ws1.cell(r1, 4, v70); ws1.cell(r1, 5, v80); ws1.cell(r1, 6, note); ws1.cell(r1, 9, ref)
    fill = fill_white if idx % 2 == 0 else fill_zebra
    for col in range(1, 10):
        cell = ws1.cell(r1, col); cell.fill = fill; cell.border = border_cell
        cell.font = font_spec if col == 3 else (font_bold if col == 1 else font_body)
        cell.alignment = al_left if col in (1, 6) else al_center
    ws1.row_dimensions[r1].height = 24
    r1 += 1

# Section B: DCO <= 2.00 nm Budget Closure
r1 += 1
style_section(ws1, r1, 9, "二、DCO / SMO ≤ 2.00 nm（同机同台双层套刻，|Mean|+3σ）动态预算闭环表（跨页公式实时计算）")
r1 += 1
write_header_row(ws1, r1, ["编号", "顶层套刻误差来源（不重复计数）", "涵盖的15大类编号", "单层曝光\n3σ X (nm)", "单层曝光\n3σ Y (nm)", "双层叠加\n系数", "两层DCO\n3σ X (nm)", "两层DCO\n3σ Y (nm)", "Y向方差占比\n(%) & 层次说明"])
r1 += 1

s2n = "'02_1-4_运动台同步与ENC规格'"
s3n = "'03_5-12_对准温控夹持框架规格'"
s4n = "'04_13-14_iHOPC物镜与WS残差'"
s5n = "'05_15_Odd_Zernike(Z5-Z64)'"

dco_start = r1
dco_items = [
    ("D1", "WS-RS 同步运动误差 MA (含平移与Rz边缘)", "Item 3（底层含 1, 2, 4, 12动）",
     f"=SQRT({s2n}!D20^2+(4*{s2n}!D25)^2)", f"=SQRT({s2n}!D21^2+(13*{s2n}!D25)^2)", "=SQRT(2)", "两层独立随机曝光×√2；WS/RS/ENC/Frame动态已内含"),
    ("D2", "M-side 晶圆对准网格与短期基线漂移", "Item 5（底层含 12静漂移）",
     f"=SQRT({s3n}!D{s3_rows['5.5']}^2+{s3n}!D{s3_rows['5.6']}^2)", f"=SQRT({s3n}!D{s3_rows['5.5']}^2+{s3n}!D{s3_rows['5.6']}^2)", "=SQRT(2)", "5.5网格重复(0.35)+5.6短期基线(0.25)=0.43 nm"),
    ("D3", "E-side 空间像掩模对准重复性 (TIS/PARIS)", "Item 6",
     f"={s3n}!D{s3_rows['6.3']}", f"={s3n}!D{s3_rows['6.3']}", "=SQRT(2)", "6.3 PARIS 7点RA重复性 0.40 nm，两层独立×√2"),
    ("D4", "晶圆温控与液浸残差 (WT + 液浸 + WH瞬态)", "Item 7 + Item 11",
     "=SQRT(0.35^2+0.20^2)", "=SQRT(0.35^2+0.20^2)", "=SQRT(2)", "WT+液浸热残差0.35 nm(7.6) + WH片间瞬态0.20 nm(11.4)"),
    ("D5", "掩模附近温控与气隙噪声残差 (含RHC)", "Item 8",
     "=SQRT(0.25^2+0.27^2)", "=SQRT(0.25^2+0.27^2)", "=SQRT(2)", "气隙点间噪声0.25 nm(8.2) + 掩模加热RHC残差0.27 nm(8.5)"),
    ("D6", "RT 掩模夹持重复性与高加速微滑移", "Item 9（9.2 + 9.3）",
     f"=SQRT({s3n}!D{s3_rows['9.2']}^2+{s3n}!D{s3_rows['9.3']}^2)", f"=SQRT({s3n}!D{s3_rows['9.2']}^2+{s3n}!D{s3_rows['9.3']}^2)", "=SQRT(2)", "同台同掩模静态NCE抵消，计入重夹重复0.15+微滑移0.15"),
    ("D7", "WT 晶圆夹持重复性与高加速微滑移", "Item 10（10.1 + 10.4）",
     f"=SQRT({s3n}!D{s3_rows['10.1']}^2+{s3n}!D{s3_rows['10.4']}^2)", f"=SQRT({s3n}!D{s3_rows['10.1']}^2+{s3n}!D{s3_rows['10.4']}^2)", "=SQRT(2)", "同台平坦参考硅片吸片重复0.25 + 微滑移0.15"),
    ("D8", "物镜 iHOPC 场内参数补偿残差 (场角RSS)", "Item 13（8项激活K参）",
     f"={s4n}!M{lens_sum_x_row}", f"={s4n}!M{lens_sum_y_row}", 1.2, "按场角最严RSS取用，两层补偿指令差分按×1.2计"),
    ("D9", "WS iHOPC 场内参数动态补偿残差 (场角RSS)", "Item 14（11项激活K参）",
     f"={s4n}!M{ws_sum_x_row}", f"={s4n}!M{ws_sum_y_row}", 1.2, "按场角最严RSS取用，两层补偿指令差分按×1.2计"),
    ("D10", "物镜 Odd Zernike 跨照明切换套刻残差 (Z5–Z64)", "Item 15（30项全奇像差）",
     f"={s5n}!R{z_sum_30_x}", f"={s5n}!R{z_sum_30_y}", 1.0, "差分灵敏度|ΔS|已直接代表两次不同照明曝光的位移差(×1.0)"),
    ("D11", "整机未建模扰动与套刻量测(SAT)本底噪声", "整机系统裕量",
     0.25, 0.25, "=SQRT(2)", "包含套刻量测机(DBO/IBO)重复性及未建模次要项"),
]

dco_end = dco_start + len(dco_items) - 1
dco_rss_row = dco_end + 1
for idx, (cid, name, cats, fx, fy, mult, note) in enumerate(dco_items):
    r = dco_start + idx
    fill = fill_white if idx % 2 == 0 else fill_zebra
    ws1.cell(r, 1, cid); ws1.cell(r, 2, name); ws1.cell(r, 3, cats)
    ws1.cell(r, 4, fx); ws1.cell(r, 5, fy); ws1.cell(r, 6, mult)
    ws1.cell(r, 7, f"=D{r}*F{r}"); ws1.cell(r, 8, f"=E{r}*F{r}")
    ws1.cell(r, 9, f'=TEXT(H{r}^2/H${dco_rss_row}^2,"0.0%")&" | {note}"')
    for col in range(1, 10):
        c = ws1.cell(r, col); c.fill = fill; c.border = border_cell; c.font = font_body
        c.alignment = al_left if col in (2, 3, 9) else al_center
    for col in (4, 5, 6, 7, 8):
        ws1.cell(r, col).number_format = "0.000" if col != 6 else "0.00"
    ws1.row_dimensions[r].height = 24

# DCO RSS, Mean, Total rows
r1 = dco_rss_row
ws1.merge_cells(start_row=r1, start_column=1, end_row=r1, end_column=3)
ws1.cell(r1, 1, "两层随机套刻 3σ RSS 合计")
ws1.cell(r1, 4, f"=SQRT(SUMSQ(D{dco_start}:D{dco_end}))")
ws1.cell(r1, 5, f"=SQRT(SUMSQ(E{dco_start}:E{dco_end}))")
ws1.cell(r1, 6, "—")
ws1.cell(r1, 7, f"=SQRT(SUMSQ(G{dco_start}:G{dco_end}))")
ws1.cell(r1, 8, f"=SQRT(SUMSQ(H{dco_start}:H{dco_end}))")
ws1.cell(r1, 9, "100.0% | 独立随机误差平方和开方")
for col in range(1, 10):
    c = ws1.cell(r1, col); c.fill = fill_subhdr; c.border = border_cell; c.font = font_bold
    c.alignment = al_left if col == 9 else (al_right if col == 1 else al_center)
for col in (4, 5, 7, 8): ws1.cell(r1, col).number_format = "0.000"
ws1.row_dimensions[r1].height = 22

r1 += 1
dco_mean_row = r1
ws1.merge_cells(start_row=r1, start_column=1, end_row=r1, end_column=6)
ws1.cell(r1, 1, "系统残余均值偏置 |Mean|（APC/基线校准后残余）")
ws1.cell(r1, 7, 0.30); ws1.cell(r1, 8, 0.30)
ws1.cell(r1, 9, "系统均值线性叠加（ASML DCO = |Mean| + 3σ 验收口径）")
for col in range(1, 10):
    c = ws1.cell(r1, col); c.fill = fill_white; c.border = border_cell; c.font = font_body
    c.alignment = al_left if col == 9 else (al_right if col == 1 else al_center)
ws1.cell(r1, 7).number_format = "0.000"; ws1.cell(r1, 8).number_format = "0.000"
ws1.row_dimensions[r1].height = 22

r1 += 1
dco_tot_row = r1
ws1.merge_cells(start_row=r1, start_column=1, end_row=r1, end_column=6)
ws1.cell(r1, 1, "【整机 DCO 闭环总计 (|Mean| + 3σ)】 vs 目标规格 ≤ 2.00 nm")
ws1.cell(r1, 7, f"=G{dco_rss_row}+G{dco_mean_row}")
ws1.cell(r1, 8, f"=H{dco_rss_row}+H{dco_mean_row}")
ws1.cell(r1, 9, f'=IF(MAX(G{r1},H{r1})<=2.0,"PASS ✓ 裕度 "&TEXT(2.0-MAX(G{r1},H{r1}),"0.000")&" nm ("&TEXT((2.0-MAX(G{r1},H{r1}))/2.0,"0.0%")&")","OVER BUDGET")')
for col in range(1, 10):
    c = ws1.cell(r1, col); c.fill = fill_total; c.border = border_total; c.font = font_bold
    c.alignment = al_left if col == 9 else (al_right if col == 1 else al_center)
ws1.cell(r1, 7).number_format = "0.000"; ws1.cell(r1, 8).number_format = "0.000"
ws1.row_dimensions[r1].height = 26

# Section C: MMO <= 3.50 nm Budget Closure
r1 += 2
style_section(ws1, r1, 9, "三、MMO ≤ 3.50 nm（跨机跨台混机套刻，99.7% / |Mean|+3σ）动态预算闭环表")
r1 += 1
write_header_row(ws1, r1, ["编号", "MMO 跨机误差来源", "对应大类", "3σ 贡献\nX (nm)", "3σ 贡献\nY (nm)", "方差占比\n(Y向)", "工程依据与跨机匹配说明", "", ""])
ws1.merge_cells(start_row=r1, start_column=7, end_row=r1, end_column=9)
r1 += 1

mmo_start = r1
mmo_items = [
    ("M1", "双机动态随机套刻基线 (等同2层 DCO 3σ RSS)", "Items 1–15 动态", f"=G{dco_rss_row}", f"=H{dco_rss_row}", "双机独立曝光的动态随机总和"),
    ("M2", "双机 Gridplate 网格板残余匹配差 (经机群标定)", "Item 4 (4.9)", 0.80, 0.80, "双机4台光栅板高阶非线性网格残余匹配差 [009, 062]"),
    ("M3", "双机物镜静态高阶畸变匹配差 (含K20及>3阶残差)", "Item 13 (K20等)", 1.10, 1.10, "1950i–1970Ci无K20及高空间频畸变操纵器 [154, 253]，为MMO第一静态大项"),
    ("M4", "双机双台晶圆夹持指纹匹配差 (含50μm工艺片翘曲)", "Item 10 (10.2+10.3)", 0.95, 0.95, "直接对标NXT:1965Ci/1970Ci实测WT全片套刻影响 1.0 nm [066 Fig.10a]"),
    ("M5", "双机掩模夹持不可校正形变匹配差 (NCE×√2)", "Item 9 (9.1)", f"={s3n}!D{s3_rows['9.1']}*SQRT(2)", f"={s3n}!D{s3_rows['9.1']}*SQRT(2)", "两台机台掩模吸盘夹持NCE(0.25 nm)非相关合成 0.35 nm [225]"),
    ("M6", "双机对准/TIS传感器与工艺标记(WAD)匹配差", "Items 5 & 6 (5.7+6.6)", 0.90, 0.90, "跨机SMASH光学不对称匹配差 + 双台TIS传感板匹配差 [006, 015]"),
    ("M7", "双机热环境与RHC/WHC前馈模型失配残差", "Items 7, 8, 11", 0.85, 0.85, "两台机台WT/WH/IRL/液浸温差及高剂量RHC模型残余差异 [016, 017]"),
    ("M8", "双机 Odd Zernike 跨机/跨照明匹配增额", "Item 15 (×√2净增)", f"={s5n}!R{z_sum_30_x}", f"={s5n}!R{z_sum_30_y}", "计入第二台物镜独立奇像差残余(已在M1含1×，此处补足第2台差值)"),
    ("M9", "双机 iHOPC 与 APC 高阶跨机补偿匹配残差", "Items 13 & 14", 0.55, 0.55, "不同机台操纵器增益与跨机前馈标定差异"),
]
mmo_end = mmo_start + len(mmo_items) - 1
mmo_rss_row = mmo_end + 1
for idx, (cid, name, cats, fx, fy, note) in enumerate(mmo_items):
    r = mmo_start + idx
    ws1.merge_cells(start_row=r, start_column=7, end_row=r, end_column=9)
    fill = fill_white if idx % 2 == 0 else fill_zebra
    ws1.cell(r, 1, cid); ws1.cell(r, 2, name); ws1.cell(r, 3, cats)
    ws1.cell(r, 4, fx); ws1.cell(r, 5, fy)
    ws1.cell(r, 6, f"=E{r}^2/E${mmo_rss_row}^2")
    ws1.cell(r, 7, note)
    for col in range(1, 10):
        c = ws1.cell(r, col); c.fill = fill; c.border = border_cell; c.font = font_body
        c.alignment = al_left if col in (2, 3, 7) else al_center
    ws1.cell(r, 4).number_format = "0.000"; ws1.cell(r, 5).number_format = "0.000"; ws1.cell(r, 6).number_format = "0.0%"
    ws1.row_dimensions[r].height = 23

r1 = mmo_rss_row
ws1.merge_cells(start_row=r1, start_column=1, end_row=r1, end_column=3)
ws1.merge_cells(start_row=r1, start_column=7, end_row=r1, end_column=9)
ws1.cell(r1, 1, "MMO 3σ RSS 合计")
ws1.cell(r1, 4, f"=SQRT(SUMSQ(D{mmo_start}:D{mmo_end}))")
ws1.cell(r1, 5, f"=SQRT(SUMSQ(E{mmo_start}:E{mmo_end}))")
ws1.cell(r1, 6, f"=SUM(F{mmo_start}:F{mmo_end})")
ws1.cell(r1, 7, "机群跨机随机+静态指纹总 3σ")
for col in range(1, 10):
    c = ws1.cell(r1, col); c.fill = fill_subhdr; c.border = border_cell; c.font = font_bold
    c.alignment = al_left if col == 7 else (al_right if col == 1 else al_center)
ws1.cell(r1, 4).number_format = "0.000"; ws1.cell(r1, 5).number_format = "0.000"; ws1.cell(r1, 6).number_format = "0.0%"
ws1.row_dimensions[r1].height = 22

r1 += 1
mmo_mean_row = r1
ws1.merge_cells(start_row=r1, start_column=1, end_row=r1, end_column=3)
ws1.merge_cells(start_row=r1, start_column=7, end_row=r1, end_column=9)
ws1.cell(r1, 1, "跨机系统均值残差 |Mean|")
ws1.cell(r1, 4, 0.45); ws1.cell(r1, 5, 0.45); ws1.cell(r1, 6, "—")
ws1.cell(r1, 7, "机群APC校准周期内跨机系统均值偏移")
for col in range(1, 10):
    c = ws1.cell(r1, col); c.fill = fill_white; c.border = border_cell; c.font = font_body
    c.alignment = al_left if col == 7 else (al_right if col == 1 else al_center)
ws1.cell(r1, 4).number_format = "0.000"; ws1.cell(r1, 5).number_format = "0.000"
ws1.row_dimensions[r1].height = 22

r1 += 1
mmo_tot_row = r1
ws1.merge_cells(start_row=r1, start_column=1, end_row=r1, end_column=3)
ws1.merge_cells(start_row=r1, start_column=7, end_row=r1, end_column=9)
ws1.cell(r1, 1, "【整机 MMO 闭环总计】 vs 目标规格 ≤ 3.50 nm")
ws1.cell(r1, 4, f"=D{mmo_rss_row}+D{mmo_mean_row}")
ws1.cell(r1, 5, f"=E{mmo_rss_row}+E{mmo_mean_row}")
ws1.cell(r1, 6, "—")
ws1.cell(r1, 7, f'=IF(MAX(D{r1},E{r1})<=3.5,"PASS ✓ 裕度 "&TEXT(3.5-MAX(D{r1},E{r1}),"0.000")&" nm ("&TEXT((3.5-MAX(D{r1},E{r1}))/3.5,"0.0%")&")","OVER BUDGET")')
for col in range(1, 10):
    c = ws1.cell(r1, col); c.fill = fill_total; c.border = border_total; c.font = font_bold
    c.alignment = al_left if col == 7 else (al_right if col == 1 else al_center)
ws1.cell(r1, 4).number_format = "0.000"; ws1.cell(r1, 5).number_format = "0.000"
ws1.row_dimensions[r1].height = 26

# Section D: Focus Uniformity <= 12.0 nm Budget Closure
r1 += 2
style_section(ws1, r1, 9, "四、全片焦面均匀性 Focus Uniformity ≤ 12.0 nm (3σ) 动态预算闭环表（验证 Z / Rx / Ry 与夹持指标）")
r1 += 1
write_header_row(ws1, r1, ["编号", "焦面误差来源", "对应大类", "3σ 贡献\n(nm)", "方差占比\n(%)", "工程说明与跨页链接来源", "", "", ""])
ws1.merge_cells(start_row=r1, start_column=6, end_row=r1, end_column=9)
r1 += 1

fu_start = r1
fu_items = [
    ("F1", "WS-RS 同步焦面运动误差 MA-Z", "Item 3 (3.3，含 1.3/2.3)", f"={s2n}!D22", "链接自 Sheet 02 同步 MA-Z = 5.00 nm [066 Fig.9]"),
    ("F2", "WS-RS 同步倾角诱发狭缝边缘离焦 (Rx+Ry)", "Item 3 (3.4+3.5)", f"=SQRT((4*{s2n}!D23)^2+(13*{s2n}!D24)^2)", "Rx×4 mm (1.00 nm) 与 Ry×13 mm (1.56 nm) RSS 合成 1.85 nm"),
    ("F3", "WT 瘤点全局平坦度离焦贡献", "Item 10 (10.5)", f"={s3n}!D{s3_rows['10.5']}", "链接自 Sheet 03 WT平坦度 = 6.00 nm [066 Fig.10a 实测6.2 nm]"),
    ("F4", "RT 掩模夹持面外变形离焦贡献", "Item 9 (9.4)", f"={s3n}!D{s3_rows['9.4']}", "链接自 Sheet 03 掩模夹持离焦 = 2.00 nm [225 Sec.2.1.3]"),
    ("F5", "E-side TIS/PARIS 最佳焦面标定重复性", "Item 6 (6.2)", f"={s3n}!D{s3_rows['6.2']}", "链接自 Sheet 03 TIS焦面重复性 = 2.50 nm"),
    ("F6", "M-side 调平传感器(UV-LS)高度测量与形貌残差", "调平传感器(配套)", 3.50, "UV-LS抑制硅片工艺膜层光学渗透误差后的形貌跟踪残差 [066]"),
    ("F7", "物镜静态场曲与透镜/掩模热离焦残差", "物镜Even项/热控", 4.00, "涵盖残余场曲、像散(Even Zernike)及高剂量瞬态热焦漂"),
    ("F8", "整机框架Z向动态与液浸水膜折射率扰动", "Items 12 & 7", f"=SQRT({s3n}!D{s3_rows['12.3']}^2+1.32^2)", "MF-物镜Z向动态 1.50 nm + 液浸水膜温度/压力折射率微扰 1.32 nm"),
]
fu_end = fu_start + len(fu_items) - 1
fu_tot_row = fu_end + 1
for idx, (cid, name, cats, fv, note) in enumerate(fu_items):
    r = fu_start + idx
    ws1.merge_cells(start_row=r, start_column=6, end_row=r, end_column=9)
    fill = fill_white if idx % 2 == 0 else fill_zebra
    ws1.cell(r, 1, cid); ws1.cell(r, 2, name); ws1.cell(r, 3, cats)
    ws1.cell(r, 4, fv); ws1.cell(r, 5, f"=D{r}^2/D${fu_tot_row}^2"); ws1.cell(r, 6, note)
    for col in range(1, 10):
        c = ws1.cell(r, col); c.fill = fill; c.border = border_cell; c.font = font_body
        c.alignment = al_left if col in (2, 3, 6) else al_center
    ws1.cell(r, 4).number_format = "0.00"; ws1.cell(r, 5).number_format = "0.0%"
    ws1.row_dimensions[r].height = 23

r1 = fu_tot_row
ws1.merge_cells(start_row=r1, start_column=1, end_row=r1, end_column=3)
ws1.merge_cells(start_row=r1, start_column=6, end_row=r1, end_column=9)
ws1.cell(r1, 1, "【全片焦面均匀性 FU (3σ RSS) 总计】 vs 目标规格 ≤ 12.0 nm")
ws1.cell(r1, 4, f"=SQRT(SUMSQ(D{fu_start}:D{fu_end}))")
ws1.cell(r1, 5, f"=SUM(E{fu_start}:E{fu_end})")
ws1.cell(r1, 6, f'=IF(D{r1}<=12.0,"PASS ✓ 裕度 "&TEXT(12.0-D{r1},"0.00")&" nm ("&TEXT((12.0-D{r1})/12.0,"0.0%")&")","OVER BUDGET")')
for col in range(1, 10):
    c = ws1.cell(r1, col); c.fill = fill_total; c.border = border_total; c.font = font_bold
    c.alignment = al_left if col == 6 else (al_right if col == 1 else al_center)
ws1.cell(r1, 4).number_format = "0.00"; ws1.cell(r1, 5).number_format = "0.0%"
ws1.row_dimensions[r1].height = 26

set_col_widths(ws1, [9, 34, 22, 13, 13, 11, 13, 13, 44])
ws1.freeze_panes = "A4"

# ==============================================================================
# SHEET 6: References Index
# ==============================================================================
style_banner(ws6, 1, 6, "参考文献与核心证据索引（全部提取自 D:\\work\\OV4 文献库及 D:\\work\\ME3 TWINSCAN 技术手册）")
write_header_row(ws6, 3, ["编号", "来源文件 (OV4 / ME3)", "文献标题与作者/年份", "核心量化数据与技术结论", "支撑的验收大类", "证据等级"])

refs = [
    ("[009]", "OV4: 009_76401N.md", "Towards Ultimate Optical Lithography with NXT:1950i Dual Stage Immersion Platform (Castenmiller et al., ASML, SPIE 2010)", "NXT:1950i DCO=2.5 nm分解(Fig.3)；同步MA-X=0.47/MA-Y=0.49 nm(Fig.10)；ENC宽带噪声0.22 nm @ 1000 Hz(Fig.4)；Gridplate 7天稳定<0.20 nm；MF气幕10 mK", "Items 1–5, 7, 10, 12", "直接实测"),
    ("[066]", "OV4: 066_86831L.md", "Extending immersion lithography down to 1x nm production nodes (de Boeij et al., ASML, SPIE 2013)", "NXT:1950i/1960Bi/1970Ci路线图；PARIS 7点重复性<0.5 nm；陶瓷WS MAz峰值4 nm/95%≤6 nm(Fig.9)；WT平坦度离焦9.4→6.2 nm、套刻1.2→1.0 nm(Fig.10a)", "Items 1–3, 6, 10, 12", "直接实测"),
    ("[015]", "OV4: 015_978011.md", "NXT:1980Di immersion scanner for 7nm production nodes (de Graaf et al., ASML, SPIE 2016)", "NXT:1970Ci vs 1980Di基准对比：1970Ci机群MMO=3.4 nm(Fig.7)；SMASH对准重复性WQ≥1%为0.15–0.25 nm、WQ 0.1–1%为0.25–0.50 nm(Fig.10)", "总览, Items 5, 10", "直接实测"),
    ("[016]", "OV4: 016_nxt1980di_reticle_heating_rhc2.md", "Reticle Heating Feed-forward Control (RHC2) on NXT:1980Di (Kim/Paarhuis et al., Samsung/ASML, SPIE 2016)", "NXT:1970Ci掩模加热误差分解(20 mJ/<5% RT)：场均值(1.2,1.7) nm、气隙点间噪声(1.1,0.7) nm、片内漂移(0.5,0.4) nm(Fig.2)", "Item 8", "直接实测"),
    ("[017]", "OV4: 017_xt1700fi_wafer_thermal_overlay.md", "Thermal behavior of wafers and its effects on overlay performance in immersion lithography (Ha et al., Samsung, MEE 2013)", "液浸蒸发吸热与晶圆边缘降温对全片非线性网格套刻影响及热敏系数分析", "Item 7, 11", "实验+仿真"),
    ("[021]/[057]", "OV4: 021_SPIE2007_XT1900_paper.md / 057_69241P.md", "Performance of 1.35NA ArF immersion system (de Klerk/Mulkens et al., ASML, SPIE 2007/2008)", "液浸超纯水UPW温控精度±2.5 mK，高NA液浸光学热管理框架", "Item 7", "直接实测"),
    ("[062]", "OV4: 062_72741S.md", "Enabling the lithography roadmap: Novel Stage Positioning System (de Jong et al., ASML, SPIE 2009)", "NXT光栅编码器替代干涉仪原理：气隙<15 mm、四角45°读数头、3-of-4读数头Handover切换标定与Gridplate结构", "Items 1, 4, 12", "架构+实测"),
    ("[060]/[063]", "OV4: 060_72741I.md / 063_76401O.md", "NSR-S620D Streamlign Platform with Encoder Metrology (Shibazaki/Kohno et al., Nikon, SPIE 2009/2010)", "700 mm/s扫速下编码器差分重复性0.25 nm、同步MA与MSD工程对标", "Items 3, 4", "行业对标"),
    ("[075]", "OV4: 075_1_s2.0_S0967066118306488_main.md", "Beyond decentralized wafer/reticle stage control design: a double-Youla approach (Evers/Oomen, CEP 2019)", "双Youla主从同步控制实验：WS-RS同步MA误差0.108–0.565 nm (3σ)", "Items 1–3", "控制实测"),
    ("[019]/[094]", "OV4: 019_heertjes_control_wafer_scanners.md / 094_Position_Control...", "Control of Wafer Scanners (Heertjes/Butler, 2020) & Position Control in Lithographic Equipment (Butler, IEEE CSM 2011)", "WS 30–40 m/s²、RS 150 m/s²高加速控制架构、Balance Mass反力解耦、Air Mount f_0≈0.5 Hz、PALM ~90 Hz主动阻尼", "Items 1–3, 12", "权威综述"),
    ("[011]", "OV4: 011_nxt1970ci_reticle_wafer_alignment.md", "Impact of reticle and wafer alignment mark placement accuracy (van Haren et al., ASML/imec, SPIE 2019)", "NXT:1970Ci上PARIS掩模对准(RA)重复性~0.43 nm与视场内高阶套刻分配", "Item 6", "直接实测"),
    ("[225]", "OV4: 225_reticle_side_wall_clamping.md", "Reticle side wall clamping (G.P. Naaijkens, TU/e-ASML PhD Thesis, 2013)", "掩模夹持NCE套刻目标<0.28 nm(晶圆1×)、焦面<2.0 nm(晶圆1×)、液浸纵向放大率~10:1(精确11.14:1)及SMO误差树(Fig.1.8)", "Items 2, 3, 9", "权威专著"),
    ("[097]/[122]", "OV4: 097_043015_1.md / 122_Conformal_slip-free_wafer_chucking...", "Wafer chucking distortion prediction (Turner, JM3) & Slip-free chucking (Hermanussen/ASML, TU/e)", "翘曲硅片与瘤点静摩擦耦合产生不可校正IPD及微滑移机理", "Item 10", "力学建模"),
    ("[184]/[186]", "OV4: 184_us10120292b2.md / 186_us10747126b2.md", "ASML Patents US10120292B2 & US10747126B2 (Support apparatus / Burl table thermal & clamping)", "WT多区独立加热(含边缘蒸发区)、瘤点高度公差与接触面积比设计规范", "Items 7, 10", "专利规格"),
    ("[154]", "OV4: 154_high_order_field_to_field_corrections...pdf (Page 7)", "High Order Field-to-Field Corrections for Imaging and Overlay (Mulkens et al., ASML, SPIE 2012)", "原件第7页Eq.1与Table 1给出精确K1–K20多项式定义及物镜/WS/动态扫描执行机构映射，明确K20在1950i–1970Ci不支持", "Items 13, 14", "官方定义"),
    ("[100]/[114]/[126]/[251]", "OV4: 100_113251K / 114_963507 / 126 / 251", "iHOPC 15–19参量产应用与R2R模型变异性研究 (STM/ASML/TSMC/UMC)", "典型场内iHOPC下发指令幅值(|K0|)范围与高阶前馈残差基准", "Items 13, 14", "量产实测"),
    ("[160]/[253]", "OV4: 160_high_order_aberration_control... / 253_on_scanner_high_spatial...", "Nikon MDDM高阶像差控制 (Ishiyama) & ASML/Zeiss Distortion Manipulator (Klinkhamer et al., SPIE 2022)", "物镜操纵器相对执行精度对标：Nikon MDDM ~2% [160]，ASML/Zeiss 5%–10% [253]", "Items 13, 15", "直接实测"),
    ("[254]", "OV4: 254_supporting_future_dram_overlay...md", "Supporting future DRAM overlay and EPE roadmaps with NXT:2100i (Smeets et al., ASML, SPIE 2023)", "NXT:2050i(1970Ci代PARIS)像差测量二次套刻贡献0.28–0.34 nm(Fig.2)；IRL温控±0.4°C→±0.2°C；K20至2100i才支持", "Items 6, 8, 13", "直接实测"),
    ("[008]", "OV4: 008_021403_1 (1).md", "High-order distortion control using computational prediction (Kang/Mulkens/Zeiss, JM3 2016)", "Z1–Z64 Fringe Zernike套刻灵敏度分析(Fig.4a/4b)：验证Z2=-0.74 nm/nm，DRAM 6F²极限照明切换下Z7/8达~1.0、Z19/20达~0.55–0.62 nm/nm", "Item 15", "权威仿真"),
    ("[024]", "OV4: 024_79731G.md", "Advanced Wavefront Engineering (FlexWave) on 1.35 NA Scanner (Staals et al., ASML, SPIE 2011)", "官方Fringe Zernike Z5–Z64金字塔排序(Fig.2)与NXT:1950i FlexWave分组控制残差实测：ComaX=0.16, ComaY=0.15, 3foilX=0.33, 3foilY=0.12 nm RMS(Fig.11)", "Item 15", "直接实测"),
    ("[165]/[266]", "OV4: 165_toward_3_nm_overlay... / 266_performance_results_300mm...", "3nm Integrated Overlay Budget (Arnold, ASML) & 300mm TWINSCAN Results (Sluijk et al., ASML)", "套刻综合误差树构建方法(RSS/线性项区分)、MSD预算与双台架构隔振基准", "总览, Items 3, 12", "方法基准"),
    ("[ME3手册]", "ME3: 01-TT_Lay_L3 / 03-TT-L2-LO / 05-TT-L2-WH / 08-TT-L3-RS / 11-TT-L3-AM", "ASML TWINSCAN Level 2/3 系统技术与维护培训手册", "LCW细温传感器<0.1 mK；TSU共用LCW+17 μm气浮预温控；WH气幕NTC校零；RS水平层流气幕；MFCW细加热器；Air Mount架构", "Items 7, 8, 11, 12", "官方手册"),
]

r6 = 4
for idx, rdata in enumerate(refs):
    fill = fill_white if idx % 2 == 0 else fill_zebra
    for col, val in enumerate(rdata, 1):
        c = ws6.cell(r6, col, val)
        c.fill = fill; c.border = border_cell
        c.font = font_bold if col == 1 else font_body
        c.alignment = al_center if col in (1, 5, 6) else al_left
    ws6.row_dimensions[r6].height = 38
    r6 += 1

set_col_widths(ws6, [12, 34, 42, 54, 18, 12])
ws6.freeze_panes = "A4"


# ==============================================================================
# SHEET 7 (v2 NEW): WS & RS Independent Acceptance Rebuttal + Uni/Bi Protocol
# ==============================================================================
s2n_q = "'02_1-4_运动台同步与ENC规格'"
s4n_q = "'04_13-14_iHOPC物镜与WS残差'"

style_banner(ws7, 1, 11, "v2 新增专题一（大类 1–2 深化）：WS / RS 独立 6-DOF 验收必要性反驳与单程 / 往返重复性验收细则")
ws7.merge_cells("A2:K2")
c = ws7.cell(2, 1, "核心工程结论：① WS-RS 同步误差绝对不能覆盖 WS 或 RS 的独立 6-DOF 重复性（存在 M-side 无 RS 参与、Z/Rx/Ry 液浸焦面非同步、场间步进整定瞬态、4× 动力学反冲与微滑移盲区等硬约束）；② 必须同时验收单程重复性（R_uni）与往返重复性（R_bi = B_res + 3σ_pooled），且动态往返总值实时闭环至 Sheet 02 表 1/表 2 红线。")
c.font = font_subtitle; c.alignment = al_left
ws7.row_dimensions[2].height = 30

# --- Section 7A: Engineering Rebuttal Matrix ---
r7 = 4
style_section(ws7, r7, 11, "7A. 反击子系统供应商“WS-RS 同步可覆盖 WS/RS 自身 6-DOF 重复性”的 6 大铁证")
r7 += 1
write_header_row(ws7, r7, ["编号", "适用对象", "反击核心论点", "物理机理与整机架构证据", "为何 WS-RS 同步闭环无法覆盖", "对用户思路评估 / 合同验收红线"])
# Merge columns 4-5, 6-8, 9-11? Better keep clean 11 columns across Sheet 7 by using unified 11-col layout!
ws7.unmerge_cells(start_row=r7, start_column=1, end_row=r7, end_column=6) if False else None
# Re-write 7A cleanly using merged spans across 11 cols so table widths align nicely with 7B/7C
for col in range(1, 12):
    ws7.cell(r7, col, None)
hdr7a_spans = [
    (1, 1, "编号"),
    (2, 2, "适用台体"),
    (3, 4, "核心工程反击论点"),
    (5, 7, "物理机理与光刻机系统架构依据"),
    (8, 9, "同步指标盲区（为何覆盖不了）"),
    (10, 11, "工程/FAT 验收要求"),
]
for c1, c2, txt in hdr7a_spans:
    if c2 > c1:
        ws7.merge_cells(start_row=r7, start_column=c1, end_row=r7, end_column=c2)
    cell = ws7.cell(r7, c1, txt)
    for cc in range(c1, c2 + 1):
        hc = ws7.cell(r7, cc)
        hc.fill = fill_hdr; hc.font = font_hdr; hc.border = border_cell; hc.alignment = al_center
ws7.row_dimensions[r7].height = 24
r7 += 1

rebuttals = [
    ("R1", "WS 核心", "M-side 测量站根本无 RS 参与（双台决定性死穴）",
     "TWINSCAN/NXT 双台架构中，晶圆对准（SMASH/AA）与调焦调平（UV-LS/AG）均在 M-side 由 WS 独立完成，此时 RS 正在 E-side 曝光另一片晶圆 [009, 066]。",
     "M-side 步进定位、网格滞回与 M→E 换台传递误差在 E-side 曝光同步开启前已永久固化，RS 同步环 100% 不可见、不可补。",
     "WS 必须独立验收静态网格与 M→E 换台定位重复性（XY ≤ 0.30 nm 3σ）。"),
    ("R2", "WS 核心\n(完善用户观点)", "场间步进整定瞬态（Stepping-to-Scan Settling）",
     "【评估用户观点：合理且切中要害！】切场时 WS 需按 M-side 预先算好的轨迹步进 26 mm 并加速切入下一视场起扫窗 [094 Fig.15–16]，此阶段无同步曝光。",
     "需补强回击：虽在匀速段理论上可由从台微调跟踪，但 WS 切入起扫窗的随机整定尾（Settling Tail）撞击曝光窗前沿时，150 m/s² 刚折返的 RS 无多余带宽追赶！",
     "必须考核 26 mm 步进+15 ms 整定窗末端的起扫首狭缝 MA/MSD 重复性。"),
    ("R3", "WS 核心", "Z/Rx/Ry 焦面跟踪与液浸弯月面不能由 RS 兜底",
     "曝光期间 WS 须高频追踪数百 nm 晶圆形貌（Z/Rx/Ry）；且液浸头固定在物镜下，与 WS 保持微米级水膜间隙 [021, 066]。",
     "RS Z 向受 n_w/16 ≈ 1/11.14 限制不做高频形貌伺服；WS 相对物镜/液浸头的偏离会破坏弯月面（气泡/水印）并改变物镜畸变采样点，同步无法消除。",
     "WS-Z/Rx/Ry 必须独立按 4.50 nm / 0.20 / 0.10 μrad 严格验收。"),
    ("R4", "WS & RS\n双向制约", "主从前馈流向与 4× 动力学/MSD 惩罚上限",
     "实际架构常将大加速度（150 m/s²）的 RS 误差前馈给高带宽轻量化 WS 短行程台（或双 Youla 双向耦合 [019, 075]）。",
     "若 RS 自身差，WS 短行程推力与液浸水膜抗扰上限被击穿；若反向让 RS 追赶 WS，1 nm WS 误差要求 RS 4 nm/4× 加速度/4× Jerk 激振，MSD 瞬间崩溃！",
     "单台自身误差决定了耦合前馈的底噪天花板，WS/RS 均须各自达标。"),
    ("R5", "RS 核心", "150 m/s² 高 g 折返下掩模微滑移与静态 RA 标定",
     "RS 以 2.80 m/s、150 m/s²（~15g）频繁折返，易在石英掩模与真空吸盘间激发微滑移 [225]；且换片掩模对准（RA/PARIS）为静态无同步。",
     "同步误差只读 RS 编码器（测台体不测石英玻璃！），掩模相对台体微滑移与静态 RA 重复性在 WS-RS 编码器同步曲线里完全隐身！",
     "RS 必须独立做 1000 趟 150 m/s² 往返+掩模标记微滑移抽检（≤0.60 nm 4×）。"),
    ("R6", "WS & RS\n契约治理", "iHOPC 独立执行能力与子系统 FAT 合同解耦",
     "WS 独立承担 11 项 iHOPC 动态轨迹，RS 独立承担 1:1 等角 Rz 与平衡质量块（BM）反力解耦；两子系统均先于整机合龙独立交付。",
     "若无单台 6-DOF 合同门禁，总装前无法验收入口、无法防止特定工况偶然误差对消掩盖硬件缺陷，整机同步挂掉时无法定责。",
     "强制执行“单台 FAT 6-DOF + 整机 SAT 同步 MA”双门禁验收。"),
]
for idx, (rid, obj, pt, mech, blind, req) in enumerate(rebuttals):
    fill = fill_white if idx % 2 == 0 else fill_zebra
    vals = [(1,1,rid), (2,2,obj), (3,4,pt), (5,7,mech), (8,9,blind), (10,11,req)]
    for c1, c2, txt in vals:
        if c2 > c1:
            ws7.merge_cells(start_row=r7, start_column=c1, end_row=r7, end_column=c2)
        ws7.cell(r7, c1, txt)
        for cc in range(c1, c2 + 1):
            cell = ws7.cell(r7, cc)
            cell.fill = fill; cell.border = border_cell
            cell.font = font_bold if c1 in (1, 3) else font_body
            cell.alignment = al_center if c1 in (1, 2) else al_left
    ws7.row_dimensions[r7].height = 46
    r7 += 1

r7 += 1
# --- Section 7B: WS 6-DOF Unidirectional vs Bidirectional Acceptance Protocol ---
style_section(ws7, r7, 11, "7B. WS（晶圆台）6 自由度单程 vs 往返重复性拆分与验收方案细则（动态链接 Sheet 02 表 1）")
r7 += 1
ws7.merge_cells(start_row=r7, start_column=1, end_row=r7, end_column=11)
c = ws7.cell(r7, 1, "数学定义：单程重复性 R_uni = max_y[3·max(s↑(y), s↓(y))]（同向重复随机离散）；残余反向差 B_res = max_y|μ↑(y)−μ↓(y)|（经方向前馈标定后的残余正反扫/左右步进滞回）；往返综合重复性 R_bi = R_uni + B_res ≤ 表 1 总规格红线（同时核查全蛇形混编样本 |Mean|+3σ 达标）。")
c.font = font_note; c.fill = fill_subhdr; c.border = border_cell; c.alignment = al_left
ws7.row_dimensions[r7].height = 28
r7 += 1

hdr7b = [
    "序号", "WS 自由度", "表 1 总红线\n(动态往返 R_bi)", "单位",
    "静态单程\nR_uni,stat", "静态往返\nR_bi,stat",
    "动态单程\nR_uni,dyn (3σ)", "残余反向差\nB_res (Up/Down)",
    "动态往返核算\n(R_uni+B_res)", "运动行程 / 步进与扫描距离规划", "验收循环工况与统计判定"
]
write_header_row(ws7, r7, hdr7b)
r7 += 1

ws_proto = [
    ("1.1", "WS-X (非扫描向)", f"={s2n_q}!D6",  "nm",   0.20, 0.30, 0.24, 0.08,  "全行程 ±150 mm（机械≥340 mm）；单步 ΔX=26 mm（±X 双向）", "9 点静态×20 往返；满场 90–100 场蛇形×10 盘（a_x=35 m/s²），干/湿态分验"),
    ("1.2", "WS-Y (扫描主轴)", f"={s2n_q}!D7",  "nm",   0.20, 0.30, 0.26, 0.10,  "全行程 ±150 mm（机械≥360 mm）；单扫 33 mm 曝光+两端各 20 mm 加减速=73 mm", "扫速 0.25/0.50/0.70 m/s、a_y=35–40 m/s²、L_s=8 mm MA；5 场×30 往返 + 全片 10 盘"),
    ("1.3", "WS-Z (焦面垂向)", f"={s2n_q}!D8",  "nm",   1.50, 2.20, 3.50, 1.00,  "工作行程 ±100 μm；扫描叠加 ±20 μm 模拟硅片坡度动态跟踪", "陶瓷短行程 WS @ 0.70 m/s 液浸湿态 8 mm MA，核查首狭缝 15 ms 整定尾"),
    ("1.4", "WS-Rx (绕X俯仰)", f"={s2n_q}!D9",  "μrad", 0.08, 0.12, 0.15, 0.05,  "倾角行程 ±300 μrad；扫描叠加 ±150 μrad 硅片局部斜率跟踪", "重点监测 ±Y 加减速反向引起的弯月面俯仰力矩滞回（B_res ≤ 50 nrad）"),
    ("1.5", "WS-Ry (绕Y滚转)", f"={s2n_q}!D10", "μrad", 0.04, 0.06, 0.075, 0.025,"倾角行程 ±300 μrad；横跨 26 mm 狭缝全宽动态调平", "重点监测 ±X 步进换向滚转整定与线缆拖链侧向滞回（B_res ≤ 25 nrad）"),
    ("1.6", "WS-Rz (绕Z偏航)", f"={s2n_q}!D11", "μrad", 0.006,0.009,0.009, 0.003,"偏航行程 ±1.0 mrad；全 300 mm 行程四角 ENC 切向闭环", "严控 ±Y 扫向与 ±X 步向切换诱发偏航滞回 ≤ 3 nrad，总往返 ≤ 12 nrad"),
]
for idx, (sid, dof, ref_f, unit, su, sb, du, br, stroke, cond) in enumerate(ws_proto):
    fill = fill_white if idx % 2 == 0 else fill_zebra
    ws7.cell(r7, 1, sid)
    ws7.cell(r7, 2, dof)
    ws7.cell(r7, 3, ref_f)
    ws7.cell(r7, 4, unit)
    ws7.cell(r7, 5, su)
    ws7.cell(r7, 6, sb)
    ws7.cell(r7, 7, du)
    ws7.cell(r7, 8, br)
    ws7.cell(r7, 9, f"=G{r7}+H{r7}")
    ws7.cell(r7, 10, stroke)
    ws7.cell(r7, 11, cond)
    fmt = "0.000" if du < 0.05 else "0.00"
    for col in range(1, 12):
        cell = ws7.cell(r7, col)
        cell.fill = fill; cell.border = border_cell
        cell.font = font_spec if col in (3, 9) else font_body
        cell.alignment = al_center if col in (1, 3, 4, 5, 6, 7, 8, 9) else al_left
        if col in (3, 5, 6, 7, 8, 9):
            cell.number_format = fmt
    ws7.row_dimensions[r7].height = 34
    r7 += 1

r7 += 1
# --- Section 7C: RS 6-DOF Unidirectional vs Bidirectional Acceptance Protocol ---
style_section(ws7, r7, 11, "7C. RS（掩模台）6 自由度单程 vs 往返重复性及 150 m/s² 微滑移验收细则（掩模侧 4×，动态链接 Sheet 02 表 2）")
r7 += 1
hdr7c = [
    "序号", "RS 自由度", "表 2 总红线\n(4× 往返 R_bi)", "单位",
    "静态往返\nR_bi,stat (RA)", "动态单程\nR_uni,dyn (3σ)",
    "残余正反扫差\nB_UD,res", "动态往返核算\n(R_uni+B_res)",
    "晶圆等效\n(1× 链接)", "掩模侧运动行程 / 扫描距离规划", "高加速度工况、气幕与微滑移验收细则"
]
write_header_row(ws7, r7, hdr7c)
r7 += 1

rs_proto = [
    ("2.1", "RS-X (非扫描向)", f"={s2n_q}!D13", "nm",   0.80, 0.72, 0.24, f"={s2n_q}!F13", "微调/对准行程 ±5–10 mm；曝光有效宽度 104 mm（4×26 mm）", "在 2.80 m/s、150 m/s² Y 向满速折返期间考核 X 向侧向串扰与往返重复性"),
    ("2.2", "RS-Y (扫描主轴)", f"={s2n_q}!D14", "nm",   0.85, 0.78, 0.30, f"={s2n_q}!F14", "有效曝光 132 mm + 两端加减速/整定各 ~50 mm = 单次 230–250 mm（装片总行程 380 mm）", "分级扫速 1.0/2.0/2.80 m/s、a_y=150 m/s²、32 mm 掩模狭缝 MA；100 趟/轮×10 轮（500 上+500 下）+5 mK 水平气幕"),
    ("2.3", "RS-Z (焦面垂向)", f"={s2n_q}!D15", "nm",   12.0, 18.0, 6.00, f"={s2n_q}!F15", "Z 行程 ±150 μm；含掩模重力下垂静补偿与扫描动态平整跟随", "按液浸纵向耦合 n_w/16=1/11.14 换算；同时核查 ±Y 折返加速下的气浮/微动 Z 弹跳"),
    ("2.4", "RS-Rx (绕X俯仰)", f"={s2n_q}!D16", "μrad", 0.25, 0.32, 0.10, f"={s2n_q}!F16", "倾角行程 ±300 μrad；补偿掩模扫描向倾斜（Scheimpflug 0.359×）", "重点考核 150 m/s² 折返瞬间质心偏心诱发的俯仰冲击与 15 ms 整定残余"),
    ("2.5", "RS-Ry (绕Y滚转)", f"={s2n_q}!D17", "μrad", 0.12, 0.14, 0.05, f"={s2n_q}!F17", "倾角行程 ±300 μrad；横跨 104 mm 掩模狭缝（Scheimpflug 0.359×）", "考核粗精台切换与反力平衡块（BM）反冲引起的横向滚转滞回"),
    ("2.6", "RS-Rz (绕Z偏航)", f"={s2n_q}!D18", "μrad", 0.006,0.0065,0.0025,f"={s2n_q}!F18","偏航行程 ±1.5 mrad；双侧 ENC 跨度 200 mm 实时差分闭环（1:1 耦合！）", "最严约束：正反扫偏航滞回 ≤ 2.5 nrad；每 100 趟前后复测掩模相对吸盘微滑移 ≤ 0.60 nm (4×)"),
]
for idx, (sid, dof, ref_f, unit, sb, du, br, w1x, stroke, cond) in enumerate(rs_proto):
    fill = fill_white if idx % 2 == 0 else fill_zebra
    ws7.cell(r7, 1, sid)
    ws7.cell(r7, 2, dof)
    ws7.cell(r7, 3, ref_f)
    ws7.cell(r7, 4, unit)
    ws7.cell(r7, 5, sb)
    ws7.cell(r7, 6, du)
    ws7.cell(r7, 7, br)
    ws7.cell(r7, 8, f"=F{r7}+G{r7}")
    ws7.cell(r7, 9, w1x)
    ws7.cell(r7, 10, stroke)
    ws7.cell(r7, 11, cond)
    fmt = "0.0000" if du < 0.01 else ("0.000" if du < 0.05 else "0.00")
    for col in range(1, 12):
        cell = ws7.cell(r7, col)
        cell.fill = fill; cell.border = border_cell
        cell.font = font_spec if col in (3, 8) else font_body
        cell.alignment = al_center if col in (1, 3, 4, 5, 6, 7, 8, 9) else al_left
        if col in (3, 5, 6, 7, 8):
            cell.number_format = fmt
        elif col == 9:
            cell.number_format = "0.000" if sid == "2.6" else "0.00"
    ws7.row_dimensions[r7].height = 36
    r7 += 1

set_col_widths(ws7, [8, 16, 13, 8, 12, 12, 13, 13, 13, 34, 38])
ws7.freeze_panes = "A4"

# ==============================================================================
# SHEET 8 (v2 NEW): WS iHOPC Km Acceptance Plan + Slit Deconvolution Calculator
# ==============================================================================
style_banner(ws8, 1, 13, "v2 新增专题二（大类 14 深化）：WS 对 iHOPC（K1–K19）分级验收方案审视与 8 mm 狭缝逆卷积计算模型")
ws8.merge_cells("A2:M2")
c = ws8.cell(2, 1, "针对用户提出的离线 K4（及通用 Km）ENC 遥测验收方案：总体框架高度合理，属于子系统 FAT 标准做法；但必须补齐① 8 mm 狭缝滑动平均滤波（MA）、② OLS 投影提取 ΔKm 与串扰、③ Z/Rx/Ry 阿贝耦合伴随护栏、④ 消除“ENC 测 ENC 自己”自闭环盲区的外部标尺+在线曝光双阶段闭环、⑤ 二/三阶轨迹狭缝逆卷积预补偿。")
c.font = font_subtitle; c.alignment = al_left
ws8.row_dimensions[2].height = 30

# --- Section 8A: Critique & Upgrade of User's Offline K4 Proposal ---
r8 = 4
style_section(ws8, r8, 13, "8A. 对用户离线 K4（ENC 实测 Q_enc(t) vs 设定 Q_0(t)）验收方案的逐条工程审视与升级")
r8 += 1
hdr8a_spans = [
    (1, 1, "审视项"),
    (2, 4, "用户原方案要点 / 疑问"),
    (5, 6, "合理性判定"),
    (7, 9, "潜在工程盲区或物理陷阱"),
    (10, 13, "升级后标准验收细则（FAT 离线 + SAT 在线）"),
]
for c1, c2, txt in hdr8a_spans:
    if c2 > c1:
        ws8.merge_cells(start_row=r8, start_column=c1, end_row=r8, end_column=c2)
    ws8.cell(r8, c1, txt)
    for cc in range(c1, c2 + 1):
        hc = ws8.cell(r8, cc)
        hc.fill = fill_hdr; hc.font = font_hdr; hc.border = border_cell; hc.alignment = al_center
ws8.row_dimensions[r8].height = 24
r8 += 1

k4_critiques = [
    ("C1", "按设定扫速 V 与扫描长度下发带 K4 补偿的轨迹 Q_0(t)，用 WS-ENC 实时采样比对",
     "高度合理\n（标准离线 FAT 骨架）",
     "需明确 K4 为扫描向放大率 dy=K4·y，对应速度微调 v_y=v_nom(1+K4)（5 nm/cm 仅 Δv=0.35 μm/s）；若直接用瞬时误差峰值判不合格，会把高频 MSD 误判为套刻误差。",
     "将时域采样映射至曝光窗 y∈[-1.65,+1.65] cm，先做 L_s=8 mm 狭缝强度加权滑动平均（MA）得 e_MA(y)，再与目标比较；同时须覆盖 ±Y 正反扫与多档幅值（0, ±25%, ±50%, ±100% Range）。"),
    ("C2", "“若只验收套刻性能，是否只需看 x_err, y_err, rz_err 三个自由度？”",
     "主判据正确\n（须加 Z/Rx/Ry 护栏）",
     "① 高阶 Km（K8/K11/K14/K19）含额外加减速/Jerk，推力偏心会激发俯仰 Rx/滚转 Ry，经 ENC-硅片残余阿贝臂 h_Abbe 折算为真实 X/Y 漂移；② 非远心度（2–5 mrad）将 z_err 耦合进套刻并劣化焦面 FU。",
     "以 x_err, y_err, rz_err（换算至 ±13 mm 场边 Δy=x·rz_err）作为套刻主判据；同步将 z_err, rx_err, ry_err 设为伴随强制护栏（不得超出表 1 对应 6-DOF 限值）。"),
    ("C3", "如何把残差序列 x_err(t), y_err(t), rz_err(t) 转化为 ΔKm 合格判定？",
     "须补充数学投影步骤",
     "原始时域波形不能直接对应 nm/cm 或 nm/cm² 规格，且下发单一 K4 时可能诱发 K2（平移）、K6（旋转）或 K8（二阶）交叉串扰。",
     "由狭缝平均残差合成 7×9 虚拟视场套刻网格：δx=ē_x(y)−s·e_rz 狭缝平均，δy=ē_y(y)+x·ē_rz(y)；再对 {K1..K19} 做最小二乘（OLS）拟合，同时验收 ΔKm、跨项串扰 ΔK_{j≠m} 与未建模残差 3σ_res。"),
    ("C4", "仅靠 WS-ENC 自身反馈（Q_enc − Q_0）离线验收是否完备？",
     "存在自测盲区！\n（必须分两阶段闭环）",
     "WS 伺服本身靠 WS-ENC 闭环！Q_enc−Q_0 只能测出“伺服跟踪残差”，对① ENC 网格板比例尺误差（如 5 ppm 标尺错直接错 50 nm/cm 却显示 0！）、② 加速下台面弹性弯曲、③ WS-RS/激光时间同步抖动 100% 不可见！",
     "【三级闭环】Stage 1 离线 ENC 遥测验伺服（收严至总红线 55%）；Stage 2 外部独立双频激光干涉仪/标准网格片核验绝对比例尺；Stage 3 整机 SAT 曝光阶跃片（YieldStar 实测 SET-vs-GET）闭合总红线！"),
    ("C5", "高阶项（K8/K11/K16/K14/K19）下发指令 Q_0(t) 应如何构造？",
     "必须内置狭缝逆卷积",
     "8 mm 狭缝对 y²/y³ 轨迹做滑动平均会固有引入 +L_s²/12 常数平移与 +L_s²/4·y 线性斜率偏置（下发 K19=1.0 时在场角多出 0.264 nm 误差！）。",
     "轨迹发生器下发的 Q_0(t) 必须是逆卷积预畸变轨迹（如 K1_cmd=K10−0.0533·K110，K4_cmd=K40−0.160·K140），并在验收中专项抽测大指令下的低阶串扰归零能力。"),
]
for idx, (cid, pt, judge, trap, fix) in enumerate(k4_critiques):
    fill = fill_white if idx % 2 == 0 else fill_zebra
    vals = [(1,1,cid), (2,4,pt), (5,6,judge), (7,9,trap), (10,13,fix)]
    for c1, c2, txt in vals:
        if c2 > c1:
            ws8.merge_cells(start_row=r8, start_column=c1, end_row=r8, end_column=c2)
        ws8.cell(r8, c1, txt)
        for cc in range(c1, c2 + 1):
            cell = ws8.cell(r8, cc)
            cell.fill = fill; cell.border = border_cell
            cell.font = font_spec if c1 == 5 else (font_bold if c1 == 1 else font_body)
            cell.alignment = al_center if c1 in (1, 5) else al_left
    ws8.row_dimensions[r8].height = 50
    r8 += 1

r8 += 1
# --- Section 8B: All 11 WS iHOPC Km Acceptance Matrix (Linked to Sheet 04!) ---
style_section(ws8, r8, 13, "8B. WS 全 11 项 iHOPC 参数（K1–K19）量程、最小调节量与离线/在线分级验收明细表（动态链接 Sheet 04）")
r8 += 1
hdr8b = [
    "参数", "方向", "单项式", "单位", "建议补偿量程\n(±Range)",
    "最小调节量\n(≤Spec/10)", "典型验收指令\n|K0|(链接S04)",
    "离线FAT伺服\n残差(≤55%总)", "在线SAT总红线\n|ΔKm|(链接S04)",
    "最大场角套刻\n(nm 链接S04)", "跨项串扰上限\n(单参满幅)",
    "WS 运动学激励机理 (@0.70 m/s)", "狭缝逆卷积预补偿要求"
]
write_header_row(ws8, r8, hdr8b)
r8 += 1

# Sheet 4 WS rows are rows 20..30 (K1..K19)
ws_k_accept = [
    (20, "±200", "静态 X 偏置位移 δx = K1", "无（线性常数，c=1）"),
    (21, "±200", "静态 Y 相位偏置 δy = K2", "无（线性常数，c=1）"),
    (22, "±50",  "恒速扫描比微调 Δv_y = K4·v（5 nm/cm → 0.35 μm/s）", "无（一阶线性，c=1）"),
    (23, "±50",  "扫描期 X 恒速交叉斜行 v_x = K5·v_y", "无（一阶线性，c=1）"),
    (24, "±50",  "静态偏航偏角 ΔRz = K6（1 nm/cm = 100 nrad）", "无（x 方向静态，c=1）"),
    (25, "±15",  "扫描期恒定微加速度 Δa_y = 2·K8·v_y²", "须预减 ΔK2 = −(L_s²/12)·K8 = −0.0533·K8"),
    (26, "±15",  "扫描期恒定偏航角速度 ω_z = K10·v_y", "无（y 一次项，c=1）"),
    (27, "±15",  "扫描期 X 抛物线加速 Δa_x = 2·K11·v_y²", "须预减 ΔK1 = −(L_s²/12)·K11 = −0.0533·K11"),
    (28, "±5.0", "扫描期 Y 恒定加加速度 Δj_y = 6·K14·v_y³", "须预减 ΔK4 = −(L_s²/4)·K14 = −0.1600·K14"),
    (29, "±5.0", "扫描期 Rz 抛物线角加速度 α_z = 2·K16·v_y²", "须预减 ΔK6 = −(L_s²/12)·K16 = −0.0533·K16"),
    (30, "±5.0", "扫描期 X 恒定加加速度 Δj_x = 6·K19·v_y³", "须预减 ΔK5 = −(L_s²/4)·K19 = −0.1600·K19"),
]
for idx, (s4r, rng_s, kin, dec) in enumerate(ws_k_accept):
    fill = fill_white if idx % 2 == 0 else fill_zebra
    ws8.cell(r8, 1,  f"={s4n_q}!A{s4r}")
    ws8.cell(r8, 2,  f"={s4n_q}!B{s4r}")
    ws8.cell(r8, 3,  f"={s4n_q}!C{s4r}")
    ws8.cell(r8, 4,  f"={s4n_q}!G{s4r}")
    ws8.cell(r8, 5,  rng_s)
    ws8.cell(r8, 6,  f"={s4n_q}!K{s4r}/10")
    ws8.cell(r8, 7,  f"={s4n_q}!J{s4r}")
    ws8.cell(r8, 8,  f"={s4n_q}!K{s4r}*0.55")
    ws8.cell(r8, 9,  f"={s4n_q}!K{s4r}")
    ws8.cell(r8, 10, f"={s4n_q}!M{s4r}")
    ws8.cell(r8, 11, f"={s4n_q}!K{s4r}*0.30")
    ws8.cell(r8, 12, kin)
    ws8.cell(r8, 13, dec)
    for col in range(1, 14):
        cell = ws8.cell(r8, col)
        cell.fill = fill; cell.border = border_cell
        cell.font = font_spec if col in (8, 9) else (font_bold if col == 1 else font_body)
        cell.alignment = al_left if col in (12, 13) else al_center
    ws8.cell(r8, 6).number_format = "0.0000"
    ws8.cell(r8, 7).number_format = "0.0"
    ws8.cell(r8, 8).number_format = "0.000"
    ws8.cell(r8, 9).number_format = "0.000"
    ws8.cell(r8, 10).number_format = "0.000"
    ws8.cell(r8, 11).number_format = "0.000"
    ws8.row_dimensions[r8].height = 28
    r8 += 1

r8 += 1
# --- Section 8C: Live Slit Deconvolution Numerical Calculator ---
style_section(ws8, r8, 13, "8C. 8 mm 曝光狭缝卷积串扰与逆卷积预补偿动态计算表（修改 Sheet 04 狭缝宽 L_s 自动重算！）")
r8 += 1
hdr8c = [
    "高阶参数", "阶次\n(y^q)", "典型目标\nK_target", "单位",
    "狭缝宽 L_s\n(cm 链接S04)", "狭缝二阶矩\nμ2=L_s²/12",
    "逆卷积耦合系数\nc_deconv", "受串扰低阶项",
    "未逆卷积诱发\n低阶串扰量", "场角额外套刻\n恶化 (nm)",
    "逆卷积预补偿\n下发修偏值", "预补偿后印刷\n理论残差", "工程结论"
]
write_header_row(ws8, r8, hdr8c)
r8 += 1

deconv_rows = [
    ("K8 (dy=K8·y²)",   2, f"={s4n_q}!J25", "nm/cm²", "1*F", "K2 (平移 dy)",   1.00, "若不预减 −0.0533·K8，产生 0.107 nm 视场平移偏置"),
    ("K11 (dx=K11·y²)", 2, f"={s4n_q}!J27", "nm/cm²", "1*F", "K1 (平移 dx)",   1.00, "若不预减 −0.0533·K11，产生 0.107 nm 视场平移偏置"),
    ("K16 (dy=K16·xy²)",2, f"={s4n_q}!J29", "nm/cm³", "1*F", "K6 (旋转 x)",    1.30, "若不预减 −0.0533·K16，诱发 0.043 nm/cm 旋转（场角 0.055 nm）"),
    ("K14 (dy=K14·y³)", 3, f"={s4n_q}!J28", "nm/cm³", "3*F", "K4 (Y放大率 y)", 1.65, "【重大风险】不逆卷积将诱发 +0.160 nm/cm Y 放大率（场角 +0.264 nm，超自身预算 2.3×！）"),
    ("K19 (dx=K19·y³)", 3, f"={s4n_q}!J30", "nm/cm³", "3*F", "K5 (X偏斜 y)",   1.65, "【重大风险】不逆卷积将诱发 +0.160 nm/cm X 偏斜（场角 +0.264 nm，超自身预算 2.3×！）"),
]
for idx, (kp, qord, kref, unit, cexpr, tgt_low, g_low, note) in enumerate(deconv_rows):
    fill = fill_warn if qord == 3 else (fill_white if idx % 2 == 0 else fill_zebra)
    ws8.cell(r8, 1, kp)
    ws8.cell(r8, 2, qord)
    ws8.cell(r8, 3, kref)
    ws8.cell(r8, 4, unit)
    ws8.cell(r8, 5, f"={s4n_q}!G3")
    ws8.cell(r8, 6, f"=(E{r8}^2)/12")
    ws8.cell(r8, 7, f"=F{r8}" if qord == 2 else f"=3*F{r8}")
    ws8.cell(r8, 8, tgt_low)
    ws8.cell(r8, 9, f"=C{r8}*G{r8}")
    ws8.cell(r8, 10, f"=I{r8}*{g_low}")
    ws8.cell(r8, 11, f"=-I{r8}")
    ws8.cell(r8, 12, f"=I{r8}+K{r8}")
    ws8.cell(r8, 13, note)
    for col in range(1, 14):
        cell = ws8.cell(r8, col)
        cell.fill = fill; cell.border = border_cell
        cell.font = font_spec if col in (9, 10, 11) else (font_bold if col == 1 else font_body)
        cell.alignment = al_left if col in (1, 8, 13) else al_center
    ws8.cell(r8, 3).number_format = "0.0"
    ws8.cell(r8, 5).number_format = "0.00"
    ws8.cell(r8, 6).number_format = "0.0000"
    ws8.cell(r8, 7).number_format = "0.0000"
    ws8.cell(r8, 9).number_format = "0.000"
    ws8.cell(r8, 10).number_format = "0.000"
    ws8.cell(r8, 11).number_format = "+0.000;-0.000;0.000"
    ws8.cell(r8, 12).number_format = "0.000"
    ws8.row_dimensions[r8].height = 30
    r8 += 1

set_col_widths(ws8, [16, 9, 11, 9, 12, 11, 12, 12, 12, 12, 12, 30, 34])
ws8.freeze_panes = "A4"

# ==============================================================================
# SHEET 9 (v2 NEW): Projection Optics (Lens) Kn 8-Dimension Capability Matrix
# ==============================================================================
style_banner(ws9, 1, 14, "v2 新增专题三（大类 13 深化）：投影物镜（PO）对 iHOPC K 参数补偿能力的 8 维综合评价体系与逐项量化指标")
ws9.merge_cells("A2:N2")
c = ws9.cell(2, 1, "核心回答：评价物镜 K 参数补偿能力绝不仅看单项残差，必须全面覆盖【1. 单参/联合补偿范围 Range】【2. 最小调节量 Resolution】【3. 单/双向重复性与滞回】【4. SET-vs-GET 线性精度】【5. 跨 K 串扰与波像差/焦面副作用】【6. 响应/整定时间】【7. 保持稳定性与热漂移】【8. 三级验证链路 PMI→ILIAS/PARIS→晶圆套刻】八大维度！")
c.font = font_subtitle; c.alignment = al_left
ws9.row_dimensions[2].height = 30

# --- Section 9A: 8-Dimension Framework ---
r9 = 4
style_section(ws9, r9, 14, "9A. 物镜 K 参数补偿能力 8 维综合评价框架（回答用户问题 4）")
r9 += 1
hdr9a_spans = [
    (1, 1, "维度"),
    (2, 3, "评价指标名称"),
    (4, 7, "物理定义与测试方法"),
    (8, 10, "工程准入原则 / 目标基准"),
    (11, 14, "典型失效模式与 OV4 文献对标"),
]
for c1, c2, txt in hdr9a_spans:
    if c2 > c1:
        ws9.merge_cells(start_row=r9, start_column=c1, end_row=r9, end_column=c2)
    ws9.cell(r9, c1, txt)
    for cc in range(c1, c2 + 1):
        hc = ws9.cell(r9, cc)
        hc.fill = fill_hdr; hc.font = font_hdr; hc.border = border_cell; hc.alignment = al_center
ws9.row_dimensions[r9].height = 24
r9 += 1

dims_8 = [
    ("D1", "补偿范围\n(单参 & 联合 Range)",
     "同时评估单参极限行程 ±K_n,max 及多参数联合工作包络（叠加冷机标定+满载透镜加热+跨机匹配 iHOPC 指令时，任意镜片操纵器均不饱和）。",
     "单参 Range ≥ 4–6× 典型量产 |K0|；联合工况下所有驱动器行程占用率 ≤ 80%（预留 ≥20% 热态裕量）。",
     "若仅测单参 Range，联合叠加 K3+K7+K13+热球差补偿时极易触发某个 Z 镜片限位裁剪，导致边缘畸变失控 [154, 253]。"),
    ("D2", "最小调节量\n(Resolution / LSB)",
     "施加递增微小阶跃指令，以空间像/干涉仪测得单调、统计可分辨的最小光学响应步长 ΔK_n,min（包含克服压电/柔性机构死区与静摩擦）。",
     "遵循 1/8–1/10 原则：ΔK_n,min ≤ 0.10 × |ΔK_n,spec|（如 K3 ≤ 0.010 nm/cm，K7/K12 ≤ 0.008 nm/cm²）。",
     "若最小调节量过大或存在死区（Deadband），APC 闭环微调时会出现“调不动”或极限环振荡。"),
    ("D3", "调节重复性误差\n(单向 + 双向滞回)",
     "分别测试单向重复定位（0→+K_n0，N≥20 次 3σ）与双向往返滞回（−K_n0→0→+K_n0 与反向差值 B_hyst）。",
     "单向重复性 ≤ 35% 总残差红线；双向滞回 B_hyst ≤ 25% 总残差红线（须靠电容/应变闭环传感抑滞回）。",
     "开环压电陶瓷与柔性铰链存在 1%–3% 固有滞回，若不闭环校准，会导致正负向补偿切换产生系统性套刻偏置。"),
    ("D4", "SET-vs-GET 精度\n与全程线性度",
     "在 ±K_n,max 内分段下发阶跃指令，用机内 ILIAS/PARIS 及曝光硅片拟合 K_n1 = (1+ε_gain)K_n0 + ε_nl，提取比例误差与非线性残差。",
     "静态项相对精度 ≤ 2.5%–5.0%，动态项 ≤ 4.0%–5.6%；全量程综合残差 |K_n1−K_n0| ≤ 表 13 验收规格。",
     "对标 Nikon MDDM 实测 2% [160 Fig.7] 与 ASML/Zeiss 畸变操纵器空间像 5%、光刻胶 10% [253 Fig.7–8]。"),
    ("D5", "跨 K 串扰与波像差/\n焦面副作用（特有！）",
     "下发满量程单一 K_n 时，同步监测① 其他畸变项 ΔK_{j≠n} 泄漏、② 最佳焦面偏移 ΔZ_focus、③ 偶/奇 Zernike 波前 ΔZ_even/odd 恶化量。",
     "跨 K 串扰 ≤ 2%–3%（或 ≤ 目标残差 30%）；诱发焦面 ≤ 1.0–1.5 nm，偶像差 ≤ 0.15 nm RMS，奇像差 ≤ 0.05 nm RMS。",
     "物镜镜片移动天生耦合畸变与波像差；[253 Sec.1] 强调畸变操纵器不得破坏邻近效应/像质匹配，必须联合解耦标定！"),
    ("D6", "响应时间与动态带宽\n(Settling Time)",
     "考核阶跃下发至进入残差带的时间 T_settle，以及动态项（K9/K15/K17/K18）在 11.4 ms 扫描狭缝内的同步跟踪相位滞后。",
     "静态镜片操纵器 ≤ 20–50 ms（场间/片间）；动态扫描项相位滞后 ≤ 0.2 ms；激光 Δλ < 1 ms；热控 FlexWave 10–60 s。",
     "对标 Nikon MDDM 50 ms 响应达 2% [160 Sec.4]；响应慢会拖累 230 wph 产能或在场首留下整定误差。"),
    ("D7", "保持稳定性与漂移\n(Creep & Thermal)",
     "锁定指令 K_n0 后，连续监测 15 s（单片压电蠕变）、15 min（满功率曝光透镜热浸）及 24 h（长期零点保持）的 K_n1 漂移。",
     "15 s 蠕变 ≤ 20% 规格；15 min 满功率批内漂移 ≤ 35% 规格；24 h 零点漂移 ≤ 50% 规格（可批间重校）。",
     "高 NA 深紫外吸收导致透镜内部温度梯度缓慢演化，若前馈热模型失配会产生片间持续漂移。"),
    ("D8", "三级可观性与\n验收闭环链路",
     "构建“离线光学台 PMI FAT → 整机机内 ILIAS/PARIS 标定 → 晶圆密集点曝光套刻 SAT”三级递增验收体系。",
     "PMI 验 Range/滞回/波像差；ILIAS/PARIS 13 点/7 点验 SET-vs-GET ≤5%；51×19 光刻胶实测验最终套刻闭环。",
     "完整复刻 ASML/Zeiss [253 Fig.3, 7, 8] 行业验证链路，杜绝单级测试遗漏实机曝光耦合效应。"),
]
for idx, (did, dname, ddef, dstd, dref) in enumerate(dims_8):
    fill = fill_white if idx % 2 == 0 else fill_zebra
    vals = [(1,1,did), (2,3,dname), (4,7,ddef), (8,10,dstd), (11,14,dref)]
    for c1, c2, txt in vals:
        if c2 > c1:
            ws9.merge_cells(start_row=r9, start_column=c1, end_row=r9, end_column=c2)
        ws9.cell(r9, c1, txt)
        for cc in range(c1, c2 + 1):
            cell = ws9.cell(r9, cc)
            cell.fill = fill; cell.border = border_cell
            cell.font = font_bold if c1 in (1, 2) else font_body
            cell.alignment = al_center if c1 in (1, 2) else al_left
    ws9.row_dimensions[r9].height = 42
    r9 += 1

r9 += 1
# --- Section 9B: Quantitative Capability Table for All 8 Active Lens Kn + K20 ---
style_section(ws9, r9, 14, "9B. 物镜全 8 项激活参数（+K20 说明）8 维能力量化验收表（动态链接 Sheet 04 表 13 残差红线）")
r9 += 1
hdr9b = [
    "参数", "方向", "单项式", "单位", "单参补偿范围\n(±Range)",
    "最小调节量\n(≤Spec/10)", "单向重复性\n(≤35%Spec)", "双向滞回\n(≤25%Spec)",
    "SET-vs-GET\n总残差(链接S04)", "跨 K 串扰\n(满幅≤30%)",
    "诱发焦面\n上限 (nm)", "诱发奇像差\n上限 (nm RMS)",
    "整定/响应时间", "执行模式与三级验证重点"
]
write_header_row(ws9, r9, hdr9b)
r9 += 1

# Sheet 4 Lens rows are rows 7..15 (K3, K7, K12, K13, K9, K15, K17, K18, K20)
lens_cap_rows = [
    (7,  True,  "±25.0", 1.0, 0.04, "≤ 20 ms（波长 <1 ms）", "纯静态：Z向镜片+Δλ联合；PMI+PARIS+曝光"),
    (8,  True,  "±10.0", 1.2, 0.05, "≤ 40 ms（场间/片间）",   "纯静态：倾斜/偏心镜片；重点验 K12/慧差串扰"),
    (9,  True,  "±10.0", 1.2, 0.05, "≤ 40 ms（场间/片间）",   "纯静态：非球面/倾斜镜片；重点验 K7/像散串扰"),
    (10, True,  "±6.0",  1.5, 0.05, "≤ 50 ms（场间/片间）",   "纯静态：球差镜片组；重点验球差 Z9 与焦面耦合"),
    (11, True,  "±8.0",  1.2, 0.05, "同步跟踪（滞后≤0.2 ms）","动态扫描：随 y 线性调 Mx/掩模 Z；验扫速相关性"),
    (12, True,  "±4.0",  1.5, 0.05, "同步跟踪（滞后≤0.2 ms）","动态扫描：随 y 线性调 K7 操纵器；验动态滞回"),
    (13, True,  "±4.0",  1.5, 0.05, "同步跟踪（滞后≤0.2 ms）","动态扫描：随 y² 二阶调 Mx/掩模 Z；验狭缝均值"),
    (14, True,  "±4.0",  1.5, 0.05, "同步跟踪（滞后≤0.2 ms）","动态扫描：随 y 线性调 K12 操纵器；验正反扫一致"),
    (15, False, "N/A（不支持）", "N/A", "N/A", "N/A", "【架构限制】1950i–1970Ci 无 K20 操纵器 [154]，仅出厂静畸变控 ≤0.15 nm/cm³"),
]
for idx, (s4r, act, rng_s, foc_lim, odd_lim, tresp, mode_txt) in enumerate(lens_cap_rows):
    fill = fill_warn if not act else (fill_white if idx % 2 == 0 else fill_zebra)
    ws9.cell(r9, 1, f"={s4n_q}!A{s4r}")
    ws9.cell(r9, 2, f"={s4n_q}!B{s4r}")
    ws9.cell(r9, 3, f"={s4n_q}!C{s4r}")
    ws9.cell(r9, 4, f"={s4n_q}!G{s4r}")
    ws9.cell(r9, 5, rng_s)
    if act:
        ws9.cell(r9, 6, f"={s4n_q}!K{s4r}/10")
        ws9.cell(r9, 7, f"={s4n_q}!K{s4r}*0.35")
        ws9.cell(r9, 8, f"={s4n_q}!K{s4r}*0.25")
        ws9.cell(r9, 9, f"={s4n_q}!K{s4r}")
        ws9.cell(r9, 10, f"={s4n_q}!K{s4r}*0.30")
        ws9.cell(r9, 11, foc_lim)
        ws9.cell(r9, 12, odd_lim)
    else:
        for cc in range(6, 13):
            ws9.cell(r9, cc, "N/A")
    ws9.cell(r9, 13, tresp)
    ws9.cell(r9, 14, mode_txt)
    for col in range(1, 15):
        cell = ws9.cell(r9, col)
        cell.fill = fill; cell.border = border_cell
        cell.font = font_na if not act else (font_spec if col in (6, 7, 8, 9) else (font_bold if col == 1 else font_body))
        cell.alignment = al_left if col == 14 else al_center
    if act:
        ws9.cell(r9, 6).number_format = "0.0000"
        ws9.cell(r9, 7).number_format = "0.000"
        ws9.cell(r9, 8).number_format = "0.000"
        ws9.cell(r9, 9).number_format = "0.000"
        ws9.cell(r9, 10).number_format = "0.000"
        ws9.cell(r9, 11).number_format = "0.0"
        ws9.cell(r9, 12).number_format = "0.00"
    ws9.row_dimensions[r9].height = 32 if act else 38
    r9 += 1

set_col_widths(ws9, [8, 8, 9, 9, 13, 11, 11, 11, 12, 11, 10, 11, 18, 34])
ws9.freeze_panes = "A4"

# Save workbook
wb.save(OUT_XLSX)
print(f"SAVED EXCEL SUCCESSFULLY: {OUT_XLSX}")

# Print exact Python-evaluated verification summary for report consistency
print("\n================ FINAL VERIFIED SUMMARY NUMBERS ================")
print(f"Item 15 (30-term All-Odd) OVL RSS (Abbe Sim): X={math.sqrt(py_ovl_x_sim30):.4f}, Y={math.sqrt(py_ovl_y_sim30):.4f} nm")
print(f"Item 15 (30-term All-Odd) OVL RSS (Envelope): X={math.sqrt(py_ovl_x_env30):.4f}, Y={math.sqrt(py_ovl_y_env30):.4f} nm")
print(f"Item 15 (28-term 1/3/5th) OVL RSS (Envelope): X={math.sqrt(py_ovl_x_env28):.4f}, Y={math.sqrt(py_ovl_y_env28):.4f} nm")
print(f"Item 15 Total Odd WFE RMS: 30-term={math.sqrt(py_wfe_30):.4f} nm RMS | 28-term={math.sqrt(py_wfe_28):.4f} nm RMS")
for gk, gv in py_grp.items():
    print(f"  Group {gk}: {math.sqrt(gv):.4f} nm RMS")

# Evaluate DCO, MMO, FU identically to Excel formulas
a, b = 1.30, 1.65
lens_cx = math.sqrt(sum((dk * (a**p)*(b**q))**2 for K, ax, mono, p, q, desc, u, k0, dk, act in lens_ihopc if act and "X" in ax))
lens_cy = math.sqrt(sum((dk * (a**p)*(b**q))**2 for K, ax, mono, p, q, desc, u, k0, dk, act in lens_ihopc if act and "Y" in ax))
lens_rx = math.sqrt(sum((dk * (a**p/math.sqrt(2*p+1))*(b**q/math.sqrt(2*q+1)))**2 for K, ax, mono, p, q, desc, u, k0, dk, act in lens_ihopc if act and "X" in ax))
lens_ry = math.sqrt(sum((dk * (a**p/math.sqrt(2*p+1))*(b**q/math.sqrt(2*q+1)))**2 for K, ax, mono, p, q, desc, u, k0, dk, act in lens_ihopc if act and "Y" in ax))

ws_cx = math.sqrt(sum((dk * (a**p)*(b**q))**2 for K, ax, mono, p, q, desc, u, k0, dk in ws_ihopc if "X" in ax))
ws_cy = math.sqrt(sum((dk * (a**p)*(b**q))**2 for K, ax, mono, p, q, desc, u, k0, dk in ws_ihopc if "Y" in ax))
ws_rx = math.sqrt(sum((dk * (a**p/math.sqrt(2*p+1))*(b**q/math.sqrt(2*q+1)))**2 for K, ax, mono, p, q, desc, u, k0, dk in ws_ihopc if "X" in ax))
ws_ry = math.sqrt(sum((dk * (a**p/math.sqrt(2*p+1))*(b**q/math.sqrt(2*q+1)))**2 for K, ax, mono, p, q, desc, u, k0, dk in ws_ihopc if "Y" in ax))

print(f"Item 13 Lens iHOPC: Corner X={lens_cx:.4f}, Y={lens_cy:.4f} nm | RMS X={lens_rx:.4f}, Y={lens_ry:.4f} nm")
print(f"Item 14 WS   iHOPC: Corner X={ws_cx:.4f}, Y={ws_cy:.4f} nm | RMS X={ws_rx:.4f}, Y={ws_ry:.4f} nm")

z30_x = math.sqrt(py_ovl_x_env30)
z30_y = math.sqrt(py_ovl_y_env30)
dco_x_list = [
    math.sqrt(0.40**2 + (4*0.015)**2)*math.sqrt(2),
    math.sqrt(0.35**2 + 0.25**2)*math.sqrt(2),
    0.40*math.sqrt(2),
    math.sqrt(0.35**2 + 0.20**2)*math.sqrt(2),
    math.sqrt(0.25**2 + 0.27**2)*math.sqrt(2),
    math.sqrt(0.15**2 + 0.15**2)*math.sqrt(2),
    math.sqrt(0.25**2 + 0.15**2)*math.sqrt(2),
    lens_cx*1.2, ws_cx*1.2, z30_x*1.0, 0.25*math.sqrt(2)
]
dco_y_list = [
    math.sqrt(0.45**2 + (13*0.015)**2)*math.sqrt(2),
    math.sqrt(0.35**2 + 0.25**2)*math.sqrt(2),
    0.40*math.sqrt(2),
    math.sqrt(0.35**2 + 0.20**2)*math.sqrt(2),
    math.sqrt(0.25**2 + 0.27**2)*math.sqrt(2),
    math.sqrt(0.15**2 + 0.15**2)*math.sqrt(2),
    math.sqrt(0.25**2 + 0.15**2)*math.sqrt(2),
    lens_cy*1.2, ws_cy*1.2, z30_y*1.0, 0.25*math.sqrt(2)
]
dco_rss_x = math.sqrt(sum(v**2 for v in dco_x_list))
dco_rss_y = math.sqrt(sum(v**2 for v in dco_y_list))
print(f"DCO 2-layer 3sigma RSS: X={dco_rss_x:.4f}, Y={dco_rss_y:.4f} nm")
print(f"DCO |Mean|(0.30)+3sigma: X={dco_rss_x+0.30:.4f}, Y={dco_rss_y+0.30:.4f} nm (Target <= 2.00 nm)")

mmo_x_list = [dco_rss_x, 0.80, 1.10, 0.95, 0.25*math.sqrt(2), 0.90, 0.85, z30_x, 0.55]
mmo_y_list = [dco_rss_y, 0.80, 1.10, 0.95, 0.25*math.sqrt(2), 0.90, 0.85, z30_y, 0.55]
mmo_rss_x = math.sqrt(sum(v**2 for v in mmo_x_list))
mmo_rss_y = math.sqrt(sum(v**2 for v in mmo_y_list))
print(f"MMO 3sigma RSS: X={mmo_rss_x:.4f}, Y={mmo_rss_y:.4f} nm | +|Mean|(0.45): X={mmo_rss_x+0.45:.4f}, Y={mmo_rss_y+0.45:.4f} nm (Target <= 3.50 nm)")

fu_list = [5.00, math.sqrt((4*0.25)**2 + (13*0.12)**2), 6.00, 2.00, 2.50, 3.50, 4.00, math.sqrt(1.50**2 + 1.32**2)]
fu_rss = math.sqrt(sum(v**2 for v in fu_list))
print(f"Focus Uniformity 3sigma RSS: {fu_rss:.4f} nm (Target <= 12.0 nm)")
