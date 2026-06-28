---
题目: "Token、上下文窗口、采样参数如何影响工程？"
分类: AI
频率: 高频
id: 385e29bd-9121-819a-a793-c1c31f1a3b2c
---
- Token
	- 定义：Token 是模型處理文字的基本單位
	- 中文/英文/代码切分不同：一个汉字≈2个token，一个英文字母≈1个token
	- 影响：成本/延迟/截断风险
- 上下文窗口：
	- 定义：是提供给 LLM 的、用于完成下一步推理或生成任务的全部信息集合
	- 不是越大越好（成本/延迟/噪声/Lost in the Middle）
- Temperature
	- 定义：控制输出的随机性
		- 0：最确定，适合代码生成，json提取，分类等
		- 1：最随机，适合头脑风暴，写作，创意
	- 生产要稳定可复现常调低。即使 Temperature=0 也可能不完全一致
- Top-P
	- 定义：和 Temperature 的作用相反，同时调 Temperature 和 Top-p 往往没有意义
- Top-K：
	- 定义：控制候选词的数量，越低候选词越集中，越高就越发散

### 参考资料
- [什麼是 Token，以及如何計算](https://help.openai.com/zh-hant/articles/4936856-what-are-tokens-and-how-to-count-them)