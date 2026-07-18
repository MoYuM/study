---
题目: "Monorepo 实践？"
分类: 前端工程
频率: 低频
id: 385e29bd-9121-8167-8c03-d6c6f0fa538d
---
Monorepo：一个仓库管理多个包/应用，共享配置、类型、工具链。工具：pnpm workspace、Turborepo、Nx、Lerna。优点：代码复用、统一依赖与版本、原子提交；难点：构建缓存、依赖提升、CI 增量。

## 发展史（问题 → 方案的链条）

❓ 一个仓库里放多个包，最早要解决的问题是什么？——包之间互相依赖，改了一个包，怎么统一给所有依赖它的包升版本号、统一发布？
✅ **Lerna**（2015 年发布）是 JS 生态最早的 monorepo 工具，专门解决"多包版本管理 + 协调发布"，一度成为事实标准。

❓ Lerna 解决了发布协调，但没解决"构建"本身的效率问题——仓库越大，每次构建/测试都要跑一遍全部包，越来越慢，怎么办？
✅ 2016 年，两位前 Google Angular 团队工程师 Jeff Cross 和 Victor Savkin 离职创业成立 Nrwl，把他们在 Google 内部使用 **Bazel**（Google 自用的超大规模 monorepo 构建工具）的经验带出来，做了 **Nx**——引入增量构建、任务依赖图、分布式任务执行这些概念，最早只支持 Angular，后来才变成框架无关的通用工具。

❓ Nx 功能全面但配置复杂，有没有更轻量、专注"构建缓存"这一件事的方案？
✅ Jared Palmer（Formik、TSDX 等开源项目作者）开发了 **Turborepo**，专注做好增量构建 + 远程缓存这一件事——同一份代码只要没变，缓存过的构建产物直接复用，不用重新跑。2021 年 12 月被 **Vercel 收购**，成为目前最流行的构建缓存方案之一。

**现状**：Lerna 因维护停滞过一段时间（2020-2022），后被 Nx 团队接手，如今内部直接用 Nx 的引擎做任务调度和缓存；Turborepo（Vercel）和 Nx（Nrwl）是目前两个最主流、仍在积极竞争的方案，`pnpm workspace`/`yarn workspace` 则是包管理器原生提供的"多包安装"能力，通常和 Nx/Turborepo 搭配使用，各自解决不同层面的问题（包管理 vs 构建调度）。

## 参考资料

- [With $8.6M in seed funding, Nx wants to take monorepos mainstream — TechCrunch](https://techcrunch.com/2022/11/17/with-8-6m-in-seed-funding-nx-wants-to-take-monorepos-mainstream/)
- [Vercel acquires Turborepo to accelerate build speed — Vercel Blog](https://vercel.com/blog/vercel-acquires-turborepo)
- [Turborepo, Nx, and Lerna: The Truth about Monorepo Tooling](https://dev.to/dataformathub/turborepo-nx-and-lerna-the-truth-about-monorepo-tooling-in-2026-71)
