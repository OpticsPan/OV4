# OV4 — 先进光刻机套刻误差控制与子系统验收规格仓库

本仓库（本机目录 `D:\work\OV4`，对应 GitHub `OpticsPan/OV4`）用于归档 ArF 液浸光刻机套刻误差预算、子系统验收规格推导、光学/物理仿真脚本、可计算 Excel 模型、正式 PDF 报告、逐条证据链 PPTX 演示文稿及完整变更历史。

**快速导航**：[成果索引](outputs/README.md) · [最新演示文稿 PPTX v2](outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v2.pptx) · [最新正式报告 MD v2](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md) · [最新正式报告 PDF v2](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.pdf) · [最新 Excel 预算表 v2](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v2.xlsx) · [仓库管理规范](REPOSITORY_MANAGEMENT.md) · [用户偏好记录](USER_PREFERENCES.md) · [协作规则](AGENTS.md) · [总变更记录](CHANGELOG.md)

---

<a name="update-history"></a>

## 更新历史（最近更新在最前面）

> 每次仓库更新均在此表首行登记并附上可直达正式内容的相对路径链接（详见 [首页展示规范](REPOSITORY_MANAGEMENT.md#sec-homepage) 与 [UP-002](USER_PREFERENCES.md#up-002)）。

| 日期 | 变更内容 | 正式成果与日志链接 |
| :--- | :--- | :--- |
| 2026-11-24 | 发布 **v2 深度验收升级版**（完整保留 v1 全部文件）：新增 ① WS/RS 独立 6-DOF 验收必要性工程反驳论证与单程/往返重复性验收细则（含 150 m/s² 微滑移）；② WS 对 iHOPC（以 K4 为例）离线 ENC 遥测/在线曝光三级闭环审视与 8 mm 狭缝逆卷积专页图解；③ 投影物镜 K 参数补偿能力 8 维综合评价体系。同步升级 28 页 PPTX、9 表 686 公式 Excel（0 错）、30 页 PDF（45 书签）与 Markdown 报告。 | [演示文稿 PPTX v2](outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v2.pptx) · [Excel 预算表 v2](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v2.xlsx) · [正式报告 MD v2](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md) · [正式报告 PDF v2](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.pdf) · [v2 变更日志](changes/2026-11-24-spec-budget-v2-acceptance-deepdive_v2.md) |
| 2026-11-24 | 将 15 大类子系统验收规格与误差预算表制作为 22 页 16:9 逐条证据链 PPTX（嵌入 25+ 张 OV4/ME3 原始论文截图、解析推导与 4 张 260 DPI 仿真/闭环图，全 22 页视觉检视通过），并同步归档 4 份可复现仿真与构建脚本。 | [正式演示文稿 PPTX](outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v1.pptx) · [Excel 预算表](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) · [PPTX 构建脚本](outputs/code/build_spec_pptx_v1.py) · [成果索引](outputs/README.md) · [变更日志](changes/2026-11-24-spec-budget-evidence-pptx_v1.md) |
| 2026-11-24 | 归档 NXT:1950i–1970Ci 验收规格推导报告和动态预算表 v1。成果署名为反重力 Agent，GPT（Codex）执行归档。 | [Markdown 报告](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) · [PDF 报告](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf) · [Excel 预算表](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) · [本次归档记录](changes/2026-11-24-archive-nxt1950i-1970i-antigravity_v1.md) |
| 2026-11-23 | 建立 OV4 仓库管理规范、用户偏好记录（`UP-001`–`UP-009`）与双层变更日志，规范归档 v1 正式 Markdown 报告与 Excel 动态预算表，并额外输出 24 页印刷级 PDF 报告（含封面目录、38 条书签、STIX 矢量公式与第 13–15 章横版宽表）。 | [正式报告 PDF](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf) · [正式报告 MD](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) · [Excel 预算表](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) · [仓库规范](REPOSITORY_MANAGEMENT.md) · [用户偏好](USER_PREFERENCES.md) · [变更日志](changes/2026-11-23-ov4-repo-setup-and-1950i-1970i-spec-baseline_v1.md) |
| 2026-11-23 | 基于 OV4 243 篇文献与 ME3 手册，完成对标 NXT:1950i–1970Ci 之间 ArF 液浸光刻机 15 大类子系统逐明细验收规格推导、2D Abbe `Z5–Z64` 奇像差仿真及整机 DCO（1.87 nm ≤ 2.00 nm）/ MMO（3.15 nm ≤ 3.50 nm）/ FU（10.34 nm ≤ 12.0 nm）动态公式闭环。 | [预算闭环总览](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-0) · [WS/RS/同步/ENC](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-1) · [iHOPC 物镜与 WS](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-13) · [Odd Zernike Z5–Z64](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-15) · [Abbe 仿真脚本](outputs/code/sim_zernike_ovl_v1.py) · [总变更记录](CHANGELOG.md#2026-11-23-spec-baseline-v1) |

---

## 当前主交付成果一览（默认指向最新 `v2`，`v1` 历史基线完整保留于 [成果索引](outputs/README.md)）

| 交付形态 | 文件入口 | 说明 |
| :--- | :--- | :--- |
| **逐条证据链演示文稿（PPTX v2）** | [NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v2.pptx](outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v2.pptx) | 28 页 16:9 白底高清汇报版，保留 v1 全部 22 页证据链并新增 6 页深度验收专题（WS/RS 反驳与单往返细则、物镜 8 维评价、WS K4 审视、狭缝逆卷积三联图解） |
| **动态公式 Excel 预算表（XLSX v2）** | [NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v2.xlsx](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v2.xlsx) | 9 个工作表、686 个跨页动态公式（已由 Excel 实算 0 错），新增 Sheet 07–09（WS/RS 验收、WS iHOPC 与逆卷积计算器、物镜 8 维能力表） |
| **综合推导报告（Markdown v2）** | [NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md) | 覆盖 15 大类规格、全部四大深度专题公式推导与 FAT/SAT 细则（GitHub 网页直读） |
| **综合推导报告（PDF v2）** | [NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.pdf](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.pdf) | 30 页印刷级排版，含执行 KPI 封面、页码目录、45 条侧边书签、STIX 矢量公式及横版宽表 |
| **可复现计算与构建代码** | [outputs/code/](outputs/code/) | [Excel v2](outputs/code/build_spec_excel_v2.py) · [PDF v2](outputs/code/build_spec_pdf_v2.py) · [PPTX v2](outputs/code/build_spec_pptx_v2.py) · [Abbe 仿真](outputs/code/sim_zernike_ovl_v1.py)（含 v1 历史脚本） |

---

## 仓库目录结构与治理文档

| 目录 / 文件 | 用途说明 |
| :--- | :--- |
| [REPOSITORY_MANAGEMENT.md](REPOSITORY_MANAGEMENT.md) | 仓库管理规范（目录、版本、首页更新、公式排版、PDF/Excel 校验、只读保护） |
| [USER_PREFERENCES.md](USER_PREFERENCES.md) | 用户长期偏好记录（`UP-001`–`UP-009`） |
| [AGENTS.md](AGENTS.md) | AI 助手与协作者启动规范及交付同步清单 |
| [CHANGELOG.md](CHANGELOG.md) / [changes/](changes/) | 全局变更时间轴与逐次详细变更日志 |
| [outputs/](outputs/README.md) | 正式成果分类目录（`reports/`、`tables/`、`presentations/`、`images/`、`code/`） |
| `参考文献-整理版/`、`参考文献-整理版-Markdown/` | **本机只读原始参考文献库**（243 篇论文/专利 PDF 与 Markdown，由 `.gitignore` 忽略不推送至 GitHub） |
| `work/` | 本地临时计算与导出缓存（由 `.gitignore` 忽略） |
