#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简推送/发布脚本 — 开发/发布分离

参数式用法(熟练开发者/AI):
  python push.py                     # refresh + 提交 + 推 dev
  python push.py -m "说明"            # 带提交说明
  python push.py --merge             # 合并 dev→main 并推送(发布,不打 tag)
  python push.py --tag 1.1.0         # 打 tag(不合并)
  python push.py --release           # 一站式发布:合并 dev→main
  python push.py --release --version 1.1.0   # 发布 + 打 tag

流程:
  开发:改代码 → python push.py(推 dev,玩家不可见)
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
    """packwiz refresh(总是)"""
    if os.path.exists(PACKWIZ):
        run([PACKWIZ, "refresh"])
    else:
        run(["packwiz", "refresh"])


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
    ap.add_argument("--merge", action="store_true", help="合并 dev→main 并推送(发布)")
    ap.add_argument("--tag", default=None, metavar="VER", help="打 tag(如 1.1.0),不合并")
    ap.add_argument("--release", action="store_true", help="一站式发布:合并 dev→main")
    ap.add_argument("--version", default=None, help="配合 --release 打 tag")
    args = ap.parse_args()

    # 模式互斥校验
    if sum([args.merge, args.release, bool(args.tag)]) > 1:
        print("[错误] --merge / --release / --tag 只能选一个")
        sys.exit(1)

    # 1. refresh + 提交(总是,除了纯 tag 模式可跳过提交)
    do_refresh()
    do_commit(args.message)

    # 2. 分支操作
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
