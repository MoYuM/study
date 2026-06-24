---
题目: "HTTP/1.1、HTTP/2、HTTP/3 演进与 QUIC？"
分类: HTTP
频率: 高频
id: 385e29bd-9121-81d3-89e4-fe772718171a
---
- HTTP/1.1：文本协议、队头阻塞、每域约 6 连接、Keep-Alive。
- HTTP/2：二进制分帧、多路复用、HPACK 头压缩、服务器推送；但只解决**应用层**队头阻塞，**TCP 层队头阻塞仍存在**（丢包会阻塞所有流）。
- HTTP/3：基于 QUIC（UDP），解决 TCP 队头阻塞，0-RTT、连接迁移（换网不断）；QUIC 传输层**集成 TLS1.3**，头压缩用 **QPACK**。

## 参考资料

- [MDN — HTTP 的演变](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Basics_of_HTTP/Evolution_of_HTTP)
- [Cloudflare — What is HTTP/3 / QUIC](https://www.cloudflare.com/learning/performance/what-is-http3/)
