---
题目: "AI 应用的性能监控指标有哪些？"
分类: AI
频率: 高频
id: 385e29bd-9121-81ef-b907-fc0bc80302f3
---
- **延迟**：首字延迟 TTFT（Time To First Token）、Token 生成速度 TPOT（tokens/s）、整体响应时延——流式场景必须把 TTFT 和整体速度拆开看，二者体现的是不同体验（"多久开始出字」vs「出字快不快"）。
- **可靠性**：失败率 / 重试率 / 流中断率（SSE abort 监听）。
- **成本**：Token 消耗与价格、并发连接数。
- **质量**：幻觉率（回答是否编造事实）、用户反馈率（点赞/点踩）——这块通常靠人工标注或 LLM-as-judge 评估，LangSmith/Langfuse/Arize Phoenix 等主流 LLM 可观测性工具都把它作为独立维度追踪，不像前三块能靠纯埋点直接拿到数字。

前端通过埋点采集延迟/可靠性/成本三块指标并上报，用于体验优化与告警；质量维度通常需要额外接入评估流程（人工标注队列或 LLM-as-judge），不是简单埋点能覆盖的。

## 参考资料

- [LLM Observability Tools: Weights & Biases, Langsmith — aimultiple](https://aimultiple.com/llm-observability)
- [Langfuse vs LangSmith: Which Observability Platform Fits Your LLM Stack? — ZenML Blog](https://www.zenml.io/blog/langfuse-vs-langsmith)
