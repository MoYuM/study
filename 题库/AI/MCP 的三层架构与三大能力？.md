---
题目: "MCP 的三层架构与三大能力？"
分类: AI
频率: 高频
掌握: 
下次复习: 
上次评测: 
id: 385e29bd-9121-8131-a9b6-fd03a985ec78
备注: ""
---
- 三层架构：Host（宿主，运行 AI 应用）/ Client（客户端接口，一对一对接 Server）/ Server（提供能力）。协议 JSON-RPC 2.0；标准传输为 **stdio（本地）或 Streamable HTTP（远程）**（旧的独立 HTTP+SSE 传输已废弃，SSE 现为 Streamable HTTP 内部的可选流式机制）。
- 三大能力：Tool（模型自主调用 / model-controlled）、Resources（应用注入数据 / application-controlled）、Prompts（用户触发的工作流模板 / user-controlled）。分层控制避免模型「瞎调用」。

## 参考资料

- [Model Context Protocol 官方文档](https://modelcontextprotocol.io/introduction)
- [MCP 规范 — Transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
- [JavaGuide — 万字拆解 MCP 协议](https://javaguide.cn/ai/agent/mcp.html)
