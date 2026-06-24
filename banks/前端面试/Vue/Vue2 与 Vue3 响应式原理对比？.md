---
题目: "Vue2 与 Vue3 响应式原理对比？"
分类: Vue
频率: 高频
id: 385e29bd-9121-81c1-bdec-c53fde29e361
---
- Vue2：`Object.defineProperty` 劫持属性 getter/setter，初始化递归遍历；无法检测属性新增/删除、数组索引/length（需 Vue.set / 重写数组方法）。
- Vue3：`Proxy` 代理整个对象，惰性递归（用到才代理），能检测新增/删除、数组、Map/Set；配合 effect/track/trigger 做依赖收集。性能与完整性都更好。

## 参考资料

- [Vue 官方 — 深入响应式系统](https://cn.vuejs.org/guide/extras/reactivity-in-depth.html)
