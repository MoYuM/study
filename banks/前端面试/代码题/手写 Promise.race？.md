---
题目: "手写 Promise.race？"
分类: 代码题
频率: 低频
id: 86e4ff5e-95b3-41b0-8087-cf3fa750a214
---
**Promise.race**：传入多个 promise，**谁先 settle（无论 resolve 还是 reject）就用谁的结果**——即使最先 settle 的是 reject，也直接整体 reject，不会等后面可能成功的 promise。

⚠️ 最容易和 **Promise.any** 搞反：any 是"谁先 **fulfilled**（成功）就用谁"，中途的 reject 会被忽略、继续等其他 promise，只有**全部**都失败才整体 reject（用 `AggregateError` 汇总所有失败原因）。记忆：**race 比谁先到终点，不分胜负**（先到就算，哪怕摔倒）；**any 比谁先跑赢**（摔倒的不算，除非全员摔倒）。

## 发展史（问题 → 方案的链条）

❓ ES2015 定稿 Promise 规范时，四个组合子最早只有 `all` 和 `race`。"谁先给结果就用谁"的场景，`race` 的方案是：谁先 settle（不管成功失败）就用谁。这对"竞速/超时控制"很好用（比如给请求配一个超时 Promise 一起 race）。
✅ 语义简单清晰：短路条件 = 任意一个 settle。

❓ 但另一类场景覆盖不了：多个候选源，只要有一个**成功**就行，个别源失败应该被忽略、继续等其他源（比如同时向多个 CDN/备用节点发请求）。用 `race` 会出问题——**如果最先返回的那个源恰好失败了，race 直接 reject，根本不会等后面可能成功的源**。社区的 userland Promise 库和 TC39 都发现这是组合子里缺的一块。
✅ 需要一个"短路条件 = 任意一个 fulfilled"的新组合子。

❓ 怎么补上这个缺口？
✅ TC39（Mathias Bynens、Kevin Gibbons、Sergey Rubanov 提案）新增 **Promise.any**，ES2021 正式定稿：谁先 fulfilled 就用谁，忽略中途的 reject，只有全部都 reject 才整体 reject（`AggregateError` 汇总原因）。

**现状对比**：四个组合子按"短路条件"记忆最清楚——`all` 任意一个 **reject** 就短路；`race` 任意一个 **settle**（无论成败）就短路；`any` 任意一个 **fulfilled** 就短路；`allSettled` 永不短路、等全部完成。`race`（2015）和 `any`（2021）是最容易搞反的一对：`any` 正是为了补 `race` "一失败就整体挂"这个短板，晚了 6 年才补上的后来者。

```tsx
/**
 * 手写 Promise.race
 **/
function promiseRace(promises) {
  return new Promise((resolve, reject) => {
    for (let i = 0; i < promises.length; i++) {
      Promise.resolve(promises[i])
        .then((res) => {
          resolve(res);
        })
        .catch((err) => {
          reject(err);
        });
    }
  });
}

const sleep = (time) => new Promise((resolve) => setTimeout(() => resolve(time), time));

promiseRace([sleep(1000), sleep(2000), sleep(3000)]).then((res) => {
  console.log(res);
});

```
