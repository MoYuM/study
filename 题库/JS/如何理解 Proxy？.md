---
题目: "如何理解 Proxy？"
分类: JS
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: 100e29bd-9121-80b4-8ea0-c95b905972d9
备注: ""
---
Proxy 是 ES6 提供的对象代理，可拦截 13 种操作（get/set/has/deleteProperty/ownKeys 等）。

Vue3 用它做响应式，相比 `Object.defineProperty` 的优势：能监听属性新增/删除、数组索引与 length、Map/Set，且惰性代理（用到才递归）无需初始化时深度遍历。

局限：不兼容 IE；深层对象仍需递归代理；无法代理原始值（要用 ref 包装）。
