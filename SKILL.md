---
name: factor-optimize
description: "当 agent 需要对一个已有股票或期货因子做原地优化时使用：复用项目本地数据和评价引擎，扫描关键 period 参数，在 best period 上做组件消融，从 core 版本出发做 refinement，并在文件报告和对话回答中同时给出指标表、稳健性讨论和是否替换原因子的结论。Use for optimizing one existing stock or futures factor with period sweeps, ablations, refinements, robustness discussion, and a keep-or-replace decision."
quantSkills:
  organization: https://github.com/quantskills
  repository: quantskills/skill-factor-optimize
  repository_url: https://github.com/quantskills/skill-factor-optimize
  project_type: skill
  collection: factor-research
  license: GPL-3.0-only
  category: factor
  tags: [factor-optimize, factor-research, period-sweep, ablation, refinement, ic]
  platforms: [claude-code, codex, cursor, hermes, openclaw]
  language: zh-en
  status: draft
  validation_level: listed
  maintainer_type: community
  requires: []
  summary_zh: 对已有股票或期货因子做参数扫描、组件消融和核心版本增强，并输出是否替换原因子的结论。
  summary_en: Optimize an existing stock or futures factor with period sweeps, ablations, refinements, and a final keep-or-replace decision.
---

# 因子优化

用这个 skill 对一个已有量化因子做诊断、优化和 baseline 选择。不要用它做开放式因子挖掘。

默认使用中文进行分析、命名和报告。除非项目原有文件、用户要求或代码接口必须使用英文，产出的 Markdown、summary、对话结论都应以中文为主。

## 核心规则

1. 复用项目已有的因子源码、数据加载器、label/target、评价引擎、日期范围、频率、股票池/品种池、成本假设和报告风格。除非用户明确要求，不要另起一套引擎。
2. 指标优先级为：用户指定指标 > 项目已有指标 > 通用因子指标。若使用推断指标，必须说明依据。
3. 先做 period sweep，再选择 best period 或 best period set，然后把该 period 固定下来做 ablation。
4. ablation 要根据现有因子逻辑拆出可解释组件，每次去掉或简化一个组件，观察剩余效果。
5. refinement 必须从 `best period + core components` 出发，增强 core，而不是重造一个无关新因子。
6. 新产物集中放在因子目录内，通常是 `optimize_tests/`。
7. final variant 选出之前，不要覆盖 canonical factor code。只有用户要求推广时，才更新源码和顶层产物。
8. 最终必须明确说明：替换原因子、保留原因子、仅作为研究候选，还是需要更多验证。

## 产物契约

在因子目录内创建或复用这个结构：

```text
<factor_dir>/
└── optimize_tests/
    ├── 00_manifest.json
    ├── period_sweep/
    │   ├── period_sweep_metrics.csv
    │   └── period_sweep_summary.md
    ├── ablation/
    │   ├── ablation_metrics.csv
    │   ├── core_variant_daily_analyze.png
    │   └── ablation_summary.md
    ├── refinement/
    │   ├── refinement_metrics.csv
    │   ├── best_variant_daily_analyze.png
    │   └── refinement_summary.md
    └── optimize_report.md
```

If the project already has an equivalent experiment folder, reuse or extend it instead of creating a duplicate.

Optional helper:
可选初始化脚本：

```bash
python <skill_dir>/scripts/init_optimize_folder.py <factor_dir> \
  --factor-name <name> \
  --engine "<project engine note>" \
  --data "<project data note>"
```

## 对话回答契约

不要只告诉用户“已完成，报告在某文件”。即使完整报告已经写入 `optimize_tests/optimize_report.md`，最终对话回答也必须暴露足够多的信息，让用户不用打开所有文件也能理解结果。

最终回答至少包含：

- 本轮复用的评价口径：数据、label/target、频率、日期范围、核心指标。
- period sweep 结论：原始 period、测试范围、best period、是否是稳健区间。
- ablation 结论：core components、helpful/risk_control/cosmetic/harmful 组件。
- refinement 结论：best final variant 的具体逻辑，以及它相对 original/core 的主要变化。
- 简短指标对比：至少列出 `original_factor`、`best_period_factor`、`core_variant`、`best_final_variant` 的关键指标；如果没有完整数据，说明缺失原因。
- 因子稳健性讨论：参数稳健性、样本/市场/频率稳定性、换手和成本、覆盖度和分布、long/short 或分组收益是否有单侧问题、是否存在搜索过拟合。
- 最终建议：是否替换原因子，以及推荐下一步。

如果实验很多，对话里给压缩表，不要完整粘贴所有 CSV；但关键证据必须出现在对话里。

## 工作流

### 1. 读取本地上下文

设计实验前先检查因子目录：

- 源码和参数默认值
- metadata、README、FactorCard、notebook 或项目说明
- 现有 png、csv、parquet、json、metrics 和历史实验
- 能揭示评价习惯的同级脚本
- 数据、label/target、股票池/品种池、日期范围、频率、成本和执行假设

把选择的引擎、数据和指标口径写入 `optimize_tests/00_manifest.json`。

### 2. 选择指标

按这个顺序选择指标：

1. 用户指定指标。
2. 项目本地已经使用的指标。
3. 通用因子指标，并说明选择理由。

常见指标类型包括：

- 收益/PnL：累计收益、spread return、long/short 分解、分组收益
- 相关性：IC、Rank IC、ICIR、分 horizon IC
- 稳定性：rolling 指标、分年、分市场、分 regime
- 风险：Sharpe、回撤、波动、tail risk
- 成本：turnover、成本调整后收益
- 覆盖度和分布：有效样本覆盖、NaN 覆盖、信号分布、mode 集中度、极端值占比

period sweep、ablation、refinement 必须尽量使用同一套指标口径，方便最终表格串联比较。

### 3. Period Sweep

period sweep 是一次性测试多个 period 参数，用来检查参数稳健性。

如果因子只有一个核心 period：

- 先围绕当前 period 局部扫描
- 如果附近没有清晰结论，再适度扩大范围
- 优先稳健好区间，而不是单点最高值

如果因子包含多个 period：

- 先识别真正驱动因子逻辑的少数核心 period
- 优先测试核心 period
- 避免全量笛卡尔积导致组合数量爆炸
- 使用分阶段 sweep：先单参数扫描，再测试少量有意义组合

把所有 sweep 候选写入 `period_sweep/period_sweep_metrics.csv`，并在 `period_sweep/period_sweep_summary.md` 中解释 best period。

### 4. 选择 Best Period

best period 不是单指标最高的一行，而是综合权衡后的最好版本。

优先选择：

- 主指标表现强
- 相邻 period 表现不差，不是孤立尖峰
- turnover、风险、覆盖度和分布没有明显恶化
- 与原始因子逻辑一致、可解释
- 在用户关心的市场、频率和 horizon 上稳定

后续 ablation 必须固定在这个 best period 上做。

### 5. 在 Best Period 上做 Ablation

只有选出 best period 后才开始 ablation。

先把因子拆成可解释组件，例如：

- 趋势、反转、波动率、流动性、成交量或状态项
- 非线性 gate 和 filter
- 横截面或时序标准化
- 中性化、风险控制、行业、市值、合约或期限结构调整

保持 best period 固定，每次去掉或简化一个逻辑组件。组件重叠时，可以测试子组件、简化 gate 或只保留某一部分。最终迭代出 `core_variant`，它可能只是原始组件的一个子集。

把组件分类为：

- `core`：承载核心 alpha
- `helpful`：改善稳定性、风险或次要指标，但不是必要组件
- `risk_control`：以可接受 alpha 成本降低不良行为
- `cosmetic`：影响很小
- `harmful`：伤害因子效果

把 ablation 结果写入 `ablation/ablation_metrics.csv`，在 `ablation/ablation_summary.md` 中解释组件逻辑。除非项目要求，否则只给选出的 core variant 画图。

### 6. 从 Best Period + Core 出发做 Refinement

refinement 起点必须是：

```text
best period + core components
```

尝试增强 core 的变换：

- 组件权重调整
- 平滑、deadband、shrinkage、clipping、winsorization
- 标准化方式调整
- 当分解结果支持时，尝试 asymmetric、long-only、short-only 或单侧逻辑
- 在不破坏目标信号周期的前提下降低 turnover
- 有概念依据时增强 regime、confidence 或 extreme-state

非 winning variant 只保留 metrics。只给 best final variant 生成图。

如果某个 refinement 只改善单一指标，却明显破坏用户主指标、稳定性、成本、覆盖度、分布或 long/short 分解，不要把它作为最终版本。

### 7. 写最终报告

写入 `optimize_tests/optimize_report.md`。报告格式参考 `references/report-format.md`。

报告必须包含三张串联表：

1. period sweep 表：所有测试过的 period 或 period set。
2. ablation 表：best period 下所有组件删除/简化变体。
3. refinement 表：从 `best period + core` 出发的所有增强尝试。

然后给出最终决策：

- 用 best final variant 替换原因子
- 保留原因子
- best-period/core 版本仅作为研究候选
- 需要更多验证后再决定

## 稳健性讨论

报告和最终对话回答都必须简单讨论因子稳健性，至少覆盖：

- 参数稳健性：best period 是否来自连续好区间，还是孤立峰值。
- 时间稳健性：分年、rolling 或 train/validation/test 表现是否一致；如未测试，要说明缺口。
- 市场/截面稳健性：股票池、品种、行业、市值、合约或 regime 分解是否存在集中失效。
- 指标稳健性：主指标提升是否以 IC/收益、风险、换手、覆盖度或分布恶化为代价。
- 单侧稳健性：long/short、分组收益或多空 spread 是否由单侧贡献支撑。
- 搜索稳健性：period 组合数量、refinement 尝试数量是否可能带来选择偏误。

如果数据不足以判断某一项稳健性，不要跳过；明确写“未验证”和建议的下一步验证。

## 代码推广

只有用户同意后才推广 final variant。推广时同步更新源码、metadata、顶层图、因子产物、metrics、README、FactorCard 和项目 registry。

## 边界

本 skill 只提供研究工作流和实验组织，不提供市场数据，不保证未来收益，也不构成投资建议。见 `references/source-boundary.md`。
