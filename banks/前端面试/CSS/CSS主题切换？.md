---
题目: "CSS主题切换？"
分类: CSS
频率: 低频
id: bbeba626-bac2-4cbc-b387-7cff2ddbd026
---
https://juejin.cn/post/7134594122391748615

- 动态设置 link 标签
- 切换类名
- css变量+切换类名
- cssInjs

## 跟随系统深色模式

用媒体查询 `@media (prefers-color-scheme: dark) { ... }`——系统的深色/浅色偏好一变，样式自动跟着变，不需要 JS 参与。

实际项目通常三者结合：`prefers-color-scheme` 提供默认值 → 用户手动切换时用 JS 覆盖（切 class）→ 用 `localStorage` 记住用户的选择，下次打开页面优先读这个而不是系统偏好。
