#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简推送/发布脚本 — 开发/发布分离

参数式用法(熟练开发者/AI):
  python push.py                     # 提交 + 推 dev(不 refresh)
  python push.py -m "说明"            # 带提交说明
  python push.py --refresh           # 兼容旧参数:开发分支仍不会 refresh
  python push.py --merge             # 发布:dev→main,main refresh,再 --no-ff 回灌 dev
  python push.py --tag 1.1.0         # 在当前提交打 tag(不合并)
  python push.py --release           # 一站式发布:dev→main + main refresh + 回灌 dev
  python push.py --release --version 1.1.0   # 发布 + 打 tag

流程:
  开发:改代码 → python push.py(推 dev,玩家不可见,不刷新索引)
  发布:验证 OK → python push.py --release --version 1.1.0

发布策略:
  - 只允许从 dev 发布到 main。
  - dev 分支日常提交一律不执行 packwiz refresh。
  - 发布前用 --ff-only 同步远端,本地落后时快进,本地/远端分叉时停止。
  - dev→main 使用 --no-ff,即使可快进也保留明确的发布合并点。
  - packwiz refresh 只在 main 上执行,并单独提交索引更新。
  - tag 打在 main 的发布索引提交上。
  - main 发布完成后用 --no-ff 合并回 dev,显式带回 index.toml / pack.toml。
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


def current_branch():
    return git(["git", "branch", "--show-current"]).stdout.strip()


def ensure_clean_worktree():
    r = git(["git", "status", "--porcelain"], check=False)
    if r.stdout.strip():
        print("[错误] 工作区仍有未提交改动,无法切换/合并分支:")
        for line in r.stdout.splitlines()[:30]:
            print(f"  {line}")
        sys.exit(1)


def checkout(branch):
    if current_branch() != branch:
        git(["git", "checkout", branch])


def fetch_origin():
    git(["git", "fetch", "origin", "--prune"])


def pull_ff_only(branch):
    checkout(branch)
    git(["git", "pull", "--ff-only", "origin", branch])


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


def commit_all_if_changed(message):
    """提交当前分支上的所有改动。无改动则跳过。"""
    r = git(["git", "status", "--porcelain"], check=False)
    if not r.stdout.strip():
        print("[*] 无改动,跳过提交")
        return False
    git(["git", "add", "-A"])
    git(["git", "commit", "-m", message])
    print(f"[*] 已提交: {message}")
    return True


def do_push_dev():
    """推 dev。"""
    git(["git", "push", "origin", "dev"])
    print("[✓] 已推送到 dev(玩家不可见,发布需 --merge 或 --release)")


def do_merge(version=None):
    """发布 dev→main,在 main 上刷新索引,再显式回灌到 dev。"""
    cur = current_branch()
    if cur != "dev":
        print(f"[错误] 当前在 {cur} 分支,发布需在 dev 分支执行")
        print("  请先: git checkout dev")
        sys.exit(1)

    ensure_clean_worktree()
    fetch_origin()

    # 发布前只接受快进同步。若 dev/main 与远端已分叉,交给维护人手动解决。
    pull_ff_only("dev")
    git(["git", "push", "origin", "dev"])

    pull_ff_only("main")

    git(["git", "merge", "--no-ff", "--no-edit", "dev"])
    do_refresh()
    if has_conflict_markers():
        sys.exit(1)
    if not verify_index_consistency():
        print("[错误] index 与磁盘文件不一致,请先修复")
        sys.exit(1)
    commit_all_if_changed("release: refresh packwiz index")

    tag = None
    if version:
        tag = f"v{version}"
        r = git(["git", "tag", tag], check=False)
        if r.returncode != 0:
            print(f"[错误] 打 tag 失败(可能已存在): {r.stderr.strip()}")
            sys.exit(1)

    git(["git", "push", "origin", "main"])
    if tag:
        git(["git", "push", "origin", tag])
        print(f"[✓] 已打 tag {tag}")
    print("[✓] 已发布到 main,玩家将增量更新(1~3 分钟)")

    # 用显式合并提交把 main 上的索引发布结果带回 dev,保留 dev 的开发线叙事。
    checkout("dev")
    git(["git", "merge", "--no-ff", "--no-edit", "main"])
    git(["git", "push", "origin", "dev"])
    print("[✓] 已将 main 的发布索引通过 --no-ff 合并回 dev")


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
    ap.add_argument("--refresh", action="store_true", help="兼容旧参数:dev 仍不会 refresh")
    ap.add_argument("--merge", action="store_true", help="发布到 main,main refresh,再 --no-ff 回灌 dev")
    ap.add_argument("--tag", default=None, metavar="VER", help="打 tag(如 1.1.0),不合并")
    ap.add_argument("--release", action="store_true", help="一站式发布:main refresh + 可选 tag + 回灌 dev")
    ap.add_argument("--version", default=None, help="配合 --release 打 tag")
    args = ap.parse_args()

    # 模式互斥校验
    if sum([args.merge, args.release, bool(args.tag)]) > 1:
        print("[错误] --merge / --release / --tag 只能选一个")
        sys.exit(1)
    if args.version and not args.release:
        print("[错误] --version 只能配合 --release 使用")
        sys.exit(1)

    if has_conflict_markers():
        sys.exit(1)

    if args.release or args.merge:
        print("[*] dev 阶段不执行 packwiz refresh;发布合并后会在 main 上刷新")
    elif args.refresh:
        print("[*] 已忽略 --refresh: dev 分支提交不执行 packwiz refresh;发布时会在 main 上刷新")
    else:
        print("[*] 跳过 packwiz refresh(dev 分支提交固定不刷新;发布时在 main 上刷新)")

    do_commit(args.message)

    # 3. 分支操作
    if args.release or args.merge:
        do_merge(args.version if args.release else None)
    elif args.tag:
        do_tag(args.tag)
    else:
        do_push_dev()


if __name__ == "__main__":
    main()
