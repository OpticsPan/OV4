# 变更日志：发布《ASML NXT:1965Ci 套刻预算规格需求书（十二大子系统完整版）》PDF/Word 套册与配套《指标规格分配计算报告》及归档计算代码（v1）

- **日期**：2026-11-27
- **版本**：完整版 SRS v1（PDF + 13 份 Word）+ 内部计算报告 v1（PDF）+ 计算与构建代码归档
- **对应需求**：
  1. 在六大核心子系统规格书基础上，补齐此前未纳入的其余 6 大子系统（IH、WT-TC/WH、WC、RC/RH、IL/LS、MF/ENV），形成覆盖整机全部 **12 大子系统** 的完整版《ASML NXT:1965Ci 套刻预算规格需求书》，严格区分 **T1（单件/单台离线）/ T2（装机解算/同步/调控）/ T3（跨台整机联调）** 验收边界，同步输出 **完整版 PDF**、**完整版 Word 总册** 及 **12 份独立下发子系统 Word 分册**。
  2. 独立复核全部数据来源可靠性、Ref009 Fig. 3 方差份额与防重复计数逻辑，回收 12 大子系统全部规格后自下而上正算预估整机套刻（DCO / SMO / MMO），严格剥离出规格需求书正文，单独形成《ASML NXT:1965Ci 指标规格分配计算报告》（PDF）并将可复现 Python 计算引擎完整归档入库。

---

## 1. 新增正式交付物清单

### 1.1 《ASML NXT:1965Ci 套刻预算规格需求书（完整版 v1）》（严格纯 SRS 口径，共 14 份文件）

- **完整版整机 PDF（31 页 / 53 书签 / 232 项独立套刻指标 / 17 张一手论文原图 / 33 条参考文献，宋体小五 `9 pt` + `Times New Roman 9 pt`）**：
  - [ASML_NXT1965Ci套刻预算规格需求书_完整版_v1.pdf](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_v1.pdf)
- **完整版 Word 套册（1 份整机总册 + 12 份自包含独立下发分册，均经 Microsoft Word COM 刷新动态目录/页码与零泄露断言核验）**：
  - [00 整机总册（34 页）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/00_整机总册_ASML_NXT1965Ci套刻预算规格需求书_v1.docx)
  - [01 WS 晶圆台（含 WRS 与运动 iHOPC，37 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/01_WS晶圆台_套刻预算规格需求书_v1.docx)
  - [02 RS 掩模台（4× 掩模侧，22 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/02_RS掩模台_套刻预算规格需求书_v1.docx)
  - [03 ENC 光栅编码器（5 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/03_ENC光栅编码器_套刻预算规格需求书_v1.docx)
  - [04 AA 晶圆对准（M-side，9 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/04_AA晶圆对准_套刻预算规格需求书_v1.docx)
  - [05 TIS + PARIS 空间像传感（E-side 湿区，7 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/05_TIS与PARIS空间像传感_套刻预算规格需求书_v1.docx)
  - [06 Lens 投影物镜（NA = 1.35，71 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/06_Lens投影物镜_套刻预算规格需求书_v1.docx)
  - [07 IH 浸没头与超纯水液控（新增，11 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/07_IH浸没液控系统_套刻预算规格需求书_v1.docx)
  - [08 WT-TC & WH 晶圆温控与传片预处理（新增，12 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/08_WT-TC与WH晶圆温控传片_套刻预算规格需求书_v1.docx)
  - [09 WC 晶圆夹持与 WT–MB 接口（新增，13 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/09_WC晶圆夹持系统_套刻预算规格需求书_v1.docx)
  - [10 RC & RH 掩模夹持、薄膜与掩模热控（新增，16 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/10_RC与RH掩模夹持及热控_套刻预算规格需求书_v1.docx)
  - [11 IL & LS 193 nm 光源与 FlexRay 照明（新增，12 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/11_IL与LS光源及FlexRay照明_套刻预算规格需求书_v1.docx)
  - [12 MF & ENV 计量框架、隔振与微环境（新增，17 项）](../outputs/reports/ASML_NXT1965Ci套刻预算规格需求书_完整版_Word套册_v1/12_MF与ENV计量框架及微环境_套刻预算规格需求书_v1.docx)

### 1.2 《ASML NXT:1965Ci 指标规格分配计算报告》（内部计算与审计档案）

- **计算报告 PDF（10 页 / 19 书签 / 5 张高清图表，宋体小五 `9 pt` + `Times New Roman 9 pt`）**：
  - [ASML_NXT1965Ci指标规格分配计算报告_v1.pdf](../outputs/reports/ASML_NXT1965Ci指标规格分配计算报告_v1.pdf)

### 1.3 仓库归档计算与构建代码（4 份 Python 脚本）

- [calc_nxt1965ci_overlay_budget_audit_v1.py](../outputs/code/calc_nxt1965ci_overlay_budget_audit_v1.py) — 主计算与审计引擎（12 子系统换算、Ref009 Fig. 3 方差核校、DCO/SMO/MMO 正算回收、共享源相关性 `ρ` 扫描、20 万次确定性蒙特卡洛与 `±10%` 龙卷风敏感度排序）
- [srs_full_data_nxt1965ci_v1.py](../outputs/code/srs_full_data_nxt1965ci_v1.py) — 12 子系统纯 SRS 单一权威数据源
- [build_nxt1965ci_full_srs_v1.py](../outputs/code/build_nxt1965ci_full_srs_v1.py) — 完整版 SRS PDF + 13 份 Word 套册生成器与自动质检脚本
- [build_nxt1965ci_calc_report_pdf_v1.py](../outputs/code/build_nxt1965ci_calc_report_pdf_v1.py) — 指标规格分配计算报告 PDF 自动排版生成器

---

## 2. 核心技术审计与回收验证摘要

1. **规格需求书与内部计算报告严格解耦**：通过自动化门禁校验全部 14 份 SRS 文档，确认正文零预算方差份额推导、零整机回收预估泄漏，严格保持工程契约文档纯净性；全部 232 项指标严格逐项单列（无 X/Y 合并行），纯套刻专项口径（不含焦面 `Z/Rx/Ry` 及 `Sync MSD`）。
2. **数据来源可靠性分级与 Ref009 Fig. 3 方差核校**：透明区分 A 类（一手论文/专利实测）、B 类（第一性原理/2D Abbe 解析换算）与 C 类（工程预算分配）；回收全部 12 大子系统后，核心六域方差份额与 `Ref009 Fig. 3` 偏差全部在 `-0.21%` 至 `+0.30%` 之内。
3. **六大共享枢纽防重复计数**：明确 `03 ENC`（内嵌 WRS 闭环，1:3 精度比 `2.93×`）、`11 IL/LS`（`0.094 nm 1L`）+ `12 MF/ENV` 像面微振（`0.129 nm 1L`）精确闭合于 `f6_dyn`（`0.1596 ≤ 0.160 nm 1L`）等唯一入账归口。
4. **整机套刻自下而上回收结果（100% 踩线确定性最严包络）**：
   - **单卡盘 DCO**：`X 2.205 / Y 2.222 / 包络 2.257 nm ≤ 2.50 nm`（余量 `9.74%`）
   - **双卡盘 SMO**：`X 2.315 / Y 2.331 / 包络 2.364 nm ≤ 2.50 nm`（余量 `5.42%`）
   - **跨机匹配 MMO**：`X 4.265 / Y 4.273 / 包络 4.291 nm ≤ 4.50 nm`（余量 `4.65%`）
5. **耦合相关性与 20 万次蒙特卡洛审计**：
   - 共享源跨子系统相关性达到 `ρ = 2.5%` 时，SMO 增至 `2.505 nm`（撞线 `2.50 nm`），从定量上证实了多阶段 `T2/T3` 耦合验收的必要性；
   - 20 万次蒙特卡洛（`seed = 19652026`）：常规交付（72%–100% Spec）下 `SMO P50 = 2.021 nm / P99.7 = 2.218 nm`；逼近上限（85%–100% Spec）下 `SMO P50 = 2.143 nm / P99.7 = 2.276 nm`，DCO / SMO / MMO 一次合格率均为 `100.0%`；
   - `±10%` 龙卷风敏感度前三位：`S2 对准域 (+48.5 pm)`、`S1 运动台域 (+38.8 pm)`、`系统残余均值偏置 |Mean| (+35.0 pm)`。

---

## 3. 历史版本保留与仓库规范核验

- 此前发布的六大核心子系统规格书 PDF (`v1/v2/v3`) 与 6 子系统 Word 套册 (`v1`) 均按 [UP-008](../USER_PREFERENCES.md#up-008) 完整保留存档，未做覆盖。
- 全部渲染 PDF 与 Word 导出预览页经人工视觉复核（修复封面及第 0 章表宽折行、单行分册标题字号与计算报告上标格式），并经 `audit_github_md_v1.py` 门禁复核通过（`Errors: 0`）。
