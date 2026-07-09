---
题目: "for...in 与 for...of 的区别？"
分类: JS
频率: 低频
id: 385e29bd-9121-8114-b1cb-f46be1910a8e
---
- `for...in`：遍历可枚举属性「键」（含原型链，顺序不保证），适合普通对象。
- `for...of`：遍历可迭代对象的「值」（需 `Symbol.iterator`），适合数组/Map/Set，不遍历原型。普通对象需自实现迭代器才能用 for...of。

## 追问

### for...of 能直接用在普通对象 `{ a: 1 }` 上吗？为什么？

不能，直接用会抛 `TypeError: xxx is not iterable`。for...of 依赖**迭代器协议**：只有实现了 `[Symbol.iterator]()` 方法（调用后返回一个具备 `next()` 方法、每次返回 `{ value, done }` 的迭代器对象）的值才能被 for...of 消费。Array、String、Map、Set、arguments、DOM NodeList、Generator 返回值都内置了这个方法，普通对象字面量默认没有。想让普通对象支持 for...of，需要手动给它加上 `[Symbol.iterator]`：

```js
const obj = {
  a: 1, b: 2,
  [Symbol.iterator]() {
    const values = Object.values(this);
    let i = 0;
    return { next: () => i < values.length ? { value: values[i++], done: false } : { value: undefined, done: true } };
  }
};
for (const v of obj) console.log(v); // 1 2
```

## 发展史（问题 → 方案的链条）

**❓ `for...in`（ES1 就有）会连着原型链上的可枚举属性一起遍历，用来遍历数组还会把索引当字符串键处理，行为对"只想拿到值"的场景很不友好**
早期 JS 只有 `for...in` 这一种遍历语法，本意是枚举对象的属性键。但把它套在数组或需要"只要值"的场景上，会带出原型链上继承来的可枚举属性（尤其是给 `Array.prototype`/`Object.prototype` 挂过自定义方法的老代码里很容易踩雷），键还是字符串形式的索引而不是数值，语义上也拧巴。

**✅ ES6（2015）引入统一的「迭代协议」：`Symbol.iterator`**
规范定义了"可迭代对象"的标准：只要一个值实现了 `[Symbol.iterator]()` 方法、返回符合 `{ next(): {value, done} }` 形状的迭代器，它就是可迭代的。Array、String、Map、Set、arguments 等内置类型统一在语言层面实现了这个协议。

**❓ 光有协议还不够，需要一个专门语法来消费"可迭代对象"，而且不能重蹈 `for...in` 会牵扯原型链的覆辙**
仅仅规定协议本身不能自动带来一种干净的遍历方式，还需要在语法层面提供入口，且要明确不去碰对象的原型链（避免重复 for...in 的老问题）。

**✅ 同在 ES6（2015）引入 `for...of` 语句**
`for...of` 只消费实现了迭代协议的值，逐个取出 `value`，完全不涉及键、也不遍历原型链——Map/Set 这类 ES6 新增的数据结构从设计之初就实现了该协议，天然可以被 `for...of` 遍历，而这是 `for...in` 做不到的。

**现状：`for...in` 保留给"枚举对象的键"（含原型链，ES1 遗留语义不变），`for...of` 是"迭代可迭代对象的值"的现代通用方式（需显式实现协议，不碰原型链）——记混的根源在于把"键 vs 值"和"含不含原型链"这两条正交的区别混成了一条**

## 参考资料

- [MDN — Iteration protocols](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Iteration_protocols)
- [MDN — for...of](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/for...of)
- [MDN — for...in](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/for...in)
