#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式管理外部资源(Mod / Resourcepack)。

外部资源指由 packwiz 通过 Modrinth / CurseForge / 直链追踪的文件:
  - 添加: 生成 .pw.toml 元数据,不把第三方 jar/zip 放进仓库/Pages
  - 移除: 删除 .pw.toml 元数据,并删除工作区中同名落地文件
  - 每次变更后自动 packwiz refresh
"""

import shutil
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib


sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
PACKWIZ_EXE = ROOT / "tools" / "packwiz-cli" / "packwiz.exe"
RESOURCE_KINDS = {
    "1": ("Mod", ROOT / "mods", "mods", "both"),
    "2": ("Resourcepack", ROOT / "resourcepacks", "resourcepacks", "client"),
}


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


def read_meta(path):
    with path.open("rb") as fh:
        return tomllib.load(fh)


def metadata_paths(folder):
    if not folder.is_dir():
        return []
    return sorted(folder.glob("*.pw.toml"))


def snapshot_metadata(folder):
    return {path: path.stat().st_mtime_ns for path in metadata_paths(folder)}


def detect_changed_metadata(folder, before):
    changed = []
    for path in metadata_paths(folder):
        stamp = path.stat().st_mtime_ns
        if path not in before or before[path] != stamp:
            changed.append(path)
    return sorted(changed)


def source_of(meta):
    update = meta.get("update", {})
    if "modrinth" in update:
        return "Modrinth"
    if "curseforge" in update:
        return "CurseForge"
    return "Direct URL"


def format_candidate(path):
    try:
        meta = read_meta(path)
    except Exception:
        return str(path.relative_to(ROOT))
    name = meta.get("name", path.stem)
    filename = meta.get("filename", "")
    side = meta.get("side", "both")
    source = source_of(meta)
    extra = f" | {filename}" if filename else ""
    return f"{path.relative_to(ROOT)} | {name}{extra} | {source} | side={side}"


def pick_candidate(paths, prompt):
    if not paths:
        return None
    if len(paths) == 1:
        print(f"已选择: {format_candidate(paths[0])}")
        return paths[0]

    print()
    for idx, path in enumerate(paths, 1):
        print(f"  {idx}. {format_candidate(path)}")

    while True:
        choice = input(prompt).strip()
        if not choice:
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(paths):
            return paths[int(choice) - 1]
        print("无效选择。")


def set_side(path, side):
    text = path.read_text(encoding="utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines()
    side_line = f'side = "{side}"'

    for idx, line in enumerate(lines):
        if line.strip().startswith("side = "):
            lines[idx] = side_line
            path.write_text(newline.join(lines) + newline, encoding="utf-8")
            return

    insert_at = len(lines)
    for idx, line in enumerate(lines):
        if line.startswith("["):
            insert_at = idx
            break

    lines.insert(insert_at, side_line)
    path.write_text(newline.join(lines) + newline, encoding="utf-8")


def choose_side(default_side):
    print("\n设置 side:")
    print("  1. both(客户端 + 服务器)")
    print("  2. client(仅客户端)")
    print("  3. server(仅服务器)")
    print(f"  0. 使用默认({default_side})")

    mapping = {"1": "both", "2": "client", "3": "server"}
    while True:
        choice = input("请选择: ").strip()
        if choice == "0" or choice == "":
            return default_side
        if choice in mapping:
            return mapping[choice]
        print("无效选择。")


def confirm_warning(lines):
    print("\n警告:")
    for line in lines:
        print(f"  - {line}")
    answer = input("确认继续? 输入 YES: ").strip()
    return answer == "YES"


def choose_kind():
    print("\n资源类型:")
    print("  1. Mod")
    print("  2. Resourcepack")
    print("  0. 返回")
    choice = input("请选择: ").strip()
    if choice in RESOURCE_KINDS:
        return RESOURCE_KINDS[choice]
    if choice == "0" or choice == "":
        return None
    print("无效选择。")
    return None


def choose_source():
    print("\n来源:")
    print("  1. Modrinth")
    print("  2. CurseForge")
    print("  3. 直链 URL")
    print("  0. 返回")
    choice = input("请选择: ").strip()
    if choice in {"1", "2", "3"}:
        return choice
    if choice == "0" or choice == "":
        return None
    print("无效选择。")
    return None


def add_resource():
    kind = choose_kind()
    if not kind:
        print("已取消。")
        return
    kind_name, folder, meta_folder, default_side = kind

    source = choose_source()
    if not source:
        print("已取消。")
        return

    warnings = [
        "这是第三方外部资源,只应提交 packwiz 元数据;不要把非原创 jar/zip 提交进仓库或 Pages。",
        "资源可用性、许可和下架风险由原站点/作者决定,维护人需要自行确认分发许可。",
    ]
    if source == "3":
        warnings.append("直链 URL 通常没有依赖解析和自动更新信息;优先使用 Modrinth/CurseForge 条目。")
    if not confirm_warning(warnings):
        print("已取消。")
        return

    before = snapshot_metadata(folder)
    cmd = resolve_packwiz()
    if source == "1":
        query = input("输入 Modrinth URL / slug / 项目 ID / 搜索词: ").strip().strip('"')
        if not query:
            print("已取消。")
            return
        cmd += ["--meta-folder", meta_folder, "modrinth", "add", query]
    elif source == "2":
        query = input("输入 CurseForge URL / slug / ID / 搜索词: ").strip().strip('"')
        if not query:
            print("已取消。")
            return
        default_category = "mc-mods" if kind_name == "Mod" else "texture-packs"
        category = input(f"CurseForge category(回车默认 {default_category}): ").strip() or default_category
        game = input("CurseForge game(回车默认 minecraft): ").strip()
        cmd += ["--meta-folder", meta_folder, "curseforge", "add", "--category", category]
        if game:
            cmd += ["--game", game]
        cmd.append(query)
    else:
        name = input("资源显示名称: ").strip()
        url = input("直接下载 URL: ").strip().strip('"')
        if not name or not url:
            print("已取消。")
            return
        meta_name = input("元数据文件名(可选,不含 .pw.toml): ").strip()
        cmd += ["--meta-folder", meta_folder, "url", "add", name, url]
        if meta_name:
            cmd += ["--meta-name", meta_name]

    print()
    run(cmd)

    changed = detect_changed_metadata(folder, before)
    if not changed:
        print("\n未检测到新增/变更的 .pw.toml 文件,仍将刷新索引。")
        refresh()
        return

    target = pick_candidate(changed, "选择主条目(回车跳过 side 设置): ")
    if target:
        side = choose_side(default_side)
        set_side(target, side)
        print(f"\n已更新 {target.relative_to(ROOT)} 的 side = \"{side}\"")

    refresh()
    print("完成。")


def find_resources(folder, keyword):
    keyword = keyword.casefold()
    matches = []
    for path in metadata_paths(folder):
        haystack = str(path.name)
        try:
            meta = read_meta(path)
            haystack += f" {meta.get('name', '')} {meta.get('filename', '')}"
        except Exception:
            pass
        if keyword in haystack.casefold():
            matches.append(path)
    return matches


def remove_resource():
    kind = choose_kind()
    if not kind:
        print("已取消。")
        return
    kind_name, folder, _meta_folder, _default_side = kind

    resources = metadata_paths(folder)
    if not resources:
        print(f"{kind_name} 没有可移除的外部资源元数据。")
        return

    keyword = input("输入名称/文件名关键词筛选(回车显示全部): ").strip()
    matches = find_resources(folder, keyword) if keyword else resources
    if not matches:
        print("未找到匹配条目。")
        return

    target = pick_candidate(matches, "选择要移除的条目(回车取消): ")
    if not target:
        print("已取消。")
        return

    try:
        meta = read_meta(target)
    except Exception:
        meta = {}
    filename = meta.get("filename")
    payload = target.parent / filename if filename else None

    print("\n将移除:")
    print(f"  - 元数据: {target.relative_to(ROOT)}")
    if payload and payload.exists():
        print(f"  - 工作区文件: {payload.relative_to(ROOT)}")
    elif filename:
        print(f"  - 工作区文件: {target.parent.relative_to(ROOT) / filename}(当前不存在)")

    if not confirm_warning([
        "移除后该资源不再被 packwiz 追踪,玩家后续更新不会再下载它。",
        "如果工作区存在同名 jar/zip,会同时删除以满足“不存在于工作区”。",
    ]):
        print("已取消。")
        return

    target.unlink()
    print(f"已删除 {target.relative_to(ROOT)}")
    if payload and payload.exists():
        payload.unlink()
        print(f"已删除 {payload.relative_to(ROOT)}")

    refresh()
    print("完成。")


def refresh():
    print("\n刷新 packwiz 索引 ...")
    run(resolve_packwiz() + ["refresh"])


def main():
    while True:
        print("=" * 52)
        print("  外部资源管理(Mod / Resourcepack)")
        print("=" * 52)
        print("  1. 添加外部资源")
        print("  2. 移除外部资源")
        print("  0. 返回")
        print("-" * 52)
        choice = input("请选择: ").strip()

        if choice == "1":
            add_resource()
        elif choice == "2":
            remove_resource()
        elif choice == "0" or choice == "":
            print("已返回。")
            break
        else:
            print("无效选择。")

        print()
        input("按回车继续...")
        print()


if __name__ == "__main__":
    main()
