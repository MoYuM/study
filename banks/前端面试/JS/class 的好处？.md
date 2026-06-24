---
题目: "class 的好处？"
分类: JS
频率: 低频
id: 10ae29bd-9121-80c3-8c0d-d5f5d75526d6
---
class 是原型继承的语法糖，好处：

- 语义清晰、结构化（constructor、方法、static、getter/setter）。
- extends / super 让继承更直观。
- 方法默认不可枚举；类体默认严格模式。
- 必须 new 调用（防止漏 new），存在暂时性死区不会变量提升。
- 支持私有字段 `#x`。

本质仍是基于原型，方法挂在 prototype 上。
