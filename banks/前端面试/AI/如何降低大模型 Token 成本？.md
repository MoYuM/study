---
题目: "如何降低大模型 Token 成本？"
分类: AI
频率: 低频
id: 385e29bd-9121-8124-9107-c6fb6dc8d1a8
---
六类手段（按"输入→输出→架构"排列），但实际分布在不同层，不是单一角色能全包：

- 精简 Prompt：去除系统提示/用户提示里的冗余。
- 历史对话摘要压缩：多轮对话不全量拼接发送，超过阈值就把旧对话总结成摘要再继续（否则历史消耗随轮数增长）。
- RAG 控 Top-K：只送检索出的高相关片段，不把整个知识库塞进去（也避开"Lost in the Middle"）。
- `max_tokens` + 流式早停：限制输出长度，用户提前拿到所需信息就中断生成。
- 缓存：重复问答直接命中缓存；结构化请求让 Prompt Caching 生效（把不变的部分放前面）。
- 模型路由：简单任务路由到小模型，复杂任务才用大模型。

## 落在架构的哪一层

- **客户端/UI 层能独立拍板**：流式生成时用 `AbortController` 中断请求（ChatGPT/Claude.ai 的"停止生成"按钮）；决定发送什么上下文（Cursor 用 `@file`/`@codebase` 让用户手动圈定范围而不是无脑全发——一次自动补全可能耗 3000+ token，实际只需要 200）。
- **后端/编排层的工作**：RAG 的向量检索（embedding + 向量库 + Top-K，检索基础设施在服务端）；历史摘要压缩（要额外调用一次模型做总结，逻辑通常跑在服务端）；模型路由（对请求难度分类再决定用哪个模型，几乎都在网关层）。
- **调用方（前端直连或后端代理都算）要遵守的规则**：Prompt Caching 要求把请求里内容不变的部分放在前面、稳定前缀不能变，否则不会命中缓存——这是组织请求结构时的硬性要求，不管这段代码写在前端还是后端。

真实例子：

- **Cursor 的 `@codebase`**：查询转 embedding → 向量相似度检索 → 取 Top-K 片段注入上下文；官方建议探索性问题用 `@codebase` 而不是 `@file` 精确圈文件。
- **LMSYS 的 RouteLLM 项目**：给查询做难度分类，简单查询路由到小模型，做到接近 GPT-4 质量但只花 40%-50% 成本；某电信公司仅"缓存 + 路由简单问候语"每年省 9 万美元。
- **Anthropic Prompt Caching**：`cache_control` 打在最后一个"前缀不变"的内容块上，默认 5 分钟 TTL（可设 1 小时）；Claude Code 本身就靠系统提示/工具定义保持稳定来吃这个缓存红利。

## 参考资料

- [Cursor — Models & Pricing / Token Management](https://cursor.com/docs/models-and-pricing)
- [Anthropic — Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [LLM Model Routing: Cheapest Capable Model Per Query](https://leanlm.ai/blog/llm-model-routing)
