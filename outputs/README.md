# OV4 成果索引

[仓库首页](../README.md) · [参考文献总目](../REFERENCES.md) · [仓库规范](../REPOSITORY_MANAGEMENT.md) · [用户偏好](../USER_PREFERENCES.md) · [协作规则](../AGENTS.md) · [总变更记录](../CHANGELOG.md)

本页按成果类型与技术专题集中索引 `D:\work\OV4`（对应 GitHub `OpticsPan/OV4`）已归档的全部正式交付物。

**最新更新 · 2026-11-25**　新增仓库强制规定 **[UP-010] GitHub 网页版阅读与公式渲染适配规范**，新增自动化门禁脚本 [audit_github_md_v1.py](code/audit_github_md_v1.py)，并完成两份 `v2` 正式 Markdown 报告的 167 处 GitHub MathJax 全量适配及 PDF 双端同步重编译核验。[本次变更日志](../changes/2026-11-25-github-web-md-math-standard_v1.md) · [参考文献清单日志](../changes/2026-11-25-reference-catalog-inventory_v1.md)

## 按类型浏览（最新成果优先，完整保留历史基线）

| 类型 | 已归档正式成果 |
| :--- | :--- |
| **九大子系统推导与计算说明书（专题版）** | **【最新专题 v2】**[九大核心子系统说明书 v2 MD（8 篇一手文献全核验）](reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md) · [印刷排版版 v2 PDF（19 页 / 35 书签）](reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.pdf)<br>【历史专题 v1】[九大核心子系统说明书 v1 MD](reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v1.md) · [v1 PDF（19 页 / 34 书签）](reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v1.pdf) |
| **正式汇报演示文稿（PPTX 逐条证据链版）** | **【最新 v2】**[28 页逐条证据链与深度验收版 v2.pptx](presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v2.pptx)（新增 6 页专题 + 3 张 260 DPI 新图）<br>【历史 v1】[22 页基线证据链版 v1.pptx](presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v1.pptx) |
| **可计算 Excel 规格与预算表** | **【最新 v2】**[9 表 686 公式预算与验收细则表 v2.xlsx](tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v2.xlsx)（新增 Sheet 07–09，Excel 实算 0 错）<br>【历史 v1】[6 表 430 公式预算表 v1.xlsx](tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) |
| **正式综合报告（Markdown 网页版）** | **【最新 v2】**[15 大类子系统验收规格推导报告 v2](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md)（[目录](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#contents) · [预算闭环](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-0)）<br>【历史 v1】[验收规格推导报告 v1](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) |
| **正式综合报告（PDF 印刷排版版）** | **【最新 v2】**[验收规格推导报告 v2 PDF（30 页 / 45 书签）](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.pdf)<br>【历史 v1】[验收规格推导报告 v1 PDF（24 页 / 38 书签）](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf) |
| **可复现仿真与构建脚本** | **最新**：[GitHub MD 质检门禁](code/audit_github_md_v1.py) · [九大子系统 PDF v2](code/build_9subsys_doc_pdf_v2.py) · [Excel v2](code/build_spec_excel_v2.py) · [PDF v2](code/build_spec_pdf_v2.py) · [PPTX v2](code/build_spec_pptx_v2.py)<br>**v1**：[九大子系统 PDF v1](code/build_9subsys_doc_pdf_v1.py) · [Abbe Z5–Z64 仿真](code/sim_zernike_ovl_v1.py) · [Excel v1](code/build_spec_excel_v1.py) · [PDF v1](code/build_spec_pdf_v1.py) · [PPTX v1](code/build_spec_pptx_v1.py) |
| **图片与示意图** | `images/`（预留用于后续专项仿真曲线与物理原理图归档） |

## 按专题直达最新 v2 报告章节

- **顶层套刻与焦面闭环（DCO ≤ 2.00 nm / MMO ≤ 3.50 nm / FU ≤ 12.0 nm）**：[第 0 章 执行摘要与预算闭环](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-0)
- **运动台与底层光栅编码器（含 v2 独立验收反驳与单/往返细则）**：[1. WS 6-DOF](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-1) · [2. RS 6-DOF](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-2) · [3. WS-RS 同步 MA](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-3) · [4. ENC 编码器](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-4)
- **对准系统（AA / TIS / PARIS）**：[5. M-side AA (SMASH)](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-5) · [6. E-side TIS/PARIS](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-6)
- **热控、夹持与整机框架**：[7. WT 温控](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-7) · [8. Reticle 温控](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-8) · [9. RT 掩模夹持](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-9) · [10. WT 晶圆夹持](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-10) · [11. WH 温控](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-11) · [12. 整机 Frame](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-12)
- **iHOPC 补偿能力评价、狭缝逆卷积与 Odd Zernike**：[13. 物镜 iHOPC 与 8 维评价](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-13) · [14. WS iHOPC 验收与狭缝逆卷积](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-14) · [15. Odd Zernike (Z5–Z64)](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-15) · [16. FAT/SAT 建议与参考文献](reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md#sec-16)
