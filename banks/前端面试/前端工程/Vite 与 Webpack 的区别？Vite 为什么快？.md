---
题目: "Vite 与 Webpack 的区别？Vite 为什么快？"
分类: 前端工程
频率: 高频
id: 385e29bd-9121-81b9-9642-ede1eb343d05
---
- 开发环境：Webpack 先打包再启动（慢）；Vite 基于浏览器原生 ESM 按需编译，启动快、HMR 更细。
- 生产环境：Vite 7 及之前用 Rollup 打包；**Vite 8（2025 年底）起默认改用 Rolldown**（Rust 编写、兼容 Rollup 插件）。Webpack 自身打包。
- Vite 快的原因：免打包启动 + esbuild 预构建依赖 + 按需编译。大型项目、复杂定制仍可能选 Webpack。

## 参考资料

- [Vite 官方 — 为什么选 Vite](https://cn.vitejs.dev/guide/why.html)
