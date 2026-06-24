---
题目: "Babel 如何把 ES6 转 ES5？"
分类: 前端工程
频率: 低频
id: 385e29bd-9121-813c-9503-fe608eadddf6
---
Babel 流程：解析（parse 成 AST）→ 转换（transform，插件/preset 改写 AST）→ 生成（generate 输出代码）。配合 core-js/polyfill 补运行时 API（Promise、Array.includes 等）。

注意：输出的语法版本由 targets / browserslist 决定，不一定是 ES5；**Babel 8（2026 年发布）起已取消默认降级到 ES5/CommonJS**，需显式声明 targets。
