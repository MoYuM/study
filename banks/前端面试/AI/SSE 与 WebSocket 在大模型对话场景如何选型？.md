---
题目: "SSE 与 WebSocket 在大模型对话场景如何选型？"
分类: AI
频率: 高频
id: 385e29bd-9121-810a-a129-e35bb91ae7e9
---
AI 一问一答、服务端单向推送、回复较长，**首选 SSE**。

## 发展史（问题 → 方案的链条）

**❓ AJAX 时代，客户端能主动问，服务端没法主动推**
2005 年前后 AJAX 普及，异步请求方便了客户端拉取数据，但依然是"客户端问、服务端答"的单向发起模式——服务端有新消息想立刻告诉客户端，做不到。

**✅ 轮询/长轮询（Comet）先顶上**
开发者用轮询（定时反复发请求）或长轮询（把请求挂起，等有数据才返回）模拟"服务端推送"的效果，这类技巧后来被称为 Comet（术语由 Alex Russell 于 2006 年提出）。

**❓ 轮询浪费带宽、延迟高，长轮询也要不断重建连接**
高频轮询造成大量无效请求；长轮询虽然省了一些无效请求，但每次响应后还要重新发起下一次挂起请求，效率仍然有限。

**✅ 两条标准化路线分别诞生：WebSocket（全双工）与 SSE（单向）**
WebSocket（2011 年，RFC 6455）提供真正的全双工持久连接，服务端/客户端随时都能主动发消息；同期 HTML5 规范也定义了 SSE（Server-Sent Events）——基于普通 HTTP 的单向服务端推送，用 `EventSource` API 消费，只解决"服务端主动推给客户端"这一个方向的需求，协议和实现都比 WebSocket 简单。

**❓ SSE 只能传文本，且早期并发连接数量很受限**
SSE 基于 `text/event-stream`，只能传 UTF-8 文本；而且 HTTP/1.1 下浏览器对每个域名的并发连接数约束在 6 个左右——如果一个页面要开多个 SSE 连接，很容易撞到这个上限。

**✅ HTTP/2（2015 年，RFC 7540）的多路复用解除了这个限制**
HTTP/2 允许在一条连接上并行传输多个流，不再受"每域名 6 个连接"约束，这是 SSE 能在生产环境大规模使用的关键前提。

**❓ 大模型对话场景兴起后，还需要比 `EventSource` 更灵活的方式**
`EventSource` 原生 API 只支持 GET 请求，而大模型对话通常需要在请求体里带上下文（POST），原生 SSE API 用不了。

**✅ fetch + ReadableStream：手动读取流式响应，绕开 `EventSource` 的限制**
用 `fetch` 发起 POST 请求，从响应体的 `ReadableStream` 里逐块读取数据，效果上等价于"单向流式推送"，但不受 `EventSource` 只能 GET 的限制，也不用严格遵守 SSE 的 `data:` 格式——这也是当前大模型 API（如 OpenAI/Anthropic 的流式接口）常用的实现方式。

**❓ 2023 年后 Agent 场景兴起：用户要能中途打断生成、批准/驳回工具调用、多轮引导——这些都要求客户端在同一条连接里随时"往回发信号"，纯 SSE 天生做不到**
LangGraph / CrewAI / AutoGen 这类 Agent 框架的本质是"模型提议动作、等人批准"的双向模式；SSE 只支持服务端→客户端单向推送，客户端想插话（打断/确认）只能另开一次 HTTP 请求，做不到在生成过程中同一条连接内实时介入。一个具体例子：MCP（Model Context Protocol）在 **2025 年 3 月 26 日的规范修订**中正式弃用了原来的 HTTP+SSE 传输（拆成 POST 发消息、SSE 收消息两个通道，人为割裂双向交互，且 Serverless 部署下长连接易掉线/会话失步），改用 **Streamable HTTP**（单个端点，按需可将响应升级为 SSE 流）。

**✅ 尚无定论：一部分场景往 WebSocket／混合架构走，一部分坚持 SSE 足够**
业界目前是两派并存，还没收敛：Google（Gemini 实时多模态 Agent）、AWS Bedrock AgentCore（2025 年 12 月上线双向流式）等采用 WebSocket 全双工，部分生产系统甚至"WebSocket 做控制通道 + SSE 做数据通道"混合；但也有观点坚持 SSE 更优——无状态、无需粘性会话、天然被负载均衡器/CDN 支持，而 WebSocket 升级协议后反而用不上 HTTP/2 多路复用。

**现状：纯文字问答场景，SSE/流式 fetch 依然是最简单够用的方案；但 Agent 场景（打断/工具调用确认/多轮交互）的选型正在演化中，核心问题已从"SSE 还是 WebSocket"变成"这个场景需不需要客户端在生成过程中主动插话"**
不要死记"大模型对话 = SSE"，先看清楚这是纯问答还是需要中途交互的 Agent 场景，再决定要不要上双向能力。

## 参考资料

- [MDN — Server-Sent Events](https://developer.mozilla.org/zh-CN/docs/Web/API/Server-sent_events)
- [RFC 6455 — The WebSocket Protocol（2011）](https://www.rfc-editor.org/rfc/rfc6455)
- [RFC 7540 — HTTP/2（2015）](https://www.rfc-editor.org/rfc/rfc7540)
- [WebSocket.org — WebSockets and AI: Why LLMs Are Moving Beyond SSE](https://websocket.org/guides/websockets-and-ai/)
- [Why MCP Deprecated SSE and Went with Streamable HTTP（MCP 规范 2025-03-26 修订）](https://blog.fka.dev/blog/2025-06-06-why-mcp-deprecated-sse-and-go-with-streamable-http/)
- [Google Developers Blog — Beyond Request-Response: Architecting Real-time Bidirectional Streaming Multi-agent System](https://developers.googleblog.com/en/beyond-request-response-architecting-real-time-bidirectional-streaming-multi-agent-system/)
- [Procedure.tech — The Streaming Backbone of LLMs: Why SSE Still Wins（反方观点，供对照）](https://procedure.tech/blogs/sse-for-llms/)
