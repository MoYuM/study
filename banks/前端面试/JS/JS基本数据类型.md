---
题目: "JS基本数据类型"
分类: JS
频率: 低频
id: 427cc92e-c981-43e2-b3cd-a29a1252eba2
---
7 种原始类型：string、number、boolean、null、undefined、symbol、bigint；外加引用类型 object（含 Array/Function 等）。

- 原始类型按值存储在栈、引用类型存堆、变量存引用地址。
- 判断：typeof（注意 `typeof null === 'object'` 是历史 bug，`typeof function === 'function'`）；精确判断用 `Object.prototype.toString.call()`。

## 发展史（问题 → 方案的链条）

**❓ 1995 年 Brendan Eich 在 Netscape 用约 10 天写出 JS 最初原型（先叫 Mocha，同年 9 月改名 LiveScript，12 月因 Netscape 与 Sun 结盟改名 JavaScript），最初的实现里每个值用"类型标签 + 数据"的方式表示（tagged union）——对象的标签是二进制 `000`，而 `null` 被实现成机器层面的空指针（全 0），取标签位后恰好也是 `000`，`typeof` 没有对 `null` 做特判**
`typeof null` 因此返回了 `"object"`——这本是实现层面的一个巧合，不是设计如此。

**❓ 1997 年 ES1（ECMA-262 第一版，定义了 Undefined/Null/Boolean/String/Number/Object 共 6 种类型）把已有实现的这套行为原封不动写进规范固化下来**
`typeof null === 'object'` 这个巧合也跟着被写进规范，从"实现细节"变成了"语言标准"。

**❓ 后来 TC39 委员会不是没想过修——es-discuss 邮件列表上确实讨论过让 `typeof null` 返回 `"null"`，但这会破坏使用 `typeof x === 'object'` 判断的海量现有网页代码**
"不能破坏 The Web"是 TC39 的铁律，收益太小、风险太大，这个修复提案最终被否决。

**✅ 现状是：`typeof null === 'object'` 从 1995 年的实现巧合，变成了一个永久保留的语言历史遗留特征——没有"修复"，只有绕过（判断 `null` 要用 `=== null`，不能靠 `typeof`）**

**❓ 6 种类型用了很多年，但框架和库越来越多之后，同一个对象上不同库各自扩展属性，字符串属性名容易互相冲突；同时需要一种"协议"机制（比如让自定义对象支持 `for...of` 遍历）又不想占用普通字符串属性名**
需要一种和字符串属性名完全不冲突的属性键。

**✅ ES6/ES2015（2015 年 6 月）新增 `Symbol`：每个 Symbol 都是独一无二的值，用作属性键天然不会和字符串键冲突，同时支撑 `Symbol.iterator` 这样的"协议"式元编程**
7 种类型：6 种原始类型（多了 symbol）+ object。

**❓ `Number` 受 IEEE 754 双精度浮点限制，安全整数范围只到 `2^53-1`（`Number.MAX_SAFE_INTEGER`），但现实场景经常需要更大的精确整数（比如雪花算法生成的 64 位 ID、密码学计算）**
需要一种能表示任意精度整数的类型。

**✅ ES2020（2020 年 6 月，由 Igalia 的 Daniel Ehrenberg 牵头的提案 2019 年 6 月进入 Stage 4）新增 `BigInt`：用 `n` 后缀表示（如 `123n`），可以表示远超 `2^53-1` 的任意精度整数**
8 种类型定型：7 种原始类型（string/number/boolean/null/undefined/symbol/bigint）+ object。

**现状：类型系统的演化是两条完全独立的线——`typeof null` 的 bug 从 1995 年的实现巧合被 1997 年的 ES1 永久锁死，此后哪怕想修也因"不能破坏 The Web"被否决；而原始类型本身则按真实需求持续扩充：ES6 加 Symbol 解决属性键冲突，ES2020 加 BigInt 解决大整数精度**

## 参考资料

- [2ality — The history of "typeof null"](https://2ality.com/2013/10/typeof-null)
- [es-discuss — typeof null 修复提案讨论](https://esdiscuss.org/topic/typeof-null)
- [ECMA-262 1st Edition (1997)](https://www.ecma-international.org/wp-content/uploads/ECMA-262_1st_edition_june_1997.pdf)
- [tc39/proposal-bigint](https://github.com/tc39/proposal-bigint)
