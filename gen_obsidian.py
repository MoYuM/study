#!/usr/bin/env python3
"""
把 banks/ 题库内容与 progress/<题库>/ 现有进度合并，确保每道题在
progress/<题库>/<id>.md 中都有一个条目（供 Obsidian Bases 查询）。

主要用途：新增题目后执行一次，为新题创建 🆕未评测 的进度文件。
已有进度的题目会保留原有 frontmatter 数据，不会覆盖。

同时确保 progress/<题库>.base（Obsidian Bases 视图）存在：缺失则按模板生成，
已存在则保留不覆盖（你可自由改视图）。

用法：
  python3 gen_obsidian.py [题库名]   # 不传则同步所有题库
"""
import os, sys, glob

SELF     = os.path.dirname(os.path.abspath(__file__))
BANKS    = os.path.join(SELF, "banks")
OUT      = os.path.join(SELF, "progress")


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        v = v[1:-1].replace('\\"', '"')
    return v


def parse_fm(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = unquote(v)
    return fm


def load_progress(progress_dir):
    """返回已有进度 {id: frontmatter_dict}，读 progress/<bank>/*.md。"""
    progress = {}
    if not os.path.isdir(progress_dir):
        return progress
    for p in glob.glob(os.path.join(progress_dir, "*.md")):
        fm = parse_fm(open(p, encoding="utf-8").read())
        if fm.get("id"):
            progress[fm["id"]] = fm
    return progress


def yaml_str(v):
    """输出安全的 YAML 字符串，含特殊字符则加引号。"""
    if not v:
        return '""'
    need_quote = any(c in v for c in ':{}[]|>&*!,#?-"\'\\%@`\n\r')
    if need_quote:
        return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return v


# progress/<题库>.base 的视图模板（仅在缺失时生成，不覆盖用户改动）。
BASE_TEMPLATE = '''filters:
  and:
    - file.inFolder("progress/{bank}")
formulas:
  days_until: 'if(下次复习, (date(下次复习) - today()).days, "")'
  due_flag: 'if(下次复习, if((date(下次复习) - today()).days <= 0, "⏰到期", ""), if(掌握 == "🆕未评测", "🆕", ""))'
properties:
  题目:
    displayName: 题目
  分类:
    displayName: 分类
  频率:
    displayName: 频率
  掌握:
    displayName: 掌握
  下次复习:
    displayName: 下次复习
  上次评测:
    displayName: 上次评测
  备注:
    displayName: 备注
  题库来源:
    displayName: 题库来源
  formula.days_until:
    displayName: 距复习(天)
  formula.due_flag:
    displayName: 状态
views:
  - type: table
    name: 全部题目
    order:
      - formula.due_flag
      - 题目
      - 分类
      - 频率
      - 掌握
      - 下次复习
      - formula.days_until
      - 题库来源
  - type: table
    name: 待复习（今天到期）
    filters:
      and:
        - formula.due_flag == "⏰到期"
    order:
      - 题目
      - 分类
      - 掌握
      - 下次复习
      - 备注
  - type: table
    name: 未评测
    filters:
      and:
        - 掌握 == "🆕未评测"
    order:
      - 题目
      - 分类
      - 频率
  - type: table
    name: 薄弱题（🔴🟡）
    filters:
      or:
        - 掌握 == "🔴生疏"
        - 掌握 == "🟡夹生"
    groupBy:
      property: 掌握
      direction: ASC
    order:
      - 题目
      - 分类
      - 掌握
      - 下次复习
      - 备注
  - type: table
    name: 已掌握（🟢⭐）
    filters:
      or:
        - 掌握 == "🟢熟练"
        - 掌握 == "⭐已掌握"
    order:
      - 题目
      - 分类
      - 掌握
      - 上次评测
      - 备注
'''


def ensure_base(bank_name):
    """确保 progress/<bank>.base 视图存在；缺失则按模板生成，已存在不覆盖。"""
    base_path = os.path.join(OUT, f"{bank_name}.base")
    if os.path.exists(base_path):
        return ".base 已存在"
    open(base_path, "w", encoding="utf-8").write(BASE_TEMPLATE.format(bank=bank_name))
    return ".base 已生成"


def sync_bank(bank_name):
    bank_dir = os.path.join(BANKS, bank_name)
    out_dir  = os.path.join(OUT, bank_name)
    os.makedirs(out_dir, exist_ok=True)

    progress = load_progress(out_dir)
    md_files = glob.glob(os.path.join(bank_dir, "**", "*.md"), recursive=True)

    seen_ids = set()
    for md_path in md_files:
        text = open(md_path, encoding="utf-8").read()
        fm = parse_fm(text)
        if not fm.get("id"):
            continue

        qid = fm["id"]
        seen_ids.add(qid)
        p = progress.get(qid, {})

        掌握 = p.get("掌握", "🆕未评测")
        下次复习 = p.get("下次复习", "")
        上次评测 = p.get("上次评测", "")
        备注 = p.get("备注", "")

        bank_link = f"[[{md_path.replace(SELF + os.sep, '')}]]"
        lines = [
            "---",
            f"题目: {yaml_str(fm.get('题目', ''))}",
            f"分类: {yaml_str(fm.get('分类', ''))}",
            f"频率: {yaml_str(fm.get('频率', ''))}",
            f"id: {qid}",
            f"题库来源: {yaml_str(bank_link)}",
            f"掌握: {yaml_str(掌握)}",
        ]
        if 下次复习:
            lines.append(f"下次复习: {下次复习}")
        if 上次评测:
            lines.append(f"上次评测: {上次评测}")
        if 备注:
            lines.append(f"备注: {yaml_str(备注)}")
        lines.append("---")
        lines.append("")

        out_path = os.path.join(out_dir, f"{qid}.md")
        open(out_path, "w", encoding="utf-8").write("\n".join(lines))

    # 删除题库里已不存在的孤立文件
    for f in glob.glob(os.path.join(out_dir, "*.md")):
        fid = os.path.splitext(os.path.basename(f))[0]
        if fid not in seen_ids:
            os.remove(f)
            print(f"  删除孤立文件: {fid}.md")

    base_state = ensure_base(bank_name)
    print(f"✅ {bank_name}: 同步 {len(seen_ids)} 题（已评测 {len(progress)}）· {base_state}")


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    banks = ([target] if target else
             [d for d in os.listdir(BANKS) if os.path.isdir(os.path.join(BANKS, d))])
    for b in banks:
        sync_bank(b)


if __name__ == "__main__":
    main()
