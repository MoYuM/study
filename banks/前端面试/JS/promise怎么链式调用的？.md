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

## 追问

### then 返回的新 Promise，状态具体是怎么决定的？

由 `.then()` 里回调函数的**返回值**决定，规则（Promises/A+ 规范里叫「thenable 解析过程」，`[[Resolve]](promise, x)` 算法）分三种情况：

1. 回调返回一个**普通值**（数字、字符串、普通对象等）→ 新 Promise 直接以这个值 **fulfilled**。
2. 回调返回一个 **Promise（或 thenable，即带 `.then` 方法的对象）**→ 新 Promise **不会立刻决议**，而是"跟随"这个返回的 Promise——等它 resolve/reject 后，新 Promise 才跟着变成相同的状态和值。
3. 回调内部**抛出异常**（或返回 `Promise.reject(...)`）→ 新 Promise 直接以这个错误 **rejected**。

```js
Promise.resolve(1)
  .then(v => v + 1)                 // 返回普通值 2 → 新 promise 直接 fulfilled(2)
  .then(v => fetch('/api/' + v))    // 返回一个新 Promise → 新 promise 跟随 fetch 的结果
  .then(res => { throw new Error('x') }) // 抛出异常 → 新 promise 直接 rejected
  .catch(err => console.log(err));  // 捕获最近的错误
```

## 发展史（问题 → 方案的链条）

**❓ 早期 JS 异步全靠回调，回调地狱难维护，也没有统一的错误传播/链式组织方式**
需要一种能"链式"组织异步操作、统一处理成功/失败的抽象。

**✅ CommonJS 社区 2009 年前后开始讨论 Promise 规范（Kris Zyp 提出 Promises/A 提案，Kris Kowal 等人参与推动并写出 Q 这样的实现库）；jQuery 1.5（2011 年 1 月）引入了自己的 `$.Deferred`**
但各家实现互不兼容——jQuery 的 Deferred 在 1.8（2012 年）之前，`.then()` 只是 `.done()/.fail()` 的别名，根本不返回新的可链式 Promise；`.then()` 回调内部抛出异常也不会被自动捕获转为 rejected，而是直接冒泡成未捕获的 JS 错误。

**❓ 各家 Promise 库行为不一致，同一段代码换个库跑出不同结果，没法在类库之间自由传递/链接 Promise**
社区需要一份"哪怕内部实现不同，只要行为一致就能互操作"的最低限度规范。

**✅ Promises/A+ 规范（Domenic Denicola、Kris Kowal 等人牵头，2012 年底至 2013 年间通过 promises-aplus 组织、多个库互相实现验证协作定案）：核心是标准化"thenable 解析过程"（`[[Resolve]](promise, x)` 算法）**
严格规定 `.then()` 必须返回一个新 Promise，新 Promise 的状态由回调返回值决定——返回普通值直接 fulfill，返回 thenable 则递归跟随其状态，抛出异常自动转为 reject。这套统一的"解析过程"第一次让不同库产出的 Promise 能自由链式调用、互相操作。

**❓ Promises/A+ 只是社区规范，不是语言内置能力，还得手动引入第三方库（Q/bluebird/when.js 等）**
需要语言原生支持，不再依赖任何第三方库。

**✅ ES6/ECMAScript 2015（2015 年 6 月）把 Promise 作为原生对象纳入语言标准，其行为设计直接基于 Promises/A+ 规范（在 thenable 解析过程基础上补充了 `Promise.all/race`、微任务调度等更多规定）**
从此不再需要任何第三方 Promise 库，"每次 `.then()` 返回新 Promise、状态由回调返回值决定、抛错自动转为 reject"这套机制成为语言标准的一部分。

**现状：`.then()` 链式调用的每一个细节（返回值决定新 Promise 状态、抛错被最近 `catch` 捕获）都不是某个库的怪癖，而是 ES6 规范内置的 Promises/A+ 解析过程明文规定的行为——这也是为什么早期 jQuery Deferred 和现在的原生 Promise "长得像但行为不完全一样"：jQuery 在 `.then()` 正式支持链式、正式捕获异常之前踩过的坑，正是 Promises/A+ 要解决的问题**

## 参考资料

- [CommonJS Promises/A — Kris Zyp](https://wiki.commonjs.org/wiki/Promises/A)
- [A Brief, Incomplete History of JavaScript Promises](https://samsaccone.com/posts/history-of-promises.html)
- [jQuery 1.5 发布公告](https://blog.jquery.com/2011/01/31/jquery-15-released/)
- [The Differences Between jQuery Deferreds and the Promises/A+ Spec](https://abdulapopoola.com/2014/12/12/the-differences-between-jquery-deferreds-and-the-promisesa-spec/)
- [jQuery 3.0 升级指南](https://jquery.com/upgrade-guide/3.0/)
- [Promises/A+ 规范](https://github.com/promises-aplus/promises-spec)
