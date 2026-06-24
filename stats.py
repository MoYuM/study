#!/usr/bin/env python3
"""
跨题库学习进度概览（只读报告）。

用法：python3 stats.py
显示每个题库：总题数 / 未评测 / 🔴🟡🟢⭐ 分布 / 到期(下次复习≤今天) / 分类分布，外加总计。
"""
import os, glob, datetime
from collections import Counter

SELF = os.path.dirname(os.path.abspath(__file__))
BANKS = os.path.join(SELF, "banks")
PROGRESS = os.path.join(SELF, "progress")
LEVELS = ["🔴生疏", "🟡夹生", "🟢熟练", "⭐已掌握"]
TODAY = datetime.date.today()


def read_progress(path):
    """返回 {id: (掌握, 下次复习)}。"""
    rows = {}
    if not os.path.exists(path):
        return rows
    lines = open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    for ln in lines[1:]:
        c = ln.split("\t")
        if len(c) >= 4 and c[0]:
            rows[c[0]] = (c[1], c[2])
    return rows


def parse_date(s):
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        return None


def bar(level_counts, total):
    """一行档位分布。"""
    parts = [f"{lvl[0]} {level_counts.get(lvl, 0)}" for lvl in LEVELS]
    return "  ".join(parts)


def main():
    bank_dirs = sorted(d for d in glob.glob(os.path.join(BANKS, "*")) if os.path.isdir(d))
    print(f"\n📊 study-drill 进度概览 · {TODAY}\n")

    g_total = g_scored = g_due = 0
    g_levels = Counter()
    if not bank_dirs:
        print("（banks/ 下还没有题库）\n")
        return

    for bd in bank_dirs:
        name = os.path.basename(bd)
        cats = Counter()
        for md in glob.glob(os.path.join(bd, "*", "*.md")):
            cats[os.path.basename(os.path.dirname(md))] += 1
        total = sum(cats.values())

        prog = read_progress(os.path.join(PROGRESS, f"{name}.tsv"))
        scored = len(prog)
        untested = total - scored
        levels = Counter(lvl for lvl, _ in prog.values())
        due = sum(1 for lvl, nxt in prog.values()
                  if (d := parse_date(nxt)) and d <= TODAY)

        g_total += total; g_scored += scored; g_due += due; g_levels += levels

        pct = f"{round(scored / total * 100)}%" if total else "0%"
        print(f"▌{name} — {total} 题（已练 {pct}）")
        print(f"  未评测 {untested}    {bar(levels, total)}")
        print(f"  ⏰ 到期(≤今天) {due}")
        cat_line = " · ".join(f"{c} {n}" for c, n in cats.most_common())
        print(f"  分类  {cat_line}\n")

    g_untested = g_total - g_scored
    print("━━ 合计 ━━")
    print(f"{len(bank_dirs)} 个题库 · {g_total} 题  |  未评测 {g_untested}  "
          f"{bar(g_levels, g_total)}  |  到期 {g_due}\n")


if __name__ == "__main__":
    main()
