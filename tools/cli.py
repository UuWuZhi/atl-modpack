#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式总入口 — 新手友好,菜单驱动。

用法:
  python cli.py          # 双击或命令行运行,进入菜单

所有操作最终调用 tools/ 下的参数式脚本:
  - 推送到 dev        -> push.py
  - 合并到 main(发布)  -> push.py --release
  - 打 tag            -> git tag + push
  - 一站式 release    -> push.py --release --version
  - 建立/断开符号链接  -> setup_dev_link.py
  - 构建导入包        -> build_import_pack.py

参数式脚本可单独直接调用(适合熟练开发者/AI):
  python tools/push.py --release --version 1.1.0
"""

import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")


def run_py(script, args=None):
    """运行 tools/ 下的参数式脚本。"""
    cmd = [sys.executable, os.path.join(TOOLS, script)]
    if args:
        cmd += args
    print(f"\n> {' '.join(cmd)}\n")
    subprocess.run(cmd)


def main():
    while True:
        print("=" * 52)
        print("  All The Leisures 整合包工具")
        print("=" * 52)
        print("  1. 推送到 dev(开发中,玩家不可见)")
        print("  2. 发布到 main(玩家可见)")
        print("  3. 打 tag")
        print("  4. 一站式发布(release = merge + tag)")
        print("  5. 建立/断开开发符号链接")
        print("  6. 构建导入包(mrpack)")
        print("  0. 退出")
        print("-" * 52)
        choice = input("请选择: ").strip()

        if choice == "1":
            msg = input("提交说明(回车用默认): ").strip()
            args = ["-m", msg] if msg else []
            run_py("push.py", args)
        elif choice == "2":
            msg = input("发布说明(回车用默认): ").strip()
            args = ["--release"]
            if msg:
                args += ["-m", msg]
            run_py("push.py", args)
        elif choice == "3":
            ver = input("版本号(如 1.1.0): ").strip()
            if ver:
                run_py("push.py", ["--tag", ver])
            else:
                print("已取消。")
        elif choice == "4":
            ver = input("版本号(如 1.1.0): ").strip()
            msg = input("发布说明(回车用默认): ").strip()
            args = ["--release"]
            if ver:
                args += ["--version", ver]
            if msg:
                args += ["-m", msg]
            run_py("push.py", args)
        elif choice == "5":
            run_py("setup_dev_link.py")
        elif choice == "6":
            run_py("build_import_pack.py", ["--seed", os.path.join(TOOLS, "cache", "seed.json"),
                                            "-o", os.path.join(ROOT, "dist", "modpack.mrpack")])
        elif choice == "0":
            print("再见。")
            break
        else:
            print("无效选择。")

        print()
        input("按回车继续...")
        print()


if __name__ == "__main__":
    main()
