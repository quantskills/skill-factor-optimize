# Factor Optimize

**简体中文** | [English](README.en.md)

> 一句话定位：对已有股票或期货因子做参数扫描、组件消融和核心版本增强，最后给出是否替换原因子的研究结论。

![type](https://img.shields.io/badge/type-agent--skill-blue)
![license](https://img.shields.io/badge/license-GPLv3-blue)

## 这是什么

`skill-factor-optimize` 是一个面向量化研究 Agent 的因子优化工作流 skill。它不从零挖因子，而是围绕一个已有因子，复用项目本地的数据、回测/评价引擎和指标口径，完成 period sweep、best period 选择、组件 ablation、core variant 提炼、refinement 增强和最终替换决策。

它适用于股票和期货因子。指标不写死，优先使用用户指定的 metrics；如果用户没有指定，则从项目上下文中推断，例如 IC、ICIR、PnL、Sharpe、turnover、coverage、分组收益或 long/short 分解。

本 skill 默认中文化：skill 指令、生成的 Markdown 总结、最终报告和对话回答都以中文为主。它还明确要求 Agent 不只把产物落到文件里，也要在对话中给出足够多的关键证据、指标对比、稳健性讨论和最终建议。

## 快速开始

```bash
cp -r skill-factor-optimize ~/.codex/skills/factor-optimize
```

触发示例：

```text
Use $factor-optimize to optimize this factor directory. Use the project's existing IC/ICIR and turnover metrics.
```

```text
Use $factor-optimize to sweep the key periods, run ablations on the best period, and tell me whether the refined version should replace the original factor.
```

## 目录结构

```text
skill-factor-optimize/
├── SKILL.md
├── README.md
├── README.en.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── references/
│   ├── report-format.md
│   └── source-boundary.md
└── scripts/
    └── init_optimize_folder.py
```

## 核心约束

| 约束 | 说明 |
| --- | --- |
| 复用本地引擎 | 优先使用项目已有数据、label、评价函数、回测脚本和报告格式 |
| 指标不写死 | 优先用户指定，其次根据上下文推断，再使用通用指标并说明原因 |
| 先 sweep 后 ablation | ablation 必须固定在 best period 上做 |
| 控制搜索空间 | 多 period 因子只测试核心参数，避免笛卡尔积爆炸 |
| 从 core 出发增强 | refinement 从 `best period + core components` 开始 |
| 不自动覆盖源码 | 只有用户确认推广最终版本时才更新 canonical factor code |
| 对话必须有信息量 | 最终回答必须包含关键指标对比、核心组件、best variant 和稳健性判断 |
| 讨论稳健性 | 至少覆盖参数、时间/市场、成本、覆盖度、单侧表现和搜索偏误 |

## 免责声明

本仓库仅作量化研究方法论与 Agent 工作流整理，不附带任何市场数据、因子数据或收益验证，不构成任何投资建议、交易信号或收益承诺。

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).

## PandaAI / QUANTSKILLS 社群

<div align="center">
  <img src="https://raw.githubusercontent.com/quantskills/.github/main/profile/assets/pandaai-community-qr.jpg" alt="PandaAI 社群二维码" width="220">
  <br>
  <sub>扫码加入 PandaAI 社群，交流 QUANTSKILLS 技能、Agent 工作流与量化研究实践。</sub>
</div>
