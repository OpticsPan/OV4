# OV4 成果索引

[仓库首页](../README.md) · [仓库规范](../REPOSITORY_MANAGEMENT.md) · [用户偏好](../USER_PREFERENCES.md) · [协作规则](../AGENTS.md) · [总变更记录](../CHANGELOG.md)

本页按成果类型与技术专题集中索引 `D:\work\OV4`（对应 GitHub `OpticsPan/OV4`）已归档的全部正式交付物。

**最新更新 · 2026-11-24（v2）**　发布 NXT:1950i–1970Ci 验收规格与误差预算 **v2 深度验收升级版**（完整保留 v1），新增 WS/RS 独立验收反驳与单/往返细则、WS iHOPC（K4）离线/在线验收与 8 mm 狭缝逆卷积三联图解、投影物镜 K 参数 8 维综合评价体系。[v2 详细变更日志](../changes/2026-11-24-spec-budget-v2-acceptance-deepdive_v2.md) · [v1 PPTX 变更日志](../changes/2026-11-24-spec-budget-evidence-pptx_v1.md)

## 按类型浏览（最新 `v2` 优先，保留 `v1` 历史基线）

| 类型 | 已归档正式成果 |
| :--- | :--- |
| **正式汇报演示文稿（PPTX 逐条证据链版）** | **【最新 v2】**[28 页逐条证据链与深度验收版 v2.pptx](presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v2.pptx)（新增 6 页专题 + 3 张 260 DPI 新图）<br>【历史 v1】[22 页基线证据链版 v1.pptx](presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v1.pptx) |
| **可计算 Excel 规格与预算表** | **【最新 v2】**[9 表 686 公式预算与验收细则表 v2.xlsx](tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v2.xlsx)（新增 Sheet 07–09，Excel 实算 0 错）<br>【历史 v1】[6 表 430 公式预算表 v1.xlsx](tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) |
| **正式综合报告（Markdown 网页版）** | **【最新 v2】**[15 大类子系统验收规格推导报告 v2](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md)（[目录](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#contents) · [预算闭环](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-0)）<br>【历史 v1】[验收规格推导报告 v1](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) |
| **正式综合报告（PDF 印刷排版版）** | **【最新 v2】**[验收规格推导报告 v2 PDF（30 页 / 45 书签）](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.pdf)<br>【历史 v1】[验收规格推导报告 v1 PDF（24 页 / 38 书签）](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf) |
| **可复现仿真与构建脚本** | **v2**：[Excel v2](code/build_spec_excel_v2.py) · [PDF v2](code/build_spec_pdf_v2.py) · [PPTX v2](code/build_spec_pptx_v2.py)<br>**v1**：[Abbe Z5–Z64 仿真](code/sim_zernike_ovl_v1.py) · [Excel v1](code/build_spec_excel_v1.py) · [PDF v1](code/build_spec_pdf_v1.py) · [PPTX v1](code/build_spec_pptx_v1.py) |
| **图片与示意图** | `images/`（预留用于后续专项仿真曲线与物理原理图归档） |

## 按专题直达最新 v2 报告章节

- **顶层套刻与焦面闭环（DCO ≤ 2.00 nm / MMO ≤ 3.50 nm / FU ≤ 12.0 nm）**：[第 0 章 执行摘要与预算闭环](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-0)
- **运动台与底层光栅编码器（含 v2 独立验收反驳与单/往返细则）**：[1. WS 6-DOF](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-1) · [2. RS 6-DOF](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-2) · [3. WS-RS 同步 MA](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-3) · [4. ENC 编码器](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-4)
- **对准系统（AA / TIS / PARIS）**：[5. M-side AA (SMASH)](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-5) · [6. E-side TIS/PARIS](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-6)
- **热控、夹持与整机框架**：[7. WT 温控](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-7) · [8. Reticle 温控](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-8) · [9. RT 掩模夹持](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-9) · [10. WT 晶圆夹持](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-10) · [11. WH 温控](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-11) · [12. 整机 Frame](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-12)
- **iHOPC 补偿能力评价、狭缝逆卷积与 Odd Zernike**：[13. 物镜 iHOPC 与 8 维评价](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-13) · [14. WS iHOPC 验收与狭缝逆卷积](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-14) · [15. Odd Zernike (Z5–Z64)](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-15) · [16. FAT/SAT 建议与参考文献](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-16)
