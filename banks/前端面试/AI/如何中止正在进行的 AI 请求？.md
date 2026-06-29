---
题目: "如何中止正在进行的 AI 请求？"
分类: AI
频率: 高频
id: 385e29bd-9121-81e4-a5d6-fb68489ccdf6
---
- 前端：`new AbortController()`，把 `controller.signal` 传入 fetch；点「停止生成」时 `controller.abort()` 取消请求与流消费。
- 后端不会自动停止：abort() 只是客户端断开连接，服务端必须**显式监听断连**（Node `req.on('close')`、FastAPI `request.is_disconnected()`、Go `ctx.Done()`）才能停止 LLM 推理、释放 GPU/CPU；经缓冲代理 / 负载均衡 / HTTP-2 多路复用时，断连信号可能延迟。
- UI：清理未完成的半成品状态，标记该条消息为已中止。

## 追问

### abort() 发出的到底是什么信号？服务端怎么感知？

`abort()` 不会向服务端发送专属的 "停止" 消息，它做的是**直接关闭 TCP 连接**（发 FIN/RST 包）。服务端感知的是连接断开事件，不是 abort 协议信号：

```
前端 abort() → 浏览器关闭 TCP 连接
                       ↓
服务端 TCP 层感知到对端关闭
                       ↓
Node.js:  req.on('close') 触发
FastAPI:  request.is_disconnected() 返回 true
Go:       ctx.Done() channel 关闭
```

### 为什么经过代理后断连信号可能失效？

```
浏览器 → Nginx（缓冲）→ Node 服务 → LLM API
```

Nginx 默认有响应缓冲，它可能等缓冲区满才关闭到后端的连接，甚至某些配置会完全屏蔽客户端断连。结果是 Node 服务感知延迟，LLM 还在生成、GPU 还在跑。

### 代理场景下更可靠的方案

依赖连接断开不够稳，可以改用显式停止请求：

```js
// 前端：abort 取消流 + 额外发停止请求
controller.abort();
fetch('/api/stop', { method: 'POST', body: JSON.stringify({ sessionId }) });
```

服务端收到 `/api/stop` 后主动取消对 LLM 的调用，不依赖 TCP 断连检测，在任何代理结构下都可靠。
