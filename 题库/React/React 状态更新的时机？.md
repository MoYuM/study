---
题目: "React 状态更新的时机？"
分类: React
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: ce0a256b-e888-4305-8661-a17ac2178120
备注: ""
---
- React 18 前：仅在 React 合成事件/生命周期中批处理（多次 setState 合并为一次渲染），而 setTimeout/Promise/原生事件里不批处理。
- React 18：默认全场景自动批处理（含 setTimeout、Promise、原生事件）。
- setState 是异步合并的，连续依赖前值要用函数式更新 `setState(prev => prev + 1)` 避免闭包陈旧值。
- 需要同步拿到更新后 DOM 可用 flushSync（慎用）。
