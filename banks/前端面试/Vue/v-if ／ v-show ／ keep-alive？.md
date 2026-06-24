---
题目: "v-if / v-show / keep-alive？"
分类: Vue
频率: 低频
id: 385e29bd-9121-81a6-a42f-f5fb864e3e70
---
- v-if：真正创建/销毁 DOM，切换开销大，适合不常切换。
- v-show：只切 `display`，初始渲染后切换快，适合频繁切换（如 tab）。
- keep-alive：缓存组件实例避免重复渲染，配 activated/deactivated 生命周期。
