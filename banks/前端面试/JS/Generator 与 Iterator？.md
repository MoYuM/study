---
题目: "Generator 与 Iterator？"
分类: JS
频率: 低频
id: 385e29bd-9121-81ac-b33c-eb300d2efda9
---
- Iterator（迭代器）：具有 `next()` 返回 `{value, done}` 的对象，符合迭代协议。
- Generator：用 `function*` + `yield` 生成迭代器的语法，可暂停/恢复执行；用于惰性序列、异步流程控制（async/await 的前身）。
