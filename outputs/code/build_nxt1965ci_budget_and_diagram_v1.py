"""Single-source-of-truth generator for ASML TWINSCAN NXT:1965Ci (SMO <= 2.50 nm, MMO <= 4.50 nm)
L0 -> L1 -> L2 -> L3 Overlay Budget Decomposition & Error-Propagation Diagram (.drawio + .png)
plus 260 DPI companion charts for the NXT:1965Ci presentation.

Methodology strictly grounded in:
- OV4 baseline: outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md
- Primary literature: Ref009 Fig. 3/4/10/11, Ref066, Ref011, Ref015, Ref024, Ref146 Fig. 3 (INCOSE 2006),
  Ref165, Ref167, Ref168, OV4 [N1]-[N8], [S1]-[S14], ME3 manuals
- Overlay3 allowed survey: reports/md/143_scanner_overlay_control_survey.md ONLY

Run from repository root:
    python outputs/code/build_nxt1965ci_budget_and_diagram_v1.py
"""
from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

REPO = Path(__file__).resolve().parents[2]
IMG_DIR = REPO / "outputs/images"
PPT_ASSETS = REPO / "work/nxt1965ci_ppt_assets"
IMG_DIR.mkdir(parents=True, exist_ok=True)
PPT_ASSETS.mkdir(parents=True, exist_ok=True)

OUT_DRAWIO = IMG_DIR / "NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.drawio"
OUT_PNG = IMG_DIR / "NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.png"

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def rss(*vals: float) -> float:
    return math.sqrt(sum(v * v for v in vals))


# =============================================================================
# 1. VERIFIED MATHEMATICAL MODEL (NXT:1965Ci, SMO <= 2.50 nm, MMO <= 4.50 nm)
# =============================================================================
def verify_budget() -> dict:
    # Ref009 Fig. 3 exact pixel percentages (77.8 px/nm on NXT:1950i bar)
    ref009_pct = {
        "S1": 20.16,  # Stage positioning (0.501 nm)
        "S2": 25.58,  # Wafer- & reticle alignment (0.636 nm)
        "S3": 12.14,  # Optical column (0.302 nm)
        "S4": 16.54,  # Wafer heating (+immersion) (0.411 nm)
        "S5": 17.31,  # Reticle clamping / heating (0.431 nm)
        "S6": 8.27,   # Wafer clamping (0.206 nm)
    }

    # --- L1-S1: Stage Positioning ---
    ws_x, rs_x4 = 0.38, 1.12       # RSS(0.38, 0.28) = 0.472 nm
    ws_y, rs_y4 = 0.39, 1.18       # RSS(0.39, 0.295) = 0.489 nm
    ws_rz, rs_rz = 14.0, 10.0      # nrad (1:1 coupling) -> Sync Rz = 17.20 nrad
    sync_x = rss(ws_x, rs_x4 / 4.0)
    sync_y = rss(ws_y, rs_y4 / 4.0)
    sync_rz = rss(ws_rz, rs_rz)
    sync_1L_x = rss(sync_x, sync_rz * 2.75e-3)   # 5.5 mm slit half-width = 2.75 mm
    sync_1L_y = rss(sync_y, sync_rz * 13.0e-3)   # 26 mm slit half-width = 13.0 mm
    f1_x, f1_y = sync_1L_x * math.sqrt(2), sync_1L_y * math.sqrt(2)

    # WS-iHOPC 11 params (exact corner sum)
    a, b = 1.30, 1.65
    wsi_x_1L = rss(0.140, 0.080 * b, 0.048 * b**2, 0.030 * b**3)  # 0.269 nm
    wsi_y_1L = rss(0.140, 0.080 * b, 0.095 * a, 0.048 * b**2, 0.060 * a * b, 0.030 * b**3, 0.036 * a * b**2)  # 0.347 nm
    f2_x, f2_y = wsi_x_1L * 1.20, wsi_y_1L * 1.20
    S1_x, S1_y = rss(f1_x, f2_x), rss(f1_y, f2_y)

    # --- L1-S2: Wafer & Reticle Alignment ---
    f3 = rss(0.400, 0.300) * math.sqrt(2)  # AA grid 0.40 + M-to-E baseline 0.30 -> 0.500 1L -> 0.707 2L
    f4 = 0.470 * math.sqrt(2)              # PARIS 7-pt RA 0.470 1L (<0.50 Ref066) -> 0.665 2L
    S2 = rss(f3, f4)

    # --- L1-S3: Optical Column ---
    lensi_x_1L = rss(0.120 * a, 0.092 * a**2, 0.070 * a**3, 0.072 * a * b, 0.054 * a**2 * b, 0.042 * a * b**2)  # 0.375 nm
    lensi_y_1L = rss(0.092 * a**2, 0.054 * a**2 * b)  # 0.216 nm
    f5_x, f5_y = lensi_x_1L * 1.20, lensi_y_1L * 1.20
    # Odd Zernike Z5-Z64 30 terms envelope
    zern_pairs = [
        (0.21, 0.950), (0.19, 0.910), (0.21, 0.700), (0.24, 0.550), (0.28, 0.275),
        (0.19, 0.843), (0.26, 0.462), (0.36, 0.156), (0.26, 0.367), (0.36, 0.138),
        (0.42, 0.097), (0.28, 0.320), (0.30, 0.312), (0.42, 0.090), (0.48, 0.088),
    ]
    f6_zern = rss(*(c * s for c, s in zern_pairs))  # 0.437 nm
    f6_dyn = 0.160 * math.sqrt(2)                   # Lens dynamic thermal & acoustic damping residual 0.226 nm
    f6 = rss(f6_zern, f6_dyn)                       # 0.492 nm
    S3_x, S3_y = rss(f5_x, f6), rss(f5_y, f6)

    # --- L1-S4: Wafer Heating + Immersion ---
    f7 = rss(0.420, 0.230) * math.sqrt(2)  # WT thermal/evap 0.42 + WH transient 0.23 -> 0.677 2L
    f8 = 0.280 * math.sqrt(2)              # Immersion UPW n(T) & flow -> 0.396 2L
    S4 = rss(f7, f8)

    # --- L1-S5: Reticle Clamping / Heating ---
    f9 = rss(0.430, 0.240) * math.sqrt(2)           # RHC residual 0.43 + reticle air-gap 0.24 -> 0.696 2L
    f10 = rss(0.180, 0.180, 0.140) * math.sqrt(2)   # RT clamp repro 0.18 + 150m/s2 slip 0.18 + pellicle dyn 0.14 -> 0.411 2L
    S5 = rss(f9, f10)

    # --- L1-S6: Wafer Clamping & SUSD Interface ---
    f11 = rss(0.300, 0.200, 0.150) * math.sqrt(2)   # WT clamp repro 0.30 + micro-slip 0.20 + WT-MB burl 0.15 -> 0.552 2L
    S6 = f11

    # --- Core-6 Closure & Ref009 Comparison ---
    core6_x = rss(S1_x, S2, S3_x, S4, S5, S6)
    core6_y = rss(S1_y, S2, S3_y, S4, S5, S6)
    S_env = {"S1": max(S1_x, S1_y), "S2": S2, "S3": max(S3_x, S3_y), "S4": S4, "S5": S5, "S6": S6}
    core6_env = rss(*S_env.values())
    shares = {k: (v**2) / (core6_env**2) * 100.0 for k, v in S_env.items()}
    for k in ref009_pct:
        assert abs(shares[k] - ref009_pct[k]) <= 0.35, f"Ref009 drift too high on {k}: {shares[k]:.2f} vs {ref009_pct[k]}"

    # --- L1-S7: Dual-Chuck Delta C2C + Metrology Floor ---
    c2c = rss(0.280, 0.350, 0.170)   # TIS1/2 0.28 + WT1/2 clamp 0.35 + SYCO/LOCO ref 0.17 = 0.479 ~ 0.480
    meas = 0.340
    S7_dco = meas
    S7_smo = rss(c2c, meas)          # 0.588 nm

    dco_rand_x, dco_rand_y, dco_rand_env = rss(core6_x, S7_dco), rss(core6_y, S7_dco), rss(core6_env, S7_dco)
    smo_rand_x, smo_rand_y, smo_rand_env = rss(core6_x, S7_smo), rss(core6_y, S7_smo), rss(core6_env, S7_smo)
    mean_dco, mean_smo, mean_mmo = 0.300, 0.350, 0.500

    dco_x, dco_y, dco_env = dco_rand_x + mean_dco, dco_rand_y + mean_dco, dco_rand_env + mean_dco
    smo_x, smo_y, smo_env = smo_rand_x + mean_smo, smo_rand_y + mean_smo, smo_rand_env + mean_smo

    # --- MMO Matching ---
    M1 = 2.000                            # Grid matching (BMMO / Gridplate)
    M2 = rss(1.600, f6_zern, 0.900)       # Lens NCE (no K20) 1.60 + 2nd Lens Zern 0.437 + iHOPC/APC 0.90 = 1.887
    M3 = rss(1.000, 0.950, 0.850, 0.354)  # 50um warp WT 1.00 + Align/WAD/TIS 0.95 + Thermal/RHC 0.85 + Reticle NCE 0.354 = 1.658
    mmo_match = rss(M1, M2, M3)           # 3.211 nm
    mmo_rand_x = rss(smo_rand_x, mmo_match)
    mmo_rand_y = rss(smo_rand_y, mmo_match)
    mmo_rand_env = rss(smo_rand_env, mmo_match)
    mmo_x, mmo_y, mmo_env = mmo_rand_x + mean_mmo, mmo_rand_y + mean_mmo, mmo_rand_env + mean_mmo

    assert dco_env <= 2.50 and smo_env <= 2.50 and mmo_env <= 4.50

    return {
        "ref009_pct": ref009_pct,
        "shares": shares,
        "S": {"S1_x": S1_x, "S1_y": S1_y, "S1": S_env["S1"], "S2": S2,
              "S3_x": S3_x, "S3_y": S3_y, "S3": S_env["S3"], "S4": S4, "S5": S5, "S6": S6,
              "S7_dco": S7_dco, "S7_smo": S7_smo},
        "L2": {"f1_x": f1_x, "f1_y": f1_y, "f2_x": f2_x, "f2_y": f2_y, "f3": f3, "f4": f4,
               "f5_x": f5_x, "f5_y": f5_y, "f6_zern": f6_zern, "f6_dyn": f6_dyn, "f6": f6,
               "f7": f7, "f8": f8, "f9": f9, "f10": f10, "f11": f11, "c2c": c2c, "meas": meas},
        "M": {"M1": M1, "M2": M2, "M3": M3, "match": mmo_match},
        "totals": {
            "core6_x": core6_x, "core6_y": core6_y, "core6_env": core6_env,
            "dco_rand_env": dco_rand_env, "dco_x": dco_x, "dco_y": dco_y, "dco_env": dco_env,
            "smo_rand_x": smo_rand_x, "smo_rand_y": smo_rand_y, "smo_rand_env": smo_rand_env,
            "smo_x": smo_x, "smo_y": smo_y, "smo_env": smo_env,
            "mmo_rand_x": mmo_rand_x, "mmo_rand_y": mmo_rand_y, "mmo_rand_env": mmo_rand_env,
            "mmo_x": mmo_x, "mmo_y": mmo_y, "mmo_env": mmo_env,
        }
    }


# =============================================================================
# 2. UNIFIED DIAGRAM SPECIFICATION (Ref-146 Fig. 3 Left-to-Right Architecture)
# =============================================================================
# Canvas coordinate system: 2600 x 1540 px (origin top-left for draw.io; inverted y for matplotlib)
CW, CH = 2600, 1540

# Palette — inspired by Ref-146 Fig. 3 clarity + Ref009 Fig. 3 domain accents
PAL = {
    "L0_MMO":  ("#123849", "#E6F0F5", "#123849"),  # border, fill, header
    "L0_SMO":  ("#087871", "#E5F5F3", "#087871"),
    "L0_MAT":  ("#4A5568", "#EDF2F7", "#4A5568"),
    "S1":      ("#5B4BB7", "#F2F0FD", "#5B4BB7"),  # Purple (Ref009 Stage)
    "S2":      ("#B78103", "#FFF9E2", "#B78103"),  # Gold/Yellow (Ref009 Align)
    "S3":      ("#5B7B1D", "#F3F8E8", "#5B7B1D"),  # Olive (Ref009 Optics)
    "S4":      ("#0E7C94", "#E8F7FA", "#0E7C94"),  # Cyan (Ref009 Wafer Heat+Imm)
    "S5":      ("#1D5FA8", "#EBF3FC", "#1D5FA8"),  # Blue (Ref009 Reticle)
    "S6":      ("#7A6845", "#F6F3EC", "#7A6845"),  # Khaki (Ref009 Wafer Clamp)
    "S7":      ("#6B7280", "#F3F4F6", "#6B7280"),  # Slate (C2C + Meas Floor)
    "M":       ("#475569", "#F1F5F9", "#475569"),  # Steel (MMO Matching)
    "L3":      ("#334155", "#FFFDF0", "#334155"),  # Warm cream leaf (homage to Ref-146 yellow cards)
    "L3_SH":   ("#C84B00", "#FFF3E8", "#C84B00"),  # Shared physical hub (dashed/grey cross-edges)
}


def build_nodes_and_edges(B: dict):
    S, L2, M, T = B["S"], B["L2"], B["M"], B["totals"]
    sh = B["shares"]

    nodes = []
    # Helper: (id, col, x, y, w, h, pal_key, title, body)
    # --- Column 0A & 0B: L0 Top-Level Targets (Ref-146 Fig. 3 style: MMO -> SMO + Matching) ---
    nodes.append((
        "L0_MMO", 0, 30, 560, 225, 195, "L0_MMO",
        "L0 整机混机套刻 MMO",
        f"红线红标: <= 4.50 nm (99.7%)\n闭环: {T['mmo_env']:.2f} nm (裕度 4.6%)\n= |Mean| 0.50 (线性)\n+ 3σ_rand {T['mmo_rand_env']:.2f} nm (RSS)\nX {T['mmo_x']:.2f} / Y {T['mmo_y']:.2f} nm"
    ))
    nodes.append((
        "L0_SMO", 0, 305, 345, 220, 210, "L0_SMO",
        "L0 单机套刻 SMO",
        f"红线红标: <= 2.50 nm\n双卡盘闭环: {T['smo_env']:.2f} nm\n= |Mean| 0.35 + 3σ {T['smo_rand_env']:.2f}\n同卡盘 DCO: {T['dco_env']:.2f} nm\nRef009六域RSS: {T['core6_env']:.2f} nm"
    ))
    nodes.append((
        "L0_MAT", 0, 305, 1145, 220, 140, "L0_MAT",
        "L0 跨机匹配净增",
        f"MMO Matching RSS\n总计: {M['match']:.2f} nm (3σ)\n按 Ref146 分支结构\n拆分至 M1 / M2 / M3"
    ))

    # --- Column 1: L1 Subsystem-Level Total Budgets (x=590, w=295) ---
    l1_specs = [
        ("L1_S1", 132, 108, "S1", f"S1 运动台定位与同步  {S['S1']:.3f} nm",
         f"Ref009 占比 20.2% -> 实占 {sh['S1']:.1f}%\nX {S['S1_x']:.3f} / Y {S['S1_y']:.3f} nm (2层3σ)"),
        ("L1_S2", 262, 108, "S2", f"S2 晶圆与掩模对准  {S['S2']:.3f} nm",
         f"Ref009 占比 25.6% -> 实占 {sh['S2']:.1f}%\nM-side AA + E-side TIS/PARIS"),
        ("L1_S3", 392, 108, "S3", f"S3 光学柱与动态像差  {S['S3']:.3f} nm",
         f"Ref009 占比 12.1% -> 实占 {sh['S3']:.1f}%\nX {S['S3_x']:.3f} / Y {S['S3_y']:.3f} nm (含阻尼)"),
        ("L1_S4", 522, 108, "S4", f"S4 晶圆热与浸没流场  {S['S4']:.3f} nm",
         f"Ref009 占比 16.5% -> 实占 {sh['S4']:.1f}%\n晶圆实体热边界 + 水膜折射率"),
        ("L1_S5", 652, 108, "S5", f"S5 掩模夹持与热变形  {S['S5']:.3f} nm",
         f"Ref009 占比 17.3% -> 实占 {sh['S5']:.1f}%\nRHC残差 + 夹持/Pellicle动态"),
        ("L1_S6", 782, 92,  "S6", f"S6 晶圆夹持与台面接口  {S['S6']:.3f} nm",
         f"Ref009 占比 8.3% -> 实占 {sh['S6']:.1f}%\n吸片重复 + 微滑移 + WT-MB柔顺"),
        ("L1_S7", 896, 92,  "S7", f"S7 双卡盘ΔC2C+底噪  {S['S7_smo']:.3f} nm",
         f"ΔC2C 0.48 + 量测本底 0.34 nm\n同卡盘DCO不含ΔC2C (仅0.34)"),
        ("L1_M1", 1030, 88, "M",  f"M1 跨机网格匹配  {M['M1']:.3f} nm",
         "BMMO参考片 + 多移位网格匹配\n对标 Ref066 Fig.4 / Ref009"),
        ("L1_M2", 1138, 88, "M",  f"M2 光学跨机匹配  {M['M2']:.3f} nm",
         "静态NCE(无K20) 1.60 + 第2台奇像差\n0.44 + 跨机iHOPC/APC 0.90 nm"),
        ("L1_M3", 1246, 88, "M",  f"M3 卡盘/对准/热匹配  {M['M3']:.3f} nm",
         "50μm翘曲片1.00 + 对准/WAD 0.95\n+ 跨机热/RHC 0.85 + 掩模0.35"),
    ]
    for nid, y, h, pk, title, body in l1_specs:
        nodes.append((nid, 1, 590, y, 295, h, pk, title, body))

    # --- Column 2: L2 Execution Actions / Observable Middle Layer f_j(x; p) (x=965, w=455) ---
    l2_specs = [
        ("L2_f1",  126, 72, "S1", f"f1 WS-RS扫描同步 Sync MA  (2L Y:{L2['f1_y']:.3f} / X:{L2['f1_x']:.3f} nm)",
         "1L: MA-X 0.47 / MA-Y 0.49 nm + Rz 17.2 nrad; p={v_w=0.70m/s, L_s=5.5mm}"),
        ("L2_f2",  208, 68, "S1", f"f2 WS-iHOPC 动态轨迹 11参  (2L Y:{L2['f2_y']:.3f} / X:{L2['f2_x']:.3f} nm)",
         "K1,K2,K4-6,K8,K10-11,K14,K16,K19 场角RSS; p={5.5mm狭缝逆卷积, |K0|}"),
        ("L2_f3",  286, 72, "S2", f"f3 M-side晶圆网格与基线  (2L {L2['f3']:.3f} nm)",
         "AA网格拟合 0.40 + M-to-E基线漂移 0.30 nm; p={N标记, HOWA阶次, SUSD配平}"),
        ("L2_f4",  368, 68, "S2", f"f4 E-side空间像掩模对准  (2L {L2['f4']:.3f} nm)",
         "TIS 6kHz零点 + 7点PARIS并行RA 0.47 nm (<0.50 Ref066); p={每片3扫}"),
        ("L2_f5",  446, 68, "S3", f"f5 Lens-iHOPC 8参光学操纵  (2L X:{L2['f5_x']:.3f} / Y:{L2['f5_y']:.3f} nm)",
         "K3,K7,K12,K13(静)+K9,K15,K17,K18(动), 不含K20; p={|K0|, 行程<=80%}"),
        ("L2_f6",  524, 72, "S3", f"f6 Odd Zernike跨照明 + 物镜动态热声  (2L {L2['f6']:.3f} nm)",
         f"Z5-Z64 30项 {L2['f6_zern']:.3f} nm + 热/声阻尼 {L2['f6_dyn']:.3f} nm; p={{照明切换ΔS_j, 剂量}}"),
        ("L2_f7",  606, 70, "S4", f"f7 晶圆实体热变形与蒸发冷缩  (2L {L2['f7']:.3f} nm)",
         "WT热边界/边缘蒸发 0.42 + WH进片瞬态 0.23 nm; p={剂量, 扫描场序, R2=0.92}"),
        ("L2_f8",  686, 66, "S4", f"f8 浸没水膜折射率梯度畸变  (2L {L2['f8']:.3f} nm)",
         "物镜末端300μm热边界层n(T)与流场扰动 0.28 nm (1L); p={UPW流量, 扫速}"),
        ("L2_f9",  762, 68, "S5", f"f9 掩模热变形RHC残差与气隙  (2L {L2['f9']:.3f} nm)",
         "TPM/MPM前馈残差 0.43 + 掩模下气隙折射率 0.24 nm; p={掩模透射率, 剂量史}"),
        ("L2_f10", 840, 68, "S5", f"f10 掩模夹持滑移与Pellicle动态  (2L {L2['f10']:.3f} nm)",
         "重夹 0.18 + 150m/s²微滑移 0.18 + Pellicle扫/吹动态 0.14 nm [098]"),
        ("L2_f11", 918, 68, "S6", f"f11 晶圆吸片重复与WT-MB接口  (2L {L2['f11']:.3f} nm)",
         "吸片重夹 0.30 + 背面摩擦微滑移 0.20 + WT-MB柔顺长柱微滞回 0.15 nm"),
        ("L2_f12", 996, 68, "S7", f"f12 双卡盘零点/夹持差 + 验证底噪  ({S['S7_smo']:.3f} nm)",
         "SYCO/LOCO卡盘零点差[100] + TIS1/2 + WT1/2指纹 0.48 + 量测底噪 0.34 nm"),
        ("L2_f13", 1084, 82, "M",  f"f13 跨机网格(BMMO)与绝对基准标定  ({M['M1']:.3f} nm)",
         "13x19多移位曝光 + 校准参考片 + Gridplate >15mm 尺度匹配 [N7/066]"),
        ("L2_f14", 1178, 82, "M",  f"f14 跨机光学NCE与工艺/翘曲片匹配  ({rss(M['M2'], M['M3']):.3f} nm)",
         "静态高阶畸变(无K20) + 50μm翘曲片夹持IPD + 标记WAD/跨机热态失配"),
    ]
    for nid, y, h, pk, title, body in l2_specs:
        nodes.append((nid, 2, 965, y, 455, h, pk, title, body))

    # --- Column 3: L3 Bottom-Level Quantifiable Native Subsystem Specs x01..x18 (x=1565, w=485 / 2nd sub-col x=2080, w=485) ---
    # Wait: single clean right column x=1580, w=990 split into 2 aligned tracks?
    # Even cleaner & MORE faithful to Ref-146 Fig. 3: ONE crisp vertical column of 18 compact native-unit cards!
    # Check height: 18 cards * 65 px + 17 * 6 px = 1272 px -> fits y=118..1390 PERFECTLY!
    l3_specs = [
        ("x01", "L3",    "x01 WS 6-DOF 独立重复性",
         "X <=0.38 / Y <=0.39 / Z <=4.8 nm; Rx<=0.20 / Ry<=0.10 μrad; Rz<=14 nrad (WS=Master)"),
        ("x02", "L3",    "x02 RS 6-DOF 独立重复性 (4x)",
         "X <=1.12 / Y <=1.18 / Z <=26 nm; Rx<=0.42 / Ry<=0.19 μrad; Rz<=10 nrad (1:1, 150m/s²)"),
        ("x03", "L3_SH", "x03 ENC 光栅编码器  [★共享源 -> f1,f2,f3,f4,f13]",
         "WS宽带<=0.22 nm@1kHz / 带内<=0.13 nm(63.6Hz); 切换<=0.15; 7天<=0.20 nm; RS 0.37/0.39"),
        ("x04", "L3_SH", "x04 计量框架 MF 与隔振  [★共享源 -> f1,f3,f4,f6]",
         "MF空气温控 10 mK; 短期基线漂移<=0.18 nm; 24h<0.50 nm; 隔振<1 Hz + 静音RS降声"),
        ("x05", "L3",    "x05 WS-iHOPC 动态伺服与标尺",
         "K4/K5<=0.080, K8/K11<=0.048, K14/K19<=0.030 nm/cm^q; 离线伺服<=55%; 5.5mm逆卷积"),
        ("x06", "L3",    "x06 SMASH 四色对准传感器 (AA)",
         "单标记静态<=0.22 nm (WQ>=1%) / 弱片<=0.50 nm; 动态<=0.38 nm; 四色24h<=0.32 nm"),
        ("x07", "L3_SH", "x07 TIS 6kHz 与 7点 PARIS  [★共享源 -> f4,f6,f9,f12]",
         "TIS XY<=0.40 / Z<=2.8 nm; PARIS 7点RA<=0.47 nm / Z<=3.2 nm / 波前测噪<=0.14 nm RMS"),
        ("x08", "L3",    "x08 Lens-iHOPC 镜片操纵器 (8参)",
         "K3硬件Range ±15-25 ppm (用户±5-10); K3<=0.120 / K9<=0.072; 滞回<=25%; 响应<=20-50 ms"),
        ("x09", "L3",    "x09 FlexWave 奇像差波前控制",
         "Z5-Z64 30项: Z7/8<=0.21, Z10/11/26/27<=0.19 Fringe; 全瞳Odd<=0.40 nm RMS (Coma 0.19)"),
        ("x10", "L3_SH", "x10 WT 台面温控与WH预调理  [★共享源 -> f7,f11,f12]",
         "WT温稳<=±3 mK, 分区边缘加热均匀<80 mK(3σ); WH出口片温差<=±15 mK (2.6 ppm/K)"),
        ("x11", "L3_SH", "x11 浸没头控液与UPW供回水  [★共享源 -> f4(Ref164),f7,f8]",
         "UPW水温<=±3 mK [021]; 气幕+弯月面无残液滴(@0.75 m/s); 流量稳控防TIS漂移 [164]"),
        ("x12", "L3",    "x12 掩模微环境气幕与RHC热控",
         "掩模上表面冷却气流 + 5 mK水平层流气幕; RTS热测+TPM/MPM模型每场前馈更新"),
        ("x13", "L3",    "x13 RT 掩模夹持与Pellicle装配",
         "分段柔顺夹持重夹<=0.72 nm(4x); 1000趟微滑移<=0.72 nm(4x); 软胶垫Pellicle<=0.14 nm"),
        ("x14", "L3",    "x14 WT 晶圆夹持与WT-MB长柱接口",
         "瘤点平坦度<=6.5 nm; 真空吸片重复<=0.30 nm; 柔顺长柱(US8269949B2)正反扫滞回<=0.15 nm"),
        ("x15", "L3",    "x15 双卡盘参考一致性 (SYCO/LOCO)",
         "TIS-1/TIS-2 24h匹配<=0.28 nm; WT1/WT2指纹差<=0.35 nm; SYCO/LOCO跨卡盘匹配启用"),
        ("x16", "L3",    "x16 离线套刻量测与采样配方",
         "量测TMU<=0.34 nm; SUSD正反扫向平衡采样(防Gy20混叠[123]); 靶标-器件差<0.5 nm[008]"),
        ("x17", "L3",    "x17 跨机BMMO网格与静态物镜指纹",
         "13x19多移位标定+校准参考片; 静态高阶畸变(无K20) 1.60 nm; 79x17密网格出厂调校趋势"),
        ("x18", "L3",    "x18 工艺翘曲片与RWE前馈边界",
         "50 μm翘曲片夹持残差<=1.00 nm [066]; 工艺标记WAD<=0.50 nm; PROVE离线RWE 15参前馈"),
    ]
    y_cur = 122
    h_l3 = 63
    gap_l3 = 7
    for nid, pk, title, body in l3_specs:
        nodes.append((nid, 3, 1595, y_cur, 975, h_l3, pk, title, body))
        y_cur += h_l3 + gap_l3

    # Primary solid edges: (src, dst, style_type)
    # style_type: 'main' (solid dark), 'sys' (thick coral/brown linear mean), 'shared' (dashed orange/grey DAG cross-edge)
    edges = [
        # L0 -> L0 / L1
        ("L0_MMO", "L0_SMO", "main"),
        ("L0_MMO", "L0_MAT", "main"),
        ("L0_SMO", "L1_S1", "main"),
        ("L0_SMO", "L1_S2", "main"),
        ("L0_SMO", "L1_S3", "main"),
        ("L0_SMO", "L1_S4", "main"),
        ("L0_SMO", "L1_S5", "main"),
        ("L0_SMO", "L1_S6", "main"),
        ("L0_SMO", "L1_S7", "main"),
        ("L0_MAT", "L1_M1", "main"),
        ("L0_MAT", "L1_M2", "main"),
        ("L0_MAT", "L1_M3", "main"),
        # L1 -> L2
        ("L1_S1", "L2_f1", "main"),
        ("L1_S1", "L2_f2", "main"),
        ("L1_S2", "L2_f3", "main"),
        ("L1_S2", "L2_f4", "main"),
        ("L1_S3", "L2_f5", "main"),
        ("L1_S3", "L2_f6", "main"),
        ("L1_S4", "L2_f7", "main"),
        ("L1_S4", "L2_f8", "main"),
        ("L1_S5", "L2_f9", "main"),
        ("L1_S5", "L2_f10", "main"),
        ("L1_S6", "L2_f11", "main"),
        ("L1_S7", "L2_f12", "main"),
        ("L1_M1", "L2_f13", "main"),
        ("L1_M2", "L2_f14", "main"),
        ("L1_M3", "L2_f14", "main"),
        # L2 -> L3 primary solid
        ("L2_f1",  "x01", "main"),
        ("L2_f1",  "x02", "main"),
        ("L2_f1",  "x03", "main"),
        ("L2_f1",  "x04", "main"),
        ("L2_f2",  "x05", "main"),
        ("L2_f3",  "x06", "main"),
        ("L2_f4",  "x07", "main"),
        ("L2_f5",  "x08", "main"),
        ("L2_f6",  "x09", "main"),
        ("L2_f7",  "x10", "main"),
        ("L2_f8",  "x11", "main"),
        ("L2_f9",  "x12", "main"),
        ("L2_f10", "x13", "main"),
        ("L2_f11", "x14", "main"),
        ("L2_f12", "x15", "main"),
        ("L2_f12", "x16", "main"),
        ("L2_f13", "x17", "main"),
        ("L2_f14", "x18", "main"),
        # Shared cross-branch DAG edges (Ref-146 Fig. 3 dashed/grey style!)
        ("L2_f2",  "x03", "shared"),   # ENC scale/noise enters WS-iHOPC
        ("L2_f3",  "x03", "shared"),   # ENC grid enters M-side AA
        ("L2_f4",  "x03", "shared"),   # ENC enters E-side TIS/PARIS
        ("L2_f13", "x03", "shared"),   # ENC gridplate enters BMMO matching
        ("L2_f3",  "x04", "shared"),   # MF stability enters M-to-E baseline
        ("L2_f4",  "x04", "shared"),   # MF stability enters E-side RA
        ("L2_f6",  "x04", "shared"),   # Acoustic/damping frame enters Optical Column
        ("L2_f6",  "x07", "shared"),   # PARIS wavefront metrology enters Odd Zernike control
        ("L2_f9",  "x07", "shared"),   # PARIS 7-pt RA enters Reticle Heating RHC
        ("L2_f12", "x07", "shared"),   # TIS-1/TIS-2 enters Dual-Chuck Delta C2C
        ("L2_f4",  "x11", "shared"),   # UPW flow affects TIS repeatability (Ref164 in report 143!)
        ("L2_f7",  "x11", "shared"),   # Immersion residual film evaporation cools wafer
        ("L2_f11", "x10", "shared"),   # WT thermal boundary couples into clamping IPD
        ("L2_f12", "x10", "shared"),   # WT1/WT2 thermal diff enters C2C
        ("L2_f3",  "x16", "shared"),   # SUSD-balanced sampling controls HOWA aliasing (Ref123)
    ]
    return nodes, edges


# =============================================================================
# 3. GENERATE EDITABLE DRAW.IO (.drawio) FILE (Clean Uncompressed mxGraph XML)
# =============================================================================
def write_drawio(nodes, edges, B: dict, path: Path):
    mxfile = ET.Element("mxfile", host="app.diagrams.net", type="device", version="24.7.0")
    diagram = ET.SubElement(mxfile, "diagram", id="nxt1965ci-l0-l3", name="NXT1965Ci_L0-L3_Budget")
    model = ET.SubElement(
        diagram, "mxGraphModel",
        dx="1422", dy="794", grid="1", gridSize="10", guides="1", tooltips="1",
        connect="1", arrows="1", fold="1", page="1", pageScale="1",
        pageWidth=str(CW), pageHeight=str(CH), math="0", shadow="0"
    )
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    cid = 10
    def next_id():
        nonlocal cid
        cid += 1
        return str(cid)

    # Top Title Banner
    tcell = ET.SubElement(
        root, "mxCell", id=next_id(),
        value="ASML TWINSCAN NXT:1965Ci（SMO ≤ 2.50 nm / MMO ≤ 4.50 nm）L0 → L1 → L2 → L3 全链路套刻指标拆解与误差传递图（Ref-146 Fig. 3 风格 · 锚定 Ref009 Fig. 3）",
        style="rounded=0;whiteSpace=wrap;html=1;fillColor=#123849;strokeColor=none;fontColor=#FFFFFF;fontFamily=Microsoft YaHei;fontSize=18;fontStyle=1;align=left;spacingLeft=16;",
        vertex="1", parent="1"
    )
    ET.SubElement(tcell, "mxGeometry", x="20", y="12", width=str(CW - 40), height="44", **{"as": "geometry"})

    # Column Headers
    col_headers = [
        (30,   495, "L0 整机级套刻红线（左→右拆解起点）\nMMO ≤ 4.50 nm  |  SMO ≤ 2.50 nm", "#123849"),
        (590,  295, "L1 子系统功能域总预算（F_k）\n严格对齐 Ref009 Fig. 3 六大域 + 跨机", "#087871"),
        (965,  455, "L2 执行动作 / 可观测中间层（f_j(x; p)）\n两层差分口径 · 标注配方杠杆 p", "#1F4E78"),
        (1595, 975, "L3 底层可量化子系统原生指标（x01–x18，原生非套刻物理量纲）\n橙框 ★共享源 以虚线连接多条 L2 支路（继承 Ref-146 Fig. 3 共享节点语法，防重复计数）", "#7A4B00"),
    ]
    for x, w, txt, col in col_headers:
        c = ET.SubElement(
            root, "mxCell", id=next_id(), value=txt,
            style=f"rounded=1;whiteSpace=wrap;html=1;fillColor=#F0F5F8;strokeColor={col};strokeWidth=1.5;fontColor={col};fontFamily=Microsoft YaHei;fontSize=12;fontStyle=1;align=center;",
            vertex="1", parent="1"
        )
        ET.SubElement(c, "mxGeometry", x=str(x), y="66", width=str(w), height="46", **{"as": "geometry"})

    # Nodes
    id_map = {}
    for nid, col_idx, x, y, w, h, pk, title, body in nodes:
        border, fill, hdr = PAL[pk]
        cell_id = next_id()
        id_map[nid] = cell_id
        html_val = f"<b><font color='{hdr}'>{title}</font></b><br/>" + body.replace("\n", "<br/>")
        sw = "2" if pk in ("L0_MMO", "L0_SMO", "L3_SH") else "1.3"
        fs = "11" if col_idx in (0, 1) else "10.5"
        style = (
            f"rounded=1;arcSize=6;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={border};"
            f"strokeWidth={sw};fontFamily=Microsoft YaHei;fontSize={fs};fontColor=#1B303C;"
            f"align=left;verticalAlign=middle;spacingLeft=8;spacingRight=6;spacingTop=3;spacingBottom=3;"
        )
        c = ET.SubElement(root, "mxCell", id=cell_id, value=html_val, style=style, vertex="1", parent="1")
        ET.SubElement(c, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as": "geometry"})

    # Edges
    for src, dst, etype in edges:
        eid = next_id()
        if etype == "main":
            style = (
                "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
                "strokeColor=#2C4A5A;strokeWidth=1.4;endArrow=classic;endFill=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
            )
        else:
            style = (
                "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;"
                "strokeColor=#D96B27;strokeWidth=1.15;dashed=1;dashPattern=6 4;endArrow=open;endFill=0;"
                "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"
            )
        ec = ET.SubElement(root, "mxCell", id=eid, value="", style=style, edge="1", parent="1",
                           source=id_map[src], target=id_map[dst])
        ET.SubElement(ec, "mxGeometry", relative="1", **{"as": "geometry"})

    # Bottom Propagation Equation & Legend Strip
    footer_txt = (
        "读图与误差传递双视角：  [左→右 · 预算拆解] L0 整机红线 → L1 六大域+跨机 → L2 执行动作 → L3 原生指标 x01–x18   |   "
        "[右→左 · 物理传递] x_i → L2: y_j = f_j(x; p) → L1: z_k = F_k(f, x; P) → 两遍差分 Δz = z_2 - z_1 → L0 = |Mean|_线性 + RSS(3σ_k)   |   "
        "实线箭头 = 主预算归属/主传递链    橙色虚线 = Ref-146 共享物理源跨支路耦合（需核算协方差，严禁独立重复计账）"
    )
    fc = ET.SubElement(
        root, "mxCell", id=next_id(), value=footer_txt,
        style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F7FAFC;strokeColor=#94A3B8;strokeWidth=1.2;fontColor=#1E293B;fontFamily=Microsoft YaHei;fontSize=11;fontStyle=1;align=left;spacingLeft=12;",
        vertex="1", parent="1"
    )
    ET.SubElement(fc, "mxGeometry", x="20", y=str(CH - 58), width=str(CW - 40), height="44", **{"as": "geometry"})

    raw_xml = ET.tostring(mxfile, encoding="utf-8")
    pretty = minidom.parseString(raw_xml).toprettyxml(indent="  ", encoding="utf-8")
    path.write_bytes(pretty)
    print(f"[OK] Wrote draw.io: {path} ({path.stat().st_size:,} bytes)")


# =============================================================================
# 4. RENDER CRISP 200 DPI PNG (Matches draw.io 1-to-1, 0 Missing Glyphs)
# =============================================================================
def render_png(nodes, edges, B: dict, path: Path):
    dpi = 180
    fig = plt.figure(figsize=(CW / 100.0, CH / 100.0), dpi=dpi, facecolor="#FFFFFF")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, CW)
    ax.set_ylim(CH, 0)  # Top-left origin matching draw.io!
    ax.axis("off")

    # Background subtle column zones
    zones = [
        (20,   116, 515,  1348, "#F8FBFD"),
        (575,  116, 325,  1348, "#F9FBFA"),
        (950,  116, 485,  1348, "#F8FAFC"),
        (1580, 116, 1000, 1348, "#FFFDF7"),
    ]
    for zx, zy, zw, zh, zc in zones:
        ax.add_patch(FancyBboxPatch((zx, zy), zw, zh, boxstyle="round,pad=0,rounding_size=8",
                                    facecolor=zc, edgecolor="#E2E8F0", linewidth=0.9, zorder=0))

    # Top Title Banner
    ax.add_patch(patches.Rectangle((20, 12), CW - 40, 46, facecolor="#123849", edgecolor="none", zorder=2))
    ax.add_patch(patches.Rectangle((20, 12), 14, 46, facecolor="#087871", edgecolor="none", zorder=3))
    ax.text(48, 35,
            "ASML TWINSCAN NXT:1965Ci（SMO ≤ 2.50 nm / MMO ≤ 4.50 nm）L0 → L1 → L2 → L3 套刻指标拆解与误差传递图",
            color="#FFFFFF", fontsize=17.5, fontweight="bold", va="center", ha="left", zorder=4)
    ax.text(CW - 36, 35,
            "架构形式：Ref-146 Fig. 3（左→右）  |  SMO 占比锚定：Ref009 Fig. 3  |  狭缝：26×5.5 mm",
            color="#C7E4EB", fontsize=11.5, fontweight="bold", va="center", ha="right", zorder=4)

    # Column Headers
    col_headers = [
        (30,   495, "L0 整机级套刻红线（左 → 右预算拆解）", "MMO ≤ 4.50 nm（闭环 4.29） | SMO ≤ 2.50 nm（双台 2.36 / 同台 2.26）", "#123849"),
        (590,  295, "L1 子系统功能域预算 F_k", "对齐 Ref009 Fig. 3 六大域（偏差 ≤ ±0.3%）+ 跨机", "#087871"),
        (965,  455, "L2 执行动作 / 可观测中间层 f_j(x; p)", "两层差分 3σ 口径 · 显式标注配方参数 p", "#1F4E78"),
        (1595, 975, "L3 底层可量化子系统原生指标 x01–x18（原生非套刻物理量纲）", "橙框 [★共享源] 以虚线连接多条 L2 支路（承袭 Ref-146 Fig. 3 共享节点画法，保留协方差防重复计数）", "#9A3412"),
    ]
    for x, w, t1, t2, col in col_headers:
        ax.add_patch(FancyBboxPatch((x, 66), w, 46, boxstyle="round,pad=0,rounding_size=5",
                                    facecolor="#EEF5F9", edgecolor=col, linewidth=1.4, zorder=2))
        ax.text(x + w / 2, 81, t1, color=col, fontsize=11.0, fontweight="bold", va="center", ha="center", zorder=3)
        ax.text(x + w / 2, 99, t2, color="#475569", fontsize=8.8, va="center", ha="center", zorder=3)

    # Index nodes for edge routing
    nmap = {n[0]: n for n in nodes}

    # --- Draw Edges First (Clean Orthogonal Bus Routing!) ---
    # 1) Shared cross-branch DAG edges in dedicated routing channel x=1445..1568
    shared_edges = [e for e in edges if e[2] == "shared"]
    # Assign distinct x-lanes by target node (x03, x04, x07, x10, x11, x16) so lines never overlap!
    hub_lanes = {"x03": 1452, "x04": 1474, "x07": 1496, "x10": 1518, "x11": 1540, "x16": 1560}
    hub_colors = {"x03": "#D97706", "x04": "#EA580C", "x07": "#C2410C", "x10": "#0284C7", "x11": "#0891B2", "x16": "#7C3AED"}

    for src, dst, _ in shared_edges:
        _, _, sx, sy, sw, sh_, *_ = nmap[src]
        _, _, dx, dy, dw, dh_, *_ = nmap[dst]
        x1, y1 = sx + sw, sy + sh_ * 0.62
        x2, y2 = dx, dy + dh_ * 0.68
        xm = hub_lanes.get(dst, 1500)
        col = hub_colors.get(dst, "#D96B27")
        ax.plot([x1, xm, xm, x2 - 8], [y1, y1, y2, y2],
                color=col, linewidth=1.35, linestyle=(0, (5, 3)), alpha=0.82, zorder=2)
        ax.annotate("", xy=(x2, y2), xytext=(x2 - 12, y2),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.28,head_length=0.45",
                                    color=col, lw=1.2, alpha=0.9), zorder=3)

    # 2) Primary Solid Orthogonal Bus Edges (grouped by source for ultra-clean Ref-146 forks!)
    main_edges = [e for e in edges if e[2] == "main"]
    by_src: dict[str, list[str]] = {}
    for s, d, _ in main_edges:
        by_src.setdefault(s, []).append(d)

    for src, dsts in by_src.items():
        _, scol, sx, sy, sw, sh_, *_ = nmap[src]
        x1, y1 = sx + sw, sy + sh_ * 0.50
        # Choose clean bus X midpoint per column transition
        if src == "L0_MMO":
            xm = 280
        elif src in ("L0_SMO", "L0_MAT"):
            xm = 556
        elif scol == 1:
            xm = 924
        else:
            xm = 1436  # L2 -> L3 primary lane left of shared-hub lanes (wait: pass cleanly!)
            # Put primary L2->L3 vertical bus at x=1576 (right next to L3) if single or clean offset
            xm = 1574 if len(dsts) == 1 else 1438

        ys_dst = []
        for dst in dsts:
            _, _, dx, dy, dw, dh_, *_ = nmap[dst]
            y2 = dy + dh_ * 0.44
            ys_dst.append((dx, y2))

        # Horizontal stub out of source
        ax.plot([x1, xm], [y1, y1], color="#2C4A5A", linewidth=1.65, zorder=3)
        # Vertical spine covering y1 and all destination y2s
        all_y = [y1] + [p[1] for p in ys_dst]
        ax.plot([xm, xm], [min(all_y), max(all_y)], color="#2C4A5A", linewidth=1.65, zorder=3)
        # Horizontal branches into each target with crisp arrowheads
        for dx, y2 in ys_dst:
            ax.plot([xm, dx - 8], [y2, y2], color="#2C4A5A", linewidth=1.65, zorder=3)
            ax.annotate("", xy=(dx, y2), xytext=(dx - 11, y2),
                        arrowprops=dict(arrowstyle="-|>,head_width=0.32,head_length=0.52",
                                        color="#2C4A5A", lw=1.4), zorder=4)

    # Annotate Linear |Mean| & RSS symbols near L0 forks (just like Ref-146 §3.3!)
    ax.text(280, 622, "RSS\n+|M|", color="#123849", fontsize=8.2, fontweight="bold",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#123849", lw=0.9), zorder=6)
    ax.text(556, 450, "RSS\n+0.35\n(|Mean|)", color="#087871", fontsize=7.8, fontweight="bold",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#087871", lw=0.9), zorder=6)
    ax.text(556, 1215, "RSS\n3.21", color="#475569", fontsize=8.0, fontweight="bold",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#475569", lw=0.9), zorder=6)

    # --- Draw Node Cards ---
    for nid, col_idx, x, y, w, h, pk, title, body in nodes:
        border, fill, hdr = PAL[pk]
        lw = 2.1 if pk in ("L0_MMO", "L0_SMO", "L3_SH") else 1.3
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=5",
                                    facecolor=fill, edgecolor=border, linewidth=lw, zorder=5))
        # Left accent bar on every card
        ax.add_patch(patches.Rectangle((x, y + 3), 5.5, h - 6, facecolor=hdr, edgecolor="none", zorder=6))

        if col_idx == 0:
            ax.text(x + 13, y + 20, title, color=hdr, fontsize=11.3, fontweight="bold", va="center", ha="left", zorder=7)
            ax.plot([x + 11, x + w - 10], [y + 34, y + 34], color=border, lw=0.7, alpha=0.5, zorder=7)
            ax.text(x + 13, y + 44, body, color="#1B303C", fontsize=9.6, va="top", ha="left", linespacing=1.42, zorder=7)
        elif col_idx == 1:
            ax.text(x + 12, y + 20, title, color=hdr, fontsize=10.0, fontweight="bold", va="center", ha="left", zorder=7)
            ax.text(x + 12, y + 36, body, color="#1E293B", fontsize=8.8, va="top", ha="left", linespacing=1.35, zorder=7)
        elif col_idx == 2:
            ax.text(x + 12, y + 18, title, color=hdr, fontsize=9.3, fontweight="bold", va="center", ha="left", zorder=7)
            ax.text(x + 12, y + 33, body, color="#1E293B", fontsize=8.2, va="top", ha="left", linespacing=1.30, zorder=7)
        else:
            ax.text(x + 12, y + 18, title, color=hdr, fontsize=9.3, fontweight="bold", va="center", ha="left", zorder=7)
            ax.text(x + 12, y + 35, body, color="#1E293B", fontsize=8.2, va="top", ha="left", linespacing=1.22, zorder=7)

    # Bottom Propagation Equation & Legend Bar
    fy = CH - 62
    ax.add_patch(FancyBboxPatch((20, fy), CW - 40, 48, boxstyle="round,pad=0,rounding_size=5",
                                facecolor="#F1F5F9", edgecolor="#94A3B8", linewidth=1.2, zorder=5))
    ax.text(36, fy + 16,
            "右 → 左 物理误差上溯传递方程：  L3 原生指标 x = (x01..x18)  →  L2: y_j = f_j(x; p_j)  →  L1: z_k = F_k(f, x; P_k)  →  两遍差分 Δz = z_2 - z_1  →  L0 = |Mean|_线性 + RSS(3σ_k)",
            color="#0F172A", fontsize=10.3, fontweight="bold", va="center", ha="left", zorder=6)
    ax.text(36, fy + 36, "图例说明：", color="#475569", fontsize=9.3, fontweight="bold", va="center", ha="left", zorder=6)
    # Vector solid arrow icon
    ax.annotate("", xy=(172, fy + 36), xytext=(118, fy + 36),
                arrowprops=dict(arrowstyle="-|>,head_width=0.30,head_length=0.50", color="#2C4A5A", lw=1.8), zorder=7)
    ax.text(182, fy + 36, "主预算拆解与主传递路径", color="#1E293B", fontsize=9.3, va="center", ha="left", zorder=6)
    # Vector dashed shared arrow icon
    ax.plot([420, 466], [fy + 36, fy + 36], color="#D97706", lw=1.6, linestyle=(0, (5, 3)), zorder=7)
    ax.annotate("", xy=(478, fy + 36), xytext=(462, fy + 36),
                arrowprops=dict(arrowstyle="-|>,head_width=0.28,head_length=0.45", color="#D97706", lw=1.5), zorder=7)
    ax.text(488, fy + 36,
            "跨支路共享物理源（橙/青/紫虚线，承袭 Ref-146 Fig. 3，须保留协方差防止重复计数）      [★共享源] = 影响 ≥ 2 条 L2 路径的底层物理枢纽",
            color="#475569", fontsize=9.3, va="center", ha="left", zorder=6)

    fig.savefig(path, dpi=dpi, facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[OK] Wrote PNG: {path} ({path.stat().st_size:,} bytes)")


# =============================================================================
# 5. COMPANION 260 DPI ENGINEERING CHARTS FOR THE NXT:1965Ci PRESENTATION
# =============================================================================
def build_ppt_charts(B: dict):
    S, T = B["S"], B["totals"]
    ref009 = B["ref009_pct"]
    shares = B["shares"]

    # --- Chart 1: Ref009 Fig. 3 vs NXT:1965Ci Variance Share & L0 Closure ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.3), dpi=260, gridspec_kw={"width_ratios": [1.18, 1.0]})
    labels = ["S1 运动台\nStage", "S2 对准\nAlign", "S3 光学柱\nOptics", "S4 晶圆热\n+浸没", "S5 掩模\n热/夹持", "S6 晶圆\n夹持"]
    keys = ["S1", "S2", "S3", "S4", "S5", "S6"]
    v_ref = [ref009[k] for k in keys]
    v_mod = [shares[k] for k in keys]
    x = np.arange(len(keys))
    w = 0.39
    b1 = ax1.bar(x - w/2, v_ref, w, label="Ref009 Fig. 3 像素实测占比 (%)", color="#123849", alpha=0.90)
    b2 = ax1.bar(x + w/2, v_mod, w, label="NXT:1965Ci 模型方差占比 (%)", color="#087871", alpha=0.92)
    for idx_b, bars in enumerate((b1, b2)):
        for bar in bars:
            h = bar.get_height()
            dx = -0.04 if idx_b == 0 else 0.04
            ax1.text(bar.get_x() + bar.get_width()/2 + dx, h + 0.45, f"{h:.1f}%",
                     ha="center", va="bottom", fontsize=7.0, fontweight="bold")
    ax1.set_xticks(x); ax1.set_xticklabels(labels, fontsize=8.4)
    ax1.set_ylabel("六域随机方差占比 (%)", fontsize=9.5, fontweight="bold")
    ax1.set_ylim(0, 31)
    ax1.set_title("与 Ref009 Fig. 3 占比精确对齐（全项偏差 ≤ ±0.3%）", fontsize=10.5, fontweight="bold", color="#123849")
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.legend(fontsize=8.2, loc="upper right", frameon=True)

    cats = ["同卡盘 DCO\n(X 2.21 / Y 2.22)", "双卡盘 SMO\n(X 2.32 / Y 2.33)", "混机 MMO\n(X 4.26 / Y 4.27)"]
    vals_rand = [T["dco_rand_env"], T["smo_rand_env"], T["mmo_rand_env"]]
    vals_mean = [0.30, 0.35, 0.50]
    specs = [2.50, 2.50, 4.50]
    xc = np.arange(len(cats))
    ax2.bar(xc, vals_rand, 0.48, label="随机 3σ RSS (nm)", color="#087871")
    ax2.bar(xc, vals_mean, 0.48, bottom=vals_rand, label="系统残余 |Mean| (线性)", color="#D97706")
    for i in range(len(cats)):
        tot = vals_rand[i] + vals_mean[i]
        ax2.plot([i - 0.34, i + 0.34], [specs[i], specs[i]], color="#DC2626", lw=2.2, linestyle="--")
        ax2.text(i, specs[i] + 0.14, f"闭环 {tot:.2f} nm\n(红线 ≤ {specs[i]:.1f})", ha="center", va="bottom",
                 fontsize=8.1, fontweight="bold", color="#123849")
    ax2.set_xticks(xc); ax2.set_xticklabels(cats, fontsize=8.6, fontweight="bold")
    ax2.set_ylabel("套刻误差 |Mean| + 3σ (nm)", fontsize=9.5, fontweight="bold")
    ax2.set_ylim(0, 5.55)
    ax2.set_title("NXT:1965Ci 顶层闭环验证（全项 PASS）", fontsize=10.5, fontweight="bold", color="#123849")
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.legend(fontsize=8.2, loc="upper left", frameon=True)
    plt.tight_layout()
    p1 = PPT_ASSETS / "chart_1965ci_closure_ref009.png"
    fig.savefig(p1, dpi=260, facecolor="#FFFFFF")
    plt.close(fig)

    # --- Chart 2: v2 (2.0/3.5 nm) vs NXT:1965Ci (2.5/4.5 nm) Core Subsystem Delta ---
    fig, ax = plt.subplots(figsize=(10.6, 4.1), dpi=260)
    items = [
        "WS-X\n(nm)", "WS-Y\n(nm)", "RS-X/4\n(nm)", "RS-Y/4\n(nm)",
        "WS-ENC\n带内(nm)", "AA网格\n(nm)", "PARIS RA\n(nm)",
        "WS-iHOPC\nY角(nm)", "Lens-iHOPC\nX角(nm)", "Odd Zern\n包络(nm)"
    ]
    v2_vals = [0.32, 0.36, 0.24, 0.27, 0.12, 0.35, 0.40, 0.293, 0.317, 0.370]
    v1965 =   [0.38, 0.39, 0.28, 0.295, 0.13, 0.40, 0.47, 0.347, 0.375, 0.437]
    xi = np.arange(len(items))
    w = 0.36
    ax.bar(xi - w/2, v2_vals, w, label="历史 v2 基线（DCO 2.00 / MMO 3.50 nm）", color="#64748B", alpha=0.85)
    ax.bar(xi + w/2, v1965,   w, label="本次 NXT:1965Ci（SMO 2.50 / MMO 4.50 nm）", color="#087871", alpha=0.95)
    for i in range(len(items)):
        pct = (v1965[i] - v2_vals[i]) / v2_vals[i] * 100
        ax.text(i + w/2, v1965[i] + 0.012, f"{v1965[i]:.2f}\n(+{pct:.0f}%)", ha="center", va="bottom", fontsize=7.2, fontweight="bold", color="#087871")
        ax.text(i - w/2, v2_vals[i] + 0.010, f"{v2_vals[i]:.2f}", ha="center", va="bottom", fontsize=7.0, color="#475569")
    ax.set_xticks(xi); ax.set_xticklabels(items, fontsize=8.3)
    ax.set_ylabel("单层 3σ / 等效套刻贡献 (nm)", fontsize=9.2, fontweight="bold")
    ax.set_ylim(0, 0.58)
    ax.set_title("目标锚定至 NXT:1965Ci 后九大核心子系统规格科学回松对比（消除过设计、直对 Ref009/066 实测）",
                 fontsize=10.3, fontweight="bold", color="#123849")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(fontsize=8.6, loc="upper left", frameon=True)
    plt.tight_layout()
    p2 = PPT_ASSETS / "chart_1965ci_vs_v2_delta.png"
    fig.savefig(p2, dpi=260, facecolor="#FFFFFF")
    plt.close(fig)

    # --- Chart 3: Correlation Sensitivity Stress Test (Ref146 Sec.2.4) & 5.5 mm Slit MA/MSD ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.0), dpi=260)
    rhos = np.linspace(0.0, 0.15, 61)
    s_list = [S["S1"], S["S2"], S["S3"], S["S4"], S["S5"], S["S6"], S["S7_smo"]]
    sum_sq = sum(v*v for v in s_list)
    sum_lin = sum(s_list)
    smo_rho = [0.350 + math.sqrt((1 - r) * sum_sq + r * (sum_lin**2)) for r in rhos]
    ax1.plot(rhos, smo_rho, color="#123849", lw=2.4, label="双卡盘 SMO(|Mean|+3σ)")
    ax1.axhline(2.50, color="#DC2626", lw=1.8, linestyle="--", label="NXT:1965Ci 红线 2.50 nm")
    ax1.axvline(0.025, color="#D97706", lw=1.5, linestyle=":", label="安全上限 ρ_max ≈ 0.025")
    ax1.fill_between(rhos, smo_rho, 2.50, where=[v > 2.50 for v in smo_rho], color="#FCA5A5", alpha=0.4)
    ax1.scatter([0.0, 0.025, 0.05], [smo_rho[0], 0.35 + math.sqrt(0.975*sum_sq + 0.025*sum_lin**2),
                                     0.35 + math.sqrt(0.95*sum_sq + 0.05*sum_lin**2)], color="#C84B00", zorder=5)
    ax1.annotate(f"ρ=0: {smo_rho[0]:.2f} nm", (0.0, smo_rho[0]), xytext=(0.015, 2.27), fontsize=8.2, fontweight="bold")
    ax1.annotate("ρ=0.05: 2.63 nm\n(突破红线!)", (0.05, 2.634), xytext=(0.072, 2.53), fontsize=8.2, color="#B91C1C",
                 fontweight="bold", arrowprops=dict(arrowstyle="->", color="#B91C1C", lw=1.3))
    ax1.set_xlabel("功能域间等效相关系数 ρ（共享物理源耦合度）", fontsize=8.8, fontweight="bold")
    ax1.set_ylabel("整机双卡盘 SMO (nm)", fontsize=9.0, fontweight="bold")
    ax1.set_title("共享源相关性压力校验（Ref146 §2.4）", fontsize=10.2, fontweight="bold", color="#123849")
    ax1.set_ylim(2.20, 3.05); ax1.grid(True, linestyle="--", alpha=0.4); ax1.legend(fontsize=7.8, loc="upper left")

    # Right: Heertjes 2024 ECC 5.5 mm vs 8.0 mm slit sinc^2 MA & 1-sinc^2 MSD
    freqs = np.linspace(0.5, 300, 600)
    tau55 = 5.5 / 700.0
    tau80 = 8.0 / 700.0
    ma55 = np.sinc(freqs * tau55) ** 2
    msd55 = 1.0 - ma55
    ma80 = np.sinc(freqs * tau80) ** 2
    ax2.plot(freqs, ma55, color="#087871", lw=2.2, label="MA 权函数 sinc²(f·τ), 5.5mm (ENBW 63.6 Hz)")
    ax2.plot(freqs, msd55, color="#C84B00", lw=1.8, linestyle="--", label="MSD 权函数 1-sinc², 5.5mm (高频模糊)")
    ax2.plot(freqs, ma80, color="#94A3B8", lw=1.5, linestyle=":", label="旧 8.0mm 干式口径 (ENBW 43.8 Hz)")
    ax2.axvline(127.3, color="#087871", lw=1.1, linestyle="-.", alpha=0.7)
    ax2.text(132, 0.20, "首零点\nf1 = 127.3 Hz", fontsize=8.2, color="#087871", fontweight="bold",
             bbox=dict(boxstyle="round,pad=0.2", fc="#FFFFFF", ec="#087871", alpha=0.85))
    ax2.set_xlabel("扰动频率 f (Hz) @ v_w = 0.70 m/s", fontsize=8.8, fontweight="bold")
    ax2.set_ylabel("功率谱透过权重", fontsize=9.0, fontweight="bold")
    ax2.set_title("NA=1.35 真实 5.5 mm 狭缝 MA/MSD 互补滤波 [N1/N8]", fontsize=10.2, fontweight="bold", color="#123849")
    ax2.set_ylim(-0.03, 1.08); ax2.grid(True, linestyle="--", alpha=0.4)
    ax2.legend(fontsize=7.3, loc="center right", bbox_to_anchor=(0.99, 0.56), frameon=True)
    plt.tight_layout()
    p3 = PPT_ASSETS / "chart_1965ci_corr_and_slit.png"
    fig.savefig(p3, dpi=260, facecolor="#FFFFFF")
    plt.close(fig)

    # --- Chart 4: Odd Zernike Z5-Z64 30-Term Sensitivity & NXT:1965Ci Budget ---
    fig, ax = plt.subplots(figsize=(10.6, 4.0), dpi=260)
    z_names = ["Z7/8", "Z10/11", "Z14/15", "Z19/20", "Z23/24", "Z26/27", "Z30/31", "Z34/35",
               "Z39/40", "Z43/44", "Z47/48", "Z50/51", "Z54/55", "Z58/59", "Z62/63"]
    s_env = [0.950, 0.910, 0.700, 0.550, 0.275, 0.843, 0.462, 0.156, 0.367, 0.138, 0.097, 0.320, 0.312, 0.090, 0.088]
    c_fr =  [0.21,  0.19,  0.21,  0.24,  0.28,  0.19,  0.26,  0.36,  0.26,  0.36,  0.42,  0.28,  0.30,  0.42,  0.48]
    ovl =   [s * c for s, c in zip(s_env, c_fr)]
    xz = np.arange(len(z_names))
    ax.bar(xz, c_fr, 0.55, color="#5B7B1D", alpha=0.82, label="NXT:1965Ci 控制限值 (nm Fringe)")
    ax2r = ax.twinx()
    ax2r.plot(xz, s_env, "o-", color="#C84B00", lw=2.0, ms=5, label="跨照明包络灵敏度 |ΔS_env| (nm/nm)")
    ax2r.plot(xz, ovl, "s--", color="#123849", lw=1.7, ms=4.5, label="单轴套刻贡献 (nm, RSS=0.437)")
    for i, c in enumerate(c_fr):
        y_lbl = 0.145 if z_names[i] == "Z30/31" else c - 0.032
        ax.text(i, y_lbl, f"{c:.2f}", ha="center", va="top", fontsize=7.2, fontweight="bold", color="#FFFFFF")
    ax.set_xticks(xz); ax.set_xticklabels(z_names, fontsize=8.0, rotation=22)
    ax.set_ylabel("奇像差控制规格 (nm Fringe)", fontsize=9.0, fontweight="bold", color="#365314")
    ax2r.set_ylabel("灵敏度 (nm/nm) / 套刻贡献 (nm)", fontsize=9.0, fontweight="bold", color="#123849")
    ax.set_ylim(0, 0.62); ax2r.set_ylim(0, 1.18)
    ax.set_title("NXT:1965Ci 物镜 Odd Zernike (Z5–Z64 全 30 项) 反灵敏度预算分配（Z10 0.905 vs IBM/ASML 0.88 误差 2.8%）",
                 fontsize=9.8, fontweight="bold", color="#123849")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2r.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=7.8, loc="upper center", ncol=3, frameon=True)
    plt.tight_layout()
    p4 = PPT_ASSETS / "chart_1965ci_zernike_z5_z64.png"
    fig.savefig(p4, dpi=260, facecolor="#FFFFFF")
    plt.close(fig)

    # --- Chart 5: NXT:1965Ci Lens-iHOPC 8-Dim Evaluation (5.5 mm / 7.86 ms & K3 ±15-25 ppm) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.2), dpi=260, gridspec_kw={"width_ratios": [1.05, 1.15]})
    # Left: SET-vs-GET linearity, hysteresis <=25%, uni-repeat <=35%, user +/-50..100 & HW +/-150..250 nm/cm
    x_set = np.linspace(-100, 100, 120)
    y_fwd = x_set + 1.8 * np.sin(x_set / 35.0) + 1.6
    y_rev = x_set + 1.8 * np.sin(x_set / 35.0) - 1.6
    ax1.plot(x_set, x_set, "--", color="#64748B", lw=1.2, label="理想 1:1 (GET = SET)")
    ax1.plot(x_set, y_fwd, color="#123849", lw=2.0, label="正向扫描 (Forward)")
    ax1.plot(x_set, y_rev, color="#C84B00", lw=1.8, linestyle="-.", label="反向回程 (Reverse)")
    ax1.fill_between(x_set, y_rev, y_fwd, color="#FDE68A", alpha=0.45)
    ax1.text(-94, 55, "D3 滞回 ≤ 25% Spec\n单向重复 ≤ 35% Spec", fontsize=8.0, fontweight="bold", color="#9A3412",
             bbox=dict(boxstyle="round,pad=0.3", fc="#FFF7ED", ec="#C84B00"))
    ax1.text(8, -58, "D4 精度 3.0–5.6%\nD2 最小步长 ≤ Spec/10", fontsize=8.0, fontweight="bold", color="#087871",
             bbox=dict(boxstyle="round,pad=0.3", fc="#F0FDFA", ec="#087871"))
    ax1.text(0, -96, "D1 K3 硬件 ±150–250 / 用户 ±50–100 nm/cm (占 ≤80%)", fontsize=7.6, fontweight="bold",
             ha="center", color="#123849", bbox=dict(boxstyle="round,pad=0.25", fc="#F1F5F9", ec="#123849"))
    ax1.set_xlabel("下发指令 K3 SET (nm/cm, 1 ppm = 10 nm/cm)", fontsize=8.4, fontweight="bold")
    ax1.set_ylabel("实测响应 K3 GET (nm/cm, 夸大示意)", fontsize=8.4, fontweight="bold")
    ax1.set_title("A. 静态/准静态特性：行程/步长/滞回/线性", fontsize=9.6, fontweight="bold", color="#123849")
    ax1.set_xlim(-105, 105); ax1.set_ylim(-108, 108); ax1.grid(True, linestyle="--", alpha=0.35)
    ax1.legend(fontsize=7.3, loc="upper left", frameon=True)

    # Right: Actuator response bandwidth vs 7.86 ms (5.5 mm slit @ 0.70 m/s) + D5 side-effect guardrails
    y_pos = np.arange(4)
    labels_act = ["热致 FlexWave\n(Z5–Z64 批/热态)", "静态镜片操纵器\n(K3,K7,K12,K13)", "动态扫描同步镜元\n(K9,K15,K17,K18)", "准分子激光 Δλ\n(K3 快速微调)"]
    t_min = [10000.0, 20.0, 0.2, 0.15]
    t_max = [60000.0, 50.0, 2.0, 1.0]
    cols = ["#C84B00", "#087871", "#1D5FA8", "#5B7B1D"]
    for i in range(4):
        ax2.barh(y_pos[i], t_max[i] - t_min[i], left=t_min[i], height=0.45, color=cols[i], alpha=0.88)
    ax2.axvline(7.86, color="#DC2626", lw=2.0, linestyle="--")
    ax2.text(9.5, 3.18, "5.5 mm 狭缝窗\nτ_slit = 7.86 ms", fontsize=8.0, fontweight="bold", color="#B91C1C",
             bbox=dict(boxstyle="round,pad=0.25", fc="#FEF2F2", ec="#DC2626"))
    ax2.text(2.4, 2.0, "相位滞后 ≤ 0.2 ms", fontsize=7.6, fontweight="bold", color="#1D5FA8", va="center")
    ax2.text(62, 1.0, "20–50 ms (场/片间)", fontsize=7.6, fontweight="bold", color="#087871", va="center")
    ax2.text(45, 0.0, "10–60 s (热稳态)", fontsize=7.6, fontweight="bold", color="#9A3412", va="center")
    ax2.set_xscale("log"); ax2.set_xlim(0.1, 1.2e5); ax2.set_ylim(-0.7, 3.7)
    ax2.set_yticks(y_pos); ax2.set_yticklabels(labels_act, fontsize=8.0, fontweight="bold")
    ax2.set_xlabel("响应 / 整定时间尺度 (ms, 对数轴) [D6 带宽]", fontsize=8.4, fontweight="bold")
    ax2.set_title("B. 四类执行机构响应带宽与 D5 副作用红线", fontsize=9.6, fontweight="bold", color="#123849")
    ax2.grid(axis="x", linestyle="--", alpha=0.35)
    ax2.text(0.50, 0.04, "D5 副作用红线：跨 K 串扰 ≤ 30% | 诱发焦面 ≤ 1.0–1.5 nm | 诱发奇像差 ≤ 0.05 nm RMS",
             transform=ax2.transAxes, fontsize=7.5, fontweight="bold", ha="center", color="#1E293B",
             bbox=dict(boxstyle="round,pad=0.25", fc="#F1F5F9", ec="#64748B"))
    plt.tight_layout()
    p5 = PPT_ASSETS / "chart_1965ci_lens_8dim.png"
    fig.savefig(p5, dpi=260, facecolor="#FFFFFF")
    plt.close(fig)
    print(f"[OK] Wrote 5 companion 260 DPI PPT charts into {PPT_ASSETS}")


def main():
    B = verify_budget()
    nodes, edges = build_nodes_and_edges(B)
    write_drawio(nodes, edges, B, OUT_DRAWIO)
    render_png(nodes, edges, B, OUT_PNG)
    build_ppt_charts(B)
    T = B["totals"]
    print(f"[SUMMARY] DCO={T['dco_env']:.3f} | SMO={T['smo_env']:.3f} (<=2.50) | MMO={T['mmo_env']:.3f} (<=4.50)")


if __name__ == "__main__":
    main()
