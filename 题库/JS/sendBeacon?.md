---
题目: "sendBeacon?"
分类: JS
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: 7098a792-c4e9-49f6-abf9-4b70ee15296b
备注: ""
---
`navigator.sendBeacon(url, data)` 异步发送少量数据、不阻塞页面卸载，属「尽力（best-effort）」发送：可靠性高于同步 XHR，但并非 100% 保证。

典型场景：埋点 / 统计上报。MDN 推荐用 `visibilitychange`（而非 unload）触发上报。局限：只能 POST、数据量有限、无法读响应。
