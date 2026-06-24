---
题目: "H5 中 IOS 和安卓兼容性问题？"
分类: 前端工程
频率: 低频
id: fdfde52b-3571-4069-a601-28e9e12b7a20
---
常见兼容问题与处理：

- 点击 300ms 延迟、点击穿透：用 FastClick 或 `touch-action`、合理处理 touch/click。
- 滚动卡顿：iOS `-webkit-overflow-scrolling: touch`。
- 1px 边框：`transform: scale(0.5)` 或 viewport 缩放。
- 软键盘弹起顶布局、安全区刘海：`env(safe-area-inset-*)`、viewport-fit=cover。
- 日期格式：iOS 不识别 `YYYY-MM-DD HH:mm:ss`，要用 `/` 或 ISO 格式。
- 输入框、audio/video 自动播放策略差异；字体与行高渲染差异。
