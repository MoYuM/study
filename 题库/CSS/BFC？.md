---
题目: "BFC？"
分类: CSS
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: 0e941c87-eb7f-455a-a946-d1590425f403
备注: ""
---
https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_flow_layout/Introduction_to_formatting_contexts

页面上所有内容都是 formatting context 的一部分，或者是一个以特定方式显示的区域

BFC（Block formatting Content）是 formatting context 的一种

一共有如下几种 formatting context

- 块级格式化上下文（BFC，block formatting context）。
- 内联格式化上下文（IFC，inline formatting context）。
- 弹性格式化上下文（FFC，flex formatting context），在 CSS3 中定义。
- 栅格格式化上下文（GFC，grid formatting context），在 CSS3 中定义。

每一种都规定了其子元素的不同布局规则

除了文档的根元素 ([`<html>`](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/html)) 之外，还将在以下情况下创建一个新的 BFC：

- 使用[`float`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/float) 使其浮动的元素
- 绝对定位的元素 (包含 [`position: fixed`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/position#fixed) 或[`position: sticky`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/position#sticky)
- 使用以下属性的元素 [`display: inline-block`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/display#inline-block)
- 表格单元格或使用 `display: table-cell`, 包括使用 `display: table-*` 属性的所有表格单元格
- 表格标题或使用 `display: table-caption` 的元素
- 块级元素的 overflow 属性不为 `visible`
- 元素属性为 `display: flow-root` 或 `display: flow-root list-item`
- 元素属性为 [`contain: layout`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/contain#layout), `content`, 或 `strict`
- [flex items](https://developer.mozilla.org/zh-CN/docs/Glossary/Flex_Item)
- 网格布局元素
- [multicol containers](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_multicol_layout/Basic_concepts)
- 元素属性 [`column-span`](https://developer.mozilla.org/zh-CN/docs/Web/CSS/column-span) 设置为 `all`
