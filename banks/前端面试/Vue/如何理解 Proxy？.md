---
题目: "如何理解 Proxy？"
分类: Vue
频率: 低频
id: 100e29bd-9121-80b4-8ea0-c95b905972d9
---
Proxy 是 ES6 提供的对象代理，可拦截 13 种操作（get/set/has/deleteProperty/ownKeys 等）。

Vue3 用它做响应式，相比 `Object.defineProperty` 的优势：能监听属性新增/删除、数组索引与 length、Map/Set，且惰性代理（用到才递归）无需初始化时深度遍历。

局限：不兼容 IE；深层对象仍需递归代理；无法代理原始值（要用 ref 包装）。

## 发展史（问题 → 方案的链条）

**❓ Vue2（2016 年 9 月 30 日发布，代号 "Ghost in the Shell"）用 `Object.defineProperty`（ES5，2009 年规范）逐个劫持属性的 getter/setter 实现响应式，但这个机制有明确边界：无法检测对象属性的新增/删除（需手动调用 `Vue.set`/`vm.$set`），也无法检测数组按下标赋值和修改 `length`（需重写 `push/pop/shift/unshift/splice/sort/reverse` 七个数组方法来打补丁）**
需要一种能从根上覆盖这些"盲区"操作、而不是逐个方法打补丁的拦截机制。

**✅ Vue3（2020 年 9 月 18 日发布，代号 "One Piece"）换用 `Proxy`（ES6/ES2015，2015 年 6 月规范）：代理整个对象而非逐个属性，能拦截 get/set/has/deleteProperty/ownKeys 等 13 种操作，天然覆盖属性新增删除、数组下标和 length 变化、Map/Set，且惰性递归（子对象用到才代理）不需要初始化时全量遍历**
但 Proxy 是一个语言层面的"陷阱机制"，无法被 polyfill——这意味着要用它，就得放弃不支持 ES6 的老旧浏览器。

**❓ Evan You 在 2018 年发文《Plans for the Next Iteration of Vue.js》中最初的计划是保留一个基于 `Object.defineProperty` 的 IE11 兼容 build，让 Proxy 版和 defineProperty 版双轨并行**
同时维护两套响应式实现成本很高，而 IE11 市场份额当时已跌破 1%。

**✅ 2021 年 4 月，vuejs/rfcs 仓库 PR #294《Proposal for dropping IE11 support in Vue 3》由 Evan You 本人提出并合并，正式确认彻底放弃 IE11 支持**
Vue3 从此只维护一套基于 Proxy 的响应式实现，官方 FAQ 明确写"需要 IE11 支持请用 Vue 2.x"。

**现状：`Object.defineProperty`（Vue2，ES5，属性级劫持，靠 `Vue.set` 和重写数组方法打补丁）与 `Proxy`（Vue3，ES6，对象级拦截，覆盖完整但彻底放弃 IE11 兼容）之间不是单纯的"新技术更好"，而是"覆盖完整性"与"浏览器兼容性"的取舍——Vue3 选择了前者**

## 参考资料

- [Vue 2.0 is here! — The Vue Point](https://medium.com/the-vue-point/vue-2-0-is-here-ef1f26acf4b8)
- [Vue 3.0 One Piece — Vue Blog](https://blog.vuejs.org/posts/vue-3-one-piece)
- [ECMA-262 5.1 Edition](https://262.ecma-international.org/5.1/)
- [MDN — Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy)
- [Vue2 — Reactivity in Depth（局限说明）](https://v2.vuejs.org/v2/guide/reactivity.html)
- [Plans for the Next Iteration of Vue.js — Evan You, 2018](https://medium.com/the-vue-point/plans-for-the-next-iteration-of-vue-js-777ffea6fabf)
- [vuejs/rfcs PR #294 — Dropping IE11 support in Vue 3](https://github.com/vuejs/rfcs/blob/master/active-rfcs/0038-vue3-ie11-support.md)
