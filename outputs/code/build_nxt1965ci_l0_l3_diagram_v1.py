# -*- coding: utf-8 -*-
"""
Generate NXT:1965Ci (SMO <= 2.50 nm, MMO <= 4.50 nm) L0 -> L1 -> L2 -> L3
Overlay Error Budget & Propagation DAG Diagram (Ref-146 Fig. 3 style).

Outputs (single source of truth):
  1. outputs/images/NXT1965Ci_SMO2.5_MMO4.5_L0-L3套刻指标拆解图_v1.drawio
  2. outputs/images/NXT1965Ci_SMO2.5_MMO4.5_L0-L3套刻指标拆解图_v1.png
"""
import os
import math
import xml.etree.ElementTree as ET
from xml.dom import minidom
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.path import Path
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------
# 1. Mathematical Verification (Single Source of Truth)
# ---------------------------------------------------------------------------
def rss(vals):
    return math.sqrt(sum(v * v for v in vals))

# L2 two-layer 3sigma budgets (nm, wafer level) grouped by L1
l2_f1 = [0.74, 0.35, 0.27]          # f1 sync MA (XY+Rz), f2 WS-iHOPC, f1b dynamic coupling/settle margin -> wait let's keep 2 clean L2 under F1!
# Let's make L2 -> L1 exact to 2 decimals!
# F1: f1 Sync MA (XY 0.72 + Rz 0.27 -> 0.77) + f2 WS-iHOPC (0.38) => sqrt(0.77^2 + 0.38^2) = 0.8587 -> 0.86 nm
# F2: f3 M-side Wafer Align (0.68) + f4 E-side Reticle Align (0.68) => sqrt(0.68^2 + 0.68^2) = 0.9617 -> 0.96 nm
# F3: f5 Lens-iHOPC (0.40) + f6 Odd Zernike (0.42) + f7 Lens Heating/Acoustic (0.32) => sqrt(0.40^2+0.42^2+0.32^2) = 0.6624 -> 0.66 nm
# F4: f8 Wafer Thermal+Evap (0.71) + f9 UPW Refractive Index (0.30) => sqrt(0.71^2+0.30^2) = 0.7708 -> 0.77 nm
# F5: f10 Reticle Heating RHC (0.55) + f11 Reticle Air-Gap (0.45) + f12 RT Clamping/Slip (0.37) => sqrt(0.55^2+0.45^2+0.37^2) = 0.8012 -> 0.80 nm
# F6: f13 WT Re-clamping & Micro-Slip (0.57) => 0.57 nm
# F7: f14 Dual-Chuck C2C (0.48) + Overlay Metrology Floor (0.34) => sqrt(0.48^2+0.34^2) = 0.5882 -> 0.59 nm

F1 = rss([0.77, 0.38])              # 0.8587 nm
F2 = rss([0.68, 0.68])              # 0.9617 nm
F3 = rss([0.40, 0.42, 0.32])        # 0.6624 nm
F4 = rss([0.71, 0.30])              # 0.7708 nm
F5 = rss([0.55, 0.45, 0.37])        # 0.8012 nm
F6 = 0.5700                         # 0.5700 nm
F7 = rss([0.48, 0.34])              # 0.5882 nm

SMO_rand = rss([F1, F2, F3, F4, F5, F6, F7])   # 2.0005 nm
SMO_mean = 0.350
SMO_tot  = SMO_rand + SMO_mean                 # 2.3505 nm <= 2.50 nm

DCO_rand = rss([F1, F2, F3, F4, F5, F6, 0.34]) # 1.9421 nm
DCO_mean = 0.300
DCO_tot  = DCO_rand + DCO_mean                 # 2.2421 nm <= 2.50 nm

M1 = 2.000                                     # Cross-machine Gridplate matching
M2 = rss([1.60, 0.50, 0.90])                   # 1.9026 nm (Lens NCE + Odd Z + LH)
M3 = rss([1.00, 1.00, 0.85])                   # 1.6500 nm (WT warp + WAD/TIS + Thermal)
MMO_rand = rss([SMO_rand, M1, M2, M3])         # 3.7878 nm
MMO_mean = 0.500
MMO_tot  = MMO_rand + MMO_mean                 # 4.2878 nm <= 4.50 nm

print(f"F1={F1:.3f}, F2={F2:.3f}, F3={F3:.3f}, F4={F4:.3f}, F5={F5:.3f}, F6={F6:.3f}, F7={F7:.3f}")
print(f"SMO: rand={SMO_rand:.3f} + mean={SMO_mean:.3f} = {SMO_tot:.3f} nm (target <= 2.50, margin={2.50-SMO_tot:.3f})")
print(f"DCO: rand={DCO_rand:.3f} + mean={DCO_mean:.3f} = {DCO_tot:.3f} nm (target <= 2.50, margin={2.50-DCO_tot:.3f})")
print(f"MMO: M1={M1:.3f}, M2={M2:.3f}, M3={M3:.3f} -> rand={MMO_rand:.3f} + mean={MMO_mean:.3f} = {MMO_tot:.3f} nm (target <= 4.50, margin={4.50-MMO_tot:.3f})")

# Variance shares of F1..F6 within DCO core (excluding F7) vs ref009-fig3
dco6_var = sum(v*v for v in [F1, F2, F3, F4, F5, F6])
for name, val, ref_pct in [
    ("F1 Stage", F1, 20.0), ("F2 Align", F2, 25.6), ("F3 Optics", F3, 12.0),
    ("F4 WaferTh", F4, 16.0), ("F5 Reticle", F5, 18.0), ("F6 WClamp", F6, 8.4)
]:
    print(f"  {name:10s}: DCO6 var% = {val*val/dco6_var*100:5.1f}%  (ref009-fig3: {ref_pct:4.1f}%) | SMO7 var% = {val*val/(SMO_rand**2)*100:5.1f}%")

# ---------------------------------------------------------------------------
# 2. Graph Layout Specification (Canvas: 2240 x 1460 px)
# ---------------------------------------------------------------------------
W_CANVAS = 2280
H_CANVAS = 1480

# Colors (clean academic/ASML palette, white background)
PAL = {
    'l0_mmo':  ('#EDE9FE', '#5B21B6'),  # deep violet
    'l0_smo':  ('#FEF3C7', '#B45309'),  # amber gold
    'l0_mean': ('#F3F4F6', '#4B5563'),  # slate gray
    'm_match': ('#F3E8FF', '#7C3AED'),  # purple matching
    'f1':      ('#E0E7FF', '#3730A3'),  # indigo (Ref009 lavender)
    'f2':      ('#FEF9C3', '#A16207'),  # yellow (Ref009 yellow)
    'f3':      ('#ECFCCB', '#4D7C0F'),  # olive (Ref009 olive)
    'f4':      ('#CFFAFE', '#0E7490'),  # cyan (Ref009 cyan)
    'f5':      ('#DBEAFE', '#1D4ED8'),  # blue (Ref009 blue)
    'f6':      ('#F5F5DC', '#78716C'),  # khaki (Ref009 khaki)
    'f7':      ('#FCE7F3', '#BE185D'),  # rose (C2C + Metrology)
    'l3_bg':   ('#FFFFFF', '#334155'),  # crisp white leaf
    'l3_sh':   ('#FFF7ED', '#C2410C'),  # shared-source highlighted leaf
}

# Node dict: id -> (col, x, y, w, h, title, sub, fill, stroke, bold_val)
nodes = {}

def add_node(nid, x, y, w, h, title, sub, theme_key, badge=None):
    fill, stroke = PAL[theme_key]
    nodes[nid] = {
        'id': nid, 'x': x, 'y': y, 'w': w, 'h': h,
        'title': title, 'sub': sub, 'fill': fill, 'stroke': stroke,
        'badge': badge
    }

# Column X coordinates
X_L0 = 40
X_L1 = 420
X_L2 = 910
X_L3 = 1460

W_L0 = 290
W_L1 = 380
W_L2 = 420
W_L3 = 770

# --- L0 Nodes (Left) ---
add_node('L0_MMO', X_L0, 155, W_L0, 125,
         'L0-A 混机套刻 MMO ≤ 4.50 nm',
         '闭环 4.29 nm = |Mean| 0.50 + 3σ 3.79 nm\n裕度 0.21 nm (4.7%) · 全晶圆 99.7%',
         'l0_mmo', badge='NXT:1965Ci')

add_node('L0_MMO_M', X_L0, 315, W_L0, 62,
         '跨机系统残余均值 |Mean|_MMO',
         '0.50 nm（线性叠加，含参考片零点与 APC 残差）',
         'l0_mean')

add_node('L0_SMO', X_L0, 645, W_L0, 145,
         'L0-B 单机套刻 SMO ≤ 2.50 nm',
         '闭环 2.35 nm = |Mean| 0.35 + 3σ 2.00 nm\n裕度 0.15 nm (6.0%) · 双卡盘全片\n(同卡盘 DCO = 2.24 nm · 对标 Ref009 Fig.3)',
         'l0_smo', badge='Ref009 基线')

add_node('L0_SMO_M', X_L0, 825, W_L0, 62,
         '单机系统残余均值 |Mean|_SMO',
         '0.35 nm（线性叠加，APC 校准后系统偏置）',
         'l0_mean')

# --- L1 Nodes (Subsystem / Functional Budget F_k(f,x; P)) ---
# Top 3: MMO incremental matching branches
add_node('M1', X_L1, 115, W_L1, 66,
         'M1 跨机栅格与工件台网格匹配　2.00 nm',
         'NXT 跨机 Gridplate 标定残差 (Ref009 §6.1: ~2 nm)',
         'm_match')
add_node('M2', X_L1, 195, W_L1, 66,
         'M2 跨机物镜静态畸变与像差匹配　1.90 nm',
         '静态高阶 NCE 1.60 + 奇像差 0.50 + 热失配 0.90 (RSS)',
         'm_match')
add_node('M3', X_L1, 275, W_L1, 66,
         'M3 跨机卡盘/翘曲/对准/热匹配　1.65 nm',
         'WT 翘曲 1.00 + WAD/TIS 1.00 + 跨机热 0.85 (RSS)',
         'm_match')

# Bottom 7: SMO = 2.00 nm (3sigma RSS) -> Ref009-Fig.3 6 domains + C2C/Floor
add_node('F1', X_L1, 385, W_L1, 86,
         'F1 运动台定位与同步　0.86 nm (3σ)',
         'Ref009 Fig.3 占比 20.0% (本模型 DCO6 20.2% / SMO 18.5%)\nF1(f1, f2; P_scan, P_iHOPC) · RSS 合成',
         'f1')
add_node('F2', X_L1, 495, W_L1, 86,
         'F2 晶圆与掩模对准　0.96 nm (3σ)',
         'Ref009 Fig.3 占比 25.6% (本模型 DCO6 25.2% / SMO 23.0%)\nF2(f3, f4; P_WA, P_RA) · RSS 合成',
         'f2')
add_node('F3', X_L1, 615, W_L1, 108,
         'F3 光学柱与动态像差　0.66 nm (3σ)',
         'Ref009 Fig.3 占比 12.0% (本模型 DCO6 11.9% / SMO 10.9%)\nF3(f5, f6, f7; P_illum, P_LM) · RSS 合成',
         'f3')
add_node('F4', X_L1, 755, W_L1, 90,
         'F4 晶圆热与液浸流场　0.77 nm (3σ)',
         'Ref009 Fig.3 占比 16.0% (本模型 DCO6 16.2% / SMO 14.8%)\nF4(f8, f9; P_dose, P_seq, P_flow) · RSS 合成',
         'f4')
add_node('F5', X_L1, 875, W_L1, 114,
         'F5 掩模热与夹持　0.80 nm (3σ)',
         'Ref009 Fig.3 占比 18.0% (本模型 DCO6 17.5% / SMO 16.0%)\nF5(f10, f11, f12; P_RHC, P_ret) · RSS 合成',
         'f5')
add_node('F6', X_L1, 1020, W_L1, 84,
         'F6 晶圆夹持与台面接口　0.57 nm (3σ)',
         'Ref009 Fig.3 占比 8.4% (本模型 DCO6 8.9% / SMO 8.1%)\nF6(f13; P_clamp, P_scan) · 独立项',
         'f6')
add_node('F7', X_L1, 1135, W_L1, 90,
         'F7 双台卡盘差与量测底噪　0.59 nm (3σ)',
         'DCO → 双台 SMO 增量 (SMO 占比 8.7%)\nF7(f14, f15; P_chuck, P_eval) · RSS 合成',
         'f7')

# --- L2 Nodes (Execution Actions / Observable Intermediate Layer f_j(x; p)) ---
l2_specs = [
    ('m_l2_1', 115, 58, 'm1 跨机参考片多移位网格残差 (2.00 nm)', 'p_cal: 13×19 网格标定片 · 扣除镜头指纹 [N7]', 'm_match'),
    ('m_l2_2', 186, 58, 'm2 跨机静态畸变/奇像差/镜头热失配 (1.90 nm)', 'p_opt: 两台物镜无 K20 残差 + 跨机照明敏感度', 'm_match'),
    ('m_l2_3', 257, 58, 'm3 跨机吸盘指纹与 WAD/热环境失配 (1.65 nm)', 'p_fab: 50 μm 翘曲片 + 双机对准/RHC 差异', 'm_match'),

    ('f1',  360, 56, 'f1 曝光窗 WS–RS 相对扫描轨迹 MA (0.77 nm)', '两层 3σ · 单层 0.54 nm (平移 0.51 + Rz 0.20) · p_S: 0.70 m/s, 5.5 mm', 'f1'),
    ('f2',  426, 54, 'f2 WS-iHOPC 11 项场内轨迹执行残差 (0.38 nm)', '两层 ×1.20 · 单层场角 0.32 nm · p_C: K1–K2, K4–K6, K8,10,11,14,16,19', 'f1'),
    ('f3',  490, 56, 'f3 M-side 晶圆网格拟合与 M→E 基线 (0.68 nm)', '两层 3σ · 单层 0.48 nm (网格 0.40 + 短基线 0.27) · p_A: ≥20 标记', 'f2'),
    ('f4',  556, 56, 'f4 E-side 掩模空间像对准 RA 残差 (0.68 nm)', '两层 3σ · 单层 0.48 nm (7 点 PARIS / TIS 拟合) · p_R: 逐片重对准', 'f2'),
    ('f5',  622, 52, 'f5 Lens-iHOPC 8 项像场校正残差 (0.40 nm)', '两层 ×1.20 · 单层场角 0.33 nm · p_C: K3, K7, K9, K12–13, K15,17–18', 'f3'),
    ('f6',  684, 52, 'f6 Odd Zernike 跨照明像移残差 (0.42 nm)', '两层直接差分 ×1.00 · p_illum: 照明 A/B 切换 (Z5–Z64 30 项)', 'f3'),
    ('f7',  746, 52, 'f7 物镜热波前与声学/阻尼动态漂移 (0.32 nm)', '两层 3σ · 单层 0.23 nm · FlexWave 闭环 + 静音 RS/隔声罩', 'f3'),
    ('f8',  808, 56, 'f8 晶圆热变形与液浸蒸发冷缩残差 (0.71 nm)', '两层 3σ · 单层 0.50 nm (WT+蒸发 0.44 + WH 瞬态 0.24) · p_T: 剂量/场序', 'f4'),
    ('f9',  874, 50, 'f9 浸没水膜温场折射率畸变 (0.30 nm)', '两层 3σ · 单层 0.21 nm · p_flow: 供水流量与喷嘴流场', 'f4'),
    ('f10', 934, 50, 'f10 掩模热变形 RHC 补偿后残差 (0.55 nm)', '两层 3σ · 单层 0.39 nm · p_T: 透射率、剂量、扫描热史', 'f5'),
    ('f11', 994, 50, 'f11 掩模-物镜气隙湍流折射像移 (0.45 nm)', '两层 3σ · 单层 0.32 nm · 气幕温度梯度波动', 'f5'),
    ('f12', 1054, 50, 'f12 掩模重夹变形与折返微滑移 (0.37 nm)', '两层 3σ · 单层 0.26 nm (重夹 0.185 + 微滑移 0.185)', 'f5'),
    ('f13', 1114, 56, 'f13 晶圆重夹 IPD 与 WT–MB 回程滑移 (0.57 nm)', '两层 3σ · 单层 0.40 nm (重夹 0.34 + 折返滑移 0.22) · p_clamp', 'f6'),
    ('f14', 1180, 50, 'f14 双卡盘 A/B 换台网格与 TIS 匹配 ΔC2C (0.48 nm)', '双台 SMO 激活 (单卡盘 DCO 时置 0) · p_chuck: A/B 切换', 'f7'),
    ('f15', 1240, 50, 'f15 离线套刻后测底噪与未建模余项 (0.34 nm)', '两层 3σ · 含套刻量测 TMU 与短时未建模随机底噪 · p_eval', 'f7'),
]
for nid, y, h, title, sub, th in l2_specs:
    add_node(nid, X_L2, y, W_L2, h, title, sub, th)

# --- L3 Nodes (Bottom-Level Quantifiable Subsystem Specs x_i, Native Units) ---
# Highlight shared-source leaves (feeding >=2 L2/L1 nodes) in warm orange-bordered card!
l3_specs = [
    ('x01', 'x01 WS 6-DOF 运动与轨迹执行', 'X/Y ≤ 0.38/0.42 nm, Rz ≤ 14 nrad, Z ≤ 4.5 nm (@ 0.70 m/s); WS-iHOPC K4 ≤ 0.08 nm/cm', True),
    ('x02', 'x02 RS 6-DOF 运动重复性 (4× 掩模侧)', 'X/Y ≤ 1.12/1.28 nm, Rz ≤ 10 nrad (1:1 耦合), Z ≤ 24 nm (@ 2.80 m/s, 150 m/s²)', True),
    ('x03', 'x03 ENC 光栅编码器与栅格基准 ★共享源', 'WS 曝光窗 ≤ 0.14 nm (1 kHz 原始 0.22 nm); RS ≤ 0.40 nm; 栅格尺度稳定性 ~10 ppb', True),
    ('x04', 'x04 计量框架 MF 相对稳定性 ★共享源', '框架–物镜动 MA ≤ 0.18 nm / Rz ≤ 4.5 nrad; M→E 短期热漂 ≤ 0.20 nm', True),
    ('x05', 'x05 AA/SMASH 晶圆对准测头', '标准片单标记 静 ≤ 0.22 nm / 动 ≤ 0.40 nm (3σ); 多色偏振抗工艺非对称', False),
    ('x06', 'x06 TIS / PARIS 空间像与波前传感 ★共享源', 'TIS 单点 ≤ 0.40 nm; PARIS 7 点 ≤ 0.45 nm, 波前测噪 ≤ 0.15 nm RMS', True),
    ('x07', 'x07 物镜操纵器与 Lens Model ★共享源', 'K3 ≤ 0.11 nm/cm (硬件 Range ±15–25 ppm), 步长 ≤ 0.01 nm/cm, 滞后 ≤ 0.2 ms', True),
    ('x08', 'x08 物镜 Odd Fringe Zernike (Z5–Z64) ★共享源', 'Z7/Z8 ≤ 0.20 nm Fringe, 全 30 项 0.38 nm RMS; 静态高阶 NCE ≤ 1.2–1.6 nm', True),
    ('x09', 'x09 物镜热态控制与声学隔振结构', 'FlexWave 局部热控 + 阻尼物镜 + 静音 RS 气浮与声学屏蔽罩', False),
    ('x10', 'x10 WT 晶圆台温控与 WHFF 前馈边界', '高剂量首末场漂移 ≤ 5 mK; WT 表面均匀性 ≤ 6 mK PV; α_Si = 2.6 ppm/K', False),
    ('x11', 'x11 WH 传片模块出口温控重复性', 'WH 出口片间温差 ≤ 6 mK; 经热衰减后 M→E 残余等效温差 ≤ 0.62 mK', False),
    ('x12', 'x12 浸没供液水温、流场与残液控制 ★共享源', 'UPW 水温 ±2.5 mK (Ref021); 喷嘴流场/气帘控蒸发与压力脉动', True),
    ('x13', 'x13 掩模热控、RTS 测温与 RHC 模型', 'RHC 补偿后掩模等效温升 ≤ 38 mK (熔石英 α = 0.52 ppm/K, 0.009 nm/mK)', False),
    ('x14', 'x14 掩模–物镜气隙气流温控', '气隙光路温度梯度波动 ≤ 12 mK (空气折射率灵敏度 ~0.025 nm/mK)', False),
    ('x15', 'x15 RT 掩模夹持力学接口 (4× 掩模侧)', '重复装夹形变 ≤ 0.74 nm、150 m/s² 折返微滑移 ≤ 0.74 nm (晶圆等效各 0.185 nm)', False),
    ('x16', 'x16 WT 晶圆夹持与 WT–MB 接口 ★共享源', '重夹 IPD ≤ 0.34 nm; 折返微滑移 ≤ 0.22 nm; 瘤点平坦度 ≤ 6.5 nm (50 μm 翘曲)', True),
    ('x17', 'x17 双台卡盘网格标定与参考基准 ★共享源', 'A/B 卡盘相对网格与 TIS 标定差 ≤ 0.48 nm; 跨机多移位标定片 ≤ 2.0 nm', True),
    ('x18', 'x18 外部套刻量测工具与工艺本底', '同靶复测重复性 TMU (3σ) ≤ 0.30 nm; 未建模短时随机底噪 ≤ 0.16 nm', False),
]

y_l3_start = 115
h_l3 = 56
gap_l3 = 10
for idx, (nid, title, sub, is_shared) in enumerate(l3_specs):
    yy = y_l3_start + idx * (h_l3 + gap_l3)
    add_node(nid, X_L3, yy, W_L3, h_l3, title, sub, 'l3_sh' if is_shared else 'l3_bg')

# ---------------------------------------------------------------------------
# 3. Edges Specification: (src, dst, kind, label)
#    kind: 'main_rss' (solid dark), 'main_lin' (solid bold amber/purple),
#          'shared' (dashed orange-red DAG cross-edge)
# ---------------------------------------------------------------------------
edges = [
    # L0 -> L1
    ('L0_MMO', 'L0_MMO_M', 'main_lin', '+ 线性'),
    ('L0_MMO', 'M1', 'main_rss', 'RSS'),
    ('L0_MMO', 'M2', 'main_rss', 'RSS'),
    ('L0_MMO', 'M3', 'main_rss', 'RSS'),
    ('L0_MMO', 'L0_SMO', 'main_rss', 'RSS (含 SMO 随机底数 2.00 nm)'),

    ('L0_SMO', 'L0_SMO_M', 'main_lin', '+ 线性'),
    ('L0_SMO', 'F1', 'main_rss', 'RSS'),
    ('L0_SMO', 'F2', 'main_rss', 'RSS'),
    ('L0_SMO', 'F3', 'main_rss', 'RSS'),
    ('L0_SMO', 'F4', 'main_rss', 'RSS'),
    ('L0_SMO', 'F5', 'main_rss', 'RSS'),
    ('L0_SMO', 'F6', 'main_rss', 'RSS'),
    ('L0_SMO', 'F7', 'main_rss', 'RSS'),

    # L1 -> L2
    ('M1', 'm_l2_1', 'main_rss', ''),
    ('M2', 'm_l2_2', 'main_rss', ''),
    ('M3', 'm_l2_3', 'main_rss', ''),

    ('F1', 'f1', 'main_rss', 'RSS'),
    ('F1', 'f2', 'main_rss', 'RSS'),
    ('F2', 'f3', 'main_rss', 'RSS'),
    ('F2', 'f4', 'main_rss', 'RSS'),
    ('F3', 'f5', 'main_rss', 'RSS'),
    ('F3', 'f6', 'main_rss', 'RSS'),
    ('F3', 'f7', 'main_rss', 'RSS'),
    ('F4', 'f8', 'main_rss', 'RSS'),
    ('F4', 'f9', 'main_rss', 'RSS'),
    ('F5', 'f10', 'main_rss', 'RSS'),
    ('F5', 'f11', 'main_rss', 'RSS'),
    ('F5', 'f12', 'main_rss', 'RSS'),
    ('F6', 'f13', 'main_rss', ''),
    ('F7', 'f14', 'main_rss', 'RSS'),
    ('F7', 'f15', 'main_rss', 'RSS'),

    # L2 -> L3 (Primary solid edges)
    ('f1', 'x01', 'main_rss', ''),
    ('f1', 'x02', 'main_rss', ''),
    ('f1', 'x03', 'main_rss', ''),
    ('f1', 'x04', 'main_rss', ''),
    ('f2', 'x01', 'main_rss', ''),

    ('f3', 'x05', 'main_rss', ''),
    ('f4', 'x06', 'main_rss', ''),

    ('f5', 'x07', 'main_rss', ''),
    ('f6', 'x08', 'main_rss', ''),
    ('f7', 'x09', 'main_rss', ''),

    ('f8', 'x10', 'main_rss', ''),
    ('f8', 'x11', 'main_rss', ''),
    ('f8', 'x12', 'main_rss', ''),
    ('f9', 'x12', 'main_rss', ''),

    ('f10', 'x13', 'main_rss', ''),
    ('f11', 'x14', 'main_rss', ''),
    ('f12', 'x15', 'main_rss', ''),

    ('f13', 'x16', 'main_rss', ''),
    ('f14', 'x17', 'main_rss', ''),
    ('f15', 'x18', 'main_rss', ''),

    # MMO L2 -> L3 (Shared cross-machine physical leaves)
    ('m_l2_1', 'x03', 'shared', ''),
    ('m_l2_1', 'x17', 'shared', ''),
    ('m_l2_2', 'x07', 'shared', ''),
    ('m_l2_2', 'x08', 'shared', ''),
    ('m_l2_3', 'x16', 'shared', ''),
    ('m_l2_3', 'x17', 'shared', ''),

    # Ref-146 Fig. 3 style DAG shared-source cross-edges (L2 -> shared L3)
    ('f3', 'x03', 'shared', ''),   # ENC shared by WA grid
    ('f3', 'x04', 'shared', ''),   # MF shared by WA M->E baseline
    ('f3', 'x01', 'shared', ''),   # WS motion/stepping enters WA sampling
    ('f4', 'x02', 'shared', ''),   # RS positioning enters RA
    ('f4', 'x03', 'shared', ''),   # ENC shared by RA
    ('f4', 'x04', 'shared', ''),   # MF shared by RA
    ('f4', 'x12', 'shared', ''),   # Immersion flow perturbs TIS/RA (Ref164)
    ('f7', 'x06', 'shared', ''),   # PARIS wavefront feedback drives LH control
    ('f14', 'x06', 'shared', ''),  # TIS/PARIS defines chuck-to-chuck matching
]

# ---------------------------------------------------------------------------
# 4. Generate Editable draw.io XML (.drawio)
# ---------------------------------------------------------------------------
def build_drawio(out_path):
    mxfile = ET.Element('mxfile', host='app.diagrams.net', modified='2026-11-25T15:00:00.000Z',
                        agent='OV4-NXT1965Ci-Builder', version='24.7.0', type='device')
    diag = ET.SubElement(mxfile, 'diagram', id='nxt1965ci-l0-l3', name='NXT1965Ci_L0-L3套刻指标拆解图')
    model = ET.SubElement(diag, 'mxGraphModel', dx='1400', dy='900', grid='1', gridSize='10',
                          guides='1', tooltips='1', connect='1', arrows='1', fold='1', page='1',
                          pageScale='1', pageWidth=str(W_CANVAS), pageHeight=str(H_CANVAS),
                          math='0', shadow='0', background='#FFFFFF')
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', id='0')
    ET.SubElement(root, 'mxCell', id='1', parent='0')

    # Title Banner
    cid = 10
    def add_text_box(x, y, w, h, text, style):
        nonlocal cid
        cid += 1
        c = ET.SubElement(root, 'mxCell', id=f't{cid}', value=text, style=style, vertex='1', parent='1')
        ET.SubElement(c, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as': 'geometry'})

    add_text_box(40, 14, 1580, 44,
                 'ASML NXT:1965Ci 套刻指标 L0 → L1 → L2 → L3 全链路拆解与误差传递图（对标 Ref146 Fig.3 & Ref009 Fig.3）',
                 'text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=22;fontStyle=1;fontColor=#0F172A;fontFamily=Microsoft YaHei;')
    add_text_box(1640, 18, 600, 38,
                 '左→右：预算拆解（SMO ≤ 2.50 nm, MMO ≤ 4.50 nm）｜ 右→左：误差传递 x → f(x;p) → F(f,x;P) → L0',
                 'text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;fontSize=12;fontStyle=0;fontColor=#475569;fontFamily=Microsoft YaHei;')

    # Column Headers
    headers = [
        (X_L0, W_L0, 'L0 整机套刻指标', 'MMO ≤ 4.50 nm / SMO ≤ 2.50 nm\n合成：RSS(随机 3σ) + 线性(|Mean|)', '#1E293B'),
        (X_L1, W_L1, 'L1 子系统/功能域总体预算 F_k(f,x; P)', '按 Ref009 Fig.3 六大功能域 + C2C/跨机匹配\n含整机配方参数 P（扫速/照明/卡盘/APC）', '#1E3A8A'),
        (X_L2, W_L2, 'L2 执行动作 / 物理可观测中间层 f_j(x; p)', '可实测的像面/位置/热/夹持中间误差（两层 3σ）\n含子系统配方参数 p（标记/狭缝/场序/控制）', '#065F46'),
        (X_L3, W_L3, 'L3 底层可量化子系统指标 x_i（原生非套刻物理量纲）', '传感器噪声、伺服重复性、温控 mK、Zernike OPD、机械滑移等\n★ 橙框为多路径共享源（DAG 交叉连线，保留协方差且严禁重复计数）', '#9A3412'),
    ]
    for hx, hw, ht, hs, col in headers:
        add_text_box(hx, 64, hw, 42, f'<b>{ht}</b><br/><span style="font-size:10px;color:#475569">{hs.replace(chr(10), "<br/>")}</span>',
                     f'rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor={col};strokeWidth=1.5;align=left;spacingLeft=8;fontSize=12;fontColor={col};fontFamily=Microsoft YaHei;')

    # Nodes
    for nid, nd in nodes.items():
        val_html = f'<b>{nd["title"]}</b><br/><span style="font-size:10px;color:#334155">{nd["sub"].replace(chr(10), "<br/>")}</span>'
        sw = '2.2' if nid.startswith('L0_') else ('1.6' if nid.startswith(('F', 'M')) else '1.2')
        style = (f'rounded=1;arcSize=8;whiteSpace=wrap;html=1;fillColor={nd["fill"]};'
                 f'strokeColor={nd["stroke"]};strokeWidth={sw};align=left;verticalAlign=middle;'
                 f'spacingLeft=8;spacingRight=6;fontSize=11;fontColor=#0F172A;fontFamily=Microsoft YaHei;')
        c = ET.SubElement(root, 'mxCell', id=nid, value=val_html, style=style, vertex='1', parent='1')
        ET.SubElement(c, 'mxGeometry', x=str(nd['x']), y=str(nd['y']),
                      width=str(nd['w']), height=str(nd['h']), **{'as': 'geometry'})

    # Edges
    for idx, (src, dst, kind, lbl) in enumerate(edges):
        eid = f'e_{idx}_{src}_{dst}'
        if kind == 'main_lin':
            estyle = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B45309;strokeWidth=2.0;endArrow=classic;endFill=1;fontSize=10;fontColor=#92400E;fontFamily=Microsoft YaHei;'
        elif kind == 'shared':
            estyle = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#EA580C;strokeWidth=1.1;dashed=1;dashPattern=5 4;opacity=75;endArrow=open;endFill=0;fontSize=9;fontFamily=Microsoft YaHei;'
        else:
            estyle = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#334155;strokeWidth=1.4;endArrow=classic;endFill=1;fontSize=9;fontColor=#334155;fontFamily=Microsoft YaHei;'

        # Special vertical connections for L0_MMO -> L0_SMO and L0 -> L0_MEAN
        if src == 'L0_MMO' and dst == 'L0_MMO_M':
            estyle += 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'
        elif src == 'L0_SMO' and dst == 'L0_SMO_M':
            estyle += 'exitX=0.5;exitY=1;entryX=0.5;entryY=0;'
        elif src == 'L0_MMO' and dst == 'L0_SMO':
            estyle += 'exitX=0.15;exitY=1;entryX=0.15;entryY=0;'
        else:
            estyle += 'exitX=1;exitY=0.5;entryX=0;entryY=0.5;'

        e = ET.SubElement(root, 'mxCell', id=eid, value=lbl, style=estyle, edge='1', parent='1', source=src, target=dst)
        ET.SubElement(e, 'mxGeometry', relative='1', **{'as': 'geometry'})

    # Bottom Legend & Error Propagation Formalism Bar
    legend_html = (
        '<b>误差逐层传递数学架构与图例说明：</b>　'
        'L3 原生底层参数 x = (x₁, x₂, …, x₁₈)　→　'
        'L2 中间执行层 y_j = f_j(x; p_j)（含对准/扫描/热/校正配方 p）　→　'
        'L1 功能子系统预算 z_k = F_k(f, x; P_k)（按 Ref009 Fig.3 分域）　→　'
        'L0 整机套刻 = |Mean|（线性） + RSS(3σ 随机项)。<br/>'
        '<b>连线图例：</b>　'
        '<span style="color:#334155">━━▶ 实线箭头</span>：主预算分配 / 主传递路径（标 RSS 平方和开方）　｜　'
        '<span style="color:#B45309">━━▶ 粗棕箭头</span>：系统均值偏置线性叠加（+ |Mean|）　｜　'
        '<span style="color:#EA580C">┄┄▷ 橙色虚线</span>：跨分支共享物理源（如 ENC、MF、PARIS、浸没流场，类似 Ref146 Fig.3 虚线，整机汇总保留协方差、严禁重复计数）。'
    )
    add_text_box(40, 1345, 2190, 96, legend_html,
                 'rounded=1;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#94A3B8;strokeWidth=1.2;align=left;verticalAlign=middle;spacingLeft=12;spacingRight=12;fontSize=11;fontColor=#1E293B;fontFamily=Microsoft YaHei;')

    raw = ET.tostring(mxfile, encoding='utf-8')
    pretty = minidom.parseString(raw).toprettyxml(indent='  ', encoding='utf-8').decode('utf-8')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(pretty)
    print(f"Wrote draw.io XML: {out_path} ({os.path.getsize(out_path):,} bytes)")

# ---------------------------------------------------------------------------
# 5. Render Crisp High-DPI PNG Matching Exact Layout
# ---------------------------------------------------------------------------
def render_png(out_path):
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    dpi = 180
    fig = plt.figure(figsize=(W_CANVAS / 100.0, H_CANVAS / 100.0), dpi=dpi, facecolor='white')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W_CANVAS)
    ax.set_ylim(H_CANVAS, 0)  # Top-down coordinates matching draw.io!
    ax.axis('off')
    ax.set_facecolor('white')

    # Subtle column background bands
    bands = [
        (X_L0 - 12, W_L0 + 24, '#FAFAF9'),
        (X_L1 - 12, W_L1 + 24, '#F8FAFC'),
        (X_L2 - 12, W_L2 + 24, '#FAFAF9'),
        (X_L3 - 12, W_L3 + 24, '#F8FAFC'),
    ]
    for bx, bw, bcol in bands:
        ax.add_patch(Rectangle((bx, 108), bw, 1222, facecolor=bcol, edgecolor='#E2E8F0', linewidth=0.8, zorder=0))

    # Title Banner
    ax.text(40, 29, 'ASML NXT:1965Ci 套刻指标 L0 → L1 → L2 → L3 全链路拆解与误差传递图（对标 Ref146 Fig.3 & Ref009 Fig.3）',
            fontsize=17.5, fontweight='bold', color='#0F172A', va='center', ha='left')
    ax.text(2230, 31, '左→右：自顶向下预算拆解（SMO ≤ 2.50 nm, MMO ≤ 4.50 nm）  |  右→左：底层误差逐层传递  x → f(x; p) → F(f, x; P) → L0',
            fontsize=9.6, color='#475569', va='center', ha='right')

    # Column Header Cards
    headers = [
        (X_L0, W_L0, 'L0 整机套刻指标', 'MMO ≤ 4.50 / SMO ≤ 2.50 nm · RSS + 线性', '#1E293B'),
        (X_L1, W_L1, 'L1 子系统/功能域预算  F_k(f, x; P)', 'Ref009 Fig.3 六大功能域 + C2C/跨机匹配 · 含配方 P', '#1E3A8A'),
        (X_L2, W_L2, 'L2 执行动作 / 中间可观测层  f_j(x; p)', '可验收的像面/位置/热/夹持中间误差（两层 3σ）· 含配方 p', '#065F46'),
        (X_L3, W_L3, 'L3 底层可量化子系统指标  x_i（原生非套刻物理量纲）', '伺服重复性、ENC 噪声、温控 mK、Zernike OPD 等 · ★橙框为 DAG 共享源（保留协方差、防重复计数）', '#9A3412'),
    ]
    for hx, hw, ht, hs, col in headers:
        ax.add_patch(FancyBboxPatch((hx, 58), hw, 44, boxstyle='round,pad=0,rounding_size=6',
                                    facecolor='#FFFFFF', edgecolor=col, linewidth=1.6, zorder=2))
        ax.text(hx + 10, 73, ht, fontsize=10.5, fontweight='bold', color=col, va='center', ha='left', zorder=3)
        ax.text(hx + 10, 91, hs, fontsize=7.9, color='#475569', va='center', ha='left', zorder=3)

    # Helper to draw smooth cubic Bezier curve with arrowhead
    def draw_bezier(p0, p1, color, lw, ls='-', alpha=1.0, zorder=2, arrow_style='-|>', rad=0.0):
        x0, y0 = p0
        x1, y1 = p1
        dx = x1 - x0
        if abs(dx) > 20:
            c1 = (x0 + dx * 0.45, y0)
            c2 = (x1 - dx * 0.45, y1)
        else:
            c1 = (x0 - 38, y0 + (y1 - y0) * 0.3)
            c2 = (x1 - 38, y1 - (y1 - y0) * 0.3)
        verts = [p0, c1, c2, p1]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        path = Path(verts, codes)
        patch = FancyArrowPatch(path=path, arrowstyle=arrow_style, mutation_scale=11 if ls == '-' else 9,
                                color=color, linewidth=lw, linestyle=ls, alpha=alpha, zorder=zorder)
        ax.add_patch(patch)

    # Draw Edges FIRST (under boxes)
    # Collect outgoing/incoming anchor fan-outs slightly so overlapping endpoints separate cleanly
    for src, dst, kind, lbl in edges:
        ns, nd = nodes[src], nodes[dst]
        if src == 'L0_MMO' and dst == 'L0_MMO_M':
            p0 = (ns['x'] + ns['w'] * 0.55, ns['y'] + ns['h'])
            p1 = (nd['x'] + nd['w'] * 0.55, nd['y'])
            ax.annotate('', xy=p1, xytext=p0, arrowprops=dict(arrowstyle='-|>', color='#B45309', lw=2.0), zorder=2)
            ax.text(p0[0] + 6, (p0[1] + p1[1]) / 2, '+ 线性', fontsize=8.0, fontweight='bold', color='#92400E', va='center')
            continue
        if src == 'L0_SMO' and dst == 'L0_SMO_M':
            p0 = (ns['x'] + ns['w'] * 0.55, ns['y'] + ns['h'])
            p1 = (nd['x'] + nd['w'] * 0.55, nd['y'])
            ax.annotate('', xy=p1, xytext=p0, arrowprops=dict(arrowstyle='-|>', color='#B45309', lw=2.0), zorder=2)
            ax.text(p0[0] + 6, (p0[1] + p1[1]) / 2, '+ 线性', fontsize=8.0, fontweight='bold', color='#92400E', va='center')
            continue
        if src == 'L0_MMO' and dst == 'L0_SMO':
            # Clean outer-left routing avoiding L0_MMO_M completely
            x_out = X_L0 - 20
            y_src = ns['y'] + ns['h'] * 0.65
            y_dst = nd['y'] + nd['h'] * 0.25
            ax.plot([ns['x'], x_out, x_out], [y_src, y_src, y_dst], color='#5B21B6', lw=2.0, zorder=2)
            ax.annotate('', xy=(nd['x'], y_dst), xytext=(x_out, y_dst),
                        arrowprops=dict(arrowstyle='-|>', color='#5B21B6', lw=2.0), zorder=2)
            ax.text(X_L0 + 82, 495, 'MMO 经 RSS 继承\nSMO 3σ 底数 (2.00 nm)',
                    fontsize=8.2, fontweight='bold', color='#5B21B6', va='center', ha='center',
                    bbox=dict(boxstyle='round,pad=0.35', facecolor='#F5F3FF', edgecolor='#C4B5FD', lw=0.9), zorder=4)
            ax.annotate('', xy=(x_out + 2, 495), xytext=(X_L0 + 18, 495),
                        arrowprops=dict(arrowstyle='->', color='#7C3AED', lw=1.0, ls='--'), zorder=3)
            continue

        p0 = (ns['x'] + ns['w'], ns['y'] + ns['h'] / 2.0)
        p1 = (nd['x'], nd['y'] + nd['h'] / 2.0)
        if kind == 'shared':
            draw_bezier(p0, p1, color='#EA580C', lw=1.15, ls=(0, (4, 3)), alpha=0.68, zorder=1, arrow_style='->')
        else:
            # Slightly tint L0->L1 and L1->L2 edges by target stroke color for instant visual grouping
            ecol = nd['stroke'] if (src.startswith('L0_') or src.startswith(('F', 'M'))) else '#334155'
            draw_bezier(p0, p1, color=ecol, lw=1.55 if src.startswith('L0_') else 1.35, ls='-', alpha=0.88, zorder=2, arrow_style='-|>')

    # Add crisp RSS operator badges in the gaps (L0->L1 and L1->L2)
    op_badges = [
        (372, 225, 'MMO\nRSS', '#5B21B6', '#EDE9FE'),
        (372, 718, 'SMO\nRSS\n(7域)', '#B45309', '#FEF3C7'),
        (850, 428, 'RSS', '#3730A3', '#E0E7FF'),
        (850, 538, 'RSS', '#A16207', '#FEF9C3'),
        (850, 668, 'RSS', '#4D7C0F', '#ECFCCB'),
        (850, 800, 'RSS', '#0E7490', '#CFFAFE'),
        (850, 932, 'RSS', '#1D4ED8', '#DBEAFE'),
        (850, 1180, 'RSS', '#BE185D', '#FCE7F3'),
        (1394, 1085, 'f_j(x; p)\n映射矩阵\n与协方差', '#334155', '#F1F5F9'),
    ]
    for bx, by, btxt, fg, bg in op_badges:
        ax.text(bx, by, btxt, fontsize=7.6, fontweight='bold', color=fg, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.25', facecolor=bg, edgecolor=fg, lw=0.9), zorder=5)

    # Draw Nodes
    for nid, nd in nodes.items():
        x, y, w, h = nd['x'], nd['y'], nd['w'], nd['h']
        sw = 2.2 if nid.startswith('L0_') else (1.6 if nid.startswith(('F', 'M')) else 1.2)
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0,rounding_size=7',
                                    facecolor=nd['fill'], edgecolor=nd['stroke'], linewidth=sw, zorder=3))
        # Left accent stripe on L1 & L3 shared nodes
        if nid.startswith(('F', 'M', 'L0_')):
            ax.add_patch(Rectangle((x, y + 4), 5.5, h - 8, facecolor=nd['stroke'], edgecolor='none', zorder=4))
            tx = x + 13
        elif nd['fill'] == '#FFF7ED':
            ax.add_patch(Rectangle((x, y + 4), 4.5, h - 8, facecolor='#EA580C', edgecolor='none', zorder=4))
            tx = x + 12
        else:
            tx = x + 10

        lines_sub = nd['sub'].split('\n')
        if nid.startswith('L0_'):
            fs_t = 11.2 if nid in ('L0_MMO', 'L0_SMO') else 9.6
            fs_s = 8.4 if nid in ('L0_MMO', 'L0_SMO') else 7.8
            y_t = y + 22 if len(lines_sub) >= 2 else y + 19
            ax.text(tx, y_t, nd['title'], fontsize=fs_t, fontweight='bold', color='#0F172A', va='center', ha='left', zorder=4)
            for li, ln in enumerate(lines_sub):
                ax.text(tx, y_t + 22 + li * 18, ln, fontsize=fs_s, color='#334155', va='center', ha='left', zorder=4)
            if nd['badge']:
                ax.text(x + w - 8, y + h - 12, nd['badge'], fontsize=7.5, fontweight='bold', color=nd['stroke'],
                        ha='right', va='center', bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor=nd['stroke'], lw=0.8), zorder=5)
        elif nid.startswith(('F', 'M')):
            y_t = y + 20 if len(lines_sub) >= 2 else y + 19
            ax.text(tx, y_t, nd['title'], fontsize=9.8, fontweight='bold', color='#0F172A', va='center', ha='left', zorder=4)
            for li, ln in enumerate(lines_sub):
                ax.text(tx, y_t + 21 + li * 16.5, ln, fontsize=7.7, color='#334155', va='center', ha='left', zorder=4)
        elif nid.startswith(('f', 'm_l2')):
            ax.text(tx, y + 17, nd['title'], fontsize=8.8, fontweight='bold', color='#0F172A', va='center', ha='left', zorder=4)
            ax.text(tx, y + 37, nd['sub'], fontsize=7.4, color='#475569', va='center', ha='left', zorder=4)
        else:  # L3
            ax.text(tx, y + 18, nd['title'], fontsize=9.0, fontweight='bold', color='#0F172A', va='center', ha='left', zorder=4)
            ax.text(tx, y + 38, nd['sub'], fontsize=7.7, color='#334155', va='center', ha='left', zorder=4)

    # Bottom Legend & Methodology Footer Box
    ax.add_patch(FancyBboxPatch((40, 1344), 2190, 110, boxstyle='round,pad=0,rounding_size=8',
                                facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=1.3, zorder=3))
    ax.text(58, 1368,
            '误差逐层传递数学架构：   L3 原生底层参数 x = (x1, …, x18)  ──[ f_j(x; p_j) 含子系统配方 p ]──→  L2 可观测中间层 y_j  ──[ F_k(f, x; P_k) 含整机配方 P ]──→  L1 功能子系统预算 (Ref009 Fig.3)  ──[ RSS + 线性 |Mean| ]──→  L0 (SMO 2.35 ≤ 2.50 / MMO 4.29 ≤ 4.50 nm)',
            fontsize=8.7, fontweight='bold', color='#0F172A', va='center', ha='left', zorder=4)
    # Draw crisp vector legend swatches on line 2
    ax.text(58, 1397, '连线与核验规则：', fontsize=8.4, fontweight='bold', color='#1E293B', va='center', ha='left', zorder=4)
    ax.annotate('', xy=(225, 1397), xytext=(178, 1397), arrowprops=dict(arrowstyle='-|>', color='#334155', lw=1.6), zorder=4)
    ax.text(233, 1397, '实线箭头 = 主预算分配与主物理传递链（标 RSS 独立平方和开方）', fontsize=8.3, color='#334155', va='center', ha='left', zorder=4)
    ax.annotate('', xy=(720, 1397), xytext=(673, 1397), arrowprops=dict(arrowstyle='-|>', color='#B45309', lw=2.2), zorder=4)
    ax.text(728, 1397, '棕粗箭头 = 系统均值偏置线性叠加（+ |Mean|）', fontsize=8.3, color='#92400E', va='center', ha='left', zorder=4)
    ax.annotate('', xy=(1095, 1397), xytext=(1045, 1397), arrowprops=dict(arrowstyle='->', color='#EA580C', lw=1.4, ls=(0, (4, 3))), zorder=4)
    ax.text(1103, 1397, '橙色虚线 = 跨分支共享物理源（如 x01 WS、x03 ENC、x04 MF、x06 PARIS、x12 浸没流场，类似 Ref146 Fig.3，整机保留协方差、严禁重复计数）',
            fontsize=8.3, color='#9A3412', va='center', ha='left', zorder=4)
    ax.text(58, 1426,
            '口径一致性说明：   Ref009 Fig.3 堆叠柱状图（Stage 20.0% / Align 25.6% / Optics 12.0% / WaferTh 16.0% / Reticle 18.0% / WClamp 8.4%）以线性高度示意占比；本图将其映射为严格物理两层方差占比（DCO6 核验偏差 ≤ ±0.5%），并补入双台卡盘差 ΔC2C (0.48 nm) 闭环至 NXT:1965Ci 双台 SMO ≤ 2.50 nm。',
            fontsize=8.2, color='#475569', va='center', ha='left', zorder=4)

    fig.savefig(out_path, dpi=dpi, facecolor='white')
    plt.close(fig)
    print(f"Wrote PNG: {out_path} ({os.path.getsize(out_path):,} bytes)")

if __name__ == '__main__':
    img_dir = r'D:\work\OV4\outputs\images'
    os.makedirs(img_dir, exist_ok=True)
    drawio_path = os.path.join(img_dir, 'NXT1965Ci_SMO2.5_MMO4.5_L0-L3套刻指标拆解图_v1.drawio')
    png_path    = os.path.join(img_dir, 'NXT1965Ci_SMO2.5_MMO4.5_L0-L3套刻指标拆解图_v1.png')
    build_drawio(drawio_path)
    render_png(png_path)
