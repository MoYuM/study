---
题目: "AI 应用怎么做评测（Golden Set / LLM-as-Judge）？"
分类: AI
频率: 低频
id: 385e29bd-9121-81c3-8a19-d95bbc52eca7
---
- 不能只靠公开 benchmark（不代表你的业务分布）。
- Golden Set：覆盖正常/边缘/对抗/高权重失败样本，重分布而非重数量。
- LLM-as-Judge：提效但有位置/冗长/同源偏差，不能完全替代人工。
- RAG/Agent 要分段评测；配合离线评测 + Trace 回放 + 线上灰度。

## 发展史（问题 → 方案的链条）

**❓ 早期评估语言模型主要靠公开学术 benchmark：GLUE（2018 年 EMNLP Workshop）、SuperGLUE（2019 年 NeurIPS）、再到 MMLU（Hendrycks 等人，2020 年，arXiv:2009.03300，覆盖 57 个学科任务）——这些 benchmark 测的是模型的通用能力**
但业务落地后发现 benchmark 分数高不代表这个具体产品在真实场景下好用——benchmark 分布跟真实业务查询分布完全不同，训练数据也可能已经"背过"benchmark 原题（数据污染）。

**✅ 自建评测集（Golden Set）：企业级实践转向针对自己产品构造评测样本——OpenAI 2023 年 3 月 14 日随 GPT-4 发布同步开源了 evals 框架，鼓励开发者贡献自定义评测集**
不再依赖别人的通用 benchmark，用真实业务查询 + 已知历史失败案例 + 人工构造的边缘/对抗样本，衡量"这个产品在真实分布下好不好用"。

**❓ 有了自建评测集，规模上来后靠人工一条条看依然太慢太贵，产品迭代速度等不起**
需要一种能自动化打分、又比简单规则（字符串匹配）更懂语义的评估方式。

**✅ LLM-as-Judge：Zheng 等人 2023 年 6 月 9 日的论文《Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena》（arXiv:2306.05685，伯克利团队，后被 NeurIPS 2023 接收）系统提出并验证了"用强模型当裁判打分"这套方法，同时这篇论文也首次系统记录了位置偏差（position bias）、冗长偏差（verbosity bias）、自我偏好偏差（self-enhancement bias）这几种裁判偏差**
让评测规模化成为可能，但论文本身也明确指出了这几种偏差，不能完全替代人工。

**❓ 裁判有偏差、自建集覆盖的也只是通用 QA/对话场景，遇到 RAG/Agent 这种多阶段管道，最终答案错了不知道是哪个环节的锅**
需要把"评测一个最终答案对不对"拆成"评测管道里每个阶段"。

**✅ 分段评测框架：Ragas（2023 年 9 月）把 RAG 拆成检索质量（context precision/recall）和生成质量（faithfulness）等独立可衡量指标，是分段评测思路在 RAG 场景下的具体落地**

**现状：离线评测（Golden Set + LLM-as-Judge 打分，人工抽样复核校准裁判）+ Trace 回放（复现线上失败案例）+ 线上灰度（小流量验证），这套组合是当前 AI 应用评测工程化的标准实践，没有单一"银弹"方法**

## 参考资料

- [MMLU 论文（arXiv:2009.03300）](https://arxiv.org/abs/2009.03300)
- [OpenAI evals GitHub](https://github.com/openai/evals)
- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena（arXiv:2306.05685）](https://arxiv.org/abs/2306.05685)
- [Ragas 论文（arXiv:2309.15217）](https://arxiv.org/abs/2309.15217)
