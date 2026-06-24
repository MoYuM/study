---
题目: "margin 重叠问题？"
分类: CSS
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: 385e29bd-9121-81e6-a0c2-cb6e1ebde5f0
备注: ""
---
相邻块级元素的垂直 margin 会取最大值合并；父子元素之间也会发生 margin 传递。

解决：给父元素触发 BFC（overflow:hidden）、加 border/padding 隔开、改用 flex/grid 布局。
