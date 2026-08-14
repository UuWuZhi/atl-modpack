#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式添加 Mod。

流程:
  1. 选择来源(Modrinth / CurseForge)
  2. 输入 slug / URL / 搜索词
  3. 运行 packwiz 生成 .pw.toml
  4. 选择主条目并设置 side
  5. 自动 packwiz refresh
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

from packwiz_lf_guard import ensure_lf_before_refresh

try:
    import tomllib
except ImportError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
PACKWIZ_EXE = ROOT / "tools" / "packwiz-cli" / "packwiz.exe"
MODS_DIR = ROOT / "mods"


def resolve_packwiz():
    if PACKWIZ_EXE.exists():
        return [str(PACKWIZ_EXE)]
    if shutil.which("packwiz"):
        return ["packwiz"]
    raise FileNotFoundError("找不到 packwiz.exe,也找不到 PATH 中的 packwiz 命令")


def run(cmd):
    print(f"> {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(r.returncode)


def snapshot_metadata():
    state = {}
    if not MODS_DIR.is_dir():
        return state
    for path in MODS_DIR.glob("*.pw.toml"):
        state[path] = path.stat().st_mtime_ns
    return state


def detect_changed_metadata(before):
    changed = []
    if not MODS_DIR.is_dir():
        return changed
    for path in MODS_DIR.glob("*.pw.toml"):
        stamp = path.stat().st_mtime_ns
        if path not in before or before[path] != stamp:
            changed.append(path)
    return sorted(changed)


def read_meta(path):
    with path.open("rb") as fh:
        return tomllib.load(fh)


def format_candidate(path):
    try:
        meta = read_meta(path)
    except Exception:
        return str(path.relative_to(ROOT))
    name = meta.get("name", path.stem)
    filename = meta.get("filename", "")
    side = meta.get("side", "both")
    extra = f" | {filename}" if filename else ""
    return f"{path.relative_to(ROOT)} | {name}{extra} | side={side}"


def pick_candidate(paths):
    if len(paths) == 1:
        print(f"已检测到新条目: {format_candidate(paths[0])}")
        return paths[0]

    print("\n检测到多个可能的新增/变更条目,请选择主 mod:")
    for idx, path in enumerate(paths, 1):
        print(f"  {idx}. {format_candidate(path)}")

    while True:
        choice = input("选择序号(回车取消): ").strip()
        if not choice:
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(paths):
            return paths[int(choice) - 1]
        print("无效选择。")


def set_side(path, side):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    side_line = f'side = "{side}"'

    for idx, line in enumerate(lines):
        if line.strip().startswith("side = "):
            lines[idx] = side_line
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return

    insert_at = len(lines)
    for idx, line in enumerate(lines):
        if line.startswith("["):
            insert_at = idx
            break

    lines.insert(insert_at, side_line)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def refresh():
    print("\n刷新 packwiz 索引 ...")
    ensure_lf_before_refresh()
    run(resolve_packwiz() + ["refresh"])


def choose_side():
    print("\n设置 side:")
    print("  1. both(客户端 + 服务器)")
    print("  2. client(仅客户端)")
    print("  3. server(仅服务器)")
    print("  0. 跳过")

    mapping = {"1": "both", "2": "client", "3": "server"}
    while True:
        choice = input("请选择: ").strip()
        if choice == "0" or choice == "":
            return None
        if choice in mapping:
            return mapping[choice]
        print("无效选择。")


def append_curseforge_add_args(cmd, query, category=None, game=None):
    cmd += ["curseforge", "add"]
    if query.isdigit():
        cmd += ["--addon-id", query]
    if category:
        cmd += ["--category", category]
    if game:
        cmd += ["--game", game]
    if not query.isdigit():
        cmd.append(query)
    return cmd


def add_with_packwiz():
    print("=" * 52)
    print("  交互式 Mod 添加")
    print("=" * 52)

    print("来源:")
    print("  1. Modrinth")
    print("  2. CurseForge")
    print("  0. 退出")
    source = input("请选择: ").strip()
    if source == "0" or source == "":
        print("已取消。")
        return
    if source not in {"1", "2"}:
        print("无效选择。")
        return

    query = input("输入 URL / slug / 搜索词: ").strip().strip('"')
    if not query:
        print("已取消。")
        return

    before = snapshot_metadata()
    cmd = resolve_packwiz()
    if source == "1":
        cmd += ["modrinth", "add", query]
    else:
        category = input("CurseForge category(回车默认 mods): ").strip()
        game = input("CurseForge game(回车默认 minecraft): ").strip()
        cmd = append_curseforge_add_args(cmd, query, category, game)

    print()
    run(cmd)

    changed = detect_changed_metadata(before)
    if not changed:
        print("\n未检测到新增的 .pw.toml 文件,跳过 side 设置。")
        refresh()
        return

    target = pick_candidate(changed)
    if target:
        side = choose_side()
        if side:
            set_side(target, side)
            print(f"\n已更新 {target.relative_to(ROOT)} 的 side = \"{side}\"")

    refresh()
    print("完成。")


def main():
    add_with_packwiz()


if __name__ == "__main__":
    main()
