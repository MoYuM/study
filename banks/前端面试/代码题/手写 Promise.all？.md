---
题目: "手写 Promise.all？"
分类: 代码题
频率: 高频
id: 31a067a8-a871-4f70-9557-0793030df591
---
接收一个可迭代对象，返回新 Promise；用计数器记录完成数量，按索引存结果保证顺序；全部 resolve 后 resolve 结果数组；任一 reject 立即 reject；空数组直接 resolve []。

```jsx
function promiseAll(iterable) {
  return new Promise((resolve, reject) => {
    const items = Array.from(iterable);
    const results = [];
    let count = 0;
    if (items.length === 0) return resolve(results);
    items.forEach((item, i) => {
      Promise.resolve(item).then(
        (val) => {
          results[i] = val;
          if (++count === items.length) resolve(results);
        },
        reject
      );
    });
  });
}
```

注意用 `Promise.resolve` 包裹每一项以兼容非 Promise 值。
