---
题目: "RAG 的 Chunk 切分策略？"
分类: AI
频率: 高频
id: 385e29bd-9121-8199-bf1f-c67c0421a796
---
不能只按固定长度切。要点：

- 优先按标题层级/段落/语义边界切。
- 表格/代码/FAQ 特殊处理。
- Overlap（重叠 10–20%）保证边界上下文连续，过大会引入重复噪声。
- 保留父级标题与元数据（来源/页码/版本/权限）。

Chunk 太大召回不精、太小语义不全。

## 发展史（问题 → 方案的链条）

**❓ LLM 的知识在训练时就被冻结、无法访问私有或更新的文档，且知识库通常大到没法在每次调用时整篇塞进上下文——这是 2020 年前后知识密集型 NLP 任务共同面对的问题**
早期开放域问答系统（如 Stanford 与 Facebook AI Research 合作的 DrQA，ACL 2017）已经用"先检索、再阅读"的两阶段思路处理类似问题——用 TF-IDF 检索出相关维基百科段落，再在段落上做抽取式阅读理解，检索粒度已经是段落而非整篇文档；但这套思路还局限在抽取式 QA，没有和生成式模型结合起来。

**✅ RAG（Retrieval-Augmented Generation）：Patrick Lewis 等人（Facebook AI Research / UCL / NYU 联合署名，arXiv 2005.11401，2020 年 5 月）正式提出这个术语和范式**
把"参数化记忆"（LLM 权重里的知识）和"非参数化记忆"（外部可检索的文档库）结合起来——检索出相关段落，拼进生成模型的输入里再生成答案，知识库更新了不用重新训练模型。

**❓ 落地到真实业务文档（网页/PDF/Word）后，如果只按固定字符数切，经常把一句话、一个表格从中间切断，读不通顺也检索不准**
工程落地到 LangChain（2022 年 10 月创建）、LlamaIndex（原 GPT Index，Jerry Liu 创建，2022 年 11 月）这些框架后，开发者发现最朴素的定长切分（每 N 个字符切一刀）常在语义边界中间切断内容。

**✅ 递归式/语义边界切分：LangChain 的 `RecursiveCharacterTextSplitter`（2023 年 1 月合并）**
按分隔符优先级递归切分——先尝试按段落切，切完还超长再按句子切，句子还超长才退化到定长切断，尽量让每个 chunk 落在语义边界上。

**❓ 即使切得很干净，chunk 切得越小、检索越精准，但小 chunk 单独拿出来常常丢失了它所在的上下文，模型看到一句孤立的话可能看不懂在说什么——精度和完整性成了一对矛盾**
"切得准"这一步没有解决"切出来的碎片读不懂"这个新问题。

**✅ 父子/由小到大检索：LlamaIndex 的 AutoMergingRetriever（2023 年 8 月合并）+ Sentence Window Retrieval（同期，2023 年下半年推出，同年 12 月被打包成官方 LlamaPack 集中推广）**
检索时用小 chunk 保证精准命中，但真正喂给 LLM 的是这个小 chunk 所在的父块/更大窗口的上下文——"检索单元"和"喂给模型的单元"被拆成两个不同粒度。

**❓ 父子合并解决了"检索到的内容读不懂"，但没解决另一个问题：一个孤立的 chunk 做 embedding 时依然不知道自己的"全局背景"（比如一句"该公司营收增长了 3%"，不知道是哪家公司、哪个季度，embedding 出来的语义仍然模糊）**
chunk 内部文字本身可能压根没提到它所属的公司名/章节标题，检索时这类 chunk 容易被匹配错或匹配不到。

**✅ Contextual Retrieval：Anthropic 官方博客（2024 年 9 月 19 日）提出用 LLM 给每个 chunk 生成一段解释性上下文**
在切分之后、embedding 之前，先用 LLM 读一遍"chunk + 它所在的整篇文档"，生成一段 50-100 token 的说明文字（这个 chunk 属于什么背景），拼接到 chunk 前面再做 embedding 和 BM25 索引——官方数据显示能让检索失败率降低 49%（配合重排序可达 67%）。

**现状：切分要解决的问题一直没变（让检索更精准），但"怎么保证被切碎的内容仍然语义完整"这套手段一直在加码——从「定长切」→「按语义边界递归切」→「小 chunk 检索、大上下文喂给模型」→「给每个 chunk 补一段上下文再索引」，是同一问题的层层递进，不是互相替代的对立方案**

## 参考资料

- [JavaGuide — RAG 文档处理与切分策略](https://javaguide.cn/ai/rag/rag-document-processing.html)
- [RAG 论文（arXiv:2005.11401）](https://arxiv.org/abs/2005.11401)
- [DrQA 论文（Reading Wikipedia to Answer Open-Domain Questions）](https://github.com/facebookresearch/DrQA)
- [LangChain RecursiveCharacterTextSplitter 引入 PR](https://github.com/langchain-ai/langchain/pull/530)
- [LlamaIndex AutoMergingRetriever 引入 commit](https://github.com/run-llama/llama_index/commit/28e5fadbeb28700fe4ff561b4b194f1a596eab69)
- [Anthropic — Introducing Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval)
