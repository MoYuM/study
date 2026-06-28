#!/usr/bin/env python3
"""
题库规范检查（lint）—— 通用多题库版。

结构：
  banks/<题库名>/meta.yml            题库元信息（名称 / 分类清单 / 可选字段枚举）
  banks/<题库名>/<分类>/<题目>.md     纯内容：frontmatter(题目/分类/id + 声明的可选字段) + 答案正文
  progress/<题库名>/<id>.md          学习进度（Obsidian Bases 数据源）：每题一份，
                                     frontmatter 存 掌握/下次复习/上次评测/备注
  progress/<题库名>.base             Obsidian Bases 视图（YAML），不参与 lint

校验：题库 frontmatter 合规、分类/可选字段取值合法、id 唯一、**题库里不得混入进度字段**；
进度 md 的 id 必须在题库中存在且不重复、文件名与 id 一致、掌握档位合法、日期合法、评测态一致。
有错误 → 退出码 1（被 pre-commit 拦下）；只有警告 → 退出码 0。
"""
import os, re, sys, glob, datetime

SELF = os.path.dirname(os.path.abspath(__file__))
BANKS = os.path.join(SELF, "banks")
PROGRESS = os.path.join(SELF, "progress")

CORE = ["题目", "分类", "id"]
PROGRESS_FIELDS = {"掌握", "下次复习", "上次评测", "备注"}
SYSTEM_FIELDS = {"禁用"}  # 系统级字段，无需在 meta.yml 声明
LEVELS = {"🔴生疏", "🟡夹生", "🟢熟练", "⭐已掌握"}
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

errors, warnings = [], []
def err(m): errors.append(m)
def warn(m): warnings.append(m)
def rel(p): return os.path.relpath(p, SELF)


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        v = v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return v


def parse_meta(path):
    info = {"名称": "", "分类": set(), "字段": {}}
    for ln in open(path, encoding="utf-8"):
        ln = ln.strip()
        if not ln or ln.startswith("#") or ":" not in ln:
            continue
        k, v = ln.split(":", 1)
        k, v = k.strip(), v.strip()
        if k == "分类":
            info["分类"] = {x.strip() for x in v.split(",") if x.strip()}
        elif k.startswith("字段."):
            info["字段"][k[len("字段."):]] = {x.strip() for x in v.split(",") if x.strip()}
        elif k == "名称":
            info["名称"] = v
    return info


def parse_fm(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None
    close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if close is None:
        return None, None
    fm = {}
    for ln in lines[1:close]:
        if ":" in ln and ln.strip():
            k, v = ln.split(":", 1)
            fm[k.strip()] = unquote(re.sub(r"\s+#.*$", "", v))
    return fm, "\n".join(lines[close + 1:]).strip()


def valid_date(s):
    if not DATE_RE.match(s):
        return False
    try:
        datetime.date.fromisoformat(s); return True
    except ValueError:
        return False


def lint_bank(bankdir):
    name = os.path.basename(bankdir)
    meta_path = os.path.join(bankdir, "meta.yml")
    if not os.path.exists(meta_path):
        err(f"{rel(bankdir)}: 缺 meta.yml"); return name, {}
    meta = parse_meta(meta_path)
    if not meta["分类"]:
        err(f"{rel(meta_path)}: 未声明任何分类")
    allowed = set(CORE) | set(meta["字段"].keys())

    ids = {}
    for p in glob.glob(os.path.join(bankdir, "*", "*.md")):
        fm, body = parse_fm(open(p, encoding="utf-8").read())
        if fm is None:
            err(f"{rel(p)}: 缺/坏 frontmatter"); continue
        for k in CORE:
            if k not in fm:
                err(f"{rel(p)}: 缺字段 `{k}`")
        for k in fm:
            if k in PROGRESS_FIELDS:
                err(f"{rel(p)}: 题库里不得出现进度字段 `{k}`（应放 progress/{name}/<id>.md）")
            elif k not in allowed and k not in SYSTEM_FIELDS:
                warn(f"{rel(p)}: 未知字段 `{k}`（meta 未声明）")
        cat = fm.get("分类", "")
        if cat and cat not in meta["分类"]:
            err(f"{rel(p)}: 分类 `{cat}` 不在 meta 声明里")
        if cat and os.path.basename(os.path.dirname(p)) != cat:
            warn(f"{rel(p)}: 分类 `{cat}` 与所在目录不一致")
        for fname, enum in meta["字段"].items():
            val = fm.get(fname, "")
            if val and val not in enum:
                err(f"{rel(p)}: 字段 `{fname}={val}` 不在允许值 {sorted(enum)}")
        nid = fm.get("id", "")
        if not nid or not UUID_RE.match(nid):
            err(f"{rel(p)}: id `{nid}` 不是合法 uuid")
        elif nid in ids:
            err(f"{rel(p)}: id `{nid}` 与 {ids[nid]} 重复")
        else:
            ids[nid] = rel(p)
        if not fm.get("题目", "").strip():
            err(f"{rel(p)}: 题目为空")
        if not body or body == "*（无答案，待补）*":
            warn(f"{rel(p)}: 答案为空（待补）")
    return name, ids


def lint_progress_dir(progress_dir, bank_ids):
    """校验 progress/<题库>/*.md 进度文件（Obsidian Bases 数据源）。"""
    seen = set()
    for p in sorted(glob.glob(os.path.join(progress_dir, "*.md"))):
        fm, _ = parse_fm(open(p, encoding="utf-8").read())
        if fm is None:
            err(f"{rel(p)}: 缺/坏 frontmatter"); continue
        nid = fm.get("id", "")
        fname_id = os.path.splitext(os.path.basename(p))[0]
        if not nid or not UUID_RE.match(nid):
            err(f"{rel(p)}: id `{nid}` 不是合法 uuid"); continue
        if nid != fname_id:
            err(f"{rel(p)}: 文件名应为 <id>.md，与 id `{nid}` 不一致")
        if nid not in bank_ids:
            err(f"{rel(p)}: id `{nid}` 在题库中不存在（孤儿进度）")
        if nid in seen:
            err(f"{rel(p)}: id `{nid}` 在进度里重复")
        seen.add(nid)
        lvl = fm.get("掌握", "")
        if lvl not in LEVELS and lvl != "🆕未评测":
            err(f"{rel(p)}: 掌握 `{lvl}` 非法（应为 🆕未评测 或 {sorted(LEVELS)} 之一）")
        nxt, last = fm.get("下次复习", ""), fm.get("上次评测", "")
        for label, d in (("下次复习", nxt), ("上次评测", last)):
            if d and not valid_date(d):
                err(f"{rel(p)}: {label} `{d}` 不是合法 YYYY-MM-DD")
        # 评测态一致性：未评测不该带日期；已评测应有复习/评测日期
        if lvl == "🆕未评测":
            if nxt or last:
                warn(f"{rel(p)}: 🆕未评测 却带了 下次复习/上次评测 日期")
        elif lvl in LEVELS and not (nxt and last):
            warn(f"{rel(p)}: 已评测（{lvl}）但缺 下次复习/上次评测 日期")


def main():
    if not os.path.isdir(BANKS):
        print(f"❌ 找不到 banks/ 目录"); sys.exit(1)
    bank_dirs = [d for d in glob.glob(os.path.join(BANKS, "*")) if os.path.isdir(d)]
    total_q = 0
    known_progress = set()
    for bd in sorted(bank_dirs):
        name, ids = lint_bank(bd)
        total_q += len(ids)
        prog_dir = os.path.join(PROGRESS, name)
        if os.path.isdir(prog_dir):
            lint_progress_dir(prog_dir, ids)
            known_progress.add(name)
    # 孤儿进度目录（没有对应题库）
    if os.path.isdir(PROGRESS):
        for d in glob.glob(os.path.join(PROGRESS, "*")):
            if os.path.isdir(d) and os.path.basename(d) not in known_progress:
                warn(f"{rel(d)}: 没有同名题库")

    for w in warnings:
        print(f"⚠️  {w}")
    for e in errors:
        print(f"❌ {e}")
    print(f"\n{len(bank_dirs)} 个题库，共 {total_q} 题，{len(errors)} 错误，{len(warnings)} 警告。")
    if errors:
        print("提交被阻止：先修正上面的错误。"); sys.exit(1)
    print("✅ 题库规范检查通过。")


if __name__ == "__main__":
    main()
