# study-drill

通用的、AI / skill 驱动的**间隔复习学习系统**。`banks/` 下每个题库一个学习方向（前端面试、操作系统…），用 `mastery-drill` 技能陪练，git 记录历史，commit 前自动 lint 强规范。

## 怎么用

- **陪练**：「开始陪练」「复习今天到期的」「练前端面试 AI 高频」「模拟面试」。`mastery-drill` 技能会读题库 + 进度选题、盖答案考、追问、揭晓打分、写回进度。
- **建 / 扩题库**：「建个 X 题库」「给 Y 加 N 道题」「把这份笔记做成题库」。同样走 `mastery-drill` 技能的 authoring 流程。
- **看进度**：`python3 stats.py` —— 跨题库概览（各档位分布、到期数、分类分布）。

## 结构与铁律（细节见 `README.md` 与 mastery-drill 技能）

- **题库内容**：`banks/<题库>/<分类>/<题目>.md` —— frontmatter 只放 `题目 / 分类 / id (+ meta 声明的可选字段)`，正文放答案。**绝不含进度字段**。
- **学习进度**：`progress/<题库>.tsv` —— `id  掌握  下次复习  上次评测  备注`，只有评过的题有行，按 `id` 关联。
- 每个题库一个 `banks/<题库>/meta.yml` 声明分类清单与可选字段。
- 改完跑 `python3 lint.py`；commit 会自动跑 lint，不过就拦。

## commit 规范

- 一次陪练 = 一个 commit；内容（`banks/`）与进度（`progress/`）分开提交。
- 前缀：`drill(<题库>):` 进度更新 ／ `bank(<题库>):` 题库增改 ／ `chore:`·`docs:`·`refactor:` 工具文档结构。
- 只本地提交，不 push（除非用户要求）。
