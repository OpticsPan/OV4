# 2026-11-25 变更日志：归档冻结纠偏前 v1（UP-012），从九大子系统说明书 v2 + Overlay3 报告 143 + 一手文献独立重建 NXT:1965Ci L0–L3 报告、Ref-146 风格 draw.io 与 18 页全新 PPTX

[仓库首页](../README.md) · [总变更记录](../CHANGELOG.md) · [成果索引](../outputs/README.md) · [NXT:1965Ci 主报告 v1](../outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v1.md) · [Ref-146 风格 draw.io](../outputs/images/NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.drawio) · [NXT:1965Ci PPTX v1](../outputs/presentations/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与子系统验收规格_v1.pptx)

## 1. 变更目的与纠偏说明

响应用户对上轮参考源指令的正式更正（仅可参考 `@github/Overlay3` 报告 `reports/md/143_scanner_overlay_control_survey.md` 及原始一手文献，严禁参考 `@github/Overlay3` 其余报告文档），执行以下三项仓库治理与重建交付：
1. **历史留档与防误引冻结（新增 `UP-012`）**：完整保留纠偏前产出的 `NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md` 及其配套 `v1` `.drawio`/`.png`/脚本，但在文件顶部、`USER_PREFERENCES.md`（`UP-012`）、`AGENTS.md`、`README.md` 与 `outputs/README.md` 全部明确标示**【已归档冻结·不再作为后续参考】**；同时将本机 `work/Overlay3_ref` 稀疏检出严格收敛至仅含 `reports/md/143_scanner_overlay_control_survey.md` 与原始 `literature/`；
2. **独立重建 `NXT:1965Ci`（`SMO ≤ 2.50 / MMO ≤ 4.50 nm`）主报告与 `Ref-146 Fig. 3` 风格 `L0–L3` 拆解图**：直接从 [九大核心子系统验收指标推导与计算说明书 v2](../outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md) 起步，结合 `Overlay3` 报告 `143`、`Ref146 Fig. 3` 原图与正文、`Ref009 Fig. 3` 像素标定（`77.80 px/nm`）、`Ref066/165/167/168`、`[N1–N8]`、`[S1–S14]` 及 `ME3` 手册独立重建完整双轴闭环与全部九大核心子系统（+6 辅助域）规格；
3. **全新构建 18 页面向 `NXT:1965Ci` 的汇报 PPTX**：全片统一至 `SMO ≤ 2.50 / MMO ≤ 4.50 / FU ≤ 14.0 nm`、`26 × 5.5 mm` 真实狭缝、`WS = Master` 同步核定及 `Ref-146` `L0–L3` 全景图，全部 18 页经 PowerPoint COM 导出 PNG 逐页视觉复核通过。

## 2. 本次新增与更新文件清单

| 文件路径 | 变更类型 | 说明 |
| :--- | :---: | :--- |
| [outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v1.md](../outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_整机L0-L3拆解与九大子系统验收规格报告_v1.md) | 新增 | `NXT:1965Ci` 正式主报告（全 6 章，符合 `UP-010/011`）：内嵌 `Ref-146 Fig. 3` 风格全景图、`Ref009 Fig. 3` 像素闭环（全项 ≤ ±0.30%）、用户四层误差传递思路评价与 4 项补强、九大核心子系统由 `v2` 向 `1965Ci` 逐项演进、6 辅助域与 `143 §7.2` 四层验收金字塔 |
| [outputs/images/NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.drawio](../outputs/images/NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.drawio) | 新增 | 严格承袭 `Ref-146 Fig. 3` 原版左→右架构与共享物理源虚线语法的可编辑 draw.io 源图 |
| [outputs/images/NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.png](../outputs/images/NXT1965Ci_SMO2.5_MMO4.5_Ref146风格L0-L3套刻指标拆解图_v1.png) | 新增 | 180 DPI 高清矢量 PNG（0 缺字告警，视觉复核零重叠零裁切，嵌入主报告第 1 章与 PPTX Slide 04） |
| [outputs/code/build_nxt1965ci_budget_and_diagram_v1.py](../outputs/code/build_nxt1965ci_budget_and_diagram_v1.py) | 新增 | 单一事实源校验脚本：内置双轴闭环断言，同步输出 `.drawio`、`.png` 及 5 张 260 DPI PPT 配套工程图 |
| [outputs/presentations/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与子系统验收规格_v1.pptx](../outputs/presentations/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与子系统验收规格_v1.pptx) | 新增 | 18 页 16:9 白底高清 `NXT:1965Ci` 汇报演示文稿（嵌入 20+ 张一手论文原图与 6 张新制高清图，全 18 页视觉复核通过） |
| [outputs/code/build_nxt1965ci_pptx_v1.py](../outputs/code/build_nxt1965ci_pptx_v1.py) | 新增 | `NXT:1965Ci` 18 页 PPTX 可复现构建脚本 |
| [outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md](../outputs/reports/NXT1965Ci套刻目标_SMO2.5_MMO4.5_L0-L3指标拆解与误差传递报告_v1.md) | 冻结标记 | 保留全部正文，顶部加注【已归档冻结·不再作为后续参考】提示并指引至新主报告 |
| [USER_PREFERENCES.md](../USER_PREFERENCES.md#up-012)、[AGENTS.md](../AGENTS.md) | 更新 | 新增 `UP-012` 冻结归档规则，防止后续工作流误引纠偏前 `v1` 产物 |
| [README.md](../README.md#update-history)、[outputs/README.md](../outputs/README.md)、[CHANGELOG.md](../CHANGELOG.md#2026-11-25-nxt1965ci-clean-ref143)、[REFERENCES.md](../REFERENCES.md)、[WS-RS同步调研报告 v2](../outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v2.md) | 更新 | 首页「更新历史」首行置顶本次正式成果，隔离冻结旧 `v1` 入口并将全部活动报告/总目导航切换至洁净版新主报告 |

## 3. 核心闭环与质量门禁核验

- **双轴数学闭环**：`Ref009 Fig. 3` 六域占比偏差全项 `≤ ±0.30%`（`Core-6 RSS = 1.926 nm`）；同卡盘 **`DCO = 2.257 nm ≤ 2.50 nm`**（裕度 `9.7%`）；双卡盘 **`SMO = 2.364 nm ≤ 2.50 nm`**（X `2.315` / Y `2.331`，裕度 `5.4%`）；混机 **`MMO = 4.291 nm ≤ 4.50 nm`**（X `4.265` / Y `4.273`，裕度 `4.6%`）；焦面 **`FU = 11.48 nm ≤ 14.0 nm`**（裕度 `18.0%`）。
- **Markdown 质量门禁**：已通过 `python outputs/code/audit_github_md_v1.py` 链接与 GitHub MathJax 双项 **`Errors: 0`** 校验。
- **PPTX 视觉复核**：全部 18 页由 Microsoft PowerPoint COM 渲染为 1600×900 PNG 并逐页人工视觉复查，重点替换了原 Slide 14 旧 `11.4 ms` 图为全新 `7.86 ms` 8 维图并校准 Slide 15 `Ref017 Fig. 7` 网格残差原图（$R^2 = 0.9245$）。
