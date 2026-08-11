#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建导入包(纯构建,不含 git 操作)

git 操作(提交/merge/tag/发布)统一用 push.py:
  python tools/push.py --release --version 1.1.0

用法:
  python tools/release.py              # 构建 mrpack 到 dist/
  python tools/release.py -o <路径>    # 指定输出路径
"""

import argparse
import json
import os
import subprocess
import sys
import zipfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED = os.path.join(ROOT, "tools", "cache", "seed.json")
BUILD_SCRIPT = os.path.join(ROOT, "tools", "build_import_pack.py")
MRPACK = os.path.join(ROOT, "dist", "modpack.mrpack")


def run(cmd, cwd=ROOT):
    print(f"> {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=cwd)
    if r.returncode != 0:
        print(f"[错误] 命令失败: {' '.join(cmd)}")
        sys.exit(1)
    return r


def main():
    ap = argparse.ArgumentParser(description="构建导入包(纯构建)")
    ap.add_argument("-o", "--output", default=MRPACK, help="输出路径")
    args = ap.parse_args()

    # 构建 mrpack
    cmd = [sys.executable, BUILD_SCRIPT, "--seed", SEED, "-o", args.output]
    run(cmd)

    # 打印产物信息
    z = zipfile.ZipFile(args.output)
    idx = json.loads(z.read("modrinth.index.json"))
    print(f"[✓] 构建完成: {args.output}")
    print(f"    大小: {os.path.getsize(args.output)//1024} KB")
    print(f"    版本: {idx['versionId']} | mods: {len(idx['files'])}")
    print()
    print("下一步(发布到玩家):")
    print("  1. python tools/push.py --release --version <版本>   # merge dev→main + tag")
    print("  2. GitHub → Releases → 附上该 mrpack → 分享到 QQ 群")


if __name__ == "__main__":
    main()
