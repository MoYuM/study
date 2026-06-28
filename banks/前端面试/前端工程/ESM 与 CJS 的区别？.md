---
题目: "ESM 与 CJS 的区别？"
分类: 前端工程
频率: 高频
id: 385e29bd-9121-811d-9c80-c49637809bd3
---
- ESM：静态导入（编译时确定依赖）、支持 Tree-shaking、可异步加载、import/export，是值引用（活绑定）。
- CJS：运行时同步加载、require/module.exports、动态、不易 Tree-shaking，是值拷贝。

## 活绑定 vs 拷贝

ESM 导出的是**活绑定**（live binding）：导入方拿到的是对原始变量的引用，源头变了它跟着变。

```js
// counter.mjs
export let count = 0
export function inc() { count++ }

// main.mjs
import { count, inc } from './counter.mjs'
inc()
console.log(count) // 1 ← 跟着变了
```

CJS 导出的是**值拷贝**：`require` 时复制一份快照，源头之后的变化不影响已拿到的值。

```js
// counter.js
let count = 0
function inc() { count++ }
module.exports = { count, inc }

// main.js
const { count, inc } = require('./counter')
inc()
console.log(count) // 0 ← 还是旧值（拿的是拷贝）
```

**坑**：用 CJS 时如果想拿到最新值，要每次重新 `require().count`，或导出函数而非值。
