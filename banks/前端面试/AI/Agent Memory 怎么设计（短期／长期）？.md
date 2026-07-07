---
题目: "Agent Memory 怎么设计（短期/长期）？"
分类: AI
频率: 高频
id: 385e29bd-9121-813e-b1cf-ed51532db25a
---
分层设计：

- 工作记忆：当前任务轨迹与关键中间结果。
- 会话记忆：滚动摘要，避免上下文过长。
- 长期记忆：向量检索 / 结构化库存历史与偏好。

写入要点：区分「事实」与「推断」、带时间戳与来源、可更新可撤销；读取时按任务检索相关记忆而非全量注入；冲突时新信息（带时间戳）优先。

## 发展史（问题 → 方案的链条）

**❓ 早期 LLM 对话（如 2022 年 11 月 ChatGPT 刚上线时）只有一个固定大小的上下文窗口，对话变长就会超出窗口**
最简单粗暴的做法是"上下文塞满了就砍掉最早的消息"（截断），这样会丢掉早期可能重要的信息。

**✅ 滚动摘要压缩：LangChain（Harrison Chase 2022 年 10 月创建）较早把这个模式做成工程抽象，如 ConversationSummaryMemory**
每轮对话后用 LLM 生成/更新一份滚动摘要，传给主模型时用摘要代替逐字保存的完整历史，在保留大意的同时腾出上下文空间。

**❓ 会话级摘要只能解决"这次对话"内的问题，没法让 Agent 记住跨会话、跨天的事实和用户偏好**
关掉这次对话，摘要也跟着没了，Agent 没法"记住"用户上次说过的偏好、之前项目里的约定。

**✅ 斯坦福大学与 Google DeepMind/Google Research 合作的 Generative Agents 论文（2023 年 4 月）：提出带打分机制的"记忆流"**
论文给每条记忆打三个分数——**时近性**（recency，指数衰减）、**重要性**（importance，让 LLM 打 1-10 分）、**相关性**（relevance，与当前查询的语义相关度），检索时按加权分数取相关记忆，而不是全量塞入上下文。

**❓ 即使有打分检索，如何在有限的上下文窗口和外部更大的存储之间统一调度，依然缺少一个系统性框架**
"什么时候该从外部存储里取记忆进上下文、什么时候该把不常用的挤出去"，需要一个更系统的架构隐喻来指导设计。

**✅ MemGPT 论文（Charles Packer 等，UC Berkeley，2023 年 10 月）：把 LLM 上下文类比操作系统的内存分页**
论文提出"虚拟上下文管理"，把有限的上下文窗口类比操作系统的 RAM，把外部向量库/结构化存储类比磁盘，仿照 OS 内存分页机制在两者间调度记忆内容，用中断机制管理控制流——这个项目后来演进成开源项目 Letta。

**现状：短期用工作记忆/滚动摘要，长期用向量检索存储；写入要区分事实与推断、带时间戳来源、可撤销；读取按任务语义检索相关记忆而非全量注入，冲突时新信息优先**

## 业界现状：按场景分层，不是"文本 vs 向量"的二选一

**编程类 Agent（Claude Code、Codex、Cursor、GitHub Copilot、Gemini CLI、Jules）：全部收敛到纯文本**

这几家都有"静态文件层"（CLAUDE.md/AGENTS.md/GEMINI.md/.cursorrules/copilot-instructions.md）+ 部分还有"自动记忆层"（Codex Memories、Cursor Memories、Copilot Memory、Jules Memory，由 AI 从对话中自动提炼事实、落地成文本条目）。六家里**没有一家官方证实使用向量/embedding 检索**——其中 **Gemini CLI 官方文档明确写死是纯 Markdown 文件读写**，其余几家是"未公开"，第三方博客关于"用了向量检索"的说法都缺乏官方信源支撑。原因和这类场景的特点直接相关：记忆量小（通常十几到几十条项目级事实）、需要精确规则遵循而非模糊召回、要可审计可编辑。

**消费级对话助手（ChatGPT Memory、Gemini App 个性化记忆）：架构未公开，无法判定**

两家官方都只描述用户可见行为（记什么、怎么关、怎么删），从未公开底层存储/检索机制。第三方逆向分析甚至彼此结论相反（一派认为是纯文本注入，一派怀疑有隐藏的向量检索层）。注意别和 Google 的**企业级** Memory Bank（Vertex AI Agent Engine 的开发者产品）搞混——那是完全不同的产品，官方文档明确写了用 similarity search，但消费级 Gemini App 的个性化记忆功能本身依然是黑箱。

**专门做"记忆管理"的产品（Mem0、Zep、Letta）：向量检索才是这里的主流，但都是混合架构**

- **Mem0**：向量语义检索为主力，配 BM25 关键词 + 实体图三路融合
- **Zep**：反而以**知识图谱**（Graphiti 引擎）为骨架，向量只是三路检索之一，官方博客标题直接叫《Stop Using RAG for Agent Memory》，明确反对"纯向量"路线，理由是向量检索缺乏时序推理和多跳推理能力
- **Letta**（MemGPT 论文团队做的产品化项目）：完整保留了论文里"向量库当磁盘"的设计，后端是 PostgreSQL + pgvector，新版又叠加了全文检索做混合
- 但 LangChain 官方文档的长期记忆默认存储其实是 **JSON key-value**，向量嵌入只是**可选的增强层**，用于"不知道确切 key 时的模糊召回"

**结论**：不是"流行的 AI 工具都不用向量检索"，而是三类场景各有取舍——编程 agent 因为记忆量小、要求精确可审计，清一色用纯文本；消费级助手架构不透明查不清；专门的记忆基础设施产品里向量确实是主力技术，但 2025-2026 年的行业共识是"混合架构"（向量 + 关键词 + 图/结构化）优于单一路线，没有一家头部产品是纯向量库。

## 参考资料

- [Generative Agents: Interactive Simulacra of Human Behavior（arXiv:2304.03442）](https://arxiv.org/abs/2304.03442)
- [MemGPT: Towards LLMs as Operating Systems（arXiv:2310.08560）](https://arxiv.org/abs/2310.08560)
- [Codex — Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [Codex — Memories](https://developers.openai.com/codex/memories)
- [Gemini CLI — Memory 工具文档](https://geminicli.com/docs/tools/memory/)
- [GitHub Copilot — About Copilot Memory](https://docs.github.com/en/copilot/concepts/agents/copilot-memory)
- [Mem0 官方文档](https://docs.mem0.ai)
- [Zep — Stop Using RAG for Agent Memory](https://blog.getzep.com/stop-using-rag-for-agent-memory/)
- [Letta — Archival Memory](https://docs.letta.com/guides/core-concepts/memory/archival-memory)
- [LangChain — Long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory)
