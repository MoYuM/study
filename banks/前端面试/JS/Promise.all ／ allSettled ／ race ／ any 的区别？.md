---
题目: "Promise.all / allSettled / race / any 的区别？"
分类: JS
频率: 高频
id: 385e29bd-9121-819e-a8b0-f741e5d32005
---
- **all**：全部成功才成功，任一失败立即 reject。
- **allSettled**：等全部结束，返回每项 `{status,value/reason}`，不短路。
- **race**：第一个落定（成功或失败）即返回。
- **any**：第一个成功即返回，全失败才报 AggregateError。
