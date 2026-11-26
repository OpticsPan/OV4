"""Single-source pure-SRS data module for ASML TWINSCAN NXT:1965Ci Complete 12-Subsystem
Overlay Specification Requirements Suite (Full PDF + Master DOCX + 12 Standalone Subsystem DOCXs).

STRICT SRS BOUNDARY POLICY:
  - Contains ONLY engineering acceptance specifications (T1/T2/T3), test definitions, dry/wet/on-machine
    fixture boundaries, multi-stage coupling philosophy, physical mechanism notes, and verified primary
    paper figures/references.
  - Intentionally EXCLUDES top-down variance allocation derivation and bottom-up full-machine overlay
    roll-up predictions (DCO/SMO/MMO recovery), which are archived separately in:
      outputs/reports/ASML_NXT1965Ci指标规格分配计算报告_v1.pdf
      outputs/code/calc_nxt1965ci_overlay_budget_audit_v1.py
"""
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OV4_ASSETS = REPO / "参考文献-整理版-Markdown/assets"

# 17 Verified Original Paper Screenshots (local read-only disk)
PAPER_IMGS = {
    "009_fig10":  OV4_ASSETS / "009_9e90b86e529c/images/page_6_chart_3.jpg",
    "022_fig1":   OV4_ASSETS / "022_1aa75fc49631/images/page_1_image_23.jpg",
    "075_fig13":  OV4_ASSETS / "075_97d74e7b9094/images/page_9_chart_2.jpg",
    "009_fig4":   OV4_ASSETS / "009_9e90b86e529c/images/page_3_image_2.jpg",
    "062_fig11":  OV4_ASSETS / "062_57355c4f4bbf/images/page_8_chart_1.jpg",
    "015_fig10":  OV4_ASSETS / "015_9a19b5ebb43f/images/page_6_chart_1.jpg",
    "252_fig3":   OV4_ASSETS / "252_277370ad3131/images/page_3_image_3.jpg",
    "066_fig6":   OV4_ASSETS / "066_d108fef2e419/images/page_4_image_3.jpg",
    "100_fig9":   OV4_ASSETS / "100_cb2cee4b24c6/images/page_6_image_7.jpg",
    "024_fig11":  OV4_ASSETS / "024_e25f1b752cb5/images/page_9_chart_3.jpg",
    "253_fig8":   OV4_ASSETS / "253_d054bfdabe17/images/page_7_chart_1.jpg",
    "021_fig1":   OV4_ASSETS / "021_d3ddae439a1d/images/page_2_image_0.jpg",
    "017_fig2":   OV4_ASSETS / "017_b5a062d07f03/images/page_2_chart_2.jpg",
    "066_fig10a": OV4_ASSETS / "066_d108fef2e419/images/page_6_chart_2.jpg",
    "066_fig5":   OV4_ASSETS / "066_d108fef2e419/images/page_3_image_1.jpg",
    "110_fig4":   OV4_ASSETS / "110_204912f00aad/images/page_2_chart_3.jpg",
    "007_fig5a":  OV4_ASSETS / "007_f7a0019e335d/images/page_3_chart_8.jpg",
}

# Verified Master Reference Catalog (R1..R33)
MASTER_REFS = {
    1: "ASML Official Product Specification. *TWINSCAN NXT:1965Ci* (193 nm, NA 1.35, DCO ≤ 2.5 nm, MMO ≤ 4.5 nm, ≥ 250 wph, FlexRay, PARIS). https://www.asml.com",
    2: "Castenmiller, T., van de Mast, F., de Kort, T., et al. (2010). Towards ultimate optical lithography with NXT:1950i dual stage immersion platform. *Proc. SPIE* 7640, 76401N. DOI: 10.1117/12.847025 [Ref009 Fig. 4 / Fig. 7 / Fig. 10].",
    3: "de Boeij, W., Pieternella, R., Bouchoms, I., et al. (2013). Extending immersion lithography down to 1x nm production nodes. *Proc. SPIE* 8683, 86831L [Ref066 §3.2, §3.4, Fig. 5 / Fig. 6 / Fig. 10a].",
    4: "Butler, H. (2011). Position control in lithographic equipment: an enabler for current-day chip manufacturing. *IEEE Control Systems Magazine*, 31(5), 28–47. DOI: 10.1109/MCS.2011.941653 [Ref094].",
    5: "Heertjes, M. F., Temizer, B., & Schneiders, M. (2013). Self-tuning in master–slave synchronization of high-precision stage systems. *Control Engineering Practice*, 21(12), 1706–1715. DOI: 10.1016/j.conengprac.2013.08.007 [Ref022 Fig. 1].",
    6: "Evers, E., van de Wal, M., & Oomen, T. (2019). Beyond decentralized wafer/reticle stage control design: A double-Youla approach for enhancing synchronized motion. *Control Engineering Practice*, 83, 21–32. DOI: 10.1016/j.conengprac.2018.10.011 [Ref075 Fig. 13].",
    7: "Heertjes, M. F., Butler, H., Dirkx, N. J., et al. (2020). Control of wafer scanners: Methods and developments (ASML/TU/e Survey, §V.B Reticle heating error correction by both reticle and wafer stage) [Ref019].",
    8: "Heertjes, M. F., et al. (2024). Frequency-domain MA/MSD filtering theorems and exposure window analysis for wafer scanners. *Proc. IEEE ECC 2024*. DOI: 10.23919/ECC64448.2024.10591183 [RefN8].",
    9: "ASML US Patent 6,373,072 B1 (2002) [S14] & Nikon US Patent App. 2012/0319637 A1 [S12] (WS Master / RS Slave synchronized scan architecture).",
    10: "Mulkens, J., Kubis, M., Hinnen, P., et al. (2013). High order field-to-field corrections for imaging and overlay to achieve sub 20-nm lithography requirements [Ref154 Eq. (1) & Table 1]; Mulkens, J., Hinnen, P., Kubis, M., et al. (2014). Holistic optimization architecture enabling sub-14-nm projection lithography. *J. Micro/Nanolith. MEMS MOEMS*, 13(1), 011006. DOI: 10.1117/1.JMM.13.1.011006 [RefN7].",
    11: "ASML Netherlands B.V. US Patent 8,237,914 B2 (2012). *Process, apparatus, and device for determining intra-field correction to correct overlay errors between overlapping patterns* (dynamic relative scan speed ratio and transverse trajectory modulation between reticle stage and wafer stage).",
    12: "Naaijkens, G. P. (2013). *Reticle side wall clamping*. PhD Thesis, Eindhoven University of Technology (TU/e). DOI: 10.6100/IR756525 [Ref225 §2.1, §6.3.4, Ch. 7 — reticle micro-slip & dual-stage iHOPC positioning].",
    13: "Carl Zeiss SMT AG. US Patent App. 2008/0174858 A1, Table 3 (NA = 1.35 catadioptric projection lens, 26 × 5.5 mm slit) [RefN1]; ASML Training Manual *12-TT-L3-L3-ME* (p. 70).",
    14: "de Jong, F., van der Pasch, B., Castenmiller, T., Vleeming, B., Droste, R., & van de Mast, F. (2009). Enabling the lithography roadmap: an immersion tool based on a novel stage positioning system. *Proc. SPIE* 7274, 72741S. DOI: 10.1117/12.814254 [Ref062 Fig. 11 — 7-day Gridplate stability < 0.20 nm].",
    15: "de Graaf, R., Weichselbaum, S., Droste, R., McLaren, M., Koek, B., & de Boeij, W. (2016). NXT:1980Di immersion scanner for 7nm production nodes. *Proc. SPIE* 9780, 978011. DOI: 10.1117/12.2220589 [Ref015 Fig. 10 — SMASH repeatability vs WQ].",
    16: "Menchtchikov, B., Socha, R., Zheng, C., et al. (2018). Reduction in overlay error from mark asymmetry using simulation, ORION, and alignment models. *Proc. SPIE* 10587, 105870C. DOI: 10.1117/12.2297493 [Ref252 Fig. 3 — multi-wavelength OCW].",
    17: "Pike, M., Felix, N., Menon, V., Ausschnitt, C., et al. (2012). High order wafer alignment in manufacturing. *Proc. SPIE* 8324, 832408. DOI: 10.1117/12.916483 [Ref123 — SUSD direction aliasing > 3.5 nm Gy20 mitigation]; Phase grating alignment dynamic scan extraction: *Applied Optics*, 64(30), 8921 (2025).",
    18: "Duclaux, B., Gatefait, M., Mermet, O., & Chapon, J.-D. (2020). Run to run and model variability of overlay high order process corrections for mean intrafield signatures. *Proc. SPIE* 11325, 113251K. DOI: 10.1117/12.2551062 [Ref100 Fig. 9 — dual-chuck C2 vs C1 offset].",
    19: "Ma, W.-K., Hwang, Y.-S., Kang, E.-K., et al. (2007). Hardware, materials, and parameters optimization for improvement of immersion overlay. *Proc. SPIE* 6518, 65182Z. DOI: 10.1117/12.712026 [Ref164 — UPW flow sensitivity of TIS].",
    20: "Streefkerk, B., Baselmans, J., Gehoel-van Ansem, W., Mulkens, J., Flagello, D., & Graeupner, P. (ASML & Carl Zeiss SMT, 2004). Extending optical lithography with immersion. *Proc. SPIE* 5377, 285–305 [Ref040 Fig. 7 — Zeiss offline wet PMI & 300 μm thermal boundary].",
    21: "Carl Zeiss SMT AG/GmbH Immersion Metrology & Dry/Wet Adjustment Patents: US 7,408,652 B2, US 8,836,929 B2 & US 8,908,269 B2 (*Device and method for the optical measurement of an optical system by using an immersion fluid*); US 7,796,274 B2, US 8,488,127 B2 & US 8,823,948 B2 (*System for measuring the image quality of an optical imaging system*); US 7,310,187 B2 (*Projection objective and method for adjusting between immersion and dry configurations*).",
    22: "Staals, F., Andryzhyieuskaya, A., Bakker, H., et al. (2011). Advanced wavefront engineering for improved imaging and overlay applications on a 1.35 NA immersion scanner. *Proc. SPIE* 7973, 79731G. DOI: 10.1117/12.880759 [Ref024 Fig. 11]; Halle, S., Crouse, M., Jiang, A., et al. (2012). Lens heating challenges for NTD layers with freeform illumination. *Proc. SPIE* 8326, 832607 [RefN6 Table 4].",
    23: "Klinkhamer, F., Smeets, B., Thijssen, T., et al. (ASML & Carl Zeiss SMT, 2020). On-scanner high-spatial-frequency overlay control using a distortion manipulator [Ref253 Fig. 8]; Pollak, T., Emer, W., Thüring, B., et al. (Carl Zeiss SMT & ASML, 2020). A novel projection lens manipulator for high frequent overlay tuning. *Proc. SPIE* 11327, 113270T. DOI: 10.1117/12.2552063 [RefN4].",
    24: "Smeets, B., Aben, P., Klinkhamer, F., et al. (2022). Supporting future DRAM overlay and EPE roadmaps with the NXT:2100i. *Proc. SPIE* 12051, 120510K. DOI: 10.1117/12.2614031 [Ref254 §2.4 K20 boundary]; Kim, Y. H., et al. (2018). Reticle heating feed-forward control (RHC2) on NXT:1980Di [Ref016]; Ishiyama, S., et al. High-order aberration control during exposure [Ref160].",
    25: "de Klerk, J., Wagner, C., Droste, R., Levasier, L., et al. (ASML & Carl Zeiss SMT, 2007). Performance of a 1.35NA ArF immersion lithography system for 40nm applications. *Proc. SPIE* 6520 [Ref021 Fig. 1 — dual-containment immersion hood & UPW ±2.5 mK thermal stability].",
    26: "D'havé, K., Laidler, D., & Cheng, S. (imec, 2009). Immersion specific error contribution to overlay control. *Proc. SPIE* 7274. DOI: 10.1117/12.814923 [Ref167 — within-lot immersion fingerprint variation < 2%].",
    27: "Ha, S. M., Ham, B.-H., Heo, J., et al. (2013). Thermal behavior of wafers and its effects on overlay performance in immersion lithography. *Microelectronic Engineering* [Ref017 Fig. 2 — SensArray wafer thermal profile, 80 mK zone uniformity, R^{2}=0.92]; Ishikawa, J., et al. (Nikon, 2007). Latest results from hyper-NA immersion scanners S609B and S610C. *Proc. SPIE* 6520, 65201W [Ref050 — scan-order thermal history].",
    28: "ASML US Patent 8,269,949 B2 (WT–MB compliant pin support hysteresis suppression); JP Patent 5,809,458 B2 (segmented compliant reticle clamping).",
    29: "Lim, M., Kim, G., Kim, S., et al. (SK Hynix, 2014). Investigation on reticle heating effect induced overlay error. *Proc. SPIE* 9050, 905014. DOI: 10.1117/12.2048281 [Ref110 Fig. 4 — batch 20-wafer reticle heating ramp].",
    30: "Chen, W., Carroll, J., Storm, G., et al. (2004). Pellicle-induced reticle distortion: An experimental investigation [Ref104 — soft adhesive gasket]; van Haren, R., Steinert, S., Roelofs, C., et al. (2017). Off-line mask-to-mask registration characterization as enabler for computational overlay. *Proc. SPIE* 10451 [Ref098 — pellicle dynamic scan/purge].",
    31: "Fujishima, Y., Ishiyama, S., Isago, S., et al. (2013). Comprehensive thermal aberration & distortion control of lithographic lenses for accurate overlay. *Proc. SPIE* 8683, 86831I [Ref025 — under-reticle laminar air-curtain thermal stabilization].",
    32: "Mulder, M., Engelen, A., Noordman, O., et al. (ASML & Carl Zeiss SMT, 2010). Performance of FlexRay, a fully programmable illumination system for generation of freeform sources on high NA immersion systems [Ref007 Fig. 5a — pupil reproducibility < 0.16%]; Matsuyama, T., et al. (2007). Catadioptric projection lens for 1.3 NA scanner. *Proc. SPIE* 6520, 652021 [Ref051 — chromatic sensitivity & wavelength stability].",
    33: "Takahashi, M., Wakui, S., & Makinouchi, S. Performance improvement of semiconductor lithography machine using active mass damper system [Ref087 — vibration & acoustic isolation]; ASML Training Manual *TT_L2_AM-3v0* (Airmount < 1 Hz isolation & Metroframe dynamic decoupling).",
}

# Opening Multi-Stage Coupling Philosophy (Strictly Pure SRS — ZERO roll-up predictions!)
PHILOSOPHY_PARAS = [
    "**核心验收理念（为何必须设置 T1 / T2 / T3 多阶段验收）：**整机之所以对各子系统设置 T1、T2（及跨工位 T3）多阶段验收，根本目的是促使各子系统团队在设计、装调与验证阶段主动建立两类系统工程意识——**模块间耦合（Inter-Module Coupling）**与**子系统–整机环境耦合（Subsystem–Machine Environment Coupling）**。任何子系统本质上都是服务于整机曝光成像与套刻精度（NXT:1965Ci 顶层目标 DCO / SMO ≤ 2.50 nm、MMO ≤ 4.50 nm）的功能单元，而非孤立交付的单体仪器；子系统在离线独立工装上验证合格的指标，仅代表其剥离外界扰动后的自身本底能力，一旦装入整机运行环境，在相邻模块动态激励、参考基准传递以及真实热/气/液/声学/框架变形的多物理场耦合作用下，其实际功能表现未必能满足真实高速扫描曝光的套刻需求。因此，必须建立由离线单件本底向装机集成与跨台整机联调逐级递进的多阶段验收机制。",
    "**两类耦合风险的内涵与拦截逻辑：**（1）**模块间耦合**涵盖 WS/RS 双台高速主从同步及相对 iHOPC 扫场轨迹耦合、ENC 读数头跨光栅拼接切换（Handover）与运动台闭环观测盲区、AA/TIS/PARIS 与投影物镜参考轴系的基准传递耦合、Lens 操纵器多参共用执行器与 WRS 扫描节拍及激光波长/照明瞳面的光学耦合、以及浸没液控供回水脉动与 TIS/WS 伺服的联动耦合；（2）**子系统与整机环境耦合**涵盖离线干态台架与装机 E 侧超纯水浸没液膜流场扰动及边缘蒸发冷缩的差异、193 nm 曝光热载荷引发的掩模热/物镜热/晶圆热漂移、10 mK 恒温气幕与局部气压波动、计量框架（MF）长期热机械微变形及隔振声学传递。",
    "**多阶段验收的分层边界与放行原则：**① **T1（单件/单台离线验收）**在剥离整机复杂耦合的可控离线工装下验证子系统自身硬本底与独立能力（WS/RS/ENC/AA/WC/RC/IL/MF 离线部件为干态独立台架；IH 为独立液控湿态台架；Lens 因 NA = 1.35 > 1.0 全内反射限制采用局部静态超纯水 wet PMI；TIS+PARIS 因物理紧耦合 E 侧 193 nm 实机光路直接设在机湿区 T1），把硬本底缺陷拦截在装机之前；② **T2（装机解算、同步与调控验收）**在装机结构框架、真实气液热环境及相邻模块联动条件下，考核双台同步、参考光栅长期漂移与跨缝切换、模拟 M 侧动态网格拟合、LensModel 调控残差与动态 iHOPC、装机热/液/夹持/照明/框架耦合指标；③ **T3（跨台整机联调验收）**打通 M 侧量测与 E 侧曝光、双卡盘轮转与满热跨照明之间的整机联调稳定性。**T1 合格仅作为装机准入前提，T2/T3 全部通过方构成子系统服务整机曝光的最终达标依据。**",
]

MASTER_STAGE_SUMMARY = [
    ("T1 阶段", "单件/单台离线验收", "独立可控离线工装（干态台架 / 独立液控台架 / 物镜局部静态 wet PMI；TIS+PARIS 为 E 侧实机湿区）", "剥离整机复杂耦合，验证各子系统硬本底、传感器噪声、单台多项式轨迹、冷机静态波前及温/液/光/隔振单件能力（装机准入前提）"),
    ("T2 阶段", "装机解算/同步/调控验收", "装机 MF 框架、恒温气幕、E 侧超纯水液膜与相邻模块联动工况", "验证模块间耦合与环境耦合：WRS 双台同步与 iHOPC、Gridplate 7 天漂移与 Handover、M 侧 HOWA、LensModel 与动态 iHOPC、液膜/热控/夹持/RHC/照明/框架在机指标"),
    ("T3 阶段", "跨台整机联调验收", "双台全机 M-side / E-side 跨框架交换、连续批曝满热与跨照明切换工况", "打通 M 侧与 E 侧跨框架基线（M-to-E）、双卡盘热/夹持/SYCO 一致性、连续 20 片升温爬坡与跨照明切换稳定性，确保整机满足曝光需求"),
]


def build_all_12_subsystems():
    # =========================================================================
    # 01 WS (Wafer Stage + WRS Sync + WRS-iHOPC) — Pure SRS
    # =========================================================================
    ws_t1a = [
        ("WS-T1A-01", "WS-X 静止在位伺服稳定性", "≤ 0.30 nm", "离线干态单台闭环静止定位（常值目标 q_{0}），经 5.5 mm 等效曝光窗滑窗均值 MA 统计 3σ [注 1]"),
        ("WS-T1A-02", "WS-Y 静止在位伺服稳定性", "≤ 0.30 nm", "离线干态单台闭环静止定位，5.5 mm 等效曝光窗滑窗均值 MA 统计 3σ [注 1]"),
        ("WS-T1A-03", "WS-Rz 静止在位伺服稳定性", "≤ 0.010 μrad", "离线干态单台闭环静止定位，绕 Z 轴偏航角 MA 统计 3σ（10.0 nrad） [注 1]"),
        ("WS-T1A-04", "WS-X 单程动态运动误差 (R_{uni,dyn})", "≤ 0.29 nm", "离线干态满速 0.70 m/s、35–40 m/s^{2} 折返，匀速有效段 A–B 距离 38.5 mm，正反扫分池统计最差点 3σ [注 2]"),
        ("WS-T1A-05", "WS-Y 单程动态运动误差 (R_{uni,dyn})", "≤ 0.29 nm", "离线干态满速 0.70 m/s 扫描主轴，A–B 距离 38.5 mm，正反扫分池统计匀速段最差点 3σ [注 2]"),
        ("WS-T1A-06", "WS-Rz 单程动态运动误差 (R_{uni,dyn})", "≤ 0.0105 μrad", "离线干态满速扫描工况，A–B 距离 38.5 mm，绕 Z 轴偏航角分池统计匀速段最差点 3σ（10.5 nrad） [注 2]"),
        ("WS-T1A-07", "WS-X 残余反向差 (B_{UD,res})", "≤ 0.09 nm", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速曝光段内正反扫平均轨迹差最大值 [注 2]"),
        ("WS-T1A-08", "WS-Y 残余反向差 (B_{UD,res})", "≤ 0.10 nm", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速曝光段内正反扫平均轨迹差最大值 [注 2]"),
        ("WS-T1A-09", "WS-Rz 残余反向差 (B_{UD,res})", "≤ 0.0035 μrad", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速曝光段内绕 Z 轴正反扫均值差最大值（3.5 nrad） [注 2]"),
        ("WS-T1A-10", "WS-X 往返动态运动误差 (R_{bi,dyn})", "≤ 0.38 nm", "离线干态连续 N ≥ 50 组完整往返，按线性包络 R_{uni,dyn} + B_{UD,res} 取匀速段最差点判定 [注 2]"),
        ("WS-T1A-11", "WS-Y 往返动态运动误差 (R_{bi,dyn})", "≤ 0.39 nm", "离线干态连续 N ≥ 50 组完整往返，按线性包络 R_{uni,dyn} + B_{UD,res} 取匀速段最差点判定 [注 2]"),
        ("WS-T1A-12", "WS-Rz 往返动态运动误差 (R_{bi,dyn})", "≤ 0.014 μrad", "离线干态连续 N ≥ 50 组完整往返，按线性包络 R_{uni,dyn} + B_{UD,res} 取匀速段最差点判定（14.0 nrad） [注 2]"),
    ]
    ws_t1b = [
        ("WS-T1B-01", "WS-iHOPC K1 (dx, 1) 单台跟踪残差", "≤ 0.077 nm", "离线干态单台独立测试（无 RS 同步），注入 X 静态偏置 ±50 nm，5.5 mm 窗 MA 拟合残差 |ΔK1| [注 4]"),
        ("WS-T1B-02", "WS-iHOPC K2 (dy, 1) 单台跟踪残差", "≤ 0.077 nm", "离线干态单台独立测试，注入 Y 静态偏置 ±50 nm，5.5 mm 窗 MA 拟合残差 |ΔK2| [注 4]"),
        ("WS-T1B-03", "WS-iHOPC K4 (dy, y) 单台跟踪残差", "≤ 0.044 nm/cm", "离线干态满速 0.70 m/s 注入 ±15 nm/cm 扫向一阶变速指令，A–B 38.5 mm 内 MA 拟合残差 |ΔK4| [注 4]"),
        ("WS-T1B-04", "WS-iHOPC K5 (dx, y) 单台跟踪残差", "≤ 0.044 nm/cm", "离线干态满速注入 ±15 nm/cm 非扫向一阶斜切轨迹 x(y)=k5·y，A–B 段内 MA 拟合残差 |ΔK5| [注 4]"),
        ("WS-T1B-05", "WS-iHOPC K6 (dy, x) 单台跟踪残差", "≤ 0.052 nm/cm", "离线干态满速注入 ±15 nm/cm（±1.5 μrad）恒定偏航角指令 Rz=k6，A–B 段内 MA 拟合残差 |ΔK6| [注 4]"),
        ("WS-T1B-06", "WS-iHOPC K8 (dy, y^{2}) 单台跟踪残差", "≤ 0.026 nm/cm^{2}", "离线干态满速注入 ±3.5 nm/cm^{2} 扫向二阶抛物线变速轨迹，A–B 段内 MA 拟合残差 |ΔK8| [注 4]"),
        ("WS-T1B-07", "WS-iHOPC K10 (dy, xy) 单台跟踪残差", "≤ 0.033 nm/cm^{2}", "离线干态满速注入 ±3.5 nm/cm^{2} 扫向线性动态偏航 Rz(y)=k10·y，A–B 段内 MA 拟合残差 |ΔK10| [注 4]"),
        ("WS-T1B-08", "WS-iHOPC K11 (dx, y^{2}) 单台跟踪残差", "≤ 0.026 nm/cm^{2}", "离线干态满速注入 ±3.5 nm/cm^{2} 非扫向二阶抛物线弯曲 x(y)=k11·y^{2}，A–B 段内 MA 拟合残差 |ΔK11| [注 4]"),
        ("WS-T1B-09", "WS-iHOPC K14 (dy, y^{3}) 单台跟踪残差", "≤ 0.017 nm/cm^{3}", "离线干态满速注入 ±1.5 nm/cm^{3} 扫向三阶变加速轨迹，A–B 段内 MA 拟合残差 |ΔK14| [注 4]"),
        ("WS-T1B-10", "WS-iHOPC K16 (dy, xy^{2}) 单台跟踪残差", "≤ 0.020 nm/cm^{3}", "离线干态满速注入 ±1.5 nm/cm^{3} 扫向二阶动态偏航 Rz(y)=k16·y^{2}，A–B 段内 MA 拟合残差 |ΔK16| [注 4]"),
        ("WS-T1B-11", "WS-iHOPC K19 (dx, y^{3}) 单台跟踪残差", "≤ 0.017 nm/cm^{3}", "离线干态满速注入 ±1.5 nm/cm^{3} 非扫向三阶 S 曲线 x(y)=k19·y^{3}，A–B 段内 MA 拟合残差 |ΔK19| [注 4]"),
    ]
    wrs_t2a = [
        ("WRS-T2A-01", "WRS 同步运动误差 Sync MA-X", "≤ 0.47 nm", "WS/RS 装机满速同步扫描（0.70 / 2.80 m/s），折算 1× 晶圆侧 5.5 mm 曝光窗 MA 3σ（对标 Ref009 Fig. 10） [注 3]"),
        ("WRS-T2A-02", "WRS 同步运动误差 Sync MA-Y", "≤ 0.49 nm", "WS/RS 装机满速同步扫描，1× 晶圆侧 5.5 mm 曝光窗 MA 3σ（对标 Ref009 Fig. 10） [注 3]"),
        ("WRS-T2A-03", "WRS 同步运动误差 Sync MA-Rz", "≤ 0.017 μrad", "WS/RS 装机满速同步扫描，绕 Z 轴相对偏航角 MA 3σ（17.0 nrad） [注 3]"),
    ]
    wrs_t2b = [
        ("WRS-T2B-01", "WRS-iHOPC K1 (dx, 1) 像面残差精度", "≤ 0.140 nm", "整机双台相对轨迹协同执行（不限定内部 WS/RS 分配比例），1× 像面总残差 |ΔK1| [注 4]"),
        ("WRS-T2B-02", "WRS-iHOPC K2 (dy, 1) 像面残差精度", "≤ 0.140 nm", "整机双台相对轨迹协同执行（不限定内部分配），1× 像面总残差 |ΔK2| [注 4]"),
        ("WRS-T2B-03", "WRS-iHOPC K4 (dy, y) 像面残差精度", "≤ 0.080 nm/cm", "整机双台相对扫描速度比调制（不限定内部分配），经 5.5 mm 狭缝有效像面残差 |ΔK4| [注 4]"),
        ("WRS-T2B-04", "WRS-iHOPC K5 (dx, y) 像面残差精度", "≤ 0.080 nm/cm", "整机双台相对横向线性斜切轨迹（不限定内部分配），1× 像面总残差 |ΔK5| [注 4]"),
        ("WRS-T2B-05", "WRS-iHOPC K6 (dy, x) 像面残差精度", "≤ 0.095 nm/cm", "整机双台相对恒定偏航角差 Rz（不限定内部分配），1× 像面总残差 |ΔK6| [注 4]"),
        ("WRS-T2B-06", "WRS-iHOPC K8 (dy, y^{2}) 像面残差精度", "≤ 0.048 nm/cm^{2}", "整机双台相对二阶变速轨迹（不限定内部分配），含 5.5 mm 狭缝平滑后的有效像面残差 |ΔK8| [注 4]"),
        ("WRS-T2B-07", "WRS-iHOPC K10 (dy, xy) 像面残差精度", "≤ 0.060 nm/cm^{2}", "整机双台相对线性动态偏航 Rz(y)（不限定内部分配），1× 像面总残差 |ΔK10| [注 4]"),
        ("WRS-T2B-08", "WRS-iHOPC K11 (dx, y^{2}) 像面残差精度", "≤ 0.048 nm/cm^{2}", "整机双台相对横向二阶抛物线轨迹（不限定内部分配），含 5.5 mm 狭缝有效像面残差 |ΔK11| [注 4]"),
        ("WRS-T2B-09", "WRS-iHOPC K14 (dy, y^{3}) 像面残差精度", "≤ 0.030 nm/cm^{3}", "整机双台相对三阶变加速轨迹（不限定内部分配），含 5.5 mm 狭缝有效像面残差 |ΔK14| [注 4]"),
        ("WRS-T2B-10", "WRS-iHOPC K16 (dy, xy^{2}) 像面残差精度", "≤ 0.036 nm/cm^{3}", "整机双台相对二阶动态偏航 Rz(y)（不限定内部分配），1× 像面总残差 |ΔK16| [注 4]"),
        ("WRS-T2B-11", "WRS-iHOPC K19 (dx, y^{3}) 像面残差精度", "≤ 0.030 nm/cm^{3}", "整机双台相对横向三阶 S 曲线轨迹（不限定内部分配），含 5.5 mm 狭缝有效像面残差 |ΔK19| [注 4]"),
    ]
    ws_notes = [
        ("p", "**[注 1] 套刻专项范围界定、干态工装与闭环观测盲区：**本规格书为套刻（Overlay）专项需求，依据曝光窗频域滤波定理（Heertjes 等，2024）[R8]，滑窗均值 MA 主导套刻位移而滑窗标准差 MSD 主导成像对比度，故运动台仅考核面内 3 自由度（X、Y、Rz）之 MA 指标，垂向 Z/Rx/Ry（焦面）与 Sync MSD 另归焦面/成像规格书。WS-T1 离线单台台架无浸没头与液体（干态环境）。依据运动台闭环观测链路分析（Butler，2011）[R4]，输入常值目标 q_{0} 时编码器观测误差为 q_{1} − q_{0}，真实物理误差满足 e_{true} = (q_{1} − q_{0}) − n_{ENC}，故须以 ENC 传感器离线本底验收合格为前提，并在装机后辅以外部独立干涉仪复核。"),
        ("p", "**[注 2] A–B 扫描行程距离及单程 / 残余反向差 / 往返误差完整数学定义与计算步骤：**"),
        ("indent", "（1）**A–B 距离与四段行程规定：**对应 NXT:1965Ci 全视场 26 × 33 mm [R1] 与 Carl Zeiss SMT 专利 US 2008/0174858 A1 Table 3 及 ASML ME3 手册（p. 70）[R13] 确认的 5.5 mm 真实曝光狭缝，WS 单场扫描依次经历加速段 → 整定段（未开光）→ 匀速有效扫描段（A→B）→ 减速段。为使有效曝光区 y ∈ [−16.5, +16.5] mm 内每一点均拥有完整 ±2.75 mm（L_{s}/2）狭缝滑窗积分数据，规定 **WS 匀速有效段 A–B 距离为 L_{AB,WS} = 38.5 mm**（两端各留 2.75 mm 缓冲，含加减速总机械行程约 55–65 mm）。在 [−16.5, +16.5] mm 内等距取 M 个固定空间点 p_{1}, p_{2}, …, p_{M}，所有趟次严格按空间坐标配准。"),
        ("indent", "（2）**曝光窗滑窗平均（MA）与分池统计：**连续执行 N ≥ 50 组完整往返（50 趟 A→B 正扫 + 50 趟 B→A 反扫）。按狭缝积分时长 τ_{slit} = L_{s}/v_{w} = 7.857 ms [R4, R8]，对第 k 趟扫描在点 p_{j} 处的瞬时跟踪误差 e_{k}(t) 求滑窗平均得 MA_{k}(p_{j}) = (1/τ_{slit}) ∫_{tⱼ−τ/2}^{tⱼ+τ/2} e_{k}(t) dt，随后正扫与反扫**严格分池**计算样本均值与样本标准差（严禁混池）："),
        ("eq", "μ_{up}(p_{j}) = (1/N) Σ_{k=1..N} MA_{k,up}(p_{j}) ，　σ_{up}(p_{j}) = √[ 1/(N−1) · Σ_{k=1..N} (MA_{k,up}(p_{j}) − μ_{up}(p_{j}))^{2} ]"),
        ("indent", "（3）**三项验收判定公式：**① **单程动态运动误差** R_{uni,dyn} = max_{pⱼ} [ max(3σ_{up}(p_{j}), 3σ_{dn}(p_{j})) ]；② **残余反向差** B_{UD,res} = max_{pⱼ} |μ_{up}(p_{j}) − μ_{dn}(p_{j})|（常规标定后考核，不限定内部控制或校准算法）；③ **往返动态运动误差** R_{bi,dyn} = max_{pⱼ} [ R_{uni,dyn}(p_{j}) + B_{UD,res}(p_{j}) ]。三项须同时达标。"),
        ("p", "**[注 3] WRS 同步定义与主从方向：**同步平均误差定义为 MA_{sync} = MA_{WS} − M_{opt}·MA_{RS}，面内 3 轴折算矩阵 M_{opt} = diag(1/4, 1/4, 1)。WRS-T2A 限值对标 Castenmiller 等（SPIE 7640，2010，Ref009 Fig. 10）[R2] 实测水平。经专利 US 6,373,072 B1、US 2012/0319637 A1 [R9] 及 Heertjes 等（2013，Ref022 Fig. 1）[R5] 确认，ArF/ArFi 横向同步均为 WS 主台（Master）、RS 从台（Slave）。"),
        ("p", "**[注 4] 运动 iHOPC 执行主体文献核证、T1 单台独立验证及取消 Range 限制说明：**（1）ASML 一手论文 Mulkens 等（Ref154 Table 1 & JM3 2014）[R10] 将全部 11 项运动 K 参数统一标为 **Scan（双台相对扫描轨迹）**；Heertjes 等（2020，Ref019 §V.B）[R7] 与 Naaijkens（2013，Ref225 Ch. 7）[R12] 均指出修正动作**由 RS 与 WS 共同执行**；ASML 专利 US 8,237,914 B2 [R11] 揭示动态调制双台相对速度比与横向相对轨迹实现场内修正。故 WRS-T2B 不限定内部 WS/RS 轨迹分配比例，严格按最终 1× 像面相对轨迹残差判定。（2）因离线干态 T1 台架无双台同步，故增设 WS-T1B（及 RS-T1B）单台合成多项式轨迹注入测试（标称激励档：0 阶 ±50 nm、1 阶 ±15 nm/cm、2 阶 ±3.5 nm/cm^{2}、3 阶 ±1.5 nm/cm^{3}），在装机前提前考核单台高阶轨迹跟踪能力。（3）WS/RS 行程与推力（35–150 m/s^{2}）[R1, R12] 远超工艺需求（三阶满档附加加速度仅约 7.2×10^{-5} m/s^{2}），不存在量程饱和瓶颈，故不设 Range 限制项。"),
    ]

    # =========================================================================
    # 02 RS (Reticle Stage, 4×) — Pure SRS
    # =========================================================================
    rs_t1a = [
        ("RS-T1A-01", "RS-X 单程动态运动误差 (R_{uni,dyn}, 4×)", "≤ 0.84 nm", "离线干态满速 2.80 m/s、150 m/s^{2} 折返，匀速段 A–B 距离 154.0 mm，正反扫分池统计最差点 3σ（1× 约 0.21 nm） [注 5]"),
        ("RS-T1A-02", "RS-Y 单程动态运动误差 (R_{uni,dyn}, 4×)", "≤ 0.88 nm", "离线干态满速 2.80 m/s 扫描主轴，A–B 距离 154.0 mm，正反扫分池统计最差点 3σ（1× 约 0.22 nm） [注 5]"),
        ("RS-T1A-03", "RS-Rz 单程动态运动误差 (R_{uni,dyn}, 4×)", "≤ 0.0075 μrad", "离线干态满速扫描工况，A–B 距离 154.0 mm，偏航角按 1:1 传至晶圆侧（7.5 nrad，无 4× 缩减） [注 5]"),
        ("RS-T1A-04", "RS-X 残余反向差 (B_{UD,res}, 4×)", "≤ 0.28 nm", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速段正反扫均值差最大值（1× 约 0.07 nm） [注 5]"),
        ("RS-T1A-05", "RS-Y 残余反向差 (B_{UD,res}, 4×)", "≤ 0.30 nm", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速段正反扫均值差最大值（1× 约 0.075 nm） [注 5]"),
        ("RS-T1A-06", "RS-Rz 残余反向差 (B_{UD,res}, 4×)", "≤ 0.0025 μrad", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速段绕 Z 轴正反扫均值差最大值（2.5 nrad） [注 5]"),
        ("RS-T1A-07", "RS-X 往返动态运动误差 (R_{bi,dyn}, 4×)", "≤ 1.12 nm", "离线干态连续 N ≥ 50 组完整往返，线性包络 0.84 + 0.28 = 1.12 nm（1× 等效 0.28 nm） [注 5]"),
        ("RS-T1A-08", "RS-Y 往返动态运动误差 (R_{bi,dyn}, 4×)", "≤ 1.18 nm", "离线干态连续 N ≥ 50 组完整往返，线性包络 0.88 + 0.30 = 1.18 nm（1× 等效 0.30 nm） [注 5]"),
        ("RS-T1A-09", "RS-Rz 往返动态运动误差 (R_{bi,dyn}, 4×)", "≤ 0.010 μrad", "离线干态连续 N ≥ 50 组完整往返，线性包络 10.0 nrad（1:1 传至晶圆侧） [注 5]"),
        ("RS-T1A-10", "RS 掩模高加减速千趟微滑移 (X 向, 4×)", "≤ 0.72 nm", "150 m/s^{2} 满载往返扫描 1000 趟前后，以外部光学标尺测 6 寸石英掩模相对吸盘 X 累积滑移（1× 约 0.18 nm） [注 5]"),
        ("RS-T1A-11", "RS 掩模高加减速千趟微滑移 (Y 向, 4×)", "≤ 0.72 nm", "同上，测扫描主轴 Y 向千趟累积微滑移（编码器无法感知石英相对滑移，须外部独立检测） [注 5]"),
    ]
    rs_t1b = [
        ("RS-T1B-01", "RS-iHOPC K1 等效 X 静态偏置残差 (4×)", "≤ 0.25 nm", "离线干态单台独立测试（无 WS 同步），注入 4× X 偏置 ±200 nm，22.0 mm 掩模窗 MA 残差（等效 1× ≤ 0.063 nm） [注 5]"),
        ("RS-T1B-02", "RS-iHOPC K2 等效 Y 静态偏置残差 (4×)", "≤ 0.25 nm", "离线干态单台独立测试，注入 4× Y 偏置 ±200 nm，22.0 mm 掩模窗 MA 残差（等效 1× ≤ 0.063 nm） [注 5]"),
        ("RS-T1B-03", "RS-iHOPC K4 等效 Y 一阶变速残差 (4×)", "≤ 0.24 nm", "离线满速 2.80 m/s 注入等效 ±15 nm/cm 扫向一阶变速，A–B 154 mm 拟合场边残差（等效 1× |ΔK4| ≤ 0.036 nm/cm） [注 5]"),
        ("RS-T1B-04", "RS-iHOPC K5 等效 X 一阶斜切残差 (4×)", "≤ 0.24 nm", "离线满速注入等效 ±15 nm/cm 横向一阶斜切轨迹，A–B 154 mm 拟合场边残差（等效 1× |ΔK5| ≤ 0.036 nm/cm） [注 5]"),
        ("RS-T1B-05", "RS-iHOPC K6 等效 Rz 静态偏航残差 (4×)", "≤ 0.0043 μrad", "离线满速注入 ±1.5 μrad 恒定偏航角（1:1 传递），A–B 段内 MA 残差（4.3 nrad，等效 1× |ΔK6| ≤ 0.043 nm/cm） [注 5]"),
        ("RS-T1B-06", "RS-iHOPC K8 等效 Y 二阶变速残差 (4×)", "≤ 0.24 nm", "离线满速注入等效 ±3.5 nm/cm^{2} 扫向二阶抛物线变速，A–B 154 mm 拟合场边残差（等效 1× |ΔK8| ≤ 0.022 nm/cm^{2}） [注 5]"),
        ("RS-T1B-07", "RS-iHOPC K10 等效 Rz 线性偏航残差 (4×)", "≤ 0.0045 μrad", "离线满速注入等效 ±3.5 nm/cm^{2} 扫向线性动态偏航 Rz(y)，场边残差（4.5 nrad，等效 1× |ΔK10| ≤ 0.027 nm/cm^{2}） [注 5]"),
        ("RS-T1B-08", "RS-iHOPC K11 等效 X 二阶弯曲残差 (4×)", "≤ 0.24 nm", "离线满速注入等效 ±3.5 nm/cm^{2} 横向二阶抛物线轨迹，A–B 154 mm 拟合场边残差（等效 1× |ΔK11| ≤ 0.022 nm/cm^{2}） [注 5]"),
        ("RS-T1B-09", "RS-iHOPC K14 等效 Y 三阶变速残差 (4×)", "≤ 0.24 nm", "离线满速注入等效 ±1.5 nm/cm^{3} 扫向三阶变加速轨迹，A–B 154 mm 拟合场边残差（等效 1× |ΔK14| ≤ 0.0135 nm/cm^{3}） [注 5]"),
        ("RS-T1B-10", "RS-iHOPC K16 等效 Rz 二阶偏航残差 (4×)", "≤ 0.0044 μrad", "离线满速注入等效 ±1.5 nm/cm^{3} 扫向二阶动态偏航 Rz(y)，场边残差（4.4 nrad，等效 1× |ΔK16| ≤ 0.016 nm/cm^{3}） [注 5]"),
        ("RS-T1B-11", "RS-iHOPC K19 等效 X 三阶 S 曲线残差 (4×)", "≤ 0.24 nm", "离线满速注入等效 ±1.5 nm/cm^{3} 横向三阶 S 曲线轨迹，A–B 154 mm 拟合场边残差（等效 1× |ΔK19| ≤ 0.0135 nm/cm^{3}） [注 5]"),
    ]
    rs_notes_master = [
        ("p", "**[注 5] RS 干态 4× 单台口径、A–B 距离、4× → 1× 折算及 T1-B 独立 iHOPC 验证：**RS 全程工作于干态 4× 掩模侧，标称扫描速度 2.80 m/s、折返加速度 150 m/s^{2} [R1, R12]。按 4:1 光学倍率放大（与第 1 章 [注 2] 严格对应 [R13]），规定 **RS 匀速有效段 A–B 距离为 L_{AB,RS} = 4 × 38.5 = 154.0 mm**（4× 有效曝光区 y_{r} ∈ [−66.0, +66.0] mm 加两端各 11.0 mm 缓冲，总往返行程约 210–230 mm），单程、残余反向差与往返包络的计算步骤与 [注 2] 完全一致 [R4, R8]，且不限定内部控制或校准算法。经投影光学折算至 1× 晶圆面后，X/Y 平移缩小 4 倍，而偏航角 Rz 按 **1:1 等角传递**（无 4× 缩减）。RS-Z/Rx/Ry 归属焦面规格书。高加减速下石英掩模微滑移对机内编码器不可见，须用外部标尺作 1000 趟前后实测（Naaijkens，2013，Ref225）[R12]。依据一手文献确认 RS 与 WS 共同承担扫描方向 iHOPC 修正 [R7, R10, R11, R12]，RS-T1B 在无 WS 同步的离线干态平台独立考核 RS 4× 侧多项式轨迹跟踪能力。图 2-1 为 Evers 等（2019，Ref075 Fig. 13）[R6] 在 ASML 双台平台验证的相对同步误差累积谱改善，说明 RS 高带宽与低重复性对双台同步的支撑作用。"),
    ]
    rs_notes_standalone = [
        ("p", "**[注 5] RS 干态 4× 单台口径、4× → 1× 光学折算界面及 T1-B 独立 iHOPC 验证：**RS 全程工作于干态 4× 掩模侧，标称扫描速度 2.80 m/s、折返加速度 150 m/s^{2} [R1, R12]。经 4:1 投影光学折算至 1× 晶圆像面后，X/Y 平移缩小 4 倍，而偏航角 Rz 按 **1:1 等角传递**（无 4× 缩减）。垂向 Z/Rx/Ry 归属焦面规格书，Sync MSD 归属成像对比度规格书 [R8]，本规格书仅考核套刻面内 3-DOF。150 m/s^{2} 急加减速下石英掩模相对吸盘微滑移在机内编码器中不可见，须用外部光学标尺作 1000 趟前后实测（Naaijkens，2013，Ref225）[R12]。依据 ASML 一手文献与专利确认 RS 与 WS 共同承担扫描方向 11 项运动 iHOPC 修正 [R7, R10, R11, R12]，RS-T1B 在无 WS 同步的离线干态平台通过单台合成多项式轨迹注入（标称档位：0 阶 ±200 nm、1 阶 ±15 nm/cm、2 阶 ±3.5 nm/cm^{2}、3 阶 ±1.5 nm/cm^{3}），独立验收 RS 4× 侧高阶轨迹跟踪能力。装机后 RS 作为从台（Slave）跟从主台 WS（Master）执行双台同步验收（Ref022、US 6,373,072 B1）[R5, R9]；下图为 Evers 等（2019，Ref075 Fig. 13）[R6] 相对同步误差累积谱实测对比。"),
        ("p", "**[附则] RS 4× 侧 A–B 扫描行程距离及单程 / 残余反向差 / 往返误差完整数学定义与计算步骤：**"),
        ("indent", "（1）**A–B 距离与有效曝光段：**对应 1× 视场 26 × 33 mm 与 5.5 mm 真实曝光狭缝（US 2008/0174858 A1 Table 3 & ME3 p. 70）[R1, R13]，按 4:1 放大至掩模侧，有效曝光区为 y_{r} ∈ [−66.0, +66.0] mm、掩模侧狭缝宽 L_{s,RS} = 22.0 mm。规定 **RS 匀速有效段 A–B 距离为 L_{AB,RS} = 154.0 mm**（两端各留 11.0 mm 缓冲，总行程约 210–230 mm），在 [−66.0, +66.0] mm 内等距取 M 个空间坐标点 p_{1}, …, p_{M}，所有趟次严格按空间坐标配准。"),
        ("indent", "（2）**曝光窗滑窗平均（MA）与正反扫分池统计：**连续执行 N ≥ 50 组完整往返（50 趟 A→B 正扫 + 50 趟 B→A 反扫）。按狭缝积分时长 τ_{slit} = 22.0 / 2800 = 7.857 ms [R4, R8]，求滑窗平均 MA_{k}(p_{j}) = (1/τ_{slit}) ∫_{tⱼ−τ/2}^{tⱼ+τ/2} e_{k}(t) dt，正反扫严格分池计算（严禁混池）："),
        ("eq", "μ_{up}(p_{j}) = (1/N) Σ_{k=1..N} MA_{k,up}(p_{j}) ，　σ_{up}(p_{j}) = √[ 1/(N−1) · Σ_{k=1..N} (MA_{k,up}(p_{j}) − μ_{up}(p_{j}))^{2} ]"),
        ("indent", "（3）**三项验收判定公式：**① **单程动态运动误差** R_{uni,dyn} = max_{pⱼ} [ max(3σ_{up}(p_{j}), 3σ_{dn}(p_{j})) ]；② **残余反向差** B_{UD,res} = max_{pⱼ} |μ_{up}(p_{j}) − μ_{dn}(p_{j})|（常规标定后考核，不限定内部算法）；③ **往返动态运动误差** R_{bi,dyn} = max_{pⱼ} [ R_{uni,dyn}(p_{j}) + B_{UD,res}(p_{j}) ]。三项须同时达标。"),
    ]

    # =========================================================================
    # 03 ENC (Optical Grating Encoder) — Pure SRS
    # =========================================================================
    enc_t1 = [
        ("ENC-T1-01", "ENC 原始带噪声测量重复性", "≤ 0.22 nm", "离线干态刚性锁死参考光栅（无伺服激励），1000 Hz 全带宽原始读数 3σ 并附 0.1 Hz–2 kHz 功率谱（对齐 Ref009 Fig. 4） [注 6]"),
        ("ENC-T1-02", "ENC 曝光窗口平滑后测量重复性", "≤ 0.13 nm", "离线干态由 ENC-T1-01 同一时序经 5.5 mm 狭缝曝光窗（τ = 7.857 ms，63.64 Hz ENBW）滑窗平滑后 3σ [注 6]"),
    ]
    enc_t2 = [
        ("ENC-T2-01", "Gridplate 二维光栅板 7 天热机械稳定性", "≤ 0.20 nm", "装机固定于计量框架（MF）底部恒温气幕（10 mK）干态环境，连续 7 天全局网格漂移 3σ（对齐 Ref062 Fig. 11） [注 7]"),
        ("ENC-T2-02", "WS 侧读数头切换 (Handover) 跳变误差 (X 向)", "≤ 0.15 nm", "装机 WS 跨光栅拼接边界与双台交换时，读数头接管解算的 X 向瞬态跳变与零点衔接误差 3σ [注 7]"),
        ("ENC-T2-03", "WS 侧读数头切换 (Handover) 跳变误差 (Y 向)", "≤ 0.15 nm", "装机 WS 跨光栅拼接边界与双台交换时，读数头接管解算的 Y 向瞬态跳变与零点衔接误差 3σ [注 7]"),
    ]
    enc_notes = [
        ("p", "**[注 6] ENC-T1 纯传感器本底定义与文献依据：**T1 离线干态验收阶段，ENC 作为独立位移量测传感器在刚性锁死参考光栅（无伺服激励）上考核两项本底：① 原始 1000 Hz 带宽重复性 ≤ 0.22 nm，对齐 Castenmiller 等（SPIE 7640，2010，Ref009 Fig. 4）[R2] 短固定光程（< 15 mm）编码器实测值，出厂须同步交付 0.1 Hz–2 kHz PSD/CPS 频谱（Heertjes 等，2024）[R8]；② 曝光窗口平滑后重复性 ≤ 0.13 nm，对应 5.5 mm 狭缝与 0.70 m/s 扫速下的等效噪声带宽 B_{ENBW} = 63.64 Hz [R8, R13]，满足相对运动台定位精度的 1:3 计量精度原则（掩模侧 4× 通道带宽与多普勒余量作装机核查）。"),
        ("p", "**[注 7] ENC-T2 基准稳定性与过缝切换要求：**运动台闭环无法察觉“尺子自身的长期漂移与跨缝跳变”[R4]。故 T2 专项验收：① Gridplate 7 天热机械稳定性 ≤ 0.20 nm，对标 de Jong 等（SPIE 7274，2009，Ref062 Fig. 11）[R14] 156 小时实测结果，须借独立参考片或 13×19 多移位标定验证（Mulkens 等，2014）[R10]；② X/Y 读数头切换（Handover）各 ≤ 0.15 nm（Ref009 Fig. 7）[R2]，防止过缝零点偏置被伺服闭环吸收。"),
    ]

    # =========================================================================
    # 04 AA (Wafer Alignment, M-side) — Pure SRS
    # =========================================================================
    aa_t1 = [
        ("AA-T1-01", "单标记静态测量重复性", "≤ 0.22 nm", "离线干态超稳参考扫描台（不分 X/Y），标准无损标记 WQ ≥ 1%，完整重扫 ≥ 30 趟扣台体位移 3σ（对齐 Ref015 Fig. 10） [注 8]"),
        ("AA-T1-02", "低信号工艺片单标记重复性", "≤ 0.50 nm", "离线干态超稳平台（不分 X/Y），衰减模拟低反射工艺标记 WQ = 0.1%–1%，完整重扫 ≥ 30 趟 3σ（对齐 Ref015 Fig. 10） [注 8]"),
        ("AA-T1-03", "四色波长/级次间 24 h 配准稳定性", "≤ 0.32 nm", "离线干态恒温平台（不分 X/Y），532/635/780/850 nm 四波长多级次通道间色差漂移 24 h 连续统计 3σ [注 9]"),
    ]
    aa_t2 = [
        ("AA-T2-01", "单标记动态扫描重复性 (X 向)", "≤ 0.38 nm", "离线干态模拟 M-side 量测端平台（含产线扫速与步进折返节拍），同一标记完整重扫 ≥ 30 趟 3σ [注 8]"),
        ("AA-T2-02", "单标记动态扫描重复性 (Y 向)", "≤ 0.38 nm", "同上，Y 向单标记动态扫描重复性 3σ [注 8]"),
        ("AA-T2-03", "全晶圆网格拟合重复性 HOWA (X 向)", "≤ 0.40 nm", "离线干态模拟 M-side 平台执行类 FIWA 动作（N ≥ 20 标记，正反扫方向配平，含边缘留出点检验），重复 3σ [注 10]"),
        ("AA-T2-04", "全晶圆网格拟合重复性 HOWA (Y 向)", "≤ 0.40 nm", "同上，Y 向全晶圆高阶网格拟合重复性 HOWA 3σ（不重装片测试本体，重装片另行记录吸片重复性） [注 10]"),
    ]
    aa_t3 = [
        ("AA-T3-01", "M-to-E 对准基线短期漂移 (X 向)", "≤ 0.30 nm", "双台整机联调（跨 MF 框架，M-side AA 与 E-side 物镜/TIS 相对位置漂移），片内/批间 X 向 3σ [注 10]"),
        ("AA-T3-02", "M-to-E 对准基线短期漂移 (Y 向)", "≤ 0.30 nm", "同上，Y 向 M-to-E 对准基线短期漂移 3σ [注 10]"),
    ]
    aa_notes = [
        ("p", "**[注 8] 干态测试边界、单标记静态（T1）与动态（T2）重复性定义：**TWINSCAN 双台机 M 侧晶圆对准全过程处于干态环境，无浸没液体 [R2, R20]。相位光栅对准（PGA）原理需带动标记匀速扫过照明光斑并提取干涉相位（*Applied Optics*，2025）[R17]，故 T1“静态重复性”是在离线超稳参考扫描台（无宏动加减速激振）上扣除参考位移后的纯传感器本底，对标 de Graaf 等（SPIE 9780，2016，Ref015 Fig. 10）[R15] 公布的 SMASH 实测曲线。单趟扫描内采集的多组样点不可充当独立重复，须完整进出标记独立重扫 ≥ 30 趟。T2 在模拟 M 侧平台叠加产线步进折返节拍考核动态重复性。"),
        ("p", "**[注 9] 四色多波长配准稳定性依据：**CMP 与刻蚀引起的标记不对称会导致衍射相位偏移（APD/WAD）。Menchtchikov 等（SPIE 10587，2018，Ref252 Fig. 3）[R16] 证实多波长加权融合（OCW）可显著压低晶圆间套刻波动；其前提是仪器自身四通道 24 h 色间漂移足够小（≤ 0.32 nm），否则仪器色差漂移会被误判为工艺不对称。验收不限定具体融合算法，仅约束硬件色间配准稳度。"),
        ("p", "**[注 10] HOWA（T2）与 M-to-E 基线漂移（T3）分级边界：**HOWA 须严格正反扫方向配平以避免 Pike 等（SPIE 8324，2012，Ref123）[R17] 报道的 > 3.5 nm 方向混叠虚假网格；M-to-E 短期漂移跨 MF 框架连接 M 侧与 E 侧，必须在双台整机联调（T3）阶段验收。产品片工艺标记不对称残差（WAD）归入客户产品工艺验证边界，不计入参考片验收。"),
    ]

    # =========================================================================
    # 05 TIS + PARIS (E-side Aerial Image Sensors) — Pure SRS
    # =========================================================================
    tp_t1 = [
        ("TP-T1-01", "TIS 水平空间像对准重复性 (X 向)", "≤ 0.40 nm", "E-side 曝光端 193 nm 湿区在机透射空间像扫描，连续 ≥ 30 次对准解算 3σ（附供水流量窗核验） [注 11]"),
        ("TP-T1-02", "TIS 水平空间像对准重复性 (Y 向)", "≤ 0.40 nm", "同上，E-side 曝光端 193 nm 湿区 Y 向空间像对准重复性 3σ（用于 M-to-E 基线定期清零） [注 11]"),
        ("TP-T1-03", "双台 TIS-1 / TIS-2 匹配稳定性 (X 向)", "≤ 0.28 nm", "整机双台交换工况下，24 h 内双传感板相对 X 位置漂移 3σ [注 11]"),
        ("TP-T1-04", "双台 TIS-1 / TIS-2 匹配稳定性 (Y 向)", "≤ 0.28 nm", "同上，24 h 内双晶圆台 TIS 基准板 Y 向相对匹配漂移 3σ [注 11]"),
        ("TP-T1-05", "PARIS 7 视场点掩模对准重复性 RA (X 向)", "≤ 0.47 nm", "E-side 7 视场点并行空间像掩模对准重复性 3σ，对标 Ref066 §3.4（< 0.50 nm） [注 11]"),
        ("TP-T1-06", "PARIS 7 视场点掩模对准重复性 RA (Y 向)", "≤ 0.47 nm", "同上，7 视场点并行 Y 向掩模对准重复性 3σ [注 11]"),
        ("TP-T1-07", "PARIS 奇像差波前测量重复性", "≤ 0.14 nm RMS", "E-side 193 nm 湿区在机波前反演重复性 RMS，为物镜奇像差闭环调控提供 1:3 计量精度支撑 [注 11]"),
    ]
    tp_notes = [
        ("p", "**[注 11] 单级在机验收（T1）、套刻范围精简与装机湿区工况说明：**TIS（6 kHz 透射空间像基准）与 PARIS（7 视场点并行空间像传感器）[R3] 直接工作于 193.368 nm 曝光光路与 E 侧投影物镜像面，物理上须在装机 E 侧（含正常超纯水浸没液膜，非干态离线）执行，故设 **T1 单级在机验收**（双台匹配项须在双台交换工况下测试）。纯焦面项（TIS-Z、PARIS-Z）另归焦面规格书。文献依据：① de Boeij 等（SPIE 8683，2013，Ref066 §3.4 & Fig. 6）[R3] 公布 PARIS 7 点掩模对准重复性规格 < 0.50 nm；② Ma 等（SPIE 6518，2007，Ref164）[R19] 证实浸没超纯水（UPW）供回水流量波动会调制 TIS 测位重复性，故 TP-T1-01/02 须在标称供水流量窗内复核；③ Duclaux 等（SPIE 11325，2020，Ref100 Fig. 9）[R18] 揭示双卡盘（C2 vs C1）切换时会诱发 K7/K12/K13 低阶参考偏置，故须严控双台 TIS 匹配稳定度并启用双卡盘参考匹配。"),
    ]

    # =========================================================================
    # 06 Lens (Projection Optics, NA = 1.35) — Pure SRS
    # =========================================================================
    odd_z = [
        ("Z7",  0.21, 0.0742, "1θ X"), ("Z8",  0.21, 0.0742, "1θ Y"),
        ("Z10", 0.19, 0.0672, "3θ X"), ("Z11", 0.19, 0.0672, "3θ Y"),
        ("Z14", 0.21, 0.0606, "1θ X"), ("Z15", 0.21, 0.0606, "1θ Y"),
        ("Z19", 0.24, 0.0693, "3θ X"), ("Z20", 0.24, 0.0693, "3θ Y"),
        ("Z23", 0.28, 0.0700, "1θ X"), ("Z24", 0.28, 0.0700, "1θ Y"),
        ("Z26", 0.19, 0.0548, "5θ X"), ("Z27", 0.19, 0.0548, "5θ Y"),
        ("Z30", 0.26, 0.0650, "3θ X"), ("Z31", 0.26, 0.0650, "3θ Y"),
        ("Z34", 0.36, 0.0805, "1θ X"), ("Z35", 0.36, 0.0805, "1θ Y"),
        ("Z39", 0.26, 0.0650, "5θ X"), ("Z40", 0.26, 0.0650, "5θ Y"),
        ("Z43", 0.36, 0.0805, "3θ X"), ("Z44", 0.36, 0.0805, "3θ Y"),
        ("Z47", 0.42, 0.0857, "1θ X"), ("Z48", 0.42, 0.0857, "1θ Y"),
        ("Z50", 0.28, 0.0700, "7θ X"), ("Z51", 0.28, 0.0700, "7θ Y"),
        ("Z54", 0.30, 0.0671, "5θ X"), ("Z55", 0.30, 0.0671, "5θ Y"),
        ("Z58", 0.42, 0.0857, "3θ X"), ("Z59", 0.42, 0.0857, "3θ Y"),
        ("Z62", 0.48, 0.0907, "1θ X"), ("Z63", 0.48, 0.0907, "1θ Y"),
    ]
    ln_t1 = [
        (f"LN-T1-{k:02d}", zc, f"≤ {flim:.2f} nm",
         f"离线局部静态超纯水浸没干涉平台（wet PMI，λ=193.368 nm，NA=1.35）冷机绝对上限；{tag}，等效 ≤ {rmsv:.4f} nm RMS [注 12]")
        for k, (zc, flim, rmsv, tag) in enumerate(odd_z, 1)
    ] + [
        ("LN-T1-31", "K20 (dy, x^{3}) 冷机静畸变", "≤ 0.18 nm/cm^{3}", "NXT:1965Ci 不配 K20 主动操纵器，冷机装调出厂静态畸变绝对上限 [注 13]")
    ]
    adj_z = [
        ("Z7",  0.12, "1θ X 彗差"), ("Z8",  0.12, "1θ Y 彗差"),
        ("Z10", 0.11, "3θ X 三叶草"), ("Z11", 0.11, "3θ Y 三叶草"),
        ("Z14", 0.12, "1θ X 二阶彗差"), ("Z15", 0.12, "1θ Y 二阶彗差"),
        ("Z19", 0.14, "3θ X 二阶三叶草"), ("Z20", 0.14, "3θ Y 二阶三叶草"),
        ("Z23", 0.16, "1θ X 三阶彗差"), ("Z24", 0.16, "1θ Y 三阶彗差"),
        ("Z26", 0.11, "5θ X 五叶草"), ("Z27", 0.11, "5θ Y 五叶草"),
    ]
    ln_t2a = [
        (f"LN-T2A-{k:02d}", zc, f"≤ {rlim:.2f} nm",
         f"任意一次经 LensModel 下发波前/畸变调节指令后，实测与目标差 |Z_{{meas}} − Z_{{target}}| 上限（{desc}） [注 12]")
        for k, (zc, rlim, desc) in enumerate(adj_z, 1)
    ] + [
        ("LN-T2A-13", "Z30–Z63 调节伴生残差增量", "≤ 0.05 nm", "任意一次 LensModel 调节前后，非主动驱动高阶奇像差单项附加变化量上限 [注 12]"),
        ("LN-T2A-14", "Z5–Z64 全瞳调整后合成残差", "≤ 0.22 nm RMS", "任意一次 LensModel 调节后，全瞳 30 项奇像差总偏差 RMS 上限（且绝对值仍不突破 T1 上限） [注 12]"),
    ]
    ln_t2b_range = [
        ("LN-T2B-01", "Lens-iHOPC K3 (dx, x) 补偿调节范围", "±50–100 nm/cm", "用户单场有效量程（硬件极限 ±150–250 nm/cm，即 ±15–25 ppm），镜片与波长协同 [注 13]"),
        ("LN-T2B-02", "Lens-iHOPC K7 (dx, x^{2}) 补偿调节范围", "±10.0 nm/cm^{2}", "用户单场有效量程，沿狭缝横向二阶拉伸畸变补偿 [注 13]"),
        ("LN-T2B-03", "Lens-iHOPC K9 (dx, xy) 补偿调节范围", "±8.0 nm/cm^{2}", "用户单场有效量程，扫描中镜片动态随动梯形补偿 [注 13]"),
        ("LN-T2B-04", "Lens-iHOPC K12 (dy, x^{2}) 补偿调节范围", "±10.0 nm/cm^{2}", "用户单场有效量程，沿狭缝横向二阶弓形补偿 [注 13]"),
        ("LN-T2B-05", "Lens-iHOPC K13 (dx, x^{3}) 补偿调节范围", "±6.0 nm/cm^{3}", "用户单场有效量程，沿狭缝横向三阶畸变补偿 [注 13]"),
        ("LN-T2B-06", "Lens-iHOPC K15 (dx, x^{2}y) 补偿调节范围", "±4.0 nm/cm^{3}", "用户单场有效量程，三阶动态混合项补偿 [注 13]"),
        ("LN-T2B-07", "Lens-iHOPC K17 (dx, xy^{2}) 补偿调节范围", "±4.0 nm/cm^{3}", "用户单场有效量程，三阶动态混合项补偿（掩模热演进项） [注 13]"),
        ("LN-T2B-08", "Lens-iHOPC K18 (dy, yx^{2}) 补偿调节范围", "±4.0 nm/cm^{3}", "用户单场有效量程，三阶动态混合项补偿（掩模热主修正项） [注 13]"),
        ("LN-T2B-09", "iHOPC 8 项联合量程占用上限", "≤ 80% Range", "8 项激活 K 参数同时施加标称满量程指令时，任一镜片执行器机械行程不饱和 [注 14]"),
    ]
    ln_t2c_prec = [
        ("LN-T2C-01", "Lens-iHOPC K3 (dx, x) 补偿调节精度", "≤ 0.120 nm/cm", "总验收残差 |ΔK3|，最小步长 ≤ 0.012 nm/cm（双档 4 / 15 nm/cm 线性核验） [注 13]"),
        ("LN-T2C-02", "Lens-iHOPC K7 (dx, x^{2}) 补偿调节精度", "≤ 0.092 nm/cm^{2}", "总验收残差 |ΔK7|，最小步长 ≤ 0.009 nm/cm^{2} [注 13]"),
        ("LN-T2C-03", "Lens-iHOPC K9 (dx, xy) 补偿调节精度", "≤ 0.072 nm/cm^{2}", "总验收残差 |ΔK9|，最小步长 ≤ 0.007 nm/cm^{2} [注 13]"),
        ("LN-T2C-04", "Lens-iHOPC K12 (dy, x^{2}) 补偿调节精度", "≤ 0.092 nm/cm^{2}", "总验收残差 |ΔK12|，最小步长 ≤ 0.009 nm/cm^{2} [注 13]"),
        ("LN-T2C-05", "Lens-iHOPC K13 (dx, x^{3}) 补偿调节精度", "≤ 0.070 nm/cm^{3}", "总验收残差 |ΔK13|，最小步长 ≤ 0.007 nm/cm^{3} [注 13]"),
        ("LN-T2C-06", "Lens-iHOPC K15 (dx, x^{2}y) 补偿调节精度", "≤ 0.054 nm/cm^{3}", "总验收残差 |ΔK15|，最小步长 ≤ 0.005 nm/cm^{3} [注 13]"),
        ("LN-T2C-07", "Lens-iHOPC K17 (dx, xy^{2}) 补偿调节精度", "≤ 0.042 nm/cm^{3}", "总验收残差 |ΔK17|，最小步长 ≤ 0.004 nm/cm^{3} [注 13]"),
        ("LN-T2C-08", "Lens-iHOPC K18 (dy, yx^{2}) 补偿调节精度", "≤ 0.054 nm/cm^{3}", "总验收残差 |ΔK18|，最小步长 ≤ 0.005 nm/cm^{3} [注 13]"),
        ("LN-T2C-09", "iHOPC 单向调节重复性", "≤ 35% Spec", "各 K 参数单方向阶跃重复调节 30 次，3σ 不超过对应精度 Spec 的 35% [注 14]"),
        ("LN-T2C-10", "iHOPC 双向调节滞回", "≤ 25% Spec", "各 K 参数正反向阶跃往返差，不超过对应精度 Spec 的 25% [注 14]"),
        ("LN-T2C-11", "iHOPC 跨 K 参数串扰抑制", "≤ 30% Spec", "单参数满量程动作时，诱发其余非目标 K 项伴生偏移不超过目标精度 Spec 的 30% [注 14]"),
        ("LN-T2C-12", "iHOPC 调节诱发奇像差增量", "≤ 0.05 nm RMS", "单参数满量程动作期间，诱发 Z5–Z64 奇像差波前附加恶化量上限（焦面串扰另归焦面规格书） [注 14]"),
        ("LN-T2C-13", "iHOPC 静态参数响应整定时间", "≤ 20–50 ms", "K3 ≤ 20 ms（波长 < 1 ms）、K7/K12 ≤ 40 ms、K13 ≤ 50 ms，满足片间与逐场静态刷新节拍 [注 14]"),
        ("LN-T2C-14", "iHOPC 动态参数扫描同步相位滞后", "≤ 0.20 ms", "动态项 K9/K15/K17/K18 在 0.70 m/s 扫描中与 WRS 同步触发，实测机电相位滞后上限 [注 14]"),
        ("LN-T2C-15", "iHOPC 短期保持漂移 (15 s)", "≤ 20% Spec", "单片曝光周期 15 s 内各 K 参数保持漂移上限 [注 14]"),
        ("LN-T2C-16", "iHOPC 中期保持漂移 (15 min)", "≤ 35% Spec", "单批 15 min 内各 K 参数保持漂移上限 [注 14]"),
        ("LN-T2C-17", "iHOPC 长期保持漂移 (24 h)", "≤ 50% Spec", "24 h 无重新标定条件下各 K 参数保持漂移上限 [注 14]"),
    ]
    ln_notes = [
        ("p", "**[注 12] NA = 1.35 物镜离线 T1 湿态耦合、Zeiss 干/湿测量专利核证及 Odd Zernike 两层定义：**（1）依据 NA = n·sin(θ) = 1.35 [R13]，若末片熔融石英（n ≈ 1.56）下方为空气，1.0 < NA ≤ 1.35 外瞳光线发生**全内反射（TIR）**无法出射。Streefkerk 等（ASML & Carl Zeiss SMT，SPIE 5377，2004，Ref040 Fig. 7）[R20] 披露 Zeiss 出厂采用**湿态相移干涉仪（wet PMI）**验收波前；Carl Zeiss SMT 专利族 **US 7,408,652 B2、US 8,836,929 B2、US 8,908,269 B2** 及 **US 7,796,274 B2、US 8,488,127 B2、US 8,823,948 B2** [R21] 披露了局部静态浸没液池与密封防退化测试结构载体；**US 7,310,187 B2** [R21] 披露了物镜干/湿态切换装调方法。（2）经核查公开专利与 SPIE 论文，尚无公开文献明文记载 Zeiss 对 NA = 1.35 物镜固定执行“先 Dry（NA = 0.93）测、再 Wet（NA = 1.35）测”双阶段出厂 SOP（属于未公开工厂细节）；装调早期可在干态缩瞳（NA < 1.0）排查风险，但 **T1 全瞳（NA = 1.35）最终验收必须且只能以局部静态超纯水 wet PMI 为准** [R20, R21]。（3）T1 约束冷机绝对奇像差上限（全瞳 ≤ 0.400 nm RMS，匹配 Staals 等 FlexWave 实测 [R22] 及 Halle 等跨照明表 [R22]）；T2-A 约束任意一次经 LensModel 调节后的偏差残差 |Z_{meas} − Z_{target}|，且调后绝对波前不得突破 T1 上限。"),
        ("p", "**[注 13] T1 K20 静畸变剥离与 T2-B/T2-C 动态 Lens-iHOPC 定义：**依据 Smeets 等（SPIE 12051，2022，Ref254 §2.4）[R24]，NXT:1965Ci 不配 K20（dy, x^{3}）主动操纵器，故归入 T1 冷机静畸变管控。T2-B（量程）与 T2-C（精度）分表考核 8 项激活 K 参数（放大率换算 1 nm/cm = 0.1 ppm），SET-vs-GET 线性精度参照 ASML/Carl Zeiss SMT 畸变操纵器实测（Klinkhamer 等，Ref253 Fig. 8；Pollak 等，SPIE 11327，2020）[R23] 与 19 参 iHOPC 架构（Mulkens 等）[R10]、RHC2 掩模热演化规律（Kim 等，Ref016）[R24]。"),
        ("p", "**[注 14] T2-B / T2-C 套刻相关联合行程与动态考核说明：**物镜镜片物理微动行程稀缺且多参共用执行器矩阵 [R23, R24]，故 T2-B-09 约束 8 项联合行程占用 ≤ 80% Range 防饱和，T2-C-09 至 T2-C-17 同步考核最小步长、单向重复、双向滞回、跨 K 串扰、诱发奇像差（≤ 0.05 nm RMS）[R22, R23]、静态整定与动态扫描同步相位滞后（≤ 0.20 ms）[R24] 及 15 s / 15 min / 24 h 保持漂移（纯焦面串扰另归焦面规格书）。"),
    ]

    # =========================================================================
    # 07 IH (Immersion Hood & UPW Fluid Control) — NEW!
    # =========================================================================
    ih_t1 = [
        ("IH-T1-01", "UPW 供水温度稳定性", "≤ ±3.0 mK", "离线独立湿态液控台架，额定供水流量连续 24 h 进口水温波动 3σ（对标 Ref021 ±2.5 mK） [注 15]"),
        ("IH-T1-02", "UPW 供水流量脉动稳定性", "≤ ±0.5%", "离线液控台架额定工况下，供回水泵及阻尼器出口流量相对脉动 3σ（0.1–100 Hz 带宽） [注 15]"),
        ("IH-T1-03", "UPW 脱气溶氧量控制上限", "≤ 2.0 ppm", "离线纯水脱气模块出口在线溶氧仪检测，抑制高速扫场微气泡与局部折射率突变 [注 15]"),
        ("IH-T1-04", "浸没头气幕气刀压力稳定性", "≤ ±0.5%", "离线液控台架标称扫描流量下，外圈气刀约束压力波动 3σ（防弯液面失稳与压脉传递） [注 15]"),
        ("IH-T1-05", "高速模拟扫描无残液滴临界扫速", "≥ 0.75 m/s", "离线模拟疏水/低接触角涂胶晶圆高速往返台架，≥ 0.75 m/s 满速扫描后无残余拖尾水膜/微液滴 [注 15]"),
        ("IH-T1-06", "浸没头垂向浮动间隙控制重复性", "≤ ±2.0 μm", "离线液控台架高速跟踪模拟晶圆起伏，液膜工作间隙稳控 3σ（防弯液面流场突变） [注 15]"),
    ]
    ih_t2 = [
        ("IH-T2-01", "E-side 满速水膜折射率梯度套刻贡献 (X 向)", "≤ 0.28 nm", "装机 E 侧 0.70 m/s 满速扫描工况，物镜末片 300 μm 水膜热边界层折射率梯度与流场扰动引起单层 X 偏移 3σ [注 15]"),
        ("IH-T2-02", "E-side 满速水膜折射率梯度套刻贡献 (Y 向)", "≤ 0.28 nm", "同上，装机 E 侧 0.70 m/s 满速扫描工况，水膜折射率梯度与流场扰动引起单层 Y 偏移 3σ [注 15]"),
        ("IH-T2-03", "供水流量扫频下 TIS 测位稳定性复核", "无系统跳变", "装机 E 侧在标称供水流量工作窗内执行流量阶跃/扫频，TIS X/Y 重复性仍满足 ≤ 0.40 nm（防 Ref164 流量调制） [注 15]"),
        ("IH-T2-04", "批内浸没特定套刻指纹相对波动", "≤ 2.0%", "装机连续满速批曝工况，浸没相关场内/场间畸变指纹随批次时间的相对波动上限（对标 Ref167） [注 15]"),
    ]
    ih_t3 = [
        ("IH-T3-01", "双卡盘满速湿区连续曝光边缘蒸发一致性", "无边缘突变", "整机双卡盘 0.70 m/s 连续批曝（含晶圆边缘跨界扫场），晶圆边缘区与中心区套刻残差无显著蒸发冷缩突变 [注 15]"),
    ]
    ih_notes = [
        ("p", "**[注 15] 浸没头与超纯水液控系统（IH）分级验收依据：**193 nm 水浸没光刻中，超纯水热光系数 dn_{w}/dT ≈ −1.0×10^{-4} K^{-1}，物镜末片下方约 300 μm 热边界层内的水温波动与流场不均会直接转化为光学折射率梯度畸变（Streefkerk 等，SPIE 5377，2004，Ref040）[R20]。de Klerk 等（ASML & Carl Zeiss SMT，SPIE 6520，2007，Ref021 Fig. 1）[R25] 披露双层水约束 + 气刀（Air Curtain）浸没头架构并将超纯水温稳控在 ±2.5 mK 量级；本规格书 T1 离线液控台架定限 ≤ ±3.0 mK 且无拖液滴临界扫速 ≥ 0.75 m/s（覆盖 0.70 m/s 标称与高产速余量）。装机 T2 阶段重点考核两类强耦合风险：① Ma 等（SPIE 6518，2007，Ref164）[R19] 证实供水流量脉动会直接调制 E 侧 TIS 对准重复性，故 IH-T2-03 强制开展流量扫频-TIS 联动复核；② D'havé 等（imec，SPIE 7274，2009，Ref167）[R26] 表明浸没特定套刻指纹批内波动须控在 2% 以内。T3 验证高速跨晶圆边缘扫场时无残液膜蒸发冷缩突变。"),
    ]

    # =========================================================================
    # 08 WT-TC & WH (Wafer Table Thermal & Wafer Handler Pre-conditioning) — NEW!
    # =========================================================================
    wt_t1 = [
        ("WT-T1-01", "晶圆台内部冷却水回路温度稳定性", "≤ ±3.0 mK", "离线干态热控台架，晶圆台控温水回路连续 24 h 稳态温度波动 3σ [注 16]"),
        ("WT-T1-02", "晶圆台分区边缘补偿加热均匀性", "≤ 80 mK", "离线干态热控台架，使用无线测温晶圆（SensArray 类）测 300 mm 硅片全片空间温度均匀性 3σ（对齐 Ref017） [注 16]"),
        ("WT-T1-03", "晶圆传片预处理单元 (TSU) 出口温差", "≤ ±15 mK", "离线干态传片预处理台架，经 WH 预调温（TSU）出片后硅片均温与机台标称基准温度差 3σ [注 16]"),
        ("WT-T1-04", "WH 预调温单元全片温度均匀性", "≤ 25 mK", "离线干态 TSU 出片状态，300 mm 硅片面内中心至边缘最大温差 3σ [注 16]"),
        ("WT-T1-05", "晶圆吸片后热平衡时间常数", "≤ 3.0 s", "离线干态台架，带 ±15 mK 初始温差的硅片吸附至 WT 后，面内温差衰减至 ≤ 1.0 mK 所需时间 [注 16]"),
    ]
    wt_t2 = [
        ("WT-T2-01", "装机 M-to-E 传片热瞬态残余偏移 (X 向)", "≤ 0.23 nm", "装机干/湿转换工况，硅片自 WH 经 M 侧对准至 E 侧曝光全流程中，未平衡热瞬态引起的单层 X 残余偏移 3σ [注 16]"),
        ("WT-T2-02", "装机 M-to-E 传片热瞬态残余偏移 (Y 向)", "≤ 0.23 nm", "同上，未平衡热瞬态引起的单层 Y 残余偏移 3σ [注 16]"),
        ("WT-T2-03", "装机曝光热载荷与蒸发冷缩补偿残差 (X 向)", "≤ 0.42 nm", "装机模拟标称曝光剂量与浸没蒸发冷缩，启用晶圆热控模型后单层非可校高阶 X 残余偏移 3σ [注 16]"),
        ("WT-T2-04", "装机曝光热载荷与蒸发冷缩补偿残差 (Y 向)", "≤ 0.42 nm", "同上，启用晶圆热控模型后单层非可校高阶 Y 残余偏移 3σ [注 16]"),
        ("WT-T2-05", "双晶圆台 WT-1 / WT-2 静态温场一致性", "≤ 10 mK", "装机双台热稳态工况下，两只晶圆卡盘面内等效平均温度及径向梯度差 3σ [注 16]"),
    ]
    wt_t3 = [
        ("WT-T3-01", "正序与倒序扫描热史差分套刻验证 (X 向)", "无热史超差", "双台连续满热批曝，对比正向场序与反向场序曝光结果，确认高阶热畸变残差受控（对齐 Ref050） [注 16]"),
        ("WT-T3-02", "正序与倒序扫描热史差分套刻验证 (Y 向)", "无热史超差", "同上，Y 向正序与倒序扫描热史差分套刻验证 [注 16]"),
    ]
    wt_notes = [
        ("p", "**[注 16] 晶圆温控与传片预处理系统（WT-TC & WH）物理机制与文献依据：**硅片线热膨胀系数 α_{Si} = 2.6 ppm/K，对于 300 mm 晶圆（半径 150 mm），全片每变化 1 mK 对应边缘径向位移达 0.39 nm。虽然均匀径向膨胀可由对准放大率部分吸收，但 M 侧量测至 E 侧曝光之间的瞬态温漂、曝光吸收热梯度及浸没边缘蒸发冷缩会形成不可线性抵消的高阶套刻畸变。Ha 等（2013，Ref017 Fig. 2）[R27] 利用无线 SensArray 测温晶圆实测揭示了硅片从 Pre-align & TSU → Measure side → Exposure side 的温场演化，并证实全片 80 mK（3σ）空间温场与套刻具有高度相关性（R^{2} = 0.92）。因此 T1 离线严控台面水冷 ±3.0 mK、分区加热均匀性 ≤ 80 mK 及 TSU 出口 ±15 mK；T2 考核装机热瞬态与曝光/蒸发补偿残差；T3 依据 Ishikawa 等（SPIE 6520，Ref050）[R27] 强制开展正序/倒序扫描热史验证。"),
    ]

    # =========================================================================
    # 09 WC (Wafer Clamping & WT-MB Interface) — NEW!
    # =========================================================================
    wc_t1 = [
        ("WC-T1-01", "晶圆吸盘瘤点接触面摩擦一致性", "变异 ≤ 10%", "离线干态台架，300 mm 碳化硅/微晶玻璃瘤点台面全区摩擦系数与接触刚度空间一致性检测 [注 17]"),
        ("WC-T1-02", "真空吸附气压控制稳定性", "≤ ±0.5 kPa", "离线干态台架，真空分区夹持稳压波动 3σ，防止吸附力变化引发背面局部滑移 [注 17]"),
        ("WC-T1-03", "标准参考片重复吸片面内变形重复性 (X 向)", "≤ 0.30 nm", "离线干态台架，标准低翘曲硅片连续卸载-重装吸片 ≥ 30 次，面内非可校形变重复性 X 向 3σ [注 17]"),
        ("WC-T1-04", "标准参考片重复吸片面内变形重复性 (Y 向)", "≤ 0.30 nm", "同上，标准低翘曲硅片重复吸片面内变形重复性 Y 向 3σ [注 17]"),
        ("WC-T1-05", "满加减速扫场背面摩擦微滑移 (X 向)", "≤ 0.20 nm", "离线干态满载 35–40 m/s^{2} 往返扫描 500 趟前后，硅片相对吸盘 X 向面内累积微滑移 3σ [注 17]"),
        ("WC-T1-06", "满加减速扫场背面摩擦微滑移 (Y 向)", "≤ 0.20 nm", "同上，扫描主轴 Y 向硅片相对吸盘累积微滑移 3σ [注 17]"),
        ("WC-T1-07", "WT–MB 柔顺长柱支承接口正反扫滞回 (X 向)", "≤ 0.15 nm", "离线干态台架，验证晶圆台-计量块柔顺支承（US 8,269,949 B2）在正反扫惯性力下的 X 向面内残余滞回 [注 17]"),
        ("WC-T1-08", "WT–MB 柔顺长柱支承接口正反扫滞回 (Y 向)", "≤ 0.15 nm", "同上，验证 WT–MB 柔顺长柱支承接口在正反扫惯性力下的 Y 向面内残余滞回 [注 17]"),
    ]
    wc_t2 = [
        ("WC-T2-01", "双卡盘 WT-1 vs WT-2 夹持指纹差异 (X 向)", "≤ 0.35 nm", "装机双台轮换工况，同一标准参考片分别吸附于 1 号与 2 号卡盘时的面内静态夹持指纹差 X 向 3σ [注 17]"),
        ("WC-T2-02", "双卡盘 WT-1 vs WT-2 夹持指纹差异 (Y 向)", "≤ 0.35 nm", "同上，双卡盘 WT-1 vs WT-2 面内静态夹持指纹差 Y 向 3σ [注 17]"),
        ("WC-T2-03", "50 μm 翘曲测试片夹持面内残差 (X 向)", "≤ 1.00 nm", "装机工况下吸附标称 50 μm 弓形翘曲测试片，扣除线性项后面内套刻残差 X 向 3σ（对齐 Ref066 Fig. 10a） [注 17]"),
        ("WC-T2-04", "50 μm 翘曲测试片夹持面内残差 (Y 向)", "≤ 1.00 nm", "同上，50 μm 翘曲测试片夹持面内残差 Y 向 3σ（对齐 Ref066 Fig. 10a） [注 17]"),
    ]
    wc_t3 = [
        ("WC-T3-01", "整机双卡盘交替批曝夹持稳定性复核", "双盘无漂移", "整机双卡盘连续批曝 25 片前后，复测双盘夹持指纹差仍满足 ≤ 0.35 nm 且无背面颗粒诱发局部畸变 [注 17]"),
    ]
    wc_notes = [
        ("p", "**[注 17] 晶圆夹持与台面接口系统（WC）分级验收依据：**晶圆吸附在瘤点（Burl）真空吸盘上时，硅片背面摩擦滞回、吸片重复性及高速往返惯性力引发的微滑移会直接转化为无法由对准完全抵消的面内位移（IPD）。吸盘平坦度（≤ 6.5 nm）主要归属焦面均匀性规格书，本规格书聚焦面内套刻项：T1 离线干态验收重复吸片（≤ 0.30 nm）、满加减速背面微滑移（≤ 0.20 nm）以及晶圆台与计量块（WT–MB）柔顺长柱支承接口正反扫滞回（≤ 0.15 nm，参照 ASML 专利 US 8,269,949 B2）[R28]；T2 装机重点考核双卡盘 WT-1/WT-2 夹持指纹差异（≤ 0.35 nm）与 50 μm 翘曲晶圆夹持残差（≤ 1.00 nm，直接对标 de Boeij 等，SPIE 8683，2013，Ref066 Fig. 10a）[R3]；T3 在双卡盘批曝下复核无背面微污染与夹持漂移。"),
    ]

    # =========================================================================
    # 10 RC & RH (Reticle Clamping, Pellicle & Reticle Thermal Conditioning) — NEW!
    # =========================================================================
    rc_t1 = [
        ("RC-T1-01", "掩模柔顺夹持重复装夹面内重复性 (X 向, 4×)", "≤ 0.72 nm", "离线干态台架，6 寸石英参考掩模连续卸载-重夹 ≥ 30 次，4× 掩模面内非可校形变重复性 X 向 3σ（1× 约 0.18 nm） [注 18]"),
        ("RC-T1-02", "掩模柔顺夹持重复装夹面内重复性 (Y 向, 4×)", "≤ 0.72 nm", "同上，4× 掩模面内非可校形变重复性 Y 向 3σ（1× 约 0.18 nm；参照分段柔顺夹持 JP 5,809,458 B2） [注 18]"),
        ("RC-T1-03", "Pellicle 防尘膜静态装配非可校变形 NCE (X 向, 1×)", "≤ 0.12 nm", "离线干态光学注册仪（PROVE 类）测软热熔胶垫装配 Pellicle 前后，经 iHOPC 拟扣后 X 向残余变形 NCE [注 18]"),
        ("RC-T1-04", "Pellicle 防尘膜静态装配非可校变形 NCE (Y 向, 1×)", "≤ 0.12 nm", "同上，测装配 Pellicle 前后经 iHOPC 拟扣后的 Y 向残余面内变形 NCE [注 18]"),
        ("RC-T1-05", "掩模下方微环境水平层流气幕温度稳定性", "≤ ±5.0 mK", "离线干态气幕测试台架，掩模下表面光学气隙层流气幕连续 24 h 稳态温控波动 3σ（对齐 Ref025） [注 18]"),
        ("RC-T1-06", "掩模上表面冷却气流速度空间均匀性", "≤ ±5.0%", "离线干态流场台架，掩模图案区上表面主动风冷气流流速空间均匀性 3σ [注 18]"),
        ("RC-T1-07", "RH 传片机械预对准重复性 (X 向, 4×)", "≤ 5.0 μm", "离线干态传片台架，掩模搬运机械手重复送片至 RS 吸盘的 X 向粗对准位置重复性 3σ（确保夹持接触区一致） [注 18]"),
        ("RC-T1-08", "RH 传片机械预对准重复性 (Y 向, 4×)", "≤ 5.0 μm", "同上，掩模搬运机械手重复送片至 RS 吸盘的 Y 向粗对准位置重复性 3σ [注 18]"),
    ]
    rc_t2 = [
        ("RC-T2-01", "装机掩模下方气隙热折射率畸变 (X 向)", "≤ 0.24 nm", "装机标称曝光热载下，掩模与物镜首片间气隙空气折射率梯度引起的单层 X 畸变 3σ [注 18]"),
        ("RC-T2-02", "装机掩模下方气隙热折射率畸变 (Y 向)", "≤ 0.24 nm", "同上，掩模下方气隙热折射率梯度引起的单层 Y 畸变 3σ [注 18]"),
        ("RC-T2-03", "Pellicle 高速扫描与吹扫气流动态变形 (X 向)", "≤ 0.14 nm", "装机 2.80 m/s 满速扫描与吹扫风速下，Pellicle 膜微振与压差诱发的 1× 等效 X 向动态套刻残差 3σ（对齐 Ref098） [注 18]"),
        ("RC-T2-04", "Pellicle 高速扫描与吹扫气流动态变形 (Y 向)", "≤ 0.14 nm", "同上，Pellicle 膜微振与吹扫压差诱发的 1× 等效 Y 向动态套刻残差 3σ（对齐 Ref098） [注 18]"),
        ("RC-T2-05", "RHC 掩模热控前馈常规工况残差 (X 向)", "≤ 0.43 nm", "装机常规生产剂量下，启用测温与 RHC 前馈（含 K4/K17/K18 协同）后的单层 X 残差 3σ [注 18]"),
        ("RC-T2-06", "RHC 掩模热控前馈常规工况残差 (Y 向)", "≤ 0.43 nm", "同上，常规工况启用 RHC 前馈后的单层 Y 残差 3σ [注 18]"),
        ("RC-T2-07", "RHC 极端满热工况抑制能力验证", "≤ 1.80 nm", "装机全视场/窄场极端高剂量热载（无控约 6.2 nm），启用动态 RHC 后压低至 ≤ 1.80 nm（对齐 Ref066 Fig. 5） [注 18]"),
    ]
    rc_t3 = [
        ("RC-T3-01", "连续 20 片高剂量升温爬坡段 RHC+PARIS 闭环稳定性", "爬坡无漂移", "整机连续高剂量批曝 ≥ 25 片（覆盖前 20 片掩模升温爬坡，对齐 Ref110 Fig. 4），片间场内套刻漂移受控 [注 18]"),
    ]
    rc_notes = [
        ("p", "**[注 18] 掩模夹持、薄膜与掩模热控系统（RC & RH）分级验收依据：**掩模侧套刻误差源于夹持变形、Pellicle 静/动变形及 193 nm 曝光吸热形变三类物理过程：① 柔顺夹持参照 JP 5,809,458 B2 与 Naaijkens（2013，Ref225）[R12, R28]，T1 离线管控 4× 重夹重复性 ≤ 0.72 nm（150 m/s^{2} 千趟微滑移接口在 RS-T1A-10/11 协同验收）；② Chen 等（Ref104）[R30] 证实软胶垫可大幅压低 Pellicle 静态装膜变形，van Haren 等（SPIE 10451，Ref098）[R30] 指出高速扫描与吹扫气流会诱发 Pellicle 动态畸变，故分设 T1 静态 NCE（≤ 0.12 nm）与 T2 动态（≤ 0.14 nm）；③ 掩模下方 5 mK 水平层流气幕抑制气隙折射率畸变（Fujishima 等，SPIE 8683，Ref025）[R31]；④ Lim 等（SPIE 9050，2014，Ref110 Fig. 4）[R29] 揭示批曝前 20 片存在显著升温爬坡，de Boeij 等（SPIE 8683，2013，Ref066 Fig. 5）[R3] 与 Kim 等（Ref016）[R24] 证实动态 RHC 可将 6.2 nm 极端热畸变压低至 ≤ 1.8 nm，故 T2 验收常规与极端 RHC 残差、T3 强制考核连续 20 片爬坡段闭环稳定性。"),
    ]

    # =========================================================================
    # 11 IL & LS (193 nm Light Source & FlexRay Illuminator) — NEW!
    # =========================================================================
    il_t1 = [
        ("IL-T1-01", "193.368 nm 中心波长长期与脉冲稳定性", "≤ ±0.05 pm", "离线 6 kHz ArF 光源台架，稳态输出中心波长漂移与波动 3σ（防色畸变与 K3 放大率偏移） [注 19]"),
        ("IL-T1-02", "激光光谱带宽 (E95) 稳定性", "≤ ±0.03 pm", "离线 6 kHz 光源台架，标称 E95 带宽（约 0.30 pm）连续批曝稳态波动 3σ（防高阶色像差漂移） [注 19]"),
        ("IL-T1-03", "FlexRay 多瞳面形状重复性", "≤ 0.20%", "离线照明台架，覆盖常规环形/偶极/C-quad 等 ≥ 14 种瞳面模式重复切换光强分布复现性（对齐 Ref007 Fig. 5a） [注 19]"),
        ("IL-T1-04", "照明瞳面质心远心角稳定性 (X 向)", "≤ 0.30 mrad", "离线照明台架，全瞳面切换与 24 h 运行期间主光线 X 向远心角偏移 3σ（防离焦耦合为水平套刻偏移） [注 19]"),
        ("IL-T1-05", "照明瞳面质心远心角稳定性 (Y 向)", "≤ 0.30 mrad", "同上，全瞳面切换与 24 h 运行期间主光线 Y 向远心角偏移 3σ [注 19]"),
        ("IL-T1-06", "26 × 5.5 mm 狭缝扫描向剂量重心偏移", "≤ 0.10 mm", "离线照明台架，狭缝内扫描向（Y）光强分布加权质心相对几何中心偏移（防改变有效 MA 积分窗中心） [注 19]"),
        ("IL-T1-07", "脉冲间积分曝光剂量稳定性", "≤ 0.30%", "离线 6 kHz 光源与剂量控台架，单场积分剂量重复性 3σ（抑制曝光热载荷随机波动） [注 19]"),
    ]
    il_t2 = [
        ("IL-T2-01", "中心波长动态调谐协同 K3 响应时间", "≤ 1.0 ms", "装机光源-物镜联动，波长微调指令下发至稳定到位时间，支撑 Lens-iHOPC K3 快速逐场刷新 [注 19]"),
        ("IL-T2-02", "波长调谐协同 K3 缩放线性残差", "≤ 0.012 nm/cm", "装机光源-物镜联动，标称波长调谐档位下对应像面 K3 实测与指令线性残差 [注 19]"),
        ("IL-T2-03", "跨照明模式切换瞳面极平衡稳定度 (X 极对)", "≤ 0.30%", "装机偶极/环形/C-quad 连续切换工况下，X 向左右极光强平衡度偏差 3σ（抑制与物镜奇像差交叉套刻漂移） [注 19]"),
        ("IL-T2-04", "跨照明模式切换瞳面极平衡稳定度 (Y 极对)", "≤ 0.30%", "同上，装机连续切换工况下，Y 向上下极光强平衡度偏差 3σ [注 19]"),
    ]
    il_t3 = [
        ("IL-T3-01", "整机跨照明切换满热连续曝光套刻稳定性", "跨瞳无突变", "整机高剂量批曝并执行偶极/环形跨照明切换，验证光源波长/瞳面稳度与物镜奇像差联动无异常套刻漂移 [注 19]"),
    ]
    il_notes = [
        ("p", "**[注 19] 193 nm 光源与 FlexRay 照明系统（IL & LS）套刻耦合机制与文献依据：**光源与照明系统虽不直接产生机械位移，但通过四条物理链路深度耦合至整机套刻：① 中心波长漂移经投影物镜横向色畸变直接诱发 K3 放大率偏移（Matsuyama 等，SPIE 6520，Ref051）[R32]，故 T1 严控中心波长 ≤ ±0.05 pm 并在 T2 验证波长快速调谐（≤ 1.0 ms）与物镜 K3 的线性协同；② 照明瞳面极平衡（Pole Balance）与质心偏移会与物镜奇像差（彗差/三叶草）交叉耦合，产生跨照明套刻偏移，Mulder 等（ASML & Carl Zeiss SMT，Ref007 Fig. 5a）[R32] 证实 FlexRay 在 14 种自由瞳面下复现性优于 0.16%，本表 T1 定限 ≤ 0.20%、T2 极平衡 ≤ 0.30%；③ 狭缝扫描向剂量分布不对称会偏移有效曝光积分窗（MA）重心（Heertjes 等，2024）[R8]，故 T1 约束狭缝重心偏移 ≤ 0.10 mm；④ 积分剂量波动直接调制掩模与晶圆热载荷。"),
    ]

    # =========================================================================
    # 12 MF & ENV (Metrology Frame, Isolation & Micro-Environment) — NEW!
    # =========================================================================
    mf_t1 = [
        ("MF-T1-01", "空气弹簧主隔振系统固有频率 (水平向)", "≤ 1.0 Hz", "离线隔振模块台架，Airmount 空气弹簧主隔振水平向固有频率实测（阻隔厂房地基微振，对齐 ME3 TT_L2_AM） [注 20]"),
        ("MF-T1-02", "空气弹簧主隔振系统固有频率 (垂向)", "≤ 1.0 Hz", "同上，Airmount 空气弹簧主隔振垂向固有频率实测 [注 20]"),
        ("MF-T1-03", "隔振系统高频地基振动传递率 (10–100 Hz)", "≤ −20 dB", "离线隔振模块台架，10–100 Hz 频段地基至计量框架（MF）的振动加速度传递率上限（对齐 Ref087） [注 20]"),
        ("MF-T1-04", "静音掩模台声罩声学隔离衰减量", "≥ 15 dB", "离线声学测试台架，RS 150 m/s^{2} 急加减速噪声向物镜与 MF 腔室辐射的宽带声压级衰减（对齐 Ref009） [注 20]"),
        ("MF-T1-05", "整机恒温气幕 (Air Shower) 出风温控稳度", "≤ ±10 mK", "离线环控风箱台架，主曝光区与 Gridplate 气幕连续 24 h 出风温度波动 3σ（对齐 Ref009） [注 20]"),
        ("MF-T1-06", "主曝光腔体局部气压控制稳定性", "≤ ±5.0 Pa", "离线环控压力模块台架，腔体气压闭环波动 3σ（抑制空气折射率 dn/dP 变化引发的光学缩放漂移） [注 20]"),
        ("MF-T1-07", "整机环控洁净空气相对湿度稳定性", "≤ ±1.0% RH", "离线环控台架，恒温恒湿气幕连续 24 h 湿度波动 3σ（防石英/微晶玻璃表面水膜吸附漂移） [注 20]"),
    ]
    mf_t2 = [
        ("MF-T2-01", "计量框架 (MF) 短期热机械基准漂移 (X 向)", "≤ 0.18 nm", "装机全机通电恒温 10 mK 气幕下，15 min 内 MF 相对光学基准面的 X 向微变形漂移 3σ [注 20]"),
        ("MF-T2-02", "计量框架 (MF) 短期热机械基准漂移 (Y 向)", "≤ 0.18 nm", "同上，15 min 内 MF 相对光学基准面的 Y 向微变形漂移 3σ [注 20]"),
        ("MF-T2-03", "计量框架 (MF) 24 h 长期热机械漂移 (X 向)", "≤ 0.50 nm", "装机恒温运行 24 h 内 MF 相对基准面 X 向热机械漂移 3σ（为 M-to-E 与 Gridplate 长稳提供基础） [注 20]"),
        ("MF-T2-04", "计量框架 (MF) 24 h 长期热机械漂移 (Y 向)", "≤ 0.50 nm", "同上，24 h 内 MF 相对基准面 Y 向热机械漂移 3σ [注 20]"),
        ("MF-T2-05", "整机地基/声学激励下物镜与框架动态微振 (X 向)", "≤ 0.129 nm", "装机满速双台扫描与厂房标称地基谱下，经隔振与声罩抑制后传至物镜像面的 X 向动态微振 1× 残差 3σ [注 20]"),
        ("MF-T2-06", "整机地基/声学激励下物镜与框架动态微振 (Y 向)", "≤ 0.129 nm", "同上，装机满速双台扫描与标称地基谱下传至物镜像面的 Y 向动态微振 1× 残差 3σ [注 20]"),
        ("MF-T2-07", "整机动态近距传感通道无机械短路复核", "无动态短路", "装机核查 Baseframe 与 Metroframe 间全线缆/水管解耦，无额外低频动态捷径传递（对齐 ME3 AM 规程） [注 20]"),
    ]
    mf_t3 = [
        ("MF-T3-01", "整机双卡盘 SYCO / LOCO 参考零点一致性 (X 向)", "≤ 0.17 nm", "整机双台交换工况，启用 SYCO/LOCO 跨卡盘参考匹配后 X 向残余零点偏差 3σ（对齐 Ref100） [注 20]"),
        ("MF-T3-02", "整机双卡盘 SYCO / LOCO 参考零点一致性 (Y 向)", "≤ 0.17 nm", "同上，启用 SYCO/LOCO 跨卡盘参考匹配后 Y 向残余零点偏差 3σ（对齐 Ref100） [注 20]"),
        ("MF-T3-03", "整机连续 24 h 环境漂移全流程稳定性复核", "24 h 无超差", "整机在正常厂房温压波动下连续运行 24 h，复测 M-to-E 与双卡盘套刻稳定性满足红线 [注 20]"),
    ]
    mf_notes = [
        ("p", "**[注 20] 计量框架、隔振与整机微环境系统（MF & ENV）分级验收依据：**计量框架（Metroframe）与恒温气幕（Air Shower）是全机 ENC 栅格板、投影物镜、AA 对准头及 TIS/PARIS 共同挂载的物理底盘，任何微小的热机械弯曲、气压突变或声学微振都会同步耦合至多个子系统。Castenmiller 等（SPIE 7640，2010，Ref009）[R2] 披露 NXT 平台采用 10 mK 气幕温控与静音掩模台声罩（Silent RS & acoustic shielding）；ASML 手册 *TT_L2_AM-3v0* 与 Takahashi 等（Ref087）[R33] 给出 < 1 Hz 空气弹簧隔振与防止 Baseframe–Metroframe 动态机械短路的装机验收规范。T1 离线考核隔振频率、声罩衰减及 10 mK / ±5 Pa 环控单件能力；T2 装机考核 MF 短期（≤ 0.18 nm）与 24 h（≤ 0.50 nm）热机械稳度及整机微振残差；T3 考核双卡盘 SYCO/LOCO 参考零点一致（Duclaux 等，Ref100）[R18] 与 24 h 全机环境稳定性。"),
    ]

    # =========================================================================
    # COMPLETE 12-SUBSYSTEM STRUCTURED LIST
    # =========================================================================
    return [
        {
            "code": "01_WS", "doc_code": "OV4-SRS-NXT1965Ci-01-WS-V1",
            "filename": "01_WS晶圆台_套刻预算规格需求书_v1.docx",
            "short_name": "WS（晶圆台，含 WRS 与运动 iHOPC）", "ch_num": 1,
            "ch_title": "第 1 章　WS（晶圆台）子系统规格需求（含 WRS 与 iHOPC 运动补偿）",
            "standalone_title": "ASML NXT:1965Ci WS（晶圆台）子系统套刻预算规格需求书",
            "standalone_subtitle": "WS 单台干态（T1-A / T1-B）与 WRS 双台同步及 iHOPC 运动补偿（T2-A / T2-B）验收规格",
            "recipient": "WS（晶圆台）子系统研发、控制与测试团队（含 WRS 同步联合验收接口）",
            "stage_scope": "T1-A（干态匀速）→ T1-B（干态单台 iHOPC）→ T2-A（双台同步）→ T2-B（双台 iHOPC）",
            "coupling_rows": [
                ("离线干态 vs 装机湿区流场/声学耦合", "T1-A/T1-B 离线干态台架无浸没头与超纯水液膜；装机 E 侧 0.70 m/s 满速扫场时，弯液面拖曳力波动、供回水脉动及结构隔振声学传递均直接叠加于 WS 伺服误差。"),
                ("WS–RS 主从同步与相对 iHOPC 耦合", "WS（Master）误差经同步前馈馈入 RS（Slave），最终决定曝光套刻的是 1× 相对轨迹 Δq(y) = q_{WS}(y) − M_{opt}·q_{RS}(y)；单台 T1-A/T1-B 合格后必须经 T2-A/T2-B 双台联合考核。"),
                ("WS 闭环 vs ENC 传感链盲区耦合", "WS 离线闭环以 ENC 读数为反馈，无法察觉编码器自身噪声、Gridplate 7 天热漂与过缝 Handover 跳变；须以 ENC 验收合格为前提并辅以外部独立干涉仪复核。"),
            ],
            "tables": [
                ("1.1", "T1-A 验收项目（WS 单台干态常规匀速扫描与静止稳定性验收，面内 3-DOF）", "指标项", [2.4, 4.5, 2.8, 8.3], ws_t1a),
                ("1.2", "T1-B 验收项目（WS 单台干态 iHOPC 多项式轨迹独立跟踪能力验收，11 项）", "指标项", [2.4, 4.5, 2.8, 8.3], ws_t1b),
                ("1.3", "T2-A 验收项目（T2-WRS 双台同步性能验收）", "指标项", [2.4, 4.5, 2.8, 8.3], wrs_t2a),
                ("1.4", "T2-B 验收项目（T2-WRS-iHOPC 11 项运动补偿整机最终像面精度验收）", "指标项", [2.4, 4.5, 2.8, 8.3], wrs_t2b),
            ],
            "notes_master": ws_notes, "notes_standalone": ws_notes,
            "figures": [
                ("pair", "009_fig10", "图 1-1：NXT:1950i 实测双台同步误差 Sync MA-X = 0.47 nm / MA-Y = 0.49 nm（来源：Castenmiller 等，SPIE 7640，Ref009 Fig. 10 [R2]）",
                         "022_fig1", "图 1-2：WS（主台 Master）误差经前馈通道送入 RS（从台 Slave）的双台同步控制架构（来源：Heertjes 等，Control Eng. Pract.，2013，Ref022 Fig. 1 [R5]）"),
            ],
        },
        {
            "code": "02_RS", "doc_code": "OV4-SRS-NXT1965Ci-02-RS-V1",
            "filename": "02_RS掩模台_套刻预算规格需求书_v1.docx",
            "short_name": "RS（掩模台，4× 掩模侧）", "ch_num": 2,
            "ch_title": "第 2 章　RS（掩模台）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci RS（掩模台）子系统套刻预算规格需求书",
            "standalone_subtitle": "RS 单台干态匀速扫描、微滑移（T1-A）与 iHOPC 多项式轨迹（T1-B）验收规格（4× 掩模侧）",
            "recipient": "RS（掩模台）子系统研发、控制与测试团队",
            "stage_scope": "T1-A（干态 4× 匀速扫描与微滑移）→ T1-B（干态 4× 单台 iHOPC）→ 装机并入 WRS T2 联调",
            "coupling_rows": [
                ("RS 从台（Slave）与 WS 主台（Master）高速同步耦合", "离线 T1 仅测试 RS 自身跟踪能力；装机后 RS 须高带宽实时跟从 WS 误差前馈与动态 iHOPC 指令，RS 带宽裕度与相移直接影响整机同步与高阶像面残差。"),
                ("150 m/s^{2} 高加减速引发的掩模微滑移与热变形耦合", "高加减速引起的石英掩模相对吸盘微滑移对机内编码器完全不可见，且装机 193 nm 曝光热载会叠加掩模面内热变形，须经外部标尺微滑移测试与在机 PARIS 闭环协同拦截。"),
                ("Rz 偏航角 1:1 透传与反作用力声学/微振耦合", "X/Y 平移经 4:1 光学缩小，但 RS 偏航角 Rz 按 1:1 直接映射至晶圆像面；150 m/s^{2} 折返反作用力与气动噪声向 MF/物镜的耦合须在装机 T2 联合复核。"),
            ],
            "tables": [
                ("2.1", "T1-A 验收项目（RS 单台干态常规匀速扫描与微滑移验收，4× 掩模侧口径）", "指标项", [2.4, 4.5, 2.8, 8.3], rs_t1a),
                ("2.2", "T1-B 验收项目（RS 单台干态 iHOPC 多项式轨迹独立跟踪能力验收，4× 掩模侧口径）", "指标项", [2.4, 4.5, 2.8, 8.3], rs_t1b),
            ],
            "notes_master": rs_notes_master, "notes_standalone": rs_notes_standalone,
            "figures": [
                ("single", "075_fig13", "图 2-1：WS/RS 相对伺服误差累积频谱实测对比（虚线为无耦合，实线为同步耦合；来源：Evers 等，Control Eng. Pract. 83，2019，Ref075 Fig. 13 [R6]）", None, None),
            ],
        },
        {
            "code": "03_ENC", "doc_code": "OV4-SRS-NXT1965Ci-03-ENC-V1",
            "filename": "03_ENC光栅编码器_套刻预算规格需求书_v1.docx",
            "short_name": "ENC（二维光栅编码器测量）", "ch_num": 3,
            "ch_title": "第 3 章　ENC（光栅编码器测量）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci ENC（光栅编码器）子系统套刻预算规格需求书",
            "standalone_subtitle": "纯传感器离线本底（T1）与 Gridplate 长期稳定性及读数头切换 Handover（T2）验收规格",
            "recipient": "ENC（二维光栅编码器测量）子系统光学、电子学与标定团队",
            "stage_scope": "T1（干态刚性锁死传感器本底与 PSD）→ T2（装机 MF 7 天稳定性与跨缝 Handover）",
            "coupling_rows": [
                ("传感器噪声频谱 vs 运动台伺服闭环耦合", "离线 T1 静态噪声仅反映刚性锁死下的本底；装机后 ENC 低频有色噪声会被 WS/RS 伺服闭环当作真实位置误差反向写入晶圆位移，高频噪声影响伺服稳定裕度，故 T1 须附全频段 PSD/CPS。"),
                ("Gridplate vs 计量框架（MF）热机械与气幕环境耦合", "离线单点光栅测试无法反映整块大尺寸 Gridplate 安装于 MF 底部、在 10 mK 恒温气幕与整机曝光热流下连续 7 天的长期全局网格漂移，必须在 T2 阶段以外部参考片/多移位法独立验收。"),
                ("读数头拼接切换（Handover）vs 双台交换路径耦合", "双台交换与跨光栅分块区域时发生读数头接管切换，任何瞬态跳变或零点衔接误差都会被伺服闭环吸收为虚假定位，必须通过 T2 Handover 专项考核拦截。"),
            ],
            "tables": [
                ("3.1", "T1 验收项目（纯 ENC 传感器离线干态测量本底验收）", "指标项", [2.4, 4.5, 2.8, 8.3], enc_t1),
                ("3.2", "T2 验收项目（Gridplate 长期稳定性与读数头切换 Handover 验收）", "指标项", [2.4, 4.5, 2.8, 8.3], enc_t2),
            ],
            "notes_master": enc_notes, "notes_standalone": enc_notes,
            "figures": [
                ("pair", "009_fig4", "图 3-1：NXT 短固定光程（< 15 mm）二维光栅编码器 1000 Hz 噪声实测 0.22 nm 3σ（来源：Castenmiller 等，SPIE 7640，Ref009 Fig. 4 [R2]）",
                         "062_fig11", "图 3-2：Gridplate 连续一周（12 h–156 h）X/Y 全局网格热机械稳定性实测 < 0.20 nm（来源：de Jong 等，SPIE 7274，2009，Ref062 Fig. 11 [R14]）"),
            ],
        },
        {
            "code": "04_AA", "doc_code": "OV4-SRS-NXT1965Ci-04-AA-V1",
            "filename": "04_AA晶圆对准_套刻预算规格需求书_v1.docx",
            "short_name": "AA（M-side 晶圆对准）", "ch_num": 4,
            "ch_title": "第 4 章　AA（晶圆对准）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci AA（晶圆对准）子系统套刻预算规格需求书",
            "standalone_subtitle": "传感器静态本底（T1）、模拟 M-side 动态 HOWA（T2）与整机 M-to-E 基线（T3）验收规格",
            "recipient": "AA（M-side 晶圆对准）子系统光学、算法与集成团队",
            "stage_scope": "T1（干态超稳台静态本底）→ T2（干态模拟 M-side 动态与 HOWA）→ T3（跨 MF 框架 M-to-E 漂移）",
            "coupling_rows": [
                ("AA 光学传感 vs M 侧晶圆台高速步进折返耦合（T1 → T2）", "离线超稳台架（T1）无宏动加减速激振与正反扫方向切换；进入模拟 M 侧量测端（T2）后，扫描动态噪声与正反扫方向混叠（SUSD）可放大至纳米级虚假高阶网格，须通过 T2 动态扫描与配平 HOWA 考核拦截。"),
                ("四色多波长通道稳度 vs 工艺膜层标记不对称耦合", "产线工艺膜层不对称依赖多波长通道差值解耦；若 AA 自身 4 通道 24 h 色间漂移超标，会被整机误判为晶圆工艺形变并错误反馈至曝光网格。"),
                ("M 侧 AA vs 整机 MF 框架与 E 侧曝光基准耦合（T2 → T3）", "M 侧对准得到的晶圆网格必须跨计量框架（MF）传递至 E 侧物镜/TIS 曝光工位；M-to-E 相对机械/热基线漂移仅在双台整机环境（T3）下显现，离线 T1/T2 无法替代。"),
            ],
            "tables": [
                ("4.1", "T1 验收项目（AA 底层传感器离线干态超稳平台验收，3 项不分 X/Y）", "指标项", [2.4, 4.5, 2.8, 8.3], aa_t1),
                ("4.2", "T2 验收项目（模拟 M-side 干态量测端 FIWA / HOWA 集成验收）", "指标项", [2.4, 4.5, 2.8, 8.3], aa_t2),
                ("4.3", "T3 验收项目（双台整机联调 M-to-E 对准基线短期漂移验收）", "指标项", [2.4, 4.5, 2.8, 8.3], aa_t3),
            ],
            "notes_master": aa_notes, "notes_standalone": aa_notes,
            "figures": [
                ("pair", "015_fig10", "图 4-1：SMASH 对准重复性随信号质量 WQ 变化实测（WQ≥1% 约 0.15–0.25 nm；WQ 0.1–1% 约 0.25–0.50 nm；来源：de Graaf 等，SPIE 9780，2016，Ref015 Fig. 10 [R15]）",
                         "252_fig3", "图 4-2：多波长加权融合（OCW）较单色方案将晶圆间套刻波动压低 0.8 nm 实测对比（来源：Menchtchikov 等，SPIE 10587，2018，Ref252 Fig. 3 [R16]）"),
            ],
        },
        {
            "code": "05_TIS+PARIS", "doc_code": "OV4-SRS-NXT1965Ci-05-TP-V1",
            "filename": "05_TIS与PARIS空间像传感_套刻预算规格需求书_v1.docx",
            "short_name": "TIS + PARIS（E-side 空间像传感）", "ch_num": 5,
            "ch_title": "第 5 章　TIS + PARIS（E-side 空间像传感）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci TIS + PARIS（E-side 空间像传感）子系统套刻预算规格需求书",
            "standalone_subtitle": "E-side 193 nm 实机湿区空间像对准、双台匹配与奇像差波前测量（T1）验收规格",
            "recipient": "TIS + PARIS（E-side 空间像对准与在机波前传感）子系统研发与集成团队",
            "stage_scope": "T1 单级在机湿区验收（E-side 193 nm 曝光光路 + 超纯水浸没 + 双台交换）",
            "coupling_rows": [
                ("传感器本体 vs E 侧 193 nm 曝光光路及超纯水液膜耦合", "TIS 与 PARIS 物理上必须透过投影物镜与浸没超纯水读取 193 nm 实机空间像，离线无光路/无液膜测试无法代表真实曝光工况，且供回水流量波动会直接调制 TIS 测位重复性。"),
                ("双晶圆台 TIS-1 / TIS-2 切换 vs 双卡盘套刻差耦合", "两台晶圆卡盘各自的 TIS 基准板相对漂移会直接映射为双卡盘低阶畸变偏置（K7/K12/K13），须在双台交换实机工况下考核 24 h 相对匹配稳定性。"),
                ("PARIS 波前量测 vs 物镜奇像差闭环调控耦合", "PARIS 在机波前测量重复性（≤ 0.14 nm RMS）是投影物镜 LensModel 闭环调整的 1:3 计量前提，其偏差将直接影响物镜在线调控残差。"),
            ],
            "tables": [
                ("5.1", "T1 验收项目（E-side 在机空间像对准与奇像差波前测量验收）", "指标项", [2.4, 4.5, 2.8, 8.3], tp_t1),
            ],
            "notes_master": tp_notes, "notes_standalone": tp_notes,
            "figures": [
                ("pair", "066_fig6", "图 5-1：PARIS 7 视场点并行空间像传感器结构示意（支持每片 3 扫，公开 RA < 0.50 nm；来源：de Boeij 等，SPIE 8683，2013，Ref066 Fig. 6 [R3]）",
                         "100_fig9", "图 5-2：双卡盘（C2 vs C1）未匹配时诱发的 K7/K13/K12 低阶偏置实测（来源：Duclaux 等，SPIE 11325，2020，Ref100 Fig. 9 [R18]）"),
            ],
        },
        {
            "code": "06_Lens", "doc_code": "OV4-SRS-NXT1965Ci-06-LENS-V1",
            "filename": "06_Lens投影物镜_套刻预算规格需求书_v1.docx",
            "short_name": "Lens（投影物镜，NA = 1.35）", "ch_num": 6,
            "ch_title": "第 6 章　Lens（投影物镜）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci Lens（投影物镜）子系统套刻预算规格需求书",
            "standalone_subtitle": "冷机湿态波前上限（T1）、LensModel 调节残差（T2-A）与 Lens-iHOPC 量程/精度双表（T2-B / T2-C）",
            "recipient": "Lens（193 nm / NA = 1.35 投影物镜与操纵器）子系统光学、精密机械与控制团队",
            "stage_scope": "T1（离线局部静态水池 wet PMI）→ T2-A（LensModel 调后残差）→ T2-B（iHOPC 量程）→ T2-C（精度与动态）",
            "coupling_rows": [
                ("冷机离线静态 wet PMI vs 装机 193 nm 曝光热载与气压耦合（T1 → T2）", "离线 T1 静态局部水池仅验证冷机绝对波前本底；装机连续曝光后，高功率极轴照明引发的非旋转对称镜片热致像差/畸变与气压微变，须依赖在机 LensModel 与 PARIS 闭环动态修正（T2-A）。"),
                ("多 K 参共用镜片操纵器 vs 串扰/奇像差/行程饱和耦合", "8 项激活 Lens-iHOPC 共用有限镜片微动执行器矩阵；单参数满量程动作可能诱发非目标 K 项串扰、奇像差恶化或联合行程饱和，必须在 T2-B（量程）与 T2-C（精度与动态）双表并行约束。"),
                ("动态物镜项（K9/K15/K17/K18）vs WRS 扫描节拍相位耦合", "扫描中动态随动的 4 项混合 K 参数必须与 0.70 m/s 双台扫描精准同步触发（相位滞后 ≤ 0.20 ms），否则动态补偿将在狭缝内错位反而放大套刻误差。"),
            ],
            "tables": [
                ("6.1", "T1 验收项目（离线冷机静态波前上限与 K20 静畸变，λ = 193.368 nm）", "指标项（Fringe Zernike 系数，193 nm）", [2.2, 3.5, 2.7, 9.6], ln_t1),
                ("6.2", "T2-A 验收项目（任意一次 LensModel 调节后的奇像差调节残差验收）", "指标项（Fringe Zernike 系数，调节残差）", [2.4, 3.8, 2.7, 9.1], ln_t2a),
                ("6.3", "T2-B 验收项目（动态 Lens-iHOPC 补偿调节范围 Range 验收表）", "指标项", [2.4, 4.9, 2.9, 7.8], ln_t2b_range),
                ("6.4", "T2-C 验收项目（动态 Lens-iHOPC K 参数调节精度与套刻相关动态考核表）", "指标项", [2.4, 4.9, 2.9, 7.8], ln_t2c_prec),
            ],
            "notes_master": ln_notes, "notes_standalone": ln_notes,
            "figures": [
                ("pair", "024_fig11", "图 6-1：FlexWave 波前控制后各奇像差残差实测（Coma X/Y 约 0.16 nm RMS；来源：Staals 等，SPIE 7973，2011，Ref024 Fig. 11 [R22]）",
                         "253_fig8", "图 6-2：物镜畸变操纵器沿 −13..+13 mm 狭缝 Target (SET) vs Measured (GET) 实测残差（来源：Klinkhamer 等，ASML/Zeiss，Ref253 Fig. 8 [R23]）"),
            ],
        },
        {
            "code": "07_IH", "doc_code": "OV4-SRS-NXT1965Ci-07-IH-V1",
            "filename": "07_IH浸没液控系统_套刻预算规格需求书_v1.docx",
            "short_name": "IH（浸没头与超纯水液控系统）", "ch_num": 7,
            "ch_title": "第 7 章　IH（浸没头与超纯水液控）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci IH（浸没头与超纯水液控）子系统套刻预算规格需求书",
            "standalone_subtitle": "离线液控单件（T1）、E-side 水膜折射率与 TIS 联动（T2）及双卡盘湿区连续曝光（T3）验收规格",
            "recipient": "IH（浸没头、气刀与超纯水供应控制）子系统流体、热控与集成团队",
            "stage_scope": "T1（离线独立湿态液控台架）→ T2（装机 E-side 水膜畸变与流量-TIS 联调）→ T3（整机湿区满速批曝）",
            "coupling_rows": [
                ("离线稳态供水 vs 装机 300 μm 热边界层折射率梯度耦合", "离线 T1 进口水温 ±3.0 mK 合格后，装机高速扫描与 193 nm 曝光热载下，物镜末片下方 300 μm 水膜仍可产生局部温差与折射率梯度畸变，必须在 T2 实机评估单层套刻贡献。"),
                ("供回水流量脉动 vs E 侧 TIS 测位重复性及 WS 伺服耦合", "供回水脉动与浸没头弯液面压脉不仅直接作用在 WS 上表面，还会调制 E 侧 TIS 透射空间像测位重复性（Ref164），必须在 T2 开展流量扫频-TIS 联动复核。"),
                ("高速跨晶圆边缘扫场 vs 残余水膜蒸发冷缩耦合（T2 → T3）", "离线模拟台架难以完全复现双卡盘连续批曝的边缘弯液面穿越与表面蒸发降温过程，必须在 T3 整机连续湿区曝光下复核边缘区无蒸发冷缩突变。"),
            ],
            "tables": [
                ("7.1", "T1 验收项目（离线独立湿态液控台架单件性能验收）", "指标项", [2.4, 4.6, 2.7, 8.3], ih_t1),
                ("7.2", "T2 验收项目（装机 E-side 水膜畸变、流量-TIS 联动与批内稳定验收）", "指标项", [2.4, 4.6, 2.7, 8.3], ih_t2),
                ("7.3", "T3 验收项目（整机双卡盘满速湿区连续曝光边缘一致性验收）", "指标项", [2.4, 4.6, 2.7, 8.3], ih_t3),
            ],
            "notes_master": ih_notes, "notes_standalone": ih_notes,
            "figures": [
                ("single", "021_fig1", "图 7-1：NA = 1.35 浸没头双层水约束（Meniscus Stability）与外圈气刀（Air Curtain）结构原理（来源：de Klerk 等，SPIE 6520，2007，Ref021 Fig. 1 [R25]）", None, None),
            ],
        },
        {
            "code": "08_WT_WH", "doc_code": "OV4-SRS-NXT1965Ci-08-WTWH-V1",
            "filename": "08_WT-TC与WH晶圆温控传片_套刻预算规格需求书_v1.docx",
            "short_name": "WT-TC & WH（晶圆温控与传片预处理）", "ch_num": 8,
            "ch_title": "第 8 章　WT-TC & WH（晶圆温控与传片预处理）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci WT-TC & WH（晶圆温控与传片预处理）套刻预算规格需求书",
            "standalone_subtitle": "离线干态热控与 TSU（T1）、装机热瞬态与曝光热补偿（T2）及双台热史批曝（T3）验收规格",
            "recipient": "WT-TC（晶圆台热控）与 WH（晶圆传片及 TSU 预调温）子系统热控与机械团队",
            "stage_scope": "T1（离线干态水冷/分区加热/TSU）→ T2（装机 M-to-E 热瞬态与热补偿残差）→ T3（正反序热史批曝）",
            "coupling_rows": [
                ("离线静态均温 vs 装机 M-to-E 传片热瞬态与吸片衰减耦合", "离线 T1 验证 TSU 出片 ±15 mK 与台面均温 ≤ 80 mK；装机高速产线节拍（≥ 250 wph）下，硅片从传片、M 侧对准到 E 侧曝光之间的残留瞬态温漂会直接按 0.39 nm/mK 转化为非线性套刻偏差。"),
                ("曝光吸收热载荷 + 浸没蒸发冷缩 vs 分区加热补偿模型耦合", "E 侧同时叠加 193 nm 激光脉冲加热与浸没弯液面蒸发冷却，形成强空间非均匀热场，离线干态无热/液载荷无法验证，必须在 T2 考核热控补偿残差。"),
                ("双卡盘温场一致性与扫描场序热史耦合（T2 → T3）", "两只卡盘的温场微小差异会放大双卡盘套刻差，且正向/反向场序会改变热累积方向，必须在 T3 执行正序/倒序扫描热史差分验证。"),
            ],
            "tables": [
                ("8.1", "T1 验收项目（离线干态晶圆台热控与 WH 预调温单元单件验收）", "指标项", [2.4, 4.6, 2.7, 8.3], wt_t1),
                ("8.2", "T2 验收项目（装机热瞬态、曝光热补偿残差与双台温场一致验收）", "指标项", [2.4, 4.6, 2.7, 8.3], wt_t2),
                ("8.3", "T3 验收项目（整机连续满热批曝正序/倒序扫描热史验证）", "指标项", [2.4, 4.6, 2.7, 8.3], wt_t3),
            ],
            "notes_master": wt_notes, "notes_standalone": wt_notes,
            "figures": [
                ("single", "017_fig2", "图 8-1：无线 SensArray 测温晶圆自 Pre-align & TSU 经 Measure side 至 Exposure side 全流程温度演化实测（来源：Ha 等，2013，Ref017 Fig. 2 [R27]）", None, None),
            ],
        },
        {
            "code": "09_WC", "doc_code": "OV4-SRS-NXT1965Ci-09-WC-V1",
            "filename": "09_WC晶圆夹持系统_套刻预算规格需求书_v1.docx",
            "short_name": "WC（晶圆夹持与台面接口系统）", "ch_num": 9,
            "ch_title": "第 9 章　WC（晶圆夹持与台面接口）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci WC（晶圆夹持与台面接口）子系统套刻预算规格需求书",
            "standalone_subtitle": "离线干态重夹/微滑移/长柱滞回（T1）、装机双卡盘与翘曲片（T2）及双盘批曝（T3）验收规格",
            "recipient": "WC（真空瘤点吸盘与 WT–MB 接口）子系统精密机械与工艺材料团队",
            "stage_scope": "T1（离线干态重夹/微滑移/WT–MB 滞回）→ T2（装机双盘指纹差与 50 μm 翘曲片）→ T3（双盘批曝复核）",
            "coupling_rows": [
                ("标准参考片离线夹持 vs 50 μm 翘曲工艺片面内变形耦合", "离线 T1 采用低翘曲标准片验证吸片本底；装机面对高应力 50 μm 翘曲晶圆时，背面摩擦滞回与瘤点支承变形会放大面内套刻残差，必须在 T2 以标准翘曲测试片专项考核。"),
                ("单卡盘重复性 vs 双卡盘 WT-1 / WT-2 静态指纹差异耦合", "单只吸盘自身重夹合格（≤ 0.30 nm）不代表两只吸盘面内变形指纹一致；装机双台交替曝光时，双盘夹持差直接贡献双卡盘套刻差，必须在 T2/T3 跨盘比对。"),
                ("吸盘真空力 + 运动台加减速惯性力 vs 背面微滑移与长柱滞回耦合", "35–40 m/s^{2} 往返折返惯性力与正反扫剪力同时作用于硅片背面和 WT–MB 柔顺支承接口，必须在 T1 满载往返与 T2 装机环境下联合复核。"),
            ],
            "tables": [
                ("9.1", "T1 验收项目（离线干态吸盘重复夹持、背面微滑移与 WT–MB 接口验收）", "指标项", [2.4, 4.6, 2.7, 8.3], wc_t1),
                ("9.2", "T2 验收项目（装机双卡盘夹持指纹差异与 50 μm 翘曲测试片验收）", "指标项", [2.4, 4.6, 2.7, 8.3], wc_t2),
                ("9.3", "T3 验收项目（整机双卡盘连续批曝夹持稳定性复核）", "指标项", [2.4, 4.6, 2.7, 8.3], wc_t3),
            ],
            "notes_master": wc_notes, "notes_standalone": wc_notes,
            "figures": [
                ("single", "066_fig10a", "图 9-1：改进型晶圆台面（Improved WT）对 50 μm 翘曲晶圆焦面与面内套刻残差（1.2 nm → 1.0 nm）实测改善（来源：de Boeij 等，SPIE 8683，2013，Ref066 Fig. 10a [R3]）", None, None),
            ],
        },
        {
            "code": "10_RC_RH", "doc_code": "OV4-SRS-NXT1965Ci-10-RCRH-V1",
            "filename": "10_RC与RH掩模夹持及热控_套刻预算规格需求书_v1.docx",
            "short_name": "RC & RH（掩模夹持、薄膜与掩模热控）", "ch_num": 10,
            "ch_title": "第 10 章　RC & RH（掩模夹持、薄膜与掩模热控）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci RC & RH（掩模夹持、薄膜与掩模热控）套刻预算规格需求书",
            "standalone_subtitle": "离线干态夹持/Pellicle/气幕（T1）、装机 RHC 常规/极热与动态薄膜（T2）及 20 片爬坡（T3）验收规格",
            "recipient": "RC（掩模夹持与热控气幕）及 RH（掩模传片）子系统机械、热控与控制团队",
            "stage_scope": "T1（离线重夹/静态 Pellicle/5 mK 气幕）→ T2（装机气隙畸变/动态 Pellicle/RHC）→ T3（20 片爬坡闭环）",
            "coupling_rows": [
                ("离线冷态重夹与静态 Pellicle vs 装机 193 nm 曝光热载与吹扫耦合", "离线 T1 验证冷态重夹与静态装膜 NCE；装机连续高剂量曝光下，掩模吸热膨胀与 2.80 m/s 高速扫描吹扫会叠加显著高阶热畸变（无控可达 6.2 nm）及 Pellicle 气动微振，须在 T2 实机验收。"),
                ("掩模下气隙层流气幕 vs 投影物镜首片光学路径耦合", "掩模下方空气隙处于 4× 成像主光路内，气幕温控波动或层流扰动会直接形成空气折射率梯度畸变，须在 T1 稳温与 T2 装机热载下双重验证。"),
                ("批曝前 20 片升温爬坡 vs RHC 前馈 + PARIS 7 点闭环耦合（T2 → T3）", "单场或稳态测试无法替代连续批曝瞬态升温过程，必须在 T3 整机连续高剂量曝光前 20 片爬坡段验收 RHC + PARIS + Lens/WRS 协同闭环稳定性。"),
            ],
            "tables": [
                ("10.1", "T1 验收项目（离线干态掩模柔顺夹持、静态 Pellicle、气幕与传片验收）", "指标项", [2.4, 4.7, 2.7, 8.2], rc_t1),
                ("10.2", "T2 验收项目（装机气隙畸变、Pellicle 动态及 RHC 常规/极热补偿验收）", "指标项", [2.4, 4.7, 2.7, 8.2], rc_t2),
                ("10.3", "T3 验收项目（整机连续 20 片高剂量升温爬坡段 RHC+PARIS 闭环验收）", "指标项", [2.4, 4.7, 2.7, 8.2], rc_t3),
            ],
            "notes_master": rc_notes, "notes_standalone": rc_notes,
            "figures": [
                ("pair", "066_fig5", "图 10-1：动态掩模热控（RHC）在全视场/窄场高热载下将套刻畸变由 6.2 nm 压低至 1.8–1.9 nm 实测（来源：de Boeij 等，SPIE 8683，2013，Ref066 Fig. 5 [R3]）",
                         "110_fig4", "图 10-2：批次连续曝光与换片冷却循环下的掩模升温爬坡曲线（前 20 片为关键瞬态爬坡区；来源：Lim 等，SPIE 9050，2014，Ref110 Fig. 4 [R29]）"),
            ],
        },
        {
            "code": "11_IL_LS", "doc_code": "OV4-SRS-NXT1965Ci-11-ILLS-V1",
            "filename": "11_IL与LS光源及FlexRay照明_套刻预算规格需求书_v1.docx",
            "short_name": "IL & LS（193 nm 光源与 FlexRay 照明）", "ch_num": 11,
            "ch_title": "第 11 章　IL & LS（193 nm 光源与 FlexRay 照明）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci IL & LS（光源与 FlexRay 照明）套刻预算规格需求书",
            "standalone_subtitle": "离线波长/带宽/瞳面/狭缝重心（T1）、装机波长-K3 与极平衡联调（T2）及跨照明批曝（T3）验收规格",
            "recipient": "LS（193 nm ArF 准分子光源）与 IL（FlexRay 自由瞳面照明）子系统光学与控制团队",
            "stage_scope": "T1（离线光学台架波长/瞳面/狭缝重心）→ T2（装机波长-K3 协同与极平衡）→ T3（跨照明高剂量联调）",
            "coupling_rows": [
                ("激光中心波长稳度/调谐 vs 投影物镜 K3 缩放与色畸变耦合", "离线 T1 考核中心波长稳度 ≤ ±0.05 pm；装机后激光波长作为物镜 K3 毫秒级微调执行通道，其响应速度（≤ 1.0 ms）与线性残差须在 T2 与物镜联合验收。"),
                ("FlexRay 瞳面极平衡与远心角 vs 物镜奇像差交叉耦合", "瞳面极平衡漂移或远心角偏移单独看似微小，但在装机环境下与物镜奇像差（彗差/三叶草）交叉耦合会直接转化为跨照明套刻漂移，须经 T2 极平衡与 T3 跨照明切换联调验证。"),
                ("狭缝扫描向剂量重心与脉冲能量波动 vs 曝光窗 MA 及热载荷耦合", "狭缝扫描向光强重心偏移会改变有效滑窗积分中心并耦合运动台同步误差，脉冲能量波动则直接扰动掩模/晶圆热载荷稳态。"),
            ],
            "tables": [
                ("11.1", "T1 验收项目（离线光源波长、带宽、FlexRay 瞳面与狭缝重心验收）", "指标项", [2.4, 4.7, 2.7, 8.2], il_t1),
                ("11.2", "T2 验收项目（装机波长-K3 快速协同与跨照明瞳面极平衡验收）", "指标项", [2.4, 4.7, 2.7, 8.2], il_t2),
                ("11.3", "T3 验收项目（整机跨照明切换满热连续曝光套刻稳定性验收）", "指标项", [2.4, 4.7, 2.7, 8.2], il_t3),
            ],
            "notes_master": il_notes, "notes_standalone": il_notes,
            "figures": [
                ("single", "007_fig5a", "图 11-1：FlexRay 自由瞳面照明系统在 14 种典型瞳面模式下的光强复现性实测（全项 < 0.16%；来源：Mulder 等，ASML/Zeiss，Ref007 Fig. 5a [R32]）", None, None),
            ],
        },
        {
            "code": "12_MF_ENV", "doc_code": "OV4-SRS-NXT1965Ci-12-MFENV-V1",
            "filename": "12_MF与ENV计量框架及微环境_套刻预算规格需求书_v1.docx",
            "short_name": "MF & ENV（计量框架、隔振与整机微环境）", "ch_num": 12,
            "ch_title": "第 12 章　MF & ENV（计量框架、隔振与整机微环境）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci MF & ENV（计量框架、隔振与微环境）套刻预算规格需求书",
            "standalone_subtitle": "离线隔振/声罩/环控单件（T1）、装机 MF 漂移与微振解耦（T2）及 24 h 整机环境联调（T3）验收规格",
            "recipient": "MF（计量框架与隔振）、声学屏蔽及 ENV（恒温气幕/气压微环境）子系统结构与环控团队",
            "stage_scope": "T1（离线隔振/声罩/10 mK/±5 Pa）→ T2（装机 MF 短长期漂移与动态微振）→ T3（SYCO 与 24 h 联调）",
            "coupling_rows": [
                ("共享结构底盘（MF）热机械微变 vs 全机多传感器基准同向耦合", "ENC 栅格板、投影物镜、AA 对准头及 TIS/PARIS 全部共用计量框架基准；离线单件刚度合格不代表装机在 10 mK 气幕与曝光热流下无微变形，必须在 T2 考核 15 min 与 24 h 热机械漂移。"),
                ("厂房地基振动 + RS 150 m/s^{2} 声辐射 vs 物镜像面动态微振耦合", "空气弹簧主隔振与静音掩模台声罩若存在线缆/水管机械短路，会在装机满速扫场时直接向物镜和框架注入微振，必须在 T2 核查动态短路并实测像面微振残差。"),
                ("恒温气幕/腔体气压与双卡盘参考零点 vs 24 h 长稳耦合（T2 → T3）", "腔体气压（±5 Pa）与气幕温控（±10 mK）决定空气折射率与整机长期稳定度，须在 T3 结合 SYCO/LOCO 双卡盘参考一致性完成 24 h 全流程复核。"),
            ],
            "tables": [
                ("12.1", "T1 验收项目（离线隔振模块、静音声罩与恒温/恒压微环境单件验收）", "指标项", [2.4, 4.7, 2.7, 8.2], mf_t1),
                ("12.2", "T2 验收项目（装机 MF 热机械漂移、像面微振与无动态短路验收）", "指标项", [2.4, 4.7, 2.7, 8.2], mf_t2),
                ("12.3", "T3 验收项目（整机双卡盘 SYCO/LOCO 一致性与 24 h 环境联调验收）", "指标项", [2.4, 4.7, 2.7, 8.2], mf_t3),
            ],
            "notes_master": mf_notes, "notes_standalone": mf_notes,
            "figures": [],  # Referenced Ref009/Ref062/Ref100 figures already anchored in respective sensor chapters
        },
    ]
