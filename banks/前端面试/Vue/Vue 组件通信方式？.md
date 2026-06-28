---
题目: "Vue 组件通信方式？"
分类: Vue
频率: 高频
id: 385e29bd-9121-817e-96b2-c4ec08117b74
禁用: true
---
- 父子：props 下发、`$emit` 上传（v-model）。
- 跨级：provide / inject。
- 全局：Vuex / Pinia。
- 兄弟/任意：EventBus / mitt、公共状态。
- 模板引用：`ref` / `$parent` / `$refs`。

兄弟通信的前提是有公共父组件或全局总线。
