# OV4 总变更记录（CHANGELOG）

[仓库首页](README.md) · [成果索引](outputs/README.md) · [仓库规范](REPOSITORY_MANAGEMENT.md) · [用户偏好](USER_PREFERENCES.md) · [协作规则](AGENTS.md)

本文件按时间倒序（最近更新排在最前面）记录 `OV4` 仓库的所有正式变更、交付物清单与核验范围。每次更新均与 [README.md 首页更新历史](README.md#update-history) 同步。

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
