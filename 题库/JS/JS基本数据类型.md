---
题目: "JS基本数据类型"
分类: JS
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: 427cc92e-c981-43e2-b3cd-a29a1252eba2
备注: ""
---
7 种原始类型：string、number、boolean、null、undefined、symbol、bigint；外加引用类型 object（含 Array/Function 等）。

- 原始类型按值存储在栈、引用类型存堆、变量存引用地址。
- 判断：typeof（注意 `typeof null === 'object'` 是历史 bug，`typeof function === 'function'`）；精确判断用 `Object.prototype.toString.call()`。
