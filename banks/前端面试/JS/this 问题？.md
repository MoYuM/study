---
题目: "this 问题？"
分类: JS
频率: 低频
id: 73851fc5-cdba-4045-aafa-3a7078400800
---
this 取决于函数的调用方式：

1. 默认绑定：独立调用，非严格模式指向全局对象，严格模式为 undefined。
2. 隐式绑定：`obj.fn()`，this 指向 obj。
3. 显式绑定：`call` / `apply` / `bind` 指定 this。
4. new 绑定：构造函数中 this 指向新建实例。
5. 箭头函数：没有自己的 this，继承外层词法作用域的 this，且无法被 call/bind 改变。

优先级：new > 显式绑定 > 隐式绑定 > 默认绑定。
