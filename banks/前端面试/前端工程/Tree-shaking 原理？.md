---
题目: "Tree-shaking 原理？"
分类: 前端工程
频率: 低频
id: 385e29bd-9121-8197-8de2-de12bd78f537
---
Tree-shaking：打包时消除未被引用的死代码。依赖 ESM 的静态结构（import/export 编译时可分析），标记未使用导出再删除。需注意副作用（package.json 的 sideEffects 配置）、CJS 不可靠 shake。
