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

## 发展史（问题 → 方案的链条）

**❓ 2020 年 RAG 提出后，纯向量检索遇到精确匹配就翻车**
Lewis 等人（Meta）提出 RAG（"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"，2020）：用检索到的文档辅助大模型生成。但纯向量（embedding）检索靠语义相似度，遇到专有名词、型号、编号这类需要**精确匹配**的查询反而检索不到——语义相似不等于字面命中。

**✅ 混合检索（Hybrid Search）：关键词 + 向量两路并行，用 RRF 融合**
经典关键词检索 **BM25**（源自 1994 年 Okapi 系统，Robertson 等人）按词频/逆文档频率打分，擅长精确匹配术语；向量检索擅长语义近似。两路各自检索后，用 **RRF（Reciprocal Rank Fusion，Cormack, Clarke & Buettcher, SIGIR 2009）** 按名次倒数求和融合——不需要归一化两路分数量纲不同的问题，直接解决了"单一检索各有盲区"。

**❓ 检索能力再强，用户输入本身模糊/省略/多意图，检索目标从一开始就错了**
"它的生命周期是啥"这种口语化省略指代、"对比 MySQL 和 Redis"这种多意图查询，直接拿去检索，两路检索（哪怕融合了）也救不回来——问题本身没问对。

**✅ Query Rewrite：检索前先把「烂问题」改写成「好问题」**
除了补全指代、拆分多意图，**HyDE**（Gao, Ma, Lin & Callan，"Precise Zero-Shot Dense Retrieval without Relevance Labels"，2022）是代表性技术：先让大模型生成一个「假设性答案」，再用这个假答案去做 embedding 检索——假答案的表达方式比原始问题更接近真实文档，检索命中率更高。

**❓ 检索和改写都做好了，向量检索的排序依然不够准**
向量检索用的是 **Bi-encoder**：query 和文档各自独立编码成向量，再算余弦相似度——两者从未"见过彼此"，算得快，但"向量相似"不等于"内容真正相关"。

**✅ Rerank：用 Cross-encoder 对少量候选做精排**
Nogueira & Cho（"Passage Re-ranking with BERT"，2019）开创了检索-精排两阶段范式：**Cross-encoder** 把 query 和文档拼在一起联合编码打分，能建模两者之间的真实交互，精度远高于 Bi-encoder，但计算量大、慢——所以只对 Bi-encoder 召回的少量候选（如 top-100）做精排，选出 top-5 送给大模型，兼顾速度与精度。

**现状：三级链路分工明确，Bi-encoder 与 Cross-encoder 是最容易记混的一对**
Query Rewrite 管入口（修问题）→ Hybrid Search 管召回（两路兼顾，广）→ Rerank 管排序（精）。其中 **Bi-encoder**（向量检索阶段用，query/文档独立编码，快但只是"粗筛"）与 **Cross-encoder**（Rerank 阶段用，query+文档联合编码，慢但精）最容易混淆——判断依据就一句话：**两者是否"见过彼此"**（是否联合编码）。

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
- [Lewis et al. — Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks（2020，原始 RAG 论文，arXiv 2005.11401）](https://arxiv.org/abs/2005.11401)
- [Cormack, Clarke & Buettcher — Reciprocal Rank Fusion outperforms Condorcet and Individual Rank Learning Methods（SIGIR 2009，RRF 原论文）](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf)
- [Gao, Ma, Lin & Callan — Precise Zero-Shot Dense Retrieval without Relevance Labels（2022，HyDE 原论文，arXiv 2212.10496）](https://arxiv.org/abs/2212.10496)
- [Nogueira & Cho — Passage Re-ranking with BERT（2019，Cross-encoder 精排范式，arXiv 1901.04085）](https://arxiv.org/abs/1901.04085)
