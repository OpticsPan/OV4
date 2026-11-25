# 2026-11-25 变更日志：新增默认 `.md` 规范（UP-011）、NXT:1965Ci L0–L3 套刻拆解与误差传递报告（含 draw.io）及 XT i-line/KrF 同步调研 v2

[仓库首页](../README.md) · [总变更记录](../CHANGELOG.md) · [成果索引](../outputs/README.md) · [NXT:1965Ci 拆解报告 v1](../outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md) · [WS-RS 同步报告 v2](../outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md) · [参考文献总目](../REFERENCES.md#sec-wsrs-sync)

## 1. 变更目的

响应用户提出的三项协同任务，完成仓库治理升级、目标机台预算重锚定及 XT 世代同步机制专项补全：
1. **修订仓库默认报告格式规定（`UP-011`）**：以后未明确指定报告格式时，默认仅整理并交付 Markdown（`.md`）格式（严格遵守 `UP-010` GitHub 网页版阅读与公式渲染规范），不冗余自动生成 PDF/Excel/PPTX；
2. **修正目标机台至 ASML `NXT:1965Ci`（`SMO ≤ 2.50 nm`、`MMO ≤ 4.50 nm`）并吸收 `@github/Overlay3` 与 `Ref146` 方法论**：基于 `Ref009 Fig. 3` 像素核定比例建立 `L0 → L1 → L2 → L3` 全链路有向无环图（DAG）拆解与误差传递模型，输出报告正文嵌入式高清 `.png` 与可编辑 `.drawio` 源文件，系统评价用户的 `x → f(x;p) → F(f,x;P) → L0` 四层传递思路，并明确决定既有 `v2` 报告与 `v2` PPTX 的处理方案；
3. **补充 ASML `TWINSCAN XT` i-line 与 KrF 机台 WS–RS 同步专项调研（发布 `v2`）**：核定 `PAS 5500` 及 `TWINSCAN AT/XT`（i-line `AT/XT:400`、KrF `AT:750/850`、`XT:850/860/1000/1060K`）的主从跟从方向与实机同步/套刻参数，并下载归档 ASML 奠基同步专利 `[S14]` `US 6,373,072 B1`。

## 2. 本次交付与仓库变更清单

| 文件路径 | 变更类型 | 说明 |
| :--- | :---: | :--- |
| [USER_PREFERENCES.md](../USER_PREFERENCES.md#up-011) | 更新 | 新增 `UP-011`（未指定格式时默认仅整理为 `.md`），并将 `UP-005` 同步更新为“按需生效” |
| [REPOSITORY_MANAGEMENT.md](../REPOSITORY_MANAGEMENT.md#sec-artifacts) | 更新 | 同步第 5 节《默认报告格式（UP-011）与按需多形态交付规范》 |
| [AGENTS.md](../AGENTS.md) | 更新 | 同步第 3 节默认 `.md` 交付规则 |
| [outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md](../outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md) | 新增 | 全 6 章报告：内嵌 `L0–L3` 全景图、`Ref009 Fig. 3` 像素核定与 `SMO 2.352 ≤ 2.50 / DCO 2.244 / MMO 4.288 ≤ 4.50 nm` 闭环、18 项 `L3` 原生指标与 8 处 DAG 共享源台账、用户四层误差传递思路评价与 4 项工程补强、既有 `v2` 报告/PPTX 处置决策与 7 页 `v3` PPTX 升级映射表 |
| [outputs/images/NXT1965Ci_SMO2.5_MMO4.5_L0-L3套刻指标拆解图_v1.drawio](../outputs/images/NXT1965Ci_SMO2.5_MMO4.5_L0-L3套刻指标拆解图_v1.drawio) | 新增 | `Ref146 Fig. 3` 风格左→右 `L0–L3` 可编辑 draw.io 源图（无压缩标准 mxGraph XML，完整保留 DAG 虚线共享源与底部传递方程栏） |
| [outputs/images/NXT1965Ci_SMO2.5_MMO4.5_L0-L3套刻指标拆解图_v1.png](../outputs/images/NXT1965Ci_SMO2.5_MMO4.5_L0-L3套刻指标拆解图_v1.png) | 新增 | 180 DPI 高清矢量导出 PNG（0 缺字告警，已视觉复核零重叠零裁切，嵌入报告正文第 1 章） |
| [outputs/code/build_nxt1965ci_l0_l3_diagram_v1.py](../outputs/code/build_nxt1965ci_l0_l3_diagram_v1.py) | 新增 | 单一事实源生成脚本：自动校验 `SMO / DCO / MMO` 与 `Ref009 Fig. 3` 占比闭合，同步输出 `.drawio` 与 `.png` |
| [outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md](../outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md) | 新增 | 完整保留 `_v1.md`（`UP-008`），新增第 4 章 ASML `TWINSCAN XT`（i-line / KrF）专题调研、全谱系参数总表及 `AT/XT:850D` 官方手册实测明细 |
| [REFERENCES.md](../REFERENCES.md#sec-wsrs-sync) | 更新 | 登记 `[S14]` `US 6,373,072 B1`（全库更新至 **265 份原件 / 264 份唯一 SHA-256**，WS–RS 同步专利增至 **14 篇 / 375 页**），同步补录 `ME3` 3 份新增引用手册 |
| `D:\work\OV4\参考文献_新增\WS-RS同步\ASML_US6373072B1_Butler_WS_ErrorFeedforward_to_RS.pdf`（9 页，`.gitignore` 排除） | 本地下载 | 自 USPTO 官方下载并完成全部 9 页视觉核验（H. Butler & T. P. H. Warmerdam，ASM Lithography B.V.，1998 优先权 / 2002 授权，SHA-256 `5498a5161270`） |
| [README.md](../README.md#update-history)、[outputs/README.md](../outputs/README.md)、[CHANGELOG.md](../CHANGELOG.md#2026-11-25-nxt1965ci-l0-l3-and-xt-sync) | 更新 | 同步首页「更新历史」首行、成果索引与全局变更时间轴 |

## 3. 核心技术核验与工程决策要点

1. **`NXT:1965Ci`（`SMO ≤ 2.50 nm` / `MMO ≤ 4.50 nm`）数学闭环与 `Ref009 Fig. 3` 像素核定**：
   - `Ref009 Fig. 3` 像素读数（`77.8 px/nm`）确定 `NXT:1950i` 六大域占比为 Stage `20.0%`、Alignment `25.6%`、Optics `12.0%`、Wafer Heating+Immersion `16.0%`、Reticle `18.0%`、Wafer Clamping `8.4%`；
   - 通过方差占比投影统一至物理两层 RSS，本模型 `F1–F6` 占比偏差全项控制在 **`≤ ±0.5%`**；叠加 `F7`（双卡盘差 `ΔC2C = 0.48 nm` + 量测底噪 `0.34 nm`）得 **`SMO = 2.002 + 0.350 = 2.352 nm ≤ 2.50 nm`**（同卡盘 **`DCO = 2.244 nm`**），叠加跨机 `M1–M3` 得 **`MMO = 3.788 + 0.500 = 4.288 nm ≤ 4.50 nm`**。
2. **对既有 `v2` 套刻报告与 `v2` PPTX 的决策**：
   - **保留既有 `v2` 文档作为历史 `2.00/3.50 nm` 深度推导基线**（符合 `UP-008`），以新增的 `NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md` 作为新的整机顶层预算入口；
   - **遵循 `UP-011` 暂不擅自重绘 28 页 `v2` PPTX**，但在报告第 5.2 节给出精确的 **7 页增量修订清单**（含 `5.5 mm` 狭缝口径同步与 `2.50/4.50 nm` 重锚定），待用户确认是否生成 `v3` PPTX 后即可一键构建。
3. **ASML `TWINSCAN XT` i-line / KrF 同步策略核定**：
   - 经三重一手铁证（`[S14]` `US 6,373,072 B1` 全 9 页实验与框图、`ME3 TT-PM-WS-3v1` Fig. 2.4 `TSPE` GUI **`Stages Error Coupling`** 选项、`ME3 08/09-TT-L3-RS/WSbook` 实测报表）坐实：ASML `PAS 5500` 及 `TWINSCAN AT/XT` 全系 i-line（`AT/XT:400`）与 KrF（`AT:750/850`、`XT:850/860/1000/1060K`）**同样全部采用 RS 跟从 WS（WS = Master，RS = Slave）**；`US 6,373,072 B1` Col. 7 实测将 `MA X` 由 `11.4 nm` 压至 `1.0 nm`（降幅 `91.2%`），`AT/XT:850D` 整机 `TSDP` 净 `MA ≤ 2.1 nm`，`XT:1060K` 做到 `DCO ≤ 3.5 nm / MMO ≤ 5.0 nm`。
4. **质量门禁**：全仓所有 `.md` 已通过 `python outputs/code/audit_github_md_v1.py` 链接与 GitHub MathJax 公式双项 **`Errors: 0`** 核验。
