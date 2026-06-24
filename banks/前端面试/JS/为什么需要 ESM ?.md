---
题目: "为什么需要 ESM ?"
分类: JS
频率: 低频
id: 426405c1-af80-46cc-b546-5852d2f79fa4
---
ESM 是 ES6 之后引入的新的、官方的、标准化的的模块编程方案。相比 CommonJS，有以下的优点。

- 官方标准 ⇒ 浏览器原生支持
- 静态 ⇒ 编译时加载 ⇒ 减少包体积
    
    > 引申：lodash-es 其实就是 lodash 的 ESM 版本，使用 lodash-es 就能利用 Tree-Shaking 来减少打包体积
    > 
- 可以异步加载
- 不存在循环引用的问题

https://exploringjs.com/es6/ch_modules.html#sec_modules-in-javascript

https://es6.ruanyifeng.com/#docs/module
