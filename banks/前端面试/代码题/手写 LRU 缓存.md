---
题目: "手写 LRU 缓存"
分类: 代码题
频率: 高频
id: 385e29bd-9121-8133-9936-e650f5a0825f
---
用 Map（保持插入顺序）实现 O(1) LRU：

```jsx
class LRUCache {
  constructor(cap) { this.cap = cap; this.map = new Map(); }
  get(key) {
    if (!this.map.has(key)) return -1;
    const v = this.map.get(key);
    this.map.delete(key); this.map.set(key, v); // 刷新为最近
    return v;
  }
  put(key, value) {
    if (this.map.has(key)) this.map.delete(key);
    else if (this.map.size >= this.cap) this.map.delete(this.map.keys().next().value);
    this.map.set(key, value);
  }
}
```
