#!/usr/bin/env python3
"""check_project_template.py — 按项目模板清单核查目录结构、README 章节与残留 TODO。

纯标准库、零依赖、只读、确定性：不联网、不修改任何文件、同输入同输出。
规则来源：assets/project-template-manifest.json（模板驱动脚本，读取时跳过 "_" 开头的注释键）。

用法:
  python3 scripts/check_project_template.py --help
  python3 scripts/check_project_template.py --check-rules            # 自检清单文件（必须 0 错误）
  python3 scripts/check_project_template.py --target ./my-project    # 核查某个项目目录
  python3 scripts/check_project_template.py                          # 默认核查当前目录

退出码: 0 = 全部合规 / 1 = 发现缺失或残留 / 2 = 清单文件无法解析。
"""
import argparse
import json
import os
import re
import sys

DEFAULT_MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "project-template-manifest.json")


def load_manifest(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        print(f"[ERROR] 清单文件无法解析: {path} -> {exc}", file=sys.stderr)
        sys.exit(2)
    return data


def visible(data):
    return {k: v for k, v in data.items() if not k.startswith("_")}


def check_manifest_schema(manifest, path):
    errors = []
    if not isinstance(manifest.get("required_files"), list):
        errors.append("required_files 必须是列表")
    if not isinstance(manifest.get("readme_required_sections"), list):
        errors.append("readme_required_sections 必须是列表")
    if not isinstance(manifest.get("missing_tokens"), list) or not manifest["missing_tokens"]:
        errors.append("missing_tokens 必须是非空列表")
    if not isinstance(manifest.get("ignore_paths"), list):
        errors.append("ignore_paths 必须是列表")
    if not isinstance(manifest.get("text_extensions"), list) or not manifest["text_extensions"]:
        errors.append("text_extensions 必须是非空列表")
    if errors:
        print(f"[FAIL] 清单文件结构校验未通过: {path}", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"[OK] 清单文件结构合法: {path}（required_files={len(manifest['required_files'])}, missing_tokens={manifest['missing_tokens']}）", file=sys.stderr)
    return 0


def scan_text_files(target, manifest):
    ignore = set(manifest.get("ignore_paths", []))
    exts = set(manifest.get("text_extensions", []))
    found = []
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in ignore and not d.startswith(".")]
        for fn in files:
            if any(fn.endswith(e) for e in exts):
                found.append(os.path.join(root, fn))
    return found


def main():
    ap = argparse.ArgumentParser(description="按项目模板清单核查目录/README/残留 TODO（只读、确定性）")
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST, help="清单文件路径（默认 assets/project-template-manifest.json）")
    ap.add_argument("--target", default=".", help="待核查的项目目录（默认当前目录）")
    ap.add_argument("--check-rules", action="store_true", help="仅自检清单文件结构，必须 0 错误")
    args = ap.parse_args()

    manifest = visible(load_manifest(args.manifest))

    if args.check_rules:
        return check_manifest_schema(manifest, args.manifest)

    if not os.path.isdir(args.target):
        print(f"[ERROR] 目标目录不存在: {args.target}", file=sys.stderr)
        return 2

    problems = 0

    # 1) 必需文件/目录
    for rel in manifest.get("required_files", []):
        p = os.path.join(args.target, rel)
        if not (os.path.isfile(p) or os.path.isdir(p)):
            print(f"[缺失] 必需项不存在: {rel}", file=sys.stderr)
            problems += 1

    # 2) README 必需章节
    readme = os.path.join(args.target, "README.md")
    if os.path.isfile(readme):
        with open(readme, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for sec in manifest.get("readme_required_sections", []):
            if sec not in text:
                print(f"[缺失] README 缺少章节: {sec!r}", file=sys.stderr)
                problems += 1
        for pat in manifest.get("readme_forbidden_patterns", []):
            if pat.lower() in text.lower():
                print(f"[禁止] README 含禁止内容: {pat!r}", file=sys.stderr)
                problems += 1
    else:
        print("[缺失] README.md 不存在，无法核查章节", file=sys.stderr)
        problems += 1

    # 3) 残留 token 扫描
    tokens = manifest.get("missing_tokens", [])
    if tokens:
        token_re = re.compile("|".join(re.escape(t) for t in tokens))
        for fp in scan_text_files(args.target, manifest):
            if os.path.abspath(fp) == os.path.abspath(args.manifest):
                continue
            try:
                with open(fp, encoding="utf-8", errors="replace") as fh:
                    for ln, line in enumerate(fh, 1):
                        if token_re.search(line):
                            hits = [t for t in tokens if t in line]
                            print(f"[残留] {os.path.relpath(fp, args.target)}:{ln} -> {', '.join(hits)}", file=sys.stderr)
                            problems += 1
            except OSError:
                continue

    if problems:
        print(f"\n[FAIL] 发现 {problems} 处问题", file=sys.stderr)
        return 1
    print(f"[OK] 项目模板清单全部通过: {args.target}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
