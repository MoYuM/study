---
题目: "Webpack loader 和 plugin 开发上的区别？"
分类: 前端工程
频率: 高频
id: 128c7c68-95e4-45e3-a46d-8449b5eddd4c
---
- **loader**：模块转换器，处理单个文件的源码转换（babel-loader、css-loader、ts-loader），本质是函数，输入源码输出转换结果，链式从右到左/从下到上执行。
- **plugin**：基于 Webpack 的 tapable 钩子，监听 Compiler / Compilation 生命周期事件，扩展构建流程（HtmlWebpackPlugin、DefinePlugin、压缩、提取 CSS），能力比 loader 更广。

一句话：loader 管「怎么转换文件」，plugin 管「在构建生命周期里做事」。
