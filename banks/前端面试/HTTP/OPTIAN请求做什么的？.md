---
题目: "OPTIAN请求做什么的？"
分类: HTTP
频率: 低频
id: 120e29bd-9121-806c-906e-f4f1ea59842e
---
OPTIONS 是一个**通用的 HTTP 方法**，作用是「向服务器/某个 URL 询问它允许的通信选项」——不是专属于 CORS 的东西，CORS 预检只是它最常见的一种具体用法。

## 用法一：直接查询某个 URL/服务器支持哪些方法

不涉及跨域也能用，命令行直接测：

```bash
curl -X OPTIONS https://example.org -i
```

响应里的 `Allow` 头会列出这个资源支持的所有方法：

```
HTTP/1.1 204 No Content
Allow: OPTIONS, GET, HEAD, POST
```

请求目标可以是具体路径，也可以用 `*` 表示"整个服务器"而不是某个特定资源。

## 用法二：CORS 预检请求（浏览器自动触发，最常被问到的场景）

当跨域请求是**非简单请求**（自定义头、PUT/DELETE、Content-Type 为 `application/json` 等）时，浏览器会在真正发请求前自动先发一个 OPTIONS，**询问服务器是否允许这次跨域请求**——跨不跨域浏览器自己就能判断，不需要问服务器；OPTIONS 问的是"这个跨域请求你服务器允不允许"：

- 请求带上 `Access-Control-Request-Method`（告诉服务器接下来真正要用的方法，比如 `POST`）、`Access-Control-Request-Headers`（告诉服务器接下来要带的自定义头，比如 `X-PINGOTHER`、`Content-Type`）
- 服务器响应里返回 `Access-Control-Allow-Origin` / `-Methods` / `-Headers` / `-Max-Age`，这几项都对得上才算"允许"，浏览器才会真正发出实际请求

`Access-Control-Max-Age` 让浏览器缓存这次预检的"允许结果"一段时间（例如 86400 秒 = 1 天），减少重复发 OPTIONS——**这是 CORS 预检专属的缓存机制，跟通用 HTTP 缓存（Cache-Control）是两回事**：OPTIONS 方法本身在通用 HTTP 语义里是**不可缓存**的（MDN 明确标注 Cacheable: 否），普通 OPTIONS 响应不会被 HTTP 缓存/CDN 缓存下来；只有 CORS 预检这个特定场景，浏览器会用 `Access-Control-Max-Age` 单独维护一份"预检权限缓存"，两者不要混为一谈。

## 其他属性

**安全（Safe）**、**幂等（Idempotent）**——OPTIONS 不会改变服务器状态，多次发送效果一样，可以放心重试。

## 参考资料

- [MDN — OPTIONS](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Reference/Methods/OPTIONS)
