#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
构建 + 发布导入包

流程:
1. packwiz refresh(更新 index)
2. 构建 modpack.mrpack
3. 打 git tag(可选)
4. 推送 tag + 提示创建 GitHub Release

用法:
  python tools/release.py <版本号>      # 例: python tools/release.py 1.1.0
  python tools/release.py --no-tag     # 只构建不打 tag

注意:需要 packwiz CLI 在 tools/packwiz-cli/packwiz.exe 或 PATH
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
PACKWIZ = os.path.join(ROOT, "tools", "packwiz-cli", "packwiz.exe")
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

def git(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)

def main():
    ap = argparse.ArgumentParser(description="构建并发布导入包")
    ap.add_argument("version", nargs="?", default=None, help="版本号(如 1.1.0),会打 tag")
    ap.add_argument("--no-tag", action="store_true", help="只构建,不打 tag 不发布")
    args = ap.parse_args()

    # 1. 校验工作区干净(有版本号时)
    if args.version and not args.no_tag:
        r = git(["git", "status", "--porcelain"])
        if r.stdout.strip():
            print("[警告] 工作区有未提交改动。发布前建议先提交。")

    # 2. packwiz refresh
    if os.path.exists(PACKWIZ):
        run([PACKWIZ, "refresh"])
    else:
        run(["packwiz", "refresh"])

    # 3. 构建 mrpack
    cmd = [sys.executable, BUILD_SCRIPT, "--seed", SEED, "-o", MRPACK]
    if args.version:
        cmd += ["--version", args.version]
    run(cmd)

    # 4. 打印产物信息
    z = zipfile.ZipFile(MRPACK)
    print(f"[✓] 构建完成: {MRPACK}")
    print(f"    大小: {os.path.getsize(MRPACK)//1024} KB")
    idx = json.loads(z.read("modrinth.index.json"))
    print(f"    版本: {idx['versionId']} | mods: {len(idx['files'])}")

    # 5. 打 tag(可选)
    if args.version and not args.no_tag:
        print(f"[*] 打 tag v{args.version} ...")
        git(["git", "add", "-A"])
        git(["git", "commit", "-m", f"release: v{args.version}", "--allow-empty"])
        r = git(["git", "tag", f"v{args.version}"])
        if r.returncode != 0:
            print(f"[错误] 打 tag 失败: {r.stderr.strip()}")
            sys.exit(1)
        git(["git", "push"])
        git(["git", "push", "--tags"])
        print()
        print("=" * 60)
        print(f"[✓] 已推送 tag v{args.version}")
        print(f"    下一步:在 GitHub 网页创建 Release 并附加:")
        print(f"      {MRPACK}")
        print(f"    或命令行: gh release create v{args.version} {MRPACK} --title 'v{args.version}'")
        print("=" * 60)

if __name__ == "__main__":
    main()
