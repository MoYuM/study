---
题目: "AI 应用怎么做评测（Golden Set / LLM-as-Judge）？"
分类: AI
频率: 低频
id: 385e29bd-9121-81c3-8a19-d95bbc52eca7
---
- 不能只靠公开 benchmark（不代表你的业务分布）。
- Golden Set：覆盖正常/边缘/对抗/高权重失败样本，重分布而非重数量。
- LLM-as-Judge：提效但有位置/冗长/同源偏差，不能完全替代人工。
- RAG/Agent 要分段评测；配合离线评测 + Trace 回放 + 线上灰度。
