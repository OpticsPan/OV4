"""Generate ASML TWINSCAN NXT:1965Ci Six-Subsystem Overlay Specification SRS (PDF v3).

Built upon v2 (OV4-SRS-OVERLAY-V2.4 minimalist engineering template) with 5 formal v3 upgrades:
  1. Primary-source audit of [注 4] (WS vs RS execution of motion iHOPC): removed unverified
     engineering inference attributing dynamic K4/K5/K8/K10/K11/K14/K16/K19 solely to RS due to
     immersion water; cited ASML primary sources Ref154 Table 1 [11], Ref019 §V.B [8], Ref225 [13],
     and US 8,237,914 B2 [12] proving coupled dual-stage relative scan actuation without locking
     internal WS/RS setpoint allocation.
  2. Complete inline citation pass across ALL technical notes [注 1]-[注 14] linked to verified
     numbered Chapter 7 references [1]-[26] (also corrected Ref062/Ref015/Ref123/Ref225 metadata).
  3. Upgraded standalone T1 verification logic for motion iHOPC: added WS-T1B (11 polynomial
     trajectories, 55% 1x residual share) and RS-T1B (11 polynomial trajectories, 4x reticle side,
     45% 1x-equivalent share) on dry offline single-stage benches without requiring WS-RS sync,
     achieving exact 3-way RSS closure: sqrt(0.55^2 + 0.45^2 + 0.70^2) = 0.9975 <= 1.00.
  4. Split Lens-iHOPC into two independent tables: 6.3 T2-B (Range, 9 items) and 6.4 T2-C
     (Precision & Overlay-related dynamics, 17 items).
  5. Verified Carl Zeiss SMT wet PMI / dry-wet metrology patents (US 7,408,652 B2, US 8,836,929 B2,
     US 8,908,269 B2, US 7,796,274 B2, US 8,488,127 B2, US 8,823,948 B2, US 7,310,187 B2) [22]
     and ASML/Zeiss SPIE 5377 wet PMI evidence [21] in [注 12], while transparently stating that
     a fixed "Dry NA=0.93 + Wet NA=1.35" Starlith factory SOP is not publicly disclosed.

Typography: SimSun (宋体) 9 pt (小五) for Chinese + Times New Roman 9 pt for English/digits/units.

Run from repository root in PowerShell:
    $env:PYTHONPATH = "D:/Codex/cache/pdf-python"
    python -B outputs/code/build_nxt1965ci_subsys_spec_pdf_v3.py
"""
import html
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pymupdf as fitz

REPO = Path(__file__).resolve().parents[2]
OV4_ASSETS = REPO / "参考文献-整理版-Markdown/assets"
OUT_PDF = REPO / "outputs/reports/NXT1965Ci套刻预算分配_六大核心子系统分层验收规格需求书_v3.pdf"
WORK_ROOT = REPO / "work/subsys-spec-pdf-v3"
WORK_ROOT.mkdir(parents=True, exist_ok=True)

# Verified original paper figures on local read-only disk (never modified)
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


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def fmt(text: str) -> str:
    s = esc(text)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s


def img_uri(key: str) -> str:
    p = PAPER_IMGS[key]
    if not p.is_file():
        raise FileNotFoundError(f"Missing paper image {key}: {p}")
    return p.as_uri()


def render_table(rows: list, col2_header: str = "指标项", widths=("13.5%", "25.5%", "16%", "45%")) -> str:
    trs = []
    for idx, name, spec, test_def in rows:
        trs.append(
            "<tr>"
            f'<td class="c-idx">{esc(idx)}</td>'
            f'<td class="c-name">{fmt(name)}</td>'
            f'<td class="c-spec">{fmt(spec)}</td>'
            f'<td class="c-def">{fmt(test_def)}</td>'
            "</tr>"
        )
    return (
        '<table class="spec-tbl">'
        "<thead><tr>"
        f'<th style="width:{widths[0]}">序号</th>'
        f'<th style="width:{widths[1]}">{esc(col2_header)}</th>'
        f'<th style="width:{widths[2]}">验收规格</th>'
        f'<th style="width:{widths[3]}">标准测试定义与工装条件</th>'
        "</tr></thead>"
        "<tbody>" + "".join(trs) + "</tbody></table>"
    )


def render_fig_pair(key1: str, cap1: str, key2: str, cap2: str, max_h: str = "150pt") -> str:
    return f"""
    <div class="fig-row">
      <div class="fig-cell">
        <img src="{img_uri(key1)}" style="max-height:{max_h}" alt="{esc(cap1)}"/>
        <div class="fig-cap">{fmt(cap1)}</div>
      </div>
      <div class="fig-cell">
        <img src="{img_uri(key2)}" style="max-height:{max_h}" alt="{esc(cap2)}"/>
        <div class="fig-cap">{fmt(cap2)}</div>
      </div>
    </div>
    """


def render_fig_single(key: str, cap: str, max_h: str = "155pt") -> str:
    return f"""
    <div class="fig-single">
      <img src="{img_uri(key)}" style="max-height:{max_h}" alt="{esc(cap)}"/>
      <div class="fig-cap">{fmt(cap)}</div>
    </div>
    """


def build_chapters_part1() -> list:
    chapters = []

    # =========================================================================
    # CHAPTER 1: WS (T1-A Constant Scan + T1-B Standalone iHOPC + T2-A Sync + T2-B WRS-iHOPC)
    # =========================================================================
    ws_t1a = [
        ("WS-T1A-01", "WS-X 静止在位伺服稳定性", "≤ 0.30 nm", "离线干态单台闭环静止定位（常值目标 q_0），经 5.5 mm 等效曝光窗滑窗均值 MA 统计 3σ [注 1]"),
        ("WS-T1A-02", "WS-Y 静止在位伺服稳定性", "≤ 0.30 nm", "离线干态单台闭环静止定位，5.5 mm 等效曝光窗滑窗均值 MA 统计 3σ [注 1]"),
        ("WS-T1A-03", "WS-Rz 静止在位伺服稳定性", "≤ 0.010 μrad", "离线干态单台闭环静止定位，绕 Z 轴偏航角 MA 统计 3σ（10.0 nrad） [注 1]"),
        ("WS-T1A-04", "WS-X 单程动态运动误差 (R_uni,dyn)", "≤ 0.29 nm", "离线干态满速 0.70 m/s、35–40 m/s² 折返，匀速有效段 A–B 距离 38.5 mm，正反扫分池统计最差点 3σ [注 2]"),
        ("WS-T1A-05", "WS-Y 单程动态运动误差 (R_uni,dyn)", "≤ 0.29 nm", "离线干态满速 0.70 m/s 扫描主轴，A–B 距离 38.5 mm，正反扫分池统计匀速段最差点 3σ [注 2]"),
        ("WS-T1A-06", "WS-Rz 单程动态运动误差 (R_uni,dyn)", "≤ 0.0105 μrad", "离线干态满速扫描工况，A–B 距离 38.5 mm，绕 Z 轴偏航角分池统计匀速段最差点 3σ（10.5 nrad） [注 2]"),
        ("WS-T1A-07", "WS-X 残余反向差 (B_UD,res)", "≤ 0.09 nm", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速曝光段内正反扫平均轨迹差最大值 [注 2]"),
        ("WS-T1A-08", "WS-Y 残余反向差 (B_UD,res)", "≤ 0.10 nm", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速曝光段内正反扫平均轨迹差最大值 [注 2]"),
        ("WS-T1A-09", "WS-Rz 残余反向差 (B_UD,res)", "≤ 0.0035 μrad", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速曝光段内绕 Z 轴正反扫均值差最大值（3.5 nrad） [注 2]"),
        ("WS-T1A-10", "WS-X 往返动态运动误差 (R_bi,dyn)", "≤ 0.38 nm", "离线干态连续 N ≥ 50 组完整往返，按线性包络 R_uni,dyn + B_UD,res 取匀速段最差点判定 [注 2]"),
        ("WS-T1A-11", "WS-Y 往返动态运动误差 (R_bi,dyn)", "≤ 0.39 nm", "离线干态连续 N ≥ 50 组完整往返，线性包络 0.29 + 0.10 = 0.39 nm，取匀速段最差点判定 [注 2]"),
        ("WS-T1A-12", "WS-Rz 往返动态运动误差 (R_bi,dyn)", "≤ 0.014 μrad", "离线干态连续 N ≥ 50 组完整往返，线性包络 14.0 nrad，对应 26 mm 视场边缘 Y 套刻 ≤ 0.182 nm [注 2]"),
    ]

    ws_t1b = [
        ("WS-T1B-01", "WS-iHOPC K1 (dx, 1) 单台跟踪残差", "≤ 0.077 nm", "离线干态单台独立测试（无 RS 同步），注入 X 静态偏置 ±50 nm 指令，5.5 mm 窗 MA 拟合残差 |ΔK1|（55% 总份额） [注 4]"),
        ("WS-T1B-02", "WS-iHOPC K2 (dy, 1) 单台跟踪残差", "≤ 0.077 nm", "离线干态单台独立测试，注入 Y 静态偏置 ±50 nm 指令，5.5 mm 窗 MA 拟合残差 |ΔK2|（55% 总份额） [注 4]"),
        ("WS-T1B-03", "WS-iHOPC K4 (dy, y) 单台跟踪残差", "≤ 0.044 nm/cm", "离线干态满速 0.70 m/s 注入 ±15 nm/cm 扫向一阶变速指令，A–B 38.5 mm 内 MA 拟合残差 |ΔK4|（场角 0.073 nm） [注 4]"),
        ("WS-T1B-04", "WS-iHOPC K5 (dx, y) 单台跟踪残差", "≤ 0.044 nm/cm", "离线干态满速注入 ±15 nm/cm 非扫向一阶斜切轨迹 x(y)=k5·y，A–B 段内 MA 拟合残差 |ΔK5|（场角 0.073 nm） [注 4]"),
        ("WS-T1B-05", "WS-iHOPC K6 (dy, x) 单台跟踪残差", "≤ 0.052 nm/cm", "离线干态满速注入 ±15 nm/cm（±1.5 μrad）恒定偏航角指令 Rz=k6，A–B 段内 MA 拟合残差 |ΔK6|（5.2 nrad） [注 4]"),
        ("WS-T1B-06", "WS-iHOPC K8 (dy, y²) 单台跟踪残差", "≤ 0.026 nm/cm²", "离线干态满速注入 ±3.5 nm/cm² 扫向二阶抛物线变速轨迹，A–B 段内 MA 拟合残差 |ΔK8|（场角 0.071 nm） [注 4]"),
        ("WS-T1B-07", "WS-iHOPC K10 (dy, xy) 单台跟踪残差", "≤ 0.033 nm/cm²", "离线干态满速注入 ±3.5 nm/cm² 扫向线性动态偏航 Rz(y)=k10·y，A–B 段内 MA 拟合残差 |ΔK10|（场角 0.071 nm） [注 4]"),
        ("WS-T1B-08", "WS-iHOPC K11 (dx, y²) 单台跟踪残差", "≤ 0.026 nm/cm²", "离线干态满速注入 ±3.5 nm/cm² 非扫向二阶抛物线弯曲 x(y)=k11·y²，A–B 段内 MA 拟合残差 |ΔK11|（场角 0.071 nm） [注 4]"),
        ("WS-T1B-09", "WS-iHOPC K14 (dy, y³) 单台跟踪残差", "≤ 0.017 nm/cm³", "离线干态满速注入 ±1.5 nm/cm³ 扫向三阶变加速轨迹，A–B 段内 MA 拟合残差 |ΔK14|（场角 0.076 nm） [注 4]"),
        ("WS-T1B-10", "WS-iHOPC K16 (dy, xy²) 单台跟踪残差", "≤ 0.020 nm/cm³", "离线干态满速注入 ±1.5 nm/cm³ 扫向二阶动态偏航 Rz(y)=k16·y²，A–B 段内 MA 拟合残差 |ΔK16|（场角 0.071 nm） [注 4]"),
        ("WS-T1B-11", "WS-iHOPC K19 (dx, y³) 单台跟踪残差", "≤ 0.017 nm/cm³", "离线干态满速注入 ±1.5 nm/cm³ 非扫向三阶 S 曲线 x(y)=k19·y³，A–B 段内 MA 拟合残差 |ΔK19|（场角 0.076 nm） [注 4]"),
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
        ("WRS-T2B-06", "WRS-iHOPC K8 (dy, y²) 像面残差精度", "≤ 0.048 nm/cm²", "整机双台相对二阶变速轨迹（不限定内部分配），含 5.5 mm 狭缝平滑后的有效像面残差 |ΔK8|（场角 0.131 nm） [注 4]"),
        ("WRS-T2B-07", "WRS-iHOPC K10 (dy, xy) 像面残差精度", "≤ 0.060 nm/cm²", "整机双台相对线性动态偏航 Rz(y)（不限定内部分配），1× 像面总残差 |ΔK10|（场角 0.129 nm） [注 4]"),
        ("WRS-T2B-08", "WRS-iHOPC K11 (dx, y²) 像面残差精度", "≤ 0.048 nm/cm²", "整机双台相对横向二阶抛物线轨迹（不限定内部分配），含 5.5 mm 狭缝有效像面残差 |ΔK11|（场角 0.131 nm） [注 4]"),
        ("WRS-T2B-09", "WRS-iHOPC K14 (dy, y³) 像面残差精度", "≤ 0.030 nm/cm³", "整机双台相对三阶变加速轨迹（不限定内部分配），含 5.5 mm 狭缝有效像面残差 |ΔK14|（场角 0.135 nm） [注 4]"),
        ("WRS-T2B-10", "WRS-iHOPC K16 (dy, xy²) 像面残差精度", "≤ 0.036 nm/cm³", "整机双台相对二阶动态偏航 Rz(y)（不限定内部分配），1× 像面总残差 |ΔK16|（场角 0.127 nm） [注 4]"),
        ("WRS-T2B-11", "WRS-iHOPC K19 (dx, y³) 像面残差精度", "≤ 0.030 nm/cm³", "整机双台相对横向三阶 S 曲线轨迹（不限定内部分配），含 5.5 mm 狭缝有效像面残差 |ΔK19|（场角 0.135 nm） [注 4]"),
    ]

    ch1_html = f"""
    <h2>1.1 T1-A 验收项目（WS 单台干态常规匀速扫描与静止稳定性验收，面内 3-DOF）</h2>
    {render_table(ws_t1a)}

    <h2>1.2 T1-B 验收项目（WS 单台干态 iHOPC 多项式轨迹独立跟踪能力验收，11 项）</h2>
    {render_table(ws_t1b)}

    <h2>1.3 T2-A 验收项目（T2-WRS 双台同步性能验收）</h2>
    {render_table(wrs_t2a)}

    <h2>1.4 T2-B 验收项目（T2-WRS-iHOPC 11 项运动补偿整机最终像面精度验收）</h2>
    {render_table(wrs_t2b)}

    <h2>1.5 技术注释、测试定义细则与文献图证</h2>
    <div class="note-box">
      <p><strong>[注 1] 套刻专项范围界定、干态工装与“自己测自己”盲区：</strong>本规格书对标 NXT:1965Ci 套刻专项需求 [1]，依据曝光窗频域滤波定理（Heertjes 等，2024）[9]，滑窗均值 MA 主导套刻位移而滑窗标准差 MSD 主导成像对比度衰减，故运动台仅考核引起像面水平位移的面内 3 自由度（X、Y、Rz）之 MA 指标，垂向 Z/Rx/Ry（焦面均匀性）及 Sync MSD 均剥离至焦面/成像规格书。WS-T1 离线单台台架无浸没头与液体（干态环境）。依据运动台闭环观测链路分析（Butler，2011）[5]，输入常值目标 q<sub>0</sub> 时编码器观测误差为 q<sub>1</sub> − q<sub>0</sub>，真实物理误差满足 e<sub>true</sub> = (q<sub>1</sub> − q<sub>0</sub>) − n<sub>ENC</sub>，故须先完成第 3 章 ENC-T1 离线本底验收，并在装机后辅以外部独立干涉仪复核 [26]。</p>
      <p><strong>[注 2] A–B 扫描行程距离及单程 / 残余反向差 / 往返误差完整数学定义与计算步骤：</strong></p>
      <p class="indent">（1）<strong>A–B 距离与四段行程规定：</strong>依据 NXT:1965Ci 全视场 26 × 33 mm [1] 与 Carl Zeiss SMT 专利 US 2008/0174858 A1 Table 3 及 ASML ME3 手册（p. 70）[14] 确认的 5.5 mm 真实曝光狭缝，WS 单场扫描依次经历加速段 → 整定段（未开光）→ 匀速有效扫描段（A→B）→ 减速段。为使有效曝光区 y ∈ [−16.5, +16.5] mm 内每一点均拥有完整的 ±2.75 mm（L<sub>s</sub>/2）狭缝滑窗积分数据，规定 <strong>WS 匀速有效段 A–B 距离为 L<sub>AB,WS</sub> = 38.5 mm</strong>（两端各留 2.75 mm 狭缝缓冲，含加减速与整定段的机械往返总行程约 55–65 mm）。在有效曝光区 [−16.5, +16.5] mm 内按固定空间步距（如 0.5 mm）等距取 M 个固定空间坐标点 p<sub>1</sub>, p<sub>2</sub>, …, p<sub>M</sub>，所有趟次严格按空间坐标 p<sub>j</sub> 配准。</p>
      <p class="indent">（2）<strong>曝光窗滑窗平均（MA）与分池统计：</strong>连续执行 N ≥ 50 组完整往返（50 趟 A→B 正扫 + 50 趟 B→A 反扫）。依据曝光窗积分模型 [5, 9]，对第 k 趟扫描在空间点 p<sub>j</sub> 处的瞬时跟踪误差 e<sub>k</sub>(t)，先按狭缝积分时长 τ<sub>slit</sub> = L<sub>s</sub>/v<sub>w</sub> = 7.857 ms 求滑窗平均得 MA<sub>k</sub>(p<sub>j</sub>) = (1/τ<sub>slit</sub>) ∫<sub>t<sub>j</sub>−τ/2</sub><sup>t<sub>j</sub>+τ/2</sup> e<sub>k</sub>(t) dt。随后将正扫与反扫<strong>严格分池</strong>，在每个固定空间点 p<sub>j</sub> 分别计算样本均值与样本标准差：</p>
      <div class="eq-line">μ<sub>up</sub>(p<sub>j</sub>) = (1/N) Σ<sub>k=1..N</sub> MA<sub>k,up</sub>(p<sub>j</sub>) ，　σ<sub>up</sub>(p<sub>j</sub>) = √[ 1/(N−1) · Σ<sub>k=1..N</sub> (MA<sub>k,up</sub>(p<sub>j</sub>) − μ<sub>up</sub>(p<sub>j</sub>))² ]</div>
      <p class="indent">反扫均值 μ<sub>dn</sub>(p<sub>j</sub>) 与标准差 σ<sub>dn</sub>(p<sub>j</sub>) 按同式计算（严禁将正扫与反扫样本混合计算 3σ）。</p>
      <p class="indent">（3）<strong>三项验收指标及物理含义：</strong>① <strong>单程动态运动误差</strong> R<sub>uni,dyn</sub> = max<sub>p<sub>j</sub></sub> [ max(3σ<sub>up</sub>(p<sub>j</sub>), 3σ<sub>dn</sub>(p<sub>j</sub>)) ]，反映同向重复扫描的随机离散度（已扣除方向均值偏移），通常在刚进入曝光场的“场头”余振处取得最大值；② <strong>残余反向差</strong> B<sub>UD,res</sub> = max<sub>p<sub>j</sub></sub> |μ<sub>up</sub>(p<sub>j</sub>) − μ<sub>dn</sub>(p<sub>j</sub>)|，反映经子系统常规标定后，正扫平均路线与反扫平均路线之间的最大系统错位（对应相邻正反扫场错位；测试不限定内部采用前馈、ILC 或其他校准算法）；③ <strong>往返动态运动误差</strong> R<sub>bi,dyn</sub> = max<sub>p<sub>j</sub></sub> [ R<sub>uni,dyn</sub>(p<sub>j</sub>) + B<sub>UD,res</sub>(p<sub>j</sub>) ]，按“随机抖动 + 方向系统偏置”线性包络合成。验收时三项指标须同时达标。</p>
      <p><strong>[注 3] WRS 同步预算锚点与主从方向：</strong>整机单机套刻预算（SMO/DCO ≤ 2.50 nm）[1] 依据系统预算分配方法（Freriks 等，2006）[4] 与 Castenmiller 等（SPIE 7640，2010，Ref009 Fig. 3，见图 1-1）[2] 按方差份额拆解，L1-S1 运动台域两层 1× 预算为 X 0.744 nm / Y 0.867 nm（占核心六域方差 20.24%）。同步平均误差定义为 MA<sub>sync</sub> = MA<sub>WS</sub> − M<sub>opt</sub>·MA<sub>RS</sub>，面内 3 轴折算矩阵 M<sub>opt</sub> = diag(1/4, 1/4, 1)。表 1.3 中 Sync MA-X ≤ 0.47 nm、MA-Y ≤ 0.49 nm 直接锚定 Ref009 Fig. 10 实测值（图 1-2）[2]，由 WS（64% 方差）与 RS/4（36% 方差）保守非相关 RSS 合成（√(0.38²+0.28²)=0.472 nm、√(0.39²+0.295²)=0.489 nm），叠加 Rz 场边 13.0 mm 杠杆后两层为 0.760 nm。经专利 US 6,373,072 B1、US 2012/0319637 A1 [10] 及 Heertjes 等（2013，Ref022 Fig. 1，见图 1-3）[6] 确认，ArF/ArFi 横向同步均为 WS 主台（Master）、RS 从台（Slave）。</p>
      <p><strong>[注 4] 运动 iHOPC 执行主体的文献核证、T1 单台独立验证升级及取消 Range 限制说明：</strong></p>
      <p class="indent">（1）<strong>一手文献对执行主体的核证（修正内部架构绑死风险）：</strong>ASML 一手论文 Mulkens 等（Ref154 Table 1 与 JM3 2014）[11] 将全部 11 项运动 K 参数（K1、K2、K4、K5、K6、K8、K10、K11、K14、K16、K19）的执行器统一标为 <strong>Scan（双台相对扫描轨迹）</strong>；Heertjes 等（2020，Ref019 §V.B）[8] 与 Naaijkens（2013，Ref225 Ch. 7）[13] 均明确指出，修正动作<strong>由掩模台（RS）与晶圆台（WS）共同执行</strong>；ASML 专利 US 8,237,914 B2 [12] 亦揭示沿扫描路径的纵向缩放（K4/K8/K14）与横向偏移（K5/K11/K19）通过动态调制双台相对速度比与横向相对轨迹实现。<strong>公开文献并未宣称“因浸没头水膜约束而将动态高阶项全部交由 RS 单独执行”</strong>；事实上即使三阶 K14/K19 满档（±1.5 nm/cm³）所需附加加速度亦仅约 7.2×10<sup>−5</sup> m/s²（不足 WS/RS 额定推力的 10<sup>−5</sup>）。因此，表 1.4（WRS-T2B）取消内部主从轨迹分工限定，严格以最终 1× 像面相对轨迹 Δq(y) = q<sub>WS</sub>(y) − M<sub>opt</sub>·q<sub>RS</sub>(y) 的残差一票判定。</p>
      <p class="indent">（2）<strong>为何在离线干态阶段增设 WS-T1B（表 1.2）与 RS-T1B（表 2.2）独立验证：</strong>WS 与 RS 各自的离线干态 T1 台架不具备双台联调同步功能，但若仅验收匀速直线扫描（T1-A），无法在出厂前暴露轨迹规划器、伺服带宽与轴间解耦在非匀速/非直线多项式轨迹下的相位滞后或残余误差。为此，本版在 WS-T1B 与 RS-T1B 均增设<strong>单台合成多项式轨迹注入测试</strong>（覆盖 0/1/2/3 阶全部 11 项运动基，按标称工程激励档：0 阶 ±50 nm、1 阶 ±15 nm/cm、2 阶 ±3.5 nm/cm²、3 阶 ±1.5 nm/cm³，经狭缝滑窗 MA 后对扣名义指令求多项式拟合残差）。预算按非相关 RSS 严格闭环：<strong>WS-T1B 占 55% 幅值（30.25% 方差）</strong>，<strong>RS-T1B 占 45% 幅值（20.25% 方差，表 2.2 以 4× 掩模侧物理场边值考核）</strong>，<strong>T2 装机同步/标定/狭缝耦合占 70% 幅值（49.00% 方差）</strong>，三项合成 √(0.55² + 0.45² + 0.70²) = 0.9975 ≤ 1.00，无缝闭合表 1.4（WRS-T2B）。11 项单层场角 RSS 为 X 0.269 / Y 0.347 nm（两层 ×1.20 为 X 0.323 / Y 0.416 nm），与 Sync MA（0.760 nm）RSS 闭合 L1-S1（0.867 nm）[2, 26]。</p>
      <p class="indent">（3）<strong>为何不设运动 iHOPC 的 Range 验收项：</strong>与物镜受限于数十微米镜片机械行程不同，WS/RS 直驱行程与推力（35–150 m/s²）[1, 13] 远超工艺需求：K1/K2 调 ±200 nm 仅占百毫米级行程的百万分之一；K4/K5 调 ±50 nm/cm 仅需 0.0005% 速度微调；K8/K11 调 ±15 nm/cm² 附加加速度仅 1.5×10<sup>−4</sup> m/s²（余量 > 5 个数量级）。故运动 iHOPC 不存在量程瓶颈，仅按上述标称工程档位考核跟踪精度。</p>
    </div>

    {render_fig_pair(
        "009_fig3", "图 1-1：NXT:1950i 单机 2.50 nm 六大物理域套刻预算构成（来源：Castenmiller 等，SPIE 7640，2010，Ref009 Fig. 3 [2]）",
        "009_fig10", "图 1-2：NXT:1950i 实测双台同步误差 Sync MA-X = 0.47 nm / MA-Y = 0.49 nm（来源：Ref009 Fig. 10 [2]，直接支撑 WRS-T2A-01/02）",
        max_h="120pt"
    )}
    {render_fig_single(
        "022_fig1", "图 1-3：WS（主台 Master）误差经前馈通道送入 RS（从台 Slave）的双台同步控制架构（来源：Heertjes 等，Control Eng. Pract.，2013，Ref022 Fig. 1 [6]）",
        max_h="118pt"
    )}
    """
    chapters.append({
        "num": 1, "id": "ch-1",
        "title": "第 1 章　WS（晶圆台）子系统规格需求（含 WRS 与 iHOPC 运动补偿）",
        "toc_title": "第 1 章　WS（晶圆台）子系统规格需求（含 WRS 与 iHOPC 运动补偿）",
        "sections": [
            "1.1 T1-A 验收项目（WS 单台干态常规匀速扫描与静止稳定性验收）",
            "1.2 T1-B 验收项目（WS 单台干态 iHOPC 多项式轨迹独立跟踪能力验收）",
            "1.3 T2-A 验收项目（T2-WRS 双台同步性能验收）",
            "1.4 T2-B 验收项目（T2-WRS-iHOPC 11 项运动补偿整机最终像面精度验收）",
        ],
        "html": ch1_html,
    })

    # =========================================================================
    # CHAPTER 2: RS (T1-A Constant Scan + Micro-slip & T1-B Standalone iHOPC, 4× Dry)
    # =========================================================================
    rs_t1a = [
        ("RS-T1A-01", "RS-X 单程动态运动误差 (R_uni,dyn, 4×)", "≤ 0.84 nm", "离线干态满速 2.80 m/s、150 m/s² 折返，匀速段 A–B 距离 154.0 mm，正反扫分池统计最差点 3σ（1× 约 0.21 nm） [注 5]"),
        ("RS-T1A-02", "RS-Y 单程动态运动误差 (R_uni,dyn, 4×)", "≤ 0.88 nm", "离线干态满速 2.80 m/s 扫描主轴，A–B 距离 154.0 mm，正反扫分池统计最差点 3σ（1× 约 0.22 nm） [注 5]"),
        ("RS-T1A-03", "RS-Rz 单程动态运动误差 (R_uni,dyn, 4×)", "≤ 0.0075 μrad", "离线干态满速扫描工况，A–B 距离 154.0 mm，偏航角按 1:1 传至晶圆侧（7.5 nrad，无 4× 缩减） [注 5]"),
        ("RS-T1A-04", "RS-X 残余反向差 (B_UD,res, 4×)", "≤ 0.28 nm", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速段正反扫均值差最大值（1× 约 0.07 nm） [注 5]"),
        ("RS-T1A-05", "RS-Y 残余反向差 (B_UD,res, 4×)", "≤ 0.30 nm", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速段正反扫均值差最大值（1× 约 0.075 nm） [注 5]"),
        ("RS-T1A-06", "RS-Rz 残余反向差 (B_UD,res, 4×)", "≤ 0.0025 μrad", "离线干态完成常规标定与方向自校准后（不限定内部算法），匀速段绕 Z 轴正反扫均值差最大值（2.5 nrad） [注 5]"),
        ("RS-T1A-07", "RS-X 往返动态运动误差 (R_bi,dyn, 4×)", "≤ 1.12 nm", "离线干态连续 N ≥ 50 组完整往返，线性包络 0.84 + 0.28 = 1.12 nm（晶圆侧 1× 等效 0.28 nm） [注 5]"),
        ("RS-T1A-08", "RS-Y 往返动态运动误差 (R_bi,dyn, 4×)", "≤ 1.18 nm", "离线干态连续 N ≥ 50 组完整往返，线性包络 0.88 + 0.30 = 1.18 nm（晶圆侧 1× 等效 0.30 nm） [注 5]"),
        ("RS-T1A-09", "RS-Rz 往返动态运动误差 (R_bi,dyn, 4×)", "≤ 0.010 μrad", "离线干态连续 N ≥ 50 组完整往返，线性包络 10.0 nrad（1:1 传至晶圆侧） [注 5]"),
        ("RS-T1A-10", "RS 掩模高加减速千趟微滑移 (X 向, 4×)", "≤ 0.72 nm", "150 m/s² 满载往返扫描 1000 趟前后，以外部光学标尺测 6 寸石英掩模相对吸盘 X 累积滑移（1× 约 0.18 nm） [注 5]"),
        ("RS-T1A-11", "RS 掩模高加减速千趟微滑移 (Y 向, 4×)", "≤ 0.72 nm", "同上，测扫描主轴 Y 向千趟累积微滑移（编码器无法感知石英相对滑移，须外部独立检测，归入 L1-S5） [注 5]"),
    ]

    rs_t1b = [
        ("RS-T1B-01", "RS-iHOPC K1 等效 X 静态偏置残差 (4×)", "≤ 0.25 nm", "离线干态单台独立测试（无 WS 同步），注入 4× X 偏置 ±200 nm，22.0 mm 掩模窗 MA 残差（等效 1× ≤ 0.063 nm） [注 5]"),
        ("RS-T1B-02", "RS-iHOPC K2 等效 Y 静态偏置残差 (4×)", "≤ 0.25 nm", "离线干态单台独立测试，注入 4× Y 偏置 ±200 nm，22.0 mm 掩模窗 MA 残差（等效 1× ≤ 0.063 nm） [注 5]"),
        ("RS-T1B-03", "RS-iHOPC K4 等效 Y 一阶变速残差 (4×)", "≤ 0.24 nm", "离线满速 2.80 m/s 注入等效 ±15 nm/cm 扫向一阶变速，A–B 154 mm 拟合场边残差（等效 1× |ΔK4| ≤ 0.036 nm/cm） [注 5]"),
        ("RS-T1B-04", "RS-iHOPC K5 等效 X 一阶斜切残差 (4×)", "≤ 0.24 nm", "离线满速注入等效 ±15 nm/cm 横向一阶斜切轨迹，A–B 154 mm 拟合场边残差（等效 1× |ΔK5| ≤ 0.036 nm/cm） [注 5]"),
        ("RS-T1B-05", "RS-iHOPC K6 等效 Rz 静态偏航残差 (4×)", "≤ 0.0043 μrad", "离线满速注入 ±1.5 μrad 恒定偏航角（1:1 传递），A–B 段内 MA 残差（4.3 nrad，等效 1× |ΔK6| ≤ 0.043 nm/cm） [注 5]"),
        ("RS-T1B-06", "RS-iHOPC K8 等效 Y 二阶变速残差 (4×)", "≤ 0.24 nm", "离线满速注入等效 ±3.5 nm/cm² 扫向二阶抛物线变速，A–B 154 mm 拟合场边残差（等效 1× |ΔK8| ≤ 0.022 nm/cm²） [注 5]"),
        ("RS-T1B-07", "RS-iHOPC K10 等效 Rz 线性偏航残差 (4×)", "≤ 0.0045 μrad", "离线满速注入等效 ±3.5 nm/cm² 扫向线性动态偏航 Rz(y)，场边残差（4.5 nrad，等效 1× |ΔK10| ≤ 0.027 nm/cm²） [注 5]"),
        ("RS-T1B-08", "RS-iHOPC K11 等效 X 二阶弯曲残差 (4×)", "≤ 0.24 nm", "离线满速注入等效 ±3.5 nm/cm² 横向二阶抛物线轨迹，A–B 154 mm 拟合场边残差（等效 1× |ΔK11| ≤ 0.022 nm/cm²） [注 5]"),
        ("RS-T1B-09", "RS-iHOPC K14 等效 Y 三阶变速残差 (4×)", "≤ 0.24 nm", "离线满速注入等效 ±1.5 nm/cm³ 扫向三阶变加速轨迹，A–B 154 mm 拟合场边残差（等效 1× |ΔK14| ≤ 0.0135 nm/cm³） [注 5]"),
        ("RS-T1B-10", "RS-iHOPC K16 等效 Rz 二阶偏航残差 (4×)", "≤ 0.0044 μrad", "离线满速注入等效 ±1.5 nm/cm³ 扫向二阶动态偏航 Rz(y)，场边残差（4.4 nrad，等效 1× |ΔK16| ≤ 0.016 nm/cm³） [注 5]"),
        ("RS-T1B-11", "RS-iHOPC K19 等效 X 三阶 S 曲线残差 (4×)", "≤ 0.24 nm", "离线满速注入等效 ±1.5 nm/cm³ 横向三阶 S 曲线轨迹，A–B 154 mm 拟合场边残差（等效 1× |ΔK19| ≤ 0.0135 nm/cm³） [注 5]"),
    ]

    ch2_html = f"""
    <h2>2.1 T1-A 验收项目（RS 单台干态常规匀速扫描与微滑移验收，4× 掩模侧口径）</h2>
    {render_table(rs_t1a)}

    <h2>2.2 T1-B 验收项目（RS 单台干态 iHOPC 多项式轨迹独立跟踪能力验收，4× 掩模侧口径）</h2>
    {render_table(rs_t1b)}

    <h2>2.3 技术注释、4× 折算界面与文献图证</h2>
    <div class="note-box">
      <p><strong>[注 5] RS 干态单台口径、A–B 距离、4× → 1× 折算及 T1-B 独立 iHOPC 验证：</strong>RS 全程工作于干态 4× 掩模侧，标称扫描速度 2.80 m/s、折返加速度 150 m/s² [1, 13]。按 4:1 光学倍率放大（与第 1 章 [注 2] 严格对应 [14]），规定 <strong>RS 匀速有效测试段 A–B 距离为 L<sub>AB,RS</sub> = 4 × 38.5 = 154.0 mm</strong>（对应 4× 掩模有效曝光区 y<sub>r</sub> ∈ [−66.0, +66.0] mm 加两端各 11.0 mm 半狭缝缓冲，含加减速往返总行程约 210–230 mm），单程、残余反向差与往返包络的计算步骤与 [注 2] 完全一致 [5, 9]，且不限定内部控制或校准算法。经投影光学折算至 1× 晶圆面后，X/Y 平移缩小 4 倍，而偏航角 Rz 按 <strong>1:1 等角传递</strong>（无 4× 缩减），故表 2.1 中 RS-Rz 往返红线严控 ≤ 0.010 μrad（10.0 nrad）。RS-Z/Rx/Ry 归属焦面规格书，本表不列。RS 在高加减速下产生的石英掩模微滑移在机内编码器读数中不可见，须用外部标尺作 1000 趟前后实测（Naaijkens，2013，Ref225）[13]。依据一手文献确认 RS 与 WS 共同承担扫描方向 iHOPC 修正 [8, 11, 12, 13]，表 2.2（RS-T1B）在无 WS 同步的离线干态平台通过单台合成多项式轨迹注入，独立验收 RS 承载 45% 总像面残差份额（20.25% 方差）的 4× 场边轨迹跟踪能力（与表 1.2 WS-T1B 55% 及 T2 同步耦合 70% RSS 闭合表 1.4 WRS-T2B）。图 2-1 展示了 Evers 等（2019，Ref075 Fig. 13）[7] 在 ASML 双台平台上验证的相对同步误差累积谱改善，证明从台 RS 的高带宽与自身低重复性是压低低频同步套刻误差的前提。</p>
    </div>

    {render_fig_single(
        "075_fig13", "图 2-1：WS/RS 相对伺服误差累积频谱实测对比（虚线为无耦合，实线为同步耦合；来源：Evers 等，Control Eng. Pract. 83，2019，Ref075 Fig. 13 [7]）",
        max_h="126pt"
    )}
    """
    chapters.append({
        "num": 2, "id": "ch-2",
        "title": "第 2 章　RS（掩模台）子系统规格需求",
        "toc_title": "第 2 章　RS（掩模台）子系统规格需求",
        "sections": [
            "2.1 T1-A 验收项目（RS 单台干态常规匀速扫描与微滑移验收，4× 口径）",
            "2.2 T1-B 验收项目（RS 单台干态 iHOPC 多项式轨迹独立跟踪能力验收，4× 口径）",
        ],
        "html": ch2_html,
    })

    # =========================================================================
    # CHAPTER 3: ENC (2D Optical Grating Encoder — Minimal Pure Sensor T1 + T2)
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

    ch3_html = f"""
    <h2>3.1 T1 验收项目（纯 ENC 传感器离线干态测量本底验收）</h2>
    {render_table(enc_t1)}

    <h2>3.2 T2 验收项目（Gridplate 长期稳定性与读数头切换 Handover 验收）</h2>
    {render_table(enc_t2)}

    <h2>3.3 技术注释、频域核算与实测文献图证</h2>
    <div class="note-box">
      <p><strong>[注 6] ENC-T1 纯传感器本底定义（2 项）与文献锚点：</strong>在 T1 离线干态验收阶段，ENC 仅作为独立位移量测传感器，不绑定 WS/RS 台体坐标系，在刚性锁死参考光栅（无伺服激励）上考核两项本底：① <strong>原始 1000 Hz 带宽重复性 ≤ 0.22 nm</strong>，直接对齐 Castenmiller 等（SPIE 7640，2010，Ref009 Fig. 4，见图 3-1）[2] 公布的 NXT 短固定光程（< 15 mm）二维光栅编码器实测值 0.22 nm，用于验证传感器本底及伺服反馈高频输入正常，出厂须同步交付 0.1 Hz–2 kHz PSD/CPS 频谱（Heertjes 等，2024）[9]；② <strong>曝光窗口平滑后重复性 ≤ 0.13 nm</strong>，按 5.5 mm 狭缝与 0.70 m/s 扫速对应等效噪声带宽 B<sub>ENBW</sub> = 1/(2τ<sub>slit</sub>) = 63.64 Hz [9, 14]，以 30% 低频气流有色噪声 + 70% 高频白噪声合成得 σ<sub>ENC,MA</sub> = √(0.30×0.22² + 0.70×0.22²×63.64/936.4) = 0.130 nm [26]，满足相对 WS-X（0.38 nm）的 1:3 计量精度原则（掩模侧 4× 通道带宽与多普勒余量按硬件选型作 T2 装机核查，本表不重复列项）。</p>
      <p><strong>[注 7] ENC-T2 仅保留闭环无法覆盖的 3 项基准指标：</strong>WS-T1 与 RS-T1 依赖 ENC 闭环监测误差，无法察觉“尺子自身的长期漂移与跨缝跳变”[5, 26]。因此 T2 专项验收：① <strong>Gridplate 7 天热机械稳定性 ≤ 0.20 nm</strong>，直接对标 de Jong 等（SPIE 7274，2009，Ref062 Fig. 11，见图 3-2）[15] 连续 156 小时实测结果（< 0.20 nm），须借独立参考片或 13×19 多移位标定验证（Mulkens 等，2014）[11]；② <strong>X/Y 读数头切换（Handover）各 ≤ 0.15 nm</strong>（Ref009 Fig. 7）[2]，防止过缝零点偏置被伺服闭环吸收。多读数头四角差分导出的 Rz 角本底（WS 侧 ≤ 1.6 nrad，RS 侧 ≤ 2.8 nrad）已内嵌于 WS-T1/RS-T1 闭环，仅作装机 1:3 故障隔离校核。ENC 全项均内嵌于 WRS 闭环，严禁重复计入顶层 SMO 预算 [26]。</p>
    </div>

    {render_fig_pair(
        "009_fig4", "图 3-1：NXT 短固定光程（< 15 mm）二维光栅编码器 1000 Hz 噪声实测 0.22 nm 3σ（来源：Castenmiller 等，SPIE 7640，Ref009 Fig. 4 [2]，支撑 ENC-T1-01）",
        "062_fig11", "图 3-2：Gridplate 连续一周（12 h–156 h）X/Y 全局网格热机械稳定性实测 < 0.20 nm（来源：de Jong 等，SPIE 7274，2009，Ref062 Fig. 11 [15]，支撑 ENC-T2-01）",
        max_h="142pt"
    )}
    """
    chapters.append({
        "num": 3, "id": "ch-3",
        "title": "第 3 章　ENC（光栅编码器测量）子系统规格需求",
        "toc_title": "第 3 章　ENC（光栅编码器测量）子系统规格需求",
        "sections": [
            "3.1 T1 验收项目（纯 ENC 传感器离线干态测量本底验收）",
            "3.2 T2 验收项目（Gridplate 长期稳定性与读数头切换 Handover 验收）",
        ],
        "html": ch3_html,
    })

    return chapters


def append_chapters_part2(chapters: list) -> list:
    # =========================================================================
    # CHAPTER 4: AA (Wafer Alignment — Dry T1 + Dry M-side T2 + Dual-Stage T3)
    # =========================================================================
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

    ch4_html = f"""
    <h2>4.1 T1 验收项目（AA 底层传感器离线干态超稳平台验收，3 项不分 X/Y）</h2>
    {render_table(aa_t1)}

    <h2>4.2 T2 验收项目（模拟 M-side 干态量测端 FIWA / HOWA 集成验收）</h2>
    {render_table(aa_t2)}

    <h2>4.3 T3 验收项目（双台整机联调 M-to-E 对准基线短期漂移验收）</h2>
    {render_table(aa_t3)}

    <h2>4.4 技术注释与实测文献图证</h2>
    <div class="note-box">
      <p><strong>[注 8] 干态测试边界、单标记静态（T1）与动态（T2）重复性定义：</strong>TWINSCAN 双台机 M 侧晶圆对准全过程处于干态环境，无浸没液体 [2, 21]。相位光栅对准（PGA）原理需带动标记匀速扫过照明光斑并提取干涉相位（<em>Applied Optics</em>，2025）[18]，因此 T1“静态重复性（≤ 0.22 nm）”并非晶圆绝对静止，而是在离线超稳参考扫描台（无宏动加减速激振）上扣除参考位移后的纯传感器本底，直接对标 de Graaf 等（SPIE 9780，2016，Ref015 Fig. 10，见图 4-1）[16] 公布的 SMASH 实测曲线（强光 WQ ≥ 1% 约 0.15–0.25 nm；弱光 WQ 0.1%–1% 约 0.25–0.50 nm）。<strong>单趟扫描内采集的多组样点不可充当独立重复</strong>，须完整进出标记独立重扫 ≥ 30 趟 [26]。T2 在模拟 M 侧平台上叠加产线步进折返节拍，合成 ≤ 0.38 nm。</p>
      <p><strong>[注 9] 四色多波长配准稳定性（≤ 0.32 nm）的文献支撑：</strong>CMP 与刻蚀引起的标记不对称会破坏衍射相位对称性并产生对准位置偏差（APD/WAD）。多波长方案利用不同波长在工艺膜层中的差异化相位灵敏度做加权融合，可显著压低晶圆间套刻波动——Menchtchikov 等（SPIE 10587，2018，Ref252 Fig. 3，见图 4-2）[17] 证实基于实测的多色加权（OCW）可将套刻波动降低 0.8–1.3 nm。其前提是仪器自身四通道 24 h 色间漂移足够小（≤ 0.32 nm）且单色可用率稳定，否则仪器色差漂移会被误判为工艺不对称 [17, 26]。表中验收不限定具体融合算法，仅约束硬件色间配准稳度。</p>
      <p><strong>[注 10] HOWA（T2）与 M-to-E 基线漂移（T3）分级与预算闭合：</strong>HOWA（≤ 0.40 nm，须正反扫方向配平以避免 Pike 等在 SPIE 8324，2012，Ref123 [18] 报道的 > 3.5 nm 方向混叠虚假网格）在干态模拟 M 侧平台（T2）独立验收；M-to-E 短期漂移（≤ 0.30 nm）跨 MF 框架连接 M 侧与 E 侧，归入 T3 整机联调。T2 与 T3 按 RSS 合成为单层 0.500 nm（两层 0.707 nm），与第 5 章 PARIS（两层 0.665 nm）[3] 共同闭合 L1-S2（0.970 nm，占 Ref009 六域方差 25.38%）[2, 26]。产品工艺不对称残差（WAD ≤ 0.50 nm）归入客户产品片工艺验证边界，不计入参考片验收。</p>
    </div>

    {render_fig_pair(
        "015_fig10", "图 4-1：SMASH 对准重复性随信号质量 WQ 变化实测（WQ≥1% 约 0.15–0.25 nm；WQ 0.1–1% 约 0.25–0.50 nm；来源：de Graaf 等，SPIE 9780，2016，Ref015 Fig. 10 [16]）",
        "252_fig3", "图 4-2：多波长加权融合（OCW）较单色方案将晶圆间套刻波动压低 0.8 nm 实测对比（来源：Menchtchikov 等，SPIE 10587，2018，Ref252 Fig. 3 [17]）",
        max_h="205pt"
    )}
    """
    chapters.append({
        "num": 4, "id": "ch-4",
        "title": "第 4 章　AA（晶圆对准）子系统规格需求",
        "toc_title": "第 4 章　AA（晶圆对准）子系统规格需求",
        "sections": [
            "4.1 T1 验收项目（AA 底层传感器离线干态超稳平台验收，3 项）",
            "4.2 T2 验收项目（模拟 M-side 干态量测端 FIWA / HOWA 集成验收）",
            "4.3 T3 验收项目（双台整机联调 M-to-E 对准基线短期漂移验收）",
        ],
        "html": ch4_html,
    })

    # =========================================================================
    # CHAPTER 5: TIS + PARIS (Overlay-only T1)
    # =========================================================================
    tp_t1 = [
        ("TP-T1-01", "TIS 水平空间像对准重复性 (X 向)", "≤ 0.40 nm", "E-side 曝光端 193 nm 湿区在机透射空间像扫描，连续 ≥ 30 次对准解算 3σ（附供水流量窗核验） [注 11]"),
        ("TP-T1-02", "TIS 水平空间像对准重复性 (Y 向)", "≤ 0.40 nm", "同上，E-side 曝光端 193 nm 湿区 Y 向空间像对准重复性 3σ（用于 M-to-E 基线定期清零） [注 11]"),
        ("TP-T1-03", "双台 TIS-1 / TIS-2 匹配稳定性 (X 向)", "≤ 0.28 nm", "整机双台交换工况下，24 h 内双传感板相对 X 位置漂移 3σ（直控双卡盘套刻差 ΔC2C ≤ 0.48 nm） [注 11]"),
        ("TP-T1-04", "双台 TIS-1 / TIS-2 匹配稳定性 (Y 向)", "≤ 0.28 nm", "同上，24 h 内双晶圆台 TIS 基准板 Y 向相对匹配漂移 3σ [注 11]"),
        ("TP-T1-05", "PARIS 7 视场点掩模对准重复性 RA (X 向)", "≤ 0.47 nm", "E-side 7 视场点并行空间像掩模对准重复性 3σ，对标 Ref066 §3.4（< 0.50 nm，两层 0.665 nm） [注 11]"),
        ("TP-T1-06", "PARIS 7 视场点掩模对准重复性 RA (Y 向)", "≤ 0.47 nm", "同上，7 视场点并行 Y 向掩模对准重复性 3σ（与 AA 0.707 nm 共同闭合 L1-S2 = 0.970 nm） [注 11]"),
        ("TP-T1-07", "PARIS 奇像差波前测量重复性", "≤ 0.14 nm RMS", "E-side 193 nm 湿区在机波前反演重复性 RMS，为第 6 章奇像差闭环调控提供 1:3 计量精度支撑 [注 11]"),
    ]

    ch5_html = f"""
    <h2>5.1 T1 验收项目（E-side 在机空间像对准与奇像差波前测量验收）</h2>
    {render_table(tp_t1)}

    <h2>5.2 技术注释、单级边界与实测文献图证</h2>
    <div class="note-box">
      <p><strong>[注 11] 单级验收（T1）、套刻范围精简与装机湿区工况说明：</strong>TIS（6 kHz 透射空间像基准）与 PARIS（7 视场点并行空间像传感器，见图 5-1）[3] 均直接工作于 193.368 nm 曝光光路与 E 侧投影物镜像面，物理上须在装机 E 侧（含正常超纯水浸没液膜，非干态离线）执行，不涉及类似 AA 的 M 侧全片步进调度，故统一设为 <strong>T1 单级验收</strong>（其中 TP-T1-03/04 双台匹配须在双台交换工况下测试）。按套刻专项范围原则，纯焦面项（TIS 最佳焦面 Z、PARIS 场曲 Z）已剥离至焦面规格书。文献依据：① de Boeij 等（SPIE 8683，2013，Ref066 §3.4 & Fig. 6）[3] 公布 PARIS 7 点掩模对准重复性规格 < 0.50 nm，本表定限 ≤ 0.47 nm（两层 0.665 nm，与 AA 0.707 nm 闭合 L1-S2 = 0.970 nm）[2, 26]；② Ma 等（SPIE 6518，2007，Ref164）[20] 证实浸没超纯水（UPW）供回水流量波动会调制 TIS 测位重复性，故 TP-T1-01/02 须在标称供水流量工作窗内复核；③ Duclaux 等（SPIE 11325，2020，Ref100 Fig. 9，见图 5-2）[19] 揭示双卡盘（C2 vs C1）切换时会诱发 K7/K12/K13 低阶参考偏置，故 TP-T1-03/04 严控双台基准 24 h 相对漂移 ≤ 0.28 nm，并在整机启用双卡盘参考匹配。</p>
    </div>

    {render_fig_pair(
        "066_fig6", "图 5-1：PARIS 7 视场点并行空间像传感器结构示意（支持每片 3 扫，公开 RA < 0.50 nm；来源：de Boeij 等，SPIE 8683，2013，Ref066 Fig. 6 [3]）",
        "100_fig9", "图 5-2：双卡盘（C2 vs C1）未匹配时诱发的 K7/K13/K12 低阶偏置实测（来源：Duclaux 等，SPIE 11325，2020，Ref100 Fig. 9 [19]，支撑双台 TIS 匹配）",
        max_h="142pt"
    )}
    """
    chapters.append({
        "num": 5, "id": "ch-5",
        "title": "第 5 章　TIS + PARIS（E-side 空间像传感）子系统规格需求",
        "toc_title": "第 5 章　TIS + PARIS（E-side 空间像传感）子系统规格需求",
        "sections": [
            "5.1 T1 验收项目（E-side 在机空间像对准与奇像差波前测量验收）",
        ],
        "html": ch5_html,
    })

    # =========================================================================
    # CHAPTER 6: Lens (193 nm / NA 1.35)
    #   - 6.1 T1: Z7..Z63 Static Absolute Ceiling + K20 Static
    #   - 6.2 T2-A: Post-LensModel Adjustment Residual (Z7..Z27 + high-order + RMS)
    #   - 6.3 T2-B: Dynamic Lens-iHOPC Range Table (9 items)
    #   - 6.4 T2-C: Dynamic Lens-iHOPC Precision & Overlay Dynamics Table (17 items)
    # =========================================================================
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
    ln_t1 = []
    for k, (zc, flim, rmsv, ovlv, tag) in enumerate(odd_z, 1):
        ln_t1.append((
            f"LN-T1-{k:02d}",
            zc,
            f"≤ {flim:.2f} nm",
            f"离线局部静态超纯水浸没干涉平台（wet PMI，λ=193.368 nm，NA=1.35）冷机绝对上限；{tag}，等效 ≤ {rmsv:.4f} nm RMS（单轴套刻 {ovlv:.3f} nm） [注 12]"
        ))
    ln_t1.append((
        "LN-T1-31",
        "K20 (dy, x³) 冷机静畸变",
        "≤ 0.18 nm/cm³",
        "NXT:1965Ci 不配 K20 主动操纵器，冷机装调出厂静态畸变上限（归入跨机匹配 MMO-M2） [注 13]"
    ))

    # Layer 2: Post-LensModel adjustment residuals (T2-A)
    adj_z = [
        ("Z7",  0.12, "1θ X 彗差"),  ("Z8",  0.12, "1θ Y 彗差"),
        ("Z10", 0.11, "3θ X 三叶草"), ("Z11", 0.11, "3θ Y 三叶草"),
        ("Z14", 0.12, "1θ X 二阶彗差"), ("Z15", 0.12, "1θ Y 二阶彗差"),
        ("Z19", 0.14, "3θ X 二阶三叶草"), ("Z20", 0.14, "3θ Y 二阶三叶草"),
        ("Z23", 0.16, "1θ X 三阶彗差"), ("Z24", 0.16, "1θ Y 三阶彗差"),
        ("Z26", 0.11, "5θ X 五叶草"), ("Z27", 0.11, "5θ Y 五叶草"),
    ]
    ln_t2a = []
    for k, (zc, rlim, desc) in enumerate(adj_z, 1):
        ln_t2a.append((
            f"LN-T2A-{k:02d}",
            zc,
            f"≤ {rlim:.2f} nm",
            f"任意一次经 LensModel 下发波前/畸变调节指令后，实测与目标差 |Z_meas − Z_target| 上限（{desc}，约 55% 静态限值） [注 12]"
        ))
    ln_t2a.extend([
        ("LN-T2A-13", "Z30–Z63 调节伴生残差增量", "≤ 0.05 nm", "任意一次 LensModel 调节前后，非主动驱动高阶奇像差单项附加变化量上限 [注 12]"),
        ("LN-T2A-14", "Z5–Z64 全瞳调整后合成残差", "≤ 0.22 nm RMS", "任意一次 LensModel 调节后，全瞳 30 项奇像差总偏差 RMS 上限（且绝对值仍不突破 T1 上限） [注 12]"),
    ])

    # Split Table 6.3: Dynamic Lens-iHOPC Range ONLY (T2-B)
    ln_t2b_range = [
        ("LN-T2B-01", "Lens-iHOPC K3 (dx, x) 补偿调节范围", "±50–100 nm/cm", "用户单场有效量程（硬件极限 ±150–250 nm/cm，即 ±15–25 ppm），镜片与波长协同 [注 13]"),
        ("LN-T2B-02", "Lens-iHOPC K7 (dx, x²) 补偿调节范围", "±10.0 nm/cm²", "用户单场有效量程，沿狭缝横向二阶拉伸畸变补偿 [注 13]"),
        ("LN-T2B-03", "Lens-iHOPC K9 (dx, xy) 补偿调节范围", "±8.0 nm/cm²", "用户单场有效量程，扫描中镜片动态随动梯形补偿 [注 13]"),
        ("LN-T2B-04", "Lens-iHOPC K12 (dy, x²) 补偿调节范围", "±10.0 nm/cm²", "用户单场有效量程，沿狭缝横向二阶弓形补偿 [注 13]"),
        ("LN-T2B-05", "Lens-iHOPC K13 (dx, x³) 补偿调节范围", "±6.0 nm/cm³", "用户单场有效量程，沿狭缝横向三阶畸变补偿 [注 13]"),
        ("LN-T2B-06", "Lens-iHOPC K15 (dx, x²y) 补偿调节范围", "±4.0 nm/cm³", "用户单场有效量程，三阶动态混合项补偿 [注 13]"),
        ("LN-T2B-07", "Lens-iHOPC K17 (dx, xy²) 补偿调节范围", "±4.0 nm/cm³", "用户单场有效量程，三阶动态混合项补偿（掩模热演进项） [注 13]"),
        ("LN-T2B-08", "Lens-iHOPC K18 (dy, yx²) 补偿调节范围", "±4.0 nm/cm³", "用户单场有效量程，三阶动态混合项补偿（掩模热主修正项） [注 13]"),
        ("LN-T2B-09", "iHOPC 8 项联合量程占用上限", "≤ 80% Range", "8 项激活 K 参数同时施加标称满量程指令时，任一镜片执行器机械行程不饱和 [注 14]"),
    ]

    # Split Table 6.4: Dynamic Lens-iHOPC Precision & Overlay Dynamics (T2-C)
    ln_t2c_prec = [
        ("LN-T2C-01", "Lens-iHOPC K3 (dx, x) 补偿调节精度", "≤ 0.120 nm/cm", "总验收残差 |ΔK3|，最小步长 ≤ 0.012 nm/cm（场角贡献 0.156 nm，双档 4/15 核验） [注 13]"),
        ("LN-T2C-02", "Lens-iHOPC K7 (dx, x²) 补偿调节精度", "≤ 0.092 nm/cm²", "总验收残差 |ΔK7|，最小步长 ≤ 0.009 nm/cm²（场角贡献 0.155 nm） [注 13]"),
        ("LN-T2C-03", "Lens-iHOPC K9 (dx, xy) 补偿调节精度", "≤ 0.072 nm/cm²", "总验收残差 |ΔK9|，最小步长 ≤ 0.007 nm/cm²（场角贡献 0.154 nm） [注 13]"),
        ("LN-T2C-04", "Lens-iHOPC K12 (dy, x²) 补偿调节精度", "≤ 0.092 nm/cm²", "总验收残差 |ΔK12|，最小步长 ≤ 0.009 nm/cm²（场角贡献 0.155 nm） [注 13]"),
        ("LN-T2C-05", "Lens-iHOPC K13 (dx, x³) 补偿调节精度", "≤ 0.070 nm/cm³", "总验收残差 |ΔK13|，最小步长 ≤ 0.007 nm/cm³（场角贡献 0.154 nm） [注 13]"),
        ("LN-T2C-06", "Lens-iHOPC K15 (dx, x²y) 补偿调节精度", "≤ 0.054 nm/cm³", "总验收残差 |ΔK15|，最小步长 ≤ 0.005 nm/cm³（场角贡献 0.151 nm） [注 13]"),
        ("LN-T2C-07", "Lens-iHOPC K17 (dx, xy²) 补偿调节精度", "≤ 0.042 nm/cm³", "总验收残差 |ΔK17|，最小步长 ≤ 0.004 nm/cm³（场角贡献 0.149 nm） [注 13]"),
        ("LN-T2C-08", "Lens-iHOPC K18 (dy, yx²) 补偿调节精度", "≤ 0.054 nm/cm³", "总验收残差 |ΔK18|，最小步长 ≤ 0.005 nm/cm³（场角贡献 0.151 nm） [注 13]"),
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

    ch6_html = f"""
    <h2>6.1 T1 验收项目（离线冷机静态波前上限与 K20 静畸变，λ = 193.368 nm）</h2>
    {render_table(ln_t1, col2_header="指标项（Fringe Zernike 系数，193 nm）", widths=("12%", "20%", "15.5%", "52.5%"))}

    <h2>6.2 T2-A 验收项目（任意一次 LensModel 调节后的奇像差调节残差验收）</h2>
    {render_table(ln_t2a, col2_header="指标项（Fringe Zernike 系数，调节残差）", widths=("13%", "21.5%", "15.5%", "50%"))}

    <h2>6.3 T2-B 验收项目（动态 Lens-iHOPC 补偿调节范围 Range 验收表）</h2>
    {render_table(ln_t2b_range, widths=("13%", "27.5%", "16.5%", "43%"))}

    <h2>6.4 T2-C 验收项目（动态 Lens-iHOPC K 参数调节精度与套刻相关动态考核表）</h2>
    {render_table(ln_t2c_prec, widths=("13%", "27.5%", "16.5%", "43%"))}

    <h2>6.5 技术注释、Zeiss 干/湿测量专利核证与实测文献图证</h2>
    <div class="note-box">
      <p><strong>[注 12] NA = 1.35 物镜离线 T1 湿态耦合、Zeiss 干/湿测量专利核证及 Odd Zernike 两层定义：</strong></p>
      <p class="indent">（1）<strong>湿态全瞳验收的物理必然性与 Carl Zeiss SMT 一手论文/专利证据：</strong>依据 NA = n·sin(θ) = 1.35 [14]，若末片熔融石英（n ≈ 1.56）下方为空气（n<sub>air</sub> ≈ 1.0003），1.0 < NA ≤ 1.35 外瞳光线将在玻璃-空气界面发生<strong>全内反射（TIR）</strong>，干态下完全无法出射测量。ASML 与 Carl Zeiss SMT 联合论文 Streefkerk 等（SPIE 5377，2004，Ref040 Fig. 7）[21] 直接披露 Zeiss 在出厂离线阶段即采用<strong>湿态相移干涉仪（wet PMI）</strong>验收浸没物镜波前；Carl Zeiss SMT 专利族 <strong>US 7,408,652 B2、US 8,836,929 B2、US 8,908,269 B2</strong> 及 <strong>US 7,796,274 B2、US 8,488,127 B2、US 8,823,948 B2</strong> [22] 进一步披露了在末片与衍射/参考载体之间构建局部静态浸没液池、采用保护窗口隔绝液膜退化并克服干态 TIR 盲区的离线湿态干涉测量系统（与整机 0.70 m/s 扫描浸没头流场扰动不同）。此外，Zeiss 专利 <strong>US 7,310,187 B2</strong> [22] 披露了物镜在干态与浸没态之间切换装调的方法。</p>
      <p class="indent">（2）<strong>关于“是否同时在 Dry（NA = 0.93）与 Wet（NA = 1.35）双状态测试”的核查边界：</strong>经核查公开 Zeiss 专利与 SPIE 论文库，<strong>尚无公开文献明文记载 Zeiss 对 NA = 1.35（Starlith 19xx）物镜固定执行“先 Dry（NA = 0.93）测、再 Wet（NA = 1.35）测”双阶段出厂检验 SOP</strong>（NA = 0.93 为传统干式 193 nm 物镜如 XT:1400 的量产上限；Starlith 工厂内部是否保留干态缩瞳预检步骤属于未公开细节）。工程装调中可在干态缩瞳（NA < 1.0，如 ≤ 0.93）作早期镜组初调与无水风险排查，但受 TIR 限制无法覆盖 1.0 < NA ≤ 1.35 外瞳，故 <strong>T1 出厂全瞳波前（NA = 1.35）最终验收必须且只能以局部静态超纯水浸没 wet PMI 为准</strong> [21, 22]。</p>
      <p class="indent">（3）<strong>Odd Zernike 两层需求闭环：</strong>第一层（表 6.1，T1）约束冷机绝对奇像差上限，按 Fringe Zernike 系数（λ = 193.368 nm，单位 nm）全 30 项单轴 RSS 为 1.196 nm Fringe、全瞳 0.400 nm RMS（Coma 单轴 ≤ 0.190 nm RMS），经 2D Abbe 仿真与 IBM/ASML 实测表（Halle 等，SPIE 8326，2012，RefN6 Table 4，Z10 = −0.88 吻合度 2.8%）[23] 核验，跨照明切换单轴套刻包络 ≤ 0.437 nm（Abbe 实算 0.388 nm），匹配 Staals 等（SPIE 7973，2011，Ref024 Fig. 11，见图 6-1）[23] 的 FlexWave 实测水平（Coma 约 0.16 nm RMS）。第二层（表 6.2，T2-A）约束任意一次调用 LensModel 执行波前/畸变调节前后的实测残差 |Z<sub>meas</sub> − Z<sub>target</sub>|（主可调阶次 Z7–Z27 约 55% 静态限值，全瞳总残差 ≤ 0.22 nm RMS），且调后绝对波前不得突破表 6.1 上限 [26]。</p>
      <p><strong>[注 13] T1 K20 静畸变剥离与 T2-B/T2-C 动态 Lens-iHOPC 预算闭环：</strong>依据 Smeets 等（SPIE 12051，2022，Ref254 §2.4）[25]，NXT:1965Ci 不配 K20（dy, x³）场平面主动操纵器（至 NXT:2050i 起开放），故将 K20 归入 T1 冷机出厂静态畸变（≤ 0.18 nm/cm³，归入 MMO-M2）。依据 Mulkens 等 [11] 19 参 iHOPC 框架及 Kim 等（RHC2，Ref016）[25] 掩模热演化规律（K17/K18），表 6.3（T2-B 量程）与表 6.4（T2-C 精度）分表考核 8 项激活 K 参数（X 向 6 项 K3/K7/K9/K13/K15/K17 单层场角 RSS 0.375 nm；Y 向 2 项 K12/K18 单层 0.216 nm），两层 ×1.20 为 X 0.450 / Y 0.260 nm，与奇像差及热声项共同闭合 L1-S3（X 0.667 / Y 0.557 nm，占 Ref009 六域方差 11.99%）[2, 26]。放大率换算为 1 nm/cm = 0.1 ppm，对应 SET-vs-GET 精度 3.0%–5.6%，直接参照 ASML/Carl Zeiss SMT 联合物镜畸变操纵器实测结果（Klinkhamer 等，Ref253 Fig. 8，见图 6-2；Pollak 等，SPIE 11327，2020，RefN4）[24]。</p>
      <p><strong>[注 14] 表 6.3 / 6.4 套刻相关联合行程与动态考核依据：</strong>与运动台不同，物镜镜片物理微动行程稀缺且多参共用执行器矩阵 [24, 25]，因此表 6.3-09 考核 8 项联合行程占用 ≤ 80% Range 防饱和，表 6.4-09 至 6.4-17 同步考核最小步长 ≤ Spec/10、单向重复 ≤ 35%、双向滞回 ≤ 25%、跨 K 串扰 ≤ 30% 且诱发奇像差 ≤ 0.05 nm RMS [23, 24]、静态整定 20–50 ms 与动态扫描同步相位滞后 ≤ 0.20 ms [25]，以及 15 s / 15 min / 24 h 保持漂移（纯焦面串扰漂移划归焦面规格书）[26]。</p>
    </div>

    {render_fig_pair(
        "024_fig11", "图 6-1：FlexWave 波前控制后各奇像差残差实测（Coma X/Y 约 0.16 nm RMS；来源：Staals 等，SPIE 7973，2011，Ref024 Fig. 11 [23]，支撑表 6.1/6.2）",
        "253_fig8", "图 6-2：物镜畸变操纵器沿 −13..+13 mm 狭缝 Target (SET) vs Measured (GET) 实测残差（来源：Klinkhamer 等，ASML/Zeiss，Ref253 Fig. 8 [24]，支撑表 6.4 精度）",
        max_h="122pt"
    )}
    """
    chapters.append({
        "num": 6, "id": "ch-6",
        "title": "第 6 章　Lens（投影物镜）子系统规格需求",
        "toc_title": "第 6 章　Lens（投影物镜）子系统规格需求",
        "sections": [
            "6.1 T1 验收项目（离线冷机静态波前上限 Z7–Z63 + K20 静畸变）",
            "6.2 T2-A 验收项目（任意一次 LensModel 调节后的奇像差调节残差）",
            "6.3 T2-B 验收项目（动态 Lens-iHOPC 补偿调节范围 Range 验收表）",
            "6.4 T2-C 验收项目（动态 Lens-iHOPC K 参数调节精度与套刻相关动态考核表）",
        ],
        "html": ch6_html,
    })

    # =========================================================================
    # CHAPTER 7: Verified Numbered References [1]-[26]
    # =========================================================================
    refs = [
        "ASML Official Product Specification. <em>TWINSCAN NXT:1965Ci</em> (193 nm, NA 1.35, DCO ≤ 2.5 nm, MMO ≤ 4.5 nm, ≥ 250 wph, FlexRay, PARIS). https://www.asml.com",
        "Castenmiller, T., van de Mast, F., de Kort, T., et al. (2010). Towards ultimate optical lithography with NXT:1950i dual stage immersion platform. <em>Proc. SPIE</em> 7640, 76401N. DOI: 10.1117/12.847025 [Ref009 Fig. 3 / Fig. 4 / Fig. 7 / Fig. 10].",
        "de Boeij, W., Pieternella, R., Bouchoms, I., et al. (2013). Extending immersion lithography down to 1x nm production nodes. <em>Proc. SPIE</em> 8683, 86831L [Ref066 §3.4 & Fig. 6, PARIS RA < 0.50 nm].",
        "Freriks, H. J. M., Heemels, W. P. M. H., Muller, G. J., & Sandee, J. H. (2006). On the systematic use of budget-based design. <em>INCOSE International Symposium</em>, 16(1), 1072–1086. DOI: 10.1002/j.2334-5837.2006.tb02781.x [Ref146].",
        "Butler, H. (2011). Position control in lithographic equipment: an enabler for current-day chip manufacturing. <em>IEEE Control Systems Magazine</em>, 31(5), 28–47. DOI: 10.1109/MCS.2011.941653 [Ref094].",
        "Heertjes, M. F., Temizer, B., & Schneiders, M. (2013). Self-tuning in master–slave synchronization of high-precision stage systems. <em>Control Engineering Practice</em>, 21(12), 1706–1715. DOI: 10.1016/j.conengprac.2013.08.007 [Ref022 Fig. 1].",
        "Evers, E., van de Wal, M., & Oomen, T. (2019). Beyond decentralized wafer/reticle stage control design: A double-Youla approach for enhancing synchronized motion. <em>Control Engineering Practice</em>, 83, 21–32. DOI: 10.1016/j.conengprac.2018.10.011 [Ref075 Fig. 13].",
        "Heertjes, M. F., Butler, H., Dirkx, N. J., et al. (2020). Control of wafer scanners: Methods and developments (ASML/TU/e Survey, §V.B Reticle heating error correction by both reticle and wafer stage) [Ref019].",
        "Heertjes, M. F., et al. (2024). Frequency-domain MA/MSD filtering theorems and exposure window analysis for wafer scanners. <em>Proc. IEEE ECC 2024</em>. DOI: 10.23919/ECC64448.2024.10591183 [RefN8].",
        "ASML US Patent 6,373,072 B1 (2002) [S14] & Nikon US Patent App. 2012/0319637 A1 [S12] (WS Master / RS Slave synchronized scan architecture).",
        "Mulkens, J., Kubis, M., Hinnen, P., et al. (2013). High order field-to-field corrections for imaging and overlay to achieve sub 20-nm lithography requirements [Ref154 Eq. (1) & Table 1]; Mulkens, J., Hinnen, P., Kubis, M., et al. (2014). Holistic optimization architecture enabling sub-14-nm projection lithography. <em>J. Micro/Nanolith. MEMS MOEMS</em>, 13(1), 011006. DOI: 10.1117/1.JMM.13.1.011006 [RefN7].",
        "ASML Netherlands B.V. US Patent 8,237,914 B2 (2012). <em>Process, apparatus, and device for determining intra-field correction to correct overlay errors between overlapping patterns</em> (dynamic relative scan speed ratio and transverse trajectory modulation between reticle stage and wafer stage).",
        "Naaijkens, G. P. (2013). <em>Reticle side wall clamping</em>. PhD Thesis, Eindhoven University of Technology (TU/e). DOI: 10.6100/IR756525 [Ref225 §2.1, §6.3.4, Ch. 7 — reticle micro-slip & dual-stage iHOPC positioning].",
        "Carl Zeiss SMT AG. US Patent App. 2008/0174858 A1, Table 3 (NA = 1.35 catadioptric projection lens, 26 × 5.5 mm slit) [RefN1]; ASML Training Manual <em>12-TT-L3-L3-ME</em> (p. 70).",
        "de Jong, F., van der Pasch, B., Castenmiller, T., Vleeming, B., Droste, R., & van de Mast, F. (2009). Enabling the lithography roadmap: an immersion tool based on a novel stage positioning system. <em>Proc. SPIE</em> 7274, 72741S. DOI: 10.1117/12.814254 [Ref062 Fig. 11 — 7-day Gridplate stability < 0.20 nm].",
        "de Graaf, R., Weichselbaum, S., Droste, R., McLaren, M., Koek, B., & de Boeij, W. (2016). NXT:1980Di immersion scanner for 7nm production nodes. <em>Proc. SPIE</em> 9780, 978011. DOI: 10.1117/12.2220589 [Ref015 Fig. 10 — SMASH repeatability vs WQ].",
        "Menchtchikov, B., Socha, R., Zheng, C., et al. (2018). Reduction in overlay error from mark asymmetry using simulation, ORION, and alignment models. <em>Proc. SPIE</em> 10587, 105870C. DOI: 10.1117/12.2297493 [Ref252 Fig. 3 — multi-wavelength OCW].",
        "Pike, M., Felix, N., Menon, V., Ausschnitt, C., et al. (2012). High order wafer alignment in manufacturing. <em>Proc. SPIE</em> 8324, 832408. DOI: 10.1117/12.916483 [Ref123 — SUSD direction aliasing > 3.5 nm Gy20 mitigation]; Phase grating alignment dynamic scan extraction: <em>Applied Optics</em>, 64(30), 8921 (2025).",
        "Duclaux, B., Gatefait, M., Mermet, O., & Chapon, J.-D. (2020). Run to run and model variability of overlay high order process corrections for mean intrafield signatures. <em>Proc. SPIE</em> 11325, 113251K. DOI: 10.1117/12.2551062 [Ref100 Fig. 9 — dual-chuck C2 vs C1 offset].",
        "Ma, W.-K., Hwang, Y.-S., Kang, E.-K., et al. (2007). Hardware, materials, and parameters optimization for improvement of immersion overlay. <em>Proc. SPIE</em> 6518, 65182Z. DOI: 10.1117/12.712026 [Ref164 — UPW flow sensitivity of TIS].",
        "Streefkerk, B., Baselmans, J., Gehoel-van Ansem, W., Mulkens, J., Flagello, D., & Graeupner, P. (ASML & Carl Zeiss SMT, 2004). Extending optical lithography with immersion. <em>Proc. SPIE</em> 5377, 285–305 [Ref040 Fig. 7 — Zeiss offline wet PMI qualification].",
        "Carl Zeiss SMT AG/GmbH Immersion Metrology & Dry/Wet Adjustment Patents: US 7,408,652 B2, US 8,836,929 B2 & US 8,908,269 B2 (<em>Device and method for the optical measurement of an optical system by using an immersion fluid</em>); US 7,796,274 B2, US 8,488,127 B2 & US 8,823,948 B2 (<em>System for measuring the image quality of an optical imaging system</em>); US 7,310,187 B2 (<em>Projection objective and method for adjusting between immersion and dry configurations</em>).",
        "Staals, F., Andryzhyieuskaya, A., Bakker, H., et al. (2011). Advanced wavefront engineering for improved imaging and overlay applications on a 1.35 NA immersion scanner. <em>Proc. SPIE</em> 7973, 79731G. DOI: 10.1117/12.880759 [Ref024 Fig. 11]; Halle, S., Crouse, M., Jiang, A., et al. (2012). Lens heating challenges for NTD layers with freeform illumination. <em>Proc. SPIE</em> 8326, 832607 [RefN6 Table 4].",
        "Klinkhamer, F., Smeets, B., Thijssen, T., et al. (ASML & Carl Zeiss SMT, 2020). On-scanner high-spatial-frequency overlay control using a distortion manipulator [Ref253 Fig. 8]; Pollak, T., Emer, W., Thüring, B., et al. (Carl Zeiss SMT & ASML, 2020). A novel projection lens manipulator for high frequent overlay tuning. <em>Proc. SPIE</em> 11327, 113270T. DOI: 10.1117/12.2552063 [RefN4].",
        "Smeets, B., Aben, P., Klinkhamer, F., et al. (2022). Supporting future DRAM overlay and EPE roadmaps with the NXT:2100i. <em>Proc. SPIE</em> 12051, 120510K. DOI: 10.1117/12.2614031 [Ref254 §2.4 K20 boundary]; Kim, Y. H., et al. (2018). Reticle heating feed-forward control (RHC2) on NXT:1980Di [Ref016]; Ishiyama, S., et al. High-order aberration control during exposure [Ref160].",
        "OpticsPan/OV4 仓库主干基准文档：<em>NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v2.md</em> 与 <em>ENC_AA_WS-RS重复性与分级验收专项答复_v1.md</em>（https://github.com/OpticsPan/OV4/tree/main）。",
    ]
    ch7_html = '<ol class="ref-list">' + "".join(f"<li>{r}</li>" for r in refs) + "</ol>"
    chapters.append({
        "num": 7, "id": "ch-7",
        "title": "第 7 章　参考文献",
        "toc_title": "第 7 章　参考文献",
        "sections": [],
        "html": ch7_html,
    })

    return chapters


# =============================================================================
# TEMPLATE-MATCHED MINIMALIST SRS CSS (SimSun 9pt + Times New Roman 9pt)
# =============================================================================
CSS = r"""
@page {
  size: A4 portrait;
  margin: 18mm 14mm 17mm 14mm;
  @top-left {
    content: "OV4 ASML NXT:1965Ci 六大核心子系统套刻预算规格需求书 (v3)";
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
  margin: 13mm 14mm 13mm 14mm;
  @top-left { content: none; border: none; }
  @bottom-right { content: none; }
}

* { box-sizing: border-box; }

body {
  margin: 0;
  padding: 0;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  line-height: 1.48;
  color: #1A2430;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

/* ---- MINIMALIST ENGINEERING SRS COVER (Matches Attached Template v2.4) ---- */
.cover-page {
  page-break-after: always;
}

.top-rule {
  height: 2.2pt;
  background: #163A59;
  margin-bottom: 10pt;
}

.doc-code {
  text-align: center;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  font-weight: bold;
  color: #2B5275;
  letter-spacing: 0.4pt;
  margin-bottom: 5pt;
}

.doc-title {
  text-align: center;
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 17.5pt;
  font-weight: bold;
  color: #102A43;
  margin: 0 0 5pt 0;
  line-height: 1.25;
}

.doc-subtitle {
  text-align: center;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  color: #486581;
  margin: 0 0 9pt 0;
}

.cover-divider {
  height: 0.7pt;
  background: #CBD6E2;
  margin-bottom: 8pt;
}

table.meta-tbl {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 8pt;
  border: 0.7pt solid #C5D2DF;
}

table.meta-tbl td {
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 8.8pt;
  line-height: 1.38;
  padding: 3.6pt 6.5pt;
  border: 0.5pt solid #D4DFE8;
  vertical-align: top;
}

table.meta-tbl td.m-k {
  width: 15%;
  background: #F4F7FA;
  font-weight: bold;
  color: #102A43;
}

table.meta-tbl td.m-v {
  width: 35%;
  color: #243442;
}

.rev-box {
  background: #F7FAFC;
  border: 0.6pt solid #D4DFE8;
  border-left: 2.6pt solid #163A59;
  padding: 5.5pt 9pt;
  margin-bottom: 8pt;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 8.5pt;
  line-height: 1.42;
  text-align: justify;
  color: #243442;
}

.toc-box {
  border: 0.7pt solid #D4DFE8;
  padding: 7pt 11pt 6pt 11pt;
}

.toc-title {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 9.8pt;
  font-weight: bold;
  color: #102A43;
  border-bottom: 1pt solid #163A59;
  padding-bottom: 3pt;
  margin: 0 0 4pt 0;
}

table.toc-tbl {
  width: 100%;
  border-collapse: collapse;
}

table.toc-tbl td {
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 8.4pt;
  line-height: 1.30;
  padding: 1.15pt 0;
  border-bottom: 0.4pt dotted #E2EAF0;
}

tr.toc-ch td {
  font-weight: bold;
  color: #102A43;
  padding-top: 2.5pt;
}

tr.toc-sec td.toc-name {
  padding-left: 15pt;
  color: #364B5E;
}

td.toc-pg {
  width: 28pt;
  text-align: right;
  font-weight: bold;
  color: #163A59;
}

/* ---- CHAPTERS & HEADINGS (Template Style) ---- */
.chapter {
  page-break-before: always;
}
.chapter.first-ch {
  page-break-before: auto;
}

h1.ch-title {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 12.5pt;
  font-weight: bold;
  color: #102A43;
  border-bottom: 1.2pt solid #163A59;
  padding-bottom: 3.5pt;
  margin: 0 0 7pt 0;
  break-after: avoid;
  page-break-after: avoid;
}

h2 {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 9.8pt;
  font-weight: bold;
  color: #163A59;
  margin: 8pt 0 4.5pt 0;
  break-after: avoid;
  page-break-after: avoid;
}

/* ---- STRICT 4-COLUMN SPECIFICATION TABLES ---- */
table.spec-tbl {
  width: 100%;
  border-collapse: collapse;
  margin: 2pt 0 8pt 0;
  table-layout: fixed;
  border: 0.7pt solid #B8C8D6;
}

table.spec-tbl thead {
  display: table-header-group;
}

table.spec-tbl th {
  background: #163A59;
  color: #FFFFFF;
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 9pt;
  font-weight: bold;
  text-align: left;
  padding: 4.3pt 5pt;
  border: 0.5pt solid #2B5275;
  line-height: 1.3;
}

table.spec-tbl th:first-child,
table.spec-tbl th:nth-child(3) {
  text-align: center;
}

table.spec-tbl tr {
  break-inside: avoid;
  page-break-inside: avoid;
}

table.spec-tbl tbody tr:nth-child(even) {
  background: #F6F9FC;
}

table.spec-tbl td {
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  line-height: 1.32;
  padding: 2.25pt 4.3pt;
  border: 0.5pt solid #D4DFE8;
  vertical-align: top;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

td.c-idx {
  text-align: center;
  color: #102A43;
  font-weight: bold;
  white-space: nowrap;
}

td.c-name {
  color: #102A43;
  font-weight: bold;
}

td.c-spec {
  text-align: center;
  color: #102A43;
  font-weight: bold;
}

td.c-def {
  color: #243442;
}

/* ---- TECHNICAL NOTE BOXES ---- */
.note-box {
  background: #F7FAFC;
  border: 0.6pt solid #D4DFE8;
  border-left: 2.5pt solid #163A59;
  padding: 5.5pt 9pt;
  margin: 4pt 0 7pt 0;
}

.note-box p {
  margin: 0 0 3.8pt 0;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  line-height: 1.43;
  text-align: justify;
}

.note-box p:last-child {
  margin-bottom: 0;
}

.note-box p.indent {
  padding-left: 10pt;
}

.eq-line {
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  text-align: center;
  background: #FFFFFF;
  border: 0.5pt solid #DCE4EC;
  padding: 3.5pt 6pt;
  margin: 3.5pt 12pt 4.5pt 12pt;
  color: #102A43;
}

/* ---- VERIFIED ORIGINAL PAPER FIGURE PANELS ---- */
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

.fig-cell img,
.fig-single img {
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
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 8.2pt;
  line-height: 1.35;
  color: #364B5E;
  text-align: left;
  width: 100%;
}

/* ---- REFERENCES ---- */
ol.ref-list {
  margin: 3pt 0 0 0;
  padding-left: 19pt;
}

ol.ref-list li {
  margin-bottom: 1.5pt;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 8.3pt;
  line-height: 1.24;
  word-break: break-word;
}
"""


def compose_html(chapters: list, ch_pages: dict, sec_pages: dict) -> str:
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
      <div class="doc-code">OV4-SRS-NXT1965Ci-V3 · 工程规格需求书（SRS · 套刻专项审定版）</div>
      <h1 class="doc-title">ASML NXT:1965Ci 六大核心子系统套刻预算规格需求书</h1>
      <div class="doc-subtitle">WS / RS / ENC / AA / TIS+PARIS / Lens 分级验收指标（T1 / T2 / T3）与标准测试定义</div>
      <div class="cover-divider"></div>

      <table class="meta-tbl">
        <tr>
          <td class="m-k">整机目标定位</td>
          <td class="m-v">ASML TWINSCAN NXT:1965Ci（λ = 193.368 nm，NA = 1.35，β = 1/4）</td>
          <td class="m-k">顶层套刻红线</td>
          <td class="m-v">DCO ≤ 2.50 nm（闭环 2.26 nm）；双卡盘 SMO ≤ 2.50 nm（闭环 2.36 nm）；MMO ≤ 4.50 nm（闭环 4.29 nm）</td>
        </tr>
        <tr>
          <td class="m-k">曝光狭缝口径</td>
          <td class="m-v">26 × 5.5 mm 真实狭缝（v<sub>w</sub> = 0.70 m/s，τ<sub>slit</sub> = 7.857 ms）</td>
          <td class="m-k">基准仓库版本</td>
          <td class="m-v">OpticsPan/OV4 (main · NXT:1965Ci v3)</td>
        </tr>
        <tr>
          <td class="m-k">验收分级原则</td>
          <td class="m-v">T1：单件/单台离线；T2：装机解算/同步/调控；T3：跨台整机联调</td>
          <td class="m-k">编制日期与字体</td>
          <td class="m-v">2026-11-26（v3 · 正文宋体小五 / Times New Roman）</td>
        </tr>
      </table>

      <div class="rev-box">
        <strong>v3 专项审定与修订说明：</strong>① <strong>运动 iHOPC 文献核证与架构解耦（[注 4]）</strong>——剔除 v2 中“因浸没水膜将动态 K 项优先交由 RS”的无文献推理，改据 Ref154 Table 1、Ref019 §V.B、Ref225 及 US 8,237,914 B2 明确运动 iHOPC 由 WS/RS 双台相对轨迹协同执行，WRS-T2B 仅按 1× 最终像面残差判定；② <strong>T1 单台独立 iHOPC 验证升级</strong>——鉴于 WS/RS 离线干态平台无双台同步，新增 WS-T1B（表 1.2，55% 份额）与 RS-T1B（表 2.2，4× 口径，45% 份额）单台合成多项式轨迹验收，三项 RSS √(0.55²+0.45²+0.70²)=0.9975 闭环；③ <strong>Lens-iHOPC 双表拆分</strong>——拆分为表 6.3（T2-B 量程，9 项）与表 6.4（T2-C 精度与套刻动态，17 项）；④ <strong>Zeiss 干/湿测量专利核证（[注 12]）</strong>——增补 Streefkerk 等（SPIE 5377）wet PMI 及 Zeiss US 7,408,652 / 7,796,274 / 7,310,187 等专利族，诚实界定“Dry NA=0.93 + Wet NA=1.35”工厂 SOP 属未公开细节；⑤ <strong>全注释文献标注与引用核校</strong>——[注 1]–[注 14] 全部补齐编号引文 [1]–[26] 并修正既有文献作者/卷期元数据。
      </div>

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
        '<title>ASML NXT:1965Ci 六大核心子系统套刻预算规格需求书 (v3)</title>'
        f'<style>{CSS}</style></head><body>'
        + "".join(parts)
        + "</body></html>"
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


def render_pdf(markup: str, work: Path, tag: str) -> Path:
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
    res = subprocess.run(cmd, capture_output=True, timeout=120,
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if res.returncode or not pdf_path.is_file():
        raise RuntimeError(res.stderr.decode("utf-8", "replace"))
    return pdf_path


def locate_headings(doc: fitz.Document, chapters: list):
    ch_pages = {}
    sec_pages = {}
    toc = [[1, "封面与目录", 1]]

    sec_lookup = {}
    for ch in chapters:
        for st in ch["sections"]:
            code = st.split()[0]
            sec_lookup[code] = (ch["id"], st)

    found_ch = set()
    found_sec = set()

    for p in doc:
        if p.number == 0:
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
                m_ch = re.match(r"^(第\s*\d+\s*章)", txt)
                if m_ch and max_sz >= 11.2:
                    key = re.sub(r"\s+", " ", m_ch.group(1)).replace("第", "第 ").replace("章", " 章")
                    key = re.sub(r"\s+", " ", key).strip()
                    for ch in chapters:
                        if f"第 {ch['num']} 章" == key and ch["id"] not in found_ch:
                            ch_pages[ch["id"]] = pg_num
                            toc.append([1, ch["toc_title"], pg_num])
                            found_ch.add(ch["id"])
                            break
                m_sec = re.match(r"^(\d+\.\d+)\s+", txt)
                if m_sec and 9.3 <= max_sz < 11.2:
                    code = m_sec.group(1)
                    if code in sec_lookup and code not in found_sec:
                        cid, full_st = sec_lookup[code]
                        sec_pages[(cid, full_st)] = pg_num
                        toc.append([2, full_st, pg_num])
                        found_sec.add(code)

    missing_ch = [ch["id"] for ch in chapters if ch["id"] not in found_ch]
    if missing_ch:
        raise RuntimeError(f"Missing chapters in TOC locate: {missing_ch}; found={ch_pages}")
    return ch_pages, sec_pages, toc


def audit_fonts(doc: fitz.Document):
    body_fonts = {}
    for p in doc:
        if p.number == 0:
            continue
        blocks = p.get_text("dict", flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)["blocks"]
        for b in blocks:
            for line in b.get("lines", []):
                for sp in line.get("spans", []):
                    sz = round(sp["size"], 1)
                    if 8.8 <= sz <= 9.2 and sp["text"].strip():
                        fn = sp["font"]
                        body_fonts[fn] = body_fonts.get(fn, 0) + len(sp["text"].strip())
    core = {k: v for k, v in body_fonts.items() if "SimSun" in k or "TimesNewRoman" in k}
    print("Body/Table 9pt primary fonts:", core)
    assert any("SimSun" in k for k in core), "SimSun 9pt missing!"
    assert any("TimesNewRoman" in k for k in core), "Times New Roman 9pt missing!"


def main():
    for k, p in PAPER_IMGS.items():
        if not p.is_file():
            raise FileNotFoundError(f"Paper image missing: {k} -> {p}")

    chapters = build_chapters_part1()
    chapters = append_chapters_part2(chapters)

    with tempfile.TemporaryDirectory(prefix="build-", dir=WORK_ROOT, ignore_cleanup_errors=True) as td:
        work = Path(td)
        pdf1 = render_pdf(compose_html(chapters, {}, {}), work, "p1")
        with fitz.open(pdf1) as d1:
            ch_p1, sec_p1, _ = locate_headings(d1, chapters)

        pdf2 = render_pdf(compose_html(chapters, ch_p1, sec_p1), work, "p2")
        with fitz.open(pdf2) as d2:
            ch_p2, sec_p2, toc = locate_headings(d2, chapters)
            assert ch_p2 == ch_p1, f"Chapter page shift: {ch_p1} -> {ch_p2}"
            assert ch_p2["ch-1"] == 2, f"Cover+TOC spilled beyond page 1! ch-1 starts on p.{ch_p2['ch-1']}"
            audit_fonts(d2)
            d2.set_toc(toc)
            d2.set_metadata({
                "title": "ASML NXT:1965Ci 六大核心子系统套刻预算规格需求书 (v3)",
                "subject": "NXT:1965Ci SMO<=2.50nm MMO<=4.50nm; WS/WRS, RS, ENC, AA, TIS+PARIS, Lens T1/T2/T3",
                "author": "OpticsPan / OV4",
            })
            OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
            d2.save(OUT_PDF, garbage=3, deflate=True)
            total_pages = len(d2)

            prev_dir = WORK_ROOT / "preview_pages"
            if prev_dir.exists():
                shutil.rmtree(prev_dir)
            prev_dir.mkdir(parents=True, exist_ok=True)
            for p in d2:
                pix = p.get_pixmap(dpi=150)
                pix.save(prev_dir / f"page_{p.number + 1:02d}.png")

    print(f"\nPDF v3 BUILT SUCCESSFULLY: {OUT_PDF}")
    print(f"Total pages: {total_pages} | Bookmarks: {len(toc)}")
    for ch in chapters:
        print(f"  p.{ch_p2[ch['id']]:2d}  {ch['toc_title']}")


if __name__ == "__main__":
    main()
