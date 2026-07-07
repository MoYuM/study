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

## 发展史（问题 → 方案的链条）

**❓ 早期 JS 异步全靠回调函数，嵌套多了变成"回调地狱"，错误处理也各写各的**
异步操作只能通过回调函数处理结果，多个异步操作依次执行时回调层层嵌套，代码难读；每个回调还得自己判断有没有出错，没有统一的错误处理方式。

**✅ Promise（社区库如 Q、jQuery Deferred 先行探索，ES2015/2015 年 6 月正式进入语言规范）：用链式 `.then()`/`.catch()` 取代嵌套回调**
Promise 把"异步结果"包装成对象，可以用 `.then()` 链式处理成功、用 `.catch()` 统一处理失败，摆脱层层嵌套。

**❓ `.then()` 链式写法虽然比嵌套回调好，但读起来还是不如同步代码直观**
即使用了 Promise，异步代码读起来仍然和同步代码的直觉不一样。

**✅ Generator（ES2015）+ 自动执行器（TJ Holowaychuk 的 `co` 库，2013 年 6 月首发）：手动实现"看起来同步"的异步代码**
Generator 函数可以用 `yield` 暂停执行；配合 `co` 这样的第三方"自动执行器"库不断调用 `.next()` 驱动 generator、遇到 Promise 就等它完成再继续，就能写出形似同步、实则异步的代码——这正是 async/await 语法糖背后的原型（`co` 早期版本基于 thunk/回调风格，2014 年 11 月的 4.0 版本才转向基于 Promise，和现在的 async/await 模式更接近）。

**❓ 这套写法依赖第三方库手动驱动 generator，不是语言原生能力**
Generator + 自动执行器模式需要额外引入库、理解 generator 运行机制。

**✅ async/await（ES2017/2017 年 6 月）：把"自动执行器"内置进语言本身**
标准把 Generator + 自动执行器这套模式直接做成语法糖：`async` 函数内部遇到 `await` 会暂停等待 Promise 落定，不需要再手动引入第三方驱动库。

**❓ async 函数内部抛出的错误，如果外部没人接住，会怎样？**
async 函数返回的 Promise 会变成 rejected 状态，如果没有任何 `.catch()`/`try-catch` 处理它，这个 rejection 就成了"没人认领"的错误。

**✅ `unhandledrejection` 事件（不是 ECMAScript 规范，而是 WHATWG HTML 规范里的 `PromiseRejectionEvent`，2015 年 11 月加入规范；浏览器实现：Chrome 49 于 2016 年 3 月率先支持，Safari 11 于 2017 年跟进，但 Firefox 默认启用晚到 2019 年 9 月的 Firefox 69）：全局兜底捕获未处理的 rejection**
监听全局的 `unhandledrejection` 事件，可以捕获所有没被 `.catch()`/`try-catch` 处理的 Promise 拒绝，常用于错误上报兜底。

**现状：async/await = Generator + 自动执行器语法糖，异常捕获用 try/catch 或 .catch()，全局兜底用 unhandledrejection，Promise.all 一个失败会拖垮全部（用 allSettled 规避）**
