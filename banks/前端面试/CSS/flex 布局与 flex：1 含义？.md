---
题目: "flex 布局与 flex:1 含义？"
分类: CSS
频率: 高频
id: 385e29bd-9121-8131-96f9-d7f5e40492db
---
flex 是一维流式布局，主轴对齐用 `justify-content`，交叉轴对齐用 `align-items`。

## flex:1 展开

```css
flex: 1  →  flex-grow: 1;  flex-shrink: 1;  flex-basis: 0%;
```

## 三个子属性

| 属性 | 含义 | 默认值 |
|------|------|--------|
| `flex-grow` | 有剩余空间时，按比例**放大**的权重 | 0（不放大） |
| `flex-shrink` | 空间不足时，按比例**缩小**的权重 | 1（会缩小） |
| `flex-basis` | grow/shrink **计算前**的基准尺寸（不是最小宽度） | auto |

## flex-basis: 0 vs auto 的区别

```
auto：先用内容/width 确定基准，再分配剩余空间
  → 内容多的元素基准更大，grow 在此基础上继续分配，结果不等宽

0：基准为 0，所有空间都算"剩余空间"
  → grow 比例直接决定最终尺寸，flex:1 的所有子元素严格等宽
```

这就是为什么 `flex:1` 能让多个子元素**等分容器**——`basis:0` 把全部空间都交给 grow 按 1:1:1 分配。

## 参考资料

- [MDN — flex](https://developer.mozilla.org/zh-CN/docs/Web/CSS/flex)
- [阮一峰 — Flex 布局教程：语法篇](https://www.ruanyifeng.com/blog/2015/07/flex-grammar.html)
