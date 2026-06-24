---
题目: "CSRF 是什么？如何防范？"
分类: 安全
频率: 低频
id: 385e29bd-9121-8140-93fe-db3928264302
---
CSRF（跨站请求伪造）：诱导已登录用户在恶意站点发出带上其 Cookie 的请求。

防范：CSRF Token（服务端下发、请求携带校验）、SameSite Cookie、校验 Origin/Referer、关键操作二次验证。与 XSS 防护配合。
