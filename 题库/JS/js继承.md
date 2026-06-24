---
题目: "js继承"
分类: JS
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: 120e29bd-9121-8051-9f68-c3f293f67972
备注: ""
---
- 原型链继承：子类原型指向父类实例，缺点是引用类型属性被共享。
- 构造函数继承：子类构造里 [Parent.call](http://Parent.call)(this)，解决共享但无法继承原型方法。
- 组合继承：call + 原型，常用但父构造被调用两次。
- 寄生组合继承（ES6 之前的最优方案）：Child.prototype = Object.create(Parent.prototype) 修正构造指向，避免两次调用。
- ES6 class extends 是原生子类化机制，与寄生组合相似但不等价：super() 前 this 处于 TDZ、实例由基类先分配、方法默认不可枚举、必须 new 调用、且能正确继承内建对象（如 Array）。
