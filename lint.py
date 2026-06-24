#!/usr/bin/env python3
"""
题库 Markdown 规范检查（lint）。

校验 题库/ 下每道题 md 的 YAML frontmatter 是否合规：
字段齐全、分类/频率/掌握取值合法、日期格式、id 唯一、评测态与日期一致、答案非空。
有错误 → 退出码 1（被 pre-commit hook 拦下提交）；只有警告 → 退出码 0。

用法：python3 lint.py
"""
import os, re, sys, datetime

SELF = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(SELF, "题库")

CATS = {"Vue", "AI", "CSS", "算法", "代码题", "HTTP", "浏览器", "React", "JS", "前端工程", "安全"}
FREQS = {"高频", "低频", ""}
LEVELS = {"🔴生疏", "🟡夹生", "🟢熟练", "⭐已掌握", ""}
REQUIRED = ["题目", "分类", "频率", "掌握", "下次复习", "上次评测", "id", "备注"]
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

errors, warnings = [], []


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        v = v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return v


def parse_frontmatter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None
    close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if close is None:
        return None, None
    fm = {}
    for ln in lines[1:close]:
        if not ln.strip():
            continue
        if ":" not in ln:
            continue
        k, v = ln.split(":", 1)
        # 去掉行内注释（# 前需空格）
        v = re.sub(r"\s+#.*$", "", v)
        fm[k.strip()] = unquote(v)
    body = "\n".join(lines[close + 1:]).strip()
    return fm, body


def valid_date(s):
    if not DATE_RE.match(s):
        return False
    try:
        datetime.date.fromisoformat(s)
        return True
    except ValueError:
        return False


def lint_file(path):
    rel = os.path.relpath(path, SELF)
    text = open(path, encoding="utf-8").read()
    fm, body = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{rel}: 缺少 YAML frontmatter（首行须是 --- 且有闭合 ---）")
        return None

    for k in REQUIRED:
        if k not in fm:
            errors.append(f"{rel}: frontmatter 缺字段 `{k}`")

    cat = fm.get("分类", "")
    if cat and cat not in CATS:
        errors.append(f"{rel}: 分类 `{cat}` 不在允许集 {sorted(CATS)}")
    # 分类应与父目录名一致（警告）
    parent = os.path.basename(os.path.dirname(path))
    if cat and parent != cat:
        warnings.append(f"{rel}: 分类 `{cat}` 与所在目录 `{parent}` 不一致")

    if fm.get("频率", "") not in FREQS:
        errors.append(f"{rel}: 频率 `{fm.get('频率')}` 非法（须 高频/低频/空）")

    lvl = fm.get("掌握", "")
    if lvl not in LEVELS:
        errors.append(f"{rel}: 掌握 `{lvl}` 非法（须 🔴生疏/🟡夹生/🟢熟练/⭐已掌握/空）")

    nxt, last = fm.get("下次复习", ""), fm.get("上次评测", "")
    for label, d in (("下次复习", nxt), ("上次评测", last)):
        if d and not valid_date(d):
            errors.append(f"{rel}: {label} `{d}` 不是合法 YYYY-MM-DD")

    # 评测态一致性：评过分必有两个日期；没评过必两空
    scored = lvl != ""
    has_dates = bool(nxt) and bool(last)
    if scored and not has_dates:
        errors.append(f"{rel}: 已有掌握档位 `{lvl}` 但缺 下次复习/上次评测 日期")
    if not scored and (nxt or last):
        errors.append(f"{rel}: 未评测（掌握为空）但填了复习/评测日期")

    if not fm.get("题目", "").strip():
        errors.append(f"{rel}: 题目为空")

    if not body or body == "*（无答案，待补）*":
        warnings.append(f"{rel}: 答案为空（待补）")

    return fm.get("id", "")


def main():
    if not os.path.isdir(BANK):
        print(f"❌ 找不到题库目录：{BANK}")
        sys.exit(1)

    files = []
    for d, _, fs in os.walk(BANK):
        for f in fs:
            if f.endswith(".md"):
                files.append(os.path.join(d, f))

    ids = {}
    for p in sorted(files):
        nid = lint_file(p)
        if nid:
            if nid in ids:
                errors.append(f"{os.path.relpath(p, SELF)}: id `{nid}` 与 {ids[nid]} 重复")
            elif not UUID_RE.match(nid):
                errors.append(f"{os.path.relpath(p, SELF)}: id `{nid}` 不是合法 uuid")
            else:
                ids[nid] = os.path.relpath(p, SELF)

    for w in warnings:
        print(f"⚠️  {w}")
    for e in errors:
        print(f"❌ {e}")

    print(f"\n共 {len(files)} 题，{len(errors)} 错误，{len(warnings)} 警告。")
    if errors:
        print("提交被阻止：先修正上面的错误。")
        sys.exit(1)
    print("✅ 题库规范检查通过。")


if __name__ == "__main__":
    main()
