---
题目: "setTimeout 与 setInterval 的区别？"
分类: JS
频率: 低频
id: 385e29bd-9121-814a-9b96-d2247c708320
---
- setTimeout：延时执行一次。
- setInterval：按间隔重复，但回调耗时过长会堆积/漂移。

实践中常用递归 setTimeout 替代 setInterval 以保证间隔稳定；记得清除定时器避免泄漏。高精度动画用 requestAnimationFrame。
