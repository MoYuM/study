---
题目: "HTTPS 原理？"
分类: HTTP
频率: 高频
id: 385e29bd-9121-81dc-9f40-d8b203b9c646
---
HTTPS = HTTP + TLS。握手用非对称加密协商出对称密钥，之后用对称加密传输（兼顾安全与性能）。

要点：CA 证书验证服务器身份防中间人；非对称（RSA/ECDHE）传递/协商密钥；对称（AES）加密正文；摆手产生会话密钥。

## 参考资料

- [MDN — 传输层安全协议 TLS](https://developer.mozilla.org/zh-CN/docs/Web/Security/Transport_Layer_Security)
- [图解 HTTPS（小林 coding）](https://xiaolincoding.com/network/2_http/https_rsa.html)
