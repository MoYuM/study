---
题目: "什么是 Lost in the Middle？怎么缓解？"
分类: AI
频率: 低频
id: 385e29bd-9121-8171-9612-dd3a8da54158
---
Lost in the Middle：长上下文中，模型对「中间位置」的信息利用率明显低于头尾。

缓解：把最相关证据放到上下文首/尾；控制上下文长度与 Top-K；Rerank 后只送少量高质片段；必要时分段总结再汇总。

## 出处

现象来自斯坦福团队 2023 年的论文《Lost in the Middle: How Language Models Use Long Contexts》（Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang；arXiv:2307.03172，2024 年发表于 TACL）。论文用多文档问答和键值检索两个任务测试发现：相关信息放在输入上下文的**开头或结尾**时模型表现最好，放在**中间**时表现明显下降——即使是号称支持长上下文的模型也存在这个问题，说明模型并不能均匀地利用长输入里的每一部分信息。

## 参考资料

- [Lost in the Middle: How Language Models Use Long Contexts — arXiv:2307.03172](https://arxiv.org/abs/2307.03172)
- [GitHub — nelson-liu/lost-in-the-middle（论文代码与数据）](https://github.com/nelson-liu/lost-in-the-middle)
