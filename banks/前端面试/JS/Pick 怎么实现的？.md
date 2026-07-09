---
题目: "Pick 怎么实现的？"
分类: JS
频率: 低频
id: 120e29bd-9121-8086-b69c-f5194ccf50c8
---
Pick 从类型 T 中挑选若干属性 K 组成新类型。

```tsx
type Pick<T, K extends keyof T> = {
  [P in K]: T[P];
};
```

用到：`keyof` 约束 K 必须是 T 的键，映射类型 `[P in K]` 遍历键、`T[P]` 取值类型。对应的 Omit 则是排除：`Pick<T, Exclude<keyof T, K>>`。

## 追问

### Omit 是怎么实现的？为什么不是独立的一套逻辑？

`Omit<T, K> = Pick<T, Exclude<keyof T, K>>`——先用 `Exclude<keyof T, K>` 从 T 的全部键里剔除 K，剩下的键集合再喂给 `Pick` 去挑。Omit 不是另造一套映射类型，而是复用 Pick 的"按键集合挑属性"能力，只是先用 `Exclude` 反向算出"要保留的键"。这也是为什么 TypeScript 官方很长一段时间没有内置 Omit——因为它本质是 Pick + Exclude 的组合，用户完全可以自己拼出来。

## 发展史（问题 → 方案的链条）

**❓ TypeScript 2.1（2016 年 11 月）之前，没有办法从一个已有类型"派生"出新类型——想要"某接口的部分字段版本"只能手写第二个接口，跟原接口维护两份、容易在改动时漏改**
早期 TS 的类型系统里，接口之间只能靠手写字段或 `extends` 继承来关联，没有"对已有类型做变换"的能力，团队里"部分字段""只读版本""按 key 取子集"这类需求全靠复制粘贴接口定义，原接口一改字段，衍生出来的接口很容易忘记同步。

**✅ TypeScript 2.1 同时引入 `keyof`（取出一个类型所有键组成的联合类型）和「映射类型」语法 `{ [P in K]: T[P] }`（遍历键联合、逐个生成新属性），并用它们内置实现了 `Partial`、`Readonly`、`Record`、`Pick` 这几个工具类型**
有了 `keyof` 拿到 T 的键集合、`K extends keyof T` 约束 K 必须是这个集合的子集、`[P in K]: T[P]` 逐个键取值类型重新拼出新类型，"从已有类型派生新类型"第一次变成了可编程的能力，Pick 就是这套机制最直接的应用：给定要保留的键集合 K，生成一个只含这些键的新类型。

**❓ 有了"挑选某些键"的 Pick，但反过来"排除某些键，保留其余全部"这个同样常见的需求（比如"这个类型除了 id 之外的字段"）没有对应的内置工具**
Pick 需要显式列出"要哪些键"，但很多场景下更自然的表达是"除了某几个键，其余都要"——尤其是字段很多、只想排除一两个的时候，手写 Pick 罗列剩下所有键既啰嗦又容易在类型改动后漏更新。

**✅ 开发者从 2016 年到 2019 年普遍自己拼出 `type Omit<T, K> = Pick<T, Exclude<keyof T, K>>`（`Exclude` 本身是 TS 2.8/2018 年随条件类型一起引入的）——这个写法流传甚广，最终 TypeScript 3.5（2019 年 5 月）把它收编为官方内置工具类型 `Omit<T, K>`，内部实现就是这个公式**
"民间约定俗成的写法被收编为标准库"和 `Function.prototype.bind` 当年从各家框架的 helper 函数被 ES5 收编为标准方法，是同一种语言演化路径。

**现状：Pick（映射类型直接应用，2016 年随 TS 2.1 内置）负责"挑选"，Omit（Pick + Exclude 的组合，2019 年 TS 3.5 才转正为内置）负责"排除"——Omit 至今的官方实现依然就是 `Pick<T, Exclude<keyof T, K>>` 这行代码，不是独立机制**

## 参考资料

- [TypeScript Handbook — Mapped Types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html)
- [TypeScript Handbook — Utility Types（Pick / Omit / Exclude 等）](https://www.typescriptlang.org/docs/handbook/utility-types.html)
