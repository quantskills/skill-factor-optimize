# 报告格式

写 `optimize_tests/optimize_report.md` 时使用这个格式。

## 必要章节

1. 原始因子
   - 因子名和源码路径
   - 原始 period 参数
   - 用自然语言解释原始因子逻辑
   - 评价引擎、数据、股票池/品种池、日期范围、频率、label/target 和成本假设
   - 本轮选择的指标和选择理由

2. Period Sweep
   - 所有测试过的 period 或 period set 表
   - 稳健可用区间
   - 原始 period 的位置或排名
   - 选择的 best period 及理由
   - 是否存在孤立峰值、组合搜索过大或选择偏误

3. Ablation
   - 所有组件删除/简化变体表
   - 固定使用的 best period
   - 组件分类：`core`、`helpful`、`risk_control`、`cosmetic`、`harmful`
   - 最终 core variant 及其理由

4. Refinement
   - 所有从 `best period + core` 出发的变体表
   - 每个候选的变换逻辑
   - best final variant 及其胜出或失败原因

5. 稳健性讨论
   - 参数稳健性：best period 是否处在连续好区间
   - 时间稳健性：分年、rolling、train/validation/test 是否稳定
   - 市场/截面稳健性：股票池、品种、行业、市值、合约、regime 是否集中失效
   - 指标稳健性：主指标改善是否伴随风险、成本、覆盖度或分布恶化
   - 单侧稳健性：long/short 或分组收益是否过度依赖一侧
   - 搜索稳健性：是否存在 period/refinement 搜索空间过大的选择偏误
   - 若某项未验证，明确写出“未验证”和建议补测方式

6. 最终决策
   - 推荐动作：替换、保留、研究候选、继续验证
   - 如果推荐替换，给出准确代码变更
   - 残余风险：稳定性、换手、覆盖度、分布、单侧分解、regime 敏感性、搜索偏误

## 表格模板

Period sweep 表：

```text
变体名, period参数, 变体逻辑, metrics..., 备注
```

Ablation 表：

```text
变体名, 固定period, 删除组件, 保留组件, 变体逻辑, metrics..., 结论
```

Refinement 表：

```text
变体名, 基准变体, period参数, refinement逻辑, metrics..., 结论
```

把 `metrics...` 替换成用户指定或项目上下文推断出的指标，例如 IC、ICIR、PnL、Sharpe、turnover、coverage、分组收益、long/short 分解。

## 对话回答模板

最终对话回答不能只指向报告文件。建议使用这个结构：

```text
完成了。本轮复用的评价口径是：...

关键结论：
- Best period: ...
- Core components: ...
- Best final variant: ...
- 是否建议替换：...

核心指标对比：
| 版本 | period | 逻辑 | 指标1 | 指标2 | 指标3 | 结论 |
| --- | --- | --- | --- | --- | --- | --- |
| original_factor | ... | ... | ... | ... | ... | ... |
| best_period_factor | ... | ... | ... | ... | ... | ... |
| core_variant | ... | ... | ... | ... | ... | ... |
| best_final_variant | ... | ... | ... | ... | ... | ... |

稳健性判断：
- 参数稳健性：...
- 时间/市场稳健性：...
- 成本和覆盖度：...
- 单侧/分组表现：...
- 搜索偏误风险：...

产物位置：...
```

如果指标很多，只展示最能支撑结论的核心指标，并说明完整表格在报告和 CSV 中。

## 决策建议

只有满足这些条件时，才建议替换：

- 主指标整体改善或明显更优
- 次要指标没有明显恶化
- 改善得到 ablation 支撑，而不是只来自大量搜索
- turnover、coverage、风险和分布可接受
- 单侧、horizon、市场或 regime 分解没有暴露严重隐藏问题

出现这些情况时，不建议替换：

- 改善只存在于单一指标或单一样本切片
- period 表现是孤立峰值
- refinement 脱离 core 逻辑
- 交易成本、覆盖度或稳定性明显恶化
- ablation 不支持最终逻辑
