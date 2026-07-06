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

**现状：大模型对话首选 SSE/流式 fetch，双向实时场景才用 WebSocket**
纯粹的服务端流式输出（如大模型逐字生成）用 SSE 或 fetch+ReadableStream 就够，轻量、兼容 HTTP 基础设施；协同编辑、语音信令这类真正需要双向实时通信的场景，才需要 WebSocket 的全双工能力。

## 参考资料

- [MDN — Server-Sent Events](https://developer.mozilla.org/zh-CN/docs/Web/API/Server-sent_events)
- [RFC 6455 — The WebSocket Protocol（2011）](https://www.rfc-editor.org/rfc/rfc6455)
- [RFC 7540 — HTTP/2（2015）](https://www.rfc-editor.org/rfc/rfc7540)
