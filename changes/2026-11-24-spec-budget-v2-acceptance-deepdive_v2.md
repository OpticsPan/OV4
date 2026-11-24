# 2026-11-24 · NXT:1950i–1970Ci 验收规格与误差预算 v2 深度验收升级版

[项目首页](../README.md) · [成果索引](../outputs/README.md) · [总变更记录](../CHANGELOG.md#2026-11-24-spec-budget-v2)

## 1. 本次 v2 升级核心内容

在严格保留 `v1` 全部文件及顶层套刻/焦面数学闭环（DCO = `1.834 / 1.869 nm ≤ 2.00 nm`，MMO = `3.134 / 3.154 nm ≤ 3.50 nm`，FU = `10.34 nm ≤ 12.0 nm`）的基础上，全面回应并落地整机子系统验收 4 大核心工程专题，同步升级 **PPTX（28 页）、Excel（9 表 686 公式）、Markdown 报告、PDF 报告（30 页 / 45 书签）及 3 份可复现构建代码**：

1. **WS 6-DOF 独立验收必要性反驳与单程/往返验收细则**（报告第 1.3–1.4 节、Excel Sheet 07A–07B、PPTX P06–P07）：
   - 精准评估并补强“场间步进切入下一视场预计算起扫位”观点，给出 6 大工程铁证彻底反击“WS–RS 同步覆盖 WS 自身 6-DOF”论调（M-side 无 RS 参与、15 ms 首狭缝整定尾、Z/Rx/Ry 液浸弯月面不可兜底、4× 动力学与 MSD 惩罚、iHOPC 独立执行、子系统 FAT 合同边界）；
   - 给出适配 ISO 230-2 与 8 mm 狭缝 MA 的单程（$R_{\mathrm{uni}}$）、残余反向差（$B_{\mathrm{res}}$）与往返综合重复性（$R_{\mathrm{bi}} = R_{\mathrm{uni}} + B_{\mathrm{res}}$）严格数学定义及 6 自由度行程/步进/扫描验收细则，并配原图 [094 Fig.15] 与 260 DPI 双联图。
2. **RS 6-DOF 独立验收必要性反驳与 150 m/s² 单程/往返及微滑移细则**（报告第 2.2–2.3 节、Excel Sheet 07C、PPTX P09）：
   - 给出 5 大 RS 反击铁证（WS 前馈推力与液浸弯月面天花板、15g 掩模微滑移在编码器同步曲线中隐身、静态 RA/PARIS、1:1 Rz 映射、BM 反力解耦 FAT）；
   - 明确掩模侧 4× 行程规划（132 mm 曝光 + 100 mm 加减速 = 230–250 mm 单次扫描、2.80 m/s、150 m/s²、1000 趟交替正反扫 + 5 mK 水平气幕 + 掩模微滑移抽检 ≤ 0.60 nm 4×）。
3. **WS 对 iHOPC 参数（以 K4 为例）离线/在线验收方案审视与 8 mm 狭缝逆卷积专页图解**（报告第 14.3–14.4 节、Excel Sheet 08A–08C、PPTX P24–P25）：
   - 逐条审视用户离线 `Q_enc(t) - Q_0(t)` 方案，指出其作为子系统 FAT 骨架高度合理，但须补齐 5 项关键修正：① 8 mm 狭缝滑动平均滤波（MA）；② 7×9 虚拟视场 OLS 回归提取 $\Delta K_m$ 与跨项串扰；③ Z/Rx/Ry 阿贝臂伴随护栏；④ 破解“ENC 测 ENC 自己”自闭环盲区的三级验收闭环（离线伺服 55% → 外部双频干涉仪标尺 → 在线曝光 100%）；⑤ 全 11 项量程、最小调节量与分级指标表；
   - 增设 **8 mm 曝光狭缝卷积与逆卷积专页 PPT（P25）** 及动态 Excel 逆卷积计算器（Sheet 08C），含正向卷积积分、二/三阶解析逆卷积修偏公式（`K14/K19` 不逆卷积多出 `+0.264 nm` 场角线性串扰）、频域 $\mathrm{sinc}$ 截止波长（$\lambda_y \le 8\text{ mm}$ 不可补）及三联 260 DPI 图解。
4. **投影物镜对 K 参数补偿能力的 8 维综合评价体系**（报告第 13.4 节、Excel Sheet 09A–09B、PPTX P22）：
   - 构建覆盖 **D1 单参/联合 Range（≤80% 占用）、D2 最小调节量（≤Spec/10）、D3 单向重复性与双向滞回（≤35% / ≤25%）、D4 SET-vs-GET 线性度、D5 跨 K 串扰与焦面/波像差副作用、D6 响应/整定时间（含 Nikon MDDM 50 ms 实测原图）、D7 保持与热蠕变漂移、D8 三级验证链路（PMI→ILIAS/PARIS→光刻胶 OVL）** 的完整量化评价矩阵。

## 2. v2 交付物清单与 SHA-256 校验

| 交付文件 | 字节数 | SHA-256 | 核心核验结果 |
| :--- | ---: | :--- | :--- |
| [逐条证据链演示文稿 PPTX v2](../outputs/presentations/NXT1950i-1970i套刻目标_15大类子系统验收规格与逐条证据链_v2.pptx) | 5,982,235 | `de1ea7391b4f7b7e08916af425e70cdf919768ba78208d781e5516239d11fc18` | 28 页 16:9，新增 6 页专题 + 3 张新图，PowerPoint 导出逐页视觉质检通过 |
| [动态公式 Excel 预算与验收表 v2](../outputs/tables/NXT1950i-1970i套刻目标_15大类子系统验收规格与误差预算表_v2.xlsx) | 83,026 | `77847c2bae0953fe44585f5f0a7c3b81a106690cae186483598343060f8a6715` | 9 工作表 / **686 动态公式**，Microsoft Excel COM 实算 `Errors = 0` |
| [综合推导报告 Markdown v2](../outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md) | 114,150 | `31bf1d473915630b24c06521bb2e4e5b7c3c619d5916b06ca5c86031f459065d` | 0 断链、0 未解析 CommonMark 粗体、与 Excel 数值 100% 一致 |
| [综合推导报告 PDF v2](../outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.pdf) | 2,857,158 | `ee78b1d5f9fe0857dbb46a8d83cb64542b05e462a77b6ee8290a12753463ca2f` | 30 页 / 45 书签 / 0 mathtext 警告 / 第 13–15 章横版宽表抽检通过 |
| [Excel v2 构建脚本](../outputs/code/build_spec_excel_v2.py) | 136,907 | `4b9915a9c9f61e6088f2a960abefa5da2cbec0f9a2ea5b0869816b04302b2846` | 完整复现 9 表 686 公式工作簿 |
| [PDF v2 导出脚本](../outputs/code/build_spec_pdf_v2.py) | 22,826 | `b7da9144827eb6d43a5d47bb50872afd40a5bc8bd6bad2f5e87864a2a114bac2` | 完整复现 30 页 45 书签 PDF |
| [PPTX v2 构建脚本](../outputs/code/build_spec_pptx_v2.py) | 108,356 | `c3eaea8ef9a7e3a6a09f2fda4c1ce93e5dd1c3fc477db0426aa93c7e9f62c806` | 完整复现 28 页高清 PPTX |
