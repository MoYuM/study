---
题目: "XSS"
分类: 安全
频率: 低频
id: fa9e9778-3776-4490-89a1-ac9d0adce7e4
---
XSS（跨站脚本攻击）：攻击者向页面注入恶意脚本并在他人浏览器执行。

类型：存储型（落库后持续触发）、反射型（恶意参数随响应返回）、DOM 型（前端直接把不可信数据写入 DOM）。

防御：对输出做转义（HTML/属性/JS 上下文分别处理）、设置 CSP、Cookie 加 HttpOnly、避免 `innerHTML`/`eval`/`document.write`、对用户输入做白名单校验、使用框架默认转义（React/Vue 默认转义，慎用 dangerouslySetInnerHTML / v-html）。

## 发展史（问题 → 方案的链条）

❓ XSS 攻击最常见的目的是什么？——通过 `document.cookie` 读取用户的会话 cookie，发给攻击者服务器，冒充用户登录状态。
✅ 2002 年，微软在 IE6 SP1 里率先实现了 **HttpOnly** cookie 属性（由 Secure Windows Initiative 团队的 Michael Howard 推动）：cookie 打上这个标记后，JS 读取 `document.cookie` 时它不会出现在结果里——就算 XSS 成功注入脚本，也偷不到这个 cookie。

❓ 但 HttpOnly 只堵住了"偷 cookie"这一条路，恶意脚本一旦注入成功，还能干别的坏事（篡改页面、监听键盘、冒用页面内 token 发请求等）。怎么从根上不让恶意脚本执行？
✅ 2004～2007 年前后，安全研究者 Robert Hansen 与 Mozilla 的 Gervase Markham 提出"内容限制"构想——让网站通过 HTTP 响应头声明"页面只允许从哪些来源加载脚本/样式"。这个构想 2011 年 3 月首次在 Firefox 4 落地，2012 年成为 W3C 候选推荐标准（CSP 1.0），2014 年发布 Level 2。这就是 **CSP（Content Security Policy）**——即使恶意脚本被注入进 HTML，只要来源不在白名单里（或页面禁止内联脚本），浏览器直接拒绝执行。

**现状对比**：HttpOnly 防的是"脚本执行后能不能偷到 cookie"，CSP 防的是"恶意脚本能不能执行"——两者针对 XSS 攻击链的不同阶段，生产环境通常两个都要配，不是二选一。

## 参考资料

- [HttpOnly — OWASP Foundation](https://owasp.org/www-community/HttpOnly)
- [Content Security Policy — Wikipedia](https://en.wikipedia.org/wiki/Content_Security_Policy)
- [Content Security Policy 1.0 Lands In Firefox — Mozilla Security Blog](https://blog.mozilla.org/security/2013/06/11/content-security-policy-1-0-lands-in-firefox/)
