---
题目: "按顺序执行 Promise"
分类: 代码题
频率: 低频
id: a58b1813-25e7-4a22-8ba7-1f92dd88db84
---
```tsx
const fetch = (url) => {
  console.log("start", url);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(url);
    }, Math.random() * 3000);
  });
};

// 当前
/*
start /a
start /b
start /c
get /b
get /c
get /a
 * */

// 改造一下方法的实现，使得控制台输出顺序
// start /a
// get /a
// start /b
// get /b
// start /c
// get /c
const request = (url) => {
  // 内部维护一个队列，通过递归控制执行顺序
  const queue = request._queue || Promise.resolve();

  request._queue = queue.then(() => fetch(url));

  return request._queue;
};

request("/a").then((r) => console.log("get", r));
request("/b").then((r) => console.log("get", r));
request("/c").then((r) => console.log("get", r));

```
