---
题目: "Bind\\Call\\Apply 的优先级和原因？"
分类: JS
频率: 低频
id: cc788a3a-033d-4c33-8eca-5c94882331bf
---
三者都用于改变函数的 this：

- call(thisArg, 参数列表)：立即执行。
- apply(thisArg, 参数数组)：立即执行。
- bind(thisArg)：返回一个 this 已固定的新函数，延迟执行。

优先级：bind 绑定后，再用 call/apply 也无法改变其 this（bind 内部用闭包+apply 固定）；但 new 调用 bind 返回的函数时，this 指向新实例（new 优先级高于 bind）。

## 追问

### bind 锁死的 this 是绝对不能改的吗？有没有办法突破？

有且只有一种办法：用 `new` 调用这个被 bind 过的函数。ES5 规范里，`bind` 返回的函数如果作为构造函数被 `new` 调用（内部走的是 `[[Construct]]`，而不是普通调用的 `[[Call]]`），会直接创建一个新对象作为 this，完全忽略 bind 时固定的 thisArg。这是刻意设计的：bind 常被用来做"构造函数的偏函数应用"（预先绑定部分参数，留到 `new` 时再实例化），如果 `new` 也无法突破绑定，这类用法就废了。而 `call`/`apply` 没有这个特权——它们只是普通函数调用，永远无法覆盖 bind 锁死的 this。

```js
function Foo(x) { this.x = x; }
const BoundFoo = Foo.bind({ fake: true }, 1);
const obj = {};
BoundFoo.call(obj);       // 无效，this 依然是 {fake:true} 绑定的那个对象
new BoundFoo();            // 有效，this 指向新创建的实例，跟 {fake:true} 无关
```

## 发展史（问题 → 方案的链条）

**❓ `call`/`apply`（ECMAScript 第 1 版，1997 年）只能在调用瞬间指定 this，但很多场景需要"提前定好 this，延迟到以后再调用"（典型如 `setTimeout` 回调、DOM 事件监听器）**
call/apply 只解决了"调用时手动指定 this"，解决不了"回调函数被别的机制在未来某个时刻调用、但那时的 this 已经不是我想要的那个"这个问题。2000 年代中期的开发者普遍写 `var self = this;` 这种手动闭包保存法来绕过它，Prototype.js、jQuery、Dojo 等库都各自造了一个近似 `bind` 的辅助函数来封装这个模式。

**✅ ES5（2009 年 12 月）把这个民间模式收编为标准方法 `Function.prototype.bind`**
`bind` 返回一个新函数，内部用闭包把 thisArg（以及可选的预置参数）永久锁住，之后无论这个新函数被怎么调用，this 都不会再变——从语言层面终结了"手写 `var self = this`"这种模式。

**❓ 函数在 JS 里既能被普通调用，也能被 `new` 当构造函数调用——bind 返回的东西还是一个函数，如果被 `new`，锁死的 this 应该继续生效，还是让 `new` 的"造实例"语义接管？**
如果锁死的 this 强到连 `new` 都突破不了，那 bind 就没法用来做"预置部分参数的构造函数"（ES5 规范文档本身举的 bind 应用场景之一就是这种构造函数的偏函数应用），`new` 出来的对象也会离奇地共享同一个被锁死的 this，完全违背 `new` 本该"每次都造一个全新实例"的语义。

**✅ ES5 规范明确区分 `[[Call]]`（普通调用）与 `[[Construct]]`（`new` 调用）两条路径，bind 返回函数的 `[[Construct]]` 内部逻辑直接忽略锁死的 thisArg，改用 `new` 新建的实例**
这样 bind 过的函数依然能正常拿去 `new`，且行为符合"每次 new 都造独立实例"的直觉；只有 call/apply 这种走 `[[Call]]` 路径的调用方式才会被 bind 锁死的 this 挡住。

**现状：call/apply 之间没有优先级、只是传参形式不同（列表 vs 数组）；bind 锁死 this 且能挡住 call/apply，但唯独挡不住 new——这是刻意为构造函数场景留的口子，不是遗漏**

## 参考资料

- [MDN — Function.prototype.bind()](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Function/bind)
- [MDN — new 运算符](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/new)
