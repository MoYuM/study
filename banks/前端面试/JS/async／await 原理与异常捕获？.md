---
题目: "async/await 原理与异常捕获？"
分类: JS
频率: 高频
id: 385e29bd-9121-8104-a226-feb1f4643274
---
原理：
- async 函数返回 Promise
- await 暂停执行等待 Promise 落定
- 本质是 Generator + 自动执行器的语法糖。

异常捕获：
1. `try/catch` 包裹 await
2. `.catch()` 整个 async 函数
3. 一个报错会让 all 整体 reject（可用 allSettled）。
