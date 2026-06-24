---
题目: "React Hooks 常用 API 与原理？"
分类: React
频率: 高频
掌握: 
下次复习: 
上次评测: 
id: 385e29bd-9121-81df-8456-f9e98c74cf6e
备注: ""
---
常用：useState（状态）、useEffect（副作用）、useMemo（缓存值）、useCallback（缓存函数）、useRef（可变引用/DOM）、useContext、useReducer、useLayoutEffect。

原理：Hook 以链表按调用顺序存在 Fiber 上，所以不能在条件/循环中调用（顺序要稳定）。

## 参考资料

- [React 官方 — Hooks 参考](https://zh-hans.react.dev/reference/react/hooks)
- [React 官方 — Hook 的规则](https://zh-hans.react.dev/reference/rules/rules-of-hooks)
