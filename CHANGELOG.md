# OV4 总变更记录（CHANGELOG）

[仓库首页](README.md) · [成果索引](outputs/README.md) · [仓库规范](REPOSITORY_MANAGEMENT.md) · [用户偏好](USER_PREFERENCES.md) · [协作规则](AGENTS.md)

本文件按时间倒序（最近更新排在最前面）记录 `OV4` 仓库的所有正式变更、交付物清单与核验范围。每次更新均与 [README.md 首页更新历史](README.md#update-history) 同步。

---

<a name="2026-11-26-nxt1965ci-overlay-primary-source"></a>

## 2026-11-26　NXT-1965Ci 套刻指标拆解报告

依据原始论文、专利与原厂资料重建 NXT-1965Ci 套刻预算，明确专用卡盘和参考晶圆匹配的验证条件，逐项定义 T1 部件、T2 装机动作和 T3 整机验收。 [套刻指标拆解报告](outputs/reports/NXT-1965Ci套刻指标拆解报告_v1.md) · [变更日志](changes/2026-11-26-nxt1965ci-overlay-primary-source-report_v1.md)

---

<a name="2026-11-26-enc-aa-stage-repeatability"></a>

## 2026-11-26　ENC、AA 与 WS/RS 重复性及分级验收专项答复

复核 ENC 计量链与闭环在位稳定性、AA 单标记及全片网格验收，给出 WS/RS 单程与往返试验定义和有条件放宽流程。 [专项报告 Markdown](outputs/reports/ENC_AA_WS-RS重复性与分级验收专项答复_v1.md) · [变更日志](changes/2026-11-26-enc-aa-stage-repeatability-acceptance_v1.md)

---

<a name="2026-11-25-nxt1965ci-clean-ref143"></a>

## 2026-11-25　冻结纠偏前 v1（UP-012），基于九大子系统说明书 v2 + Overlay3 报告 143 + 一手文献独立重建 NXT:1965Ci 主报告、Ref-146 风格 draw.io 与 18 页全新 PPTX

- **详细变更日志**：[2026-11-25-nxt1965ci-clean-ref143-budget-and-pptx_v1.md](changes/2026-11-25-nxt1965ci-clean-ref143-budget-and-pptx_v1.md)
- **治理与冻结**：新增 [UP-012](USER_PREFERENCES.md#up-012) 与 [AGENTS.md](AGENTS.md) 禁引红线，完整保留纠偏前 `v1` 报告/图件/脚本但正式标记为**【已归档冻结·不再作为后续参考】**。
- **正式交付入口（严格仅参考 OV4 v2 说明书 + Overlay3 报告 143 + 原始一手文献 Ref146/009/066/165/167/168）**：
  - [ASML TWINSCAN NXT:1965Ci（SMO 2.50 / MMO 4.50 nm）整机 L0–L3 拆解与九大子系统验收规格报告 v1 MD](outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v1.md)
  - [Ref-146 Fig. 3 风格可编辑 draw.io 源图](outputs/images/NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.drawio) · [180 DPI 高清 PNG](outputs/images/NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.png) · [单一事实源脚本](outputs/code/build_nxt1965ci_budget_and_diagram_v1.py)
  - [ASML NXT:1965Ci 18 页全新汇报演示文稿 PPTX v1](outputs/presentations/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与子系统验收规格_v1.pptx) · [PPTX 构建脚本](outputs/code/build_nxt1965ci_pptx_v1.py)
- **核验要点**：`Ref009 Fig. 3` 六大域方差占比全项误差 `≤ ±0.30%`，双轴闭环同卡盘 `DCO = 2.26` / 双卡盘 `SMO = 2.36 ≤ 2.50 nm` / `MMO = 4.29 ≤ 4.50 nm` / `FU = 11.48 ≤ 14.0 nm`；全部 18 页 PPTX 经 PowerPoint COM 导出 PNG 逐页视觉核检通过；全仓经 `audit_github_md_v1.py` 链接与公式双项 `Errors: 0`。

---

<a name="2026-11-25-nxt1965ci-l0-l3-and-xt-sync"></a>

## 2026-11-25　修订默认 `.md` 规范（UP-011）、新增 NXT:1965Ci（SMO 2.5 / MMO 4.5）L0–L3 拆解报告与 draw.io 源图、升级 WS–RS 同步报告 v2（含 XT i-line/KrF 专题与 `[S14]` 专利）

- **详细变更日志**：[2026-11-25-nxt1965ci-l0-l3-budget-and-xt-sync_v1.md](changes/2026-11-25-nxt1965ci-l0-l3-budget-and-xt-sync_v1.md)
- **规则更新**：新增 [UP-011（未指定报告格式时默认仅整理为 `.md`）](USER_PREFERENCES.md#up-011)，同步修订 [REPOSITORY_MANAGEMENT.md 第 5 节](REPOSITORY_MANAGEMENT.md#sec-artifacts) 与 [AGENTS.md](AGENTS.md)。
- **正式交付入口**：
  - [ASML NXT:1965Ci（SMO 2.50 / MMO 4.50 nm）L0–L3 套刻指标拆解与误差传递报告 v1 MD](outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md)（[全景拆解图](outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md#sec-1) · [Ref009 Fig. 3 像素核定与闭环](outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md#sec-2) · [用户四层误差传递思路评价](outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md#sec-4) · [既有报告/PPTX 决策](outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md#sec-5)）
  - [L0–L3 全景拆解图可编辑 draw.io 源图](outputs/images/NXT1965Ci_SMO2.5_MMO4.5_L0-L3套刻指标拆解图_v1.drawio) · [180 DPI 高清 PNG](outputs/images/NXT1965Ci_SMO2.5_MMO4.5_L0-L3套刻指标拆解图_v1.png) · [单一事实源生成脚本](outputs/code/build_nxt1965ci_l0_l3_diagram_v1.py)
  - [ArF / ArFi 及 ASML TWINSCAN XT（i-line / KrF）WS–RS 同步策略调研报告 v2 MD](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md)（完整保留 `v1`，新增 [第 4 章 XT i-line/KrF 专题](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md#sec-4)）
  - [参考文献总目 REFERENCES.md（新增 `[S14]` `US 6,373,072 B1`，全库 265 份原件）](REFERENCES.md#sec-wsrs-sync)
- **核验要点**：融合 `@github/Overlay3` 与 `Ref146` DAG 共享源框架及 `Ref009 Fig. 3` 像素测量闭环 `SMO 2.352 ≤ 2.50 nm` / `DCO 2.244 nm` / `MMO 4.288 ≤ 4.50 nm`；新下载并视觉核验 ASML 早期 `WS → RS` 奠基同步专利 `US 6,373,072 B1`（全 9 页）及 `ME3 TSPE` GUI 截图，证实 XT i-line/KrF 依然全部采用 RS 跟从 WS；全仓经 `audit_github_md_v1.py` 质检双项 `Errors: 0`。

---

<a name="2026-11-25-ws-rs-sync-survey-v1"></a>

## 2026-11-25　新增 WS–RS 同步策略（主从方向）与单台重复性误差专项调研报告 v1（含 13 篇 USPTO 专利入库）

- **详细变更日志**：[2026-11-25-ws-rs-sync-master-slave-repeatability-survey_v1.md](changes/2026-11-25-ws-rs-sync-master-slave-repeatability-survey_v1.md)
- **正式交付入口**：
  - [ArF / ArFi 光刻机 WS–RS 同步控制策略与单台重复性误差专项调研报告 v1 MD](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v1.md)（[核心结论](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v1.md#sec-0) · [主从专利核查](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v1.md#sec-2) · [单台重复性实测数据](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v1.md#sec-3) · [手动下载清单](outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v1.md#sec-5-3)）
  - [参考文献总目 REFERENCES.md（新增 S1–S13，全库 264 份原件）](REFERENCES.md#sec-wsrs-sync)
- **核验要点**：从 USPTO 官方直下 13 篇 ASML/Nikon 专利原件（8 ASML + 5 Nikon，366 页，全部经封面视觉核验与 SHA-256 唯一性校验）落盘至 `.gitignore` 保护的 `参考文献_新增/WS-RS同步/`；其中 Nikon `US 2012/0319637 A1` 首页控制框图直接证实 `wafer error → synch target filter H(s) → reticle stage` 主从链路；全仓经 `audit_github_md_v1.py` 质检通过（`Errors: 0`）。

---

<a name="2026-11-25-dco-budget-tree"></a>

## 2026-11-25　DCO 双层预算分配与子系统验收图

按 5.5 mm 狭缝重算 D1，按晶圆侧 X、Y 两轴衔接 11 项双层预算及其子系统规格。新增[可编辑图](outputs/images/DCO_budget_v1.drawio)、[五页图册](outputs/images/DCO_budget_v1.pdf)、[公式工作簿](outputs/tables/DCO_budget_v1.xlsx)、[使用说明](outputs/reports/DCO_budget_notes_v1.md)及[详细日志](changes/2026-11-25-dco-budget-tree_v1.md)。

---

<a name="2026-11-25-github-web-md-standard"></a>

## 2026-11-25　新增仓库规定：GitHub 网页版阅读与公式渲染强制适配（UP-010）并完成 v2 报告全量适配

- **详细变更日志**：[2026-11-25-github-web-md-math-standard_v1.md](changes/2026-11-25-github-web-md-math-standard_v1.md)
- **规则与质检入口**：
  - [USER_PREFERENCES.md (`UP-010`)](USER_PREFERENCES.md#up-010) · [REPOSITORY_MANAGEMENT.md 第 4.3 节](REPOSITORY_MANAGEMENT.md#sec-markdown) · [AGENTS.md](AGENTS.md)
  - 自动化质检脚本：[outputs/code/audit_github_md_v1.py](outputs/code/audit_github_md_v1.py)
- **同步修复的正式报告与构建脚本（数值 0 变更，纯 GitHub 网页版公式/排版升级）**：
  - [九大子系统说明书 v2 MD](outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md) · [PDF v2](outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.pdf) · [构建脚本](outputs/code/build_9subsys_doc_pdf_v2.py)
  - [15 大类验收规格推导报告 v2 MD](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md) · [PDF v2](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.pdf) · [构建脚本](outputs/code/build_spec_pdf_v2.py)
- **核验范围**：修复全部 167 处 GitHub MathJax 隐患（单行/深缩进 `$$` 改为 0 缩进多行 `$$` 块前后留空行、含 `≥2` 下划线/`*` 行内公式升级为 GitHub 官方 `` $`...`$ ``、表格内 `|`/`\|` 统一改 `\vert`、`\{`/`\}` 改 `\lbrace`/`\rbrace`、消除 `**$...$**`），`audit_github_md_v1.py` 链接与公式双项 `Errors: 0`，两份 PDF 重编译 0 报错 0 回退。

---

<a name="2026-11-25-reference-catalog"></a>

## 2026-11-25　归档全库参考文献清单总目（REFERENCES.md，251 份原件含新增 8 篇）

- **详细变更日志**：[2026-11-25-reference-catalog-inventory_v1.md](changes/2026-11-25-reference-catalog-inventory_v1.md)
- **正式交付入口**：
  - [OV4 参考文献完整清单总目 REFERENCES.md](REFERENCES.md)（[统计总览](REFERENCES.md#sec-0) · [新增 8 篇 N1–N8](REFERENCES.md#sec-new) · [243 份基线 003–266](REFERENCES.md#sec-base) · [跨库 ME3 手册](REFERENCES.md#sec-me3)）
- **核验要点**：全量扫描并记录本机 `参考文献_新增/`（8 份）与 `参考文献-整理版/`（243 份）全部 251 份原件的编号、文件名、清理后标题、分类、页数、SHA-256 指纹与报告引用状态；经 SHA-256 去重核查确认 `[N4] 113270T (1).pdf` 与基线 `[010]` 原件哈希一致（250 份唯一文献）；全仓 Markdown 相对路径审计 0 错。

---

<a name="2026-11-24-nine-subsystems-doc-v2"></a>

## 2026-11-24　发布九大核心子系统验收指标推导与计算说明书 v2（新增 8 篇一手文献全核验版）

- **详细变更日志**：[2026-11-24-nine-subsystems-doc-v2-new-refs-verification.md](changes/2026-11-24-nine-subsystems-doc-v2-new-refs-verification.md)
- **正式交付入口（完整保留 v1）**：
  - [九大核心子系统验收指标推导与计算说明书 MD v2](outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md)
  - [九大核心子系统验收指标推导与计算说明书 PDF v2（19 页 / 35 书签 / STIX 矢量公式 / 第 7–9 章横版宽表 / 零孤行尾页）](outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.pdf)
  - [PDF 导出构建脚本 v2](outputs/code/build_9subsys_doc_pdf_v2.py)
- **一手文献核验与修订要点**：通读并逐页核验 `参考文献_新增\` 全部 8 篇一手论文/专利（`[N1] US20080174858A1`、`[N2] SPIE 6154`、`[N3] SPIE 5962`、`[N4] SPIE 11327`、`[N5] SPIE 7973`、`[N6] SPIE 8326`、`[N7] JM3 2014`、`[N8] 2024 IEEE ECC`）：① 确证 `US20080174858A1` Table 3 `NA=1.35 / 26×5.5 mm` 原表铁证；② 引入 Heertjes 2024 ECC Theorem 2.1 / Prop. 3.1 补齐 `MA`/`MSD` 互补功率谱公式、白噪声下限 `0.050 nm`（`8 mm` 为 `0.042 nm`）解析及 FAT PSD/CPS 条款；③ 用 IBM/ASML SPIE 8326 Table 4 实证 `Z10 = -0.88 nm/nm`（与本文 Abbe 仿真 `0.905` 仅差 2.8%）与高透热漂 `>6 nm`；④ 引入 Zeiss/ASML 双平面操纵器正交矩阵、`79×17` 高密调校网、`12→15→18→19` 参数演进与 5 机 MMO `3.0–3.8 / 2.5 nm` 对标，并在 `.gitignore` 中排除 `/参考文献_新增/`；全仓 Markdown 相对路径审计 0 错。

---

<a name="2026-11-24-nine-subsystems-doc-v1"></a>

## 2026-11-24　新增九大核心子系统验收指标推导与计算说明书 v1（含 5.5 mm 狭缝、K3 Range 与 K0 专项调研核定）

- **详细变更日志**：[2026-11-24-nine-subsystems-derivation-doc-and-audit_v1.md](changes/2026-11-24-nine-subsystems-derivation-doc-and-audit_v1.md)
- **正式交付入口**：
  - [九大核心子系统验收指标推导与计算说明书 MD v1](outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v1.md)（全 11 章，覆盖 WS、RS、ENC、AA、TIS、PARIS、WS-iHOPC、Lens Zernike、Lens-iHOPC）
  - [九大核心子系统验收指标推导与计算说明书 PDF v1（19 页 / 34 书签 / STIX 矢量公式 / 第 7–9 章横版宽表）](outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v1.pdf)
  - [PDF 导出构建脚本](outputs/code/build_9subsys_doc_pdf_v1.py)
- **核定要点与验证**：确证 NA=1.35 物镜真实离轴狭缝为 `26 × 5.5 mm`（Carl Zeiss `US 2008/0174858 A1` / `US 8,873,022 B2` + ASML `ME3 12-TT-L3-L3-ME` + Nikon [060]）；澄清 `1 ppm = 10 nm/cm` 并将 `K3` 硬件总 Range 重估为 `±15–25 ppm`（`±150–250 nm/cm`）；结合 [100/114/251] 与第一性原理校核 Lens/WS `|K0|` 并整理 7 篇外部论文/专利下载清单；PDF 视觉抽检通过（0 处公式回退、0 处未解析粗体），全仓 Markdown 相对链接审计 0 错。

---

<a name="2026-11-24-spec-budget-v2"></a>

## 2026-11-24　发布 v2 深度验收升级版（WS/RS 单往返细则、WS Km 验收与狭缝逆卷积专页、物镜 8 维评价）

- **详细变更日志**：[2026-11-24-spec-budget-v2-acceptance-deepdive_v2.md](changes/2026-11-24-spec-budget-v2-acceptance-deepdive_v2.md)
- **正式交付入口（v2，完整保留全部 v1 文件）**：
  - [逐条证据链演示文稿 PPTX v2（28 页 16:9 / 新增 6 页深度验收专题 + 3 张 260 DPI 新图）](outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v2.pptx)
  - [Excel 动态预算与验收细则表 v2（9 表 / 686 公式 / Excel 实算 0 错）](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v2.xlsx)
  - [Markdown 正式报告 v2（增补第 1.3–1.4、2.2–2.3、13.4、14.3–14.4 节）](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md)
  - [PDF 正式报告 v2（30 页 / 45 书签 / STIX 透明矢量公式 / 第 13–15 章横版宽表）](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.pdf)
  - 可复现代码：[build_spec_excel_v2.py](outputs/code/build_spec_excel_v2.py) · [build_spec_pdf_v2.py](outputs/code/build_spec_pdf_v2.py) · [build_spec_pptx_v2.py](outputs/code/build_spec_pptx_v2.py)
- **核验范围**：Excel v2 经 Microsoft Excel COM 重算确认 9 表 686 公式 `FormulaErrorsCount = 0`；PPTX v2 新增/修订页（P01/06/07/09/22/24/25/28）经 PowerPoint COM 导出高清 PNG 逐页视觉核验通过；PDF v2 30 页 45 书签 0 mathtext 警告并完成视觉抽检；全仓 Markdown 相对路径与锚点审计 0 错。

---

<a name="2026-11-24-spec-budget-pptx-v1"></a>

## 2026-11-24　新增 15 大类验收规格与逐条证据链 22 页 PPTX 及 4 份可复现脚本

- **详细变更日志**：[2026-11-24-spec-budget-evidence-pptx_v1.md](changes/2026-11-24-spec-budget-evidence-pptx_v1.md)
- **正式交付入口**：
  - [逐条证据链演示文稿 PPTX v1（22 页 16:9 / 原始论文截图 + 4 张仿真图）](outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v1.pptx)
  - 可复现代码：[PPTX 构建脚本](outputs/code/build_spec_pptx_v1.py) · [Abbe 仿真脚本](outputs/code/sim_zernike_ovl_v1.py) · [Excel 生成脚本](outputs/code/build_spec_excel_v1.py) · [PDF 导出脚本](outputs/code/build_spec_pdf_v1.py)
  - 配套基线：[Excel 动态预算表](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) · [Markdown 报告](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) · [PDF 报告](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf)
- **核验范围**：全部 22 页幻灯片经本机 PowerPoint COM 导出 PDF 并转 PNG 逐页视觉核检，已修正 P02（066 Fig.2 全 4 联图高清裁切）、P18（253 Fig.8 SET-vs-GET 实测图）与 P19（8 mm 狭缝去卷积图放大）并复检通过；全仓 Markdown 相对路径与锚点链接审计 0 错；已推送至远端 `OpticsPan/OV4` (`main`)。

---

<a name="2026-11-24-antigravity-v1"></a>

## 2026-11-24　归档反重力 Agent 的验收规格与误差预算 v1

反重力 Agent 的结果。GPT（Codex）按用户指定的文件和署名归档，核对三份原件的 SHA-256。

[Markdown 报告](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) · [PDF 报告](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf) · [Excel 预算表](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) · [本次归档记录](changes/2026-11-24-archive-nxt1950i-1970i-antigravity_v1.md)

---

<a name="2026-11-23-repo-governance-and-pdf-v1"></a>

## 2026-11-23　建立仓库治理体系、规范归档 v1 成果并输出 24 页正式 PDF 报告

- **详细变更日志**：[2026-11-23-ov4-repo-setup-and-1950i-1970i-spec-baseline_v1.md](changes/2026-11-23-ov4-repo-setup-and-1950i-1970i-spec-baseline_v1.md)
- **正式交付入口**：
  - [PDF 正式报告 v1（24 页 / 38 书签 / 横版宽表）](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf)
  - [Markdown 正式报告 v1（GitHub 网页版，带目录与稳定锚点）](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md)
  - [Excel 动态预算表 v1（6 表 / 430 公式 / 0 错）](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx)
  - 治理文档：[README.md](README.md) · [REPOSITORY_MANAGEMENT.md](REPOSITORY_MANAGEMENT.md) · [USER_PREFERENCES.md](USER_PREFERENCES.md) · [AGENTS.md](AGENTS.md) · [outputs/README.md](outputs/README.md)
  - 工程配置与脚本：`.gitignore` · `.gitattributes` · `.editorconfig` · [PDF 导出脚本](outputs/code/build_spec_pdf_v1.py) · [Excel 生成脚本](outputs/code/build_spec_excel_v1.py)
- **核验范围**：PDF 重开核对 24 页/38 书签/0 mathtext 警告并完成 6 页视觉抽检；全仓 Markdown 相对路径与锚点链接核验通过；本地就绪（本机当前环境未检测到全局 `git`/`gh` CLI，待同步至 `OpticsPan/OV4`）。

---

<a name="2026-11-23-spec-baseline-v1"></a>

## 2026-11-23　完成 NXT:1950i–1970Ci 档位 15 大类子系统验收规格推导与 Abbe 光学仿真

- **正式交付入口**：
  - [整机预算闭环（第 0 章）](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-0)
  - [WS / RS / 同步 MA / ENC 规格（第 1–4 章）](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-1)
  - [AA / TIS-PARIS / 温控 / 夹持 / 框架规格（第 5–12 章）](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-5)
  - [物镜与 WS iHOPC 20 参补偿残差（第 13–14 章）](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-13)
  - [Odd Fringe Zernike Z5–Z64 全 30 项控制误差（第 15 章）](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-15)
  - [2D Abbe 仿真脚本](outputs/code/sim_zernike_ovl_v1.py)
- **核心数值与核验**：调研 `OV4` 243 篇文献与 `ME3` TWINSCAN 手册；2D Abbe 仿真精确复现 `Z2 = -1/NA = -0.7407 nm/nm`；Microsoft Excel 实算 430 公式确认 DCO = `1.834 / 1.869 nm ≤ 2.00 nm`，MMO = `3.134 / 3.154 nm ≤ 3.50 nm`，FU = `10.34 nm ≤ 12.0 nm`。
