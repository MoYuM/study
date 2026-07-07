---
题目: "Webpack loader 和 plugin 开发上的区别？"
分类: 前端工程
频率: 高频
id: 128c7c68-95e4-45e3-a46d-8449b5eddd4c
---
- **loader**：模块转换器，处理单个文件的源码转换（babel-loader、css-loader、ts-loader），本质是函数，输入源码输出转换结果，链式从右到左/从下到上执行。
- **plugin**：基于 Webpack 的 tapable 钩子，监听 Compiler / Compilation 生命周期事件，扩展构建流程（HtmlWebpackPlugin、DefinePlugin、压缩、提取 CSS），能力比 loader 更广。

一句话：loader 管「怎么转换文件」，plugin 管「在构建生命周期里做事」。

## 追问

### loader 链的执行顺序是从右到左，为什么？

loader 链是**从右到左、从下到上**执行的，和配置数组的书写顺序相反：

```js
// 配置
use: ['style-loader', 'css-loader', 'sass-loader']
// 执行顺序：sass-loader → css-loader → style-loader
```

原因是函数式编程里的 **compose**（组合）惯例：`f(g(h(x)))` 中 h 最先执行，对应数组末尾。可以理解为把多个 loader 当作管道，原始文件从右端进入，逐层转换后从左端输出。

上面这个例子的数据流：
```
.scss 源码
  → sass-loader  → 转成 CSS 字符串
  → css-loader   → 解析 @import / url()，转成 JS 模块
  → style-loader → 注入 <style> 标签到 DOM
```

顺序写反会导致编译报错或输出错误，是常见踩坑点。

## plugin 补充细节

- plugin 本质是一个实现了 `apply(compiler)` 方法的 class；`apply` 只在 Webpack **启动时调用一次**（不是每个钩子都调一次），内部通过 `compiler.hooks.xxx.tap/tapAsync` 主动注册回调订阅生命周期钩子，底层依赖 **Tapable**。
- `compiler`（全局只有一个，代表整个 Webpack 环境配置）vs `compilation`（每次构建都会新建一个，代表一次具体的编译过程）。
- 常见插件：`HtmlWebpackPlugin`（自动生成 HTML 并注入 bundle）、`MiniCssExtractPlugin`（把 CSS 从 JS 里抽出来单独文件）、`DefinePlugin`（编译时注入全局常量）、`CleanWebpackPlugin`（构建前清空 dist）。

## 追问：compiler 和 compilation 有什么区别？

- **`compiler`**：代表整个 Webpack 的运行环境，**全局只有一个**，包含完整配置（entry/output/module/plugins 等）。启动时创建一次，贯穿整个生命周期。
- **`compilation`**：代表**一次具体的编译**，**每次构建都会新建一个**。包含这一次编译的模块、依赖关系图、生成的 chunk/asset 等中间数据。`watch` 模式下文件一变化就触发新一轮编译，每一轮都会创建一个新的 `compilation` 对象，但 `compiler` 还是原来那一个。

一句话区分：**compiler 是"进程级"的，一个 Webpack 运行周期只有一个；compilation 是"构建级"的，每编译一次就换一个新的。** 这也是为什么有些钩子挂在 `compiler.hooks` 上（如 `run`、`done`，关心整个运行周期），有些钩子挂在 `compilation.hooks` 上（如 `optimize`、`seal`，关心某一次具体编译的内部细节）。

## 发展史（问题 → 方案的链条）

**❓ Webpack 出现之前，模块打包工具设计边界各不相同：Browserify（2011 年发布）官方文档明确说"设计上不关心 CSS"，处理非 JS 资源要靠额外的 transform（如 `brfs`、`browserify-css`）且有局限；RequireJS/AMD 生态虽然通过 loader plugin 语法（如 `text!`、第三方 `require-css` 提供的 `css!`）能加载非 JS 资源，但要靠特定前缀语法，不是原生统一的模块依赖图**
不同类型的资源（JS/CSS/图片）要么完全没法被"当模块处理"，要么各自需要专门的、不统一的语法，没有一种通用机制能把"任何资源"都纳入同一张依赖图。

**✅ Webpack（Tobias Koppers 大约 2012 年开始开发——前身是给 `modules-webmake` 项目添加类 GWT 代码分割功能，因改动太大难以合并回去而另起项目，2014 年 2 月 19 日 webpack 1.0.0 正式发布）：引入"loader"概念——每个 loader 是一个函数，输入源文件内容，输出转换后的内容，可以链式串联**
不管是不是 JS，只要配置了对应 loader，任何资源都能被 require/import，统一纳入依赖图管理——这是 webpack 相比之前工具的核心差异化设计。（网上常有"loader 的 `!` 语法借鉴自 RequireJS 的 loader plugin 语法"这类说法，但没有找到 Tobias Koppers 本人或官方资料的一手确认，应视为未证实的社区说法，不当作史实。）

**❓ Loader 只能处理"单个文件内容的转换"，没法做全局性的事情（比如根据入口生成 HTML、抽取多个 chunk 间的公共代码、往产物里注入常量）**
需要一种更高层、能介入整个构建生命周期的扩展机制，而不只是对单个文件的转换。

**✅ Plugin + Tapable 钩子系统：Tapable 是 Koppers 本人开发的发布订阅式钩子库（至少 2014 年已存在，具体首次发布日期未能查实），plugin 通过实现 `apply(compiler)` 方法、内部用 `compiler.hooks.xxx.tap()` 订阅特定生命周期节点，能读写整个编译上下文**
plugin 的能力边界远大于 loader——不受"单个文件"限制，能在任意构建阶段插入自定义逻辑、操作整个 compilation 对象。

**现状：loader 和 plugin 分别对应"资源怎么转换"和"构建流程里做什么事"这两个不同粒度的扩展点——loader 是纯函数式的单文件转换链，plugin 是基于 Tapable 发布订阅机制的全生命周期钩子，二者不是谁比谁高级，而是解决不同层面问题的正交机制**

## 参考资料
- [plugin](https://www.webpackjs.com/concepts/plugins/)
- [Webpack — Wikipedia（1.0.0 发布日期）](https://en.wikipedia.org/wiki/Webpack)
- [browserify-handbook — 关于 CSS 的设计边界](https://github.com/browserify/browserify-handbook)
- [RequireJS — Plugins 文档](https://requirejs.org/docs/plugins.html)
- [webpack/tapable](https://github.com/webpack/tapable)
