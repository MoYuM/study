---
题目: "ESM 与 CJS 的区别？"
分类: 前端工程
频率: 高频
掌握: 
下次复习: 
上次评测: 
id: 385e29bd-9121-811d-9c80-c49637809bd3
备注: ""
---
- ESM：静态导入（编译时确定依赖）、支持 Tree-shaking、可异步加载、import/export，是值引用（活绑定）。
- CJS：运行时同步加载、require/module.exports、动态、不易 Tree-shaking，是值拷贝。
