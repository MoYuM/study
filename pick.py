#!/usr/bin/env python3
"""
快速出题（盖答案选题器）—— 通用多题库版。

把题库内容（banks/）与学习进度（progress/<题库>.tsv）按 id 关联，按 mastery-drill
的优先级挑题，**只输出题目元信息 + 文件路径，绝不打印答案正文**（盖答案是主动回忆的前提）。

默认排序优先级（对齐 SKILL.md 第三步）：
  今日到期复习（下次复习≤今天）＞ 从未评测 ＞ 🔴/🟡 低档位 ＞ 高频/重点
组内再以「到期早→档位低→高频→随机抖动」打散，避免每次都抽到同几道。

用法示例：
  python3 pick.py                       # 默认题库、按优先级出 5 题
  python3 pick.py 前端面试 -n 8         # 指定题库、出 8 题
  python3 pick.py --due                 # 只出今天到期复习的
  python3 pick.py --new                 # 只出从未评测的
  python3 pick.py --weak                # 只出 🔴生疏/🟡夹生
  python3 pick.py --cat JS,React        # 只出这些分类
  python3 pick.py --field 频率=高频      # 按 meta 声明的可选字段筛（可重复）
  python3 pick.py --level 🟢            # 只出某档位（名/emoji 都认）
  python3 pick.py --random              # 纯随机，无视优先级
  python3 pick.py --json                # 结构化输出，给程序/Claude 精确解析
  python3 pick.py --all --weak          # 列出全部薄弱题（不截断），看池子有多大
"""
import os, re, sys, glob, random, json, argparse, datetime
from collections import Counter

SELF = os.path.dirname(os.path.abspath(__file__))
BANKS = os.path.join(SELF, "banks")
PROGRESS = os.path.join(SELF, "progress")
TODAY = datetime.date.today()

LEVELS = ["🔴生疏", "🟡夹生", "🟢熟练", "⭐已掌握"]
LEVEL_RANK = {lvl: i for i, lvl in enumerate(LEVELS)}          # 🔴=0 … ⭐=3（越小越弱）
WEAK = {"🔴生疏", "🟡夹生"}


# ── 解析 frontmatter / 进度（与 lint.py、stats.py 行为一致） ──────────────
def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        v = v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return v


def parse_fm(text):
    """返回 frontmatter dict（不读正文，盖答案）。坏 frontmatter → None。"""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if close is None:
        return None
    fm = {}
    for ln in lines[1:close]:
        if ":" in ln and ln.strip():
            k, v = ln.split(":", 1)
            fm[k.strip()] = unquote(re.sub(r"\s+#.*$", "", v))
    return fm


def read_progress(path):
    """返回 {id: {掌握, 下次复习, 上次评测, 备注}}。"""
    rows = {}
    if not os.path.exists(path):
        return rows
    lines = open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    for ln in lines[1:]:
        c = ln.split("\t")
        if len(c) >= 5 and c[0]:
            rows[c[0]] = {"掌握": c[1], "下次复习": c[2], "上次评测": c[3], "备注": c[4]}
    return rows


def parse_date(s):
    try:
        return datetime.date.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def list_banks():
    return sorted(os.path.basename(d) for d in glob.glob(os.path.join(BANKS, "*"))
                  if os.path.isdir(d))


def load_questions(bank):
    """把一个题库的题目 + 进度组装成候选列表。"""
    bankdir = os.path.join(BANKS, bank)
    prog = read_progress(os.path.join(PROGRESS, f"{bank}.tsv"))
    out = []
    for p in glob.glob(os.path.join(bankdir, "*", "*.md")):
        fm = parse_fm(open(p, encoding="utf-8").read())
        if fm is None or not fm.get("id"):
            continue
        if fm.get("禁用", "").lower() in ("true", "是", "yes"):
            continue
        pr = prog.get(fm["id"])
        nxt = parse_date(pr["下次复习"]) if pr else None
        out.append({
            "id": fm["id"],
            "题目": fm.get("题目", "").strip(),
            "分类": os.path.basename(os.path.dirname(p)),
            "档位": pr["掌握"] if pr else None,
            "下次复习": pr["下次复习"] if pr else None,
            "上次评测": pr["上次评测"] if pr else None,
            "备注": pr["备注"] if pr else None,
            "未评测": pr is None,
            "到期": bool(nxt and nxt <= TODAY),
            "_nxt": nxt,
            "fm": fm,                                  # 含可选字段（频率/难度…）
            "file": os.path.relpath(p, SELF),
        })
    return out


# ── 筛选 ──────────────────────────────────────────────────────────────────
def norm_level(s):
    """'🟢' / '熟练' / '🟢熟练' → 标准档位串；认不出返回原串。"""
    s = s.strip()
    for lvl in LEVELS:
        if s == lvl or s == lvl[0] or s == lvl[1:]:
            return lvl
    return s


def apply_filters(qs, args):
    if args.cat:
        wanted = {c.strip() for part in args.cat for c in part.split(",") if c.strip()}
        qs = [q for q in qs if q["分类"] in wanted]
    if args.level:
        wanted = {norm_level(x) for part in args.level for x in part.split(",")}
        qs = [q for q in qs if q["档位"] in wanted]
    if args.field:
        # 同 key 多值 → OR；不同 key → AND
        by_key = {}
        for kv in args.field:
            if "=" not in kv:
                sys.exit(f"--field 需写成 K=V，收到：{kv}")
            k, v = kv.split("=", 1)
            by_key.setdefault(k.strip(), set()).add(v.strip())
        qs = [q for q in qs if all(q["fm"].get(k) in vs for k, vs in by_key.items())]
    if args.due:
        qs = [q for q in qs if q["到期"]]
    if args.new:
        qs = [q for q in qs if q["未评测"]]
    if args.weak:
        qs = [q for q in qs if q["档位"] in WEAK]
    return qs


# ── 排序 ──────────────────────────────────────────────────────────────────
def freq_rank(q):
    f = q["fm"].get("频率", "")
    return {"高频": 0, "低频": 1}.get(f, 2)


def priority_key(q, rnd):
    """(tier, 到期日, 档位弱, 高频优先, 随机抖动)。"""
    if q["到期"]:
        tier, due_ord = 0, q["_nxt"].toordinal()
    elif q["未评测"]:
        tier, due_ord = 1, 0
    else:
        tier, due_ord = 2, 0
    lvl = LEVEL_RANK.get(q["档位"], 99)               # 未评测无档位 → 排后（但其 tier 已靠前）
    return (tier, due_ord, lvl, freq_rank(q), rnd.random())


def order(qs, args, rnd):
    if args.random:
        rnd.shuffle(qs)
        return qs
    return sorted(qs, key=lambda q: priority_key(q, rnd))


# ── 输出 ──────────────────────────────────────────────────────────────────
def status_tag(q):
    if q["未评测"]:
        return "🆕未评测"
    tag = q["档位"]
    if q["到期"]:
        tag += f"  ⏰到期 {q['下次复习']}"
    else:
        tag += f"  下次 {q['下次复习']}"
    return tag


def print_human(picked, bank, total_pool, args):
    filt = describe_filters(args)
    mode = "随机" if args.random else "优先级"
    print(f"\n📝 {bank} · 出题 {len(picked)} 题"
          f"（符合筛选 {total_pool} 题 | 排序: {mode} | 筛选: {filt}）\n")
    if not picked:
        print("（没有符合条件的题——放宽筛选，或换个题库/分类）\n")
        return
    for i, q in enumerate(picked, 1):
        freq = q["fm"].get("频率", "")
        head = f"{i}. {status_tag(q)}"
        if freq:
            head += f"  · {freq}"
        print(head)
        print(f"   {q['分类']} / {q['题目']}")
        print(f"   id {q['id']}   file {q['file']}")
        if q["备注"]:
            print(f"   上次备注  {q['备注']}")
        print()
    print("揭晓答案时读上面的 file 正文；评完把结果写回 "
          f"progress/{bank}.tsv 里对应 id 的行。\n")


def describe_filters(args):
    bits = []
    if args.cat:    bits.append("分类=" + ",".join(args.cat))
    if args.level:  bits.append("档位=" + ",".join(args.level))
    if args.field:  bits.append("/".join(args.field))
    if args.due:    bits.append("仅到期")
    if args.new:    bits.append("仅未评测")
    if args.weak:   bits.append("仅薄弱")
    return " ".join(bits) if bits else "全部"


def to_json(picked, bank):
    out = []
    for q in picked:
        item = {k: q[k] for k in
                ("id", "题目", "分类", "档位", "下次复习", "上次评测", "备注",
                 "未评测", "到期", "file")}
        item["题库"] = bank
        for k, v in q["fm"].items():                  # 带上可选字段（频率/难度…）
            if k not in ("题目", "分类", "id"):
                item.setdefault(k, v)
        out.append(item)
    return out


# ── main ──────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(
        description="快速出题：按掌握度优先级 + 多维筛选盖答案选题（不打印答案正文）。",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bank", nargs="?", help="题库名（缺省=唯一题库；多题库时必填）")
    ap.add_argument("-n", type=int, default=5, help="出题数（默认 5）")
    ap.add_argument("--cat", action="append", help="按分类筛，逗号分隔可多个；可重复")
    ap.add_argument("--field", action="append",
                    help="按 meta 可选字段筛，如 频率=高频；可重复")
    ap.add_argument("--level", action="append", help="按档位筛（名/emoji 均可），可逗号/重复")
    ap.add_argument("--due", action="store_true", help="只出今天到期复习的")
    ap.add_argument("--new", action="store_true", help="只出从未评测的")
    ap.add_argument("--weak", action="store_true", help="只出 🔴生疏/🟡夹生")
    ap.add_argument("--random", action="store_true", help="纯随机，无视优先级")
    ap.add_argument("--all", action="store_true", help="输出全部符合项，不按 -n 截断")
    ap.add_argument("--seed", type=int, help="随机种子（可复现）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    banks = list_banks()
    if not banks:
        sys.exit("banks/ 下还没有题库。")
    bank = args.bank or (banks[0] if len(banks) == 1 else None)
    if bank is None:
        sys.exit(f"有多个题库，请指定其一：{', '.join(banks)}")
    if bank not in banks:
        sys.exit(f"题库 `{bank}` 不存在。可选：{', '.join(banks)}")

    rnd = random.Random(args.seed)
    qs = apply_filters(load_questions(bank), args)
    total_pool = len(qs)
    ordered = order(qs, args, rnd)
    picked = ordered if args.all else ordered[:max(args.n, 0)]

    if args.json:
        print(json.dumps(to_json(picked, bank), ensure_ascii=False, indent=2))
    else:
        print_human(picked, bank, total_pool, args)


if __name__ == "__main__":
    main()
