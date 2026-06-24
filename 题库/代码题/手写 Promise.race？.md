---
题目: "手写 Promise.race？"
分类: 代码题
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: 86e4ff5e-95b3-41b0-8087-cf3fa750a214
备注: ""
---
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
