---
题目: "Bind\\Call\\Apply 的优先级和原因？"
分类: JS
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: cc788a3a-033d-4c33-8eca-5c94882331bf
备注: ""
---
三者都用于改变函数的 this：

- call(thisArg, 参数列表)：立即执行。
- apply(thisArg, 参数数组)：立即执行。
- bind(thisArg)：返回一个 this 已固定的新函数，延迟执行。

优先级：bind 绑定后，再用 call/apply 也无法改变其 this（bind 内部用闭包+apply 固定）；但 new 调用 bind 返回的函数时，this 指向新实例（new 优先级高于 bind）。
