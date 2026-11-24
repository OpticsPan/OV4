import numpy as np
import math
import json

# ==============================================================================
# 1. Exact Fringe Zernike Z1..Z64 Generator & Verification
# ==============================================================================
def radial_poly(n, m, rho):
    """Exact Zernike radial polynomial R_n^m(rho)."""
    res = np.zeros_like(rho, dtype=np.float64)
    for k in range((n - m) // 2 + 1):
        c = ((-1)**k * math.factorial(n - k)) / (
            math.factorial(k)
            * math.factorial((n + m) // 2 - k)
            * math.factorial((n - m) // 2 - k)
        )
        res += c * (rho ** (n - 2 * k))
    return res

def build_fringe_zernike_table(max_j=64):
    """
    Standard Fringe (University of Arizona / ASML / Zeiss) Zernike ordering:
    Grouped by N = (n + m)/2 = 0, 1, 2, ...
    Within each N, m descends from N down to 0, with n = 2N - m.
    For m > 0: cos(m*theta) first, then sin(m*theta).
    """
    table = []
    j = 1
    N = 0
    while j <= max_j:
        for m in range(N, -1, -1):
            n = 2 * N - m
            if m == 0:
                table.append({'j': j, 'n': n, 'm': m, 'trig': '1', 'N': N})
                j += 1
                if j > max_j: break
            else:
                table.append({'j': j, 'n': n, 'm': m, 'trig': 'cos', 'N': N})
                j += 1
                if j > max_j: break
                table.append({'j': j, 'n': n, 'm': m, 'trig': 'sin', 'N': N})
                j += 1
                if j > max_j: break
        N += 1
    return table

ztable = build_fringe_zernike_table(64)
odd_z = [z for z in ztable if z['j'] >= 5 and (z['m'] % 2 == 1)]
print(f"Total Z1..Z64: {len(ztable)}, Odd Z5..Z64 count: {len(odd_z)}")
for z in odd_z:
    rms_factor = 1.0 / math.sqrt(2 * (z['n'] + 1))
    print(f"  Z{z['j']:2d}: n={z['n']:2d}, m={z['m']} ({z['trig']:3s}), RMS/Fringe={rms_factor:.4f}")

# ==============================================================================
# 2. Partially Coherent Abbe Optical Simulation (193.368 nm, NA = 1.35)
#    Exact 1D/2D dense grating & contact pattern shift sensitivity d(OVL)/d(Zj)
# ==============================================================================
LAM = 193.368  # nm
NA = 1.35

# Pupil grid (normalized coordinates fx, fy in [-1, 1], r <= 1)
N_P = 81
g = np.linspace(-1.0, 1.0, N_P)
PX, PY = np.meshgrid(g, g)
PR = np.sqrt(PX**2 + PY**2)
PTH = np.arctan2(PY, PX)
PUPIL_MASK = PR <= 1.0

def eval_fringe_z(zinfo, fx, fy):
    r = np.sqrt(fx**2 + fy**2)
    th = np.arctan2(fy, fx)
    val = radial_poly(zinfo['n'], zinfo['m'], r)
    if zinfo['trig'] == 'cos':
        val = val * np.cos(zinfo['m'] * th)
    elif zinfo['trig'] == 'sin':
        val = val * np.sin(zinfo['m'] * th)
    return val

# Define realistic illumination sources on 193nm NA=1.35 ArFi scanner
def make_source(kind):
    r = PR
    th = PTH  # radians in [-pi, pi]
    if kind == 'Conv_0.55':
        S = (r <= 0.55).astype(float)
    elif kind == 'Annular_0.65_0.90':
        S = ((r >= 0.65) & (r <= 0.90)).astype(float)
    elif kind == 'DipoleX_0.78_0.96_30deg':
        ang = np.abs(np.arctan2(np.abs(PY), np.abs(PX)))
        S = ((r >= 0.78) & (r <= 0.96) & (ang <= np.deg2rad(15.0))).astype(float)
    elif kind == 'DipoleY_0.78_0.96_30deg':
        ang = np.abs(np.arctan2(np.abs(PX), np.abs(PY)))
        S = ((r >= 0.78) & (r <= 0.96) & (ang <= np.deg2rad(15.0))).astype(float)
    elif kind == 'CQuad_0.80_0.96_30deg':
        ang_x = np.abs(np.arctan2(np.abs(PY), np.abs(PX)))
        ang_y = np.abs(np.arctan2(np.abs(PX), np.abs(PY)))
        S = ((r >= 0.80) & (r <= 0.96) & ((ang_x <= np.deg2rad(15.0)) | (ang_y <= np.deg2rad(15.0)))).astype(float)
    elif kind == 'Quasar_0.75_0.95_30deg':
        # 45 deg diagonal poles
        ang45 = np.abs(np.abs(np.arctan2(np.abs(PY), np.abs(PX))) - np.deg2rad(45.0))
        S = ((r >= 0.75) & (r <= 0.95) & (ang45 <= np.deg2rad(15.0))).astype(float)
    elif kind == 'RotDipole_21deg_0.82_0.97':
        # Rotated dipole at 21 deg (classic DRAM 6F2 active layer, cf. paper 008!)
        phi0 = np.deg2rad(21.0)
        dth1 = np.abs(np.angle(np.exp(1j * (th - phi0))))
        dth2 = np.abs(np.angle(np.exp(1j * (th - (phi0 - np.pi)))))
        S = ((r >= 0.82) & (r <= 0.97) & ((dth1 <= np.deg2rad(15.0)) | (dth2 <= np.deg2rad(15.0)))).astype(float)
    else:
        raise ValueError(kind)
    return S / np.sum(S)

def compute_1d_grating_shift_sensitivity(zinfo, source_mask, pitch_nm, angle_deg=0.0, dz_nm=1.0):
    """
    Exact Abbe imaging for 1D 1:1 binary / 6% AttPSM line-space grating of pitch P oriented with grating vector at angle_deg.
    Returns pattern centerline shift (nm) per +1 nm of Fringe Zernike amplitude along the grating vector direction (perp to lines).
    """
    # Normalized spatial frequency of +/-1st order: f1 = lambda / (NA * P)
    f1 = LAM / (NA * pitch_nm)
    ux = f1 * np.cos(np.deg2rad(angle_deg))
    uy = f1 * np.sin(np.deg2rad(angle_deg))
    # 6% AttPSM 1:1 L/S Fourier amplitudes: a0 = (1 - t)/2, a1 = (1 + t)/pi where t = sqrt(0.06) = 0.245
    t_att = math.sqrt(0.06)
    a0 = (1.0 - t_att) / 2.0
    a1 = (1.0 + t_att) / math.pi

    idx = np.argwhere(source_mask > 0)
    weights = source_mask[idx[:, 0], idx[:, 1]]
    sx = PX[idx[:, 0], idx[:, 1]]
    sy = PY[idx[:, 0], idx[:, 1]]

    # Evaluate aerial image I(u) along grating coordinate u in [-P/2, P/2]
    # Because only orders m in {-1, 0, +1} (and +/-2 if pitch large) pass through pupil:
    # I(u) = sum_s w_s * | sum_{m} a_m * P(s + m*u_vec) * exp(i*2pi/lam * W(s+m*u_vec)) * exp(i*2pi*m*u/P) |^2
    # Wait: the fundamental 1st-harmonic phase of I(u) gives the EXACT centerline shift at threshold:
    # I(u) = C0 + 2*Re(C1 * exp(i*2pi*u/P)) + 2*Re(C2 * exp(i*4pi*u/P)) ...
    # Shift dx = - (P / (2*pi)) * arg(C1)  (when I(u) peak/trough is at u=0 for W=0)!
    # Let's include orders m = -2, -1, 0, 1, 2 (for 1:1 grating a2 = 0, a3 = -(1+t)/(3*pi))
    orders = [-3, -1, 0, 1, 3]
    amps = {0: a0, 1: a1, -1: a1, 3: -(1.0 + t_att)/(3*math.pi), -3: -(1.0 + t_att)/(3*math.pi)}

    # Compute for +dz and -dz for central-difference numerical purity
    shifts = []
    for sign in (+1.0, -1.0):
        C1 = 0.0 + 0.0j
        for m in orders:
            fx_m = sx + m * ux
            fy_m = sy + m * uy
            in_m = (fx_m**2 + fy_m**2) <= 1.0
            if not np.any(in_m): continue
            # Pair with m-1 to contribute to exp(+i 2pi u / P)
            m2 = m - 1
            if m2 not in amps: continue
            fx_2 = sx + m2 * ux
            fy_2 = sy + m2 * uy
            in_both = in_m & ((fx_2**2 + fy_2**2) <= 1.0)
            if not np.any(in_both): continue
            W_m = sign * dz_nm * eval_fringe_z(zinfo, fx_m[in_both], fy_m[in_both])
            W_2 = sign * dz_nm * eval_fringe_z(zinfo, fx_2[in_both], fy_2[in_both])
            dphi = (2.0 * math.pi / LAM) * (W_m - W_2)
            # C1 = sum_s w_s * E_m * conj(E_{m-1})
            C1 += np.sum(weights[in_both] * amps[m] * amps[m2] * np.exp(1j * dphi))
        # For bright-space centered at u=0 (a0>0, a1>0), Re(C1)>0; shift of intensity peak is u0 = -(P/2pi)*atan2(Im(C1), Re(C1))
        if abs(C1) < 1e-12:
            shifts.append(0.0)
        else:
            u0 = -(pitch_nm / (2.0 * math.pi)) * math.atan2(C1.imag, C1.real)
            shifts.append(u0)
    return (shifts[0] - shifts[1]) / (2.0 * dz_nm)

# Sanity check with Z2 (pure X-tilt): MUST give -1/NA = -0.7407 nm/nm for ANY source & pitch!
z2 = ztable[1]
s_z2_dip = compute_1d_grating_shift_sensitivity(z2, make_source('DipoleX_0.78_0.96_30deg'), 85.0, 0.0)
s_z2_ann = compute_1d_grating_shift_sensitivity(z2, make_source('Annular_0.65_0.90'), 120.0, 0.0)
s_z2_conv = compute_1d_grating_shift_sensitivity(z2, make_source('Conv_0.55'), 180.0, 0.0)
print(f"\n=== Sanity Check Z2 (Exact Theory = {-1.0/NA:.4f} nm/nm) ===")
print(f"  DipoleX 85nm: {s_z2_dip:.4f}, Annular 120nm: {s_z2_ann:.4f}, Conv 180nm: {s_z2_conv:.4f}")

# Define realistic illumination/pattern configurations for dual-layer overlay switching
configs_X = [
    ('DipX_85',    make_source('DipoleX_0.78_0.96_30deg'),   85.0,  0.0),
    ('CQuad_90',   make_source('CQuad_0.80_0.96_30deg'),     90.0,  0.0),
    ('Quasar_100', make_source('Quasar_0.75_0.95_30deg'),   100.0,  0.0),
    ('Ann_120',    make_source('Annular_0.65_0.90'),        120.0,  0.0),
    ('Conv_180',   make_source('Conv_0.55'),                180.0,  0.0),
    ('RotDip_85',  make_source('RotDipole_21deg_0.82_0.97'), 85.0, 21.0),
    ('Met_300',    make_source('Annular_0.65_0.90'),        300.0,  0.0),
]

configs_Y = [
    ('DipY_85',    make_source('DipoleY_0.78_0.96_30deg'),   85.0, 90.0),
    ('CQuad_90',   make_source('CQuad_0.80_0.96_30deg'),     90.0, 90.0),
    ('Quasar_100', make_source('Quasar_0.75_0.95_30deg'),   100.0, 90.0),
    ('Ann_120',    make_source('Annular_0.65_0.90'),        120.0, 90.0),
    ('Conv_180',   make_source('Conv_0.55'),                180.0, 90.0),
    ('RotDip_85',  make_source('RotDipole_21deg_0.82_0.97'), 85.0, 111.0),
    ('Met_300',    make_source('Annular_0.65_0.90'),        300.0, 90.0),
]

print("\n=== Simulated Odd Fringe Zernike Overlay Sensitivities (Z5..Z64) [nm OVL / nm Fringe] ===")
print(f"{'Z':>4s} {'n':>2s} {'m':>2s} {'tr':>3s} | {'DipX85':>7s} {'Ann120':>7s} {'Conv180':>7s} {'Quas100':>7s} {'RotD21':>7s} | {'Max|dS_X|':>9s} {'Max|dS_Y|':>9s} {'Worst|dS|':>9s}")
results = []
for z in odd_z:
    sx_vals = {}
    for name, src, p, ang in configs_X:
        val = compute_1d_grating_shift_sensitivity(z, src, p, ang)
        # project onto X if rotated
        sx_vals[name] = val * math.cos(math.radians(ang))
    sy_vals = {}
    for name, src, p, ang in configs_Y:
        val = compute_1d_grating_shift_sensitivity(z, src, p, ang)
        sy_vals[name] = val * math.sin(math.radians(ang))
    # Max differential overlay sensitivity across illumination/layer switches:
    vx = list(sx_vals.values())
    vy = list(sy_vals.values())
    max_dsx = max(vx) - min(vx)
    max_dsy = max(vy) - min(vy)
    worst_ds = max(max_dsx, max_dsy)
    # Typical worst-case pair (e.g. Dipole vs Conv/Annular)
    results.append({
        'j': z['j'], 'n': z['n'], 'm': z['m'], 'trig': z['trig'],
        'rms_factor': 1.0 / math.sqrt(2 * (z['n'] + 1)),
        'sx': sx_vals, 'sy': sy_vals,
        'max_dsx': max_dsx, 'max_dsy': max_dsy, 'worst_ds': worst_ds
    })
    print(f"Z{z['j']:2d} {z['n']:2d} {z['m']:2d} {z['trig']:>3s} | {sx_vals['DipX_85']:7.3f} {sx_vals['Ann_120']:7.3f} {sx_vals['Conv_180']:7.3f} {sx_vals['Quasar_100']:7.3f} {sx_vals['RotDip_85']:7.3f} | {max_dsx:9.3f} {max_dsy:9.3f} {worst_ds:9.3f}")

with open(r'C:\Users\panwk\.gemini\antigravity\brain\94f60b53-daaf-4e06-bef7-f19aa42ee521\scratch\zernike_sim.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nSaved zernike_sim.json")
