---
题目: "js继承"
分类: JS
频率: 低频
id: 120e29bd-9121-8051-9f68-c3f293f67972
---
- 原型链继承：子类原型指向父类实例，缺点是引用类型属性被共享。
- 构造函数继承：子类构造里 [Parent.call](http://Parent.call)(this)，解决共享但无法继承原型方法。
- 组合继承：call + 原型，常用但父构造被调用两次。
- 寄生组合继承（ES6 之前的最优方案）：Child.prototype = Object.create(Parent.prototype) 修正构造指向，避免两次调用。
- ES6 class extends 是原生子类化机制，与寄生组合相似但不等价：super() 前 this 处于 TDZ、实例由基类先分配、方法默认不可枚举、必须 new 调用、且能正确继承内建对象（如 Array）。

## 追问

### 组合继承为什么会调用父构造函数两次？具体是哪两次？

第一次是 `Child.prototype = new Parent()`——为了让子类原型上能访问到父类原型的方法，用 `new Parent()` 生成一个父类实例挂到 `Child.prototype` 上，这一步执行了一整遍父构造函数。第二次是子类构造函数内部的 `Parent.call(this, ...)`——为了让每个子类实例都有自己独立的一份父类实例属性（不共享引用），又完整执行了一遍父构造函数。两次调用意味着父构造函数里的初始化逻辑（包括可能有的副作用，比如打日志、发请求）会执行两遍，且第一次调用产生的那份属性（挂在 `Child.prototype` 上）是多余的、纯粹为了"借"到原型方法而付出的浪费。

### 寄生组合继承具体怎么避免这两次调用？

把 `Child.prototype = new Parent()` 换成 `Child.prototype = Object.create(Parent.prototype)`——`Object.create` 只是复制了一个以 `Parent.prototype` 为原型的空对象，完全不执行 `Parent` 构造函数本身，自然拿到了原型方法却不产生多余的实例属性和副作用；再手动把 `Child.prototype.constructor` 修回 `Child`（因为 `Object.create` 不会像 `new` 那样自动关联构造函数）。这样父构造函数就只在子类构造函数内的 `Parent.call(this, ...)` 里被调用一次。

## 发展史（问题 → 方案的链条）

**❓ ES1 时代最朴素的想法：直接让 `Child.prototype` 指向一个 `Parent` 的实例（`Child.prototype = new Parent()`），子类实例通过原型链自然能访问到父类的属性和方法——但父类实例上的引用类型属性（如数组、对象）会被所有子类实例共享，一个实例改了，其他实例全变**
纯原型链继承把"父类的一个实例"当成所有子类共享的原型，父类实例上任何引用类型的属性天生就是所有子类实例共用的同一份引用，这在多实例场景下是致命缺陷（`child1.colors.push('red')` 会影响到 `child2.colors`）。

**✅ 改用「构造函数继承」：在子类构造函数里手动 `Parent.call(this, ...)`，把父类的初始化逻辑在每个子类实例上重新执行一遍，属性各自独立、不再共享引用**
解决了引用共享问题，但代价是父类原型 `Parent.prototype` 上定义的方法完全够不到——`Parent.call(this)` 只执行了父构造函数体内 `this.xxx = ...` 这部分逻辑，不会把 `Parent.prototype` 关联给子类，方法复用又丢了。

**❓ 需要同时要"属性不共享"（构造函数继承的优点）和"能访问父类原型方法"（原型链继承的优点），单独用哪一种都不够**
两种方案分别只解决了问题的一半，需要把两者组合起来。

**✅ 「组合继承」：`Child.prototype = new Parent()` 拿到原型方法，子类构造函数内再 `Parent.call(this, ...)` 拿到独立属性——这是 ES5 时代书籍（如 Nicholas Zakas《Professional JavaScript for Web Developers》）里最经典的"标准答案"**
两个问题都解决了，但组合出了一个新问题：`Parent` 构造函数被完整执行了两次（一次在 `new Parent()` 里、一次在 `Parent.call(this)` 里），如果父构造函数有副作用（发请求、打日志、递增计数器），会被意外触发两次；且第一次调用产生的那份实例属性挂在 `Child.prototype` 上，是纯粹被浪费掉的多余数据。

**❓ 只是想借用 `Parent.prototype` 上的方法，却不得不完整跑一遍 `Parent` 构造函数才能拿到一个"合适的原型对象"，代价太大**
需要一种只复制原型对象、完全不触发构造函数执行的方式。

**✅ 「寄生组合继承」：用 `Object.create(Parent.prototype)` 替代 `new Parent()`（`Object.create` 由 Douglas Crockford 早在 2006 年撰文提出、ES5/2009 年正式写入规范），只造一个以 `Parent.prototype` 为原型的空对象，不执行任何构造函数逻辑，父构造函数因此只需在 `Parent.call(this)` 里被调用一次——这被广泛认为是 ES6 之前 JS 继承的最优实践**
`Object.create` 提供了"只要原型关系、不要构造过程"的精确手术刀，彻底避免了组合继承的双重调用问题，同时保留了属性独立、方法共享两大优点。

**✅ ES6（2015）把这套最佳实践正式收编为原生 `class`/`extends`/`super` 语法，且补上了 ES5 模式永远做不到的一件事——正确继承内建对象（如 `Array`）**
ES5 时代所有继承方案（无论原型链、组合、寄生组合）继承 `Array` 都有缺陷：`Array` 等内建构造函数在创建实例时会用自己内部的 `[[DefineOwnProperty]]` 机制分配特殊的内部槽，`Parent.call(this)` 这种"手动挪用父构造函数逻辑"的方式无法触发这个内部机制。ES6 class 的 `super()` 语义不同：子类的 `this` 由**基类构造函数亲自创建**（子类构造函数在调用 `super()` 之前甚至处于 TDZ、访问不了 `this`），这才让继承 `Array` 这类内建对象成为可能。

**现状：原型链继承（共享引用坑）→ 构造函数继承（丢方法坑）→ 组合继承（两次调用坑，ES5 时代"标准答案"）→ 寄生组合继承（ES6 前最优解）这条链，每一步都是对上一步遗留问题的针对性修补；ES6 class 不是简单复刻寄生组合继承，而是从"手动挪用父构造函数"换成"基类亲自分配实例"这一更底层的机制，顺带解决了 ES5 时代所有方案都搞不定的内建对象继承问题**
