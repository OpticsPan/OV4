# DCO 分配图与子系统验收预算 v1

[仓库首页](../README.md) · [成果索引](../outputs/README.md) · [总变更记录](../CHANGELOG.md#2026-11-25-dco-budget-tree)

2026-11-25，基于 Freriks 等（2006）Fig. 3 的预算分层方法、上传的 29 节点草图与 OV4 v2 技术报告，将同机同台 DCO 整理为双层验收量、均值／随机项、功能分组、D1–D11 及可测子系统规格。

- [draw.io 源图](../outputs/images/DCO_budget_v1.drawio)含五个可编辑页面，附[矢量图册](../outputs/images/DCO_budget_v1.pdf)和[高清总图](../outputs/images/DCO_budget_v1.png)。
- [公式工作簿](../outputs/tables/DCO_budget_v1.xlsx)按 5.5 mm 狭缝更新 D1-X 力臂，保留其余 v2 预算输入。X/Y 设计预算为 1.833222 / 1.868911 nm，Y 轴余量 0.131089 nm。原工作簿 8 mm 基线为 1.834459 / 1.868911 nm。
- [使用说明](../outputs/reports/DCO_budget_notes_v1.md)列有输入口径、两层倍率、19 个 iHOPC 系数、30 项奇像差上限、试验工况及原图各分支对照。源摘要的 X=1.832 nm 与逐行复算值一并记录。

验证采用 LibreOffice 对 204 个公式重算，逐项比对 11 行的输入与双层 X/Y。逐页检查了 draw.io XML 的节点、连接端点、PDF 页数及书签。可在仓库根目录运行 `python outputs/code/audit_github_md_v1.py` 检查正式 Markdown 链接与格式。
