# 2026-11-25 变更日志：新增 WS–RS 同步策略与单台重复性专项调研报告（v1）及 13 篇 USPTO 专利入库

[仓库首页](../README.md) · [总变更记录](../CHANGELOG.md) · [成果索引](../outputs/README.md) · [调研报告 v1](../outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v1.md) · [参考文献总目](../REFERENCES.md#sec-wsrs-sync)

## 1. 变更目的

针对 ArF / ArFi 光刻机子系统验收规格论证过程中的三个核心技术问题完成系统调研、一手官方专利原件抓取与正式归档：
1. 数学与实机实证回答：已知 `Sync MA = 0.47 nm` 时，单台 WS 或 RS 的独立重复性是否必然小于 `0.47 nm`；
2. 核验 ASML 与 Nikon 在 ArF / ArFi 机台同步策略中的主从方向（Master vs Slave）及最新双向耦合演进；
3. 汇总 ArF / ArFi 机台 WS / RS 各自独立伺服误差与同步重复性公开实测数据，反校本仓独立 FAT 规格（`WS-X ≤ 0.32 nm` / `RS-X ≤ 0.96 nm`），并同步记录本机已下载与待手动下载的完整文献清单。

## 2. 本次交付与仓库变更清单

| 文件路径 | 变更类型 | 说明 |
| :--- | :---: | :--- |
| [outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v1.md](../outputs/reports/WS-RS同步策略与单台重复性误差专项调研报告_v1.md) | 新增 | 全 5 章 GitHub 网页版适配调研报告（严格遵循 `UP-010`），含含相关系数方差方程、ASML/Nikon 主从专利核验、独立误差/同步重复性数据汇总、FAT 反校及 36 篇三类文献下载状态表 |
| [REFERENCES.md](../REFERENCES.md#sec-wsrs-sync) | 更新 | 新增第 1.2 节 `[S1]–[S13]` 登记表（13 篇 USPTO 专利原件页数与 SHA-256），全库总计由 251 份更新为 **264 份（263 份唯一 SHA-256）** |
| [README.md](../README.md#update-history) | 更新 | 首页「更新历史」首行置顶登记本次专项调研报告与 13 篇 USPTO 专利入库，并同步更新「当前主交付成果一览」与 `REFERENCES.md` 统计说明 |
| [outputs/README.md](../outputs/README.md) | 更新 | 新增「专题调研报告」条目并刷新最新更新横幅 |
| [CHANGELOG.md](../CHANGELOG.md#2026-11-25-ws-rs-sync-survey-v1) | 更新 | 顶部追加全局变更时间轴条目 |
| `D:\work\OV4\参考文献_新增\WS-RS同步\`（13 份 PDF，366 页，`.gitignore` 排除） | 本地下载 | 自 USPTO 官方公共 PDF 接口直下 8 篇 ASML + 5 篇 Nikon 专利原件（`[S1]–[S13]`），全部完成封面视觉核验与 SHA-256 唯一性校验 |

## 3. 核验与纠偏亮点

1. **官方原件实锤**：下载并视觉核验 Nikon `US 2012/0319637 A1`（`[S12]`，72 页）首页控制框图，直观呈现 `wafer error → synch target filter H(s) → reticle stage` 的 **WS = Master、RS = Slave** 架构，与 Nikon `NSR-S308F`（`[090]`）、`NSR-S620D`（`[085]`）及 ASML `[022]` / `[147]` / `[075]` 互证。
2. **元数据防错纠偏**：通过封面核验纠正了在线搜索摘要对 `US 7,405,811 B2`（实为 ASML Beems & Sakai，非 Nikon）与 `US 8,451,431 B2`（实为 Nikon Yang & Koo，非 ASML）的误归属，同时记录了对本仓 `v2` 说明书第 1.3 节第 ④ 条主从方向措辞的后续勘误备忘。
3. **手动下载清单**：针对 8 篇因 IEEE/Elsevier 付费墙或非 US 专利站点 503 限流而无法脚本直下的文献（`[M1]–[M8]`，其中 `Lambregts 2015 ACC` DOI 已由 Crossref 核准为 `10.1109/ACC.2015.7171980`），完整列出直达链接与建议保存文件名。
4. **GitHub 渲染门禁**：已通过 `python outputs/code/audit_github_md_v1.py` 链接与公式双项 `Errors: 0` 校验。
