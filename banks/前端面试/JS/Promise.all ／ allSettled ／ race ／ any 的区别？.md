---
题目: "Promise.all / allSettled / race / any 的区别？"
分类: JS
频率: 高频
id: 385e29bd-9121-819e-a8b0-f741e5d32005
---
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
