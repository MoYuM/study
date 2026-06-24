---
题目: "CSRF"
分类: 安全
频率: 低频
id: 4617d89b-039c-4d5e-9b73-91233329f8f5
---
https://tech.meituan.com/2018/10/11/fe-security-csrf.html

- 什么是 CSRF？
    - 跨站请求伪造，攻击者在一个第三方网站对本站做请求，因为我们刚登录了本站，所以他能拿到我的 cookie，冒充用户执行一些操作
- 类型？
    - GET
    - POST
    - 链接
- 预防？
    - 同源检测
    - 双重 cookie
    - CSRF Token
    - Samesite Cookie
