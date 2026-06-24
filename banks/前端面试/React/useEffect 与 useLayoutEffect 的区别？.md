---
题目: "useEffect 与 useLayoutEffect 的区别？"
分类: React
频率: 低频
id: 385e29bd-9121-81aa-bff6-ea29720d2eb3
---
- useEffect：渲染提交、浏览器绘制后异步执行，不阻塞画面。
- useLayoutEffect：在 DOM 变更后、浏览器绘制前同步执行，适合读取布局/同步修改 DOM 避免闪烁。

优先 useEffect；需要在绘制前同步读写布局才用 useLayoutEffect。
