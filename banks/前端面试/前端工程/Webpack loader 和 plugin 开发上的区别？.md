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
