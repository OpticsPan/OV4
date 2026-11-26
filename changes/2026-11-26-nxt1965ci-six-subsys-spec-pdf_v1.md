# 变更日志：发布 ASML NXT:1965Ci 六大核心子系统套刻预算分配与分层验收规格需求书（PDF v1）

- **日期**：2026-11-26
- **主笔**：Antigravity
- **相关规范**：`UP-002`、`UP-003`、`UP-004`、`UP-010`、`UP-011`（本次按用户显式要求先交付 PDF 格式）

## 变更摘要

依据用户专项要求，围绕 **WS（含 WS 自身、WRS 双台同步与 iHOPC 运动补偿）、RS、ENC、AA、TIS+PARIS、Lens** 六大核心子系统，编制并输出印刷级规格需求书 PDF（22 页 / 27 条嵌入式书签 / 6 张 300 DPI 高清工程图），同步归档单一事实源可复现构建脚本。

## 核心规格与排版要求核验

1. **严格排版与字体规范（PyMuPDF 逐字核验通过）**：
   - 正文与表格中文字体严格嵌入 **`SimSun`（宋体）`9.0 pt`（小五号）**，英文/数字/物理单位严格嵌入 **`Times New Roman` `9.0 pt`**；
   - 视觉样式对齐 OV4 技术评审报告风格：深青蓝渐变封面横幅、2×2 元数据卡片、左侧蓝条结论速览、首页完整自动分页目录（2-pass 精确页码无偏移）、跨页自动重复深蓝表头、页眉与 `第 X 页 / 共 22 页` 页脚。
2. **严格一章一子系统、先表后释、四列标准表、零合并单列（共 213 项独立指标）**：
   - 全部 12 张子系统验收表均为严格四列：**`序号` | `指标项` | `验收规格（附单位）` | `标准测试定义与工装条件`**，复杂项标注 `[注 X-Y]` 并在各章末尾详释；
   - 全部 213 项指标严格逐轴（X/Y/Z/Rx/Ry/Rz）、逐模式（静止/单程/残余反向差/往返/Sync MA/Sync MSD）、逐色（532/635/780/850 nm）、逐阶（Odd Zernike Z7–Z63 全 30 项）、逐项（iHOPC 调节范围与调节精度分开）单列，**零合并行**。
3. **核心工程裁决与分层体系**：
   - **iHOPC 11 项场内运动补偿明确划归 `WRS`（第 1 章 T2）**：基于扫描放大率 `K4`、斜切/偏航 `K5/K6/K10/K16` 与高阶弯曲 `K8/K11/K14/K19` 在像面生效的本质物理量为 WS 与 RS/4 的相对轨迹，且高频项需双台按带宽协同执行并内嵌 `5.5 mm` 狭缝逆卷积预补偿；
   - **分级体系**：`WS/WRS`（T1 WS 自身 + T2 WRS 同步与 iHOPC）、`RS`（T1 单台独立 6-DOF 与 1000 趟微滑移，`4×` 原值）、`ENC`（T1 纯传感器离线 + T2 装机切头/热稳/外部标尺）、`AA`（T1 参考扫单标与四色可用率/色差 + T2 类 FIWA/HOWA 全片网格）、`TIS+PARIS`（按在机曝光光学基准本质单设 T1 闭环）、`Lens`（T1 出厂干涉仪 193 nm Odd Zernike 30 项 Fringe 系数 `nm` + Lens-iHOPC 8 项范围/精度与 `K20` 边界 + T2 装机 PARIS 8 维耦合与跨照明套刻验证）。

## 新增与更新文件清单

- 新增：[outputs/reports/NXT1965Ci套刻预算分配_六大核心子系统分层验收规格需求书_v1.pdf](../outputs/reports/NXT1965Ci套刻预算分配_六大核心子系统分层验收规格需求书_v1.pdf)（22 页 / 27 书签）
- 新增：[outputs/code/build_nxt1965ci_subsys_spec_pdf_v1.py](../outputs/code/build_nxt1965ci_subsys_spec_pdf_v1.py)
- 新增：[changes/2026-11-26-nxt1965ci-six-subsys-spec-pdf_v1.md](2026-11-26-nxt1965ci-six-subsys-spec-pdf_v1.md)
- 更新：[README.md](../README.md)、[outputs/README.md](../outputs/README.md)、[CHANGELOG.md](../CHANGELOG.md)

## 核验结果

- PyMuPDF 字体审计：正文与表格 9 pt 字体均为 `SimSun`（10,963 字）与 `Times New Roman`（18,745 字符），封面首页 27 项目录零溢出，全部 6 张 300 DPI 配图与跨页表格经逐页 PNG 视觉复核零遮挡、零断行。
- `python outputs/code/audit_github_md_v1.py`：全仓链接与 GitHub Markdown 格式核验 `Errors: 0`。
