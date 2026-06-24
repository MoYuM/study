---
题目: "setTimeout 和 setTimeIntervel 的区别？"
分类: JS
频率: 高频
掌握: 
下次复习: 
上次评测: 
id: 2d8945d4-217c-4447-8541-101d7db96137
备注: ""
---
在处理定时任务的时候，setTimeout 比 setInterval 更灵活。

setTimeout 可以在每次执行时候拿到前一次任务的结果，setInterval 不能。

setInterval 的间隔指的是任务的开始时间，并没有计算任务的执行时间，所以会导致间隔比实际的短，极端情况下会有无间隔执行的问题

https://zh.javascript.info/settimeout-setinterval
