---
题目: "setTimeout 和 setInterval 的区别？"
分类: JS
频率: 高频
id: 2d8945d4-217c-4447-8541-101d7db96137
---
- setTimeout：延时执行一次。
- setInterval：按固定间隔重复执行，但**间隔只计算任务开始时间，没算上任务本身的执行耗时**——如果回调耗时过长，会导致间隔比设定的短，极端情况下会堆积甚至无间隔连续执行。

实践中常用**递归 setTimeout** 替代 setInterval：可以在每次回调里根据实际情况动态调整下一次延迟，保证间隔更稳定。记得清除定时器避免泄漏；高精度动画用 requestAnimationFrame。

https://zh.javascript.info/settimeout-setinterval
