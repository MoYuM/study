---
题目: "RAG 的向量索引（Flat/HNSW/IVF）怎么选？"
分类: AI
频率: 低频
id: 385e29bd-9121-8132-8051-de6159b17dac
---
- Flat：暴力精确，适合小规模/评测基准。
- HNSW：图索引，查询快、召回高，但内存占用大；ef_search 调大提召回降速度。
- IVFFLAT/IVF-PQ：聚类分桁 + （PQ 压缩），省内存、适合大规模，需训练与调参。

ANN 牺牲一点精确换高查询性能。按规模/延迟/内存选型。

## 发展史（问题 → 方案的链条）

❓ 最原始的做法：查询向量来了，跟库里每一个向量都算一遍距离，排序取最近的几个——这就是 **Flat**（暴力搜索）。
✅ 100% 精确，但数据量一大，每次查询都要扫全量，延迟线性增长，扛不住大规模场景。

❓ "倒排索引"（inverted index）是经典信息检索（搜索引擎）里的老技术——不用扫全部文档，先把文档按关键词分桶，查询时只看相关的桶。这个思路能不能搬到向量检索上？
✅ **IVF**（Inverted File Index）把这个思路搬了过来：先用聚类算法（如 K-means）把向量空间分成若干"桶"，查询时先定位到最相近的几个桶，只在桶内搜索，不用扫全库。代价是需要预先训练聚类中心、调参（分几个桶、查几个桶），召回率也不是 100%。

❓ IVF 靠"分桶跳过大部分数据"提速，但桶的边界是提前固定的，查询点如果刚好在桶边界上，容易漏掉桶外其实很近的点。有没有更精细的组织方式？
✅ 2016 年，Yury Malkov 和 Dmitry Yashunin 提出 **HNSW**（Hierarchical Navigable Small World，分层可导航小世界图）——把所有向量组织成一个多层图结构，查询时从顶层稀疏图快速定位大致方向，逐层下探到底层稠密图精确查找，复杂度接近对数级。论文 2018 年发表在 IEEE TPAMI，是目前查询速度和召回率综合表现最好的方案之一，代价是要为每个向量存图的连接关系，内存占用比 IVF 大。

**现状对比**：三者是"精确度 vs 速度 vs 内存"这个三角权衡上的三个不同取舍点——Flat 不省时间但 100% 准；IVF 靠经典倒排索引思路省时间和内存，但精度和调参成本换来的；HNSW 用图结构换到了目前最好的速度/召回综合表现，代价是内存。选型口诀：**数据小要精确用 Flat，有内存预算要速度用 HNSW，数据量巨大要省内存用 IVF**。

## 参考资料

- [Efficient and robust approximate nearest neighbor search using HNSW graphs — Malkov & Yashunin](https://arxiv.org/pdf/1603.09320)
- [IVF (Inverted File Index) Explained](https://theaidatabaseblog.com/learn/ivf/)
- [Approximate Nearest Neighbor (ANN) Search Explained: IVF vs HNSW vs PQ — TiDB](https://www.pingcap.com/article/approximate-nearest-neighbor-ann-search-explained-ivf-vs-hnsw-vs-pq/)
