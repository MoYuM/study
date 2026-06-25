---
题目: "Transformer 原理简述？"
分类: AI
频率: 低频
id: 385e29bd-9121-8143-a6c4-da671a5ebe14
---
Transformer 基于自注意力（Self-Attention），核心组件：多头注意力 + 位置编码 + 残差连接 + LayerNorm + 前馈网络（FFN）；相比 RNN 可并行、能捕捉长距依赖，是 LLM 的基础。

- 自注意力：每个 token 按相关性动态关注序列中其他 token。
- 架构分三族：encoder-decoder（原始 2017 版 / T5）、encoder-only（BERT，偏理解）、decoder-only（GPT / Llama / Claude，偏生成）。**当今主流大模型以 decoder-only 为主**，「编码器-解码器」只适用于原始版与少数模型。

## 要点补充

- **取代 RNN 的两大优势**：① 可并行（自注意力让所有 token 同时计算，不像 RNN 必须按序）；② 长距依赖强（任意两 token 直接建立联系，距离再远不衰减）。两者同源——都因为「顺序无关」。
- **代价**：正因顺序无关，必须靠**位置编码**补回先后信息。
- **Q/K/V**：每个词生成 Query（想找什么）/ Key（我是什么标签）/ Value（我的内容）；用 Q 与所有 K 算相似度得到关注权重，再加权汇总 V。类比「拿问题(Q)匹配每本书标签(K)，按匹配度读取内容(V)」。

## 参考资料

- [YouTube 视频讲解（用户推荐，含 self-attention/Transformer 系列课）](https://www.youtube.com/watch?v=ugWDIIOHtPA&list=PLJV_el3uVTsOK_ZK5L0Iv_EQoL1JefRL4&index=62)
- [Attention Is All You Need（2017 原始论文）](https://arxiv.org/abs/1706.03762)
