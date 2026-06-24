---
题目: "手写 Promise.retry?"
分类: 代码题
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: b086fe54-10cb-49a6-9311-14e26d7c39bc
备注: ""
---
```tsx
/**
 * 手写 promise.retry
 */
function promiseRetry(promiseFn, times) {
  return new Promise((resolve, reject) => {
    const run = (t) => {
      promiseFn()
        .then((res) => {
          resolve(res);
        })
        .catch((err) => {
          const newT = t - 1;
          if (newT === 0) {
            reject(err);
          } else {
            run(newT);
          }
        });
    };

    run(times);
  });
}

const random = () => {
  const r = Math.random();

  return r > 0.99 ? Promise.resolve("success") : Promise.reject("fail");
};

promiseRetry(random, 3)
  .then((res) => {
    console.log(res);
  })
  .catch((err) => {
    console.log(err);
  });

```
