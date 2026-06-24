---
题目: "BFC 是什么？解决什么？"
分类: CSS
频率: 高频
掌握: 
下次复习: 
上次评测: 
id: 385e29bd-9121-8195-bc0a-fcee10b17a47
备注: ""
---
BFC（块级格式化上下文）是一个独立渲染区域，内部布局不影响外部。

触发：根元素、overflow 非 visible、float、绝对/固定定位、display: inline-block / table-cell / flow-root 等。注意：display:flex / grid 建立的是弹性/网格格式化上下文（FFC/GFC），**并不是 BFC**，但同样能包含浮动、阻止 margin 折叠。

解决：清除浮动（包住浮动子元素）、防止 margin 重叠、实现自适应两栏。

## 参考资料

- [MDN — 块格式化上下文（BFC）](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_display/Block_formatting_context)
