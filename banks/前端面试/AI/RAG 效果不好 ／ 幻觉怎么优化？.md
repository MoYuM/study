---
题目: "RAG 效果不好 / 幻觉怎么优化？"
分类: AI
频率: 高频
id: 385e29bd-9121-8132-ab9b-e86cc25500ff
---
先分段排查问题出在哪一段：文档解析 → Chunk → Embedding → 召回 → 排序 → 上下文 → 生成。

手段：Hybrid Search（BM25+向量）、Query Rewrite/HyDE、Rerank、调 chunk 大小与 overlap、补充元数据、生成阶段加「仅基于参考内容回答 / 要求引用来源 / 允许说不知道」边界提示。优化必须先建失败样本集，别凭感觉调 Prompt。

注意：HyDE（用 LLM 生成假设文档再检索）能提升召回，但在精确数值 / 金融等场景可能引入噪声，宜与 BM25 混合使用，而非无条件降幻觉。

## 追问：怎么判断是检索失败还是生成幻觉？

把实际召回、拼进 prompt 的 chunk 内容打印出来，人工核对一遍：

- **chunk 里压根没有能回答这个问题的信息** → 检索阶段的问题，往 chunk 切分、embedding 模型、hybrid search、rerank 这条线调。
- **chunk 里明明有正确答案，但模型的回答跟这些内容对不上、甚至编造了 chunk 里没有的细节** → 生成阶段的幻觉，往 prompt 加约束（"仅基于参考内容回答"）、要求引用来源、允许模型说"不知道"这条线调。

不看中间产物、只凭最终答案对不对就去调参数，是最容易调错方向的误区。

## 发展史（问题 → 方案的链条）

**❓ Naive RAG（Lewis et al. 2020 论文提出的最初范式）直接把检索到的内容拼给模型生成，实际落地后效果经常不稳定，但开发者分不清问题该往检索这边修还是往生成这边修**
最终用户只能看到"答案对不对"，看不到中间到底发生了什么。

**✅ 检索侧最先暴露的问题：纯向量语义检索对专业名词/型号/精确数值这类需要"字面匹配"的内容不敏感——业界把信息检索领域的老思路搬过来做 Hybrid Search。融合算法 Reciprocal Rank Fusion（RRF，Cormack/Clarke/Büttcher 2009 年 SIGIR 论文）比 RAG 概念早了十多年，Elasticsearch/Weaviate/Pinecone/Vespa 等厂商在 2022–2023 年 RAG 兴起后陆续把它接入自家产品——没有单一"首创者"，是老技术的复用**
专业名词/编号交给 BM25 兜底，语义相关但字面不同的内容交给向量检索，两路结果再融合。

**❓ 用户输入的原始问题往往口语化、信息不完整，直接拿原始问题去检索命中率不高**
需要在检索前先把问题改写成更贴近答案语义的形式。

**✅ HyDE（Gao/Ma/Lin/Callan，2022 年 12 月论文《Precise Zero-Shot Dense Retrieval without Relevance Labels》，arXiv:2212.10496）：让 LLM 先生成一段"假设性答案"，再用这段假设文档去做向量检索**
假设文档的语义比一个简短问题更贴近真实答案文档的分布，检索命中率通常更高——但生成的假设内容可能带偏，在精确数值/金融等场景需要和 BM25 搭配而非单独使用。

**❓ 粗排（向量相似度/BM25 分数）得出的候选列表未必是真正最相关的排序**
需要一个更精细的二次排序步骤。

**✅ Cross-encoder 重排序：把问题和每个候选 chunk 一起送进模型算相关性分数，Cohere 于 2023 年 5 月推出的 Rerank API 是这类"重排序即服务"产品里较早、有代表性的一个**
cross-encoder 比向量相似度更精确（能看到问题和文档的交互），但计算成本更高，所以放在粗排之后只对少量候选做精排。

**❓ 即便用了这些手段，效果还是不稳定时，"人工感觉答案不对"这种评估方式没法说清楚问题到底出在检索还是生成——这正是这道题最容易卡住的地方**
需要把"检索质量"和"生成质量"拆成两组独立可衡量的指标。

**✅ Ragas（Shahul Es 等人，2023 年 9 月论文《Ragas: Automated Evaluation of Retrieval Augmented Generation》，arXiv:2309.15217）：把 RAG 系统的评估拆解成 Faithfulness（忠实度，衡量生成内容是否基于检索到的上下文，对应"生成幻觉"）和 Context Precision/Recall（上下文精确率/召回率，衡量检索到的内容是否真的相关，对应"检索失败"）等独立指标**
第一次把"感觉答案不对"变成"哪个阶段的哪个具体指标不达标"——这正是"怎么判断是检索失败还是生成幻觉"这个问题的历史答案：业界最终是靠专门的评估框架把两件事拆开量化，而不是靠人工猜。

**现状：没有一招治好幻觉的银弹——Hybrid Search（老 IR 技术复用，解决字面匹配）+ HyDE（改写查询，解决语义鸿沟）+ Rerank（精排，解决排序不准）三类手段各自解决检索链路上不同的子问题；诊断问题该往哪个方向调，靠 Ragas 这类框架把"检索质量"和"生成质量"拆成独立指标，而不是凭感觉**

## 参考资料

- [RAG 论文（arXiv:2005.11401）](https://arxiv.org/abs/2005.11401)
- [Reciprocal Rank Fusion — Cormack/Clarke/Büttcher, SIGIR 2009](https://research.google/pubs/reciprocal-rank-fusion-outperforms-condorcet-and-individual-rank-learning-methods/)
- [HyDE 论文（arXiv:2212.10496）](https://arxiv.org/abs/2212.10496)
- [Cohere — Introducing Rerank（2023-05）](https://cohere.com/blog/rerank)
- [Ragas 论文（arXiv:2309.15217）](https://arxiv.org/abs/2309.15217)
