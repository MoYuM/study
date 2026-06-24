---
题目: "Hybrid Search / Query Rewrite / Rerank 各解决什么？"
分类: AI
频率: 高频
id: 385e29bd-9121-81fa-98c6-eb412c25fcee
---
- Hybrid Search：BM25（关键词）+ 向量（语义）融合，适合专业术语/编号/实体名与语义混杂场景。
- Query Rewrite：解决用户问题口语化/多意图/缩写/上下文省略（HyDE/Self-Query）。
- Rerank：在候选里重排，解决「向量相似≠答案相关」。

三者组合提升召回与排序质量。

## 参考资料

- [JavaGuide — 万字详解 RAG 检索优化](https://javaguide.cn/ai/rag/rag-optimization.html)
