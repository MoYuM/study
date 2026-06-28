---
题目: "Hybrid Search / Query Rewrite / Rerank 各解决什么？"
分类: AI
频率: 高频
id: 385e29bd-9121-81fa-98c6-eb412c25fcee
---
**锚点：Rewrite 管入口 / Hybrid 管召回 / Rerank 管排序**

```
用户提问
  ↓  Query Rewrite  — 把「烂问题」改成「好问题」
  ↓  Hybrid Search  — 两路检索，召回全面
  ↓  Rerank         — 精排，排序精准
  ↓  大模型生成答案
```

## Hybrid Search

**解决**：单一检索各有盲区——纯向量不擅长精确术语，纯关键词没有语义理解。

- **BM25（关键词）**：按词频/逆文档频率打分，精确匹配术语、型号、编号、专有名词
- **向量（语义）**：embedding 余弦相似度，理解同义词和近义表达
- **融合**：两路各自检索，用 RRF（Reciprocal Rank Fusion）合并——按名次倒数求和，不需要归一化两路分数

```
score(doc) = Σ 1 / (k + rank_in_list_i)
```

## Query Rewrite

**解决**：用户输入质量差（口语化/省略/多意图/缩写），直接检索效果差。

| 问题类型 | 例子 | 处理方式 |
|------|------|------|
| 口语化/省略 | "它的生命周期是啥" | 补全指代 → "React 组件的生命周期" |
| 多意图 | "对比 MySQL 和 Redis" | 拆成多个子查询分别检索 |
| HyDE | 问题抽象难检索 | 先生成假答案，用假答案 embedding 检索 |
| Self-Query | "2024 年后的 RAG 论文" | 提取结构化过滤条件 `{ 时间: ">2024" }` |

## Rerank

**解决**：向量相似 ≠ 真正相关（Bi-encoder 的 query 和文档从未「见过彼此」）。

- **Bi-encoder**（向量检索）：query 和文档各自编码，余弦相似度打分，快但精度有限
- **Cross-encoder**（Rerank）：把 query + 文档拼在一起联合打分，精度高但慢

两阶段策略：
```
全量文档 → Bi-encoder 快速召回 top-100 → Cross-encoder 精排 top-5 → 送大模型
```

Cross-encoder 只对少量候选运行，性能可接受。

## 参考资料

- [JavaGuide — 万字详解 RAG 检索优化](https://javaguide.cn/ai/rag/rag-optimization.html)
