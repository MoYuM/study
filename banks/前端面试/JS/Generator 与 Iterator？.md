---
题目: "Generator 与 Iterator？"
分类: JS
频率: 低频
id: 385e29bd-9121-81ac-b33c-eb300d2efda9
---
- Iterable（可迭代）：实现了 `[Symbol.iterator]()` 方法、调用后能产出一个 Iterator 的对象——Array/String/Map/Set 都是内置的 Iterable。
- Iterator（迭代器）：具有 `next()` 方法、每次调用返回 `{value, done}` 的对象，符合迭代协议。
- Generator：用 `function*` + `yield` 写的函数，调用后返回的对象**同时是 Iterator 又是 Iterable**；函数体不会立即执行，靠外部反复调用 `next()` 才会往下走，每个 `yield` 都会暂停并把值抛给调用方，同时接收下次 `next(x)` 传入的 x 作为这次 yield 表达式的值（双向通道）。

```js
function* gen() {
  const a = yield 1;
  const b = yield 2;
  return a + b;
}
const it = gen();
it.next();     // { value: 1, done: false }
it.next(10);   // { value: 2, done: false }，yield 1 的值变成 10
it.next(20);   // { value: 30, done: true }，yield 2 的值变成 20，return 30

// 返回值同时是 Iterable，可以直接 for...of / 展开
function* range(a, b) { for (let i = a; i <= b; i++) yield i; }
[...range(1, 3)]; // [1, 2, 3]
```

用途：惰性求值（无限序列按需取值，`while(true) yield n++` 不会卡死，因为每次 yield 都真正让出控制权）；异步流程控制（`yield` 一个 Promise，配合外部"自动执行器"在 resolve 后自动调用 `next()`——这正是 async/await 出现之前，`co` 等库实现"用同步写法写异步代码"的原理）。

## 追问

### Iterable 和 Iterator 具体怎么区分？

**Iterable(可迭代)** 是"可以被迭代的东西"——只要实现了 `[Symbol.iterator]()` 方法即可，调用这个方法会返回一个 Iterator。**Iterator(迭代器)** 是"真正在迭代的那个对象本身"——有 `next()` 方法，每次调用推进一步、返回 `{value, done}`。Array 本身是 Iterable（`arr[Symbol.iterator]` 存在），但 Array 本身不是 Iterator（`arr.next` 不存在）；调用 `arr[Symbol.iterator]()` 拿到的那个东西才是 Iterator。Generator 函数调用后返回的对象比较特殊，**同时满足两者**：它自己有 `next()`（是 Iterator），它的 `[Symbol.iterator]()` 又返回自身（是 Iterable），这也是它既能被 `for...of` 直接消费、又能手动调 `next()` 精细控制执行的原因。

## 发展史（问题 → 方案的链条）

**❓ ES6（2015）之前，写"看起来像同步代码"的异步流程只能靠回调地狱或 Promise 链式 `.then`，函数一旦暂停等待异步结果、再恢复执行，语言层面完全没有"暂停-恢复"这种控制流原语**
无论回调还是 Promise，本质都是"注册一个未来会被调用的函数"，写法上永远是"往前"的，没法像同步代码一样在某一行"等一下"再往下走。

**✅ ES6（2015）在引入迭代协议（`Symbol.iterator`）的同时，也引入了 Generator（`function*`/`yield`）——语言第一次拥有了真正的"暂停并让出控制权，之后还能从原地恢复"的执行原语**
Generator 最初的设计目的是配合迭代协议实现自定义可迭代对象（不用手写 `next()`/`{value,done}`），但社区很快发现它的"暂停-恢复"能力可以拿来解决异步流程的写法问题：如果把 `yield` 后面接一个 Promise，再写一个"自动执行器"在 Promise resolve 后自动调用 `next()`，就能让异步代码"看起来"像同步代码一样一行行往下写。

**❓ 这个"自动执行器"是纯手写的，每个用 Generator 写异步流程的项目都得自己造一个或依赖第三方库**
TJ Holowaychuk 2013 年发布的 `co` 库（Node.js 社区广为使用）把这套"Generator + Promise + 自动执行器"的模式封装成了标准做法，redux-saga 等库也建立在同样的原理上；但终究是用户态代码在模拟语言特性，写法上还是要套一层 `co(function*(){...})`，不是原生语法。

**✅ ES2017（ECMAScript 2017，第 8 版）把这套模式正式收编为原生语法 `async`/`await`**
`async function` 本质就是「Generator + Promise 自动执行器」被语言原生化：`await` 等价于 `yield` 一个会被自动 resolve 并恢复执行的 Promise，只是不再需要用户手写 `co` 这样的驱动函数，引擎内置了这个"自动执行器"。

**现状：Generator 依然承担"迭代协议的手动实现工具"和"更底层的暂停-恢复原语"两个角色；async/await 是 Generator 在"异步流程"这一个具体场景下被语言原生化、去掉手写执行器负担后的产物——日常业务代码里 async/await 已经覆盖了 Generator 当年在异步场景里的大部分用途**

## 参考资料

- [MDN — function*](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/function*)
- [MDN — Iteration protocols](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols)
- [TJ Holowaychuk — co（GitHub）](https://github.com/tj/co)
