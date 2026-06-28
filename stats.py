#!/usr/bin/env python3
"""
跨题库学习进度概览（只读报告）。

用法：
  python3 stats.py            # 所有题库 + 合计
  python3 stats.py 前端面试    # 只看某一个题库
显示每个题库：总题数 / 未评测 / 🔴🟡🟢⭐ 分布 / 到期(下次复习≤今天) / 分类分布，外加总计。
"""
import os, sys, glob, datetime
from collections import Counter

SELF     = os.path.dirname(os.path.abspath(__file__))
BANKS    = os.path.join(SELF, "banks")
PROGRESS = os.path.join(SELF, "progress")
LEVELS = ["🔴生疏", "🟡夹生", "🟢熟练", "⭐已掌握"]
TODAY = datetime.date.today()


def is_disabled(path):
    """快速检查 .md 文件是否有 禁用: true。"""
    try:
        lines = open(path, encoding="utf-8").read().split("\n")
        if not lines or lines[0].strip() != "---":
            return False
        close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if close is None:
            return False
        for ln in lines[1:close]:
            if ":" in ln:
                k, v = ln.split(":", 1)
                if k.strip() == "禁用" and v.strip().lower() in ("true", "是", "yes"):
                    return True
    except Exception:
        pass
    return False


def parse_fm(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if close is None:
        return {}
    fm = {}
    for ln in lines[1:close]:
        if ":" in ln and ln.strip():
            k, v = ln.split(":", 1)
            v = v.strip()
            if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
                v = v[1:-1].replace('\\"', '"')
            fm[k.strip()] = v
    return fm


def read_progress(bank):
    """返回 {id: (掌握, 下次复习)}，读 progress/<bank>/*.md frontmatter。"""
    rows = {}
    prog_dir = os.path.join(PROGRESS, bank)
    if not os.path.isdir(prog_dir):
        return rows
    for p in glob.glob(os.path.join(prog_dir, "*.md")):
        fm = parse_fm(open(p, encoding="utf-8").read())
        if not fm.get("id"):
            continue
        掌握 = fm.get("掌握", "")
        if not 掌握 or 掌握 == "🆕未评测":
            continue
        rows[fm["id"]] = (掌握, fm.get("下次复习", ""))
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
    only = sys.argv[1] if len(sys.argv) > 1 else None
    bank_dirs = sorted(d for d in glob.glob(os.path.join(BANKS, "*")) if os.path.isdir(d))
    if only:
        bank_dirs = [d for d in bank_dirs if os.path.basename(d) == only]
        if not bank_dirs:
            print(f"题库 `{only}` 不存在。"); return
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
            if not is_disabled(md):
                cats[os.path.basename(os.path.dirname(md))] += 1
        total = sum(cats.values())

        prog = read_progress(name)
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

    if only:
        return
    g_untested = g_total - g_scored
    print("━━ 合计 ━━")
    print(f"{len(bank_dirs)} 个题库 · {g_total} 题  |  未评测 {g_untested}  "
          f"{bar(g_levels, g_total)}  |  到期 {g_due}\n")


if __name__ == "__main__":
    main()
