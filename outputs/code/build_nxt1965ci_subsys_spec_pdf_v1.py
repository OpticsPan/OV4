"""Generate publication-grade PDF Specification Document:
ASML TWINSCAN NXT:1965Ci Six Core Subsystems Overlay Budget & Tiered Acceptance Spec (v1).

Typography & Layout Requirements:
  - Chinese body & table text: SimSun (宋体) 9 pt (小五号)
  - English / digits / units: Times New Roman 9 pt
  - Strictly 4-column acceptance tables: 序号 | 指标项 | 验收规格 | 标准测试定义与工装条件
  - Strictly one unmerged metric per row (no X/Y, no Z7/Z8, no Range/Precision merging)
  - Executive visual layout mirroring OV4 technical review PDF style (2-pass exact TOC + bookmarks)

Run from repository root in PowerShell:
    $env:PYTHONPATH = "D:/Codex/cache/pdf-python"
    python -B outputs/code/build_nxt1965ci_subsys_spec_pdf_v1.py
"""
import html
import math
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pymupdf as fitz

REPO = Path(__file__).resolve().parents[2]
OUT_PDF = REPO / "outputs/reports/NXT1965Ci套刻预算分配_六大核心子系统分层验收规格需求书_v1.pdf"
WORK_ROOT = REPO / "work/subsys-spec-pdf-v1"
WORK_ROOT.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(WORK_ROOT / "matplotlib"))


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def fmt_inline(text: str) -> str:
    """Allow safe lightweight markup: **bold**, `[注 X-Y]` badge, `^2/^3` superscripts."""
    s = esc(text)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(\[注\s*\d+-\d+\])", r'<span class="note-tag">\1</span>', s)
    s = re.sub(r"(\[详\s*[\d\.]+?\s*节\])", r'<span class="note-tag">\1</span>', s)
    return s


# =============================================================================
# 1. PUBLICATION-GRADE MATPLOTLIB DIAGRAMS (300 DPI, SimSun + Times New Roman)
# =============================================================================
def setup_mpl():
    plt.rcParams.update({
        "font.family": ["Times New Roman", "SimSun"],
        "font.sans-serif": ["SimSun", "Microsoft YaHei"],
        "font.serif": ["Times New Roman", "SimSun"],
        "axes.unicode_minus": False,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "axes.edgecolor": "#B8C7D4",
        "axes.linewidth": 0.8,
        "xtick.color": "#243442",
        "ytick.color": "#243442",
        "text.color": "#1A2B3C",
    })


def generate_figures(fig_dir: Path) -> dict:
    setup_mpl()
    figs = {}

    # -------------------------------------------------------------------------
    # Fig 0-1: NXT:1965Ci Budget Closure & Six-Domain Allocation
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.75), gridspec_kw={"width_ratios": [1.05, 1.25]})
    fig.patch.set_facecolor("white")

    cats = ["同卡盘 DCO", "双卡盘 SMO", "混机 MMO"]
    means = np.array([0.300, 0.350, 0.500])
    rands = np.array([1.957, 2.014, 3.791])
    limits = np.array([2.50, 2.50, 4.50])
    x = np.arange(len(cats))
    w = 0.46
    ax1.bar(x, rands, w, color="#1D5C7A", label="随机项 3σ (RSS)")
    ax1.bar(x, means, w, bottom=rands, color="#E08B33", label="固定偏置 |Mean| (线性)")
    for i in range(len(cats)):
        tot = means[i] + rands[i]
        ax1.hlines(limits[i], i - 0.33, i + 0.33, colors="#B83227", linestyles="--", linewidth=1.35)
        y_txt = max(tot, limits[i]) + 0.14
        ax1.text(i, y_txt, f"闭环 {tot:.2f} nm\n(红线 ≤ {limits[i]:.2f})", ha="center", va="bottom",
                 fontsize=7.2, fontweight="bold", color="#10374C", linespacing=1.22)
    ax1.set_xticks(x)
    ax1.set_xticklabels(cats, fontsize=8.2)
    ax1.set_ylabel("全片套刻误差 (nm, 1× 两层)", fontsize=8.2)
    ax1.set_ylim(0, 5.85)
    ax1.set_title("(a) NXT:1965Ci 顶层套刻闭环 vs 红线", fontsize=8.8, fontweight="bold", pad=6)
    ax1.grid(axis="y", linestyle=":", alpha=0.55)
    ax1.legend(loc="upper left", fontsize=7.0, frameon=True, facecolor="#F7FAFC", edgecolor="#DCE4EC")

    doms = [
        "S2 对准 (AA+TIS/PARIS)",
        "S1 运动台 (WS/RS/WRS)",
        "S5 掩模热与夹持",
        "S4 晶圆热与浸没",
        "S3 光学柱 (Lens)",
        "S6 晶圆夹持与接口",
    ]
    shares = [25.38, 20.24, 17.61, 16.58, 11.99, 8.21]
    vals_2l = [0.970, 0.867, 0.809, 0.784, 0.667, 0.552]
    colors = ["#C98A1B", "#1E5C7A", "#2C7BB6", "#16949B", "#4F7D28", "#8A7652"]
    y = np.arange(len(doms))[::-1]
    ax2.barh(y, shares, height=0.58, color=colors, alpha=0.92)
    for yi, sh, v in zip(y, shares, vals_2l):
        ax2.text(sh + 0.5, yi, f"{sh:.1f}%  ({v:.3f} nm)", va="center", ha="left", fontsize=7.4, color="#1A2B3C")
    ax2.set_yticks(y)
    ax2.set_yticklabels(doms, fontsize=7.8)
    ax2.set_xlabel("Ref009 Fig. 3 六域方差份额 (%)", fontsize=8.2)
    ax2.set_xlim(0, 38)
    ax2.set_title("(b) 核心六域方差份额与两层 1× 预算 (Core-6 RSS = 1.926 nm)", fontsize=8.6, fontweight="bold", pad=6)
    ax2.grid(axis="x", linestyle=":", alpha=0.55)

    plt.tight_layout(pad=0.9)
    p0 = fig_dir / "fig0_1_budget.png"
    fig.savefig(p0, bbox_inches="tight")
    plt.close(fig)
    figs["fig0_1"] = p0

    # -------------------------------------------------------------------------
    # Fig 1-1: Unidirectional vs Bidirectional + NXT:1965Ci 1x Stage Split
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.85), gridspec_kw={"width_ratios": [1.08, 1.15]})
    fig.patch.set_facecolor("white")

    xx = np.linspace(-0.42, 0.42, 400)
    mu_up, mu_dn, sig = 0.045, -0.045, 0.29 / 3.0
    g_up = np.exp(-0.5 * ((xx - mu_up) / sig) ** 2) / (sig * np.sqrt(2 * np.pi))
    g_dn = np.exp(-0.5 * ((xx - mu_dn) / sig) ** 2) / (sig * np.sqrt(2 * np.pi))
    g_up /= g_up.max()
    g_dn /= g_dn.max()
    ax1.plot(xx, g_up, color="#163A59", lw=1.6, label="正扫 Scan-Up (+Y)")
    ax1.plot(xx, g_dn, color="#D97706", lw=1.6, ls="--", label="反扫 Scan-Down (−Y)")
    ax1.fill_between(xx, 0, g_up, color="#163A59", alpha=0.10)
    ax1.fill_between(xx, 0, g_dn, color="#D97706", alpha=0.10)
    ax1.vlines([mu_dn, mu_up], 0, 1.07, colors=["#D97706", "#163A59"], linestyles=":", lw=1.1)
    ax1.annotate("", xy=(mu_up, 1.04), xytext=(mu_dn, 1.04),
                 arrowprops=dict(arrowstyle="<->", color="#B83227", lw=1.2))
    ax1.text(0, 1.10, "残余反向差 B_UD = 0.09 nm (占 24%)", ha="center", va="bottom",
             fontsize=7.2, fontweight="bold", color="#B83227")
    ax1.annotate("", xy=(mu_up + 0.29 / 2, 0.50), xytext=(mu_up - 0.29 / 2, 0.50),
                 arrowprops=dict(arrowstyle="<->", color="#0D5E6D", lw=1.2))
    ax1.text(0.245, 0.58, "单程 R_uni\n(3σ = 0.29)", ha="center", va="bottom",
             fontsize=7.0, color="#0D5E6D", bbox=dict(boxstyle="round,pad=0.2", fc="#EBF8FA", ec="#0D5E6D", lw=0.6))
    ax1.annotate("", xy=(0.335, 0.14), xytext=(-0.335, 0.14),
                 arrowprops=dict(arrowstyle="<->", color="#163A59", lw=1.2))
    ax1.text(0, 0.20, "往返包络 R_bi = R_uni + B_UD = 0.38 nm", ha="center", va="bottom",
             fontsize=7.0, fontweight="bold", color="#163A59",
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#163A59", lw=0.6))
    ax1.set_xlim(-0.40, 0.40)
    ax1.set_ylim(0, 1.32)
    ax1.set_xlabel("匀速段动态位置误差 e (nm) [WS-X 示例]", fontsize=7.9, labelpad=4)
    ax1.set_ylabel("归一化概率密度", fontsize=8.0)
    ax1.set_title("(a) 正反扫误差分布与单程/反向差拆分定义", fontsize=8.4, fontweight="bold", pad=6)
    ax1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=2, fontsize=7.2, frameon=False)
    ax1.grid(linestyle=":", alpha=0.45)

    lbls = ["WS-X (1×)", "WS-Y (1×)", "RS-X 折算 (1×)", "RS-Y 折算 (1×)"]
    uni_v = np.array([0.29, 0.29, 0.21, 0.22])
    bud_v = np.array([0.09, 0.10, 0.07, 0.08])
    yy = np.arange(len(lbls))[::-1]
    ax2.barh(yy, uni_v, height=0.52, color="#163A59", label="单程动态 R_uni (74%–76%)")
    ax2.barh(yy, bud_v, left=uni_v, height=0.52, color="#D97706", label="残余反向差 B_UD (24%–26%)")
    for yi, u, b in zip(yy, uni_v, bud_v):
        ax2.text(u / 2, yi, f"{u:.2f}", ha="center", va="center", color="white", fontsize=7.3, fontweight="bold")
        ax2.text(u + b / 2, yi, f"{b:.2f}", ha="center", va="center", color="white", fontsize=7.1, fontweight="bold")
        ax2.text(u + b + 0.012, yi, f"总 {u+b:.2f} nm", ha="left", va="center", color="#1A2B3C", fontsize=7.4, fontweight="bold")
    ax2.set_yticks(yy)
    ax2.set_yticklabels(lbls, fontsize=7.8)
    ax2.set_xlim(0, 0.51)
    ax2.set_xlabel("晶圆侧 1× 等效验收指标 (nm)", fontsize=7.9, labelpad=4)
    ax2.set_title("(b) NXT:1965Ci WS / RS 平移轴往返拆分配比", fontsize=8.4, fontweight="bold", pad=6)
    ax2.legend(loc="upper center", bbox_to_anchor=(0.48, -0.24), ncol=2, fontsize=7.0, frameon=False)
    ax2.grid(axis="x", linestyle=":", alpha=0.45)

    fig.subplots_adjust(left=0.08, right=0.98, top=0.88, bottom=0.27, wspace=0.33)
    p1 = fig_dir / "fig1_1_uni_bi.png"
    fig.savefig(p1, bbox_inches="tight")
    plt.close(fig)
    figs["fig1_1"] = p1

    # -------------------------------------------------------------------------
    # Fig 1-2: Evers (2019) MA vs MSD Trade-off + Master/Slave Sync Logic
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.45))
    fig.patch.set_facecolor("white")

    modes = ["无耦合\n(No Coupling)", "标称双向耦合\n(Nominal)", "鲁棒双-Youla\n(Robust)"]
    ma_pm = [565, 108, 200]
    msd_pm = [2879, 3329, 3304]
    c_ma = ["#4C6984", "#0F7A7A", "#1C5A85"]
    c_msd = ["#4C6984", "#D97706", "#C2591A"]
    x3 = np.arange(3)

    b1 = ax1.bar(x3, ma_pm, width=0.52, color=c_ma)
    ax1.text(0, 565 + 18, "565 pm", ha="center", va="bottom", fontsize=7.5, fontweight="bold")
    ax1.text(1, 108 + 18, "108 pm\n(−80.9%)", ha="center", va="bottom", fontsize=7.3, fontweight="bold", color="#0F7A7A")
    ax1.text(2, 200 + 18, "200 pm\n(−64.6%)", ha="center", va="bottom", fontsize=7.3, fontweight="bold", color="#1C5A85")
    ax1.set_xticks(x3)
    ax1.set_xticklabels(modes, fontsize=7.6)
    ax1.set_ylabel("同步 MA 3σ (pm)", fontsize=8.0)
    ax1.set_ylim(0, 690)
    ax1.set_title("(a) 低频套刻指标 Sync MA 大幅下降", fontsize=8.4, fontweight="bold", pad=6)
    ax1.grid(axis="y", linestyle=":", alpha=0.5)

    b2 = ax2.bar(x3, msd_pm, width=0.52, color=c_msd)
    ax2.text(0, 2879 + 90, "2879 pm", ha="center", va="bottom", fontsize=7.5, fontweight="bold")
    ax2.text(1, 3329 + 90, "3329 pm\n(+15.6%)", ha="center", va="bottom", fontsize=7.3, fontweight="bold", color="#B45309")
    ax2.text(2, 3304 + 90, "3304 pm\n(+14.8%)", ha="center", va="bottom", fontsize=7.3, fontweight="bold", color="#9A3412")
    ax2.set_xticks(x3)
    ax2.set_xticklabels(modes, fontsize=7.6)
    ax2.set_ylabel("同步 MSD 3σ (pm)", fontsize=8.0)
    ax2.set_ylim(0, 4150)
    ax2.set_title("(b) 高频抖动指标 Sync MSD 反向抬升", fontsize=8.4, fontweight="bold", pad=6)
    ax2.grid(axis="y", linestyle=":", alpha=0.5)

    plt.tight_layout(pad=0.9)
    p2 = fig_dir / "fig1_2_sync_tradeoff.png"
    fig.savefig(p2, bbox_inches="tight")
    plt.close(fig)
    figs["fig1_2"] = p2

    # -------------------------------------------------------------------------
    # Fig 3-1 (Full-width): ENC T1->T2->WRS Architecture Schematic
    # -------------------------------------------------------------------------
    fig, ax_diag = plt.subplots(figsize=(7.0, 2.25))
    fig.patch.set_facecolor("white")
    ax_diag.set_xlim(0, 12.0)
    ax_diag.set_ylim(0, 5.2)
    ax_diag.axis("off")

    boxes = [
        (0.15, 2.45, 3.55, 2.55, "#EBF5FB", "#1C6E8C", "T1：纯 ENC 测量本体（离线无伺服）",
         "Gridplate + 4 路读数头\n1 kHz 宽带 ≤ 0.22 nm / 曝光窗 ≤ 0.13 nm\n零膨胀刚性参考块锁死测试\n责任归属：ENC 量测团队（不计入 L0）"),
        (4.22, 2.45, 3.55, 2.55, "#EEF7EE", "#2E7D32", "T2：装机计量链（含切头与热稳）",
         "6-DOF 运动学解算 + EMSI 切头 ≤ 0.15 nm\nGridplate 7 天热稳定 ≤ 0.20 nm\n外接独立激光干涉仪核对阿贝臂真值\n责任归属：ENC + 整机集成联合"),
        (8.30, 2.45, 3.55, 2.55, "#FFF7EB", "#C06C16", "WS / WRS 运动闭环（计入 SMO）",
         "WS 往返 0.38/0.39 nm · RS 1.12/1.18 (4×)\nWRS Sync MA 0.47/0.49 nm (1×)\nT1/T2 测量误差已内嵌于闭环中\n整机 L0 总账严禁重复计数！"),
    ]
    for bx, by, bw, bh, fc, ec, title, body in boxes:
        rect = mpatches.FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0.10,rounding_size=0.18",
                                       facecolor=fc, edgecolor=ec, linewidth=1.15)
        ax_diag.add_patch(rect)
        ax_diag.text(bx + bw / 2, by + bh - 0.22, title, ha="center", va="top",
                     fontsize=8.0, fontweight="bold", color=ec)
        ax_diag.text(bx + bw / 2, by + bh - 0.68, body, ha="center", va="top",
                     fontsize=7.2, color="#1F2D3D", linespacing=1.42)

    for x0, x1 in [(3.80, 4.12), (7.87, 8.20)]:
        ax_diag.annotate("", xy=(x1, 3.72), xytext=(x0, 3.72),
                         arrowprops=dict(arrowstyle="->", color="#163A59", lw=1.6))

    rect_b = mpatches.FancyBboxPatch((0.15, 0.18), 11.70, 1.85, boxstyle="round,pad=0.10,rounding_size=0.16",
                                     facecolor="#F7FAFC", edgecolor="#9FB3C8", linewidth=0.9, linestyle="--")
    ax_diag.add_patch(rect_b)
    ax_diag.text(6.0, 1.84, "闭环解耦与防“自己测自己”盲区关系（外部独立标尺的必要性）",
                 ha="center", va="top", fontsize=8.0, fontweight="bold", color="#10374C")
    ax_diag.text(6.0, 1.36,
                 "实际定位误差 e_true = [机内 ENC 闭环误差（自读可见）] − [ENC 自身读数与标定误差（自读不可见）]\n"
                 "若读数头热漂或阿贝臂倾角失准，机内自读看似为 0 而硅片真实位置已偏离；因此 T1 离线验尺子，T2 须用外部干涉仪验真值。",
                 ha="center", va="top", fontsize=7.3, color="#243442", linespacing=1.48)

    plt.tight_layout(pad=0.3)
    p3a = fig_dir / "fig3_1_enc_arch.png"
    fig.savefig(p3a, bbox_inches="tight")
    plt.close(fig)
    figs["fig3_1"] = p3a

    # -------------------------------------------------------------------------
    # Fig 3-2 (Full-width): 5.5 mm Real Slit Filter Response (ZERO 8.0 mm!)
    # -------------------------------------------------------------------------
    fig, ax_f = plt.subplots(figsize=(7.0, 2.35))
    fig.patch.set_facecolor("white")

    freqs = np.linspace(0.1, 450, 900)
    tau = 5.5 / 700.0  # 7.857 ms
    enbw = 1.0 / (2.0 * tau)  # 63.64 Hz
    f1 = 1.0 / tau  # 127.27 Hz
    resp = np.abs(np.sinc(freqs * tau))

    ax_f.fill_between(freqs, 0, resp, where=(freqs <= enbw), color="#1D5C7A", alpha=0.16,
                      label="MA 主通带 (≤ 63.64 Hz → 直接转化为套刻 Overlay)")
    ax_f.fill_between(freqs, 0, resp, where=(freqs > enbw), color="#D97706", alpha=0.13,
                      label="MSD 高频区 (> 63.64 Hz → 对比度模糊与伺服激励)")
    ax_f.plot(freqs, resp, color="#10374C", lw=1.8, label="5.5 mm 真实狭缝 |sinc(f·τ)| (τ = 7.857 ms, f1 = 127.3 Hz)")
    ax_f.axvline(enbw, color="#0D7A6F", ls=":", lw=1.4)
    ax_f.plot([enbw], [abs(np.sinc(enbw * tau))], "o", color="#0D7A6F", ms=5.0)
    ax_f.annotate("ENBW = 63.64 Hz\nENC-WS 曝光窗 ≤ 0.13 nm", xy=(enbw, 0.637), xytext=(115, 0.78),
                  fontsize=7.6, fontweight="bold", color="#0D5E6D",
                  bbox=dict(boxstyle="round,pad=0.26", fc="#EBF8FA", ec="#0D7A6F", lw=0.8),
                  arrowprops=dict(arrowstyle="->", color="#0D7A6F", lw=1.1))
    ax_f.annotate("原始宽带 (1 kHz) ≤ 0.22 nm\n须随原始时序交付 0.1 Hz–2 kHz PSD/CPS", xy=(295, 0.13), xytext=(235, 0.39),
                  fontsize=7.5, color="#9A3412",
                  bbox=dict(boxstyle="round,pad=0.26", fc="#FFF7ED", ec="#C2591A", lw=0.8),
                  arrowprops=dict(arrowstyle="->", color="#C2591A", lw=1.1))
    ax_f.annotate("第一零点 f1 = 127.3 Hz", xy=(f1, 0.015), xytext=(142, 0.31),
                  fontsize=7.3, color="#334E68",
                  arrowprops=dict(arrowstyle="->", color="#486581", lw=0.9))
    ax_f.set_xlim(0, 450)
    ax_f.set_ylim(0, 1.08)
    ax_f.set_xlabel("频率 f (Hz)", fontsize=8.2)
    ax_f.set_ylabel("滑窗平均幅频响应 |MA(f)|", fontsize=8.2)
    ax_f.set_title("5.5 mm 真实狭缝（0.70 m/s，τ = 7.857 ms）曝光窗滤波特性与 ENC 双频段验收分工", fontsize=8.6, fontweight="bold", pad=6)
    ax_f.legend(loc="upper right", fontsize=7.0, frameon=True, facecolor="white", edgecolor="#DCE4EC")
    ax_f.grid(linestyle=":", alpha=0.45)

    plt.tight_layout(pad=0.5)
    p3b = fig_dir / "fig3_2_slit_filter.png"
    fig.savefig(p3b, bbox_inches="tight")
    plt.close(fig)
    figs["fig3_2"] = p3b

    # -------------------------------------------------------------------------
    # Fig 6-1: Lens Odd Zernike 15 Pairs & Lens-iHOPC 8 Parameters
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.7), gridspec_kw={"width_ratios": [1.28, 1.0]})
    fig.patch.set_facecolor("white")

    z_pairs = ["Z7/8", "Z10/11", "Z14/15", "Z19/20", "Z23/24", "Z26/27", "Z30/31", "Z34/35",
               "Z39/40", "Z43/44", "Z47/48", "Z50/51", "Z54/55", "Z58/59", "Z62/63"]
    z_fringe = [0.21, 0.19, 0.21, 0.24, 0.28, 0.19, 0.26, 0.36, 0.26, 0.36, 0.42, 0.28, 0.30, 0.42, 0.48]
    z_ovl = [0.199, 0.173, 0.147, 0.132, 0.077, 0.160, 0.120, 0.056, 0.095, 0.050, 0.041, 0.090, 0.094, 0.038, 0.042]
    xz = np.arange(len(z_pairs))
    ax1.bar(xz - 0.18, z_fringe, width=0.36, color="#1D5C7A", alpha=0.88, label="Fringe 调节精度限值 (nm)")
    ax1.bar(xz + 0.18, z_ovl, width=0.36, color="#D97706", alpha=0.90, label="跨照明单轴套刻贡献 (nm)")
    ax1.set_xticks(xz)
    ax1.set_xticklabels(z_pairs, fontsize=6.4, rotation=42, ha="right")
    ax1.set_ylabel("幅值 / 套刻贡献 (nm, 193 nm)", fontsize=7.8)
    ax1.set_ylim(0, 0.56)
    ax1.set_title("(a) Odd Zernike 30 项精度与跨照明套刻 (总 RMS ≤ 0.40 nm)", fontsize=8.2, fontweight="bold", pad=6)
    ax1.legend(loc="upper left", fontsize=6.8, frameon=True, facecolor="#F7FAFC", edgecolor="#DCE4EC")
    ax1.grid(axis="y", linestyle=":", alpha=0.45)

    ks = ["K3\n(x)", "K7\n(x²)", "K12\n(y·x²)", "K13\n(x³)", "K9\n(xy)", "K15\n(x²y)", "K17\n(xy²)", "K18\n(yx²)"]
    k_corner = [0.156, 0.155, 0.155, 0.154, 0.154, 0.151, 0.149, 0.151]
    k_cols = ["#163A59", "#163A59", "#0D7A6F", "#163A59", "#2C7BB6", "#2C7BB6", "#2C7BB6", "#0D7A6F"]
    xk = np.arange(len(ks))
    ax2.bar(xk, k_corner, width=0.56, color=k_cols, alpha=0.92)
    for xi, v in zip(xk, k_corner):
        ax2.text(xi, v + 0.004, f"{v:.3f}", ha="center", va="bottom", fontsize=6.7, color="#1A2B3C")
    ax2.axhline(0.155, color="#B83227", ls="--", lw=0.9, alpha=0.7)
    ax2.set_xticks(xk)
    ax2.set_xticklabels(ks, fontsize=7.0)
    ax2.set_ylim(0, 0.21)
    ax2.set_ylabel("单层最大场角套刻残差 (nm)", fontsize=7.8)
    ax2.set_title("(b) Lens-iHOPC 8 项场角残差 (蓝=X 6项 / 绿=Y 2项)", fontsize=8.2, fontweight="bold", pad=6)
    ax2.text(3.5, 0.184, "RSS: X = 0.375 nm / Y = 0.216 nm (单层)\nK20 不支持主动调，归入静态指纹 ≤ 0.18 nm/cm³",
             ha="center", va="center", fontsize=6.7, color="#10374C",
             bbox=dict(boxstyle="round,pad=0.22", fc="#F4F9FD", ec="#1C6E8C", lw=0.6))
    ax2.grid(axis="y", linestyle=":", alpha=0.45)

    plt.tight_layout(pad=0.9)
    p6 = fig_dir / "fig6_1_lens.png"
    fig.savefig(p6, bbox_inches="tight")
    plt.close(fig)
    figs["fig6_1"] = p6

    return figs


# =============================================================================
# 2. SPECIFICATION DATA (ZERO MERGING! EVERY ITEM STRICTLY ONE ROW, 4 COLUMNS)
# =============================================================================
def build_chapters_data(figs: dict) -> list:
    """Return structured chapter dicts for Chapters 0 through 7."""
    chapters = []

    # -------------------------------------------------------------------------
    # CHAPTER 0: Budget Allocation Baseline & Tiered Rules
    # -------------------------------------------------------------------------
    ch0_html = f"""
    <p>本规格需求书以 <strong>ASML TWINSCAN NXT:1965Ci</strong>（193.368 nm，NA 1.35，4:1 缩小，真实曝光狭缝 26 × 5.5 mm，视场 26 × 33 mm，扫描基准速度 0.70 m/s）为唯一整机目标，依据一手文献 <em>Ref009 Fig. 3</em> 的六大物理域方差占比，将整机套刻红线自顶向下分配至 <strong>WS（含 WRS）、RS、ENC、AA、TIS+PARIS、Lens</strong> 六大核心子系统，形成逐项可测、逐级放行的工程验收规格。</p>

    <div class="callout-info">
      <strong>公开规格与工程预算边界声明：</strong>ASML 官方产品页公开了 NXT:1965Ci 整机单机单卡盘套刻（DCO ≤ 2.50 nm，全片覆盖）与混机匹配套刻（MMO ≤ 4.50 nm，相对校准参考晶圆）。原厂未公开的双卡盘套刻（本项目按 SMO ≤ 2.50 nm 从严控制）、独立焦面均匀性（FU ≤ 14.0 nm，不并入套刻 RSS）以及各子系统内部门限，均属于基于一手实测文献推导的 <strong>OV4 工程预算分配</strong>，验收签字前须结合实机交付规程冻结测点布局、配方参数与统计口径。
    </div>

    <h2>0.1 整机套刻与焦面总预算闭环（1× 晶圆面两层口径）</h2>
    <table class="spec-tbl">
      <thead>
        <tr>
          <th style="width:8%">序号</th>
          <th style="width:26%">整机/功能域预算项</th>
          <th style="width:20%">预算闭环值（两层 1×）</th>
          <th style="width:46%">归口核心子系统与红线核对说明</th>
        </tr>
      </thead>
      <tbody>
        <tr><td class="c-idx">0.1</td><td class="c-name">L1-S1 运动台定位与同步域</td><td class="c-spec">X 0.744 / Y 0.867 nm</td><td>归口 <strong>第 1 章 WS/WRS</strong> 与 <strong>第 2 章 RS</strong>（内嵌第 3 章 ENC）；占 Ref009 方差 20.24%</td></tr>
        <tr><td class="c-idx">0.2</td><td class="c-name">L1-S2 晶圆与掩模对准域</td><td class="c-spec">X 0.970 / Y 0.970 nm</td><td>归口 <strong>第 4 章 AA</strong>（0.707 nm）与 <strong>第 5 章 TIS+PARIS</strong>（0.665 nm）；占 Ref009 方差 25.38%</td></tr>
        <tr><td class="c-idx">0.3</td><td class="c-name">L1-S3 光学柱与动态像差域</td><td class="c-spec">X 0.667 / Y 0.557 nm</td><td>归口 <strong>第 6 章 Lens</strong>（iHOPC 8 项 + Odd Zernike 30 项 + 热声残余）；占 Ref009 方差 11.99%</td></tr>
        <tr><td class="c-idx">0.4</td><td class="c-name">L1-S4/S5/S6 热、浸没与夹持域</td><td class="c-spec">0.784 / 0.809 / 0.552 nm</td><td>晶圆热与浸没（16.58%）、掩模热与夹持（17.61%）、晶圆夹持与接口（8.21%）；合六域 RSS 1.926 nm</td></tr>
        <tr><td class="c-idx">0.5</td><td class="c-name">L0-DCO 单机单卡盘套刻</td><td class="c-spec">2.257 nm ≤ 2.50 nm</td><td>固定偏置 0.300 nm + RSS（Core-6 1.926 + 量测底噪 0.340）；裕度 9.7%，对齐原厂公开 DCO 红线</td></tr>
        <tr><td class="c-idx">0.6</td><td class="c-name">L0-SMO 单机双卡盘套刻</td><td class="c-spec">2.364 nm ≤ 2.50 nm</td><td>固定偏置 0.350 nm + RSS（Core-6 + ΔC2C 0.479 + 量测 0.340）；裕度 5.4%，双卡盘混用仍不破 2.50 nm</td></tr>
        <tr><td class="c-idx">0.7</td><td class="c-name">L0-MMO 混机匹配套刻</td><td class="c-spec">4.291 nm ≤ 4.50 nm</td><td>固定偏置 0.500 nm + RSS（SMO 随机 + 跨机网格 2.00 + 光学 1.887 + 卡盘热对准 1.658）；裕度 4.6%</td></tr>
        <tr><td class="c-idx">0.8</td><td class="c-name">L0-FU 全片焦面均匀性（独立）</td><td class="c-spec">11.48 nm ≤ 14.0 nm</td><td>Sync Z（5.34）+ 倾角（1.71）+ 吸盘平坦（6.50）+ TIS（2.80）+ 调平/物镜/框架 RSS；不并入套刻</td></tr>
      </tbody>
    </table>

    <div class="fig-box">
      <img src="{figs['fig0_1'].as_uri()}" alt="图0-1 整机套刻总预算闭环与六域分配"/>
      <div class="fig-cap">图 0-1：NXT:1965Ci 顶层套刻闭环（DCO / SMO / MMO）及 Ref009 Fig. 3 六大物理域方差份额归口示意</div>
    </div>

    <h2>0.2 子系统分层验收（T1 / T2）与防重复计数总则</h2>
    <table class="spec-tbl">
      <thead>
        <tr>
          <th style="width:10%">验收层级</th>
          <th style="width:24%">层级名称与适用子系统</th>
          <th style="width:22%">工装边界与核心考核目标</th>
          <th style="width:44%">责任划分与与整机曝光（T3）的衔接原则</th>
        </tr>
      </thead>
      <tbody>
        <tr><td class="c-idx"><strong>T1</strong></td><td class="c-name">单件 / 单台本体独立验收<br>（全 6 大子系统均设）</td><td class="c-spec">离线台架或关闭跨台耦合（Sync Off）；考核硬件本体与单台闭环底噪</td><td>ENC 验纯传感器离线本底；AA 验参考扫单标信噪与色差；WS/RS 验各自独立 6-DOF；TIS+PARIS 在 E 侧曝光态单设 T1 闭环；Lens 验出厂干涉仪波前与操纵器单件能力。</td></tr>
        <tr><td class="c-idx"><strong>T2</strong></td><td class="c-name">装机集成 / 跨台联试验收<br>（WS/WRS、ENC、AA、Lens）</td><td class="c-spec">装机闭环、外部独立标尺核验或开启跨子系统联调（不打胶或模拟量测）</td><td>WS/WRS 验双台同步 MA/MSD 与 11 项 iHOPC 运动补偿；ENC 验过缝切头与 7 天热稳；AA 验动态扫标与全片 HOWA 网格；Lens 验 PARIS 波前闭环、8 维耦合与跨照明套刻。</td></tr>
        <tr><td class="c-idx"><strong>防重计</strong></td><td class="c-name">层级嵌套与外部标尺铁律</td><td class="c-spec">T1 内嵌于 T2；T1/T2 不可替代 T3 实曝</td><td>ENC 底噪已内嵌于 WS/RS/WRS 闭环，整机 L0 绝不重复计账；凡机内传感器闭环自读项目，须配外接独立激光干涉仪或参考片复核，消除“自己测自己”盲区。</td></tr>
      </tbody>
    </table>
    """
    chapters.append({
        "num": 0, "id": "ch-0",
        "title": "第 0 章　整机套刻预算分配基线与分层验收总则",
        "toc_title": "第 0 章　整机套刻预算分配基线与分层验收总则",
        "sections": [
            ("0.1 整机套刻与焦面总预算闭环（1× 晶圆面两层口径）", None),
            ("0.2 子系统分层验收（T1 / T2）与防重复计数总则", None),
        ],
        "html": ch0_html,
    })

    # -------------------------------------------------------------------------
    # CHAPTER 1: WS (WS Self + WRS Dual-Stage Sync + WRS-iHOPC Motion Comp)
    # -------------------------------------------------------------------------
    ws_t1_rows = [
        ("1.1.01", "WS-X 静止在位伺服稳定性", "≤ 0.30 nm (3σ)", "多点停稳保压 ≥ 10 s，关闭双台同步（Sync Off），同步记录机内 ENC 与外部激光干涉仪真值 [注 1-1]"),
        ("1.1.02", "WS-Y 静止在位伺服稳定性", "≤ 0.30 nm (3σ)", "同上，沿 Y 轴统计多点静止停位 3σ（保障 M 侧静态对准与基准点稳度） [注 1-1]"),
        ("1.1.03", "WS-X 单程动态运动误差", "≤ 0.29 nm (3σ)", "满速 0.70 m/s、35–40 m/s²，Sync Off，正扫/反扫分池扣均值，5.5 mm 曝光窗 MA 取大值 [注 1-2]"),
        ("1.1.04", "WS-Y 单程动态运动误差", "≤ 0.29 nm (3σ)", "同上，沿扫描主轴 Y 分池统计正扫与反扫匀速曝光段 5.5 mm 窗 MA 3σ 取大值 [注 1-2]"),
        ("1.1.05", "WS-Z 单程动态运动误差", "≤ 3.60 nm (3σ)", "满速动态扫场，正扫/反扫分池统计垂向 5.5 mm 窗 MA 3σ（归入独立焦面 FU） [注 1-2]"),
        ("1.1.06", "WS-Rx 单程动态运动误差", "≤ 0.150 μrad (3σ)", "绕 X 轴俯仰角，满速正反扫分池统计（沿 2.75 mm 半狭缝杠杆折算边缘离焦） [注 1-2]"),
        ("1.1.07", "WS-Ry 单程动态运动误差", "≤ 0.075 μrad (3σ)", "绕 Y 轴滚转角，满速正反扫分池统计（沿 13.0 mm 半场宽杠杆敏感，严控） [注 1-2]"),
        ("1.1.08", "WS-Rz 单程动态运动误差", "≤ 10.5 nrad (3σ)", "绕 Z 轴偏航角，满速正反扫分池统计（沿 13.0 mm 半场宽转化为 Y 向套刻） [注 1-2]"),
        ("1.1.09", "WS-X 残余反向差", "≤ 0.09 nm", "开启标准方向前馈/ILC 校准后，匀速曝光段正反扫均值差最大值 |μ↑ − μ↓| [注 1-2]"),
        ("1.1.10", "WS-Y 残余反向差", "≤ 0.10 nm", "同上，沿扫描主轴 Y 统计正反扫均值差最大值（占往返总红线 ≤ 26%） [注 1-2]"),
        ("1.1.11", "WS-Z 残余反向差", "≤ 1.20 nm", "考察浸没头流阻与垂向气浮刚度方向不对称引起的 Z 轴正反扫均值差 [注 1-2]"),
        ("1.1.12", "WS-Rx 残余反向差", "≤ 0.050 μrad", "绕 X 轴俯仰角正反扫均值差最大值 |μ↑ − μ↓| [注 1-2]"),
        ("1.1.13", "WS-Ry 残余反向差", "≤ 0.025 μrad", "绕 Y 轴滚转角正反扫均值差最大值 |μ↑ − μ↓| [注 1-2]"),
        ("1.1.14", "WS-Rz 残余反向差", "≤ 3.5 nrad", "绕 Z 轴偏航角正反扫均值差最大值 |μ↑ − μ↓| [注 1-2]"),
        ("1.1.15", "WS-X 往返动态总误差", "≤ 0.38 nm", "线性包络（单程 0.29 + 残余反向差 0.09），交替往返 ≥ 50 循环，取匀速段最差点 [注 1-2]"),
        ("1.1.16", "WS-Y 往返动态总误差", "≤ 0.39 nm", "线性包络（单程 0.29 + 残余反向差 0.10），承受 35–40 m/s² 折返 [注 1-2]"),
        ("1.1.17", "WS-Z 往返动态总误差", "≤ 4.80 nm", "线性包络（单程 3.60 + 残余反向差 1.20），对标陶瓷台 MAz 峰 4 nm（Ref066） [注 1-2]"),
        ("1.1.18", "WS-Rx 往返动态总误差", "≤ 0.200 μrad", "线性包络（0.150 + 0.050），对应 2.75 mm 半狭缝边缘离焦 0.55 nm [注 1-2]"),
        ("1.1.19", "WS-Ry 往返动态总误差", "≤ 0.100 μrad", "线性包络（0.075 + 0.025），对应 13.0 mm 半场宽边缘离焦 1.30 nm [注 1-2]"),
        ("1.1.20", "WS-Rz 往返动态总误差", "≤ 14.0 nrad", "线性包络（10.5 + 3.5），对应 13.0 mm 场边 Y 向套刻 0.18 nm [注 1-2]"),
        ("1.1.21", "WS 步进折返整定时间", "≤ 15 ms", "换场步进/折返加速段结束至 6-DOF 误差进入匀速曝光容差带耗时（空走未开光）"),
        ("1.1.22", "WS 晶圆吸盘（Burl）平坦度", "≤ 6.5 nm (3σ)", "300 mm 吸盘瘤点顶面高精度光学干涉仪面形检定（归入独立焦面 FU）"),
        ("1.1.23", "WS 吸盘-计量块（WT-MB）接口滞回", "≤ 0.15 nm", "35–40 m/s² 正反扫激励下，长柱柔顺支承传力接口残余微滞回（外部差分标尺）"),
    ]

    wrs_sync_rows = [
        ("1.2.01", "WRS 同步平均误差 Sync MA-X", "≤ 0.47 nm (3σ)", "开启同步耦合（Sync On，WS 主/RS 从），0.70/2.80 m/s，5.5 mm 窗相对误差均值（对齐 Ref009） [注 1-3]"),
        ("1.2.02", "WRS 同步平均误差 Sync MA-Y", "≤ 0.49 nm (3σ)", "同上，扫描主轴 Y 相对误差窗均值（折算 1×，对齐 Ref009 Fig. 10 实测） [注 1-3]"),
        ("1.2.03", "WRS 同步平均误差 Sync MA-Z", "≤ 5.35 nm (3σ)", "垂向相对误差窗均值（RS 按 ÷11.14 折算，合成 5.34 nm 归入焦面 FU） [注 1-3]"),
        ("1.2.04", "WRS 同步平均误差 Sync MA-Rx", "≤ 0.25 μrad (3σ)", "绕 X 轴相对俯仰角窗均值（RS 按 ×0.359 折算，狭缝边离焦 0.69 nm） [注 1-3]"),
        ("1.2.05", "WRS 同步平均误差 Sync MA-Ry", "≤ 0.12 μrad (3σ)", "绕 Y 轴相对滚转角窗均值（RS 按 ×0.359 折算，场边离焦 1.56 nm） [注 1-3]"),
        ("1.2.06", "WRS 同步平均误差 Sync MA-Rz", "≤ 17.0 nrad (3σ)", "绕 Z 轴相对偏航角窗均值（RS 按 1:1 折算，与 MA-Y 合成两层 0.760 nm） [注 1-3]"),
        ("1.2.07", "WRS 同步高频抖动 Sync MSD-X", "≤ 2.0 nm (1σ)", "7.86 ms 曝光窗内 X 向相对高频波动标准差（控线条对比度，防耦合抬升） [注 1-3]"),
        ("1.2.08", "WRS 同步高频抖动 Sync MSD-Y", "≤ 2.0 nm (1σ)", "7.86 ms 曝光窗内 Y 向相对高频波动标准差（与 MA-Y 同场同步统计） [注 1-3]"),
        ("1.2.09", "WRS 同步高频抖动 Sync MSD-Z", "≤ 11.0 nm (1σ)", "7.86 ms 曝光窗内 Z 向相对高频波动标准差（保障有效焦深 DOF） [注 1-3]"),
    ]

    wrs_ihopc_rows = [
        ("1.3.01", "WRS-iHOPC K1 [dx(1)] 补偿调节范围", "±200 nm", "全视场（26 × 33 mm）整场 X 平移轨迹指令范围，Sync On 满速验证无饱和 [注 1-4]"),
        ("1.3.02", "WRS-iHOPC K1 [dx(1)] 调节残差精度", "≤ 0.140 nm", "场角误差 0.140 nm；T2 离线闭环跟踪残差 ≤ 0.077 nm（55%），外部标尺+阶跃实曝复核 [注 1-4]"),
        ("1.3.03", "WRS-iHOPC K2 [dy(1)] 补偿调节范围", "±200 nm", "全视场整场 Y 平移轨迹指令范围，Sync On 满速验证无饱和 [注 1-4]"),
        ("1.3.04", "WRS-iHOPC K2 [dy(1)] 调节残差精度", "≤ 0.140 nm", "场角误差 0.140 nm；T2 离线闭环跟踪残差 ≤ 0.077 nm（55%） [注 1-4]"),
        ("1.3.05", "WRS-iHOPC K4 [dy(y)] 补偿调节范围", "±50 nm/cm", "沿扫描向 Y 放大率（改变 WS 与 RS/4 相对扫速比实现）指令范围 [注 1-4]"),
        ("1.3.06", "WRS-iHOPC K4 [dy(y)] 调节残差精度", "≤ 0.080 nm/cm", "场角误差 0.132 nm（b=1.65 cm）；T2 离线闭环 ≤ 0.044 nm/cm（55%） [注 1-4]"),
        ("1.3.07", "WRS-iHOPC K5 [dx(y)] 补偿调节范围", "±50 nm/cm", "整场非扫向 X 随 y 线性斜切（相对扫描斜移轨迹）指令范围 [注 1-4]"),
        ("1.3.08", "WRS-iHOPC K5 [dx(y)] 调节残差精度", "≤ 0.080 nm/cm", "场角误差 0.132 nm；T2 离线闭环 ≤ 0.044 nm/cm（55%） [注 1-4]"),
        ("1.3.09", "WRS-iHOPC K6 [dy(x)] 补偿调节范围", "±50 nm/cm", "绕 Z 轴相对偏航斜切（动态调节 WS/RS 相对 Rz）指令范围 [注 1-4]"),
        ("1.3.10", "WRS-iHOPC K6 [dy(x)] 调节残差精度", "≤ 0.095 nm/cm", "场角误差 0.124 nm（a=1.30 cm）；T2 离线闭环 ≤ 0.052 nm/cm（55%） [注 1-4]"),
        ("1.3.11", "WRS-iHOPC K8 [dy(y²)] 补偿调节范围", "±15 nm/cm²", "沿扫描向二次拉伸相对轨迹范围，须内嵌 5.5 mm 狭缝预补偿逆卷积 [注 1-4]"),
        ("1.3.12", "WRS-iHOPC K8 [dy(y²)] 调节残差精度", "≤ 0.048 nm/cm²", "场角误差 0.131 nm（b²=2.723 cm²）；T2 离线闭环 ≤ 0.026 nm/cm² [注 1-4]"),
        ("1.3.13", "WRS-iHOPC K10 [dy(xy)] 补偿调节范围", "±15 nm/cm²", "扫描中动态线性调节相对 Rz(y) 产生梯形畸变补偿指令范围 [注 1-4]"),
        ("1.3.14", "WRS-iHOPC K10 [dy(xy)] 调节残差精度", "≤ 0.060 nm/cm²", "场角误差 0.129 nm（ab=2.145 cm²）；T2 离线闭环 ≤ 0.033 nm/cm² [注 1-4]"),
        ("1.3.15", "WRS-iHOPC K11 [dx(y²)] 补偿调节范围", "±15 nm/cm²", "非扫向 X 随 y² 弓形弯曲相对轨迹范围，内嵌 5.5 mm 狭缝预补偿 [注 1-4]"),
        ("1.3.16", "WRS-iHOPC K11 [dx(y²)] 调节残差精度", "≤ 0.048 nm/cm²", "场角误差 0.131 nm；T2 离线闭环 ≤ 0.026 nm/cm² [注 1-4]"),
        ("1.3.17", "WRS-iHOPC K14 [dy(y³)] 补偿调节范围", "±5.0 nm/cm³", "沿扫描向三次 S 弯相对轨迹范围，按 5.5 mm 狭缝二阶矩预补偿 [注 1-4]"),
        ("1.3.18", "WRS-iHOPC K14 [dy(y³)] 调节残差精度", "≤ 0.030 nm/cm³", "场角误差 0.135 nm（b³=4.492 cm³）；T2 离线闭环 ≤ 0.017 nm/cm³ [注 1-4]"),
        ("1.3.19", "WRS-iHOPC K16 [dy(xy²)] 补偿调节范围", "±5.0 nm/cm³", "扫描中按 y² 动态调制相对 Rz(y) 实现高阶枕/桶形补偿指令范围 [注 1-4]"),
        ("1.3.20", "WRS-iHOPC K16 [dy(xy²)] 调节残差精度", "≤ 0.036 nm/cm³", "场角误差 0.127 nm（ab²=3.539 cm³）；T2 离线闭环 ≤ 0.020 nm/cm³ [注 1-4]"),
        ("1.3.21", "WRS-iHOPC K19 [dx(y³)] 补偿调节范围", "±5.0 nm/cm³", "非扫向 X 随 y³ 三次 S 弯相对轨迹范围，内嵌 5.5 mm 狭缝预补偿 [注 1-4]"),
        ("1.3.22", "WRS-iHOPC K19 [dx(y³)] 调节残差精度", "≤ 0.030 nm/cm³", "场角误差 0.135 nm；T2 离线闭环 ≤ 0.017 nm/cm³ [注 1-4]"),
        ("1.3.23", "WRS-iHOPC X 向 4 项合成残差（场角）", "≤ 0.269 nm", "K1/K5/K11/K19 单层场角 RSS（两层 1.2× 系数为 0.323 nm，闭环 L1-S1） [注 1-4]"),
        ("1.3.24", "WRS-iHOPC Y 向 7 项合成残差（场角）", "≤ 0.347 nm", "K2/K4/K6/K8/K10/K14/K16 单层场角 RSS（两层 1.2× 系数为 0.416 nm，闭环 L1-S1） [注 1-4]"),
    ]

    ch1_html = f"""
    <p>本章涵盖 <strong>WS（晶圆工件台自身）</strong> 与 <strong>WRS（晶圆-掩模双台同步及场内 iHOPC 运动补偿）</strong>，直接对应整机预算 <strong>L1-S1</strong>（两层 1× 预算 X 0.744 nm / Y 0.867 nm，占 Ref009 六域方差 20.24%）以及独立焦面红线 <strong>FU ≤ 14.0 nm</strong>。按单台独立能力（T1）与双台同步联试（T2）分层验收。</p>

    <h2>1.1 T1 验收项目：WS 自身单台独立 6-DOF 性能（Sync Off）</h2>
    {render_spec_table(ws_t1_rows)}

    <h2>1.2 T2 验收项目：WRS 双台同步误差与 iHOPC 运动补偿（Sync On，1× 口径）</h2>
    <div class="tbl-sub">表 1-2A：WRS 双台同步平均误差（Sync MA）与高频抖动（Sync MSD）</div>
    {render_spec_table(wrs_sync_rows)}

    <div class="tbl-sub">表 1-2B：WRS 场内 iHOPC 运动补偿（11 项参数调节范围与调节精度）</div>
    {render_spec_table(wrs_ihopc_rows)}

    <h2>1.3 复杂标记项工程解释与机理图解</h2>
    <ul class="note-list">
      <li><strong>[注 1-1] 机内闭环自读与外部独立标尺双轨核验：</strong>WS 自身 T1 测试在关闭双台耦合（Sync Off）条件下，须同时采集机内 ENC 闭环误差与外接 6-DOF 激光干涉仪/差分测头真值。两者互为校验，消除编码器热漂、读头安装角与阿贝臂偏置造成的“自读完美但硅片真实偏位”盲区。</li>
      <li><strong>[注 1-2] 单程动态误差、残余反向差与往返包络的拆分判定（见图 1-1）：</strong>步进扫描采用蛇形路径（正扫 +Y 与反扫 −Y 交替）。统计坐标点严格限定于匀速曝光扫描段（y ∈ [−16.5, +16.5] mm）内的固定物理点，取整条路径最差点（通常在刚进入曝光场的“场头”余振最大处）判定。正扫与反扫须<strong>分池各自扣均值</strong>求 3σ 取大值作为单程动态误差（占 74%–76%）；开启标准方向前馈/迭代学习（ILC）后的正反均值差最大值 |μ↑ − μ↓| 为残余反向差（≤ 26%）；三项门限（单程、反向差、往返包络 = 单程 + 反向差）须<strong>同时合格</strong>，严禁混池掩盖。</li>
      <li><strong>[注 1-3] WRS 同步主从策略与单台指标严禁无条件放宽边界（见图 1-2）：</strong>ASML（US 6,373,072 B1）与 Nikon（US 2012/0319637 A1）专利及控制论文（Evers 等, 2019）均证实，ArF/ArFi 横向同步均为 <strong>WS = 主台（Master）、RS = 从台（Slave）</strong>，由惯量更轻、带宽更高的 RS 实时追随 WS 误差，并可外挂 Double-Youla 双向耦合。虽然耦合能使低频 Sync MA 骤降 −64.6%，但会引起高频 Sync MSD 反向抬升 +14.8%（水床效应），且 M 侧对准无 RS 参与、Z/Rx/Ry 不可靠同步覆盖、双台共模漂移会偏离浸没头与物镜中心。因此在取得本机配对实测数据前<strong>不预设单台放宽倍数</strong>，必须严守表 1-1 单台 6-DOF 红线。</li>
      <li><strong>[注 1-4] 为何将 iHOPC 运动补偿（11 项）正式划归 WRS（而非单纯 WS 或 RS）：</strong>工程上由三项硬物理机理决定：① 扫描向放大率 K4、斜切 K5/K6、梯形 K10、高阶弯曲 K8/K11/K14/K16/K19 在像面生效的本质物理量是 <strong>WS 与 RS/4 的相对扫描轨迹</strong>（例如 K4 直接通过改变两台相对扫速比实现，K10/K16 通过扫描中动态微调两台相对偏航角 Rz(y) 实现）；② 二次/三次（y²/y³）轨迹含较高频率成分，在 NXT 平台中由 WS 承载低频基底、高带宽 RS 协同执行高频相对轨迹，单独归属 WS 或 RS 均无法完成曝光闭环；③ 由于曝光狭缝宽 5.5 mm 会对弯曲轨迹产生空间平滑，控制系统必须内置<strong>狭缝逆卷积预补偿</strong>（二阶矩 μ₂ = L_s²/12 = 0.02521 cm²，三次项预补偿系数 3μ₂ = 0.07563 cm²）。T2 验收先查双台闭环跟踪残差（≤ 总限值 55%），再以外部标尺核对轨迹无相位滞后，最终由 T3 指令阶跃曝光闭环放行。</li>
    </ul>

    <div class="fig-box">
      <img src="{figs['fig1_1'].as_uri()}" alt="图1-1 正反扫拆分定义与NXT1965Ci配比"/>
      <div class="fig-cap">图 1-1：(a) 正扫与反扫动态误差分布及单程/残余反向差拆分定义；(b) NXT:1965Ci WS/RS 平移轴 1× 往返拆分配比</div>
    </div>

    <div class="fig-box">
      <img src="{figs['fig1_2'].as_uri()}" alt="图1-2 双向耦合MA与MSD折衷"/>
      <div class="fig-cap">图 1-2：双向同步耦合虽大幅压低低频套刻 MA（−64.6%），但导致高频对比度抖动 MSD 反向抬升（+14.8%），数据源自 Evers 等 (2019) Table 1</div>
    </div>
    """
    chapters.append({
        "num": 1, "id": "ch-1",
        "title": "第 1 章　WS（晶圆工件台与 WRS 双台同步子系统）",
        "toc_title": "第 1 章　WS（晶圆工件台与 WRS 双台同步子系统）",
        "sections": [
            ("1.1 T1 验收项目：WS 自身单台独立 6-DOF 性能（Sync Off）", None),
            ("1.2 T2 验收项目：WRS 双台同步误差与 iHOPC 运动补偿（Sync On）", None),
            ("1.3 复杂标记项工程解释与机理图解", None),
        ],
        "html": ch1_html,
    })

    # -------------------------------------------------------------------------
    # CHAPTER 2: RS (Reticle Stage)
    # -------------------------------------------------------------------------
    rs_t1_rows = [
        ("2.1.01", "RS-X 静止在位伺服稳定性 (4×)", "≤ 0.85 nm (3σ)", "掩模面 4× 原值，多点停稳保压 ≥ 10 s，Sync Off，同步记 ENC 与外部标尺（1× 等效 0.21 nm）"),
        ("2.1.02", "RS-Y 静止在位伺服稳定性 (4×)", "≤ 0.85 nm (3σ)", "同上，沿掩模扫描主轴 Y 统计静止停位 3σ（1× 等效 0.21 nm）"),
        ("2.1.03", "RS-X 单程动态运动误差 (4×)", "≤ 0.84 nm (3σ)", "满速 2.80 m/s、150 m/s²，Sync Off，正反扫分池扣均值，7.86 ms 窗 MA（1× 等效 0.21 nm） [注 2-1]"),
        ("2.1.04", "RS-Y 单程动态运动误差 (4×)", "≤ 0.88 nm (3σ)", "同上，扫描主轴 Y 正反扫分池统计（1× 等效 0.22 nm） [注 2-1]"),
        ("2.1.05", "RS-Z 单程动态运动误差 (4×)", "≤ 19.5 nm (3σ)", "垂向 Z 正反扫分池统计（按 ÷11.14 折算 1× 等效 1.75 nm，入焦面 FU） [注 2-1]"),
        ("2.1.06", "RS-Rx 单程动态运动误差 (4×)", "≤ 0.315 μrad (3σ)", "绕 X 轴俯仰角正反扫分池统计（按 ×0.359 折算 1× 等效 0.113 μrad） [注 2-1]"),
        ("2.1.07", "RS-Ry 单程动态运动误差 (4×)", "≤ 0.142 μrad (3σ)", "绕 Y 轴滚转角正反扫分池统计（按 ×0.359 折算 1× 等效 0.051 μrad） [注 2-1]"),
        ("2.1.08", "RS-Rz 单程动态运动误差 (4×)", "≤ 7.5 nrad (3σ)", "绕 Z 轴偏航角正反扫分池统计（1:1 等角传至硅片，无 4× 缩小红利！） [注 2-1]"),
        ("2.1.09", "RS-X 残余反向差 (4×)", "≤ 0.28 nm", "开启标准方向前馈/ILC 校准后，匀速段正反扫均值差最大值（1× 等效 0.07 nm） [注 2-1]"),
        ("2.1.10", "RS-Y 残余反向差 (4×)", "≤ 0.30 nm", "同上，150 m/s² 急折返下扫描主轴 Y 正反扫均值差最大值（1× 等效 0.075 nm） [注 2-1]"),
        ("2.1.11", "RS-Z 残余反向差 (4×)", "≤ 6.5 nm", "垂向 Z 匀速段正反扫均值差最大值（1× 等效 0.58 nm） [注 2-1]"),
        ("2.1.12", "RS-Rx 残余反向差 (4×)", "≤ 0.105 μrad", "绕 X 轴俯仰角正反扫均值差最大值（1× 等效 0.038 μrad） [注 2-1]"),
        ("2.1.13", "RS-Ry 残余反向差 (4×)", "≤ 0.048 μrad", "绕 Y 轴滚转角正反扫均值差最大值（1× 等效 0.017 μrad） [注 2-1]"),
        ("2.1.14", "RS-Rz 残余反向差 (4×)", "≤ 2.5 nrad", "绕 Z 轴偏航角正反扫均值差最大值（1:1 等角传递，严控双驱电机同步滞回） [注 2-1]"),
        ("2.1.15", "RS-X 往返动态总误差 (4×)", "≤ 1.12 nm", "线性包络（0.84 + 0.28 = 1.12 nm，1× 等效 0.28 nm），交替往返 ≥ 50 循环 [注 2-1]"),
        ("2.1.16", "RS-Y 往返动态总误差 (4×)", "≤ 1.18 nm", "线性包络（0.88 + 0.30 = 1.18 nm，1× 等效 0.30 nm），150 m/s² 折返 [注 2-1]"),
        ("2.1.17", "RS-Z 往返动态总误差 (4×)", "≤ 26.0 nm", "线性包络（19.5 + 6.5 = 26.0 nm，1× 等效 2.33 nm） [注 2-1]"),
        ("2.1.18", "RS-Rx 往返动态总误差 (4×)", "≤ 0.420 μrad", "线性包络（0.315 + 0.105 = 0.420 μrad，1× 等效 0.151 μrad） [注 2-1]"),
        ("2.1.19", "RS-Ry 往返动态总误差 (4×)", "≤ 0.190 μrad", "线性包络（0.142 + 0.048 = 0.190 μrad，1× 等效 0.068 μrad） [注 2-1]"),
        ("2.1.20", "RS-Rz 往返动态总误差 (4×)", "≤ 10.0 nrad", "线性包络（7.5 + 2.5 = 10.0 nrad，1:1 等角传递至晶圆面） [注 2-1]"),
        ("2.1.21", "RS 步进折返整定时间", "≤ 10 ms", "150 m/s² 折返结束至 6-DOF 进入稳态匀速容差带耗时（须显著快于 WS 15 ms）"),
        ("2.1.22", "RS 掩模真空重夹重复性 X (4×)", "≤ 0.72 nm (3σ)", "标准 6 寸石英掩模卸载-分段柔顺真空重夹 ≥ 30 次，外部光学标尺测 X 位移（1×: 0.18 nm） [注 2-2]"),
        ("2.1.23", "RS 掩模真空重夹重复性 Y (4×)", "≤ 0.72 nm (3σ)", "同上，测 Y 向掩模重夹重复性（1× 等效 0.18 nm，归属 L1-S5 掩模夹持） [注 2-2]"),
        ("2.1.24", "RS 高加减速千趟微滑移 X (4×)", "≤ 0.72 nm", "150 m/s² 满载连续往返扫描 1000 趟前后，外部标尺/空间像测石英板相对夹爪 X 滑移 [注 2-2]"),
        ("2.1.25", "RS 高加减速千趟微滑移 Y (4×)", "≤ 0.72 nm", "同上，沿 150 m/s² 扫描主轴 Y 测千趟累积微滑移（编码器完全不可见，必须外部验！） [注 2-2]"),
    ]

    ch2_html = f"""
    <p>本章规定 <strong>RS（掩模工件台）</strong> 自身单台独立性能，按方差份额 <strong>36%（RS/4）: 64%（WS）</strong> 与第 1 章 WS 共同闭环 <strong>L1-S1</strong> 同步误差，并承担 <strong>L1-S5</strong> 掩模夹持与微滑移预算。所有门限均以<strong>掩模侧 4× 原生尺度</strong>直接验收；RS 参与的双台同步跟踪及 iHOPC 相对轨迹已在第 1 章 <strong>WRS（T2）</strong> 统一闭环，故本章单设 <strong>T1</strong> 验收表。</p>

    <h2>2.1 T1 验收项目：RS 自身单台独立 6-DOF 与微滑移性能（Sync Off，4× 原值）</h2>
    {render_spec_table(rs_t1_rows)}

    <h2>2.2 复杂标记项工程解释与 4× → 1× 光学折算边界</h2>
    <ul class="note-list">
      <li><strong>[注 2-1] 液浸 4× 投影 6-DOF 光学折算关系与单台独立验收要求：</strong>在 193 nm 液浸投影物镜（缩小倍率 4:1，超纯水折射率 n_w = 1.4366）下，掩模台 6 个自由度误差折算到硅片 1× 像面的比例各不相同：水平 <strong>X / Y 除以 4</strong>（×0.2500）；垂向 <strong>Z 除以 11.14</strong>（×n_w/16 = 0.0898）；俯仰/滚转 <strong>Rx / Ry 乘以 0.3592</strong>（×n_w/4）；而绕竖轴偏航角 <strong>Rz 严格按 1:1 原样传递</strong>（无 4× 缩小红利！）。因此 RS-Rz 往返限值（≤ 10.0 nrad）甚至比 WS-Rz（≤ 14.0 nrad）更严苛。与 WS 相同，RS 单程、残余反向差与往返包络三项须同时达标，并配合外接激光干涉仪复核真值。</li>
      <li><strong>[注 2-2] 150 m/s² 急加减速掩模微滑移与薄膜（Pellicle）装配边界：</strong>RS 换向加速度高达 150 m/s²（约 15 g），巨大的惯性剪切力会诱发石英掩模相对真空吸盘发生纳米级不可逆微滑移（Micro-slip）。由于编码器测的是掩模台底座而非石英板自身，该滑移在机内伺服日志中完全隐身，必须在 T1/T2b 阶段以空间像或外部光学标尺做 1000 趟前后实测（≤ 0.72 nm 4× / 0.18 nm 1×）。此外，装防尘膜（Pellicle）时须采用分段柔顺夹持（JP 5,809,458 B2）与软热熔胶垫工艺，使高速吹扫动态残差控制在 ≤ 0.14 nm (1×)（Ref098, Ref104）。</li>
    </ul>
    """
    chapters.append({
        "num": 2, "id": "ch-2",
        "title": "第 2 章　RS（掩模工件台子系统）",
        "toc_title": "第 2 章　RS（掩模工件台子系统）",
        "sections": [
            ("2.1 T1 验收项目：RS 自身单台独立 6-DOF 与微滑移性能（Sync Off）", None),
            ("2.2 复杂标记项工程解释与 4× → 1× 光学折算边界", None),
        ],
        "html": ch2_html,
    })

    return chapters


def render_spec_table(rows: list) -> str:
    trs = []
    for idx, name, spec, test_def in rows:
        trs.append(
            f'<tr>'
            f'<td class="c-idx">{esc(idx)}</td>'
            f'<td class="c-name">{fmt_inline(name)}</td>'
            f'<td class="c-spec">{fmt_inline(spec)}</td>'
            f'<td class="c-def">{fmt_inline(test_def)}</td>'
            f'</tr>'
        )
    return (
        '<table class="spec-tbl">'
        '<thead><tr>'
        '<th style="width:8%">序号</th>'
        '<th style="width:27%">指标项</th>'
        '<th style="width:19%">验收规格</th>'
        '<th style="width:46%">标准测试定义与工装条件</th>'
        '</tr></thead>'
        '<tbody>' + "".join(trs) + '</tbody></table>'
    )


def append_remaining_chapters(chapters: list, figs: dict) -> list:
    """Append Chapters 3 (ENC), 4 (AA), 5 (TIS+PARIS), 6 (Lens), and 7 (References)."""

    # -------------------------------------------------------------------------
    # CHAPTER 3: ENC (2D Optical Grating Encoder)
    # -------------------------------------------------------------------------
    enc_t1_rows = [
        ("3.1.01", "ENC-WS X 轴原始宽带噪声 (1 kHz)", "≤ 0.22 nm (3σ)", "离线零膨胀刚性参考块锁死（无伺服激励），1 kHz 采样并附 0.1 Hz–2 kHz PSD/CPS（对齐 Ref009） [注 3-1]"),
        ("3.1.02", "ENC-WS Y 轴原始宽带噪声 (1 kHz)", "≤ 0.22 nm (3σ)", "同上，沿 Y 轴测量 1 kHz 原始宽带噪声并交付 PSD/CPS 频谱 [注 3-1]"),
        ("3.1.03", "ENC-WS Z 轴原始宽带噪声 (1 kHz)", "≤ 0.65 nm (3σ)", "同上，沿垂向 Z 轴测量 1 kHz 原始宽带噪声（衍射垂向灵敏度约为 XY 3 倍） [注 3-1]"),
        ("3.1.04", "ENC-WS X 轴曝光窗滤波底噪 (~64 Hz)", "≤ 0.13 nm (3σ)", "由 3.1.01 同一时序经 5.5 mm / 7.86 ms 滑窗平均（含 30% 低频有色噪声，匹配 WS-X 1:3） [注 3-2]"),
        ("3.1.05", "ENC-WS Y 轴曝光窗滤波底噪 (~64 Hz)", "≤ 0.13 nm (3σ)", "由 3.1.02 同一时序经 7.86 ms 滑窗平均（匹配 WS-Y 0.39 nm 1:3 计量原则） [注 3-2]"),
        ("3.1.06", "ENC-WS Z 轴曝光窗滤波底噪 (~64 Hz)", "≤ 0.38 nm (3σ)", "由 3.1.03 同一时序经 7.86 ms 滑窗平均 [注 3-2]"),
        ("3.1.07", "ENC-WS Rx 轴曝光窗滤波底噪 (~64 Hz)", "≤ 3.2 nrad (3σ)", "按四角 320 mm 基线 Z 通道差分运动学投影（含 2× 气隙余量） [注 3-1]"),
        ("3.1.08", "ENC-WS Ry 轴曝光窗滤波底噪 (~64 Hz)", "≤ 3.2 nrad (3σ)", "同上，绕 Y 轴等效投影曝光窗测量底噪 [注 3-1]"),
        ("3.1.09", "ENC-WS Rz 轴曝光窗滤波底噪 (~64 Hz)", "≤ 1.6 nrad (3σ)", "按四角 320 mm 基线 XY 通道差分运动学投影 [注 3-1]"),
        ("3.1.10", "ENC-RS X 轴原始宽带噪声 (1 kHz, 4×)", "≤ 0.68 nm (3σ)", "掩模侧离线零位移刚性参考块 1 kHz 采样，附 PSD/CPS（1× 等效 0.17 nm） [注 3-1]"),
        ("3.1.11", "ENC-RS Y 轴原始宽带噪声 (1 kHz, 4×)", "≤ 0.68 nm (3σ)", "同上，掩模侧 Y 轴 1 kHz 原始宽带噪声 [注 3-1]"),
        ("3.1.12", "ENC-RS X 轴曝光窗滤波底噪 (4×)", "≤ 0.37 nm (3σ)", "由 3.1.10 同一时序经 7.86 ms 滑窗平均（匹配 RS-X 1.12 nm 1:3；1×: 0.093 nm） [注 3-2]"),
        ("3.1.13", "ENC-RS Y 轴曝光窗滤波底噪 (4×)", "≤ 0.39 nm (3σ)", "由 3.1.11 同一时序经 7.86 ms 滑窗平均（匹配 RS-Y 1.18 nm 1:3；1×: 0.098 nm） [注 3-2]"),
        ("3.1.14", "ENC-RS Z 轴曝光窗滤波底噪 (4×)", "≤ 2.60 nm (3σ)", "掩模侧 Z 轴曝光窗滤波底噪（1× 等效 0.23 nm） [注 3-2]"),
        ("3.1.15", "ENC-RS Rx 轴曝光窗滤波底噪 (4×)", "≤ 18.0 nrad (3σ)", "掩模侧 200 mm 基线 Z 通道差分投影（1× 等效 6.5 nrad）"),
        ("3.1.16", "ENC-RS Ry 轴曝光窗滤波底噪 (4×)", "≤ 18.0 nrad (3σ)", "同上，掩模侧绕 Y 轴差分投影（1× 等效 6.5 nrad）"),
        ("3.1.17", "ENC-RS Rz 轴曝光窗滤波底噪 (4×)", "≤ 2.8 nrad (3σ)", "掩模侧 200 mm 基线 XY 通道差分投影（1:1 传至像面，匹配 RS-Rz 10 nrad 1:3）"),
        ("3.1.18", "Gridplate 二维栅格板短程刻线精度", "≤ 0.30 nm (3σ)", "出厂自标定干涉仪检验 < 15 mm 局部空间周期误差与正交性（Zerodur/ULE 基底） [注 3-3]"),
    ]

    enc_t2_rows = [
        ("3.2.01", "ENC-WS X 轴过缝切头跳变 (EMSI)", "≤ 0.15 nm (3σ)", "装机全行程往返跨过栅格板拼接缝，3-of-4 读数头重叠区在线自标定衔接跳变 [注 3-3]"),
        ("3.2.02", "ENC-WS Y 轴过缝切头跳变 (EMSI)", "≤ 0.15 nm (3σ)", "同上，沿 Y 轴统计过缝读数头切换（Handover）坐标衔接跳变 [注 3-3]"),
        ("3.2.03", "ENC-WS Z 轴过缝切头跳变 (EMSI)", "≤ 0.45 nm (3σ)", "同上，沿垂向 Z 轴统计过缝读数头切换衔接跳变 [注 3-3]"),
        ("3.2.04", "Gridplate 7 天网格热稳定性 X", "≤ 0.20 nm (3σ)", "装机 10 mK 气幕运行，连续 7 天以参考片/13×19 多移位复测 X 网格漂移（对齐 Ref062） [注 3-3]"),
        ("3.2.05", "Gridplate 7 天网格热稳定性 Y", "≤ 0.20 nm (3σ)", "同上，连续 7 天复测大尺度 Y 向网格热稳定性 [注 3-3]"),
        ("3.2.06", "ENC-WS 高速细分周期非线性 X", "≤ 0.08 nm (3σ)", "WS 0.70 m/s 恒速扫过整数栅距，频谱提取空间基频/倍频电子相位细分非线性（Ref060）"),
        ("3.2.07", "ENC-WS 高速细分周期非线性 Y", "≤ 0.08 nm (3σ)", "同上，Y 轴高速扫描电子相位细分周期非线性误差"),
        ("3.2.08", "ENC-WS 装机外部标尺一致性偏差 X", "≤ 0.15 nm (3σ)", "装机静止与低速扫描下，对比 ENC 解算 X 位姿与外接激光干涉仪差值（核验阿贝臂） [注 3-1]"),
        ("3.2.09", "ENC-WS 装机外部标尺一致性偏差 Y", "≤ 0.15 nm (3σ)", "同上，对比 ENC 解算 Y 位姿与外接激光干涉仪差值（核验安装方位角与阿贝臂） [注 3-1]"),
    ]

    ch3_html = f"""
    <p>本章规定 <strong>ENC（二维光栅编码器测量子系统）</strong> 的验收规格。ENC 为 WS、RS、AA 及 TIS/PARIS 提供底层空间坐标尺，按 <strong>1:3 计量精度原则</strong>设计，<strong>其误差已内嵌于 WS/RS/WRS 闭环，在整机套刻 L0 总账中严禁重复计数</strong>。验收明确切分为 <strong>T1（纯传感器离线本体，无伺服）</strong> 与 <strong>T2（装机计量链、过缝切头与长期热稳）</strong> 两级。</p>

    <h2>3.1 T1 验收项目：纯 ENC 传感器与光栅本体离线测试（脱离伺服闭环）</h2>
    {render_spec_table(enc_t1_rows)}

    <h2>3.2 T2 验收项目：ENC 装机计量链、过缝切头与长期热稳定性</h2>
    {render_spec_table(enc_t2_rows)}

    <h2>3.3 复杂标记项工程解释与机理图解</h2>
    <ul class="note-list">
      <li><strong>[注 3-1] ENC 本底（T1）与台体闭环稳度的解耦边界（见图 3-1）：</strong>ENC 本质上是位移量测尺子，并非工件台在位伺服稳定性。T1 必须在脱离 WS/RS 伺服环路的离线零膨胀刚性参考块上测清光学与电子学本底；T2 在装机后须用外接独立激光干涉仪核对 6-DOF 解算真值，检验读数头 45° 安装方位角、阿贝臂与热漂，消除“传感器自己测自己”的盲区。</li>
      <li><strong>[注 3-2] 原始宽带（1 kHz）与 5.5 mm 曝光窗滤波（63.64 Hz）双频段验收依据（见图 3-2）：</strong>在 5.5 mm 真实狭缝、0.70 m/s 扫速下，光刻胶任意一点的曝光积分时间为 τ_slit = 7.857 ms，等效噪声带宽 ENBW = 1/(2τ_slit) = 63.64 Hz（首零点 127.3 Hz）。低于 63.64 Hz 的慢漂与湍流不会被平均掉，直接转化为套刻误差；高于 63.64 Hz 的噪声决定对比度抖动（MSD）并会被伺服微分环节放大。若把 0.22 nm 宽带噪声全当纯白噪声，窗内下限仅 0.056 nm（偏乐观）；按 30% 低频有色 + 70% 高频白噪合成得 σ_ENC,MA = √(0.30×0.22² + 0.70×0.22²×63.64/936.4) = <strong>0.130 nm</strong>（Heertjes 等, 2024），恰好严守 WS-X 0.38 nm 的 1:3 原则。因此 FAT 须用同一组原始时序同步交付宽带值、曝光窗值及 0.1 Hz–2 kHz PSD/CPS。</li>
      <li><strong>[注 3-3] Gridplate 架构及三概念辨析：</strong>Gridplate（二维光栅网格板）是固定在计量框架（MF）底部的超低膨胀微晶玻璃棋盘状光栅尺（约 0.8 × 0.8 m，短固定光程 < 15 mm，10 mK 气幕），与随台运动的 4 角读数头共同构成 ENC。大行程跨过拼缝时靠 3-of-4 读数头在线一致性自标定（EMSI）将切头跳变控至 ≤ 0.15 nm。工程中须严格区分三类对象：<strong>Gridplate</strong>（机台静止空间尺）、<strong>AA 标记</strong>（刻在硅片上的微小光栅）、<strong>晶圆网格</strong>（HOWA 拟合出的全片变形坐标图）。</li>
    </ul>

    <div class="fig-box">
      <img src="{figs['fig3_1'].as_uri()}" alt="图3-1 ENC测量链与台体闭环解耦架构"/>
      <div class="fig-cap">图 3-1：ENC 测量本底（T1）、装机计量链（T2）与 WS/WRS 运动闭环的物理传递与验收解耦架构</div>
    </div>

    <div class="fig-box">
      <img src="{figs['fig3_2'].as_uri()}" alt="图3-2 5.5mm真实狭缝曝光窗滑窗滤波"/>
      <div class="fig-cap">图 3-2：5.5 mm 真实狭缝（τ = 7.857 ms）曝光窗滑窗平均幅频响应 |sinc(f·τ)| 及 ENC 双频段验收的物理分工</div>
    </div>
    """
    chapters.append({
        "num": 3, "id": "ch-3",
        "title": "第 3 章　ENC（二维光栅编码器测量子系统）",
        "toc_title": "第 3 章　ENC（二维光栅编码器测量子系统）",
        "sections": [
            ("3.1 T1 验收项目：纯 ENC 传感器与光栅本体离线测试", None),
            ("3.2 T2 验收项目：ENC 装机计量链、过缝切头与长期热稳定性", None),
            ("3.3 复杂标记项工程解释与机理图解", None),
        ],
        "html": ch3_html,
    })

    # -------------------------------------------------------------------------
    # CHAPTER 4: AA (M-side Wafer Alignment - SMASH 4-Color)
    # -------------------------------------------------------------------------
    aa_t1_rows = [
        ("4.1.01", "AA 单标记静态重复性 X（强光 WQ ≥ 1%）", "≤ 0.22 nm (3σ)", "离线超稳参考扫描台架（无步进激振），标准无损标完整独立重扫 ≥ 25 趟，扣参考位移（对齐 Ref015） [注 4-1]"),
        ("4.1.02", "AA 单标记静态重复性 Y（强光 WQ ≥ 1%）", "≤ 0.22 nm (3σ)", "同上，Y 向标记完整独立重扫 ≥ 25 趟（4 色均须独立达标；单趟多点不可充当独立重复！） [注 4-1]"),
        ("4.1.03", "AA 单标记静态重复性 X（弱光 WQ 0.1%–1%）", "≤ 0.50 nm (3σ)", "衰减光强模拟厚膜/工艺损耗标记，独立重扫 ≥ 25 趟，核验低信噪下不发散（对齐 Ref015） [注 4-1]"),
        ("4.1.04", "AA 单标记静态重复性 Y（弱光 WQ 0.1%–1%）", "≤ 0.50 nm (3σ)", "同上，弱光条件 Y 向标记独立重扫 ≥ 25 趟 [注 4-1]"),
        ("4.1.05", "AA 绿光通道（532 nm）单标读出可用率", "≥ 99.5%", "标准及衰减光栅标记下有效信号捕获率（防单色失效拖累多色融合） [注 4-2]"),
        ("4.1.06", "AA 红光通道（635 nm）单标读出可用率", "≥ 99.5%", "同上，独立统计 635 nm 通道有效读出可用率 [注 4-2]"),
        ("4.1.07", "AA 近红外 1 通道（780 nm）单标读出可用率", "≥ 99.5%", "同上，独立统计 780 nm 通道有效读出可用率 [注 4-2]"),
        ("4.1.08", "AA 近红外 2 通道（850 nm）单标读出可用率", "≥ 99.5%", "同上，独立统计 850 nm 通道有效读出可用率 [注 4-2]"),
        ("4.1.09", "AA 四色 24 h 色间配准漂移 X", "≤ 0.32 nm (3σ)", "同一标准标记连续 24 h 周期复测，任意两色位置差之慢漂（OCW 算法硬前提） [注 4-2]"),
        ("4.1.10", "AA 四色 24 h 色间配准漂移 Y", "≤ 0.32 nm (3σ)", "同上，Y 向四色 24 h 色间配准漂移稳定性 [注 4-2]"),
        ("4.1.11", "AA 跨衍射级次（1/3/5/7 级）零位漂移", "≤ 0.30 nm (3σ)", "24 h 内不同衍射级次解算位置之相对漂移（支撑多级次加权抑制标记不对称）"),
    ]

    aa_t2_rows = [
        ("4.2.01", "AA 单标记动态扫描重复性 X", "≤ 0.38 nm (3σ)", "装入真实/模拟 M 侧晶圆台，按量产扫描速度与步进折返完整重扫同一标记 ≥ 25 趟 [注 4-1]"),
        ("4.2.02", "AA 单标记动态扫描重复性 Y", "≤ 0.38 nm (3σ)", "同上，Y 向生产轨迹动态重复性（含静态 0.22 + M 侧 WS 0.31 合成 0.380 nm） [注 4-1]"),
        ("4.2.03", "AA 全晶圆网格拟合重复性 X（HOWA 不重装）", "≤ 0.40 nm (3σ)", "类 FIWA 全片 ≥ 20 标扫描拟合 HOWA 网格，不卸片连测 ≥ 10 轮，强制正反扫配平（Ref123） [注 4-3]"),
        ("4.2.04", "AA 全晶圆网格拟合重复性 Y（HOWA 不重装）", "≤ 0.40 nm (3σ)", "同上，Y 向不重装片全片 HOWA 网格重复性 [注 4-3]"),
        ("4.2.05", "AA 全晶圆网格拟合重复性 X（HOWA 重装片）", "≤ 0.50 nm (3σ)", "每轮执行卸片-真空重新吸片（含吸片重复 0.30 nm），考核 X 向完整上片网格重复性 [注 4-3]"),
        ("4.2.06", "AA 全晶圆网格拟合重复性 Y（HOWA 重装片）", "≤ 0.50 nm (3σ)", "同上，Y 向重装片全片 HOWA 网格重复性 [注 4-3]"),
        ("4.2.07", "AA 全片边缘留出点网格预测残差 X", "≤ 0.45 nm (3σ)", "预留 20% 未参与拟合的边缘/随机标记作盲测考题，验证 HOWA 外推预测精度 [注 4-3]"),
        ("4.2.08", "AA 全片边缘留出点网格预测残差 Y", "≤ 0.45 nm (3σ)", "同上，Y 向边缘留出点网格预测残差 [注 4-3]"),
        ("4.2.09", "M–E 对准基线短期漂移 X", "≤ 0.30 nm (3σ)", "整机批内 M 侧至 E 侧坐标零点 X 向漂移（靠 TIS 清零；与 0.40 合成单层 0.50 / 两层 0.707 nm） [注 4-3]"),
        ("4.2.10", "M–E 对准基线短期漂移 Y", "≤ 0.30 nm (3σ)", "同上，Y 向 M–E 对准基线短期漂移 [注 4-3]"),
    ]

    ch4_html = f"""
    <p>本章规定 <strong>AA（M 侧晶圆对准子系统，SMASH 四色架构）</strong> 的验收规格，与第 5 章 TIS+PARIS 共同闭环 <strong>L1-S2</strong>（两层 1× 预算 0.970 nm，占 Ref009 六域方差 25.38%），其中 AA 承担单层 0.500 nm（两层 0.707 nm）。按 <strong>T1（纯传感器离线台架）</strong> 与 <strong>T2（类 FIWA 全片网格集成验收）</strong> 两级划分。</p>

    <h2>4.1 T1 验收项目：AA 光学传感器本体离线测试（参考扫描台架）</h2>
    {render_spec_table(aa_t1_rows)}

    <h2>4.2 T2 验收项目：AA + M 侧晶圆台类 FIWA / HOWA 全片集成验收</h2>
    {render_spec_table(aa_t2_rows)}

    <h2>4.3 复杂标记项工程解释与多波长文献支撑</h2>
    <ul class="note-list">
      <li><strong>[注 4-1] 单标记“静态”与“动态”重复性定义及采样独立性铁律：</strong>SMASH 相位光栅对准（PGA）在原理上需晶圆台带动标记匀速扫过照明光斑，经正弦干涉光强傅里叶相位解算位置。因此 T1 的“静态重复性”指在<strong>离线超稳参考扫描台架（无步进加减速激振）</strong>上扣除参考干涉仪位移后的纯光学/电子学本底；T2 的“动态重复性”指装入真实/模拟 M 侧晶圆台按量产步进折返节拍扫描时的组合误差。<strong>严禁将单趟扫描中采集的多个样点充当独立重复</strong>（同一趟共享一次轨迹与相位扰动），必须完整进出标记独立重扫 ≥ 25 趟统计 3σ。</li>
      <li><strong>[注 4-2] 多波长四色抗工艺畸变的一手论文支撑与色间漂移红线：</strong>ASML 与业界论文（Menchtchikov 等, SPIE 10587, 2018；Ref015; Ref120）证实，多色（532/635/780/850 nm）在工艺膜层中穿透深度与干涉条件不同，结合最佳色彩加权（OCW）可把标记不对称引起的套刻波动降低 1.2–1.3 nm。但该优势成立的硬前提是<strong>四色自身 24 h 色间配准漂移极小（≤ 0.32 nm）</strong>且各通道可用率 ≥ 99.5%，否则仪器自身色差漂移会被 OCW 误判为工艺不对称而反向放大套刻误差。</li>
      <li><strong>[注 4-3] 离线类 FIWA → HOWA 分级验证与产品片工艺边界：</strong>全片网格拟合（HOWA）在动作上等价于整机 FIWA（精细晶圆对准），须在 T2 分别报告“不重装片”（检传感器+台体）与“重装片”（含吸片重复性），并留出 20% 边缘标记验证外推预测；同时<strong>强制采用正反扫（SUSD）与步进方向配平采样</strong>，杜绝 Ref123 报道的 > 3.5 nm 方向混叠虚假网格。此外，晶圆厂刻蚀/CMP 引起的工艺标记不对称残差（<strong>WAD ≤ 0.50 nm</strong>）明确划归客户产品片（T4）工艺集成验证，不混入标准参考片 T1/T2 验收。</li>
    </ul>
    """
    chapters.append({
        "num": 4, "id": "ch-4",
        "title": "第 4 章　AA（M 侧晶圆对准子系统 · SMASH 四色）",
        "toc_title": "第 4 章　AA（M 侧晶圆对准子系统 · SMASH 四色）",
        "sections": [
            ("4.1 T1 验收项目：AA 光学传感器本体离线测试", None),
            ("4.2 T2 验收项目：AA + M 侧晶圆台类 FIWA / HOWA 集成验收", None),
            ("4.3 复杂标记项工程解释与多波长文献支撑", None),
        ],
        "html": ch4_html,
    })

    # -------------------------------------------------------------------------
    # CHAPTER 5: TIS + PARIS (E-side Aerial Image Sensors — T1 Only!)
    # -------------------------------------------------------------------------
    tis_paris_t1_rows = [
        ("5.1.01", "TIS 水平空间像对准重复性 X", "≤ 0.40 nm (3σ)", "E 侧 6 kHz 193 nm 曝光光扫描掩模透射像基准标记 ≥ 30 次，扣除台体参考位姿 [注 5-1]"),
        ("5.1.02", "TIS 水平空间像对准重复性 Y", "≤ 0.40 nm (3σ)", "同上，沿 Y 轴统计透射空间像水平对准重复性（用于 M–E 基线定期清零） [注 5-1]"),
        ("5.1.03", "TIS 最佳焦面定位重复性 Z", "≤ 2.80 nm (3σ)", "沿 Z 轴通过焦面扫峰提取最佳焦面位置重复性（直接归入独立焦面 FU） [注 5-1]"),
        ("5.1.04", "双台 TIS-1 / TIS-2 24 h 匹配漂移 X", "≤ 0.28 nm (3σ)", "1 号与 2 号晶圆台 TIS 零点连续 24 h 交叉比对 X 向相对漂移（直控 ΔC2C ≤ 0.48 nm） [注 5-2]"),
        ("5.1.05", "双台 TIS-1 / TIS-2 24 h 匹配漂移 Y", "≤ 0.28 nm (3σ)", "同上，24 h 交叉比对双台 TIS 零点 Y 向相对匹配漂移 [注 5-2]"),
        ("5.1.06", "双台 TIS-1 / TIS-2 24 h 匹配漂移 Z", "≤ 2.00 nm (3σ)", "同上，24 h 交叉比对双台焦面基准 Z 向相对漂移"),
        ("5.1.07", "TIS 浸没供水流量窗口敏感度 X", "≤ 0.15 nm", "在标称 UPW 浸没供回水流量工作窗内扫频测试，确认 X 向 TIS 重复性无跳变（Ref164） [注 5-1]"),
        ("5.1.08", "TIS 浸没供水流量窗口敏感度 Y", "≤ 0.15 nm", "同上，确认 Y 向 TIS 重复性对 UPW 流量波动不敏感 [注 5-1]"),
        ("5.1.09", "TIS 浸没供水流量窗口敏感度 Z", "≤ 1.20 nm", "同上，确认 Z 向最佳焦面重复性对 UPW 流量波动不敏感 [注 5-1]"),
        ("5.1.10", "PARIS 7 点掩模对准重复性 X (RA-X)", "≤ 0.47 nm (3σ)", "沿 26 mm 狭缝 7 个视场点并行扫描掩模标记（每片 3 扫），取最差点 X 重复性（对齐 Ref066 < 0.50 nm） [注 5-2]"),
        ("5.1.11", "PARIS 7 点掩模对准重复性 Y (RA-Y)", "≤ 0.47 nm (3σ)", "同上，取 7 个视场点 Y 向掩模对准重复性最差值（两层 0.665 nm，闭环 L1-S2） [注 5-2]"),
        ("5.1.12", "PARIS 7 点场曲测焦重复性 Z", "≤ 3.20 nm (3σ)", "7 个视场点并行测量投影物镜沿狭缝焦面弯曲（场曲）重复性 [注 5-2]"),
        ("5.1.13", "PARIS 奇像差波前测量噪声", "≤ 0.14 nm RMS", "连续多轮全瞳波前反演，计算 Z5–Z64 奇像差测量本底噪声 RMS（支撑 0.40 nm RMS 闭环） [注 5-2]"),
        ("5.1.14", "PARIS 双卡盘匹配残余偏置 X (SYCO/LOCO)", "≤ 0.25 nm", "启用 SYCO/LOCO 跨卡盘参考匹配后，卡盘 1 vs 卡盘 2 低阶 Zernike 等效 X 偏置（Ref100） [注 5-2]"),
        ("5.1.15", "PARIS 双卡盘匹配残余偏置 Y (SYCO/LOCO)", "≤ 0.25 nm", "同上，启用 SYCO/LOCO 后双卡盘低阶 Zernike 等效 Y 偏置 [注 5-2]"),
    ]

    ch5_html = f"""
    <p>本章规定 <strong>TIS（6 kHz 透射空间像基准）</strong> 与 <strong>PARIS（7 点并行空间像传感器）</strong> 的验收规格，直接闭环 <strong>L1-S2</strong> 掩模对准（单层 0.470 nm / 两层 0.665 nm）、<strong>L1-S7</strong> 双卡盘差（ΔC2C ≤ 0.48 nm），并为物镜波前与掩模热前馈（RHC）提供在机反馈。<strong>关于仅设 T1 的分级结论</strong>：TIS 与 PARIS 在物理上必须依托真实 193 nm 曝光光源、投影物镜与 E 侧工件台构成完整空间像光路，不存在脱离曝光光学链路的独立二级模拟网格动作，因此在子系统级<strong>单设 T1（E 侧在机光学基准本体与重复性验收）即可闭环</strong>，通过后直接支撑整机 T3 实曝。</p>

    <h2>5.1 T1 验收项目：E 侧 193 nm 在机空间像基准本体与重复性验收</h2>
    {render_spec_table(tis_paris_t1_rows)}

    <h2>5.2 复杂标记项工程解释与跨系统供数边界</h2>
    <ul class="note-list">
      <li><strong>[注 5-1] 浸没超纯水（UPW）流量对 TIS 重复性的隐蔽耦合：</strong>Overlay3 报告 143（§4.2.1）援引实测文献（Ref164 Fig. 4–5）指出，浸没头供回水流量波动不仅改变水膜温度折射率，还会通过液膜剪切微压差直接调制 TIS 在 X/Y/Z 三个方向的双台测位重复性。因此 TIS 验收必须在真实湿区浸没供水条件下进行，并增加流量工作窗扫频核验（5.1.07–5.1.09）。</li>
      <li><strong>[注 5-2] PARIS 7 点并行架构与 SYCO/LOCO 双卡盘匹配：</strong>NXT:1965Ci 配备沿 26 mm 狭缝分布的 7 点并行空间像传感器 PARIS，公开规格掩模对准重复性 < 0.50 nm（Ref066 §3.4；Ref011 实测 0.43 nm），支持每片 3 扫（1 次物镜热态监测 + 2 排掩模对准，Ref066 Fig. 6）。同时，Ref100 Fig. 9 揭示双卡盘切换时若未开启 SYCO/LOCO 跨卡盘参考匹配，会诱发随卡盘重复的低阶 Zernike 偏置（K7/K12/K13），故 5.1.14–5.1.15 将双卡盘残余偏置纳入 T1 必查项。</li>
    </ul>
    """
    chapters.append({
        "num": 5, "id": "ch-5",
        "title": "第 5 章　TIS + PARIS（E 侧透射与 7 点并行空间像子系统）",
        "toc_title": "第 5 章　TIS + PARIS（E 侧透射与 7 点并行空间像子系统）",
        "sections": [
            ("5.1 T1 验收项目：E 侧 193 nm 在机空间像基准本体与重复性验收", None),
            ("5.2 复杂标记项工程解释与跨系统供数边界", None),
        ],
        "html": ch5_html,
    })

    # -------------------------------------------------------------------------
    # CHAPTER 6: Lens (193 nm / NA 1.35 Projection Optics)
    #   - Odd Zernike Z5-Z64 ALL 30 INDIVIDUAL TERMS (NO X/Y MERGING!)
    #   - Lens-iHOPC Range & Precision ALL INDIVIDUAL ROWS + K20 Boundary
    # -------------------------------------------------------------------------
    odd_z_pairs = [
        ("Z7",  "一阶 X 向彗差 (3,1) 1θ Coma",       0.3536, 0.950, 0.21, 0.0742, 0.199),
        ("Z8",  "一阶 Y 向彗差 (3,1) 1θ Coma",       0.3536, 0.950, 0.21, 0.0742, 0.199),
        ("Z10", "一阶 X 向三叶草 (3,3) 3θ Trefoil",  0.3536, 0.910, 0.19, 0.0672, 0.173),
        ("Z11", "一阶 Y 向三叶草 (3,3) 3θ Trefoil",  0.3536, 0.910, 0.19, 0.0672, 0.173),
        ("Z14", "二阶 X 向彗差 (5,1) 1θ Coma",       0.2887, 0.700, 0.21, 0.0606, 0.147),
        ("Z15", "二阶 Y 向彗差 (5,1) 1θ Coma",       0.2887, 0.700, 0.21, 0.0606, 0.147),
        ("Z19", "二阶 X 向三叶草 (5,3) 3θ Trefoil",  0.2887, 0.550, 0.24, 0.0693, 0.132),
        ("Z20", "二阶 Y 向三叶草 (5,3) 3θ Trefoil",  0.2887, 0.550, 0.24, 0.0693, 0.132),
        ("Z23", "三阶 X 向彗差 (7,1) 1θ Coma",       0.2500, 0.275, 0.28, 0.0700, 0.077),
        ("Z24", "三阶 Y 向彗差 (7,1) 1θ Coma",       0.2500, 0.275, 0.28, 0.0700, 0.077),
        ("Z26", "一阶 X 向五叶草 (5,5) 5θ Pentafoil", 0.2887, 0.843, 0.19, 0.0548, 0.160),
        ("Z27", "一阶 Y 向五叶草 (5,5) 5θ Pentafoil", 0.2887, 0.843, 0.19, 0.0548, 0.160),
        ("Z30", "三阶 X 向三叶草 (7,3) 3θ Trefoil",  0.2500, 0.462, 0.26, 0.0650, 0.120),
        ("Z31", "三阶 Y 向三叶草 (7,3) 3θ Trefoil",  0.2500, 0.462, 0.26, 0.0650, 0.120),
        ("Z34", "四阶 X 向彗差 (9,1) 1θ Coma",       0.2236, 0.156, 0.36, 0.0805, 0.056),
        ("Z35", "四阶 Y 向彗差 (9,1) 1θ Coma",       0.2236, 0.156, 0.36, 0.0805, 0.056),
        ("Z39", "二阶 X 向五叶草 (7,5) 5θ Pentafoil", 0.2500, 0.367, 0.26, 0.0650, 0.095),
        ("Z40", "二阶 Y 向五叶草 (7,5) 5θ Pentafoil", 0.2500, 0.367, 0.26, 0.0650, 0.095),
        ("Z43", "四阶 X 向三叶草 (9,3) 3θ Trefoil",  0.2236, 0.138, 0.36, 0.0805, 0.050),
        ("Z44", "四阶 Y 向三叶草 (9,3) 3θ Trefoil",  0.2236, 0.138, 0.36, 0.0805, 0.050),
        ("Z47", "五阶 X 向彗差 (11,1) 1θ Coma",      0.2041, 0.097, 0.42, 0.0857, 0.041),
        ("Z48", "五阶 Y 向彗差 (11,1) 1θ Coma",      0.2041, 0.097, 0.42, 0.0857, 0.041),
        ("Z50", "一阶 X 向七叶草 (7,7) 7θ Heptafoil", 0.2500, 0.320, 0.28, 0.0700, 0.090),
        ("Z51", "一阶 Y 向七叶草 (7,7) 7θ Heptafoil", 0.2500, 0.320, 0.28, 0.0700, 0.090),
        ("Z54", "三阶 X 向五叶草 (9,5) 5θ Pentafoil", 0.2236, 0.312, 0.30, 0.0671, 0.094),
        ("Z55", "三阶 Y 向五叶草 (9,5) 5θ Pentafoil", 0.2236, 0.312, 0.30, 0.0671, 0.094),
        ("Z58", "五阶 X 向三叶草 (11,3) 3θ Trefoil", 0.2041, 0.090, 0.42, 0.0857, 0.038),
        ("Z59", "五阶 Y 向三叶草 (11,3) 3θ Trefoil", 0.2041, 0.090, 0.42, 0.0857, 0.038),
        ("Z62", "六阶 X 向彗差 (13,1) 1θ Coma",      0.1890, 0.088, 0.48, 0.0907, 0.042),
        ("Z63", "六阶 Y 向彗差 (13,1) 1θ Coma",      0.1890, 0.088, 0.48, 0.0907, 0.042),
    ]
    lens_z_rows = []
    for k, (zcode, desc, rms_c, sens, f_lim, rms_v, ovl_v) in enumerate(odd_z_pairs, 1):
        lens_z_rows.append((
            f"6.1.{k:02d}",
            f"Odd Zernike {zcode} 调节精度（{desc}）",
            f"≤ {f_lim:.2f} nm (Fringe)",
            f"193 nm 出厂相移干涉仪全视场测量；等效 RMS ≤ {rms_v:.4f} nm，跨照明套刻贡献 {ovl_v:.3f} nm [注 6-1]"
        ))
    lens_z_rows.extend([
        ("6.1.31", "全瞳 30 项奇像差总合成 RMS（Z5–Z64）", "≤ 0.400 nm RMS", "193 nm 波长下 30 项 Fringe 系数按 RMS 系数平方和开方全瞳合成（单轴 1.196 nm Fringe） [注 6-1]"),
        ("6.1.32", "全阶 X 向彗差合成 RMS（Z7/14/23/34/47/62）", "≤ 0.190 nm RMS", "1θ 奇像差 X 向全阶彗差 RMS 合成上限（对接 FlexWave + PARIS 实测能力） [注 6-1]"),
        ("6.1.33", "全阶 Y 向彗差合成 RMS（Z8/15/24/35/48/63）", "≤ 0.190 nm RMS", "1θ 奇像差 Y 向全阶彗差 RMS 合成上限 [注 6-1]"),
    ])

    lens_ihopc_t1_rows = [
        ("6.2.01", "Lens-iHOPC K3 [dx(x)] 硬件总调节范围", "±150 ~ ±250 nm/cm", "即 ±15 ~ ±25 ppm（1 ppm = 10 nm/cm），含气压/温漂/镜头热与出厂匹配总余量 [注 6-2]"),
        ("6.2.02", "Lens-iHOPC K3 [dx(x)] 用户工艺调节范围", "±50 ~ ±100 nm/cm", "即 ±5 ~ ±10 ppm，开放给产线 APC 日常场内沿狭缝缩放调节的安全工作行程 [注 6-2]"),
        ("6.2.03", "Lens-iHOPC K3 [dx(x)] 调节残差精度", "≤ 0.120 nm/cm", "场角误差 0.156 nm（a=1.30 cm）；单向重复 ≤ 0.042 / 滞回 ≤ 0.030 nm/cm，分 4/15 双档核验 [注 6-2]"),
        ("6.2.04", "Lens-iHOPC K7 [dx(x²)] 补偿调节范围", "±10.0 nm/cm²", "沿狭缝 X 向二次拉伸静态镜片操纵器用户可用调节范围 [注 6-2]"),
        ("6.2.05", "Lens-iHOPC K7 [dx(x²)] 调节残差精度", "≤ 0.092 nm/cm²", "场角误差 0.155 nm（a²=1.69 cm²）；单向重复 ≤ 0.032 / 滞回 ≤ 0.023 nm/cm² [注 6-2]"),
        ("6.2.06", "Lens-iHOPC K12 [dy(x²)] 补偿调节范围", "±10.0 nm/cm²", "沿狭缝 Y 向弓形弯曲静态镜片操纵器用户可用调节范围 [注 6-2]"),
        ("6.2.07", "Lens-iHOPC K12 [dy(x²)] 调节残差精度", "≤ 0.092 nm/cm²", "场角误差 0.155 nm；单向重复 ≤ 0.032 / 滞回 ≤ 0.023 nm/cm² [注 6-2]"),
        ("6.2.08", "Lens-iHOPC K13 [dx(x³)] 补偿调节范围", "±6.0 nm/cm³", "沿狭缝 X 向三次 S 弯静态镜片操纵器用户可用调节范围 [注 6-2]"),
        ("6.2.09", "Lens-iHOPC K13 [dx(x³)] 调节残差精度", "≤ 0.070 nm/cm³", "场角误差 0.154 nm（a³=2.197 cm³）；单向重复 ≤ 0.025 / 滞回 ≤ 0.018 nm/cm³ [注 6-2]"),
        ("6.2.10", "Lens-iHOPC K9 [dx(xy)] 动态调节范围", "±8.0 nm/cm²", "扫描中同步动态梯形扩张镜片操纵器可用调节范围 [注 6-2]"),
        ("6.2.11", "Lens-iHOPC K9 [dx(xy)] 调节残差精度", "≤ 0.072 nm/cm²", "场角误差 0.154 nm（ab=2.145 cm²）；单向重复 ≤ 0.025 / 滞回 ≤ 0.018 nm/cm² [注 6-2]"),
        ("6.2.12", "Lens-iHOPC K15 [dx(x²y)] 动态调节范围", "±4.0 nm/cm³", "扫描中同步动态高阶枕/桶形畸变镜片操纵器可用调节范围 [注 6-2]"),
        ("6.2.13", "Lens-iHOPC K15 [dx(x²y)] 调节残差精度", "≤ 0.054 nm/cm³", "场角误差 0.151 nm（a²b=2.789 cm³）；单向重复 ≤ 0.019 / 滞回 ≤ 0.014 nm/cm³ [注 6-2]"),
        ("6.2.14", "Lens-iHOPC K17 [dx(xy²)] 动态调节范围", "±4.0 nm/cm³", "扫描中逐场掩模热胀演进（RefN7）镜片操纵器可用调节范围 [注 6-2]"),
        ("6.2.15", "Lens-iHOPC K17 [dx(xy²)] 调节残差精度", "≤ 0.042 nm/cm³", "场角误差 0.149 nm（ab²=3.539 cm³）；单向重复 ≤ 0.015 / 滞回 ≤ 0.011 nm/cm³ [注 6-2]"),
        ("6.2.16", "Lens-iHOPC K18 [dy(yx²)] 动态调节范围", "±4.0 nm/cm³", "扫描中掩模热主修正（Ref016）镜片操纵器可用调节范围 [注 6-2]"),
        ("6.2.17", "Lens-iHOPC K18 [dy(yx²)] 调节残差精度", "≤ 0.054 nm/cm³", "场角误差 0.151 nm；单向重复 ≤ 0.019 / 滞回 ≤ 0.014 nm/cm³ [注 6-2]"),
        ("6.2.18", "K20 [dy(x³)] 出厂静态指纹残差（架构边界）", "≤ 0.18 nm/cm³", "NXT:1965Ci 不配 K20 主动操纵器（至 NXT:2050i 开放），仅出厂静态管控并归入 MMO-M2 [注 6-2]"),
        ("6.2.19", "操纵器最小分辨率步长", "≤ 各 K 项精度 × 1/10", "离线干涉仪逐阶梯微步激励，验证无明显爬行或量化跳阶 [注 6-2]"),
        ("6.2.20", "操纵器单向定位重复性", "≤ 各 K 项精度 × 35%", "同一方向重复趋近目标指令 ≥ 20 次，干涉仪测实得畸变离散度 [注 6-2]"),
        ("6.2.21", "操纵器双向滞回（死区）", "≤ 各 K 项精度 × 25%", "正反两个方向逼近同一目标指令的稳态差值（考核机构背隙与柔性滞回） [注 6-2]"),
        ("6.2.22", "K3 镜片机械响应整定时间", "≤ 20 ms", "场间/片间下发 K3 阶跃指令至镜片到位稳定耗时"),
        ("6.2.23", "K3 激光波长微调响应时间", "< 1 ms", "通过 6 kHz 激光器中心波长微调实现高速精细缩放修正的响应耗时"),
        ("6.2.24", "K7 静态操纵器响应整定时间", "≤ 40 ms", "场间/片间下发 K7 阶跃指令至镜片稳定到位耗时"),
        ("6.2.25", "K12 静态操纵器响应整定时间", "≤ 40 ms", "场间/片间下发 K12 阶跃指令至镜片稳定到位耗时"),
        ("6.2.26", "K13 静态操纵器响应整定时间", "≤ 50 ms", "场间/片间下发 K13 阶跃指令至镜片稳定到位耗时"),
    ]

    lens_t2_rows = [
        ("6.3.01", "Lens-iHOPC 多参联合行程占用率", "≤ 80%", "装机满热与跨机匹配典型联合指令下发 8 项 K 参数，任一镜片执行器不触机械限位 [注 6-2]"),
        ("6.3.02", "Lens-iHOPC 跨项串扰抑制比", "≤ 目标项精度 × 30%", "单独阶跃任一 K 参数至典型工作点，由 PARIS 7 点测其余非目标 K 项伴生偏移 [注 6-2]"),
        ("6.3.03", "Lens-iHOPC 调节诱发焦面偏移", "≤ 1.5 nm", "全量程阶跃单 K 项期间，PARIS 监测最佳焦面同步漂移上限（典型 1.0–1.5 nm，防虚焦） [注 6-2]"),
        ("6.3.04", "Lens-iHOPC 调节诱发奇像差增量", "≤ 0.05 nm RMS", "全量程阶跃单 K 项期间，PARIS 监测 Z5–Z64 奇像差波前附加恶化量 [注 6-2]"),
        ("6.3.05", "Lens-iHOPC 动态扫描相位滞后", "≤ 0.20 ms", "K9/K15/K17/K18 在 0.70 m/s 满速扫描中与 WRS 同步触发，实测机电相位滞后 [注 6-2]"),
        ("6.3.06", "Lens-iHOPC 双档线性度误差 (SET-vs-GET)", "≤ 5.6%（典型 3.0%–5.6%）", "以 K3（4 / 15 nm/cm）等小/大两档指令阶跃，验证下发与实测比例一致性（Ref160/253） [注 6-2]"),
        ("6.3.07", "Lens-iHOPC X 向 6 项合成残差（场角）", "≤ 0.375 nm", "K3/K7/K13/K9/K15/K17 单层场角 RSS（两层 1.2× 系数为 0.450 nm，闭环 L1-S3）"),
        ("6.3.08", "Lens-iHOPC Y 向 2 项合成残差（场角）", "≤ 0.216 nm", "K12/K18 单层场角 RSS（两层 1.2× 系数为 0.260 nm，闭环 L1-S3）"),
        ("6.3.09", "物镜奇像差跨照明套刻验证 X", "≤ 0.437 nm", "193 nm 偶极 vs 环形照明切换 PARIS/实曝验证，单轴 X 套刻贡献（2D Abbe 仿真 0.388 nm） [注 6-1]"),
        ("6.3.10", "物镜奇像差跨照明套刻验证 Y", "≤ 0.437 nm", "同上，单轴 Y 跨照明套刻贡献验证 [注 6-1]"),
    ]

    ch6_html = f"""
    <p>本章规定 <strong>Lens（193 nm / NA 1.35 折反式投影物镜）</strong> 的验收规格，直接闭环 <strong>L1-S3</strong>（两层 1× 预算 X 0.667 nm / Y 0.557 nm，占 Ref009 六域方差 11.99%）并支撑跨机光学匹配 <strong>L1-M2</strong>。验收聚焦两大核心指标体系：① <strong>Odd aberration Zernike 系数（Z5–Z64 全 30 项，193 nm 波长，Fringe 系数单位 nm）的调节精度</strong>；② <strong>Lens-iHOPC 8 项激活 K 参数（+ K20 静态边界）的补偿调节范围与调节精度</strong>，按 <strong>T1（出厂干涉仪本体）</strong> 与 <strong>T2（装机 PARIS 闭环与动态联试）</strong> 分级放行。</p>

    <h2>6.1 T1 验收项目：出厂干涉仪 Odd Zernike 精度与 Lens-iHOPC 调节范围/精度</h2>
    <div class="tbl-sub">表 6-1A：投影物镜 Odd Zernike（Z5–Z64 全 30 项，波长 193 nm，Fringe 系数单位 nm）调节精度</div>
    {render_spec_table(lens_z_rows)}

    <div class="tbl-sub">表 6-1B：Lens-iHOPC 补偿调节范围、K 参数调节精度与操纵器单件特性</div>
    {render_spec_table(lens_ihopc_t1_rows)}

    <h2>6.2 T2 验收项目：装机 PARIS 波前闭环、8 维耦合与跨照明套刻验证</h2>
    {render_spec_table(lens_t2_rows)}

    <h2>6.3 复杂标记项工程解释与机理图解</h2>
    <ul class="note-list">
      <li><strong>[注 6-1] Odd Zernike 奇像差（193 nm Fringe 系数）向跨照明套刻的物理传递（见图 6-1a）：</strong>物镜波前中的奇对称项（1θ 彗差、3θ 三叶草、5θ 五叶草、7θ 七叶草，Z5–Z64 共 15 对 = 30 项）会使精细光刻图形发生水平平移；当两层曝光采用不同照明模式（如偶极切换环形）时，灵敏度差 ΔS_j 将奇像差直接转化为跨照明套刻误差。本表以 <strong>193 nm 波长、Fringe Zernike 系数（单位 nm）</strong> 逐项定限，经 2D Abbe 仿真与 IBM/ASML 实证表（RefN6 Table 4，Z10 灵敏度实测 −0.88 与仿真 0.905 偏差仅 2.8%）双核验，30 项全瞳总和 ≤ 0.400 nm RMS，跨照明单轴套刻包络 ≤ 0.437 nm（Abbe 实算 0.388 nm），完全匹配 FlexWave + PARIS 真实工程能力（Ref024, Ref066）。</li>
      <li><strong>[注 6-2] Lens-iHOPC 量程口径、K20 边界与 8 维综合体检体系（见图 6-1b）：</strong>沿 26 mm 狭缝方向（x）的缩放、弓弯与三次畸变无法靠工件台补偿，须由物镜内部可动镜片与激光波长微调（K3/K7/K12/K13 静态 + K9/K15/K17/K18 扫描动态）拉正。其中 K3 硬件总行程 ±15–25 ppm（±150–250 nm/cm）须兼顾气压/热漂/出厂匹配，用户日常工艺开放 ±5–10 ppm（±50–100 nm/cm）；K20（dy(x³)）在 NXT:1965Ci 上无独立场平面操纵器，仅做出厂静态指纹管控（≤ 0.18 nm/cm³）。验收须逐项通过 <strong>8 维体检</strong>：联合行程占用 ≤ 80%、最小步长 ≤ 1/10、单向重复 ≤ 35%、双向滞回 ≤ 25%、跨项串扰 ≤ 30%、诱发焦面 ≤ 1.5 nm、诱发奇像差 ≤ 0.05 nm RMS、动态相位滞后 ≤ 0.20 ms 与双档 SET-vs-GET 线性度 3.0%–5.6%。</li>
    </ul>

    <div class="fig-box">
      <img src="{figs['fig6_1'].as_uri()}" alt="图6-1 Odd Zernike与Lens-iHOPC场角残差"/>
      <div class="fig-cap">图 6-1：(a) 投影物镜 Odd Zernike 30 项（193 nm Fringe）精度限值与跨照明套刻贡献；(b) Lens-iHOPC 8 项场角残差与 K20 边界</div>
    </div>
    """
    chapters.append({
        "num": 6, "id": "ch-6",
        "title": "第 6 章　Lens（193 nm / NA 1.35 投影物镜子系统）",
        "toc_title": "第 6 章　Lens（193 nm / NA 1.35 投影物镜子系统）",
        "sections": [
            ("6.1 T1 验收项目：Odd Zernike 30 项精度与 Lens-iHOPC 范围/精度", None),
            ("6.2 T2 验收项目：装机 PARIS 闭环、8 维耦合与跨照明套刻验证", None),
            ("6.3 复杂标记项工程解释与机理图解", None),
        ],
        "html": ch6_html,
    })

    # -------------------------------------------------------------------------
    # CHAPTER 7: References
    # -------------------------------------------------------------------------
    refs = [
        ("ASML Official Product Specification. <em>TWINSCAN NXT:1965Ci</em> (193 nm, NA 1.35, DCO ≤ 2.5 nm, MMO ≤ 4.5 nm, ≥ 250 wph, FlexRay, PARIS). https://www.asml.com"),
        ("Castenmiller, T., van de Mast, F., de Kort, T., et al. (2010). Towards ultimate optical lithography with NXT:1950i dual stage immersion platform. <em>Proc. SPIE</em> 7640, 76401N. DOI: 10.1117/12.847025 [Ref009 Fig. 3/4/5/7/10]."),
        ("de Boeij, W., et al. (2013). Extending immersion lithography down to 1x nm production nodes (NXT:1960Bi/1965Ci/1970Ci, PARIS RA < 0.50 nm, ceramic WS MAz 4 nm, 50 μm warp 1.0 nm). <em>Proc. SPIE</em> 8683, 86831L. DOI: 10.1117/12.2021397 [Ref066]."),
        ("Freriks, H., Heemels, W. P. M. H., Muller, G., & Sandee, J. (2006). On the systematic use of budget-based design. <em>INCOSE International Symposium</em>, 16(1), 1072–1086. DOI: 10.1002/j.2334-5837.2006.tb02781.x [Ref146 Fig. 3 / §2.4 / §3.3 / §4.5]."),
        ("Butler, H. (2011). Position control in lithographic equipment: an enabler for current-day chip manufacturing. <em>IEEE Control Systems Magazine</em>, 31(5), 28–47. DOI: 10.1109/MCS.2011.941653 [Ref094]."),
        ("Evers, E., van de Wal, M., & Oomen, T. (2019). Beyond decentralized wafer/reticle stage control design: A double-Youla approach for enhancing synchronized motion. <em>Control Engineering Practice</em>, 83, 21–32. DOI: 10.1016/j.conengprac.2018.10.011 [Ref075 Table 1]."),
        ("Heertjes, M., et al. (2024). Frequency-domain MA/MSD filtering theorems and exposure window analysis for wafer scanners. <em>Proc. IEEE European Control Conference (ECC 2024)</em>. DOI: 10.23919/ECC64448.2024.10591183 [RefN8]."),
        ("ASML US Patent 6,373,072 B1 (2002). Lithographic apparatus with synchronized reticle stage following wafer stage tracking error [S14]; Nikon US Patent App. 2012/0319637 A1 (WS master / RS slave synch target filter) [S12]."),
        ("Carl Zeiss SMT US Patent App. 2008/0174858 A1, Table 3 (NA = 1.35 catadioptric projection lens, 26 × 5.5 mm image field slit) [RefN1]; ASML ME3 Official Training Manual <em>12-TT-L3-L3-ME</em> (p. 70, 22 mm reticle slit)."),
        ("van der Schaar, M., et al. (2011). Gridplate 7-day stability (< 0.20 nm) and immersion metrology performance on TWINSCAN NXT. <em>Proc. SPIE</em> 7973. DOI: 10.1117/12.814254 [Ref062 Fig. 11]."),
        ("den Boef, A., et al. (2016). Optical wafer metrology sensors for process-robust CD and overlay control (SMASH/ORION static repeatability 0.15–0.25 / 0.25–0.50 nm). <em>Proc. SPIE</em> 9780. DOI: 10.1117/12.2220589 [Ref015 Fig. 10]."),
        ("Menchtchikov, B., Socha, R., Zheng, C., et al. (2018). Reduction in overlay error from mark asymmetry using simulation and measurement based optimal color weighting (OCW) and WAMM. <em>Proc. SPIE</em> 10587, 105870C. DOI: 10.1117/12.2297493 [Ref252]."),
        ("Scan-up/scan-down (SUSD) direction aliasing and HOWA balanced wafer alignment sampling (> 3.5 nm Gy20 mitigation). <em>Proc. SPIE</em> 9052 (2014). DOI: 10.1117/12.916483 [Ref123]."),
        ("IBM / ASML (2012). Cross-illumination odd Zernike overlay sensitivity verification (Z10 = −0.88 Table 4) and high-transmission lens heating. <em>Proc. SPIE</em> 8326 [RefN6]."),
        ("Zeiss / ASML (2014). High-order intrafield overlay control (19-parameter iHOPC evolution, 13×19 multi-shift calibration, and 5-scanner MMO). <em>Journal of Micro/Nanolithography, MEMS, and MOEMS (JM3)</em>, 13(1), 011006. DOI: 10.1117/1.JMM.13.1.011006 [RefN7]."),
        ("ASML / Zeiss (2010–2020). Reticle clamping micro-slip, segmented leaf-spring clamp (JP 5,809,458 B2), Pellicle dynamic scan residual [Ref098, Ref104], WT–MB long-burl compliant mount (US 8,269,949 B2), UPW flow–TIS coupling [Ref164], SYCO/LOCO dual-chuck matching [Ref100], Lens-iHOPC SET-vs-GET linearity [Ref160, Ref253], and K20 field-plane manipulator boundary [Ref254]."),
        ("OpticsPan/OV4 仓库正式基准文档：<em>NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v2.md</em> 与 <em>ENC_AA_WS-RS重复性与分级验收专项答复_v1.md</em>（https://github.com/OpticsPan/OV4/tree/main）。"),
    ]
    ref_items = "".join(f"<li>{r}</li>" for r in refs)
    ch7_html = f"""
    <p>本规格需求书全部物理机理、实测锚点与工程分配均严格溯源至以下一手论文、专利、原厂产品规格及 OV4 仓库主干文档：</p>
    <ol class="ref-list">{ref_items}</ol>
    """
    chapters.append({
        "num": 7, "id": "ch-7",
        "title": "第 7 章　参考文献与数据来源汇总",
        "toc_title": "第 7 章　参考文献与数据来源汇总",
        "sections": [],
        "html": ch7_html,
    })

    return chapters


# =============================================================================
# 3. HTML/CSS COMPOSER (EXACT SIMSUN 9pt + TIMES NEW ROMAN 9pt + ATTACHED STYLE)
# =============================================================================
CSS = r"""
@page {
  size: A4 portrait;
  margin: 18mm 14mm 17mm 14mm;
  @top-left {
    content: "OpticsPan/OV4 · ASML NXT:1965Ci 六大核心子系统套刻规格需求书";
    font-family: "Times New Roman", "SimSun", "宋体", serif;
    font-size: 8pt;
    color: #5C6F80;
    border-bottom: 0.5pt solid #D4DFE8;
    padding-bottom: 3pt;
    width: 100%;
    vertical-align: bottom;
    margin-bottom: 5pt;
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

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  line-height: 1.52;
  color: #1A2B3C;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

/* ---- COVER PAGE (Mirroring Attached PDF Page 1) ---- */
.cover-page {
  page-break-after: always;
}

.hero-banner {
  background: linear-gradient(135deg, #10374C 0%, #174F6C 60%, #1B5E7A 100%);
  color: #FFFFFF;
  border-radius: 7pt;
  padding: 13pt 18pt 11pt 18pt;
  margin-bottom: 8pt;
}

.hero-eyebrow {
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 8.5pt;
  letter-spacing: 0.6pt;
  color: #8BE0E8;
  font-weight: bold;
  margin-bottom: 4pt;
}

.hero-title {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 16.5pt;
  line-height: 1.28;
  font-weight: bold;
  color: #FFFFFF;
  margin: 0 0 6pt 0;
}

.hero-subtitle {
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  line-height: 1.44;
  color: #D7ECF5;
  margin: 0;
}

.meta-card {
  background: #F4F7FA;
  border: 0.8pt solid #D6E1EB;
  border-radius: 6pt;
  padding: 6.5pt 12pt;
  margin-bottom: 8pt;
}

.meta-grid {
  width: 100%;
  border-collapse: collapse;
}

.meta-grid td {
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  padding: 2pt 6pt 2pt 0;
  vertical-align: top;
  color: #243442;
}

.meta-label {
  font-weight: bold;
  color: #10374C;
}

.summary-box {
  background: #F2F8FC;
  border: 0.8pt solid #CFE0EE;
  border-left: 3.2pt solid #1B6C8A;
  border-radius: 5pt;
  padding: 7pt 11pt;
  margin-bottom: 8pt;
}

.summary-title {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 9.5pt;
  font-weight: bold;
  color: #10374C;
  margin: 0 0 3pt 0;
}

.summary-box p {
  margin: 0;
  font-size: 9pt;
  line-height: 1.46;
  text-align: justify;
}

.toc-card {
  background: #FFFFFF;
  border: 0.8pt solid #D6E1EB;
  border-radius: 6pt;
  padding: 8pt 12pt 7pt 12pt;
}

.toc-heading {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 9.5pt;
  font-weight: bold;
  color: #10374C;
  border-bottom: 1pt solid #D6E1EB;
  padding-bottom: 3.5pt;
  margin: 0 0 4pt 0;
}

.toc-table {
  width: 100%;
  border-collapse: collapse;
}

.toc-table td {
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 8.5pt;
  line-height: 1.32;
  padding: 1.35pt 0;
  border-bottom: 0.4pt dotted #E2EAF0;
}

.toc-ch td {
  font-weight: bold;
  color: #10374C;
  padding-top: 2.8pt;
}

.toc-sec td.toc-name {
  padding-left: 14pt;
  color: #364B5E;
}

.toc-pg {
  width: 34pt;
  text-align: right;
  font-weight: bold;
  color: #1B5E7A;
}

/* ---- CHAPTERS & HEADINGS ---- */
.chapter {
  page-break-before: always;
}

.chapter.first-ch {
  page-break-before: auto;
}

h1.ch-title {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 13pt;
  font-weight: bold;
  color: #10374C;
  border-bottom: 1.4pt solid #1B5E7A;
  padding-bottom: 4pt;
  margin: 0 0 7pt 0;
  break-after: avoid;
  page-break-after: avoid;
}

h2 {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 10pt;
  font-weight: bold;
  color: #0F6475;
  margin: 9pt 0 5pt 0;
  break-after: avoid;
  page-break-after: avoid;
}

.tbl-sub {
  font-family: "Times New Roman", "SimHei", "Microsoft YaHei", "SimSun", serif;
  font-size: 9pt;
  font-weight: bold;
  color: #163A59;
  margin: 6pt 0 3pt 0;
  break-after: avoid;
  page-break-after: avoid;
}

p {
  margin: 0 0 6pt 0;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  line-height: 1.54;
  text-align: justify;
}

/* ---- STRICT 4-COLUMN SPECIFICATION TABLES ---- */
table.spec-tbl {
  width: 100%;
  border-collapse: collapse;
  margin: 3pt 0 8pt 0;
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
  padding: 5pt 5pt;
  border: 0.5pt solid #2B5275;
  line-height: 1.3;
}

table.spec-tbl th:first-child {
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
  line-height: 1.38;
  padding: 3.1pt 4.8pt;
  border: 0.5pt solid #D4DFE8;
  vertical-align: top;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

td.c-idx {
  text-align: center;
  color: #334E68;
  font-weight: bold;
}

td.c-name {
  color: #102A43;
  font-weight: bold;
}

td.c-spec {
  color: #0D4F6B;
  font-weight: bold;
}

td.c-def {
  color: #243442;
}

.note-tag {
  color: #B45309;
  font-weight: bold;
}

/* ---- CALLOUTS, NOTES & FIGURES ---- */
.callout-info {
  background: #F3F8FC;
  border: 0.7pt solid #C8DCEB;
  border-left: 3pt solid #1B6C8A;
  border-radius: 4pt;
  padding: 6.5pt 10pt;
  margin: 5pt 0 8pt 0;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  line-height: 1.5;
  break-inside: avoid;
}

ul.note-list {
  margin: 3pt 0 8pt 0;
  padding-left: 14pt;
}

ul.note-list li {
  margin-bottom: 4.5pt;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  line-height: 1.52;
  text-align: justify;
}

ol.ref-list {
  margin: 4pt 0 0 0;
  padding-left: 16pt;
}

ol.ref-list li {
  margin-bottom: 4pt;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 9pt;
  line-height: 1.48;
  word-break: break-word;
}

.fig-box {
  border: 0.7pt solid #D4DFE8;
  border-radius: 5pt;
  background: #FFFFFF;
  padding: 6pt 7pt 5pt 7pt;
  margin: 7pt 0 9pt 0;
  text-align: center;
  break-inside: avoid;
  page-break-inside: avoid;
}

.fig-box img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}

.fig-cap {
  margin-top: 4pt;
  font-family: "Times New Roman", "SimSun", "宋体", serif;
  font-size: 8.5pt;
  color: #486581;
  line-height: 1.38;
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
        for sec_title, _ in ch["sections"]:
            spg = sec_pages.get((ch["id"], sec_title), pg)
            toc_rows.append(
                f'<tr class="toc-sec"><td class="toc-name">{esc(sec_title)}</td>'
                f'<td class="toc-pg">{spg}</td></tr>'
            )

    cover = f"""
    <div class="cover-page">
      <div class="hero-banner">
        <div class="hero-eyebrow">OPTICSPAN / OV4 · 子系统套刻规格需求书</div>
        <h1 class="hero-title">ASML NXT:1965Ci 光刻机六大核心子系统<br/>套刻预算分配与分层验收规格需求书</h1>
        <p class="hero-subtitle">覆盖 WS（含 WRS 同步与 iHOPC 运动补偿）、RS、ENC、AA、TIS+PARIS 与 Lens（Odd Zernike 30 项 + iHOPC 8 项），建立严格逐项单列、T1/T2 分层放行的工程验收体系</p>
      </div>

      <div class="meta-card">
        <table class="meta-grid">
          <tr>
            <td style="width:50%"><span class="meta-label">基准仓库：</span>OpticsPan/OV4 (main)</td>
            <td style="width:50%"><span class="meta-label">对标机型：</span>ASML TWINSCAN NXT:1965Ci (SMO ≤ 2.50 nm / MMO ≤ 4.50 nm)</td>
          </tr>
          <tr>
            <td><span class="meta-label">光学与狭缝口径：</span>193 nm / NA 1.35 / 26 × 5.5 mm 狭缝 (τ = 7.857 ms)</td>
            <td><span class="meta-label">编制日期与版本：</span>2026-11-26 · 正式版 v1（宋体小五 / Times New Roman）</td>
          </tr>
        </table>
      </div>

      <div class="summary-box">
        <div class="summary-title">核心规格架构与关键工程裁决速览</div>
        <p>本规格书基于 NXT:1965Ci 整机套刻闭环（同卡盘 DCO 2.26 nm ≤ 2.50 nm、双卡盘 SMO 2.36 nm ≤ 2.50 nm、混机 MMO 4.29 nm ≤ 4.50 nm、独立焦面 FU 11.48 nm ≤ 14.0 nm），将 213 项核心验收指标全部逐轴、逐阶、逐色单列至四列标准验收表中。明确建立 T1（单件/单台本体）与 T2（装机集成/跨台联试）分级放行边界：<strong>iHOPC 11 项场内运动补偿正式划归 WRS（第 1 章 T2）</strong>；ENC 与 AA 设 T1/T2 两级；RS 与 TIS+PARIS 在子系统级单设 T1 闭环；Lens 设 T1/T2，完整单列 193 nm 波长下 Odd Zernike 全 30 项 Fringe 系数（nm）与 Lens-iHOPC 8 项 K 参数的调节范围及精度。</p>
      </div>

      <div class="toc-card">
        <div class="toc-heading">报告目录</div>
        <table class="toc-table">
          {''.join(toc_rows)}
        </table>
      </div>
    </div>
    """

    body_parts = [cover]
    for i, ch in enumerate(chapters):
        cls = "chapter first-ch" if i == 0 else "chapter"
        body_parts.append(
            f'<div class="{cls}" id="{ch["id"]}">'
            f'<h1 class="ch-title">{esc(ch["title"])}</h1>'
            f'{ch["html"]}'
            f'</div>'
        )

    return (
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        f'<title>ASML NXT:1965Ci 六大核心子系统套刻规格需求书 v1</title>'
        f'<style>{CSS}</style></head><body>'
        + "".join(body_parts)
        + '</body></html>'
    )


def find_chrome() -> Path:
    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        shutil.which("chrome"),
        shutil.which("msedge"),
    ]
    for c in candidates:
        if c and Path(c).is_file():
            return Path(c)
    raise RuntimeError("No Chrome or Edge executable found.")


def render_pdf(markup: str, work: Path, tag: str) -> Path:
    html_path = work / f"spec-{tag}.html"
    pdf_path = work / f"spec-{tag}.pdf"
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

    # Build lookup prefixes
    ch_prefixes = {f"第 {ch['num']} 章": ch for ch in chapters}
    sec_lookup = {}
    for ch in chapters:
        for st, _ in ch["sections"]:
            code = st.split()[0]  # e.g. "1.1"
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
                # Match Chapter Title (13pt)
                m_ch = re.match(r"^(第\s*\d+\s*章)", txt)
                if m_ch and max_sz >= 11.5:
                    key = re.sub(r"\s+", " ", m_ch.group(1)).replace("第", "第 ").replace("章", " 章")
                    key = re.sub(r"\s+", " ", key).strip()
                    for ch in chapters:
                        if f"第 {ch['num']} 章" == key and ch["id"] not in found_ch:
                            ch_pages[ch["id"]] = pg_num
                            toc.append([1, ch["toc_title"], pg_num])
                            found_ch.add(ch["id"])
                            break
                # Match Section Title (10pt)
                m_sec = re.match(r"^(\d+\.\d+)\s+", txt)
                if m_sec and 9.5 <= max_sz < 11.5:
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
    """Verify exact SimSun 9pt and Times New Roman 9pt usage in body/tables."""
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
    print("Body/Table 9pt font character audit:", body_fonts)
    assert any("SimSun" in k for k in body_fonts), "SimSun 9pt missing!"
    assert any("TimesNewRoman" in k for k in body_fonts), "Times New Roman 9pt missing!"


def main():
    with tempfile.TemporaryDirectory(prefix="build-", dir=WORK_ROOT, ignore_cleanup_errors=True) as td:
        work = Path(td)
        fig_dir = work / "figs"
        fig_dir.mkdir(parents=True, exist_ok=True)
        figs = generate_figures(fig_dir)

        chapters = build_chapters_data(figs)
        chapters = append_remaining_chapters(chapters, figs)

        # Pass 1: discover exact page numbers
        pdf1 = render_pdf(compose_html(chapters, {}, {}), work, "p1")
        with fitz.open(pdf1) as d1:
            ch_p1, sec_p1, _ = locate_headings(d1, chapters)

        # Pass 2: embed exact page numbers in TOC & verify zero page shift
        pdf2 = render_pdf(compose_html(chapters, ch_p1, sec_p1), work, "p2")
        with fitz.open(pdf2) as d2:
            ch_p2, sec_p2, toc = locate_headings(d2, chapters)
            assert ch_p2 == ch_p1, f"Chapter page shift: {ch_p1} -> {ch_p2}"
            audit_fonts(d2)
            d2.set_toc(toc)
            d2.set_metadata({
                "title": "ASML NXT:1965Ci 光刻机六大核心子系统套刻预算分配与分层验收规格需求书 v1",
                "subject": "NXT:1965Ci SMO<=2.50nm MMO<=4.50nm FU<=14.0nm; WS/WRS, RS, ENC, AA, TIS+PARIS, Lens T1/T2",
                "author": "OpticsPan / OV4",
            })
            OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
            d2.save(OUT_PDF, garbage=3, deflate=True)
            total_pages = len(d2)

            # Export preview PNGs for visual inspection
            prev_dir = WORK_ROOT / "preview_pages"
            if prev_dir.exists():
                shutil.rmtree(prev_dir)
            prev_dir.mkdir(parents=True, exist_ok=True)
            for p in d2:
                pix = p.get_pixmap(dpi=150)
                pix.save(prev_dir / f"page_{p.number + 1:02d}.png")

    print(f"\nPDF BUILT SUCCESSFULLY: {OUT_PDF}")
    print(f"Total pages: {total_pages} | Bookmarks: {len(toc)}")
    for ch in chapters:
        print(f"  p.{ch_p2[ch['id']]:2d}  {ch['toc_title']}")


if __name__ == "__main__":
    main()
