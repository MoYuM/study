---
题目: "URL 参数解析"
分类: 代码题
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: 385e29bd-9121-81ce-9f14-d24b0a9dc36d
备注: ""
---
推荐用 `URLSearchParams`：`Object.fromEntries(new URL(url).searchParams)`。

手动版：取 `?` 后部分按 `&` split、再按 `=` split，`decodeURIComponent` 解码；注意重复 key 转数组、空值、hash 处理。
