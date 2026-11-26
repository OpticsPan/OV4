# 2026-11-26 ENC、AA 与 WS/RS 重复性及分级验收答复

[仓库首页](../README.md) · [总变更记录](../CHANGELOG.md#2026-11-26-enc-aa-stage-repeatability) · [成果索引](../outputs/README.md) · [专项报告](../outputs/reports/ENC_AA_WS-RS重复性与分级验收专项答复_v1.md)

## 改动范围

- Antigravity（反重力 agent）在原 OV4 会话作答，Codex 核对文献原图、统计定义、公式及仓库链接，并整理专项 Markdown 报告。
- 报告覆盖九项问题。ENC 分开验收带内计量、曝光窗等效量和外部参考下的在位稳定性。AA 分开验收每色读数、跨色偏差、可用率、融合及离线 FIWA/HOWA 网格。WS/RS 按单程同向、同周期往返、反向差、返程闭合、停位及同步曝光分别记录。
- 复核了 Castenmiller 等图 4 的 3σ 标注、de Jong 等图 11 的原型网格试验口径、de Graaf 等图 10 的 REPRO 轴，以及 Evers 等表 1 的两类同步统计。具体门限以报告所列工程预算及待验证项为准。

## 核验方式

在仓库根目录运行 `python outputs/code/audit_github_md_v1.py` 和 `git diff --check`。在首页更新历史、成果索引及总变更记录中均可访问本报告。
