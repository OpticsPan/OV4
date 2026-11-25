# ArF / ArFi 及 ASML TWINSCAN XT（i-line / KrF）WS–RS 同步控制策略与单台重复性误差专项调研报告（v2）

[仓库首页](../../README.md) · [成果索引](../README.md) · [参考文献总目](../../REFERENCES.md) · [调研报告 v1 存档](WS-RS同步策略与单台重复性误差专项调研报告_v1.md) · [NXT:1965Ci 主报告 v1](NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v1.md) · [九大子系统说明书 v2](NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md) · [总变更记录](../../CHANGELOG.md)

> **v2 核心升级说明（2026-11-25）**：在完整保留 [v1 存档](WS-RS同步策略与单台重复性误差专项调研报告_v1.md) 关于 ArF / ArFi 机台主从方向、单台独立误差实测与 13 篇专利核验的基础上，**新增第 4 章专题调研：ASML `TWINSCAN XT` i-line（365 nm，`AT/XT:400` 系列）与 KrF（248 nm，`AT:750/850`、`XT:850/860/1000/1060K` 及 `PAS 5500/500`）WS–RS 同步跟从方向与全谱系性能参数**；并新下载、逐页视觉核验归档 ASML 奠基同步专利 **`[S14]` `US 6,373,072 B1`**（Hans Butler & Thomas Warmerdam，1998 优先权 / 2002 授权，9 页），结合本机 `ME3` ASML 官方 `TWINSCAN` Level 1/2/3 维护手册（`TSPE` GUI、`SWLF`/`SRLF`/`SRSM` 实测报表）彻底坐实 XT 世代同步机制与量化边界。  
> **文献下载与核验状态**：本报告共引用 **42 篇一手文献、官方手册与专利**，其中 **18 篇论文/手册**已在本机基线库（`OV4` 与 `ME3`）就位，**14 篇官方 USPTO 美国专利原件（9 篇 ASML + 5 篇 Nikon，合计 375 页）**已自动下载至本机 `D:\work\OV4\参考文献_新增\WS-RS同步\` 并完成封面/关键页视觉核验与 SHA-256 唯一性登记，另 **8 篇**（付费墙或非 US 专利）整理于第 6.3 节手动下载清单。

---

<a name="contents"></a>

## 目录

- [0. 执行摘要与核心结论速览](#sec-0)
- [1. 数学与物理机理：为何 WS 独立误差可以大于同步相对误差](#sec-1)
  - [1.1 含相关系数 $\rho$ 的同步方差合成方程](#sec-1-1)
  - [1.2 本地 OV4 两项工业实机铁证（`[075]` 与 `[022]`）](#sec-1-2)
- [2. ASML 与 Nikon ArF / ArFi 机台主从同步策略专利与文献核查](#sec-2)
  - [2.1 Nikon 路线：原厂总师确证 + USPTO 专利框图实锤（WS = Master，RS = Slave）](#sec-2-1)
  - [2.2 ASML 路线：由单向 WS→RS 主从演进至双向 Double-Youla 耦合](#sec-2-2)
  - [2.3 专利检索避坑与多自由度主从方向辨析](#sec-2-3)
- [3. ArF / ArFi 机台 WS / RS 独立误差与同步重复性公开实测数据](#sec-3)
  - [3.1 商业规格书披露边界与数据来源说明](#sec-3-1)
  - [3.2 WS / RS 各自独立工作（无耦合）实机伺服误差汇总](#sec-3-2)
  - [3.3 商用 ArFi 机台同步 `MA / MSD` 与曝光级 Stage Repeatability 汇总](#sec-3-3)
- [4. 【v2 新增专题】ASML TWINSCAN XT（i-line / KrF）WS–RS 同步跟从方向与性能参数核查](#sec-4)
  - [4.1 核心核定结论：XT i-line 与 KrF 依然是“RS 跟从 WS”（且比 NXT 更加依赖）](#sec-4-1)
  - [4.2 三重一手铁证：ASML 奠基专利 `US 6,373,072 B1`、`TSPE` 固件界面与 `SRLF/SWLF` 双层架构](#sec-4-2)
  - [4.3 ASML i-line / KrF（PAS 5500 → AT → XT）全谱系同步与套刻性能参数总表](#sec-4-3)
  - [4.4 ASML 官方手册实测明细：`AT/XT:850D`（WS Type-2 + RS D-spec）单台 `MA / MSD` 与 `TSDP` 限值](#sec-4-4)
- [5. 对 OV4 子系统独立验收规格的工程反校与勘误备忘](#sec-5)
  - [5.1 为何独立 FAT 仍须坚持解耦预算而不放宽 WS 上限](#sec-5-1)
  - [5.2 前期 `v2` 说明书第 1.3 节主从方向表述勘误备忘](#sec-5-2)
- [6. 参考文献总清单与下载状态（本地已有 / 已自动下载 / 手动下载清单）](#sec-6)
  - [6.1 A 类：本机 OV4 / ME3 既有文献与手册库已就位（18 篇 + 4 份手册）](#sec-6-1)
  - [6.2 B 类：已自动下载至 `参考文献_新增\WS-RS同步\` 的官方专利原件（14 篇，含新增 `[S14]`）](#sec-6-2)
  - [6.3 C 类：需手动下载清单（8 篇，含精确 DOI / 专利号与下载链接）](#sec-6-3)

---

<a name="sec-0"></a>

## 0. 执行摘要与核心结论速览

[返回目录](#contents)

| 核心调研问题 | 核验后明确结论 | 最硬核一手证据来源 |
| :--- | :--- | :--- |
| **1. 已知同步 `MA = 0.47 nm`，单台 WS 或 RS 重复性是否必然 `< 0.47 nm`？** | **不一定！**不仅数学上完全允许，而且在工业 ArF/ArFi 与 XT 机台中，**WS 独立误差大于同步相对误差 `\|WS − RS/4\|`** 是主从/耦合同步控制刻意实现的结果（ArFi 实测可大 **2.4–4.4 倍**；早期 XT 专利实测 `MA X` 由 `11.4 → 1.0 nm` 压缩 **11.4 倍**）。 | `[075]` Evers/ASML (*CEP* 2019) Fig. 12–13；`[022]` Heertjes/ASML (*CEP* 2013) Fig. 10；`[S14]` ASML `US 6,373,072 B1` Col. 7 |
| **2. ArF / ArFi 横向（X / Y / Rz）同步策略中，谁是 Master、谁是 Slave？** | **ASML 与 Nikon 高度一致：单向主从均以 WS 为 Master、RS 为 Slave**；ASML 进一步向双向 Double-Youla 耦合演进，但在决定套刻 `MA` 的低中频段（`< 250–400 Hz`）仍是 **RS 主动复现并追随 WS 误差**。 | Nikon `[S12]` `US 2012/0319637 A1`、`[090]` Shibazaki、`[085]` `NSR-S620D`；ASML `[147]` Fig. 6、`[022]`、`[075]` |
| **3. 【v2 新增】ASML `TWINSCAN XT` i-line / KrF 机台中，还是 RS 跟从 WS 吗？能做到什么程度？** | **是的！从 `PAS 5500` 到 `TWINSCAN AT/XT`（i-line `AT/XT:400`、KrF `AT:750/850`、`XT:850/860/1000/1060K`）一直都是 RS 跟从 WS（`Stages Error Coupling`）！**事实上，ASML 的 `WS → RS` 位置+二阶微分加速度前馈架构（`US 6,373,072 B1`）正是为早期 i-line/KrF 扫描机发明的。性能跨度：`PAS 5500/500`（`250 mm/s`，净 `MA 8 nm`）→ `AT/XT:850D`（`500 mm/s / 13.5 m/s²`，`TSDP` 净 `MA ≤ 2.1 nm`）→ `XT:1060K`（`≥ 205 wph`，`DCO ≤ 3.5 nm / MMO ≤ 5.0 nm`）；i-line `XT:400L/M`（`230–250 wph`，`OVL ≤ 15–20 nm`）。 | **`[S14]` ASML `US 6,373,072 B1`**（Butler & Warmerdam, 1998/2002, Fig. 1 & Col. 7）；`ME3 TT-PM-WS-3v1` Fig. 2.4 (`TSPE` GUI)；`ME3 08/09-TT-L3-RS/WSbook`；`[006]`、`[256]`、`[266]` |
| **4. Z / Rx / Ry 焦面自由度的主从方向是否相同？** | **不同！**轴向缩小倍率为 $`n_w \beta^2`$（干式 `1/16`，液浸 `1/11.14`），RS-Z 无法高速追随硅片形貌，故 **Z/Rx/Ry 调平由 WS 独立伺服**；掩模不平度经低频映射前馈给 WS 或物镜补偿。 | `[S6]` ASML `US 7,239,368 B2`、`[066]` Fig. 9、`[256]` §2.4 |
| **5. 工业实测的 WS 与 RS 独立（无耦合）误差各为多少？** | 商业手册不单列单台 FAT 指标。控制论文实测 ArFi 无耦合 `≤ 100 Hz`：**WS 约 `0.48 nm`**、**RS 折算晶圆侧仅 `~0.11 nm`**（4× 侧 `0.44 nm`）。ASML `ME3` 手册实测 KrF `AT/XT:850D` 静止/步进后：**WS `SWLF` `MA = 0.50–0.62 nm`（限 `1.5 nm`）**、**RS 4× 侧 `SRSM` `MA = 0.37–0.55 nm` / `SRLF` 步进后 `0.71–1.39 nm`（折算 1× 约 `0.18–0.35 nm`）**。 | `[075]` Fig. 12 & Table 1；`[022]` Fig. 10；`ME3 08-TT-L3-RSbook` L5001–5360；`ME3 09-TT-L3-WSbook` L5641–5660 |

---

<a name="sec-1"></a>

## 1. 数学与物理机理：为何 WS 独立误差可以大于同步相对误差

[返回目录](#contents)

<a name="sec-1-1"></a>

### 1.1 含相关系数 $\rho$ 的同步方差合成方程

沿横向（$X$ 非扫描向或 $Y$ 扫描向，投影物镜横向缩小倍率 $\beta = 1/4$），决定套刻偏移的同步相对位置误差为 $`e_{\mathrm{sync}}(t) = e_{\mathrm{WS}}(t) - e_{\mathrm{RS}}(t)/4`$。在狭缝移动平均（`MA`）低通窗内，其统计方差严格服从：

$$
\sigma_{\mathrm{sync}}^2 = \mathrm{Var}\!\left(e_{\mathrm{WS}} - \frac{e_{\mathrm{RS}}}{4}\right) = \sigma_{\mathrm{WS}}^2 + \left(\frac{\sigma_{\mathrm{RS}}}{4}\right)^2 - 2\rho\,\sigma_{\mathrm{WS}}\!\left(\frac{\sigma_{\mathrm{RS}}}{4}\right)
$$

其中 $\rho \in [-1, 1]$ 为两台在曝光狭缝 `MA` 频段内误差信号的线性相关系数：

1. **完全解耦独立控制（$\rho = 0$）**：仅当两台伺服环互相独立且无共模扰动时，有 $`\sigma_{\mathrm{sync}} = \sqrt{\sigma_{\mathrm{WS}}^2 + (\sigma_{\mathrm{RS}}/4)^2}`$，此时在数学上才必然满足 $`\sigma_{\mathrm{WS}} < \sigma_{\mathrm{sync}}`$ 且 $`\sigma_{\mathrm{RS}}/4 < \sigma_{\mathrm{sync}}`$（例如同步 `0.47 nm` 时单台必小于 `0.47 nm`）。
2. **存在强正相关（$\rho > 0$）**：交叉抵消项 $`-2\rho\,\sigma_{\mathrm{WS}}(\sigma_{\mathrm{RS}}/4)`$ 为负值。只要满足

$$
\rho > \frac{\sigma_{\mathrm{RS}} / 4}{2\,\sigma_{\mathrm{WS}}}
$$

即会出现 $`\sigma_{\mathrm{WS}} > \sigma_{\mathrm{sync}}`$ （同理，当 RS 为追随 WS 而放大自身位移误差时，耦合后的 $`\sigma_{\mathrm{RS}}/4`$ 同样可大于 $`\sigma_{\mathrm{sync}}`$ ）。在真实光刻机中，$\rho > 0$ 来自两类物理机制：
- **主动同步耦合（主导机制）**：通过主从前馈或双向 Youla 耦合，在狭缝 `MA` 敏感的低中频段（`< 100–500 Hz`）故意让 RS 复现 WS 的实测伺服误差（$`e_{\mathrm{RS}}/4 \approx e_{\mathrm{WS}}`$），使两台误差在晶圆像面上共模相消。
- **物理共模扰动（自然机制）**：同一计量框架（Metrology Frame）或投影物镜低频微振（通过 `SWLF` 与 `SRLF` 共追踪物镜加速度）、同相扫描加减速轨迹引发的同类伺服滞后，在 $`e_{\mathrm{WS}} - e_{\mathrm{RS}}/4`$ 做差时天然部分抵消。

<a name="sec-1-2"></a>

### 1.2 本地 OV4 两项工业实机铁证（`[075]` 与 `[022]`）

本地文献库中两篇由 **ASML 控制团队与 TU/e 联合发表** 的工业光刻机实测论文，直接量化了“单台独立误差 > 同步相对误差”的现象与物理代价：

| 文献来源 | 工况对比 | WS 低频 / 宽带独立误差 | RS 折算晶圆侧（1×）误差 | 同步相对误差 `e_sync`（频域 / 时域 `MA`） | 高频水床代价（`MSD`） |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`[075]` Evers, van de Wal (ASML) & Oomen (TU/e), *CEP* 2019**（Fig. 12–13 & Table 1，8 组实测扫描轨迹） | **无耦合（各自独立）** | `≤ 100 Hz`：**`~0.48 nm`**<br>`≤ 10 kHz`：`~3.32 nm` | `≤ 100 Hz`：**`~0.11 nm`**<br>`≤ 10 kHz`：`~2.40 nm` | `≤ 100 Hz` 累积：`~0.50 nm`<br>时域 `MA (3σ)`：**`0.565 nm`**（Peak `0.603 nm`） | `MSD (3σ) = 2.879 nm`（Peak `3.145 nm`） |
| **`[075]` 同上** | **双向 Double-Youla 耦合（标称 / 鲁棒）** | `≤ 100 Hz`：**`~0.48 nm`**（几乎不变）<br>`≤ 10 kHz`：`~3.82 nm` | `≤ 100 Hz`：**主动升至 `~0.48 nm`**（与 WS 曲线重合至 `~400 Hz`）<br>`≤ 10 kHz`：`~4.18 nm` | `≤ 100 Hz` 累积骤降至 **`~0.08 nm`**<br>时域 `MA (3σ)`：**`0.108 nm`（标称）/ `0.200 nm`（鲁棒）** | `MSD (3σ)` 升至 **`3.329 / 3.304 nm`**（Peak `3.485 / 3.670 nm`） |
| **`[022]` Heertjes (TU/e), Temizer (ASML) & Schneiders, *CEP* 2013**（Sec. 6 & Fig. 10，实机扫描） | **未开同步前馈（$`C_p = C_q = 0`$）** | `100 Hz`：`~1.8 nm` (rms)<br>`≤ 2500 Hz`：**`~5.9 nm` (rms)** | 未单独绘出（由无耦合同步 `~6.3 nm` 反推宽带约 `~2.2 nm` rms） | `100 Hz`：`~1.4 nm` (rms)；全频段 `~6.3 nm` (rms)<br>扫描段 `MA`（$`\mathcal{L}_\infty`$）：**`2.92 nm`** | 扫描段 `MSD = 6.27 nm` |
| **`[022]` 同上** | **WS→RS 双 FIR 前馈同步优化** | 同上（WS 作为 Master 不变，`e_m` 全频段 `~5.9 nm` rms） | RS 主动跟踪 `e_m` 的 `50–500 Hz` 分量 | `100 Hz` 降至 `~1.0 nm` (rms)；全频段降至 **`~4.0 nm` (rms)**<br>扫描段 `MA`：**`1.55 nm`** | 扫描段 `MSD = 3.56 nm`（`> 500 Hz` 触发前馈水床放大，Eq. 46） |

**核心物理洞察**：在 `[075]` 中，WS 独立低频误差为 `~0.48 nm`，而开启耦合后整机同步 `MA (3σ)` 压低至 `0.108–0.200 nm`——**WS 独立误差实测达到同步相对误差的 2.4–4.4 倍**；甚至 RS 为了完美复制 WS 轨迹，把自身低频绝对误差从 `0.11 nm` 主动拉大 4 倍以上至 `0.48 nm`，以换取相对误差 `e_wr` 坍塌 84%，但根据波特/前馈水床积分定理（`[022]` Eq. 46），低频压制必然在高频换来 `MSD` 抬升（`2.88 → 3.33 nm`）。

---

<a name="sec-2"></a>

## 2. ASML 与 Nikon ArF / ArFi 机台主从同步策略专利与文献核查

[返回目录](#contents)

<a name="sec-2-1"></a>

### 2.1 Nikon 路线：原厂总师确证 + USPTO 专利框图实锤（WS = Master，RS = Slave）

Nikon 的 ArF 与 ArFi 机台（`NSR-S308F` → `NSR-S620D` → `NSR-S630D/S636E`）证据链最为清晰，原厂总师论文、控制综述与已下载的 5 篇官方 USPTO 专利原件完全互相印证：

1. **官方专利首页控制框图实锤（已下载 `[S12]` `US 2012/0319637 A1`，72 页，Nikon Corp.，发明人 Pai-Hsueh Yang / Kazuhiro Hirano / Masao Yuasa，2012）**：
   - 该专利直接被 Nikon `NSR-S620D` ArFi 控制综述 `[085]`（L195）引用。
   - 经逐页视觉核验其 USPTO 原件封面图（Page 1），系统控制框图明确分为上下双环：
     - **下环（Master，晶圆台 WS）**：`stage trajectory` → `wafer error` → `WS MILC` + `WS FB filter` → `wafer stage` → `wafer position`。
     - **跨台前馈链路（自下向上）**：**`wafer error` 经同步目标滤波器 `synch target filter H(s)` 直接送入上环 `reticle error` 求和节点！**
     - **上环（Slave，掩模台 RS）**：`stage trajectory` + `H(s)·(wafer error)` → `reticle error` → `RS MILC` + `RS FB filter C(s)` → `reticle stage P(s)` → `reticle position`，最终与 `wafer position` 做差得到 `synch error`。
   - 专利摘要（Abstract）原文直述：*“A synchronization target filter couples the first and second control loops and causes the first controller [RS] to move the first movable body [reticle stage] in a manner that tracks the position-error data of the second movable body [wafer stage] at one or more frequencies of interest.”*
2. **Nikon 精机工作台首席架构师原话（`[090]` Yuichi Shibazaki，*IJAT* 2008，ArF `NSR-S308F`，L37）**：
   - *“Our Company has adopted the master-slave control method in which **RS follows WS**. Accordingly, the final synchronous accuracy depends on RS. Even if WS performed somewhat arbitrarily, RS could work hard to make up for it.”*
3. **Nikon ArFi `NSR-S620D` 控制综述（`[085]` 後藤太邦・湯浅匡夫，*SICE* 2013，L35 & Eq. 8–9）**：
   - 明确表述 **“レチクルステージがウェハステージに同期追従して動く”（RS 同步追随 WS 运动）**，并给出 $`[x_{\mathrm{RS}}, y_{\mathrm{RS}}, \theta_{\mathrm{RS}}]^T = \mathbf{A}[x_{\mathrm{WS}}, y_{\mathrm{WS}}, \theta_{\mathrm{WS}}]^T + \mathbf{B}`$。
4. **Nikon 配套专利家族（全部已下载本地 `[S9]–[S13]`）**：
   - **`[S9]` `US 2004/0128918 A1`**（41 页，P.-H. Yang / K. Hirano / S. Makinouchi 等，2004）：奠基同步 + ILC 专利，摘要明确披露将第二台（WS）定位数据送入控制器调整第一台（RS）驱动以改善两台同步。
   - **`[S10]` `US 2005/0231706 A1`**（25 页，P.-H. Yang 等，2005）：视场分组多遍迭代学习前馈（MILC）。
   - **`[S11]` `US 2006/0170382 A1`**（34 页，P.-H. Yang 等，2006）：直线电机推力波动 ILC 补偿（`[085]` 引用）。
   - **`[S13]` `US 8,451,431 B2`**（47 页，P.-H. Yang & S.-L. Koo，2013）：采用迭代反馈整定（IFT）联合优化前馈与两台同步控制参数（同时被 ASML `[147]` L719 引用）。
   - 配合 Nikon Research (NRCA) / UC Berkeley 论文 `[078]`（Mishra, Yeh & Tomizuka, *ACC* 2008，L37），完整阐明物理第一性原理：**RS 更轻、闭环带宽远高于大质量 300 mm WS**，故以 WS 实测位置乘倍率驱动 RS 追随。

<a name="sec-2-2"></a>

### 2.2 ASML 路线：由单向 WS→RS 主从演进至双向 Double-Youla 耦合

ASML（Veldhoven 控制团队 + TU/e 合作组）的文献与专利链显示出清晰的三代演进脉络（详见第 4 章补充的 PAS 5500 / XT 起源），且各代在决定 `MA` 的低中频段均以 **RS 追随 WS** 为核心：

1. **起源与阶段一（PAS 5500 → TWINSCAN AT/XT → 早期 NXT）：工业单向主从双路径前馈（WS = Master，RS = Slave）**：
   - **`[S14]` `US 6,373,072 B1`**（Hans Butler & Thomas Warmerdam，ASM Lithography B.V.，1998 优先权 / 2002 授权）：奠定 ASML 经典 `WS → RS` 位置设定点 + $ms^2$ 加速度力双路径前馈（详述于第 4.2 节）。
   - **`[022]` Heertjes (TU/e), Temizer (ASML) & Schneiders (*CEP* 2013，L49–L71)**：显式指定 WS 为 Master（误差 $e_m$）、RS 为 Slave，将模拟/固定 $ms^2$ 滤波升级为数据驱动自整定双 FIR 同步滤波器（位置设定点滤波器 $`\mathcal{C}_p`$ + 前馈力滤波器 $`\mathcal{C}_q`$）强制 RS 追踪 $e_m$。
   - **`[147]` M. F. Heertjes（ASML Netherlands B.V.，*IFAC* 2016，Sec. 4.2 & Fig. 6–8）**：将该机制直接命名为 **“wafer-to-reticle stage synchronization”**，结构图 Fig. 6 明确以 WS 输出 $`y_{\mathrm{ws}}`$ 驱动双前馈滤波器 $`\mathcal{F}_1(\boldsymbol{\rho}), \mathcal{F}_2(\boldsymbol{\rho})`$ 注入 RS 伺服环，实测同步前馈带宽（$`\vert\mathcal{S}_{\mathrm{ff}}\vert = 0\text{ dB}`$）高达 **`543.7–588.2 Hz`**。
2. **阶段二（高带宽磁浮 NXT / EUV 时代）：双向耦合（WS→RS + RS→WS）**：
   - **`[M1]` Lambregts, Heertjes & van der Veek（ASML / TU/e，*ACC* 2015）** 指出：随着 NXT 轻量化磁浮平面电机使 WS 带宽大幅提高（`[009]` 披露 NXT WS 第一阶模态较 XT 提升 40%），在传统单向 WS→RS 同步之上叠加反向 RS→WS 耦合，构成多变量 $\mathcal{H}_\infty$ 双向耦合控制。
   - **`[075]` Evers, van de Wal (ASML) & Oomen (*CEP* 2019)** 进一步建立保证鲁棒稳定性的 **双向 Double-Youla 耦合框架**；但从其工业扫描机实测累积误差曲线（Fig. 12）可见，在 `< 250–400 Hz` 的 `MA` 主导频段，**依然是 RS 主动复现 WS 的误差轨迹**（原文图注：*“To achieve stage synchronization the reticle stage is synchronized to the wafer stage”*）。
3. **ASML 配套核心专利群（9 篇官方 USPTO 原件已全部下载本地 `[S1]–[S8]` 及新增 `[S14]`）**：
   - **`[S14]` `US 6,373,072 B1`**（Butler & Warmerdam，2002，本次新归档）：**ASML `WS → RS` 误差前馈同步奠基专利**（详见第 4.2 节）。
   - **`[S8]` `US 8,279,401 B2`**（Vervoordeldonk & Baggen，2012，`[147]` 引用）：位置控制系统中集成结构柔度补偿（Compliance Compensation）与加速度/Snap 前馈。
   - **`[S2]` `US 2006/0285101 A1`**（Hans Butler, Draaijer & Breukers，2006）：投影系统位置信号滤波与前馈注入晶圆台伺服环，抑制框架相对振动误差（对应 `SWLF`）。
   - **`[S1]` `US 2004/0176861 A1`**（Hans Butler，2004）与 **`[S3]` `US 7,098,990 B2`**（Hans Butler，2006）：晶圆台在线质量辨识自适应加速度前馈及外扰加速度抑制控制。
   - **`[S4]` `US 7,170,581 B2`**（Rob Tousain，2007）：工作台速度/加速度/Jerk/Snap 多阶自适应前馈系数在线学习。
   - **`[S5]` `US 7,181,296 B2`**（Rotariu, Ellenbroek, Steinbuch & Van Baars，2007）：面向变扫长光刻扫描台的时频自适应迭代学习控制（Adaptive ILC）。
   - **`[S6]` `US 7,239,368 B2`**（Oesterholt 等，2007）：利用衬底台或掩模台面形不平度（Unflatness）映射进行扫描曝光前馈补偿。
   - **`[S7]` `US 7,405,811 B2`**（Beems & Sakai，2008）：基于中间结构短程双测量系统的晶圆台高精度定位测量架构。

<a name="sec-2-3"></a>

### 2.3 专利检索避坑与多自由度主从方向辨析

1. **专利中 `"master"` 一词的三重歧义**：ASML 与 Nikon 的正式专利权利要求书极少直接写 `"master stage / slave stage"`。检索时遇到 `"master"`，需仔细区分其语境是指 ① **掩模原版（pattern master）**、② **单台内部的“短行程（Master）–长行程（Slave）/ 平衡质量块”**（如 `ME3 08-TT-L3-RSbook` L998 明确指 RS 内部 Short Stroke 是 Master、Long Stroke 是 Slave），还是 ③ **传感器通信总线主从时钟**；真正的跨台同步控制多表述为 *"first/second movable body"*、*"synchronization target filter"*、*"tracks the position-error data"* 或 ASML 固件中的 **`Stages Error Coupling`**。
2. **自由度维度差异（横向 X/Y/Rz vs 焦面 Z/Rx/Ry）**：
   - **X / Y / Rz（面内套刻）**：WS = Master，RS = Slave（或低中频 RS 追随 WS 的双向耦合）。
   - **Z / Rx / Ry（轴向焦面调平）**：干式物镜轴向缩小倍率为 $1/16$，液浸物镜为 $`n_w \beta^2 = 1.4366 / 16 = 1 / 11.14`$，RS-Z 位移对像面焦深几乎没有高速调平能力，因此 **硅片起伏跟随由 WS-Z/Rx/Ry 独立伺服**；而掩模弯曲/不平度（如 `[S6]` `US 7,239,368 B2`）则是以静态/低频映射前馈给 WS 或投影物镜补偿。
3. **官方原件视觉核验纠偏记录**：在线检索摘要极易混淆专利号与发明人（如曾误将 `US 7,405,811 B2` 标为 Nikon、误将 `US 2016/0299446 A1` 当作 ASML 同步专利——经本次下载封面核验 `US 2016/0299446 A1` 实为 Canon 碳粉专利！亦曾误将 `US 6,373,072 B1` 发明人标为 Braat/van der Laan——实为 **Hans Butler & Thomas Warmerdam**）。本报告全部 14 篇 `[S1]–[S14]` 均已下载官方 USPTO PDF 并逐一完成封面视觉核验。

---

<a name="sec-3"></a>

## 3. ArF / ArFi 机台 WS / RS 独立误差与同步重复性公开实测数据

[返回目录](#contents)

<a name="sec-3-1"></a>

### 3.1 商业规格书披露边界与数据来源说明

ASML（`NXT:1950i / 1965Ci / 1970Ci / 1980Di / 2000i`）与 Nikon（`NSR-S620D / S630D / S635E / S636E`）在对外商业规格书和常规 SPIE 机型汇报中，**从不单独公布 WS 或 RS 的子系统独立 FAT 重复性指标**——对外仅承诺整机 `DCO / SMO / MMO`，偶见同步扫描误差 `|WS − RS/4| MA / MSD` 以及光刻胶双次曝光法测得的 `Stage Repeatability`。真正可查到 **WS 与 RS 各自独立（无耦合）伺服误差** 的一手数据，主要来源于原厂控制工程师在 *Control Engineering Practice*、*IFAC*、*IEEE* 发表的实机曲线（及第 4.4 节补充的 `ME3` ASML 内部维护手册实测报表）。

<a name="sec-3-2"></a>

### 3.2 WS / RS 各自独立工作（无耦合）实机伺服误差汇总

| 数据来源与测试平台 | 统计口径与频带 | WS 自身独立误差（无耦合） | RS 自身独立误差（无耦合，折算至 1× 晶圆侧） | 工程解读 |
| :--- | :--- | :--- | :--- | :--- |
| **`[075]` ASML 工业光刻机**（Fig. 12 & Table 1） | 8 组扫描实测，累积伺服误差 `mean + 3σ` | `≤ 60 Hz`：`~0.40 nm`<br>**`≤ 100 Hz`：`~0.48 nm`**<br>`≤ 10 kHz`：**`~3.32 nm`** | **`≤ 100 Hz`：`~0.11 nm`**（4× 掩模侧约 `0.44 nm`）<br>`≤ 10 kHz`：**`~2.40 nm`**（4× 侧约 `9.6 nm`） | 低频 `MA` 频段内 **WS 独立误差约为 RS 折算误差的 4.4 倍**，直接说明 WS 才是低频误差主导源 |
| **`[022]` ASML 工业光刻机**（Sec. 6 & Fig. 10） | 实机扫描 CPSD（rms） | `100 Hz`：`~1.8 nm` (rms)<br>`~170 Hz` 阶跃至 `5.0 nm`<br>`≤ 2500 Hz`：**`~5.9 nm` (rms)** | 未单列（结合无耦合同步全频段 `~6.3 nm` 反推宽带约 `~2.2 nm` rms） | 同步前馈将 WS 在 `50–500 Hz` 的主误差大幅相消，使同步全频段降至 `~4.0 nm` (rms) |
| **`[147]` ASML 短行程 WS**（Fig. 5） | 匀速扫描段（`0.08–0.12 s`）**原始瞬时宽带误差（未做 MA 滤波）** | `e_x, e_y` 峰峰值 **`±1–2 nm`**；`e_rz ≈ ±15–20 nrad`；`e_z ≈ ±2–3 nm`；`e_rx ≈ ±0.05 μrad`；`e_ry ≈ ±25 nrad` | — | 经狭缝低通（`MA`）平均后横向误差压至亚纳米量级 |
| **`[066]` ASML `NXT:1965Ci / 1970Ci`**（Fig. 9） | 陶瓷短行程 WS，`800 mm/s` 扫描 `MAz` | 分布峰值 **`4 nm`**，95% 视场 **`≤ 6 nm`**（旧金属 WS 为 `5–17 nm`） | 液浸 RS-Z 按 $1/11.14$ 衰减占比极小 | 该实测 `MAz` 基本等同 **WS 独立 Z 向扫描跟踪误差** |

<a name="sec-3-3"></a>

### 3.3 商用 ArFi 机台同步 `MA / MSD` 与曝光级 Stage Repeatability 汇总

| 商业 ArFi 机型（NA = 1.35） | 文献出处 | 同步扫描误差 `\|WS − RS/4\|`（`MA` / `MSD`） | 曝光级 Stage Repeatability / Stage Positioning 分项 |
| :--- | :--- | :--- | :--- |
| **ASML `NXT:1950i`**（`175 wph`） | `[009]` Fig. 3 & Fig. 10 | **`Sync MA-X = 0.47 nm`**<br>**`Sync MA-Y = 0.49 nm`** | Fig. 3 DCO 拆解中 **Stage Positioning 占比 `20.0%`（堆叠段高 `~0.50 nm`）**，较 `XT:1900Gi` 压降 3×，整机 `DCO ≤ 2.5 nm` |
| **ASML `NXT:1965Ci`**（`~250 wph`） | `[066]` Fig. 9 & ASML 官方规格 | 陶瓷 WS `MAz` 峰值 `4 nm`（95% `≤ 6 nm`）；横向同步 `MA` 处于 `~0.45–0.50 nm` 档 | 商业红线 **`SMO ≤ 2.5 nm`**、**`MMO ≤ 4.5 nm`**（详见本仓 [NXT:1965Ci 主报告 v1](NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v1.md)） |
| **ASML `NXT:1970Ci / 1980Di`**（`250–275 wph`） | `[066]` & `[015]` Fig. 4–7 | 全片焦面 `FU < 9.1 nm (3σ)`、`MMO < 2.0–2.5 nm` | 横向同步 `MA` 反推处于 `~0.30–0.35 nm` 档位 |
| **Nikon `NSR-S620D`**（`700 mm/s`） | `[063]` Fig. 14–15 & `[085]` L109 | 零整定时间实测：<br>**`MA-X < 0.6 nm`、`MA-Y < 0.6 nm`、`MA-Z < 4 nm`**<br>**`MSD-X < 2.5 nm`、`MSD-Y < 3.0 nm`、`MSD-Z < 6.5 nm`** | **单片不卸载双次曝光套刻差 `3σ`**（单遍等效 $\div\sqrt{2}$）：<br>• `320 mm/s`：**`0.96 / 1.20 nm`**<br>• `500 mm/s`：**`1.56 / 1.45 nm`**<br>• `700 mm/s`：**`1.60 / 1.49 nm`** |
| **Nikon `NSR-S630D`**（`250 wph`） | `[018]` Fig. 3–6 | RS 升级编码器伺服取代干涉仪；`SMO = 1.7 nm`、`MMO = 2.5 nm`、`FU < 15 nm` | 未单独公开单台重复性数值 |

---

<a name="sec-4"></a>

## 4. 【v2 新增专题】ASML TWINSCAN XT（i-line / KrF）WS–RS 同步跟从方向与性能参数核查

[返回目录](#contents)

<a name="sec-4-1"></a>

### 4.1 核心核定结论：XT i-line 与 KrF 依然是“RS 跟从 WS”（且比 NXT 更加依赖）

针对专题提问——**“ASML 的 `TWINSCAN XT` i-line 或 KrF 机台中，WS–RS 同步跟从是谁跟谁？还是 RS 跟从 WS 吗？相关参数能做到什么程度？”**——经逐页核验 ASML 奠基专利原件（`[S14]` `US 6,373,072 B1`）、本机 `ME3` ASML 官方 `TWINSCAN` Level 1/2/3 维护手册及公开文献，给出明确结论：

1. **首先厘清机型类型**：与早期单台步进投影式（Stepper）的 `PAS 5500/100–400` i-line 光刻机不同，**ASML `TWINSCAN AT:400` / `XT:400`（365 nm i-line）与 `AT:750/850`、`XT:850/860/1000/1060K`（248 nm KrF）全部都是双工件台步进扫描投影光刻机（Dual-Stage Step & Scan，4× 缩小、`26 × 33 mm` 视场）**，共享同一套 `TWINSCAN` 机电与运动控制架构（`AT` 为早期命名，自 `850D/1250D` 起演进为 `XT` 平台）。
2. **同步跟从方向明确结论：依然是 `RS 跟从 WS`（`WS = Master`，`RS = Slave`）！**
   - 事实上，ASML 的 **“WS 误差实时前馈给 RS（Stages Error Coupling）”** 架构，正是 Hans Butler 与 Thomas Warmerdam 在 **1998 年**面向 `PAS 5500` 与 `TWINSCAN AT/XT`（涵盖汞灯 i-line 与准分子激光 KrF/ArF）步进扫描机发明的核心专利（`[S14]` `US 6,373,072 B1`）。
3. **为什么 `XT`（i-line / KrF）在物理上甚至比 `NXT` 更依赖“RS 跟从 WS”？**
   - `TWINSCAN AT/XT` 的晶圆台采用 **H 型直线电机气浮导轨 + 笨重微晶玻璃干涉仪反射镜块（Mirror Block）**，其运动质量接近后来 `NXT` 磁浮平面电机的 **3 倍**、第一阶结构共振频率比 `NXT` **低 40%**（`[009 Fig. 9–10]`）；
   - 与此同时，6 英寸掩模台 `RS` 质量轻得多、自 `AT/XT C-spec / 850D` 起已率先采用低质量短行程洛伦兹执行器 + 编码器测量 + 磁力重力补偿器（`ME3 08-TT-L3-RSbook` L413–432），且物镜 4× 缩小天然把 RS 自身扰动在晶圆面衰减 4 倍（方差衰减 16 倍）。因此 `XT` 世代 WS 的低频/中频带宽瓶颈远大于 RS，**只能由轻快的高带宽 RS 追随笨重的 WS**，绝不可能反过来让 H-bar 晶圆台去追随高速 2.0–2.2 m/s 的掩模台！
   - **后期演进补充**：2018 年后的新一代干式/i-line 机型 **`XT:400M`**（`[006]` IWAPS 2018 Slide 16–17：*"Productivity boost with new wafer stage"*）与 `NXT:1470` 将 `NXT` 磁浮平面电机 WS 下放至 i-line/干式平台，套刻与产能显著跃升，但横向低中频同步控制仍沿袭 `WS → RS` 主从及可选双向耦合路线。

<a name="sec-4-2"></a>

### 4.2 三重一手铁证：ASML 奠基专利 `US 6,373,072 B1`、`TSPE` 固件界面与 `SRLF/SWLF` 双层架构

#### 铁证 1：ASML 奠基同步专利原件 `[S14]` `US 6,373,072 B1`（Hans Butler & Thomas Warmerdam，ASM Lithography B.V.，1998 优先权 / 2002 授权，已下载本地）

经逐页视觉核验该专利全部 9 页（Cover、Fig. 1–3 及 Col. 1–8），原文直接披露了 ASML 早期 i-line/KrF/ArF 步进扫描机（Col. 7 明确写明光源可为 `Hg lamp or excimer laser`，Col. 1 明确引证 ASML 双工件台母专利 `WO 98/28665` 与 `WO 98/40791`）的 **`WS → RS` 双支路误差前馈控制框图（Fig. 1）**：

- **主环（Master = WS）**：参考轨迹 $\mathrm{SPW}$ 与实测 $y_{\mathrm{WS}}$ 做差得 $e_{\mathrm{WS}}$，经 `WS` 反馈控制器 $G_{\mathrm{WS}}$ 驱动晶圆台本体 $H_{\mathrm{WS}}$。
- **跨台光纤前馈链（`WS → RS`，Claim 8 明确采用光纤链路传输以压低延时，对应实机 `PMCR` 机柜的 `HSSL` 高速光纤链路）**：
  - 将 $e_{\mathrm{WS}}$ 乘以 4× 经低通 + 超前/滞后相位补偿滤波器 $H_F$（在 `175–225 Hz` 频段优化，典型零点 `175 Hz` / 极点 `205 Hz`，阻尼比 `0.3`），兵分两路送入 `RS`：
    1. **位置设定点支路**：叠加至 `RS` 设定点 `SPR`（$`4\cdot\mathrm{SP} + H_F e_{\mathrm{WS}}`$），使 `RS` 反馈控制器 $G_{\mathrm{RS}}$ 不会把额外加速度前馈力误判为外部干扰而抵消；
    2. **二阶微分加速度前馈力支路（Block `D` = $ms^2$）**：对误差求二阶时间导数再乘以掩模台质量 $m$，直接注入 `RS` 电机推力端——**绕过 `RS` 反馈环自身仅 `150–175 Hz` 的闭环带宽限制，直接利用 `1/(ms²)` 刚体动力学精准消去 WS 在 `175–225 Hz` 频段最顽固的结构振动扰动！**
- **专利 Col. 7 实测对比数据（晶圆像面 `nm`）**：

| 实测同步指标（晶圆像面） | 未开同步耦合（Uncorrected） | 开启 `WS → RS` 双支路（Loop，Fig. 1） | 叠加 `175/205 Hz` 超前滞后滤波（Filter） | 相对无耦合压降幅度 |
| :--- | :---: | :---: | :---: | :---: |
| **`MA X`**（非扫描向套刻主导） | **11.4 nm** | 1.4 nm | **1.0 nm** | **↓ 91.2%**（压缩 11.4×） |
| **`MSD X`**（非扫描向高频模糊） | **14.9 nm** | 7.9 nm | **6.9 nm** | **↓ 53.7%** |
| **`MA Y`**（扫描主轴套刻主导） | **4.3 nm** | 1.6 nm | **1.1 nm** | **↓ 74.4%**（压缩 3.9×） |
| **`MSD Y`**（扫描主轴高频模糊） | **22.7 nm** | 15.8 nm | **9.3 nm** | **↓ 59.0%** |

> 专利 Fig. 2A/2B 及 Col. 6 原文明确证实：开启该架构后，RS 折算误差（`RS / 4`）在幅频谱上紧贴 WS 误差曲线（*“the RS follows the WS quite accurately when it comes to the amplitude of the error”*），由此换来净同步误差 `e_WRS` 的断崖式下降——这也直接从 1998 年第一代扫描机起就印证了本文第 1 章的核心结论：**WS 独立误差（`11.4 nm`）可以远大于同步净误差（`1.0 nm`）！**

#### 铁证 2：ASML 官方 `TWINSCAN AT/XT` 维护手册 `TSPE` 原厂软件界面（`ME3 TT-PM-WS-3v1` Fig. 2.4）

在本机 `ME3` 仓库的 ASML 官方培训手册 `TT-PM-WS-3v1`（2007 年，适用于 `TWINSCAN AT/XT` 全系）第 46 页 **Figure 2.4 `RS+WS test software: TSPE: Stages Performance Test`** 实机界面截图中，右侧明确设有独立的硬件/固件控制选项：
- **`Stages Error Coupling`：`Automatic`（默认）/ `On` / `Off`**；
- 底部原厂帮助行白纸黑字注明：*“Select Automatic to set the stages error coupling on or off depending of measurement type. Default: Automatic.”*
- 在 `WSE+RS combined scan`（联合曝光扫描测试）时固件自动置 `On`（启用 `WS → RS` 误差耦合），而在 `WSM only`（量测侧单台扫描）或 `RS performance scan`（单掩模台诊断）时自动置 `Off` 独立考核。

#### 铁证 3：`TWINSCAN AT/XT` 双层协同参考机制（`SWLF` + `SRLF` 共追踪物镜 + `WS → RS` 误差耦合）

查阅 `ME3` 的 `08-TT-L3-RSbook_v1.md`（L5080–5360）与 `09-TT-L3-WSbook_v1.md`（L5466–5660，`WS Type-2`，标明适用于 **`AT/XT 850D & 1250D`**）：
- **第一层（共同光学参考追踪）**：投影物镜顶部/底部安装有高精度加速度计。WS 通过 **`SWLF`（Wafer Stage Lens Feedforward）**、RS 通过 **`SRLF`（Reticle Stage Lens Feedforward）** 分别将物镜振动加速度经相位超前与陷波滤波器前馈注入各自短行程洛伦兹电机，使两台先共同“锁死”在同一投影物镜坐标参考系上（原文：`Suppressing the lens eigenfrequencies in the controller error means that the Reticle Stage follows the lens vibrations very well`）。
- **第二层（跨台主从残余补偿）**：两台各自闭环后仍残留的 WS 低中频跟踪误差，通过 `PMCR` 运动控制机柜（含 4 块 WS 伺服板 + 1 块 RS 伺服板）经 `HSSL` 光纤链路送入 RS 环路，执行 **`Stages Error Coupling`（`WS → RS`）** 实时抵消；同时各台内部遵循 **Short Stroke = Master、Long Stroke = Slave**（经 Difference Sensor 跟随）及 Balance Mass 动量抵消架构（`ME3 09-TT-L3-WSbook` Fig. 1.77）。

<a name="sec-4-3"></a>

### 4.3 ASML i-line / KrF（PAS 5500 → AT → XT）全谱系同步与套刻性能参数总表

下表汇集了 ASML 官方 `ME3` 维护手册、SPIE 一手论文（`[256]`, `[266]`, `[006]`）与 ASML 官方公开产品规格书，完整呈现 **i-line（365 nm）与 KrF（248 nm）步进扫描机** 从早期 `PAS 5500/500` 到最新 `XT:400M` / `XT:1060K` 的运动、同步与套刻性能边界：

| 机型与波段 | 平台架构与 NA / 分辨率 | WS 扫描速度 / 加速度 | RS 扫描速度 / 加速度（4×） | WS–RS 净同步误差（`MA` / `MSD`） | 整机套刻（`SMO/DCO` 与 `MMO`） | 产能（300 mm wph） | 一手数据来源 |
| :--- | :--- | :---: | :---: | :--- | :--- | :---: | :--- |
| **`PAS 5500/500`**（248 nm KrF，单台扫描） | 单 WS、0.40–0.63 NA、220 nm、`26×8 mm` 狭缝 | `250 mm/s`（整定 `22 ms`） | `1000 mm/s` | 扫描峰值 **`MA = 8 nm`**、**`MSD = 22 nm`**（Stage OVL `12/23 nm`） | SMO 实测 `19/23 nm`（规格 `≤ 45 nm`） | `96 wph`（200 mm） | `[256]` de Zwart / Butler 等 (*SPIE* 1997) §2.2, §3.2 |
| **`AT:400B / AT:400C`**（365 nm i-line，双台扫描） | 双 WS Type-1、0.48–0.65 NA、280 nm、5–5.5 kW 汞灯 | **`320 / 360 mm/s`** | `1.28 / 1.44 m/s` | 与同代 AT 平台共用 `WS→RS` 耦合架构（量级 `~2–4 nm`） | SMO **`≤ 25 nm`**；MMO **`≤ 45 / 40 nm`** | `100 / 110 wph` | `ME3 Level1 01_AP-L1-Hardware_Introduction` Slide 20 |
| **`XT:400F / K / L`**（365 nm i-line，双台扫描） | 双 WS、0.48–0.65 NA、`350/280/220 nm`、SMASH 对准 | 升级至 `XT` 高速档（≥ `500 mm/s` 级） | ≥ `2.0 m/s` 级 | 商业书未单列；支持 200/300 mm 桥接与大形貌调平 | 全片套刻 **`≤ 20 nm`**（配 TOP-2） | **`≥ 230 wph`**（200 mm `≥ 250`） | ASML 官方规格 & `[006]` IWAPS 2018 Slide 16 |
| **`XT:400M`**（365 nm i-line，新一代双台） | **引入新型工件台（NXT 干式技术下放）**、0.65 NA | 新型高速平面/轻量化台 | 匹配 4× 高速 RS | 商业书未单列；继承 NXT 级动态精度 | 全片套刻 **`≤ 15 nm`** | **`≥ 250 wph`** | `[006]` ASML IWAPS 2018 Slide 16–17 |
| **`AT:750B / C`**（248 nm KrF，首代双台） | 双 WS Type-1、0.50–0.70 NA、130 nm | **`250–360 mm/s`**、`8 m/s²` | `1.0–1.44 m/s` | 双台串扰 `< 0.85 nm MA`（`< 1.7 nm p-p`）；Stage 精度 `4 nm (99.7%)` | SMO 规格 `≤ 20 nm`（实测短时 `8–10 nm`、3 天 `13 nm`）；MMO `35 / 30 nm` | `95 / 112 wph` | `[266]` Sluijk 等 (*SPIE* 2001) & `ME3 Level1` Slide 21 |
| **`AT/XT:850D`**（248 nm KrF，**XT 通用基线**） | **WS Type-2 + RS D-spec**（RS 编码器+磁重力补偿）、0.80 NA、100 nm | **`500 mm/s`**、**`13.5 m/s²`** | **`2.0 m/s`**、**`54 m/s²`** | **官方原厂手册 `TSDP` 净误差指标：`≤ 2.1 nm`（X/Y MA）**（详表见 4.4 节） | SMO **`≤ 15 nm`**；MMO **`≤ 25 nm`** | `130 wph`（50 mJ） | `ME3 Level1` Slide 21；`ME3 08/09-TT-L3-RS/WSbook` |
| **`XT:860M / N`**（248 nm KrF，高产双台） | 0.55–0.80 NA（Starlith 860+）、≤ 110 nm、40–60 W 激光 | `XT-rev2` 高速档（`≥ 550 mm/s` 级） | `≥ 2.2 m/s`、`69 m/s²` 级 | 同代 `XT-rev2`（`XT:1400` 参照）`TSDP` 净误差 **`≤ 2.0 nm`**（X/Y MA） | `860M`：DCO `≤ 12` / MMO `≤ 14 nm`<br>`860N`：MMO **`≤ 7.5 nm`** | **`240 / 260 wph`**（200 mm `275`） | ASML 官方规格 & `ME3 TT-Ma-RS-Construction` L263–281 |
| **`XT:1000` / `XT:1060K`**（248 nm KrF，超高 NA 旗舰） | **0.93 NA** 折反物镜、≤ 80 nm、40 W 窄线宽 KrF、ILIAS/DoseMapper | 高速 XT 干式台（`~550–600 mm/s` 级） | `~2.2–2.4 m/s` 级 | 商业书未单列；由 `DCO ≤ 3.5 nm` 反推横向净 `Sync MA` 达 **`~0.8–1.2 nm`** 档 | `XT:1000`：DCO `~6` / MMO `~10 nm`<br>**`XT:1060K`：DCO `≤ 3.5 nm` / MMO `≤ 5.0 nm`** | `165` → **`≥ 205 wph`** | ASML 官方规格（`asml.com`）& SEC 披露 |

<a name="sec-4-4"></a>

### 4.4 ASML 官方手册实测明细：`AT/XT:850D`（WS Type-2 + RS D-spec）单台 `MA / MSD` 与 `TSDP` 限值

本机 `ME3` 仓库保存了 ASML 内部 Level 3 维护手册（`08-TT-L3-RSbook_v1.md` 与 `09-TT-L3-WSbook_v1.md`，明确标注为 **`AT/XT 850D & 1250D`** 通用基线模块 `WS Type-2` 与 `RS D-spec`），直接给出了 **罕见的原厂单台实测 `MA / MSD` 报表与工厂验收限值**：

| 子系统与原厂测试项 | 工况条件 | 自由度 | 实测 `MA` | 原厂 `MA` 限值 | 实测 `MSD` | 原厂 `MSD` 限值 | 折算至 1× 晶圆侧实测 `MA` | 对应 `ME3` 手册定位 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **WS（Type-2）`SWLF` 测试** | LFF 开、RS 静止（1× 晶圆侧） | `X`（pos.1 / pos.2） | **`0.62 / 0.50 nm`** | `1.50 nm` | **`4.44 / 4.10 nm`** | `5.00 nm` | **`0.62 / 0.50 nm`** | `09-TT-L3-WSbook` L5641–5649（Fig. 2.42） |
| **WS `SWLF` 镜架参考梁** | 经 MI 陷波滤波后 | `X / Y` | — | — | `4.14 / 3.44 nm` | `4.50 nm` | — | `09-TT-L3-WSbook` L5626–5635 |
| **RS（D-spec）`SRSM` 测试** | 静止（4× 掩模侧原始值） | `X / Y` | **`0.547 / 0.373 nm`** | `7.50 nm` | **`3.08 / 2.80 nm`** | `20.0 nm` | **`0.137 / 0.093 nm`** | `08-TT-L3-RSbook` L5001–5018 |
| **RS（D-spec）`SRSM` 测试** | 静止（角度与 Z） | `Rz` / `Z` | **`1.94 nrad` / `4.68 nm`** | `75 nrad` / `75 nm` | `9.73 nrad` / `25.4 nm` | `150 nrad` / `150 nm` | `1.94 nrad`（1:1）/ `0.29 nm`（1/16） | `08-TT-L3-RSbook` L5001–5018 |
| **RS（D-spec）`SRLF` 测试** | LFF 开、RS 静止（4× 侧） | `X / Y` | `0.48–0.61` / `0.34–0.43 nm` | `4.00 nm` | `2.00–2.74 nm` | `12.0 nm` | `0.12–0.15` / `0.09–0.11 nm` | `08-TT-L3-RSbook` L5320–5360 |
| **RS（D-spec）`SRLF` 测试** | LFF 开、**RS 步进后**（4× 侧） | `X / Y` | **`0.71`** / **`0.76–1.39 nm`** | `4.00 nm` | `3.55–3.62` / `4.90–5.09 nm` | `12.0 nm` | **`0.18`** / **`0.19–0.35 nm`** | `08-TT-L3-RSbook` L5320–5360 |
| **整机 `WS + RS` 联机 `TSDP`** | 满速扫描（`0.50` / `2.0 m/s`） | `X, Y` 净同步误差 | — | **`≤ 2.1 nm`**（`XT:1400 ≤ 2.0 nm`） | — | — | **`≤ 2.1 nm`**（ATP 规格） | `08-RSbook` L475；`09-WSbook` L413；`TT-Ma-RS` L281 |

**横跨三代 ASML 平台的规律总结**：从 `AT/XT:850D` 静止/步进单台实测可见，即便早在 2004 年的 KrF `XT` 机台上，**RS 折算至 1× 晶圆侧的自身 `MA`（`0.09–0.35 nm`）就已经显著小于 WS 自身 `MA`（`0.50–0.62 nm` 静止，扫描中因 H-bar 导轨与干涉仪气扰进一步放大至 `~1.5–2+ nm`）**——这与 2019 年 `[075]` 现代 ArFi 机台测得的 `WS 0.48 nm vs RS/4 0.11 nm`（约 4 : 1）一脉相承！正是这一跨越 i-line / KrF / ArF / ArFi 四代不变的物理不对称性，决定了 ASML 与 Nikon 始终以 **WS 为 Master、RS 为 Slave** 作为横向同步控制的核心架构。

---

<a name="sec-5"></a>

## 5. 对 OV4 子系统独立验收规格的工程反校与勘误备忘

[返回目录](#contents)

<a name="sec-5-1"></a>

### 5.1 为何独立 FAT 仍须坚持解耦预算而不放宽 WS 上限

尽管第 1–4 章证实无论是在 `XT`（i-line/KrF）还是 `NXT`（ArFi）上，“主从/双向耦合都可以让同步 `MA` 显著小于 WS 独立误差”，在整机对子系统下达独立 FAT 验收合同时（例如本仓库 [NXT:1965Ci 主报告 v1](NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v1.md) 设定的 `WS-X/Y ≤ 0.38/0.39 nm`、`RS-X/Y ≤ 1.12/1.18 nm`，以及紧缩 `v2` 基线的 `0.32/0.36 nm`），**仍必须坚持按保守解耦（$\rho = 0$）分配**，理由有四：

1. **子系统独立解耦定责与整机裕度储备**：`[075]` Sec. 1 明确指出，解耦子系统预算（$\rho = 0$）是保证各模块独立定责的工程基石；整机联调开启 `WS → RS` 前馈或双向耦合获得的 2×–4× `MA` 压降，应留作应对实际产线工艺扰动与老化漂移的**整机套刻系统裕度**。
2. **双台机 M-side 完全无 RS 陪跑**：在 TWINSCAN 架构中，晶圆对准（SMASH）与调平测量在 M-side 由 WS 独立执行，无 RS 同步抵消。若放任 WS 独立重复性放大，M-side 网格采样与换台定位误差将直接击穿顶层红线。
3. **4× 动力学惩罚与高频水床 `MSD` 劣化硬边界**：RS 追随 WS 需承受 4× 行程/速度/加速度放大，且高频结构柔性模态不确定性迫使鲁棒耦合滤波器滚降（`[075]` Fig. 14–16）；同时 `[022]` Eq. 46 与 `[075]` Table 1 证明，低频 `MA` 压得越狠，高频水床放大越剧烈，直接推高 **`MSD`（`2.88 → 3.33 nm`）**、劣化成像对比度与 CDU。
4. **跨代实测比例印证预算权重合理性**：无论是 KrF `XT:850D`（WS `0.50–0.62 nm` vs RS/4 `0.09–0.15 nm`）还是 ArFi `[075]`（WS `0.48 nm` vs RS/4 `0.11 nm`），WS 与 RS/4 的低频误差比均约 `4 : 1`（方差比约 `16 : 1`），说明独立考核中给 WS 分配远大于 RS/4 的方差占比（本仓 `64% : 36%`）完全符合重质量 WS 与轻量化 4× RS 的物理规律。

<a name="sec-5-2"></a>

### 5.2 前期 `v2` 说明书第 1.3 节主从方向表述勘误备忘

在既有正式文档 [九大核心子系统验收指标推导与计算说明书_v2.md](NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md) 第 1.3 节第 ④ 条及 [总报告 v2](NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md) 第 3.1 节注记中，曾简略表述为*“实际常将大扰动 RS 误差前馈给轻量化 WS”*。经本次逐一核验 `[S14]` ASML `US 6,373,072 B1`、`[S12]` Nikon `US 2012/0319637 A1`、`[090]`、`[085]`、`[078]`、`[147]`、`[022]` 与 `[075]` 原文，**该处主从流向表述已在新发布的 [NXT:1965Ci 主报告 v1](NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v1.md) 中正式勘误为**：

> **标准修订口径**：无论是 ASML `PAS 5500`、`TWINSCAN XT`（i-line/KrF/ArF）还是 `NXT`（ArFi）及 Nikon `NSR` 系列，横向同步主流均为 **WS 为 Master、更轻且更高带宽的 RS 为 Slave**（ASML 在高带宽 NXT 上进一步扩展为低中频仍由 RS 追随 WS 的双向 Double-Youla 耦合 `[075]`）；之所以仍不能免除 WS 自身独立验收，是因为受 **4× 行程/加速度/推力放大、高频结构模态不确定性鲁棒滚降及前馈水床效应（`MSD` 劣化）** 约束，RS 仅能在有限低中频段对 WS 做有限度补偿，且双台 M-side 无 RS 参与。

---

<a name="sec-6"></a>

## 6. 参考文献总清单与下载状态（本地已有 / 已自动下载 / 手动下载清单）

[返回目录](#contents)

<a name="sec-6-1"></a>

### 6.1 A 类：本机 OV4 / ME3 既有文献与手册库已就位（18 篇论文 + 4 份 ASML 手册，无需重复下载）

> 论文均已完整留存于本机只读目录 `D:\work\OV4\参考文献-整理版\`（或 `参考文献_新增\`）并在 [REFERENCES.md](../../REFERENCES.md) 登记 SHA-256；ASML `TWINSCAN` 官方维护手册位于本机只读目录 `D:\work\ME3\参考文献\Markdown_v1\`。

| 引用编号 | 本机目录与原件文件名 | 完整书目信息（作者 / 标题 / 出处 / 年份） | 本报告核心支撑点 | 状态 |
| :---: | :--- | :--- | :--- | :---: |
| **`[075]`** | `OV4/参考文献-整理版/075_1_s2.0_S0967066118306488_main.pdf` | E. Evers, M. van de Wal (ASML), T. Oomen (TU/e), *Beyond decentralized wafer/reticle stage control design: A double-Youla approach for enhancing synchronized motion*, *Control Engineering Practice* 83, pp. 21–32 (2019) | Fig. 12–13 & Table 1：WS 独立 `~0.48 nm`、RS 独立 `~0.11 nm`、无耦合 `MA = 0.565 nm` → 耦合 `0.108/0.200 nm`、`MSD 2.88 → 3.33 nm` | **已在本机** |
| **`[022]`** | `OV4/参考文献-整理版/022_1-s2.0-S0967066113001536-main.pdf` | M. F. Heertjes (TU/e), B. Temizer (ASML), M. Schneiders (JPE), *Self-tuning in master–slave synchronization of high-precision stage systems*, *Control Engineering Practice* 21(12), pp. 1706–1715 (2013) | Sec. 2 定义 WS=Master/RS=Slave；Sec. 6 & Fig. 10 实机 `MA 2.92 → 1.55 nm`、WS `e_m ≈ 5.9 nm` vs 同步 `4.0 nm` rms；Eq. 46 前馈水床效应 | **已在本机** |
| **`[147]`** | `OV4/参考文献-整理版/147_data_based_motion_control_of_wafer_scanners.pdf` | M. F. Heertjes (ASML / TU/e), *Data-based motion control of wafer scanners*, *IFAC-PapersOnLine* 49(13), pp. 1–12 (2016) | Sec. 4.2 & Fig. 6–8：WS→RS 同步框图与 `543.7–588.2 Hz` 带宽；Fig. 5 短行程 WS 6-DOF 扫描误差 | **已在本机** |
| **`[078]`** | `OV4/参考文献-整理版/078_2008_Mishra_ILC_Synchronization_WS_RS.pdf` | S. Mishra, W. Yeh (NRCA), M. Tomizuka (UC Berkeley), *Iterative Learning Control Design for Synchronization of Wafer and Reticle Stages*, *Proc. ACC*, pp. 3908–3913 (2008) | 阐明 RS 更轻、带宽高于 WS，采用 WS=Master、RS=Slave（ $`r_r = \mathbf{S} y_w`$ ）主从 ILC 同步 | **已在本机** |
| **`[090]`** | `OV4/参考文献-整理版/090_Fujipress_IJAT-2-2-5.pdf` | Y. Shibazaki (Nikon Corp.), *Realization of Tubeless Stage in Semiconductor Exposure System*, *IJAT* 2(2), pp. 86–92 (2008) | Nikon ArF `NSR-S308F` 总师明确声明：公司采用 **RS 跟随 WS** 的主从控制方法 | **已在本机** |
| **`[085]`** | `OV4/参考文献-整理版/085_52_425.pdf` | 後藤太邦・湯浅匡夫 (Nikon Corp.), *半導体露光装置の制御技術（NSR-620D）*, *計測と制御 (SICE)* 52(5), pp. 425–430 (2013) | 明确 ArFi `NSR-S620D` 为 RS 追随 WS 同步（Eq. 8–9），ILC 后同步达 `0.5 nm` 级 | **已在本机** |
| **`[063]`** | `OV4/参考文献-整理版/063_76401O.pdf` | H. Nakano 等 (Nikon Corp.), *NSR-S620D immersion scanner performance*, *Proc. SPIE* 7640, 76401O (2010) | Fig. 14 同步 `MA < 0.6/0.6/4 nm`、`MSD < 2.5/3/6.5 nm`；Fig. 15 曝光级 Stage Repeatability `0.96–1.60 nm` | **已在本机** |
| **`[009]`** | `OV4/参考文献-整理版/009_76401N.pdf` | T. Castenmiller 等 (ASML), *Towards ultimate optical lithography with NXT:1950i dual stage immersion platform*, *Proc. SPIE* 7640, 76401N (2010) | Fig. 3 Stage Positioning 拆解；Fig. 9–10 对比 XT H-bar 与 NXT 磁浮 WS（质量降 ~3×、首阶模态 +40%）；`Sync MA = 0.47/0.49 nm` | **已在本机** |
| **`[066]`** | `OV4/参考文献-整理版/066_86831L.pdf` | I. Bouchoms 等 (ASML), *Extending immersion lithography down to 1x nm production nodes*, *Proc. SPIE* 8683, 86831L (2013) | Fig. 9 陶瓷短行程 WS `800 mm/s` 扫描 `MAz` 峰值 `4 nm`（95% `≤ 6 nm`） | **已在本机** |
| **`[015]`** | `OV4/参考文献-整理版/015_978011.pdf` | ASML, *NXT:1980Di immersion scanner for 7nm production nodes*, *Proc. SPIE* 9780, 978011 (2016) | `NXT:1980Di` 全片焦面 `FU < 9.1 nm (3σ)`、`MMO < 2.0 nm`、产能 `> 275 wph` | **已在本机** |
| **`[018]`** | `OV4/参考文献-整理版/018_nikon_nsr_s630d_immersion.pdf` | Nikon Corp., *Immersion Scanners Enabling 10 nm half pitch Production and Beyond (NSR-S630D)*, *Proc. SPIE* (2014) | `NSR-S630D` RS 升级编码器伺服、`SMO = 1.7 nm`、`MMO = 2.5 nm` | **已在本机** |
| **`[064]`** | `OV4/参考文献-整理版/064_79730Z.pdf` | M. Yasuda 等 (Nikon Corp.), *Stability and Calibration of Overlay and Focus Control for a Double Patterning Immersion Scanner*, *Proc. SPIE* 7973, 79730Z (2011) | `NSR-S620D` 混合编码器+干涉仪（Bird's Eye Control）测量重复性与稳定性 | **已在本机** |
| **`[019]`** | `OV4/参考文献-整理版/019_Control_of_Wafer_Scanners_Methods_and_Developments.pdf` | M. Heertjes, H. Butler 等 (ASML / TU/e / Cymer), *Control of Wafer Scanners: Methods and Developments*, *Proc. ACC* (2020) | ASML 官方控制综述，引证 `[022]` 与 `[M2]` 作为工业台同步代表 | **已在本机** |
| **`[094]`** | `OV4/参考文献-整理版/094_Position_Control_in_Lithographic_Equipment_Applications_of_Control.pdf` | H. Butler (ASML), *Position Control in Lithographic Equipment*, *IEEE Control Systems Magazine* 31(5), pp. 28–47 (2011) | 三代步进/扫描台控制演进、L587 明确列举 `stage-to-stage feedforward` 与物镜加速度前馈 | **已在本机** |
| **`[256]`** | `OV4/参考文献-整理版/256_performance_of_a_step_and_scan_system_for_duv_lithogr.pdf` | G. de Zwart, M. van den Brink, H. Butler 等 (ASML), *Performance of a Step and Scan System for DUV Lithography (PAS 5500/500)*, *Proc. SPIE* 3051 (1997) | **【v2 新增】** `PAS 5500/500` KrF 实测 WS `250 mm/s`、RS `1000 mm/s`、同步峰值 `MA = 8 nm` / `MSD = 22 nm`、Stage OVL `12/23 nm` | **已在本机** |
| **`[266]`** | `OV4/参考文献-整理版/266_performance_results_300mm_twinscan_lithography.pdf` | B. Sluijk, T. Castenmiller 等 (ASML), *Performance results of a new generation of 300 mm lithography systems (TWINSCAN AT:750)*, *Proc. SPIE* 4346 (2001) | **【v2 新增】** 首代双台 KrF `AT:750` 实测 `250 mm/s`、`8 m/s²`、双台串扰 `< 0.85 nm MA`、Stage 精度 `4 nm`、SMO `8–13 nm` | **已在本机** |
| **`[006]`** | `OV4/参考文献-整理版/006_asml_iwaps_2018_scanner_innovations.pdf` | ASML, *Scanner Innovations for Advanced Lithography*, *IWAPS 2018*, Xiamen (2018) | **【v2 新增】** Slide 16–17 官方路线图：`XT:400K/L`（`230 wph / 20 nm`）、`XT:400M`（新型工件台 `250 wph / 15 nm`）与 `NXT` 干式下放 | **已在本机** |
| **`[N8]`** | `OV4/参考文献_新增/Frequency-Domain_Properties_of_Moving_Average_and_Moving_Standard_Deviation_with_Application_to_Stage_Motion_Control.pdf` | M. Heertjes (TU/e / ASML), *Frequency-domain properties of moving average and moving standard deviation*, *2024 IEEE ECC*, pp. 3521–3526 (2024) | 狭缝 `MA`/`MSD` 频域互补功率谱定理与 CPS 验证（工业台 $\tau_{\mathrm{slit}} = 9.2\text{ ms}$） | **已在本机** |
| **`[ME3-1..4]`** | `ME3/参考文献/Markdown_v1/`（`Level1/01_AP-L1-Hardware_Introduction`、`Level2/TT-PM-WS-3v1`、`Level3/08-TT-L3-RSbook`、`Level3/09-TT-L3-WSbook`、`TT-Ma-RS-Construction`） | ASML 官方 `TWINSCAN` Level 1/2/3 内部工程与维护手册（2003–2007，覆盖 `AT:400/750/850` 与 `XT:850D/1250D/1400`） | **【v2 核心铁证】** `AT:400/750/850` 完整规格表；`TSPE` GUI **`Stages Error Coupling` (`Automatic/On/Off`)**；`SWLF`/`SRLF`/`SRSM` 单台实测报表与 `TSDP ≤ 2.1 / 2.0 nm` | **已在本机** |

<a name="sec-6-2"></a>

### 6.2 B 类：已自动下载至 `参考文献_新增\WS-RS同步\` 的官方专利原件（14 篇，含新增 `[S14]`）

> 全部经 USPTO 官方公共专利 PDF 接口直接下载并落盘至 **`D:\work\OV4\参考文献_新增\WS-RS同步\`**（受 `.gitignore` `/参考文献_新增/` 保护不上传至 GitHub），且全部 **14/14 篇完成封面/关键页视觉核验与 SHA-256 全库去重校验（100% 唯一，合计 375 页）**。

| 编号 | 专利号与权利人 | 本地保存文件名（位于 `参考文献_新增\WS-RS同步\`） | 页数 | SHA-256（前 12 位） | 核验后发明人与标题摘要 | 官方直链 | 下载状态 |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- | :---: |
| **`[S14]`** | **`US 6,373,072 B1`（ASML，v2 新增核心！）** | `ASML_US6373072B1_Butler_WS_ErrorFeedforward_to_RS.pdf` | 9 | `5498a5161270` | **Hans Butler, Thomas P. H. Warmerdam** — *Lithographic Projection Apparatus*（**1998 优先权 / 2002 授权，ASML `PAS 5500` & `TWINSCAN AT/XT` `WS → RS` 位置+$ms^2$ 加速度前馈奠基专利**，实测 `MA X 11.4→1.0 nm`、`MA Y 4.3→1.1 nm`） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6373072) | **已自动下载** |
| **`[S1]`** | `US 2004/0176861 A1`（ASML） | `ASML_US20040176861A1_Butler_WS_MassEstFeedforward.pdf` | 39 | `35bb9a8190d0` | Hans Butler — *System for Controlling a Position of a Mass*（WS 在线质量辨识 + 自适应加速度前馈，2004） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20040176861) | **已自动下载** |
| **`[S2]`** | `US 2006/0285101 A1`（ASML） | `ASML_US20060285101A1_Butler_Breukers_PS_Feedforward.pdf` | 14 | `de5eed816fde` | Hans Butler, E. H. J. Draaijer, M. J. E. G. Breukers — *Lithographic Apparatus...*（投影系统位置信号滤波前馈注入晶圆台，2006） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20060285101) | **已自动下载** |
| **`[S3]`** | `US 7,098,990 B2`（ASML） | `ASML_US7098990B2_Butler_StageAccelControl.pdf` | 14 | `0ffcf355053b` | Hans Butler — *Lithographic Apparatus...*（双支路加速度反馈抑外扰控制，2006） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7098990) | **已自动下载** |
| **`[S4]`** | `US 7,170,581 B2`（ASML） | `ASML_US7170581B2_SelfAdaptingFeedforwardTuning.pdf` | 14 | `4ad7c9f4d350` | Rob Tousain — *Self-Adapting Feedforward Control Tuning for Motion System*（速度/加速度/Jerk/Snap 自适应前馈，2007） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7170581) | **已自动下载** |
| **`[S5]`** | `US 7,181,296 B2`（ASML） | `ASML_US7181296B2_AdaptiveILC_LithoStage.pdf` | 24 | `0093a2f391c4` | A. I. Rotariu, R. Ellenbroek, M. Steinbuch, G. E. Van Baars — *Method of Adaptive Interactive Learning Control...*（2007） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7181296) | **已自动下载** |
| **`[S6]`** | `US 7,239,368 B2`（ASML） | `ASML_US7239368B2_UnflatnessFeedforwardOverlay.pdf` | 13 | `98d0744e4140` | R. Oesterholt 等 — *Using Unflatness Information of the Substrate Table or Mask Table...*（2007） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7239368) | **已自动下载** |
| **`[S7]`** | `US 7,405,811 B2`（ASML） | `ASML_US7405811B2_LithoPositioningApparatus.pdf` | 16 | `3079eb332226` | M. H. M. Beems, J. Sakai — *Lithographic Apparatus and Positioning Apparatus*（2008；已纠偏非 Nikon） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7405811) | **已自动下载** |
| **`[S8]`** | `US 8,279,401 B2`（ASML） | `ASML_US8279401B2_PositionControlComplianceFF.pdf` | 13 | `cba17490471b` | M. J. Vervoordeldonk, M. C. J. Baggen — *Position Control System...*（柔度补偿 + 加速度/Snap 前馈，2012） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8279401) | **已自动下载** |
| **`[S9]`** | `US 2004/0128918 A1`（Nikon） | `Nikon_US20040128918A1_ILC_StageSyncTracking.pdf` | 41 | `1892fe42639e` | P.-H. Yang, B. Yuan, S. Makinouchi, K. Hirano 等 — *Control System and Method for Improving Tracking Accuracy...*（2004） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20040128918) | **已自动下载** |
| **`[S10]`** | `US 2005/0231706 A1`（Nikon） | `Nikon_US20050231706A1_FeedforwardMILC_Grouping.pdf` | 25 | `5ffba327a38a` | P.-H. Yang, H. Hashimoto, B. Yuan 等 — *Feedforward Control with Reduced Learning Time...*（2005） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20050231706) | **已自动下载** |
| **`[S11]`** | `US 2006/0170382 A1`（Nikon） | `Nikon_US20060170382A1_LinearMotorForceRippleILC.pdf` | 34 | `89c5de51cb9f` | P.-H. Yang, H. Hashimoto, B. Yuan 等 — *Linear Motor Force Ripple Identification and Compensation with ILC*（2006） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20060170382) | **已自动下载** |
| **`[S12]`** | `US 2012/0319637 A1`（Nikon） | `Nikon_US20120319637A1_SyncControlDevicesMethods.pdf` | 72 | `8439247074ae` | **P.-H. Yang, K. Hirano, M. Yuasa** — *Synchronization Control Devices and Methods*（首页框图实锤 `wafer error → H(s) → reticle stage`，2012） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20120319637) | **已自动下载** |
| **`[S13]`** | `US 8,451,431 B2`（Nikon） | `Nikon_US8451431B2_IFT_SyncControlStages.pdf` | 47 | `a629cbaeabc2` | P.-H. Yang, S.-L. Koo — *Control Systems and Methods Applying Iterative Feedback Tuning...*（2013） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8451431) | **已自动下载** |

<a name="sec-6-3"></a>

### 6.3 C 类：需手动下载清单（8 篇，含精确 DOI / 专利号与下载链接）

> 以下 8 篇高价值论文/非 US 专利因出版商付费墙（IEEE Xplore / Elsevier）或非 US 专利站点对脚本限流未能自动拉取。建议在具备校园/机构权限或普通浏览器环境下手动下载，并统一保存至 **`D:\work\OV4\参考文献_新增\WS-RS同步\`**。

| 编号 | 优先级 | 完整书目 / 专利信息 | 精准 DOI 或专利检索链接 | 未自动下载原因 | 建议保存文件名 |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **`[M1]`** | **P0（高）** | C. J. H. Lambregts, M. F. Heertjes, B. J. van der Veek (ASML / TU/e), *Multivariable feedback control in stage synchronization*, *Proc. 2015 ACC*, pp. 4149–4154 (2015) | DOI: [10.1109/ACC.2015.7171980](https://doi.org/10.1109/ACC.2015.7171980) | IEEE Xplore 付费墙（非 OA） | `ASML_Lambregts_2015_ACC_MultivariableStageSync.pdf` |
| **`[M2]`** | **P0（高）** | M. F. Heertjes, M. Galluzzo, L. Kuindersma (ASML / TU/e), *Robust Data-Driven Control for the Stage Synchronization Problem*, *IFAC Proceedings Volumes* 47(3), pp. 1134–1139 (2014) | DOI: [10.3182/20140824-6-ZA-1003.00625](https://doi.org/10.3182/20140824-6-ZA-1003.00625) · [TU/e 记录页](https://research.tue.nl/en/publications/00df834d-6de4-4e6b-98ff-328d1e7ddaa0) | ScienceDirect 拦截脚本请求（403） | `ASML_Heertjes_2014_IFAC_RobustStageSync.pdf` |
| **`[M3]`** | **P0（高）** | V. A. Looijen, M. F. Heertjes (TU/e / ASML), *Robust Synchronization of Motion in Wafer Scanners Using Particle Swarm Optimization*, *2018 IEEE CCTA*, pp. 1102–1107 (2018) | DOI: [10.1109/CCTA.2018.8511380](https://doi.org/10.1109/CCTA.2018.8511380) | IEEE Xplore 付费墙（非 OA） | `ASML_Looijen_2018_CCTA_RobustMotionSync.pdf` |
| **`[M4]`** | **P1（中）** | M. O. Navarrete, M. F. Heertjes, R. H. Munnig Schmidt (TU Delft / ASML), *Common zeros in synchronization of high-precision stage systems*, *2015 IEEE ICM*, pp. 602–607 (2015) | DOI: [10.1109/ICMECH.2015.7084045](https://doi.org/10.1109/ICMECH.2015.7084045) | IEEE Xplore 付费墙（非 OA） | `ASML_Navarrete_2015_ICM_CommonZerosSync.pdf` |
| **`[M5]`** | **P1（中）** | H. Butler (ASML / TU/e), *Feedforward signal prediction for accurate motion systems using digital filters*, *Mechatronics* 22(6), pp. 827–835 (2012) | DOI: [10.1016/j.mechatronics.2012.05.002](https://doi.org/10.1016/j.mechatronics.2012.05.002) | Elsevier 付费墙（非 OA） | `ASML_Butler_2012_Mechatronics_FFPrediction.pdf` |
| **`[M6]`** | **P1（中）** | M. F. Heertjes, B. J. C. H. van der Velden, T. A. Oomen (ASML / TU/e), *Constrained Iterative Feedback Tuning for Robust Control of a Wafer Stage System*, *IEEE TCST* 24(1), pp. 56–66 (2016) | DOI: [10.1109/TCST.2015.2418311](https://doi.org/10.1109/TCST.2015.2418311) · [TU/e 记录页](https://research.tue.nl/en/publications/4e608fc7-18d7-4c15-ab2d-557c329de354) | IEEE Xplore 付费墙 | `ASML_Heertjes_2016_TCST_ConstrainedIFT_WS.pdf` |
| **`[M7]`** | **P1（中）** | ASML Netherlands B.V.（发明人 H. Butler, M. J. E. G. Breukers, M. F. Heertjes），欧洲/荷兰同步控制专利族 `EP 13198925.3` / `NL 2013810`（2013 优先权） | [Espacenet 检索](https://worldwide.espacenet.com/patent/search?q=pn%3DNL2013810) · [Google Patents 检索](https://patents.google.com/?q=NL2013810+Heertjes) | 非 US 专利（不在 USPTO 库） | `ASML_NL2013810_Butler_Breukers_Heertjes.pdf` |
| **`[M8]`** | **P2（参考）** | 上海微电子装备有限公司（SMEE，吴立伟、杨晓燕），《工件台和掩模台的同步控制方法及其系统》，授权发明专利 `CN 103135357 B` | [Google Patents 中文页](https://patents.google.com/patent/CN103135357B/zh) | 非 US 专利（CNIPA） | `SMEE_CN103135357B_WS_RS_SyncControl.pdf` |
