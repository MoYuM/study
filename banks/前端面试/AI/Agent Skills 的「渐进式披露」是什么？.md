---
题目: "Agent Skills 的「渐进式披露」是什么？"
分类: AI
频率: 低频
id: 385e29bd-9121-8114-bc77-ef97260cedfa
---
渐进式披露（Progressive Disclosure）：Skill 分层按需加载，降低上下文占用。

- 元数据层：启动时只加载每个技能的 name + description，让模型知道「有哪些技能、何时该用」。
- 技能主体：命中后才加载完整 [SKILL.md](http://SKILL.md)（步骤 / SOP）。
- 附加资源：执行到那一步才加载脚本 / 参考文件。

定位：Skills 与 MCP **互补**——MCP 解决「工具怎么接入」，Skills 解决「拿到能力后按什么流程做好」，并通过分层加载减少一次性塞入的上下文。

## 参考资料

- [Anthropic — Agent Skills 工程博客](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [JavaGuide — 万字详解 Agent Skills](https://javaguide.cn/ai/agent/skills.html)
