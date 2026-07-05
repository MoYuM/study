---
题目: "什么是 Agent Loop / ReAct？"
分类: AI
频率: 高频
id: 385e29bd-9121-816a-8c36-ebe396b3fd97
---
Agent 以「推理→行动→观察→修正」闭环执行任务。

## 发展史（问题 → 方案的链条）

**❓ 大模型单次调用只能靠内部知识回答，容易幻觉，也没法自我纠错**
问一句答一句的单次调用，模型只能依赖训练时记住的（可能过时或错误的）知识生成答案，没有办法核实、没有反馈，说错了也不知道。

**✅ 2022 年 1 月，Chain-of-Thought：先让模型把推理过程写出来**
Wei 等人（Google）提出思维链提示（"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"，2022）：让模型在给出最终答案前先展开中间推理步骤，显著提升了复杂推理任务的准确率。

**❓ 但 CoT 依然只是"想得更清楚"，没法接触真实世界**
思维链只是让模型把内部知识想得更透彻，本质上还是闭眼做事——如果模型的内部知识本身就是错的或过时的，推理链条再清晰也纠正不了，无法查证、无法获取新信息。

**✅ 2022 年 10 月，ReAct：把推理和行动交织起来，加入真实反馈**
Yao 等人（普林斯顿 + Google）提出 ReAct（"ReAct: Synergizing Reasoning and Acting in Language Models"，2022）：循环执行 **Thought**（思考下一步做什么）→ **Action**（调用外部工具，如搜索/API）→ **Observation**（拿到工具返回的真实结果，喂回模型上下文）→ 重复直到完成。论文用"调 Wikipedia API 答题"的实验证明：光推理（CoT）会幻觉、光行动没规划，二者交织才靠谱——**Observation 之所以能纠错，是因为它把行动的真实后果喂回了模型上下文，模型才能基于现实而非假设调整下一步**。

**❓ 循环没有边界，投入生产会出问题**
Thought→Action→Observation 可以一直循环下去，但生产环境里这意味着风险：模型可能陷入死循环、调用出错没人处理、成本失控、也不知道现在跑到哪一步了。

**✅ 工程框架补上退出条件、步数限制、错误恢复、可观测性**
LangChain / LangGraph 等框架把 ReAct 循环包装成默认的 agent 执行模式，围绕它加上退出条件（模型自己判断"完成"或触发终止动作）、步数/超时上限、工具调用失败后的错误恢复、以及任务状态的可观测记录，让这个循环能安全地跑在生产环境里。

**现状：ReAct 式循环是当今 LLM Agent 的默认执行模型**
Thought→Action→Observation 的交织循环，已经是绝大多数编程助手、研究助手等 LLM Agent 系统的执行底座——很多人每天在用其实现，却未必知道这个名字。

## 参考资料

- [Wei et al. — Chain-of-Thought Prompting Elicits Reasoning in Large Language Models（2022，arXiv 2201.11903）](https://arxiv.org/abs/2201.11903)
- [Yao et al. — ReAct: Synergizing Reasoning and Acting in Language Models（原论文 arXiv 2210.03629）](https://arxiv.org/abs/2210.03629)
- [官方项目主页 react-lm.github.io](https://react-lm.github.io/) —— 有 Thought/Action/Observation 交织的轨迹示例，最直观，适合入门。
- [Prompt Engineering Guide — ReAct](https://www.promptingguide.ai/techniques/react) —— 带代码的工程视角，讲怎么写 ReAct prompt。
