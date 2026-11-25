# OV4 仓库管理规范

[仓库首页](README.md) · [成果索引](outputs/README.md) · [用户偏好](USER_PREFERENCES.md) · [协作规则](AGENTS.md) · [总变更记录](CHANGELOG.md)

本文件是 `OV4`（先进光刻机套刻误差控制与子系统验收规格）仓库管理规则的唯一维护位置，适用于本机工作目录 `D:\work\OV4` 及对应的 GitHub 仓库 `OpticsPan/OV4`。

**核心原则：所有正式成果以 GitHub 网页直接阅读为主，辅以可计算表格与印刷级 PDF；每次更新均须同步首页更新历史与变更日志，最近更新始终排在最前面。**

<a name="contents"></a>

## 目录

- [1. 仓库目录分工](#sec-layout)
- [2. 首页更新历史展示规范](#sec-homepage)
- [3. 变更记录与版本命名规则](#sec-versioning)
- [4. 文档排版、公式与导航规范](#sec-markdown)
- [5. PDF 与 Excel 多形态交付规范](#sec-artifacts)
- [6. 只读参考资料区保护红线](#sec-readonly)
- [7. 提交与同步前自检清单](#sec-checklist)

<a name="sec-layout"></a>

## 1. 仓库目录分工

[返回目录](#contents)

| 路径 | 职责 | Git 跟踪状态 |
| :--- | :--- | :---: |
| [README.md](README.md) | 仓库首页：核心入口导航 + **更新历史总表（最新置顶，直达正式成果）** | 跟踪 |
| [REPOSITORY_MANAGEMENT.md](REPOSITORY_MANAGEMENT.md) | 仓库管理规范唯一维护位置（本文件） | 跟踪 |
| [USER_PREFERENCES.md](USER_PREFERENCES.md) | 用户长期偏好记录（`UP-xxx` 编号管理） | 跟踪 |
| [AGENTS.md](AGENTS.md) | AI 助手及协作者启动入口、学习与交付流程 | 跟踪 |
| [REFERENCES.md](REFERENCES.md) | **全库参考文献清单总目**（记录全部本地原件书目、新增批次、页数、SHA-256 与引用状态） | 跟踪 |
| [CHANGELOG.md](CHANGELOG.md) | 全局变更记录汇总（带稳定锚点，倒序排列） | 跟踪 |
| `changes/` | 逐次变更明细日志，命名 `YYYY-MM-DD-主题_v1.md` | 跟踪 |
| `outputs/README.md` | 正式成果按类型与主题分类索引 | 跟踪 |
| `outputs/reports/` | 正式 Markdown 报告、正式 PDF 报告及审阅草稿 | 跟踪 |
| `outputs/tables/` | 正式可计算 Excel 规格表与误差预算表（`.xlsx`） | 跟踪 |
| `outputs/presentations/` | 正式汇报演示文稿（`.pptx`，含原始论文截图与仿真图表证据链） | 跟踪 |
| `outputs/images/` | 正式技术插图、仿真曲线与示意图（白底高分辨率） | 跟踪 |
| `outputs/code/` | 可复现光学/物理仿真脚本、Excel/PDF/PPTX 构建脚本 | 跟踪 |
| `work/` | 本地临时计算、中间 JSON 缓存、浏览器打印临时文件 | 忽略（`.gitignore`） |
| `参考文献-整理版/`、`参考文献-整理版-Markdown/`、`参考文献_新增/` | 本机**只读原始参考文献库**（243 份基线 + 8 份新增一手 PDF 与 MinerU Markdown，清单见 [REFERENCES.md](REFERENCES.md)） | 忽略（`.gitignore`） |

<a name="sec-homepage"></a>

## 2. 首页更新历史展示规范

[返回目录](#contents)

依据用户 2026-11-23 明确要求（见 [UP-002](USER_PREFERENCES.md#up-002)）：

1. **强制首页展示**：每一次仓库更新（包括新增报告、修订数值、新增表格/PDF、调整仓库规范或偏好），都必须在根目录 [README.md](README.md#update-history) 的「更新历史」表格中同步新增一条记录。
2. **最近更新置顶**：按 Asia/Shanghai 日期**倒序排列**，最新日期永远位于表格第一行；同一日期内的多次更新，最新一次排在最上面。
3. **直达正式内容**：每条更新记录必须包含：① 日期（`YYYY-MM-DD`）、② 一句话清晰说明本次变更要点、③ 可直接点击跳转的**正式成果相对路径链接**（如 Markdown 报告正文/章节锚点、PDF 正式版、Excel 表格、源码脚本）以及**对应变更日志链接**。不得仅写笼统文字或本地绝对路径。
4. **未更新首页视为未交付**：新增或修改正式文件但未同步更新 `README.md` 与 `CHANGELOG.md` / `changes/` 时，不得宣称交付完成。

首页更新条目标准格式：

```markdown
| 日期 | 变更内容 | 正式成果与日志链接 |
| :--- | :--- | :--- |
| YYYY-MM-DD | 一句话概括本次新增或修订的核心内容。 | [正式报告 MD](outputs/reports/文件名_v1.md) · [正式报告 PDF](outputs/reports/文件名_v1.pdf) · [Excel 表格](outputs/tables/文件名_v1.xlsx) · [变更日志](changes/YYYY-MM-DD-主题_v1.md) |
```

<a name="sec-versioning"></a>

## 3. 变更记录与版本命名规则

[返回目录](#contents)

1. **成果版本后缀**：所有正式交付文档、表格、PDF、图件与脚本在扩展名前统一附加递增版本后缀 `_v1`、`_v2`、`_v3`……（例如 `NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v1.md`）。根目录固定治理文件（`README.md`、`CHANGELOG.md`、`REPOSITORY_MANAGEMENT.md`、`USER_PREFERENCES.md`、`AGENTS.md`）不加版本号。
2. **保留历史版本**：发布新版本（如 `_v2`）时保留已发布的 `_v1`，确保历史变更日志与旧链接永远可追溯；首页与成果索引将默认阅读入口指向最新版本。
3. **双层变更记录**：
   - `changes/YYYY-MM-DD-主题_v1.md`：记录单次任务的完整改动列表、关键数值变化、验证方式与复现命令；
   - [CHANGELOG.md](CHANGELOG.md)：按时间倒序汇总历次发布，并设置唯一、稳定的英文锚点（如 `<a name="2026-11-23-v1-baseline"></a>`）供首页与跨文档引用。

<a name="sec-markdown"></a>

## 4. 文档排版、公式与导航规范

[返回目录](#contents)

1. **统一导航与目录**：
   - 每份正文报告仅使用一个一级标题 `#`，紧跟顶部快捷导航栏（返回首页、成果索引、配套 PDF/Excel 与变更日志）。
   - 正文包含 3 个及以上二级章节或超过 120 行时，必须在文首提供可点击目录，为所有主要章节设置稳定英文锚点（`<a name="sec-..."></a>`），并在章节内提供 `[返回目录](#contents)`。
2. **相对路径与可移植性**：仓库内所有 Markdown 链接一律使用**相对路径**（中文文件名中若含空格需做 URL 编码，避免空格）；严禁在提交至 GitHub 的 `.md` 中写入 `file:///D:/...` 本机绝对路径。
3. **GitHub 网页版阅读与数学公式渲染强制规范（[UP-010](USER_PREFERENCES.md#up-010)）**：
   所有面向人类在 GitHub 网页端阅读的 `.md` 报告必须严格适配 GitHub Flavored Markdown（`cmark-gfm`）与 **MathJax** 引擎，同时兼顾本机 Matplotlib STIX PDF 导出：
   - **块级公式（Display Math）**：
     - 必须使用**多行独立 `$$` 围栏**（起止 `$$` 各自独占一行，表达式夹在中间），且**块前与块后必须各保留至少一个空行**；严禁单行 `$$...$$` 紧贴正文/列表，严禁相邻两个 `$$` 块无空行堆叠；
     - 块级公式优先置于**顶格（`0` 缩进）独立段落**（严禁在列表内缩进 `≥ 4` 空格，避免 CommonMark 将其误判为缩进代码块导致原样暴露 `$$`）；
     - 如需联立多行方程，优先拆为多个独立 `$$` 块（中间留空行），避免使用本机 STIX 不支持的 `\begin{aligned}` 环境。
   - **行内公式（Inline Math）**：
     - **含 2 个及以上下划线 `_`、星号 `*`、反斜杠括号或复杂上下标的行内公式**，必须使用 GitHub 官方反引号定界语法（`` $`...`$ ``，例如 `` $`T_{\mathrm{slit}} = L_s / v_w`$ ``），彻底隔绝 `cmark-gfm` 在 MathJax 运行前将 `_..._` 误解析为斜体 `<em>`；
     - 行内 `$...$` 或 `` $`...`$ `` **内侧严禁留空格**（禁止 `$ x $`），与前后中文字符间建议留半角空格以防粘连或定界符误判；
     - **严禁用粗体包裹公式**（禁止 `**$...$**`），需加粗时在 LaTeX 内部使用 `\mathbf{...}` 或仅加粗外部中文；
     - **简单孤立数值、范围与带单位常量**（如 `≤ 2.00 nm`、`26 × 5.5 mm`、`±15–25 ppm`、`3σ`）优先使用纯文本 Unicode（`×`、`±`、`≤`、`≥`、`μ`、`σ`、`λ`）或反引号代码，减少网页端 MathJax 渲染卡顿。
   - **表格内公式与特殊符号防冲突**：
     - **Markdown 表格单元格（`| ... |`）内的公式严禁出现裸竖线 `|` 或 `\|`**（GFM 表格解析器早于 MathJax 切分列，会导致表格错列或渲染成双竖线范数）；绝对值一律使用 **`\vert ... \vert`**（如 `` $`\vert\Delta S_{\mathrm{env}}\vert`$ ``），集合花括号统一用 **`\lbrace ... \rbrace`**；
     - 禁用在 GitHub 或本机 STIX 中报错的 LaTeX 宏：`\operatorname{...}`、`\tag{...}`、`\lvert`、`\rvert`；统一使用 `\mathrm{...}`、`\vert`，公式编号放于公式块外；
     - **公式内严禁混写中文字符**（如 `\text{稳态}`），中文注释一律置于公式外；正文中的字面美元符号 `$` 须转义为 `\$`（或放进反引号）。
   - **网页版排版与 CommonMark 洁净度**：
     - 严禁出现无法解析的 CommonMark 标点侧翼粗体（如 `**文字（括号）**紧接汉字`），应将右括号移出粗体或留空格；
     - 正文中 `<` 后紧跟字母或易被误判为 HTML 标签的片段须加空格或反引号（如 `` `< 15 mm` ``）；表格单元格保持精炼，避免超长无空格串拉宽网页横向滚动条；
     - 配套 PDF 导出脚本（`outputs/code/build_*_pdf_v*.py`）必须同步兼容 `` ```math ``、`$$\n...\n$$` 与 `` $`...`$ `` 语法，确保“一份 Markdown 源，GitHub 网页与本地 PDF 双端零瑕疵渲染”。
4. **推导依据透明化**：任何技术规格与数值推导均须明确标注依据类型——**直接调研证据**、**物理/光学解析与仿真计算**、或**误差预算反推预估**，并注明来源文献编号及图表页码。

<a name="sec-artifacts"></a>

## 5. PDF 与 Excel 多形态交付规范

[返回目录](#contents)

1. **数值一致性**：同一专题的 Markdown、PDF、Excel 三份交付物必须保持 100% 数值一致（均由同一份计算数据源与验证脚本产出）。
2. **Excel 规范**：
   - 所有汇总、放大系数、RSS 闭合与百分比必须采用原生动态 Excel 公式，不得硬编码计算结果；
   - 交付前须经 Microsoft Excel 引擎重算并保存缓存值，核验公式错误数 `FormulaErrorsCount = 0`。
3. **PDF 规范**：
   - 正式 PDF 由可复现脚本（`outputs/code/build_*_pdf_v1.py`）从对应正式 Markdown 导出，使用无头浏览器 + 矢量数学公式渲染，并由 PyMuPDF 写入精确页码目录、PDF 侧边栏书签（Outline）与元数据；
   - 含宽表（如 13 列以上 iHOPC / Zernike 表格）的章节必须使用横向 A4 页面或响应式列宽，确保零裁切、零文字重叠；
   - 交付前必须重新打开生成的 PDF，核查总页数、书签跳转有效性，并对封面/目录、公式页及宽表页进行视觉抽检。

<a name="sec-readonly"></a>

## 6. 只读参考资料区保护红线

[返回目录](#contents)

- `D:\work\OV4\参考文献-整理版\` 与 `D:\work\OV4\参考文献-整理版-Markdown\` 均为**严格只读原始参考资料区**。
- 严禁在该两目录内新增、编辑、覆盖、移动、重命名或删除任何文件及子目录；中间解析脚本、提取缓存和仿真中间数据一律写入 `work/`。
- 该两目录及原始入口 `开始阅读.html` 所对应的外部参考文献体积庞大，由 `.gitignore` 排除，仅保留在本机供调研查证，不推送至 GitHub 远端。

<a name="sec-checklist"></a>

## 7. 提交与同步前自检清单

[返回目录](#contents)

- [ ] 新增或更新的正式成果已按类型归档至 `outputs/reports/`、`outputs/tables/`、`outputs/presentations/`、`outputs/images/` 或 `outputs/code/`，文件名带正确版本后缀 `_vN`。
- [ ] **GitHub 网页版阅读与公式门禁通过**：已运行 `python outputs/code/audit_github_md_v1.py`，确认最新正式报告与根目录文档达到 `Errors: 0`（多行 `$$` 块前后空行无深缩进、复杂行内公式采用 `` $`...`$ ``、表内无裸 `|`/`\|`、无 `**$...$**`、无未解析粗体、无 `file:///` 绝对路径、0 断链与 0 断锚点）。
- [ ] 若交付 Excel，已通过公式审计（0 个 `#REF!/#NAME?/#VALUE!/#DIV/0!`）且缓存值已更新。
- [ ] 若交付 PDF，已核验总页数、目录页码、PDF 书签与宽表/公式视觉排版无截断。
- [ ] 已新增 `changes/YYYY-MM-DD-主题_v1.md`，并按倒序同步更新 `CHANGELOG.md`、`outputs/README.md` 与首页 `README.md`（「更新历史」最新一条位于最前面）。
- [ ] 若远端 `OpticsPan/OV4` 已连接且本地具备 Git 凭据，已推送至 `main` 并回读确认；若当前环境暂缺 Git 工具或凭据，如实记录状态并提供同步命令，绝不虚报“已推送”。
