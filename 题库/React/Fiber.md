---
题目: "Fiber"
分类: React
频率: 高频
掌握: 
下次复习: 
上次评测: 
id: 67a7bad8-cbf2-480e-a4cd-f903613f7738
备注: ""
---
https://www.youtube.com/watch?v=ZCuYPiUIONs&list=PLb0IAmt7-GS3fZ46IGFirdqKTIxlws7e0&index=5

[https://github.com/acdlite/react-fiber-architecture](https://github.com/acdlite/react-fiber-architecture)

- React 16 新功能
- 为了解决协调过程阻塞的问题
- 通过将工作切片，分成若干个工作单元
- 遍历工作单元 ⇒ 构建 work-in-progress 树
- 每完成一个单元，就回到主进程看看还有没有剩余时间，有的话，继续工作，没有就将资源让给主线程
- 不断重复，直至完成
