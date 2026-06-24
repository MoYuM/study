---
题目: "XSS"
分类: 安全
频率: 低频
id: fa9e9778-3776-4490-89a1-ac9d0adce7e4
---
XSS（跨站脚本攻击）：攻击者向页面注入恶意脚本并在他人浏览器执行。

类型：存储型（落库后持续触发）、反射型（恶意参数随响应返回）、DOM 型（前端直接把不可信数据写入 DOM）。

防御：对输出做转义（HTML/属性/JS 上下文分别处理）、设置 CSP、Cookie 加 HttpOnly、避免 `innerHTML`/`eval`/`document.write`、对用户输入做白名单校验、使用框架默认转义（React/Vue 默认转义，慎用 dangerouslySetInnerHTML / v-html）。
