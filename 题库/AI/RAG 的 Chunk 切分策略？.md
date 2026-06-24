---
题目: "RAG 的 Chunk 切分策略？"
分类: AI
频率: 高频
掌握: 
下次复习: 
上次评测: 
id: 385e29bd-9121-8199-bf1f-c67c0421a796
备注: ""
---
不能只按固定长度切。要点：

- 优先按标题层级/段落/语义边界切。
- 表格/代码/FAQ 特殊处理。
- Overlap（重叠 10–20%）保证边界上下文连续，过大会引入重复噪声。
- 保留父级标题与元数据（来源/页码/版本/权限）。

Chunk 太大召回不精、太小语义不全。

## 参考资料

- [JavaGuide — RAG 文档处理与切分策略](https://javaguide.cn/ai/rag/rag-document-processing.html)
