---
题目: "如何理解 React Hook？"
分类: React
频率: 高频
id: 096a0d52-05b3-4891-8a49-87f5d8213d25
---
- 提供一种组件之间可以复用带状态逻辑的方式
- 更灵活的组织代码的方式
- 不必依赖 Class，其会导致门槛、编译方面的问题

## 追问：什么是 Hook 的"闭包陷阱"？

**不是**"`setState` 之后同步代码拿不到最新值，要等下次渲染"——那是所有 `setState` 更新的通用特性（异步生效），跟闭包无关，class 组件的 `this.setState` 也是一样。

真正的闭包陷阱长这样：

```js
useEffect(() => {
  const id = setInterval(() => {
    console.log(count); // 永远打印挂载时的值，比如 0
  }, 1000);
  return () => clearInterval(id);
}, []); // 空依赖数组
```

因为空依赖数组让这个 effect 只在挂载时执行一次，`setInterval` 的回调函数在第一次渲染时就被创建并"捕获"了当时的 `count`；之后即便 `count` 状态更新，这个已经存在的定时器回调引用的还是第一次渲染时闭包里的旧值，不会跟着变。**本质是：一个跨越多次渲染依然存活的函数（定时器回调、未清理的事件监听等），捕获了某一次渲染的旧值，且没有因为依赖变化被重新创建**——不是"当次渲染内部代码执行顺序"的问题。

## 发展史（问题 → 方案的链条）

**❓ class 组件的跨组件状态逻辑复用主要靠两种模式：Higher-Order Components（HOC，术语由 Sebastian Markbåge 2015 年 2 月的 "Enhance.js" gist 提出，Dan Abramov 同年 3 月发博文《Mixins Are Dead. Long Live Composition》推广，作为 React 移除 mixin 支持后的替代方案）和 Render Props（Michael Jackson 2017 年 9 月的演讲《Never Write Another HOC》与博文《Use a Render Prop!》推广）——两种模式都会造成"包装地狱"：组件树因为层层包裹变得很深，难以追踪某个 prop 到底从哪层传下来的**
逻辑复用的问题被"解决"了，但引入了组件树臃肿、调试困难的新代价，本质上还是绕开 class 写法的补丁，没有解决"逻辑只能按生命周期组织，不能按业务关注点组织"这个根本问题。

**✅ Hooks：2018 年 10 月 25 日 React Conf 上，Sophie Alpert 与 Dan Abramov 做开场演讲《React Today and Tomorrow》首次公开介绍 Hooks 的设计理念，同一天 Ryan Florence 做了实操演示《90% Cleaner React with Hooks》，同日 Sebastian Markbåge 在官方 RFC 仓库提交了 Hooks 提案（RFC #68，同年 11 月 21 日合并），2019 年 2 月 6 日 React 16.8 正式发布 Hooks 为稳定功能**
让状态逻辑可以按"业务关注点"自由组合、抽取成自定义 Hook 复用，不再需要嵌套额外的组件层级，从组件树结构上根治了包装地狱问题。

**❓ Hooks 放弃了 class 的实例（`this`），改用函数每次渲染都重新执行的方式实现——但这带来一个新问题：怎么保证多次渲染之间，同一个 `useState` 调用拿到的还是"同一份"状态，而不是每次渲染都被重新初始化？**
需要一种机制，把状态和"这是第几次 hook 调用"绑定起来，让状态能跨渲染保留。

**✅ Fiber 节点上按调用顺序保存 hook 记录（链表/数组结构），通过调用顺序索引在多次渲染之间匹配"同一个" hook——这就是"Hook 规则"（不能在条件/循环里调用 Hook）存在的原因：顺序一旦被打乱，状态就会跟错的 hook 记录对上**
但"函数每次渲染都重新执行"这个设计代价也带来了新问题——此前渲染里创建的闭包（定时器回调、事件回调）如果没有随依赖变化被重新创建，就会一直拿着旧值不放，这就是上面讲的闭包陷阱。

**现状：class 时代的 HOC/Render Props 模式已经很少在新代码里出现，Hooks 成为主流方案；但"函数式组件 + 每次渲染重新执行"这套设计换来了新的心智负担——Hook 调用顺序规则和闭包陷阱，都是这次设计范式转换必须付出的代价，不是 bug 而是特性的直接后果**

## 参考资料

- [Mixins Are Dead. Long Live Composition — Dan Abramov（2015-03）](https://medium.com/@dan_abramov/mixins-are-dead-long-live-higher-order-components-94a0d2f9e750)
- [Use a Render Prop! — Michael Jackson（2017-09-18）](https://medium.com/@mjackson/use-a-render-prop-50de598f11ce)
- [React Today and Tomorrow — React Conf 2018](https://www.youtube.com/watch?v=V-QO-KO90iQ)
- [RFC #68 — React Hooks](https://github.com/reactjs/rfcs/blob/main/text/0068-react-hooks.md)
- [React v16.8: The One With Hooks（2019-02-06）](https://legacy.reactjs.org/blog/2019/02/06/react-v16.8.0.html)
