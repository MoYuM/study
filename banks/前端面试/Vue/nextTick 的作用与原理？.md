---
题目: "nextTick 的作用与原理？"
分类: Vue
频率: 低频
id: 385e29bd-9121-8183-a45a-fc6e3616d4a8
---
nextTick：在下一次 DOM 更新完成后执行回调。

Vue 的响应式更新是异步批量的：同一 tick 内多次改数据只触发一次渲染；要拿到更新后的 DOM 需用 nextTick。Vue3 的 nextTick **基于 Promise 微任务实现，没有宏任务降级**；Vue 2.6 起也始终使用微任务（2.5.x 曾短暂用 MessageChannel/setTimeout 回退，因 bug 被回退）。
