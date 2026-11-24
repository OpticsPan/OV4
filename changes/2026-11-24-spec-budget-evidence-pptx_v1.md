# 2026-11-24 · 15 大类验收规格与逐条证据链 22 页 PPTX 及可复现脚本归档

[项目首页](../README.md) · [成果索引](../outputs/README.md) · [总变更记录](../CHANGELOG.md#2026-11-24-spec-budget-pptx-v1)

## 1. 本次变更概述

围绕 [NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx](../outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v1.xlsx) 与 [综合推导报告 v1](../outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md)，制作并归档 22 页 16:9 白底高清演示文稿，逐条解释全部 15 大类子系统验收规格的**原始论文/手册调研截图**、**物理公式推导过程**与**光学/热学/运动学仿真方法**；同时将 4 份可复现仿真与构建脚本纳入 `outputs/code/` 正式版本管理，使全仓四形态交付物（MD / PDF / XLSX / PPTX）与构建代码实现完整可追溯闭环。

## 2. 本次新增与归档交付物核验

| 交付文件 | 字节数 | SHA-256 | 说明 |
| :--- | ---: | :--- | :--- |
| [逐条证据链演示文稿 PPTX v1](../outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v1.pptx) | 4,155,985 | `989bb8efbb9d7fb5819564a7f17926f4f8da100826130da82eb1fed7d8622740` | 22 页 16:9 白底汇报版，含 25+ 张 OV4/ME3 原始论文截图与 4 张 260 DPI 仿真/分析图 |
| [PPTX 构建脚本](../outputs/code/build_spec_pptx_v1.py) | 81,152 | `8840c000d60df7e2cd2e338540bfc1d39a89628c5ffd541d1f44308e2ee3ab2b` | 复现 22 页 PPTX 与高清图件排版 |
| [2D Abbe 奇像差仿真脚本](../outputs/code/sim_zernike_ovl_v1.py) | 10,908 | `c680a3df20e65ede4feee5d8b5d98e151316b7fb04e93225d3e7113e1e6a7168` | 复现 Fringe Zernike `Z5–Z64` 奇像差套刻敏感度矩阵 |
| [Excel 动态预算表生成脚本](../outputs/code/build_spec_excel_v1.py) | 99,446 | `6ed9591825b46879f47812a5c070720daa183eaf0cb7f2319646feeedcad3b8f` | 复现 6 表 430 动态公式 Excel 工作簿 |
| [PDF 正式报告导出脚本](../outputs/code/build_spec_pdf_v1.py) | 22,225 | `7ffb37485279c9a0d8faf136462c04eef779afb051f9f9509dedc83cb4d8d630` | 复现 24 页印刷级 PDF（38 书签 + STIX 公式 + 横版宽表） |

## 3. 22 页 PPTX 逐条证据链结构

| 页码 | 覆盖模块 / 验收大类 | 嵌入原始论文截图 / 解析推导 / 仿真图表 |
| :---: | :--- | :--- |
| P01 | 封面与顶层 KPI 总览 | 顶层目标 DCO ≤ 2.00 nm / MMO ≤ 3.50 nm / FU ≤ 12.0 nm 及四形态一致基线 |
| P02 | 整机对标与代际标尺（1950i → 1970Ci） | OV4 `009` Fig.3、`066` Fig.2 全 4 联高清裁切图、`015` Fig.7 |
| P03 | 整机 DCO / MMO / FU 预算分配与 RSS 闭环 | 260 DPI 分析图 `chart_01`（Excel 430 动态公式闭环：1.834/1.869、3.134/3.154、10.34 nm） |
| P04 | ArF 液浸 6-DOF 光学灵敏度矩阵 | OV4 `094` Fig.16、`225` Fig.1.9 与 1/4 缩小及液浸折射率推导 |
| P05 | 第 1 项：WS 6-DOF 重复性误差（6 行明细） | OV4 `066` Fig.9、`009` Fig.10(L) 与 Z 轴焦面/RxRy 倾斜换算 |
| P06 | 第 2 项：RS 6-DOF 重复性误差（6 行明细） | OV4 `094` Fig.24、`225` Fig.1.9 与 4×/16× 杠杆关系推导 |
| P07 | 第 3 项：WS-RS 同步运动误差 MA（6 行明细） | OV4 `009` Fig.10(R)、`075` Fig.13 与 $\mathrm{MA}_{\mathrm{sync}} = \mathrm{WS} - \mathrm{RS}/4$ 闭环 |
| P08 | 第 4 项：ENC 光栅编码器测量重复性（16 行明细） | OV4 `009` Fig.4、`062` Fig.11 与底层测量噪声 < 执行器 1/3 原则 |
| P09 | 第 5 项：M-side 晶圆对准系统 AA（SMASH） | OV4 `015` Fig.10 与对准重复性/工艺色散抑制推导 |
| P10 | 第 6 项：E-side 空间像对准系统（TIS/PARIS） | OV4 `066` Fig.8、`254` Fig.2 与 TIS/PARIS 静态与热漂校准链路 |
| P11 | 第 7 项：Wafer Table 温控误差 | OV4 `021` Fig.12、`017` Fig.7 与 Si CTE 2.6 ppm/K 径向伸缩计算 |
| P12 | 第 8 项：Reticle 附近温控误差 | OV4 `016` Fig.6、`254` Fig.3 与石英掩模 CTE 0.55 ppm/K 及 EUV/ArF 对比 |
| P13 | 第 9 项：RT 掩模夹持误差 | OV4 `225` Fig.1.8、Fig.6.15 与掩模重力垂度/真空吸附面形分析 |
| P14 | 第 10 项：WT 晶圆夹持误差 | OV4 `066` Fig.10a、`009` Fig.3 与硅片局部翘曲/背面颗粒平面度预算 |
| P15 | 第 11 项：Wafer Handler 温控误差 | `ME3 05-TT-L2-WH` Fig.2.5（TSU 热稳定单元）+ 260 DPI 瞬态热弛豫仿真图 `chart_02` |
| P16 | 第 12 项：整机 Frame 稳定性误差 | OV4 `019` Fig.9、Fig.15 与计量框架热漂/微振动传递预算 |
| P17 | iHOPC K1–K20 官方参数定义与执行器分工 | OV4 `154` 第 7 页 Eq.1 & Table 1 高清裁切图、`254` Fig.9 |
| P18 | 第 13 项：物镜对 iHOPC 场内参数补偿残差 | OV4 `253` Fig.7、Fig.8（Z2 SET-vs-GET 实测）与物镜可调项残差推导 |
| P19 | 第 14 项：WS 对 iHOPC 场内参数补偿残差 | 8 mm 狭缝扫描平均去卷积公式 + 260 DPI 仿真曲线图 `chart_03`（`c_slit` 放大因子） |
| P20 | 第 15 项（上）：Odd Zernike 波像差 Abbe 仿真方法 | OV4 `024` Fig.2、`008` Fig.4a + 260 DPI 2D Abbe 敏感度图 `chart_04` |
| P21 | 第 15 项（下）：Z5–Z64 全 30 项奇像差控制预算与验证 | OV4 `024` Fig.11（FlexWave 实测）与全 30 项分配汇总表 |
| P22 | FAT/SAT 验收路径与四形态可追溯交付闭环 | MD / PDF / XLSX / PPTX + 4 份代码脚本一致性与仓库入口总览 |

## 4. 质量核验记录

1. **全 22 页视觉检视（PowerPoint COM → PDF → PNG）**：
   - 将生成的 `.pptx` 通过本机 Microsoft PowerPoint COM 导出 PDF 后逐页转 PNG 核检。
   - 发现并修复 3 处版面细节：① P02 将 MinerU 截断的 `066` 窄条替换为 `066_86831L.pdf` 第 2 页 220 DPI 全 4 联 Figure 2 裁切图；② P18 将重复的 `009` 图替换为专属的 `253` Fig.8（Z2 SET-vs-GET 实测曲线）；③ P19 放大 `c_slit` 狭缝去卷积仿真图提升可读性。复检 P02、P18、P19 确认 22 页全部零溢出、零截断、零重叠、零缺字警告。
2. **仓库治理同步与链接审计**：
   - 同步更新 [README.md](../README.md#update-history)（最新条目置顶）、[CHANGELOG.md](../CHANGELOG.md#2026-11-24-spec-budget-pptx-v1)、[outputs/README.md](../outputs/README.md)、[REPOSITORY_MANAGEMENT.md](../REPOSITORY_MANAGEMENT.md) 及 `.gitignore`（排除本地只读入口 `/开始阅读.html` 与 `~$*.pptx`）。
   - 全仓 Markdown 相对路径与锚点扫描确认 0 断链、0 本机绝对路径泄露，只读文献区 `参考文献-整理版/` 与 `参考文献-整理版-Markdown/` 保持零改动且未被 Git 跟踪。
