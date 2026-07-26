---
题目: "flex 布局和 grid 布局？"
分类: CSS
频率: 高频
id: 6f0a3840-33ca-4866-86e4-372daebebdc3
---
flex 是一种一维布局；grid 是二维的网格布局，能实现更复杂的排布。

Grid 常用属性：`grid-template-columns/rows`、`fr` 弹性单位、`repeat()`、`minmax()`、`auto-fill/auto-fit`、`grid-area`、`gap`。

选型：flex 适合一维（导航栏、按钮组）；grid 适合复杂网格（仪表盘、卡片布局）。

## 发展史（问题 → 方案的链条）

**❓ Flexbox 出现之前，前端布局靠 float / table-cell / inline-block 等 hack 手段实现——清除浮动、垂直居中、多列等高都缺乏原生方案**
这些 hack 本质是借用了别的 CSS 特性来"凑合"实现布局效果（比如 float 本来是为了让文字环绕图片，被拿来做多栏布局），Philip Walton 的《Solved by Flexbox》等资料系统整理过这类痛点。

**✅ CSS Flexible Box Layout Module（Flexbox）：最早草案 2009 年 7 月提出（基于 Firefox XUL box model 的旧语法，与现在写法差异很大），2011 年 Tab Atkins 接手重写为现代语法（`display: flex`/`flex-grow` 等），2015 年完成 Last Call、2016 年 3 月正式成为 W3C 候选推荐标准（CR），同年主流浏览器基本完成无前缀支持**
提供了原生的"一维弹性布局"能力：元素在一个方向上根据内容大小和 `flex-grow`/`shrink` 自动分配空间——这是一种**内容优先（content-out）**的布局思路，容器结构跟着内容"长"出来。MDN 官方文档原话："Flexbox works from the content out"。

**❓ Flexbox 只能控制一个维度（行或列），没法同时对齐"行和列"两个维度——比如仪表盘/整站级布局需要行列同时精确控制的网格结构，Flexbox 力不从心**
局部组件内的一维排列问题解决了，但页面级的二维网格排布依然没有原生方案。

**✅ CSS Grid Layout：候选推荐标准发布于 2016 年 11 月，Chrome 57 / Firefox 52 / Safari 10.1 于 2017 年 3 月同步支持（Edge 要到同年 10 月才跟进现代语法），Rachel Andrew（Grid by Example 站点、大量文档著作）与 Jen Simmons（时任 Mozilla Design Advocate，Labs 项目、Layout Land 视频系列）是推广 Grid 新布局思维的代表性人物**
Grid 采用**布局优先（layout in）**的设计思路：先用 `grid-template-columns/rows` 定义好整张网格结构，内容再往里填。MDN 官方文档原话："grid works from the layout in — you create a layout and then place items into it"——这个设计动机是 MDN 官方文档明确表述的，不是社区事后总结出来的；Elika Etemad 是 CSS Grid 规范的主要编辑者之一。

**现状：Flexbox 解决局部/一维的弹性分布问题（导航栏、按钮组），Grid 解决整体/二维的网格布局问题（整站/仪表盘/卡片墙）——二者不是替代关系，而是分别对应 MDN 所说的"content out"和"layout in"两种不同的设计思路**

## 参考资料

- [阮一峰 — Grid 网格布局教程](https://www.ruanyifeng.com/blog/2019/03/grid-layout-tutorial.html)
- [Solved by Flexbox — Philip Walton](https://philipwalton.github.io/solved-by-flexbox/demos/holy-grail/)
- [W3C — CSS Flexbox Level 1 候选推荐标准公告](https://www.w3.org/blog/CSS/2016/03/02/css-flexbox-cr2/)
- [W3C — CSS Grid 候选推荐标准公告](https://www.w3.org/blog/CSS/2016/11/02/grid-cr/)
- [A List Apart — The Story of CSS Grid, from Its Creators](https://alistapart.com/article/the-story-of-css-grid-from-its-creators/)
- [MDN — Relationship of grid layout to other layout methods](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Relationship_with_other_layout_methods)
- [MDN — Relationship of flexbox to other layout methods](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Relationship_of_flexbox_to_other_layout_methods)
