---
题目: "如何中止正在进行的 AI 请求？"
分类: AI
频率: 高频
id: 385e29bd-9121-81e4-a5d6-fb68489ccdf6
---
- 前端：`new AbortController()`，把 `controller.signal` 传入 fetch；点「停止生成」时 `controller.abort()` 取消请求与流消费。
- 后端不会自动停止：abort() 只是客户端断开连接，服务端必须**显式监听断连**（Node `req.on('close')`、FastAPI `request.is_disconnected()`、Go `ctx.Done()`）才能停止 LLM 推理、释放 GPU/CPU；经缓冲代理 / 负载均衡 / HTTP-2 多路复用时，断连信号可能延迟。
- UI：清理未完成的半成品状态，标记该条消息为已中止。
