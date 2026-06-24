---
题目: "什么是 Agent Loop / ReAct？"
分类: AI
频率: 高频
id: 385e29bd-9121-816a-8c36-ebe396b3fd97
---
Agent 以「推理→行动→观察→修正」闭环执行任务。

- ReAct = Reasoning + Acting，循环：Thought（思考）→ Action（调用工具）→ Observation（获取结果）→ 重复直到完成。
- 与单次调用区别：有反馈闭环与工具调用，能根据观察修正。
- 生产需要：退出条件、步数/超时限制、错误恢复、可观测与任务状态管理。
