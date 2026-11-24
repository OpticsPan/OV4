# OV4 成果索引

[仓库首页](../README.md) · [仓库规范](../REPOSITORY_MANAGEMENT.md) · [用户偏好](../USER_PREFERENCES.md) · [协作规则](../AGENTS.md) · [总变更记录](../CHANGELOG.md)

本页按成果类型与技术专题集中索引 `D:\work\OV4`（对应 GitHub `OpticsPan/OV4`）已归档的全部正式交付物。

**最新更新 · 2026-11-24**　新增 NXT:1950i–1970Ci 15 大类子系统验收规格与逐条证据链 22 页 PPTX 演示文稿，并同步归档 4 份可复现仿真与构建脚本。[本次详细变更日志](../changes/2026-11-24-spec-budget-evidence-pptx_v1.md) · [前次三原件归档记录](../changes/2026-11-24-archive-nxt1950i-1970i-antigravity_v1.md)

## 按类型浏览

| 类型 | 已归档正式成果 |
| :--- | :--- |
| **正式汇报演示文稿（PPTX 逐条证据链版）** | [NXT:1950i–1970Ci 15 大类子系统验收规格与逐条证据链 v1.pptx](presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v1.pptx)（22 页 16:9 白底版，逐条附 OV4/ME3 原始论文截图、公式推导与 4 张 260 DPI 仿真分析图） |
| **正式综合报告（Markdown 网页版）** | [NXT:1950i–1970Ci 档位 15 大类子系统验收规格推导报告 v1](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md)（[目录](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#contents) · [预算闭环](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-0)） |
| **正式综合报告（PDF 印刷排版版）** | [NXT:1950i–1970Ci 档位 15 大类子系统验收规格推导报告 v1 PDF](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf)（含封面、页码目录、PDF 书签、矢量公式与横版宽表） |
| **可计算 Excel 规格与预算表** | [NXT:1950i–1970Ci 15 大类子系统验收规格与误差预算表 v1.xlsx](tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx)（6 个工作表、430 个跨页动态公式、0 错误） |
| **可复现仿真与构建脚本** | [PPTX 逐条证据链构建](code/build_spec_pptx_v1.py) · [2D Abbe Z5–Z64 奇像差仿真](code/sim_zernike_ovl_v1.py) · [Excel 生成与闭环核验](code/build_spec_excel_v1.py) · [PDF 正式报告导出](code/build_spec_pdf_v1.py) |
| **图片与示意图** | `images/`（预留用于后续专项仿真曲线与物理原理图归档） |

## 按专题直达报告章节

- **顶层套刻与焦面闭环（DCO ≤ 2.00 nm / MMO ≤ 3.50 nm / FU ≤ 12.0 nm）**：[第 0 章 执行摘要与预算闭环](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-0)
- **运动台与底层光栅编码器（WS / RS / 同步 MA / ENC）**：[1. WS 6-DOF](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-1) · [2. RS 6-DOF](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-2) · [3. WS-RS 同步 MA](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-3) · [4. ENC 编码器](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-4)
- **对准系统（AA / TIS / PARIS）**：[5. M-side AA (SMASH)](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-5) · [6. E-side TIS/PARIS](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-6)
- **热控、夹持与整机框架**：[7. WT 温控](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-7) · [8. Reticle 温控](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-8) · [9. RT 掩模夹持](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-9) · [10. WT 晶圆夹持](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-10) · [11. WH 温控](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-11) · [12. 整机 Frame](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-12)
- **iHOPC 场内补偿残差与 Odd Zernike 波像差**：[13. 物镜 iHOPC](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-13) · [14. WS iHOPC](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-14) · [15. Odd Zernike (Z5–Z64)](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-15) · [16. FAT/SAT 建议与参考文献](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md#sec-16)
