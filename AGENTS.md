# OV4 协作规则（AI 助手与维护者入口）

[仓库首页](README.md) · [仓库规范](REPOSITORY_MANAGEMENT.md) · [用户偏好](USER_PREFERENCES.md) · [成果索引](outputs/README.md) · [总变更记录](CHANGELOG.md)

## 1. 启动工作前必读顺序

每次在 `D:\work\OV4`（对应 GitHub 仓库 `OpticsPan/OV4`）开始新任务前，按以下顺序核对基线：

1. 阅读本文件（[AGENTS.md](AGENTS.md)）、[用户偏好记录](USER_PREFERENCES.md) 与 [仓库管理规范](REPOSITORY_MANAGEMENT.md)；
2. 阅读 [README.md](README.md) 与最近一条 [CHANGELOG.md](CHANGELOG.md) / `changes/` 日志，了解当前最新正式版本与未决事项；
3. 若本机已安装 Git 且已关联远端 `origin/main`，先检查 `git status --short --branch` 并 `git fetch origin main`，保留用户已有本地修改。

## 2. 本机资料学习与引用规范

- 本机只读参考文献库位于 `D:\work\OV4\参考文献-整理版\`（原始 PDF）与 `D:\work\OV4\参考文献-整理版-Markdown\`（MinerU 转换 Markdown 及提取图表）。**严禁修改或删除这两个目录内的任何文件。**
- 查阅文献时优先检索 Markdown 版本，遇到关键公式、参数表（如 iHOPC 映射表）、高密度图表或 OCR 疑似合并单元格时，**必须回看原始 PDF 页面或提取原图做视觉核验**。
- 引用时逐处注明文献编号、作者/年份、图号/表号或章节号；明确区分“直接调研实测”、“物理/光学仿真计算”与“预算反推预估”。

## 3. 成果归档与默认交付格式

- **默认报告格式（[UP-011](USER_PREFERENCES.md#up-011)）**：未明确指定报告格式时，报告**默认仅整理为 Markdown（`.md`）格式**，不冗余导出 PDF / Excel / PPTX；仅当任务显式指定时再附加生成对应格式。
- 正式成果统一保存至 `outputs/` 对应子目录：
  - `outputs/reports/`：正式 Markdown 报告（`_vN.md`，**必须严格遵守 [UP-010](USER_PREFERENCES.md#up-010) GitHub 网页版阅读与公式规范**）及按需生成的正式 PDF 报告（`_vN.pdf`）；
  - `outputs/tables/`：按需生成的动态公式 Excel 表格（`_vN.xlsx`）；
  - `outputs/images/`：白底高分辨率图件（`_vN.png`）与可编辑架构图源文件（`_vN.drawio`）；
  - `outputs/code/`：可复现仿真、绘图、质检与按需导出脚本（`_vN.py`）。
- 临时计算与中间文件放入 `work/`（由 `.gitignore` 忽略）。
- **提交前强制门禁**：运行 `python outputs/code/audit_github_md_v1.py` 确认 GitHub 网页公式/排版/链接审计 `Errors: 0`；若本次交付含 Excel，须用 Excel 引擎重算确认 0 个公式错误；若本次交付含 PDF / PNG / draw.io，须进行视觉核检确认无截断或文字重叠。

## 4. 每次更新后的强制同步清单

每完成一次正式更新，必须在同一次变更中同步以下 4 处，缺一不可：

1. 新增单次详细日志 `changes/YYYY-MM-DD-主题_v1.md`；
2. 更新 [CHANGELOG.md](CHANGELOG.md)（最近更新置于最前，添加稳定英文锚点）；
3. 更新 [outputs/README.md](outputs/README.md) 成果索引；
4. **更新首页 [README.md](README.md#update-history) 的「更新历史」表格，将最新条目置顶并附直达正式内容（MD / PDF / Excel / 日志）的相对路径链接。**

## 5. GitHub 同步与诚实交付边界

- 本机完成修改与全部自检后，若环境具备 `git` 与有效 GitHub 认证，直接提交并快进推送至 `OpticsPan/OV4` 的 `main` 分支后回读确认。
- 若当前运行环境未安装 `git`/`gh` 或暂未配置远端认证，**如实报告仅完成本地仓库归档**，提供可直接执行的 Git 同步命令，不得将“已写入本地”表述为“已推送 GitHub”。
