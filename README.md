# 面试准备

前端面试题库（纯本地，每题一个 Markdown）+ 掌握度记录 + 陪练 skill。git 记录历史，commit 前自动 lint 强规范。

## 目录布局

| 路径 | 作用 |
|---|---|
| `题库/<分类>/<题目>.md` | 每道题一个 md：frontmatter 存元数据（分类/频率/掌握/复习日期/id/备注），正文存答案。共 172 题。 |
| `lint.py` | 题库规范检查（字段齐全 / 取值合法 / 日期格式 / id 唯一 / 评测态与日期一致 / 答案非空）。 |
| `.githooks/pre-commit` | commit 前自动跑 `lint.py`，不通过就拦下提交。 |
| `.claude/skills/mastery-drill/` | 陪练 skill（项目级，只在本目录下工作时被发现）。 |
| `README.md` | 本说明。 |

## 每题 md 格式

```markdown
---
题目: 深拷贝
分类: JS
频率: 高频
掌握: 🔴生疏            # 🔴生疏/🟡夹生/🟢熟练/⭐已掌握；未评测留空
下次复习: 2026-06-25     # YYYY-MM-DD；未评测留空
上次评测: 2026-06-24
id: 55e72a4d-7a4c-4142-a6b5-045c0adbae0e
备注: "循环引用解法(WeakMap)忘了；..."
---
深拷贝递归复制对象所有层级……（答案正文）
```

间隔复习：🔴+1d、🟡+3d、🟢+7d、⭐+21d；🟢/⭐ 没过直接打回 🔴。

## 用陪练

在本目录（`面试准备/`）下启动 Claude Code（cwd 在这），首次 `/reload-skills`，然后直接说：

- 「开始陪练」/「考考我 5 道」
- 「复习今天到期的」（frontmatter 里 `下次复习 ≤ 今天`）
- 「只练 AI 高频」/「专挑生疏的」
- 「模拟面试」

Claude 会扫题库 frontmatter 选题、盖答案考你、追问、揭晓打分、把掌握度写回 frontmatter。

## git + lint

```bash
git add -A && git commit -m "..."   # 提交前自动 lint，不过就拦下
python3 lint.py                      # 也可手动校验
```

新增/改题：在 `题库/<分类>/` 下加/改 md，保证 frontmatter 合规（`id` 用一个 uuid、未评测字段留空）。lint 会把关。

> 钩子通过 `core.hooksPath=.githooks` 启用（随仓库版本管理）。换台机器克隆后若钩子没生效，跑一次 `git config core.hooksPath .githooks`。
