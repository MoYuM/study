# study-drill

多题库的「主动回忆 + 间隔复习」陪练仓库。**题库内容**与**学习进度**分离，git 记录历史，commit 前自动 lint 强规范。配合 Claude 的 `mastery-drill` 技能用。

## 目录布局

```
study-drill/
  banks/                          # 所有题库（可放多个，学不同方向）
    前端面试/
      meta.yml                    # 题库元信息：名称 / 分类清单 / 可选字段
      <分类>/<题目>.md             # 纯内容：frontmatter(题目/分类/id+可选字段) + 答案
  progress/
    前端面试.tsv                  # 学习进度：id ⇄ 掌握/下次复习/上次评测/备注（仅评过的题）
  lint.py                         # 题库 + 进度规范检查
  stats.py                        # 跨题库进度概览（python3 stats.py）
  .githooks/pre-commit            # commit 前自动 lint
  .claude/skills/mastery-drill/   # 陪练 skill（项目级）
  README.md
```

**核心原则**：`banks/` 只放题目内容（干净、可分享/复用）；学习进度全在 `progress/`，按 `id` 关联。lint 会阻止进度字段混进题库。

## 题目 md（纯内容）

```markdown
---
题目: 深拷贝
分类: JS
频率: 高频          # meta 声明的可选字段
id: 55e72a4d-...    # uuid，唯一，进度靠它关联
---
答案正文……
```

## 进度 TSV（`progress/<题库>.tsv`）

制表符分隔，只有评过的题才有行：

```
id	掌握	下次复习	上次评测	备注
55e72a4d-...	🔴生疏	2026-06-25	2026-06-24	循环引用(WeakMap)忘了…
```

掌握档位：🔴生疏 / 🟡夹生 / 🟢熟练 / ⭐已掌握。间隔：🔴+1d 🟡+3d 🟢+7d ⭐+21d；🟢/⭐ 没过打回 🔴。

## 加一个新题库（模板）

1. 建 `banks/<新题库名>/meta.yml`：
   ```
   名称: 操作系统
   说明: 408 操作系统
   分类: 进程, 内存, 文件系统, 并发, IO
   字段.难度: 简单, 中等, 困难       # 可选字段，想要别的照此加 字段.X
   ```
2. 在 `banks/<新题库名>/<分类>/` 下加题目 md（frontmatter：题目 / 分类 / id + 你声明的可选字段，正文写答案）。
3. 进度文件 `progress/<新题库名>.tsv` 首次陪练时自动产生。
4. `python3 lint.py` 校验。

## 用陪练

在本目录（`study-drill/`）下启动 Claude Code，首次 `/reload-skills`，然后说「开始陪练」「复习今天到期的」「练前端面试 AI 高频」「模拟面试」。Claude 会读题库内容 + 进度选题，盖答案考你、追问、揭晓打分，把结果写回 `progress/<题库>.tsv`。

## 看进度

```bash
python3 stats.py
```

显示各题库的总题数 / 未评测 / 🔴🟡🟢⭐ 分布 / 到期(下次复习≤今天)数 / 分类分布，外加总计。

## git + lint

```bash
git add -A && git commit -m "..."   # 提交前自动 lint，不过就拦
python3 lint.py                      # 也可手动校验
```

> 钩子通过 `core.hooksPath=.githooks` 启用（随仓库版本管理）。换机器克隆后若没生效：`git config core.hooksPath .githooks`。
