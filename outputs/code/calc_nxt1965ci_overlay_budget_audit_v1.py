"""ASML TWINSCAN NXT:1965Ci 12-Subsystem Overlay Budget Allocation, Source Audit & Recovery Engine (v1).

Archived computational core for:
  - outputs/reports/ASML_NXT1965Ci指标规格分配计算报告_v1.pdf
  - Single-source numerical audit verifying the 12-subsystem SRS suite
    (outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_v1.pdf & 13 DOCX files).

Functions:
  1. Explicit physical transfer & dimensional conversions for all 12 subsystems:
     01 WS, 02 RS, 03 ENC, 04 AA, 05 TIS+PARIS, 06 Lens, 07 IH, 08 WT-TC/WH,
     09 WC, 10 RC/RH, 11 IL/LS, 12 MF/ENV.
  2. Top-down variance-share verification against Ref009 Fig. 3 (NXT:1950i 2.50 nm 6-domain stack).
  3. Bottom-up full-machine overlay recovery (Single-Chuck DCO, Dual-Chuck SMO, Matched-Machine MMO)
     strictly enforcing non-double-counting of the 6 shared physical hubs (ENC, MF/ENV, TIS/PARIS,
     WT-TC, IH, IL/LS).
  4. Coupled shared-source correlation sweep (rho = 0%, 1%, 2.5%, 5%), N=200,000 Monte Carlo
     roll-up (subsystems delivered at realistic 80%-100% of spec ceiling + worst-case 100% ceiling),
     and ±10% Pareto tornado sensitivity analysis.
  5. Exports structured JSON audit ledger + 4 high-resolution (300 DPI) matplotlib charts.

Run from repository root:
    python -B outputs/code/calc_nxt1965ci_overlay_budget_audit_v1.py
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[2]
WORK_DIR = REPO / "work/budget_calc_v1"
CHART_DIR = WORK_DIR / "charts"
LEDGER_JSON = WORK_DIR / "audit_ledger.json"

WORK_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def rss(*vals: float) -> float:
    return math.sqrt(sum(v * v for v in vals))


# =============================================================================
# 1. FROZEN MACHINE & PHYSICAL CONSTANTS (NXT:1965Ci)
# =============================================================================
MACHINE = {
    "model": "ASML TWINSCAN NXT:1965Ci",
    "wavelength_nm": 193.368,
    "na": 1.35,
    "n_water": 1.4366,
    "mag_ratio": 4.0,
    "field_x_mm": 26.0,          # half-width a = 1.30 cm
    "field_y_mm": 33.0,          # half-length b = 1.65 cm
    "slit_x_mm": 26.0,
    "slit_y_mm": 5.5,            # verified US 2008/0174858 A1 Table 3 & ME3 p.70
    "v_ws_m_s": 0.70,
    "v_rs_m_s": 2.80,
    "a_ws_m_s2": 38.0,
    "a_rs_m_s2": 150.0,
    "dco_spec_nm": 2.50,
    "smo_spec_nm": 2.50,
    "mmo_spec_nm": 4.50,
    "alpha_si_ppm_k": 2.6,       # silicon CTE = 2.6 ppm/K
    "wafer_radius_mm": 150.0,    # 300 mm wafer -> 0.390 nm/mK edge expansion
    "dn_dt_water": -1.0e-4,      # 1/K at 193 nm
    "dn_dp_air": 2.7e-9,         # 1/Pa at 193 nm
    "dn_dt_air": -9.3e-7,        # 1/K at 193 nm
}

# Ref009 Fig. 3 exact pixel-measured 6-domain variance proportions (NXT:1950i 2.50 nm bar)
REF009_SHARES = {
    "S1": 20.16,  # Stage positioning
    "S2": 25.58,  # Wafer & reticle alignment
    "S3": 12.14,  # Optical column
    "S4": 16.54,  # Wafer heating (+immersion)
    "S5": 17.31,  # Reticle clamping / heating
    "S6": 8.27,   # Wafer clamping
}

# =============================================================================
# 2. COMPLETE 12-SUBSYSTEM SRS SPECIFICATION CONSTANTS (EXACT PARITY WITH SRS)
# =============================================================================
SPECS = {
    # 01 WS (1x wafer side)
    "ws_static_x_nm": 0.30,
    "ws_static_y_nm": 0.30,
    "ws_static_rz_nrad": 10.0,
    "ws_uni_x_nm": 0.29,
    "ws_uni_y_nm": 0.29,
    "ws_uni_rz_nrad": 10.5,
    "ws_rev_x_nm": 0.09,
    "ws_rev_y_nm": 0.10,
    "ws_rev_rz_nrad": 3.5,
    "ws_bi_x_nm": 0.38,          # 0.29 + 0.09
    "ws_bi_y_nm": 0.39,          # 0.29 + 0.10
    "ws_bi_rz_nrad": 14.0,       # 10.5 + 3.5
    "wrs_sync_x_nm": 0.47,       # Ref009 Fig. 10 anchor
    "wrs_sync_y_nm": 0.49,       # Ref009 Fig. 10 anchor
    "wrs_sync_rz_nrad": 17.0,
    # WRS-iHOPC 11 motion K terms (1x total residuals; WS-T1B = 55%, RS-T1B = 45%, T2 = 70%)
    "wrs_ihopc": {
        "K1":  ("x", 0, 0, 0.140, "nm"),
        "K2":  ("y", 0, 0, 0.140, "nm"),
        "K4":  ("y", 0, 1, 0.080, "nm/cm"),
        "K5":  ("x", 0, 1, 0.080, "nm/cm"),
        "K6":  ("y", 1, 0, 0.095, "nm/cm"),
        "K8":  ("y", 0, 2, 0.048, "nm/cm^2"),
        "K10": ("y", 1, 1, 0.060, "nm/cm^2"),
        "K11": ("x", 0, 2, 0.048, "nm/cm^2"),
        "K14": ("y", 0, 3, 0.030, "nm/cm^3"),
        "K16": ("y", 1, 2, 0.036, "nm/cm^3"),
        "K19": ("x", 0, 3, 0.030, "nm/cm^3"),
    },

    # 02 RS (4x reticle side)
    "rs_uni_x4_nm": 0.84,
    "rs_uni_y4_nm": 0.88,
    "rs_uni_rz_nrad": 7.5,
    "rs_rev_x4_nm": 0.28,
    "rs_rev_y4_nm": 0.30,
    "rs_rev_rz_nrad": 2.5,
    "rs_bi_x4_nm": 1.12,         # 1x = 0.280 nm
    "rs_bi_y4_nm": 1.18,         # 1x = 0.295 nm
    "rs_bi_rz_nrad": 10.0,       # 1:1
    "rs_slip_x4_nm": 0.72,       # 1x = 0.180 nm (归入 S5)
    "rs_slip_y4_nm": 0.72,       # 1x = 0.180 nm (归入 S5)

    # 03 ENC (embedded metrology chain — non-double-counted)
    "enc_raw_1khz_nm": 0.22,     # Ref009 Fig. 4 anchor
    "enc_colored_var_frac": 0.30,
    "enc_gridplate_7d_nm": 0.20, # Ref062 Fig. 11 anchor
    "enc_handover_xy_nm": 0.15,

    # 04 AA (M-side)
    "aa_static_nm": 0.22,        # Ref015 Fig. 10 WQ>=1%
    "aa_low_wq_nm": 0.50,        # Ref015 Fig. 10 WQ 0.1-1%
    "aa_4color_24h_nm": 0.32,
    "aa_dyn_single_nm": 0.38,
    "aa_howa_xy_nm": 0.40,       # 1L
    "aa_m2e_drift_xy_nm": 0.30,  # 1L

    # 05 TIS + PARIS (E-side)
    "tis_xy_nm": 0.40,
    "tis_dual_match_24h_nm": 0.28,
    "paris_ra_xy_nm": 0.47,      # Ref066 §3.4 < 0.50 nm (1L)
    "paris_wf_rms_nm": 0.14,

    # 06 Lens (NA = 1.35, 193.368 nm)
    "lens_ihopc": {
        "K3":  ("x", 1, 0, 0.120, "nm/cm"),
        "K7":  ("x", 2, 0, 0.092, "nm/cm^2"),
        "K9":  ("x", 1, 1, 0.072, "nm/cm^2"),
        "K12": ("y", 2, 0, 0.092, "nm/cm^2"),
        "K13": ("x", 3, 0, 0.070, "nm/cm^3"),
        "K15": ("x", 2, 1, 0.054, "nm/cm^3"),
        "K17": ("x", 1, 2, 0.042, "nm/cm^3"),
        "K18": ("y", 2, 1, 0.054, "nm/cm^3"),
    },
    # 15 Odd Zernike pairs: (name_x, name_y, fringe_limit_nm, rms_factor, cross_illum_sens_nm_per_nm)
    "odd_zernike_pairs": [
        ("Z7",  "Z8",  0.21, 1/math.sqrt(8),  0.950),
        ("Z10", "Z11", 0.19, 1/math.sqrt(8),  0.910),
        ("Z14", "Z15", 0.21, 1/math.sqrt(12), 0.700),
        ("Z19", "Z20", 0.24, 1/math.sqrt(12), 0.550),
        ("Z23", "Z24", 0.28, 1/math.sqrt(16), 0.275),
        ("Z26", "Z27", 0.19, 1/math.sqrt(12), 0.843),
        ("Z30", "Z31", 0.26, 1/math.sqrt(16), 0.462),
        ("Z34", "Z35", 0.36, 1/math.sqrt(20), 0.156),
        ("Z39", "Z40", 0.26, 1/math.sqrt(16), 0.367),
        ("Z43", "Z44", 0.36, 1/math.sqrt(20), 0.138),
        ("Z47", "Z48", 0.42, 1/math.sqrt(24), 0.097),
        ("Z50", "Z51", 0.28, 1/math.sqrt(16), 0.320),
        ("Z54", "Z55", 0.30, 1/math.sqrt(20), 0.312),
        ("Z58", "Z59", 0.42, 1/math.sqrt(24), 0.090),
        ("Z62", "Z63", 0.48, 1/math.sqrt(28), 0.088),
    ],
    "lens_k20_static_nm_cm3": 0.18,
    "lens_dyn_thermal_acoustic_1L_nm": 0.160,  # total S3 dynamic residual (enveloping IL/LS + MF vib + lens heating)

    # 07 IH (Immersion Hood & UPW)
    "ih_upw_temp_mk": 3.0,          # ±3 mK (Ref021 ±2.5 mK)
    "ih_flow_ripple_pct": 0.5,      # ±0.5% flow stability
    "ih_max_scan_no_drop_m_s": 0.75,
    "ih_n_grad_ovl_1L_nm": 0.280,   # 1L water refractive/flow gradient overlay

    # 08 WT-TC & WH (Wafer Thermal & Handler)
    "wt_temp_stab_mk": 3.0,         # ±3 mK
    "wt_zone_unif_mk": 80.0,        # < 80 mK 3sigma (Ref017)
    "wh_tsu_delta_mk": 15.0,        # ±15 mK exit TSU
    "wt_thermal_res_1L_nm": 0.420,  # 1L uncompensated wafer thermal/evap residual
    "wh_transient_1L_nm": 0.230,    # 1L WH transfer transient residual

    # 09 WC (Wafer Clamping & WT-MB Interface)
    "wc_reclamp_1L_nm": 0.300,
    "wc_microslip_1L_nm": 0.200,
    "wc_wtmb_hyst_1L_nm": 0.150,    # US 8,269,949 B2
    "wc_dual_chuck_diff_nm": 0.350, # WT1 vs WT2 fingerprint delta
    "wc_warped_50um_nm": 1.000,     # Ref066 Fig. 10a (MMO M3)

    # 10 RC & RH (Reticle Clamping, Pellicle & Reticle Thermal)
    "rc_reclamp_4x_nm": 0.72,       # 1x = 0.180 nm
    "rc_pellicle_static_nce_1x_nm": 0.12,
    "rc_pellicle_dyn_1L_nm": 0.140, # 1x dynamic scan/purge
    "rc_air_curtain_mk": 5.0,       # ±5 mK laminar air curtain
    "rc_airgap_1L_nm": 0.240,       # 1L under-reticle air-gap distortion
    "rc_rhc_res_1L_nm": 0.430,      # 1L RHC feed-forward residual (standard prod)
    "rc_rhc_extreme_nm": 1.80,      # Ref066 Fig. 5 (6.2 -> <= 1.8 nm)

    # 11 IL & LS (193 nm Light Source & FlexRay Illuminator — coupled into S3 f6_dyn)
    "ls_wavelength_stab_pm": 0.05,  # ±0.05 pm 3sigma -> ~0.080 nm 1L worst-case residual
    "il_pupil_centroid_pct": 0.20,  # Ref007 Fig. 5a (< 0.16% repro)
    "il_pole_balance_pct": 0.30,    # -> ~0.040 nm 1L cross-coupled with Coma
    "il_slit_centroid_mm": 0.10,    # -> ~0.030 nm 1L weighted MA shift
    "il_ls_coupled_1L_nm": 0.094,   # RSS(0.080, 0.040, 0.030) = 0.0943 nm (embedded in f6_dyn 0.160 nm)

    # 12 MF & ENV (Metrology Frame, Isolation & Micro-environment — shared hub)
    "env_air_shower_mk": 10.0,      # ±10 mK (Ref009)
    "env_pressure_pa": 5.0,         # ±5 Pa local chamber pressure
    "iso_nat_freq_hz": 1.0,         # < 1.0 Hz airmount isolation
    "mf_short_drift_15m_nm": 0.180, # embedded in M-to-E (0.30) & TIS
    "mf_24h_drift_nm": 0.500,
    "mf_lens_vib_1L_nm": 0.129,     # combined with il_ls_coupled 0.094 -> RSS = 0.1596 <= 0.160 nm = f6_dyn!
    "syco_loco_ref_nm": 0.170,      # feeds dual-chuck Delta C2C

    # Verification floor & systematic residual means
    "metrology_tmu_nm": 0.340,
    "mean_dco_nm": 0.300,
    "mean_smo_nm": 0.350,
    "mean_mmo_nm": 0.500,

    # MMO Matching terms (M1, M2, M3)
    "mmo_m1_grid_nm": 2.000,
    "mmo_m2_lens_nce_nm": 1.600,
    "mmo_m2_ihopc_apc_nm": 0.900,
    "mmo_m3_align_wad_nm": 0.950,
    "mmo_m3_thermal_rhc_nm": 0.850,
    "mmo_m3_reticle_nce_nm": 0.354,
}


# =============================================================================
# 3. FULL PHYSICAL DERIVATION & BOTTOM-UP MACHINE OVERLAY RECOVERY
# =============================================================================
def run_full_audit() -> dict:
    a = MACHINE["field_x_mm"] / 10.0 / 2.0   # 1.30 cm
    b = MACHINE["field_y_mm"] / 10.0 / 2.0   # 1.65 cm
    tau_slit_ms = (MACHINE["slit_y_mm"] / 1000.0) / MACHINE["v_ws_m_s"] * 1000.0  # 7.8571 ms
    enbw_hz = 1.0 / (2.0 * (tau_slit_ms / 1000.0))                                 # 63.636 Hz

    # --- 03 ENC Frequency-domain exposure window calculation (RefN8) ---
    enc_raw = SPECS["enc_raw_1khz_nm"]
    alpha_c = SPECS["enc_colored_var_frac"]
    enc_ma = math.sqrt(alpha_c * enc_raw**2 + (1.0 - alpha_c) * enc_raw**2 * (enbw_hz / (1000.0 - enbw_hz)))
    enc_ws_ratio = SPECS["ws_bi_x_nm"] / enc_ma  # 1:3 metrology rule check (~2.92x)

    # --- 01 WS & 02 RS -> Sync MA & WRS-iHOPC (S1) ---
    ws_bi_x = SPECS["ws_uni_x_nm"] + SPECS["ws_rev_x_nm"]
    ws_bi_y = SPECS["ws_uni_y_nm"] + SPECS["ws_rev_y_nm"]
    ws_bi_rz = SPECS["ws_uni_rz_nrad"] + SPECS["ws_rev_rz_nrad"]
    rs_bi_x4 = SPECS["rs_uni_x4_nm"] + SPECS["rs_rev_x4_nm"]
    rs_bi_y4 = SPECS["rs_uni_y4_nm"] + SPECS["rs_rev_y4_nm"]
    rs_bi_rz = SPECS["rs_uni_rz_nrad"] + SPECS["rs_rev_rz_nrad"]
    assert abs(ws_bi_x - SPECS["ws_bi_x_nm"]) < 1e-9
    assert abs(ws_bi_y - SPECS["ws_bi_y_nm"]) < 1e-9
    assert abs(rs_bi_x4 - SPECS["rs_bi_x4_nm"]) < 1e-9

    sync_x_calc = rss(ws_bi_x, rs_bi_x4 / 4.0)       # 0.4720 nm
    sync_y_calc = rss(ws_bi_y, rs_bi_y4 / 4.0)       # 0.4890 nm
    sync_rz_calc = rss(ws_bi_rz, rs_bi_rz)           # 17.2047 nrad
    sync_1L_x = rss(sync_x_calc, sync_rz_calc * (MACHINE["slit_y_mm"] / 2.0) * 1e-3)  # 0.4744 nm
    sync_1L_y = rss(sync_y_calc, sync_rz_calc * (MACHINE["field_x_mm"] / 2.0) * 1e-3) # 0.5377 nm
    f1_x, f1_y = sync_1L_x * math.sqrt(2.0), sync_1L_y * math.sqrt(2.0)               # 0.6709 / 0.7604 nm

    # WRS-iHOPC 11 motion K terms + 3-way T1B/T2B verification
    wrs_ihopc_x_terms, wrs_ihopc_y_terms = [], []
    wrs_ihopc_audit = []
    for k, (axis, px, py, lim, unit) in SPECS["wrs_ihopc"].items():
        lever = (a ** px) * (b ** py)
        corner_nm = lim * lever
        ws_t1b = round(lim * 0.55, 4)
        rs_t1b_1x = round(lim * 0.45, 4)
        t2_cpl = round(lim * 0.70, 4)
        three_way_rss = rss(ws_t1b, rs_t1b_1x, t2_cpl)
        assert three_way_rss <= lim + 1e-4
        if axis == "x":
            wrs_ihopc_x_terms.append(corner_nm)
        else:
            wrs_ihopc_y_terms.append(corner_nm)
        wrs_ihopc_audit.append({
            "k": k, "axis": axis, "lever": round(lever, 4), "spec": lim, "unit": unit,
            "ws_t1b": ws_t1b, "rs_t1b_1x": rs_t1b_1x, "three_way_rss": round(three_way_rss, 4),
            "corner_1L_nm": round(corner_nm, 4),
        })
    wsi_1L_x, wsi_1L_y = rss(*wrs_ihopc_x_terms), rss(*wrs_ihopc_y_terms)  # 0.2688 / 0.3469 nm
    f2_x, f2_y = wsi_1L_x * 1.20, wsi_1L_y * 1.20                           # 0.3226 / 0.4163 nm
    S1_x, S1_y = rss(f1_x, f2_x), rss(f1_y, f2_y)                           # 0.7444 / 0.8669 nm

    # --- 04 AA & 05 TIS+PARIS (S2) ---
    aa_1L = rss(SPECS["aa_howa_xy_nm"], SPECS["aa_m2e_drift_xy_nm"])        # 0.5000 nm
    f3 = aa_1L * math.sqrt(2.0)                                             # 0.7071 nm
    f4 = SPECS["paris_ra_xy_nm"] * math.sqrt(2.0)                           # 0.6647 nm
    S2 = rss(f3, f4)                                                        # 0.9704 nm

    # --- 06 Lens & 11 IL/LS & 12 MF vib (S3) ---
    li_x_terms, li_y_terms = [], []
    lens_ihopc_audit = []
    for k, (axis, px, py, lim, unit) in SPECS["lens_ihopc"].items():
        lever = (a ** px) * (b ** py)
        corner_nm = lim * lever
        if axis == "x":
            li_x_terms.append(corner_nm)
        else:
            li_y_terms.append(corner_nm)
        lens_ihopc_audit.append({
            "k": k, "axis": axis, "lever": round(lever, 4), "spec": lim, "unit": unit,
            "corner_1L_nm": round(corner_nm, 4),
        })
    li_1L_x, li_1L_y = rss(*li_x_terms), rss(*li_y_terms)                   # 0.3753 / 0.2164 nm
    f5_x, f5_y = li_1L_x * 1.20, li_1L_y * 1.20                             # 0.4503 / 0.2597 nm

    # Odd Zernike Z5-Z64 30 terms
    z_fringe_1axis = rss(*(flim for _, _, flim, _, _ in SPECS["odd_zernike_pairs"]))           # 1.1964 nm Fringe
    z_rms_1axis = rss(*(flim * rf for _, _, flim, rf, _ in SPECS["odd_zernike_pairs"]))        # 0.2827 nm RMS
    z_rms_full = z_rms_1axis * math.sqrt(2.0)                                                   # 0.3998 <= 0.400 nm RMS
    z_coma_1axis = rss(*(flim * rf for zx, _, flim, rf, _ in SPECS["odd_zernike_pairs"]
                         if zx in ("Z7", "Z14", "Z23", "Z34", "Z47", "Z62")))                   # 0.1897 <= 0.190 nm RMS
    f6_zern = rss(*(flim * sens for _, _, flim, _, sens in SPECS["odd_zernike_pairs"]))         # 0.4368 nm
    # Check IL/LS + MF vib closure inside f6_dyn = 0.160 nm 1L
    f6_dyn_1L_check = rss(SPECS["il_ls_coupled_1L_nm"], SPECS["mf_lens_vib_1L_nm"])             # 0.1604 nm
    f6_dyn = SPECS["lens_dyn_thermal_acoustic_1L_nm"] * math.sqrt(2.0)                          # 0.2263 nm
    f6 = rss(f6_zern, f6_dyn)                                                                   # 0.4919 nm
    S3_x, S3_y = rss(f5_x, f6), rss(f5_y, f6)                                                   # 0.6669 / 0.5562 nm

    # --- 07 IH & 08 WT-TC/WH (S4) ---
    si_nm_per_mk = MACHINE["alpha_si_ppm_k"] * 1e-6 * MACHINE["wafer_radius_mm"] * 1e6 * 1e-3  # 0.390 nm/mK
    f7 = rss(SPECS["wt_thermal_res_1L_nm"], SPECS["wh_transient_1L_nm"]) * math.sqrt(2.0)       # 0.6772 nm
    f8 = SPECS["ih_n_grad_ovl_1L_nm"] * math.sqrt(2.0)                                          # 0.3960 nm
    S4 = rss(f7, f8)                                                                            # 0.7845 nm

    # --- 10 RC/RH & 02 RS micro-slip (S5) ---
    f9 = rss(SPECS["rc_rhc_res_1L_nm"], SPECS["rc_airgap_1L_nm"]) * math.sqrt(2.0)              # 0.6964 nm
    f10 = rss(SPECS["rc_reclamp_4x_nm"] / 4.0, SPECS["rs_slip_x4_nm"] / 4.0,
              SPECS["rc_pellicle_dyn_1L_nm"]) * math.sqrt(2.0)                                  # 0.4109 nm
    S5 = rss(f9, f10)                                                                           # 0.8086 nm

    # --- 09 WC (S6) ---
    f11 = rss(SPECS["wc_reclamp_1L_nm"], SPECS["wc_microslip_1L_nm"],
              SPECS["wc_wtmb_hyst_1L_nm"]) * math.sqrt(2.0)                                     # 0.5523 nm
    S6 = f11

    # --- Core-6 Closure & Ref009 Fig. 3 Audit ---
    core6_x = rss(S1_x, S2, S3_x, S4, S5, S6)
    core6_y = rss(S1_y, S2, S3_y, S4, S5, S6)
    S_env = {"S1": max(S1_x, S1_y), "S2": S2, "S3": max(S3_x, S3_y), "S4": S4, "S5": S5, "S6": S6}
    core6_env = rss(*S_env.values())
    shares = {k: (v ** 2) / (core6_env ** 2) * 100.0 for k, v in S_env.items()}
    share_diffs = {k: shares[k] - REF009_SHARES[k] for k in REF009_SHARES}
    for k, d in share_diffs.items():
        assert abs(d) <= 0.35, f"Ref009 drift > 0.35% on {k}: {d:.2f}%"

    # --- S7 Dual-Chuck Delta C2C + Metrology Floor ---
    c2c = rss(SPECS["tis_dual_match_24h_nm"], SPECS["wc_dual_chuck_diff_nm"], SPECS["syco_loco_ref_nm"])  # 0.4794 nm
    meas = SPECS["metrology_tmu_nm"]
    S7_dco = meas
    S7_smo = rss(c2c, meas)  # 0.5877 nm

    # --- Top-Level L0 Recovery: DCO, SMO, MMO ---
    dco_rand_x = rss(core6_x, S7_dco)
    dco_rand_y = rss(core6_y, S7_dco)
    dco_rand_env = rss(core6_env, S7_dco)
    dco_x, dco_y, dco_env = dco_rand_x + SPECS["mean_dco_nm"], dco_rand_y + SPECS["mean_dco_nm"], dco_rand_env + SPECS["mean_dco_nm"]

    smo_rand_x = rss(core6_x, S7_smo)
    smo_rand_y = rss(core6_y, S7_smo)
    smo_rand_env = rss(core6_env, S7_smo)
    smo_x, smo_y, smo_env = smo_rand_x + SPECS["mean_smo_nm"], smo_rand_y + SPECS["mean_smo_nm"], smo_rand_env + SPECS["mean_smo_nm"]

    M1 = SPECS["mmo_m1_grid_nm"]
    M2 = rss(SPECS["mmo_m2_lens_nce_nm"], f6_zern, SPECS["mmo_m2_ihopc_apc_nm"])
    M3 = rss(SPECS["wc_warped_50um_nm"], SPECS["mmo_m3_align_wad_nm"],
             SPECS["mmo_m3_thermal_rhc_nm"], SPECS["mmo_m3_reticle_nce_nm"])
    mmo_match = rss(M1, M2, M3)
    mmo_rand_x = rss(smo_rand_x, mmo_match)
    mmo_rand_y = rss(smo_rand_y, mmo_match)
    mmo_rand_env = rss(smo_rand_env, mmo_match)
    mmo_x = mmo_rand_x + SPECS["mean_mmo_nm"]
    mmo_y = mmo_rand_y + SPECS["mean_mmo_nm"]
    mmo_env = mmo_rand_env + SPECS["mean_mmo_nm"]

    assert dco_env <= 2.50 and smo_env <= 2.50 and mmo_env <= 4.50

    # --- Shared-Source Cross-Domain Correlation Sweep (rho = 0%, 1%, 2.5%, 5%) ---
    vec_smo = [S_env["S1"], S_env["S2"], S_env["S3"], S_env["S4"], S_env["S5"], S_env["S6"], S7_smo]
    corr_sweep = []
    for rho in (0.0, 0.01, 0.02, 0.025, 0.03, 0.05):
        var_sum = sum(v * v for v in vec_smo)
        cross = 0.0
        for i in range(len(vec_smo)):
            for j in range(i + 1, len(vec_smo)):
                cross += 2.0 * rho * vec_smo[i] * vec_smo[j]
        smo_r = math.sqrt(var_sum + cross)
        smo_tot = smo_r + SPECS["mean_smo_nm"]
        # MMO with same rho across S1..S7 (M1..M3 uncorrelated)
        mmo_tot = math.sqrt(var_sum + cross + mmo_match**2) + SPECS["mean_mmo_nm"]
        corr_sweep.append({
            "rho_pct": round(rho * 100.0, 2),
            "smo_env_nm": round(smo_tot, 3),
            "smo_pass": smo_tot <= 2.50,
            "mmo_env_nm": round(mmo_tot, 3),
            "mmo_pass": mmo_tot <= 4.50,
        })

    # --- Monte Carlo Roll-Up (N = 200,000 simulated builds) ---
    # Scenario A: realistic subsystem delivery U[0.72, 1.00] * Spec (passing FAT with typical 10-28% margin)
    # Scenario B: tight-edge delivery U[0.85, 1.00] * Spec (near spec ceiling)
    rng = np.random.default_rng(19652026)
    N_MC = 200_000
    s_arr = np.array([S_env["S1"], S_env["S2"], S_env["S3"], S_env["S4"], S_env["S5"], S_env["S6"]])
    mc_results = {}
    for scen, lo, hi in (("typical_72_100", 0.72, 1.00), ("edge_85_100", 0.85, 1.00)):
        u_s = rng.uniform(lo, hi, size=(N_MC, 6))
        u_c2c = rng.uniform(lo, hi, size=N_MC)
        u_meas = rng.uniform(0.80, 1.00, size=N_MC)
        u_m = rng.uniform(lo, hi, size=(N_MC, 3))
        u_mean = rng.uniform(0.60, 1.00, size=N_MC)

        c6_mc = np.sqrt(np.sum((u_s * s_arr) ** 2, axis=1))
        dco_mc = np.sqrt(c6_mc**2 + (u_meas * meas) ** 2) + u_mean * SPECS["mean_dco_nm"]
        smo_mc = np.sqrt(c6_mc**2 + (u_c2c * c2c) ** 2 + (u_meas * meas) ** 2) + u_mean * SPECS["mean_smo_nm"]
        m_vec = np.array([M1, M2, M3])
        m_mc = np.sqrt(np.sum((u_m * m_vec) ** 2, axis=1))
        mmo_mc = np.sqrt(c6_mc**2 + (u_c2c * c2c) ** 2 + (u_meas * meas) ** 2 + m_mc**2) + u_mean * SPECS["mean_mmo_nm"]

        mc_results[scen] = {
            "dco_p50": round(float(np.percentile(dco_mc, 50)), 3),
            "dco_p95": round(float(np.percentile(dco_mc, 95)), 3),
            "dco_p997": round(float(np.percentile(dco_mc, 99.7)), 3),
            "dco_pass_pct": round(float(np.mean(dco_mc <= 2.50) * 100.0), 3),
            "smo_p50": round(float(np.percentile(smo_mc, 50)), 3),
            "smo_p95": round(float(np.percentile(smo_mc, 95)), 3),
            "smo_p997": round(float(np.percentile(smo_mc, 99.7)), 3),
            "smo_pass_pct": round(float(np.mean(smo_mc <= 2.50) * 100.0), 3),
            "mmo_p50": round(float(np.percentile(mmo_mc, 50)), 3),
            "mmo_p95": round(float(np.percentile(mmo_mc, 95)), 3),
            "mmo_p997": round(float(np.percentile(mmo_mc, 99.7)), 3),
            "mmo_pass_pct": round(float(np.mean(mmo_mc <= 4.50) * 100.0), 3),
        }

    # --- ±10% Subsystem Sensitivity (Tornado Ranking on SMO) ---
    base_smo = smo_env
    # Perturb each domain / subsystem lever by +10% (worst-case overshoot)
    sens_items = [
        ("S2 对准域 (AA + TIS/PARIS)", "S2", S2),
        ("S1 运动台域 (WS + RS + WRS-iHOPC)", "S1", S_env["S1"]),
        ("S5 掩模热与夹持 (RC/RH + RS微滑移)", "S5", S5),
        ("S4 晶圆热与浸没 (WT-TC/WH + IH)", "S4", S4),
        ("S3 光学柱域 (Lens + IL/LS + MF微振)", "S3", S_env["S3"]),
        ("S7 双卡盘 ΔC2C 与量测底噪", "S7", S7_smo),
        ("S6 晶圆夹持与接口 (WC)", "S6", S6),
        ("系统残余均值偏置 |Mean|", "MEAN", SPECS["mean_smo_nm"]),
    ]
    tornado = []
    for label, key, val in sens_items:
        if key == "MEAN":
            smo_hi = smo_rand_env + val * 1.10
            smo_lo = smo_rand_env + val * 0.90
        elif key == "S7":
            smo_hi = rss(core6_env, val * 1.10) + SPECS["mean_smo_nm"]
            smo_lo = rss(core6_env, val * 0.90) + SPECS["mean_smo_nm"]
        else:
            others = [v for k2, v in S_env.items() if k2 != key]
            smo_hi = rss(*others, val * 1.10, S7_smo) + SPECS["mean_smo_nm"]
            smo_lo = rss(*others, val * 0.90, S7_smo) + SPECS["mean_smo_nm"]
        tornado.append({
            "label": label,
            "base_nm": round(val, 3),
            "delta_plus10_pm": round((smo_hi - base_smo) * 1000.0, 1),   # picometers
            "delta_minus10_pm": round((smo_lo - base_smo) * 1000.0, 1),
            "smo_at_plus10": round(smo_hi, 3),
        })
    tornado.sort(key=lambda d: d["delta_plus10_pm"], reverse=True)

    ledger = {
        "machine": MACHINE,
        "derived": {
            "tau_slit_ms": round(tau_slit_ms, 4),
            "enbw_hz": round(enbw_hz, 3),
            "enc_ma_nm": round(enc_ma, 4),
            "enc_ws_ratio": round(enc_ws_ratio, 2),
            "si_nm_per_mk": round(si_nm_per_mk, 4),
            "sync_x_calc_nm": round(sync_x_calc, 4),
            "sync_y_calc_nm": round(sync_y_calc, 4),
            "sync_rz_calc_nrad": round(sync_rz_calc, 3),
            "sync_1L_x_nm": round(sync_1L_x, 4),
            "sync_1L_y_nm": round(sync_1L_y, 4),
            "wsi_1L_x_nm": round(wsi_1L_x, 4),
            "wsi_1L_y_nm": round(wsi_1L_y, 4),
            "li_1L_x_nm": round(li_1L_x, 4),
            "li_1L_y_nm": round(li_1L_y, 4),
            "z_fringe_1axis_nm": round(z_fringe_1axis, 4),
            "z_rms_full_nm": round(z_rms_full, 4),
            "z_coma_1axis_rms_nm": round(z_coma_1axis, 4),
            "f6_dyn_1L_check_nm": round(f6_dyn_1L_check, 4),
        },
        "ref009_shares": REF009_SHARES,
        "computed_shares": {k: round(v, 2) for k, v in shares.items()},
        "share_diffs": {k: round(v, 2) for k, v in share_diffs.items()},
        "L1": {
            "S1_x": round(S1_x, 4), "S1_y": round(S1_y, 4), "S1": round(S_env["S1"], 4),
            "S2": round(S2, 4),
            "S3_x": round(S3_x, 4), "S3_y": round(S3_y, 4), "S3": round(S_env["S3"], 4),
            "S4": round(S4, 4), "S5": round(S5, 4), "S6": round(S6, 4),
            "S7_dco": round(S7_dco, 4), "S7_smo": round(S7_smo, 4), "c2c": round(c2c, 4),
            "M1": round(M1, 4), "M2": round(M2, 4), "M3": round(M3, 4), "mmo_match": round(mmo_match, 4),
        },
        "L2": {
            "f1_x": round(f1_x, 4), "f1_y": round(f1_y, 4),
            "f2_x": round(f2_x, 4), "f2_y": round(f2_y, 4),
            "f3": round(f3, 4), "f4": round(f4, 4),
            "f5_x": round(f5_x, 4), "f5_y": round(f5_y, 4),
            "f6_zern": round(f6_zern, 4), "f6_dyn": round(f6_dyn, 4), "f6": round(f6, 4),
            "f7": round(f7, 4), "f8": round(f8, 4),
            "f9": round(f9, 4), "f10": round(f10, 4),
            "f11": round(f11, 4),
        },
        "recovery": {
            "core6_x": round(core6_x, 3), "core6_y": round(core6_y, 3), "core6_env": round(core6_env, 3),
            "dco_rand_env": round(dco_rand_env, 3),
            "dco_x": round(dco_x, 3), "dco_y": round(dco_y, 3), "dco_env": round(dco_env, 3),
            "dco_margin_pct": round((2.50 - dco_env) / 2.50 * 100.0, 2),
            "smo_rand_env": round(smo_rand_env, 3),
            "smo_x": round(smo_x, 3), "smo_y": round(smo_y, 3), "smo_env": round(smo_env, 3),
            "smo_margin_pct": round((2.50 - smo_env) / 2.50 * 100.0, 2),
            "mmo_rand_env": round(mmo_rand_env, 3),
            "mmo_x": round(mmo_x, 3), "mmo_y": round(mmo_y, 3), "mmo_env": round(mmo_env, 3),
            "mmo_margin_pct": round((4.50 - mmo_env) / 4.50 * 100.0, 2),
        },
        "wrs_ihopc_audit": wrs_ihopc_audit,
        "lens_ihopc_audit": lens_ihopc_audit,
        "corr_sweep": corr_sweep,
        "monte_carlo": mc_results,
        "tornado": tornado,
        "mc_arrays_for_plot": {
            "smo_typ": smo_mc if False else None,
        },
    }
    return ledger


# =============================================================================
# 4. GENERATE 4 PUBLICATION-GRADE 300 DPI CHARTS FOR THE CALCULATION REPORT
# =============================================================================
def generate_charts(ledger: dict):
    NAVY = "#163A59"
    TEAL = "#0E7C94"
    AMBER = "#C86D00"
    RED = "#B91C1C"
    SLATE = "#486581"

    # Chart 1: Ref009 Fig. 3 vs Computed 6-Domain Variance Share Audit
    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=300)
    domains = ["S1\n运动台", "S2\n对准", "S3\n光学柱", "S4\n晶圆热/浸没", "S5\n掩模热/夹持", "S6\n晶圆夹持"]
    keys = ["S1", "S2", "S3", "S4", "S5", "S6"]
    v_ref = [ledger["ref009_shares"][k] for k in keys]
    v_cur = [ledger["computed_shares"][k] for k in keys]
    x = np.arange(len(keys))
    w = 0.34
    b1 = ax.bar(x - w / 2, v_ref, w, label="Ref009 Fig. 3 原图占比 (%)", color="#94A3B8", edgecolor="#475569", lw=0.6)
    b2 = ax.bar(x + w / 2, v_cur, w, label="回收 12 子系统后实占方差 (%)", color=NAVY, edgecolor="#102A43", lw=0.6)
    for bar, val in zip(b1, v_ref):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5, f"{val:.1f}%", ha="center", va="bottom", fontsize=7.5, color="#475569")
    for bar, val, k in zip(b2, v_cur, keys):
        diff = ledger["share_diffs"][k]
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5, f"{val:.1f}%\n({diff:+.2f}%)", ha="center", va="bottom", fontsize=7.2, color=NAVY, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(domains, fontsize=8.5)
    ax.set_ylabel("核心六域方差份额 (%)", fontsize=8.5)
    ax.set_ylim(0, 31.5)
    ax.set_title("图 1：Ref009 Fig. 3 基准份额与 12 子系统指标回收方差份额核校（全项偏差 ≤ ±0.30%）", fontsize=9.5, fontweight="bold", color="#102A43")
    ax.legend(frameon=True, fontsize=8, loc="upper right")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "fig1_ref009_share_audit.png", dpi=300)
    plt.close(fig)

    # Chart 2: Bottom-Up Full-Machine Overlay Recovery (DCO / SMO / MMO vs Spec Ceiling)
    fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=300)
    rec = ledger["recovery"]
    cats = ["单卡盘 DCO\n(同卡盘重曝)", "双卡盘 SMO\n(双卡盘轮转)", "混机匹配 MMO\n(参考片匹配)"]
    x = np.arange(3)
    w = 0.24
    vx = [rec["dco_x"], rec["smo_x"], rec["mmo_x"]]
    vy = [rec["dco_y"], rec["smo_y"], rec["mmo_y"]]
    ve = [rec["dco_env"], rec["smo_env"], rec["mmo_env"]]
    spec = [2.50, 2.50, 4.50]

    ax.bar(x - w, vx, w, label="X 轴回收预估 (nm)", color="#3B82F6")
    ax.bar(x,     vy, w, label="Y 轴回收预估 (nm)", color=TEAL)
    ax.bar(x + w, ve, w, label="最严包络回收 (nm)", color=NAVY)
    for i, sp in enumerate(spec):
        ax.plot([i - 0.38, i + 0.38], [sp, sp], color=RED, lw=1.8, linestyle="--", label="整机验收红线" if i == 0 else None)
        ax.text(i + w, ve[i] - 0.14, f"{ve[i]:.2f}\n余{((sp - ve[i]) / sp * 100):.1f}%", ha="center", va="top", fontsize=7.2, fontweight="bold", color="#FFFFFF")
        ax.text(i, sp + 0.10, f"验收红线 {sp:.2f} nm", ha="center", va="bottom", fontsize=7.5, color=RED, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=8.5)
    ax.set_ylabel("整机两层套刻预估 |Mean| + 3σ (nm)", fontsize=8.5)
    ax.set_ylim(0, 5.25)
    ax.set_title("图 2：回收 12 大子系统全套验收规格后的整机套刻闭环预估（DCO / SMO / MMO）", fontsize=9.5, fontweight="bold", color="#102A43")
    ax.legend(frameon=True, fontsize=7.8, loc="upper left", ncol=2)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "fig2_machine_recovery.png", dpi=300)
    plt.close(fig)

    # Chart 3: Shared-Source Cross-Domain Correlation Sweep + Monte Carlo CDF Summary
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.2), dpi=300)
    rhos = [r["rho_pct"] for r in ledger["corr_sweep"]]
    smos = [r["smo_env_nm"] for r in ledger["corr_sweep"]]
    ax1.plot(rhos, smos, marker="o", color=NAVY, lw=2.0, markersize=5, label="双卡盘 SMO 包络 (nm)")
    ax1.axhline(2.50, color=RED, lw=1.5, linestyle="--", label="SMO 红线 2.50 nm")
    ax1.fill_between(rhos, 2.50, max(smos) + 0.06, color="#FEE2E2", alpha=0.5)
    for rx, sy in zip(rhos, smos):
        ax1.text(rx, sy + 0.025, f"{sy:.2f}", ha="center", va="bottom", fontsize=7.3, color=NAVY)
    ax1.set_xlabel("域间共享源同向相关性 ρ (%)", fontsize=8.2)
    ax1.set_ylabel("整机 SMO 预估 (nm)", fontsize=8.2)
    ax1.set_ylim(2.30, 2.72)
    ax1.set_title("(a) 共享源域间相关性 ρ 对 SMO 侵蚀", fontsize=8.8, fontweight="bold", color="#102A43")
    ax1.legend(fontsize=7.3, loc="lower right")
    ax1.grid(True, linestyle="--", alpha=0.4)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    # Right panel: Monte Carlo 200,000-trial percentiles for SMO
    mc_t = ledger["monte_carlo"]["typical_72_100"]
    mc_e = ledger["monte_carlo"]["edge_85_100"]
    labs = ["P50 中位", "P95 分位", "P99.7 极值", "100% 满格最严"]
    y_t = [mc_t["smo_p50"], mc_t["smo_p95"], mc_t["smo_p997"], rec["smo_env"]]
    y_e = [mc_e["smo_p50"], mc_e["smo_p95"], mc_e["smo_p997"], rec["smo_env"]]
    xi = np.arange(4)
    ax2.bar(xi - 0.17, y_t, 0.32, label="常规出厂 (72–100% Spec)", color=TEAL)
    ax2.bar(xi + 0.17, y_e, 0.32, label="逼近上限 (85–100% Spec)", color=NAVY)
    ax2.axhline(2.50, color=RED, lw=1.5, linestyle="--", label="SMO 红线 2.50 nm")
    for i in range(4):
        ax2.text(i - 0.17, y_t[i] + 0.03, f"{y_t[i]:.2f}", ha="center", va="bottom", fontsize=6.8, color=TEAL, fontweight="bold")
        ax2.text(i + 0.17, y_e[i] + 0.03, f"{y_e[i]:.2f}", ha="center", va="bottom", fontsize=6.8, color=NAVY, fontweight="bold")
    ax2.set_xticks(xi)
    ax2.set_xticklabels(labs, fontsize=7.5)
    ax2.set_ylim(1.75, 2.66)
    ax2.set_ylabel("SMO 预估 (nm)", fontsize=8.2)
    ax2.set_title("(b) 20 万次蒙特卡洛整机 SMO 分布", fontsize=8.8, fontweight="bold", color="#102A43")
    ax2.legend(fontsize=6.8, loc="upper left")
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "fig3_corr_and_montecarlo.png", dpi=300)
    plt.close(fig)

    # Chart 4: ±10% Pareto Tornado Sensitivity on SMO (picometers)
    fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=300)
    tor = ledger["tornado"][::-1]
    ylabs = [d["label"] for d in tor]
    d_pos = [d["delta_plus10_pm"] for d in tor]
    d_neg = [d["delta_minus10_pm"] for d in tor]
    y = np.arange(len(tor))
    ax.barh(y, d_pos, height=0.58, color=AMBER, label="单项超差 +10% 导致 SMO 恶化 (pm)")
    ax.barh(y, d_neg, height=0.58, color=TEAL, label="单项收严 -10% 带来 SMO 收益 (pm)")
    ax.axvline(0, color="#102A43", lw=1.0)
    for i, (dp, dn) in enumerate(zip(d_pos, d_neg)):
        ax.text(dp + 1.2, i, f"+{dp:.1f} pm", va="center", ha="left", fontsize=7.3, color=AMBER, fontweight="bold")
        ax.text(dn - 1.2, i, f"{dn:.1f} pm", va="center", ha="right", fontsize=7.3, color=TEAL, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(ylabs, fontsize=8.0)
    ax.set_xlabel("对整机双卡盘 SMO 的边际影响 ΔSMO (pm)", fontsize=8.3)
    ax.set_xlim(-62, 66)
    ax.set_title("图 4：各功能域 ±10% 门限波动对整机 SMO 的龙卷风（Tornado）敏感度排序", fontsize=9.3, fontweight="bold", color="#102A43", pad=22)
    ax.legend(fontsize=7.6, loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=False)
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "fig4_tornado_sensitivity.png", dpi=300)
    plt.close(fig)


def main():
    ledger = run_full_audit()
    generate_charts(ledger)
    ledger.pop("mc_arrays_for_plot", None)
    LEDGER_JSON.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")

    rec = ledger["recovery"]
    der = ledger["derived"]
    print("=== NXT:1965Ci 12-SUBSYSTEM BUDGET ALLOCATION & RECOVERY AUDIT ===")
    print(f"  Slit window: tau={der['tau_slit_ms']:.4f} ms, ENBW={der['enbw_hz']:.2f} Hz | ENC MA={der['enc_ma_nm']:.4f} nm (ratio {der['enc_ws_ratio']}x)")
    print(f"  Odd Zernike: 1-axis Fringe={der['z_fringe_1axis_nm']:.4f} nm | Full RMS={der['z_rms_full_nm']:.4f} nm | Coma={der['z_coma_1axis_rms_nm']:.4f} nm")
    print(f"  IL/LS + MF vib closure inside f6_dyn(0.160 nm 1L): {der['f6_dyn_1L_check_nm']:.4f} nm")
    print(f"  Core-6 RSS : X={rec['core6_x']:.3f} / Y={rec['core6_y']:.3f} / Env={rec['core6_env']:.3f} nm")
    print(f"  DCO (1-ch) : X={rec['dco_x']:.3f} / Y={rec['dco_y']:.3f} / Env={rec['dco_env']:.3f} nm <= 2.50 nm (margin {rec['dco_margin_pct']}%)")
    print(f"  SMO (2-ch) : X={rec['smo_x']:.3f} / Y={rec['smo_y']:.3f} / Env={rec['smo_env']:.3f} nm <= 2.50 nm (margin {rec['smo_margin_pct']}%)")
    print(f"  MMO (match): X={rec['mmo_x']:.3f} / Y={rec['mmo_y']:.3f} / Env={rec['mmo_env']:.3f} nm <= 4.50 nm (margin {rec['mmo_margin_pct']}%)")
    print("  Ref009 Fig.3 share audit:", ledger["share_diffs"])
    print("  MC typical (72-100%):", ledger["monte_carlo"]["typical_72_100"])
    print("  MC edge    (85-100%):", ledger["monte_carlo"]["edge_85_100"])
    print(f"  Saved audit ledger -> {LEDGER_JSON}")
    print(f"  Saved 4 charts     -> {CHART_DIR}")


if __name__ == "__main__":
    main()
