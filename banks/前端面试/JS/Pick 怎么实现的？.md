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
