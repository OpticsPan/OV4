# OV4 参考文献完整清单总目（共 265 份本地原件 · 含新增 22 篇一手文献与专利）

[仓库首页](README.md) · [成果索引](outputs/README.md) · [NXT:1965Ci L0–L3 拆解报告 v1](outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md) · [WS-RS 同步调研报告 v2](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md) · [九大子系统说明书 v2](outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md) · [总报告 v2](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md) · [仓库规范](REPOSITORY_MANAGEMENT.md) · [总变更记录](CHANGELOG.md)

> **归档说明**：受版权与大体积限制，本机原始 PDF 与 MinerU Markdown 文献库（`参考文献-整理版/`、`参考文献-整理版-Markdown/`、`参考文献_新增/`）由 [.gitignore](.gitignore) 排除、仅保留于本机只读目录；本文件作为 **Git 跟踪的全库唯一书目总目**，完整记录全部 **265 份原件**（SHA-256 去重后 **264 份唯一文献**）的编号、文件名、标题、类型、页数、校验指纹及引用状态，便于在 GitHub 网页端检索与评审溯源。

<a name="contents"></a>

## 目录

- [0. 文献库统计总览与目录映射](#sec-0)
- [1. 新增专项一手文献清单（参考文献_新增 · N1–N8，共 8 份）](#sec-new)
- [1.2 新增 WS–RS 同步专项 USPTO 专利原件（参考文献_新增/WS-RS同步 · S1–S14，共 14 份）](#sec-wsrs-sync)
- [2. 原始基线文献完整清单（参考文献-整理版 · 003–266，共 243 份）](#sec-base)
- [3. 跨库配套引用手册（ME3 官方培训资料）与维护说明](#sec-me3)

---

<a name="sec-0"></a>

## 0. 文献库统计总览与目录映射

[返回目录](#contents)

| 文献批次 | 本机只读目录 | 原件数 | 唯一 SHA-256 数 | 学术论文 | 专利 | 专著/硕博论文/标准 | 官方手册/规格书 | 核验/引用说明 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **WS–RS 同步专项专利批次（2026-11-25）** | `D:\work\OV4\参考文献_新增\WS-RS同步\` | **14** | 14（全部唯一） | 0 | 14 | 0 | 0 | **14/14 篇 USPTO 官方原件完成封面/关键页视觉核验（9 ASML + 5 Nikon，375 页，含新增 `[S14]` ASML 奠基同步专利 `US 6,373,072 B1`），纳入 [WS-RS 同步调研报告 v2](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md)** |
| **新增专项批次（2026-11-24）** | `D:\work\OV4\参考文献_新增\` | **8** | 7（`[N4]` 同 `[010]`） | 7 | 1 | 0 | 0 | **8/8 全部完成全文核验并纳入说明书 v2** |
| **原始基线库（OV4）** | `D:\work\OV4\参考文献-整理版\` | **243** | 243 | 168 | 62 | 5 | 8 | 同名 MinerU Markdown 存放于 `参考文献-整理版-Markdown\`；已在正式报告中直接引用 45+ 份核心条目 |
| **合计** | — | **265** | **264** | **175** | **77** | **5** | **8** | 全库均保留原件 SHA-256 指纹供复查；另 8 篇待手动下载清单见 [WS-RS 同步调研报告 v2 第 6.3 节](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md#sec-6-3) |

---

<a name="sec-new"></a>

## 1. 新增专项一手文献清单（`参考文献_新增/` · `[N1]–[N8]`，共 8 份）

[返回目录](#contents)

| 编号 | 原始 PDF 文件名 | 类型 | 页数 | SHA-256（前 12 位） | 完整书目信息（作者 / 标题 / 出处 / DOI） | 本仓库核验结论与支撑章节 | 入库状态 |
| :---: | :--- | :---: | :---: | :---: | :--- | :--- | :--- |
| **`[N1]`** | `US20080174858A1.pdf` | 专利 | 25 | `61266ca47d28` | H. Feldmann 等 (Carl Zeiss SMT), *Projection Objective for Microlithography*, US 2008/0174858 A1 (2008) | Table 3 (p. 9) 原表确证 NA = 1.35 离轴狭缝 `26 × 5.5 mm`（H2O）；¶0098–0100 光瞳/场间双校正板机理 | 全新入库（已核验） |
| **`[N2]`** | `615420.pdf` | 学术论文 | 10 | `9281a83e3f1c` | B. Kneer, P. Gräupner, R. Garreis, R. Kläsges, H. Feldmann (Carl Zeiss SMT), *Catadioptric Lens Design: The Breakthrough to Hyper-NA Optics*, Proc. SPIE 6154, 615420 (2006), DOI: 10.1117/12.668024 | 直筒折反减重 40%、保留 26 mm 矩形场（避开环形场 20% 产能损失）；Fig. 9 NA = 1.2 波前基线 `< 1.2 nm` | 全新入库（已核验） |
| **`[N3]`** | `59620Y.pdf` | 学术论文 | 8 | `e808cc8c1f90` | H. Feldmann, A. Dodoc, A. Epple, H.-J. Rostalski, D. Shafer, W. Ulrich (Carl Zeiss SMT), *Catadioptric Projection Lenses for Immersion Lithography*, Proc. SPIE 5962, 59620Y (2005), DOI: 10.1117/12.625199 | Sec. 3.1–3.3 & Fig. 4–8 直筒折反光路避遮挡与离轴狭缝扫描宽度上限机理 | 全新入库（已核验） |
| **`[N4]`** | `113270T (1).pdf` | 学术论文 | 6 | `793d89179f91` | T. Pollak, W. Emer, B. Thüring (Zeiss), F. Fahrni, F. Klinkhamer, W. de Boeij, W. Bouman (ASML), *A novel projection lens manipulator for high frequent overlay tuning*, Proc. SPIE 11327, 113270T (2020), DOI: 10.1117/12.2552063 | HD `79×17 = 1,343` 点调校网；Fig. 5 FlexWave（光瞳面）vs 场平面畸变操纵器（7–9 阶扫描实时）正交矩阵 | 与基线 `[010]` SHA-256 一致（已核验） |
| **`[N5]`** | `79730V.pdf` | 学术论文 | 11 | `2b52dde41443` | J. Bekaert 等 (imec / ASML / BRION / Zeiss), *Characterization and control of dynamic lens heating effects under high volume manufacturing conditions*, Proc. SPIE 7973, 79730V (2011), DOI: 10.1117/12.881609 | XT:1900i（NA=1.35）未控热漂 `8–10 nm` CD 漂移；cASCAL 等效 ALHC；FlexWave 控旋转偶极至 Z64 | 全新入库（已核验） |
| **`[N6]`** | `832607.pdf` | 学术论文 | 19 | `bd500ea50782` | S. Halle, M. Crouse, A. Jiang, Y. van Dommelen, T. Brunner 等 (IBM / ASML / BRION), *Lens Heating Challenges for Negative Tone Develop Layers with Freeform Illumination*, Proc. SPIE 8326, 832607 (2012), DOI: 10.1117/12.916312 | 78% 高透 NTD 掩模未控奇像差套刻 `> 6 nm`（FlexWave 压至 `< 2 nm`）；Table 4 `Z10 = -0.88 nm/nm` 交叉验证 Abbe 仿真 `0.905`（误差 2.8%） | 全新入库（已核验） |
| **`[N7]`** | `011006_1.pdf` | 学术论文 | 11 | `06f8732be40c` | J. Mulkens, P. Hinnen, M. Kubis, A. Padiy, J. Benschop (ASML), *Holistic optimization architecture enabling sub-14-nm projection lithography*, JM3 13(1), 011006 (2014), DOI: 10.1117/1.JMM.13.1.011006 | 20 参逐场 Eq. 3；Gridplate `< 15 mm` vs 多移位 `> 15 mm`（5 机 MMO `3.0–3.8 nm`、HO-CPE `2.5 nm`）；18 参 RHC 极热压至 `1.58 nm` | 全新入库（已核验） |
| **`[N8]`** | `Frequency-Domain_Properties_of_Moving_Average_and_Moving_Standard_Deviation_with_Application_to_Stage_Motion_Control.pdf` | 学术论文 | 6 | `d79e3e797370` | M. Heertjes (TU/e / ASML), *Frequency-domain properties of moving average and moving standard deviation with application to stage (motion) control*, 2024 IEEE ECC, pp. 3521–3526, DOI: 10.23919/ECC64448.2024.10591183 | Theorem 2.1 / Eq. 8–9 / Prop. 3.1 严格给出曝光狭缝 `MA`/`MSD` 互补功率谱公式与 CPS 验证（工业台 `τ_slit = 9.2 ms`） | 全新入库（已核验） |

---

<a name="sec-wsrs-sync"></a>

## 1.2 新增 WS–RS 同步专项 USPTO 专利原件清单（`参考文献_新增/WS-RS同步/` · `[S1]–[S14]`，共 14 份）

[返回目录](#contents)

> 说明：本批次 14 份专利全部自 USPTO 官方 PDF 接口合法直下并完成首页/关键页视觉核验与 SHA-256 去重校验（均与基线库 100% 唯一，合计 375 页），直接支撑 [WS-RS 同步策略与单台重复性误差专项调研报告 v2](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md)（[XT i-line/KrF 专题第 4 章](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md#sec-4)）。另 8 篇待手动下载论文与非 US 专利清单（`[M1]–[M8]`）见该报告 [第 6.3 节](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md#sec-6-3)。

| 编号 | 本地 PDF 文件名（`参考文献_新增/WS-RS同步/`） | 权利人 | 专利号 | 页数 | SHA-256（前 12 位） | 核验后发明人、标题与核心支撑点 | 入库状态 |
| :---: | :--- | :---: | :--- | :---: | :---: | :--- | :--- |
| **`[S1]`** | `ASML_US20040176861A1_Butler_WS_MassEstFeedforward.pdf` | ASML | `US 2004/0176861 A1` | 39 | `35bb9a8190d0` | H. Butler, *System for Controlling a Position of a Mass*（2004）；WS 在线质量辨识与自适应加速度前馈（对应 `[088]`） | 全新入库（已核验） |
| **`[S2]`** | `ASML_US20060285101A1_Butler_Breukers_PS_Feedforward.pdf` | ASML | `US 2006/0285101 A1` | 14 | `de5eed816fde` | H. Butler, E. H. J. Draaijer, M. J. E. G. Breukers, *Lithographic Apparatus, Projection Apparatus...*（2006）；投影系统位置滤波前馈至晶圆台 | 全新入库（已核验） |
| **`[S3]`** | `ASML_US7098990B2_Butler_StageAccelControl.pdf` | ASML | `US 7,098,990 B2` | 14 | `0ffcf355053b` | H. Butler, *Lithographic Apparatus, Device Manufacturing Method...*（2006）；双支路加速度反馈外扰抑制 | 全新入库（已核验） |
| **`[S4]`** | `ASML_US7170581B2_SelfAdaptingFeedforwardTuning.pdf` | ASML | `US 7,170,581 B2` | 14 | `4ad7c9f4d350` | R. Tousain, *Self-Adapting Feedforward Control Tuning for Motion System*（2007）；速度/加速度/Jerk/Snap 前馈在线自适应学习 | 全新入库（已核验） |
| **`[S5]`** | `ASML_US7181296B2_AdaptiveILC_LithoStage.pdf` | ASML | `US 7,181,296 B2` | 24 | `0093a2f391c4` | A. I. Rotariu, R. Ellenbroek, M. Steinbuch, G. E. Van Baars, *Method of Adaptive Interactive Learning Control...*（2007）；变扫长时频自适应 ILC | 全新入库（已核验） |
| **`[S6]`** | `ASML_US7239368B2_UnflatnessFeedforwardOverlay.pdf` | ASML | `US 7,239,368 B2` | 13 | `98d0744e4140` | R. Oesterholt 等, *Using Unflatness Information of the Substrate Table or Mask Table for Decreasing Overlay*（2007）；面形不平度前馈 | 全新入库（已核验） |
| **`[S7]`** | `ASML_US7405811B2_LithoPositioningApparatus.pdf` | ASML | `US 7,405,811 B2` | 16 | `3079eb332226` | M. H. M. Beems, J. Sakai, *Lithographic Apparatus and Positioning Apparatus*（2008）；中间结构短程双测量系统（已核验确属 ASML） | 全新入库（已核验） |
| **`[S8]`** | `ASML_US8279401B2_PositionControlComplianceFF.pdf` | ASML | `US 8,279,401 B2` | 13 | `cba17490471b` | M. J. Vervoordeldonk, M. C. J. Baggen, *Position Control System...*（2012）；结构柔度补偿 + 加速度/Snap 前馈（`[147]` 引用） | 全新入库（已核验） |
| **`[S9]`** | `Nikon_US20040128918A1_ILC_StageSyncTracking.pdf` | Nikon | `US 2004/0128918 A1` | 41 | `1892fe42639e` | P.-H. Yang, B. Yuan, S. Makinouchi, K. Hirano 等, *Control System and Method for Improving Tracking Accuracy...*（2004）；两台同步耦合 + ILC 奠基专利 | 全新入库（已核验） |
| **`[S10]`** | `Nikon_US20050231706A1_FeedforwardMILC_Grouping.pdf` | Nikon | `US 2005/0231706 A1` | 25 | `5ffba327a38a` | P.-H. Yang, H. Hashimoto, B. Yuan, A. Yamaguchi, S. Makinouchi, *Feedforward Control with Reduced Learning Time...*（2005）；分组 MILC 前馈 | 全新入库（已核验） |
| **`[S11]`** | `Nikon_US20060170382A1_LinearMotorForceRippleILC.pdf` | Nikon | `US 2006/0170382 A1` | 34 | `89c5de51cb9f` | P.-H. Yang, H. Hashimoto, B. Yuan, A. Yamaguchi, *Linear Motor Force Ripple Identification and Compensation with ILC*（2006，`[085]` 引用） | 全新入库（已核验） |
| **`[S12]`** | `Nikon_US20120319637A1_SyncControlDevicesMethods.pdf` | Nikon | `US 2012/0319637 A1` | 72 | `8439247074ae` | **P.-H. Yang, K. Hirano, M. Yuasa**, *Synchronization Control Devices and Methods*（2012，`[085]` 引用）；首页框图实锤 `wafer error → H(s) → RS` 主从链路 | 全新入库（已核验） |
| **`[S13]`** | `Nikon_US8451431B2_IFT_SyncControlStages.pdf` | Nikon | `US 8,451,431 B2` | 47 | `a629cbaeabc2` | P.-H. Yang, S.-L. Koo, *Control Systems and Methods Applying IFT for Feed-Forward and Synchronization Control...*（2013，`[147]` 引用） | 全新入库（已核验） |
| **`[S14]`** | `ASML_US6373072B1_Butler_WS_ErrorFeedforward_to_RS.pdf` | ASML | `US 6,373,072 B1` | 9 | `5498a5161270` | **H. Butler, T. P. H. Warmerdam** (ASM Lithography B.V.), *Lithographic Projection Apparatus and Device Manufacturing Method*（1998 优先权 / 2002 授权，全 9 页视觉核验）；ASML 早期步进扫描（PAS 5500 / TWINSCAN AT·XT）`WS → RS` 位置+二阶微分加速度双路前馈奠基专利，Col. 7 实测 `MA X: 11.4 → 1.0 nm`（降 91.2%）、`MA Y: 4.3 → 1.1 nm` | **v2 新增入库（全 9 页核验）** |

---

<a name="sec-base"></a>

## 2. 原始基线文献完整清单（`参考文献-整理版/` · `[003]–[266]`，共 243 份）

[返回目录](#contents)

> 说明：本表按原始编号升序全量列出 `参考文献-整理版/` 中全部 243 份 PDF（与 `参考文献-整理版-Markdown/` 中 243 份 MinerU Markdown 一一对应，来源自 `转换清单.csv`）。“已引用”列标记 `★` 表示已在 OV4 正式报告/说明书/PPTX 中直接引用。

| 序号 | 编号 | 原始 PDF 文件名 | 文献标题 / 专利名称 | 类型 | 页数 | 原件 SHA-256（前 12 位） | 已引用 |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| 1 | `[003]` | `003_advanced_lithography_process.pdf` | 现代集成电路工厂中的先进光刻工艺研发方法与流程 | 专著/硕博论文/标准 | 342 | `5ec4a53792f6` |  |
| 2 | `[006]` | `006_asml_iwaps_2018_scanner_innovations.pdf` | Immersion and dry scanner innovations to support next generation device nodes. | 学术论文 | 25 | `66f92a76b031` | ★ |
| 3 | `[007]` | `007_flexray_programmable_illumination.pdf` | Performance of FlexRay, a fully programmable Illumination system for generation of Freeform Sources on high NA immersion systems | 学术论文 | 10 | `f7a0019e335d` |  |
| 4 | `[008]` | `008_021403_1 (1).pdf` | High-order distortion control using a computational prediction method for device overlay | 学术论文 | 11 | `8d2163e59192` | ★ |
| 5 | `[009]` | `009_76401N.pdf` | Towards Ultimate Optical Lithography with NXT:1950i Dual Stage Immersion Platform. | 学术论文 | 12 | `9e90b86e529c` | ★ |
| 6 | `[010]` | `010_projection_lens_manipulator_overlay.pdf` | A novel projection lens manipulator for high frequent overlay tuning | 学术论文 | 6 | `793d89179f91` |  |
| 7 | `[011]` | `011_111780R.pdf` | The impact of the reticle and wafer alignment mark placement accuracy on the intra-field mask-to-mask overlay | 学术论文 | 12 | `106b1bcef0e4` | ★ |
| 8 | `[011]` | `011_nxt1970ci_reticle_wafer_alignment.pdf` | The impact of the reticle and wafer alignment mark placement accuracy on the intra-field mask-to-mask overlay | 学术论文 | 13 | `a8de92bd3269` | ★ |
| 9 | `[012]` | `012_asml_xt1700i_xt1900i_performance.pdf` | TWINSCAN XT:1900i paving the way to sub 40nm imaging and double patterning | 官方手册/规格书 | 2 | `10022ad86872` |  |
| 10 | `[013]` | `013_nikon_nsr_s636e_specifications.pdf` | Nikon NSR-S636E ArF Immersion Scanner Specifications | 官方手册/规格书 | 2 | `3fb783c1f1b1` |  |
| 11 | `[014]` | `014_nikon_nsr_s620d_performance_forum.pdf` | Extens ion of 1 93 I m mers ion Lithog raphy | 官方手册/规格书 | 20 | `ba30b188b3e3` |  |
| 12 | `[015]` | `015_978011.pdf` | NXT:1980Di immersion scanner for 7nm production nodes | 学术论文 | 9 | `9a19b5ebb43f` | ★ |
| 13 | `[016]` | `016_nxt1980di_reticle_heating_rhc2.pdf` | Reticle Heating Feed-forward Control (RHC2) on NXT:1980Di immersion scanner for enhanced on-product overlay | 学术论文 | 6 | `ccbee0872f24` | ★ |
| 14 | `[017]` | `017_1-s2.0-S0167931713000804-main.pdf` | Thermal behavior of wafers and its effects on overlay performance in immersion lithography | 学术论文 | 4 | `b5a062d07f03` | ★ |
| 15 | `[017]` | `017_xt1700fi_wafer_thermal_overlay.pdf` | Thermal behavior of wafers and its effects on overlay performance in immersion lithography | 学术论文 | 4 | `8936fe20711b` | ★ |
| 16 | `[018]` | `018_nikon_nsr_s630d_immersion.pdf` | Immersion Scanners Enabling 10 nm half pitch Production and Beyond | 学术论文 | 10 | `6f8268cae043` |  |
| 17 | `[019]` | `019_Control_of_Wafer_Scanners_Methods_and_Developments.pdf` | Control of Wafer Scanners: Methods and Developments | 学术论文 | 18 | `cc58b4c2ee97` | ★ |
| 18 | `[019]` | `019_heertjes_control_wafer_scanners.pdf` | Control of Wafer Scanners: Methods and Developments | 学术论文 | 18 | `fa276f73329c` | ★ |
| 19 | `[020]` | `020_meiling_euv_alpha_stage_performance.pdf` | The EUV Program at ASML: an update | 学术论文 | 12 | `003507a6d41c` |  |
| 20 | `[021]` | `021_SPIE2007_XT1900_paper.pdf` | Performance of a 1.35NA ArF immersion lithography system for 40nm applications | 学术论文 | 14 | `d3ddae439a1d` | ★ |
| 21 | `[022]` | `022_1-s2.0-S0967066113001536-main.pdf` | Self-tuning in master–slave synchronization of high-precision stage systems | 学术论文 | 10 | `1aa75fc49631` |  |
| 22 | `[024]` | `024_79731G.pdf` | Advanced Wavefront Engineering for Improved Imaging and Overlay Applications on a 1.35 NA Immersion Scanner | 学术论文 | 13 | `e25f1b752cb5` | ★ |
| 23 | `[025]` | `025_86831I.pdf` | Comprehensive thermal aberration & distortion control of lithographic lenses for accurate overlay | 学术论文 | 7 | `e2e5bb7618ea` |  |
| 24 | `[027]` | `027_Identifying_Position_Dependent_Mechanical_Systems_A_Modal_Approach_Applied_to_a_Flexible_Wafer_Stage.pdf` | Identifying Position-Dependent Mechanical Systems: A Modal Approach Applied to a Flexible Wafer Stage | 学术论文 | 14 | `17f08d1780fc` |  |
| 25 | `[027]` | `027_voorhoeve_position_dependent_wafer_stage_arxiv.pdf` | Identifying Position-Dependent Mechanical Systems: A Modal Approach Applied to a Flexible Wafer Stage | 学术论文 | 13 | `1cb022e96ba1` |  |
| 26 | `[028]` | `028_US20100092881A1.pdf` | US20100092881A1 — Process, Apparatus and Device (ASML) | 专利 | 13 | `bf31c9c01ba2` |  |
| 27 | `[029]` | `029_US20220244649A1.pdf` | US20220244649A1 — Sub-Field Control of a Lithographic Process and Associated Apparatus (ASML) | 专利 | 19 | `7404d9217d9b` |  |
| 28 | `[030]` | `030_021202_1.pdf` | Overlay error statistics for multipleexposure patterning | 学术论文 | 17 | `bb647d856e01` |  |
| 29 | `[031]` | `031_031106_1.pdf` | Polarization effects in immersion lithography | 学术论文 | 10 | `ec3dcbcab92a` |  |
| 30 | `[032]` | `032_104_1.pdf` | Benefits and limitations of immersion lithography | 学术论文 | 11 | `3c2a913a4829` |  |
| 31 | `[033]` | `033_1058611.pdf` | Multi-color fly-cut-SAQP for reduced process variation | 学术论文 | 9 | `05208457540c` |  |
| 32 | `[034]` | `034_105871I.pdf` | A Novel Positive Tone Development Method for Defect Reduction in the Semiconductor 193 nm Immersion Lithography Process | 学术论文 | 6 | `e2fc88071941` |  |
| 33 | `[035]` | `035_120550U.pdf` | Continuous improvement of defectivity rate and CD uniformity in immersion lithography via track co-optimization method | 学术论文 | 8 | `3f9b4af1032d` |  |
| 34 | `[036]` | `036_134240K.pdf` | Breaking Down ADI Line Edge Roughness from a DUV Scanner into Components | 学术论文 | 6 | `a9fd270d1644` |  |
| 35 | `[037]` | `037_139791N.pdf` | Reduction of LER/LWR through Resist Optimization and Widening of Laser Spectral Width: Process Window Acquisition | 学术论文 | 9 | `2cb94fd97e30` |  |
| 36 | `[038]` | `038_196.pdf` | ArF Immersion Lithography using TWINSCAN Technology. | 学术论文 | 12 | `1ff655b7724e` |  |
| 37 | `[039]` | `039_264.pdf` | Feasibility of immersion lithography | 学术论文 | 9 | `c9378846a53a` |  |
| 38 | `[040]` | `040_285.pdf` | Extending optical lithography with immersion | 学术论文 | 21 | `ad97328c11a4` |  |
| 39 | `[041]` | `041_377_1.pdf` | Immersion lithography and its impact on semiconductor manufacturing | 学术论文 | 19 | `e6418dbe9a2f` |  |
| 40 | `[042]` | `042_615237.pdf` | Integrated Projecting Optics Tester for Inspection of Immersion ArF Scanner | 学术论文 | 7 | `0dc73b8f2f41` |  |
| 41 | `[043]` | `043_615408.pdf` | Current status and future prospect of immersion lithography | 学术论文 | 12 | `474b341bd61d` |  |
| 42 | `[044]` | `044_61540B.pdf` | Enabling the 45nm node by hyper-NA polarized lithography | 学术论文 | 11 | `e123b347517c` |  |
| 43 | `[045]` | `045_61541U.pdf` | Mass Production Level ArF Immersion Exposure Tool | 学术论文 | 8 | `d18062ebac87` |  |
| 44 | `[046]` | `046_61541W.pdf` | Immersion lithography with an ultrahigh-NA in-line catadioptric lens and a high-transmission flexible polarization illumination system | 学术论文 | 14 | `7ca5b6a7b302` |  |
| 45 | `[047]` | `047_65181M.pdf` | Enabling Immersion Lithography and Double Patterning | 学术论文 | 8 | `b2d0c12b2e0e` |  |
| 46 | `[048]` | `048_652005.pdf` | Defects, Overlay and Focus Performance Improvements with Five Generations of Immersion Exposure Systems | 学术论文 | 11 | `0e98c30affba` |  |
| 47 | `[049]` | `049_652012.pdf` | Immersion Defect Reduction (2) | 学术论文 | 7 | `8b986963f738` |  |
| 48 | `[050]` | `050_65201W.pdf` | Latest results from the hyper-NA immersion scanners S609B and S610C | 学术论文 | 12 | `98c3afcd38a7` |  |
| 49 | `[051]` | `051_652021.pdf` | Catadioptric Projection Lens for 1.3 NA scanner | 学术论文 | 8 | `76f404a3524d` |  |
| 50 | `[052]` | `052_65202K.pdf` | Sub k1 = 0.25 Lithography with Double Patterning Technique for 45nm Technology Node Flash Memory Devices at $\lambda = 193\mathrm{nm}$ | 学术论文 | 12 | `cbdd63d21bfb` |  |
| 51 | `[053]` | `053_655.pdf` | Full-field exposure tools for immersion lithography | 学术论文 | 14 | `8ab3dc413698` |  |
| 52 | `[054]` | `054_660731.pdf` | Implementation of Double Dipole Lithography for 45nm node poly and diffusion layer manufacturing with 0.93NA | 学术论文 | 9 | `3cba56a39e04` |  |
| 53 | `[055]` | `055_679.pdf` | Water Immersion Optical Lithography for the 45nm Node | 学术论文 | 11 | `6d6f350d9f15` |  |
| 54 | `[056]` | `056_69241N.pdf` | Recent performance results of Nikon immersion lithography tools | 学术论文 | 8 | `5763a2025fad` |  |
| 55 | `[057]` | `057_69241P.pdf` | Latest Developments on Immersion Exposure Systems. | 学术论文 | 12 | `96ce3f39bfc2` | ★ |
| 56 | `[058]` | `058_710.pdf` | Immersion Lithography Exposure Systems: Today’s Capabilities and Tomorrow’s Expectations | 学术论文 | 15 | `09e9082b7723` |  |
| 57 | `[059]` | `059_724.pdf` | Immersion lithography; its potential performance and issues | 学术论文 | 10 | `322528a83c8a` |  |
| 58 | `[060]` | `060_72741I.pdf` | An innovative platform for high-throughput, high-accuracy lithography using a single wafer stage | 学术论文 | 12 | `3b61946b25ef` | ★ |
| 59 | `[061]` | `061_72741P.pdf` | Control and reduction of immersion defectivity for yield enhancement at high volume production | 学术论文 | 9 | `a1f9f5d4367d` |  |
| 60 | `[062]` | `062_72741S.pdf` | Enabling the lithography roadmap: an immersion tool based on a Novel Stage Positioning System. | 学术论文 | 10 | `57355c4f4bbf` | ★ |
| 61 | `[063]` | `063_76401O.pdf` | Latest performance of immersion scanner S620D with the Streamlign platform for the double patterning generation | 学术论文 | 12 | `cea32d004e56` | ★ |
| 62 | `[064]` | `064_79730Z.pdf` | Stability and Calibration of Overlay and Focus Control for a Double Patterning Immersion Scanner | 学术论文 | 12 | `a0258812609a` |  |
| 63 | `[065]` | `065_83280H.pdf` | Plasma treatments to improve Linewidth roughness during gate patterning | 学术论文 | 11 | `f80ad518aa7b` |  |
| 64 | `[066]` | `066_86831L.pdf` | Extending immersion lithography down to 1x nm production nodes | 学术论文 | 9 | `d108fef2e419` | ★ |
| 65 | `[067]` | `067_961.pdf` | Simulations of immersion lithography | 学术论文 | 8 | `f56792cbacf2` |  |
| 66 | `[068]` | `068_97_1.pdf` | Advantage and feasibility of immersion lithography | 学术论文 | 7 | `d453b6ec1b08` |  |
| 67 | `[069]` | `069_abdallah2005.pdf` | 193nm dual layer organic B.A.R.C.s for high NA immersion lithography | 学术论文 | 19 | `17bc70d95327` |  |
| 68 | `[070]` | `070_Advanced Processes for 193-nm Immersion Lithography (SPIE Press Monograph Vol. PM189) (Yayi Wei, Robert L. Brainard) (z-library.sk, 1lib.sk, z-lib.sk).pdf` | Advanced Processes for 193-nm Immersion Lithography | 专著/硕博论文/标准 | 325 | `c2ded6b32db4` |  |
| 69 | `[071]` | `071_Immersion_Lithography_Ready_for_45_nm_Manufacturing_and_Beyond.pdf` | Immersion Lithography Ready for 45 nm Manufacturing and Beyond | 学术论文 | 7 | `3c4675195cb7` |  |
| 70 | `[072]` | `072_sanders2010.pdf` | Advances in Patterning Materials for 193 nm Immersion Lithography | 学术论文 | 40 | `cce743305e5f` |  |
| 71 | `[073]` | `073_stepanenko2006.pdf` | Top Coat or no Top Coat for immersion lithography? | 学术论文 | 17 | `d77ceb1f3474` |  |
| 72 | `[074]` | `074_129_564.pdf` | Auto Focus and Leveling Control of Large-Scale High-Precision Scan-Stage Using Driving Force and Surface Shape of the Stage | 学术论文 | 8 | `a1113f15b3ba` |  |
| 73 | `[075]` | `075_1_s2.0_S0967066118306488_main.pdf` | Beyond decentralized wafer/reticle stage control design: a double-Youla approach for enhancing synchronized motion | 学术论文 | 13 | `97d74e7b9094` | ★ |
| 74 | `[076]` | `076_2006_Trumper_Levitation_Linear_Motors_Precision_Positioning.pdf` | Levitation Linear Motors for Precision Positioning | 学术论文 | 8 | `d27992d1cb59` |  |
| 75 | `[077]` | `077_2008_Baggen_Data_Based_MIMO_Feedforward_Wafer_Stage.pdf` | Data-Based Feed-Forward Control in MIMO Motion Systems | 学术论文 | 6 | `0cc61c36cace` |  |
| 76 | `[078]` | `078_2008_Mishra_ILC_Synchronization_WS_RS.pdf` | Iterative Learning Control Design for Synchronization of Wafer and Reticle Stages | 学术论文 | 6 | `9a8cd74e2dfb` |  |
| 77 | `[079]` | `079_2008_Yu_Kim_6DOF_Maglev_Positioning_System.pdf` | Controller design and implementation of six-degree-of-freedom magnetically levitated positioning system with high precision | 学术论文 | 12 | `53efcbe26a63` |  |
| 78 | `[080]` | `080_2009_Heertjes_N_PID_Wafer_Stages.pdf` | Performance-improved design of N-PID controlled motion systems with applications to wafer stages | 学术论文 | 10 | `db96e0fe17b0` |  |
| 79 | `[081]` | `081_2011_Tanaka_Nikon_Environmentally_Compatible_Stage.pdf` | 電子線露光装置における環境適合ステージ開発 | 学术论文 | 8 | `f03facc2c02a` |  |
| 80 | `[082]` | `082_2016_Ohnishi_Decoupling_Control_High_Precision_Stage.pdf` | Decoupling Control Method for High-Precision Stages using Multiple Actuators considering the Misalignment among the Actuation Point, Center of... | 学术论文 | 7 | `e88de4466a10` |  |
| 81 | `[083]` | `083_2017_Oomen_Sparse_ILC_Wafer_Stage.pdf` | Sparse iterative learning control with application to a wafer stage | 学术论文 | 15 | `c4db6def2436` |  |
| 82 | `[084]` | `084_2023_Li_Data_Driven_MIMO_Feedforward_Lithographic_Stage.pdf` | 光刻机超精密运动台数据驱动 MIMO 定结构前馈控制 | 学术论文 | 11 | `858a46dff4b1` |  |
| 83 | `[085]` | `085_52_425.pdf` | 半導体露光装置の制御技術 | 学术论文 | 5 | `e0ede2497c7a` |  |
| 84 | `[086]` | `086_76_552.pdf` | スキャン光学エンコーダによるギャップ計測に関する一研究 | 学术论文 | 5 | `54b77d214160` |  |
| 85 | `[087]` | `087_76_KJ00006813286.pdf` | アクティブマスダンパによる露光装置の性能改善 | 学术论文 | 7 | `19548207d73c` |  |
| 86 | `[088]` | `088_Adaptive_Feedforward_for_a_Wafer_Stage_in_a_Lithographic_Tool.pdf` | Adaptive Feedforward for a Wafer Stage in a Lithographic Tool | 学术论文 | 7 | `b3063f8eba23` |  |
| 87 | `[089]` | `089_Connecting_System_Identification_and_Robust_Control_for_Next-Generation_Motion_Control_of_a_Wafer_Stage.pdf` | Connecting System Identification and Robust Control for Next-Generation Motion Control of a Wafer Stage | 学术论文 | 17 | `75ff9e51c887` |  |
| 88 | `[090]` | `090_Fujipress_IJAT-2-2-5.pdf` | Realization of Tubeless Stage in Semiconductor Exposure System | 学术论文 | 5 | `beab8bf617bf` |  |
| 89 | `[091]` | `091_main.pdf` | Multivariable $\mathcal { H } _ { \infty } / \mu$ feedback control design for high-precision wafer stage motion | 学术论文 | 17 | `06b0c626112c` |  |
| 90 | `[092]` | `092_Main_final.pdf` | Active deformation control for a magnetically-levitated planar motor mover | 学术论文 | 9 | `5d7e425e2187` |  |
| 91 | `[093]` | `093_Metis215047.pdf` | Modeling of a magnetically levitated planar actuator with moving magnets | 学术论文 | 12 | `d875250abc2f` |  |
| 92 | `[094]` | `094_Position_Control_in_Lithographic_Equipment_Applications_of_Control.pdf` | Position Control in Lithographic Equipment An Enabler for Current-Day Chip Manufacturing | 学术论文 | 20 | `9198e4d130a4` | ★ |
| 93 | `[095]` | `095_Set-point variation in learning schemes with applications to wafer scanners.pdf` | Set-point variation in learning schemes with applications to wafer scanners | 学术论文 | 12 | `0353ccee5a60` |  |
| 94 | `[096]` | `096_uehara2012.pdf` | Immersion and Dry ArF Scanners Enabling 22nm hp Production and Beyond | 学术论文 | 12 | `bbd0a5d72f11` |  |
| 95 | `[097]` | `097_043015_1.pdf` | Predicting distortions and overlay errors due to wafer deformation during chucking on lithography scanners | 学术论文 | 8 | `6a0bf2cdfb83` | ★ |
| 96 | `[098]` | `098_1045111.pdf` | Off-line mask-to-mask registration characterization as enabler for computational overlay | 学术论文 | 16 | `76219de6435f` |  |
| 97 | `[099]` | `099_109591I.pdf` | Intra-field stress impact on global wafer deformation | 学术论文 | 15 | `2e5ef85a3b28` |  |
| 98 | `[100]` | `100_113251K.pdf` | Run to run and model variability of overlay high order process corrections for mean intrafield signatures | 学术论文 | 10 | `cb2cee4b24c6` | ★ |
| 99 | `[101]` | `101_1132910.pdf` | Intra-field etch induced overlay penalties | 学术论文 | 10 | `3af60048f311` |  |
| 100 | `[102]` | `102_116150N.pdf` | On-product overlay characterization after stressed layer etch | 学术论文 | 14 | `6a549fe2399b` |  |
| 101 | `[103]` | `103_1249633.pdf` | Die-Level Nano-topography Metrology to characterize the stress-induced In-Plane Distortion contribution to overlay | 学术论文 | 5 | `c82fe472689f` |  |
| 102 | `[104]` | `104_167.pdf` | Pellicle-Induced Reticle Distortion: An Experimental Investigation | 学术论文 | 6 | `f08c5d143370` |  |
| 103 | `[105]` | `105_652013.pdf` | Optical Error Sensitivities of Immersion Lithography | 学术论文 | 11 | `1b21ba1fde18` |  |
| 104 | `[106]` | `106_74700O.pdf` | Reduced Pellicle Impact on Overlay using High Order Intrafield Grid Corrections | 学术论文 | 11 | `166fada2632e` |  |
| 105 | `[106]` | `106_Reduced pellicle impact on overlay using high order intrafield grid corrections.pdf` | Reduced Pellicle Impact on Overlay using High Order Intrafield Grid Corrections | 学术论文 | 11 | `c7c6124b1f12` |  |
| 106 | `[107]` | `107_752023.pdf` | Overlay Improvement by ASML HOWA 5th Alignment Strategy | 学术论文 | 5 | `fc3e2f91fc32` |  |
| 107 | `[108]` | `108_806.pdf` | Process Induced Wafer distortion: measurement and effects on Overlay in stepper based advanced lithography | 学术论文 | 8 | `58e16c1d8c56` |  |
| 108 | `[109]` | `109_905013.pdf` | Monitoring Process-Induced Overlay Errors through High-Resolution Wafer Geometry Measurements | 学术论文 | 9 | `9e0f527542c3` |  |
| 109 | `[110]` | `110_905014.pdf` | Investigation on reticle heating effect induced overlay error | 学术论文 | 10 | `204912f00aad` |  |
| 110 | `[111]` | `111_90502F.pdf` | Focus control budget analysis for critical layers of flash devices | 学术论文 | 7 | `1e178c2b5cb1` |  |
| 111 | `[112]` | `112_90520U.pdf` | Characterization and mitigation of overlay error on silicon wafers with nonuniform stress | 学术论文 | 12 | `28d3896b600f` |  |
| 112 | `[112]` | `112_Characterization and mitigation of overlay error on silicon wafers with nonuniform stress.pdf` | Characterization and mitigation of overlay error on silicon wafers with nonuniform stress | 学术论文 | 12 | `8c68f051e328` |  |
| 113 | `[113]` | `113_923522.pdf` | Impact of reticle writing errors on the on-product overlay performance | 学术论文 | 9 | `601ab28cfcab` |  |
| 114 | `[114]` | `114_963507.pdf` | Higher order feed-forward control of reticle writing error fingerprints | 学术论文 | 11 | `3a843d42b610` | ★ |
| 115 | `[115]` | `115_97781Y.pdf` | Holistic Overlay Control for Multi-Patterning Process layers at the 10-nm and 7-nm nodes | 学术论文 | 8 | `3c18440b41d3` |  |
| 116 | `[116]` | `116_97783D.pdf` | Co-optimization of RegC® and TWINSCANTM corrections to improve the intra-field on-product overlay performance | 学术论文 | 21 | `e9e134083de1` |  |
| 117 | `[117]` | `117_97800W.pdf` | Patterned Wafer Geometry(PWG) metrology for improving process-induced overlay and focus problems | 学术论文 | 10 | `ae59ab9b103d` |  |
| 118 | `[118]` | `118_A wafer-shape based model for predicting in-plane distortion.pdf` | A wafer-shape based model for predicting in-plane distortion | 学术论文 | 11 | `2116ca5b9653` |  |
| 119 | `[119]` | `119_Advanced overlay stability control with correction per exposure on immersion scanners.pdf` | Advanced overlay stability control with correction per exposure on immersion scanners | 学术论文 | 6 | `843f99220433` |  |
| 120 | `[120]` | `120_Advances in process overlay on 300-mm wafers.pdf` | Advances in Process Overlay on 300 mm wafers | 学术论文 | 10 | `3605ace356eb` |  |
| 121 | `[121]` | `121_Characterization of wafer geometry and overlay error on silicon wafers with nonuniform stress.pdf` | Characterization of wafer geometry and overlay error on silicon wafers with nonuniform stress | 学术论文 | 13 | `efd20efe8c9b` |  |
| 122 | `[122]` | `122_Conformal_slip-free_wafer_chucking_using_an_actuated_wafer_table.pdf` | Conformal slip-free wafer chucking using an actuated wafer table | 学术论文 | 5 | `87043bfbe465` | ★ |
| 123 | `[123]` | `123_High-order wafer alignment in manufacturing.pdf` | High Order Wafer Alignment in Manufacturing | 学术论文 | 11 | `67b8041faadd` |  |
| 124 | `[124]` | `124_Pattern positioning error of reticle writing induced by reticle clamping.pdf` | Effects of chrome pattern characteristics on image placement due to thermomechanical distortion of optical reticles during exposure | 学术论文 | 6 | `46dfacf9cd98` |  |
| 125 | `[125]` | `125_Reducing overlay sampling for APC-based correction per exposure by replacing measured data with computational predictio.pdf` | Reducing overlay sampling for APC-based correction per exposure by replacing measured data with computational prediction | 学术论文 | 6 | `cb9e46af7e34` |  |
| 126 | `[126]` | `126_Using intrafield high-order correction to achieve overlay requirement beyond sub-40nm node.pdf` | Using Intra-Field High Order Correction to Achieve Overlay Requirement beyond Sub-40nm Node | 学术论文 | 9 | `a4b4cf75f9f3` | ★ |
| 127 | `[127]` | `127_EP3887905B1_对称非对称放大率透镜组与光学畸变抑制.pdf` | EP3887905B1 — 对称非对称放大率透镜组与光学畸变抑制 (Optical Distortion Reduction in Projection Systems) | 专利 | 59 | `df503ec0c0b2` | ★ |
| 128 | `[128]` | `128_US10996573B2_投影系统畸变与掩模图形定位协同优化.pdf` | US10996573B2 — 投影系统畸变与掩模图形定位协同优化 | 专利 | 28 | `179ee5e374ea` |  |
| 129 | `[129]` | `129_US8237914B2_扫描路径动态场内套刻校正.pdf` | US8237914B2 — 扫描路径动态场内套刻校正 | 专利 | 14 | `148c2196941d` |  |
| 130 | `[130]` | `130_us8947630b2_source_a1b3221a9d83.pdf` | US8947630B2 — Lithographic Apparatus and Device Manufacturing Method | 专利 | 19 | `a1b3221a9d83` |  |
| 131 | `[130]` | `130_US8947630B2_对称与非对称场放大率漂移补偿.pdf` | US8947630B2 — 对称与非对称场放大率漂移补偿 | 专利 | 18 | `c404ea5b0439` |  |
| 132 | `[131]` | `131_WO2005109105A2_动态扫描场内畸变测定与控制.pdf` | WO2005109105A2 — 动态扫描场内畸变测定与控制 | 专利 | 54 | `3506bb657b6e` |  |
| 133 | `[132]` | `132_US10571816B2_带重力补偿的投影物镜洛伦兹致动器.pdf` | US10571816B2 — 带重力补偿的投影物镜洛伦兹致动器 | 专利 | 13 | `760bd6eb0e50` |  |
| 134 | `[133]` | `133_US20190170991A1_光瞳面可变形反射镜波前操纵.pdf` | US20190170991A1 — 光瞳面可变形反射镜波前操纵 | 专利 | 26 | `8276ecaf4eae` |  |
| 135 | `[134]` | `134_US20230393485A1_可逆形变光学操纵器.pdf` | US20230393485A1 — 可逆形变光学操纵器 | 专利 | 16 | `ca88334411e3` |  |
| 136 | `[135]` | `135_US7551361B2_场平面双面非球面透镜调控视场畸变.pdf` | US7551361B2 — 场平面双面非球面透镜调控视场畸变 | 专利 | 34 | `576172fa9bf0` |  |
| 137 | `[136]` | `136_US8319944B2_Z向镜片间距调节畸变与倍率.pdf` | US8319944B2 — Z 向镜片间距调节畸变与倍率 | 专利 | 30 | `0e7cb5fdaefb` |  |
| 138 | `[137]` | `137_US8873022B2_EUV凹面镜纳米级动态形变校正.pdf` | US8873022B2 — EUV 凹面镜纳米级动态形变校正 (Projection Exposure Method, System and Objective) | 专利 | 35 | `bf982d0a9f84` | ★ |
| 139 | `[138]` | `138_WO2016041805A1_EUV异向成像比例与动态波前操纵.pdf` | WO2016041805A1 — EUV 异向成像比例与动态波前操纵 | 专利 | 40 | `6c624adf8b2c` |  |
| 140 | `[139]` | `139_US8570485B2_随狭缝与扫描位置变化的镜头加热与操纵器模型.pdf` | US8570485B2 — 随狭缝与扫描位置变化的镜头加热与操纵器模型 (Lens Heating Compensation Systems and Methods) | 专利 | 30 | `0d66e5b81eef` |  |
| 141 | `[140]` | `140_US9164401B2_力框测量框分离的高精度六轴光学元件定位.pdf` | US9164401B2 — 力框测量框分离的高精度六轴光学元件定位 | 专利 | 16 | `18d83613bc21` |  |
| 142 | `[141]` | `141_WO2022233542A1_投影系统光学元件致动器与驱动反作用力衰减.pdf` | WO2022233542A1 — 投影系统光学元件致动器与驱动反作用力衰减 | 专利 | 20 | `aaa10a949038` |  |
| 143 | `[144]` | `144_nikon_iwaps_2022_absolute_coordinate_overlay.pdf` | Overlay control by absolute coordinate adjustment and calibration method | 学术论文 | 31 | `1068e45dd2af` |  |
| 144 | `[145]` | `145_bacus_newsletter_july_2018_intra_field_mask_to_mask_o.pdf` | Intra-field mask-to-mask overlay, separating the mask writing from the dynamic pellicle contribution | 学术论文 | 11 | `19109c4363b4` |  |
| 145 | `[146]` | `146_on_the_systematic_use_of_budget_based_design.pdf` | On the Systematic Use of Budget-Based Design | 学术论文 | 16 | `b5f559746fd8` |  |
| 146 | `[147]` | `147_data_based_motion_control_of_wafer_scanners.pdf` | Data-Based Motion Control of Wafer Scanners | 学术论文 | 12 | `66d774abc526` |  |
| 147 | `[148]` | `148_lens_distortion_for_liquid_renovation_in_immersion_li.pdf` | Lens distortion for liquid renovation in immersion lithography | 学术论文 | 5 | `7bb529ed3d0c` |  |
| 148 | `[149]` | `149_next_generation_wafer_stage_motion_control_connecting.pdf` | Next-Generation Wafer Stage Motion Control: Connecting System Identification and Robust Control | 学术论文 | 6 | `956f431046a8` |  |
| 149 | `[150]` | `150_advanced_overlay_control_in_volume_manufacturing.pdf` | Advanced Overlay Control in Volume Manufacturing | 学术论文 | 6 | `202bc8dab470` | ★ |
| 150 | `[151]` | `151_effect_of_sparse_or_asymmetric_sampling_on_the_estima.pdf` | Effect of Sparse or Asymmetric Sampling on the Estimation of Photolithography Overlay Regression Parameters | 学术论文 | 6 | `3e37659498cc` |  |
| 151 | `[152]` | `152_magnetically_levitated_planar_actuator_with_moving_ma.pdf` | Magnetically levitated planar actuator with moving magnets | 学术论文 | 9 | `516e0f9440e6` |  |
| 152 | `[153]` | `153_simulation_of_the_coupled_thermal_optical_effects_for.pdf` | Simulation of the coupled thermal/optical effects for liquid immersion nanolithography | 学术论文 | 39 | `ce5b809ac434` |  |
| 153 | `[154]` | `154_high_order_field_to_field_corrections_for_imaging_and.pdf` | High Order Field-to-Field Corrections for Imaging and Overlay to Achieve Sub 20-nm Lithography Requirements | 学术论文 | 13 | `48a0bf8eb081` | ★ |
| 154 | `[155]` | `155_integrated_production_overlay_field_by_field_control.pdf` | Integrated Production Overlay Field-by-Field Control for Leading Edge Technology Nodes | 学术论文 | 10 | `928a7f29bf8b` |  |
| 155 | `[156]` | `156_high_order_overlay_modeling_and_apc_simulation_with_z.pdf` | High Order Overlay Modeling and APC simulation with Zernike-Legendre Polynomials | 学术论文 | 10 | `2f10e476b198` |  |
| 156 | `[157]` | `157_overlay_and_edge_placement_control_strategies_for_the.pdf` | Overlay and Edge Placement Control Strategies for the 7-nm node using EUV and ArF lithography | 学术论文 | 13 | `c52e9e4e5142` |  |
| 157 | `[158]` | `158_influence_of_the_process_induced_asymmetry_on_the_acc.pdf` | Influence of the process-induced asymmetry on the accuracy of overlay measurements | 学术论文 | 9 | `60f2e2ffeef7` |  |
| 158 | `[159]` | `159_scanner_baseliner_monitoring_and_control_in_high_volu.pdf` | Scanner Baseliner Monitoring and Control in High Volume Manufacturing | 学术论文 | 6 | `ce132dd3884d` |  |
| 159 | `[160]` | `160_high_order_aberration_control_during_exposure_for_lea.pdf` | High-order aberration control during exposure for leading-edge lithography projection optics | 学术论文 | 8 | `9ee189fd3a42` | ★ |
| 160 | `[161]` | `161_improvement_of_euv_mix_match_overlay_for_production_i.pdf` | Improvement of EUV mix-match overlay for production implementation | 学术论文 | 8 | `84c973df4eb3` |  |
| 161 | `[162]` | `162_reducing_the_impact_of_etch_induced_pattern_shift_on.pdf` | Reducing the impact of etch-induced pattern shift on overlay by using lithography and etch tool corrections | 学术论文 | 9 | `3402b8535e3e` |  |
| 162 | `[163]` | `163_immersion_effects_on_lithography_system_performance.pdf` | Immersion Effects on Lithography System Performance | 学术论文 | 12 | `c2a2397d8650` |  |
| 163 | `[164]` | `164_hardware_materials_and_parameters_optimization_for_im.pdf` | Hardware, materials, and parameters optimization for improvement of immersion overlay | 学术论文 | 8 | `ef4d5cb07ae5` |  |
| 164 | `[165]` | `165_toward_3_nm_overlay_and_critical_dimension_uniformity.pdf` | Towards 3nm overlay and critical dimension uniformity: an integrated error budget for double patterning lithography | 学术论文 | 9 | `59851ca4075e` | ★ |
| 165 | `[166]` | `166_advance_overlay_correction_beyond_32nm_dram_process.pdf` | Advance Overlay Correction beyond 32nm DRAM Process | 学术论文 | 6 | `c18c9faec01e` |  |
| 166 | `[167]` | `167_immersion_specific_error_contribution_to_overlay_cont.pdf` | Immersion Specific Error Contribution to Overlay Control | 学术论文 | 6 | `621e0f59719a` |  |
| 167 | `[168]` | `168_mask_contribution_on_cd_and_ovl_errors_budgets_for_do.pdf` | Mask contribution on CD & OVL errors budgets for Double Patterning Lithography | 学术论文 | 13 | `4c75921887fa` |  |
| 168 | `[169]` | `169_overlay_control_methodology_comparison_field_by_field.pdf` | Overlay control methodology comparison: field-by-field and high-order methods | 学术论文 | 9 | `0440ef0941ed` |  |
| 169 | `[170]` | `170_10_12086_oee_2023_220226.pdf` | Opto-Electronic Engineering | 学术论文 | 14 | `68c8bda4102a` |  |
| 170 | `[171]` | `171_wafer_based_aberration_metrology_for_lithographic_sys.pdf` | Wafer-based aberration metrology for lithographic systems using overlay measurements on targets imaged from phaseshift gratings | 学术论文 | 22 | `dabb53d75991` |  |
| 171 | `[171]` | `171_wafer_based_aberration_metrology_for_lithographic_sys_source_479b5fcd2336.pdf` | Wafer based aberration metrology for lithographic systems using overlay measurements on targets imaged from phase-shift gratings | 学术论文 | 20 | `479b5fcd2336` |  |
| 172 | `[172]` | `172_variable_gain_motion_control_of_wafer_scanners.pdf` | Variable gain motion control of wafer scanners | 学术论文 | 12 | `fa9b74a101f9` |  |
| 173 | `[173]` | `173_suppressing_non_collocated_disturbances_in_inferentia.pdf` | Suppressing non-collocated disturbances in inferential motion control: with application to a wafer stage | 学术论文 | 6 | `609c8c77f2ba` |  |
| 174 | `[174]` | `174_10_37155_2717_5197_0802_37.pdf` | 光刻机精密机电部件的调试与校准技术研究 | 学术论文 | 3 | `757741944a6c` |  |
| 175 | `[175]` | `175_10_3788_aos241643.pdf` | 套刻标记光学模型建立及性能参数仿真方法 | 学术论文 | 10 | `3e8712e51211` |  |
| 176 | `[176]` | `176_10_3788_lop202259_0922023.pdf` | 光刻套刻误差测量技术 | 学术论文 | 12 | `e467f927e0e7` |  |
| 177 | `[177]` | `177_10_3788_lop51_021201.pdf` | 基于二维周期结构衍射的套刻测量技术研究 | 学术论文 | 6 | `025571e2810e` |  |
| 178 | `[178]` | `178_do_useful_multi_domain_methods_exist.pdf` | Do Useful Multi-Domain Methods Exist? | 学术论文 | 18 | `77e80b894218` |  |
| 179 | `[179]` | `179_cn117234040a.pdf` | CN117234040A — 方法和更换工具 | 专利 | 29 | `7d3ef60ee1f5` |  |
| 180 | `[180]` | `180_cn120344910a.pdf` | CN120344910A — 基于掩模版形状测量来推断和估计掩模版温度的方法 | 专利 | 26 | `8522703e5b19` |  |
| 181 | `[181]` | `181_de102016205618a1.pdf` | DE102016205618A1 — Projektionsobjektiv mit Wellenfrontmanipulator, Projektionsbelichtungsverfahren und Projektionsbelichtungsanlage | 专利 | 72 | `b0d416ca7fd7` |  |
| 182 | `[182]` | `182_ep4632488a1.pdf` | A METHOD OF LITHOGRAPHY AND ASSOCIATED APPARATUSES | 专利 | 23 | `36000e7dabee` |  |
| 183 | `[183]` | `183_jp5809458b2.pdf` | JP5809458B2 — Reticle clamp system | 专利 | 19 | `6667deed44c1` |  |
| 184 | `[184]` | `184_us10120292b2.pdf` | US10120292B2 — Support apparatus, lithographic apparatus and device manufacturing method | 专利 | 35 | `a9be4a6b8146` | ★ |
| 185 | `[185]` | `185_us10429749b2.pdf` | US10429749B2 — Method of reducing effects of reticle heating and/or cooling in a lithographic process | 专利 | 16 | `bbe3698aa7c8` |  |
| 186 | `[186]` | `186_us10747126b2.pdf` | US10747126B2 — Support table for a lithographic apparatus, lithographic apparatus and device manufacturing method | 专利 | 30 | `4f18e1111c87` | ★ |
| 187 | `[187]` | `187_us10884345b2.pdf` | US10884345B2 — Calibration method for a lithographic apparatus | 专利 | 22 | `e78f39b295b4` |  |
| 188 | `[188]` | `188_us11175593b2.pdf` | US11175593B2 — Alignment sensor apparatus for process sensitivity compensation | 专利 | 41 | `72a88475a34e` |  |
| 189 | `[189]` | `189_us11300886b2.pdf` | METHOD OF ADAPTING FEED-FORWARD PARAMETERS | 专利 | 13 | `8101c8e9dc90` |  |
| 190 | `[190]` | `190_us11513444b2.pdf` | US11513444B2 — Noise reduction for overlay control | 专利 | 17 | `cc6fdf4ad59e` |  |
| 191 | `[191]` | `191_us11599027b2.pdf` | US11599027B2 — Lithographic process and apparatus and inspection process and apparatus | 专利 | 19 | `4fa17973c3a0` |  |
| 192 | `[192]` | `192_us11703772b2.pdf` | US11703772B2 — Recipe selection based on inter-recipe consistency (US11703772B2) | 专利 | 36 | `a872556312da` |  |
| 193 | `[193]` | `193_us11754931b2.pdf` | METHOD FOR DETERMINING CORRECTIONS FOR LITHOGRAPHIC APPARATUS | 专利 | 20 | `decd80102dee` |  |
| 194 | `[194]` | `194_us11886124b2.pdf` | US11886124B2 — Flows of optimization for patterning processes | 专利 | 50 | `b21ee29dc652` |  |
| 195 | `[195]` | `195_us12663725b2.pdf` | US12663725B2 — Methods and systems to calibrate reticle thermal effects (US12663725B2) | 专利 | 26 | `a3a83fc84b12` |  |
| 196 | `[196]` | `196_us20020008861a1.pdf` | US20020008861A1 — Projection lens, in particular for microlithography | 专利 | 14 | `4d01d12a77f5` |  |
| 197 | `[197]` | `197_us20090207511a1.pdf` | US20090207511A1 — Assembly for adjusting an optical element | 专利 | 20 | `c180459af2f4` |  |
| 198 | `[198]` | `198_us20130188160a1.pdf` | US20130188160A1 — Optical System of a Microlithographic Projection Exposure Apparatus and Method of Reducing Image Placement Errors | 专利 | 22 | `ab3b6ee8f899` |  |
| 199 | `[199]` | `199_us20180081281a1.pdf` | US20180081281A1 — Projection lens with wave front manipulator and related method and apparatus | 专利 | 20 | `73b882eed695` |  |
| 200 | `[200]` | `200_us20190041758a1.pdf` | US20190041758A1 — Methods of determining a mechanical property of a layer applied to a substrate, control system for a lithographic apparatus ... | 专利 | 14 | `8293b7e808d4` |  |
| 201 | `[201]` | `201_us20200089127a1.pdf` | US20200089127A1 — Projection exposure method and projection exposure apparatus for microlithography | 专利 | 24 | `9a5dc19e8625` |  |
| 202 | `[202]` | `202_us20210096472a1.pdf` | CONTROL METHOD FOR A SCANNING EXPOSURE APPARATUS | 专利 | 15 | `3527aebf901e` |  |
| 203 | `[203]` | `203_us20220146946a1.pdf` | METHOD FOR CONTROLLING A LITHOGRAPHIC APPARATUS AND ASSOCIATED APPARATUSES | 专利 | 20 | `d7b88b0b703c` |  |
| 204 | `[204]` | `204_us20230077090a1.pdf` | US20230077090A1 — Magnification adjustable projection system using deformable lens plates | 专利 | 23 | `1e7592445397` |  |
| 205 | `[205]` | `205_us20230400772a1.pdf` | US20230400772A1 — Method and swapping tool | 专利 | 24 | `b931cde5bfbb` |  |
| 206 | `[206]` | `206_us20240184221a1.pdf` | US20240184221A1 — Alignment method and associated alignment and lithographic apparatuses | 专利 | 13 | `d5111c1e50fc` |  |
| 207 | `[207]` | `207_us20250021017a1.pdf` | US20250021017A1 — Methods and systems to calibrate reticle thermal effects | 专利 | 26 | `6a2fb372e388` |  |
| 208 | `[208]` | `208_us20250110413a1.pdf` | US20250110413A1 — Method for compensating actuator effects of actuators | 专利 | 14 | `26559a08f974` |  |
| 209 | `[209]` | `209_us6961116b2.pdf` | US6961116B2 — Lithographic apparatus, device manufacturing method, and device manufactured thereby | 专利 | 32 | `8a1d141c5d2e` |  |
| 210 | `[210]` | `210_us7362446b2.pdf` | US7362446B2 — Position measurement unit, measurement system and lithographic apparatus comprising such position measurement unit | 专利 | 16 | `95a5d07d506a` |  |
| 211 | `[211]` | `211_us7423725b2.pdf` | US7423725B2 — Lithographic method | 专利 | 14 | `2f1a82be6d59` |  |
| 212 | `[212]` | `212_us8184265b2.pdf` | US8184265B2 — Correction method for non-uniform reticle heating in a lithographic apparatus | 专利 | 15 | `ce9bb94c3dd8` |  |
| 213 | `[213]` | `213_us8208120b2.pdf` | US8208120B2 — Lithographic apparatus and device manufacturing method | 专利 | 23 | `33a11f1c32d3` |  |
| 214 | `[214]` | `214_us8269949b2.pdf` | US8269949B2 — Lithographic apparatus and device manufacturing method | 专利 | 9 | `e65b42c94025` |  |
| 215 | `[215]` | `215_us8659745b2.pdf` | US8659745B2 — Optical system with an exchangeable, manipulable correction arrangement for reducing image aberrations | 专利 | 24 | `4a88da77d5c5` |  |
| 216 | `[216]` | `216_us9069263b2.pdf` | US9069263B2 — Method for improving the imaging properties of a projection objective, and such a projection objective | 专利 | 30 | `a62e4347e754` |  |
| 217 | `[217]` | `217_us9772561b2.pdf` | US9772561B2 — Semiconductor manufacturing method and tool | 专利 | 17 | `e3cc969751dc` |  |
| 218 | `[218]` | `218_wo2017108453a1.pdf` | METHODS OF CONTROLLING A PATTERNING PROCESS, DEVICE MANUFACTURING METHOD, CONTROL SYSTEM FOR A LITHOGRAPHIC APPARATUS AND LITHOGRAPHIC APPARATUS | 专利 | 43 | `a2fd3fd67db8` |  |
| 219 | `[219]` | `219_wo2020094369a1.pdf` | WO2020094369A1 — Apparatus for and method of measuring distortion of a patterning device in a photolithographic apparatus | 专利 | 25 | `f881a9e96d4c` |  |
| 220 | `[220]` | `220_wo2021032376a1.pdf` | METHOD FOR CONTROLLING A SEMICONDUCTOR MANUFACTURING PROCESS | 专利 | 33 | `edbb522a58fb` |  |
| 221 | `[221]` | `221_wo2023126174a1.pdf` | WO2023126174A1 — Enhanced alignment for a photolithographic apparatus | 专利 | 38 | `e5daae4a42e2` |  |
| 222 | `[222]` | `222_wo2024132326a1.pdf` | WO2024132326A1 — Method to infer and estimate reticle temperature based on reticle shape measurements | 专利 | 33 | `a291bfb7dd8e` |  |
| 223 | `[223]` | `223_jcgm_100_2008_evaluation_of_measurement_data_guide_to.pdf` | Evaluation of measurement data — Guide to the expression of uncertainty in measurement | 专著/硕博论文/标准 | 134 | `41bbf068fbc0` |  |
| 224 | `[224]` | `224_magnetically_levitated_planar_actuator_with_moving_ma.pdf` | Magnetically levitated planar actuator with moving magnets | 专著/硕博论文/标准 | 126 | `6e31bd8d5c04` |  |
| 225 | `[225]` | `225_reticle_side_wall_clamping.pdf` | Reticle side wall clamping | 专著/硕博论文/标准 | 155 | `2cf70b4ec278` | ★ |
| 226 | `[226]` | `226_imaging_and_overlay_parameters.pdf` | ASML Training: Imaging and Overlay Parameters | 官方手册/规格书 | 57 | `aebc0a33e5cc` |  |
| 227 | `[227]` | `227_in_line_calibrations.pdf` | ASML Training: In-line Calibrations | 官方手册/规格书 | 50 | `8e275aa26d09` |  |
| 228 | `[228]` | `228_system_correction.pdf` | ASML Training: System Correction | 官方手册/规格书 | 19 | `1d93794217d3` |  |
| 229 | `[229]` | `229_level_2_periodic_maintenance_training_metrology.pdf` | LEVEL 2 PERIODIC MAINTENANCE TRAINING - METROLOGY | 官方手册/规格书 | 44 | `02ff8dc9b4f7` |  |
| 230 | `[230]` | `230_lens_heating_on_twinscan_at3_3.pdf` | ASML Training: Lens Heating on TWINSCAN AT3.3 | 官方手册/规格书 | 51 | `431054a5ab57` |  |
| 231 | `[248]` | `248_design_and_control_of_a_piezoelectric_driven_reticle.pdf` | Design and control of a piezoelectric driven reticle assist device for prevention of reticle slip in lithography systems | 学术论文 | 10 | `082194cde249` |  |
| 232 | `[249]` | `249_holistic_analysis_of_aberration_induced_overlay_error.pdf` | Holistic analysis of aberration induced overlay error in EUV lithography | 学术论文 | 11 | `0eb613b5b3e9` |  |
| 233 | `[250]` | `250_impact_of_aberrations_in_euv_lithography_metal_to_via.pdf` | Impact of Aberrations in EUV Lithography: Metal to Via Edge Placement Control | 学术论文 | 10 | `ba4d6928e6a8` |  |
| 234 | `[251]` | `251_higher_order_intra_field_alignment_for_intra_wafer_le.pdf` | Higher order intra-field alignment for intra-wafer lens and reticle heating control | 学术论文 | 12 | `1001cdacbe9f` | ★ |
| 235 | `[252]` | `252_reduction_in_overlay_error_from_mark_asymmetry_using.pdf` | Reduction in overlay error from mark asymmetry using simulation, ORION, and alignment models | 学术论文 | 10 | `277370ad3131` |  |
| 236 | `[253]` | `253_on_scanner_high_spatial_frequency_overlay_control_usi.pdf` | On-Scanner High-Spatial-Frequency Overlay Control using a Distortion Manipulator | 学术论文 | 10 | `d054bfdabe17` | ★ |
| 237 | `[254]` | `254_supporting_future_dram_overlay_and_epe_roadmaps_with.pdf` | Supporting future DRAM overlay and EPE roadmaps with the NXT:2100i | 学术论文 | 13 | `2b7cddcca8f2` | ★ |
| 238 | `[255]` | `255_overlay_deviation_caused_by_mask_heating_during_euv_e.pdf` | Overlay deviation caused by mask heating during EUV exposure | 学术论文 | 12 | `bc5d64a6bec2` |  |
| 239 | `[256]` | `256_performance_of_a_step_and_scan_system_for_duv_lithogr.pdf` | PERFORMANCE OF A STEP AND SCAN SYSTEM FOR DUV LITHOGRAPHY | 学术论文 | 19 | `2413f39022d9` |  |
| 240 | `[257]` | `257_influence_of_the_vibration_of_extreme_ultraviolet_lit.pdf` | Influence of the vibration of extreme ultraviolet lithographic tool stages on imaging | 学术论文 | 14 | `f673602f1d2a` | ★ |
| 241 | `[258]` | `258_source_and_mask_optimization_for_stability_of_reticle.pdf` | Source and mask optimization for stability of reticle and wafer stages | 学术论文 | 15 | `4a6ab68bfbbf` |  |
| 242 | `[265]` | `265_magnetic_levitation_stage_for_photolithography.pdf` | High-precision magnetic levitation stage for photolithography | 学术论文 | 12 | `1ab3e8f4ba5a` |  |
| 243 | `[266]` | `266_performance_results_300mm_twinscan_lithography.pdf` | PERFORMANCE RESULTS OF A NEW GENERATION OF 300 mm LITHOGRAPHY SYSTEMS | 学术论文 | 14 | `a3d0faa017a9` | ★ |

---

<a name="sec-me3"></a>

## 3. 跨库配套引用手册（`ME3` 官方培训资料）与维护说明

[返回目录](#contents)

除本机 `OV4` 文献库外，OV4 规格推导报告还交叉引用了同机工作区 `D:\work\ME3` 中以下 ASML TWINSCAN 官方培训教材章节：

| 引用代号 | 来源资料 | 在 OV4 报告中的核心引用内容 |
| :--- | :--- | :--- |
| `ME3 12-TT-L3-L3-ME` | ASML TWINSCAN Level 3 Metrology Training Book（第 70 页） | 明确记录掩模侧（4×）曝光狭缝宽度 `22 mm`（除以 4 等于晶圆侧 `5.5 mm`），交叉确证 NA = 1.35 真实狭缝宽度。 |
| `ME3 08-TT-L3-RSbook` | ASML TWINSCAN Level 3 Reticle Stage Training Book | 掩模台（RS）`5 mK` 水平层流气幕温控、RS D-spec `2.0 m/s / 54 m/s²` 动态参数及 `SRSM`/`SRLF` 实测报表。 |
| `ME3 09-TT-L3-WSbook` | ASML TWINSCAN Level 3 Wafer Stage Training Book | `AT/XT 850D & 1250D` WS Type-2 `0.50 m/s / 13.5 m/s²`、`SWLF` 静止 `MA/MSD` 实测报表与 `TSDP ≤ 2.1 nm`（`XT:1400 ≤ 2.0 nm`）限值。 |
| `ME3 TT-PM-WS-3v1` | ASML TWINSCAN Level 2 Periodic Maintenance — Wafer Stage（Fig. 2.4） | `TSPE: Stages Performance Test` 固件界面截屏实证 **`Stages Error Coupling: Automatic / On / Off`** 开关（支撑 WS–RS 同步报告 v2 第 4 章）。 |
| `ME3 01_AP-L1-Hardware` | ASML TWINSCAN Level 1 Hardware Introduction v2（Slides 20–22） | `AT:400B/C`（i-line）与 `AT:750/850`（KrF）整机速度、产能与套刻规格对比。 |
| `ME3 08_AP_L2_LAB` | ASML TWINSCAN Level 2 Lens Aberration & Calibration Lab Manual | 投影物镜放大率对环境气压的灵敏度（`1–3 ppm/mbar`），用于第 9.2 节 `K3` 硬件总补偿 Range 第一性核算。 |

### 维护规则

1. 后续如在本机 `参考文献_新增/` 继续补充新论文/专利，请在本文件第 1 节追加 `[N9]`、`[N10]`……并同步更新第 0 节统计表、首页 [README.md](README.md) 更新历史及 [CHANGELOG.md](CHANGELOG.md)。
2. 原始 PDF 仍严格遵守 [REPOSITORY_MANAGEMENT.md](REPOSITORY_MANAGEMENT.md#sec-readonly) 只读红线，由 [.gitignore](.gitignore) 排除上传至 GitHub。
