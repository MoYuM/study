---
题目: "什么是 Agent Loop / ReAct？"
分类: AI
频率: 高频
id: 385e29bd-9121-816a-8c36-ebe396b3fd97
---
Agent 以「推理→行动→观察→修正」闭环执行任务。

- ReAct = Reasoning + Acting，循环：Thought（思考）→ Action（调用工具）→ Observation（获取结果）→ 重复直到完成。
- 与单次调用区别：有反馈闭环与工具调用，能根据观察修正。
- **为何 Observation 能纠错**：它把行动的真实后果喂回模型上下文，模型才能基于现实（而非假设）调整下一步——没有观察 = 闭眼做事，错了也不知道。
- 生产需要：退出条件、步数/超时限制、错误恢复、可观测与任务状态管理。

## 出处与参考

ReAct 概念出自 2022 年 10 月普林斯顿 + Google 的论文（Yao et al.），后被 LangChain / LangGraph 等框架做成默认 agent 模式——很多人用过其实现却没听过这个名字。

- [ReAct: Synergizing Reasoning and Acting in Language Models（原论文 arXiv 2210.03629）](https://arxiv.org/abs/2210.03629) —— 用「调 Wikipedia API 答题」证明：光推理(CoT)会幻觉、光行动没规划，二者交织才靠谱。
- [官方项目主页 react-lm.github.io](https://react-lm.github.io/) —— 有 Thought/Action/Observation 交织的轨迹示例，最直观，适合入门。
- [Prompt Engineering Guide — ReAct](https://www.promptingguide.ai/techniques/react) —— 带代码的工程视角，讲怎么写 ReAct prompt。
