---
题目: "promise怎么链式调用的？"
分类: JS
频率: 低频
id: 120e29bd-9121-80a4-8fc1-ef2892c4f97f
---
then 每次返回一个新的 Promise，从而支持链式调用。

- 回调的返回值作为下一个 then 的入参；返回 Promise 时会等待其 resolve。
- 抛出错误或返回 reject 会被最近的 catch 捕获。
- then(onFulfilled, onRejected)、catch、finally。

链式把嵌套回调扁平化，解决回调地狱；注意每个 then 都应 return 以保持链路。
