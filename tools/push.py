#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简推送脚本 — 开发/发布分离

用法:
  python push.py              # 默认:packwiz refresh + 提交 + 推 dev
  python push.py -m "说明"    # 带提交说明
  python push.py --release    # 发布:merge dev→main + 推 main(Pages 更新,玩家可见)
  python push.py --version 1.1.0   # 发布时可选:打 tag(配合 release.py)

流程:
  开发:改代码 → python push.py(推 dev,玩家不可见)
  发布:验证 OK → python push.py --release(玩家增量更新)
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
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        print(f"[错误] git {' '.join(cmd)}: {r.stderr.strip()}")
        sys.exit(1)
    return r

def main():
    ap = argparse.ArgumentParser(description="极简推送(开发/发布分离)")
    ap.add_argument("-m", "--message", default=None, help="提交说明")
    ap.add_argument("--release", action="store_true", help="发布:merge dev→main 并推送")
    ap.add_argument("--version", default=None, help="发布时打 tag(如 1.1.0)")
    args = ap.parse_args()

    # 1. packwiz refresh(总是)
    if os.path.exists(PACKWIZ):
        run([PACKWIZ, "refresh"])
    else:
        run(["packwiz", "refresh"])

    # 2. 提交(如果有改动)
    r = git(["git", "status", "--porcelain"], check=False)
    if r.stdout.strip():
        if not args.message:
            args.message = "update: 开发更新"
        git(["git", "add", "-A"])
        git(["git", "commit", "-m", args.message])
        print(f"[*] 已提交: {args.message}")
    else:
        print("[*] 无改动,跳过提交")

    # 3. 分支选择
    if args.release:
        # 发布:从 dev 切到 main,merge,推送
        git(["git", "checkout", "main"])
        git(["git", "pull", "origin", "main"])
        git(["git", "merge", "dev", "--no-edit"])
        git(["git", "push", "origin", "main"])
        print("[✓] 已发布到 main,玩家将增量更新(1~3 分钟)")
        # 回到 dev 继续开发
        git(["git", "checkout", "dev"])

        # 可选打 tag
        if args.version:
            tag = f"v{args.version}"
            git(["git", "tag", tag])
            git(["git", "push", "origin", tag])
            print(f"[✓] 已打 tag {tag}")
    else:
        # 开发:直接推 dev
        git(["git", "push", "origin", "dev"])
        print("[✓] 已推送到 dev(玩家不可见,发布需 --release)")

if __name__ == "__main__":
    main()
