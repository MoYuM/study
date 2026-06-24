---
题目: "OPTIAN请求做什么的？"
分类: HTTP
频率: 低频
id: 120e29bd-9121-806c-906e-f4f1ea59842e
---
OPTIONS 是 CORS 的「预检请求」。当跨域请求是非简单请求（自定义头、PUT/DELETE、Content-Type 为 application/json 等）时，浏览器会先自动发一个 OPTIONS 询问服务器是否允许。

服务器在响应里返回 Access-Control-Allow-Origin / -Methods / -Headers / -Max-Age；通过后才发真正请求。可用 Access-Control-Max-Age 缓存预检结果减少 OPTIONS 次数。
