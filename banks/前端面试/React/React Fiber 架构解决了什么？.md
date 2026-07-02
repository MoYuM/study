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

## 参考资料

- [React 官方 — 渲染与提交](https://zh-hans.react.dev/learn/render-and-commit)
- [A Cartoon Intro to Fiber（Lin Clark, React Conf）](https://www.youtube.com/watch?v=ZCuYPiUIONs)
