#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简推送/发布脚本 — 开发/发布分离

参数式用法(熟练开发者/AI):
  python push.py                     # 提交 + 推 dev(默认不 refresh)
  python push.py -m "说明"            # 带提交说明
  python push.py --refresh           # refresh + 提交 + 推 dev
  python push.py --merge             # 合并 dev→main 并推送(发布,不打 tag)
  python push.py --tag 1.1.0         # 打 tag(不合并)
  python push.py --release           # 一站式发布:合并 dev→main
  python push.py --release --version 1.1.0   # 发布 + 打 tag

流程:
  开发:改代码 → python push.py(推 dev,玩家不可见,不刷新索引)
  发布:验证 OK → python push.py --release --version 1.1.0
"""

import argparse
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKWIZ = os.path.join(ROOT, "tools", "packwiz-cli", "packwiz.exe")


def run(cmd, cwd=ROOT, check=True):
    print(f"> {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=cwd)
    if check and r.returncode != 0:
        print(f"[错误] 命令失败: {' '.join(cmd)}")
        sys.exit(1)
    return r


def git(cmd, cwd=ROOT, check=True):
    # errors="replace" 避免中文文件名导致 GBK 解码崩溃
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, errors="replace", encoding="utf-8")
    if check and r.returncode != 0:
        print(f"[错误] git {' '.join(cmd)}: {r.stderr.strip()}")
        sys.exit(1)
    return r


def do_refresh():
    """packwiz refresh"""
    if os.path.exists(PACKWIZ):
        run([PACKWIZ, "refresh"])
    else:
        run(["packwiz", "refresh"])


def has_conflict_markers():
    """阻止提交 Git 冲突标记,尤其是 index.toml/pack.toml。"""
    markers = ("<<<<<<<", "=======", ">>>>>>>")
    candidates = []
    for name in ["pack.toml", "index.toml"]:
        path = os.path.join(ROOT, name)
        if os.path.exists(path):
            candidates.append(path)

    found = []
    for path in candidates:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for lineno, line in enumerate(fh, 1):
                if line.startswith(markers):
                    found.append(f"{os.path.relpath(path, ROOT)}:{lineno}: {line.strip()}")
    if found:
        print("[错误] 检测到 Git 冲突标记,请先解决后再继续:")
        for item in found[:20]:
            print(f"  - {item}")
        return True
    return False


def verify_index_consistency():
    """验证 index.toml 记录的 hash 与磁盘文件一致。
    防止 refresh 与 git 提交之间存在 CRLF/LF 或缓存差异导致 hash 不同步。"""
    import hashlib
    import re

    idx = open(os.path.join(ROOT, "index.toml"), encoding="utf-8").read()
    entries = re.findall(r'file = "([^"]+)"\n(?:hash-format = "[^"]+"\n)?hash = "([0-9a-f]+)"', idx)
    mismatch = []
    for fname, hashval in entries:
        path = os.path.join(ROOT, fname)
        if not os.path.exists(path):
            continue  # metafile 可能不存在(如 jar 只存元数据)
        actual = hashlib.sha256(open(path, "rb").read()).hexdigest()
        if actual != hashval:
            mismatch.append(fname)
    if mismatch:
        print(f"[警告] {len(mismatch)} 个文件 hash 与 index 不一致:")
        for m in mismatch[:10]:
            print(f"  - {m}")
        print("建议重新 packwiz refresh 后提交")
        return False
    return True


def do_commit(message):
    """提交当前改动。无改动则跳过。"""
    r = git(["git", "status", "--porcelain"], check=False)
    if r.stdout.strip():
        if not message:
            message = "update: 开发更新"
        git(["git", "add", "-A"])
        git(["git", "commit", "-m", message])
        print(f"[*] 已提交: {message}")
        return True
    else:
        print("[*] 无改动,跳过提交")
        return False


def do_push_dev():
    """推 dev。"""
    git(["git", "push", "origin", "dev"])
    print("[✓] 已推送到 dev(玩家不可见,发布需 --merge 或 --release)")


def do_merge():
    """合并 dev→main 并推送。"""
    # 确认当前在 dev,发布基于 dev
    cur = git(["git", "branch", "--show-current"]).stdout.strip()
    if cur != "dev":
        print(f"[错误] 当前在 {cur} 分支,发布需在 dev 分支执行")
        print("  请先: git checkout dev")
        sys.exit(1)
    git(["git", "checkout", "main"])
    git(["git", "pull", "origin", "main"])
    git(["git", "merge", "dev", "--no-edit"])
    git(["git", "push", "origin", "main"])
    print("[✓] 已发布到 main,玩家将增量更新(1~3 分钟)")
    git(["git", "checkout", "dev"])  # 回到 dev


def do_tag(version):
    """打 tag(不合并)。"""
    tag = f"v{version}"
    r = git(["git", "tag", tag], check=False)
    if r.returncode != 0:
        print(f"[错误] 打 tag 失败(可能已存在): {r.stderr.strip()}")
        return
    git(["git", "push", "origin", tag])
    print(f"[✓] 已打 tag {tag}")


def main():
    ap = argparse.ArgumentParser(description="极简推送/发布(开发/发布分离)")
    ap.add_argument("-m", "--message", default=None, help="提交说明")
    ap.add_argument("--refresh", action="store_true", help="开发推送前也执行 packwiz refresh")
    ap.add_argument("--merge", action="store_true", help="合并 dev→main 并推送(发布)")
    ap.add_argument("--tag", default=None, metavar="VER", help="打 tag(如 1.1.0),不合并")
    ap.add_argument("--release", action="store_true", help="一站式发布:合并 dev→main")
    ap.add_argument("--version", default=None, help="配合 --release 打 tag")
    args = ap.parse_args()

    # 模式互斥校验
    if sum([args.merge, args.release, bool(args.tag)]) > 1:
        print("[错误] --merge / --release / --tag 只能选一个")
        sys.exit(1)

    if has_conflict_markers():
        sys.exit(1)

    # 开发推送默认不 refresh,避免多人协作时 index.toml/pack.toml 频繁冲突。
    # 发布/合并必须 refresh,因为 main 是玩家实际拉取的索引源。
    should_refresh = args.refresh or args.release or args.merge
    if should_refresh:
        do_refresh()
        if has_conflict_markers():
            sys.exit(1)
    else:
        print("[*] 跳过 packwiz refresh(开发推送默认行为;发布时会自动 refresh)")

    # 2. 校验 index 一致性(发布前必须)
    if args.release or args.merge:
        if not verify_index_consistency():
            print("[错误] index 与磁盘文件不一致,请先修复(重新 refresh 并提交)")
            sys.exit(1)

    do_commit(args.message)

    # 3. 分支操作
    if args.release or args.merge:
        do_merge()
        if args.release and args.version:
            do_tag(args.version)
    elif args.tag:
        do_tag(args.tag)
    else:
        do_push_dev()


if __name__ == "__main__":
    main()
