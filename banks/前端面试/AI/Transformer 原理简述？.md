---
题目: "Transformer 原理简述？"
分类: AI
频率: 低频
id: 385e29bd-9121-8143-a6c4-da671a5ebe14
---
Transformer 基于自注意力（Self-Attention），核心组件：多头注意力 + 位置编码 + 残差连接 + LayerNorm + 前馈网络（FFN）；相比 RNN 可并行、能捕捉长距依赖，是 LLM 的基础。

## 发展史（问题 → 方案的链条）

**❓ RNN/LSTM 逐词顺序处理，训练没法并行，长距离依赖还会衰减**
序列模型（RNN/LSTM）必须按时间步顺序一步步算隐藏状态，后一步依赖前一步的结果：训练时序列维度没法并行，GPU 利用率低；早期信息要经过很多步才能传到后面的位置，距离越远衰减越严重（LSTM 只是缓解，没有根除）。

**✅ 2014，给 RNN 加上注意力机制（Attention）**
Bahdanau 等人在机器翻译里提出注意力机制（"Neural Machine Translation by Jointly Learning to Align and Translate"，2014）：解码器生成每个词时直接看编码器所有位置的隐藏状态、按相关性加权，不再只依赖一个固定长度的上下文向量。任意两个位置之间多了一条直接通道，长距离依赖问题缓解了不少。

**❓ 但底子还是 RNN，训练依然没法并行**
注意力只是加在 RNN 编码器-解码器上的附加模块，序列内部仍按时间步顺序展开计算，训练速度的瓶颈没解决。

**✅ 2017，《Attention Is All You Need》：干脆去掉循环结构，只用注意力**
Vaswani 等人（Google）提出 Transformer：完全抛弃循环结构，整个模型只用自注意力（self-attention）+ 前馈网络堆出来。自注意力直接计算序列内任意两个位置的相关度，不需要按步传递，序列维度可以整体并行；任意两个 token 之间的路径长度都是常数，不再随距离衰减。**取代 RNN 的这两大优势（可并行、长距依赖强）同源——都因为自注意力"顺序无关"**。

**❓ 去掉循环之后，模型不知道词的先后顺序了**
自注意力本质是对一整个集合算相关度，交换输入顺序结果不变（排列不变性）——这正是"顺序无关"的代价，丢失了序列该有的先后信息。

**✅ 加一份位置编码（Positional Encoding）**
论文用正弦/余弦函数生成一份位置编码，加到每个词的向量上，让模型能区分"谁在前谁在后"，补回自注意力本身对顺序不敏感的缺陷。

**❓ 一次注意力计算，只能捕捉一种关系视角**
单一一组 Query/Key/Value 权重，只能学到一种"相关性"的度量方式，可能不够同时捕捉句法、语义等不同类型的依赖关系。

**✅ 多头注意力（Multi-Head Attention）**
把 Q/K/V 投影到多个不同的子空间，并行做多组注意力计算再拼接，让模型能同时从不同的表示子空间捕捉不同类型的关系。

**❓ 层数一深，训练就不稳定**
自注意力 + 前馈网络一层层往深堆，容易出现梯度消失、训练不稳定。

**✅ 残差连接 + LayerNorm**
每个子层（注意力/前馈网络）的输出都是 `LayerNorm(x + Sublayer(x))`，残差连接让梯度能跨层直接传递，训练更深的网络也能稳定收敛。

**现状：原始 Transformer 是 encoder-decoder，后来分裂成三族，当今大模型以 decoder-only 为主**
2017 年的原始 Transformer 是给机器翻译设计的 encoder-decoder 结构。此后按用途分裂成三族：**encoder-only**（如 BERT，2018，偏理解/掩码语言建模）、**decoder-only**（如 GPT 系列，偏自回归生成）、**encoder-decoder**（如 T5，仍保留原始结构，做序列到序列任务）。**当今主流大模型（GPT、Claude、LLaMA 等）以 decoder-only 为主**。

## Q/K/V 是什么

每个词生成 Query（想找什么）/ Key（我是什么标签）/ Value（我的内容）；用 Q 与所有 K 算相似度得到关注权重，再加权汇总 V。类比「拿问题(Q)匹配每本书标签(K)，按匹配度读取内容(V)」。

## 参考资料

- [Bahdanau, Cho, Bengio — Neural Machine Translation by Jointly Learning to Align and Translate（2014，注意力机制的提出）](https://arxiv.org/abs/1409.0473)
- [Vaswani et al. — Attention Is All You Need（2017 原始论文）](https://arxiv.org/abs/1706.03762)
- [YouTube 视频讲解（用户推荐，含 self-attention/Transformer 系列课）](https://www.youtube.com/watch?v=ugWDIIOHtPA&list=PLJV_el3uVTsOK_ZK5L0Iv_EQoL1JefRL4&index=62)
