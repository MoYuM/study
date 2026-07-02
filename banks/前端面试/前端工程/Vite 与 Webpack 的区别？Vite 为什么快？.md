---
题目: "Vite 与 Webpack 的区别？Vite 为什么快？"
分类: 前端工程
频率: 高频
id: 385e29bd-9121-81b9-9642-ede1eb343d05
---
- 开发环境：Webpack 先打包再启动（慢）；Vite 基于浏览器原生 ESM 按需编译，启动快、HMR 更细。
- 生产环境：Vite 7 及之前用 Rollup 打包；**Vite 8（2025 年底）起默认改用 Rolldown**（Rust 编写、兼容 Rollup 插件）。Webpack 自身打包。
- Vite 快的原因：免打包启动 + esbuild 预构建依赖 + 按需编译。大型项目、复杂定制仍可能选 Webpack。

## 为什么生产环境仍需要打包

打包本质是 Tree-shaking + 懒加载 + chunk 分割。尽管原生 ESM 已被广泛支持，但嵌套 import 会导致大量额外的网络往返，即使有 HTTP/2 多路复用，未打包的生产环境仍然效率低下——所以生产构建通常仍要打包（Vite 生产环境也是打包的，只是开发环境不打包）。

## 参考资料

- [Vite 官方 — 为什么选 Vite](https://cn.vitejs.dev/guide/why.html)
