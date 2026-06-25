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
  stats.py                        # 跨题库进度概览（python3 stats.py [题库名]）
  pick.py                         # 快速出题：按优先级盖答案选题 + 多维筛选
  .githooks/pre-commit            # commit 前自动 lint
  .claude/skills/mastery-drill/   # 陪练 skill（项目级）
  README.md
```

@.claude/skills/mastery-drill
