#!/usr/bin/env python3
"""check_commit_conventions.py — 校验 Git 提交信息与分支命名是否符合项目约定。

纯标准库、零依赖、只读、确定性：不联网、不修改任何文件、同输入同输出。
规则来源：assets/commit-conventions.json（模板驱动脚本，读取时跳过 "_" 开头的注释键）。

用法:
  python3 scripts/check_commit_conventions.py --help
  python3 scripts/check_commit_conventions.py --check-rules            # 自检规则文件（必须 0 错误）
  python3 scripts/check_commit_conventions.py --commits-file commits.txt
  git log --pretty=%s main..HEAD | python3 scripts/check_commit_conventions.py --stdin
  python3 scripts/check_commit_conventions.py --branch feature/login-page

退出码: 0 = 全部合规 / 1 = 发现违规或参数错误 / 2 = 规则文件无法解析。
"""
import argparse
import json
import os
import re
import sys

DEFAULT_RULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "commit-conventions.json")

SUBJECT_RE = re.compile(r"^(?P<type>[a-z]+)(?P<scope>\([^)]*\))?(?P<breaking>!)?:\s?(?P<desc>.+)$")


def load_rules(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        print(f"[ERROR] 规则文件无法解析: {path} -> {exc}", file=sys.stderr)
        sys.exit(2)
    return data


def visible(data):
    """去掉 '_' 开头的注释/元信息键，避免被当成规则。"""
    return {k: v for k, v in data.items() if not k.startswith("_")}


def check_rules_schema(rules, path):
    """校验规则文件自身结构是否合法（0 错误才算通过）。返回 (errors,)。"""
    errors = []
    if not isinstance(rules.get("commit_types"), list) or not rules["commit_types"]:
        errors.append("commit_types 必须是非空列表")
    else:
        for t in rules["commit_types"]:
            if not isinstance(t, str) or not re.match(r"^[a-z]+$", t):
                errors.append(f"commit_types 含非法元素: {t!r}")
    br = rules.get("branch_regex")
    if not isinstance(br, str) or not br:
        errors.append("branch_regex 缺失或非字符串")
    else:
        try:
            re.compile(br)
        except re.error as exc:
            errors.append(f"branch_regex 不是合法正则: {exc}")
    for key in ("subject_max_len", "subject_min_len"):
        v = rules.get(key)
        if not isinstance(v, int) or v <= 0:
            errors.append(f"{key} 必须是正整数")
    if errors:
        print(f"[FAIL] 规则文件结构校验未通过: {path}", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"[OK] 规则文件结构合法: {path}（commit_types={len(rules['commit_types'])}, branch_regex 已编译）", file=sys.stderr)
    return 0


def lint_commit(subject, rules, idx):
    errors = []
    types = set(rules.get("commit_types", []))
    max_len = rules.get("subject_max_len", 72)
    min_len = rules.get("subject_min_len", 4)
    scope_pattern = rules.get("scope_pattern")
    breaking_allowed = rules.get("breaking_allowed", True)

    m = SUBJECT_RE.match(subject)
    if not m:
        errors.append("不符合 Conventional Commits 格式: 应为 'type(scope)!: description'")
        return errors
    ctype = m.group("type")
    if ctype not in types:
        errors.append(f"未知提交类型 '{ctype}'，允许: {', '.join(sorted(types))}")
    scope = m.group("scope")
    if scope:
        inner = scope[1:-1]
        if scope_pattern and not re.match(scope_pattern, inner):
            errors.append(f"scope '{inner}' 不符合 scope_pattern")
    if not breaking_allowed and m.group("breaking"):
        errors.append("本仓库禁止在提交中使用 '!' (breaking) 标记")
    desc = m.group("desc")
    if len(desc) < min_len:
        errors.append(f"描述过短（<{min_len} 字符）")
    if len(subject) > max_len:
        errors.append(f"主题行超长（{len(subject)}>{max_len}）")
    return errors


def lint_branch(name, rules):
    errors = []
    br = rules.get("branch_regex", "")
    forbidden = rules.get("branch_forbidden_chars")
    try:
        ok = bool(re.match(br, name))
    except re.error:
        ok = False
    if not ok:
        errors.append(f"分支名 '{name}' 不匹配 branch_regex: {br}")
    if forbidden and re.search(forbidden, name):
        errors.append(f"分支名含禁止字符（匹配 {forbidden}）")
    return errors


def main():
    ap = argparse.ArgumentParser(description="校验 Git 提交信息与分支命名的项目约定（只读、确定性）")
    ap.add_argument("--rules", default=DEFAULT_RULES, help="规则文件路径（默认 assets/commit-conventions.json）")
    ap.add_argument("--check-rules", action="store_true", help="仅自检规则文件结构，必须 0 错误")
    ap.add_argument("--commits-file", help="逐行存放提交主题的文件路径")
    ap.add_argument("--branch", help="待校验的分支名")
    ap.add_argument("--stdin", action="store_true", help="从标准输入逐行读取提交主题")
    args = ap.parse_args()

    rules = visible(load_rules(args.rules))

    if args.check_rules:
        return check_rules_schema(rules, args.rules)

    violations = 0
    if args.commits_file:
        with open(args.commits_file, encoding="utf-8") as fh:
            lines = [ln.rstrip("\n") for ln in fh if ln.strip()]
        for i, subj in enumerate(lines, 1):
            errs = lint_commit(subj, rules, i)
            for e in errs:
                print(f"[commit #{i}] {subj!r}: {e}", file=sys.stderr)
                violations += 1
    if args.stdin:
        for i, raw in enumerate(sys.stdin, 1):
            subj = raw.rstrip("\n")
            if not subj.strip():
                continue
            for e in lint_commit(subj, rules, i):
                print(f"[stdin #{i}] {subj!r}: {e}", file=sys.stderr)
                violations += 1
    if args.branch is not None:
        for e in lint_branch(args.branch, rules):
            print(f"[branch] {e}", file=sys.stderr)
            violations += 1

    if not (args.commits_file or args.stdin or args.branch is not None):
        ap.error("需指定 --commits-file / --stdin / --branch 之一（或用 --check-rules 自检）")

    if violations:
        print(f"\n[FAIL] 发现 {violations} 处违规", file=sys.stderr)
        return 1
    print("[OK] 全部提交/分支命名合规", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
