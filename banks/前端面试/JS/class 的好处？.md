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

## 追问

### class 定义的构造函数，忘记加 new 直接调用会发生什么？跟传统 function 构造函数忘加 new 相比有什么不同？

**class 会直接报错**：`TypeError: Class constructor Foo cannot be invoked without 'new'`——调用瞬间就失败，问题第一时间暴露。

**传统 function 构造函数忘加 new 则是静默的隐蔽 bug**：`this` 不会指向新实例，而是退化成普通函数调用的 this——严格模式下 `this` 是 `undefined`（后续访问 `this.xxx` 才报错，报错点已经偏离真正的问题根源），非严格模式下 `this` 指向全局对象（`window`/`globalThis`），会悄悄把本该挂在实例上的属性挂到全局对象上，完全不报错，只在后续某个不相关的地方才会看出数据不对劲，排查成本很高。

```js
function Foo(x) { this.x = x; }
Foo(1);           // 非严格模式：无报错，window.x = 1（悄悄污染全局）
class Bar { constructor(x) { this.x = x; } }
Bar(1);            // 立即抛 TypeError: Class constructor Bar cannot be invoked without 'new'
```

## 发展史（问题 → 方案的链条）

**❓ ES6 之前，JS 的"类"完全靠函数 + 手动挂 prototype 模拟，业界公认这套写法有三个反复被抱怨的坑**
- 忘记 `new` 直接调用构造函数：`this` 静默指向全局对象（非严格模式）或 `undefined`（严格模式），不报错，bug 很晚才暴露。
- 继承样板代码繁琐易错：得手写 `Child.prototype = Object.create(Parent.prototype)`、修回 `constructor`、在子构造函数里手动 `Parent.call(this, ...)`，四五行样板代码任何一步漏了都很难一眼看出。
- `Foo.prototype.method = function(){}` 这种写法赋出来的方法默认可枚举，会意外出现在 `for...in`/`Object.keys` 遍历结果里。

**✅ 业界在语言层面补丁之前，先用编译到 JS 的方式自己造了"类"语法——最有代表性的是 2009 年发布的 CoffeeScript，其 `class`/`extends` 关键字编译出来的正是上面那套手写原型样板**
CoffeeScript 证明了开发者对"class 语法糖"的真实需求早已存在多年，且验证了一套可行的语法设计（`class`、`extends`），这也是 TC39 后来设计 ES6 class 提案时公开参考的先例之一。

**✅ ES6（2015 年）把这套语法收编为原生 `class`/`extends`/`super` 关键字，针对性地堵住上面三个坑**
调用 class 构造函数忘 `new` 直接抛 `TypeError`（fail-fast，而不是静默污染全局）；`extends`/`super` 由引擎自动完成原型链接和父构造函数调用，样板代码消失；class 语法定义的方法默认不可枚举，不会再意外出现在遍历结果里；类体还默认是严格模式。

**❓ class 把"怎么组织方法、怎么继承"的语法问题解决了，但 JS 对象成员依然没有真正的私有性——`_foo` 这种下划线前缀只是命名约定，外部照样能读写**
即便用了 class，字段封装也只能靠约定（`this._foo`）或额外套一层闭包（模块模式）来"假装私有"，没有语言层面强制的访问限制，团队协作时约定很容易被破坏。

**✅ ES2022（2022 年）新增私有字段/方法语法 `#x`，是真正被引擎强制拒绝外部访问的私有成员，不是约定**
`class Foo { #secret = 1; getSecret() { return this.#secret; } }`，外部代码访问 `foo.#secret` 直接是语法错误，而不是"能访问但不建议"——这是 class 语法在原有基础上又晚了 7 年补上的真正封装能力。

**现状：class 本质仍是原型继承的语法糖（方法依然挂在 `prototype` 上，`instanceof` 判断规则不变），它解决的是"手写原型模式"里三个反复被吐槽的老坑（忘 new、继承样板、方法误枚举），私有字段 `#x` 则是后来单独追加、真正意义上的封装能力**

## 参考资料

- [MDN — Classes](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Classes)
- [MDN — Private class features](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Classes/Private_properties)
