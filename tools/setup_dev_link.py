#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发者符号链接工具 — 打通工作区与开发实例

作用:把 开发实例 的 kubejs/scripts 链接到 工作区
     让"在实例里改脚本" == "改工作区文件",避免手动复制。

注意:默认不链接 config —— 游戏运行会大量改写 config(默认值、线程数等),
     链接会导致运行时污染工作区。需要时用 --link 手动指定。

参数式用法:
  python setup_dev_link.py <工作区> <实例>                    建立(kubejs,scripts)
  python setup_dev_link.py <工作区> <实例> --link kubejs      只链 kubejs
  python setup_dev_link.py --remove <实例>                    断开
  python setup_dev_link.py --remove <实例> --link config      断开 config

交互式用法(无参数):
  python setup_dev_link.py
"""

import argparse
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 默认链接目录:config 不链接(游戏运行会大量改写 config,污染工作区)
DEFAULT_LINKS = ["kubejs", "scripts"]


def is_junction(path):
    """检查 path 是否是 junction(Windows)。"""
    try:
        r = subprocess.run(
            ["fsutil", "reparsepoint", "query", path],
            capture_output=True,
        )
        return r.returncode == 0
    except Exception:
        return False


def make_junction(link_path, target):
    """建立 junction。mklink /J 不需要管理员权限。"""
    r = subprocess.run(
        ["cmd", "/c", "mklink", "/J", link_path, target],
        capture_output=True,
    )
    return r.returncode == 0


def remove_junction(link_path):
    """移除 junction(rmdir 只删链接,不删目标)。"""
    subprocess.run(["rmdir", link_path], capture_output=True)


def link_dir(workspace, instance, name):
    """为一个目录建链。返回 (成功?, 消息)。"""
    ws_dir = os.path.join(workspace, name)
    inst_dir = os.path.join(instance, name)

    if not os.path.isdir(ws_dir):
        return False, f"工作区缺少目录 {name}(跳过)"

    # 若实例已有真实目录,备份
    if os.path.exists(inst_dir) and not is_junction(inst_dir):
        bak = inst_dir + ".bak"
        if not os.path.exists(bak):
            os.rename(inst_dir, bak)
            print(f"  [*] 已备份实例的 {name} -> {name}.bak")
        else:
            print(f"  [*] 实例的 {name} 已是备份状态,跳过备份")

    # 建立 junction
    if os.path.isdir(inst_dir) and is_junction(inst_dir):
        return True, f"{name} 已是链接,跳过"
    if make_junction(inst_dir, ws_dir):
        return True, f"{name} 已链接 -> 工作区"
    else:
        return False, f"{name} 链接失败(目标可能被占用)"


def unlink_dir(instance, name):
    """断开一个目录的链接。"""
    inst_dir = os.path.join(instance, name)
    if not os.path.exists(inst_dir):
        return f"{name} 不存在,跳过"
    if not is_junction(inst_dir):
        return f"{name} 是真实目录,跳过"
    remove_junction(inst_dir)
    # 恢复备份
    bak = inst_dir + ".bak"
    if os.path.exists(bak):
        os.rename(bak, inst_dir)
        return f"{name} 链接已断开,并恢复备份"
    return f"{name} 链接已断开"


def interactive(workspace=None, instance=None, links=None):
    """交互式模式。"""
    print("=" * 50)
    print(" 开发者符号链接设置")
    print("=" * 50)

    if not workspace:
        workspace = input("工作区路径(如 D:\\Code\\atl-modpack): ").strip().strip('"')
    if not instance:
        instance = input("开发实例路径(如 D:\\Minecraft\\.minecraft\\versions\\All The Leisures v1.0.1b): ").strip().strip('"')
    if not links:
        links = DEFAULT_LINKS

    if not os.path.isdir(workspace):
        print(f"[错误] 工作区不存在: {workspace}")
        return
    if not os.path.isdir(instance):
        print(f"[错误] 实例不存在: {instance}")
        return

    print(f"\n工作区: {workspace}")
    print(f"实例:   {instance}")
    print(f"将链接: {', '.join(links)}")
    print()
    action = input("建立链接输入 1,断开输入 2,取消直接回车: ").strip()

    if action == "1":
        print("\n[建立链接]")
        for name in links:
            ok, msg = link_dir(workspace, instance, name)
            print(f"  [{'✓' if ok else '✗'}] {msg}")
        print("\n[完成] 在实例里改脚本 = 改工作区文件,git 立即可见。")
    elif action == "2":
        print("\n[断开链接]")
        for name in links:
            msg = unlink_dir(instance, name)
            print(f"  [✓] {msg}")
        print("\n[完成] 已断开链接。")
    else:
        print("已取消。")
    print()


def main():
    ap = argparse.ArgumentParser(description="开发者符号链接工具")
    ap.add_argument("workspace", nargs="?", help="工作区路径(建立时必需)")
    ap.add_argument("instance", nargs="?", help="开发实例路径")
    ap.add_argument("--remove", action="store_true", help="断开链接模式")
    ap.add_argument("--link", default=",".join(DEFAULT_LINKS), help="要链接的目录,逗号分隔")
    args = ap.parse_args()

    links = [x.strip() for x in args.link.split(",") if x.strip()]

    # 交互式(无参数)
    if not args.workspace and not args.instance:
        interactive(links=links)
        return

    # 断开模式:位置参数是实例路径(argparse 会放到 workspace)
    if args.remove:
        instance = args.instance or args.workspace
        if not instance:
            ap.print_help()
            return
        print("[断开链接]")
        for name in links:
            msg = unlink_dir(instance, name)
            print(f"  [✓] {msg}")
        return

    # 建立模式:需要 workspace + instance
    if not args.workspace or not args.instance:
        ap.print_help()
        return
    if not os.path.isdir(args.workspace):
        print(f"[错误] 工作区不存在: {args.workspace}")
        return
    if not os.path.isdir(args.instance):
        print(f"[错误] 实例不存在: {args.instance}")
        return
    print("[建立链接]")
    for name in links:
        ok, msg = link_dir(args.workspace, args.instance, name)
        print(f"  [{'OK' if ok else 'FAIL'}] {msg}")


if __name__ == "__main__":
    main()
