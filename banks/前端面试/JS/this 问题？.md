---
题目: "this 问题？"
分类: JS
频率: 低频
id: 73851fc5-cdba-4045-aafa-3a7078400800
---
this 的值取决于它出现的**上下文**：函数、类、全局——这是 MDN 的原始分类方式，比"五种绑定规则"更完整（五规则是业界流行的教学简化框架，源自 Kyle Simpson《You Don't Know JS》，方便记但只覆盖了"函数上下文"这一支）。

## 函数上下文（this 是调用时才确定的隐藏参数）

- **隐式绑定**：`obj.fn()` 调用形式，this 指向 obj。
- **this 替换**（非严格模式专属）：调用时 this 会是 `undefined`/`null` → 替换成 `globalThis`；会是原始值（数字/字符串/布尔值）→ 替换成对应包装对象（`Number`/`String`/`Boolean` 实例）。严格模式下不替换，直接是 `undefined`。
- **回调函数**：this 由 API 实现者决定——默认以 `undefined` 调用（非严格模式下即变 `globalThis`，如 `[1,2,3].forEach(fn)`）；部分 API 提供 `thisArg` 参数（`forEach` 第二参数）；少数 API 主动设置 this（`JSON.parse` 的 reviver）。
- **显式绑定**：`call`/`apply`/`bind` 手动指定 this；`bind` 返回的新函数 this 永久锁定，唯一能突破的是用 `new` 调用它（见「Bind\Call\Apply 的优先级和原因」）。
- **箭头函数**：没有自己的 this 绑定机制，词法继承外层作用域的 this，`call`/`apply`/`bind` 传的 thisArg 对它无效。
- **构造函数（new）**：this 绑定到新创建的实例；但若构造函数显式 `return` 了另一个非原始值，这个新实例会被丢弃，this 的值不再是 new 表达式的结果。
- **`super.method()`**：method 内部的 this 与外围调用处的 this 相同，不等于 `super` 指向的父类原型对象——特殊语法，不能按"看点前面是谁"的直觉去推。

**这几种绑定规则之间的优先级**（只在函数被显式调用时才谈得上排序，不含全局/类上下文）：`new > 显式绑定 > 隐式绑定 > 默认绑定（含 this 替换）`；箭头函数完全不参与这个优先级仲裁。

## 类上下文（先分「静态 / 实例」两个子上下文）

- **实例上下文**（constructor / 方法 / 实例字段初始化器）：this = 类的实例。
- **静态上下文**（static 方法 / 静态字段 / 静态初始化块）：this = 类本身。
- **派生类（extends）构造函数**：没有初始 this 绑定，`super()` 之前访问 this 直接报错（TDZ，和 let/const 那道题是同一套机制的复用），`super()` 执行的效果约等于 `this = new Base()`。

## 全局上下文（不是"调用方式"决定的，是"代码跑在哪个容器里"决定的）

| 运行环境 | 顶层 this |
|---|---|
| 普通 `<script>` 脚本（不管严格/非严格模式） | `globalThis` |
| ES Module（`type="module"`） | `undefined` |
| Node.js CommonJS 模块 | `module.exports`（不是全局对象） |
| `eval` 执行 | 直接调用跟外层 this 相同；间接调用等于 `globalThis` |

对象字面量本身不开 this 作用域，只有函数（方法）才会——对象字面量里裸写的 this 继承自外围作用域。容易踩的坑：普通脚本顶层加了 `'use strict'` 之后 this **依然是** `globalThis`，不会变成 `undefined`——顶层 this 绑定和"函数内部默认绑定受严格模式影响"是两条独立的规则。

## 两个常被漏记的"寄生"情况（本质是函数上下文里"回调"的变体）

- **getter/setter**：this 绑定到"正在访问属性的那个对象"，不是定义这个属性的对象。
- **DOM 事件监听器**（`addEventListener`）/ 内联 `onclick`：this 绑定到监听器所在的 DOM 元素。

## 追问

### 箭头函数为什么"无法被 call/bind 改变"？

因为箭头函数根本没有自己的 this 绑定这个内部机制——普通函数在被调用时，引擎会为这次调用单独确定一份 this（走上面函数上下文里的某条规则）；箭头函数完全没有这个"每次调用重新确定 this"的步骤，它的 this 在**定义时**就直接沿用外层作用域的 this 并永久固定。`call`/`apply`/`bind` 传入的 thisArg 对箭头函数无效——不是"被忽略"，而是箭头函数压根没有可供这几个方法操作的 this 槽位。

## 发展史（问题 → 方案的链条）

**❓ ES1（1997 年）起，this 只有默认/隐式/显式/new 这四种"运行时根据调用方式动态决定"的规则——回调函数被框架/浏览器在未来某个时刻调用时，this 早已不是定义时那个 this 了（典型如 DOM 事件监听器、`setTimeout`、数组遍历回调），这是长期被吐槽的痛点**
写 `obj.method = function(){ this.x }`，一旦这个方法被当作回调传出去单独调用（比如 `setTimeout(obj.method, 100)`），this 就丢了，变成默认绑定（严格模式 undefined，非严格模式全局对象），完全不是开发者想要的 `obj`。

**✅ ES5（2009 年）给出的方案是 `Function.prototype.bind`：调用时显式指定 this，返回一个 this 已被永久锁定的新函数（细节见 Bind\Call\Apply 那道题的发展史）**
`setTimeout(obj.method.bind(obj), 100)`——本质还是"运行时动态决定 this"这套体系内的一种规则（显式绑定），只是把绑定的时机从"调用瞬间"提前到了"生成新函数的时候"。

**❓ `bind` 解决了问题，但每次传回调都要手写 `.bind(this)`，模板代码啰嗦、容易漏写（React/Backbone 时代 class 组件构造函数里成排的 `this.handleClick = this.handleClick.bind(this)` 是这个问题最典型的历史见证）**
需要一种更彻底、不用每次手动绑定的写法。

**✅ ES6（2015）引入箭头函数，除了追求简洁语法，也明确把"不创建自己的 this、定义时直接继承外层词法作用域的 this"作为设计目标之一，从根上避免"运行时决定 this"这套机制导致的丢失问题**
箭头函数用的是另一条完全不同的路径——不是运行时根据调用方式动态决定（这也是它无法被 call/apply/bind 强改的原因，因为压根没有这个动态决定的步骤），而是定义时词法作用域直接继承、永久固定，class 组件里 `handleClick = () => { this.x }` 这种箭头函数写法后来基本取代了构造函数里手写 bind 的模式。

**现状：默认/隐式/显式/new 这四种规则共享同一套"运行时按调用方式动态决定"的机制，彼此之间才谈得上优先级（new > 显式 > 隐式 > 默认）；箭头函数是解决"回调丢 this"这同一个历史问题的另一条路径（定义时词法继承），完全不参与这套优先级仲裁，问"箭头函数优先级排第几"本身就是问错了问题**

## 参考资料

- [MDN — this](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/this)
- [MDN — Arrow function expressions](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Functions/Arrow_functions)
