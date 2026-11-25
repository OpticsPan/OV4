# ArF / ArFi 光刻机 WS–RS 同步控制策略（主从方向）与单台重复性误差专项调研报告（v1）

[仓库首页](../../README.md) · [成果索引](../README.md) · [参考文献总目](../../REFERENCES.md) · [九大子系统说明书 v2](NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md) · [15 大类总报告 v2](NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md) · [总变更记录](../../CHANGELOG.md)

> **报告定位**：本报告针对 ArF / ArFi 步进扫描光刻机（对标 ASML `TWINSCAN XT/NXT` 与 Nikon `NSR-S3xx/S6xx` 平台）中三个关键工程疑问展开一手文献与官方专利原件核查：
> 1. 已知整机 WS–RS 同步误差 `Sync MA = 0.47 nm` 时，WS 或 RS 自身独立工作下的重复性/伺服误差是否必然小于 `0.47 nm`？
> 2. 在 ArF / ArFi 机台同步策略中，ASML 与 Nikon 究竟以哪一台作为 Master（主台）、哪一台作为 Slave（从台）？
> 3. 公开专利与原厂控制论文中，WS 与 RS 各自独立的伺服/重复性实测数据究竟处于什么量级，对本仓库 `WS-X ≤ 0.32 nm` / `RS-X ≤ 0.96 nm` 子系统独立 FAT 规格有何启示？
>
> **文献下载与核验状态**：本报告共引用 **36 篇一手文献与专利**，其中 **15 篇**已在本机基线库（`参考文献-整理版/` 与 `参考文献_新增/`）就位，**13 篇官方 USPTO 美国专利原件（8 篇 ASML + 5 篇 Nikon，合计 366 页）**已自动下载至本机 `D:\work\OV4\参考文献_新增\WS-RS同步\` 并完成封面视觉核验与 SHA-256 唯一性登记，另 **8 篇**（受 IEEE/Elsevier 付费墙或非 US 专利站点脚本限流限制）整理于第 5.3 节手动下载清单。

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
- [4. 对 OV4 子系统独立验收规格的工程反校与勘误备忘](#sec-4)
  - [4.1 为何独立 FAT 仍须坚持解耦预算（`WS-X ≤ 0.32 nm`）而不放宽 WS 上限](#sec-4-1)
  - [4.2 前期 `v2` 说明书第 1.3 节主从方向表述勘误备忘](#sec-4-2)
- [5. 参考文献总清单与下载状态（本地已有 / 已自动下载 / 手动下载清单）](#sec-5)
  - [5.1 A 类：本机 OV4 既有文献库已下载（15 篇，无需重复下载）](#sec-5-1)
  - [5.2 B 类：本次已自动下载至 `参考文献_新增\WS-RS同步\` 的官方专利原件（13 篇）](#sec-5-2)
  - [5.3 C 类：需手动下载清单（8 篇，含精确 DOI / 专利号与下载链接）](#sec-5-3)

---

<a name="sec-0"></a>

## 0. 执行摘要与核心结论速览

[返回目录](#contents)

| 核心调研问题 | 核验后明确结论 | 最硬核一手证据来源 |
| :--- | :--- | :--- |
| **1. 若已知同步 `MA = 0.47 nm`，单台 WS 或 RS 重复性是否必然 `< 0.47 nm`？** | **不一定！**不仅数学上完全允许，而且在工业 ArF/ArFi 光刻机中，**WS 独立误差大于同步相对误差 `|WS − RS/4|`** 是主从/耦合同步控制刻意实现的结果（实测可大 **2.4–4.4 倍**）。 | `[075]` Evers/ASML (*CEP* 2019) Fig. 12–13 & Table 1；`[022]` Heertjes/ASML (*CEP* 2013) Fig. 10 |
| **2. ArF / ArFi 横向（X / Y / Rz）同步策略中，谁是 Master、谁是 Slave？** | **ASML 与 Nikon 高度一致：单向主从均以 WS 为 Master、RS 为 Slave**；ASML 进一步向双向 Double-Youla 耦合演进，但在决定套刻 `MA` 的低中频段（`< 250–400 Hz`）仍是 **RS 主动复现并追随 WS 误差**。 | Nikon `[S12]` `US 2012/0319637 A1` 首页框图、`[090]` Shibazaki (*IJAT* 2008)、`[085]` `NSR-S620D`；ASML `[147]` Fig. 6、`[022]`、`[075]` |
| **3. Z / Rx / Ry 焦面自由度的主从方向是否相同？** | **不同！**液浸轴向缩小倍率为 $1/11.14$，RS-Z 无法高速追随硅片形貌，故 **Z/Rx/Ry 调平由 WS 独立伺服**；掩模不平度则经静态/低频映射前馈给 WS 或物镜补偿。 | `[S6]` ASML `US 7,239,368 B2`、`[066]` Fig. 9、本仓说明书 v2 第 2.1 节 |
| **4. 工业实测的 WS 与 RS 独立（无耦合）误差各为多少？** | 商业手册不单列单台 FAT 指标；控制论文实测无耦合 `≤ 100 Hz`（`MA` 频段）：**WS 约 `0.48 nm`**、**RS 折算晶圆侧仅 `~0.11 nm`**（掩模 4× 侧约 `0.44 nm`，WS : RS/4 约 4 : 1）；全频段 WS 约 `3.32 nm`、RS 折算约 `2.40 nm`。 | `[075]` Fig. 12 & Table 1；`[022]` Fig. 10；`[147]` Fig. 5；`[066]` Fig. 9 (`MAz` 峰值 `4 nm`) |
| **5. 既然同步能把大误差 WS 压低，为何本仓 FAT 仍须要求 `WS-X ≤ 0.32 nm`？** | ① 独立 FAT 须按解耦（$\rho = 0$）考核定责，将耦合红利留作整机裕度；② 双台机 M-side 对准/调平无 RS 陪跑；③ 过度让 RS 追随 WS 会触发 4× 推力惩罚与高频水床效应（`MSD` 劣化成像对比度）。 | `[075]` Sec. 1 & Table 1（`MSD` `2.88 → 3.33 nm`）；`[022]` Eq. 46；`[009]` M-side 架构 |

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
- **物理共模扰动（自然机制）**：同一计量框架（Metrology Frame）或地基低频微振、同相扫描加减速轨迹引发的同类伺服滞后，在 $`e_{\mathrm{WS}} - e_{\mathrm{RS}}/4`$ 做差时天然部分抵消。

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
   - **`[S10]` `US 2005/0231706 A1`**（25 页，P.-H. Yang 等，2005）：视场分组多遍迭代学习前馈（MILC），同时被 ASML `US 7,170,581 B2` 与 Nikon `US 8,451,431 B2` 引证。
   - **`[S11]` `US 2006/0170382 A1`**（34 页，P.-H. Yang 等，2006）：直线电机推力波动 ILC 补偿（`[085]` 引用）。
   - **`[S13]` `US 8,451,431 B2`**（47 页，P.-H. Yang & S.-L. Koo，2013）：采用迭代反馈整定（IFT）联合优化前馈与两台同步控制参数（同时被 ASML `[147]` L719 引用）。
   - 配合 Nikon Research (NRCA) / UC Berkeley 论文 `[078]`（Mishra, Yeh & Tomizuka, *ACC* 2008，L37），完整阐明物理第一性原理：**RS 更轻、闭环带宽远高于大质量 300 mm WS**，故以 WS 实测位置乘倍率驱动 RS 追随。

<a name="sec-2-2"></a>

### 2.2 ASML 路线：由单向 WS→RS 主从演进至双向 Double-Youla 耦合

ASML（Veldhoven 控制团队 + TU/e 合作组）的文献与专利链显示出清晰的两阶段技术演进，且两个阶段在决定 `MA` 的低中频段均以 **RS 追随 WS** 为核心：

1. **阶段一：工业单向主从前馈（WS = Master，RS = Slave）**：
   - **`[022]` Heertjes (TU/e), Temizer (ASML) & Schneiders (*CEP* 2013，L49–L71)**：显式指定 WS 为 Master（误差 $e_m$）、RS 为 Slave，利用自整定双 FIR 同步滤波器（位置设定点滤波器 $`\mathcal{C}_p`$ + 前馈力滤波器 $`\mathcal{C}_q`$）强制 RS 追踪 $e_m$。
   - **`[147]` M. F. Heertjes（ASML Netherlands B.V.，*IFAC* 2016，Sec. 4.2 & Fig. 6–8）**：将该机制直接命名为 **“wafer-to-reticle stage synchronization”**，结构图 Fig. 6 明确以 WS 输出 $`y_{\mathrm{ws}}`$ 驱动双前馈滤波器 $`\mathcal{F}_1(\boldsymbol{\rho}), \mathcal{F}_2(\boldsymbol{\rho})`$ 注入 RS 伺服环（$`\mathcal{P}_{\mathrm{rs}}, \mathcal{C}_{fb}^{rs}`$），实测同步前馈带宽（$`\vert\mathcal{S}_{\mathrm{ff}}\vert = 0\text{ dB}`$）高达 **`543.7–588.2 Hz`**。
2. **阶段二：高带宽 WS 时代的双向耦合（WS→RS + RS→WS）**：
   - **`[M1]` Lambregts, Heertjes & van der Veek（ASML / TU/e，*ACC* 2015）** 指出：随着 NXT 轻量化磁浮平面电机使 WS 带宽大幅提高（如 `[009]` 披露 NXT WS 第一阶模态较 XT 提升 40%），在传统单向 WS→RS 同步之上叠加反向 RS→WS 耦合，构成多变量 $\mathcal{H}_\infty$ 双向耦合控制。
   - **`[075]` Evers, van de Wal (ASML) & Oomen (*CEP* 2019)** 进一步建立保证鲁棒稳定性的 **双向 Double-Youla 耦合框架**；但从其工业扫描机实测累积误差曲线（Fig. 12）可见，在 `< 250–400 Hz` 的 `MA` 主导频段，**依然是 RS 主动复现 WS 的误差轨迹**（原文图注：*“To achieve stage synchronization the reticle stage is synchronized to the wafer stage”*）。
3. **ASML 配套核心专利群（8 篇官方 USPTO 原件已全部下载本地 `[S1]–[S8]`）**：
   - **`[S8]` `US 8,279,401 B2`**（Vervoordeldonk & Baggen，2012，`[147]` 引用）：位置控制系统中集成结构柔度补偿（Compliance Compensation）与加速度/Snap 前馈。
   - **`[S2]` `US 2006/0285101 A1`**（Hans Butler, Draaijer & Breukers，2006）：投影系统位置信号滤波与前馈注入晶圆台伺服环，抑制框架相对振动误差。
   - **`[S1]` `US 2004/0176861 A1`**（Hans Butler，2004，对应 `[088]`）与 **`[S3]` `US 7,098,990 B2`**（Hans Butler，2006）：晶圆台在线质量辨识自适应加速度前馈及外扰加速度抑制控制。
   - **`[S4]` `US 7,170,581 B2`**（Rob Tousain，2007）：工作台速度/加速度/Jerk/Snap 多阶自适应前馈系数在线学习。
   - **`[S5]` `US 7,181,296 B2`**（Rotariu, Ellenbroek, Steinbuch & Van Baars，2007）：面向变扫长光刻扫描台的时频自适应迭代学习控制（Adaptive ILC）。
   - **`[S6]` `US 7,239,368 B2`**（Oesterholt 等，2007）：利用衬底台或掩模台面形不平度（Unflatness）映射进行扫描曝光前馈补偿。
   - **`[S7]` `US 7,405,811 B2`**（Beems & Sakai，2008）：基于中间结构短程双测量系统的晶圆台高精度定位测量架构。
   - 另含欧洲/荷兰专利族 **`[M7]` `EP 13198925.3` / `NL 2013810`**（Hans Butler, Marcus Breukers, Marcel Heertjes，2013 优先权，多运动体同步定位控制）及国内 SMEE 旁证专利 **`[M8]` `CN 103135357 B`**（同样采用将工件台伺服误差转换后前馈注入掩模台力信号的主从逻辑）。

<a name="sec-2-3"></a>

### 2.3 专利检索避坑与多自由度主从方向辨析

1. **专利中 `"master"` 一词的三重歧义**：ASML 与 Nikon 的正式专利权利要求书极少直接写 `"master stage / slave stage"`。检索时遇到 `"master"`，需仔细区分其语境是指 ① **掩模原版（pattern master）**、② **单台内部的“短行程（Master）–长行程（Slave）/ 平衡质量块”**，还是 ③ **传感器通信总线主从时钟**；真正的跨台同步控制多表述为 *"first/second movable body"*、*"synchronization target filter"*、*"tracks the position-error data"*。
2. **自由度维度差异（横向 X/Y/Rz vs 焦面 Z/Rx/Ry）**：
   - **X / Y / Rz（面内套刻）**：WS = Master，RS = Slave（或低中频 RS 追随 WS 的双向耦合）。
   - **Z / Rx / Ry（轴向焦面调平）**：由于液浸物镜轴向缩小倍率为 $`n_w \beta^2 = 1.4366 / 16 = 1 / 11.14`$，RS-Z 位移对像面焦深几乎没有高速调平能力，因此 **硅片起伏跟随由 WS-Z/Rx/Ry 独立伺服**；而掩模弯曲/不平度（如 `[S6]` `US 7,239,368 B2`）则是以静态/低频映射前馈给 WS 或投影物镜补偿。
3. **官方原件核验纠偏记录**：在线检索摘要曾将 `US 7,405,811 B2` 误标为 Nikon / Yuichi Shibazaki，亦曾将 Nikon 的 `US 8,451,431 B2` 误归为 ASML；本次通过下载并视觉核验 USPTO 官方 PDF 首页（Page 1），已 100% 确证 **`US 7,405,811 B2` 权利人为 ASML Netherlands B.V.（Beems & Sakai）**、**`US 8,451,431 B2` 权利人为 Nikon Corporation（Yang & Koo）**、**`US 8,279,401 B2` 发明人为 Vervoordeldonk & Baggen（ASML Netherlands B.V.）**。

---

<a name="sec-3"></a>

## 3. ArF / ArFi 机台 WS / RS 独立误差与同步重复性公开实测数据

[返回目录](#contents)

<a name="sec-3-1"></a>

### 3.1 商业规格书披露边界与数据来源说明

ASML（`NXT:1950i / 1970Ci / 1980Di / 2000i`）与 Nikon（`NSR-S620D / S630D / S635E / S636E`）在对外商业规格书和常规 SPIE 机型汇报中，**从不单独公布 WS 或 RS 的子系统独立 FAT 重复性指标**——对外仅承诺整机 `DCO / SMO / MMO`，偶见同步扫描误差 `|WS − RS/4| MA / MSD` 以及光刻胶双次曝光法测得的 `Stage Repeatability`。真正可查到 **WS 与 RS 各自独立（无耦合）伺服误差** 的一手数据，主要来源于原厂控制工程师在 *Control Engineering Practice*、*IFAC*、*IEEE* 及专题 *SPIE* 发表的实机曲线。

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

| 商业 ArFi 机型（NA = 1.35） | 文献出处 | 同步扫描误差 `|WS − RS/4|`（`MA` / `MSD`） | 曝光级 Stage Repeatability / Stage Positioning 分项 |
| :--- | :--- | :--- | :--- |
| **ASML `NXT:1950i`**（`175 wph`） | `[009]` Fig. 3 & Fig. 10 | **`Sync MA-X = 0.47 nm`**<br>**`Sync MA-Y = 0.49 nm`** | Fig. 3 DCO 拆解中 **Stage Positioning 分项 `~0.50 nm`**（较 `XT:1900Gi` 的 `~1.6 nm` 压降 3×，整机 `DCO = 2.5 nm`） |
| **ASML `NXT:1970Ci / 1980Di`**（`250–275 wph`） | `[066]` Fig. 9 & `[015]` Fig. 4–7 | WS 陶瓷短行程 `MAz` 峰值 `4 nm`（95% `≤ 6 nm`）；整机 `FU < 9.1 nm (3σ)`、`MMO < 2.0 nm` | 商用手册未单独拆出横向 `Sync MA`，由 `DCO ≤ 1.6 nm` 反推横向同步 `MA` 处于 `~0.30–0.35 nm` 档位 |
| **Nikon `NSR-S620D`**（`700 mm/s`） | `[063]` Fig. 14–15 & `[085]` L109 | 零整定时间实测：<br>**`MA-X < 0.6 nm`、`MA-Y < 0.6 nm`、`MA-Z < 4 nm`**<br>**`MSD-X < 2.5 nm`、`MSD-Y < 3.0 nm`、`MSD-Z < 6.5 nm`**（`[085]` 记为 `0.5 nm` 档） | **单片不卸载双次曝光套刻差 `3σ`**（含 WS+RS+编码器两遍合成，单遍等效 $\div\sqrt{2}$）：<br>• `320 mm/s`：**`0.96 / 1.20 nm`**（单遍 `~0.68 / 0.85 nm`）<br>• `500 mm/s`：**`1.56 / 1.45 nm`**（单遍 `~1.10 / 1.03 nm`）<br>• `700 mm/s`：**`1.60 / 1.49 nm`**（单遍 `~1.13 / 1.05 nm`） |
| **Nikon `NSR-S630D`**（`250 wph`） | `[018]` Fig. 3–6 | 引入 RS 编码器伺服取代干涉仪；`SMO = 1.7 nm`、`MMO = 2.5 nm`、`FU < 15 nm` | 未单独公开单台重复性数值 |

---

<a name="sec-4"></a>

## 4. 对 OV4 子系统独立验收规格的工程反校与勘误备忘

[返回目录](#contents)

<a name="sec-4-1"></a>

### 4.1 为何独立 FAT 仍须坚持解耦预算（`WS-X ≤ 0.32 nm`）而不放宽 WS 上限

尽管前文证实“主从/双向耦合可以让同步 `MA` 显著小于 WS 独立误差”，在整机对子系统供应商下达独立 FAT 验收合同时，**仍必须坚持按保守解耦（$\rho = 0$）分配 `WS-X ≤ 0.32 nm`、`RS-X/4 ≤ 0.24 nm`（掩模侧 `0.96 nm`）→ 保守 RSS `0.40 nm`**，理由有四：

1. **子系统独立解耦考核与整机裕度储备**：`[075]` Sec. 1 明确指出，工业界将系统分解为解耦子系统预算（$\rho = 0$）是保证各模块独立定责的工程基石；整机联调开启 WS→RS 前馈或双向耦合获得的 2×–4× `MA` 压降，应留作应对实际产线工艺扰动与老化漂移的**整机套刻系统裕度**。
2. **双台机 M-side 完全无 RS 陪跑**：在 TWINSCAN 架构中，晶圆对准（SMASH）与调平测量在 M-side 由 WS 独立执行，无 RS 同步抵消。若放任 WS 独立重复性高于 `0.47 nm`，M-side 网格采样与换台定位误差将直接击穿 `DCO ≤ 2.00 nm` 顶层红线。
3. **4× 动力学惩罚与高频水床 `MSD` 劣化硬边界**：RS 追随 WS 需承受 4× 行程/速度/加速度放大，且高频结构柔性模态不确定性迫使鲁棒耦合滤波器滚降（`[075]` Fig. 14–16）；同时 `[022]` Eq. 46 与 `[075]` Table 1 证明，低频 `MA` 压得越狠，高频水床放大越剧烈，直接推高 **`MSD`（`2.88 → 3.33 nm`）**、劣化成像对比度与 CDU。
4. **实测比例印证预算权重合理性**：`[075]` 无耦合低频实测为 **WS `0.48 nm` vs RS/4 `0.11 nm`**（方差比超过 16 : 1），说明在独立考核中给 WS 分配远大于 RS/4 的方差占比（本仓 `64% : 36%`）完全符合重质量液浸 WS 与轻量化 4× RS 的物理规律，且 RS 在 4× 缩小加持下实有进一步收紧的工程潜力。

<a name="sec-4-2"></a>

### 4.2 前期 `v2` 说明书第 1.3 节主从方向表述勘误备忘

在既有正式文档 [九大核心子系统验收指标推导与计算说明书_v2.md](NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md) 第 1.3 节第 ④ 条中，曾简略表述为*“实际常将大扰动 RS 误差前馈给轻量化 WS”*。经本次逐一核验 `[S12]` Nikon `US 2012/0319637 A1` 首页框图、`[090]`、`[085]`、`[078]`、`[147]`、`[022]` 与 `[075]` 原文，**该处主从流向表述需在后续 `v3` 修订时同步勘误为**：

> **标准修订口径**：工业 ArF / ArFi 机台横向同步主流为 **WS 为 Master、更轻且更高带宽的 RS 为 Slave**（或低中频段仍由 RS 追随 WS 的双向 Double-Youla 耦合 `[075]`）；之所以仍不能免除 WS 自身独立验收，是因为受 **4× 行程/加速度/推力放大、高频结构模态不确定性鲁棒滚降及前馈水床效应（`MSD` 劣化）** 约束，RS 仅能在有限低中频段对 WS 做有限度补偿，无法无限兜底（且双台 M-side 无 RS 参与）。

---

<a name="sec-5"></a>

## 5. 参考文献总清单与下载状态（本地已有 / 已自动下载 / 手动下载清单）

[返回目录](#contents)

<a name="sec-5-1"></a>

### 5.1 A 类：本机 OV4 既有文献库已下载（15 篇，无需重复下载）

> 均已完整留存于本机只读目录 `D:\work\OV4\参考文献-整理版\`（或 `D:\work\OV4\参考文献_新增\`）并在 [REFERENCES.md](../../REFERENCES.md) 登记 SHA-256。

| 引用编号 | 本机目录与原件文件名 | 完整书目信息（作者 / 标题 / 出处 / 年份） | 本报告核心支撑点 | 下载状态 |
| :---: | :--- | :--- | :--- | :---: |
| **`[075]`** | `参考文献-整理版/075_1_s2.0_S0967066118306488_main.pdf` | E. Evers, M. van de Wal (ASML), T. Oomen (TU/e), *Beyond decentralized wafer/reticle stage control design: A double-Youla approach for enhancing synchronized motion*, *Control Engineering Practice* 83, pp. 21–32 (2019) | Fig. 12–13 & Table 1：WS 独立 `~0.48 nm`、RS 独立 `~0.11 nm`、无耦合 `MA = 0.565 nm` → 耦合 `0.108/0.200 nm`、`MSD 2.88 → 3.33 nm` | **已在本机** |
| **`[022]`** | `参考文献-整理版/022_1-s2.0-S0967066113001536-main.pdf` | M. F. Heertjes (TU/e), B. Temizer (ASML), M. Schneiders (JPE), *Self-tuning in master–slave synchronization of high-precision stage systems*, *Control Engineering Practice* 21(12), pp. 1706–1715 (2013) | Sec. 2 定义 WS=Master/RS=Slave；Sec. 6 & Fig. 10 实机 `MA 2.92 → 1.55 nm`、WS `e_m ≈ 5.9 nm` vs 同步 `4.0 nm` rms；Eq. 46 前馈水床效应 | **已在本机** |
| **`[147]`** | `参考文献-整理版/147_data_based_motion_control_of_wafer_scanners.pdf` | M. F. Heertjes (ASML / TU/e), *Data-based motion control of wafer scanners*, *IFAC-PapersOnLine* 49(13), pp. 1–12 (2016) | Sec. 4.2 & Fig. 6–8：WS→RS 同步框图与 `543.7–588.2 Hz` 带宽；Fig. 5 短行程 WS 6-DOF 扫描误差；引用 `US8279401B2` 与 `US8451431B2` | **已在本机** |
| **`[078]`** | `参考文献-整理版/078_2008_Mishra_ILC_Synchronization_WS_RS.pdf` | S. Mishra, W. Yeh (NRCA), M. Tomizuka (UC Berkeley), *Iterative Learning Control Design for Synchronization of Wafer and Reticle Stages*, *Proc. ACC*, pp. 3908–3913 (2008) | 阐明 RS 更轻、带宽高于 WS，采用 WS=Master、RS=Slave（ $`r_r = \mathbf{S} y_w`$ ）主从 ILC 同步 | **已在本机** |
| **`[090]`** | `参考文献-整理版/090_Fujipress_IJAT-2-2-5.pdf` | Y. Shibazaki (Nikon Corp.), *Realization of Tubeless Stage in Semiconductor Exposure System*, *IJAT* 2(2), pp. 86–92 (2008) | Nikon ArF `NSR-S308F` 总师明确声明：公司采用 **RS 跟随 WS** 的主从控制方法 | **已在本机** |
| **`[085]`** | `参考文献-整理版/085_52_425.pdf` | 後藤太邦・湯浅匡夫 (Nikon Corp.), *半導体露光装置の制御技術（NSR-620D）*, *計測と制御 (SICE)* 52(5), pp. 425–430 (2013) | 明确 ArFi `NSR-S620D` 为 RS 追随 WS 同步（Eq. 8–9），ILC 后同步达 `0.5 nm` 级，引用 `US 2012/0319637 A1` 与 `US 2006/0170382 A1` | **已在本机** |
| **`[063]`** | `参考文献-整理版/063_76401O.pdf` | H. Nakano 等 (Nikon Corp.), *NSR-S620D immersion scanner performance*, *Proc. SPIE* 7640, 76401O (2010) | Fig. 14 同步 `MA < 0.6/0.6/4 nm`、`MSD < 2.5/3/6.5 nm`；Fig. 15 曝光级 Stage Repeatability `0.96–1.60 nm`（320–700 mm/s） | **已在本机** |
| **`[009]`** | `参考文献-整理版/009_76401N.pdf` | T. Castenmiller 等 (ASML), *Towards ultimate optical lithography with NXT:1950i dual stage immersion platform*, *Proc. SPIE* 7640, 76401N (2010) | Fig. 3 Stage Positioning 拆解 `~0.50 nm`；Fig. 10 实测 `Sync MA-X = 0.47 nm`、`MA-Y = 0.49 nm`；NXT WS 模态 +40% | **已在本机** |
| **`[066]`** | `参考文献-整理版/066_86831L.pdf` | I. Bouchoms 等 (ASML), *NXT:1965Ci / 1970Ci immersion lithography enhancements*, *Proc. SPIE* 8683, 86831L (2013) | Fig. 9 陶瓷短行程 WS `800 mm/s` 扫描 `MAz` 峰值 `4 nm`（95% `≤ 6 nm`） | **已在本机** |
| **`[015]`** | `参考文献-整理版/015_978011.pdf` | ASML, *NXT:1980Di immersion scanner for 7nm production nodes*, *Proc. SPIE* 9780, 978011 (2016) | `NXT:1980Di` 全片焦面 `FU < 9.1 nm (3σ)`、`MMO < 2.0 nm`、产能 `> 275 wph` | **已在本机** |
| **`[018]`** | `参考文献-整理版/018_nikon_nsr_s630d_immersion.pdf` | Nikon Corp., *Immersion Scanners Enabling 10 nm half pitch Production and Beyond (NSR-S630D)*, *Proc. SPIE* (2014) | `NSR-S630D` RS 升级编码器伺服、`SMO = 1.7 nm`、`MMO = 2.5 nm` | **已在本机** |
| **`[064]`** | `参考文献-整理版/064_79730Z.pdf` | M. Yasuda 等 (Nikon Corp.), *Stability and Calibration of Overlay and Focus Control for a Double Patterning Immersion Scanner (NSR-S620D)*, *Proc. SPIE* 7973, 79730Z (2011) | `NSR-S620D` 混合编码器+干涉仪（Bird's Eye Control）测量重复性与 5 天稳定性 | **已在本机** |
| **`[019]`** | `参考文献-整理版/019_Control_of_Wafer_Scanners_Methods_and_Developments.pdf` | M. Heertjes, H. Butler 等 (ASML / TU/e / Cymer), *Control of Wafer Scanners: Methods and Developments*, *Proc. ACC* (2020) | ASML 官方控制综述，引证 `[022]` 与 `[M2]` 作为工业台同步代表 | **已在本机** |
| **`[094]`** | `参考文献-整理版/094_Position_Control_in_Lithographic_Equipment_Applications_of_Control.pdf` | H. Butler (ASML), *Position Control in Lithographic Equipment*, *IEEE Control Systems Magazine* 31(5), pp. 28–47 (2011) | 扫描台长短行程解耦、MA/MSD 狭缝定义与双台架构基础 | **已在本机** |
| **`[N8]`** | `参考文献_新增/Frequency-Domain_Properties_of_Moving_Average_and_Moving_Standard_Deviation_with_Application_to_Stage_Motion_Control.pdf` | M. Heertjes (TU/e / ASML), *Frequency-domain properties of moving average and moving standard deviation with application to stage (motion) control*, *2024 IEEE ECC*, pp. 3521–3526 (2024) | 狭缝 `MA`/`MSD` 频域互补功率谱定理与 CPS 验证（工业台 $\tau_{\mathrm{slit}} = 9.2\text{ ms}$） | **已在本机** |

<a name="sec-5-2"></a>

### 5.2 B 类：本次已自动下载至 `参考文献_新增\WS-RS同步\` 的官方专利原件（13 篇）

> 全部经 USPTO 官方公共专利 PDF 接口直接下载并落盘至 **`D:\work\OV4\参考文献_新增\WS-RS同步\`**（受 `.gitignore` `/参考文献_新增/` 保护不上传至 GitHub），且全部 **13/13 篇完成首页视觉核验与 SHA-256 全库去重校验（100% 唯一，合计 366 页）**。

| 编号 | 专利号与权利人 | 本地保存文件名（位于 `参考文献_新增\WS-RS同步\`） | 页数 | SHA-256（前 12 位） | 核验后发明人与标题摘要 | 官方直链 | 下载状态 |
| :---: | :--- | :--- | :---: | :---: | :--- | :--- | :---: |
| **`[S1]`** | `US 2004/0176861 A1`（ASML） | `ASML_US20040176861A1_Butler_WS_MassEstFeedforward.pdf` | 39 | `35bb9a8190d0` | Hans Butler — *System for Controlling a Position of a Mass*（WS 在线质量辨识 + 自适应加速度前馈，2004） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20040176861) | **已自动下载** |
| **`[S2]`** | `US 2006/0285101 A1`（ASML） | `ASML_US20060285101A1_Butler_Breukers_PS_Feedforward.pdf` | 14 | `de5eed816fde` | Hans Butler, E. H. J. Draaijer, M. J. E. G. Breukers — *Lithographic Apparatus, Projection Apparatus and Device Manufacturing Method*（投影系统位置信号滤波前馈注入晶圆台，2006） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20060285101) | **已自动下载** |
| **`[S3]`** | `US 7,098,990 B2`（ASML） | `ASML_US7098990B2_Butler_StageAccelControl.pdf` | 14 | `0ffcf355053b` | Hans Butler — *Lithographic Apparatus, Device Manufacturing Method...*（双支路加速度反馈抑外扰控制，2006） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7098990) | **已自动下载** |
| **`[S4]`** | `US 7,170,581 B2`（ASML） | `ASML_US7170581B2_SelfAdaptingFeedforwardTuning.pdf` | 14 | `4ad7c9f4d350` | Rob Tousain — *Self-Adapting Feedforward Control Tuning for Motion System*（速度/加速度/Jerk/Snap 自适应前馈系数在线学习，2007） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7170581) | **已自动下载** |
| **`[S5]`** | `US 7,181,296 B2`（ASML） | `ASML_US7181296B2_AdaptiveILC_LithoStage.pdf` | 24 | `0093a2f391c4` | A. I. Rotariu, R. Ellenbroek, M. Steinbuch, G. E. Van Baars — *Method of Adaptive Interactive Learning Control...*（变扫长扫描台时频自适应 ILC，2007） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7181296) | **已自动下载** |
| **`[S6]`** | `US 7,239,368 B2`（ASML） | `ASML_US7239368B2_UnflatnessFeedforwardOverlay.pdf` | 13 | `98d0744e4140` | R. Oesterholt 等 — *Using Unflatness Information of the Substrate Table or Mask Table for Decreasing Overlay*（面形不平度映射前馈降套刻/焦面误差，2007） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7239368) | **已自动下载** |
| **`[S7]`** | `US 7,405,811 B2`（ASML） | `ASML_US7405811B2_LithoPositioningApparatus.pdf` | 16 | `3079eb332226` | M. H. M. Beems, J. Sakai — *Lithographic Apparatus and Positioning Apparatus*（中间结构短程双测量系统降定位噪声，2008；已纠偏非 Nikon） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7405811) | **已自动下载** |
| **`[S8]`** | `US 8,279,401 B2`（ASML） | `ASML_US8279401B2_PositionControlComplianceFF.pdf` | 13 | `cba17490471b` | M. J. Vervoordeldonk, M. C. J. Baggen — *Position Control System, a Lithographic Apparatus...*（柔度补偿 + 加速度/Snap 前馈，2012，`[147]` 引用） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8279401) | **已自动下载** |
| **`[S9]`** | `US 2004/0128918 A1`（Nikon） | `Nikon_US20040128918A1_ILC_StageSyncTracking.pdf` | 41 | `1892fe42639e` | P.-H. Yang, B. Yuan, S. Makinouchi, Y. Itakura, K. Hirano, H. Hashimoto, R. Kawaguchi — *Control System and Method for Improving Tracking Accuracy...*（第二台定位数据调节第一台同步 + ILC 奠基专利，2004） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20040128918) | **已自动下载** |
| **`[S10]`** | `US 2005/0231706 A1`（Nikon） | `Nikon_US20050231706A1_FeedforwardMILC_Grouping.pdf` | 25 | `5ffba327a38a` | P.-H. Yang, H. Hashimoto, B. Yuan, A. Yamaguchi, S. Makinouchi — *Feedforward Control with Reduced Learning Time...*（视场分组 MILC 前馈，2005） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20050231706) | **已自动下载** |
| **`[S11]`** | `US 2006/0170382 A1`（Nikon） | `Nikon_US20060170382A1_LinearMotorForceRippleILC.pdf` | 34 | `89c5de51cb9f` | P.-H. Yang, H. Hashimoto, B. Yuan, A. Yamaguchi — *Linear Motor Force Ripple Identification and Compensation with ILC*（直线电机推力波动 ILC，2006，`[085]` 引用） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20060170382) | **已自动下载** |
| **`[S12]`** | `US 2012/0319637 A1`（Nikon） | `Nikon_US20120319637A1_SyncControlDevicesMethods.pdf` | 72 | `8439247074ae` | **P.-H. Yang, K. Hirano, M. Yuasa** — *Synchronization Control Devices and Methods*（**核心实锤**：首页框图明确 `wafer error → H(s) → reticle stage`，2012，`[085]` 引用） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/20120319637) | **已自动下载** |
| **`[S13]`** | `US 8,451,431 B2`（Nikon） | `Nikon_US8451431B2_IFT_SyncControlStages.pdf` | 47 | `a629cbaeabc2` | P.-H. Yang, S.-L. Koo — *Control Systems and Methods Applying Iterative Feedback Tuning for Feed-Forward and Synchronization Control...*（IFT 同步整定，2013，`[147]` 引用） | [USPTO PDF](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8451431) | **已自动下载** |

<a name="sec-5-3"></a>

### 5.3 C 类：需手动下载清单（8 篇，含精确 DOI / 专利号与下载链接）

> 以下 8 篇高价值论文/非 US 专利因出版商付费墙（IEEE Xplore / Elsevier）或非 US 专利站点对脚本返回 `HTTP 503` / `403` 而未能自动拉取。建议在具备校园/机构权限或普通浏览器环境下手动下载，并统一保存至 **`D:\work\OV4\参考文献_新增\WS-RS同步\`**。

| 编号 | 优先级 | 完整书目 / 专利信息 | 精准 DOI 或专利检索链接 | 未自动下载原因 | 建议保存文件名 |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **`[M1]`** | **P0（高）** | C. J. H. Lambregts, M. F. Heertjes, B. J. van der Veek (ASML / TU/e), *Multivariable feedback control in stage synchronization*, *Proc. 2015 ACC*, pp. 4149–4154 (2015) | DOI: [10.1109/ACC.2015.7171980](https://doi.org/10.1109/ACC.2015.7171980) | IEEE Xplore 付费墙（非 OA） | `ASML_Lambregts_2015_ACC_MultivariableStageSync.pdf` |
| **`[M2]`** | **P0（高）** | M. F. Heertjes, M. Galluzzo, L. Kuindersma (ASML / TU/e), *Robust Data-Driven Control for the Stage Synchronization Problem*, *IFAC Proceedings Volumes* 47(3), pp. 1134–1139 (2014) | DOI: [10.3182/20140824-6-ZA-1003.00625](https://doi.org/10.3182/20140824-6-ZA-1003.00625) · [TU/e 记录页](https://research.tue.nl/en/publications/00df834d-6de4-4e6b-98ff-328d1e7ddaa0) | ScienceDirect 拦截脚本请求（403），浏览器通常可开放访问下载 | `ASML_Heertjes_2014_IFAC_RobustStageSync.pdf` |
| **`[M3]`** | **P0（高）** | V. A. Looijen, M. F. Heertjes (TU/e / ASML), *Robust Synchronization of Motion in Wafer Scanners Using Particle Swarm Optimization*, *2018 IEEE CCTA*, pp. 1102–1107 (2018) | DOI: [10.1109/CCTA.2018.8511380](https://doi.org/10.1109/CCTA.2018.8511380) | IEEE Xplore 付费墙（非 OA） | `ASML_Looijen_2018_CCTA_RobustMotionSync.pdf` |
| **`[M4]`** | **P1（中）** | M. O. Navarrete, M. F. Heertjes, R. H. Munnig Schmidt (TU Delft / ASML), *Common zeros in synchronization of high-precision stage systems*, *2015 IEEE ICM*, pp. 602–607 (2015) | DOI: [10.1109/ICMECH.2015.7084045](https://doi.org/10.1109/ICMECH.2015.7084045) | IEEE Xplore 付费墙（非 OA） | `ASML_Navarrete_2015_ICM_CommonZerosSync.pdf` |
| **`[M5]`** | **P1（中）** | H. Butler (ASML / TU/e), *Feedforward signal prediction for accurate motion systems using digital filters*, *Mechatronics* 22(6), pp. 827–835 (2012) | DOI: [10.1016/j.mechatronics.2012.05.002](https://doi.org/10.1016/j.mechatronics.2012.05.002) | Elsevier 付费墙（非 OA） | `ASML_Butler_2012_Mechatronics_FFPrediction.pdf` |
| **`[M6]`** | **P1（中）** | M. F. Heertjes, B. J. C. H. van der Velden, T. A. Oomen (ASML / TU/e), *Constrained Iterative Feedback Tuning for Robust Control of a Wafer Stage System*, *IEEE TCST* 24(1), pp. 56–66 (2016) | DOI: [10.1109/TCST.2015.2418311](https://doi.org/10.1109/TCST.2015.2418311) · [TU/e 记录页](https://research.tue.nl/en/publications/4e608fc7-18d7-4c15-ab2d-557c329de354) | IEEE Xplore 付费墙，TU/e Pure 旧链接 404 | `ASML_Heertjes_2016_TCST_ConstrainedIFT_WS.pdf` |
| **`[M7]`** | **P1（中）** | ASML Netherlands B.V.（发明人 H. Butler, M. J. E. G. Breukers, M. F. Heertjes），欧洲/荷兰同步控制专利族 `EP 13198925.3` / `NL 2013810`（2013 优先权） | [Espacenet 检索](https://worldwide.espacenet.com/patent/search?q=pn%3DNL2013810) · [Google Patents 检索](https://patents.google.com/?q=NL2013810+Heertjes) | 非 US 专利（不在 USPTO 库），Google Patents 脚本直连返回 503 | `ASML_NL2013810_Butler_Breukers_Heertjes.pdf` |
| **`[M8]`** | **P2（参考）** | 上海微电子装备有限公司（SMEE，吴立伟、杨晓燕），《工件台和掩模台的同步控制方法及其系统》，授权发明专利 `CN 103135357 B` | [Google Patents 中文页](https://patents.google.com/patent/CN103135357B/zh) | 非 US 专利（CNIPA），Google Patents 脚本直连返回 503 | `SMEE_CN103135357B_WS_RS_SyncControl.pdf` |
