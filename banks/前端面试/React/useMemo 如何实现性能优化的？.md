---
题目: "useMemo 如何实现性能优化的？"
分类: React
频率: 高频
id: 2b89d23f-3806-42ca-b96f-ad55b6369bdd
---
```tsx
function updateMemo<T>(
  nextCreate: () => T,
  deps: Array<mixed> | void | null,
): T {
  const hook = updateWorkInProgressHook();
  const nextDeps = deps === undefined ? null : deps;
  const prevState = hook.memoizedState;
  // Assume these are defined. If they're not, areHookInputsEqual will warn.
  if (nextDeps !== null) {
    const prevDeps: Array<mixed> | null = prevState[1];
    if (areHookInputsEqual(nextDeps, prevDeps)) {
      return prevState[0];
    }
  }
  const nextValue = nextCreate();
  
  // DEV 下的特殊处理，不用管
  // if (shouldDoubleInvokeUserFnsInHooksDEV) {
  //   setIsStrictModeForDevtools(true);
  //   nextCreate();
  //   setIsStrictModeForDevtools(false);
  // }
  hook.memoizedState = [nextValue, nextDeps];
  return nextValue;
}
```

useMemo 对比上次的 deps 和当前的 deps 如果相同就跳过计算环节，直接将缓存的计算解过缓存
