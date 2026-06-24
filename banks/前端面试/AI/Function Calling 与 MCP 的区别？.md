---
题目: "Function Calling 与 MCP 的区别？"
分类: AI
频率: 高频
id: 385e29bd-9121-81df-946e-f8d886e73f58
---
Function Calling 与 MCP 不在同一层，常被混为一谈，要讲清边界。

- **Function Calling**：让模型输出结构化的工具调用意图（name + arguments JSON），真正执行权在业务系统；解决「模型不能动手」。前端配合：定义工具 schema、把模型返回的调用参数交给后端/前端执行、再把结果回填给模型。
- **MCP（Model Context Protocol）**：Anthropic 2024 年 11 月推出的开放协议，标准化工具的「发现 / 描述 / 调用 / 返回」。三层架构 Host / Client / Server，协议 JSON-RPC 2.0，标准传输为 **stdio（本地）或 Streamable HTTP（远程）**（旧的独立 HTTP+SSE 传输已废弃，SSE 现为 Streamable HTTP 内部的可选流式机制）。
- **选型**：工具少且固定、追求低延迟 → Function Calling；工具被多应用共享、第三方提供、动态变化、需安全隔离 → MCP。二者可组合：MCP 负责「工具怎么接入」，Function Calling 是「模型怎么表达调用」。
