---
题目: "Webpack 如何加快构建速度的？"
分类: 前端工程
频率: 低频
id: 24102620-4409-4083-be26-00c821f5e94e
---
- 缩小处理范围：loader 加 include/exclude，resolve.modules/extensions 精简。
- 缓存：持久化缓存（cache: filesystem）、babel-loader cacheDirectory。
- 多进程：thread-loader、并行压缩。
- 预编译：DllPlugin / externals 抽离第三方库。
- 用更快的工具：esbuild-loader / swc 替代 babel、Terser 换 esbuild 压缩。
- 合理 splitChunks 分包、按需加载。
- 开发环境用 Vite（原生 ESM、免打包）。
