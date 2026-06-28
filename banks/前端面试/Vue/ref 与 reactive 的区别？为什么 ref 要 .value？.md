---
题目: "ref 与 reactive 的区别？为什么 ref 要 .value？"
分类: Vue
频率: 高频
id: 385e29bd-9121-8113-9606-c563c2ac7fa0
禁用: true
---
- ref：包裹任意值（常用于原始类型），访问/修改需 `.value`，模板中自动解包；它通过自身的 getter/setter（`.value` 访问器）做依赖追踪，**不是靠 Proxy**。
- reactive：只能用于对象/数组，返回 Proxy 代理。

为什么 ref 要 `.value`：JS 无法直接拦截原始值的读写，用对象包一层（`{ value }`）才能在 get/set 时 track/trigger。reactive 整个变量重新赋值会丢响应式，常用 ref 或 `Object.assign`。
