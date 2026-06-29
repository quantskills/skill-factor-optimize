# Portable Loader

本文件用于 Hermes、OpenClaw 或其他没有原生 skill 机制的 Agent/IDE。

## 加载顺序

1. 读取根目录 `SKILL.md`，把它作为主工作流指令。
2. 需要写完整报告时，读取 `references/report-format.md`。
3. 需要说明研究边界、数据边界或免责声明时，读取 `references/source-boundary.md`。
4. 如需初始化标准产物目录，运行：

```bash
python scripts/init_optimize_folder.py <factor_dir> \
  --factor-name <name> \
  --engine "<项目评价引擎说明>" \
  --data "<项目数据说明>" \
  --metrics "<用户指定或上下文推断的指标>"
```

## 任务触发

当用户给出已有因子目录、因子源码或已有 factor artifact，并要求：

- 优化因子
- 选择更好的 period
- 做组件消融
- 提炼 core variant
- 尝试 refinement
- 判断是否替换原因子

就应加载并执行 `SKILL.md`。

## 输出要求

Agent 需要同时输出文件产物和对话总结。

文件产物默认写入：

```text
<factor_dir>/optimize_tests/
```

最终对话回答必须包含：

- 本轮评价口径
- period sweep 结论
- ablation 结论
- refinement 结论
- 核心指标对比
- 因子稳健性讨论
- 是否替换原因子的建议

不要只回复“报告已生成”。
