---
题目: "computed 与 watch 的区别与原理？"
分类: Vue
频率: 高频
id: 385e29bd-9121-811e-8454-da5693d48bc0
---
- computed：基于响应式依赖缓存，依赖不变不重算，适合派生值。
- watch：监听源变化执行副作用（异步、调接口），可 deep/immediate。

原理：computed 是惰性求值的 effect + 缓存标记；watch 为每个源创建 Watcher/effect，变化时触发回调。能用 computed 就不用 watch。
