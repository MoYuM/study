---
题目: "Transformer 原理简述？"
分类: AI
频率: 低频
id: 385e29bd-9121-8143-a6c4-da671a5ebe14
---
Transformer 基于自注意力（Self-Attention），核心组件：多头注意力 + 位置编码 + 残差连接 + LayerNorm + 前馈网络（FFN）；相比 RNN 可并行、能捕捉长距依赖，是 LLM 的基础。

- 自注意力：每个 token 按相关性动态关注序列中其他 token。
- 架构分三族：encoder-decoder（原始 2017 版 / T5）、encoder-only（BERT，偏理解）、decoder-only（GPT / Llama / Claude，偏生成）。**当今主流大模型以 decoder-only 为主**，「编码器-解码器」只适用于原始版与少数模型。
