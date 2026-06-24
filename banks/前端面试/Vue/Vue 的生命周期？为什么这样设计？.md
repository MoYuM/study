---
题目: "Vue 的生命周期？为什么这样设计？"
分类: Vue
频率: 低频
id: 385e29bd-9121-81a3-82c3-fb1d17136f0c
---
8 个阶段：beforeCreate / created / beforeMount / mounted / beforeUpdate / updated / beforeUnmount / unmounted（Vue3 组合式为 onMounted 等）。

设计意义：在不同阶段插入逻辑——created 取数据、mounted 操作 DOM/初始化第三方、unmounted 清理定时器/事件防泄漏。
