# 变更日志：发布 ASML NXT:1965Ci 六大核心子系统套刻预算规格需求书 Word 套册（1 份整机总册 + 6 份独立下发子系统分册，v1）

- **日期**：2026-11-27
- **交付目录**：`outputs/reports/NXT1965Ci六大子系统套刻规格需求书_Word_v1/`
- **可复现单一事实源构建脚本**：[build_nxt1965ci_subsys_spec_docx_v1.py](../outputs/code/build_nxt1965ci_subsys_spec_docx_v1.py)
- **7 份正式 Word（`.docx`）交付清单**（与 `v3.pdf` 100% 数值与证据同源，历史 PDF `v1/v2/v3` 按 `UP-008` 完整保留）：
  1. **整机自查总册（23 页，动态 Word 目录与页码）**：[00_整机总册_NXT1965Ci六大核心子系统套刻预算规格需求书_v1.docx](../outputs/reports/NXT1965Ci六大子系统套刻规格需求书_Word_v1/00_整机总册_NXT1965Ci六大核心子系统套刻预算规格需求书_v1.docx)
  2. **WS 晶圆台独立分册（6 页）**：[01_WS晶圆台_套刻预算规格需求书_v1.docx](../outputs/reports/NXT1965Ci六大子系统套刻规格需求书_Word_v1/01_WS晶圆台_套刻预算规格需求书_v1.docx)
  3. **RS 掩模台独立分册（4 页）**：[02_RS掩模台_套刻预算规格需求书_v1.docx](../outputs/reports/NXT1965Ci六大子系统套刻规格需求书_Word_v1/02_RS掩模台_套刻预算规格需求书_v1.docx)
  4. **ENC 光栅编码器独立分册（3 页）**：[03_ENC光栅编码器_套刻预算规格需求书_v1.docx](../outputs/reports/NXT1965Ci六大子系统套刻规格需求书_Word_v1/03_ENC光栅编码器_套刻预算规格需求书_v1.docx)
  5. **AA 晶圆对准独立分册（3 页）**：[04_AA晶圆对准_套刻预算规格需求书_v1.docx](../outputs/reports/NXT1965Ci六大子系统套刻规格需求书_Word_v1/04_AA晶圆对准_套刻预算规格需求书_v1.docx)
  6. **TIS + PARIS 空间像传感独立分册（3 页）**：[05_TIS与PARIS空间像传感_套刻预算规格需求书_v1.docx](../outputs/reports/NXT1965Ci六大子系统套刻规格需求书_Word_v1/05_TIS与PARIS空间像传感_套刻预算规格需求书_v1.docx)
  7. **Lens 投影物镜独立分册（7 页）**：[06_Lens投影物镜_套刻预算规格需求书_v1.docx](../outputs/reports/NXT1965Ci六大子系统套刻规格需求书_Word_v1/06_Lens投影物镜_套刻预算规格需求书_v1.docx)

---

## 核心新增与拆解要点

1. **文首增设《总则：多阶段验收理念与模块-整机耦合边界》（总册第 0 章 & 全部 6 份独立分册第 1 节）**：
   - 系统阐述整机设置 `T1 / T2 / T3` 多阶段验收的根本目的：促使各子系统建立**模块间耦合（Inter-Module Coupling）**与**子系统–整机环境耦合（Subsystem–Machine Environment Coupling）**双重视角；
   - 明确**子系统服务于整机曝光，离线验证合格的指标放到整机多物理场与跨模块联动环境下未必满足曝光需求**，故 T1 仅作装机准入前提，T2/T3 通过方构成最终达标依据；
   - 总册配套《`T1/T2/T3` 验收职责与耦合边界总表》及《六大子系统预算分工与分册分发清单》；6 份独立分册各自定制针对该子系统的 3 条专属《关键模块耦合与整机环境耦合边界清单》（`CP-01`–`CP-03`）。
2. **6 份独立下发分册 100% 自包含（零悬空跨章引用）**：
   - 全部 6 份分册自动采集本分册引用的参考文献并按 `[1]..[k]` 连续重排编号，内置对应的全部一手论文原图；
   - `02_RS掩模台` 独立分册完整内嵌 `4×` 掩模侧 `L_AB,RS = 154.0 mm` A–B 距离及单程 / 残余反向差 / 往返完整三步公式，不依赖 WS 分册即可独立执行验收。
3. **原生 Word 排版质量与自动化核验**：
   - 全部 7 份 `.docx` 严格锁定正文字体 `SimSun 9.0 pt`（宋体小五）+ `Times New Roman 9.0 pt`、表头跨页重复（`w:tblHeader`）、行内禁断页（`w:cantSplit`）、真上下标公式与高清原图；
   - 经本机 Microsoft Word 16.0 COM 自动化刷新动态目录（`TOC`）与页码域（`PAGE/NUMPAGES`）并导出核验 PDF/PNG，PyMuPDF 硬检 7 份文档全部满足 `SimSun 9pt` + `Times New Roman 9pt` 且零残留大括号/反引号；全 7 份渲染页视觉复核通过（6 份分册第 1 页完整落稳封面 + 总则 + `CP-01..03` 三条耦合表，无稀疏碎片页）。
   - `python outputs/code/audit_github_md_v1.py` 核验全仓 `Errors: 0`。
