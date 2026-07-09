---
题目: "let const var 的区别"
分类: JS
频率: 低频
id: 10ae29bd-9121-803a-a494-d8e28c58c4ec
---
- var：函数作用域、有变量提升（提升为 undefined）、可重复声明；非严格模式下全局 var 会挂到 window（注意 ES Module 顶层 var 不挂 window）。
- let：块级作用域、存在暂时性死区（TDZ）、不可重复声明。
- const：块级作用域、必须声明即初始化；其「绑定」不可重新赋值，但若是对象/数组，内部属性仍可修改（并非不可变）。

实践：优先 const，需要重新赋值用 let，避免 var。

## 追问

### let/const 到底有没有变量提升？

**有**，这是最容易记混的一点。三者的声明在进入作用域时都会被"处理"（登记到当前作用域的环境记录里），区别只在于登记后的初始状态：
- `var` 登记后立刻可用，值是 `undefined`，所以"提前访问"不报错、只是拿到 `undefined`——这才是"var 有提升"给人的直观印象。
- `let`/`const` 登记后进入**暂时性死区（TDZ, Temporal Dead Zone）**：绑定已经存在，但处于"未初始化"状态，从进入作用域开始到真正执行到声明语句这段区间内，访问它会直接抛 `ReferenceError`，而不是拿到 `undefined`。

```js
console.log(a); // undefined（var 提升，可用但值是 undefined）
var a = 1;

console.log(b); // ReferenceError: Cannot access 'b' before initialization（TDZ）
let b = 1;
```
说"let/const 没有提升"是把"提升"狭义地等同于"提升后能被正常访问"，但按规范定义，绑定本身确实在作用域开始时就创建了，只是访问权限被 TDZ 挡住。

## 发展史（问题 → 方案的链条）

**❓ ES1（1997 年）开始 JS 只有 `var`，只有函数作用域，没有块级作用域——`if`/`for` 里的 `{}` 不会像 C/Java 那样开辟新作用域**
习惯了 C/Java 的开发者写 `if (x) { var y = 1; } console.log(y)`，会惊讶 `y` 在块外依然能访问到；更经典的坑是 `for (var i = 0; i < 3; i++) setTimeout(() => console.log(i))`——三个回调打印的都是最终值 `3`，因为循环体内外共用同一个 `i`，不是每次迭代独立一份。

**✅ TC39 决定给 JS 补上真正的块级作用域，但不能改 `var` 本身的语义（大量存量代码依赖它）——于是新增两个关键字 `let`/`const`，随 ES6（2015 年）落地**
不修改 `var`，而是新增关键字，是保证向后兼容的常规做法：老代码里的 `var` 行为分毫不变，`let`/`const` 只在新代码里生效块级作用域。`const` 同时解决了另一件事：此前只能靠命名约定（如全大写）表达"这个变量不该被重新赋值"，现在有了语言层面强制的绑定不可变。

**❓ 块级作用域意味着 `let`/`const` 声明的变量只在自己的块里"存在"，但如果完全照搬 `var` 的提升语义（提升后可用、值是 undefined），会重新制造"声明前使用却不报错、静默拿到 undefined"这个 var 早就被诟病的坑**
如果 `let x; ...; x = 1;` 提升后跟 `var` 一样能在声明前正常访问到 `undefined`，那本质上又绕回了 var 那种"用了没声明的变量也不报错"的宽松行为，没有解决"提前使用未初始化变量"这个真实存在的 bug 来源。

**✅ 规范引入「暂时性死区」（TDZ）：绑定在进入作用域时就创建（这一点和提升一致），但保持"未初始化"状态直到执行到声明语句，期间访问直接抛 ReferenceError**
这样"作用域开始时绑定就已存在"（技术上仍是提升）和"声明前访问必须报错、不能静默放行"（修复 var 的老毛病）两个目标同时达成——TDZ 不是"取消提升"，而是"提升了但故意锁住，逼你在真正赋值前不能用"。

**现状：`var`（函数作用域 + 提升后即可用，ES1 遗留、为兼容保留）与 `let`/`const`（块级作用域 + 提升到 TDZ、声明前访问直接报错）并存——"有没有提升"不是两者的区别，"提升后能不能立刻用"才是**

## 参考资料

- [MDN — let](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/let)（含 Temporal dead zone 一节）
- [MDN — const](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/const)
- [TC39 — ECMAScript® 2015 Language Specification](https://www.ecma-international.org/ecma-262/6.0/)
