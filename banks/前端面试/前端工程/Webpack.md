---
题目: "Webpack"
分类: 前端工程
频率: 高频
id: a31c2f13-632b-4512-a52b-83211c220a76
---
## 插件

- 插件本质上是有一个实现了 `apply(compiler)` 方法的 class
- 插件的 apply 方法在 webpack 启动时调用一次
- 插件通过订阅钩子实现功能
- 常见插件
	- `HtmlWebpackPlugin` — 自动生成 HTML 并注入 bundle
	- `MiniCssExtractPlugin` — 把 CSS 从 JS 里抽出来单独文件
	- `DefinePlugin` — 编译时注入全局常量
	- `CleanWebpackPlugin` — 构建前清空 dist 

## 参考资料
- [plugin](https://www.webpackjs.com/concepts/plugins/)
