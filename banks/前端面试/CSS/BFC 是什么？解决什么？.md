---
题目: "BFC 是什么？解决什么？"
分类: CSS
频率: 高频
id: 385e29bd-9121-8195-bc0a-fcee10b17a47
---
BFC（块级格式化上下文）是一个独立渲染区域，内部布局不影响外部。

触发：根元素、overflow 非 visible、float、绝对/固定定位、display: inline-block / table-cell / flow-root、`contain: layout` 等。注意：display:flex / grid 建立的是弹性/网格格式化上下文（FFC/GFC），**并不是 BFC**，但同样能包含浮动、阻止 margin 折叠。

> 补充：页面上所有内容都属于某种 formatting context——块级（BFC）、内联（IFC）、弹性（FFC）、栅格（GFC）——各自定义子元素的布局规则。

解决：清除浮动（包住浮动子元素）、防止 margin 重叠、实现自适应两栏。

## 参考资料

- [MDN — 块格式化上下文（BFC）](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_display/Block_formatting_context)
