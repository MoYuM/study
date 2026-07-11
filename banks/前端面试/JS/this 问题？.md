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

## 追问

### 独立调用一个普通函数（不在任何对象上调用），this 到底是什么？

**非严格模式**下指向全局对象（浏览器里是 `window`）；**严格模式**下是 `undefined`——这是常被漏掉的一半：不加限定说"独立调用 this 指向全局"只对了一半，严格模式（包括 ES Module、class 内部默认严格模式）下会直接是 `undefined`，访问 `this.xxx` 会抛 `TypeError`。

### 箭头函数为什么"无法被 call/bind 改变"？跟前面四种绑定规则是什么关系？

因为箭头函数**根本没有自己的 this 绑定这个内部机制**——普通函数在被调用时，引擎会为这次调用单独确定一份 this（走默认/隐式/显式/new 这四种规则之一，取决于怎么调用它）；箭头函数则完全没有这个"每次调用重新确定 this"的步骤，它的 this 在定义时就直接沿用外层作用域的 this 并永久固定。`call`/`apply`/`bind` 传入的 thisArg 对箭头函数是无效的——不是"被忽略"，而是箭头函数压根没有可供这几个方法操作的 this 槽位。所以箭头函数不参与前面四种规则的优先级仲裁，它是跳出这套体系之外的第五种情况。

### 补充：以上"五种规则+优先级"是简化框架，MDN 真实是怎么分类的？

"五种规则+优先级"是业界流行的教学简化框架（源自 Kyle Simpson《You Don't Know JS》），方便记但不是 MDN/规范的原始分类。MDN 按「函数上下文 / 类上下文 / 全局上下文」组织，大部分场景（DOM 事件监听器里 this 绑定到元素、getter/setter 里 this 绑定到"正在访问属性的对象"）本质还是隐式绑定的变体，但有几个框架完全没覆盖到的独立机制：

### 非严格模式下，如果调用时 this 会是 undefined/null 或一个原始值，实际发生什么？

"默认绑定：非严格模式指向全局对象"这句话简化了一层，真实机制叫「this 替换」——非严格模式下函数体内的 this 必须是一个对象：
- 调用时 this 会是 `undefined`/`null` → 替换成 `globalThis`。
- 调用时 this 会是一个**原始值**（数字/字符串/布尔值）→ 替换成对应的包装对象（`Number`/`String`/`Boolean` 实例）。

```js
function bar() { console.log(Object.prototype.toString.call(this)); }
bar.call(7);      // [object Number]，不是原始值 7 本身
bar.call("foo");  // [object String]
```

### 全局作用域顶层的 this 是什么？

这不是"函数怎么被调用"能解释的——**全局上下文的 this 取决于代码跑在什么容器里**，是和前面四种规则完全独立的一层：

| 运行环境 | 顶层 this |
|---|---|
| 普通 `<script>` 脚本（不管严格/非严格模式） | `globalThis`（浏览器里是 `window`） |
| ES Module（`<script type="module">`） | `undefined` |
| Node.js CommonJS 模块 | `module.exports`（不是全局对象） |

容易踩的坑：普通脚本顶层加了 `'use strict'` 之后 this **依然是** `globalThis`，不会变成 `undefined`——顶层 this 绑定和"函数内部默认绑定受严格模式影响"是两条独立的规则。

### 用 extends 继承出来的子类（派生类），constructor 里的 this 什么时候才能用？

必须先调用 `super()`，之前访问 this 会直接报错——这是 let/const 那道题学过的 **TDZ 机制在 this 绑定上的又一次复用**。基类构造函数一调用 this 就绑定好了，但派生类构造函数没有初始的 this 绑定，`super()` 执行的效果大致相当于 `this = new Base()`：

```js
class Bad extends Base {
  constructor() {} // 忘了调用 super()
}
new Bad(); // ReferenceError: Must call super constructor in derived class before accessing 'this'...
```

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
