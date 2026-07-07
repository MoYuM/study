---
题目: "React Fiber 架构解决了什么？"
分类: React
频率: 高频
id: 385e29bd-9121-811e-8a9d-d655462e0780
---
Fiber 解决同步递归更新大组件树时阻塞主线程导致的卡顿。

- 把更新拆成可中断/可恢复的 Fiber 节点，带优先级。
- 双缓存 current / workInProgress 树，完成后一次提交。
- 两阶段：Render（可中断、算 diff）+ Commit（不可中断、改 DOM）。用 Scheduler + MessageChannel 调度。
- **可中断的本质**：每个 Fiber 节点用链表三指针（`return`/`child`/`sibling`）取代函数调用栈来遍历树，进度变成一个可保存/恢复的 `workInProgress` 指针，而不是压在调用栈里出不来——这是"可中断"真正得以实现的底层原因。

## 发展史（问题 → 方案的链条）

**❓ React 最早的协调算法（支撑 React 15 及更早版本，官方 legacy 文档称之为 "stack" reconciler）是纯递归函数调用实现——一旦对一棵组件树开始 diff/更新就必须递归到底才能返回，复杂组件树的更新会长时间占用主线程，造成掉帧卡顿**
这是 Fiber 项目的直接起因——React 核心团队（Sebastian Markbåge 主导架构设计）大约从 2014 年前后开始内部研究这个问题的解法（`acdlite/react-fiber-architecture` 项目文档 2016 年称这是"两年多研究的成果"），整个重写耗时数年。

**✅ Fiber 重写：用链表结构（`return`/`child`/`sibling` 三指针）取代函数调用栈遍历组件树，让"进度"变成一个可保存/恢复的 `workInProgress` 指针——2017 年 3 月 Lin Clark 在 React Conf 上做了公开演讲《A Cartoon Intro to Fiber》介绍这套设计，同年 9 月 26 日 React 16 正式发布，搭载 Fiber 架构**
可中断的数据结构解决了"能不能暂停"的问题，但还需要知道"什么时候该暂停、该等多久继续"。

**❓ Sebastian Markbåge 2016 年提交过给 `requestIdleCallback` 做 polyfill 的 PR（#8833），说明团队一度考虑过用浏览器原生的 rIC API 来判断"主线程什么时候空闲"；但 rIC 存在兼容性问题（尤其 Safari 长期不支持）、且触发时机不受控（页面有动画/频繁交互时可能长时间不触发）——这两点综合起来让 rIC 不适合做核心调度机制（这个因果关系是社区综合 Dan Abramov 等人的只言片语与客观兼容性事实得出的推断，没有单一官方声明完整讲过这个决策过程）**
需要一套自己完全可控的调度机制，不依赖浏览器"自己判断空闲"。

**✅ Scheduler + MessageChannel：React 自己实现了一套基于 MessageChannel 的时间切片机制——`postMessage` 触发的回调是宏任务，比 `setTimeout(0)` 更快更可控（不受 HTML 规范里嵌套定时器 4ms 最小延迟的限制），每个时间片约 5ms，到点就检查 `shouldYield()` 让出主线程**
调度机制解决了"什么时候暂停"，但多个更新任务同时存在时，还缺一个"谁先谁后"的优先级模型。

**❓ React 16.1（2017 年 11 月）引入的 `expirationTime` 模型，用数字时间戳表示优先级（越紧急数值越小、越早处理），这套模型在后续需要支持"多个并行的 Suspense transition 同时存在"的场景下，灵活性不够**
需要一套能同时表示、合并、比较多种优先级的新机制。

**✅ Lanes 模型：Andrew Clark（acdlite）2020 年 5 月提交 PR #18796《Initial Lanes implementation》，用 32 位数字的位运算（bitmask）表示优先级，每个 bit 代表一条"车道"，可以合并/比较多条车道——2022 年 3 月 29 日随 React 18 正式发布，配合 `startTransition`/`useTransition` 等并发特性登场**
高优先级更新（比如用户输入）可以插队，必要时中断正在进行的低优先级渲染（比如列表渲染）去优先处理。

**现状：Render 阶段（算 diff，操作 workInProgress 树）可中断，Commit 阶段（改真实 DOM）不可中断；调度靠 Scheduler + MessageChannel 实现时间切片；优先级靠 Lanes 模型的位运算表示——这套"可中断 + 可调度 + 分优先级"的完整体系是十年间（2014年前后设计 → 2017年Fiber落地 → 2022年Lanes落地）逐层搭建起来的，不是一次性设计出来的**

## 参考资料

- [React 官方 — 渲染与提交](https://zh-hans.react.dev/learn/render-and-commit)
- [A Cartoon Intro to Fiber（Lin Clark, React Conf 2017）](https://www.youtube.com/watch?v=ZCuYPiUIONs)
- [React v16.0 — React Blog（2017-09-26）](https://legacy.reactjs.org/blog/2017/09/26/react-v16.0.html)
- [PR #8833 — Polyfill requestIdleCallback](https://github.com/facebook/react/pull/8833)
- [PR #18796 — Initial Lanes implementation](https://github.com/facebook/react/pull/18796)
- [React v18.0 — React Blog（2022-03-29）](https://react.dev/blog/2022/03/29/react-v18)
- [acdlite/react-fiber-architecture](https://github.com/acdlite/react-fiber-architecture)
