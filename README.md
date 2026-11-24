# OV4 — 先进光刻机套刻误差控制与子系统验收规格仓库

本仓库（本机目录 `D:\work\OV4`，对应 GitHub `OpticsPan/OV4`）用于归档 ArF 液浸光刻机套刻误差预算、子系统验收规格推导、光学/物理仿真脚本、可计算 Excel 模型、正式 PDF 报告、逐条证据链 PPTX 演示文稿及完整变更历史。

**快速导航**：[成果索引](outputs/README.md) · [最新演示文稿 PPTX](outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v1.pptx) · [最新正式报告 MD](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) · [最新正式报告 PDF](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf) · [最新 Excel 预算表](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) · [仓库管理规范](REPOSITORY_MANAGEMENT.md) · [用户偏好记录](USER_PREFERENCES.md) · [协作规则](AGENTS.md) · [总变更记录](CHANGELOG.md)

---

<a name="update-history"></a>

## 更新历史（最近更新在最前面）

> 每次仓库更新均在此表首行登记并附上可直达正式内容的相对路径链接（详见 [首页展示规范](REPOSITORY_MANAGEMENT.md#sec-homepage) 与 [UP-002](USER_PREFERENCES.md#up-002)）。

| 日期 | 变更内容 | 正式成果与日志链接 |
| :--- | :--- | :--- |
| 2026-11-24 | 将 15 大类子系统验收规格与误差预算表制作为 22 页 16:9 逐条证据链 PPTX（嵌入 25+ 张 OV4/ME3 原始论文截图、解析推导与 4 张 260 DPI 仿真/闭环图，全 22 页视觉检视通过），并同步归档 4 份可复现仿真与构建脚本。 | [正式演示文稿 PPTX](outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v1.pptx) · [Excel 预算表](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) · [PPTX 构建脚本](outputs/code/build_spec_pptx_v1.py) · [成果索引](outputs/README.md) · [变更日志](changes/2026-11-24-spec-budget-evidence-pptx_v1.md) |
| 2026-11-24 | 归档 NXT:1950i–1970Ci 验收规格推导报告和动态预算表 v1。成果署名为反重力 Agent，GPT（Codex）执行归档。 | [Markdown 报告](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) · [PDF 报告](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf) · [Excel 预算表](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) · [本次归档记录](changes/2026-11-24-archive-nxt1950i-1970i-antigravity_v1.md) |
| 2026-11-23 | 建立 OV4 仓库管理规范、用户偏好记录（`UP-001`–`UP-009`）与双层变更日志，规范归档 v1 正式 Markdown 报告与 Excel 动态预算表，并额外输出 24 页印刷级 PDF 报告（含封面目录、38 条书签、STIX 矢量公式与第 13–15 章横版宽表）。 | [正式报告 PDF](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf) · [正式报告 MD](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) · [Excel 预算表](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) · [仓库规范](REPOSITORY_MANAGEMENT.md) · [用户偏好](USER_PREFERENCES.md) · [变更日志](changes/2026-11-23-ov4-repo-setup-and-1950i-1970i-spec-baseline_v1.md) |
| 2026-11-23 | 基于 OV4 243 篇文献与 ME3 手册，完成对标 NXT:1950i–1970Ci 之间 ArF 液浸光刻机 15 大类子系统逐明细验收规格推导、2D Abbe `Z5–Z64` 奇像差仿真及整机 DCO（1.87 nm ≤ 2.00 nm）/ MMO（3.15 nm ≤ 3.50 nm）/ FU（10.34 nm ≤ 12.0 nm）动态公式闭环。 | [预算闭环总览](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-0) · [WS/RS/同步/ENC](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-1) · [iHOPC 物镜与 WS](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-13) · [Odd Zernike Z5–Z64](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-15) · [Abbe 仿真脚本](outputs/code/sim_zernike_ovl_v1.py) · [总变更记录](CHANGELOG.md#2026-11-23-spec-baseline-v1) |

---

## 当前主交付成果一览

| 交付形态 | 文件入口 | 说明 |
| :--- | :--- | :--- |
| **逐条证据链演示文稿（PPTX）** | [NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v1.pptx](outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v1.pptx) | 22 页 16:9 白底高清汇报版，覆盖 15 大类全明细指标，逐条附原始论文截图、计算过程与 4 张仿真图 |
| **综合推导报告（Markdown）** | [NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) | 覆盖 15 大类全部逐明细规格表、物理公式推导、文献出处与 FAT/SAT 建议（GitHub 网页直读） |
| **综合推导报告（PDF）** | [NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf](outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf) | 24 页印刷级排版，含执行 KPI 封面、页码目录、38 条侧边书签、STIX 矢量公式及横版宽表 |
| **动态公式 Excel 预算表** | [NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx](outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) | 6 个工作表、430 个跨页动态公式（已由 Excel 实算 0 错），修改任意子项自动重算整机闭环 |
| **可复现计算与构建代码** | [outputs/code/](outputs/code/) | [Abbe Zernike 仿真](outputs/code/sim_zernike_ovl_v1.py) · [Excel 生成与校验](outputs/code/build_spec_excel_v1.py) · [PDF 导出脚本](outputs/code/build_spec_pdf_v1.py) · [PPTX 构建脚本](outputs/code/build_spec_pptx_v1.py) |

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
