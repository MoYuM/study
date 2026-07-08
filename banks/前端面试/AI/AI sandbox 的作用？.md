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

**✅ ChatGPT Code Interpreter（2023 年 3 月以插件形式 alpha 宣布，同年 7 月 6 日对所有 Plus 用户开放，后改名 Advanced Data Analysis）：把"执行 AI 生成的 Python 代码"这个能力产品化，运行在隔离沙箱容器里，无 root 权限、无互联网访问**
第一次让"大规模、面向消费者"的产品把"执行不可信 AI 生成代码"这件事标准化，具体限制维度（断网、无 root）成为这类沙箱的标配。（早期流传的"基于 Ubuntu 20.04.6、120 秒执行时限"这个具体描述已过时——2024-2025 年多份独立逆向研究显示当前底层实际是 Debian 12 + gVisor，见下方"业界现状"。）

**❓ 消费级产品够用，但开发者要自己搭建 Agent 执行环境时，从零用 Docker 手搭隔离设计成本高——需要能直接开箱即用、专门为 AI/LLM 场景设计的沙箱基础设施**
市面上出现了专门做"浏览器端沙箱"和"AI sandbox 即服务"的产品。

**✅ WebContainer（StackBlitz，2021 年 5 月发布，基于 WebAssembly + WASI 把完整 Node.js 运行时编译进浏览器，含虚拟化 TCP 网络栈，无需服务端容器）+ E2B（2023 年由 Vasek Mlejnsky 与 Tomas Valenta 创立，基于 Firecracker microVM 实现毫秒级启动的隔离沙箱，专门服务 LLM/AI Agent 场景）**
这类工具把"给 AI 一个安全的地方运行代码"变成了一个专门的产品品类，而不是每个团队各自拿 Docker 从零搭建。

**现状：容器（Docker，通用方案）/ WebContainer（浏览器端方案）/ iframe 沙箱（轻量前端场景）/ 进程隔离（底层机制）四类手段并存，2023 年后 AI Agent 的兴起让"沙箱"从"运维/安全的通用需求"细分出了"专门为不可预知的 AI 生成代码/行为设计"这个新场景，催生了 E2B 这类专门产品**

## 业界现状：本地 Agent 用 OS 原生沙箱，云端产品要么不公开、要么走容器/虚拟机

**编程类 Agent（本地 CLI/编辑器）：清一色收敛到 OS 原生沙箱**

- **Claude Code**：macOS 用 Seatbelt（`sandbox-exec`），Linux 用 bubblewrap（可选 seccomp 阻断 socket 创建）。文件系统默认只允许写当前工作目录+会话临时目录；网络默认不放行任何域名，命令首次请求新域名会弹窗批准（默认走沙箱外代理，不做 TLS 终止）。
- **Codex CLI**：同样是 macOS Seatbelt、Linux bubblewrap+seccomp（Landlock 作兼容回退），并用 `--unshare-user/pid/net` 等 namespace 隔离；默认文件系统整个根目录只读，网络默认关闭，需显式配置开启。
- **Cursor**：macOS Seatbelt、Linux Landlock+seccomp、Windows 借道 WSL2；官方分了三档批准模式（Auto-review 默认/Allowlist/Run Everything 即 YOLO 模式），官方数据称沙箱化 agent "少中断 40%"，默认限制网络访问。
- **Gemini CLI**：提供 5 种可选后端（macOS Seatbelt、Docker/Podman、Linux gVisor"最强隔离"、Windows 原生、实验性 LXC/LXD），需用户显式选择启用。

四家的共同点：本地跑在用户自己机器上的 CLI/编辑器工具，直接复用操作系统级隔离原语（Seatbelt/bubblewrap/Landlock+seccomp），不引入容器/虚拟机这类更重的方案——这类工具只需要隔离"这一个进程"，OS 原生机制足够且启动零开销。

**云端消费产品：官方基本不公开细节，只能靠第三方逆向工程**

- **ChatGPT Code Interpreter/Advanced Data Analysis**：官方文档只说"完全沙箱化的虚拟机"，未点名具体技术。2024-2025 年多份独立安全研究逆向发现：底层是 **gVisor** 沙箱化容器，跑在 Azure Kubernetes 上，镜像是 **Debian 12**（此前网传的"Ubuntu 20.04.6"已过时/不准确，"内核版本 4.4"实为 gVisor 用户态内核的固定签名而非真实宿主内核），非 root、无出站网络。OpenAI 2024 年一篇讲研究基础设施安全的官方博客提到对"高风险"工作负载用 gVisor 做额外隔离，可作旁证但非直接针对这个消费产品的官方说明。
- **Replit Agent**：自研 **omegajail**（源自开源判题系统 omegaUp）——用 namespace + seccomp-bpf + cgroups 做隔离；容易被误认为是"Nix"，但 Nix 管的是依赖版本一致性，不是安全边界，两者是完全不同的机制。

**专门的沙箱基础设施产品：隔离强度是一个可选的光谱**

- **E2B**：Firecracker microVM，每个沙箱独立内核（硬件级虚拟化隔离），隔离最强，冷启动 <200ms，官方明确表示容器隔离"不够安全"所以选择微虚拟机路线。
- **Modal**：gVisor 用户态内核，在隔离强度和 GPU 直通能力之间取平衡。
- **Daytona**：Docker 容器（可选叠加 gVisor），主打启动速度（宣称 27-90ms），隔离强度相对最弱。

**结论**：不是所有 AI 产品都用同一种沙箱方案——本地 Agent 因为只需隔离"用户自己机器上的一个进程"，收敛到轻量的 OS 原生沙箱；云端多租户产品因为要复用硬件、隔离陌生用户的代码，天然需要更强的容器/微虚拟机隔离，且大多不愿公开具体实现（只有专门"卖沙箱"的基础设施公司如 E2B/Modal 会主动讲清楚技术选型）。

## 参考资料

- [Docker (software) — Wikipedia](https://en.wikipedia.org/wiki/Docker_(software))
- [Introducing WebContainers — StackBlitz Blog（2021）](https://blog.stackblitz.com/posts/introducing-webcontainers/)
- [E2B — The Enterprise AI Agent Cloud](https://e2b.dev/)
- [Claude Code — Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing)
- [Codex — Sandbox concepts](https://developers.openai.com/codex/concepts/sandboxing)
- [Cursor — Implementing a secure sandbox for local agents](https://cursor.com/blog/agent-sandboxing)
- [Gemini CLI — sandbox.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/sandbox.md)
- [Poking Around ChatGPT's Sandbox](https://mkarots.github.io/blog/chatgpt-sandbox-exploration/)
- [Secrets of the ChatGPT Linux system](https://incoherency.co.uk/blog/stories/chatgpt-linux.html)
- [Replit — AI Agent Code Execution API](https://blog.replit.com/ai-agents-code-execution)
- [E2B — Firecracker vs QEMU](https://e2b.dev/blog/firecracker-vs-qemu)
- [Modal — Sandboxes docs](https://modal.com/docs/guide/sandboxes)
- [Daytona GitHub](https://github.com/daytonaio/daytona)
