# 2026-11-23　建立 OV4 仓库管理体系并归档 1950i–1970Ci 档位验收规格 v1（MD + PDF + Excel）

[仓库首页](../README.md) · [总变更记录](../CHANGELOG.md#2026-11-23-repo-governance-and-pdf-v1) · [成果索引](../outputs/README.md) · [正式报告 MD](../outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md) · [正式报告 PDF](../outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf) · [Excel 预算表](../outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx)

## 一、本次变更摘要

1. **建立 OV4 标准仓库治理体系**：
   - 新增 [REPOSITORY_MANAGEMENT.md](../REPOSITORY_MANAGEMENT.md)（仓库目录分工、首页更新置顶规则、版本命名、GitHub 数学/导航规范、只读文献保护红线与提交前检查清单）；
   - 新增 [USER_PREFERENCES.md](../USER_PREFERENCES.md)（以 `UP-001` 至 `UP-009` 完整登记用户路径偏好、首页更新置顶偏好、逐明细拆行、推导透明化及 MD+PDF+Excel 多形态交付要求）；
   - 新增 [AGENTS.md](../AGENTS.md)（AI 助手与维护者启动检查流）、[CHANGELOG.md](../CHANGELOG.md)（倒序全局变更记录）、[outputs/README.md](../outputs/README.md)（成果总索引）及 `.gitignore`、`.gitattributes`、`.editorconfig`（忽略只读大文献库与 `work/` 临时区）。
2. **规范归档 1950i–1970Ci 档位 15 大类子系统验收规格 v1 成果**：
   - 将正式 Markdown 报告升级为 GitHub 网页阅读友好版，补齐顶部快捷导航、全 17 章稳定英文锚点目录、相对路径链接及 CommonMark 粗体排版修复，归档至 [NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md](../outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md)；
   - 将含 6 个工作表、430 个跨页动态公式的 Excel 规格与预算表归档至 [NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx](../outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx)；
   - 归档三份可复现脚本：sim_zernike_ovl_v1.py（本地 `outputs/code/sim_zernike_ovl_v1.py`）、build_spec_excel_v1.py（本地 `outputs/code/build_spec_excel_v1.py`）、build_spec_pdf_v1.py（本地 `outputs/code/build_spec_pdf_v1.py`）；
   - 清理根目录未版本化旧临时副本，保持只读原始参考文献库与 `开始阅读.html` 原封不动。
3. **新增印刷级 PDF 正式报告**：
   - 通过 Chrome 无头渲染 + Matplotlib STIX 透明矢量公式 + PyMuPDF 双遍页码与书签写入，生成 24 页正式 PDF 报告 [NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf](../outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.pdf)；
   - 涵盖执行 KPI 封面与实时页码目录（第 1 页）、38 条层级书签、正文竖版 A4（第 0–12、16 章）以及第 13–15 章（iHOPC 20 参、Odd Zernike Z5–Z64 全 30 项 17 列宽表）横向 A4 宽页。

## 二、核心技术结论与核验结果

- **整机预算闭环（Excel 引擎 430 公式全量重算 0 错误，MD / PDF / Excel 100% 一致）**：
  - 同机套刻 DCO（`|Mean|+3σ`）：X = **1.834 nm** / Y = **1.869 nm** ≤ 2.00 nm（裕度 6.6%）；
  - 混机套刻 MMO（99.7%）：X = **3.134 nm** / Y = **3.154 nm** ≤ 3.50 nm（裕度 9.9%）；
  - 全片焦面均匀性 FU（`3σ`）：**10.34 nm** ≤ 12.0 nm（裕度 13.8%）；
  - Odd Zernike（Z5–Z64 全 30 项）：总奇波前 **0.337 nm RMS**，跨照明切换套刻 **≤ 0.370 nm**（包络）/ **0.328 nm**（Abbe 实算）。
- **PDF 质量与视觉核验**：
  - 24 页、38 条有效书签全部在 `[1, 24]` 范围内，0 条 mathtext 回退警告，0 处未解析 `**`；
  - 视觉抽检封面（p.1）、DCO 闭环表（p.3）、同步运动公式页（p.6）、iHOPC 横版公式页（p.16）及 17 列 Odd Zernike 横版总表（p.21），确认中文、矢量公式、透明底框与宽表零裁切。
- **远端 GitHub 同步状态**：本机当前 shell 环境未安装全局 `git` / `gh` CLI，本次已完成本地 `D:\work\OV4` 全部 Git 标准文件建设与校验，待本地安装 Git 或在具备 Git 权限的终端执行初始化与推送至 `OpticsPan/OV4`。
