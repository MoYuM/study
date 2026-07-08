---
题目: "AI sandbox 的作用？"
分类: AI
频率: 低频
id: 385e29bd-9121-815c-a5ae-c6ac3c90ce5f
---
AI sandbox：安全执行 AI 生成代码/工具调用的隔离环境（如 WebContainer、容器、iframe 沙箱、进程隔离）。

作用：限制文件/网络/系统调用权限，防止恶意/出错代码损害宿主环境，限定资源与超时，是 AI Coding/Agent 执行类产品的安全基线。

## 发展史（问题 → 方案的链条）

**❓ 软件安全领域"沙箱隔离不可信代码"的需求由来已久——Docker（Solomon Hykes 2013 年 3 月 15 日在 PyCon 闪电演讲首次公开并开源，同年 10 月 dotCloud 改名为 Docker Inc. 专注容器技术，基于 Linux namespaces + cgroups 实现隔离）让容器化隔离成为工程标配，但这解决的是"部署/运维"场景的通用隔离，不是专门为"运行 AI 生成的、不可预知的代码"设计的**
AI 生成代码在执行前无法静态保证其安全性——不像人写的代码经过 review，模型输出的代码可能因为幻觉/被注入攻击而包含危险操作（删除文件、发起恶意网络请求）。

**✅ ChatGPT Code Interpreter（2023 年 3 月以插件形式 alpha 宣布，同年 7 月 6 日对所有 Plus 用户开放，后改名 Advanced Data Analysis）：把"执行 AI 生成的 Python 代码"这个能力产品化，运行在基于 Ubuntu 20.04.6 的隔离沙箱容器里，无 root 权限、无互联网访问、单进程 120 秒执行时限**
第一次让"大规模、面向消费者"的产品把"执行不可信 AI 生成代码"这件事标准化，具体限制维度（断网、无 root、执行时限）成为这类沙箱的标配。

**❓ 消费级产品够用，但开发者要自己搭建 Agent 执行环境时，从零用 Docker 手搭隔离设计成本高——需要能直接开箱即用、专门为 AI/LLM 场景设计的沙箱基础设施**
市面上出现了专门做"浏览器端沙箱"和"AI sandbox 即服务"的产品。

**✅ WebContainer（StackBlitz，2021 年 5 月发布，基于 WebAssembly + WASI 把完整 Node.js 运行时编译进浏览器，含虚拟化 TCP 网络栈，无需服务端容器）+ E2B（2023 年由 Vasek Mlejnsky 与 Tomas Valenta 创立，基于 Firecracker microVM 实现毫秒级启动的隔离沙箱，专门服务 LLM/AI Agent 场景）**
这类工具把"给 AI 一个安全的地方运行代码"变成了一个专门的产品品类，而不是每个团队各自拿 Docker 从零搭建。

**现状：容器（Docker，通用方案）/ WebContainer（浏览器端方案）/ iframe 沙箱（轻量前端场景）/ 进程隔离（底层机制）四类手段并存，2023 年后 AI Agent 的兴起让"沙箱"从"运维/安全的通用需求"细分出了"专门为不可预知的 AI 生成代码/行为设计"这个新场景，催生了 E2B 这类专门产品**

## 参考资料

- [Docker (software) — Wikipedia](https://en.wikipedia.org/wiki/Docker_(software))
- [ChatGPT's Code Interpreter is now Advanced Data Analysis — Pluralsight](https://www.pluralsight.com/resources/blog/ai-and-data/ChatGPT-Advanced-Data-Analytics)
- [Introducing WebContainers — StackBlitz Blog（2021）](https://blog.stackblitz.com/posts/introducing-webcontainers/)
- [E2B — The Enterprise AI Agent Cloud](https://e2b.dev/)
