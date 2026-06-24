---
题目: "JSON Mode 与 Structured Outputs 的区别？"
分类: AI
频率: 低频
掌握: 
下次复习: 
上次评测: 
id: 385e29bd-9121-8131-badc-e4919beaffb0
备注: ""
---
- JSON Mode：保证输出是合法 JSON，但不保证符合你的结构。
- Structured Outputs：按你给的 JSON Schema 约束字段/类型/枚举，更可靠。

两者都不能免除服务端校验；「请返回 JSON」只是自然语言提示，不可靠。输出后仍要 schema 校验 + 失败重试/修复。
