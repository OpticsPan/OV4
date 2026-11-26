"""Generate ASML TWINSCAN NXT:1965Ci Overlay Specification SRS Word Suite (7 DOCX files, v1).

Produces from a single verified data source:
  - 00_整机总册_NXT1965Ci六大核心子系统套刻预算规格需求书_v1.docx   (System-level master manual)
  - 01_WS晶圆台_套刻预算规格需求书_v1.docx                          (Standalone WS delivery)
  - 02_RS掩模台_套刻预算规格需求书_v1.docx                          (Standalone RS delivery)
  - 03_ENC光栅编码器_套刻预算规格需求书_v1.docx                     (Standalone ENC delivery)
  - 04_AA晶圆对准_套刻预算规格需求书_v1.docx                        (Standalone AA delivery)
  - 05_TIS与PARIS空间像传感_套刻预算规格需求书_v1.docx              (Standalone TIS+PARIS delivery)
  - 06_Lens投影物镜_套刻预算规格需求书_v1.docx                      (Standalone Lens delivery)

Key features:
  1. Opening "总则：多阶段验收理念与模块-整机耦合边界" in BOTH the master document and all 6
     standalone subsystem manuals, explicitly establishing inter-module coupling, subsystem-to-
     machine environment coupling, and why offline-qualified subsystem metrics do not automatically
     satisfy on-machine exposure overlay requirements without staged T1/T2/T3 verification.
  2. 100% numeric & evidence parity with SRS PDF v3 (including WS-T1B / RS-T1B standalone iHOPC,
     Lens-iHOPC Range & Precision two-table split, verified ASML/Zeiss patents & papers, 12 real
     original paper figures).
  3. Every standalone subsystem DOCX is 100% self-contained (zero dangling cross-chapter references;
     RS standalone includes full 4x A-B distance and unidirectional/reversal/bidirectional equations;
     local reference list [1]..[k] auto-renumbered per document).
  4. Strict typography: SimSun (宋体) 9.0 pt (小五) + Times New Roman 9.0 pt; repeating dark-navy
     headers (w:tblHeader), non-splitting rows (w:cantSplit), native Word dynamic TOC & page numbers
     updated automatically via Microsoft Word COM, plus PDF/PNG visual verification export.

Run from repository root in PowerShell:
    $env:PYTHONPATH = "D:/Codex/cache/pdf-python"
    python -B outputs/code/build_nxt1965ci_subsys_spec_docx_v1.py
"""
import re
import shutil
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

REPO = Path(__file__).resolve().parents[2]
OV4_ASSETS = REPO / "参考文献-整理版-Markdown/assets"
OUT_DIR = REPO / "outputs/reports/NXT1965Ci六大子系统套刻规格需求书_Word_v1"
WORK_DIR = REPO / "work/subsys-spec-docx-v1"
VERIFY_PDF_DIR = WORK_DIR / "verify_pdf"
PREVIEW_PNG_DIR = WORK_DIR / "preview_png"

# Verified original paper figures (read-only local assets)
PAPER_IMGS = {
    "009_fig3":  OV4_ASSETS / "009_9e90b86e529c/images/page_2_chart_4.jpg",
    "009_fig4":  OV4_ASSETS / "009_9e90b86e529c/images/page_3_image_2.jpg",
    "009_fig10": OV4_ASSETS / "009_9e90b86e529c/images/page_6_chart_3.jpg",
    "022_fig1":  OV4_ASSETS / "022_1aa75fc49631/images/page_1_image_23.jpg",
    "075_fig13": OV4_ASSETS / "075_97d74e7b9094/images/page_9_chart_2.jpg",
    "062_fig11": OV4_ASSETS / "062_57355c4f4bbf/images/page_8_chart_1.jpg",
    "015_fig10": OV4_ASSETS / "015_9a19b5ebb43f/images/page_6_chart_1.jpg",
    "252_fig3":  OV4_ASSETS / "252_277370ad3131/images/page_3_image_3.jpg",
    "066_fig6":  OV4_ASSETS / "066_d108fef2e419/images/page_4_image_3.jpg",
    "100_fig9":  OV4_ASSETS / "100_cb2cee4b24c6/images/page_6_image_7.jpg",
    "024_fig11": OV4_ASSETS / "024_e25f1b752cb5/images/page_9_chart_3.jpg",
    "253_fig8":  OV4_ASSETS / "253_d054bfdabe17/images/page_7_chart_1.jpg",
}

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

# Master A4 usable width: 21.0 cm - 2 * 1.5 cm = 18.0 cm
PAGE_WIDTH_CM = 18.0

# =============================================================================
# VERIFIED MASTER REFERENCE CATALOG (R1..R26)
# =============================================================================
MASTER_REFS = {
    1: "ASML Official Product Specification. *TWINSCAN NXT:1965Ci* (193 nm, NA 1.35, DCO ≤ 2.5 nm, MMO ≤ 4.5 nm, ≥ 250 wph, FlexRay, PARIS). https://www.asml.com",
    2: "Castenmiller, T., van de Mast, F., de Kort, T., et al. (2010). Towards ultimate optical lithography with NXT:1950i dual stage immersion platform. *Proc. SPIE* 7640, 76401N. DOI: 10.1117/12.847025 [Ref009 Fig. 3 / Fig. 4 / Fig. 7 / Fig. 10].",
    3: "de Boeij, W., Pieternella, R., Bouchoms, I., et al. (2013). Extending immersion lithography down to 1x nm production nodes. *Proc. SPIE* 8683, 86831L [Ref066 §3.4 & Fig. 6, PARIS RA < 0.50 nm].",
    4: "Freriks, H. J. M., Heemels, W. P. M. H., Muller, G. J., & Sandee, J. H. (2006). On the systematic use of budget-based design. *INCOSE International Symposium*, 16(1), 1072–1086. DOI: 10.1002/j.2334-5837.2006.tb02781.x [Ref146].",
    5: "Butler, H. (2011). Position control in lithographic equipment: an enabler for current-day chip manufacturing. *IEEE Control Systems Magazine*, 31(5), 28–47. DOI: 10.1109/MCS.2011.941653 [Ref094].",
    6: "Heertjes, M. F., Temizer, B., & Schneiders, M. (2013). Self-tuning in master–slave synchronization of high-precision stage systems. *Control Engineering Practice*, 21(12), 1706–1715. DOI: 10.1016/j.conengprac.2013.08.007 [Ref022 Fig. 1].",
    7: "Evers, E., van de Wal, M., & Oomen, T. (2019). Beyond decentralized wafer/reticle stage control design: A double-Youla approach for enhancing synchronized motion. *Control Engineering Practice*, 83, 21–32. DOI: 10.1016/j.conengprac.2018.10.011 [Ref075 Fig. 13].",
    8: "Heertjes, M. F., Butler, H., Dirkx, N. J., et al. (2020). Control of wafer scanners: Methods and developments (ASML/TU/e Survey, §V.B Reticle heating error correction by both reticle and wafer stage) [Ref019].",
    9: "Heertjes, M. F., et al. (2024). Frequency-domain MA/MSD filtering theorems and exposure window analysis for wafer scanners. *Proc. IEEE ECC 2024*. DOI: 10.23919/ECC64448.2024.10591183 [RefN8].",
    10: "ASML US Patent 6,373,072 B1 (2002) [S14] & Nikon US Patent App. 2012/0319637 A1 [S12] (WS Master / RS Slave synchronized scan architecture).",
    11: "Mulkens, J., Kubis, M., Hinnen, P., et al. (2013). High order field-to-field corrections for imaging and overlay to achieve sub 20-nm lithography requirements [Ref154 Eq. (1) & Table 1]; Mulkens, J., Hinnen, P., Kubis, M., et al. (2014). Holistic optimization architecture enabling sub-14-nm projection lithography. *J. Micro/Nanolith. MEMS MOEMS*, 13(1), 011006. DOI: 10.1117/1.JMM.13.1.011006 [RefN7].",
    12: "ASML Netherlands B.V. US Patent 8,237,914 B2 (2012). *Process, apparatus, and device for determining intra-field correction to correct overlay errors between overlapping patterns* (dynamic relative scan speed ratio and transverse trajectory modulation between reticle stage and wafer stage).",
    13: "Naaijkens, G. P. (2013). *Reticle side wall clamping*. PhD Thesis, Eindhoven University of Technology (TU/e). DOI: 10.6100/IR756525 [Ref225 §2.1, §6.3.4, Ch. 7 — reticle micro-slip & dual-stage iHOPC positioning].",
    14: "Carl Zeiss SMT AG. US Patent App. 2008/0174858 A1, Table 3 (NA = 1.35 catadioptric projection lens, 26 × 5.5 mm slit) [RefN1]; ASML Training Manual *12-TT-L3-L3-ME* (p. 70).",
    15: "de Jong, F., van der Pasch, B., Castenmiller, T., Vleeming, B., Droste, R., & van de Mast, F. (2009). Enabling the lithography roadmap: an immersion tool based on a novel stage positioning system. *Proc. SPIE* 7274, 72741S. DOI: 10.1117/12.814254 [Ref062 Fig. 11 — 7-day Gridplate stability < 0.20 nm].",
    16: "de Graaf, R., Weichselbaum, S., Droste, R., McLaren, M., Koek, B., & de Boeij, W. (2016). NXT:1980Di immersion scanner for 7nm production nodes. *Proc. SPIE* 9780, 978011. DOI: 10.1117/12.2220589 [Ref015 Fig. 10 — SMASH repeatability vs WQ].",
    17: "Menchtchikov, B., Socha, R., Zheng, C., et al. (2018). Reduction in overlay error from mark asymmetry using simulation, ORION, and alignment models. *Proc. SPIE* 10587, 105870C. DOI: 10.1117/12.2297493 [Ref252 Fig. 3 — multi-wavelength OCW].",
    18: "Pike, M., Felix, N., Menon, V., Ausschnitt, C., et al. (2012). High order wafer alignment in manufacturing. *Proc. SPIE* 8324, 832408. DOI: 10.1117/12.916483 [Ref123 — SUSD direction aliasing > 3.5 nm Gy20 mitigation]; Phase grating alignment dynamic scan extraction: *Applied Optics*, 64(30), 8921 (2025).",
    19: "Duclaux, B., Gatefait, M., Mermet, O., & Chapon, J.-D. (2020). Run to run and model variability of overlay high order process corrections for mean intrafield signatures. *Proc. SPIE* 11325, 113251K. DOI: 10.1117/12.2551062 [Ref100 Fig. 9 — dual-chuck C2 vs C1 offset].",
    20: "Ma, W.-K., Hwang, Y.-S., Kang, E.-K., et al. (2007). Hardware, materials, and parameters optimization for improvement of immersion overlay. *Proc. SPIE* 6518, 65182Z. DOI: 10.1117/12.712026 [Ref164 — UPW flow sensitivity of TIS].",
    21: "Streefkerk, B., Baselmans, J., Gehoel-van Ansem, W., Mulkens, J., Flagello, D., & Graeupner, P. (ASML & Carl Zeiss SMT, 2004). Extending optical lithography with immersion. *Proc. SPIE* 5377, 285–305 [Ref040 Fig. 7 — Zeiss offline wet PMI qualification].",
    22: "Carl Zeiss SMT AG/GmbH Immersion Metrology & Dry/Wet Adjustment Patents: US 7,408,652 B2, US 8,836,929 B2 & US 8,908,269 B2 (*Device and method for the optical measurement of an optical system by using an immersion fluid*); US 7,796,274 B2, US 8,488,127 B2 & US 8,823,948 B2 (*System for measuring the image quality of an optical imaging system*); US 7,310,187 B2 (*Projection objective and method for adjusting between immersion and dry configurations*).",
    23: "Staals, F., Andryzhyieuskaya, A., Bakker, H., et al. (2011). Advanced wavefront engineering for improved imaging and overlay applications on a 1.35 NA immersion scanner. *Proc. SPIE* 7973, 79731G. DOI: 10.1117/12.880759 [Ref024 Fig. 11]; Halle, S., Crouse, M., Jiang, A., et al. (2012). Lens heating challenges for NTD layers with freeform illumination. *Proc. SPIE* 8326, 832607 [RefN6 Table 4].",
    24: "Klinkhamer, F., Smeets, B., Thijssen, T., et al. (ASML & Carl Zeiss SMT, 2020). On-scanner high-spatial-frequency overlay control using a distortion manipulator [Ref253 Fig. 8]; Pollak, T., Emer, W., Thüring, B., et al. (Carl Zeiss SMT & ASML, 2020). A novel projection lens manipulator for high frequent overlay tuning. *Proc. SPIE* 11327, 113270T. DOI: 10.1117/12.2552063 [RefN4].",
    25: "Smeets, B., Aben, P., Klinkhamer, F., et al. (2022). Supporting future DRAM overlay and EPE roadmaps with the NXT:2100i. *Proc. SPIE* 12051, 120510K. DOI: 10.1117/12.2614031 [Ref254 §2.4 K20 boundary]; Kim, Y. H., et al. (2018). Reticle heating feed-forward control (RHC2) on NXT:1980Di [Ref016]; Ishiyama, S., et al. High-order aberration control during exposure [Ref160].",
    26: "OpticsPan/OV4 仓库主干基准文档：*NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v2.md* 与 *ENC_AA_WS-RS重复性与分级验收专项答复_v1.md*（https://github.com/OpticsPan/OV4/tree/main）。",
}


# =============================================================================
# SHARED OPENING PHILOSOPHY (User Request #1 — Master & All 6 Standalone Files)
# =============================================================================
PHILOSOPHY_PARAS = [
    "**核心验收理念（为何必须设置 T1 / T2 / T3 多阶段验收）：**整机之所以对各子系统设置 T1、T2（及跨工位 T3）多阶段验收，根本目的是促使各子系统团队在设计、装调与验证阶段主动建立两类系统工程意识——**模块间耦合（Inter-Module Coupling）**与**子系统–整机环境耦合（Subsystem–Machine Environment Coupling）**。任何子系统本质上都是服务于整机曝光成像与套刻精度（NXT:1965Ci 目标 DCO / SMO ≤ 2.50 nm、MMO ≤ 4.50 nm）的功能单元，而非孤立交付的单体仪器；子系统在离线独立工装上验证合格的指标，仅代表其剥离外界扰动后的自身本底能力，一旦装入整机运行环境，在相邻模块动态激励、参考基准传递以及真实热/气/液/声学/框架变形的多物理场耦合作用下，其实际功能表现未必能满足真实高速扫描曝光的套刻需求。因此，必须建立由离线单件本底向装机集成与整机联调逐级递进的多阶段验收机制。",
    "**两类耦合风险的内涵与拦截逻辑：**（1）**模块间耦合**涵盖 WS/RS 双台高速主从同步及相对 iHOPC 扫场轨迹耦合、ENC 读数头跨光栅拼接切换（Handover）与运动台闭环观测盲区、AA/TIS/PARIS 与投影物镜参考轴系的基准传递耦合、以及 Lens 操纵器多参共用执行器与扫描同步节拍的相位耦合；（2）**子系统与整机环境耦合**涵盖离线干态台架与装机 E 侧超纯水浸没液膜流场扰动的差异、供回水流量波动、193 nm 曝光载荷引发的掩模热/物镜热/晶圆热漂移、10 mK 恒温气幕波动、计量框架（MF）长期热机械微变形及隔振声学传递。",
    "**多阶段验收的分层职责与放行原则：**① **T1（单件/单台离线本底验收）**在可控的独立离线工装下剥离整机复杂耦合，验证子系统硬本底性能与单台独立功能（WS/RS/ENC/AA 为干态离线台架；Lens 因 NA = 1.35 > 1.0 全内反射限制采用局部静态超纯水 wet PMI；TIS+PARIS 因物理上紧耦合 E 侧 193 nm 实机光路直接设装机湿区 T1），将单体硬缺陷拦截在装机之前；② **T2（装机集成、跨模块协同与在机调控验收）**在装机结构框架、真实气液热环境及相邻模块联动条件下，考核双台同步、参考光栅长期漂移与跨缝切换、模拟 M 侧动态网格拟合、LensModel 调控残差与动态 iHOPC 等强耦合指标；③ **T3（跨工位整机联调验收）**打通 M 侧量测与 E 侧曝光之间的跨框架基线稳定度，最终闭合整机曝光套刻红线。**T1 合格仅作为装机准入前提，T2/T3 全部通过方构成子系统服务整机曝光的最终达标依据。**",
]

MASTER_STAGE_SUMMARY = [
    ("T1 阶段", "离线单件/单台本底验收", "干态离线台架（WS/RS/ENC/AA）；局部静态水池 wet PMI（Lens）；E 侧实机湿区（TIS+PARIS）", "剥离整机复杂扰动，拦截单体硬本底、传感器噪声、单台多项式轨迹跟踪与冷机静态波前缺陷（准入装机）"),
    ("T2 阶段", "装机集成与跨模块协同验收", "装机 MF 框架、恒温气幕、E 侧液膜与多模块联动工况", "验证模块间耦合与环境耦合：WRS 双台同步与 iHOPC 1× 像面残差、Gridplate 7 天漂移与 Handover、M 侧 HOWA、LensModel 调控残差与动态 Lens-iHOPC"),
    ("T3 阶段", "跨工位整机联调验收", "双台全机 M-side / E-side 跨框架交换与闭环曝光准备工况", "打通 M 侧对准与 E 侧曝光基线（M-to-E 短期漂移），与双卡盘 TIS 匹配共同闭合整机 SMO ≤ 2.50 nm / MMO ≤ 4.50 nm"),
]

MASTER_DISPATCH_TABLE = [
    ("01_WS", "WS（晶圆台，含 WRS 与运动 iHOPC）", "T1-A / T1-B / T2-A / T2-B（37 项）", "L1-S1 两层 1× 预算 X 0.744 / Y 0.867 nm（20.24% 方差）", "01_WS晶圆台_套刻预算规格需求书_v1.docx"),
    ("02_RS", "RS（掩模台，4× 掩模侧）", "T1-A / T1-B（22 项）", "占 WRS 同步 36% 方差 + 运动 iHOPC 45% 幅值份额；微滑移归 L1-S5", "02_RS掩模台_套刻预算规格需求书_v1.docx"),
    ("03_ENC", "ENC（光栅编码器测量）", "T1 / T2（5 项）", "内嵌 WRS 闭环（1:3 计量精度原则，不重复计入 SMO 顶层）", "03_ENC光栅编码器_套刻预算规格需求书_v1.docx"),
    ("04_AA", "AA（晶圆对准，M-side）", "T1 / T2 / T3（9 项）", "单层 0.500 / 两层 0.707 nm，与 PARIS 闭合 L1-S2（0.970 nm）", "04_AA晶圆对准_套刻预算规格需求书_v1.docx"),
    ("05_TIS+PARIS", "TIS + PARIS（E-side 空间像传感）", "T1 单级在机湿区（7 项）", "PARIS 两层 0.665 nm 闭合 L1-S2；双台 TIS 控 ΔC2C ≤ 0.48 nm", "05_TIS与PARIS空间像传感_套刻预算规格需求书_v1.docx"),
    ("06_Lens", "Lens（投影物镜，NA = 1.35）", "T1 / T2-A / T2-B 量程 / T2-C 精度（71 项）", "奇像差 + 8 项 Lens-iHOPC 闭合 L1-S3（X 0.667 / Y 0.557 nm）", "06_Lens投影物镜_套刻预算规格需求书_v1.docx"),
]


# =============================================================================
# SUBSYSTEM DATA DEFINITIONS (100% Parity with SRS PDF v3)
# =============================================================================
def build_subsystems_data():
    # ----- 1. WS -----
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
        ("WS-T1A-11", "WS-Y 往返动态运动误差 (R_{bi,dyn})", "≤ 0.39 nm", "离线干态连续 N ≥ 50 组完整往返，线性包络 0.29 + 0.10 = 0.39 nm，取匀速段最差点判定 [注 2]"),
        ("WS-T1A-12", "WS-Rz 往返动态运动误差 (R_{bi,dyn})", "≤ 0.014 μrad", "离线干态连续 N ≥ 50 组完整往返，线性包络 14.0 nrad，对应 26 mm 视场边缘 Y 套刻 ≤ 0.182 nm [注 2]"),
    ]
    ws_t1b = [
        ("WS-T1B-01", "WS-iHOPC K1 (dx, 1) 单台跟踪残差", "≤ 0.077 nm", "离线干态单台独立测试（无 RS 同步），注入 X 静态偏置 ±50 nm 指令，5.5 mm 窗 MA 拟合残差 |ΔK1|（55% 总份额） [注 4]"),
        ("WS-T1B-02", "WS-iHOPC K2 (dy, 1) 单台跟踪残差", "≤ 0.077 nm", "离线干态单台独立测试，注入 Y 静态偏置 ±50 nm 指令，5.5 mm 窗 MA 拟合残差 |ΔK2|（55% 总份额） [注 4]"),
        ("WS-T1B-03", "WS-iHOPC K4 (dy, y) 单台跟踪残差", "≤ 0.044 nm/cm", "离线干态满速 0.70 m/s 注入 ±15 nm/cm 扫向一阶变速指令，A–B 38.5 mm 内 MA 拟合残差 |ΔK4|（场角 0.073 nm） [注 4]"),
        ("WS-T1B-04", "WS-iHOPC K5 (dx, y) 单台跟踪残差", "≤ 0.044 nm/cm", "离线干态满速注入 ±15 nm/cm 非扫向一阶斜切轨迹 x(y)=k5·y，A–B 段内 MA 拟合残差 |ΔK5|（场角 0.073 nm） [注 4]"),
        ("WS-T1B-05", "WS-iHOPC K6 (dy, x) 单台跟踪残差", "≤ 0.052 nm/cm", "离线干态满速注入 ±15 nm/cm（±1.5 μrad）恒定偏航角指令 Rz=k6，A–B 段内 MA 拟合残差 |ΔK6|（5.2 nrad） [注 4]"),
        ("WS-T1B-06", "WS-iHOPC K8 (dy, y^{2}) 单台跟踪残差", "≤ 0.026 nm/cm^{2}", "离线干态满速注入 ±3.5 nm/cm^{2} 扫向二阶抛物线变速轨迹，A–B 段内 MA 拟合残差 |ΔK8|（场角 0.071 nm） [注 4]"),
        ("WS-T1B-07", "WS-iHOPC K10 (dy, xy) 单台跟踪残差", "≤ 0.033 nm/cm^{2}", "离线干态满速注入 ±3.5 nm/cm^{2} 扫向线性动态偏航 Rz(y)=k10·y，A–B 段内 MA 拟合残差 |ΔK10|（场角 0.071 nm） [注 4]"),
        ("WS-T1B-08", "WS-iHOPC K11 (dx, y^{2}) 单台跟踪残差", "≤ 0.026 nm/cm^{2}", "离线干态满速注入 ±3.5 nm/cm^{2} 非扫向二阶抛物线弯曲 x(y)=k11·y^{2}，A–B 段内 MA 拟合残差 |ΔK11|（场角 0.071 nm） [注 4]"),
        ("WS-T1B-09", "WS-iHOPC K14 (dy, y^{3}) 单台跟踪残差", "≤ 0.017 nm/cm^{3}", "离线干态满速注入 ±1.5 nm/cm^{3} 扫向三阶变加速轨迹，A–B 段内 MA 拟合残差 |ΔK14|（场角 0.076 nm） [注 4]"),
        ("WS-T1B-10", "WS-iHOPC K16 (dy, xy^{2}) 单台跟踪残差", "≤ 0.020 nm/cm^{3}", "离线干态满速注入 ±1.5 nm/cm^{3} 扫向二阶动态偏航 Rz(y)=k16·y^{2}，A–B 段内 MA 拟合残差 |ΔK16|（场角 0.071 nm） [注 4]"),
        ("WS-T1B-11", "WS-iHOPC K19 (dx, y^{3}) 单台跟踪残差", "≤ 0.017 nm/cm^{3}", "离线干态满速注入 ±1.5 nm/cm^{3} 非扫向三阶 S 曲线 x(y)=k19·y^{3}，A–B 段内 MA 拟合残差 |ΔK19|（场角 0.076 nm） [注 4]"),
    ]
    wrs_t2a = [
        ("WRS-T2A-01", "WRS 同步运动误差 Sync MA-X", "≤ 0.47 nm", "WS/RS 满速同步扫描（0.70 / 2.80 m/s），折算 1× 晶圆侧 5.5 mm 曝光窗 MA 3σ，对标 Ref009 Fig. 10 实测 0.47 nm [注 3]"),
        ("WRS-T2A-02", "WRS 同步运动误差 Sync MA-Y", "≤ 0.49 nm", "WS/RS 满速同步扫描，1× 晶圆侧 MA 3σ，对标 Ref009 Fig. 10 实测 0.49 nm（含 Rz 场边合成 0.538 nm） [注 3]"),
        ("WRS-T2A-03", "WRS 同步运动误差 Sync MA-Rz", "≤ 0.017 μrad", "WS/RS 满速同步扫描，绕 Z 轴相对偏航角 MA 3σ（17.0 nrad），Y 边套刻 ≤ 0.221 nm、X 边 ≤ 0.047 nm [注 3]"),
    ]
    wrs_t2b = [
        ("WRS-T2B-01", "WRS-iHOPC K1 (dx, 1) 像面残差精度", "≤ 0.140 nm", "整机双台相对轨迹协同执行（不限定内部 WS/RS 分配比例），1× 像面总残差 |ΔK1|（场角 0.140 nm） [注 4]"),
        ("WRS-T2B-02", "WRS-iHOPC K2 (dy, 1) 像面残差精度", "≤ 0.140 nm", "整机双台相对轨迹协同执行（不限定内部分配），1× 像面总残差 |ΔK2|（场角 0.140 nm） [注 4]"),
        ("WRS-T2B-03", "WRS-iHOPC K4 (dy, y) 像面残差精度", "≤ 0.080 nm/cm", "整机双台相对扫描速度比调制（不限定内部分配），经 5.5 mm 狭缝有效像面残差 |ΔK4|（场角 0.132 nm） [注 4]"),
        ("WRS-T2B-04", "WRS-iHOPC K5 (dx, y) 像面残差精度", "≤ 0.080 nm/cm", "整机双台相对横向线性斜切轨迹（不限定内部分配），1× 像面总残差 |ΔK5|（场角 0.132 nm） [注 4]"),
        ("WRS-T2B-05", "WRS-iHOPC K6 (dy, x) 像面残差精度", "≤ 0.095 nm/cm", "整机双台相对恒定偏航角差 Rz（不限定内部分配），1× 像面总残差 |ΔK6|（场角 0.124 nm） [注 4]"),
        ("WRS-T2B-06", "WRS-iHOPC K8 (dy, y^{2}) 像面残差精度", "≤ 0.048 nm/cm^{2}", "整机双台相对二阶变速轨迹（不限定内部分配），含 5.5 mm 狭缝平滑后的有效像面残差 |ΔK8|（场角 0.131 nm） [注 4]"),
        ("WRS-T2B-07", "WRS-iHOPC K10 (dy, xy) 像面残差精度", "≤ 0.060 nm/cm^{2}", "整机双台相对线性动态偏航 Rz(y)（不限定内部分配），1× 像面总残差 |ΔK10|（场角 0.129 nm） [注 4]"),
        ("WRS-T2B-08", "WRS-iHOPC K11 (dx, y^{2}) 像面残差精度", "≤ 0.048 nm/cm^{2}", "整机双台相对横向二阶抛物线轨迹（不限定内部分配），含 5.5 mm 狭缝有效像面残差 |ΔK11|（场角 0.131 nm） [注 4]"),
        ("WRS-T2B-09", "WRS-iHOPC K14 (dy, y^{3}) 像面残差精度", "≤ 0.030 nm/cm^{3}", "整机双台相对三阶变加速轨迹（不限定内部分配），含 5.5 mm 狭缝有效像面残差 |ΔK14|（场角 0.135 nm） [注 4]"),
        ("WRS-T2B-10", "WRS-iHOPC K16 (dy, xy^{2}) 像面残差精度", "≤ 0.036 nm/cm^{3}", "整机双台相对二阶动态偏航 Rz(y)（不限定内部分配），1× 像面总残差 |ΔK16|（场角 0.127 nm） [注 4]"),
        ("WRS-T2B-11", "WRS-iHOPC K19 (dx, y^{3}) 像面残差精度", "≤ 0.030 nm/cm^{3}", "整机双台相对横向三阶 S 曲线轨迹（不限定内部分配），含 5.5 mm 狭缝有效像面残差 |ΔK19|（场角 0.135 nm） [注 4]"),
    ]

    ws_notes = [
        ("p", "**[注 1] 套刻专项范围界定、干态工装与“自己测自己”盲区：**本规格书对标 NXT:1965Ci 套刻专项需求 [R1]，依据曝光窗频域滤波定理（Heertjes 等，2024）[R9]，滑窗均值 MA 主导套刻位移而滑窗标准差 MSD 主导成像对比度衰减，故运动台仅考核引起像面水平位移的面内 3 自由度（X、Y、Rz）之 MA 指标，垂向 Z/Rx/Ry（焦面均匀性）及 Sync MSD 均剥离至焦面/成像规格书。WS-T1 离线单台台架无浸没头与液体（干态环境）。依据运动台闭环观测链路分析（Butler，2011）[R5]，输入常值目标 q_{0} 时编码器观测误差为 q_{1} − q_{0}，真实物理误差满足 e_{true} = (q_{1} − q_{0}) − n_{ENC}，故须以 ENC 传感器离线本底验收合格为前提，并在装机后辅以外部独立干涉仪复核 [R26]。"),
        ("p", "**[注 2] A–B 扫描行程距离及单程 / 残余反向差 / 往返误差完整数学定义与计算步骤：**"),
        ("indent", "（1）**A–B 距离与四段行程规定：**依据 NXT:1965Ci 全视场 26 × 33 mm [R1] 与 Carl Zeiss SMT 专利 US 2008/0174858 A1 Table 3 及 ASML ME3 手册（p. 70）[R14] 确认的 5.5 mm 真实曝光狭缝，WS 单场扫描依次经历加速段 → 整定段（未开光）→ 匀速有效扫描段（A→B）→ 减速段。为使有效曝光区 y ∈ [−16.5, +16.5] mm 内每一点均拥有完整的 ±2.75 mm（L_{s}/2）狭缝滑窗积分数据，规定 **WS 匀速有效段 A–B 距离为 L_{AB,WS} = 38.5 mm**（两端各留 2.75 mm 狭缝缓冲，含加减速与整定段的机械往返总行程约 55–65 mm）。在有效曝光区 [−16.5, +16.5] mm 内按固定空间步距（如 0.5 mm）等距取 M 个固定空间坐标点 p_{1}, p_{2}, …, p_{M}，所有趟次严格按空间坐标 p_{j} 配准。"),
        ("indent", "（2）**曝光窗滑窗平均（MA）与分池统计：**连续执行 N ≥ 50 组完整往返（50 趟 A→B 正扫 + 50 趟 B→A 反扫）。依据曝光窗积分模型 [R5, R9]，对第 k 趟扫描在空间点 p_{j} 处的瞬时跟踪误差 e_{k}(t)，先按狭缝积分时长 τ_{slit} = L_{s}/v_{w} = 7.857 ms 求滑窗平均得 MA_{k}(p_{j}) = (1/τ_{slit}) ∫_{tⱼ−τ/2}^{tⱼ+τ/2} e_{k}(t) dt。随后将正扫与反扫**严格分池**，在每个固定空间点 p_{j} 分别计算样本均值与样本标准差："),
        ("eq", "μ_{up}(p_{j}) = (1/N) Σ_{k=1..N} MA_{k,up}(p_{j}) ，　σ_{up}(p_{j}) = √[ 1/(N−1) · Σ_{k=1..N} (MA_{k,up}(p_{j}) − μ_{up}(p_{j}))^{2} ]"),
        ("indent", "反扫均值 μ_{dn}(p_{j}) 与标准差 σ_{dn}(p_{j}) 按同式计算（严禁将正扫与反扫样本混合计算 3σ）。"),
        ("indent", "（3）**三项验收指标及物理含义：**① **单程动态运动误差** R_{uni,dyn} = max_{pⱼ} [ max(3σ_{up}(p_{j}), 3σ_{dn}(p_{j})) ]，反映同向重复扫描的随机离散度（已扣除方向均值偏移），通常在刚进入曝光场的“场头”余振处取得最大值；② **残余反向差** B_{UD,res} = max_{pⱼ} |μ_{up}(p_{j}) − μ_{dn}(p_{j})|，反映经子系统常规标定后，正扫平均路线与反扫平均路线之间的最大系统错位（对应相邻正反扫场错位；测试不限定内部采用前馈、ILC 或其他校准算法）；③ **往返动态运动误差** R_{bi,dyn} = max_{pⱼ} [ R_{uni,dyn}(p_{j}) + B_{UD,res}(p_{j}) ]，按“随机抖动 + 方向系统偏置”线性包络合成。验收时三项指标须同时达标。"),
        ("p", "**[注 3] WRS 同步预算锚点与主从方向：**整机单机套刻预算（SMO/DCO ≤ 2.50 nm）[R1] 依据系统预算分配方法（Freriks 等，2006）[R4] 与 Castenmiller 等（SPIE 7640，2010，Ref009 Fig. 3，见图 1-1）[R2] 按方差份额拆解，L1-S1 运动台域两层 1× 预算为 X 0.744 nm / Y 0.867 nm（占核心六域方差 20.24%）。同步平均误差定义为 MA_{sync} = MA_{WS} − M_{opt}·MA_{RS}，面内 3 轴折算矩阵 M_{opt} = diag(1/4, 1/4, 1)。WRS-T2A 中 Sync MA-X ≤ 0.47 nm、MA-Y ≤ 0.49 nm 直接锚定 Ref009 Fig. 10 实测值（图 1-2）[R2]，由 WS（64% 方差）与 RS/4（36% 方差）保守非相关 RSS 合成（√(0.38^{2}+0.28^{2})=0.472 nm、√(0.39^{2}+0.295^{2})=0.489 nm），叠加 Rz 场边 13.0 mm 杠杆后两层为 0.760 nm。经专利 US 6,373,072 B1、US 2012/0319637 A1 [R10] 及 Heertjes 等（2013，Ref022 Fig. 1，见图 1-3）[R6] 确认，ArF/ArFi 横向同步均为 WS 主台（Master）、RS 从台（Slave）。"),
        ("p", "**[注 4] 运动 iHOPC 执行主体的文献核证、T1 单台独立验证升级及取消 Range 限制说明：**"),
        ("indent", "（1）**一手文献对执行主体的核证：**ASML 一手论文 Mulkens 等（Ref154 Table 1 与 JM3 2014）[R11] 将全部 11 项运动 K 参数（K1、K2、K4、K5、K6、K8、K10、K11、K14、K16、K19）的执行器统一标为 **Scan（双台相对扫描轨迹）**；Heertjes 等（2020，Ref019 §V.B）[R8] 与 Naaijkens（2013，Ref225 Ch. 7）[R13] 均明确指出，修正动作**由掩模台（RS）与晶圆台（WS）共同执行**；ASML 专利 US 8,237,914 B2 [R12] 亦揭示沿扫描路径的纵向缩放（K4/K8/K14）与横向偏移（K5/K11/K19）通过动态调制双台相对速度比与横向相对轨迹实现。**公开文献并未宣称“因浸没头水膜约束而将动态高阶项全部交由 RS 单独执行”**；即使三阶 K14/K19 满档（±1.5 nm/cm^{3}）所需附加加速度亦仅约 7.2×10^{-5} m/s^{2}（不足 WS/RS 额定推力的 10^{-5}）。因此，WRS-T2B 取消内部主从轨迹分工限定，严格以最终 1× 像面相对轨迹 Δq(y) = q_{WS}(y) − M_{opt}·q_{RS}(y) 的残差一票判定。"),
        ("indent", "（2）**为何在离线干态阶段增设 WS-T1B 与 RS-T1B 独立验证：**WS 与 RS 各自的离线干态 T1 台架不具备双台联调同步功能，仅验收匀速直线扫描（T1-A）无法在出厂前暴露轨迹规划器、伺服带宽与轴间解耦在非匀速/非直线多项式轨迹下的相位滞后或残余误差。为此，在 WS-T1B 与 RS-T1B 均增设**单台合成多项式轨迹注入测试**（覆盖 0/1/2/3 阶全部 11 项运动基，按标称工程激励档：0 阶 ±50 nm、1 阶 ±15 nm/cm、2 阶 ±3.5 nm/cm^{2}、3 阶 ±1.5 nm/cm^{3}，经狭缝滑窗 MA 后对扣名义指令求多项式拟合残差）。预算按非相关 RSS 严格闭环：**WS-T1B 占 55% 幅值（30.25% 方差）**，**RS-T1B 占 45% 幅值（20.25% 方差，以 4× 掩模侧物理场边值考核）**，**T2 装机同步/标定/狭缝耦合占 70% 幅值（49.00% 方差）**，三项合成 √(0.55^{2} + 0.45^{2} + 0.70^{2}) = 0.9975 ≤ 1.00，无缝闭合 WRS-T2B。11 项单层场角 RSS 为 X 0.269 / Y 0.347 nm（两层 ×1.20 为 X 0.323 / Y 0.416 nm），与 Sync MA（0.760 nm）RSS 闭合 L1-S1（0.867 nm）[R2, R26]。"),
        ("indent", "（3）**为何不设运动 iHOPC 的 Range 验收项：**与物镜受限于数十微米镜片机械行程不同，WS/RS 直驱行程与推力（35–150 m/s^{2}）[R1, R13] 远超工艺需求：K1/K2 调 ±200 nm 仅占百毫米级行程的百万分之一；K4/K5 调 ±50 nm/cm 仅需 0.0005% 速度微调；K8/K11 调 ±15 nm/cm^{2} 附加加速度仅 1.5×10^{-4} m/s^{2}（余量 > 5 个数量级）。故运动 iHOPC 不存在量程瓶颈，仅按上述标称工程档位考核跟踪精度。"),
    ]

    ws_coupling = [
        ("离线干态 vs 装机湿区流场/声学耦合", "T1-A/T1-B 离线干态台架无浸没头与超纯水液膜；装机 E 侧 0.70 m/s 满速扫场时，浸没头弯液面拖曳力波动、供回水脉动及结构隔振声学传递均直接叠加于 WS 伺服误差。"),
        ("WS–RS 主从同步与相对 iHOPC 耦合", "WS（Master）误差经同步前馈馈入 RS（Slave），最终决定曝光套刻的是 1× 相对轨迹 Δq(y) = q_{WS}(y) − M_{opt}·q_{RS}(y)；单台 T1-A/T1-B 合格后必须经 T2-A/T2-B 双台联合考核。"),
        ("WS 闭环 vs ENC 传感链盲区耦合", "WS 离线闭环以 ENC 读数为反馈，无法察觉编码器自身噪声、Gridplate 7 天热漂与过缝 Handover 跳变；须先通过 ENC-T1/T2 验收并辅以外部独立干涉仪复核。"),
    ]

    # ----- 2. RS -----
    rs_t1a = [
        ("RS-T1A-01", "RS-X 单程动态运动误差 (R_{uni,dyn}, 4×)", "≤ 0.84 nm", "离线干态满速 2.80 m/s、150 m/s^{2} 折返，匀速段 A–B 距离 154.0 mm，正反扫分池统计最差点 3σ（1× 约 0.21 nm） [注 5]"),
        ("RS-T1A-02", "RS-Y 单程动态运动误差 (R_{uni,dyn}, 4×)", "≤ 0.88 nm", "离线干态满速 2.80 m/s 扫描主轴，A–B 距离 154.0 mm，正反扫分池统计最差点 3σ（1× 约 0.22 nm） [注 5]"),
        ("RS-T1A-03", "RS-Rz 单程动态运动误差 (R_{uni,dyn}, 4×)", "≤ 0.0075 μrad", "离线干态满速扫描工况，A–B 距离 154.0 mm，偏航角按 1:1 传至晶圆侧（7.5 nrad，无 4× 缩减） [注 5]"),
        ("RS-T1A-04", "RS-X 残余反向差 (B_{UD,res}, 4×)", "≤ 0.28 nm", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速段正反扫均值差最大值（1× 约 0.07 nm） [注 5]"),
        ("RS-T1A-05", "RS-Y 残余反向差 (B_{UD,res}, 4×)", "≤ 0.30 nm", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速段正反扫均值差最大值（1× 约 0.075 nm） [注 5]"),
        ("RS-T1A-06", "RS-Rz 残余反向差 (B_{UD,res}, 4×)", "≤ 0.0025 μrad", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速段绕 Z 轴正反扫均值差最大值（2.5 nrad） [注 5]"),
        ("RS-T1A-07", "RS-X 往返动态运动误差 (R_{bi,dyn}, 4×)", "≤ 1.12 nm", "离线干态连续 N ≥ 50 组完整往返，线性包络 0.84 + 0.28 = 1.12 nm（晶圆侧 1× 等效 0.28 nm） [注 5]"),
        ("RS-T1A-08", "RS-Y 往返动态运动误差 (R_{bi,dyn}, 4×)", "≤ 1.18 nm", "离线干态连续 N ≥ 50 组完整往返，线性包络 0.88 + 0.30 = 1.18 nm（晶圆侧 1× 等效 0.30 nm） [注 5]"),
        ("RS-T1A-09", "RS-Rz 往返动态运动误差 (R_{bi,dyn}, 4×)", "≤ 0.010 μrad", "离线干态连续 N ≥ 50 组完整往返，线性包络 10.0 nrad（1:1 传至晶圆侧） [注 5]"),
        ("RS-T1A-10", "RS 掩模高加减速千趟微滑移 (X 向, 4×)", "≤ 0.72 nm", "150 m/s^{2} 满载往返扫描 1000 趟前后，以外部光学标尺测 6 寸石英掩模相对吸盘 X 累积滑移（1× 约 0.18 nm） [注 5]"),
        ("RS-T1A-11", "RS 掩模高加减速千趟微滑移 (Y 向, 4×)", "≤ 0.72 nm", "同上，测扫描主轴 Y 向千趟累积微滑移（编码器无法感知石英相对滑移，须外部独立检测，归入 L1-S5） [注 5]"),
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
        ("p", "**[注 5] RS 干态单台口径、A–B 距离、4× → 1× 折算及 T1-B 独立 iHOPC 验证：**RS 全程工作于干态 4× 掩模侧，标称扫描速度 2.80 m/s、折返加速度 150 m/s^{2} [R1, R13]。按 4:1 光学倍率放大（与第 1 章 [注 2] 严格对应 [R14]），规定 **RS 匀速有效测试段 A–B 距离为 L_{AB,RS} = 4 × 38.5 = 154.0 mm**（对应 4× 掩模有效曝光区 y_{r} ∈ [−66.0, +66.0] mm 加两端各 11.0 mm 半狭缝缓冲，含加减速往返总行程约 210–230 mm），单程、残余反向差与往返包络的计算步骤与 [注 2] 完全一致 [R5, R9]，且不限定内部控制或校准算法。经投影光学折算至 1× 晶圆面后，X/Y 平移缩小 4 倍，而偏航角 Rz 按 **1:1 等角传递**（无 4× 缩减），故 RS-T1A 中 RS-Rz 往返红线严控 ≤ 0.010 μrad（10.0 nrad）。RS-Z/Rx/Ry 归属焦面规格书，本表不列。RS 在高加减速下产生的石英掩模微滑移在机内编码器读数中不可见，须用外部标尺作 1000 趟前后实测（Naaijkens，2013，Ref225）[R13]。依据一手文献确认 RS 与 WS 共同承担扫描方向 iHOPC 修正 [R8, R11, R12, R13]，RS-T1B 在无 WS 同步的离线干态平台通过单台合成多项式轨迹注入，独立验收 RS 承载 45% 总像面残差份额（20.25% 方差）的 4× 场边轨迹跟踪能力（与 WS-T1B 55% 及 T2 同步耦合 70% RSS 闭合 WRS-T2B）。图 2-1 展示了 Evers 等（2019，Ref075 Fig. 13）[R7] 在 ASML 双台平台上验证的相对同步误差累积谱改善，证明从台 RS 的高带宽与自身低重复性是压低低频同步套刻误差的前提。"),
    ]

    # Standalone RS notes include full self-contained A-B + unidirectional/reversal/bidirectional math (zero dangling [注 2]!)
    rs_notes_standalone = [
        ("p", "**[注 5] RS 干态 4× 单台口径、4× → 1× 光学折算界面及 T1-B 独立 iHOPC 验证：**RS 全程工作于干态 4× 掩模侧，标称扫描速度 2.80 m/s、折返加速度 150 m/s^{2} [R1, R13]。经 4:1 投影光学折算至 1× 晶圆像面后，X/Y 平移缩小 4 倍，而偏航角 Rz 按 **1:1 等角传递**（无 4× 缩减），故 RS-Rz 往返红线严控 ≤ 0.010 μrad（10.0 nrad）。垂向 Z/Rx/Ry 归属焦面规格书，Sync MSD 归属成像对比度规格书 [R9]，本规格书仅考核套刻面内 3-DOF。RS 在 150 m/s^{2} 急加减速下产生的石英掩模相对吸盘微滑移在机内编码器中不可见，须用外部光学标尺作 1000 趟前后实测（Naaijkens，2013，Ref225）[R13]。依据 ASML 一手文献与专利确认 RS 与 WS 共同承担扫描方向 11 项运动 iHOPC 修正 [R8, R11, R12, R13]，表 RS-T1B 在无 WS 同步的离线干态平台通过单台合成多项式轨迹注入（标称档位：0 阶 ±200 nm、1 阶 ±15 nm/cm、2 阶 ±3.5 nm/cm^{2}、3 阶 ±1.5 nm/cm^{3}），独立验收 RS 承载 45% 总像面残差份额（20.25% 方差）的 4× 场边轨迹跟踪能力，与 WS 离线 55% 及装机 T2 耦合 70% 按 √(0.55^{2}+0.45^{2}+0.70^{2})=0.9975 闭合整机 WRS-iHOPC 精度。装机后 RS 作为从台（Slave）跟从主台 WS（Master）执行双台同步验收（Ref022、US 6,373,072 B1）[R6, R10]；下图展示了 Evers 等（2019，Ref075 Fig. 13）[R7] 在 ASML 双台平台上验证的相对同步误差累积谱改善，证明 RS 高带宽与低单台重复性是压低整机同步套刻误差的前提。"),
        ("p", "**[附则] RS 4× 侧 A–B 扫描行程距离及单程 / 残余反向差 / 往返误差完整数学定义与计算步骤：**"),
        ("indent", "（1）**A–B 距离与有效曝光段：**对应 1× 视场 26 × 33 mm 与 5.5 mm 真实曝光狭缝（US 2008/0174858 A1 Table 3 & ME3 p. 70）[R1, R14]，按 4:1 倍率放大至掩模侧，有效曝光区为 y_{r} ∈ [−66.0, +66.0] mm、掩模侧狭缝宽 L_{s,RS} = 22.0 mm。为使有效曝光区内每一点均具备完整 ±11.0 mm 狭缝滑窗积分数据，规定 **RS 匀速有效段 A–B 距离为 L_{AB,RS} = 154.0 mm**（两端各留 11.0 mm 缓冲，含加减速与整定段总机械行程约 210–230 mm）。在 [−66.0, +66.0] mm 内按固定空间步距等距取 M 个空间坐标点 p_{1}, p_{2}, …, p_{M}，所有趟次严格按空间坐标配准。"),
        ("indent", "（2）**曝光窗滑窗平均（MA）与正反扫分池统计：**连续执行 N ≥ 50 组完整往返（50 趟 A→B 正扫 + 50 趟 B→A 反扫）。按狭缝积分时长 τ_{slit} = L_{s,RS}/v_{r} = 22.0 / 2800 = 7.857 ms [R5, R9]，对第 k 趟扫描在点 p_{j} 处的瞬时跟踪误差 e_{k}(t) 求滑窗平均得 MA_{k}(p_{j}) = (1/τ_{slit}) ∫_{tⱼ−τ/2}^{tⱼ+τ/2} e_{k}(t) dt，正扫与反扫严格分池计算样本均值与样本标准差（严禁混池）："),
        ("eq", "μ_{up}(p_{j}) = (1/N) Σ_{k=1..N} MA_{k,up}(p_{j}) ，　σ_{up}(p_{j}) = √[ 1/(N−1) · Σ_{k=1..N} (MA_{k,up}(p_{j}) − μ_{up}(p_{j}))^{2} ]"),
        ("indent", "（3）**三项验收判定公式：**① **单程动态运动误差** R_{uni,dyn} = max_{pⱼ} [ max(3σ_{up}(p_{j}), 3σ_{dn}(p_{j})) ]；② **残余反向差** B_{UD,res} = max_{pⱼ} |μ_{up}(p_{j}) − μ_{dn}(p_{j})|（常规标定后考核，不限定内部控制或校准算法）；③ **往返动态运动误差** R_{bi,dyn} = max_{pⱼ} [ R_{uni,dyn}(p_{j}) + B_{UD,res}(p_{j}) ]。三项指标须同时达标。"),
    ]

    rs_coupling = [
        ("RS 从台（Slave）与 WS 主台（Master）高速同步耦合", "离线 T1 仅测试 RS 自身跟踪能力；装机后 RS 须以高带宽实时跟从 WS 误差前馈与动态 iHOPC 指令，RS 自身带宽裕度与相移决定整机 WRS 同步与高阶像面残差。"),
        ("150 m/s^{2} 高加减速引发的掩模微滑移与热变形耦合", "高加减速引起的石英掩模相对吸盘微滑移对机内编码器完全不可见，且装机 193 nm 曝光热载会叠加掩模面内热变形（K4/K17/K18），须经外部标尺微滑移测试与在机 PARIS 闭环协同拦截。"),
        ("Rz 偏航角 1:1 透传与整机反作用力隔振耦合", "X/Y 平移经 4:1 光学缩小，但 RS 偏航角 Rz 按 1:1 直接映射至晶圆像面；同时 150 m/s^{2} 折返反作用力经平衡质量块与机架向 MF/物镜的残余声学/微振耦合须在装机 T2 联合复核。"),
    ]

    # ----- 3. ENC -----
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
        ("p", "**[注 6] ENC-T1 纯传感器本底定义（2 项）与文献锚点：**在 T1 离线干态验收阶段，ENC 仅作为独立位移量测传感器，不绑定 WS/RS 台体坐标系，在刚性锁死参考光栅（无伺服激励）上考核两项本底：① **原始 1000 Hz 带宽重复性 ≤ 0.22 nm**，直接对齐 Castenmiller 等（SPIE 7640，2010，Ref009 Fig. 4）[R2] 公布的 NXT 短固定光程（< 15 mm）二维光栅编码器实测值 0.22 nm，用于验证传感器本底及伺服反馈高频输入正常，出厂须同步交付 0.1 Hz–2 kHz PSD/CPS 频谱（Heertjes 等，2024）[R9]；② **曝光窗口平滑后重复性 ≤ 0.13 nm**，按 5.5 mm 狭缝与 0.70 m/s 扫速对应等效噪声带宽 B_{ENBW} = 1/(2τ_{slit}) = 63.64 Hz [R9, R14]，以 30% 低频气流有色噪声 + 70% 高频白噪声合成得 σ_{ENC,MA} = √(0.30×0.22^{2} + 0.70×0.22^{2}×63.64/936.4) = 0.130 nm [R26]，满足相对 WS-X（0.38 nm）的 1:3 计量精度原则（掩模侧 4× 通道带宽与多普勒余量按硬件选型作 T2 装机核查，本表不重复列项）。"),
        ("p", "**[注 7] ENC-T2 仅保留闭环无法覆盖的 3 项基准指标：**WS 与 RS 闭环均依赖 ENC 读数监测误差，无法察觉“尺子自身的长期漂移与跨缝跳变”[R5, R26]。因此 T2 专项验收：① **Gridplate 7 天热机械稳定性 ≤ 0.20 nm**，直接对标 de Jong 等（SPIE 7274，2009，Ref062 Fig. 11）[R15] 连续 156 小时实测结果（< 0.20 nm），须借独立参考片或 13×19 多移位标定验证（Mulkens 等，2014）[R11]；② **X/Y 读数头切换（Handover）各 ≤ 0.15 nm**（Ref009 Fig. 7）[R2]，防止过缝零点偏置被伺服闭环吸收。多读数头四角差分导出的 Rz 角本底（WS 侧 ≤ 1.6 nrad，RS 侧 ≤ 2.8 nrad）已内嵌于 WS/RS 闭环，仅作装机 1:3 故障隔离校核。ENC 全项均内嵌于 WRS 闭环，严禁重复计入顶层 SMO 预算 [R26]。"),
    ]
    enc_coupling = [
        ("传感器噪声频谱 vs 运动台伺服闭环耦合", "离线 T1 静态噪声仅反映刚性锁死下的本底；装机后 ENC 低频有色噪声会被 WS/RS 伺服闭环直接“当作真实位置误差”反向写入晶圆位移，高频噪声则影响伺服稳定裕度，故 T1 须附全频段 PSD/CPS。"),
        ("Gridplate vs 计量框架（MF）热机械与气幕环境耦合", "离线单点光栅测试无法反映整块大尺寸 Gridplate 安装于 MF 底部、在 10 mK 恒温气幕与整机曝光热流下连续 7 天的长期全局网格漂移，必须在 T2 阶段以外部参考片/多移位法独立验收。"),
        ("读数头拼接切换（Handover）vs 双台交换路径耦合", "双台交换与跨光栅分块区域时发生读数头接管切换，任何瞬态跳变或零点衔接误差都会被伺服闭环吸收为虚假定位，必须通过 T2 Handover 专项考核拦截。"),
    ]

    # ----- 4. AA -----
    aa_t1 = [
        ("AA-T1-01", "单标记静态测量重复性", "≤ 0.22 nm", "离线干态超稳参考扫描台（不分 X/Y），标准无损标记 WQ ≥ 1%，完整重扫 ≥ 30 趟扣台体位移 3σ（对齐 Ref015 Fig. 10） [注 8]"),
        ("AA-T1-02", "低信号工艺片单标记重复性", "≤ 0.50 nm", "离线干态超稳平台（不分 X/Y），衰减模拟低反射工艺标记 WQ = 0.1%–1%，完整重扫 ≥ 30 趟 3σ（对齐 Ref015 Fig. 10） [注 8]"),
        ("AA-T1-03", "四色波长/级次间 24 h 配准稳定性", "≤ 0.32 nm", "离线干态恒温平台（不分 X/Y），532/635/780/850 nm 四波长多级次通道间色差漂移 24 h 连续统计 3σ [注 9]"),
    ]
    aa_t2 = [
        ("AA-T2-01", "单标记动态扫描重复性 (X 向)", "≤ 0.38 nm", "离线干态模拟 M-side 量测端平台（含产线扫速与步进折返节拍），同一标记完整重扫 ≥ 30 趟 3σ [注 8]"),
        ("AA-T2-02", "单标记动态扫描重复性 (Y 向)", "≤ 0.38 nm", "同上，Y 向单标记动态扫描重复性 3σ（静态 0.22 + M 侧 WS 动态 0.31 合成 0.380 nm） [注 8]"),
        ("AA-T2-03", "全晶圆网格拟合重复性 HOWA (X 向)", "≤ 0.40 nm", "离线干态模拟 M-side 平台执行类 FIWA 动作（N ≥ 20 标记，正反扫方向配平，含边缘留出点检验），重复 3σ [注 10]"),
        ("AA-T2-04", "全晶圆网格拟合重复性 HOWA (Y 向)", "≤ 0.40 nm", "同上，Y 向全晶圆高阶网格拟合重复性 HOWA 3σ（不重装片测试本体，重装片另行记录吸片重复性） [注 10]"),
    ]
    aa_t3 = [
        ("AA-T3-01", "M-to-E 对准基线短期漂移 (X 向)", "≤ 0.30 nm", "双台整机联调（跨 MF 框架，M-side AA 与 E-side 物镜/TIS 相对位置漂移），片内/批间 X 向 3σ [注 10]"),
        ("AA-T3-02", "M-to-E 对准基线短期漂移 (Y 向)", "≤ 0.30 nm", "同上，Y 向 M-to-E 对准基线短期漂移 3σ（与 HOWA 0.40 合成单层 0.500 nm / 两层 0.707 nm） [注 10]"),
    ]
    aa_notes = [
        ("p", "**[注 8] 干态测试边界、单标记静态（T1）与动态（T2）重复性定义：**TWINSCAN 双台机 M 侧晶圆对准全过程处于干态环境，无浸没液体 [R2, R21]。相位光栅对准（PGA）原理需带动标记匀速扫过照明光斑并提取干涉相位（*Applied Optics*，2025）[R18]，因此 T1“静态重复性（≤ 0.22 nm）”并非晶圆绝对静止，而是在离线超稳参考扫描台（无宏动加减速激振）上扣除参考位移后的纯传感器本底，直接对标 de Graaf 等（SPIE 9780，2016，Ref015 Fig. 10）[R16] 公布的 SMASH 实测曲线（强光 WQ ≥ 1% 约 0.15–0.25 nm；弱光 WQ 0.1%–1% 约 0.25–0.50 nm）。**单趟扫描内采集的多组样点不可充当独立重复**，须完整进出标记独立重扫 ≥ 30 趟 [R26]。T2 在模拟 M 侧平台上叠加产线步进折返节拍，合成 ≤ 0.38 nm。"),
        ("p", "**[注 9] 四色多波长配准稳定性（≤ 0.32 nm）的文献支撑：**CMP 与刻蚀引起的标记不对称会破坏衍射相位对称性并产生对准位置偏差（APD/WAD）。多波长方案利用不同波长在工艺膜层中的差异化相位灵敏度做加权融合，可显著压低晶圆间套刻波动——Menchtchikov 等（SPIE 10587，2018，Ref252 Fig. 3）[R17] 证实基于实测的多色加权（OCW）可将套刻波动降低 0.8–1.3 nm。其前提是仪器自身四通道 24 h 色间漂移足够小（≤ 0.32 nm）且单色可用率稳定，否则仪器色差漂移会被误判为工艺不对称 [R17, R26]。表中验收不限定具体融合算法，仅约束硬件色间配准稳度。"),
        ("p", "**[注 10] HOWA（T2）与 M-to-E 基线漂移（T3）分级与预算闭合：**HOWA（≤ 0.40 nm，须正反扫方向配平以避免 Pike 等在 SPIE 8324，2012，Ref123 [R18] 报道的 > 3.5 nm 方向混叠虚假网格）在干态模拟 M 侧平台（T2）独立验收；M-to-E 短期漂移（≤ 0.30 nm）跨 MF 框架连接 M 侧与 E 侧，归入 T3 整机联调。T2 与 T3 按 RSS 合成为单层 0.500 nm（两层 0.707 nm），与 E 侧 PARIS 掩模对准（两层 0.665 nm）[R3] 共同闭合 L1-S2（0.970 nm，占 Ref009 六域方差 25.38%）[R2, R26]。产品工艺不对称残差（WAD ≤ 0.50 nm）归入客户产品片工艺验证边界，不计入参考片验收。"),
    ]
    aa_coupling = [
        ("AA 光学传感 vs M 侧晶圆台高速步进折返耦合（T1 → T2）", "离线超稳台架（T1）无宏动加减速激振与正反扫方向切换；进入模拟 M 侧量测端（T2）后，扫描动态噪声与正反扫方向混叠（SUSD）可放大至纳米级虚假高阶网格，须通过 T2 动态扫描与配平 HOWA 考核拦截。"),
        ("四色多波长通道稳度 vs 工艺膜层标记不对称耦合", "产线工艺膜层不对称依赖多波长通道差值解耦；若 AA 自身 4 通道 24 h 色间漂移超标，会被整机误判为晶圆工艺形变并错误反馈至曝光网格。"),
        ("M 侧 AA vs 整机 MF 框架与 E 侧曝光基准耦合（T2 → T3）", "M 侧对准得到的晶圆网格必须跨计量框架（MF）传递至 E 侧物镜/TIS 曝光工位；M-to-E 相对机械/热基线漂移仅在双台整机环境（T3）下显现，离线 T1/T2 无法替代。"),
    ]

    # ----- 5. TIS + PARIS -----
    tp_t1 = [
        ("TP-T1-01", "TIS 水平空间像对准重复性 (X 向)", "≤ 0.40 nm", "E-side 曝光端 193 nm 湿区在机透射空间像扫描，连续 ≥ 30 次对准解算 3σ（附供水流量窗核验） [注 11]"),
        ("TP-T1-02", "TIS 水平空间像对准重复性 (Y 向)", "≤ 0.40 nm", "同上，E-side 曝光端 193 nm 湿区 Y 向空间像对准重复性 3σ（用于 M-to-E 基线定期清零） [注 11]"),
        ("TP-T1-03", "双台 TIS-1 / TIS-2 匹配稳定性 (X 向)", "≤ 0.28 nm", "整机双台交换工况下，24 h 内双传感板相对 X 位置漂移 3σ（直控双卡盘套刻差 ΔC2C ≤ 0.48 nm） [注 11]"),
        ("TP-T1-04", "双台 TIS-1 / TIS-2 匹配稳定性 (Y 向)", "≤ 0.28 nm", "同上，24 h 内双晶圆台 TIS 基准板 Y 向相对匹配漂移 3σ [注 11]"),
        ("TP-T1-05", "PARIS 7 视场点掩模对准重复性 RA (X 向)", "≤ 0.47 nm", "E-side 7 视场点并行空间像掩模对准重复性 3σ，对标 Ref066 §3.4（< 0.50 nm，两层 0.665 nm） [注 11]"),
        ("TP-T1-06", "PARIS 7 视场点掩模对准重复性 RA (Y 向)", "≤ 0.47 nm", "同上，7 视场点并行 Y 向掩模对准重复性 3σ（与 AA 0.707 nm 共同闭合 L1-S2 = 0.970 nm） [注 11]"),
        ("TP-T1-07", "PARIS 奇像差波前测量重复性", "≤ 0.14 nm RMS", "E-side 193 nm 湿区在机波前反演重复性 RMS，为物镜奇像差闭环调控提供 1:3 计量精度支撑 [注 11]"),
    ]
    tp_notes = [
        ("p", "**[注 11] 单级在机验收（T1）、套刻范围精简与装机湿区工况说明：**TIS（6 kHz 透射空间像基准）与 PARIS（7 视场点并行空间像传感器）[R3] 均直接工作于 193.368 nm 曝光光路与 E 侧投影物镜像面，物理上须在装机 E 侧（含正常超纯水浸没液膜，非干态离线）执行，不涉及类似 AA 的 M 侧全片步进调度，故统一设为 **T1 单级在机验收**（其中 TP-T1-03/04 双台匹配须在双台交换工况下测试）。按套刻专项范围原则，纯焦面项（TIS 最佳焦面 Z、PARIS 场曲 Z）已剥离至焦面规格书。文献依据：① de Boeij 等（SPIE 8683，2013，Ref066 §3.4 & Fig. 6）[R3] 公布 PARIS 7 点掩模对准重复性规格 < 0.50 nm，本表定限 ≤ 0.47 nm（两层 0.665 nm，与 M 侧 AA 0.707 nm 闭合 L1-S2 = 0.970 nm）[R2, R26]；② Ma 等（SPIE 6518，2007，Ref164）[R20] 证实浸没超纯水（UPW）供回水流量波动会调制 TIS 测位重复性，故 TP-T1-01/02 须在标称供水流量工作窗内复核；③ Duclaux 等（SPIE 11325，2020，Ref100 Fig. 9）[R19] 揭示双卡盘（C2 vs C1）切换时会诱发 K7/K12/K13 低阶参考偏置，故 TP-T1-03/04 严控双台基准 24 h 相对漂移 ≤ 0.28 nm，并在整机启用双卡盘参考匹配。"),
    ]
    tp_coupling = [
        ("传感器本体 vs E 侧 193 nm 曝光光路及超纯水液膜耦合", "TIS 与 PARIS 物理上必须透过投影物镜与浸没超纯水读取 193 nm 实机空间像，离线无光路/无液膜测试无法代表真实曝光工况，且超纯水供回水流量波动会直接调制 TIS 测位重复性，故直接在 E 侧实机湿区开展 T1 验收。"),
        ("双晶圆台 TIS-1 / TIS-2 切换 vs 双卡盘套刻差（ΔC2C）耦合", "两台晶圆卡盘各自的 TIS 基准板相对漂移会直接映射为双卡盘低阶畸变偏置（K7/K12/K13），须在双台交换实机工况下考核 24 h 相对匹配稳定性。"),
        ("PARIS 波前量测 vs 物镜奇像差闭环调控耦合", "PARIS 在机波前测量重复性（≤ 0.14 nm RMS）是投影物镜 LensModel 闭环调整的 1:3 计量前提，其偏差将直接决定物镜在线调控残差上限。"),
    ]

    # ----- 6. Lens -----
    odd_z = [
        ("Z7",  0.21, 0.0742, 0.199, "1θ X"), ("Z8",  0.21, 0.0742, 0.199, "1θ Y"),
        ("Z10", 0.19, 0.0672, 0.173, "3θ X"), ("Z11", 0.19, 0.0672, 0.173, "3θ Y"),
        ("Z14", 0.21, 0.0606, 0.147, "1θ X"), ("Z15", 0.21, 0.0606, 0.147, "1θ Y"),
        ("Z19", 0.24, 0.0693, 0.132, "3θ X"), ("Z20", 0.24, 0.0693, 0.132, "3θ Y"),
        ("Z23", 0.28, 0.0700, 0.077, "1θ X"), ("Z24", 0.28, 0.0700, 0.077, "1θ Y"),
        ("Z26", 0.19, 0.0548, 0.160, "5θ X"), ("Z27", 0.19, 0.0548, 0.160, "5θ Y"),
        ("Z30", 0.26, 0.0650, 0.120, "3θ X"), ("Z31", 0.26, 0.0650, 0.120, "3θ Y"),
        ("Z34", 0.36, 0.0805, 0.056, "1θ X"), ("Z35", 0.36, 0.0805, 0.056, "1θ Y"),
        ("Z39", 0.26, 0.0650, 0.095, "5θ X"), ("Z40", 0.26, 0.0650, 0.095, "5θ Y"),
        ("Z43", 0.36, 0.0805, 0.050, "3θ X"), ("Z44", 0.36, 0.0805, 0.050, "3θ Y"),
        ("Z47", 0.42, 0.0857, 0.041, "1θ X"), ("Z48", 0.42, 0.0857, 0.041, "1θ Y"),
        ("Z50", 0.28, 0.0700, 0.090, "7θ X"), ("Z51", 0.28, 0.0700, 0.090, "7θ Y"),
        ("Z54", 0.30, 0.0671, 0.094, "5θ X"), ("Z55", 0.30, 0.0671, 0.094, "5θ Y"),
        ("Z58", 0.42, 0.0857, 0.038, "3θ X"), ("Z59", 0.42, 0.0857, 0.038, "3θ Y"),
        ("Z62", 0.48, 0.0907, 0.042, "1θ X"), ("Z63", 0.48, 0.0907, 0.042, "1θ Y"),
    ]
    ln_t1 = [
        (f"LN-T1-{k:02d}", zc, f"≤ {flim:.2f} nm",
         f"离线局部静态超纯水浸没干涉平台（wet PMI，λ=193.368 nm，NA=1.35）冷机绝对上限；{tag}，等效 ≤ {rmsv:.4f} nm RMS（单轴套刻 {ovlv:.3f} nm） [注 12]")
        for k, (zc, flim, rmsv, ovlv, tag) in enumerate(odd_z, 1)
    ]
    ln_t1.append((
        "LN-T1-31", "K20 (dy, x^{3}) 冷机静畸变", "≤ 0.18 nm/cm^{3}",
        "NXT:1965Ci 不配 K20 主动操纵器，冷机装调出厂静态畸变上限（归入跨机匹配 MMO-M2） [注 13]"
    ))

    adj_z = [
        ("Z7",  0.12, "1θ X 彗差"),  ("Z8",  0.12, "1θ Y 彗差"),
        ("Z10", 0.11, "3θ X 三叶草"), ("Z11", 0.11, "3θ Y 三叶草"),
        ("Z14", 0.12, "1θ X 二阶彗差"), ("Z15", 0.12, "1θ Y 二阶彗差"),
        ("Z19", 0.14, "3θ X 二阶三叶草"), ("Z20", 0.14, "3θ Y 二阶三叶草"),
        ("Z23", 0.16, "1θ X 三阶彗差"), ("Z24", 0.16, "1θ Y 三阶彗差"),
        ("Z26", 0.11, "5θ X 五叶草"), ("Z27", 0.11, "5θ Y 五叶草"),
    ]
    ln_t2a = [
        (f"LN-T2A-{k:02d}", zc, f"≤ {rlim:.2f} nm",
         f"任意一次经 LensModel 下发波前/畸变调节指令后，实测与目标差 |Z_{{meas}} − Z_{{target}}| 上限（{desc}，约 55% 静态限值） [注 12]")
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
        ("LN-T2C-01", "Lens-iHOPC K3 (dx, x) 补偿调节精度", "≤ 0.120 nm/cm", "总验收残差 |ΔK3|，最小步长 ≤ 0.012 nm/cm（场角贡献 0.156 nm，双档 4/15 核验） [注 13]"),
        ("LN-T2C-02", "Lens-iHOPC K7 (dx, x^{2}) 补偿调节精度", "≤ 0.092 nm/cm^{2}", "总验收残差 |ΔK7|，最小步长 ≤ 0.009 nm/cm^{2}（场角贡献 0.155 nm） [注 13]"),
        ("LN-T2C-03", "Lens-iHOPC K9 (dx, xy) 补偿调节精度", "≤ 0.072 nm/cm^{2}", "总验收残差 |ΔK9|，最小步长 ≤ 0.007 nm/cm^{2}（场角贡献 0.154 nm） [注 13]"),
        ("LN-T2C-04", "Lens-iHOPC K12 (dy, x^{2}) 补偿调节精度", "≤ 0.092 nm/cm^{2}", "总验收残差 |ΔK12|，最小步长 ≤ 0.009 nm/cm^{2}（场角贡献 0.155 nm） [注 13]"),
        ("LN-T2C-05", "Lens-iHOPC K13 (dx, x^{3}) 补偿调节精度", "≤ 0.070 nm/cm^{3}", "总验收残差 |ΔK13|，最小步长 ≤ 0.007 nm/cm^{3}（场角贡献 0.154 nm） [注 13]"),
        ("LN-T2C-06", "Lens-iHOPC K15 (dx, x^{2}y) 补偿调节精度", "≤ 0.054 nm/cm^{3}", "总验收残差 |ΔK15|，最小步长 ≤ 0.005 nm/cm^{3}（场角贡献 0.151 nm） [注 13]"),
        ("LN-T2C-07", "Lens-iHOPC K17 (dx, xy^{2}) 补偿调节精度", "≤ 0.042 nm/cm^{3}", "总验收残差 |ΔK17|，最小步长 ≤ 0.004 nm/cm^{3}（场角贡献 0.149 nm） [注 13]"),
        ("LN-T2C-08", "Lens-iHOPC K18 (dy, yx^{2}) 补偿调节精度", "≤ 0.054 nm/cm^{3}", "总验收残差 |ΔK18|，最小步长 ≤ 0.005 nm/cm^{3}（场角贡献 0.151 nm） [注 13]"),
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
        ("p", "**[注 12] NA = 1.35 物镜离线 T1 湿态耦合、Zeiss 干/湿测量专利核证及 Odd Zernike 两层定义：**"),
        ("indent", "（1）**湿态全瞳验收的物理必然性与 Carl Zeiss SMT 一手论文/专利证据：**依据 NA = n·sin(θ) = 1.35 [R14]，若末片熔融石英（n ≈ 1.56）下方为空气（n_{air} ≈ 1.0003），1.0 < NA ≤ 1.35 外瞳光线将在玻璃-空气界面发生**全内反射（TIR）**，干态下完全无法出射测量。ASML 与 Carl Zeiss SMT 联合论文 Streefkerk 等（SPIE 5377，2004，Ref040 Fig. 7）[R21] 直接披露 Zeiss 在出厂离线阶段即采用**湿态相移干涉仪（wet PMI）**验收浸没物镜波前；Carl Zeiss SMT 专利族 **US 7,408,652 B2、US 8,836,929 B2、US 8,908,269 B2** 及 **US 7,796,274 B2、US 8,488,127 B2、US 8,823,948 B2** [R22] 进一步披露了在末片与衍射/参考载体之间构建局部静态浸没液池、采用保护窗口隔绝液膜退化并克服干态 TIR 盲区的离线湿态干涉测量系统（与整机 0.70 m/s 扫描浸没头流场扰动不同）。此外，Zeiss 专利 **US 7,310,187 B2** [R22] 披露了物镜在干态与浸没态之间切换装调的方法。"),
        ("indent", "（2）**关于“是否同时在 Dry（NA = 0.93）与 Wet（NA = 1.35）双状态测试”的核查边界：**经核查公开 Zeiss 专利与 SPIE 论文库，**尚无公开文献明文记载 Zeiss 对 NA = 1.35（Starlith 19xx）物镜固定执行“先 Dry（NA = 0.93）测、再 Wet（NA = 1.35）测”双阶段出厂检验 SOP**（NA = 0.93 为传统干式 193 nm 物镜如 XT:1400 的量产上限；Starlith 工厂内部是否保留干态缩瞳预检步骤属于未公开细节）。工程装调中可在干态缩瞳（NA < 1.0，如 ≤ 0.93）作早期镜组初调与无水风险排查，但受 TIR 限制无法覆盖 1.0 < NA ≤ 1.35 外瞳，故 **T1 出厂全瞳波前（NA = 1.35）最终验收必须且只能以局部静态超纯水浸没 wet PMI 为准** [R21, R22]。"),
        ("indent", "（3）**Odd Zernike 两层需求闭环：**第一层（T1）约束冷机绝对奇像差上限，按 Fringe Zernike 系数（λ = 193.368 nm，单位 nm）全 30 项单轴 RSS 为 1.196 nm Fringe、全瞳 0.400 nm RMS（Coma 单轴 ≤ 0.190 nm RMS），经 2D Abbe 仿真与 IBM/ASML 实测表（Halle 等，SPIE 8326，2012，RefN6 Table 4，Z10 = −0.88 吻合度 2.8%）[R23] 核验，跨照明切换单轴套刻包络 ≤ 0.437 nm（Abbe 实算 0.388 nm），匹配 Staals 等（SPIE 7973，2011，Ref024 Fig. 11）[R23] 的 FlexWave 实测水平（Coma 约 0.16 nm RMS）。第二层（T2-A）约束任意一次调用 LensModel 执行波前/畸变调节前后的实测残差 |Z_{meas} − Z_{target}|（主可调阶次 Z7–Z27 约 55% 静态限值，全瞳总残差 ≤ 0.22 nm RMS），且调后绝对波前不得突破 T1 上限 [R26]。"),
        ("p", "**[注 13] T1 K20 静畸变剥离与 T2-B/T2-C 动态 Lens-iHOPC 预算闭环：**依据 Smeets 等（SPIE 12051，2022，Ref254 §2.4）[R25]，NXT:1965Ci 不配 K20（dy, x^{3}）场平面主动操纵器（至 NXT:2050i 起开放），故将 K20 归入 T1 冷机出厂静态畸变（≤ 0.18 nm/cm^{3}，归入 MMO-M2）。依据 Mulkens 等 [R11] 19 参 iHOPC 框架及 Kim 等（RHC2，Ref016）[R25] 掩模热演化规律（K17/K18），T2-B（量程）与 T2-C（精度）分表考核 8 项激活 K 参数（X 向 6 项 K3/K7/K9/K13/K15/K17 单层场角 RSS 0.375 nm；Y 向 2 项 K12/K18 单层 0.216 nm），两层 ×1.20 为 X 0.450 / Y 0.260 nm，与奇像差及热声项共同闭合 L1-S3（X 0.667 / Y 0.557 nm，占 Ref009 六域方差 11.99%）[R2, R26]。放大率换算为 1 nm/cm = 0.1 ppm，对应 SET-vs-GET 精度 3.0%–5.6%，直接参照 ASML/Carl Zeiss SMT 联合物镜畸变操纵器实测结果（Klinkhamer 等，Ref253 Fig. 8；Pollak 等，SPIE 11327，2020，RefN4）[R24]。"),
        ("p", "**[注 14] T2-B / T2-C 套刻相关联合行程与动态考核依据：**与运动台不同，物镜镜片物理微动行程稀缺且多参共用执行器矩阵 [R24, R25]，因此 T2-B-09 考核 8 项联合行程占用 ≤ 80% Range 防饱和，T2-C-09 至 T2-C-17 同步考核最小步长 ≤ Spec/10、单向重复 ≤ 35%、双向滞回 ≤ 25%、跨 K 串扰 ≤ 30% 且诱发奇像差 ≤ 0.05 nm RMS [R23, R24]、静态整定 20–50 ms 与动态扫描同步相位滞后 ≤ 0.20 ms [R25]，以及 15 s / 15 min / 24 h 保持漂移（纯焦面串扰漂移划归焦面规格书）[R26]。"),
    ]
    ln_coupling = [
        ("冷机离线静态 wet PMI vs 装机 193 nm 曝光热载与气压耦合（T1 → T2）", "离线 T1 静态局部水池仅验证冷机绝对波前本底；装机连续曝光后，高功率极轴照明引发的非旋转对称镜片热致像差/畸变与气压微变，须依赖在机 LensModel 与 PARIS 闭环动态修正（T2-A）。"),
        ("多 K 参共用镜片操纵器 vs 串扰/奇像差/行程饱和耦合", "8 项激活 Lens-iHOPC 共用有限镜片微动执行器矩阵；单参数满量程动作可能诱发非目标 K 项串扰、奇像差恶化或联合行程饱和，必须在 T2-B（量程）与 T2-C（精度与动态）双表并行约束。"),
        ("动态物镜项（K9/K15/K17/K18）vs WRS 扫描节拍相位耦合", "扫描中动态随动的 4 项混合 K 参数必须与 0.70 m/s 双台扫描精准同步触发（相位滞后 ≤ 0.20 ms），否则动态补偿将在狭缝内错位反而放大套刻误差。"),
    ]

    return [
        {
            "code": "01_WS",
            "doc_code": "OV4-SRS-NXT1965Ci-WS-V1",
            "filename": "01_WS晶圆台_套刻预算规格需求书_v1.docx",
            "short_name": "WS（晶圆台，含 WRS 与运动 iHOPC）",
            "ch_num": 1,
            "ch_title": "第 1 章　WS（晶圆台）子系统规格需求（含 WRS 与 iHOPC 运动补偿）",
            "standalone_title": "ASML NXT:1965Ci WS（晶圆台）子系统套刻预算规格需求书",
            "standalone_subtitle": "WS 单台干态（T1-A / T1-B）与 WRS 双台同步及 iHOPC 运动补偿（T2-A / T2-B）验收规格",
            "recipient": "WS（晶圆台）子系统研发、控制与测试团队（含 WRS 同步联合验收接口）",
            "l1_budget": "L1-S1 运动台域两层 1× 预算 X ≤ 0.744 nm / Y ≤ 0.867 nm（占核心六域方差 20.24%）",
            "stage_scope": "T1-A（干态匀速）→ T1-B（干态单台 iHOPC）→ T2-A（双台同步）→ T2-B（双台 iHOPC）",
            "coupling_rows": ws_coupling,
            "tables": [
                ("1.1", "T1-A 验收项目（WS 单台干态常规匀速扫描与静止稳定性验收，面内 3-DOF）", "指标项", [2.4, 4.5, 2.8, 8.1], ws_t1a),
                ("1.2", "T1-B 验收项目（WS 单台干态 iHOPC 多项式轨迹独立跟踪能力验收，11 项）", "指标项", [2.4, 4.5, 2.8, 8.1], ws_t1b),
                ("1.3", "T2-A 验收项目（T2-WRS 双台同步性能验收）", "指标项", [2.4, 4.5, 2.8, 8.1], wrs_t2a),
                ("1.4", "T2-B 验收项目（T2-WRS-iHOPC 11 项运动补偿整机最终像面精度验收）", "指标项", [2.4, 4.5, 2.8, 8.1], wrs_t2b),
            ],
            "notes_master": ws_notes,
            "notes_standalone": ws_notes,
            "figures": [
                ("pair", "009_fig3", "图 1-1：NXT:1950i 单机 2.50 nm 六大物理域套刻预算构成（来源：Castenmiller 等，SPIE 7640，2010，Ref009 Fig. 3 [R2]）",
                         "009_fig10", "图 1-2：NXT:1950i 实测双台同步误差 Sync MA-X = 0.47 nm / MA-Y = 0.49 nm（来源：Ref009 Fig. 10 [R2]，支撑 WRS-T2A-01/02）"),
                ("single", "022_fig1", "图 1-3：WS（主台 Master）误差经前馈通道送入 RS（从台 Slave）的双台同步控制架构（来源：Heertjes 等，Control Eng. Pract.，2013，Ref022 Fig. 1 [R6]）", None, None),
            ],
        },
        {
            "code": "02_RS",
            "doc_code": "OV4-SRS-NXT1965Ci-RS-V1",
            "filename": "02_RS掩模台_套刻预算规格需求书_v1.docx",
            "short_name": "RS（掩模台）",
            "ch_num": 2,
            "ch_title": "第 2 章　RS（掩模台）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci RS（掩模台）子系统套刻预算规格需求书",
            "standalone_subtitle": "RS 单台干态匀速扫描、微滑移（T1-A）与 iHOPC 多项式轨迹（T1-B）验收规格（4× 掩模侧）",
            "recipient": "RS（掩模台）子系统研发、控制与测试团队",
            "l1_budget": "承载 WRS 同步 36% 方差份额 + 运动 iHOPC 45% 幅值份额（微滑移归入 L1-S5 掩模夹持域）",
            "stage_scope": "T1-A（干态 4× 匀速扫描与微滑移）→ T1-B（干态 4× 单台 iHOPC）→ 装机并入 WRS T2 联调",
            "coupling_rows": rs_coupling,
            "tables": [
                ("2.1", "T1-A 验收项目（RS 单台干态常规匀速扫描与微滑移验收，4× 掩模侧口径）", "指标项", [2.4, 4.5, 2.8, 8.1], rs_t1a),
                ("2.2", "T1-B 验收项目（RS 单台干态 iHOPC 多项式轨迹独立跟踪能力验收，4× 掩模侧口径）", "指标项", [2.4, 4.5, 2.8, 8.1], rs_t1b),
            ],
            "notes_master": rs_notes_master,
            "notes_standalone": rs_notes_standalone,
            "figures": [
                ("single", "075_fig13", "图 2-1：WS/RS 相对伺服误差累积频谱实测对比（虚线为无耦合，实线为同步耦合；来源：Evers 等，Control Eng. Pract. 83，2019，Ref075 Fig. 13 [R7]）", None, None),
            ],
        },
        {
            "code": "03_ENC",
            "doc_code": "OV4-SRS-NXT1965Ci-ENC-V1",
            "filename": "03_ENC光栅编码器_套刻预算规格需求书_v1.docx",
            "short_name": "ENC（光栅编码器测量）",
            "ch_num": 3,
            "ch_title": "第 3 章　ENC（光栅编码器测量）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci ENC（光栅编码器）子系统套刻预算规格需求书",
            "standalone_subtitle": "纯传感器离线本底（T1）与 Gridplate 长期稳定性及读数头切换 Handover（T2）验收规格",
            "recipient": "ENC（二维光栅编码器测量）子系统光学、电子学与标定团队",
            "l1_budget": "全项内嵌于 WRS 闭环（1:3 计量精度原则，不重复计入 SMO 顶层预算）",
            "stage_scope": "T1（干态刚性锁死传感器本底与 PSD）→ T2（装机 MF 7 天稳定性与跨缝 Handover）",
            "coupling_rows": enc_coupling,
            "tables": [
                ("3.1", "T1 验收项目（纯 ENC 传感器离线干态测量本底验收）", "指标项", [2.4, 4.5, 2.8, 8.1], enc_t1),
                ("3.2", "T2 验收项目（Gridplate 长期稳定性与读数头切换 Handover 验收）", "指标项", [2.4, 4.5, 2.8, 8.1], enc_t2),
            ],
            "notes_master": enc_notes,
            "notes_standalone": enc_notes,
            "figures": [
                ("pair", "009_fig4", "图 3-1：NXT 短固定光程（< 15 mm）二维光栅编码器 1000 Hz 噪声实测 0.22 nm 3σ（来源：Castenmiller 等，SPIE 7640，Ref009 Fig. 4 [R2]，支撑 ENC-T1-01）",
                         "062_fig11", "图 3-2：Gridplate 连续一周（12 h–156 h）X/Y 全局网格热机械稳定性实测 < 0.20 nm（来源：de Jong 等，SPIE 7274，2009，Ref062 Fig. 11 [R15]，支撑 ENC-T2-01）"),
            ],
        },
        {
            "code": "04_AA",
            "doc_code": "OV4-SRS-NXT1965Ci-AA-V1",
            "filename": "04_AA晶圆对准_套刻预算规格需求书_v1.docx",
            "short_name": "AA（晶圆对准）",
            "ch_num": 4,
            "ch_title": "第 4 章　AA（晶圆对准）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci AA（晶圆对准）子系统套刻预算规格需求书",
            "standalone_subtitle": "传感器静态本底（T1）、模拟 M-side 动态 HOWA（T2）与整机 M-to-E 基线（T3）验收规格",
            "recipient": "AA（M-side 晶圆对准）子系统光学、算法与集成团队",
            "l1_budget": "AA 合计单层 ≤ 0.500 nm / 两层 ≤ 0.707 nm，与 E 侧 PARIS 共同闭合 L1-S2（0.970 nm，25.38% 方差）",
            "stage_scope": "T1（干态超稳台静态本底）→ T2（干态模拟 M-side 动态与 HOWA）→ T3（跨 MF 框架 M-to-E 漂移）",
            "coupling_rows": aa_coupling,
            "tables": [
                ("4.1", "T1 验收项目（AA 底层传感器离线干态超稳平台验收，3 项不分 X/Y）", "指标项", [2.4, 4.5, 2.8, 8.1], aa_t1),
                ("4.2", "T2 验收项目（模拟 M-side 干态量测端 FIWA / HOWA 集成验收）", "指标项", [2.4, 4.5, 2.8, 8.1], aa_t2),
                ("4.3", "T3 验收项目（双台整机联调 M-to-E 对准基线短期漂移验收）", "指标项", [2.4, 4.5, 2.8, 8.1], aa_t3),
            ],
            "notes_master": aa_notes,
            "notes_standalone": aa_notes,
            "figures": [
                ("pair", "015_fig10", "图 4-1：SMASH 对准重复性随信号质量 WQ 变化实测（WQ≥1% 约 0.15–0.25 nm；WQ 0.1–1% 约 0.25–0.50 nm；来源：de Graaf 等，SPIE 9780，2016，Ref015 Fig. 10 [R16]）",
                         "252_fig3", "图 4-2：多波长加权融合（OCW）较单色方案将晶圆间套刻波动压低 0.8 nm 实测对比（来源：Menchtchikov 等，SPIE 10587，2018，Ref252 Fig. 3 [R17]）"),
            ],
        },
        {
            "code": "05_TIS+PARIS",
            "doc_code": "OV4-SRS-NXT1965Ci-TP-V1",
            "filename": "05_TIS与PARIS空间像传感_套刻预算规格需求书_v1.docx",
            "short_name": "TIS + PARIS（E-side 空间像传感）",
            "ch_num": 5,
            "ch_title": "第 5 章　TIS + PARIS（E-side 空间像传感）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci TIS + PARIS（E-side 空间像传感）子系统套刻预算规格需求书",
            "standalone_subtitle": "E-side 193 nm 实机湿区空间像对准、双台匹配与奇像差波前测量（T1）验收规格",
            "recipient": "TIS + PARIS（E-side 空间像对准与在机波前传感）子系统研发与集成团队",
            "l1_budget": "PARIS RA 两层 ≤ 0.665 nm（与 AA 闭合 L1-S2 = 0.970 nm）；双台 TIS 匹配控 ΔC2C ≤ 0.48 nm",
            "stage_scope": "T1 单级在机湿区验收（E-side 193 nm 曝光光路 + 超纯水浸没 + 双台交换）",
            "coupling_rows": tp_coupling,
            "tables": [
                ("5.1", "T1 验收项目（E-side 在机空间像对准与奇像差波前测量验收）", "指标项", [2.4, 4.5, 2.8, 8.1], tp_t1),
            ],
            "notes_master": tp_notes,
            "notes_standalone": tp_notes,
            "figures": [
                ("pair", "066_fig6", "图 5-1：PARIS 7 视场点并行空间像传感器结构示意（支持每片 3 扫，公开 RA < 0.50 nm；来源：de Boeij 等，SPIE 8683，2013，Ref066 Fig. 6 [R3]）",
                         "100_fig9", "图 5-2：双卡盘（C2 vs C1）未匹配时诱发的 K7/K13/K12 低阶偏置实测（来源：Duclaux 等，SPIE 11325，2020，Ref100 Fig. 9 [R19]，支撑双台 TIS 匹配）"),
            ],
        },
        {
            "code": "06_Lens",
            "doc_code": "OV4-SRS-NXT1965Ci-LENS-V1",
            "filename": "06_Lens投影物镜_套刻预算规格需求书_v1.docx",
            "short_name": "Lens（投影物镜）",
            "ch_num": 6,
            "ch_title": "第 6 章　Lens（投影物镜）子系统规格需求",
            "standalone_title": "ASML NXT:1965Ci Lens（投影物镜）子系统套刻预算规格需求书",
            "standalone_subtitle": "冷机湿态波前上限（T1）、LensModel 调节残差（T2-A）与 Lens-iHOPC 量程/精度双表（T2-B / T2-C）",
            "recipient": "Lens（193 nm / NA = 1.35 投影物镜与操纵器）子系统光学、精密机械与控制团队",
            "l1_budget": "L1-S3 光学与畸变域两层 1× 预算 X ≤ 0.667 nm / Y ≤ 0.557 nm（占核心六域方差 11.99%）",
            "stage_scope": "T1（离线局部静态水池 wet PMI）→ T2-A（LensModel 调后残差）→ T2-B（iHOPC 量程）→ T2-C（精度与动态）",
            "coupling_rows": ln_coupling,
            "tables": [
                ("6.1", "T1 验收项目（离线冷机静态波前上限与 K20 静畸变，λ = 193.368 nm）", "指标项（Fringe Zernike 系数，193 nm）", [2.2, 3.5, 2.7, 9.4], ln_t1),
                ("6.2", "T2-A 验收项目（任意一次 LensModel 调节后的奇像差调节残差验收）", "指标项（Fringe Zernike 系数，调节残差）", [2.4, 3.8, 2.7, 8.9], ln_t2a),
                ("6.3", "T2-B 验收项目（动态 Lens-iHOPC 补偿调节范围 Range 验收表）", "指标项", [2.4, 4.9, 2.9, 7.6], ln_t2b_range),
                ("6.4", "T2-C 验收项目（动态 Lens-iHOPC K 参数调节精度与套刻相关动态考核表）", "指标项", [2.4, 4.9, 2.9, 7.6], ln_t2c_prec),
            ],
            "notes_master": ln_notes,
            "notes_standalone": ln_notes,
            "figures": [
                ("pair", "024_fig11", "图 6-1：FlexWave 波前控制后各奇像差残差实测（Coma X/Y 约 0.16 nm RMS；来源：Staals 等，SPIE 7973，2011，Ref024 Fig. 11 [R23]，支撑 T1/T2-A）",
                         "253_fig8", "图 6-2：物镜畸变操纵器沿 −13..+13 mm 狭缝 Target (SET) vs Measured (GET) 实测残差（来源：Klinkhamer 等，ASML/Zeiss，Ref253 Fig. 8 [R24]，支撑 T2-C 精度）"),
            ],
        },
    ]


# =============================================================================
# LOW-LEVEL PYTHON-DOCX STYLING HELPERS
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


TOKEN_RE = re.compile(
    r"(\*\*[^*]+?\*\*|\*[^*]+?\*|_\{[^{}]+\}|\^\{[^{}]+\})"
)


def add_rich_runs(p, text: str, size_pt=9.0, base_bold=False, color=TEXT_MAIN,
                  zh_font="宋体", en_font="Times New Roman"):
    """Parse **bold**, *italic*, _{sub}, ^{sup} (and nested _{}/^{} inside bold) cleanly."""
    parts = TOKEN_RE.split(str(text))
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            inner = part[2:-2]
            add_rich_runs(p, inner, size_pt=size_pt, base_bold=True, color=color,
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
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=42, bottom=42, left=75, right=75):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in (("top", top), ("bottom", bottom), ("left", left), ("right", right)):
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, outer_hex=HEX_OUTER, inner_hex=HEX_BORDER, sz_outer="6", sz_inner="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz_outer}" w:space="0" w:color="{outer_hex}"/>'
        f'<w:bottom w:val="single" w:sz="{sz_outer}" w:space="0" w:color="{outer_hex}"/>'
        f'<w:left w:val="single" w:sz="{sz_outer}" w:space="0" w:color="{outer_hex}"/>'
        f'<w:right w:val="single" w:sz="{sz_outer}" w:space="0" w:color="{outer_hex}"/>'
        f'<w:insideH w:val="single" w:sz="{sz_inner}" w:space="0" w:color="{inner_hex}"/>'
        f'<w:insideV w:val="single" w:sz="{sz_inner}" w:space="0" w:color="{inner_hex}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


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
    tblLayout = parse_xml(f'<w:tblLayout {nsdecls("w")} w:type="fixed"/>')
    tblPr.append(tblLayout)
    total_dxa = int(round(sum(col_widths_cm) * 566.929))
    tblW = parse_xml(f'<w:tblW {nsdecls("w")} w:w="{total_dxa}" w:type="dxa"/>')
    tblPr.append(tblW)
    # Set tblGrid
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
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))


def set_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:tblHeader"))


def add_p_bottom_border(paragraph, color_hex=HEX_NAVY, sz="12"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="3" w:color="{color_hex}"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)


def add_field(paragraph, instr_text: str, size_pt=8.0, color=HDR_GRAY):
    run_begin = paragraph.add_run()
    set_run_font(run_begin, size_pt=size_pt, color=color)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    run_begin._r.append(fld_begin)

    run_instr = paragraph.add_run()
    set_run_font(run_instr, size_pt=size_pt, color=color)
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = f" {instr_text} "
    run_instr._r.append(instr)

    run_sep = paragraph.add_run()
    set_run_font(run_sep, size_pt=size_pt, color=color)
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    run_sep._r.append(fld_sep)

    run_val = paragraph.add_run("1")
    set_run_font(run_val, size_pt=size_pt, color=color)

    run_end = paragraph.add_run()
    set_run_font(run_end, size_pt=size_pt, color=color)
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run_end._r.append(fld_end)


def init_document(header_text: str) -> Document:
    doc = Document()

    # Configure Normal style: SimSun 9pt + Times New Roman 9pt
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(9.0)
    normal.font.color.rgb = TEXT_MAIN
    rPr = normal.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:cs"), "Times New Roman")
    rFonts.set(qn("w:eastAsia"), "宋体")

    # Configure Heading 1 & Heading 2 so Word Navigation Pane + TOC work natively
    for level, sz, clr in ((1, 12.5, NAVY_DARK), (2, 10.0, NAVY_MAIN)):
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
        srFonts.set(qn("w:ascii"), "Times New Roman")
        srFonts.set(qn("w:hAnsi"), "Times New Roman")
        srFonts.set(qn("w:cs"), "Times New Roman")
        srFonts.set(qn("w:eastAsia"), "黑体")

    # Configure TOC 1 & TOC 2 styles so Master Cover + full TOC fits cleanly on Page 1
    for toc_name, sz, is_b, sb, sa in (
        ("TOC 1", 8.4, True, 1.5, 0.5),
        ("TOC 2", 8.1, False, 0.3, 0.3),
    ):
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
        tst.paragraph_format.line_spacing = 1.08
        trPr = tst.element.get_or_add_rPr()
        trFonts = trPr.find(qn("w:rFonts"))
        if trFonts is None:
            trFonts = OxmlElement("w:rFonts")
            trPr.insert(0, trFonts)
        trFonts.set(qn("w:ascii"), "Times New Roman")
        trFonts.set(qn("w:hAnsi"), "Times New Roman")
        trFonts.set(qn("w:cs"), "Times New Roman")
        trFonts.set(qn("w:eastAsia"), "宋体")

    # Page setup: A4 portrait, clean compact engineering margins (usable width = 18.0 cm)
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

    # Running Header (Pages 2+)
    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(2)
    hr = hp.add_run(header_text)
    set_run_font(hr, size_pt=8.0, color=HDR_GRAY)
    add_p_bottom_border(hp, color_hex=HEX_BORDER, sz="4")

    # Running Footer (Pages 2+)
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fp.paragraph_format.space_before = Pt(2)
    fp.paragraph_format.space_after = Pt(0)
    r1 = fp.add_run("第 ")
    set_run_font(r1, size_pt=8.0, color=HDR_GRAY)
    add_field(fp, "PAGE", size_pt=8.0, color=HDR_GRAY)
    r2 = fp.add_run(" 页 / 共 ")
    set_run_font(r2, size_pt=8.0, color=HDR_GRAY)
    add_field(fp, "NUMPAGES", size_pt=8.0, color=HDR_GRAY)
    r3 = fp.add_run(" 页")
    set_run_font(r3, size_pt=8.0, color=HDR_GRAY)

    # Set updateFields on open so Word always keeps TOC/page numbers fresh
    settings = doc.settings.element
    upd = OxmlElement("w:updateFields")
    upd.set(qn("w:val"), "true")
    settings.append(upd)

    return doc


def add_heading_1(doc: Document, text: str, page_break_before=False):
    if page_break_before:
        doc.add_page_break()
    p = doc.add_paragraph(style="Heading 1")
    p.paragraph_format.space_before = Pt(2 if page_break_before else 6)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, size_pt=12.0, bold=True, color=NAVY_DARK, zh_font="黑体", en_font="Times New Roman")
    add_p_bottom_border(p, color_hex=HEX_NAVY, sz="12")
    return p


def add_heading_2(doc: Document, text: str):
    p = doc.add_paragraph(style="Heading 2")
    p.paragraph_format.space_before = Pt(5.5)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, size_pt=9.8, bold=True, color=NAVY_MAIN, zh_font="黑体", en_font="Times New Roman")
    return p


def add_cover_header(doc: Document, doc_code: str, title: str, subtitle: str, meta_rows: list):
    # Top navy accent rule
    p_rule = doc.add_paragraph()
    p_rule.paragraph_format.space_before = Pt(0)
    p_rule.paragraph_format.space_after = Pt(6)
    add_p_bottom_border(p_rule, color_hex=HEX_NAVY, sz="20")

    p_code = doc.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(3)
    r = p_code.add_run(doc_code)
    set_run_font(r, size_pt=8.8, bold=True, color=RGBColor(0x2B, 0x52, 0x75))

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(3)
    rt = p_title.add_run(title)
    set_run_font(rt, size_pt=14.8, bold=True, color=NAVY_DARK, zh_font="黑体", en_font="Times New Roman")

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(5)
    rs = p_sub.add_run(subtitle)
    set_run_font(rs, size_pt=8.8, color=SLATE_SUB)
    add_p_bottom_border(p_sub, color_hex="CBD6E2", sz="6")

    # 4-col metadata table
    tbl = doc.add_table(rows=len(meta_rows), cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, outer_hex="C5D2DF", inner_hex=HEX_BORDER, sz_outer="6", sz_inner="4")
    for r_idx, (k1, v1, k2, v2) in enumerate(meta_rows):
        row = tbl.rows[r_idx]
        set_row_cant_split(row)
        vals = [(k1, True), (v1, False), (k2, True), (v2, False)]
        for c_idx, (txt, is_k) in enumerate(vals):
            cell = row.cells[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_margins(cell, top=34, bottom=34, left=68, right=68)
            if is_k:
                set_cell_shading(cell, HEX_META_K)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.18
            add_rich_runs(p, txt, size_pt=8.8, base_bold=is_k, color=NAVY_DARK if is_k else TEXT_MAIN)
    set_table_fixed_widths(tbl, [2.7, 6.3, 2.7, 6.3])


def add_callout_box(doc: Document, items: list, compact: bool = False):
    """Add shaded engineering callout/note box with thick left navy bar.
    items: list of (kind, text) where kind in ('p', 'indent', 'eq').
    """
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    set_cell_shading(cell, HEX_NOTE_BG)
    pad_v = 52 if compact else 72
    set_cell_margins(cell, top=pad_v, bottom=pad_v, left=115, right=100)
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
        p.paragraph_format.space_before = Pt(0 if idx == 0 else (1.8 if compact else 2.5))
        p.paragraph_format.space_after = Pt((1.2 if compact else 1.8) if idx < len(items) - 1 else 0)
        p.paragraph_format.line_spacing = 1.18 if compact else 1.26
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
            add_rich_runs(p, txt, size_pt=9.0, base_bold=False, color=NAVY_DARK)


def add_styled_table(doc: Document, headers: list, rows: list, col_widths_cm: list,
                     center_cols=(0, 2), bold_cols=(0, 1, 2), compact: bool = False):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, outer_hex=HEX_OUTER, inner_hex=HEX_BORDER, sz_outer="6", sz_inner="4")

    # Rescale col widths proportionally if sum differs from PAGE_WIDTH_CM
    s = sum(col_widths_cm)
    if abs(s - PAGE_WIDTH_CM) > 0.01:
        col_widths_cm = [round(w * PAGE_WIDTH_CM / s, 3) for w in col_widths_cm]

    # Header row
    hdr_row = tbl.rows[0]
    set_row_header(hdr_row)
    set_row_cant_split(hdr_row)
    hpad = 40 if compact else 50
    for c_idx, htxt in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, HEX_NAVY)
        set_cell_margins(cell, top=hpad, bottom=hpad, left=65, right=65)
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
        r = p.add_run(htxt)
        set_run_font(r, size_pt=9.0, bold=True, color=WHITE, zh_font="黑体", en_font="Times New Roman")

    # Body rows
    bpad = 28 if compact else 38
    bls = 1.14 if compact else 1.20
    for r_idx, row_vals in enumerate(rows):
        row = tbl.rows[1 + r_idx]
        set_row_cant_split(row)
        stripe = (r_idx % 2 == 1)
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            if stripe:
                set_cell_shading(cell, HEX_STRIPE)
            set_cell_margins(cell, top=bpad, bottom=bpad, left=64, right=64)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in center_cols else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = bls
            is_b = (c_idx in bold_cols)
            clr = NAVY_DARK if is_b else TEXT_MAIN
            add_rich_runs(p, val, size_pt=9.0, base_bold=is_b, color=clr)

    set_table_fixed_widths(tbl, col_widths_cm)
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(1.5 if compact else 2.5)
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
            set_cell_margins(cell, top=65, bottom=65, left=75, right=75)
            p_img = cell.paragraphs[0]
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(0)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.paragraph_format.keep_with_next = True
            w_cm, _ = fit_image_dims_cm(PAPER_IMGS[k], max_w_cm=8.1, max_h_cm=5.2)
            p_img.add_run().add_picture(str(PAPER_IMGS[k]), width=Cm(w_cm))

            p_cap = cell.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_cap.paragraph_format.space_before = Pt(0)
            p_cap.paragraph_format.space_after = Pt(0)
            p_cap.paragraph_format.line_spacing = 1.22
            add_rich_runs(p_cap, cap, size_pt=8.2, color=TEXT_MUTED)
        set_table_fixed_widths(tbl, [PAGE_WIDTH_CM / 2, PAGE_WIDTH_CM / 2])
    else:
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, outer_hex=HEX_BORDER, inner_hex=HEX_BORDER, sz_outer="4", sz_inner="4")
        row = tbl.rows[0]
        set_row_cant_split(row)
        cell = row.cells[0]
        set_cell_margins(cell, top=70, bottom=65, left=100, right=100)
        p_img = cell.paragraphs[0]
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.keep_with_next = True
        w_cm, _ = fit_image_dims_cm(PAPER_IMGS[k1], max_w_cm=13.5, max_h_cm=5.4)
        p_img.add_run().add_picture(str(PAPER_IMGS[k1]), width=Cm(w_cm))

        p_cap = cell.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(0)
        p_cap.paragraph_format.line_spacing = 1.22
        add_rich_runs(p_cap, cap1, size_pt=8.2, color=TEXT_MUTED)
        set_table_fixed_widths(tbl, [PAGE_WIDTH_CM])

    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)


def add_toc_block(doc: Document, title: str = "目　录"):
    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_before = Pt(8)
    p_hdr.paragraph_format.space_after = Pt(5)
    p_hdr.paragraph_format.keep_with_next = True
    r = p_hdr.add_run(title)
    set_run_font(r, size_pt=10.5, bold=True, color=NAVY_DARK, zh_font="黑体", en_font="Times New Roman")
    add_p_bottom_border(p_hdr, color_hex=HEX_NAVY, sz="10")

    p_toc = doc.add_paragraph()
    p_toc.paragraph_format.space_before = Pt(2)
    p_toc.paragraph_format.space_after = Pt(4)
    add_field(p_toc, 'TOC \\o "1-2" \\h \\z \\u', size_pt=9.0, color=TEXT_MAIN)


# =============================================================================
# CITATION RENUMBERING ENGINE (Master 1..26 vs Local Standalone 1..k)
# =============================================================================
REF_TOKEN_RE = re.compile(r"\[((?:R\d+(?:,\s*)?)+)\]")


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


def add_references_list(doc: Document, ref_ids: list):
    for local_no, rid in enumerate(ref_ids, 1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.24
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.first_line_indent = Cm(-0.75)
        r_no = p.add_run(f"[{local_no}]\t")
        set_run_font(r_no, size_pt=9.0, bold=True, color=NAVY_DARK)
        add_rich_runs(p, MASTER_REFS[rid], size_pt=9.0, color=TEXT_MAIN)


# =============================================================================
# DOCUMENT BUILDERS: (A) MASTER SYSTEM MANUAL  &  (B) 6 STANDALONE SUBSYSTEMS
# =============================================================================
def build_master_docx(subsystems: list, out_path: Path):
    doc = init_document("OV4 ASML NXT:1965Ci 六大核心子系统套刻预算规格需求书（整机自查总册 v1）")
    master_map = {i: i for i in range(1, 27)}

    # ----- Page 1: Cover + Dynamic TOC -----
    meta_rows = [
        ("整机目标定位", "ASML TWINSCAN NXT:1965Ci（λ = 193.368 nm，NA = 1.35，β = 1/4）",
         "顶层套刻红线", "DCO ≤ 2.50 nm（闭环 2.26 nm）；SMO ≤ 2.50 nm（闭环 2.36 nm）；MMO ≤ 4.50 nm（闭环 4.29 nm）"),
        ("文档定位与用途", "整机总体自查总册（汇总六大核心子系统全部 T1/T2/T3 验收规格与耦合边界）",
         "曝光狭缝口径", "26 × 5.5 mm 真实狭缝（v_{w} = 0.70 m/s，τ_{slit} = 7.857 ms）"),
        ("验收分级原则", "T1：离线单件/单台；T2：装机集成/协同/调控；T3：跨工位整机联调",
         "编制日期与字体", "2026-11-27（Word 总册 v1 · 正文宋体小五 9 pt / Times New Roman 9 pt）"),
    ]
    add_cover_header(
        doc,
        "OV4-SRS-NXT1965Ci-MASTER-V1 · 整机工程规格需求总册（套刻专项 · 含六大子系统分册汇总）",
        "ASML NXT:1965Ci 六大核心子系统套刻预算规格需求书（总册）",
        "WS / RS / ENC / AA / TIS+PARIS / Lens 多阶段耦合验收理念与分层验收规格（T1 / T2 / T3）",
        meta_rows,
    )
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(3)
    sp.paragraph_format.space_after = Pt(2)

    add_callout_box(doc, [
        ("p", "**总册使用说明：**本总册供整机总体组统筹审阅与接口闭合核验，涵盖第 0 章多阶段耦合验收总则、第 1–6 章六大核心子系统（WS/WRS、RS、ENC、AA、TIS+PARIS、Lens）全部四列验收表、技术注释及 12 张一手论文原图，并配套拆分输出 6 份完全自包含的子系统独立 Word 分册（01_WS 至 06_Lens），便于直接分发给各子系统责任团队执行验收。"),
    ], compact=True)

    add_toc_block(doc, "目　录")

    # ----- Chapter 0: Philosophy & Module-Machine Coupling -----
    add_heading_1(doc, "第 0 章　总则：多阶段验收理念与模块-整机耦合边界", page_break_before=True)
    add_heading_2(doc, "0.1 整机设置 T1 / T2 / T3 多阶段验收的核心工程理念")
    add_callout_box(doc, [("p", t) for t in PHILOSOPHY_PARAS], compact=True)

    add_heading_2(doc, "0.2 T1 / T2 / T3 多阶段验收职责与耦合边界总表")
    add_styled_table(
        doc,
        ["验收阶段", "验收定位", "标准测试环境与工装边界", "拦截的耦合风险与整机放行意义"],
        MASTER_STAGE_SUMMARY,
        [2.2, 3.6, 5.2, 7.0],
        center_cols=(0,),
        bold_cols=(0, 1),
        compact=True,
    )

    add_heading_2(doc, "0.3 六大核心子系统预算分工与独立分册分发清单")
    add_styled_table(
        doc,
        ["分册编号", "子系统名称", "验收层级与项数", "顶层预算承接关系", "对应独立下发 Word 文件"],
        MASTER_DISPATCH_TABLE,
        [1.9, 3.6, 3.2, 4.5, 4.8],
        center_cols=(0,),
        bold_cols=(0, 1),
        compact=True,
    )

    # ----- Chapters 1..6 -----
    for sub in subsystems:
        add_heading_1(doc, sub["ch_title"], page_break_before=True)
        for sec_no, sec_title, col2_hdr, col_w, rows in sub["tables"]:
            add_heading_2(doc, f"{sec_no} {sec_title}")
            add_styled_table(
                doc,
                ["序号", col2_hdr, "验收规格", "标准测试定义与工装条件"],
                rows,
                col_w,
                center_cols=(0, 2),
                bold_cols=(0, 1, 2),
            )

        note_sec_no = f"{sub['ch_num']}.{len(sub['tables']) + 1}"
        add_heading_2(doc, f"{note_sec_no} 技术注释、测试定义细则与文献图证")
        resolved_notes = [(k, resolve_citations(t, master_map)) for k, t in sub["notes_master"]]
        add_callout_box(doc, resolved_notes)
        sp2 = doc.add_paragraph()
        sp2.paragraph_format.space_before = Pt(0)
        sp2.paragraph_format.space_after = Pt(4)

        for fig in sub["figures"]:
            kind, k1, c1, k2, c2 = fig
            r_c1 = resolve_citations(c1, master_map)
            r_c2 = resolve_citations(c2, master_map) if c2 else None
            add_figure_block(doc, (kind, k1, r_c1, k2, r_c2))

    # ----- Chapter 7: All 26 Verified References -----
    add_heading_1(doc, "第 7 章　参考文献", page_break_before=True)
    add_references_list(doc, list(range(1, 27)))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)


def build_standalone_subsystem_docx(sub: dict, out_path: Path):
    doc = init_document(f"OV4 ASML NXT:1965Ci {sub['short_name']} 套刻预算规格需求书 (v1)")

    # Collect local references in order of appearance and renumber 1..k
    all_text_for_refs = [t for _, t in sub["notes_standalone"]]
    for _, _, c1, _, c2 in sub["figures"]:
        all_text_for_refs.append(c1)
        if c2:
            all_text_for_refs.append(c2)
    local_ref_ids = collect_ref_ids(all_text_for_refs)
    local_map = {rid: idx for idx, rid in enumerate(local_ref_ids, 1)}

    # ----- Page 1: Standalone Cover + Philosophy Preface -----
    meta_rows = [
        ("发送对象", sub["recipient"],
         "整机顶层目标", "ASML NXT:1965Ci（193.368 nm，NA 1.35，DCO/SMO ≤ 2.50 nm，MMO ≤ 4.50 nm）"),
        ("本分册承接预算", sub["l1_budget"],
         "曝光狭缝口径", "26 × 5.5 mm 真实狭缝（v_{w} = 0.70 m/s，τ_{slit} = 7.857 ms）"),
        ("本分册验收层级", sub["stage_scope"],
         "编制日期与字体", "2026-11-27（子系统独立下发版 v1 · 宋体小五 9 pt / Times New Roman 9 pt）"),
    ]
    add_cover_header(
        doc,
        f"{sub['doc_code']} · 子系统独立验收规格需求书（套刻专项 · 单独下发分册）",
        sub["standalone_title"],
        sub["standalone_subtitle"],
        meta_rows,
    )

    # Section 1: Opening Multi-Stage Coupling Philosophy (Fits 100% cleanly on Page 1!)
    add_heading_1(doc, "1. 总则：多阶段验收理念与本子系统整机耦合边界", page_break_before=False)
    add_heading_2(doc, "1.1 整机设置 T1 / T2 多阶段验收的核心理念")
    add_callout_box(doc, [("p", t) for t in PHILOSOPHY_PARAS], compact=True)

    add_heading_2(doc, f"1.2 {sub['short_name']} 关键模块耦合与整机环境耦合边界清单")
    add_styled_table(
        doc,
        ["序号", "核心耦合机制", "为何离线合格不能替代多阶段/整机验收（对本子系统的具体要求）"],
        [(f"CP-{i:02d}", k, desc) for i, (k, desc) in enumerate(sub["coupling_rows"], 1)],
        [1.8, 5.2, 11.0],
        center_cols=(0,),
        bold_cols=(0, 1),
        compact=True,
    )

    # Section 2: Tiered Acceptance Tables (Page break for clean start)
    add_heading_1(doc, f"2. {sub['short_name']} 分层验收指标要求", page_break_before=True)
    for idx, (_, sec_title, col2_hdr, col_w, rows) in enumerate(sub["tables"], 1):
        add_heading_2(doc, f"2.{idx} {sec_title}")
        add_styled_table(
            doc,
            ["序号", col2_hdr, "验收规格", "标准测试定义与工装条件"],
            rows,
            col_w,
            center_cols=(0, 2),
            bold_cols=(0, 1, 2),
        )

    # Section 3: Self-contained Notes & Verified Paper Figures
    add_heading_1(doc, "3. 技术注释、测试定义细则与实测文献图证", page_break_before=False)
    resolved_notes = [(k, resolve_citations(t, local_map)) for k, t in sub["notes_standalone"]]
    add_callout_box(doc, resolved_notes)
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

    # Renumber figure captions cleanly as 图 3-1, 图 3-2...
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


# =============================================================================
# WORD COM FIELD UPDATE + PDF/PNG VISUAL AUDIT
# =============================================================================
def update_and_verify_with_word(docx_paths: list):
    import win32com.client

    VERIFY_PDF_DIR.mkdir(parents=True, exist_ok=True)
    if PREVIEW_PNG_DIR.exists():
        shutil.rmtree(PREVIEW_PNG_DIR)
    PREVIEW_PNG_DIR.mkdir(parents=True, exist_ok=True)

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
                # Update all dynamic fields (TOC, PAGE, NUMPAGES)
                wdoc.Fields.Update()
                for i in range(1, wdoc.TablesOfContents.Count + 1):
                    wdoc.TablesOfContents(i).Update()
                for s_idx in range(1, wdoc.Sections.Count + 1):
                    sec = wdoc.Sections(s_idx)
                    for hf_idx in (1, 2):  # primary & first page
                        sec.Headers(hf_idx).Range.Fields.Update()
                        sec.Footers(hf_idx).Range.Fields.Update()
                wdoc.Save()
                # Export to verification PDF (17 = wdExportFormatPDF)
                wdoc.ExportAsFixedFormat(str(pdf_out.resolve()), 17)
            finally:
                wdoc.Close(False)

            # Audit fonts & render PNG previews via PyMuPDF
            with fitz.open(pdf_out) as pdoc:
                pages = len(pdoc)
                fonts_9pt = {}
                for pg in pdoc:
                    blocks = pg.get_text("dict", flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)["blocks"]
                    for b in blocks:
                        for line in b.get("lines", []):
                            for sp in line.get("spans", []):
                                sz = round(sp["size"], 1)
                                if 8.8 <= sz <= 9.2 and sp["text"].strip():
                                    fn = sp["font"]
                                    fonts_9pt[fn] = fonts_9pt.get(fn, 0) + len(sp["text"].strip())
                # Save preview PNGs (first 2 pages + last page; all key pages for master)
                sub_prev = PREVIEW_PNG_DIR / dp.stem[:6]
                sub_prev.mkdir(parents=True, exist_ok=True)
                for pg in pdoc:
                    pix = pg.get_pixmap(dpi=130)
                    pix.save(sub_prev / f"p{pg.number + 1:02d}.png")

                has_simsun = any("SimSun" in k for k in fonts_9pt)
                has_tnr = any("TimesNewRoman" in k for k in fonts_9pt)
                assert has_simsun, f"Missing SimSun 9pt in {dp.name}: {fonts_9pt}"
                assert has_tnr, f"Missing Times New Roman 9pt in {dp.name}: {fonts_9pt}"
                full_txt = "\n".join(pg.get_text("text") for pg in pdoc)
                assert "{" not in full_txt and "}" not in full_txt, f"Raw brace leaked in {dp.name}!"
                assert "`" not in full_txt, f"Raw backtick leaked in {dp.name}!"
                results.append((dp.name, pages, fonts_9pt))
    finally:
        word.Quit()

    return results


def main():
    for k, p in PAPER_IMGS.items():
        if not p.is_file():
            raise FileNotFoundError(f"Missing paper image {k}: {p}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    subsystems = build_subsystems_data()

    built_paths = []

    # 1. Master system-level Word manual
    master_path = OUT_DIR / "00_整机总册_NXT1965Ci六大核心子系统套刻预算规格需求书_v1.docx"
    build_master_docx(subsystems, master_path)
    built_paths.append(master_path)

    # 2. Six standalone subsystem Word manuals
    for sub in subsystems:
        sub_path = OUT_DIR / sub["filename"]
        build_standalone_subsystem_docx(sub, sub_path)
        built_paths.append(sub_path)

    # 3. Update live TOC/page fields via Word COM & audit fonts + render PNG previews
    audit_results = update_and_verify_with_word(built_paths)
    print("\n=== ALL 7 WORD DOCUMENTS BUILT & VERIFIED ===")
    for name, pages, fdict in audit_results:
        core = {k: v for k, v in fdict.items() if "SimSun" in k or "TimesNewRoman" in k}
        print(f"  {pages:2d} pp | {name} | 9pt fonts={core}")


if __name__ == "__main__":
    main()
