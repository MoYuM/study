---
题目: "Promise.all / allSettled / race / any 的区别？"
分类: JS
频率: 高频
id: 385e29bd-9121-819e-a8b0-f741e5d32005
---
## 发展史（问题 → 方案的链条）

**❓ ES6（2015）Promise.all：多个异步任务要「全部拿到结果」，但任一失败就整体判负，其余成功结果全丢**
`Promise.all` / `Promise.race` 是 ES6（ECMAScript 2015）随 Promise 规范一起引入的两个组合器。`all` 等待全部 resolve，但**任一 reject 就立即整体 reject（fail-fast）**——哪怕另外 9 个任务都成功了，返回的还是那一个失败原因，其余成功结果全部丢失。

**✅ 2020 年（ES2020），Promise.allSettled：不管成败，等全部有结果再说**
TC39 提案 2019 年进入 Stage 4，随 ECMAScript 2020 发布：**等所有 promise 都 settle**（不管 fulfilled 还是 rejected），自己**从不 reject**，返回每一项的 `{status, value/reason}`，交给调用方自己判断哪些成功哪些失败——"批量请求，各自独立处理结果"的场景终于有了标准方案。

**❓ Promise.race（同样 ES6 就有）：谁先 settle 听谁的——但如果最先 settle 的恰好是一次失败，即使后面还有会成功的，也直接判负**
比如多源容灾（同时打三个 CDN，谁先返回用谁的），如果最快返回的那个 CDN 恰好挂了，`race` 立刻整体 reject，完全不管另外两个 CDN 稍后是否会成功——这不是"容灾"该有的行为。

**✅ 2021 年（ES2021），Promise.any：只认「第一个成功」，中途的失败先忽略**
TC39 提案 2020 年进入 Stage 4，随 ECMAScript 2021 发布：**第一个 resolve 的赢**，中途出现的 reject 先记下忽略掉，除非**全部**都 reject，才用新引入的 **AggregateError**（把所有失败原因打包）报错——这才是"多源容灾，有一个成功就行"真正需要的组合器。

**现状：race 与 any 长得像，设计意图正好相反**
`race` 认的是"**第一个 settle**"（resolve/reject 都算数）；`any` 认的是"**第一个 resolve**"（reject 先忽略，除非全灭才报 `AggregateError`）。两者都是"发生了什么就地判定"，唯一区别就是**要不要把 reject 也算数**——这正是本题最容易被张冠李戴的一对。

## 对比表

| 方法 | 结束条件 | 失败行为 | 典型场景 |
|------|---------|---------|---------|
| `all` | 全部 resolve | 任一 reject → 立即整体 reject | 多个请求都需要，缺一不可 |
| `allSettled` | 全部 settle（不管成败） | 从不 reject，每项带 `{status, value/reason}` | 批量请求，各自独立处理结果 |
| `race` | **第一个 settle**（成功或失败都算） | 第一个 reject 就整体 reject | 超时控制：`race([fetch(), timeout()])` |
| `any` | 第一个 resolve | 全部 reject 才报 `AggregateError` | 多源容灾：有一个成功就行 |

## 关键区别

- **all vs allSettled**：all 任一失败立即短路；allSettled 等所有结束，结果是数组 `[{status:'fulfilled',value},{status:'rejected',reason}]`
- **race vs any**：race 是第一个 **settle**（reject 也算）；any 是第一个 **resolve**，忽略失败直到全部失败

## 典型用法

```js
// 超时控制（race）
const timeout = ms => new Promise((_, reject) => setTimeout(() => reject('timeout'), ms));
const result = await Promise.race([fetchData(), timeout(3000)]);

// 批量容错（allSettled）
const results = await Promise.allSettled([fetchA(), fetchB(), fetchC()]);
results.forEach(r => {
  if (r.status === 'fulfilled') console.log(r.value);
  else console.error(r.reason);
});

// 多源容灾（any）
const fastest = await Promise.any([fetchFromCDN1(), fetchFromCDN2(), fetchFromCDN3()]);
```

## 参考资料

- [MDN — Promise.allSettled()](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise/allSettled)
- [MDN — Promise.any()](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise/any)
- [TC39 — Promise.allSettled 提案（Stage 4，2019）](https://github.com/tc39/proposal-promise-allSettled)
- [TC39 — Promise.any 提案（Stage 4，2020）](https://github.com/tc39/proposal-promise-any)
