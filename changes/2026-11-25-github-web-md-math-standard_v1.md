# 2026-11-25 · 新增仓库规定：GitHub 网页版阅读与数学公式渲染强制适配（UP-010）及存量 v2 报告全量修复

[项目首页](../README.md) · [仓库规范](../REPOSITORY_MANAGEMENT.md#sec-markdown) · [用户偏好 UP-010](../USER_PREFERENCES.md#up-010) · [成果索引](../outputs/README.md) · [总变更记录](../CHANGELOG.md#2026-11-25-github-web-md-standard)

## 1. 本次变更概述

应用户新增仓库规定要求——**“在 GitHub 上给人阅读的 `.md` 报告，格式需要适配网页版阅读；尤其是公式”**，本次完成“制度落地 + 自动化门禁脚本 + 存量最新 `v2` 报告全量适配 + 双端 PDF 构建器同步升级”四步闭环：

1. **制度落地（[UP-010](../USER_PREFERENCES.md#up-010)、[REPOSITORY_MANAGEMENT.md 第 4.3 节 & 第 7 节](../REPOSITORY_MANAGEMENT.md#sec-markdown)、[AGENTS.md](../AGENTS.md)）**：
   - **块级公式（Display Math）**：一律采用独立多行 `$$` 围栏（或 ` ```math `），起止 `$$` 各自独占一行、前后各留空行、优先 `0` 缩进（严禁 `≥ 4` 空格深缩进或单行 `$$...$$` 紧贴列表，防止 GitHub CommonMark 误判为代码块或原样暴露）；
   - **行内公式（Inline Math）**：含 `≥ 2` 个下划线 `_`、星号 `*` 或特殊括号的行内公式一律采用 GitHub 官方反引号定界语法（`` $`...`$ ``），并与相邻中文留空格，彻底防止 `cmark-gfm` 将 `_..._` 误解析为斜体 `<em>`；禁止 `$` 内侧空格、禁止 `**$...$**` 粗体包裹、禁止公式内混写中文；
   - **表格内公式与便携宏**：Markdown 表格单元格内公式严禁出现裸 `|` 或 `\|`，绝对值统一改用 `\vert ... \vert`（同时兼容 GitHub MathJax 与本机 Matplotlib STIX，禁用 STIX 不支持的 `\lvert`/`\rvert`），集合花括号统一用 `\lbrace ... \rbrace`；
   - **网页版阅读洁净度**：孤立带单位数值优先用纯文本 Unicode 或反引号、禁止 CommonMark 标点侧翼粗体冲突、禁止 `file:///` 绝对路径。
2. **新增自动化质检门禁脚本（[audit_github_md_v1.py](../outputs/code/audit_github_md_v1.py)）**：
   - 一键扫描全仓 GitHub 网页版公式/排版规范与所有相对路径/锚点链接，接入 `REPOSITORY_MANAGEMENT.md` 第 7 节提交前必跑清单。
3. **存量最新正式报告全量适配与双端 PDF 同步验证**：
   - 完整修复 [九大核心子系统说明书 v2 MD](../outputs/reports/NXT1950i-1970i套刻目标_九大核心子系统验收指标推导与计算说明书_v2.md)、[15 大类验收规格推导报告 v2 MD](../outputs/reports/NXT1950i-1970i套刻目标_整机及子系统验收规格推导报告_v2.md) 与 [v2 变更日志](2026-11-24-spec-budget-v2-acceptance-deepdive_v2.md) 中全部 167 处 GitHub 网页公式隐患（含深缩进单行 `$$`、表格内裸 `|`/`\|`、含多下划线行内 `$...$`、`**$...$**` 与 `\{`/`\}`），所有数值与结论保持 100% 不变；
   - 同步升级 [build_9subsys_doc_pdf_v2.py](../outputs/code/build_9subsys_doc_pdf_v2.py) 与 [build_spec_pdf_v2.py](../outputs/code/build_spec_pdf_v2.py) 原生支持 `` $`...`$ `` 与 ` ```math ` 语法并重编译双份 `v2` PDF 验证 0 报错、0 公式回退。

## 2. 本次核验结果

- `python outputs/code/audit_github_md_v1.py`：全仓 Markdown 相对路径链接审计 **0 错**，全部活跃 Markdown 文档 GitHub 网页版公式与排版审计 **0 错**。
- 两份 `v2` PDF 重建与视觉抽检通过（STIX 矢量公式 0 回退、0 误转 `<pre>` 块）。
