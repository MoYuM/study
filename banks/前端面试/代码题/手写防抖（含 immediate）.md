---
题目: "手写防抖（含 immediate）"
分类: 代码题
频率: 高频
id: 385e29bd-9121-8183-b658-ce40be30d9e3
---
防抖：事件停止触发 n 毫秒后才执行，连续触发则重新计时（如搜索联想）。

```jsx
function debounce(fn, delay, immediate) {
  let timer = null;
  return function (...args) {
    if (timer) clearTimeout(timer);
    if (immediate && !timer) fn.apply(this, args);
    timer = setTimeout(() => {
      timer = null;
      if (!immediate) fn.apply(this, args);
    }, delay);
  };
}
```
