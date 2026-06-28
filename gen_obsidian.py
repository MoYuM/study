#!/usr/bin/env python3
"""
把 banks/ 题库内容 + progress/ 学习进度合并，
生成 obsidian-db/<题库名>/<id>.md，供 Obsidian Bases 查询。

用法：
  python3 gen_obsidian.py [题库名]   # 不传则同步所有题库
"""
import os, sys, csv, glob, re

SELF = os.path.dirname(os.path.abspath(__file__))
BANKS = os.path.join(SELF, "banks")
PROGRESS = os.path.join(SELF, "progress")
OUT = os.path.join(SELF, "obsidian-db")


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


def load_progress(tsv_path):
    progress = {}
    if not os.path.exists(tsv_path):
        return progress
    with open(tsv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            progress[row["id"]] = row
    return progress


def yaml_str(v):
    """输出安全的 YAML 字符串，含特殊字符则加引号。"""
    if not v:
        return '""'
    need_quote = any(c in v for c in ':{}[]|>&*!,#?-"\'\\%@`\n\r')
    if need_quote:
        return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'
    return v


def sync_bank(bank_name):
    bank_dir = os.path.join(BANKS, bank_name)
    tsv_path = os.path.join(PROGRESS, f"{bank_name}.tsv")
    out_dir = os.path.join(OUT, bank_name)
    os.makedirs(out_dir, exist_ok=True)

    progress = load_progress(tsv_path)
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

        lines = [
            "---",
            f"题目: {yaml_str(fm.get('题目', ''))}",
            f"分类: {yaml_str(fm.get('分类', ''))}",
            f"频率: {yaml_str(fm.get('频率', ''))}",
            f"id: {qid}",
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
        lines.append(f"题库来源: [[{md_path.replace(SELF + os.sep, '')}]]")

        out_path = os.path.join(out_dir, f"{qid}.md")
        open(out_path, "w", encoding="utf-8").write("\n".join(lines))

    # 删除题库里已不存在的孤立文件
    for f in glob.glob(os.path.join(out_dir, "*.md")):
        fid = os.path.splitext(os.path.basename(f))[0]
        if fid not in seen_ids:
            os.remove(f)
            print(f"  删除孤立文件: {fid}.md")

    print(f"✅ {bank_name}: 同步 {len(seen_ids)} 题（已评测 {len(progress)}）")


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    banks = ([target] if target else
             [d for d in os.listdir(BANKS) if os.path.isdir(os.path.join(BANKS, d))])
    for b in banks:
        sync_bank(b)


if __name__ == "__main__":
    main()
