---
题目: "BFC 是什么？解决什么？"
分类: CSS
频率: 高频
id: 385e29bd-9121-8195-bc0a-fcee10b17a47
---
BFC（块级格式化上下文）是一个独立渲染区域，内部布局不影响外部。

## 发展史（问题 → 方案的链条）

**❓ 图文混排需要「浮动」，但浮动元素会脱离文档流**
CSS1（1996）引入 `float` 属性，让元素脱离正常的块级排列、靠一侧浮动，实现文字环绕图片这类排版。但脱离文档流的代价是：浮动元素不再占据自己在文档流里该有的位置。

**❓ 父容器只包含浮动子元素时，会「塌陷」成零高度**
因为浮动子元素脱离了文档流，父容器在计算自身高度时不会把它们算进去——如果父容器里只有浮动的子元素，父容器的高度直接塌陷成 0，包不住里面的内容，边框/背景色也跟着看不出效果。

**✅ 其实 CSS2（1998）就已经定义了「块格式化上下文（BFC）」——离问题出现只隔 2 年**
CSS2 规范把这类"独立渲染区域"正式定义为 Block Formatting Context：只要父容器自己建立了 BFC，它计算自身高度时就会把内部的浮动子元素算进去。能触发 BFC 的写法当时就有：根元素、`float`、绝对/固定定位、`display: inline-block`/`table-cell`、`overflow` 非 `visible` 等（后来 2011 年成为 Recommendation 的 CSS2.1，主要是对已有浏览器行为做勘误和措辞澄清，并不是重新发明 BFC）。

**❓ 但规范里能触发 BFC 的属性全都有副作用，逼得开发者绕开它**
`overflow: hidden` 会连带裁剪掉本不该被裁剪的内容（比如子元素的 `box-shadow`、下拉菜单）；`float` 会让容器自己也脱离文档流；`inline-block` 会改变容器的外部排列方式。这些副作用太麻烦，所以从 2000 年代中期开始，很多开发者干脆不用 BFC，转而用「clearfix」标记 hack：先是在浮动元素后面加一个 `clear: both` 的空 `<div>`，后来演化成不用额外标签、直接用 `::after` 伪元素模拟这个空块（2011 年 Nicolas Gallagher 发布的 "micro clearfix" 是流传最广的版本之一）。clearfix 和"用 overflow 等触发 BFC"两种方案在这十几年里长期并存、各有取舍——真正等待解决的不是"能不能清浮动"，而是"能不能没有副作用地清浮动"。

**✅ CSS Display Module Level 3 新增 `display: flow-root`：专门只触发 BFC，没有其他副作用**
`flow-root` 是专为"只想要 BFC 的清浮动效果，不想要任何副作用"这个诉求设计的属性值，2017 年前后主流浏览器陆续跟进支持，是目前触发 BFC 的首选写法。

**现状：`flow-root` 是首选，但 flex/grid 建立的是 FFC/GFC 不是 BFC，容易和 BFC 搞混**
`display: flex`/`grid` 各自建立自己独立的格式化上下文（FFC/GFC），效果上同样能包含浮动、阻止 margin 折叠，但它们在规范里**不属于** BFC——BFC/IFC（内联）/FFC/GFC 是并列的几种不同格式化上下文，各自定义子元素的排布规则，名字相似但不是一回事。

## 解决的问题

清除浮动（包住浮动子元素，父容器不再塌陷）、防止 margin 重叠、实现自适应两栏布局。

## 参考资料

- [MDN — 块格式化上下文（BFC）](https://developer.mozilla.org/zh-CN/docs/Web/CSS/CSS_display/Block_formatting_context)
- [MDN — flow-root](https://developer.mozilla.org/zh-CN/docs/Web/CSS/display#flow-root)
